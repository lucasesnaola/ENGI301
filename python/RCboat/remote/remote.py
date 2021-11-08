"""
--------------------------------------------------------------------------
Remote Components
--------------------------------------------------------------------------
License:   
Copyright 2020 Lucas Esnaola

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
"""
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import serial

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
SG90_FREQ       = 50        # 20ms period (50Hz)
SG90_POL        = 0         # Rising Edge polarity
SG90_STRAIGHT   = 7.5       # 1.5 ms pulse (7.5% duty cycle) -- In the middle
SG90_RIGHT      = 5         # 1 ms pulse (5% duty cycle) -- All the way Right
SG90_LEFT       = 10        # 2ms pulse (10% duty cycle) -- All the way Left

SG90_OFF    = SG90_CLOSE          # Set the "off" state to "closed"

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    pass