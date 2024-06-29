import re
from typing import Dict, List

from langdetect.lang_detect_exception import LangDetectException
from pydantic import BaseModel
from wtpsplit import SaT, WtP

from langsplit.detect_lang.detector import (
    DEFAULT_LANG,
    LANG_MAP,
    detect_lang,
    fast_detect_lang,
)

# 定义正则表达式来匹配汉字（简体和繁体）
chinese_char_pattern = re.compile(r"[\u4e00-\u9fff]")
# 定义正则表达式来匹配韩文
hangul_pattern = re.compile(r"[\uac00-\ud7af]")
# 定义正则表达式来匹配日文平假名
hiragana_pattern = re.compile(r"[\u3040-\u309f]")
# 定义正则表达式来匹配日文片假名
katakana_pattern = re.compile(r"[\u30a0-\u30ff]")


def _contains_chinese_char(text: str):
    return bool(chinese_char_pattern.search(text))


def _contains_hangul(text: str):
    return bool(hangul_pattern.search(text))


def _contains_hiragana(text: str):
    return bool(hiragana_pattern.search(text))


def _contains_katakana(text: str):
    return bool(katakana_pattern.search(text))


def _contains_zh_ja_ko(text):
    if (
        _contains_chinese_char(text)
        or _contains_hangul(text)
        or _contains_hiragana(text)
        or _contains_katakana(text)
    ):
        return True
    return False


class SubString(BaseModel):
    lang: str
    text: str


class SubStringSection(BaseModel):
    is_punctuation: bool = False
    text: str
    substrings: List[SubString]


class SentenceSplitter:
    def __init__(self, wtp_split_model: WtP | SaT = WtP("wtp-bert-mini")):
        self.wtp_split_model = wtp_split_model

    def split(self, text: str, threshold: float = 5e-5, verbose=False) -> List[str]:
        if text in PUNCTUATION:
            return text
        return self.wtp_split_model.split(
            text_or_texts=text, threshold=threshold, verbose=verbose
        )


default_sentence_splitter = SentenceSplitter()


def split(
    text: str,
    threshold: float = 5e-5,
    lang_map: Dict = None,
    default_lang: str = DEFAULT_LANG,
    verbose=False,
    splitter: SentenceSplitter = default_sentence_splitter,
) -> List[SubStringSection]:
    """using
    1. `wtpsplit` to split sentences into 'small' substring
    2. concat substring based on language using `fasttext` and `langdetect`

    Args:
        text (str): text to split
        threshold (float, optional): the lower the more separated (more) substring will return. Defaults to 5e-5 (if your text contains no Chinese, Japanese, Korean, 1e-3 is suggested)
        lang_map (_type_, optional): mapping different language to same language for better result, if you know the range of your target languages. Defaults to None.
        verbose (bool, optional): print the process. Defaults to False.
        splitter (SentenceSplitter, optional): sentence splitter. Defaults to default_sentence_splitter.

    Returns:
        List[SubString]: substring with .lang and .text
    """
    # MARK: pre split by languages (zh, ja, ko)
    pre_split_section = _pre_split(text=text)
    if verbose:
        print("---------pre_split_section:")
        for section in pre_split_section:
            print(section)

    # MARK: wtpsplit

    for section in pre_split_section:
        if section.is_punctuation:
            continue
        substrings = splitter.split(
            text=section.text, threshold=threshold, verbose=verbose
        )
        if verbose:
            print("---------wtpsplit")
            print(substrings)

        # MARK: initialize language detect
        substrings_with_lang = _init_substr_lang(
            texts=substrings, lang_map=lang_map, default_lang=default_lang
        )
        section.substrings = substrings_with_lang

    if verbose:
        print("---------_init_substr_lang")
        for section in pre_split_section:
            print(section)

    # MARK: smart merge substring together
    wtpsplit_section = pre_split_section
    for section in wtpsplit_section:
        if section.is_punctuation:
            continue
        smart_concat_result = _smart_merge(
            substr_list=section.substrings,
            lang_map=lang_map,
            default_lang=default_lang,
        )
        section.substrings.clear()
        section.substrings = smart_concat_result
    if verbose:
        print("---------smart_concat_result")
        for section in wtpsplit_section:
            print(section)
    return wtpsplit_section


# Adding additional punctuation from other languages
PUNCTUATION = r""",.;:!?，。！？；：、·([{<（【《〈「『“‘)]}>）】》〉」』”’"""


