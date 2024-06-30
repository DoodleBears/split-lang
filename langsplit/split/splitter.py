from typing import Dict, List

from langdetect.lang_detect_exception import LangDetectException
from wtpsplit import SaT, WtP

from langsplit.detect_lang.detector import (
    DEFAULT_LANG,
    LANG_MAP,
    detect_lang,
    fast_detect_lang,
)
from langsplit.split.utils import contains_zh_ja_ko, PUNCTUATION
from langsplit.split.model import SubString, SubStringSection


class TextSplitter:
    """
    Base class for splitting text into substrings.

    This class provides a default implementation using a WtP model.
    Users can override the `split` method to implement their own custom splitter.

    Attributes:
        wtp_split_model (WtP | SaT): The model used for splitting text.
    """

    def __init__(self, wtp_split_model: WtP | SaT = WtP("wtp-bert-mini")):
        self.wtp_split_model = wtp_split_model

    def split(self, text: str, threshold: float = 4.9e-5, verbose=False) -> List[str]:
        """
        Split the given text into substrings.

        Args:
            text (str): The text to be split.
            threshold (float, optional): The threshold for splitting. Defaults to 4.9e-5.
            verbose (bool, optional): If True, provides verbose output. Defaults to False.

        Returns:
            List[str]: A list of substrings.

        Note:
            Override this method to implement a custom splitter.
        """
        if text in PUNCTUATION:
            return text
        return self.wtp_split_model.split(
            text_or_texts=text, threshold=threshold, verbose=verbose
        )


def split_to_substring(
    text: str,
    threshold: float = 4.9e-5,
    lang_map: Dict = None,
    default_lang: str = DEFAULT_LANG,
    verbose=False,
    splitter: TextSplitter = TextSplitter(),
    merge_across_punctuation: bool = False,
) -> List[SubString]:
    """_summary_

    Args:
        text (str): _description_
        threshold (float, optional): _description_. Defaults to 4.9e-5.
        lang_map (Dict, optional): _description_. Defaults to None.
        default_lang (str, optional): default language to fallback. Defaults to `DEFAULT_LANG`.
        verbose (bool, optional): _description_. Defaults to False.
        splitter (TextSplitter, optional): _description_. Defaults to default_sentence_splitter.

    Returns:
        List[SubString]: substring with .lang and .text
    """
    sections = split(
        text=text,
        threshold=threshold,
        lang_map=lang_map,
        default_lang=default_lang,
        verbose=verbose,
        splitter=splitter,
    )
    substrings: List[SubString] = []
    for section in sections:
        substrings.extend(section.substrings)

    if merge_across_punctuation:
        substrings = _merge_substrings_across_punctuation(
            substrings=substrings,
        )
    return substrings


def split(
    text: str,
    threshold: float = 4.9e-5,
    lang_map: Dict = None,
    default_lang: str = DEFAULT_LANG,
    verbose=False,
    splitter: TextSplitter = TextSplitter(),
) -> List[SubStringSection]:
    """using
    1. `wtpsplit` to split sentences into 'small' substring
    2. concat substring based on language using `fasttext` and `langdetect`

    Args:
        text (str): text to split
        threshold (float, optional): the lower the more separated (more) substring will return. Defaults to 4.9e-5 (if your text contains no Chinese, Japanese, Korean, 4.9e-4 is suggested)
        lang_map (_type_, optional): mapping different language to same language for better result, if you know the range of your target languages. Defaults to None.
        default_lang (str, optional): default language to fallback. Defaults to `DEFAULT_LANG`.
        verbose (bool, optional): print the process. Defaults to False.
        splitter (TextSplitter, optional): sentence splitter. Defaults to default_sentence_splitter.

    Returns:
        List[SubStringSection]: Multiple sections (separate by punctuation), each section contains substring with .lang and .text
    """
    # MARK: pre split by languages (zh, ja, ko)
    pre_split_section = _pre_split(text=text)
    if verbose:
        print("---------pre_split_section:")
        for section in pre_split_section:
            print(section)

    # MARK: wtpsplit

    section_index = 0
    for section in pre_split_section:
        section_len = len(section.text)
        if section.is_punctuation:
            section.substrings.append(
                SubString(
                    is_punctuation=True,
                    text=section.text,
                    lang="punctuation",
                    index=section_index,
                    length=section_len,
                )
            )
        else:
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

        section_index += section_len

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
                    text=concat_text,
                    is_punctuation=is_punctuation,
                    substrings=[],
                )
            )
            # substrings.append("".join(current_text))
            current_text.clear()

    for char in text:
        if char.isspace() is False:
            if contains_zh_ja_ko(char):
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
    substrings = []
    lang = ""
    if lang_map is None:
        lang_map = LANG_MAP

    substring_index = 0
    for text in texts:
        length = len(text)
        if text in PUNCTUATION:
            substrings.append(
                SubString(
                    is_punctuation=True,
                    lang="punctuation",
                    text=text,
                    length=length,
                    index=substring_index,
                )
            )
        else:
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
            substrings.append(
                SubString(
                    is_punctuation=False,
                    lang=cur_lang,
                    text=text,
                    length=length,
                    index=substring_index,
                )
            )
            lang = cur_lang

        substring_index += length
    return substrings


