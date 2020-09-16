"""CPU functionality."""

import sys

SP = 7

LDI = 0b10000010 # 0x820RII
PRN = 0b01000111 # 0x450R
HLT = 0b00000001 # 0x01
MUL = 0b10100010 # 
PUSH = 0b01000101 # 
POP = 0b01000110 #


alu_dict = {}
alu_dict[0b00000000] = "ADD"
alu_dict[0b00000001] = "SUB"
alu_dict[0b00000010] = "MUL"
alu_dict[0b00000011] = "DIV"
alu_dict[0b00000100] = "MOD"
alu_dict[0b00000101] = "INC"
alu_dict[0b00000110] = "DEC"
alu_dict[0b00000111] = "CMP"
alu_dict[0b00001000] = "AND"
alu_dict[0b00001001] = "NOT"
alu_dict[0b00001010] = "OR"
alu_dict[0b00001011] = "XOR"
alu_dict[0b00001100] = "SHL"
alu_dict[0b00001101] = "SHR"


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0
        self.reg[SP] = 244

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        if len(sys.argv) != 2:
            print("MISSING ARG --->  Usage: cpu.py FILENAME")
            sys.exit(1)
        
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    l = line.split("#")
                    ls = l[0].strip()

                    if ls == "":
                        continue

                    try:
                        ls = int(ls, 2)
                    except ValueError:
                        print(f"invalid binary number '{n}'")
                        sys.exit(1)

                    self.ram[address] = ls
                    address += 1
        
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def ram_read(self, add):
        return self.ram[add]

    def ram_write(self, val, add):
        self.ram[add] = val

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]

        else:
            print(op)
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
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
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # str_ir = str(ir)

            if ir == HLT:
                break

            elif ir == LDI:
                self.reg[operand_a] = operand_b

            elif ir == PRN:
                print(self.reg[operand_a])

            elif ((ir & 0b00100000) >> 5) == 0b001:
                self.alu(alu_dict[(ir & 0b00001111)], operand_a, operand_b) 

            elif ir == PUSH:
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.reg[operand_a]
            
            elif ir == POP:
                self.reg[operand_a] = self.ram[self.reg[SP]]
                self.reg[SP] += 1

            
            self.pc += ((ir & 0b11000000) >> 6) + 1
            


