from PIL import Image, ImageDraw, ImageFont
from ImageUI import Translations
from ImageUI import Variables
from ImageUI import Settings
from ImageUI import Errors
from ImageUI import States
import traceback
import numpy
import math
import time
import cv2


# MARK: Label
def Label(Text, X1, Y1, X2, Y2, Align, AlignPadding, Layer, FontSize, FontType, TextColor):
    try:
        if Text == "": return
        Text = Translations.Translate(Text)
        if f"{FontSize}-{FontType}" in Variables.Fonts:
            Font = Variables.Fonts[f"{FontSize}-{FontType}"]
        else:
            Font = ImageFont.truetype(FontType, FontSize)
            Variables.Fonts[f"{FontSize}-{FontType}"] = Font
        Frame = Image.fromarray(Variables.Frame)
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
        Variables.Frame = numpy.array(Frame)
    except:
        Errors.ShowError("Elements - Error in function Label.", str(traceback.format_exc()))


# MARK: Button
def Button(Text, X1, Y1, X2, Y2, Layer, FontSize, FontType, RoundCorners, TextColor, Color, HoverColor):
    try:
        if X1 <= States.MouseX * Variables.Frame.shape[1] <= X2 and Y1 <= States.MouseY * Variables.Frame.shape[0] <= Y2 and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False:
            Hovered = True
        else:
            Hovered = False
        if Hovered == True:
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, RoundCorners, Settings.RectangleLineType)
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, - 1, Settings.RectangleLineType)
        else:
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, RoundCorners, Settings.RectangleLineType)
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, - 1, Settings.RectangleLineType)
        Label(Text, X1, Y1, X2, Y2, "Center", 0, Layer, FontSize, FontType, TextColor)
        if X1 <= States.MouseX * Variables.Frame.shape[1] <= X2 and Y1 <= States.MouseY * Variables.Frame.shape[0] <= Y2 and States.LeftPressed == False and States.LastLeftPressed == True and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False:
            return True, States.LeftPressed and Hovered, Hovered
        else:
            return False, States.LeftPressed and Hovered, Hovered
    except:
        Errors.ShowError("Elements - Error in function Button.", str(traceback.format_exc()))
        return False, False, False


