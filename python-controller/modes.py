#In here, the logic of the different modes are defined.
#Each mode has to implement four functions (use "pass" if not needed):
#
#- activate
#Called when the mode becomes active. Usually used to set up static key assignment and icons
#- poll
#Called periodically and typically used to poll a state which you need to monitor. At the end you have to return an interval in seconds before the function is to be called again - otherwise it is not called a second time
#- animate
#Called up to 30 times per second, used for LED animation
#- deactivate
#Called when the mode becomes inactive. Used to clean up callback functions and images on the screen that are outside commonly overwritten areas.

#To avoid multiple screen refreshs, the modules usually do not clean-up the display when being deactivvated. Instead, each module is supposed to set at least the area corresponding to each button (even if it needs to be set to white if unused).

from inkkeys import *
import time
from threading import Timer
from math import ceil, floor
from PIL import Image, ImageDraw, ImageFont
from colorsys import hsv_to_rgb

#Optional libraries you might want to remove if you do not require them.
import pulsectl                                  # Get volume level in Linux, pip3 install pulsectl
from obswebsocket import obsws, requests, events # Control OBS. This requires the websocket plugin in OBS (https://github.com/Palakis/obs-websocket) and the Python library obs-websocket-py (pip3 install obs-websocket-py, https://github.com/Elektordi/obs-websocket-py)


        ############# Simple example. For Blender we just set up a few key assignments with corresponding images.
        ## Blender ## To be honest: Blender is just the minimalistic example here. Blender is very keyboard centric
        ############# and you should get used to the real shortcuts as it is much more efficient to stay on the keyboard all the time.

