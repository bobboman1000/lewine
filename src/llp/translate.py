from langdetect import detect
from transformers import pipeline

# Translation pipelines
el_translation_pipelines = {
    "en": pipeline("translation", model="Helsinki-NLP/opus-mt-en-el", device="cpu"),
    "de": pipeline("translation", model="Helsinki-NLP/opus-mt-de-el", device="cpu"),
}


def auto_translate_to_modern_greek(text: str) -> str:
    # detect source language
    lang = detect(text)

    # check if already in greek
    if lang == "el":
        return text

    if lang in el_translation_pipelines:
        translated = el_translation_pipelines[lang](text)[0]["translation_text"]
        return translated
    else:
        raise ValueError(f"Language '{lang}' is not supported for translation to Greek.")
