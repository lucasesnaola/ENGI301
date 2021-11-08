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
import struct
import busio
import board
import digitalio
import Adafruit_BBIO.GPIO as GPIO

from circuitpython_nrf24l01.rf24 import RF24

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

payload_fmt = "<2b"

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Receiver():
    ce_pin = None
    csn_pin = None
    spi_bus = None
    pa_level = None
    address = None
    device = None
    
    def __init__(self, address=[b'1Node', b'2Node'], clk_pin=board.SCLK_1, 
                    miso_pin=board.MISO_1, mosi_pin = board.MOSI_1,
                    ce_pin=board.P2_24, csn_pin=board.P2_22, pa_level=-12):
                        
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
        """Initialize the display itself"""
        # set the Power Amplifier level to -12 dBm since this test example is
        # usually run with nRF24L01 transceivers in close proximity
        self.device.pa_level = -12

        self.device.open_tx_pipe(self.address[1])
        self.device.open_rx_pipe(1, self.address[0])
        
    #End def
    
    def slave(self, payload_fmt, timeout=6):
        """Polls the radio and prints the received value. This method expires
        after 6 seconds of no received transmission"""
        self.device.listen = True  # put radio into RX mode and power up
        
        start   = time.time()

        while (time.time() - start) < timeout:
            
            if self.device.available():
                
                # grab information about the received payload
                payload_size, pipe_number = (self.device.any(), self.device.pipe)
                
                # fetch 1 payload from RX FIFO
                buffer = self.device.read()  # also clears nrf.irq_dr status flag
                
               
                payload = struct.unpack(payload_fmt, buffer)
                
                if (False):       
                    print(payload)
                 
                xdirection = payload[0]
                ydirection = payload[1]
                
                start = time.time()
                
            else: 
                xdirection = 3
                ydirection = 3
                
            return (xdirection,ydirection)
                
                
    #End def
                
    def cleanup(self):
    
        self.device.listen = False #Put the nRF24L01 in TX mode when idle
        
    #End def

#End def

        
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    receiver=Receiver()
      
    