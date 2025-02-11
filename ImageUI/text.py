from ImageUI import Settings
from ImageUI import Errors
import traceback
import os


# MARK: SetFontSize
def SetFontSize(FontSize:float = 13):
    """
    Set the font size of the UI Elements.

    Parameters
    ----------
    FontSize : float
        The font size to use.

    Returns
    -------
    None
    """
    try:
        if 0.5 <= float(FontSize) <= 65535.4:
            Settings.FontSize = float(FontSize)
        else:
            Errors.ShowError("Text - Invalid font size.", f"Invalid font size: {FontSize}\nFont size must be between 0.5 and 65535.4.")
    except:
        Errors.ShowError("Text - Error in function SetFontSize.", str(traceback.format_exc()))


# MARK: SetFontType
def SetFontType(FontType:str = "arial.ttf"):
    """
    Set the font type of the UI Elements.

    Parameters
    ----------
    FontType : str
        The font type to use.

    Returns
    -------
    None
    """
    try:
        ParsedFontType = FontType
        if ParsedFontType.endswith(".ttf") == False:
            ParsedFontType += ".ttf"
        if ParsedFontType in ListFontTypes():
            Settings.FontType = ParsedFontType
        else:
            Errors.ShowError("Text - Invalid font type.", f"Invalid font type: {FontType}\nUse ImageUI.Text.ListFontTypes() to get a list of available font types.")
    except:
        Errors.ShowError("Text - Error in function SetFontType.", str(traceback.format_exc()))


# MARK: ListFontTypes
def ListFontTypes():
    """
    List all the available .ttf fonts in the system fonts folder.

    Returns
    -------
    list
        The available .ttf fonts in the system fonts folder.
    """
    try:
        FontPath = os.path.join(os.environ["SystemRoot"], "Fonts")
        AvailableFonts = [File for File in os.listdir(FontPath) if File.endswith(".ttf")]
        return AvailableFonts
    except:
        Errors.ShowError("Text - Error in function ListFontTypes.", str(traceback.format_exc()))
        return []