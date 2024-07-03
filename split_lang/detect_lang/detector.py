import logging
import langdetect
import fast_langdetect
from langdetect.lang_detect_exception import LangDetectException

logger = logging.getLogger(__name__)

LANG_MAP = {
    "zh": "zh",
    "yue": "zh",  # 粤语
    "wuu": "zh",  # 吴语
    "zh-cn": "zh",
    "zh-tw": "x",
    "ko": "ko",
    "ja": "ja",
    "de": "de",
    "fr": "fr",
    "en": "en",
}
DEFAULT_LANG = "x"


def detect_lang(text: str) -> str:
    try:
        result = str(langdetect.detect(text))
        result = result.lower()
        return result
    except LangDetectException as e:
        logger.warning(
            "Language detection of `%s` using `langdetect.detect(text)` failed: %s",
            text,
            e,
        )
        return "zh"
    except Exception as e:
        logger.warning(
            "An unexpected error occurred of `%s` using `langdetect.detect(text)`: %s",
            text,
            e,
        )
    return "x"


def fast_lang_detect(text: str) -> str:
    result = str(fast_langdetect.detect(text, low_memory=False)["lang"])
    result = result.lower()
    return result


# For example '衬衫' cannot be detected by `langdetect`, and `fast_langdetect` will detect it as 'en'
def detect_lang_combined(text: str, text_len_threshold=3) -> str:
    if len(text) <= text_len_threshold:
        return detect_lang(text)
    return fast_lang_detect(text=text)
