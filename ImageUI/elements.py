from PIL import Image, ImageDraw, ImageFont
from ImageUI import translations
from ImageUI import variables
from ImageUI import settings
from ImageUI import errors
from ImageUI import states
import traceback
import numpy
import math
import time
import cv2


# MARK: Label
def Label(Text, X1, Y1, X2, Y2, Align, AlignPadding, Layer, FontSize, FontType, TextColor):
    try:
        if Text == "": return
        Text = translations.Translate(Text)
        if f"{FontSize}-{FontType}" in variables.Fonts:
            Font = variables.Fonts[f"{FontSize}-{FontType}"]
        else:
            Font = ImageFont.truetype(FontType, FontSize)
            variables.Fonts[f"{FontSize}-{FontType}"] = Font
        Frame = Image.fromarray(variables.Frame)
        Draw = ImageDraw.Draw(Frame)
        BBoxX1, BBoxY1, BBoxX2, BBoxY2 = Draw.textbbox((0, 0), Text, font=Font)
        if Align.lower() == "left":
            X = round(X1 + BBoxX1 + AlignPadding)
        elif Align.lower() == "right":
            X = round(X2 - BBoxX2 - AlignPadding)
        else:
            X = round(X1 + (X2 - X1) / 2 - (BBoxX2 - BBoxX1) / 2)
        Y = round(Y1 + (Y2 - Y1) / 2 - (BBoxY2 - BBoxY1) / 2)
        Draw.text((X, Y), Text, font=Font, fill=(TextColor[0], TextColor[1], TextColor[2], 255))
        variables.Frame = numpy.array(Frame)
    except:
        errors.ShowError("Elements - Error in function Label.", str(traceback.format_exc()))


# MARK: Button
def Button(Text, X1, Y1, X2, Y2, Layer, FontSize, FontType, RoundCorners, TextColor, Color, HoverColor):
    try:
        if X1 <= states.MouseX * variables.Frame.shape[1] <= X2 and Y1 <= states.MouseY * variables.Frame.shape[0] <= Y2 and states.ForegroundWindow and states.TopMostLayer == Layer:
            Hovered = True
        else:
            Hovered = False
        if Hovered == True:
            cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, RoundCorners, settings.RectangleLineType)
            cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor,  - 1, settings.RectangleLineType)
        else:
            cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, RoundCorners, settings.RectangleLineType)
            cv2.rectangle(variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color,  - 1, settings.RectangleLineType)
        Label(Text, X1, Y1, X2, Y2, "Center", 0, Layer, FontSize, FontType, TextColor)
        if X1 <= states.MouseX * variables.Frame.shape[1] <= X2 and Y1 <= states.MouseY * variables.Frame.shape[0] <= Y2 and states.LeftClicked == False and states.LastLeftClicked == True:
            return states.ForegroundWindow and states.TopMostLayer == Layer, states.LeftClicked and Hovered, Hovered
        else:
            return False, states.LeftClicked and Hovered, Hovered
    except:
        errors.ShowError("Elements - Error in function Button.", str(traceback.format_exc()))
        return False, False, False


