from PIL import Image as PILImage, ImageDraw as PILDraw, ImageFont as PILFont
from ImageUI import Translations
from ImageUI import Variables
from ImageUI import Settings
from ImageUI import Errors
from ImageUI import States
import win32clipboard
import traceback
import numpy
import math
import time
import cv2


# MARK: Label
def Label(Text, X1, Y1, X2, Y2, ID, Align, AlignPadding, Layer, FontSize, FontType, Translate, TextColor):
    try:
        if Text == "": return X1, Y1, X2, Y2
        if Translate:
            Text = Translations.Translate(Text)
        Frame = Variables.Frame.copy()
        for CachedText in Variables.TextCache:
            if CachedText[0] != f"{Text}-{X1}-{Y1}-{X2}-{Y2}-{ID}-{Align}-{AlignPadding}-{FontSize}-{FontType}-{Translate}-{TextColor}":
                continue
            EmptyFrame, TextFrame, BBoxX1, BBoxY1, BBoxX2, BBoxY2 = CachedText[1]
            CurrentFrame = Frame[BBoxY1:BBoxY2, BBoxX1:BBoxX2].copy()
            if (CurrentFrame == EmptyFrame).all():
                Frame[BBoxY1:BBoxY2, BBoxX1:BBoxX2] = TextFrame
                Variables.Frame = Frame.copy()
                return BBoxX1 + 2, BBoxX1 + 2, BBoxX2 - 2, BBoxY2 - 2

        if f"{FontSize}-{FontType}" in Variables.Fonts:
            Font = Variables.Fonts[f"{FontSize}-{FontType}"]
        else:
            Font = PILFont.truetype(FontType, FontSize)
            Variables.Fonts[f"{FontSize}-{FontType}"] = Font
        Frame = PILImage.fromarray(Frame)
        Draw = PILDraw.Draw(Frame)
        BBoxX1, BBoxY1, BBoxX2, BBoxY2 = Draw.textbbox((0, 0), Text, Font)
        if Align.lower() == "left":
            X = round(X1 + BBoxX1 + AlignPadding)
        elif Align.lower() == "right":
            X = round(X2 - BBoxX2 - AlignPadding)
        else:
            X = round(X1 + (X2 - X1) / 2 - (BBoxX2 - BBoxX1) / 2)
        Y = round(Y1 + (Y2 - Y1) / 2 - (BBoxY2 - BBoxY1) / 2)
        BBoxX1 += X - 2
        BBoxY1 += Y - 2
        BBoxX2 += X + 2
        BBoxY2 += Y + 2
        EmptyFrame = Variables.Frame[BBoxY1:BBoxY2, BBoxX1:BBoxX2].copy()
        Draw.text((X, Y), Text, font=Font, fill=(TextColor[0], TextColor[1], TextColor[2], 255))
        Frame = numpy.array(Frame)
        Variables.Frame = Frame.copy()
        TextFrame = Frame[BBoxY1:BBoxY2, BBoxX1:BBoxX2]
        Variables.TextCache.append([f"{Text}-{X1}-{Y1}-{X2}-{Y2}-{ID}-{Align}-{AlignPadding}-{FontSize}-{FontType}-{Translate}-{TextColor}", [EmptyFrame, TextFrame, BBoxX1, BBoxY1, BBoxX2, BBoxY2]])
        return BBoxX1 + 2, BBoxX1 + 2, BBoxX2 - 2, BBoxY2 - 2
    except:
        Errors.ShowError("Elements - Error in function Label.", str(traceback.format_exc()))
        return X1, Y1, X2, Y2