def _pre_split(text: str) -> List[SubStringSection]:
    """
    1. split Chinese, Japanese and Korean substring and other languages
    2. split punctuation

    Args:
        text (str): input text

    Returns:
        List[str]: list of substring
    """
    sections = []
    current_lang = None
    current_text = []

    def add_substring():
        if current_text:
            concat_text = "".join(current_text)

            is_punctuation = concat_text.strip() in PUNCTUATION
            sections.append(
                SubStringSection(
                    text=concat_text, is_punctuation=is_punctuation, substrings=[]
                )
            )
            # substrings.append("".join(current_text))
            current_text.clear()

    for char in text:
        if char.isspace() is False:
            if _contains_zh_ja_ko(char):
                if current_lang != "zh_ja_ko":
                    add_substring()
                    current_lang = "zh_ja_ko"
            elif char in PUNCTUATION:
                add_substring()
                current_lang = "punctuation"
            else:
                if current_lang != "other":
                    add_substring()
                    current_lang = "other"
        current_text.append(char)

    add_substring()
    return sections


# def _pre_split_by_paired_brackets(text: str) -> List[str]:
#     """Separate text into substrings based on paired brackets.

#     Args:
#         text (str): input text

#     Returns:
#         List[str]: list of substrings
#     """
#     substrings = []
#     current_text = []
#     bracket_stack = []
#     left_brackets = "([{<（【《〈「『“‘"
#     right_brackets = ")]}>）】》〉」』”’"
#     bracket_pairs = {
#         ")": "(",
#         "]": "[",
#         "}": "{",
#         "）": "（",
#         "】": "【",
#         "》": "《",
#         "〉": "〈",
#         "」": "「",
#         "』": "『",
#         "”": "“",
#         "’": "‘",
#     }

#     def add_substring():
#         if current_text:
#             substrings.append("".join(current_text))
#             current_text.clear()

#     i = 0
#     while i < len(text):
#         char = text[i]
#         if char in left_brackets:
#             if not bracket_stack:
#                 add_substring()
#             bracket_stack.append(char)
#             current_text.append(char)
#         elif char in right_brackets:
#             current_text.append(char)
#             if bracket_stack and bracket_stack[-1] == bracket_pairs[char]:
#                 bracket_stack.pop()
#                 if not bracket_stack:
#                     add_substring()
#             else:
#                 # Unmatched right bracket, treat as normal character
#                 add_substring()
#                 substrings.append(char)
#         else:
#             current_text.append(char)
#         i += 1

#     add_substring()
#     return substrings


def _smart_merge(
    substr_list: List[SubString],
    lang_map: Dict = None,
    default_lang: str = DEFAULT_LANG,
):
    if lang_map is None:
        lang_map = LANG_MAP
    is_concat_complete = False
    while is_concat_complete is False:
        substr_list = _smart_concat_logic(
            substr_list, lang_map=lang_map, default_lang=default_lang
        )
        is_concat_complete = True

        if len(substr_list) == 1 and substr_list[0].lang == "x":
            substr_list[0].lang = fast_detect_lang(substr_list[0].text)

        for index, block in enumerate(substr_list):
            if block.lang == "x":
                is_concat_complete = False
                break
            if index < len(substr_list) - 1:
                if substr_list[index].lang == substr_list[index + 1].lang:
                    is_concat_complete = False
                    break
    return substr_list


def _init_substr_lang(
    texts: List[str], lang_map: Dict = None, default_lang: str = DEFAULT_LANG
) -> List[SubString]:
    concat_result = []
    lang = ""
    if lang_map is None:
        lang_map = LANG_MAP

    for text in texts:
        if text in PUNCTUATION:
            concat_result.append(
                SubString(is_punctuation=True, lang="punctuation", text=text)
            )
            continue
        try:
            cur_lang = detect_lang(text)
        except LangDetectException:
            cur_lang = lang
        cur_lang = lang_map.get(cur_lang, default_lang)
        if cur_lang == "x":
            try:
                cur_lang = fast_detect_lang(text)
                cur_lang = lang_map.get(cur_lang, default_lang)
            except Exception:
                cur_lang = lang
        concat_result.append(SubString(lang=cur_lang, text=text))
        lang = cur_lang
    return concat_result


def _merge_middle_substr_to_two_side(substr_list: List[SubString]):
    substr_len = len(substr_list)
    if substr_len <= 2:
        return substr_list
    for index in range(substr_len - 2):
        left_block = substr_list[index]
        middle_block = substr_list[index + 1]
        right_block = substr_list[index + 2]

        if left_block.lang == right_block.lang and left_block.lang != "x":
            if len(middle_block.text) <= 1 or middle_block.lang == "x":
                substr_list[index + 1].lang = left_block.lang
    return substr_list