def _merge_middle_substr_to_two_side(substrings: List[SubString]):
    substr_len = len(substrings)
    if substr_len <= 2:
        return substrings
    for index in range(substr_len - 2):
        left_block = substrings[index]
        middle_block = substrings[index + 1]
        right_block = substrings[index + 2]

        if left_block.lang == right_block.lang and left_block.lang != "x":
            if len(middle_block.text) <= 1 or middle_block.lang == "x":
                substrings[index + 1].lang = left_block.lang
    return substrings


def _merge_two_side_substr_to_near(substrings: List[SubString]):
    if substrings[0].lang == "x":
        for substr in substrings:
            if substr.lang != "x":
                substrings[0].lang = substr.lang
                break
    elif len(substrings[0].text) <= 1:
        substrings[0].lang = _find_nearest_lang_with_direction(
            substrings, 0, is_left=False
        )
    if substrings[-1].lang == "x":
        substrings[-1].lang = _find_nearest_lang_with_direction(
            substrings, len(substrings) - 1, is_left=True
        )
    return substrings


def _fill_missing_languages(substrings: List[SubString]):
    for index, substr in enumerate(substrings):
        if substr.lang == "x":
            if index == 0:
                # For head substring, find right substring
                substrings[index].lang = _find_nearest_lang_with_direction(
                    substrings, index, is_left=False
                )
            elif index == len(substrings) - 1:
                # For tail substring, find left substring
                substrings[index].lang = _find_nearest_lang_with_direction(
                    substrings, index, is_left=True
                )
            else:
                # For body (middle) substring, find based on rule
                is_left = _get_find_direction(substrings, index)
                substrings[index].lang = _find_nearest_lang_with_direction(
                    substrings, index, is_left
                )
    return substrings


def _find_nearest_lang_with_direction(
    substrings: List[SubString], index: int, is_left: bool
):
    if is_left:
        for i in range(1, len(substrings)):
            if index - i >= 0 and substrings[index - i].lang != "x":
                return substrings[index - i].lang
    else:
        for i in range(1, len(substrings)):
            if index + i < len(substrings) and substrings[index + i].lang != "x":
                return substrings[index + i].lang
    return "x"


def _get_find_direction(substrings: List[SubString], index: int) -> bool:
    is_left = False
    if index == 0:
        is_left = False
        return is_left
    elif index == len(substrings) - 1:
        is_left = True
        return is_left
    left_block = substrings[index - 1]
    right_block = substrings[index + 1]
    if len(left_block.text) < len(right_block.text) or right_block.lang not in [
        "ja",
        "zh",
    ]:
        is_left = True
    else:
        is_left = False
    return is_left


def _merge_substrings(substrings: List[SubString]):
    smart_concat_result: List[SubString] = []
    lang = ""
    for block in substrings:
        cur_lang = block.lang
        if cur_lang != lang:
            smart_concat_result.append(block)
        else:
            smart_concat_result[-1].text += block.text
            smart_concat_result[-1].length += block.length
        lang = cur_lang
    return smart_concat_result


def _merge_substrings_across_punctuation(substrings: List[SubString]):
    new_substrings: List[SubString] = []
    lang = ""
    for substring in substrings:
        if substring.is_punctuation:
            if new_substrings and new_substrings[-1].lang == lang:
                new_substrings[-1].text += substring.text
                new_substrings[-1].length += substring.length
            else:
                new_substrings.append(substring)
        else:
            if substring.lang != lang:
                new_substrings.append(substring)
            else:
                new_substrings[-1].text += substring.text
                new_substrings[-1].length += substring.length
        lang = substring.lang if substring.lang != "punctuation" else lang
    return new_substrings


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
            if fast_lang != cur_lang:
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
    # print("# _merge_middle_substr_to_two_side")
    lang_text_list = _merge_middle_substr_to_two_side(lang_text_list)
    # print("# _merge_blocks")
    lang_text_list = _merge_substrings(lang_text_list)
    # print("# _check_languages")
    lang_text_list = _check_languages(
        lang_text_list=lang_text_list, lang_map=lang_map, default_lang=default_lang
    )
    # print("# _merge_middle_substr_to_two_side")
    lang_text_list = _merge_middle_substr_to_two_side(lang_text_list)
    # print("# _fill_missing_languages")
    lang_text_list = _fill_missing_languages(lang_text_list)
    # print("# _merge_two_side_substr_to_near")
    lang_text_list = _merge_two_side_substr_to_near(lang_text_list)
    # print("# _merge_blocks")
    lang_text_list = _merge_substrings(lang_text_list)
    # print("# _check_languages")
    lang_text_list = _check_languages(
        lang_text_list=lang_text_list, lang_map=lang_map, default_lang=default_lang
    )

    return lang_text_list
