import os
import re
import sys
from os.path import isfile, join

# Regex Expressions:

COMMENT = "\s*\/\/.*"
WHITESPACES = "\s*$"
COMMENT_END_LINE = "((^(?!(\s*\/\/))).*)(\/\/).*"
SYMBOL = "\s*\(.*\)\s*"


class Assembler:

    def __init__(self):

        self.files = dict()
        self.parse_args()
        # {files : [code_lines]}
        # {files: {symbols}}
        self.symbols = dict()
        self.initialize_symbols()


    def parse_args(self):
        # Check if directory:
        arg = sys.argv[1]
        if os.path.isdir(arg):
            # Take all files out of it:
            self.files = {arg + "\\" + f: [] for f in os.listdir(arg) if
                          isfile(join(arg, f))}
        elif os.path.isfile(arg):
            self.files[arg] = []
        for file in self.files.keys():
            self.parse_file(file)

    def parse_file(self, file: str):
        lines = open(file, "r")
        for line in lines:
            # Remove comment lines, empty lines and comments:
            if self.is_ignored(line):
                continue
            if self.is_comment_at_end(line):
                line = self.remove_comment_at_end(line)
            self.files[file].append(line)


    def is_ignored(self, line: str):
        """

        :param line:
        :return:
        """
        return True if (re.match(COMMENT, line) or re.match(WHITESPACES,
                                                            line)) else False

    def is_comment_at_end(self, line: str):
        """

        :param line:
        :return:
        """
        return True if re.match(COMMENT_END_LINE, line) else False

    def remove_comment_at_end(self, line: str):
        """

        :param line:
        :return:
        """
        return re.match(COMMENT_END_LINE, line).group(1)

    def test_regexes(self, line: str):
        return True if re.match(SYMBOL, line) else False

    def initialize_symbol_table(self, symbols: dict):
        for i in range(15):
            symbols["R" + str(i)] = i
        symbols["SCREEN"] = 16384
        symbols["KBD"] = 24576
        symbols["SP"] = 0
        symbols["LCL"] = 1
        symbols["ARG"] = 2
        symbols["THIS"] = 3
        symbols["THAT"] = 4

    def initialize_symbols(self):
        for filename in self.files.keys():
            self.symbols[filename] = dict()
        for file in self.symbols.keys():
            self.initialize_symbol_table(self.symbols[file])

    def first_pass(self, lines: list, filename: str):
        lines_to_remove = []
        for line_num, line in enumerate(lines):
            match = re.match(SYMBOL, line)
            if match:
                res = self.extract_symbol(match)
                self.symbols[filename][res] = line_num
                lines_to_remove.append(line)
        for line in lines_to_remove:
            lines.remove(line)



    def extract_symbol(self, match):
        open = match.string.index('(')
        close = match.string.index(')')
        return match.string[open + 1:close]

    def translate(self):


        for lines in self.files.items():
            self.first_pass(lines[1], lines[0])



if __name__ == '__main__':
    a = Assembler()
    a.translate()

# Tests:
# print(is_comment_at_end("  guyguy // oijoi  "))
# remove_comment_at_end("  uyguyg // oijoi  ")
# print(test_regexes("   (rgrg)   "))