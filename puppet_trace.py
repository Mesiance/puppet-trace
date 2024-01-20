import os
import re


class PuppetClassTrace:
    def __init__(self, puppet_repo_path) -> None:
        self.puppet_repo_path = puppet_repo_path
        self.includes_tree = {}

    def _getModuleFiles(self, classname) -> dict:
        pp_files = []
        path = self.puppet_repo_path

        # If classname is empty for some reasons just return empty list
        if not classname:
            return pp_files
        elif classname[0] == ":":
            classname = classname.lstrip(":")

        if path[-1] == "/":
            path = path.rstrip(path[-1]) + "/modules"
        else:
            path += "/modules"

        path += f"/{classname.split('::')[0]}/manifests"

        for dirpath, dirnames, files in os.walk(path):
            for file in files:
                if file.endswith(".pp"):
                    full_path = os.path.join(dirpath, file)
                    pp_files.append(full_path)

        if not pp_files:
            print(
                "No one .pp files found. Maybe you forgot about --path argument?\
                \nType -h or --help to get more details"
            )
            exit(1)
        return pp_files

    def _findClassFile(self, class_name):
        class_pattern = re.compile(r"class\s+([a-zA-Z:_\d]+)\s*[{(]")
        pp_files = self._getModuleFiles(class_name)

        for file in pp_files:
            with open(file, "r") as pp_file:
                for line in pp_file:
                    match = class_pattern.match(line)
                    if match and (match.group(1) == class_name):
                        return file
        # Добавить эксепшн с сообщением если файл не найден
        return None

    def _getIncludes(self, class_name) -> list:
        classes = []
        classes_dict = {}
        current_class = None

        pp_file_path = self._findClassFile(class_name)
        class_pattern_str = f"class\\s+({re.escape(class_name)})\\s*[{{(]"

        class_pattern = re.compile(rf"{class_pattern_str}")
        # define_pattern = re.compile(r"define\s+([a-zA-Z:_\d]+)\s*[{(]")
        include_pattern = re.compile(r"^(?!.*#.*include).*include ([\w::]*)")
        close_bracket_pattern = re.compile(r"((?<! |\w|}|#|:)})")
        crutch_pattern = re.compile(r"(?<=\n)\) ({)")

        try:
            if not pp_file_path:
                return classes

            with open(pp_file_path, "r") as pp_file:
                close_bracket_found = False
                for line in pp_file:
                    class_match = class_pattern.match(line)
                    include_match = include_pattern.search(line)
                    close_bracket_match = close_bracket_pattern.search(line)
                    # define_match = define_pattern.search(line)
                    crutch_match = crutch_pattern.search(line)

                    if (
                        class_match
                    ):  # If searching class match, create empty dict with class name as a key
                        current_class = class_match.group(1)
                        classes_dict[current_class] = []
                    elif (
                        include_match and current_class
                    ):  # Add to current_class dict met class includes match and current_class dict exists
                        included_class = include_match.group(1)
                        classes_dict[current_class].append(included_class)
                    elif crutch_match and close_bracket_match:  # Kostyl'
                        break
                    elif close_bracket_match and classes_dict:
                        close_bracket_found = True
                        break
                    else:
                        pass

            if (
                classes_dict
                and close_bracket_found
                and len(classes_dict[class_name]) > 0
            ):
                classes = classes_dict[class_name]
            else:
                classes = []

        except Exception as error:
            raise SystemError(
                f"Error while reading file {pp_file_path}\n{repr(error)}"
            ) from error
        return classes

    def _recursiveSearch(self, includes: dict):
        # Iterate over current layer includes dictionary
        for pup_class in includes.keys():
            # If key exists and is list, try to get includes for this class and dive into it recursively
            if includes[pup_class] and isinstance(includes[pup_class], list):
                subincludes = {}
                for classname in includes[pup_class]:
                    subincludes[classname] = self._getIncludes(classname)

                includes[pup_class] = subincludes
                self._recursiveSearch(subincludes)
            # If current key is dict dive into it recursively
            elif includes[pup_class] and isinstance(includes[pup_class], dict):
                self._recursiveSearch(includes[pup_class])
            # In the end just pass
            else:
                pass
        return includes

    def createIncludesTree(self, class_name):
        self.includes_tree[class_name] = self._getIncludes(
            class_name
        )  # Get depth 1 includes
        final_includes_tree = self._recursiveSearch(
            self.includes_tree
        )  # Sarch for other includes
        return final_includes_tree

    def classSeek(
        self, classTree: dict, targetClass, classChain=None, classChains=None
    ):
        if classChain is None:
            classChain = []
        if classChains is None:
            classChains = []

        # Run loop over class tree
        for key, value in classTree.items():
            # Add key to current path
            current_path = classChain + [key]

            # If key = target class then add path to paths list
            if key == targetClass:
                classChains.append(" => ".join(current_path))

            # If dict then run recursive to it
            if isinstance(value, dict):
                self.classSeek(value, targetClass, current_path, classChains)
        return classChains