# MARK: Button
def Button(Text, X1, Y1, X2, Y2, ID, Layer, FontSize, FontType, RoundCorners, Translate, TextColor, Color, HoverColor):
    try:
        if X1 <= States.MouseX * Variables.Frame.shape[1] <= X2 and Y1 <= States.MouseY * Variables.Frame.shape[0] <= Y2 and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False and States.AnyInputsOpen == False:
            Hovered = True
        else:
            Hovered = False
        if Hovered == True:
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, RoundCorners, Settings.RectangleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, - 1, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1), round(Y1)), (round(X2), round(Y2)), HoverColor, - 1, Settings.RectangleLineType)
        else:
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, RoundCorners, Settings.RectangleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, - 1, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1), round(Y1)), (round(X2), round(Y2)), Color, - 1, Settings.RectangleLineType)
        Label(Text, X1, Y1, X2, Y2, ID + "#LABEL", "Center", 0, Layer, FontSize, FontType, Translate, TextColor)
        if X1 <= States.MouseX * Variables.Frame.shape[1] <= X2 and Y1 <= States.MouseY * Variables.Frame.shape[0] <= Y2 and States.LeftPressed == False and States.LastLeftPressed == True and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False and States.AnyInputsOpen == False:
            return True, States.LeftPressed and Hovered, Hovered
        else:
            return False, States.LeftPressed and Hovered, Hovered
    except:
        Errors.ShowError("Elements - Error in function Button.", str(traceback.format_exc()))
        return False, False, False


# MARK: Switch
def Switch(Text, X1, Y1, X2, Y2, ID, Layer, SwitchWidth, SwitchHeight, TextPadding, State, FontSize, FontType, Translate, TextColor, SwitchColor, SwitchKnobColor, SwitchHoverColor, SwitchEnabledColor, SwitchEnabledHoverColor):
    try:
        CurrentTime = time.time()

        if ID in Variables.Switches:
            State = Variables.Switches[ID][0]
        else:
            Variables.Switches[ID] = State, 0

        x = CurrentTime - Variables.Switches[ID][1]
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

        if X1 <= States.MouseX * States.FrameWidth <= X2 and Y1 <= States.MouseY * States.FrameHeight <= Y2 and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False and States.AnyInputsOpen == False:
            SwitchHovered = True
        else:
            SwitchHovered = False
        if SwitchHovered == True:
            if State == True:
                cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchEnabledHoverColor, -1, Settings.CircleLineType)
                cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchEnabledHoverColor, -1, Settings.CircleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + SwitchHeight / 2 + 1), round((Y1 + Y2) / 2 - SwitchHeight / 2)), (round(X1 + SwitchWidth - SwitchHeight / 2 - 1), round((Y1 + Y2) / 2 + SwitchHeight / 2)), SwitchEnabledHoverColor, -1, Settings.RectangleLineType)
                if AnimationState < 1:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2 + (SwitchWidth - SwitchHeight) * AnimationState), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, Settings.CircleLineType)
                else:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, Settings.CircleLineType)
            else:
                cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchHoverColor, -1, Settings.CircleLineType)
                cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchHoverColor, -1, Settings.CircleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + SwitchHeight / 2 + 1), round((Y1 + Y2) / 2 - SwitchHeight / 2)), (round(X1 + SwitchWidth - SwitchHeight / 2 - 1), round((Y1 + Y2) / 2 + SwitchHeight / 2)), SwitchHoverColor, -1, Settings.RectangleLineType)
                if AnimationState < 1:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2 + (SwitchWidth - SwitchHeight) * (1 - AnimationState)), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, Settings.CircleLineType)
                else:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, Settings.CircleLineType)
        else:
            if State == True:
                cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchEnabledColor, -1, Settings.CircleLineType)
                cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchEnabledColor, -1, Settings.CircleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + SwitchHeight / 2 + 1), round((Y1 + Y2) / 2 - SwitchHeight / 2)), (round(X1 + SwitchWidth - SwitchHeight / 2 - 1), round((Y1 + Y2) / 2 + SwitchHeight / 2)), SwitchEnabledColor, -1, Settings.RectangleLineType)
                if AnimationState < 1:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2 + (SwitchWidth - SwitchHeight) * AnimationState), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, Settings.CircleLineType)
                else:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, Settings.CircleLineType)
            else:
                cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchColor, -1, Settings.CircleLineType)
                cv2.circle(Variables.Frame, (round(X1 + SwitchWidth - SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2), SwitchColor, -1, Settings.CircleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + SwitchHeight / 2 + 1), round((Y1 + Y2) / 2 - SwitchHeight / 2)), (round(X1 + SwitchWidth - SwitchHeight / 2 - 1), round((Y1 + Y2) / 2 + SwitchHeight / 2)), SwitchColor, -1, Settings.RectangleLineType)
                if AnimationState < 1:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2 + (SwitchWidth - SwitchHeight) * (1 - AnimationState)), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, Settings.CircleLineType)
                else:
                    cv2.circle(Variables.Frame, (round(X1 + SwitchHeight / 2), round((Y1 + Y2) / 2)), round(SwitchHeight / 2.5), SwitchKnobColor, -1, Settings.CircleLineType)
        Label(Text, X1, Y1, X2, Y2, ID + "#LABEL", "Left", SwitchWidth + TextPadding, Layer, FontSize, FontType, Translate, TextColor)
        if X1 <= States.MouseX * States.FrameWidth <= X2 and Y1 <= States.MouseY * States.FrameHeight <= Y2 and States.LeftPressed == False and States.LastLeftPressed == True and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False and States.AnyInputsOpen == False:
            Variables.Switches[ID] = not State, CurrentTime
            return not State, True, States.LeftPressed and SwitchHovered, SwitchHovered
        else:
            return State, False, States.LeftPressed and SwitchHovered, SwitchHovered
    except:
        Errors.ShowError("Elements - Error in function Switch.", str(traceback.format_exc()))
        return False, False, False, False


