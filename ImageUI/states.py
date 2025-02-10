from ImageUI import variables
from ImageUI import errors
import threading
import traceback
import pynput

Frame = None
FrameWidth = 0
FrameHeight = 0

MouseX = 0
MouseY = 0

TopMostLayer = 0

LeftClicked = False
RightClicked = False
LastLeftClicked = False
LastRightClicked = False

ForegroundWindow = False
LastForegroundWindow = False

ScrollEventQueue = []
def HandleScrollEvents():
    try:
        global ScrollEventQueue
        with pynput.mouse.Events() as Events:
            while variables.Exit == False:
                Event = Events.get()
                if isinstance(Event, pynput.mouse.Events.Scroll):
                    ScrollEventQueue.append(Event)
                    variables.ForceSingleRender = True
    except:
        errors.ShowError("States - Error in function HandleScrollEvents.", str(traceback.format_exc()))
ScrollEventThread = threading.Thread(target=HandleScrollEvents, daemon=True).start()