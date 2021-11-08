#X range (AIN0) 0 (up-down) to 3550 centerpoint around 1000
#Y range (AIN1) 0 (left-right) to 3550 centerpoint around 1000

import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Joystick():
    vertical = None
    horizontal = None
    switch = None
    
    
    def __init__(self, horizontal="P1_21", vertical="P1_23", switch="P1_20"):
        "Initialize variables and set up display"
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
        
        xvalue = ADC.read_raw(self.horizontal)
        yvalue = ADC.read_raw(self.vertical)
        
        return (xvalue,yvalue)

       
       #End def
    
    def get_direction(self):
        
        (xvalue,yvalue) = self.read_analog_value()
        #print("xvalue =",xvalue)
        #print("yvalue =",yvalue)
        
        if yvalue <= 750:
            # Go forward
            ydirection = 2
        elif yvalue >= 1500:
            # Go backward
            ydirection = 1
        else:
            # Turn off
            ydirection = 3
            
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
        
        GPIO.cleanup()
        
    #End def
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    joystick=Joystick()