class ModeBlender:

    def activate(self, device):
        device.sendTextFor("title", "Blender", inverted=True) #Title

        #Button1 (Jog dial press)
        device.sendTextFor(1, "<   Play/Pause   >")
        device.assignKey(KeyCode.SW1_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.PRESS)]) #Play/pause
        device.assignKey(KeyCode.SW1_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.RELEASE)])

        #Jog dial rotation
        device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT)]) #CW = Clock-wise, one frame forward
        device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT)]) #CCW = Counter clock-wise, one frame back

        #Button2 (top left)
        device.sendIconFor(2, "icons/camera-reels.png")
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_0, ActionCode.PRESS)]) #Set view to camera
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_0, ActionCode.RELEASE)])

        #Button3 (left, second from top)
        device.sendIconFor(3, "icons/person-bounding-box.png")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.PRESS)]) #Isolation view
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.RELEASE)])

        #Button4 (left, third from top)
        device.sendIconFor(4, "icons/dot.png")
        device.assignKey(KeyCode.SW4_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW4_RELEASE, [])

        #Button5 (bottom left)
        device.sendIconFor(5, "icons/dot.png")
        device.assignKey(KeyCode.SW5_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW5_RELEASE, [])

        #Button6 (top right)
        device.sendIconFor(6, "icons/aspect-ratio.png")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.PRESS)]) #Center on selection
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.RELEASE)])

        #Button7 (right, second from top)
        #Button4 (left, third from top)
        device.sendIconFor(7, "icons/collection.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_F12), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE)]) #Render sequence
        device.assignKey(KeyCode.SW7_RELEASE, [])

        #Button8 (right, third from top)
        device.sendIconFor(8, "icons/dot.png")
        device.assignKey(KeyCode.SW8_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW8_RELEASE, [])

        #Button9 (bottom right)
        device.sendIconFor(9, "icons/dot.png")
        device.assignKey(KeyCode.SW9_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW9_RELEASE, [])

        device.updateDisplay()

    def poll(self, device):
        return False    # No polling in this example

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        pass            # Nothing to clean up in this example




        ##########
        ## Gimp ## The Gimp example is similar to Blender, but we add a callback to pressing the jog dial to switch functions
        ##########

class ModeGimp:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Gimp", inverted=True)  #Title

        #Button2 (top left)
        device.sendIconFor(2, "icons/fullscreen.png")
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_Z)]) #Cut to selection (this shortcut appears to be language dependent, so you will probably need to change it)
        device.assignKey(KeyCode.SW2_RELEASE, [])

        #Button3 (left, second from top)
        device.sendIconFor(3, "icons/upc-scan.png")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_I)]) #Cut to content (this shortcut appears to be language dependent, so you will probably need to change it)
        device.assignKey(KeyCode.SW3_RELEASE, [])

        #Button4 (left, third from top)
        device.sendIconFor(4, "icons/crop.png")
        device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_L)]) #Canvas size (this shortcut appears to be language
        device.assignKey(KeyCode.SW4_RELEASE, [])

        #Button5 (bottom left)
        device.sendIconFor(5, "icons/arrows-angle-expand.png")
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S)]) #Resize (this shortcut appears to be language
        device.assignKey(KeyCode.SW5_RELEASE, [])

        #Button6 (top right)
        device.sendIconFor(6, "icons/clipboard-plus.png")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #Paste as new image
        device.assignKey(KeyCode.SW6_RELEASE, [])

        #Button7 (right, second from top)
        device.sendIconFor(7, "icons/layers-half.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #New layer
        device.assignKey(KeyCode.SW7_RELEASE, [])

        #Button8 (right, third from top)
        device.sendIconFor(8, "icons/arrows-fullscreen.png")
        device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #Zom to fill screen
        device.assignKey(KeyCode.SW8_RELEASE, [])

        #Button9 (bottom right)
        device.sendIconFor(9, "icons/dot.png")
        device.assignKey(KeyCode.SW9_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW9_RELEASE, [])


        self.jogFunction = ""

        #This toggles the jog function and sets up key assignments and the label for the jog dial. It calls "updateDiplay()" if update is not explicitly set to False (for example if you need to update more parts of the display before updating it.)
        def toggleJogFunction(update=True):
            if self.jogFunction == "size":  #Tool opacity in GIMP
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Tool opacity")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_COMMA), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PERIOD), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
                self.jogFunction = "opacity"
                if update:
                    device.updateDisplay()
            else:                            #Tool size in GIMP
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Tool size")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_BRACE)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT_BRACE)])
                self.jogFunction = "size"
                if update:
                    device.updateDisplay()


        #Button 1 / jog dial press
        device.registerCallback(toggleJogFunction, KeyCode.JOG_PRESS) #Call "toggleJogFunction" if the dial is pressed
        device.assignKey(KeyCode.SW1_PRESS, [])                       #We do not send a key stroke when the dial is pressed, instead we use the callback.
        device.assignKey(KeyCode.SW1_RELEASE, [])                     #We still need to overwrite the assignment to clear previously set assignments.
        toggleJogFunction(False)    #We call toggleJogFunction to initially set the label and assignment
        device.updateDisplay()      #Everything has been sent to the display. Time to refresh it.

    def poll(self, device):
        return False #Nothing to poll

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        device.clearCallbacks() #Remove our callbacks if we switch to a different mode




        ############## This mode is used as a fallback and a much more complex example than Gimp. It also uses a switchable Jog dial,
        ## Fallback ## but most of its functions give a feedback via LED. Also, we use MQTT (via a separately defined class) to get
        ############## data from a CO2 sensor and control a light (both including feedback)

class ModeFallback:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial
    mqtt = None         #The MQTT object defined in mqtt.py. It will be passed when this class is contructed and kept in this variable
    lightState = None   #Current state of the lights in my office. (Keeping track to know when to update the screen)
    demoActive = False  #We have a demo button and this keeps track whether the demo mode is active, so we know when to update the screen

    def __init__(self, mqtt):
        self.mqtt = mqtt

    def activate(self, device):
        device.sendTextFor("title", "Default", inverted=True) #Title

        ### Buttons 2, 3, 6 and 7 are media controls ###

        device.sendIconFor(2, "icons/play.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_PLAY_PAUSE, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_PLAY_PAUSE, ActionCode.RELEASE)])
        device.sendIconFor(3, "icons/skip-start.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_PREV, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_PREV, ActionCode.RELEASE)])

        device.sendIconFor(6, "icons/stop.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_STOP, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_STOP, ActionCode.RELEASE)])
        device.sendIconFor(7, "icons/skip-end.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_NEXT, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW7_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_NEXT, ActionCode.RELEASE)])



        ### Buttons 5 and 9 are shortcuts to applications ###

        device.sendIconFor(5, "icons/envelope.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_EMAIL_READER, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW5_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_EMAIL_READER, ActionCode.RELEASE)])
        device.sendIconFor(9, "icons/calculator.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW9_PRESS, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_CALCULATOR, ActionCode.PRESS)])
        device.assignKey(KeyCode.SW9_RELEASE, [event(DeviceCode.CONSUMER, ConsumerKeycode.CONSUMER_CALCULATOR, ActionCode.RELEASE)])



        ### Button 4 controls the light in my office and displays its state ###

        def toggleLight():
            target = not self.lightState
            self.mqtt.setLight(target)
            self.lightState = target
            self.showLightState(device)

        self.lightState = self.mqtt.getLight
        self.showLightState(device, False)

        device.assignKey(KeyCode.SW4_PRESS, [])
        device.assignKey(KeyCode.SW4_RELEASE, [])
        device.registerCallback(toggleLight, KeyCode.SW4_PRESS)


        ### Button 8 set display and LEDs to a demo state (only used for videos and pictures of the thing)
        def toggleDemo():
            if self.demoActive:
                self.demoActive = False
                img = Image.new("1", (device.dispW, device.dispH), color=1)
                device.sendImage(0, 0, img)
                self.activate(device) #Recreate the screen content after the demo
            else:
                self.demoActive = True
                self.activate(device) #Recreate the screen because with demo active, the buttons will align differently to give room for "there.oughta.be"
                text = "there.oughta.be/a/macro-keyboard"
                font = ImageFont.truetype("arial.ttf", 17)
                w, h = font.getsize(text);
                x = (device.dispW-h)//2
                x8 = floor(x / 8) * 8 #needs to be a multiple of 8
                h8 = ceil((h + x - x8) / 8) * 8 #needs to be a multiple of 8
                img = Image.new("1", (w, h8), color=1)
                d = ImageDraw.Draw(img)
                d.text((0, x-x8), text, font=font, fill=0)
                device.sendImage(x8, (device.dispH-w)//2, img.transpose(Image.ROTATE_90))
                device.updateDisplay(True)

        device.registerCallback(toggleDemo, KeyCode.SW8_PRESS)
        device.sendIconFor(8, "icons/emoji-sunglasses.png", centered=(not self.demoActive))
        device.assignKey(KeyCode.SW8_PRESS, [])
        device.assignKey(KeyCode.SW8_RELEASE, [])

        ### The jog wheel can be pressed to switch between three functions: Volume control, mouse wheel, arrow keys left/right ###

        def showVolume(n):
            with pulsectl.Pulse('inkkeys') as pulse:
                sinkList = pulse.sink_list()
                name = pulse.server_info().default_sink_name
                for sink in sinkList:
                    if sink.name == name:
                        vol = sink.volume.value_flat
                off = 0x00ff00
                on = 0xff0000
                leds = [on if vol > i/(device.nLeds-1) else off for i in range(device.nLeds)]
                device.setLeds(leds)

        self.jogFunction = ""

        def toggleJogFunction(update=True):
            if self.jogFunction == "wheel":
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Arrow Keys")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT)])
                self.jogFunction = "arrow"
                if update:
                    device.updateDisplay()
            elif self.jogFunction == "arrow":
                device.sendTextFor(1, "Volume")
                device.registerCallback(showVolume, KeyCode.JOG)
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_VOL_UP)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.CONSUMER, ConsumerKeycode.MEDIA_VOL_DOWN)])
                self.jogFunction = "volume"
                if update:
                    device.updateDisplay()
            else:
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Mouse Wheel")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, 1)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.MOUSE, MouseAxisCode.MOUSE_WHEEL, -1)])
                self.jogFunction = "wheel"
                if update:
                    device.updateDisplay()

        device.registerCallback(toggleJogFunction, KeyCode.JOG_PRESS)
        device.assignKey(KeyCode.SW1_PRESS, [])
        device.assignKey(KeyCode.SW1_RELEASE, [])
        toggleJogFunction(False)



        ### All set, let's update the display ###

        device.updateDisplay()

    def poll(self, device):
        if not self.demoActive:
            co2 = self.mqtt.getCO2()
            if co2 != None and co2 > 1000:
                leds = [0x0000ff for i in range(device.nLeds)]
                device.setLeds(leds)
            light = self.mqtt.getLight()
            if light != self.lightState:
                self.lightState = light
                self.showLightState(device)
        return 10 #Since we only retrieve the current state from the Mqtt class, the 10 seconds do not really control how often the value is querries but how often we react to it. For the CO2 warning, this is a not too intrusive blue flash every 10 seconds and a 10 second delay to update the light state if it has been switched from somewhere else (rare) seems reasonable, too.

    #Called to update the icon of button 4, showing the state of the office light (as if I couldn't see it in the real room, but it is a nice touch to update the display accordingly)
    def showLightState(self, device, update=True):
        if self.lightState:
            device.sendIconFor(4, "icons/lightbulb.png", centered=(not self.demoActive))
        else:
            device.sendIconFor(4, "icons/lightbulb-off.png", centered=(not self.demoActive))
        if update:
            device.updateDisplay()

    def animate(self, device):
        if self.demoActive: #In demo mode, we animate the LEDs here

            def rgbTupleToInt(rgb):
                return (int(rgb[0]*255) << 16) | (int(rgb[1]*255) << 8) | int(rgb[2]*255)

            t = time.time()
            leds = [rgbTupleToInt(hsv_to_rgb(t + i/device.nLeds, 1, 1)) for i in range(device.nLeds)]
            device.setLeds(leds)
        else:               #If not in demo mode, we call "fadeLeds" to create a fade animation for any color set anywhere in this mode
            device.fadeLeds()

    def deactivate(self, device):
        device.clearCallbacks() #Clear our callbacks if we switch to a different mode





        ######### One of the most complex examples. This controls OBS scenes and gives feedback about the current state. For this we
        ## OBS ## use the websocket plugin and address scenes and sources by their names (so, you need to adapt these to your setup).
        ######### We subscribe to OBS events and show the status on the key and LEDs.

class ModeOBS:
    ws = None           #Websocket instance
    currentScene = None #Keep track of current scene

    #Scenes assigned to buttons with respective icons.
    scenes = [\
                {"name": "Moderation", "icon": "icons/card-image.png", "button": 2}, \
                {"name": "Closeup", "icon": "icons/person-square.png", "button": 3}, \
                {"name": "Slides", "icon": "icons/easel.png", "button": 4}, \
                {"name": "Video-Mute", "icon": "icons/camera-video-off.png", "button": 5}, \
             ]

    #State of sources within scenes. "items" is an array of scene/item combinations to keep track of items that need to be switched on multiple scenes simultaneously, so you can mute all mics in all scenes and switch scenes without an unpleasant surprise. The current state is tracked in this object ("current")
    states = [\
                {"items": [("Moderation", "Phone"), ("Closeup", "Phone"), ("Slides", "Phone")], "icon": "icons/phone.png", "button": 7, "current": True}, \
                {"items": [("Slides", "Cam: Closeup")], "icon": "icons/pip.png", "button": 8, "current": True}, \
                {"items": [("Moderation", "Mic: Moderation"), ("Closeup", "Mic: Closeup"), ("Slides", "Mic: Closeup")], "icon": "icons/mic.png", "button": 9, "current": True}, \
             ]

    #Switch to scene with name "name"
    def setScene(self, name):
        self.ws.call(requests.SetCurrentScene(name))

    #Toggle source visibility as defined in a state (see states above)
    def toggleState(self, state):
        visible = not state["current"]
        for item in state["items"]:
            self.ws.call(requests.SetSceneItemProperties(item[1], scene_name=item[0], visible=visible))

    #Generates a callback function which in turn calls "setScene" with the fixed scene "name" without requiring a parameter
    def getSetSceneCallback(self, name):
        return lambda: self.setScene(name)

    #Generates a callback function which in turn calls "toggleState" with a fixed "state" object without requiting a parameter
    def getToggleStateCallback(self, state):
        return lambda: self.toggleState(state)

    #Updates the buttons associated with scenes. Unless "init" is set to true, it only updates changed parts of the display and returns True if anything has changed so that the calling function should call updateDisplay()
    def updateSceneButtons(self, device, newScene, init=False):
        if self.currentScene == newScene:
            return False
        for scene in self.scenes:
            if (init and newScene != scene["name"]) or self.currentScene == scene["name"]:
                device.sendIconFor(scene["button"], scene["icon"], centered=True)
            elif newScene == scene["name"]:
                device.sendIconFor(scene["button"], scene["icon"], centered=True, marked=True)
        self.currentScene = newScene
        return True

    #Updates the buttons associated with states. Unless "init" is set to true, it only updates changed parts of the display and returns True if anything has changed so that the calling function should call updateDisplay()
    def updateStateButtons(self, device, scene, item, visible, init=False):
        anyUpdate = False
        for state in self.states:
            if init or ((scene, item) in state["items"] and visible != state["current"]):
                device.sendIconFor(state["button"], state["icon"], centered=True, crossed=(not (state["current"] if init else visible)))
                anyUpdate = True
                if not init:
                    state["current"] = visible
        return anyUpdate

    #Change LED colors if the microphones are muted
    def updateLED(self, device):
        if self.currentScene == "Video-Mute" or self.states[2]["current"] == False:
            leds = [0xff0000 for i in range(device.nLeds)] #Either this is the empty "Video-Mute" scene or the mics are muted -> red
        else:
            leds = [0x00ff00 for i in range(device.nLeds)] #In any other case the mics are live -> green
        device.setLeds(leds)

    def activate(self, device):
        self.ws = obsws("localhost", 4444) #Connect to websockets plugin in OBS

        #Callback if OBS is shutting down
        def on_exit(message):
            self.ws.disconnect()

        #Callback if the scene changes
        def on_scene(message):
            if self.updateSceneButtons(device, message.getSceneName()):
                device.updateDisplay() #Only update if parts of the display actually changed
            self.updateLED(device)

        #Callback if the visibility of a source changes
        def on_visibility_changed(message):
            if self.updateStateButtons(device, message.getSceneName(), message.getItemName(), message.getItemVisible()):
                device.updateDisplay() #Only update if parts of the display actually changed
            self.updateLED(device)

        #Register callbacks to OBS
        self.ws.register(on_exit, events.Exiting)
        self.ws.register(on_scene, events.SwitchScenes)
        self.ws.register(on_visibility_changed, events.SceneItemVisibilityChanged)

        self.ws.connect()

        device.sendTextFor("title", "OBS", inverted=True) #Title



        ### Buttons 2 to 5 set different scenes (Moderation, Closeup, Slides and Video Mute) ###

        for scene in self.scenes:
            device.assignKey(KeyCode["SW"+str(scene["button"])+"_PRESS"], [])
            device.assignKey(KeyCode["SW"+str(scene["button"])+"_RELEASE"], [])
            device.registerCallback(self.getSetSceneCallback(scene["name"]), KeyCode["SW"+str(scene["button"])+"_PRESS"])



        ### Button 6: Order!

        def stopOrder():
            self.ws.call(requests.SetSceneItemProperties("Order", visible=False))

        def playOrder():
            self.ws.call(requests.SetSceneItemProperties("Order", visible=True))
            Timer(3, stopOrder).start()


        device.assignKey(KeyCode["SW6_PRESS"], [])
        device.assignKey(KeyCode["SW6_RELEASE"], [])
        device.registerCallback(playOrder, KeyCode["SW6_PRESS"])
        device.sendIconFor(6, "icons/megaphone.png", centered=True)


        ### Buttons 7 to 9 toogle the visibility of items, some of which are present in multiple scenes (Mics, Picture-In-Picture cam, Video stream from phone) ###

        for state in self.states:
            device.assignKey(KeyCode["SW"+str(state["button"])+"_PRESS"], [])
            device.assignKey(KeyCode["SW"+str(state["button"])+"_RELEASE"], [])
            device.registerCallback(self.getToggleStateCallback(state), KeyCode["SW"+str(state["button"])+"_PRESS"])



        ### Get current state and initialize buttons accordingly ###
        current = self.ws.call(requests.GetSceneList())
        for scene in current.getScenes():
            for item in scene["sources"]:
                for state in self.states:
                    if (scene["name"], item["name"]) in state["items"]:
                        state["current"] = item["render"]

        #Call updateSceneButtons and updateStateButtons to initialize their images
        self.currentScene = None
        self.updateSceneButtons(device, current.getCurrentScene(), init=True)
        self.updateStateButtons(device, None, None, True, init=True)
        device.updateDisplay()
        self.updateLED(device)

    def poll(self, device):
        return False    #No polling required

    def animate(self, device):
        pass    #In this mode we want permanent LED illumination. Do not fade or animate otherwise.

    def deactivate(self, device):
        device.clearCallbacks() #Clear our callbacks if we switch to a different mode

