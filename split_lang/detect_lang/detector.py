import logging
from typing import List

import fast_langdetect
from wordfreq import word_frequency

from ..model import LangSectionType
from ..split.utils import contains_ja_kana

logger = logging.getLogger(__name__)


def fast_lang_detect(text: str) -> str:
    result = str(fast_langdetect.detect(text, low_memory=False)["lang"])
    result = result.lower()
    return result


# For example '衬衫' cannot be detected by `langdetect`, and `fast_langdetect` will detect it as 'en'
def detect_lang_combined(text: str, lang_section_type: LangSectionType) -> str:
    if lang_section_type is LangSectionType.ZH_JA:
        if contains_ja_kana(text):
            return "ja"
        return fast_lang_detect(text)
    return fast_lang_detect(text)


def possible_detection_list(text: str) -> List[str]:
    text = text.replace("\n", "").strip()
    languages = [
        item["lang"]
        for item in fast_langdetect.detect_multilingual(
            text,
            low_memory=False,
            k=5,
            threshold=0.01,
        )
    ]
    return languages


def _detect_word_freq_in_lang(word: str, lang: str) -> float:
    return word_frequency(word=word, lang=lang)


def is_word_freq_higher_in_lang_b(word: str, lang_a: str, lang_b: str) -> bool:
    if lang_a == "x" or lang_b == "x":
        return False
    word_freq_lang_b = _detect_word_freq_in_lang(word=word, lang=lang_b)
    word_freq_lang_a = _detect_word_freq_in_lang(word=word, lang=lang_a)
    if word_freq_lang_a == 0:
        return False
    # 0.8 means either is more frequently used in Japanese or in both language the word is frequently used
    return (word_freq_lang_b / word_freq_lang_a) > 0.8
