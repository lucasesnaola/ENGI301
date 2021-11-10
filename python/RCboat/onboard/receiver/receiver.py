"""
--------------------------------------------------------------------------
Receiver
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
This program receives the payload data sent out by the transmitter on the remote control

Software Setup:
  - sudo apt-get update
  - sudo pip3 install circuitpython-nrf24l01
  
 Links:
  - https://circuitpython-nrf24l01.readthedocs.io/en/latest/
  - https://circuitpython-nrf24l01.readthedocs.io/en/latest/examples.html#simple-
test
"""

import time
import struct
import busio
import board
import digitalio
import Adafruit_BBIO.GPIO as GPIO

from circuitpython_nrf24l01.rf24 import RF24

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

payload_fmt = "<2b"             # The receiver and transmitter payload formats

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Receiver():
    """Receiver components"""
    ce_pin = None
    csn_pin = None
    spi_bus = None
    pa_level = None
    address = None
    device = None
    
    def __init__(self, address=[b'1Node', b'2Node'], clk_pin=board.SCLK_1, 
                    miso_pin=board.MISO_1, mosi_pin = board.MOSI_1,
                    ce_pin=board.P2_24, csn_pin=board.P2_22, pa_level=-12):
        """ Initialize variables and begin set up"""
                        
        # Set class variables
        self.pa_level  = pa_level
        self.address   = address
                
        #Configuration of ce and csn pins
        self.ce_pin = digitalio.DigitalInOut(ce_pin)
        self.csn_pin = digitalio.DigitalInOut(csn_pin)
        
        # Setup SPI bus using hardware SPI
        self.spi_bus = busio.SPI(clock=clk_pin, MISO=miso_pin, MOSI=mosi_pin)
        
        # Create the ILI9341 display:
        self.device = RF24(self.spi_bus, self.csn_pin, self.ce_pin)
        
        #Initialize Hardware
        self._setup()
        
    #End def
    
    def _setup(self):
        """Initialize the receiver itself"""
        # set the Power Amplifier level to -12 dBm since this test example is
        # usually run with nRF24L01 transceivers in close proximity
        self.device.pa_level = -12
        
        # set RX address of TX node into an RX pipe
        self.device.open_tx_pipe(self.address[1])
        self.device.open_rx_pipe(1, self.address[0])
        
    #End def
    
    def slave(self, payload_fmt, timeout=6):
        """Polls the radio and prints the received value. This method expires
        after 6 seconds of no received transmission"""
        self.device.listen = True  # put radio into RX mode and power up
        
        start   = time.time()
        payload = None
        
        while (time.time() - start) < timeout:
            
            if self.device.available():
                
                # grab information about the received payload
                payload_size, pipe_number = (self.device.any(), self.device.pipe)
                
                # fetch payload from RX FIFO
                buffer = self.device.read()  # also clears nrf.irq_dr status flag
                
                # Unpack the payload
                payload = struct.unpack(payload_fmt, buffer)
                
                if (False):       
                    print(payload)
                 
                return (payload)
                
            
                
                
    #End def
                
    def cleanup(self):
        """Clean up the hardware components"""
    
        self.device.listen = False #Put the nRF24L01 in TX mode when idle
        
    #End def

#End def

        
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    #Create instantiation of the receiver program
    receiver=Receiver()
      
    
