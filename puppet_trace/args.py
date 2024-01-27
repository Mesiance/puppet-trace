import argparse
import os
from dotenv import load_dotenv


class GetArgs:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog="puppet-tracer",
            description="This tool can be handy in case when you have a realy huge \
            puppet manifests base and serching for puppet class calls(includes) becomes to pain.",
        )

    def _getEnvFile():
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-e",
            "--env-file",
            type=str,
            help="Path to the .env file with environment variables.",
            metavar="<path to env file>",
            dest="env_file",
        )
        args, _ = parser.parse_known_args()
        return args

    env = _getEnvFile()
    if hasattr(env, 'env_file') and env.env_file:
        load_dotenv(dotenv_path=env.env_file)

    def parseArgs(self):
        self.parser.add_argument(
            "-e",
            "--env-file",
            type=str,
            help=f"Environments file. You can set it for some permanent params like path to puppet manifests directory.",
            metavar="<path to env file>",
            dest="env_file",
        )

        self.parser.add_argument(
            "-s",
            "--seek",
            type=str,
            help="Seek the class in includes tree of onother class.\
                            Specify here class name that will be seeked.",
            metavar="<class to seek>",
            dest="class_seek",
        )

        self.parser.add_argument(
            "-p",
            "--path",
            type=str,
            default = os.getenv("PUPPET_CODE_DIR", os.getcwd()),
            help="Path to puppet manifests directory. Default: your current directory",
            metavar="<path to manifests dir>",
            dest="puppet_code_dir",
        )

        availableFormats = ["tree", "json", "yaml"]
        self.parser.add_argument(
            "--format",
            type=str,
            default = os.getenv("FORMAT", "tree"),
            choices=availableFormats,
            help=f"Output format. Available options {str(availableFormats)}",
            metavar="<format>",
            dest="format",
        )

        self.parser.add_argument("classname", default=None, metavar="class name")

        return self.parser
