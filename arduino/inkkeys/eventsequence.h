//Structure to hold events to be assigned to keys
typedef struct {
  byte deviceAndType; //Defines the device in the lower nibble (mouse, keyboard, consumer, delay) and the type in the higher nibble (key press, key release, increment by value, key stroke (press and release)), see definitions below
  unsigned short keycodeOrDelay; //For regular devices, this is the keycode, for mice the higher byte is the button, axis or wheel and the lower is the increment value as signed int8, for delays this is the time in ms
} Event;

const byte N_EVENTS = 10; //Maximum Number of events
//Array holding the current assignments, keys 1-9 at indices 0-8, then rotary at index 9. Second index is press (0) or release (1) or + (0) or - (1) for rotary. Third index is sequence of events up to N_EVENTS
Event assignments[10][2][N_EVENTS];