# MARK: Switch
def Switch(Text, X1, Y1, X2, Y2, Layer, SwitchWidth, SwitchHeight, TextPadding, State, FontSize, FontType, TextColor, SwitchColor, SwitchKnobColor, SwitchHoverColor, SwitchEnabledColor, SwitchEnabledHoverColor):
    try:
        CurrentTime = time.time()

        if Text in variables.Switches:
            State = variables.Switches[Text][0]
        else:
            variables.Switches[Text] = State, 0

        x = CurrentTime - variables.Switches[Text][1]
        if x < 0.3333:
            x *= 3
            animationState = 1 - math.pow(2, -10 * x)
            variables.ForceSingleRender = True
            if State == False:
                SwitchColor = SwitchColor[0] * animationState + SwitchEnabledColor[0] * (1 - animationState), SwitchColor[1] * animationState + SwitchEnabledColor[1] * (1 - animationState), SwitchColor[2] * animationState + SwitchEnabledColor[2] * (1 - animationState)
                SwitchHoverColor = SwitchHoverColor[0] * animationState + SwitchEnabledHoverColor[0] * (1 - animationState), SwitchHoverColor[1] * animationState + SwitchEnabledHoverColor[1] * (1 - animationState), SwitchHoverColor[2] * animationState + SwitchEnabledHoverColor[2] * (1 - animationState)
            else:
                SwitchEnabledColor = SwitchColor[0] * (1 - animationState) + SwitchEnabledColor[0] * animationState, SwitchColor[1] * (1 - animationState) + SwitchEnabledColor[1] * animationState, SwitchColor[2] * (1 - animationState) + SwitchEnabledColor[2] * animationState
                SwitchEnabledHoverColor = SwitchHoverColor[0] * (1 - animationState) + SwitchEnabledHoverColor[0] * animationState, SwitchHoverColor[1] * (1 - animationState) + SwitchEnabledHoverColor[1] * animationState, SwitchHoverColor[2] * (1 - animationState) + SwitchEnabledHoverColor[2] * animationState
        else:
            animationState = 1

        if X1 <= states.MouseX * states.FrameWidth <= X2 and Y1 <= states.MouseY * states.FrameHeight <= Y2 and states.ForegroundWindow and states.TopMostLayer == Layer:
            SwitchHovered = True
        else:
            SwitchHovered = False
        if SwitchHovered == True:
            if State == True:
                cv2.circle(variables.Frame, (round(X1+SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2), SwitchEnabledHoverColor, -1, cv2.LINE_AA)
                cv2.circle(variables.Frame, (round(X1+SwitchWidth-SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2), SwitchEnabledHoverColor, -1, cv2.LINE_AA)
                cv2.rectangle(variables.Frame, (round(X1+SwitchHeight/2+1), round((Y1+Y2)/2-SwitchHeight/2)), (round(X1+SwitchWidth-SwitchHeight/2-1), round((Y1+Y2)/2+SwitchHeight/2)), SwitchEnabledHoverColor, -1, cv2.LINE_AA)
                if animationState < 1:
                    cv2.circle(variables.Frame, (round(X1+SwitchHeight/2+(SwitchWidth-SwitchHeight)*animationState), round((Y1+Y2)/2)), round(SwitchHeight/2.5), SwitchKnobColor, -1, cv2.LINE_AA)
                else:
                    cv2.circle(variables.Frame, (round(X1+SwitchWidth-SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2.5), SwitchKnobColor, -1, cv2.LINE_AA)
            else:
                cv2.circle(variables.Frame, (round(X1+SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2), SwitchHoverColor, -1, cv2.LINE_AA)
                cv2.circle(variables.Frame, (round(X1+SwitchWidth-SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2), SwitchHoverColor, -1, cv2.LINE_AA)
                cv2.rectangle(variables.Frame, (round(X1+SwitchHeight/2+1), round((Y1+Y2)/2-SwitchHeight/2)), (round(X1+SwitchWidth-SwitchHeight/2-1), round((Y1+Y2)/2+SwitchHeight/2)), SwitchHoverColor, -1, cv2.LINE_AA)
                if animationState < 1:
                    cv2.circle(variables.Frame, (round(X1+SwitchHeight/2+(SwitchWidth-SwitchHeight)*(1-animationState)), round((Y1+Y2)/2)), round(SwitchHeight/2.5), SwitchKnobColor, -1, cv2.LINE_AA)
                else:
                    cv2.circle(variables.Frame, (round(X1+SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2.5), SwitchKnobColor, -1, cv2.LINE_AA)
        else:
            if State == True:
                cv2.circle(variables.Frame, (round(X1+SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2), SwitchEnabledColor, -1, cv2.LINE_AA)
                cv2.circle(variables.Frame, (round(X1+SwitchWidth-SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2), SwitchEnabledColor, -1, cv2.LINE_AA)
                cv2.rectangle(variables.Frame, (round(X1+SwitchHeight/2+1), round((Y1+Y2)/2-SwitchHeight/2)), (round(X1+SwitchWidth-SwitchHeight/2-1), round((Y1+Y2)/2+SwitchHeight/2)), SwitchEnabledColor, -1, cv2.LINE_AA)
                if animationState < 1:
                    cv2.circle(variables.Frame, (round(X1+SwitchHeight/2+(SwitchWidth-SwitchHeight)*animationState), round((Y1+Y2)/2)), round(SwitchHeight/2.5), SwitchKnobColor, -1, cv2.LINE_AA)
                else:
                    cv2.circle(variables.Frame, (round(X1+SwitchWidth-SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2.5), SwitchKnobColor, -1, cv2.LINE_AA)
            else:
                cv2.circle(variables.Frame, (round(X1+SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2), SwitchColor, -1, cv2.LINE_AA)
                cv2.circle(variables.Frame, (round(X1+SwitchWidth-SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2), SwitchColor, -1, cv2.LINE_AA)
                cv2.rectangle(variables.Frame, (round(X1+SwitchHeight/2+1), round((Y1+Y2)/2-SwitchHeight/2)), (round(X1+SwitchWidth-SwitchHeight/2-1), round((Y1+Y2)/2+SwitchHeight/2)), SwitchColor, -1, cv2.LINE_AA)
                if animationState < 1:
                    cv2.circle(variables.Frame, (round(X1+SwitchHeight/2+(SwitchWidth-SwitchHeight)*(1-animationState)), round((Y1+Y2)/2)), round(SwitchHeight/2.5), SwitchKnobColor, -1, cv2.LINE_AA)
                else:
                    cv2.circle(variables.Frame, (round(X1+SwitchHeight/2), round((Y1+Y2)/2)), round(SwitchHeight/2.5), SwitchKnobColor, -1, cv2.LINE_AA)
        Label(Text, X1, Y1, X2, Y2, "Left", SwitchWidth + TextPadding, Layer, FontSize, FontType, TextColor)
        if X1 <= states.MouseX * states.FrameWidth <= X2 and Y1 <= states.MouseY * states.FrameHeight <= Y2 and states.LeftClicked == False and states.LastLeftClicked == True:
            variables.Switches[Text] = not State, CurrentTime
            return not State, states.ForegroundWindow and states.TopMostLayer == Layer, states.LeftClicked and SwitchHovered, SwitchHovered
        else:
            return State, False, states.LeftClicked and SwitchHovered, SwitchHovered
    except:
        errors.ShowError("Elements - Error in function Switch.", str(traceback.format_exc()))
        return False, False, False, False


# MARK: Dropdown
def Dropdown(Title, Items, DefaultItem, X1, Y1, X2, Y2, DropdownHeight, DropdownPadding, Layer, FontSize, FontType, RoundCorners, TextColor, SecondaryTextColor, Color, HoverColor):
    try:
        if Title + str(Items) not in variables.Dropdowns:
            DefaultItem = int(max(min(DefaultItem, len(Items) - 1), 0))
            variables.Dropdowns[Title + str(Items)] = False, DefaultItem

        DropdownSelected, SelectedItem = variables.Dropdowns[Title + str(Items)]

        if X1 <= states.MouseX * states.FrameWidth <= X2 and Y1 <= states.MouseY * states.FrameHeight <= Y2 + ((DropdownHeight + DropdownPadding) if DropdownSelected else 0) and states.ForegroundWindow and states.TopMostLayer == Layer:
            DropdownHovered = True
            DropdownPressed = states.LeftClicked
            DropdownChanged = True if states.LastLeftClicked == True and states.LeftClicked == False and DropdownSelected == True else False
            DropdownSelected = not DropdownSelected if states.LastLeftClicked == True and states.LeftClicked == False else DropdownSelected
        else:
            DropdownHovered = False
            DropdownPressed = False
            DropdownChanged =  DropdownSelected
            DropdownSelected = False

        if DropdownHovered == True:
            cv2.rectangle(variables.Frame, (round(X1+RoundCorners/2), round(Y1+RoundCorners/2)), (round(X2-RoundCorners/2), round(Y2-RoundCorners/2)), HoverColor, RoundCorners, cv2.LINE_AA)
            cv2.rectangle(variables.Frame, (round(X1+RoundCorners/2), round(Y1+RoundCorners/2)), (round(X2-RoundCorners/2), round(Y2-RoundCorners/2)), HoverColor, -1, cv2.LINE_AA)
        else:
            cv2.rectangle(variables.Frame, (round(X1+RoundCorners/2), round(Y1+RoundCorners/2)), (round(X2-RoundCorners/2), round(Y2-RoundCorners/2)), Color, RoundCorners, cv2.LINE_AA)
            cv2.rectangle(variables.Frame, (round(X1+RoundCorners/2), round(Y1+RoundCorners/2)), (round(X2-RoundCorners/2), round(Y2-RoundCorners/2)), Color, -1, cv2.LINE_AA)
        if DropdownSelected == True:
            cv2.rectangle(variables.Frame, (round(X1+RoundCorners/2), round(Y2+DropdownPadding+RoundCorners/2)), (round(X2-RoundCorners/2), round(Y2+DropdownHeight+DropdownPadding-RoundCorners/2)), HoverColor, RoundCorners, cv2.LINE_AA)
            cv2.rectangle(variables.Frame, (round(X1+RoundCorners/2), round(Y2+DropdownPadding+RoundCorners/2)), (round(X2-RoundCorners/2), round(Y2+DropdownHeight+DropdownPadding-RoundCorners/2)), HoverColor, -1, cv2.LINE_AA)

            Padding = (Y2 + Y1) / 2 - FontSize / 4 - Y1
            Height = round(Y2 - Padding) - round(Y1 + Padding)
            cv2.line(variables.Frame, (round(X2 - Padding - Height), round(Y1 + Padding)), (round(X2 - Padding), round(Y2 - Padding)), TextColor, max(round(FontSize / 15), 1), cv2.LINE_AA)
            cv2.line(variables.Frame, (round(X2 - Padding - Height), round(Y1 + Padding)), (round(X2 - Padding  - Height * 2), round(Y2 - Padding)), TextColor, max(round(FontSize / 15), 1), cv2.LINE_AA)

            for Event in states.ScrollEventQueue:
                if Event.dy > 0:
                    SelectedItem = (SelectedItem - 1) if SelectedItem > 0 else 0
                elif Event.dy < 0:
                    SelectedItem = (SelectedItem + 1) if SelectedItem < len(Items) - 1 else len(Items) - 1
            states.ScrollEventQueue = []

            for i in range(3):
                Index = SelectedItem - 1 + i
                if Index >= len(Items):
                    Index = -1
                if Index < 0:
                    Index = -1
                if Index == -1:
                    Item = ""
                else:
                    Item = Items[Index]
                if i == 1:
                    ItemText = "> " + Item + " <"
                else:
                    ItemText = Item
                Label(ItemText, X1, Y2 + DropdownPadding + DropdownHeight / 3 * i, X2, Y2 + DropdownPadding + DropdownHeight / 3 * (i + 1), "Center", 0, Layer, FontSize, FontType, TextColor if i == 1 else SecondaryTextColor)

        else:

            Padding = (Y2 + Y1) / 2 - FontSize / 4 - Y1
            Height = round(Y2 - Padding) - round(Y1 + Padding)
            cv2.line(variables.Frame, (round(X2 - Padding - Height), round(Y2 - Padding)), (round(X2 - Padding), round(Y1 + Padding)), TextColor, max(round(FontSize / 15), 1), cv2.LINE_AA)
            cv2.line(variables.Frame, (round(X2 - Padding - Height), round(Y2 - Padding)), (round(X2 - Padding  - Height * 2), round(Y1 + Padding)), TextColor, max(round(FontSize / 15), 1), cv2.LINE_AA)

        Label(Title, X1, Y1, X2, Y2, "Center", 0, Layer, FontSize, FontType, TextColor)

        variables.Dropdowns[Title + str(Items)] = DropdownSelected, SelectedItem

        return Items[SelectedItem], DropdownChanged, DropdownSelected, DropdownPressed, DropdownHovered
    except:
        errors.ShowError("Elements - Error in function Dropdown.", str(traceback.format_exc()))
        return "", False, False, False, False