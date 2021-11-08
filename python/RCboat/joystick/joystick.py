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
    
    
    def __init__(self, vertical="P1_19", horizontal="P1_21", switch="P1_20"):
        "Initialize variables and set up display"
        self.vertical = vertical
        self.horizontal = horizontal
        self.switch = switch
        
        self.setup()
        
    #End def
        
    def setup(self):
       "Setup hardware components" 
       
       #Initialize switch
       GPIO.setup(self.switch,GPIO.IN)
       
       #Initialize Analog Input
       ADC.setup()
    
    def read_analog_value(self):
        
        xvalue = ADC.read_raw(self.vertical)
        yvalue = ADC.read_raw(self.horizontal)
        
        print(xvalue)
        print(yvalue)
        
        return (xvalue,yvalue)

       
       #End def
    
    def get_direction(self):
        (xvalue,yvalue) = self.read_analog_value()
        
        if yvalue >= 1500:
        # Go forward
            ydirection = True
        
        if yvalue <= 750:
        # Go backward
            ydirection = False
            
        if xvalue <= 750:
        # Go Left
            xdirection = False
            
        if xvalue >= 1500:
        # Go right
            xdirection = True
            
        return (xdirection,ydirection)
       
    def cleanup(self):

        GPIO.output(self.switch, GPIO.LOW)
        
        GPIO.cleanup()
        
    #End def
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    joystick=Joystick()
    
    try:
        (xvalue,yvalue) = joystick.read_analog_value()
        
        
    except KeyboardInterrupt:
        joystick.cleanup()
    