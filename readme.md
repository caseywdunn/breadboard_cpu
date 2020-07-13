# 8 bit breadboard computer

![bentium](bentium_fib.gif)



My build of Ben Eater's 8 bit breadboard computer. More on that project at:

- Project description at https://eater.net/8bit
- Code for burning EEPROMs at https://github.com/beneater/eeprom-programmer


## Changes and notes

A few modifications I made to change the design of the build:
- I generate the EEPROM binaries with python and write them with an EEPROM programmer rather
  than use an arduino. the python code for writing the binaries is included here.
- I wanted to be able to run it with the clock, halt at a specific point, and then step through code. To do this
I added a halt bypass button with an OR gate. When it halts, I can switch it to step mode, press and hold the bypass, hit the step button once, release the bypass, and resume stepping through the code or turn the clock back on.

Some changes I made in the course of debugging:
- The 220 ohm resistors on LEDs are required, or the LEDs pull the line voltage below what is recognized as a high.
- The pulldown resistors on the bus needed to be 4.7k rather than 10k
- The memory address register would spontaneously clear when numbers with a large number of highs, including in particular D2 and D3, was on the bus. After a bunch of poking around I determined that there was instability on the CLR line. Don't know if it was stray capacitance, a bum chip, or something else. I fixed it by using a 74LS08, with one leg of each gate held high to configure it as a buffer, to separately drive each board CLR is connected to. This successfully isolated noise on the CLR line.
- Above didn't fully resolve register A clearing when it has a high count, adding a 100nF capacitor on that clear line reduced the problem
- To isolate potential clock issues, I used inverters as buffers to independently supply clock signal to post modules.
- Subtracting one sometimes makes big jumps. Adding a 100nF capacitor on the SU line at the ALU greatly reduced but did not entirely stop the problem
- The 4 bit dip-switch needed leads soldered on to fit in the breadboard


## Programs

Some programs that run on the CPU are in the `programs/` directory


## Control logic

I modified the control logic to experiment with freeing up some pins by using a 74LS138 to
demultiplex some commands that would never be used at the same time. This includes
the OUT commands, which could damage the computer if they were activated simultaneously,
as well as HALT. In the end I did not use the 74LS138 (it took the same board space
  that adding another EEPROM would, and I found it glitchy), and settled on the control
logic map in the `control` column below.

| Chip  | IO | control_original | control_138  | control  |
| ----- | -- | --------         | --------     | -------- |
| LEFT  |  0 | AO               |   AI         |  AI        
| LEFT  |  1 | AI               |   BI         |   BI         |
| LEFT  |  2 | II               |   II         |   II         |
| LEFT  |  3 | IO               |   RI         |   RI         |
| LEFT  |  4 | RO               |   MI         |   MI         |
| LEFT  |  5 | RI               |   OI         |   OI         |
| LEFT  |  6 | MI               |   FI         |   FI         |
| LEFT  |  7 | HLT              |   None       |   EO         |
| RIGHT |  0 | FI               |   74LS138-A  |   HLT        |
| RIGHT |  1 | J                |   74LS138-B  |   AO         |
| RIGHT |  2 | CO               |   74LS138-C  |   IO         |
| RIGHT |  3 | CE               |   J          |   J          |
| RIGHT |  4 | OI               |   CE         |   CE         |
| RIGHT |  5 | BI               |   SU         |   SU         |
| RIGHT |  6 | SU               |   None       |   RO         |
| RIGHT |  7 | EO               |   None       |   CO         |


74LS138 connections for `control_138` configuration above:

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

- `rom_control_138.bin` is my modified control logic that multiplexes hlt and
output pins with a 74LS138 to free up some control lines

- `rom_control.bin` is a derivative of the above, but without multiplexing.
