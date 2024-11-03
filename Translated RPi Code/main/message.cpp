#include "Message.h"

// Constructor
Message::Message(const String& message, int x_pos, int y_pos, int rot, float horz_offset, float vert_offset, int scroll_time, Adafruit_SSD1309* oled)
    : message(message), x_pos(x_pos), y_pos(y_pos), rot(rot), horz_offset(horz_offset), vert_offset(vert_offset), scroll_time(scroll_time), oled(oled) {
    
    scrollable = false;
    start_time = millis();
    message_len = measureTextWidth(message);
}

// Sets the message and updates its length
void Message::setMessage(const String& m) {
    message = m;
    message_len = measureTextWidth(m);
}

// Determines if the message is scrollable
void Message::determineScrollable() {
    // If the message does not fit on the screen, make it scrollable
    if (message_len > oled->height()) {
        scrollable = true;

        // Pad the message with spaces for centering
        int num_spaces = message.length() / 2;
        for (int i = 0; i < num_spaces; i++) {
            message = " " + message;
        }

        // Update the message length
        message_len = measureTextWidth(message);
    } else {
        scrollable = false;
    }
}

// Draws the message and updates scrolling if necessary
void Message::drawMessage() {
    // Handle scrolling
    if (scrollable) {
        unsigned long current_time = millis();
        if (current_time - start_time >= scroll_time * 1000) {
            // Scroll by moving the first character to the end
            message = message.substring(1) + message[0];
            start_time = current_time;
        }
    }

    // Draw the message on the display at the specified position
    int text_x = x_pos + round(message_len * horz_offset);
    int text_y = y_pos + round(message_len * vert_offset);
    oled->setRotation(rot);
    oled->setCursor(text_x, text_y);
    oled->print(message);
    oled->display();
}

// Approximates the width of the text based on character width (adjust as needed)
int Message::measureTextWidth(const String& text) {
    int char_width = 5;  // Approximate width per character for a 5x8 font
    return text.length() * char_width;
}
