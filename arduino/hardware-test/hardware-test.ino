/*
 * E-Ink adaptive macro keyboard
 * See https://there.oughta.be/a/macro-keyboard
 * 
 * This is only the test code for the assembled device.
 * It should show a circular pattern on the e-ink screen and run a
 * sequence of red, green, blue and white across the LEDs of the jog
 * dial (moving clock-wise, starting with the
 * LED closest to the display).
 * 
 * It should also report key presses, rotations of the jog dial and
 * a press of the jog dial on the serial.
 * 
 * It also tests the USB functions. It should register as a serial
 * device and as a HID device with keyboard and mouse functions. If
 * you send "test" (terminated with a carriage return) to the serial
 * device, it will send the key sequence
 * [Hold Alt]+[3xTab]+[Release Alt]
 * followed by moving the mouse pointer to the right. (This sequence
 * should initiate a task switch on most operating systems but will
 * not mess up your work.)
 */

#include "settings.h"           //Customize your settings in settings.h!

#include <HID-Project.h>           //HID (Keyboard/Mouse etc.)
#include <Encoder.h>            //Rotary Encoder
#include <GxEPD2_BW.h>          //E-Ink Display
#include <Adafruit_NeoPixel.h>  //Digital RGB LEDs

//Keys
const byte nSW = 9;
const byte SW[] = {PIN_SW1, PIN_SW2, PIN_SW3, PIN_SW4, PIN_SW5, PIN_SW6, PIN_SW7, PIN_SW8, PIN_SW9}; //Array of switches for easy iteration
bool pressed[] = {false, false, false, false, false, false, false, false, false}; //Last state of each key to track changes
uint32_t swDebounce[] = {0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L, 0L};

//Rotary encoder
Encoder rotary(PIN_ROTA, PIN_ROTB);
long rotaryPosition = 0;  //Last position to keep track of changes

//Display
GxEPD2_290_T94 display(/*CS=*/ PIN_CS, /*DC=*/ PIN_DC, /*RST=*/ PIN_RST, /*BUSY=*/ PIN_BUSY);

//LEDs
Adafruit_NeoPixel leds = Adafruit_NeoPixel(N_LED, PIN_LED, NEO_RGB + NEO_KHZ400);

//Buffer to process serial input
const byte serialBufferSize = 10;
char serialBuffer[serialBufferSize];
byte serialBufferCount = 0;

uint32_t demoColors[] = {0x00ff0000, 0x0000ff00, 0x000000ff, 0x00ffffff};
int demoColor = 0;
int demoBrightness;

void setup() {
  //Initialize LEDs first, for some reason they initialize blue
  //  after a power cycle which is pretty annoying.
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
  
  Serial.begin(115200);

  //Greeting on serial
  Serial.println("=== HARDWARE TEST ===");
  Serial.println("https://there.oughta.be/a/macro-keyboard");
  
  //Set pin modes for keys
  for (int i = 0; i < nSW; i++) {
    pinMode(SW[i], INPUT_PULLUP);
  }

  //Set rotary encoder to zero
  rotary.write(rotaryPosition);

  //Init e-ink screen, clear it, show test pattern and turn it off.
  Serial.println("Eink Test.");
  display.init(0, true, 2, false);
  display.clearScreen();
  einkTestPattern();
  display.refresh();
  display.powerOff();

  //Show LED test animation
  Serial.println("LED Test.");
  ledTestPattern();

  //Init HID. This test only uses keyboard and mouse, but we start
  //all types that are relevant to the final device as we want to
  //make sure that they can all be started in parallel.
  //These three should provide most desired functions and as the 32u4
  //on the Pro Micro provides 6 endpoints (-1 for serial), we can
  //use the single report variants for compatibility.
  Serial.println("Initializing HID devices.");
  BootKeyboard.begin();
  BootMouse.begin();
  SingleConsumer.begin();

  //Clear screen
  display.writeScreenBuffer();
  display.refresh();
  display.writeScreenBufferAgain();

  Serial.println("Tests on setup complete.");
  Serial.println("Send \"test\" to test keyboard and mouse.");
}

void loop() {
  checkKeysAndReportChanges();
  checkRotaryEncoderAndReportChanges();
  handleSerialInput();
}

//Draw circular pattern
void einkTestPattern() {
  uint8_t bitmap[DISP_W/8];
  for (short y = 0; y < DISP_H; y++) {
    uint8_t b;     //Holds the current byte
    short i = 0;   //Index of current byte
    uint8_t j = 0; //Index of current bit within current byte
    for (short x = 0; x < DISP_W; x++) { //Note that DISP_W needs to be a multiple of eight!
      if (j == 0)
        b = 0; //Start a new byte
      b <<= 1; //Shift bit from previous pixel

      //The color of the actual pixel at x/y
      uint8_t pixel;
      int dx = x - DISP_W/2;
      int dy = y - DISP_H/2;
      int d = dx*dx+dy*dy; 
      pixel = d % 1000 > 500 ? 1 : 0;
      
      b |= pixel; //Set bit of current pixel
      j++;
      if (j > 7) {
        bitmap[i++] = b;  //Store byte if this was its last bit
        j = 0;
      }
    }
    display.writeImage(bitmap, 0, y, DISP_W, 1, false, false, false);
  }
}

