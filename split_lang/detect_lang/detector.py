import logging
from typing import List

import fast_langdetect

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
