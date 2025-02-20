import re

PUNCTUATION = r"""〜~,.;:!?，。！？；：、·([{<（【《〈「『“‘)]}>）】》〉」』”’"-_——#$%&……￥'*+<=>?@[\]^_`{|}~"""

chinese_char_pattern = re.compile(r"[\u4e00-\u9fff]")
hangul_pattern = re.compile(r"[\uac00-\ud7af]")
hiragana_katakana_pattern = re.compile(r"[\u3040-\u30ff々]")  # 添加了对“々”符号的判断

zh_ja_pattern = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff々]")


def contains_chinese_char(text: str) -> bool:
    """
    check if the text contains Chinese character

    Args:
        text (str): the text to check

    Returns:
    """
    return bool(chinese_char_pattern.search(text))

def contains_hangul(text: str) -> bool:
    """
    check if the text contains hangul

    Args:
        text (str): the text to check

    Returns:
    """
    return bool(hangul_pattern.search(text))
def contains_ja_kana(text: str) -> bool:
    """
    check if the text contains Japanese or kana

    Args:
        text (str): the text to check

    Returns:
    """
    return bool(hiragana_katakana_pattern.search(text))

def contains_zh_ja(text: str) -> bool:
    """
    check if the text contains Chinese or Japanese

    Args:
        text (str): the text to check

    Returns:
        bool: if the text contains Chinese or Japanese, return True, otherwise return False
    """
    return bool(zh_ja_pattern.search(text))

def contains_only_kana(text: str) -> bool:
    """
    check if the text only contains hiragana or katakana

    Args:
        text (str): the text to check

    Returns:
        bool: if the text only contains hiragana or katakana, return True, otherwise return False
    """
    is_only_kana = True
    for char in text:
        if not hiragana_katakana_pattern.match(char):
            is_only_kana = False
            break
    return is_only_kana