def _merge_two_side_substr_to_near(concat_result: List[SubString]):
    if concat_result[0].lang == "x":
        for substr in concat_result:
            if substr.lang != "x":
                concat_result[0].lang = substr.lang
                break
    elif len(concat_result[0].text) <= 1:
        concat_result[0].lang = _find_nearest_lang_with_direction(
            concat_result, 0, is_left=False
        )
    if concat_result[-1].lang == "x":
        concat_result[-1].lang = _find_nearest_lang_with_direction(
            concat_result, len(concat_result) - 1, is_left=True
        )
    return concat_result


def _fill_missing_languages(concat_result: List[SubString]):
    for index, substr in enumerate(concat_result):
        if substr.lang == "x":
            if index == 0:
                # For head substring, find right substring
                concat_result[index].lang = _find_nearest_lang_with_direction(
                    concat_result, index, is_left=False
                )
            elif index == len(concat_result) - 1:
                # For tail substring, find left substring
                concat_result[index].lang = _find_nearest_lang_with_direction(
                    concat_result, index, is_left=True
                )
            else:
                # For body (middle) substring, find based on rule
                is_left = _get_find_direction(concat_result, index)
                concat_result[index].lang = _find_nearest_lang_with_direction(
                    concat_result, index, is_left
                )
    return concat_result


def _find_nearest_lang_with_direction(
    concat_result: List[SubString], index: int, is_left: bool
):
    if is_left:
        for i in range(1, len(concat_result)):
            if index - i >= 0 and concat_result[index - i].lang != "x":
                return concat_result[index - i].lang
    else:
        for i in range(1, len(concat_result)):
            if index + i < len(concat_result) and concat_result[index + i].lang != "x":
                return concat_result[index + i].lang
    return "x"


def _get_find_direction(substr_list: List[SubString], index: int) -> bool:
    is_left = False
    if index == 0:
        is_left = False
        return is_left
    elif index == len(substr_list) - 1:
        is_left = True
        return is_left
    left_block = substr_list[index - 1]
    right_block = substr_list[index + 1]
    if len(left_block.text) < len(right_block.text) or right_block.lang not in [
        "ja",
        "zh",
    ]:
        is_left = True
    else:
        is_left = False
    return is_left


def _merge_blocks(concat_result: List[SubString]):
    smart_concat_result: List[SubString] = []
    lang = ""
    for block in concat_result:
        cur_lang = block.lang
        if cur_lang != lang:
            smart_concat_result.append(block)
        else:
            smart_concat_result[-1].text += block.text
        lang = cur_lang
    return smart_concat_result


def _check_languages(
    lang_text_list: List[SubString],
    lang_map: Dict = None,
    default_lang: str = DEFAULT_LANG,
):
    if lang_map is None:
        lang_map = LANG_MAP

    for index, substr in enumerate(lang_text_list):
        try:
            cur_lang = fast_detect_lang(substr.text)
        except LangDetectException:
            cur_lang = default_lang
        cur_lang = lang_map.get(cur_lang, default_lang)
        if cur_lang == "ko":
            fast_lang = fast_detect_lang(substr.text, text_len_threshold=0)
            if fast_lang != "ko":
                is_left = _get_find_direction(lang_text_list, index)
                cur_lang = _find_nearest_lang_with_direction(
                    lang_text_list, index, is_left
                )
        if cur_lang != "x":
            substr.lang = cur_lang
    return lang_text_list


def _smart_concat_logic(
    lang_text_list: List[SubString], lang_map: Dict = None, default_lang: str = None
):
    print("# _merge_middle_substr_to_two_side")
    lang_text_list = _merge_middle_substr_to_two_side(lang_text_list)
    print("# _merge_blocks")
    lang_text_list = _merge_blocks(lang_text_list)
    print("# _check_languages")
    lang_text_list = _check_languages(
        lang_text_list=lang_text_list, lang_map=lang_map, default_lang=default_lang
    )
    print("# _merge_middle_substr_to_two_side")
    lang_text_list = _merge_middle_substr_to_two_side(lang_text_list)
    print("# _fill_missing_languages")
    lang_text_list = _fill_missing_languages(lang_text_list)
    print("# _merge_two_side_substr_to_near")
    lang_text_list = _merge_two_side_substr_to_near(lang_text_list)
    print("# _merge_blocks")
    lang_text_list = _merge_blocks(lang_text_list)
    print("# _check_languages")
    lang_text_list = _check_languages(
        lang_text_list=lang_text_list, lang_map=lang_map, default_lang=default_lang
    )

    return lang_text_list
