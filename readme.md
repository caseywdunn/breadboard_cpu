# 8 bit breadboard computer

My build of Ben Eater's 8 bit breadboard computer. More on that project at:

- Project description at https://eater.net/8bit
- Code for burning EEPROMs at https://github.com/beneater/eeprom-programmer

## Changes and notes

A few things I came across in my build:

- The 220 ohm resistors on LEDs are required, or the LEDs pull the line voltage below what is recognized as a high.
- The pulldown resistors on the bus needed to be 4.7k rather than 10k
- The memory address register would spontaneously clear when numbers with a large number of highs, including in particular D2 and D3, was on the bus. After a bunch of poking around I determinded that there was instability on the CLR line. Addint a 10nF capacitor to stiffen it patched the problem. Don't know if it was stray capacitance, a bum chip, or something else.
- The 4 bit dip-switch needed leads soldered on to fit in the breadboard
- I generate the EEPROM binaries with python and write them with an EEPROM programmer rather
  than use an arduino


## Control logic

I modified the control logic to free up some pins by using a 74LS138 to
demultiplex some commands that would never be used at the same time. This includes
the OUT commands, which could damage the computer if they were activated simultaneously,
as well as HALT.

| Chip  | IO | Original | Modified |
| ----- | -- | -------- | -------- |
| LEFT  |  0 | AO       |   AI         |
| LEFT  |  1 | AI       |   BI         |
| LEFT  |  2 | II       |   II         |
| LEFT  |  3 | IO       |   RI         |
| LEFT  |  4 | RO       |   MI         |
| LEFT  |  5 | RI       |   OI         |
| LEFT  |  6 | MI       |   None       |
| LEFT  |  7 | HLT      |   None       |
| RIGHT |  0 |          |   74LS138-A  |
| RIGHT |  1 | J        |   74LS138-B  |
| RIGHT |  2 | CO       |   74LS138-C  |
| RIGHT |  3 | CE       |   J        |
| RIGHT |  4 | OI       |   CE       |
| RIGHT |  5 | BI       |   SU       |
| RIGHT |  6 | SU       |   None     |
| RIGHT |  7 | EO       |   None     |


74LS138

| Index | Control |
| ----- | ------- |
| 0     | None    |
| 1     | HLT     |
| 2     | AO      |
| 3     | IO      |
| 4     | RO      |
| 5     | CO      |
| 6     | EO      |
| 7     | BO    |

## Executing the code

### Single digit display

This writes the code needed for the demo at 6:29 in https://www.youtube.com/watch?v=dLh1n2dErzE

    python makerom_single_display.py
    hexdump -C rom_single_display.bin
    minipro -p CAT28C16A -w rom_single_display.bin



### Multiplex digit display

    python makerom_multi_display.py
    hexdump -C rom_multi_display.bin
    minipro -p CAT28C16A -w rom_multi_display.bin

### Control logic, no flags

python makerom_control_original_no_flags.py
hexdump -C rom_control_original_no_flags.bin
minipro -p CAT28C16A -w rom_control_original_no_flags.bin

### Control logic, flags

python makerom_control_original.py
hexdump -C rom_control_origina.bin
minipro -p CAT28C16A -w rom_control_original.bin
