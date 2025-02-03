from ImageUI import translate
from ImageUI import elements
from ImageUI import settings
from ImageUI import colors
from ImageUI import errors
from ImageUI import states
import numpy as np
import traceback
import win32gui
import ctypes
import mouse


# MARK: SetTranslator
def SetTranslator(SourceLanguage=None, DestinationLanguage=None):
    """
    All the text from the UI will be translated. Available languages can be listed with GetTranslatorLanguages().

    Parameters
    ----------
    SourceLanguage : str
        The source language.
    DestinationLanguage : str
        The destination language.

    Returns
    -------
    None
    """
    translate.Initialize(SourceLanguage, DestinationLanguage)


# MARK: GetTranslatorLanguages
def GetTranslatorLanguages():
    """
    Returns the available languages.

    Returns
    -------
    dict
        The available languages.
    """
    return translate.GetAvailableLanguages()


# MARK: Button
def Button(Frame:np.ndarray, Text:str, X1:int, Y1:int, X2:int, Y2:int, Selected:bool = False, FontSize:float = settings.FontSize, RoundCorners:float = settings.CornerRoundness, TextColor:tuple = colors.TEXT_COLOR, Color:tuple = colors.BUTTON_COLOR, HoverColor:tuple = colors.BUTTON_HOVER_COLOR, SelectedColor:tuple = colors.BUTTON_SELECTED_COLOR, SelectedHoverColor:tuple = colors.BUTTON_SELECTED_HOVER_COLOR):
    """
    Creates a button.

    Parameters
    ----------
    Frame : np.ndarray
        The frame on which the button will be drawn.
    Text : str
        The text of the button.
    X1 : int
        The x coordinate of the top left corner.
    Y1 : int
        The y coordinate of the top left corner.
    X2 : int
        The x coordinate of the bottom right corner.
    Y2 : int
        The y coordinate of the bottom right corner.
    Selected : bool
        Whether the button is selected.
    FontSize : float
        The font size of the text.
    RoundCorners : float
        The roundness of the corners.
    TextColor : tuple
        The color of the text.
    Color : tuple
        The color of the button.
    HoverColor : tuple
        The color of the button when hovered.
    SelectedColor : tuple
        The color of the button when selected.
    SelectedHoverColor : tuple
        The color of the button when selected and hovered.

    Returns
    -------
    tuple of (bool, bool, bool)
        1. Clicked: Whether the button was clicked.
        2. Pressed: Whether the button is currently pressed.
        3. Hovered: Whether the button is currently hovered.
    """
    return elements.Button(Frame, Text, X1, Y1, X2, Y2, Selected, FontSize, RoundCorners, TextColor, Color, HoverColor, SelectedColor, SelectedHoverColor)


# MARK: Update
def Update(WindowHWND:int):
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


# MARK: Exit
def Exit():
    """
    Call this when exiting the UI module.

    Returns
    -------
    None
    """
    translate.SaveCache()