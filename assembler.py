import re
import sys
import os
from os.path import isfile, join

# Regex Expressions:

COMMENT = "\s*\/\/.*"
WHITESPACES = "\s*$"
COMMENT_END_LINE = "((^(?!(\s*\/\/))).*)(\/\/).*"
SYMBOL = "\s*\(.*\)\s*"


class Assembler:

    def __init__(self):
        self.symbols = dict()
        self.initialize_symbol_table(self.symbols)

        self.files = dict()
        self.check_files()

    def check_files(self):
        # Check if directory:
        arg = sys.argv[1]
        if os.path.isdir(arg):
            # Take all files out of it:
            self.files = {arg + "\\" + f:[] for f in os.listdir(arg) if isfile(join(arg, f))}
        elif os.path.isfile(arg):
            self.files[arg] = []
        for file in self.files.keys():
            self.parse_file(arg)

    def parse_file(self,file:str):
        lines = open(file, "r")
        for _ in lines:
            self.files[file].append(lines.readline())
        print(self.files)


    # @24 //this is a comment

    def is_ignored(self,line:str):
        """

        :param line:
        :return:
        """
        return True if (re.match(COMMENT,line) or re.match(WHITESPACES,line)) else False

    def is_comment_at_end(self,line: str):
        """

        :param line:
        :return:
        """
        return True if re.match(COMMENT_END_LINE, line) else False

    def remove_comment_at_end(self,line:str):
        """

        :param line:
        :return:
        """
        print(re.match(COMMENT_END_LINE, line).group(1))

    def test_regexes(self,line:str):
        return True if re.match(SYMBOL, line) else False



    def initialize_symbol_table(self,symbols:dict):
        for i in range(15):
            symbols["R" + str(i)] = i
        symbols["SCREEN"] = 16384
        symbols["KBD"] = 24576
        symbols["SP"] = 0
        symbols["LCL"] = 1
        symbols["ARG"] = 2
        symbols["THIS"] = 3
        symbols["THAT"] = 4


    def first_pass(self,line:str):
        # if re.match(SYMBOL, line):
        pass



    def translate(self):
        # self.first_pass(line)
        pass





if __name__ == '__main__':
    a = Assembler()






# Tests:
# print(is_comment_at_end("  guyguy // oijoi  "))
# remove_comment_at_end("  uyguyg // oijoi  ")
# print(test_regexes("   (rgrg)   "))
