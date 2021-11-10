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
This program user a reciever to collect data from the joystick in the reomte control.
The data is then intepreted into directions which control the dc motor throuhg the L293D motor controller and the servo.
The program additionaly has a led to indicate the program is running and a button to halt the program.

Requirements:
   -Move the DC motor and servo in the direction corresponding to the movement of the joystick.
   -Halt the program when the button is pressed.
   
Uses:
    -The receiver library contained within the onboard directory


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

payload_fmt = "<2b"                    # The receiver and transmitter payload formats

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Onboard():
    """Onboard Components"""
    servo = None
    rcvr=None
    enable=None
    in1=None
    in2=None
    button=None
    green_led=None
    
    def __init__(self, enable="P2_2", in1="P1_6", in2="P1_8",servo="P2_1",
                 button="P1_36", green_led="P1_35"):
         """ Initialize variables and begin set up"""
         self.servo = servo
         self.rcvr = receiver.Receiver()
         self.enable = enable
         self.in1 = in1
         self.in2 = in2
         self.button = button
         self.green_led = green_led
         
         self._setup()
    
    def _setup(self):
        """Setup the hardware components"""
        
        #Intialize the L293D
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        
        #Intialize the LED
        GPIO.setup(self.green_led, GPIO.OUT)

        
        # Initialize Servo; Servo should be "off"
        PWM.start(self.servo, SG90_STRAIGHT, SG90_FREQ, SG90_POL)
        
        #Initialize the Receiver
        self.rcvr._setup()
        
        # Initialize Button
        GPIO.setup(self.button, GPIO.IN)

        
    def turn_left(self):
        """Turns the servo to the left"""
        #Set servo
        PWM.set_duty_cycle(self.servo, SG90_LEFT)
        
    def turn_right(self):
        """Turns the servo to the right"""
        #Set servo
        PWM.set_duty_cycle(self.servo, SG90_RIGHT)
    
    def go_straight(self):
        """Turns the servo to the middle position"""
        #Set servo
        PWM.set_duty_cycle(self.servo, SG90_STRAIGHT)
        
    def forward(self):
        """Turns the DC motor clockwise"""
        #Set GPIOs
        GPIO.output(self.enable,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        
    def backward(self):
        """Turns the DC motor counter-clockwise"""
        #Set GPIOs
        GPIO.output(self.enable,GPIO.HIGH)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
    
    def motor_stop(self):
        """Turns the DC motor off"""
        #Set GPIOs
        GPIO.output(self.enable,GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        
    def run(self):
        """Execute the main program
           -Collects the payload data from the reciever
           -Employs that data to determine the state of the servo and motor
           -Halts program once button is pressed and cleans up the hardware components
        """
        #Runs the program until the button is pressed
        while(GPIO.input(self.button)==1):
            
            #Turn on the LED
            GPIO.output(self.green_led,GPIO.HIGH)
            
            #Collect delivered payload from the reciever
            (payload) = self.rcvr.slave(payload_fmt)
            
            #Ensures that if no payload is received then xdirection and ydirection still have a value
            if payload is None:
                xdirection = 0
                ydirection = 0
            
            else:
                xdirection = payload[0]
                ydirection = payload[1]
                
                
            if xdirection == 1
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
        
        #Begins cleanup function after the button is pressed
        self.cleanup()
        
    #End def
            
        
    def cleanup(self):
        """Cleanup the Hardware components"""
        #Clean up the GPIOs
        GPIO.output(self.green_led,GPIO.LOW)
        GPIO.output(self.enable, GPIO.LOW)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.cleanup()
        
        #Clean up the servo
        PWM.stop(self.servo)
        PWM.cleanup()
        
        #Clean up the receiver
        self.rcvr.cleanup()
        
        



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Program Start")
    #Create instantiation of the onboard program
    onboard = Onboard()
    
    try: 
        #Runs the onboard program
        onboard.run()
    
    except KeyboardInterrupt:
        
    print("Program Complete")
