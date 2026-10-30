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
#if DISPLAY_REVISION == 2

//GxEPD2 only loads the waveform table for partial refreshes, so they run with whatever voltages
//the last full refresh left behind. This subclass loads the table together with the voltages and
//VCOM from Waveshare's reference driver for this panel (epd2in9_V2).
//The table differs from the stock one in one way: while changed pixels are driven, unchanged pixels
//sit slightly off VCOM and black ones slowly fade to grey. So in every repeat, after the 10 frames
//that drive changed pixels (phase A), unchanged black pixels get 2 frames pushing them back (phase B).
const unsigned char partialLut[153] PROGMEM = {
  0x10, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, //Voltages per phase for black->black
  0x80, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, //black->white
  0x40, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, //white->black
  0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, //white->white
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, //VCOM
  0x0A, 0x02, 0x00, 0x00, 0x00, 0x00, 0x02, //Group 0: phase A 10 frames, phase B 2 frames, repeated (last byte, see PARTIAL_REFRESH_REPEATS)
  0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
  0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x00, 0x00, 0x00,
};
const byte PARTIAL_LUT_REPEAT_INDEX = 66;

class InkkeysDisplay : public GxEPD2_290_T94_V2 {
  public:
    InkkeysDisplay(int16_t cs, int16_t dc, int16_t rst, int16_t busy) : GxEPD2_290_T94_V2(cs, dc, rst, busy) {}

    //Call before every partial refresh, a full refresh replaces these settings
    void preparePartialRefresh(byte repeats) {
      _writeCommand(0x32); //Waveform table
      for (byte i = 0; i < sizeof(partialLut); i++)
        _writeData(i == PARTIAL_LUT_REPEAT_INDEX ? repeats : pgm_read_byte(&partialLut[i]));
      _writeCommand(0x3F); //End option
      _writeData(0x22);
      _writeCommand(0x03); //Gate voltage
      _writeData(0x17);
      _writeCommand(0x04); //Source voltages
      _writeData(0x41);
      _writeData(0xB0);
      _writeData(0x32);
      _writeCommand(0x2C); //VCOM
      _writeData(0x36);
      _using_partial_mode = true; //Keeps GxEPD2 from loading its own table over ours
    }
};

#else

class InkkeysDisplay : public GxEPD2_290 {
  public:
    InkkeysDisplay(int16_t cs, int16_t dc, int16_t rst, int16_t busy) : GxEPD2_290(cs, dc, rst, busy) {}
    void preparePartialRefresh(byte repeats) {} //The stock waveform works for revision 1
};

#endif

InkkeysDisplay display(/*CS=*/ PIN_CS, /*DC=*/ PIN_DC, /*RST=*/ PIN_RST, /*BUSY=*/ PIN_BUSY);

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

  //From here on, keys and the jog dial keep working while the display refreshes (see checkInputWhileBusy)
  display.setBusyCallback(checkInputWhileBusy);

  //Show LED greeting to confirm completion
  ledGreeting(800);
  Serial.println("Ready.");
}

void loop() {
  checkKeysAndReportChanges();
  checkRotaryEncoderAndReportChanges();
  handleSerialInput();
}

//GxEPD2 calls this over and over while it waits for the panel to finish a refresh (about 1s, a full
//refresh 4s). Without it, loop() stands still that long and presses that are over before it ends are lost.
//Serial input waits: a command arriving now must not start another refresh in the middle of this one.
void checkInputWhileBusy(const void*) {
  checkKeysAndReportChanges();
  checkRotaryEncoderAndReportChanges();
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
