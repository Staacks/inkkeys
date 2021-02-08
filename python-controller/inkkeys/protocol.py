from enum import Enum
from PIL import Image

def event(device, keycode, value=""):
    if device == DELAY:
        return device + str(keycode)
    elif type(value) == int:
        return device.value + str(keycode.value) + "i" + str(value)
    elif type(value) == ActionCode:
        return device.value + str(keycode.value) + value.value
    else:
        return device.value + str(keycode.value)

class CommandCode(Enum):
    ASSIGN = "A"
    DISPLAY = "D"
    LED = "L"
    REFRESH = "R"
    INFO = "I"

class RefreshTypeCode(Enum):
    PARTIAL = "p"
    FULL = "f"
    OFF = "o"
    
class KeyCode(Enum):
    JOG_PRESS = "1p"
    JOG_RELEASE = "1r"
    SW1_PRESS = "1p"   #Alias
    SW1_RELEASE = "1r" #Alias
    SW2_PRESS = "2p"
    SW2_RELEASE = "2r"
    SW3_PRESS = "3p"
    SW3_RELEASE = "3r"
    SW4_PRESS = "4p"
    SW4_RELEASE = "4r"
    SW5_PRESS = "5p"
    SW5_RELEASE = "5r"
    SW6_PRESS = "6p"
    SW6_RELEASE = "6r"
    SW7_PRESS = "7p"
    SW7_RELEASE = "7r"
    SW8_PRESS = "8p"
    SW8_RELEASE = "8r"
    SW9_PRESS = "9p"
    SW9_RELEASE = "9r"
    JOG_CW = "R+"
    JOG_CCW = "R-"
    JOG = "R" # Only for callbacks!

class ActionCode(Enum):
    PRESS = "p"
    RELEASE = "r"
    INCREMENT = "i"

class DeviceCode(Enum):
    CONSUMER = "c"
    KEYBOARD = "k"
    MOUSE = "m"

#DelayCode
DELAY = "d"

#Converted from HID-project: https://github.com/NicoHood/HID/blob/master/src/HID-APIs/ConsumerAPI.h
class ConsumerKeycode(Enum):
    CONSUMER_POWER = 0x30
    CONSUMER_SLEEP = 0x32
    MEDIA_RECORD = 0xB2
    MEDIA_FAST_FORWARD = 0xB3
    MEDIA_REWIND = 0xB4
    MEDIA_NEXT = 0xB5
    MEDIA_PREVIOUS = 0xB6
    MEDIA_PREV = 0xB6
    MEDIA_STOP = 0xB7
    MEDIA_PLAY_PAUSE = 0xCD
    MEDIA_PAUSE = 0xB0
    MEDIA_VOLUME_MUTE = 0xE2
    MEDIA_VOL_MUTE = 0xE2
    MEDIA_VOLUME_UP = 0xE9
    MEDIA_VOL_UP = 0xE9
    MEDIA_VOLUME_DOWN = 0xEA
    MEDIA_VOL_DOWN = 0xEA
    CONSUMER_BRIGHTNESS_UP = 0x006F
    CONSUMER_BRIGHTNESS_DOWN = 0x0070
    CONSUMER_SCREENSAVER = 0x19e
    CONSUMER_PROGRAMMABLE_BUTTON_CONFIGURATION = 0x182
    CONSUMER_CONTROL_CONFIGURATION = 0x183
    CONSUMER_EMAIL_READER = 0x18A
    CONSUMER_CALCULATOR = 0x192
    CONSUMER_EXPLORER = 0x194
    CONSUMER_BROWSER_HOME = 0x223
    CONSUMER_BROWSER_BACK = 0x224
    CONSUMER_BROWSER_FORWARD = 0x225
    CONSUMER_BROWSER_REFRESH = 0x227
    CONSUMER_BROWSER_BOOKMARKS = 0x22A
    #Converted from HID-project: https://github.com/NicoHood/HID/blob/master/src/KeyboardLayouts/ImprovedKeylayoutsUS.h

