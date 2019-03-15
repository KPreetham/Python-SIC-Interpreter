"""
constants.py
Constants related to SIC.
"""

from optab import Optab

INDEX_MODE_INSTRUCTION_LIST = [
    Optab.LDA.mnemonic,
    Optab.STA.mnemonic,
    Optab.LDCH.mnemonic,
    Optab.STCH.mnemonic,
]

TOKEN_INDEX_MODE = "X"
TOKEN_EOF = "454F46"

NEW_LINE = "\n"


class OpCode(object):
    RESB = "RESB"
    RESW = "RESW"
    WORD = "WORD"
    START = "START"
    BYTE = "BYTE"
    END = "END"
