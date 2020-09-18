"""CPU functionality."""

import sys
# print(sys.argv[0])
# print(sys.argv[1])

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100

class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # memory
        self.register = [0] * 8 # registers
        self.SP = 0xF4 # SP 
        self.pc = 0 # Program Counter 
        self.running = False
        self.FL = 0b00000000


    def ram_read( self, MAR):
        """should accept the address to read and return the value stored there."""
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                t = line.split('#')
                n = t[0].strip()

                if n == '':
                    continue
            
                try:
                    n = int(n, 2)
                except ValueError:
                    print(f"Invalid number '{n}'")
                    sys.exit(1)

                self.ram[address] = n
                address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.reg[reg_b]
        elif op == "MUL": 
            self.register[reg_a] *= self.register[reg_b]
        elif op == "CMP": 
            if self.register[reg_a] == self.register[reg_b]:
                self.FL = 0b00000001 
            elif self.register[reg_a] < self.register[reg_b]:
                self.FL = 0b00000100
            elif self.register[reg_a] > self.register[reg_b]:
                self.FL = 0b00000001
                
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

    def PUSH(self):
        # decrement the stack pointer
        self.SP -= 1
        # get value from next line of instruction
        operand_a = self.ram_read(self.pc + 1)
        # the actual value we want to push
        value = self.register[operand_a]
        # get the address at the stack pointer
        top_stack_address = self.SP
        # store it on the stack
        self.ram[top_stack_address] = value
       


    def POP(self):
        # get the address at stack pointer
        top_stack_address = self.SP
        # get value at address of stack pointer
        value = self.ram[top_stack_address]
        # get next line instruction to find where to update value
        operand_a = self.ram_read(self.pc + 1)
        # update the value
        self.register[operand_a] = value
        # increment 
        self.SP += 1 

    def CMP(self):
        reg1_num = self.ram[self.pc + 1]
        reg2_num = self.ram[self.pc + 2]
        self.alu("CMP", reg1_num, reg2_num)
        self.pc += 3
       
    def JEQ(self):
        if self.FL == 0b00000001:
            reg_num = self.ram[self.pc + 1]
            value = self.register[reg_num]
            self.pc = value
        else: self.pc += 2
    
    def JNE(self):
        if self.FL != 0b00000001:
            reg_num = self.ram[self.pc + 1]
            value = self.register[reg_num]
            self.pc = value
        else: self.pc += 2

    def JMP(self):
        reg_num = self.ram[self.pc + 1]
        value = self.register[reg_num]
        self.pc = value
    
        


    def run(self):
        """Run the CPU."""
        self.running = True 

        while self.running:

    # initialize Ir with value of ram at index pc 
            ir = self.ram_read(self.pc)
            if ir == LDI:  # PRINT_BEEJ
                self.LDI()
                self.pc += 3

            elif ir == MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu( "MUL",operand_a, operand_b)
                self.pc += 3 

            elif ir == PRN:
                self.PRN() 
                self.pc += 2 

            elif ir == HLT:  # SAVE_REG
                self.HLT() 

            elif ir == POP: 
                self.POP()
                self.pc += 2 

            elif ir == PUSH: 
                self.PUSH()
                self.pc += 2 

            elif ir == CMP: 
                self.CMP()

                
