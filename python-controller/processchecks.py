import sys
import psutil

if sys.platform in ['linux', 'linux2']:
    import Xlib
    import Xlib.display
    display = Xlib.display.Display()
    root = display.screen().root
elif sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
else:
    print("Unknown platform: " + sys.platform)

def getActiveProcesses():
    return {p.name() for p in psutil.process_iter(["name"])}

# Adapted from Martin Thoma on stackoverflow
# https://stackoverflow.com/a/36419702/8068814
def getActiveWindow():
    active_window_name = None
    try:
        if sys.platform in ['linux', 'linux2']:
            windowID = root.get_full_property(display.intern_atom('_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value[0]
            window = display.create_resource_object('window', windowID)
            return window.get_wm_class()[0]
        elif sys.platform in ['Windows', 'win32', 'cygwin']:
            window = win32gui.GetForegroundWindow()
            active_window_name = win32gui.GetWindowText(window)
        elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
            active_window_name = (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
    except:
        print("Could not get active window: ", sys.exc_info()[0])
    return active_window_name
