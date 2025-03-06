from ImageUI import Translations
from ImageUI import Variables
from ImageUI import Defaults
from ImageUI import Elements
from ImageUI import Settings
from ImageUI import Colors
from ImageUI import Errors
from ImageUI import States
import numpy as np
import traceback
import win32gui
import ctypes
import mouse
import time


# MARK: Label
def Label(Text:str, X1:int, Y1:int, X2:int, Y2:int, ID:str, Align:str = "Center", AlignPadding:int = 10, Layer:int = 0, FontSize:float = Defaults.FontSize, FontType:str = Defaults.FontType, Translate:bool = True, TextColor:tuple = Defaults.TextColor):
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
    ID : str
        A unique identifier for the label.
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
        if FontSize == Defaults.FontSize: FontSize = Settings.FontSize
        if FontType == Defaults.FontType: FontType = Settings.FontType
        if TextColor == Defaults.TextColor: TextColor = Colors.TextColor

        Variables.Elements.append(["Label",
                                   None,
                                   {"Text": Text,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "ID": ID,
                                    "Align": Align,
                                    "AlignPadding": AlignPadding,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "Translate": Translate,
                                    "TextColor": TextColor}])
    except:
        Errors.ShowError("ImageUI - Error in function Label.", str(traceback.format_exc()))


# MARK: Button
def Button(Text:str, X1:int, Y1:int, X2:int, Y2:int, ID:str, Layer:int = 0, OnPress:callable = None, FontSize:float = Defaults.FontSize, FontType:str = Defaults.FontType, RoundCorners:float = Defaults.CornerRoundness, Translate:bool = True, TextColor:tuple = Defaults.TextColor, Color:tuple = Defaults.ButtonColor, HoverColor:tuple = Defaults.ButtonHoverColor):
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
    ID : str
        A unique identifier for the button.
    Layer : int
        The layer of the button in the UI.
    OnPress : callable
        The function to call when the button was clicked.
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
        if FontSize == Defaults.FontSize: FontSize = Settings.FontSize
        if FontType == Defaults.FontType: FontType = Settings.FontType
        if RoundCorners == Defaults.CornerRoundness: RoundCorners = Settings.CornerRoundness
        if TextColor == Defaults.TextColor: TextColor = Colors.TextColor
        if Color == Defaults.ButtonColor: Color = Colors.ButtonColor
        if HoverColor == Defaults.ButtonHoverColor: HoverColor = Colors.ButtonHoverColor

        Variables.Elements.append(["Button",
                                   OnPress,
                                   {"Text": Text,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "ID": ID,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "RoundCorners": RoundCorners,
                                    "Translate": Translate,
                                    "TextColor": TextColor,
                                    "Color": Color,
                                    "HoverColor": HoverColor}])
    except:
        Errors.ShowError("ImageUI - Error in function Button.", str(traceback.format_exc()))


# MARK: Switch
def Switch(Text:str, X1:int, Y1:int, X2:int, Y2:int, ID:str, State:bool = False, SwitchWidth:int = 40, SwitchHeight:int = 20, TextPadding:int = 10, Layer:int = 0, OnChange:callable = None, FontSize:float = Defaults.FontSize, FontType:str = Defaults.FontType, Translate:bool = True, TextColor:tuple = Defaults.TextColor, SwitchColor=Defaults.SwitchColor, SwitchKnobColor=Defaults.SwitchKnobColor, SwitchHoverColor=Defaults.SwitchHoverColor, SwitchEnabledColor=Defaults.SwitchEnabledColor, SwitchEnabledHoverColor=Defaults.SwitchEnabledHoverColor):
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
    ID : str
        A unique identifier for the switch.
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
        if FontSize == Defaults.FontSize: FontSize = Settings.FontSize
        if FontType == Defaults.FontType: FontType = Settings.FontType
        if TextColor == Defaults.TextColor: TextColor = Colors.TextColor
        if SwitchColor == Defaults.SwitchColor: SwitchColor = Colors.SwitchColor
        if SwitchKnobColor == Defaults.SwitchKnobColor: SwitchKnobColor = Colors.SwitchKnobColor
        if SwitchHoverColor == Defaults.SwitchHoverColor: SwitchHoverColor = Colors.SwitchHoverColor
        if SwitchEnabledColor == Defaults.SwitchEnabledColor: SwitchEnabledColor = Colors.SwitchEnabledColor
        if SwitchEnabledHoverColor == Defaults.SwitchEnabledHoverColor: SwitchEnabledHoverColor = Colors.SwitchEnabledHoverColor

        Variables.Elements.append(["Switch",
                                   OnChange,
                                   {"Text": Text,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "ID": ID,
                                    "State": State,
                                    "SwitchWidth": SwitchWidth,
                                    "SwitchHeight": SwitchHeight,
                                    "TextPadding": TextPadding,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "Translate": Translate,
                                    "TextColor": TextColor,
                                    "SwitchColor": SwitchColor,
                                    "SwitchKnobColor": SwitchKnobColor,
                                    "SwitchHoverColor": SwitchHoverColor,
                                    "SwitchEnabledColor": SwitchEnabledColor,
                                    "SwitchEnabledHoverColor": SwitchEnabledHoverColor}])
    except:
        Errors.ShowError("ImageUI - Error in function Switch.", str(traceback.format_exc()))


