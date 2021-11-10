"""
--------------------------------------------------------------------------
Joystick
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
This program reads the raw analog voltage value of the joysticks Vrx and Vry
and then determines the state of the motor and servo.

Analog Voltage Information
-Vrx range(AIN1): 0 to 3550, centerpoint around 1000
-Vry range(AIN2): 0 to 3550, centerpoint around 1000

"""


import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Joystick():
    """Joystick components"""
    vertical = None
    horizontal = None
    switch = None
    
    
    def __init__(self, horizontal="P1_21", vertical="P1_23", switch="P1_20"):
        "Initialize variables"
        self.vertical = vertical
        self.horizontal = horizontal
        self.switch = switch
        
        self._setup()
        
    #End def
        
    def _setup(self):
       "Setup hardware components" 
       
       #Initialize switch
       GPIO.setup(self.switch,GPIO.IN)
       
       #Initialize Analog Input
       ADC.setup()
    
    def read_analog_value(self):
        """"Reads raw analog voltage values for Vrx and Vry"""
        xvalue = ADC.read_raw(self.horizontal)
        yvalue = ADC.read_raw(self.vertical)
        
        return (xvalue,yvalue)

       
       #End def
    
    def get_direction(self):
        """Determines state of the DC motor and servo based on analog values"""
        #Import raw analog values
        (xvalue,yvalue) = self.read_analog_value()
        
        # State for the DC motor
        if yvalue <= 750:
            # Go clockwise
            ydirection = 2
        elif yvalue >= 1500:
            # Go counter-clockwise
            ydirection = 1
        else:
            # Turn off
            ydirection = 3
        
        #Directions for the servo
        if xvalue <= 750:
            # Go Right
            xdirection = 1
        elif xvalue >= 1500:
            # Go Left
            xdirection = 2
        else: 
            # Go Straight
            xdirection = 3
            
        return (xdirection,ydirection)
       
    def cleanup(self):
        """Clean up the hardware components"""
        GPIO.cleanup()
        
    #End def
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    #Create instantiation of the joystick program
    joystick=Joystick()

