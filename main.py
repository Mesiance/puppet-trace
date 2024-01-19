import cProfile
from puppet_trace import PuppetClassTrace
from args import GetArgs
from out import OutputFormatter

parser = GetArgs().parser()
args = parser.parse_args()
class_name_to_find = args.classname
puppet_code_dir = args.puppet_code_dir


def main():
    puppetClassTraceObject = PuppetClassTrace(puppet_code_dir)
    output = puppetClassTraceObject.createIncludesTree(class_name_to_find)
    prettifyOutput = OutputFormatter(output)
    prettifyOutput.output(output)


if __name__ == "__main__":
    main()
    # cProfile.run("main()")
