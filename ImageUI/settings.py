import tempfile
import cv2
import os

SourceLanguage:str = "en"
DestinationLanguage:str = "en"
DevelopmentMode:bool = False
CachePath:str = os.path.join(tempfile.gettempdir(), "ImageUI-Cache")

FontSize:float = 11
FontType:int = cv2.FONT_HERSHEY_SIMPLEX
CornerRoundness:float = 5