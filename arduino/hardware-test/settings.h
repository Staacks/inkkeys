//Display
const byte PIN_DIN = 16;
const byte PIN_CLK = 15;
const byte PIN_CS = 19;
const byte PIN_DC = 18;
const byte PIN_RST = 10;
const byte PIN_BUSY = 14;

//Display size
const short DISP_W = 128; //Dispaly width
const short DISP_H = 296; //Display height

//LEDs
const byte PIN_LED = 20;
const byte N_LED = 12; //Number of LEDs

//Rotary encoder
const byte PIN_ROTA = 0;
const byte PIN_ROTB = 1;
const byte PIN_SW1 = 21;

const byte ROT_FACTOR = 4;         //Smallest reported step, typically one "click" on the encoder 
const byte ROT_CIRCLE_STEPS = 20;  //Rotary steps in a full circle

//Keys
const byte PIN_SW2 = 2;
const byte PIN_SW3 = 3;
const byte PIN_SW4 = 4;
const byte PIN_SW5 = 5;
const byte PIN_SW6 = 6;
const byte PIN_SW7 = 7;
const byte PIN_SW8 = 8;
const byte PIN_SW9 = 9;

const int DEBOUNCE_TIME = 50; //Debounce reject interval in milliseconds
