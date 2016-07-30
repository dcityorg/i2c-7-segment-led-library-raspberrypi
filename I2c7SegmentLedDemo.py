# -*- coding: utf-8 -*-

# Notes
#   1. You must enable I2C on your Raspberry Pi board (see your particular operating system documentation).
#       On Raspian: Menu...Preferences...Raspberry Pi Configuration...Interfaces...Enable I2C
#   2. If using Python 3, you will need to install python3-smbus:
#       sudo apt-get install python3-smbus

'''
  I2c7SegmentLed.py - class library for using 7 Segment Leds

  Written by: Gary Muhonen  gary@wht.io

  versions
    1.0.0 - 7/31/2016
      Original Release.


  Short Description:

    These files provide software for the Raspberry Pi, using the Python2 or Python3
    The library files provide useful functions to make it easy
    to communicate with 7 Segment LED display modules that use the AMS AS1115
    LED controller chip. This chip uses the I2C communication protocol. The demo
    program shows the usage of the functions in the library.

    The library files and demo will work with 7 segment LED displays with up to
    8 digits. The LED display must use the AMS AS1115 controller chip.

    See the links below for installation and usage information.

    Project Details:
    * Library installation and usage:                  http://wht.io/portfolio/i2c-7-segment-led-library/
    * .8 inch,  7 Segment module hardware information: http://wht.io/portfolio/i2c-7-segment-led-backpack-dot8inch
    * .56 inch, 7 Segment module hardware information: http://wht.io/portfolio/i2c-7-segment-led-backpack-dot56inch
    * .36 inch, 7 Segment module hardware information: http://wht.io/portfolio/i2c-7-segment-led-backpack-dot36inch

    Software Github repositories (library and demo programs):
    * Arduino library files:      https://github.com/wht-io/i2c-7-segment-led-library-arduino.git
    * Particle library files:     https://github.com/wht-io/i2c-7-segment-led-library-particle.git
    * Raspberry Pi library files: https://github.com/wht-io/i2c-7-segment-led-library-raspberrypi.git

    Hardware Design Github repositories (schematic and board layouts):
    * .8 inch,  7 Segment module design: http://wht.io/portfolio/i2c-7-segment-led-backpack-dot8inch
    * .56 inch, 7 Segment module design: http://wht.io/portfolio/i2c-7-segment-led-backpack-dot56inch
    * .36 inch, 7 Segment module design: http://wht.io/portfolio/i2c-7-segment-led-backpack-dot36inch    See the project details links below for installation and usage information.

    Github repositories:
    * Raspberry Pi library files:  https://github.com/wht-io/i2c-7-segment-led-raspberrypi.git
    * Arduino library files:  https://github.com/wht-io/i2c-7-segment-led-arduino.git
    * Particle library files: https://github.com/wht-io/i2c-7-segment-led-particle.git

    Project Details:

    * Library installation and usage: http://wht.io/portfolio/i2c-7-segment-led-library/
    * 7 Segment module hardware information: http://wht.io/portfolio/i2c-7-segment-led-board/



  Windy Hill Technology LLC code, firmware, and software is released under the
  MIT License (http://opensource.org/licenses/MIT).

  The MIT License (MIT)

  Copyright (c) 2016 Windy Hill Technology LLC

  Permission is hereby granted, free of charge, to any person obtaining a
  copy of this software and associated documentation files (the "Software"),
  to deal in the Software without restriction, including without limitation
  the rights to use, copy, modify, merge, publish, distribute, sublicense,
  and/or sell copies of the Software, and to permit persons to whom the
  Software is furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included
  in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
  DEALINGS IN THE SOFTWARE.

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
