from machine import Pin, SPI, UART
from ssd1309 import Display
from xglcd_font import XglcdFont
from time import sleep

# Define screen orientation and text offsets
rot = 90
horz_offset = 0.5
vert_offset = 0

# Change text offsets based on screen orientation
if rot == 0:
    horz_offset = -0.5
    vert_offset = 0
if rot == 90:
    horz_offset = 0
    vert_offset = -0.5
if rot == 180:
    horz_offset = 0.5
    vert_offset = 0
if rot == 270:
    horz_offset = 0
    vert_offset = 0.5


# Define pins for OLED
din_pin = machine.Pin(19)
clk_pin = machine.Pin(18)
cs_pin = machine.Pin(17)
dc_pin = machine.Pin(16)
rst_pin = machine.Pin(20)

# Define pins for UART
tx_pin = machine.Pin(0)
rx_pin = machine.Pin(1)

# Define UART object on UART0 ports
uart = UART(0, baudrate=9600, tx=tx_pin, rx=rx_pin)

# Define the SPI bus on SPI0 ports
spi = SPI(0, sck=clk_pin, mosi=din_pin)

# Create an SSD1309 OLED object
oled = Display(spi, dc=dc_pin, cs=cs_pin, rst=rst_pin)

# Font
#font = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
font = XglcdFont('fonts/Bally5x8.c', 5, 8)

# Define global variables for stuff to display
CODE_LEN = 4
time = ""
typed_message = ""

# Recieve UART messages
while True:
    
    # If we have received a message
    if uart.any():
        
        # Clear the display so that it can be updated
        oled.clear()
        
        sleep(0.1)
        
        # Grab the message
        message = uart.readline().decode().strip()  # Decode the received bytes and remove whitespace
        message = message.replace('\r', '')  # Remove carriage return character
        print(message)
        
        # Determine what the message code is
        code = message[0:CODE_LEN]
        
        # If the message code is M::: --> typed message
        if code == "M:::":
            
            # Update the typed message variable
            typed_message = message[CODE_LEN:len(message)]
            
            
        # Display typed message to the OLED
        text_len = font.measure_text(typed_message)
        oled.draw_text(2*oled.width//3 + round(text_len*horz_offset), oled.height//2 + round(text_len*vert_offset), typed_message, font, rotate=rot)
        #oled.present()
            
        # If the message code is T::: --> time
        if code == "T:::":
            
            # Update the time variable
            time = message[CODE_LEN:len(message)]
        
        # Display time to the OLED
        text_len = font.measure_text(time)
        oled.draw_text(oled.width//3 + round(text_len*horz_offset), oled.height//2 + round(text_len*vert_offset), time, font, rotate=rot)
        #oled.draw_text(oled.width//2, oled.height//2 - text_len//2, time, font, rotate=rot)
        
        oled.present()

        #sleep(10)

        #oled.clear()
        