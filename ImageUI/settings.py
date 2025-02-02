import tempfile
import cv2
import os

SourceLanguage = "en"
DestinationLanguage = "en"
DevelopmentMode = False
CachePath = os.path.join(tempfile.gettempdir(), "ImageUI-Cache")

FontSize:float = 11
FontType:int = cv2.FONT_HERSHEY_SIMPLEX
CornerRoundness:float = 5