# MARK: Input
def Input(X1, Y1, X2, Y2, ID, DefaultInput, Placeholder, TextAlign, TextAlignPadding, Layer, FontSize, FontType, RoundCorners, Translate, TextColor, SecondaryTextColor, Color, HoverColor, ThemeColor):
    try:
        if ID not in Variables.Inputs:
            Variables.Inputs[ID] = False, DefaultInput

        Selected, Input = Variables.Inputs[ID]

        Changed = False

        if X1 <= States.MouseX * Variables.Frame.shape[1] <= X2 and Y1 <= States.MouseY * Variables.Frame.shape[0] <= Y2 and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False:
            Hovered = True
            Pressed = States.LeftPressed
        else:
            Hovered = False
            Pressed = False

            if Selected and States.LastLeftPressed == True and States.LeftPressed == False and States.AnyDropdownOpen == False:
                Selected = False
                Changed = True

        if Selected and (States.ForegroundWindow == False or States.TopMostLayer != Layer or States.AnyDropdownOpen == True):
            Selected = False
            Changed = True

        if Hovered and States.LastLeftPressed == True and States.LeftPressed == False:
            Selected = True
            States.KeyboardEventQueue = []
            Variables.ForceSingleRender = True

        if Hovered == True or Selected == True:
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, RoundCorners, Settings.RectangleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, - 1, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1), round(Y1)), (round(X2), round(Y2)), HoverColor, - 1, Settings.RectangleLineType)
            cv2.line(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y2)), (round(X2 - RoundCorners / 2), round(Y2)), ThemeColor, 1, Settings.LineType)
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2) + 2, round(Y1 + RoundCorners / 2) + 2), (round(X2 - RoundCorners / 2) - 2, round(Y2 - RoundCorners / 2) - 2), HoverColor, RoundCorners, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1) + 2, round(Y1) + 2), (round(X2) - 2, round(Y2) - 2), HoverColor, - 1, Settings.RectangleLineType)
        else:
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, RoundCorners, Settings.RectangleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, - 1, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1), round(Y1)), (round(X2), round(Y2)), Color, - 1, Settings.RectangleLineType)
            cv2.line(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y2)), (round(X2 - RoundCorners / 2), round(Y2)), ThemeColor, 1, Settings.LineType)
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2) + 2, round(Y1 + RoundCorners / 2) + 2), (round(X2 - RoundCorners / 2) - 2, round(Y2 - RoundCorners / 2) - 2), Color, RoundCorners, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1) + 2, round(Y1) + 2), (round(X2) - 2, round(Y2) - 2), Color, - 1, Settings.RectangleLineType)

        if TextAlign.lower() == "left":
            CursorX = X1 + TextAlignPadding
        elif TextAlign.lower() == "right":
            CursorX = X2 - TextAlignPadding
        else:
            CursorX = (X1 + X2) / 2
        if Input != "":
            _, _, CursorX, _ = Label(Input, X1, Y1, X2, Y2, ID + "#LABEL", TextAlign, TextAlignPadding, Layer, FontSize, FontType, False, TextColor)
        elif Placeholder != "":
            if TextAlign.lower() == "left":
                Offset = 3
            elif TextAlign.lower() == "right":
                Offset = -3
            else:
                Offset = 0
            Label(Placeholder, X1 + Offset, Y1, X2 + Offset, Y2, ID + "#LABEL", TextAlign, TextAlignPadding, Layer, FontSize, FontType, Translate, SecondaryTextColor)

        if Selected:
            for Key in States.KeyboardEventQueue:
                if Key == "Paste":
                    try:
                        win32clipboard.OpenClipboard()
                        Input += win32clipboard.GetClipboardData()
                        win32clipboard.CloseClipboard()
                    except:
                        pass
                elif Key == "Backspace":
                    Input = Input[:-1] if len(Input) > 0 else ""
                elif Key == "Enter":
                    Selected = False
                    Changed = True
                else:
                    try:
                        Input += str(Key)
                    except:
                        pass

                Variables.ForceSingleRender = True
                States.KeyboardEventQueue.pop(0)

            cv2.line(Variables.Frame, (round(CursorX), round(Y1 + (Y2 - Y1) * 0.3)), (round(CursorX), round(Y2 - (Y2 - Y1) * 0.3)), TextColor, 1, Settings.LineType)

        Variables.Inputs[ID] = Selected, Input

        return Input, Changed, Selected, Pressed, Hovered
    except:
        Errors.ShowError("Elements - Error in function Input.", str(traceback.format_exc()))
        return "", False, False, False, False


