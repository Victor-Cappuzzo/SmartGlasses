//#include "U8glib.h"
#include <Arduino.h>
#include <U8g2lib.h>
#include <SPI.h>
#include <Wire.h>

// (Clock, Data in, CS, A0, Reset)
//U8GLIB_LD7032_60x32 u8g(9, 8, 11, 10, 12);
#define CLOCK_PIN 8
#define DATA_PIN 10
#define CS_PIN 2
#define A0_PIN 3
#define RESET_PIN 4
//U8GLIB_LD7032_60x32 u8g(CLOCK_PIN, DATA_PIN, CS_PIN, A0_PIN, RESET_PIN);
U8G2_LD7032_60X32_1_4W_SW_SPI u8g2(U8G2_R0, CLOCK_PIN, DATA_PIN, CS_PIN, A0_PIN, RESET_PIN);

void setup(void) {
  u8g2.begin();
}

void loop(void) {
  u8g2.firstPage();
  do {
    u8g2.setFont(u8g2_font_ncenB14_tr);
    u8g2.drawStr(0,24,"Hello World!");
  } while ( u8g2.nextPage() );
}


/**
void setup(void) {
}
const uint8_t rook_bitmap[] PROGMEM = {
  0x00,         // 00000000
  0x55,         // 01010101
  0x7f,          // 01111111
  0x3e,         // 00111110
  0x3e,         // 00111110
  0x3e,         // 00111110
  0x3e,         // 00111110
  0x7f           // 01111111
};

void loop(void) {
  // picture loop
  u8g.firstPage();
  do {
    u8g.setFont(u8g_font_unifont);
    //       u8g.setFont(u8g_font_osb21);
    u8g.drawStr( 5, 20, "DFROBOT");
  } while ( u8g.nextPage() );
  delay(1000);
  u8g.firstPage();
  do {
    u8g.drawCircle(30, 20, 18);
    u8g.drawEllipse(26, 12, 7, 5,U8G_DRAW_UPPER_LEFT );
    u8g.drawEllipse(34, 12, 7, 5, U8G_DRAW_UPPER_RIGHT);
    u8g.drawTriangle(30,14, 27, 18, 33, 18);
    u8g.drawFilledEllipse( 30, 25, 10,5, U8G_DRAW_LOWER_LEFT);
    u8g.drawFilledEllipse( 30, 25, 10,5, U8G_DRAW_LOWER_RIGHT);
    u8g.drawLine(30, 13, 30, 16);


    u8g.drawFrame(0, 0,60 ,32);

  } while ( u8g.nextPage() );
  delay(5000);

  u8g.firstPage();
  do {
    u8g.drawBitmapP(30, 16,1, 8, rook_bitmap);
  } while ( u8g.nextPage() );
  delay(1000);
  u8g.firstPage();
  do {

  } while ( u8g.nextPage() );
  delay(2000);

}
**/

/**
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <HardwareSerial.h>
#include "U8glib.h"

// Define screen orientation and text offsets
int rot = 90;
float horz_offset = 0.5;
float vert_offset = 0;

// Change text offsets based on screen orientation
if (rot == 0) {
    horz_offset = -0.5;
    vert_offset = 0;
} else if (rot == 90) {
    horz_offset = 0;
    vert_offset = -0.5;
} else if (rot == 180) {
    horz_offset = 0.5;
    vert_offset = 0;
} else if (rot == 270) {
    horz_offset = 0;
    vert_offset = 0.5;
}

// Define OLED pins
#define OLED_CS    17
#define OLED_DC    16
#define OLED_RST   20

// Initialize the display with the SSD1309 driver (make sure the dimensions match your display)
Adafruit_SSD1309 display(OLED_CS, OLED_DC, OLED_RST);

// Define UART settings
#define TX_PIN 0
#define RX_PIN 1
HardwareSerial uart(1); // Use Serial1 on pins TX (0) and RX (1)

#define CODE_LEN 4
#define SCROLL_TIME 1 // Time for text to scroll

// Create Message objects for each display message type
Message typed_message("", display.width() * 4 / 5, display.height() / 2, font, rot, horz_offset, vert_offset, SCROLL_TIME, display);
Message time_message("", display.width() * 3 / 5, display.height() / 2, font, rot, horz_offset, vert_offset, SCROLL_TIME, display);
Message batper_message("", display.width() * 2 / 5, display.height() / 2, font, rot, horz_offset, vert_offset, SCROLL_TIME, display);
Message charge_message("", display.width() / 5, display.height() / 2, font, rot, horz_offset, vert_offset, SCROLL_TIME, display);

String code_array[] = {"M:::", "T:::", "P:::", "C:::"};
Message* message_array[] = {&typed_message, &time_message, &batper_message, &charge_message};

void setup() {
    // Start UART with baud rate 9600
    uart.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);
    
    // Initialize the OLED display
    display.begin(SSD1309_SWITCHCAPVCC);
    display.clearDisplay();
    display.display();
}

void loop() {
    // Check if a UART message is available
    if (uart.available() > 0) {
        // Clear the display
        display.clearDisplay();
        
        delay(100); // Small delay to ensure the display is cleared
        
        // Read the incoming UART message
        String message = uart.readStringUntil('\n');
        message.trim();
        message.replace('\r', '');  // Remove carriage return if present
        Serial.println(message);  // Debug print to Serial Monitor
        
        // Extract the message code
        String code = message.substring(0, CODE_LEN);
        
        // Loop through each message/code
        for (int i = 0; i < sizeof(message_array) / sizeof(message_array[0]); i++) {
            // Check if the code matches the current message's code
            if (code == code_array[i]) {
                // Update the message variable
                message_array[i]->setMessage(message.substring(CODE_LEN));
                
                // Check if the message is scrollable
                message_array[i]->determineScrollable();
            }
        }
        
        // Display each message
        for (int i = 0; i < sizeof(message_array) / sizeof(message_array[0]); i++) {
            // Draw the message
            message_array[i]->drawMessage();
        }
        
        // Present the display (commit to the screen)
        display.display();
    }
}
**/
