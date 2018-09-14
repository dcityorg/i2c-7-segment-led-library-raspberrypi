# -*- coding: utf-8 -*-

'''
    I2c7SegmentLed.py - class library for using 7 Segment LEDs

    Written by: Gary Muhonen  gary@dcity.org

    Versions
        1.0.0 - 7/31/2016
            Original Release.
        1.0.1 - 9/1/2018
            Transfer to GM, and some minor changes

    Short Description:

        These files provide a software library and demo program for the Raspberry Pi.

        The library files provide useful functions to make it easy
        to communicate with 7 Segment LEDs
        that use the I2C communication protocol. The demo
        program shows the usage of the functions in the library.

        The 7 Segment LED must connect to the I2C bus using a AMS AS1115 controller chip.
        A backback board with the AMS AS1115 chip is available and details are in the link below.

    https://www.dcity.org/portfolio/i2c-7-segment-led-library/
    This link has details including:
        * software library installation for use with Arduino, Particle and Raspberry Pi boards
        * list of functions available in these libraries
        * a demo program (which shows the usage of most library functions)
        * info on 7 segment LED displays that work with this software
        * hardware design for a backpack board for 7 segment LEDs, available on github
        * info on backpack “bare” pc boards available from OSH Park.


    License Information:  https://www.dcity.org/license-information/


    Notes:
        1. You must enable I2C on your Raspberry Pi board (see your particular operating system documentation).
            On Raspian: Menu...Preferences...Raspberry Pi Configuration...Interfaces...Enable I2C
        2. This software was tested on a RASPBERRY PI 3 MODEL B, running Rasbian and Python 3.5.2

'''

import smbus                # import the i2c library
from time import sleep      # import the sleep functions

i2c = smbus.SMBus(1)        # create an i2c object for writing/reading from i2c

