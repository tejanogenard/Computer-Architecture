"""CPU functionality."""

import sys
print(sys.argv[0])
print(sys.argv[1])


class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # memory
        self.register = [0] * 8 # registers
        self.pc = 0 # Program Counter 
        self.running = False

    def ram_read( self, MAR):
        """should accept the address to read and return the value stored there."""
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(sys.argv[1]) as f:
            for line in f:
                t = line.split('#')
                n = t[0].strip()

                if n == '':
                    continue
            
            try:
                n = int(n)
            except ValueError:
                print(f"Invalid number '{n}'")
                sys.exit(1)

            self.ram[address] = n
            address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
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

    def LDI(self):
        """Load Register Immediate: set the value of a register to an integer"""
        operand_num = self.ram_read(self.pc + 1)
        operand_value = self.ram_read(self.pc + 2)
        self.register[operand_num] = operand_value

    def PRN(self):
        """Print Register: print the numeric value stored in a given register"""
        address = self.ram_read(self.pc + 1)
        print(self.register[address])

    def HLT(self):
        """Halt: halt the CPU (& exit the emulator)"""
        self.running = False 

    def run(self):
        """Run the CPU."""
        self.running = True 

    # Machine Code value binary 
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while self.running:

    # initialize Ir with value of ram at index pc 
            ir = self.ram_read(self.pc)

            if ir == LDI:  # PRINT_BEEJ
                self.LDI()
                self.pc += 3

            elif ir == PRN:
                self.PRN() 
                self.pc += 2 

            elif ir == HLT:  # SAVE_REG
                self.HLT() 
