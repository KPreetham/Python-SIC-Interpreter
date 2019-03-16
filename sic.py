"""
sic.py
SIC parser module
"""
import logging
from math import ceil

from constants import OpCode, NEW_LINE, TOKEN_EOF, ERROR_INVALID_OPCODE
from optab import Optab
from utils import Util


class SIC(object):
    def __init__(self, input_file):
        """
        :param input_file: input program file.
        :type input_file: str
        """
        self.__input_file = input_file

        self.__locctr = 0

        self.__program_length = None
        self.__program_name = None
        self.__start_address = None
        self.__sym_tab = {}

        self.__logger = logging.getLogger("sic")
        logging.basicConfig(level=logging.DEBUG, format="%(message)s")
        self.__dry_run = True

        self.__intermediate_file = "{file_name}.intermediate".format(file_name=input_file)
        self.__output_file = "{file_name}.output".format(file_name=input_file)
        self.__file_data_template = "{locctr} {label} {opcode} {operand}"

    @property
    def input_file(self):
        return self.__input_file

    @staticmethod
    def parse_line(line):
        """
        Parse the current line. Returns tuple of label, opcode, operand


        :param line: Line to be parsed
        :type line: str
        :return: tuple of label, opcode, operand
        :rtype: tuple
        """
        label = opcode = operand = ""

        token_list = Util.get_token_list(line)

        token_length = len(token_list)

        mnemonics_list = list(Optab.as_dict().keys())

        if token_length == 1:
            if token_list[0] in mnemonics_list:
                # like RSUB
                opcode = token_list[0]
            else:
                # like END
                label = token_list[0]
        elif token_length == 2:
            if token_list[0] in mnemonics_list:
                # like ADD THREE
                opcode, operand = token_list
            elif token_list[1] in mnemonics_list:
                # like END RSUB
                label, opcode = token_list
        elif token_length == 3:
            if token_list[0] in mnemonics_list:
                # like LDA BUFFER, X
                opcode, operand, _ = token_list
            else:
                # like THREE WORD 3
                label, opcode, operand = token_list
        elif token_length == 4:
            # like LOOP LDA BUFFER, X
            # or EOF BYTE C'454F46'
            label = token_list[0]
            opcode = token_list[1]

            if opcode == OpCode.BYTE:
                # if opcode is BYTE then the 4th string
                # will be the actual value,(token_list[3]).
                # 3rd string will be 'C' or 'X'
                operand = token_list[3]
            else:
                operand = token_list[2]

        return label, opcode, operand

    def process(self, pass_level=1, dry_run=True):
        self.__dry_run = dry_run

        self.__pass_1()

        if pass_level == 2:
            self.__pass_2()

    def __pass_1(self):
        self.__logger.info("Pass 1 started")

        mnemonics_list = list(Optab.as_dict().keys())

        output_data_list = []

        with open(self.__input_file) as f_input:
            first_line = f_input.readline()
            first_line = Util.clean(first_line)

            label, opcode, operand = self.parse_line(first_line)

            if opcode == OpCode.START:
                self.__locctr = hex(int(operand, 16))
                self.__program_name = label
            else:
                self.__locctr = 0

            self.__start_address = self.__locctr

            write_content = self.__file_data_template.format(
                locctr=self.__locctr,
                label=label,
                opcode=opcode,
                operand=operand,
            )

            self.__logger.info(write_content)

            if not self.__dry_run:
                output_data_list.append(write_content)

            while True:
                current_line = Util.clean(f_input.readline())

                # If the current line is empty or is a comment, skip
                if current_line and current_line[0] == ".":
                    continue

                label, opcode, operand = self.parse_line(current_line)

                if opcode == OpCode.END or label == OpCode.END:
                    self.__locctr = hex(int(self.__locctr, 16) + value)
                    write_content = self.__file_data_template.format(
                        locctr=self.__locctr,
                        label=label,
                        opcode=opcode,
                        operand=operand,
                    )

                    self.__logger.info(write_content)

                    if not self.__dry_run:
                        with open(self.__intermediate_file, "w") as f_output:
                            for line in output_data_list:
                                f_output.write(Util.clean(line))
                                f_output.write(NEW_LINE)

                    self.__program_length = int(self.__locctr, 16) - int(self.__start_address, 16)
                    self.__logger.info("Program length: {length}".format(length=self.__program_length))
                    break

                if label in self.__sym_tab.keys():
                    raise Exception("Error. Duplicate symbol")

                if label:
                    # hex values contain 0x in the beginning, remove it.
                    self.__sym_tab[label] = self.__locctr[2:]

                value = self.__get_memory_space(opcode, operand, current_line, mnemonics_list)
                if value == ERROR_INVALID_OPCODE:
                    raise Exception("Error. Opcode {opcode} is invalid".format(opcode=opcode))

                self.__locctr = hex(int(self.__locctr, 16) + value)

                write_content = self.__file_data_template.format(
                    locctr=self.__locctr,
                    label=label,
                    opcode=opcode,
                    operand=operand,
                )

                self.__logger.info(write_content)

                if not self.__dry_run:
                    output_data_list.append(write_content)

    def __pass_2(self):
        self.__logger.info("Pass 2 started")

        output_data_list = []

        with open(self.__input_file) as f_input:
            while True:
                current_line = Util.clean(f_input.readline())
                label, opcode, operand = self.parse_line(current_line)

                if label == OpCode.START or opcode == OpCode.START:
                    output_header_template = "H {program_name} {start_address} {program_length}".format(
                        program_name=self.__program_name.rjust(6, " "),
                        start_address=self.__start_address[2:].rjust(6, "0"),
                        program_length=hex(self.__program_length)[2:].rjust(6, "0")
                    )

                    start_address_line = "\nT {start_address}".format(
                        start_address=self.__start_address[2:].rjust(6, "0")
                    )

                    self.__logger.info(output_header_template)
                    self.__logger.info(start_address_line)

                    if not self.__dry_run:
                        output_data_list.append(output_header_template)
                        output_data_list.append(start_address_line)

                    continue

                if label == OpCode.END or opcode == OpCode.END:
                    end_line = "\nE {start_address}".format(start_address=self.__start_address[2:].rjust(6, "0"))
                    self.__logger.info(end_line)

                    if not self.__dry_run:
                        output_data_list.append(end_line)
                        with open(self.__output_file, "w") as f_output:
                            f_output.write(" ".join(output_data_list))

                    break

                optab_dict = Optab.as_dict()
                mnemonics_list = list(optab_dict.keys())

                instruction = None

                if opcode in mnemonics_list:
                    if operand:
                        if operand in self.__sym_tab.keys():
                            address = self.__sym_tab[operand]
                        else:
                            raise Exception("Error. Undefined symbol: {operand}.".format(operand=operand))
                    else:
                        address = "0"

                    instruction = optab_dict[opcode]

                    # address field is 16 bit(4 nibbles)
                    # So if the address is not 4  nibble long we pad it with extra 0's.
                    address = address.rjust(4, "0")

                    # in the next line we calculate the 3rd nibble(i.e the first nibble after opcode).
                    nibble = int(str(int(Util.is_index_mode(current_line))) + "0"*3) + int(address[0])
                    nibble = hex(nibble)  # convert it back to hex.
                    nibble = nibble[2:]  # remove the 0x in the beginning.

                    instruction = instruction + nibble + address[1:]

                elif opcode == OpCode.WORD or opcode == OpCode.BYTE:
                    instruction = operand.rjust(6, "0")

                if instruction:
                    self.__logger.info(instruction)

                if not self.__dry_run and instruction:
                    output_data_list.append(instruction)

    @staticmethod
    def __get_memory_space(opcode, operand, current_line, mnemonics_list):
        """
        Returns the memory required for current instruction.


        :param opcode: Opcode
        :type opcode: str
        :param operand: Operand
        :type operand: str
        :param current_line: Current parsed line
        :type current_line: str
        :param mnemonics_list: List of mnemonics
        :type mnemonics_list: list
        :return: Memory required for current instruction.
        :rtype: int
        """
        value = ERROR_INVALID_OPCODE

        if opcode in mnemonics_list:
            value = 3
        elif opcode == OpCode.WORD:
            value = 3
        elif opcode == OpCode.RESW:
            value = 3 * int(operand)
        elif opcode == OpCode.RESB:
            value = int(operand)
        elif opcode == OpCode.BYTE:
            if Util.is_hex_constant(current_line):
                value = ceil(len(operand) / 2)
            elif operand == TOKEN_EOF:
                value = 3
            else:
                value = len(operand)

        return value


if __name__ == '__main__':
    file_path = "/home/preetham/A Simple SIC interpreter/pro1.txt"
    sic = SIC(file_path)
    sic.process(pass_level=2, dry_run=False)