# MARK: Input
def Input(X1:int, Y1:int, X2:int, Y2:int, ID:str, DefaultInput:str = "", Placeholder:str = "", TextAlign:str = "Left", TextAlignPadding:int = 10, Layer:int = 0, OnChange:callable = None, FontSize:float = Defaults.FontSize, FontType:str = Defaults.FontType, RoundCorners:float = Defaults.CornerRoundness, Translate:bool = True, TextColor:tuple = Defaults.TextColor, SecondaryTextColor:tuple = Defaults.GrayTextColor, Color:tuple = Defaults.InputColor, HoverColor:tuple = Defaults.InputHoverColor, ThemeColor:tuple = Defaults.InputThemeColor):
    """
    Creates an input box.

    Parameters
    ----------
    X1 : int
        The x coordinate of the top left corner.
    Y1 : int
        The y coordinate of the top left corner.
    X2 : int
        The x coordinate of the bottom right corner.
    Y2 : int
        The y coordinate of the bottom right corner.
    ID : str
        A unique identifier for the input box.
    DefaultInput : str
        The default text in the input.
    Placeholder : str
        The placeholder for the input.
    TextAlign : str
        The alignment of the text. (Left, Right, Center)
    TextAlignPadding : int
        The padding of the text when aligned left or right.
    Layer : int
        The layer of the button in the UI.
    OnChange : callable
        The function to call when the input is changed.
    FontSize : float
        The font size of the text.
    FontType : str
        The font type of the text.
    RoundCorners : float
        The roundness of the corners.
    TextColor : tuple
        The color of the text.
    SecondaryTextColor : tuple
        The color of the example text.
    Color : tuple
        The color of the input.
    HoverColor : tuple
        The color of the input when hovered.

    Returns
    -------
    None
    """
    try:
        if FontSize == Defaults.FontSize: FontSize = Settings.FontSize
        if FontType == Defaults.FontType: FontType = Settings.FontType
        if RoundCorners == Defaults.CornerRoundness: RoundCorners = Settings.CornerRoundness
        if TextColor == Defaults.TextColor: TextColor = Colors.TextColor
        if SecondaryTextColor == Defaults.GrayTextColor: SecondaryTextColor = Colors.GrayTextColor
        if Color == Defaults.InputColor: Color = Colors.InputColor
        if HoverColor == Defaults.InputHoverColor: HoverColor = Colors.InputHoverColor
        if ThemeColor == Defaults.InputThemeColor: ThemeColor = Colors.InputThemeColor

        Variables.Elements.append(["Input",
                                   OnChange,
                                   {"X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "ID": ID,
                                    "DefaultInput": DefaultInput,
                                    "Placeholder": Placeholder,
                                    "TextAlign": TextAlign,
                                    "TextAlignPadding": TextAlignPadding,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "RoundCorners": RoundCorners,
                                    "Translate": Translate,
                                    "TextColor": TextColor,
                                    "SecondaryTextColor": SecondaryTextColor,
                                    "Color": Color,
                                    "HoverColor": HoverColor,
                                    "ThemeColor": ThemeColor}])
    except:
        Errors.ShowError("ImageUI - Error in function Input.", str(traceback.format_exc()))


