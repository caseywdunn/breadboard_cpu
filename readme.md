# 8 bit breadboard computer

My build of Ben Eater's 8 bit breadboard computer. More on that project at:

- Project description at https://eater.net/8bit
- Code for burning EEPROMs at https://github.com/beneater/eeprom-programmer

## Changes and notes

A few things I came across in my build:

- The 220 ohm resistors on LEDs are required, or the LEDs pull the line voltage below what is recognized as a high.
- The pulldown resistors on the bus needed to be 4.7k rather than 10k.
- The 4 bit dip-switch needed leads soldered on to fit in the breadboard
- I generate the EEPROM binaries with python and write them with an EEPROM programmer rather
  than use an arduino


## Executing the code

### Single digit display

This writes the code needed for the demo at 6:29 in https://www.youtube.com/watch?v=dLh1n2dErzE

    python makerom_single_display.py
    hexdump -C rom_single_display.bin
    minipro -p CAT28C16A -w rom_single_display.bin



### Multiplex digit display
