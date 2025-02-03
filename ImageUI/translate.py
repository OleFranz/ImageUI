from deep_translator import GoogleTranslator
from ImageUI import variables
from ImageUI import settings
from ImageUI import errors
import threading
import traceback
import unidecode
import json
import time
import os


Translator = None
TRANSLATING = False
TRANSLATION_CACHE = {}


def Initialize(SourceLanguage=None, DestinationLanguage=None):
    try:
        global Translator, TRANSLATION_CACHE
        if SourceLanguage != None:
            settings.SourceLanguage = SourceLanguage
        if DestinationLanguage != None:
            settings.DestinationLanguage = DestinationLanguage

        Languages = GetAvailableLanguages()

        SourceLanguageIsValid = False
        DestinationLanguageIsValid = False
        for Language in Languages:
            if str(Languages[Language]) == str(settings.SourceLanguage):
                SourceLanguageIsValid = True
                break
            if str(Languages[Language]) == str(settings.DestinationLanguage):
                DestinationLanguageIsValid = True
                break
        if SourceLanguageIsValid == False:
            errors.ShowError("Translate - Error in function Initialize.", "Source language not found. Use GetAvailableLanguages() to list available languages.")
            return
        if DestinationLanguageIsValid == False:
            errors.ShowError("Translate - Error in function Initialize.", "Destination language not found. Use GetAvailableLanguages() to list available languages.")
            return

        Translator = GoogleTranslator(source=settings.SourceLanguage, target=settings.DestinationLanguage)

        if os.path.exists(os.path.join(settings.CachePath, f"Translations/{settings.DestinationLanguage}.json")):
            with open(os.path.join(settings.CachePath, f"Translations/{settings.DestinationLanguage}.json"), "r") as f:
                try:
                    File = json.load(f)
                except:
                    File = {}
                    with open(os.path.join(settings.CachePath, f"Translations/{settings.DestinationLanguage}.json"), "w") as f:
                        json.dump({}, f, indent=4)
                TRANSLATION_CACHE = File
    except:
        errors.ShowError("Translate - Error in function Initialize.", str(traceback.format_exc()))


def TranslateThread(Text):
    try:
        global TRANSLATING, TRANSLATION_CACHE
        while TRANSLATING:
            time.sleep(0.1)
        TRANSLATING = True
        Translation = Translator.translate(Text)
        TRANSLATION_CACHE[Text] = unidecode.unidecode(Translation)
        variables.ForceSingleRender = True
        TRANSLATING = False
        return Translation
    except:
        errors.ShowError("Translate - Error in function TranslateThread.", str(traceback.format_exc()))
        return Text


def TranslationRequest(Text):
    try:
        threading.Thread(target=TranslateThread, args=(Text,), daemon=True).start()
    except:
        errors.ShowError("Translate - Error in function TranslationRequest.", str(traceback.format_exc()))


def Translate(Text):
    try:
        if settings.DestinationLanguage == settings.SourceLanguage or Translator == None:
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
        errors.ShowError("Translate - Error in function Translate.", str(traceback.format_exc()))
        return Text


def GetAvailableLanguages():
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
        errors.ShowError("Translate - Error in function GetAvailableLanguages.", str(traceback.format_exc()))
        return {}


def SaveCache():
    try:
        if settings.DestinationLanguage != settings.SourceLanguage:
            if os.path.exists(os.path.join(settings.CachePath, "Translations")) == False:
                os.makedirs(os.path.join(settings.CachePath, "Translations"))
            with open(os.path.join(settings.CachePath, f"Translations/{settings.DestinationLanguage}.json"), "w") as f:
                json.dump(TRANSLATION_CACHE, f, indent=4)
    except:
        errors.ShowError("Translate - Error in function SaveCache.", str(traceback.format_exc()))