# MARK: Dropdown
def Dropdown(Title:str, Items:list, DefaultItem:any, X1:int, Y1:int, X2:int, Y2:int, ID:str, DropdownHeight:int = 100, DropdownPadding:int = 5, Layer:int = 0, OnChange:callable = None, FontSize:float = Defaults.FontSize, FontType:str = Defaults.FontType, RoundCorners:float = Defaults.CornerRoundness, Translate:bool = True, TextColor:tuple = Defaults.TextColor, SecondaryTextColor:tuple = Defaults.GrayTextColor, Color:tuple = Defaults.DropdownColor, HoverColor:tuple = Defaults.DropdownHoverColor):
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
    DefaultItem : any
        The item from the items list which is the default item.
    X1 : int
        The x coordinate of the top left corner.
    Y1 : int
        The y coordinate of the top left corner.
    X2 : int
        The x coordinate of the bottom right corner.
    Y2 : int
        The y coordinate of the bottom right corner.
    ID : str
        A unique identifier for the dropdown.
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
        if FontSize == Defaults.FontSize: FontSize = Settings.FontSize
        if FontType == Defaults.FontType: FontType = Settings.FontType
        if RoundCorners == Defaults.CornerRoundness: RoundCorners = Settings.CornerRoundness
        if TextColor == Defaults.TextColor: TextColor = Colors.TextColor
        if SecondaryTextColor == Defaults.GrayTextColor: SecondaryTextColor = Colors.GrayTextColor
        if Color == Defaults.DropdownColor: Color = Colors.DropdownColor
        if HoverColor == Defaults.DropdownHoverColor: HoverColor = Colors.DropdownHoverColor

        Variables.Elements.append(["Dropdown",
                                   OnChange,
                                   {"Title": Title,
                                    "Items": Items,
                                    "DefaultItem": DefaultItem,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "ID": ID,
                                    "DropdownHeight": DropdownHeight,
                                    "DropdownPadding": DropdownPadding,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "RoundCorners": RoundCorners,
                                    "Translate": Translate,
                                    "TextColor": TextColor,
                                    "SecondaryTextColor": SecondaryTextColor,
                                    "Color": Color,
                                    "HoverColor": HoverColor}])
    except:
        Errors.ShowError("ImageUI - Error in function Dropdown.", str(traceback.format_exc()))


# MARK: Image
def Image(Image:np.ndarray, X1:int, Y1:int, X2:int, Y2:int, ID:str, Layer:int = 0, OnPress:callable = None, RoundCorners:float = Defaults.CornerRoundness):
    """
    Creates an image.

    Parameters
    ----------
    Image : np.ndarray
        The image to draw.
    X1 : int
        The x coordinate of the top left corner.
    Y1 : int
        The y coordinate of the top left corner.
    X2 : int
        The x coordinate of the bottom right corner.
    Y2 : int
        The y coordinate of the bottom right corner.
    ID : str
        A unique identifier for the image.
    Layer : int
        The layer of the image in the UI.
    OnPress : callable
        The function to call when the image was clicked.
    RoundCorners : float
        The roundness of the corners.

    Returns
    -------
    None
    """
    try:
        if RoundCorners == Defaults.CornerRoundness: RoundCorners = Settings.CornerRoundness

        Variables.Elements.append(["Image",
                                   OnPress,
                                   {"Image": Image,
                                    "X1": X1,
                                    "Y1": Y1,
                                    "X2": X2,
                                    "Y2": Y2,
                                    "ID": ID,
                                    "Layer": Layer,
                                    "RoundCorners": RoundCorners}])
    except:
        Errors.ShowError("ImageUI - Error in function Image.", str(traceback.format_exc()))


