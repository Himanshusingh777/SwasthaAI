from googletrans import Translator
import re

translator = Translator()

def translate_to_hindi(text):
    try:
        res = translator.translate(text, dest='hi')
        return res.text
    except Exception:
        return None

def safe_text(s: str):
    if not s:
        return ""
    return re.sub(r"\s+", " ", s.strip())
