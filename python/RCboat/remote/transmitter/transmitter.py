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
import board
import digitalio
import Adafruit_BBIO.GPIO as GPIO

from circuitpython_nrf24l01.rf24 import RF24

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------




# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Receiver():
    ce_pin = None
    csn_pin = None
    spi_bus = None
    
    def __init__(self, clk_pin=board.SCLK_1, miso_pin=board.MISO_1, mosi_pin = board.MOSI_1,
                ce_pin=board.P2_24, csn_pin=board.P2_22):
                
        #Configuration of ce and csn pins
        self.ce_pin = digitalio.DigitalInOut(ce_pin)
        self.csn_pin = digitalio.DigitalInOut(csn_pin)
        
        # Setup SPI bus using hardware SPI
        self.spi_bus = busio.SPI(clock=clk_pin, MISO=miso_pin, MOSI=mosi_pin)
        
        self.setup()
        
    #End def
    
    def _setup(self):
        
        nrf = RF24(spi_bus, csn_pin, ce_pin)
        
        # set the Power Amplifier level to -12 dBm since this test example is
        # usually run with nRF24L01 transceivers in close proximity
        nrf.pa_level = -12
        
        # set RX address of TX node into an RX pipe
        nrf.open_rx_pipe(b"1Node")  # using pipe 0
        
    #End def
    
    def master(self,payload):
        """Polls the radio and prints the received value. This method expires
        after 6 seconds of no received transmission"""
        nrf.listen = False # put radio into TX mode and power up
        
        if nrf.available():
            # use struct.pack to packetize your data
            # into a usable payload
            buffer = struct.pack("<f", payload[0])
                
                
                
                
    #End def
                
#End def

        
# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    transmitter=Transmitter()
      