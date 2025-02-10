from ImageUI import translations
from ImageUI import variables
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
import time


# MARK: Label
def Label(Text:str, X1:int, Y1:int, X2:int, Y2:int, Align:str = "Center", AlignPadding:int = 10, Layer:int = 0, FontSize:float = settings.FontSize, FontType:str = settings.FontType, TextColor:tuple = colors.TEXT_COLOR):
    """
    Creates a label.

    Parameters
    ----------
    Text : str
        The text of the label.
    X1 : int
        The x coordinate of the top left corner.
    Y1 : int
        The y coordinate of the top left corner.
    X2 : int
        The x coordinate of the bottom right corner.
    Y2 : int
        The y coordinate of the bottom right corner.
    Align : str
        The alignment of the text. (Left, Right, Center)
    AlignPadding : int
        The padding of the text when aligned left or right.
    Layer : int
        The layer of the label in the UI.
    FontSize : float
        The font size of the text.
    FontType : str
        The font type of the text.
    TextColor : tuple
        The color of the text.

    Returns
    -------
    None
    """
    try:
        variables.Elements.append(["Label",
                                   None,
                                   {"Text": Text,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "Align": Align,
                                    "AlignPadding": AlignPadding,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "TextColor": TextColor}])
    except:
        errors.ShowError("ImageUI - Error in function Label.", str(traceback.format_exc()))


# MARK: Button
def Button(Text:str, X1:int, Y1:int, X2:int, Y2:int, Layer:int = 0, OnPress:callable = None, FontSize:float = settings.FontSize, FontType:str = settings.FontType, RoundCorners:float = settings.CornerRoundness, TextColor:tuple = colors.TEXT_COLOR, Color:tuple = colors.BUTTON_COLOR, HoverColor:tuple = colors.BUTTON_HOVER_COLOR):
    """
    Creates a button.

    **OnPress Usage:**

    **1. Using a pre-defined function:**

    ```python
    def ButtonCallback():
        print("Button Pressed!")

    ImageUI.Button(..., OnPress=ButtonCallback, ...)
    ```

    **2. Using a lambda function for simple actions:**

    ```python
    ImageUI.Button(..., OnPress=lambda: print("Button Pressed!"), ...)
    ```

    Parameters
    ----------
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
    Layer : int
        The layer of the button in the UI.
    OnPress : callable
        The function to call when the button is clicked.
    FontSize : float
        The font size of the text.
    FontType : str
        The font type of the text.
    RoundCorners : float
        The roundness of the corners.
    TextColor : tuple
        The color of the text.
    Color : tuple
        The color of the button.
    HoverColor : tuple
        The color of the button when hovered.

    Returns
    -------
    None
    """
    try:
        variables.Elements.append(["Button",
                                   OnPress,
                                   {"Text": Text,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "RoundCorners": RoundCorners,
                                    "TextColor": TextColor,
                                    "Color": Color,
                                    "HoverColor": HoverColor}])
    except:
        errors.ShowError("ImageUI - Error in function Button.", str(traceback.format_exc()))