# MARK: Popup
def Popup(Text:str, StartX1:int, StartY1:int, StartX2:int, StartY2:int, EndX1:int, EndY1:int, EndX2:int, EndY2:int, ID:str, Progress:float = 0, DoAnimation:bool = True, AnimationDuration:float = Defaults.PopupAnimationDuration, ShowDuration:float = Defaults.PopupShowDuration, Layer:int = 0, FontSize:float = Defaults.FontSize, FontType:str = Defaults.FontType, RoundCorners:float = Defaults.CornerRoundness, Translate:bool = True, TextColor:tuple = Defaults.TextColor, Color:tuple = Defaults.PopupColor, OutlineColor:tuple = Defaults.PopupOutlineColor, ProgressBarColor:tuple = Defaults.PopupProgressBarColor):
    """
    Creates a popup.

    If the `Progress` value is 0, the progress bar will not be shown.
    The `Progress` value should be between 0 and 100, if it is in this range, the `ShowDuration` value will be ignored and the popup will be shown indefinitely.
    If the `Progress` value is less than 0, an indeterminate progress bar will be shown.

    If the `ShowDuration` value is less or equal to 0, the popup will be shown indefinitely.

    Parameters
    ----------
    Text : str
        The text of the popup.
    StartX1 : int
        The x coordinate of the top left corner at the start of the animation.
    StartY1 : int
        The y coordinate of the top left corner at the start of the animation.
    StartX2 : int
        The x coordinate of the bottom right corner at the start of the animation.
    StartY2 : int
        The y coordinate of the bottom right corner at the start of the animation.
    EndX1 : int
        The x coordinate of the top left corner at the end of the animation.
    EndY1 : int
        The y coordinate of the top left corner at the end of the animation.
    EndX2 : int
        The x coordinate of the bottom right corner at the end of the animation.
    EndY2 : int
        The y coordinate of the bottom right corner at the end of the animation.
    ID : str
        A unique identifier for the popup.
    Progress : float
        The progress shown in the progress bar.
    DoAnimation : bool
        Whether to animate the popup. If set to false, the popup will be shown immediately at the end coordinates.
    AnimationDuration : float
        The duration of the animation in seconds.
    ShowDuration : float
        The duration of the popup in seconds. Negative values will show the popup indefinitely.
    Layer : int
        The layer of the popup in the UI.
    FontSize : float
        The font size of the text.
    FontType : str
        The font type of the text.
    RoundCorners : float
        The roundness of the corners.
    TextColor : tuple
        The color of the text.
    Color : tuple
        The color of the popup.
    OutlineColor : tuple
        The color of the outline of the popup.
    ProgressBarColor : tuple
        The color of the progress bar.

    Returns
    -------
    None
    """
    try:
        if AnimationDuration == Defaults.PopupAnimationDuration: AnimationDuration = Settings.PopupAnimationDuration
        if ShowDuration == Defaults.PopupShowDuration: ShowDuration = Settings.PopupShowDuration
        if FontSize == Defaults.FontSize: FontSize = Settings.FontSize
        if FontType == Defaults.FontType: FontType = Settings.FontType
        if RoundCorners == Defaults.CornerRoundness: RoundCorners = Settings.CornerRoundness
        if TextColor == Defaults.TextColor: TextColor = Colors.TextColor
        if Color == Defaults.PopupColor: Color = Colors.PopupColor
        if OutlineColor == Defaults.PopupOutlineColor: OutlineColor = Colors.PopupOutlineColor
        if ProgressBarColor == Defaults.PopupProgressBarColor: ProgressBarColor = Colors.PopupProgressBarColor

        Variables.Elements.append(["Popup",
                                   None,
                                   {"Text": Text,
                                    "StartX1": StartX1,
                                    "StartY1": StartY1,
                                    "StartX2": StartX2,
                                    "StartY2": StartY2,
                                    "EndX1": EndX1,
                                    "EndY1": EndY1,
                                    "EndX2": EndX2,
                                    "EndY2": EndY2,
                                    "ID": ID,
                                    "Progress": min(Progress, 100),
                                    "DoAnimation": DoAnimation,
                                    "AnimationDuration": AnimationDuration,
                                    "ShowDuration": ShowDuration,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "RoundCorners": RoundCorners,
                                    "Translate": Translate,
                                    "TextColor": TextColor,
                                    "Color": Color,
                                    "OutlineColor": OutlineColor,
                                    "ProgressBarColor": ProgressBarColor}])
    except:
        Errors.ShowError("ImageUI - Error in function Popup.", str(traceback.format_exc()))


# MARK: SetSwitch
def SetSwitch(ID:str, State:bool):
    """
    Set the state of a switch.
    Won't call the OnChange callback.

    Parameters
    ----------
    ID : str
        The ID of the switch to set.
    State : bool
        The state to set the switch to.

    Returns
    -------
    None
    """
    try:
        if Variables.Switches[ID][0] != State:
            Variables.Switches[ID] = State, time.time()
    except:
        Errors.ShowError("ImageUI - Error in function SetSwitch.", str(traceback.format_exc()))


