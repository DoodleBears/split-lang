from typing import List
from dataclasses import dataclass

from langdetect.lang_detect_exception import LangDetectException
from wtpsplit import SaT, WtP

from langsplit.detect_lang.detector import detect_lang, fast_detect_lang, lang_map


@dataclass
class SubString:
    lang: str
    text: str


class SentenceSplitter:
    def __init__(self, wtp_split_model: WtP | SaT = WtP("wtp-bert-mini")):
        self.wtp_split_model = wtp_split_model

    def split(self, text: str, threshold: float = 5e-5, verbose=False):
        return self.wtp_split_model.split(
            text_or_texts=text, threshold=threshold, verbose=verbose
        )


default_sentence_splitter = SentenceSplitter()


def split(
    text: str,
    threshold: float = 5e-5,
    verbose=False,
    splitter: SentenceSplitter = default_sentence_splitter,
):
    """using
    1. `wtpsplit` to split sentences into 'small' substring
    2. concat substring based on language using `fasttext` and `langdetect`

    Args:
        text (str): text to split
        threshold (float, optional): the lower the more separated (more) substring will return. Defaults to 5e-5.
    """
    substr_list = splitter.split(text=text, threshold=threshold, verbose=verbose)
    if verbose:
        print(f"substr_list: {substr_list}")
    substr_list = _init_substr_lang(substr_list)
    if verbose:
        print(f"substr_list: {substr_list}")
    substr_list = _smart_concat(substr_list)
    if verbose:
        print(f"split_result: {substr_list}")
    return substr_list


def _smart_concat(substr_list: List[SubString]):
    is_concat_complete = False
    while is_concat_complete is False:
        substr_list = _smart_concat_logic(substr_list)
        is_concat_complete = True
        for index, block in enumerate(substr_list):
            if block.lang == "x":
                is_concat_complete = False
                break
            if index < len(substr_list) - 1:
                if substr_list[index].lang == substr_list[index + 1].lang:
                    is_concat_complete = False
                    break
    return substr_list


def _init_substr_lang(substr: List[str]) -> List[SubString]:
    concat_result = []
    lang = ""
    for block in substr:
        try:
            cur_lang = detect_lang(block)
        except LangDetectException:
            cur_lang = lang
        cur_lang = lang_map.get(cur_lang, "en")
        concat_result.append(SubString(cur_lang, block))
        lang = cur_lang
    return concat_result


def _merge_middle_substr_to_two_side(substr_list: List[SubString]):
    for index in range(len(substr_list) - 2):
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
    return "en"


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
    smart_concat_result = []
    lang = ""
    for block in concat_result:
        cur_lang = block.lang
        if cur_lang != lang:
            smart_concat_result.append(block)
        else:
            smart_concat_result[-1].text += block.text
        lang = cur_lang
    return smart_concat_result


def _check_languages(lang_text_list: List[SubString]):
    for index, block in enumerate(lang_text_list):
        try:
            cur_lang = fast_detect_lang(block.text)
        except LangDetectException:
            cur_lang = "en"
        cur_lang = lang_map.get(cur_lang, "en")
        if cur_lang == "ko":
            fast_lang = fast_detect_lang(block.text, text_len_threshold=0)
            if fast_lang != "ko":
                is_left = _get_find_direction(lang_text_list, index)
                cur_lang = _find_nearest_lang_with_direction(
                    lang_text_list, index, is_left
                )
        if cur_lang != "x":
            block.lang = cur_lang
    return lang_text_list


def _smart_concat_logic(lang_text_list: List[SubString]):
    lang_text_list = _merge_middle_substr_to_two_side(lang_text_list)
    lang_text_list = _merge_blocks(lang_text_list)
    lang_text_list = _check_languages(lang_text_list)
    lang_text_list = _merge_middle_substr_to_two_side(lang_text_list)
    lang_text_list = _fill_missing_languages(lang_text_list)
    lang_text_list = _merge_two_side_substr_to_near(lang_text_list)
    lang_text_list = _merge_blocks(lang_text_list)
    lang_text_list = _check_languages(lang_text_list)
    return lang_text_list
