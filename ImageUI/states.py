from ImageUI import Variables
from ImageUI import Errors
import threading
import traceback
import pynput

Frame = None
FrameWidth = 0
FrameHeight = 0

MouseX = 0
MouseY = 0

TopMostLayer = 0

LeftPressed = False
RightPressed = False
LastLeftPressed = False
LastRightPressed = False

LeftClicked = False
"""If the left mouse button was clicked. Clicked means pressed in the last update and released in the current update."""
RightClicked = False
"""If the right mouse button was clicked. Clicked means pressed in the last update and released in the current update."""
LeftClickPosition = 0, 0
"""The position at which the left mouse button was clicked. Does not get reset when the mouse button is not clicked."""
RightClickPosition = 0, 0
"""The position at which the right mouse button was clicked. Does not get reset when the mouse button is not clicked."""

ForegroundWindow = False
LastForegroundWindow = False

ScrollEventQueue = []
def HandleScrollEvents():
    try:
        global ScrollEventQueue
        with pynput.mouse.Events() as Events:
            while Variables.Exit == False:
                Event = Events.get()
                if isinstance(Event, pynput.mouse.Events.Scroll):
                    if 0 <= MouseX <= 1 and 0 <= MouseY <= 1 and ForegroundWindow:
                        ScrollEventQueue.append(Event)
                        Variables.ForceSingleRender = True
    except:
        Errors.ShowError("States - Error in function HandleScrollEvents.", str(traceback.format_exc()))
ScrollEventThread = threading.Thread(target=HandleScrollEvents, daemon=True).start()

AnyDropdownOpen = False