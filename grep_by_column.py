import os,argparse


def grep_by_column(file1, file2, col1, col2, sep = '\t'):
    dic = {}
    with open(file2, "r") as query:
        for line in query:
            dic[line.rstrip()[col2-1]] = ''
    with open(file1, "r") as input:
        for line in input:
            if line.split(sep)[col1-1] in dic:
                print(line.rstrip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="subset a file by a list")
    parser.add_argument("-1", "--input1", required=True, type=str, help="big file")
    parser.add_argument("-2", "--input2", required=True, type=str, help="query list")
    parser.add_argument("-i", "--col1", required=True, type=int, help="column number of in big file")
    parser.add_argument("-j", "--col2", required=True, type=int, help="column number of in big file")
    parser.add_argument("-f", "--sep", required=False, type=str, help="field delimiter, default is tab")

    Args = parser.parse_args()

    grep_by_column(Args.input1, Args.input2, Args.col1, Args.col2, Args.sep)