# MARK: Switch
def Switch(Text, X1, Y1, X2, Y2, Layer, SwitchWidth, SwitchHeight, TextPadding, State, FontSize, FontType, TextColor, SwitchColor, SwitchKnobColor, SwitchHoverColor, SwitchEnabledColor, SwitchEnabledHoverColor):
    try:
        CurrentTime = time.time()

        if Text in Variables.Switches:
            State = Variables.Switches[Text][0]
        else:
            Variables.Switches[Text] = State, 0

        x = CurrentTime - Variables.Switches[Text][1]
        if x < Settings.SwitchAnimationDuration:
            x *= 1/Settings.SwitchAnimationDuration
            AnimationState = 1 - math.pow(2, -10 * x)
            Variables.ForceSingleRender = True
            if State == False:
                SwitchColor = SwitchColor[0] * AnimationState + SwitchEnabledColor[0] * (1 - AnimationState), SwitchColor[1] * AnimationState + SwitchEnabledColor[1] * (1 - AnimationState), SwitchColor[2] * AnimationState + SwitchEnabledColor[2] * (1 - AnimationState)
                SwitchHoverColor = SwitchHoverColor[0] * AnimationState + SwitchEnabledHoverColor[0] * (1 - AnimationState), SwitchHoverColor[1] * AnimationState + SwitchEnabledHoverColor[1] * (1 - AnimationState), SwitchHoverColor[2] * AnimationState + SwitchEnabledHoverColor[2] * (1 - AnimationState)
            else:
                SwitchEnabledColor = SwitchColor[0] * (1 - AnimationState) + SwitchEnabledColor[0] * AnimationState, SwitchColor[1] * (1 - AnimationState) + SwitchEnabledColor[1] * AnimationState, SwitchColor[2] * (1 - AnimationState) + SwitchEnabledColor[2] * AnimationState
                SwitchEnabledHoverColor = SwitchHoverColor[0] * (1 - AnimationState) + SwitchEnabledHoverColor[0] * AnimationState, SwitchHoverColor[1] * (1 - AnimationState) + SwitchEnabledHoverColor[1] * AnimationState, SwitchHoverColor[2] * (1 - AnimationState) + SwitchEnabledHoverColor[2] * AnimationState
        else:
            AnimationState = 1

        if X1 <= States.MouseX * States.FrameWidth <= X2 and Y1 <= States.MouseY * States.FrameHeight <= Y2 and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False:
            SwitchHovered = True
        else:
            SwitchHovered = False
        if SwitchHovered == True:
            if State == True:
                cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchEnabledHoverColor, -1, cv2.LINE_AA)
                cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchEnabledHoverColor, -1, cv2.LINE_AA)
                cv2.rectangle(Variables.Frame, (round(X1 + SwitchHeight / 2 + 1), round((Y1 + Y2) / 2 - SwitchHeight / 2)), (round(X1 + SwitchWidth - SwitchHeight / 2 - 1), round((Y1 + Y2) / 2 + SwitchHeight / 2)), SwitchEnabledHoverColor, -1, cv2.LINE_AA)
                if AnimationState < 1:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2 + (SwitchWidth - SwitchHeight) * AnimationState), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, cv2.LINE_AA)
                else:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, cv2.LINE_AA)
            else:
                cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchHoverColor, -1, cv2.LINE_AA)
                cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchHoverColor, -1, cv2.LINE_AA)
                cv2.rectangle(Variables.Frame, (round(X1 + SwitchHeight / 2 + 1), round((Y1 + Y2) / 2 - SwitchHeight / 2)), (round(X1 + SwitchWidth - SwitchHeight / 2 - 1), round((Y1 + Y2) / 2 + SwitchHeight / 2)), SwitchHoverColor, -1, cv2.LINE_AA)
                if AnimationState < 1:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2 + (SwitchWidth - SwitchHeight) * (1 - AnimationState)), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, cv2.LINE_AA)
                else:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, cv2.LINE_AA)
        else:
            if State == True:
                cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchEnabledColor, -1, cv2.LINE_AA)
                cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchEnabledColor, -1, cv2.LINE_AA)
                cv2.rectangle(Variables.Frame, (round(X1 + SwitchHeight / 2 + 1), round((Y1 + Y2) / 2 - SwitchHeight / 2)), (round(X1 + SwitchWidth - SwitchHeight / 2 - 1), round((Y1 + Y2) / 2 + SwitchHeight / 2)), SwitchEnabledColor, -1, cv2.LINE_AA)
                if AnimationState < 1:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2 + (SwitchWidth - SwitchHeight) * AnimationState), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, cv2.LINE_AA)
                else:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, cv2.LINE_AA)
            else:
                cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchColor, -1, cv2.LINE_AA)
                cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchColor, -1, cv2.LINE_AA)
                cv2.rectangle(Variables.Frame, (round(X1 + SwitchHeight / 2 + 1), round((Y1 + Y2) / 2 - SwitchHeight / 2)), (round(X1 + SwitchWidth - SwitchHeight / 2 - 1), round((Y1 + Y2) / 2 + SwitchHeight / 2)), SwitchColor, -1, cv2.LINE_AA)
                if AnimationState < 1:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2 + (SwitchWidth - SwitchHeight) * (1 - AnimationState)), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, cv2.LINE_AA)
                else:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, cv2.LINE_AA)
        Label(Text, X1, Y1, X2, Y2, "Left", SwitchWidth + TextPadding, Layer, FontSize, FontType, TextColor)
        if X1 <= States.MouseX * States.FrameWidth <= X2 and Y1 <= States.MouseY * States.FrameHeight <= Y2 and States.LeftPressed == False and States.LastLeftPressed == True and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False:
            Variables.Switches[Text] = not State, CurrentTime
            return not State, True, States.LeftPressed and SwitchHovered, SwitchHovered
        else:
            return State, False, States.LeftPressed and SwitchHovered, SwitchHovered
    except:
        Errors.ShowError("Elements - Error in function Switch.", str(traceback.format_exc()))
        return False, False, False, False


