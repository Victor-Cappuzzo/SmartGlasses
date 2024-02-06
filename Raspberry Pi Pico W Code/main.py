from machine import Pin, SPI, UART
from ssd1309 import Display
from xglcd_font import XglcdFont
from time import sleep
from message import Message

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

# Define a font
#font = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
font = XglcdFont('fonts/Bally5x8.c', 5, 8)

# Define global variables for display parameters
CODE_LEN = 4 # length of code delimiter
SCROLL_TIME = 1 # time needed to pass for the text to move when scrolling [seconds]

# Define typed message
typed_x_pos = 4*oled.width//5
typed_y_pos = oled.height//2
typed_message = Message("", typed_x_pos, typed_y_pos, font, rot, horz_offset, vert_offset, SCROLL_TIME, oled)

# Define time message
time_x_pos = 3*oled.width//5
time_y_pos = oled.height//2
time_message = Message("", time_x_pos, time_y_pos, font, rot, horz_offset, vert_offset, SCROLL_TIME, oled)

# Define battery percentage message
batper_x_pos = 2*oled.width//5
batper_y_pos = oled.height//2
batper_message = Message("", batper_x_pos, batper_y_pos, font, rot, horz_offset, vert_offset, SCROLL_TIME, oled)

# Define battery charging message
charge_x_pos = oled.width//5
charge_y_pos = oled.height//2
charge_message = Message("", charge_x_pos, charge_y_pos, font, rot, horz_offset, vert_offset, SCROLL_TIME, oled)

# Define code array (NOTE: messages in the message_array must be in the same order as the code_array!)
# Codes:
# 	M --> Typed message (for debugging)
#	T --> Time and date
#	P --> Battery percentage
#	C --> Charging status
#	N --> Notification and count
code_array = ["M:::", "T:::", "P:::", "C:::"]

# Define message array
message_array = [typed_message, time_message, batper_message, charge_message]


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
        
        """
        # If the message code is M::: --> typed message
        if code == "M:::":
            
            # Update the typed message variable
            typed_message.setMessage(message[CODE_LEN:len(message)])
            
            # Check if the message is scrollable
            typed_message.determineScrollable()
        
        # If the message code is T::: --> time
        if code == "T:::":
            
            # Update the time variable
            time_message.setMessage(message[CODE_LEN:len(message)])
            
            # Check if the message is scrollable
            time_message.determineScrollable()
            
        # If the message code is P::: --> battery percentage
        if code == "P:::":
            
            # Update the battery percentage variable
            batper_message.setMessage(message[CODE_LEN:len(message)])
            
            # Check if the message is scrollable
            batper_message.determineScrollable()
            
        # If the message code is C::: --> charging status
        if code == "C:::":
            
            # Update the battery charging variable
            charge_message.setMessage(message[CODE_LEN:len(message)])
            
            # Check if the message is scrollable
            charge_message.determineScrollable()
            
    # Concatenate all messages into an array
    message_array = [typed_message, time_message, batper_message, charge_message]
    
        
    # Loop through each message
    for m in message_array:
        
        # Check if the message is scrollable
        #m.determineScrollable()
        
        # Draw the message
        m.drawMessage()
    """
        
        # Loop through each message/code
        for i in range(len(message_array)):
            
            # Get current code and message
            c = code_array[i]
            m = message_array[i]
            
            # Check if the code matches the current message's code
            if code == c:
                
                # Update the message variable
                m.setMessage(message[CODE_LEN:len(message)])
                
                # Check if the message is scrollable
                m.determineScrollable()
                
    # Display each message
    for m in message_array:
        
        # Check if the message is scrollable
        #m.determineScrollable()
        
        # Draw the message
        m.drawMessage()
    
    oled.present()
        
    

        