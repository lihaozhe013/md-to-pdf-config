import locale
import json
from pathlib import Path


_translations: dict[str, str] = {}
_current_lang: str = "en"


def load_language(lang: str):
    global _translations, _current_lang
    path = Path(__file__).parent / f"{lang}.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            _translations = json.load(f)
    else:
        _translations = {}
    _current_lang = lang


def _(text: str) -> str:
    return _translations.get(text, text)


def current_lang() -> str:
    return _current_lang


def detect_system_lang() -> str:
    try:
        lang, _ = locale.getlocale(locale.LC_CTYPE)
        if lang and lang.startswith("zh"):
            return "zh_CN"
    except Exception:
        pass
    return "en"