# MARK: Dropdown
def Dropdown(Title, Items, DefaultItem, X1, Y1, X2, Y2, DropdownHeight, DropdownPadding, Layer, FontSize, FontType, RoundCorners, TextColor, SecondaryTextColor, Color, HoverColor):
    try:
        if Title + str(Items) not in Variables.Dropdowns:
            DefaultItem = int(max(min(DefaultItem, len(Items) - 1), 0))
            Variables.Dropdowns[Title + str(Items)] = False, DefaultItem

        DropdownSelected, SelectedItem = Variables.Dropdowns[Title + str(Items)]

        if X1 <= States.MouseX * States.FrameWidth <= X2 and Y1 <= States.MouseY * States.FrameHeight <= Y2 + ((DropdownHeight + DropdownPadding) if DropdownSelected else 0) and States.ForegroundWindow and States.TopMostLayer == Layer:
            DropdownHovered = True
            DropdownPressed = States.LeftPressed
            DropdownChanged = True if States.LastLeftPressed == True and States.LeftPressed == False and DropdownSelected == True else False
            DropdownSelected = not DropdownSelected if States.LastLeftPressed == True and States.LeftPressed == False else DropdownSelected
        else:
            DropdownHovered = False
            DropdownPressed = False
            DropdownChanged = DropdownSelected
            DropdownSelected = False

        if DropdownHovered == True:
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, RoundCorners, cv2.LINE_AA)
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, -1, cv2.LINE_AA)
        else:
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, RoundCorners, cv2.LINE_AA)
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, -1, cv2.LINE_AA)
        if DropdownSelected == True:
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y2 + DropdownPadding + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 + DropdownHeight + DropdownPadding - RoundCorners / 2)), HoverColor, RoundCorners, cv2.LINE_AA)
            cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y2 + DropdownPadding + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 + DropdownHeight + DropdownPadding - RoundCorners / 2)), HoverColor, -1, cv2.LINE_AA)

            Padding = (Y2 + Y1) / 2 - FontSize / 4 - Y1
            Height = round(Y2 - Padding) - round(Y1 + Padding)
            cv2.line(Variables.Frame, (round(X2 - Padding - Height), round(Y1 + Padding)), (round(X2 - Padding), round(Y2 - Padding)), TextColor, max(round(FontSize / 15), 1), cv2.LINE_AA)
            cv2.line(Variables.Frame, (round(X2 - Padding - Height), round(Y1 + Padding)), (round(X2 - Padding - Height * 2), round(Y2 - Padding)), TextColor, max(round(FontSize / 15), 1), cv2.LINE_AA)

            for Event in States.ScrollEventQueue:
                if Event.dy > 0:
                    SelectedItem = (SelectedItem - 1) if SelectedItem > 0 else 0
                elif Event.dy < 0:
                    SelectedItem = (SelectedItem + 1) if SelectedItem < len(Items) - 1 else len(Items) - 1
            States.ScrollEventQueue = []

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
            cv2.line(Variables.Frame, (round(X2 - Padding - Height), round(Y2 - Padding)), (round(X2 - Padding), round(Y1 + Padding)), TextColor, max(round(FontSize / 15), 1), cv2.LINE_AA)
            cv2.line(Variables.Frame, (round(X2 - Padding - Height), round(Y2 - Padding)), (round(X2 - Padding - Height * 2), round(Y1 + Padding)), TextColor, max(round(FontSize / 15), 1), cv2.LINE_AA)

        Label(Title, X1, Y1, X2, Y2, "Center", 0, Layer, FontSize, FontType, TextColor)

        Variables.Dropdowns[Title + str(Items)] = DropdownSelected, SelectedItem

        return Items[SelectedItem], DropdownChanged, DropdownSelected, DropdownPressed, DropdownHovered
    except:
        Errors.ShowError("Elements - Error in function Dropdown.", str(traceback.format_exc()))
        return "", False, False, False, False