class KeyboardKeycode(Enum):
    KEY_RESERVED = 0
    KEY_ERROR_ROLLOVER = 1
    KEY_POST_FAIL = 2
    KEY_ERROR_UNDEFINED = 3
    KEY_A = 4
    KEY_B = 5
    KEY_C = 6
    KEY_D = 7
    KEY_E = 8
    KEY_F = 9
    KEY_G = 10
    KEY_H = 11
    KEY_I = 12
    KEY_J = 13
    KEY_K = 14
    KEY_L = 15
    KEY_M = 16
    KEY_N = 17
    KEY_O = 18
    KEY_P = 19
    KEY_Q = 20
    KEY_R = 21
    KEY_S = 22
    KEY_T = 23
    KEY_U = 24
    KEY_V = 25
    KEY_W = 26
    KEY_X = 27
    KEY_Y = 28
    KEY_Z = 29
    KEY_1 = 30
    KEY_2 = 31
    KEY_3 = 32
    KEY_4 = 33
    KEY_5 = 34
    KEY_6 = 35
    KEY_7 = 36
    KEY_8 = 37
    KEY_9 = 38
    KEY_0 = 39
    KEY_ENTER = 40
    KEY_RETURN = 40
    KEY_ESC = 41
    KEY_BACKSPACE = 42
    KEY_TAB = 43
    KEY_SPACE = 44
    KEY_MINUS = 45
    KEY_EQUAL = 46
    KEY_LEFT_BRACE = 47
    KEY_RIGHT_BRACE = 48
    KEY_BACKSLASH = 49
    KEY_NON_US_NUM = 50
    KEY_SEMICOLON = 51
    KEY_QUOTE = 52
    KEY_TILDE = 53
    KEY_COMMA = 54
    KEY_PERIOD = 55
    KEY_SLASH = 56
    KEY_CAPS_LOCK = 0x39
    KEY_F1 = 0x3A
    KEY_F2 = 0x3B
    KEY_F3 = 0x3C
    KEY_F4 = 0x3D
    KEY_F5 = 0x3E
    KEY_F6 = 0x3F
    KEY_F7 = 0x40
    KEY_F8 = 0x41
    KEY_F9 = 0x42
    KEY_F10 = 0x43
    KEY_F11 = 0x44
    KEY_F12 = 0x45
    KEY_PRINT = 0x46
    KEY_PRINTSCREEN = 0x46
    KEY_SCROLL_LOCK = 0x47
    KEY_PAUSE = 0x48
    KEY_INSERT = 0x49
    KEY_HOME = 0x4A
    KEY_PAGE_UP = 0x4B
    KEY_DELETE = 0x4C
    KEY_END = 0x4D
    KEY_PAGE_DOWN = 0x4E
    KEY_RIGHT_ARROW = 0x4F
    KEY_LEFT_ARROW = 0x50
    KEY_DOWN_ARROW = 0x51
    KEY_UP_ARROW = 0x52
    KEY_RIGHT = 0x4F
    KEY_LEFT = 0x50
    KEY_DOWN = 0x51
    KEY_UP = 0x52
    KEY_NUM_LOCK = 0x53
    KEYPAD_DIVIDE = 0x54
    KEYPAD_MULTIPLY = 0x55
    KEYPAD_SUBTRACT = 0x56
    KEYPAD_ADD = 0x57
    KEYPAD_ENTER = 0x58
    KEYPAD_1 = 0x59
    KEYPAD_2 = 0x5A
    KEYPAD_3 = 0x5B
    KEYPAD_4 = 0x5C
    KEYPAD_5 = 0x5D
    KEYPAD_6 = 0x5E
    KEYPAD_7 = 0x5F
    KEYPAD_8 = 0x60
    KEYPAD_9 = 0x61
    KEYPAD_0 = 0x62
    KEYPAD_DOT = 0x63
    KEY_NON_US = 0x64
    KEY_APPLICATION = 0x65
    KEY_MENU = 0x65
    KEY_POWER = 0x66
    KEY_PAD_EQUALS = 0x67
    KEY_F13 = 0x68
    KEY_F14 = 0x69
    KEY_F15 = 0x6A
    KEY_F16 = 0x6B
    KEY_F17 = 0x6C
    KEY_F18 = 0x6D
    KEY_F19 = 0x6E
    KEY_F20 = 0x6F
    KEY_F21 = 0x70
    KEY_F22 = 0x71
    KEY_F23 = 0x72
    KEY_F24 = 0x73
    KEY_EXECUTE = 0x74
    KEY_HELP = 0x75
    KEY_MENU2 = 0x76
    KEY_SELECT = 0x77
    KEY_STOP = 0x78
    KEY_AGAIN = 0x79
    KEY_UNDO = 0x7A
    KEY_CUT = 0x7B
    KEY_COPY = 0x7C
    KEY_PASTE = 0x7D
    KEY_FIND = 0x7E
    KEY_MUTE = 0x7F
    KEY_VOLUME_MUTE = 0x7F
    KEY_VOLUME_UP = 0x80
    KEY_VOLUME_DOWN = 0x81
    KEY_LOCKING_CAPS_LOCK = 0x82
    KEY_LOCKING_NUM_LOCK = 0x83
    KEY_LOCKING_SCROLL_LOCK = 0x84
    KEYPAD_COMMA = 0x85
    KEYPAD_EQUAL_SIGN = 0x86
    KEY_INTERNATIONAL1 = 0x87
    KEY_INTERNATIONAL2 = 0x88
    KEY_INTERNATIONAL3 = 0x89
    KEY_INTERNATIONAL4 = 0x8A
    KEY_INTERNATIONAL5 = 0x8B
    KEY_INTERNATIONAL6 = 0x8C
    KEY_INTERNATIONAL7 = 0x8D
    KEY_INTERNATIONAL8 = 0x8E
    KEY_INTERNATIONAL9 = 0x8F
    KEY_LANG1 = 0x90
    KEY_LANG2 = 0x91
    KEY_LANG3 = 0x92
    KEY_LANG4 = 0x93
    KEY_LANG5 = 0x94
    KEY_LANG6 = 0x95
    KEY_LANG7 = 0x96
    KEY_LANG8 = 0x97
    KEY_LANG9 = 0x98
    KEY_ALTERNATE_ERASE = 0x99
    KEY_SYSREQ_ATTENTION = 0x9A
    KEY_CANCEL = 0x9B
    KEY_CLEAR = 0x9C
    KEY_PRIOR = 0x9D
    KEY_RETURN2 = 0x9E
    KEY_SEPARATOR = 0x9F
    KEY_OUT = 0xA0
    KEY_OPER = 0xA1
    KEY_CLEAR_AGAIN = 0xA2
    KEY_CRSEL_PROPS = 0xA3
    KEY_EXSEL = 0xA4
    KEY_PAD_00 = 0xB0
    KEY_PAD_000 = 0xB1
    KEY_THOUSANDS_SEPARATOR = 0xB2
    KEY_DECIMAL_SEPARATOR = 0xB3
    KEY_CURRENCY_UNIT = 0xB4
    KEY_CURRENCY_SUB_UNIT = 0xB5
    KEYPAD_LEFT_BRACE = 0xB6
    KEYPAD_RIGHT_BRACE = 0xB7
    KEYPAD_LEFT_CURLY_BRACE = 0xB8
    KEYPAD_RIGHT_CURLY_BRACE = 0xB9
    KEYPAD_TAB = 0xBA
    KEYPAD_BACKSPACE = 0xBB
    KEYPAD_A = 0xBC
    KEYPAD_B = 0xBD
    KEYPAD_C = 0xBE
    KEYPAD_D = 0xBF
    KEYPAD_E = 0xC0
    KEYPAD_F = 0xC1
    KEYPAD_XOR = 0xC2
    KEYPAD_CARET = 0xC3
    KEYPAD_PERCENT = 0xC4
    KEYPAD_LESS_THAN = 0xC5
    KEYPAD_GREATER_THAN = 0xC6
    KEYPAD_AMPERSAND = 0xC7
    KEYPAD_DOUBLEAMPERSAND = 0xC8
    KEYPAD_PIPE = 0xC9
    KEYPAD_DOUBLEPIPE = 0xCA
    KEYPAD_COLON = 0xCB
    KEYPAD_POUND_SIGN = 0xCC
    KEYPAD_SPACE = 0xCD
    KEYPAD_AT_SIGN = 0xCE
    KEYPAD_EXCLAMATION_POINT = 0xCF
    KEYPAD_MEMORY_STORE = 0xD0
    KEYPAD_MEMORY_RECALL = 0xD1
    KEYPAD_MEMORY_CLEAR = 0xD2
    KEYPAD_MEMORY_ADD = 0xD3
    KEYPAD_MEMORY_SUBTRACT = 0xD4
    KEYPAD_MEMORY_MULTIPLY = 0xD5
    KEYPAD_MEMORY_DIVIDE = 0xD6
    KEYPAD_PLUS_MINUS = 0xD7
    KEYPAD_CLEAR = 0xD8
    KEYPAD_CLEAR_ENTRY = 0xD9
    KEYPAD_BINARY = 0xDA
    KEYPAD_OCTAL = 0xDB
    KEYPAD_DECIMAL = 0xDC
    KEYPAD_HEXADECIMAL = 0xDD
    KEY_LEFT_CTRL = 0xE0
    KEY_LEFT_SHIFT = 0xE1
    KEY_LEFT_ALT = 0xE2
    KEY_LEFT_GUI = 0xE3
    KEY_LEFT_WINDOWS = 0xE3
    KEY_RIGHT_CTRL = 0xE4
    KEY_RIGHT_SHIFT = 0xE5
    KEY_RIGHT_ALT = 0xE6
    KEY_RIGHT_GUI = 0xE7
    KEY_RIGHT_WINDOWS = 0xE7
    #Converted from HID-project: https://github.com/NicoHood/HID/blob/master/src/HID-APIs/MouseAPI.h

class MouseKeycode(Enum):
    MOUSE_LEFT = 1
    MOUSE_RIGHT = 2
    MOUSE_MIDDLE = 4
    MOUSE_PREV = 8
    MOUSE_NEXT = 16

class MouseAxisCode(Enum):
    MOUSE_X = "x"
    MOUSE_Y = "y"
    MOUSE_WHEEL = "w"



