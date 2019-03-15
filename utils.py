"""
utils.py
List of utilities
"""
import re

from constants import (TOKEN_INDEX_MODE, INDEX_MODE_INSTRUCTION_LIST, OpCode)
from optab import Optab


class Util(object):
    @classmethod
    def is_index_mode(cls, line):
        """
        Determine whether list of tokens belong to index mode or not.


        :param line: List of tokens
        :type line: str
        :return: Is index mode instruction?
        :rtype: bool
        """

        # Index mode instruction will have 3 or four parts.
        # i.e like LDA BUFFER,X     , opcode position = 0 (3 - 3)
        # or LOOP LDA BUFFER,X      , opcode position = 1 (4 - 3)
        # in such cases the opcode will always be in the position length(tokens) - 3

        token_list = cls.get_token_list(line)

        print(token_list)

        return (
            len(token_list) >= 3 and token_list[-1] == TOKEN_INDEX_MODE
            and token_list[len(token_list) - 3] in INDEX_MODE_INSTRUCTION_LIST
        )

    @classmethod
    def clean(cls, line):
        """

        :param line:
        :type line: str
        :return:
        """

        # Replace anything other than alphanumeric with space
        line = re.sub(r"[^0-9a-zA-Z]+", " ", line)

        # replace multiple spaces with a single space and convert it to upper case.
        line = re.sub(r" +", " ", line).upper()

        line = line.strip()

        return line

    @classmethod
    def get_token_list(cls, line):
        """
        Normalises the line and returns the list of tokens


        :param line: Line to get token from
        :type line: str
        :return: List of tokens parsed from line
        :rtype: list
        """

        return [token.upper() for token in cls.clean(line).split()]

    @classmethod
    def is_hex_constant(cls, line):
        """
        Determines whether the current line has hex constant symbol.


        :param line: Current line
        :type line: str
        :return: Bool. True if current line has hex constant.
        :rtype: bool
        """

        line = cls.get_token_list(line)

        return len(line) == 4 and line[2] == TOKEN_INDEX_MODE

    @classmethod
    def is_valid_opcode(cls, opcode):
        """
        Checks whether `opcode` is valid or not


        :param opcode: OpCode to verify
        :type opcode: str
        :return: Boolean
        :rtype: bool
        """

        return (opcode in Optab.as_dict().keys()) or (opcode in [OpCode.BYTE, OpCode.WORD, OpCode.RESB, OpCode.RESW])