# MARK: Dropdown
def Dropdown(Title, Items, DefaultItem, X1, Y1, X2, Y2, ID, DropdownHeight, DropdownPadding, Layer, FontSize, FontType, RoundCorners, Translate, TextColor, SecondaryTextColor, Color, HoverColor):
    try:
        if ID not in Variables.Dropdowns:
            try:
                DefaultItem = Items.index(DefaultItem)
            except ValueError:
                DefaultItem = 0
            Variables.Dropdowns[ID] = False, Items, DefaultItem

        DropdownSelected, Items, SelectedItem = Variables.Dropdowns[ID]

        if X1 <= States.MouseX * States.FrameWidth <= X2 and Y1 <= States.MouseY * States.FrameHeight <= Y2 + ((DropdownHeight + DropdownPadding) if DropdownSelected else 0) and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyInputsOpen == False:
            if DropdownSelected == False and States.LastLeftPressed == True and States.LeftPressed == False: Variables.ForceSingleRender = True
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
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, RoundCorners, Settings.RectangleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), HoverColor, -1, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1), round(Y1)), (round(X2), round(Y2)), HoverColor, -1, Settings.RectangleLineType)
        else:
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, RoundCorners, Settings.RectangleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), Color, -1, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1), round(Y1)), (round(X2), round(Y2)), Color, -1, Settings.RectangleLineType)
        if DropdownSelected == True:
            if RoundCorners > 0:
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y2 + DropdownPadding + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 + DropdownHeight + DropdownPadding - RoundCorners / 2)), HoverColor, RoundCorners, Settings.RectangleLineType)
                cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y2 + DropdownPadding + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 + DropdownHeight + DropdownPadding - RoundCorners / 2)), HoverColor, -1, Settings.RectangleLineType)
            else:
                cv2.rectangle(Variables.Frame, (round(X1), round(Y2 + DropdownPadding)), (round(X2), round(Y2 + DropdownHeight + DropdownPadding)), HoverColor, -1, Settings.RectangleLineType)

            Padding = (Y2 + Y1) / 2 - FontSize / 4 - Y1
            Height = round(Y2 - Padding) - round(Y1 + Padding)
            cv2.line(Variables.Frame, (round(X2 - Padding - Height), round(Y1 + Padding)), (round(X2 - Padding), round(Y2 - Padding)), TextColor, max(round(FontSize / 15), 1), Settings.CircleLineType)
            cv2.line(Variables.Frame, (round(X2 - Padding - Height), round(Y1 + Padding)), (round(X2 - Padding - Height * 2), round(Y2 - Padding)), TextColor, max(round(FontSize / 15), 1), Settings.CircleLineType)

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
                Label(ItemText, X1, Y2 + DropdownPadding + DropdownHeight / 3 * i, X2, Y2 + DropdownPadding + DropdownHeight / 3 * (i + 1), ID + "#LABEL", "Center", 0, Layer, FontSize, FontType, Translate, TextColor if i == 1 else SecondaryTextColor)

        else:

            Padding = (Y2 + Y1) / 2 - FontSize / 4 - Y1
            Height = round(Y2 - Padding) - round(Y1 + Padding)
            cv2.line(Variables.Frame, (round(X2 - Padding - Height), round(Y2 - Padding)), (round(X2 - Padding), round(Y1 + Padding)), TextColor, max(round(FontSize / 15), 1), Settings.LineType)
            cv2.line(Variables.Frame, (round(X2 - Padding - Height), round(Y2 - Padding)), (round(X2 - Padding - Height * 2), round(Y1 + Padding)), TextColor, max(round(FontSize / 15), 1), Settings.LineType)

        Label(Title, X1, Y1, X2, Y2, ID + "#LABEL", "Center", 0, Layer, FontSize, FontType, Translate, TextColor)

        Variables.Dropdowns[ID] = DropdownSelected, Items, SelectedItem

        return Items[SelectedItem], DropdownChanged, DropdownSelected, DropdownPressed, DropdownHovered
    except:
        Errors.ShowError("Elements - Error in function Dropdown.", str(traceback.format_exc()))
        return "", False, False, False, False


