# ImageUI

A package for easily creating UIs in Python, mainly using OpenCV's drawing functions.

## Installation

```
pip install ImageUI
```

## Usage

```python
import SimpleWindow
import ImageUI
import numpy
import time

# Create a background to render the UI on
Background = numpy.zeros((250, 400, 3), dtype=numpy.uint8)
Background[:] = (28, 28, 28)

# Initialize a window could be a OpenCV window too
SimpleWindow.Initialize(Name="Example UI",
                        Size=(Background.shape[1], Background.shape[0]),
                        Position=(100, 100),
                        TitleBarColor=(28, 28, 28),
                        Resizable=False,
                        TopMost=False,
                        Foreground=True,
                        Minimized=False,
                        Undestroyable=False,
                        Icon="",
                        NoWarnings=False)

# Get all available translation languages
TranslationLanguages = list(ImageUI.Translations.GetAvailableLanguages().keys())

def SetTranslator(Language):
    # Set the auto UI translator, automatically translates all the UI elements
    ImageUI.SetTranslator(SourceLanguage="English", DestinationLanguage=Language)

def SetTheme(Theme):
    ThemeColor = (28, 28, 28) if Theme == "Dark" else (250, 250, 250)
    Background[:] = ThemeColor
    # Set the ImageUI theme, either "Dark" or "Light"
    ImageUI.SetTheme(Theme)
    SimpleWindow.SetTitleBarColor(Name="Example UI", Color=ThemeColor)

while True:
    # Add a button to the UI
    ImageUI.Button(Text="Button",
                   X1=10,
                   Y1=10,
                   X2=150,
                   Y2=45,
                   ID="Button",
                   OnPress=lambda: print("Button pressed!"))

    # Add a switch to the UI
    ImageUI.Switch(Text="Switch",
                   X1=10,
                   Y1=55,
                   X2=150,
                   Y2=80,
                   ID="Switch",
                   OnChange=lambda State: print("Switch changed to:", State))

    # Add a label to the UI
    ImageUI.Label(Text="This is a Label",
                  X1=200,
                  Y1=55,
                  X2=380,
                  Y2=80,
                  ID="Label")

    # Add a dropdown for language selection to the UI
    ImageUI.Dropdown(Title="Dropdown",
                     Items=TranslationLanguages,
                     DefaultItem="English",
                     X1=10,
                     Y1=90,
                     X2=190,
                     Y2=125,
                     ID="LanguageDropdown",
                     OnChange=SetTranslator)

    # Add a dropdown for theme selection to the UI
    ImageUI.Dropdown(Title="Theme",
                     Items=["Dark", "Light"],
                     DefaultItem="Dark",
                     X1=200,
                     Y1=90,
                     X2=380,
                     Y2=125,
                     ID="ThemeDropdown",
                     OnChange=SetTheme)

    # Add an input to the UI
    ImageUI.Input(X1=10,
                  Y1=135,
                  X2=380,
                  Y2=170,
                  Placeholder="Enter something...",
                  ID="Input",
                  OnChange=lambda Text: print("Input changed to:", Text))

    # Get the window handle
    WindowHandle = SimpleWindow.GetHandle(Name="Example UI")

    # Render the UI on the background
    Frame = ImageUI.Update(WindowHWND=WindowHandle, Frame=Background)

    # Show the background with the UI rendered on it
    SimpleWindow.Show(Name="Example UI", Frame=Frame)
    if SimpleWindow.GetOpen(Name="Example UI") != True:
        # Saves cache like translations
        ImageUI.Exit()
        break

    # Limit to about 60 FPS
    time.sleep(1 / 60)
```