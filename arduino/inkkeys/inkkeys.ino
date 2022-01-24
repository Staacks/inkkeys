/*
 * E-Ink adaptive macro keyboard
 * See https://there.oughta.be/a/macro-keyboard
 * 
 * This is the main code which acts as a HID keyboard while
 * allowing to be controlled through a serial interface.
 */

#include "settings.h"           //Customize your settings in settings.h!

#include "eventsequence.h"      //Structure and constants to define the sequence of events assigned to different buttons

#include <HID-Project.h>        //HID (Keyboard/Mouse etc.)
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

void initDisplay() {
  display.init(0, true, 2, false);
  display.writeScreenBuffer();
  display.refresh();
  display.writeScreenBufferAgain();
  display.powerOff();
}

void setup() {
  initLEDs();
  //Initialize LEDs first, for some reason they initialize blue
  //  after a power cycle which is pretty annoying.
  
  Serial.begin(115200);

  defaultAssignment();

  //Greeting on serial
  Serial.println("= InkKeys =");
  
  //Set pin modes for keys
  for (int i = 0; i < nSW; i++) {
    pinMode(SW[i], INPUT_PULLUP);
  }

  //Set rotary encoder to zero
  rotary.write(rotaryPosition);

  //Init e-ink screen, clear it and turn it off.
  initDisplay();

  //Init HID.
  //These three should provide most desired functions and as the 32u4
  //on the Pro Micro provides 6 endpoints (-1 for serial), we can
  //use the single report variants for compatibility.
  BootKeyboard.begin();
  BootMouse.begin();
  SingleConsumer.begin();

  //Show LED greeting to confirm completion
  ledGreeting(800);
  Serial.println("Ready.");
}

void loop() {
  checkKeysAndReportChanges();
  checkRotaryEncoderAndReportChanges();
  handleSerialInput();
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
        pressed[i] = true;
        Serial.print(i+1);
        Serial.println("p");
        executeEvents(assignments[i][0]);
      }
    } else if (state == HIGH && pressed[i]) {
      if (debounce(i)) {
        pressed[i] = false;
        Serial.print(i+1);
        Serial.println("r");
        executeEvents(assignments[i][1]);
      }
    }
  }
}

//Check if rotary encoder position changed and report any changes
void checkRotaryEncoderAndReportChanges() {
  long rotaryNew = rotary.read();
  if (abs(rotaryNew - rotaryPosition) >= ROT_FACTOR) {
    int report = (rotaryNew-rotaryPosition)/ROT_FACTOR;
    Serial.print("R");
    Serial.println(report);
    rotaryPosition += report*ROT_FACTOR;
    for (int i = 0; i < report; i++)
      executeEvents(assignments[9][0]);
    for (int i = 0; i < -report; i++)
      executeEvents(assignments[9][1]);
  }
}
