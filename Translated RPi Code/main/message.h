#ifndef MESSAGE_H
#define MESSAGE_H

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1309.h>

class Message {
public:
    Message(const String& message, int x_pos, int y_pos, int rot, float horz_offset, float vert_offset, int scroll_time, Adafruit_SSD1309* oled);
    
    void setMessage(const String& m);
    void determineScrollable();
    void drawMessage();

private:
    String message;
    int x_pos, y_pos;
    int rot;
    float horz_offset, vert_offset;
    int scroll_time;
    unsigned long start_time;
    bool scrollable;
    int message_len;
    Adafruit_SSD1309* oled;

    int measureTextWidth(const String& text);  // Function to measure text length (approximation)
};

#endif
