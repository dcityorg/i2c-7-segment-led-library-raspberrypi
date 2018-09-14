# -*- coding: utf-8 -*-

'''
    I2c7SegmentLedDemo.py

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


    This demo program is public domain. You may use it for any purpose.
        NO WARRANTY IS IMPLIED.

    License Information:  https://www.dcity.org/license-information/

    Notes:
        1. You must enable I2C on your Raspberry Pi board (see your particular operating system documentation).
            On Raspian: Menu...Preferences...Raspberry Pi Configuration...Interfaces...Enable I2C
        2. This software was tested on a RASPBERRY PI 3 MODEL B, running Rasbian and Python 3.5.2

'''

from I2c7SegmentLed import I2c7SegmentLed
from time import sleep

if __name__ == "__main__":

    I2C_LED_ADDRESS = 0x03           # i2c address for the 7 segment led module
    LED_DIGITS = 4                   # number of digits in the 7 segment led module
    TESTNUM = 2                      # number of times to repeat each of the following test cases

    led = I2c7SegmentLed(I2C_LED_ADDRESS, LED_DIGITS)    # create led display object

    while 1:                         # keep running this program until ctrl C is pressed

        # display some typical messages on led
        # For examples of printing numbers:  https://mkaz.tech/python-string-format.html
        led.clear()
        led.writeString("Typ")
        temp = 72
        pH = 7.02
        for i in range(0,TESTNUM):
            led.clear()

            led.writeString("T=%s" %temp)
            sleep(1)
            led.clear()
            led.writeString("pH=")
            sleep(1)
            led.clear()
            led.writeString("%s" %pH)
            sleep(1)

        # test displaying ASCII strings
        led.clear()
        led.writeString("ASCI")
        sleep(1)
        for i in range(0,TESTNUM):
            led.clear()
            led.writeString("ABCD")
            sleep(1)
            led.clear()
            led.writeString("EFGH")
            sleep(1)
            led.clear()
            led.writeString("abcd")
            sleep(1)
            led.clear()
            led.writeString("efgh")
            sleep(1)

        # test displaying floating point numbers containing decimal points
        led.clear()
        led.writeString("FLT")
        sleep(1)
        for i in range(0,TESTNUM):
            led.clear()
            led.writeString("%s" %.678)
            sleep(1)
            led.clear()
            led.writeString("%s" %5.678)
            sleep(1)
            led.clear()
            led.writeString("%s" %56.78)
            sleep(1)
            led.clear()
            led.writeString("%s" %567.8)
            sleep(1)
            led.clear()
            led.writeString("%s" %5678.)
            sleep(1)

        # test displaying all ASCII characters
        led.clear()
        led.writeString("ASCI")
        sleep(1)
        for i in range(0,TESTNUM):
            for j in range(0, 128):
                led.clear()
                led.write(chr(j))
                sleep(.1)

        # test the clear command
        led.clear()
        for i in range(0,TESTNUM):
            led.writeString("Clr")
            sleep(1)
            led.clear()
            sleep(1)

        # test the cursor home command
        led.clear()
        led.writeString("HOME")
        sleep(1)
        for i in range(0,TESTNUM):
            led.clear()
            led.writeString("HOME")
            sleep(1)
            led.home()
            sleep(1)
            led.writeString("1")
            sleep(.500)
            led.writeString("2")
            sleep(.500)
            led.writeString("3")
            sleep(.500)
            led.writeString("4")
            sleep(.500)

        # test the cursor move command
        led.clear()
        led.writeString("MOVE")
        for i in range(0,TESTNUM):
            led.clear()
            led.writeString("MOVE")
            sleep(1)
            led.cursorMove(4)
            led.writeString(" ")
            sleep(1)
            led.cursorMove(3)
            led.writeString(" ")
            sleep(1)
            led.cursorMove(2)
            led.writeString(" ")
            sleep(1)
            led.cursorMove(1)
            led.writeString(" ")
            sleep(1)

        # test the display on/off commands
        led.clear()
        led.writeString("OFF")
        sleep(1)
        for i in range(0,TESTNUM):
            led.displayOn()
            sleep(1)
            led.displayOff()
            sleep(1)
            led.displayOn()

        # test the set segments command, where you control the individual segments of the LED
        # The 7 LED segments and the decimal point are arranged as (from MSB to LSB)
        #    DP A B C D E F G   (DP, top, top right, btm right, btm, btm left, top left, middle)
        led.clear()
        led.writeString("SEG")
        sleep(1)
        led.clear()
        for i in range(0,TESTNUM):
            led.setSegments(1, 0x36)       # turn on side segments
            sleep(1)
            led.setSegments(1, 0x48)       # turn on top and bottom segments
            sleep(1)

        # test the setBrightness command.
        led.clear()
        led.writeString("BRIT")
        sleep(1)
        for i in range(0,TESTNUM):
            led.setBrightness(0)       # set brightness to min
            sleep(1)
            led.setBrightness(15)       # set brightness to max
            sleep(1)

        # test the setDecimalPoint and clearDecimalPoint command.
        led.clear()
        led.writeString("DP")
        sleep(1)
        for i in range(0,TESTNUM):
            led.setDecimalPoint(3)         # set the dp on the 1st digit
            sleep(1)
            led.clearDecimalPoint(3)       # clear the dp on the 1st digit
            sleep(1)