# create a class for the i2c 7 segment led displays that use the AS1115 chip
class I2c7SegmentLed(object):

    # Control Register Addresses in the AS1115
    # Digit 0-7 are at adresses 1-8
    REG_DECODE_MODE       = 0x09     # sets which digits respond to data that is decoded (like BCD or HEX)
    REG_GLOBAL_INTENSITY  = 0X0a     # set the brightness for all digits... only bottom 4 bits are used for 16 brightness values
    REG_SCAN_LIMIT        = 0x0b     # controls which digits are turned on
    REG_SHUTDOWN          = 0x0c     # used to shutdown the display and save power
    REG_FEATURE           = 0x0e     # register that contains key features
    REG_DISPLAY_TEST_MODE = 0x0f     # used for test mode
    REG_DIGIT01_INTENSITY = 0x10
    REG_DIGIT23_INTENSITY = 0x11
    REG_DIGIT45_INTENSITY = 0x12
    REG_DIGIT67_INTENSIGY = 0x13

    REG_DIAGNOSTIC_DIGIT0 = 0x14
    REG_DIAGNOSTIC_DIGIT1 = 0x15
    REG_DIAGNOSTIC_DIGIT2 = 0x16
    REG_DIAGNOSTIC_DIGIT3 = 0x17
    REG_DIAGNOSTIC_DIGIT4 = 0x18
    REG_DIAGNOSTIC_DIGIT5 = 0x19
    REG_DIAGNOSTIC_DIGIT6 = 0x1a
    REG_DIAGNOSTIC_DIGIT7 = 0x1b
    REG_KEYA              = 0x1c
    REG_KEYB              = 0x1d

    REG_SELF_ADDRESSING   = 0x2d     # register used to set the chip to read jumpers to determine it's own i2c address

    # Constants that can be written to the control registers above

    # REG_DECODE_MODE values (type of decode is set in REG_FEATURE)
    REG_DECODE_MODE_NO_DIGITS  = 0x00      # no decoding
    REG_DECODE_MODE_ALL_DIGITS = 0xFF     # used for BCD or HEX decoding, bit 0 turns on digit 0 for decoding, etc

    # REG_SCAN_LIMIT values (how many digits are displayed)
    REG_SCAN_LIMIT_1 =  0x00  # if there is only 1 digit in the display
    REG_SCAN_LIMIT_2 =  0x01
    REG_SCAN_LIMIT_3 =  0x02
    REG_SCAN_LIMIT_4 =  0x03
    REG_SCAN_LIMIT_5 =  0x04
    REG_SCAN_LIMIT_6 =  0x05
    REG_SCAN_LIMIT_7 =  0x06
    REG_SCAN_LIMIT_8 =  0x07  # if there are 8 digits in the display

    # REG_SHUTDOWN values
    REG_SHUTDOWN_SHUTDOWN_AND_RESET = 0x00  # shutdown chip and reset the feature register
    REG_SHUTDOWN_SHUTDOWN = 0x80            # shutdown chip and don't reset the feature register
    REG_SHUTDOWN_NORMAL_AND_RESET = 0x01    # set normal mode and reset the feature register
    REG_SHUTDOWN_NORMAL = 0X81              # set normal mode and don't reset the feature register...this is the normal running values

    # REG_SELF_ADDRESSING values, for determinine the chip's i2c address
    REG_SELF_ADDRESSING_FACTORY_ADDRESS = 0x00  # for using factory set i2c address = 0x00
    REG_SELF_ADDRESSING_USER_ADDRESS = 0x01     # for using jumpers to determine i2c address

    # REG_FEATURE bit values
    REG_FEATURE_EXTERNAL_CLOCK = 0X01   # set bit if using an external clock
    REG_FEATURE_RESET = 0x02            # set bit to reset all registers
    REG_FEATURE_HEX = 0x04              # clear this bit for BCD decoding, set for HEX decoding
    REG_FEATURE_BLINK = 0x10            # set bit to enable blinking of display
    REG_FEATURE_BLINK_FREQUENCY = 0x020 # set bit for 2 second blinking, clear for 1 second blinking
    REG_FEATURE_SYNC = 0x40             # set bit for multiple device blinking
    REG_FEATURE_BLINK_START = 0x80      # set bit to start blinking when display turns on, clear to start blinking when display turns off

    DECIMAL_POINT_MASK = 0x80           # bit to control the decimal point

    # segment values for the LED for all 128 ASCII characters
    # the first value is for ASCII character 0, then 1, etc
    # each byte contains the 7 LED segments and the decimal point, arranged as (from MSB to LSB)
    #    DP G F E D C B A   (DP, middle, top left, btm left, btm, btm right, top right, top)
    # if a bit is a '1', then that segment of the led will be turned on.
    LedSegments = [
        0b01111110,0b00110000,0b01101101,0b01111001,0b00110011,0b01011011,0b01011111,0b01110010,  # Ascii decimal:0-7       hex:00-07
        0b01111110,0b01111011,0b01111101,0b00011111,0b00001101,0b00111101,0b01101111,0b01000111,  # Ascii decimal:8-15      hex:08-0F
        0b01111110,0b00000110,0b01101101,0b01001111,0b00010111,0b01011011,0b01111011,0b00011110,  # Ascii decimal:16-23     hex:10-17
        0b01111111,0b01011111,0b01101111,0b01110011,0b01100001,0b01100111,0b01111101,0b00111001,  # Ascii decimal:24-31     hex:18-1f
        0b00000000,0b00110000,0b00100010,0b01000001,0b01001001,0b00100101,0b00110001,0b00000010,  # Ascii decimal:32-39     hex:20-27
        0b01001010,0b01101000,0b01000010,0b00000111,0b00000100,0b00000001,0b00000000,0b00100101,  # Ascii decimal:40-47     hex:28-2F
        0b01111110,0b00110000,0b01101101,0b01111001,0b00110011,0b01011011,0b01011111,0b01110010,  # Ascii decimal:48-55     hex:30-37
        0b01111111,0b01111011,0b01001000,0b01011000,0b01000011,0b00001001,0b01100001,0b01100101,  # Ascii decimal:56-63     hex:38-3F
        0b01111101,0b01110111,0b01111111,0b01001110,0b00111101,0b01001111,0b01000111,0b01011110,  # Ascii decimal:64-71     hex:40-47
        0b00110111,0b00000110,0b00111100,0b01010111,0b00001110,0b01010100,0b01110110,0b01111110,  # Ascii decimal:72-79     hex:48-4F
        0b01100111,0b01101011,0b01100110,0b01011011,0b00001111,0b00111110,0b00111110,0b00101010,  # Ascii decimal:80-87     hex:50-57
        0b00110111,0b00111011,0b01101101,0b00011110,0b00010011,0b00110110,0b01100010,0b00001000,  # Ascii decimal:88-95     hex:58-5F
        0b00100000,0b01111101,0b00011111,0b00001101,0b00111101,0b01101111,0b01000111,0b01111011,  # Ascii decimal:96-103    hex:60-67
        0b00010111,0b00000100,0b00011000,0b01010111,0b00000110,0b00010100,0b00010101,0b00011101,  # Ascii decimal:104-111   hex:68-6F
        0b01100111,0b01110011,0b00000101,0b01011011,0b00001111,0b00011100,0b00011100,0b00010100,  # Ascii decimal:112-119   hex:70-77
        0b00110111,0b00111011,0b01101101,0b01001011,0b01010101,0b01100011,0b01000000,0b00000000   # Ascii decimal:120-127   hex:78-7F
        ]


    # constructor to create I2c7SegmentLed object, and initialize the LED module
    def __init__(self, i2cAddress, digits):
        self._digits = digits
        self._i2cAddress = i2cAddress
        self._feature = 0
        self._segments = [0,0,0,0,0,0,0,0,0]
        self._cursorPosition = 1

        # Start talking to the AS1115 chip, as it will be at i2c address 0 initially (upon powerup)

        # Power down the AS1115 chip
        try:
            i2c.write_byte_data(0x00, I2c7SegmentLed.REG_SHUTDOWN, I2c7SegmentLed.REG_SHUTDOWN_NORMAL)
        except:
            pass        # an error just means that the i2c led display has already had it's address set
        sleep(0.020)

        # tell all AS1115 chips to use their hardware jumpered i2c address
        try:
            i2c.write_byte_data(0x00, I2c7SegmentLed.REG_SELF_ADDRESSING, I2c7SegmentLed.REG_SELF_ADDRESSING_USER_ADDRESS)
        except:
            pass        # an error just means that the i2c led display has already had it's address set
        sleep(0.020)

        # power up and reset the AS1115 chip and the feature register
        self.setRegister(I2c7SegmentLed.REG_SHUTDOWN, I2c7SegmentLed.REG_SHUTDOWN_NORMAL_AND_RESET)

        # display all digits, full brightness, decoded using the hex font
        self.setBrightness(15)
        self.setRegister(I2c7SegmentLed.REG_SCAN_LIMIT,self._digits-1)   # set number of digits in use
        self.setRegister(I2c7SegmentLed.REG_DECODE_MODE,I2c7SegmentLed.REG_DECODE_MODE_NO_DIGITS)   # we won't use their decoder

        self._feature = 0                         # starting value for the _feature register
        self.setRegister(I2c7SegmentLed.REG_FEATURE,self._feature)    # initialize the feature register

        self.clear()                             # clear the display

    # write value to register
    def setRegister(self, reg, value):
        try:
            i2c.write_byte_data(self._i2cAddress, reg, value)
        except:
            print("Error writing to i2c 7 Segment Led at Address 0x%02x" %self._i2cAddress  )

    # write the 8 segments to this digit of the led
    def setSegments(self, digit, segments):
        if (digit <= self._digits) and (digit >= 1):
            self.setRegister(digit, segments)
            self._segments[digit] = segments

    # set the brightness to value (0-15)
    def setBrightness(self, value):
        self.setRegister(I2c7SegmentLed.REG_GLOBAL_INTENSITY, value)

    # clear all digits of the LED
    def clear(self):
        for i in range(1,self._digits+1):
            self._segments[i] = 0x00    # clear local storage
            self.setSegments(i,0x00)    # clear led display
        self._cursorPosition = 1        # move cursor to home position

    # move the invisible virtual cursor to the 1st position, so that the next char written will go to that digit
    def home(self):
        self.cursorMove(1)

    # move the invisible virtual cursor to specified digit
    def cursorMove(self, digit):
        if (digit <= self._digits) and (digit >= 1):
            self._cursorPosition = digit

    # turn the display off (also reduces current consumption
    def displayOff(self):
        self.setRegister(I2c7SegmentLed.REG_SHUTDOWN,I2c7SegmentLed.REG_SHUTDOWN_SHUTDOWN)

    # turn the display on
    def displayOn(self):
        self.setRegister(I2c7SegmentLed.REG_SHUTDOWN,I2c7SegmentLed.REG_SHUTDOWN_NORMAL)

    # set the brightness of the LEDs to value (0-15)
    def setBrightness(self, value):
        self.setRegister(I2c7SegmentLed.REG_GLOBAL_INTENSITY, value)

    # set the decimal point on digit specified
    def setDecimalPoint(self, digit):
        if (digit <= self._digits) and (digit >= 1):
            currentSegments = self._segments[digit] | I2c7SegmentLed.DECIMAL_POINT_MASK
            self.setSegments(digit, currentSegments)

    # clear the decimal point on digit specified
    def clearDecimalPoint(self, digit):
        if (digit <= self._digits) and (digit >= 1):
            currentSegments = self._segments[digit] & ~I2c7SegmentLed.DECIMAL_POINT_MASK
            self.setSegments(digit, currentSegments)

    # write an ascii character (value) to the led
    def write(self, value):
        # if we are not past the number of digits that we have
        if self._cursorPosition <= self._digits:
            # check if the character is a decimal point
            if value == '.':
                if self._cursorPosition == 1:
                    self.setDecimalPoint(self._cursorPosition);     # set the dp for digit 1 and inc cursorPosition
                    self._cursorPosition += 1
                else:
                    self.setDecimalPoint(self._cursorPosition-1);     # set the dp for the previous digit
            # else it is not a decimal point
            else:
                self._segments[self._cursorPosition] = I2c7SegmentLed.LedSegments[ord(value)];     # save the segments to local storage
                self.setSegments(self._cursorPosition, I2c7SegmentLed.LedSegments[ord(value)]);   # write the segments to the display
                self._cursorPosition += 1

    # write a string (including formatting options)
    # For examples of printing numbers:  https://mkaz.tech/python-string-format.html
    def writeString(self, value):
        for char in value:
            self.write(char)
