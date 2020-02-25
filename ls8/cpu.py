"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111


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

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(program, 'r') as f:
            for line in f:
                # drop the '\n'
                instruction = line.strip()
                # strip out the comment, if any
                instruction = instruction.partition('#')[0]
                if instruction == '':
                    continue
                self.ram[address] = int(instruction, base=2)
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # N.B. enforce 8-bit maximum value with ... & 0xFF

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            elf.reg[reg_a] = self.reg[reg_a] & 0xFF
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
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif ir == PRN:
                num = self.reg[operand_a]
                print(num)
                self.pc += 2
            elif ir == HLT:
                sys.exit(0)
            else:
                print(f"I did not understand that ir: {ir}")
                sys.exit(1)
