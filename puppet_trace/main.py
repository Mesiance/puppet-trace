import cProfile
from puppet_trace.puppet_trace import PuppetClassTrace
from puppet_trace.args import *
from puppet_trace.out import OutputFormatter


def main():
    parser = GetArgs().parseArgs()
    args = parser.parse_args()
    root_class = args.classname
    class_to_seek = args.class_seek
    puppet_code_dir = args.puppet_code_dir
    format = args.format
    env_file = args.env_file

    puppetClassTraceObject = PuppetClassTrace(puppet_code_dir)
    outputTree = puppetClassTraceObject.createIncludesTree(root_class)
    if class_to_seek:
        outputTree = puppetClassTraceObject.classSeek(outputTree, class_to_seek)
        index = 1
        if not outputTree:
            print(
                f'Class "{class_to_seek}" not found in includes tree of "{root_class}"'
            )
            exit(0)
        print(f"Found {len(outputTree)} matches for {class_to_seek}\n")
        for path in outputTree:
            print(f"{str(index)}: {path}")
            index += 1
    else:
        prettifyOutput = OutputFormatter(outputTree)
        prettifyOutput.getClassGraph(format)


if __name__ == "__main__":
    main()
    # cProfile.run("main()")
