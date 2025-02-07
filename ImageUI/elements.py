from PIL import Image, ImageDraw, ImageFont
from ImageUI import translations
from ImageUI import variables
from ImageUI import settings
from ImageUI import errors
from ImageUI import states
import traceback
import numpy
import cv2


# MARK: Label
def Label(Text, X1, Y1, X2, Y2, Layer, FontSize, TextColor):
    try:
        Text = translations.Translate(Text)
        Frame = Image.fromarray(variables.Frame)
        Font = ImageFont.truetype("arial.ttf", FontSize)
        Draw = ImageDraw.Draw(Frame)
        BBoxX1, BBoxY1, BBoxX2, BBoxY2 = Draw.textbbox((0, 0), Text, font=Font)
        Draw.text((round(X1 + (X2 - X1) / 2 - (BBoxX2 - BBoxX1) / 2), round(Y1 + (Y2 - Y1) / 2 - (BBoxY2 - BBoxY1) / 2)), Text, font=Font, fill=(TextColor[0], TextColor[1], TextColor[2], 255))
        variables.Frame = numpy.array(Frame)
    except:
        errors.ShowError("Elements - Error in function Label.", str(traceback.format_exc()))


# MARK: Button
def Button(Text, X1, Y1, X2, Y2, Layer, Selected, FontSize, RoundCorners, TextColor, Color, HoverColor, SelectedColor, SelectedHoverColor):
    try:
        if X1 <= states.MouseX * variables.Frame.shape[1] <= X2 and Y1 <= states.MouseY * variables.Frame.shape[0] <= Y2 and states.ForegroundWindow and states.TopMostLayer == Layer:
            Hovered = True
        else:
            Hovered = False
        if Selected == True:
            if Hovered == True:
                cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), SelectedHoverColor, RoundCorners, settings.RectangleLineType)
                cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), SelectedHoverColor,  - 1, settings.RectangleLineType)
            else:
                cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), SelectedColor, RoundCorners, settings.RectangleLineType)
                cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), SelectedColor,  - 1, settings.RectangleLineType)
        elif Hovered == True:
            cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, RoundCorners, settings.RectangleLineType)
            cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor,  - 1, settings.RectangleLineType)
        else:
            cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, RoundCorners, settings.RectangleLineType)
            cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color,  - 1, settings.RectangleLineType)
        Label(Text, X1, Y1, X2, Y2, Layer, FontSize, TextColor)
        if X1 <= states.MouseX * variables.Frame.shape[1] <= X2 and Y1 <= states.MouseY * variables.Frame.shape[0] <= Y2 and states.LeftClicked == False and states.LastLeftClicked == True:
            return states.ForegroundWindow and states.TopMostLayer == Layer, states.LeftClicked and Hovered, Hovered
        else:
            return False, states.LeftClicked and Hovered, Hovered
    except:
        errors.ShowError("Elements - Error in function Button.", str(traceback.format_exc()))
        return False, False, False