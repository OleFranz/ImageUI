from deep_translator import GoogleTranslator
from ImageUI import variables
from ImageUI import settings
import threading
import unidecode
import json
import time
import os


TRANSLATING = False
TRANSLATION_CACHE = {}
AVAILABLE_LANGUAGES = {}


def Initialize(SourceLanguage=None, DestinationLanguage=None):
    global Translator, TRANSLATION_CACHE
    if SourceLanguage != None:
        settings.SourceLanguage = SourceLanguage
    if DestinationLanguage != None:
        settings.DestinationLanguage = DestinationLanguage
    Languages = GetAvailableLanguages()
    LanugageIsValid = False
    for Language in Languages:
        if str(Languages[Language]) == str(settings.DestinationLanguage):
            LanugageIsValid = True
            break
    if LanugageIsValid == False:
        settings.DestinationLanguage = settings.SourceLanguage
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


def TranslateThread(Text):
    global TRANSLATING, TRANSLATION_CACHE
    while TRANSLATING:
        time.sleep(0.1)
    TRANSLATING = True
    Translation = Translator.translate(Text)
    TRANSLATION_CACHE[Text] = unidecode.unidecode(Translation)
    variables.ForceSingleRender = True
    TRANSLATING = False
    return Translation


def TranslationRequest(Text):
    threading.Thread(target=TranslateThread, args=(Text,), daemon=True).start()


def Translate(Text):
    if settings.DestinationLanguage == settings.SourceLanguage:
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


def GetAvailableLanguages(ForceNewSearch=False):
    global AVAILABLE_LANGUAGES
    if ForceNewSearch == False and AVAILABLE_LANGUAGES != {}:
        return AVAILABLE_LANGUAGES
    Languages = GoogleTranslator().get_supported_languages(as_dict=True)
    FormattedLanguages = {}
    for Language in Languages:
        FormattedLanguage = ""
        for i, Part in enumerate(str(Language).split("(")):
            FormattedLanguage += ("(" if i > 0 else "") + Part.capitalize()
        FormattedLanguages[FormattedLanguage] = Languages[Language]
    AVAILABLE_LANGUAGES = FormattedLanguages
    return FormattedLanguages


def SaveCache():
    if settings.DestinationLanguage != settings.SourceLanguage:
        if os.path.exists(os.path.join(settings.CachePath, "Translations")) == False:
            os.makedirs(os.path.join(settings.CachePath, "Translations"))
        with open(os.path.join(settings.CachePath, f"Translations/{settings.DestinationLanguage}.json"), "w") as f:
            json.dump(TRANSLATION_CACHE, f, indent=4)