# -*- coding: utf-8 -*-


"""
--------------------------------------------------------------------------
USR3 Blink
--------------------------------------------------------------------------
License:   
Copyright 2021 Lucas Esnaola
Copyright (c) 2014 MIT OpenCourseWare
Copyright (c) 2017 Adafruit Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
--------------------------------------------------------------------------
Simple program that will flash the BBB on-board USR3 led at a frequency of 5 Hz


--------------------------------------------------------------------------
"""

#Supports use of input function for Python2
try:
    input = raw_input
except NameError:
    pass

import time

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------



# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

#Sets the intial status for the led as on
with open("/sys/class/leds/beaglebone:green:usr3/brightness", 'w') as f:
    f.write("1")

while True:
#Flashes the led at a frequency of 5 Hz until the program is ended
    with open("/sys/class/leds/beaglebone:green:usr3/brightness", 'w') as f: #Turns led on
        f.write("0")
    time.sleep(0.1) #Contols the interval between the led switching 
    
    with open("/sys/class/leds/beaglebone:green:usr3/brightness", 'w') as f: #Turns led off
        f.write("1")
    time.sleep(0.1)
    
    
    