//Returns a darker version of color, dimmed to brightness/255
uint32_t dimmedColor(uint32_t color, byte brightness) {
  return (((color & 0xff0000) * brightness / 255) & 0xff0000)
       | (((color & 0x00ff00) * brightness / 255) & 0x00ff00)
       | (((color & 0xff) * brightness / 255) & 0x0000ff);
}

//Change LED color along their indices to red, green, blue and white
void ledTestPattern() {
  uint32_t color;
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < N_LED; j++) {
      leds.setPixelColor(j, demoColors[i]);
      leds.show();
      delay(30);
    }
  }
  for (byte i = 255; i > 0; i--) {
    leds.fill(dimmedColor(0x00ffffff, i), 0, N_LED);
    leds.show();
  }
  leds.clear();
  leds.show();
}

//Called when state of key has changed. Checks debounce time
//and returns false if event should be filtered. Otherwise it
//returns true and resets the debounce timer.
bool debounce(byte i) {
  long t = millis();
  if (t - swDebounce[i] < DEBOUNCE_TIME)
    return false;
  else {
    swDebounce[i] = t;
    return true;
  }
}

//Check if keys have changed and report any changes
void checkKeysAndReportChanges() {
  for (int i = 0; i < nSW; i++) {
    int state = digitalRead(SW[i]);
    if (state == LOW && !pressed[i]) {
      if (debounce(i)) {
        Serial.print("SW");
        Serial.print(i+1);
        Serial.println(" pressed.");
        pressed[i] = true;

        if (i == 0) {
          demoColor = (demoColor + 1) % 4;
        }
      }
    } else if (state == HIGH && pressed[i]) {
      if (debounce(i)) {
        Serial.print("SW");
        Serial.print(i+1);
        Serial.println(" released.");
        pressed[i] = false;
      }
    }
  }
}

//Check if rotary encoder position changed and report any changes
void checkRotaryEncoderAndReportChanges() {
  long rotaryNew = rotary.read();
  if (rotaryNew != rotaryPosition) {
    rotaryPosition = rotaryNew;
    Serial.print("Rotary encoder changed to ");
    Serial.print(rotaryPosition);
    Serial.println(".");

    demoBrightness = 255;
  }
  if (demoBrightness > 0) {
    demoBrightness--;
    leds.clear();
    if (demoBrightness > 0) {
      leds.setPixelColor((12000+rotaryPosition/ROT_FACTOR*N_LED/ROT_CIRCLE_STEPS)%N_LED, dimmedColor(demoColors[demoColor], demoBrightness));
      leds.setPixelColor((12000+rotaryPosition/ROT_FACTOR*N_LED/ROT_CIRCLE_STEPS+N_LED/2)%N_LED, dimmedColor(demoColors[(demoColor+1)%4], demoBrightness));
    }
    leds.show();
  }
}

//Read from Serial in and react to enter (carriage return)
void handleSerialInput() {
  if (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n') {
      //Carriage return. Command ends and needs to be processed
      if (serialBufferCount == serialBufferSize) {
        Serial.println("Error: Command exceeds buffer size.");
      } else if (serialBufferCount > 0) {
        if (strncmp(serialBuffer, "I", 1) == 0) {
          Serial.println("Inkkeys");
          Serial.println("TEST 1");
          Serial.print("N_LED ");
          Serial.println(N_LED);
          Serial.print("DISP_W ");
          Serial.println(DISP_W);
          Serial.print("DISP_H ");
          Serial.println(DISP_H);
          Serial.print("ROT_CIRCLE_STEPS ");
          Serial.println(ROT_CIRCLE_STEPS);
          Serial.println("Done");
        } else if (strncmp(serialBuffer, "test", 4) == 0) {
          runHIDTests();
        } else {
          Serial.println("Error: Unknown command. The hardware test code only supports the commands \"test\" and \"I\".");
        }
        
      }
      
      //Command was handled. Reset buffer
      serialBufferCount = 0;
      
    } else {
      //Just a normal character. Store it in the buffer.
      if (serialBufferCount < serialBufferSize) {
        serialBuffer[serialBufferCount] = c;
        serialBufferCount++;
      }
    }
  }
}

//Test mouse and keyboard
void runHIDTests() {
  //Hold Alt, press Tab three times and release Alt
  Serial.println("Testing keyboard...");
  BootKeyboard.press(KEY_LEFT_ALT);
  delay(100);
  for (int i = 0; i < 3; i++) {
    BootKeyboard.press(KEY_TAB);
    delay(100);
    BootKeyboard.release(KEY_TAB);
    delay(100);
  }
  BootKeyboard.releaseAll();

  //Move the mouse to the right, starting with small steps,
  //increasing to larger steps and then returning to small steps again
  Serial.println("Testing mouse...");
  for (int i = 1; i < 10; i++) {
    BootMouse.move(i,0,0);
    delay(100);
  }
  for (int i = 10; i > 0; i--) {
    BootMouse.move(i,0,0);
    delay(100);
  }
  Serial.println("Test complete.");
}