# MARK: Image
def Image(Image, X1, Y1, X2, Y2, ID, Layer, RoundCorners):
    try:
        if type(Image) == type(None): return
        if Image.shape[1] <= 0 or Image.shape[0] <= 0: return
        Frame = Variables.Frame.copy()
        Image = cv2.resize(Image, (X2 - X1 + 1, Y2 - Y1 + 1))
        if RoundCorners > 0:
            Mask = numpy.zeros(Frame.shape, dtype=numpy.float32)
            ImageFull = numpy.zeros_like(Frame)
            ImageFull[Y1:Y2 + 1, X1:X2 + 1] = Image
            cv2.rectangle(Mask, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), (1, 1, 1), RoundCorners, Settings.RectangleLineType)
            cv2.rectangle(Mask, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), (1, 1, 1), -1, Settings.RectangleLineType)
            Frame = cv2.multiply(Frame, 1.0 - Mask, dtype=cv2.CV_8UC3)
            ImageFull = cv2.multiply(ImageFull, Mask, dtype=cv2.CV_8UC3)
            Frame = cv2.add(Frame, ImageFull)
        else:
            Frame[Y1:Y2 + 1, X1:X2 + 1] = Image
        Variables.Frame = Frame
        if X1 <= States.MouseX * Variables.Frame.shape[1] <= X2 and Y1 <= States.MouseY * Variables.Frame.shape[0] <= Y2 and States.LeftPressed == False and States.LastLeftPressed == True and States.ForegroundWindow and States.TopMostLayer == Layer and States.AnyDropdownOpen == False and States.AnyInputsOpen == False:
            return True
        else:
            return False
    except:
        Errors.ShowError("Elements - Error in function Image.", str(traceback.format_exc()))


