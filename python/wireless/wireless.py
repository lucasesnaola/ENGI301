# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Wireless Library
--------------------------------------------------------------------------
License:   
Copyright 2021 Erik Welsh

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
Software API:

  Wireless()


--------------------------------------------------------------------------
Background Information: 

Links:
  - https://circuitpython-nrf24l01.readthedocs.io/en/latest/
  - https://circuitpython-nrf24l01.readthedocs.io/en/latest/examples.html#simple-test

Software Setup:
  - sudo apt-get update
  - sudo pip3 install circuitpython-nrf24l01

"""
import time
import busio
import board
import digitalio
import struct

from circuitpython_nrf24l01.rf24 import RF24

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
TX       = 0
RX       = 1


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class Wireless():
    """ Class to manage an Wireless device """
    ce_pin    = None
    cs_pin    = None
    spi_bus   = None
    pa_level  = None
    address   = None
    role      = None 
    device    = None
    
    def __init__(self, role, address=[b'1Node', b'2Node'],
                       clk_pin=board.SCLK, miso_pin=board.MISO, mosi_pin=board.MOSI,
                       cs_pin=board.P1_6, ce_pin=board.P1_4, pa_level=-12):
        """ SPI Display Constructor
        
        :param clk_pin   : Value must be a pin from adafruit board library
        :param miso_pin  : Value must be a pin from adafruit board library
        :param mosi_pin  : Value must be a pin from adafruit board library
        :param cs_pin    : Value must be a pin from adafruit board library
        :param ce_pin    : Value must be a pin from adafruit board library

        """
        # Set class variables
        self.pa_level  = pa_level
        self.address   = address
        self.role      = role
        
        # Configuration for CS and CE pins:
        self.ce_pin    = digitalio.DigitalInOut(ce_pin)
        self.cs_pin    = digitalio.DigitalInOut(cs_pin)

        # Setup SPI bus using hardware SPI
        self.spi_bus   = busio.SPI(clock=clk_pin, MISO=miso_pin, MOSI=mosi_pin)

        # Create the ILI9341 display:
        self.device    = RF24(self.spi_bus, self.cs_pin, self.ce_pin)
        
        # Initialize Hardware
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Initialize the display itself"""
        # Set PA level
        self.device.pa_level = -12
        
        if self.role == TX:
            self.device.open_tx_pipe(self.address[0])
            self.device.open_rx_pipe(1, self.address[1])
        elif self.role == RX:
            self.device.open_tx_pipe(self.address[1])
            self.device.open_rx_pipe(1, self.address[0])
        else:
            raise ValueError("Error:  Role not defined")

    # End def    


    def transmit(self, payload, payload_fmt):
        """Transmits an incrementing integer every second"""
        self.device.listen = False  # ensures the nRF24L01 is in TX mode
    
        buffer = struct.pack(payload_fmt, *payload)
        
        if (False):
            print(buffer)

        result = self.device.send(buffer)

        if not result:
            print("send() failed or timed out")
    
    # End def


    def receive(self, payload_fmt, timeout):
        """Polls the radio and prints the received value. This method expires
        after 6 seconds of no received transmission"""
        self.device.listen = True  # put radio into RX mode and power up
        
        payload = None
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
                
                return payload

        # recommended behavior is to keep in TX mode while idle
        self.device.listen = False  # put the nRF24L01 is in TX mode

    # End def


# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time
    import threading

    delay = 1
    
    print("Wireless:")
    
    print("Create Transmitter")
    xmit = Wireless(clk_pin=board.SCLK, miso_pin=board.MISO, mosi_pin=board.MOSI,
                    cs_pin=board.P1_6, ce_pin=board.P1_4, role=TX)

    print("Create Receiver")
    rcvr = Wireless(clk_pin=board.SCLK_1, miso_pin=board.MISO_1, mosi_pin=board.MOSI_1,
                    cs_pin=board.P2_31, ce_pin=board.P2_33, role=RX)


    payload_fmt = "<2b"
    payload     = [0,1]

    thread1 = threading.Thread(target=rcvr.receive, args=(payload_fmt, 20,))    
    thread1.start()
    time.sleep(1)
    
    print("Transmitting Packet")
    
    xmit.transmit(payload, payload_fmt)
    
    thread1.join()

    print("Test Finished.")



