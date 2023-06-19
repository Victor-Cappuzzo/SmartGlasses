from machine import Pin, SPI, UART
from ssd1309 import Display
from xglcd_font import XglcdFont
from time import sleep

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
font = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)

# Recieve UART messages
while True:
    
    # If we have received a message
    if uart.any():
        
        sleep(0.1)
        
        # Grab the message
        message = uart.readline().decode().strip()  # Decode the received bytes and remove whitespace
        message = message.replace('\r', '')  # Remove carriage return character
        print(message)
        
        # Display message to the OLED
        text_len = font.measure_text(message)
        oled.draw_text(oled.width//2 + text_len//2, oled.height//2, message, font, rotate=180)
        oled.present()

        sleep(10)

        oled.clear()
        