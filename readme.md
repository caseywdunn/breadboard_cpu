# 8 bit breadboard computer

My build of Ben Eater's 8 bit breadboard computer. More on that project at:

- Project description at https://eater.net/8bit
- Code for burning EEPROMs at https://github.com/beneater/eeprom-programmer

## Changes and notes

A few things I came across in my build:

- The 220 ohm resistors on LEDs are required, or the LEDs pull the line voltage below what is recognized as a high.
- The pulldown resistors on the bus needed to be 4.7k rather than 10k.
- The 4 bit dip-switch needed leads soldered on to fit in the breadboard