# MARK: SetInput
def SetInput(ID:str, Input:str):
    """
    Set the text of an input.
    Won't call the OnChange callback.

    Parameters
    ----------
    ID : str
        The ID of the input to set.
    Input : str
        The text to set the input to.

    Returns
    -------
    None
    """
    try:
        if Variables.Inputs[ID][1] != Input:
            Variables.Inputs[ID] = Variables.Inputs[ID][0], Input
    except:
        Errors.ShowError("ImageUI - Error in function SetInput.", str(traceback.format_exc()))


# MARK: SetDropdown
def SetDropdown(ID:str, Items:list, SelectedItem:any):
    """
    Set the available items and selected item of a dropdown.
    Won't call the OnChange callback.

    Parameters
    ----------
    ID : str
        The ID of the dropdown to set.
    Items : list
        The items of the dropdown.
    SelectedItem : any
        The selected item of the dropdown.

    Returns
    -------
    None
    """
    try:
        if Variables.Dropdowns[ID][1] != Items:
            Variables.Dropdowns[ID] = Variables.Dropdowns[ID][0], Items, Variables.Dropdowns[ID][2]
        if Variables.Dropdowns[ID][2] != SelectedItem:
            try:
                SelectedItem = Variables.Dropdowns[ID][1].index(SelectedItem)
            except ValueError:
                SelectedItem = 0
            Variables.Dropdowns[ID] = Variables.Dropdowns[ID][0], Variables.Dropdowns[ID][1], SelectedItem
    except:
        Errors.ShowError("ImageUI - Error in function SetInput.", str(traceback.format_exc()))


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
        LeftPressed = ctypes.windll.user32.GetKeyState(0x01) & 0x8000 != 0 and ForegroundWindow and 0 <= MouseX <= 1 and 0 <= MouseY <= 1
        RightPressed = ctypes.windll.user32.GetKeyState(0x02) & 0x8000 != 0 and ForegroundWindow and 0 <= MouseX <= 1 and 0 <= MouseY <= 1
        LastLeftPressed = States.LeftPressed
        LastRightPressed = States.RightPressed
        States.FrameWidth = WindowWidth
        States.FrameHeight = WindowHeight
        States.MouseX = MouseX
        States.MouseY = MouseY
        States.LastLeftPressed = States.LeftPressed if ForegroundWindow else False
        States.LastRightPressed = States.RightPressed if ForegroundWindow else False
        States.LeftPressed = LeftPressed
        States.RightPressed = RightPressed
        if LastLeftPressed == False and LeftPressed == False and LastRightPressed == False and RightPressed == False:
            if ForegroundWindow != States.ForegroundWindow:
                Variables.ForceSingleRender = True
            States.ForegroundWindow = ForegroundWindow

        if LeftPressed == False and LastLeftPressed == True:
            States.LeftClicked = True
            States.LeftClickPosition = round(MouseX * WindowWidth), round(MouseY * WindowHeight)
        else:
            States.LeftClicked = False
        if RightPressed == False and LastRightPressed == True:
            States.RightClicked = True
            States.RightClickPosition = round(MouseX * WindowWidth), round(MouseY * WindowHeight)
        else:
            States.RightClicked = False


        RenderFrame = False

        for Area in Variables.Areas:
            if States.AnyDropdownOpen and Area[0] != "Dropdown":
                continue
            if States.AnyInputsOpen and Area[0] != "Input":
                continue
            if (Area[1] <= MouseX * WindowWidth <= Area[3] and Area[2] <= MouseY * WindowHeight <= Area[4]) != Area[6] and Area[5] == States.TopMostLayer:
                Area = (Area[1], Area[2], Area[3], Area[4], not Area[5])
                RenderFrame = True

        if ForegroundWindow == False and Variables.CachedFrame is not None:
            RenderFrame = False

        if np.array_equal(Frame, Variables.LastFrame) == False:
            RenderFrame = True
        Variables.LastFrame = Frame.copy()

        Variables.Elements = sorted(Variables.Elements, key=lambda Item: (Item[2]["Layer"], {"Image": 1, "Button": 2, "Switch": 3, "Input": 4, "Label": 5, "Dropdown": 6, "Popup": 7}.get(Item[0], 0)))

        List1 = [[Item[0], Item[2]] for Item in Variables.Elements]
        List2 = [[Item[0], Item[2]] for Item in Variables.LastElements]
        if len(List1) != len(List2):
            RenderFrame = True
        else:
            for i in range(len(List1)):
                Element1 = List1[i]
                Element2 = List2[i]
                if Element1[0] != Element2[0]:
                    RenderFrame = True
                else:
                    Dict1 = Element1[1]
                    Dict2 = Element2[1]

                    if Dict1.keys() != Dict2.keys():
                        RenderFrame = True
                    else:
                        for Key in Dict1:
                            Value1 = Dict1[Key]
                            Value2 = Dict2[Key]

                            if isinstance(Value1, np.ndarray) and isinstance(Value2, np.ndarray):
                                if not np.array_equal(Value1, Value2):
                                    RenderFrame = True
                            else:
                                if Value1 != Value2:
                                    RenderFrame = True

        if RenderFrame or Variables.ForceSingleRender or LastLeftPressed != LeftPressed:
            Variables.ForceSingleRender = False
            Variables.Frame = Frame.copy()
            Variables.Areas = []

            States.TopMostLayer = Variables.Elements[-1][2]["Layer"] if len(Variables.Elements) > 0 else 0
            if len(Variables.Popups) > 0: 
                States.TopMostLayer = max(States.TopMostLayer, max([Item["Layer"] for Item in Variables.Popups.values()]))

            States.AnyDropdownOpen = any([Item for Item in Variables.Dropdowns if Variables.Dropdowns[Item][0] == True])
            States.AnyInputsOpen = any([Item for Item in Variables.Inputs if Variables.Inputs[Item][0] == True])

            for Item in Variables.Elements:
                ItemType = Item[0]
                ItemFunction = Item[1]

                if ItemType == "Label":
                    Elements.Label(**Item[2])

                elif ItemType == "Button":
                    Clicked, Pressed, Hovered = Elements.Button(**Item[2])
                    Variables.Areas.append((ItemType, Item[2]["X1"], Item[2]["Y1"], Item[2]["X2"], Item[2]["Y2"], Item[2]["Layer"], Pressed or Hovered))

                    if Clicked:
                        if ItemFunction is not None:
                            ItemFunction()
                        Variables.ForceSingleRender = True

                elif ItemType == "Switch":
                    State, Changed, Pressed, Hovered = Elements.Switch(**Item[2])
                    Variables.Areas.append((ItemType, Item[2]["X1"], Item[2]["Y1"], Item[2]["X2"], Item[2]["Y2"], Item[2]["Layer"], Pressed or Hovered))

                    if Changed:
                        if ItemFunction is not None:
                            ItemFunction(State)
                        Variables.ForceSingleRender = True

                elif ItemType == "Input":
                    Input, Changed, Selected, Pressed, Hovered = Elements.Input(**Item[2])
                    Variables.Areas.append((ItemType, Item[2]["X1"], Item[2]["Y1"], Item[2]["X2"], Item[2]["Y2"], Item[2]["Layer"], Pressed or Hovered))

                    if Changed:
                        if ItemFunction is not None:
                            ItemFunction(Input)
                        Variables.ForceSingleRender = True

                elif ItemType == "Dropdown":
                    SelectedItem, Changed, Selected, Pressed, Hovered = Elements.Dropdown(**Item[2])
                    Variables.Areas.append((ItemType, Item[2]["X1"], Item[2]["Y1"], Item[2]["X2"], Item[2]["Y2"] + ((Item[2]["DropdownHeight"] + Item[2]["DropdownPadding"]) if Selected else 0), Item[2]["Layer"], Pressed or Hovered))

                    if Changed:
                        if ItemFunction is not None:
                            ItemFunction(SelectedItem)
                        Variables.ForceSingleRender = True

                elif ItemType == "Image":
                    Clicked = Elements.Image(**Item[2])

                    if Clicked:
                        if ItemFunction is not None:
                            ItemFunction()
                        Variables.ForceSingleRender = True

                elif ItemType == "Popup":
                    Elements.Popup(**Item[2])

            Variables.CachedFrame = Variables.Frame.copy()
            Variables.LastElements = Variables.Elements

            if Settings.DevelopmentMode:
                print(f"New Frame Rendered! ({round(time.time(), 1)})")

        Variables.Frame = Variables.CachedFrame.copy()
        Elements.CheckAndRenderPopups()

        Variables.Elements = []

        return Variables.Frame
    except:
        Errors.ShowError("ImageUI - Error in function Update.", str(traceback.format_exc()))
        return Frame


# MARK: Exit
def Exit():
    """
    Call this when exiting the UI module.

    Returns
    -------
    None
    """
    Translations.SaveCache()
    Variables.Exit = True