# MARK: Switch
def Switch(Text:str, X1:int, Y1:int, X2:int, Y2:int, State:bool = False, SwitchWidth:int = 40, SwitchHeight:int = 20, TextPadding:int = 5, Layer:int = 0, OnChange:callable = None, FontSize:float = settings.FontSize, FontType:str = settings.FontType, TextColor:tuple = colors.TEXT_COLOR, SwitchColor=colors.SWITCH_COLOR, SwitchKnobColor=colors.SWITCH_KNOB_COLOR, SwitchHoverColor=colors.SWITCH_HOVER_COLOR, SwitchEnabledColor=colors.SWITCH_ENABLED_COLOR, SwitchEnabledHoverColor=colors.SWITCH_ENABLED_HOVER_COLOR):
    """
    Creates a switch.

    **OnChange Usage:**

    **1. Using a pre-defined function:**

    ```python
    def SwitchCallback(State:bool):
        if State == True:
            print("Switch is ON!")
        else:
            print("Switch is OFF!")

    ImageUI.Switch(..., OnChange=SwitchCallback, ...)
    ```

    **2. Using a lambda function for simple actions:**

    ```python
    ImageUI.Switch(..., OnChange=lambda State: print(f"Switch state changed to: {State}"), ...)
    ```

    Parameters
    ----------
    Text : str
        The text of the switch.
    X1 : int
        The x coordinate of the top left corner.
    Y1 : int
        The y coordinate of the top left corner.
    X2 : int
        The x coordinate of the bottom right corner.
    Y2 : int
        The y coordinate of the bottom right corner.
    State : bool
        The state of the switch.
    SwitchWidth : int
        The width of the switch.
    SwitchHeight : int
        The height of the switch.
    TextPadding : int
        The padding between the text and the switch.
    Layer : int
        The layer of the switch in the UI.
    OnChange : callable
        The function to call when the switch is changed.
    FontSize : float
        The font size of the text.
    FontType : str
        The font type of the text.
    TextColor : tuple
        The color of the text.
    SwitchColor : tuple
        The color of the switch.
    SwitchKnobColor : tuple
        The color of the switch knob.
    SwitchHoverColor : tuple
        The color of the switch when hovered.
    SwitchEnabledColor : tuple
        The color of the switch when enabled.
    SwitchEnabledHoverColor : tuple
        The color of the switch when enabled and hovered.

    Returns
    -------
    None
    """
    try:
        variables.Elements.append(["Switch",
                                   OnChange,
                                   {"Text": Text,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "State": State,
                                    "SwitchWidth": SwitchWidth,
                                    "SwitchHeight": SwitchHeight,
                                    "TextPadding": TextPadding,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "TextColor": TextColor,
                                    "SwitchColor": SwitchColor,
                                    "SwitchKnobColor": SwitchKnobColor,
                                    "SwitchHoverColor": SwitchHoverColor,
                                    "SwitchEnabledColor": SwitchEnabledColor,
                                    "SwitchEnabledHoverColor": SwitchEnabledHoverColor}])
    except:
        errors.ShowError("ImageUI - Error in function Switch.", str(traceback.format_exc()))


# MARK: Dropdown
def Dropdown(Title:str, Items:list, DefaultItem:int, X1:int, Y1:int, X2:int, Y2:int, DropdownHeight:int = 100, DropdownPadding:int = 5, Layer:int = 0, OnChange:callable = None, FontSize:float = settings.FontSize, FontType:str = settings.FontType, RoundCorners:float = settings.CornerRoundness, TextColor:tuple = colors.TEXT_COLOR, SecondaryTextColor:tuple = colors.GRAY_TEXT_COLOR, Color:tuple = colors.DROPDOWN_COLOR, HoverColor:tuple = colors.DROPDOWN_HOVER_COLOR):
    """
    Creates a dropdown.

    **OnChange Usage:**

    **1. Using a pre-defined function:**

    ```python
    def DropdownCallback(SelectedItem):
        print(f"Dropdown item selected: {SelectedItem}")

    ImageUI.Dropdown(..., OnChange=DropdownCallback, ...)
    ```

    **2. Using a lambda function for simple actions:**

    ```python
    ImageUI.Dropdown(..., OnChange=lambda SelectedItem: print(f"Dropdown item selected: {SelectedItem}"), ...)
    ```

    Parameters
    ----------
    Title : str
        The title of the dropdown.
    Items : list
        The items of the dropdown.
    X1 : int
        The x coordinate of the top left corner.
    Y1 : int
        The y coordinate of the top left corner.
    X2 : int
        The x coordinate of the bottom right corner.
    Y2 : int
        The y coordinate of the bottom right corner.
    DefaultItem : int
        The index of the default item.
    DropdownHeight : int
        The height of the dropdown.
    DropdownPadding : int
        The padding between the title and the dropdown box.
    Layer : int
        The layer of the button in the UI.
    OnChange : callable
        The function to call when the selected item is changed.
    FontSize : float
        The font size of the text.
    FontType : str
        The font type of the text.
    RoundCorners : float
        The roundness of the corners.
    TextColor : tuple
        The color of the text.
    SecondaryTextColor : tuple
        The color of the secondary text.
    Color : tuple
        The color of the button.
    HoverColor : tuple
        The color of the button when hovered.

    Returns
    -------
    None
    """
    try:
        variables.Elements.append(["Dropdown",
                                   OnChange,
                                   {"Title": Title,
                                    "Items": Items,
                                    "DefaultItem": DefaultItem,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "DropdownHeight": DropdownHeight,
                                    "DropdownPadding": DropdownPadding,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "RoundCorners": RoundCorners,
                                    "TextColor": TextColor,
                                    "SecondaryTextColor": SecondaryTextColor,
                                    "Color": Color,
                                    "HoverColor": HoverColor}])
    except:
        errors.ShowError("ImageUI - Error in function Dropdown.", str(traceback.format_exc()))