# MARK: Popup
def Popup(Text, StartX1, StartY1, StartX2, StartY2, EndX1, EndY1, EndX2, EndY2, ID, Progress, DoAnimation, AnimationDuration, ShowDuration, Layer, FontSize, FontType, RoundCorners, Translate, TextColor, Color, OutlineColor, ProgressBarColor):
    try:
        if ID not in Variables.Popups:
            Variables.Popups[ID] = {"ID": ID,
                                    "Time": time.time(),
                                    "Text": Text,
                                    "StartX1": StartX1,
                                    "StartY1": StartY1,
                                    "StartX2": StartX2,
                                    "StartY2": StartY2,
                                    "EndX1": EndX1,
                                    "EndY1": EndY1,
                                    "EndX2": EndX2,
                                    "EndY2": EndY2,
                                    "Progress": Progress,
                                    "DoAnimation": DoAnimation,
                                    "AnimationDuration": AnimationDuration,
                                    "ShowDuration": ShowDuration,
                                    "Layer": Layer,
                                    "FontSize": FontSize,
                                    "FontType": FontType,
                                    "RoundCorners": RoundCorners,
                                    "Translate": Translate,
                                    "TextColor": TextColor,
                                    "Color": Color,
                                    "OutlineColor": OutlineColor,
                                    "ProgressBarColor": ProgressBarColor}
        else:
            if Variables.Popups[ID]["DoAnimation"] and Variables.Popups[ID]["Time"] + Variables.Popups[ID]["AnimationDuration"] <= time.time():
                Variables.Popups[ID]["Time"] = time.time() - Variables.Popups[ID]["AnimationDuration"]
            Variables.Popups[ID]["Text"] = Text
            Variables.Popups[ID]["StartX1"] = StartX1
            Variables.Popups[ID]["StartY1"] = StartY1
            Variables.Popups[ID]["StartX2"] = StartX2
            Variables.Popups[ID]["StartY2"] = StartY2
            Variables.Popups[ID]["EndX1"] = EndX1
            Variables.Popups[ID]["EndY1"] = EndY1
            Variables.Popups[ID]["EndX2"] = EndX2
            Variables.Popups[ID]["EndY2"] = EndY2
            Variables.Popups[ID]["Progress"] = Progress
            Variables.Popups[ID]["DoAnimation"] = DoAnimation
            Variables.Popups[ID]["AnimationDuration"] = AnimationDuration
            Variables.Popups[ID]["ShowDuration"] = ShowDuration
            Variables.Popups[ID]["Layer"] = Layer
            Variables.Popups[ID]["FontSize"] = FontSize
            Variables.Popups[ID]["FontType"] = FontType
            Variables.Popups[ID]["RoundCorners"] = RoundCorners
            Variables.Popups[ID]["Translate"] = Translate
            Variables.Popups[ID]["TextColor"] = TextColor
            Variables.Popups[ID]["Color"] = Color
            Variables.Popups[ID]["OutlineColor"] = OutlineColor
            Variables.Popups[ID]["ProgressBarColor"] = ProgressBarColor
    except:
        Errors.ShowError("Elements - Error in function Popup.", str(traceback.format_exc()))


