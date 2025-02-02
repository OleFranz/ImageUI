import SimpleWindow
import numpy as np
import ImageUI
import time

import ImageUI.elements
import ImageUI.settings
import ImageUI.translate

ImageUI.settings.DevelopmentMode = True
ImageUI.translate.Initialize(SourceLanguage="en", DestinationLanguage="de")

SimpleWindow.Initialize(Name="Test UI",
                        Size=(1280, 720),
                        Position=(100, 100), 
                        TitleBarColor=(0, 0, 0),
                        Resizable=True,
                        TopMost=False,
                        Foreground=True,
                        Minimized=False,
                        Undestroyable=False,
                        Icon="",
                        NoWarnings=False)

BackGround = np.zeros((720, 1280, 3), dtype=np.uint8)

SimpleWindow.Show(Name="Test UI", Frame=BackGround)

while True:
    Frame = BackGround.copy()

    ImageUI.states.Frame = Frame.copy()
    ImageUI.elements.Button(Text="This is a test button with a long text", X1=10, Y1=10, X2=400, Y2=100)
    Frame = ImageUI.states.Frame.copy()

    ImageUI.Update(SimpleWindow.GetHandle(Name="Test UI"))

    SimpleWindow.Show(Name="Test UI", Frame=Frame)

    WindowIsOpen = SimpleWindow.GetOpen(Name="Test UI")
    if WindowIsOpen != True:
        ImageUI.translate.SaveCache()
        break

    time.sleep(0.01)