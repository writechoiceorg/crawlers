import langdetect
import langid


def is_translated(text, language):
    try:
        lang = langdetect.detect(text)
        lang2, _ = langid.classify(text)
        return lang == language and lang2 == language
    except Exception:
        return None
