from deep_translator import GoogleTranslator
from ImageUI import Variables
from ImageUI import Settings
from ImageUI import Errors
import threading
import traceback
import json
import time
import os


Translator = None
TRANSLATING = False
TRANSLATION_CACHE = {}


# MARK: SetTranslator
def SetTranslator(SourceLanguage:str, DestinationLanguage:str):
    """
    All the text from the UI will be translated. Available languages can be listed with ImageUI.Translations.GetTranslatorLanguages().

    Parameters
    ----------
    SourceLanguage : str
        The source language. Either the language code or the english language name.
    DestinationLanguage : str
        The destination language. Either the language code or the english language name.

    Returns
    -------
    None
    """
    try:
        global Translator, TRANSLATION_CACHE

        SaveCache()

        Translator = None
        while TRANSLATING: time.sleep(0.1)
        TRANSLATION_CACHE = {}

        Languages = GetAvailableLanguages()

        SourceLanguageIsValid = False
        DestinationLanguageIsValid = False
        for Language in Languages:
            if Languages[Language] == SourceLanguage:
                SourceLanguageIsValid = True
                break
            elif Language == SourceLanguage:
                SourceLanguageIsValid = True
                SourceLanguage = Languages[Language]
                break
        for Language in Languages:
            if Languages[Language] == DestinationLanguage:
                DestinationLanguageIsValid = True
                break
            elif Language == DestinationLanguage:
                DestinationLanguageIsValid = True
                DestinationLanguage = Languages[Language]
                break
        if SourceLanguageIsValid:
            Settings.SourceLanguage = SourceLanguage
        else:
            Errors.ShowError("Translate - Error in function SetTranslator.", "Source language not found. Use ImageUI.Translations.GetAvailableLanguages() to list available languages.")
            return
        if DestinationLanguageIsValid:
            Settings.DestinationLanguage = DestinationLanguage
        else:
            Errors.ShowError("Translate - Error in function SetTranslator.", "Destination language not found. Use ImageUI.Translations.GetAvailableLanguages() to list available languages.")
            return

        if SourceLanguage == DestinationLanguage:
            return

        Translator = GoogleTranslator(source=Settings.SourceLanguage, target=Settings.DestinationLanguage)

        if os.path.exists(os.path.join(Settings.CachePath, f"Translations/{Settings.DestinationLanguage}.json")):
            with open(os.path.join(Settings.CachePath, f"Translations/{Settings.DestinationLanguage}.json"), "r") as f:
                try:
                    File = json.load(f)
                except:
                    File = {}
                    with open(os.path.join(Settings.CachePath, f"Translations/{Settings.DestinationLanguage}.json"), "w") as f:
                        json.dump({}, f, indent=4)
                TRANSLATION_CACHE = File
    except:
        Errors.ShowError("Translate - Error in function SetTranslator.", str(traceback.format_exc()))


def TranslateThread(Text):
    try:
        global TRANSLATING, TRANSLATION_CACHE
        while TRANSLATING:
            time.sleep(0.01)
        TRANSLATING = True
        Translation = Translator.translate(Text)
        TRANSLATION_CACHE[Text] = Translation
        Variables.ForceSingleRender = True
        TRANSLATING = False
        return Translation
    except:
        Errors.ShowError("Translate - Error in function TranslateThread.", str(traceback.format_exc()))
        return Text


def TranslationRequest(Text):
    try:
        threading.Thread(target=TranslateThread, args=(Text,), daemon=True).start()
    except:
        Errors.ShowError("Translate - Error in function TranslationRequest.", str(traceback.format_exc()))


def Translate(Text):
    try:
        if Settings.DestinationLanguage == Settings.SourceLanguage or Translator == None:
            return Text
        elif Text in TRANSLATION_CACHE:
            Translation = TRANSLATION_CACHE[Text]
            return Translation
        elif TRANSLATING:
            return Text
        else:
            if Text != "":
                TranslationRequest(Text)
            return Text
    except:
        Errors.ShowError("Translate - Error in function Translate.", str(traceback.format_exc()))
        return Text


# MARK: ManualTranslation
def ManualTranslation(Text, Translation):
    """
    Manually translate a text.

    Parameters
    ----------
    Text : str
        The text to translate.
    Translation : str
        The translated text.

    Returns
    -------
    None
    """
    try:
        global TRANSLATION_CACHE
        TRANSLATION_CACHE[Text] = Translation
        Variables.ForceSingleRender = True
    except:
        Errors.ShowError("Translate - Error in function ManualTranslation.", str(traceback.format_exc()))


# MARK: GetAvailableLanguages
def GetAvailableLanguages():
    """
    Returns the available languages.

    Returns
    -------
    dict
        The available languages.
    """
    try:
        Languages = GoogleTranslator().get_supported_languages(as_dict=True)
        FormattedLanguages = {}
        for Language in Languages:
            FormattedLanguage = ""
            for i, Part in enumerate(str(Language).split("(")):
                FormattedLanguage += ("(" if i > 0 else "") + Part.capitalize()
            FormattedLanguages[FormattedLanguage] = Languages[Language]
        return FormattedLanguages
    except:
        Errors.ShowError("Translate - Error in function GetAvailableLanguages.", str(traceback.format_exc()))
        return {}


# MARK: SaveCache
def SaveCache():
    """
    Save the translation cache. Will be automatically called when using ImageUI.Exit()

    Returns
    -------
    None
    """
    try:
        if Settings.DestinationLanguage != Settings.SourceLanguage and TRANSLATION_CACHE != {}:
            if os.path.exists(os.path.join(Settings.CachePath, "Translations")) == False:
                os.makedirs(os.path.join(Settings.CachePath, "Translations"))
            with open(os.path.join(Settings.CachePath, f"Translations/{Settings.DestinationLanguage}.json"), "w") as f:
                json.dump(TRANSLATION_CACHE, f, indent=4)
    except:
        Errors.ShowError("Translate - Error in function SaveCache.", str(traceback.format_exc()))