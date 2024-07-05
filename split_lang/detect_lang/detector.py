import logging
import langdetect
import fast_langdetect
from langdetect.lang_detect_exception import LangDetectException
from lingua import Language, LanguageDetectorBuilder

from ..model import LangSectionType


all_detector = LanguageDetectorBuilder.from_all_languages().build()


logger = logging.getLogger(__name__)


def detect_lang(text: str) -> str:
    try:
        result = str(langdetect.detect(text))
        result = result.lower()
        return result
    except LangDetectException as e:
        logger.debug(
            "Language detection of `%s` using `langdetect.detect(text)` failed: %s",
            text,
            e,
        )
        return "zh"
    except Exception as e:
        logger.debug(
            "An unexpected error occurred of `%s` using `langdetect.detect(text)`: %s",
            text,
            e,
        )
    return "x"


def fast_lang_detect(text: str) -> str:
    result = str(fast_langdetect.detect(text, low_memory=False)["lang"])
    result = result.lower()
    return result


def lingua_lang_detect_all(text: str) -> str:
    language: Language | None = all_detector.detect_language_of(text=text)
    if language is None:
        return "x"
    return language.iso_code_639_1.name.lower()


# For example '衬衫' cannot be detected by `langdetect`, and `fast_langdetect` will detect it as 'en'
def detect_lang_combined(
    text: str, lang_section_type: LangSectionType, text_len_threshold=3
) -> str:
    # if len(text) <= text_len_threshold:
    #     return detect_lang(text)
    # return fast_lang_detect(text=text)
    return lingua_lang_detect_all(text)
