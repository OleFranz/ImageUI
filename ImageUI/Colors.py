RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
NORMAL = "\033[0m"


Theme = "Dark"

TextColor = (255, 255, 255)
GrayTextColor = (155, 155, 155)

ButtonColor = (42, 42, 42)
ButtonHoverColor = (47, 47, 47)

SwitchColor = (60, 60, 60)
SwitchHoverColor = (65, 65, 65)
SwitchKnobColor = (28, 28, 28)
SwitchEnabledColor = (255, 200, 87)
SwitchEnabledHoverColor = (255, 200, 87)

InputColor = (42, 42, 42)
InputHoverColor = (47, 47, 47)
InputThemeColor = (208, 208, 208)

DropdownColor = (42, 42, 42)
DropdownHoverColor = (47, 47, 47)

PopupColor = (42, 42, 42)
PopupOutlineColor = (155, 155, 155)
PopupProgressBarColor = (255, 200, 87)

def SetTheme(Theme:str):
    """
    Sets the theme of the UI.

    Parameters
    ----------
    Theme : str
        The theme to set to. Can be either "Dark" or "Light".

    Returns
    -------
    None
    """
    global TextColor; TextColor = (255, 255, 255) if Theme == "Dark" else (0, 0, 0)
    global GrayTextColor; GrayTextColor = (155, 155, 155) if Theme == "Dark" else (100, 100, 100)

    global ButtonColor; ButtonColor = (42, 42, 42) if Theme == "Dark" else (236, 236, 236)
    global ButtonHoverColor; ButtonHoverColor = (47, 47, 47) if Theme == "Dark" else (231, 231, 231)

    global SwitchColor; SwitchColor = (60, 60, 60) if Theme == "Dark" else (208, 208, 208)
    global SwitchHoverColor; SwitchHoverColor = (65, 65, 65) if Theme == "Dark" else (203, 203, 203)
    global SwitchKnobColor; SwitchKnobColor = (28, 28, 28) if Theme == "Dark" else (250, 250, 250)
    global SwitchEnabledColor; SwitchEnabledColor = (255, 200, 87) if Theme == "Dark" else (184, 95, 0)
    global SwitchEnabledHoverColor; SwitchEnabledHoverColor = (255, 200, 87) if Theme == "Dark" else (184, 95, 0)

    global InputColor; InputColor = (42, 42, 42) if Theme == "Dark" else (236, 236, 236)
    global InputHoverColor; InputHoverColor = (47, 47, 47) if Theme == "Dark" else (231, 231, 231)
    global InputThemeColor; InputThemeColor = (208, 208, 208) if Theme == "Dark" else (60, 60, 60)

    global DropdownColor; DropdownColor = (42, 42, 42) if Theme == "Dark" else (236, 236, 236)
    global DropdownHoverColor; DropdownHoverColor = (47, 47, 47) if Theme == "Dark" else (231, 231, 231)

    global PopupColor; PopupColor = (42, 42, 42) if Theme == "Dark" else (236, 236, 236)
    global PopupOutlineColor; PopupOutlineColor = (155, 155, 155) if Theme == "Dark" else (100, 100, 100)
    global PopupProgressBarColor; PopupProgressBarColor = (255, 200, 87) if Theme == "Dark" else (184, 95, 0)