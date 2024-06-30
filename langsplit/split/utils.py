import re

PUNCTUATION = r""",.;:!?，。！？；：、·([{<（【《〈「『“‘)]}>）】》〉」』”’"""

chinese_char_pattern = re.compile(r"[\u4e00-\u9fff]")
hangul_pattern = re.compile(r"[\uac00-\ud7af]")
hiragana_pattern = re.compile(r"[\u3040-\u309f]")
katakana_pattern = re.compile(r"[\u30a0-\u30ff]")


def _contains_chinese_char(text: str):
    return bool(chinese_char_pattern.search(text))


def _contains_hangul(text: str):
    return bool(hangul_pattern.search(text))


def _contains_hiragana(text: str):
    return bool(hiragana_pattern.search(text))


def _contains_katakana(text: str):
    return bool(katakana_pattern.search(text))


def contains_zh_ja_ko(text):
    if (
        _contains_chinese_char(text)
        or _contains_hangul(text)
        or _contains_hiragana(text)
        or _contains_katakana(text)
    ):
        return True
    return False
