import re

PUNCTUATION = r"""〜~,.;:!?，。！？；：、·([{<（【《〈「『“‘)]}>）】》〉」』”’"-_——#$%&……￥'*+<=>?@[\]^_`{|}~"""

chinese_char_pattern = re.compile(r"[\u4e00-\u9fff]")
hangul_pattern = re.compile(r"[\uac00-\ud7af]")
hiragana_katakana_pattern = re.compile(r"[\u3040-\u30ff々]")  # 添加了对“々”符号的判断

zh_ja_pattern = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff々]")


def contains_chinese_char(text: str) -> bool:
    return bool(chinese_char_pattern.search(text))


def contains_hangul(text: str) -> bool:
    return bool(hangul_pattern.search(text))


def contains_ja_kana(text: str) -> bool:
    return bool(hiragana_katakana_pattern.search(text))


def contains_zh_ja(text: str) -> bool:
    return bool(zh_ja_pattern.search(text))
