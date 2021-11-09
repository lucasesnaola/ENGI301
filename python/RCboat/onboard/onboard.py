"""
--------------------------------------------------------------------------
Onboard Components
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
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import receiver



# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

SG90_FREQ        = 50                  # 20ms period (50Hz)
SG90_POL         = 0                   # Rising Edge polarity
SG90_STRAIGHT    = 7.5                 # 0ms pulse -- Servo is inactive
SG90_RIGHT       = 5                   # 1ms pulse (5% duty cycle)  -- All the way right
SG90_LEFT        = 10                  # 2ms pulse (10% duty cycle) -- All the way Left

payload_fmt = "<2b"

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Onboard():
    servo = None
    rcvr=None
    enable=None
    in1=None
    in2=None
    button=None
    green_led=None
    
    def __init__(self, enable="P2_2", in1="P1_6", in2="P1_8",servo="P2_1",
                 button="P1_36", green_led="P1_35"):
         """ Initialize variables and set up display """
         self.servo = servo
         self.rcvr = receiver.Receiver()
         self.enable = enable
         self.in1 = in1
         self.in2 = in2
         self.button = button
         self.green_led = green_led
         
         self._setup()
    
    def _setup(self):
        
        #Intialize the L293D
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        
        #Intialize the LED
        GPIO.setup(self.green_led, GPIO.OUT)

        
        # Initialize Servo; Servo should be "off"
        PWM.start(self.servo, SG90_STRAIGHT, SG90_FREQ, SG90_POL)
        
        self.rcvr._setup()
        
        # Initialize Button
        GPIO.setup(self.button, GPIO.IN)

        
    def turn_left(self):
        PWM.set_duty_cycle(self.servo, SG90_LEFT)
        
    def turn_right(self):
        PWM.set_duty_cycle(self.servo, SG90_RIGHT)
    
    def go_straight(self):
        PWM.set_duty_cycle(self.servo, SG90_STRAIGHT)
        
    def forward(self):
        GPIO.output(self.enable,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        
    def backward(self):
        GPIO.output(self.enable,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
    
    def motor_stop(self):
        GPIO.output(self.enable,GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        
    def run(self):
        
        while(GPIO.input(self.button)==1):
            
            GPIO.output(self.green_led,GPIO.HIGH)
            
            (payload) = self.rcvr.slave(payload_fmt)
            
            if payload is None:
                xdirection = 0
                ydirection = 0
            
            else:
                xdirection = payload[0]
                ydirection = payload[1]
                
            print("xdirection=",xdirection)
            print("ydirection=",ydirection)
                
                
            if xdirection == 1:
                self.turn_right()
            
            if xdirection == 2:
                self.turn_left()
            
            if xdirection == 3:
                self.go_straight()
            
            if ydirection == 2:
                self.forward()
            
            if ydirection == 1:
                self.backward()
                
            if ydirection == 3:
                self.motor_stop()

            time.sleep(0.2)
            
        self.cleanup()
        
    #End def
            
        
    def cleanup(self):
        GPIO.output(self.green_led,GPIO.LOW)
        GPIO.output(self.enable, GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        
        PWM.stop(self.servo)
        PWM.cleanup()
        GPIO.cleanup()
        self.rcvr.cleanup()
        
        



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Program Start")
    onboard = Onboard()
    
    try: 
        onboard.run()
    
    except KeyboardInterrupt:
        onboard.cleanup()
        
    print("Program Complete")