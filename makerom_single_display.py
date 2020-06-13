#
# Please see this video for details:
# https://www.youtube.com/watch?v=yl8vPW5hydQ
#
code = bytearray([
  # Bit patterns for the digits 0..9
  0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b
  ])

rom = code + bytearray([0xff] * (2048 - len(code)))

with open("rom_single_display.bin", "wb") as out_file:
  out_file.write(rom)
