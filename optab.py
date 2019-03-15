"""
optab.py
Contains OPTAB list
"""

from collections import namedtuple


class Optab(object):
    """
    Optab class.
    """
    __optab_named_tuple = namedtuple("OptabTuple", ["mnemonic", "opcode"])

    ADD = __optab_named_tuple(mnemonic='ADD', opcode='18')
    ADDF = __optab_named_tuple(mnemonic='ADDF', opcode='58')
    ADDR = __optab_named_tuple(mnemonic='ADDR', opcode='90')
    AND = __optab_named_tuple(mnemonic='AND', opcode='40')
    CLEAR = __optab_named_tuple(mnemonic='CLEAR', opcode='B4')
    COMP = __optab_named_tuple(mnemonic='COMP', opcode='28')
    COMPF = __optab_named_tuple(mnemonic='COMPF', opcode='88')
    COMPR = __optab_named_tuple(mnemonic='COMPR', opcode='A0')
    DIV = __optab_named_tuple(mnemonic='DIV', opcode='24')
    DIVF = __optab_named_tuple(mnemonic='DIVF', opcode='64')
    DIVR = __optab_named_tuple(mnemonic='DIVR', opcode='9C')
    FIX = __optab_named_tuple(mnemonic='FIX', opcode='C4')
    FLOAR = __optab_named_tuple(mnemonic='FLOAR', opcode='C0')
    HIO = __optab_named_tuple(mnemonic='HIO', opcode='F4')
    J = __optab_named_tuple(mnemonic='J', opcode='3C')
    JEQ = __optab_named_tuple(mnemonic='JEQ', opcode='30')
    JGT = __optab_named_tuple(mnemonic='JGT', opcode='34')
    JLT = __optab_named_tuple(mnemonic='JLT', opcode='38')
    JSUB = __optab_named_tuple(mnemonic='JSUB', opcode='48')
    LDA = __optab_named_tuple(mnemonic='LDA', opcode='00')
    LDB = __optab_named_tuple(mnemonic='LDB', opcode='68')
    LDCH = __optab_named_tuple(mnemonic='LDCH', opcode='50')
    LDF = __optab_named_tuple(mnemonic='LDF', opcode='70')
    LDL = __optab_named_tuple(mnemonic='LDL', opcode='08')
    LDS = __optab_named_tuple(mnemonic='LDS', opcode='6C')
    LDT = __optab_named_tuple(mnemonic='LDT', opcode='74')
    LDX = __optab_named_tuple(mnemonic='LDX', opcode='04')
    LPS = __optab_named_tuple(mnemonic='LPS', opcode='D0')
    MUL = __optab_named_tuple(mnemonic='MUL', opcode='20')
    MULF = __optab_named_tuple(mnemonic='MULF', opcode='60')
    MULR = __optab_named_tuple(mnemonic='MULR', opcode='98')
    NORM = __optab_named_tuple(mnemonic='NORM', opcode='C8')
    OR = __optab_named_tuple(mnemonic='OR', opcode='44')
    RD = __optab_named_tuple(mnemonic='RD', opcode='D8')
    RMO = __optab_named_tuple(mnemonic='RMO', opcode='AC')
    RSUB = __optab_named_tuple(mnemonic='RSUB', opcode='4C')
    SHIFTL = __optab_named_tuple(mnemonic='SHIFTL', opcode='A4')
    SHIFTR = __optab_named_tuple(mnemonic='SHIFTR', opcode='A8')
    SIO = __optab_named_tuple(mnemonic='SIO', opcode='F0')
    SSK = __optab_named_tuple(mnemonic='SSK', opcode='EC')
    STA = __optab_named_tuple(mnemonic='STA', opcode='0C')
    STB = __optab_named_tuple(mnemonic='STB', opcode='78')
    STCH = __optab_named_tuple(mnemonic='STCH', opcode='54')
    STF = __optab_named_tuple(mnemonic='STF', opcode='80')
    STI = __optab_named_tuple(mnemonic='STI', opcode='D4')
    STL = __optab_named_tuple(mnemonic='STL', opcode='14')
    STS = __optab_named_tuple(mnemonic='STS', opcode='7C')
    STSW = __optab_named_tuple(mnemonic='STSW', opcode='E8')
    STT = __optab_named_tuple(mnemonic='STT', opcode='84')
    STX = __optab_named_tuple(mnemonic='STX', opcode='10')
    SUB = __optab_named_tuple(mnemonic='SUB', opcode='1C')
    SUBF = __optab_named_tuple(mnemonic='SUBF', opcode='5C')
    TIX = __optab_named_tuple(mnemonic='TIX', opcode='2C')

    @classmethod
    def as_dict(cls):
        """
        Returns the Optab as a dictionary where key will be the mnemonic code and value will be the opcode.


        :return: Optab dict
        :rtype: dict
        """
        optab_dict = {}

        for member in dir(Optab):
            if not callable(getattr(Optab, member)) and not member.startswith("_"):
                optab_dict[member] = getattr(Optab, member).opcode

        return optab_dict
