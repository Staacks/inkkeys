/*
 * E-Ink adaptive macro keyboard
 * See https://there.oughta.be/a/macro-keyboard
 * 
 * This part contains LED related functions
 */

//LEDs
Adafruit_NeoPixel leds = Adafruit_NeoPixel(N_LED, PIN_LED, NEO_RGB + NEO_KHZ400);

void initLEDs() {
  leds.begin();
  leds.setBrightness(100);
  leds.clear();
  leds.show();
  //IMPORTANT: The original hardware design cannot provide enough
  //           current to set all LEDs to full white. If you want to
  //           increase the brightness, you have to consider their
  //           maximum current draw and either adapt the hardware
  //           design or the animations accordingly (i.e. do not
  //           allow for white color).
}

//Returns a darker version of color, dimmed to brightness/255
uint32_t dimmedColor(uint32_t color, byte brightness) {
  return (((color & 0xff0000) * brightness / 255) & 0xff0000)
       | (((color & 0x00ff00) * brightness / 255) & 0x00ff00)
       | (((color & 0xff) * brightness / 255) & 0x0000ff);
}

//Returns fully saturated color by hue (0..255)
uint32_t hue2rgb(int hue) {
  uint32_t r = constrain(abs( hue        % 256 * 6 - 765) - 255, 0, 255);
  uint32_t g = constrain(abs((hue + 85)  % 256 * 6 - 765) - 255, 0, 255);
  uint32_t b = constrain(abs((hue + 170) % 256 * 6 - 765) - 255, 0, 255);
  return r << 16 | g << 8 | b;
}

//Short rainbow swirl on the LEDs as a greeting
void ledGreeting(int steps) {
  for (int i = 0; i < steps; i++) {
    byte brightness = constrain(steps/2 - abs(i-steps/2), 0, 255);
    for (int j = 0; j < N_LED; j++) {
      leds.setPixelColor(j, dimmedColor(hue2rgb(i/2 + j*256/N_LED), brightness));
    }
    leds.show();
  }
  leds.clear();
  leds.show();
}

