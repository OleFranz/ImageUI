import tempfile
import cv2
import os

SourceLanguage:str = "en"
"""The Language to translate from."""
DestinationLanguage:str = "en"
"""The Language to translate to."""
DevelopmentMode:bool = False
"""Whether the UI is in development mode."""
CachePath:str = os.path.join(tempfile.gettempdir(), "ImageUI-Cache")
"""The path to the cache directory, things like translations are saved there."""

FontSize:float = 13
"""The font size of the UI Elements."""
FontType:str = "arial.ttf"
"""The cv2.FONT_{?} font type to use."""
LineType:int = cv2.LINE_AA
"""The cv2.LINE_{?} line type to use."""
TextLineType:int = cv2.LINE_AA
"""The cv2.LINE_{?} line type to use for text."""
CircleLineType:int = cv2.LINE_AA
"""The cv2.LINE_{?} line type to use for circles."""
RectangleLineType:int = cv2.LINE_AA
"""The cv2.LINE_{?} line type to use for rectangles."""
CornerRoundness:float = 5
"""The roundness of the corners of the UI Elements."""

SwitchAnimationDuration:float = 0.3333
"""The duration of the switch animation in seconds."""
PopupAnimationDuration:float = 0.5
"""The duration of the popup animation in seconds."""
PopupShowDuration:float = 5
"""The duration of the popup show in seconds."""