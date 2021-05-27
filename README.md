# inkkeys
Details and instructions can be found on https://there.oughta.be/a/macro-keyboard

In contrast to most of my other projects, I decided to put this into its own repository as it is slightly more complex and I am hoping for community contributions.

If you have pull-requests, bug reports or want to contribute new case designs, please do not hesitate to open an issue. For generic discussions, "show and tell" and if you are looking for support for something that is not a problem in the code here, I would recommend [r/thereoughtabe on reddit](https://www.reddit.com/r/thereoughtabe/).

<a href="https://www.buymeacoffee.com/there.oughta.be" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" height="47" width="174" ></a>

## Common problems

### Display revision 2
Apparently, the original design used revision 1 of the display, while many newly ordered version are revision 2. There are a few differences and thankfully, [Corky402 made a good list of required changes on Reddit](https://www.reddit.com/r/arduino/comments/l4wxxf/the_hardware_is_assembled_and_passed_all_tests/gqovq1j?utm_source=share&utm_medium=web2x&context=3). Here is an excerpt of the original post for reference:
>If you want to test your display hooked to a Arduino or Raspberry Pi you need to run examples for the epd2in9_V2 not the epd2in9.
>
>To get this awesome project working there is no need to make any alterations to the PCB, just simply plumb the Waveshare up on the connectors as I describe, not as per Sebastian's original post.
>
>PCB Pin Waveshare wiring loom
>
>+5v Grey
>
>GND Brown
>
>DIN Blue
>
>CLK Yellow
>
>CS Orange
>
>DC Green
>
>RST Purple
>
>BUSY White
>
>In short you are swapping the RST & BUSY lines on the PCB.
>
>Next, go to your Arduino sketch. This is for the hardware-test script. Enable line numbering and go to line 43 which reads -
>
>GxEPD2_290 display(/*CS=*/ PIN_CS, /*DC=*/ PIN_DC, /*RST=*/ PIN_RST, /*BUSY=*/ PIN_BUSY);
>
>Change this to -
>
>GxEPD2_290_T94 display(/*CS=*/ PIN_CS, /*DC=*/ PIN_DC, /*RST=*/ PIN_RST, /*BUSY=*/ PIN_BUSY);
>
>Then go to settings.h
>
>Lines 2 - 7 need to be altered so change that section of code as follows -
>
>const byte PIN_DIN = 16;
>
>const byte PIN_CLK = 15;
>
>const byte PIN_CS = 19;
>
>const byte PIN_DC = 18;
>
>const byte PIN_RST = 10;
>
>const byte PIN_BUSY = 14;
>
>The sketch will then compile and when uploaded to the board you will get the Waveshare drawing all sorts of Austin Powers time machine circles that make your eyes spin! 


## Gallery

![Original design](img/original.jpg?raw=true "Original design as presented on there.oughta.be with the 3d printing files from this repository.")
Original design as presented on there.oughta.be with the 3d printing files from this repository.

![Original design](img/john_mat_roland.jpg?raw=true "Design by John, Mat and Roland from the UK. The case was CNC milled from beech with a similarly machined clear perspex lid.")
Design by John, Mat and Roland from the UK. The case was CNC milled from beech with a similarly machined clear perspex lid. You can find the knob with finger dimple by Roland Irving in the 3dprint folder as know_with_dimple.stl.

