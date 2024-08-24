#include <FastLED.h>

// How many leds in your strip?
#define NUM_LEDS 256

#define TIME_ANIMATE_OFF 10
#define ON_COLOUR CRGB::White

// For led chips like WS2812, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define DATA_PIN 8
// #define CLOCK_PIN 13

// Define the array of leds
CRGB leds[NUM_LEDS];

// Params for width and height
#define kMatrixWidth 16
#define kMatrixHeight 16

uint16_t XY(uint8_t x, uint8_t y) {
  uint16_t i;
  if(y & 0x01) {
    // Odd rows run backwards
    uint8_t reverseX = (kMatrixWidth - 1) - x;
    i = (y * kMatrixWidth) + reverseX;
  } else {
    // Even rows run forwards
    i = (y * kMatrixWidth) + x;
  }
  
  return i;
}

void setXY(int x, int y, bool active) {
  int i = XY(x, y);
  leds[i] = active ? ON_COLOUR : CRGB::Black;
}

// idx in [0, 7]
void setRing(int idx, bool active) {
  // top
  for (int x = idx; x < 16 - idx; x++) {
    setXY(x, idx, active);
  }

  // bottom
  for (int x = idx; x < 16 - idx; x++) {
    setXY(x, 15 - idx, active);
  }

  // left
  for (int y = idx; y < 16 - idx; y++) {
    setXY(idx, y, active);
  }

  // right
  for (int y = idx; y < 16 - idx; y++) {
    setXY(15 - idx, y, active);
  }
}

void setup() {
    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed

    // LEDs off
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CRGB::Black;
    }
    FastLED.show();

    Serial.begin(2400); 
	  Serial.setTimeout(1);

    FastLED.setMaxRefreshRate(0, false);
}

void loop() {
  if (Serial.available()) {
    int duration = Serial.read();
    if (!duration) return;
  
    // Turn the LEDs on, then pause
    for (int i = 0; i < 256; i++) {
      leds[i] = ON_COLOUR;
    }
    FastLED.show();

    delay(duration);

    // Now turn the LEDs off with animation
    for (int i = 0; i < 8; i++) {
      setRing(i, false);
      FastLED.show();
      delay(TIME_ANIMATE_OFF);
    }
  }
}
