import argparse
import os


class GetArgs:
    def __init__(self) -> None:
        pass

    def parser(self):
        parser = argparse.ArgumentParser(
            prog="puppet-tracer",
            description="This tool can be handy in case when you have a realy huge \
            puppet manifests base and serching for puppet class calls(includes) becomes to pain.",
        )

        parser.add_argument(
            "-s",
            "--class-seek",
            type=str,
            help="Seek the class in includes tree of onother class.\
                            Specify here class name that will be seeked.",
            metavar="<class to seek>",
            dest="class_seek",
        )

        parser.add_argument(
            "-p",
            "--path",
            type=str,
            default=os.getcwd(),
            help="Path to puppet manifests directory. Default: your current directory",
            metavar="<path to manifests dir>",
            dest="puppet_code_dir",
        )

        parser.add_argument("classname", default=None, metavar="class name")

        return parser
