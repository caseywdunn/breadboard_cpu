import numpy as np

# Derived from https://github.com/beneater/eeprom-programmer/blob/master/microcode-eeprom-with-flags/microcode-eeprom-with-flags.ino
# But without flags...


rom_bytes = 2048
debug = False
# debug = True


# Take in a 16 bit unsigned integer, and return the lower and upper bytes
# (little endian)
def int_to_bytes ( x ):
    x = int(x)
    if (x<0 or x > 0b1111111111111111):
        raise ValueError
    low  = x & 0b0000000011111111
    high = x >> 8
    output = bytes([ low, high ])
    return( output )

def lower_byte (x):
    return( int_to_bytes(x)[0] )

def upper_byte (x):
    return( int_to_bytes(x)[1] )

v_lower_byte = np.vectorize(lower_byte)
v_upper_byte = np.vectorize(upper_byte)


code = bytearray( [0x00] * rom_bytes )
# Chip  LLLLLLLLRRRRRRRR
# D     7654321076543210

# Left EEPROM
EO  = 0b1000000000000000  # ALU out
FI  = 0b0100000000000000  # Flags in
OI  = 0b0010000000000000  # Output register in
MI  = 0b0001000000000000  # Memory address register in
RI  = 0b0000100000000000  # RAM data in
II  = 0b0000010000000000  # Instruction register in
BI  = 0b0000001000000000  # B register in
AI  = 0b0000000100000000  # A register in

# Right EEPROM

# Right EEPROM
CO  = 0b0000000010000000  # Program counter out
RO  = 0b0000000001000000  # RAM data out
SU  = 0b0000000000100000  # ALU subtract
CE  = 0b0000000000010000  # Program counter enable
J   = 0b0000000000001000  # Jump (program counter in)
IO  = 0b0000000000000100  # Instruction register out
AO  = 0b0000000000000010  # A register out
HLT = 0b0000000000000001  # Halt clock




# 74LS138 controlled pins, driven by right EEPROM
#                    CBA
# HLT = 0b0000000000000001  # Halt clock
# AO  = 0b0000000000000010  # A register out
# IO  = 0b0000000000000011  # Instruction register out
# RO  = 0b0000000000000100  # RAM data out
# CO  = 0b0000000000000101  # Program counter out
# EO  = 0b0000000000000110  # ALU out
# BO  = 0b0000000000000111  # B register out

UCODE_TEMPLATE = np.array([
  [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ],   # 0000 - NOP
  [ MI|CO,  RO|II|CE,  IO|MI,  RO|AI,  0,           0, 0, 0 ],   # 0001 - LDA
  [ MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  EO|AI|FI,    0, 0, 0 ],   # 0010 - ADD
  [ MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  EO|AI|SU|FI, 0, 0, 0 ],   # 0011 - SUB
  [ MI|CO,  RO|II|CE,  IO|MI,  AO|RI,  0,           0, 0, 0 ],   # 0100 - STA
  [ MI|CO,  RO|II|CE,  IO|AI,  0,      0,           0, 0, 0 ],   # 0101 - LDI
  [ MI|CO,  RO|II|CE,  IO|J,   0,      0,           0, 0, 0 ],   # 0110 - JMP
  [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ],   # 0111 - JC
  [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ],   # 1000 - JZ
  [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ],   # 1001 - JNZ
  [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ],   # 1010
  [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ],   # 1011
  [ MI|CO,  RO|II|CE,  0,      0,      0,           0, 0, 0 ],   # 1100
  [ MI|CO,  RO|II|CE,  IO|MI,  RO|BI,  SU|FI,       0, 0, 0 ],   # 1101 - CMP  does a subtraction, sets flags, and then throws away result
  [ MI|CO,  RO|II|CE,  AO|OI,  0,      0,           0, 0, 0 ],   # 1110 - OUT
  [ MI|CO,  RO|II|CE,  HLT,    0,      0,           0, 0, 0 ],   # 1111 - HLT
]);


# Address lines
# A0-A2  Microcode counter
# A3-A6  Instruction register
# A7     Chip select (low for the left chip (the higher order byte) and high for the right chip (the lower order byte))
# A8     Carry flag
# A9     Zero flag
# A10    Ground

# ZF = 0, CF = 0
chunk = UCODE_TEMPLATE
chunk[9,2] =  IO|J
upper = bytearray(v_upper_byte(chunk).flatten().tolist())
lower = bytearray(v_lower_byte(chunk).flatten().tolist())
code[0:128] = upper
code[128:256] = lower

# ZF = 0, CF = 1
chunk = UCODE_TEMPLATE
chunk[7,2] =  IO|J
chunk[9,2] =  IO|J
upper = bytearray(v_upper_byte(chunk).flatten().tolist())
lower = bytearray(v_lower_byte(chunk).flatten().tolist())
code[256:384] = upper
code[384:512] = lower

# ZF = 1, CF = 0
chunk = UCODE_TEMPLATE
chunk[8,2] =  IO|J
upper = bytearray(v_upper_byte(chunk).flatten().tolist())
lower = bytearray(v_lower_byte(chunk).flatten().tolist())
code[512:640] = upper
code[640:768] = lower

#  ZF = 1, CF = 1
chunk = UCODE_TEMPLATE
chunk[7,2] =  IO|J
chunk[8,2] =  IO|J
upper = bytearray(v_upper_byte(chunk).flatten().tolist())
lower = bytearray(v_lower_byte(chunk).flatten().tolist())
code[768:896] = upper
code[896:1024] = lower


with open("rom_control_no138.bin", "wb") as out_file:
  out_file.write(code)