def CheckAndRenderPopups():
    try:
        for Popup in list(Variables.Popups.values()):
            Render = False
            CurrentTime = time.time()
            ID = Popup["ID"]
            Time = Popup["Time"]
            Text = Popup["Text"]
            StartX1 = Popup["StartX1"]
            StartY1 = Popup["StartY1"]
            StartX2 = Popup["StartX2"]
            StartY2 = Popup["StartY2"]
            EndX1 = Popup["EndX1"]
            EndY1 = Popup["EndY1"]
            EndX2 = Popup["EndX2"]
            EndY2 = Popup["EndY2"]
            Progress = Popup["Progress"]
            DoAnimation = Popup["DoAnimation"]
            AnimationDuration = Popup["AnimationDuration"]
            ShowDuration = Popup["ShowDuration"]
            Layer = Popup["Layer"]
            FontSize = Popup["FontSize"]
            FontType = Popup["FontType"]
            RoundCorners = Popup["RoundCorners"]
            Translate = Popup["Translate"]
            TextColor = Popup["TextColor"]
            Color = Popup["Color"]
            OutlineColor = Popup["OutlineColor"]
            ProgressBarColor = Popup["ProgressBarColor"]

            if Progress < 0 or (Progress > 0 and Progress < 100) or ShowDuration <= 0:
                if CurrentTime >= Time + (AnimationDuration if DoAnimation else 0):
                    Time = CurrentTime - (AnimationDuration if DoAnimation else 0)
                    Popup["Time"] = Time

            if Popup["DoAnimation"] == True:
                if Time <= CurrentTime <= Time + AnimationDuration:
                    X = (CurrentTime - Time) / AnimationDuration
                    X = -(math.cos(math.pi * X) - 1) / 2
                    X1 = round(StartX1 * (1 - X) + EndX1 * X)
                    Y1 = round(StartY1 * (1 - X) + EndY1 * X)
                    X2 = round(StartX2 * (1 - X) + EndX2 * X)
                    Y2 = round(StartY2 * (1 - X) + EndY2 * X)
                    Render = True
                elif Time + ShowDuration + AnimationDuration <= CurrentTime <= Time + ShowDuration + AnimationDuration * 2 and DoAnimation == True:
                    X = (CurrentTime - Time - ShowDuration - AnimationDuration) / AnimationDuration
                    X = math.pow(2, 10 * X - 10)
                    X1 = round(EndX1 * (1 - X) + StartX1 * X)
                    Y1 = round(EndY1 * (1 - X) + StartY1 * X)
                    X2 = round(EndX2 * (1 - X) + StartX2 * X)
                    Y2 = round(EndY2 * (1 - X) + StartY2 * X)
                    Render = True
            if Time + (AnimationDuration if DoAnimation else 0) <= CurrentTime <= Time + ShowDuration + (AnimationDuration if DoAnimation else 0):
                X1 = round(EndX1)
                Y1 = round(EndY1)
                X2 = round(EndX2)
                Y2 = round(EndY2)
                Render = True
            elif Time + ShowDuration + (AnimationDuration * 2 if DoAnimation else 0) <= CurrentTime:
                del Variables.Popups[Popup["ID"]]
                Variables.ForceSingleRender = True
            if Render:

                if RoundCorners > 0:
                    cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y1 + RoundCorners / 2)), (round(X2 - RoundCorners / 2), round(Y2 - RoundCorners / 2)), OutlineColor, RoundCorners, Settings.RectangleLineType)
                else:
                    cv2.rectangle(Variables.Frame, (round(X1), round(Y1)), (round(X2), round(Y2)), OutlineColor, -1, Settings.RectangleLineType)

                if RoundCorners > 0:
                    cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2) + 1, round(Y1 + RoundCorners / 2) + 1), (round(X2 - RoundCorners / 2) - 1, round(Y2 - RoundCorners / 2) - 1), Color, RoundCorners, Settings.RectangleLineType)
                    cv2.rectangle(Variables.Frame, (round(X1 + RoundCorners / 2) + 1, round(Y1 + RoundCorners / 2) + 1), (round(X2 - RoundCorners / 2) - 1, round(Y2 - RoundCorners / 2) - 1), Color, -1, Settings.RectangleLineType)
                else:
                    cv2.rectangle(Variables.Frame, (round(X1) + 1, round(Y1) + 1), (round(X2) - 1, round(Y2) - 1), Color, -1, Settings.RectangleLineType)

                if Progress > 0:
                    cv2.line(Variables.Frame, (round(X1 + RoundCorners / 2), round(Y2)), (round(X1 + RoundCorners / 2 + (X2 - X1 - RoundCorners) * Progress / 100), round(Y2)), ProgressBarColor, 1, Settings.LineType)
                elif Progress < 0:
                    X = time.time() % 2
                    if X < 1:
                        Left = 0.5 - math.cos(X ** 2 * math.pi) / 2
                        Right = 0.5 - math.cos((X + (X - X ** 2)) * math.pi) / 2
                    else:
                        X -= 1
                        Left = 0.5 + math.cos((X + (X - X ** 2)) * math.pi) / 2
                        Right = 0.5 + math.cos(X ** 2 * math.pi) / 2
                    cv2.line(Variables.Frame, (round(X1 + RoundCorners / 2 + (X2 - X1 - RoundCorners) * Right), round(Y2)), (round(X1 + RoundCorners / 2 + (X2 - X1 - RoundCorners) * Left), round(Y2)), ProgressBarColor, 1, Settings.LineType)

                Label(Text, X1, Y1, X2, Y2, ID + "#LABEL", "Center", 0, Layer, FontSize, FontType, Translate, TextColor)

    except:
        Errors.ShowError("Elements - Error in function CheckAndRenderPopups.", str(traceback.format_exc()))