# MARK: Update
def Update(WindowHWND:int, Frame:np.ndarray):
    """
    Updates the UI.

    Parameters
    ----------
    WindowHWND : int
        The handle of the window which is showing the UI.
    Frame : np.ndarray
        The frame on which the ui will be drawn.

    Returns
    -------
    np.ndarray
        The new frame with the UI drawn on it.
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
        LastLeftClicked = states.LeftClicked
        LastRightClicked = states.RightClicked
        states.FrameWidth = WindowWidth
        states.FrameHeight = WindowHeight
        states.MouseX = MouseX
        states.MouseY = MouseY
        states.LastLeftClicked = states.LeftClicked if ForegroundWindow else False
        states.LastRightClicked = states.RightClicked if ForegroundWindow else False
        states.LeftClicked = LeftClicked if ForegroundWindow else False
        states.RightClicked = RightClicked if ForegroundWindow else False
        if LastLeftClicked == False and LeftClicked == False and LastRightClicked == False and RightClicked == False:
            states.ForegroundWindow = ForegroundWindow


        RenderFrame = False

        for Area in variables.Areas:
            if Area[0] != "Label":
                if (Area[1] <= MouseX * WindowWidth <= Area[3] and Area[2] <= MouseY * WindowHeight <= Area[4]) != Area[6] and Area[5] == states.TopMostLayer:
                    Area = (Area[1], Area[2], Area[3], Area[4], not Area[5])
                    RenderFrame = True

        if ForegroundWindow == False and variables.CachedFrame is not None:
            RenderFrame = False

        if np.array_equal(Frame, variables.LastFrame) == False:
            RenderFrame = True
        variables.LastFrame = Frame.copy()

        if [[Item[0], Item[2]] for Item in variables.Elements] != [[Item[0], Item[2]] for Item in variables.LastElements]:
            RenderFrame = True

        if RenderFrame or variables.ForceSingleRender or LastLeftClicked != LeftClicked:
            variables.ForceSingleRender = False

            variables.Elements = sorted(variables.Elements, key=lambda Item: Item[2]["Layer"])
            states.TopMostLayer = variables.Elements[-1][2]["Layer"] if len(variables.Elements) > 0 else 0

            variables.Frame = Frame.copy()
            variables.Areas = []

            for Item in variables.Elements:
                ItemType = Item[0]
                ItemFunction = Item[1]

                if ItemType == "Label":
                    elements.Label(**Item[2])
                    variables.Areas.append((ItemType, Item[2]["X1"], Item[2]["Y1"], Item[2]["X2"], Item[2]["Y2"], Item[2]["Layer"]))

                elif ItemType == "Button":
                    Clicked, Pressed, Hovered = elements.Button(**Item[2])
                    variables.Areas.append((ItemType, Item[2]["X1"], Item[2]["Y1"], Item[2]["X2"], Item[2]["Y2"], Item[2]["Layer"], Pressed or Hovered))

                    if Clicked:
                        if ItemFunction is not None:
                            ItemFunction()
                        variables.ForceSingleRender = True

                elif ItemType == "Switch":
                    State, Changed, Pressed, Hovered = elements.Switch(**Item[2])
                    variables.Areas.append((ItemType, Item[2]["X1"], Item[2]["Y1"], Item[2]["X2"], Item[2]["Y2"], Item[2]["Layer"], Pressed or Hovered))

                    if Changed:
                        if ItemFunction is not None:
                            ItemFunction(State)
                        variables.ForceSingleRender = True

                elif ItemType == "Dropdown":
                    SelectedItem, Changed, Selected, Pressed, Hovered = elements.Dropdown(**Item[2])
                    variables.Areas.append((ItemType, Item[2]["X1"], Item[2]["Y1"], Item[2]["X2"], Item[2]["Y2"] + ((Item[2]["DropdownHeight"] + Item[2]["DropdownPadding"]) if Selected else 0), Item[2]["Layer"], Pressed or Hovered))

                    if Changed:
                        if ItemFunction is not None:
                            ItemFunction(SelectedItem)
                        variables.ForceSingleRender = True

            variables.CachedFrame = variables.Frame.copy()
            variables.LastElements = variables.Elements

            if settings.DevelopmentMode:
                print(f"New Frame Rendered! ({round(time.time(), 1)})")

        variables.Elements = []

        return variables.CachedFrame
    except:
        errors.ShowError("ImageUI - Error in function Update.", str(traceback.format_exc()))
        return Frame


# MARK: Exit
def Exit():
    """
    Call this when exiting the UI module.

    Returns
    -------
    None
    """
    translations.SaveCache()
    variables.Exit = True