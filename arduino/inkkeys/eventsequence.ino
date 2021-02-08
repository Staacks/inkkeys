/*
 * E-Ink adaptive macro keyboard
 * See https://there.oughta.be/a/macro-keyboard
 * 
 * This part defines functions that handle event sequences that can be assigned to buttons
 */

// Compare to Event.deviceAndType & 0x0f
const byte DEVICE_NONE = 0x00; //No event
const byte DEVICE_DELAY = 0x01;
const byte DEVICE_CONSUMER = 0x02;
const byte DEVICE_KEYBOARD = 0x03;
const byte DEVICE_MOUSE = 0x04;

// Compare to Event.deviceAndType & 0xf0
const byte TYPE_NONE = 0x00;
const byte TYPE_PRESS = 0x10;
const byte TYPE_RELEASE = 0x20;
const byte TYPE_INCREMENT = 0x30;
const byte TYPE_STROKE = 0x40;

// Compare to Event.keycodeOrDelay & 0xff00
const byte MOUSEAXIS_BUTTON = 0x00; //The button is defined in second byte using the definitions in BootMouse
const byte MOUSEAXIS_X = 0x01;
const byte MOUSEAXIS_Y = 0x02;
const byte MOUSEAXIS_WHEEL = 0x03;

void executeEvents(Event events[]) {
  for (byte i = 0; i < N_EVENTS; i++) {
    byte device = events[i].deviceAndType & 0x0f;
    byte etype = events[i].deviceAndType & 0xf0;
    switch(device) {
      case DEVICE_NONE:
        return; //Empty event. We are done.
      case DEVICE_DELAY:
        delay(events[i].keycodeOrDelay);
        break;
      case DEVICE_CONSUMER:
        switch (etype) {
          case TYPE_PRESS:
            SingleConsumer.press(ConsumerKeycode(events[i].keycodeOrDelay));
            break;
          case TYPE_RELEASE:
            SingleConsumer.release(ConsumerKeycode(events[i].keycodeOrDelay));
            break;
          case TYPE_STROKE:
            SingleConsumer.write(ConsumerKeycode(events[i].keycodeOrDelay));
            break;
        }
        break;
      case DEVICE_KEYBOARD:
        switch (etype) {
          case TYPE_PRESS:
            BootKeyboard.press(KeyboardKeycode(events[i].keycodeOrDelay));
            break;
          case TYPE_RELEASE:
            BootKeyboard.release(KeyboardKeycode(events[i].keycodeOrDelay));
            break;
          case TYPE_STROKE:
            BootKeyboard.write(KeyboardKeycode(events[i].keycodeOrDelay));
            break;
        }
        break;
      case DEVICE_MOUSE:
        byte axis = (events[i].keycodeOrDelay >> 8) & 0xff;
        int8_t increment = (int8_t)(events[i].keycodeOrDelay & 0xff);
        switch(axis) {
          case MOUSEAXIS_BUTTON:
            switch (etype) {
              case TYPE_PRESS:
                BootMouse.press(increment);
                break;
              case TYPE_RELEASE:
                BootMouse.release(increment);
                break;
              case TYPE_STROKE:
                BootMouse.click(increment);
                break;
            }
            break;
          case MOUSEAXIS_X:
            if (etype == TYPE_INCREMENT)
              BootMouse.move(increment,0,0);
            break;
          case MOUSEAXIS_Y:
            if (etype == TYPE_INCREMENT)
              BootMouse.move(0,increment,0);
            break;
          case MOUSEAXIS_WHEEL:
            if (etype == TYPE_INCREMENT)
              BootMouse.move(0,0,increment);
            break;
        }
        break;
    }
  }
}

void defaultAssignment() {
  //Initialize assignments array with defaults
  for (byte key = 0; key < 10; key++) {
    for (byte event = 0; event < N_EVENTS; event++) {
      assignments[key][0][event].deviceAndType = DEVICE_NONE;
      assignments[key][1][event].deviceAndType = DEVICE_NONE;
    }
  }
  //Left click on rotary press
  assignments[0][0][0].deviceAndType = DEVICE_MOUSE | TYPE_PRESS;
  assignments[0][0][0].keycodeOrDelay = (MOUSEAXIS_BUTTON << 8) | MOUSE_LEFT;
  assignments[0][1][0].deviceAndType = DEVICE_MOUSE | TYPE_RELEASE;
  assignments[0][1][0].keycodeOrDelay = (MOUSEAXIS_BUTTON << 8) | MOUSE_LEFT;
  for (byte key = 1; key < 9; key++) {
    //F1 to F8 on buttons
    assignments[key][0][0].deviceAndType = DEVICE_KEYBOARD | TYPE_PRESS;
    assignments[key][0][0].keycodeOrDelay = KEY_F1 + key - 1;
    assignments[key][1][0].deviceAndType = DEVICE_KEYBOARD | TYPE_RELEASE;
    assignments[key][1][0].keycodeOrDelay = KEY_F1 + key - 1;
  }
  //Mouse wheel on rotary
  assignments[9][0][0].deviceAndType = DEVICE_MOUSE | TYPE_INCREMENT;
  assignments[9][0][0].keycodeOrDelay = (MOUSEAXIS_WHEEL << 8) | (1 & 0xff);
  assignments[9][1][0].deviceAndType = DEVICE_MOUSE | TYPE_INCREMENT;
  assignments[9][1][0].keycodeOrDelay = (MOUSEAXIS_WHEEL << 8) | (-1 & 0xff);
}
