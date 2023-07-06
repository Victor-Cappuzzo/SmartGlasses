"""
Victor Cappuzzo

Class for a Message object
"""

from ssd1309 import Display
from xglcd_font import XglcdFont
import time

class Message():

    # Initialization
    def __init__(self, message, x_pos, y_pos, font, rot, horz_offset, vert_offset, scroll_time, scroll_speed, oled, screen_width, screen_height):
        
        self.message = message
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font
        self.rot = rot
        self.horz_offset = horz_offset
        self.vert_offset = vert_offset
        self.scroll_time = scroll_time
        self.scroll_speed = scroll_speed
        self.oled = oled
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.scrollable = False
        self.start_time = time.time()
        self.message_len = self.font.mesure_text(self.message)
    
    # Determine if the message is scrollable (does not fit in the bounds of the screen)
    def determineScrollable(self):

        # If the message does not fit on the screen, make it scrollable
        if self.message_len > self.screen_width:
            
            self.scrollable = True

            # Pad the message at the beginning with spaces so that the message starts in the middle of the screen
            num_spaces = self.message_len // 2
            for _ in range(num_spaces):
                self.message = " " + self.message

            # Update the message length
            self.message_len = self.font.mesure_text(self.message)
        
        # If the message does fit on the screen, scrolling is not necessary
        else:

            self.scrollable = False

    # Draw the message (if it is scrollable, update the messages movement)
    def draw_message(self):

        # If the message is scrollable
        if self.scrollable:

            # Get the current timer reading
            current_time = time.time()

            # Check if the timer has surpassed the scroll time
            if current_time - self.start_time >= self.scroll_time:

                # Take a space from the beginning of the message and move it to the end
                self.message = self.message[1: len(self.message)] + " "

                # Reset the start timer to the current time (keeps track of elapsed time)
                self.start_time = current_time

        
        # Draw the message
        self.oled.draw_text(self.oled.width//3 + round(self.message_len*self.horz_offset), self.oled.height//2 + round(self.message_len*self.vert_offset), self.message, self.font, rotate=self.rot)
