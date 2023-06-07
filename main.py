from machine import Pin, SPI
from ssd1309 import Display
from xglcd_font import XglcdFont
from time import sleep

# Define pins
din_pin = machine.Pin(19)
clk_pin = machine.Pin(18)
cs_pin = machine.Pin(17)
dc_pin = machine.Pin(16)
rst_pin = machine.Pin(20)

# Define the SPI bus
spi = SPI(0, sck=clk_pin, mosi=din_pin)

# Create an SSD1309 OLED object
oled = Display(spi, dc=dc_pin, cs=cs_pin, rst=rst_pin)

# Initialize the OLED
#oled.init_display()
#oled.clear_display()

# Font
font = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)

# Display "Hello World!"
oled.draw_text(oled.width//2, oled.height//2, "Hello", font)
oled.present()

sleep(10)

oled.cleanup()