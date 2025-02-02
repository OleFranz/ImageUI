from ImageUI import errors
from ImageUI import states
import traceback
import win32gui
import ctypes
import mouse


def Update(WindowHWND):
    """
    Updates the UI.

    Parameters
    ----------
    WindowHWND : int
        The handle of the window.

    Returns
    -------
    None
    """
    try:
        RECT = win32gui.GetClientRect(WindowHWND)
        X1, Y1 = win32gui.ClientToScreen(WindowHWND, (RECT[0], RECT[1]))
        X2, Y2 = win32gui.ClientToScreen(WindowHWND, (RECT[2], RECT[3]))

        WindowX, WindowY = X1, Y1
        WindowWidth, WindowHeight = X2 - X1, Y2 - Y1

        MouseX, MouseY = mouse.get_position()
        MouseRelativeWindow = MouseX - WindowX, MouseY - WindowY
        if WindowWidth != 0 and WindowHeight != 0:
            MouseX = MouseRelativeWindow[0]/WindowWidth
            MouseY = MouseRelativeWindow[1]/WindowHeight
        else:
            MouseX = 0
            MouseY = 0

        ForegroundWindow = ctypes.windll.user32.GetForegroundWindow() == WindowHWND
        LeftClicked = ctypes.windll.user32.GetKeyState(0x01) & 0x8000 != 0 and ForegroundWindow
        RightClicked = ctypes.windll.user32.GetKeyState(0x02) & 0x8000 != 0 and ForegroundWindow
        states.ForegroundWindow = ForegroundWindow
        states.FrameWidth = WindowWidth
        states.FrameHeight = WindowHeight
        states.MouseX = MouseX
        states.MouseY = MouseY
        states.LastLeftClicked = states.LeftClicked
        states.LastRightClicked = states.RightClicked
        states.LeftClicked = LeftClicked
        states.RightClicked = RightClicked
    except:
        errors.ShowError("ImageUI - Error in function Update.", str(traceback.format_exc()))