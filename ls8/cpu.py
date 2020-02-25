"""CPU functionality."""

import sys

# Instructions
# ADD  = 0b10100000  #  0
# AND  = 0b10101000  #  8
# CALL = 0b01010000  #  0
# CMP  = 0b10100111  #  7
# DEC  = 0b01100110  #  6
# DIV  = 0b10100011  #  3
HLT  = 0b00000001  #  1
# INC  = 0b01100101  #  5
# INT  = 0b01010010  #  2
# IRET = 0b00010011  #  3
# JEQ  = 0b01010101  #  5
# JGE  = 0b01011010  # 10
# JGT  = 0b01010111  #  7
# JLE  = 0b01011001  #  9
# JLT  = 0b01011000  #  8
# JMP  = 0b01010100  #  4
# JNE  = 0b01010110  #  6
# LD   = 0b10000011  #  3
LDI  = 0b10000010  #  2
# MOD  = 0b10100100  #  4
MUL  = 0b10100010  #  2
# NOP  = 0b00000000  #  0
# NOT  = 0b01101001  #  9
# OR   = 0b10101010  # 10
# POP  = 0b01000110  #  6
# PRA  = 0b01001000  #  8
PRN  = 0b01000111  #  7
# PUSH = 0b01000101  #  5
# RET  = 0b00010001  #  1
# SHL  = 0b10101100  # 12
# SHR  = 0b10101101  # 13
# ST   = 0b10000100  #  4
# SUB  = 0b10100001  #  1
# XOR  = 0b10101011  # 11


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pc represents the Program Counter
        self.pc = 0
        # reg represents the eight general purpose registers
        self.reg = [0] * 8
        # ram represents 256 bytes of random access memory
        self.ram = [0] * 256
        # branch table
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[MUL] = self.mul
        self.branchtable[PRN] = self.prn

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def hlt(self):
        sys.exit(0)

    def ldi(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def mul(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('MUL', operand_a, operand_b)
        self.pc += 3

    def prn(self):
        operand = self.ram_read(self.pc + 1)
        print(self.reg[operand])
        self.pc += 2

    def load(self, program):
        """Load a program into memory."""

        address = 0

        try:
            with open(program, 'r') as f:
                for line in f:
                    # strip out comment, if any, and whitespace
                    instruction = line.split('#')[0].strip()
                    if instruction == '':
                        continue
                    self.ram[address] = int(instruction, base=2)
                    address += 1

        except FileNotFoundError:
            print(f'File not found. path: {program}')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # Enforce 8-bit max value with last line of each statement: ...& 0xFF
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.reg[reg_a] = self.reg[reg_a] & 0xFF
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.reg[reg_a] = self.reg[reg_a] & 0xFF
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            # ir represents the Instruction Register
            ir = self.ram_read(self.pc)

            if ir in self.branchtable:
                self.branchtable[ir]()
            else:
                print(f"I did not understand that ir: {ir}")
                sys.exit(1)
