#
# A python adaptation of
# https://github.com/beneater/eeprom-programmer/blob/master/multiplexed-display/multiplexed-display.ino
#

# Takes an integer. If less than 0, converts it to two's complement binary than
# converts back to an integer using standard binary
def abs_byte (input):
  if ( 0 <= input and input <256 ):
    return input
  return int.from_bytes(  (input).to_bytes(1, byteorder='big', signed=True), byteorder='big')


rom_bytes = 2048
debug = False
# debug = True

# Bit patterns for the digits 0..9
digits = bytearray([ 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b ])

if debug:
  digits = bytearray([ 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09 ])

code = bytearray( [0xff] * rom_bytes )

# Unsigned

# ones place
# 0000 - 00ff
for value in range(0, 256):
  code[ value ] = digits[ value % 10 ]

# tens place
# 0100 - 01ff
for value in range(0, 256):
  code[ value + 256 ] = digits[ (value // 10) % 10 ]

# hundreds place
# 0200 - 02ff
for value in range(0, 256):
  code[ value + 512 ] = digits[ (value // 100) % 10 ]

# sign
# 0300 - 03ff
for value in range(0, 256):
  code[ value + 768] = 0x00

# Twos complement

# ones place
# 0400 - 04ff
for value in range(-128, 128):
  code[ abs_byte(value) + 1024 ] = digits[ abs(value) % 10 ]

# tens place
# 0500 - 05ff
for value in range(-128, 128):
  code[ abs_byte(value) + 1280 ] = digits[ (abs(value) // 10) % 10 ]

# hundreds place
# 0600 - 06ff
for value in range(-128, 128):
  code[ abs_byte(value) + 1536 ] = digits[ (abs(value) // 100) % 10 ]

# sign
# 0800 - 08ff
for value in range(-128, 128):
  if value < 0:
    if debug:
      code[ abs_byte(value) + 1792] = 0x0a
    else:
      code[ abs_byte(value) + 1792] = 0x01
  else:
    code[ abs_byte(value) + 1792] = 0x00


with open("rom_multi_display.bin", "wb") as out_file:
  out_file.write(code)
