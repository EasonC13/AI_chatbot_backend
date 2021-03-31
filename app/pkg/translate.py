import os
from core.config import GOOGLE_APPLICATION_CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= GOOGLE_APPLICATION_CREDENTIALS

text = "I'm so good"
target = "zh"

import six
from google.cloud import translate_v2 as translate
translate_client = translate.Client()

def translate(text, target = "zh-tw"):
    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    return {
        "translatedText": result["translatedText"],
        "detectedSourceLanguage": result["detectedSourceLanguage"]
    }
    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
