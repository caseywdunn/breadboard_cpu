# 8 bit breadboard computer

![bentium](bentium.gif)



My build of Ben Eater's 8 bit breadboard computer. More on that project at:

- Project description at https://eater.net/8bit
- Code for burning EEPROMs at https://github.com/beneater/eeprom-programmer

## Changes and notes

A few changes I made in my build:

- The 220 ohm resistors on LEDs are required, or the LEDs pull the line voltage below what is recognized as a high.
- The pulldown resistors on the bus needed to be 4.7k rather than 10k
- The memory address register would spontaneously clear when numbers with a large number of highs, including in particular D2 and D3, was on the bus. After a bunch of poking around I determined that there was instability on the CLR line. Don't know if it was stray capacitance, a bum chip, or something else. I fixed it by using a 74LS08, with one leg of each gate held high to configure it as a buffer, to separately drive each board CLR is connected to. This successfully isolated noise on the CLR line.
- Above didn't fully resolve register A clearing when it has a high count, adding a 100nF capacitor on that clear line reduced the problem
- Subtracting one sometimes makes big jumps. Adding a 100nF capacitor on the SU line at the ALU greatly reduced but did not entirely stop the problem
- The 4 bit dip-switch needed leads soldered on to fit in the breadboard
- I generate the EEPROM binaries with python and write them with an EEPROM programmer rather
  than use an arduino
- I wanted to be able to run it with the clock, halt at a specific point, and then step through code. To do this
I added a halt bypass button with an OR gate. When it halts, I can switch it to step mode, press and hold the bypass, hit the step button once, release the bypass, and resume stepping through the code or turn the clock back on.


## Programs

Some programs that run on the CPU are in the `programs/` directory


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
| LEFT  |  6 | MI       |   FI         |
| LEFT  |  7 | HLT      |   None       |
| RIGHT |  0 | FI       |   74LS138-A  |
| RIGHT |  1 | J        |   74LS138-B  |
| RIGHT |  2 | CO       |   74LS138-C  |
| RIGHT |  3 | CE       |   J        |
| RIGHT |  4 | OI       |   CE       |
| RIGHT |  5 | BI       |   SU        |
| RIGHT |  6 | SU       |   None     |
| RIGHT |  7 | EO       |   None     |


74LS138 for modified control logic

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

## Writing EEPROMs

Code for writing EEPROM binaries, and the binaries themselves, are in the
`eeproms/` directory. The general approach to using them is:

    python makerom_single_display.py
    hexdump -C rom_single_display.bin
    minipro -p CAT28C16A -w rom_single_display.bin

The EEPROM files are:

- `rom_single_display.bin` is for the demo at 6:29 in
https://www.youtube.com/watch?v=dLh1n2dErzE

- `rom_multi_display.bin` is for the final display driver

- `rom_control_original_no_flags.bin` is for the incremental demo without
control logic

- `rom_control_original.bin` is the final control logic of the Ben Eater video
series

- `rom_control.bin` is my modified control logic that multiplexes hlt and
output pins with a 74LS138 to free up some control lines

- `rom_control_no138.bin` is a derivative of the above, but without multiplexing.
Had some problems likely due to timing, so removed the 74LS138.
