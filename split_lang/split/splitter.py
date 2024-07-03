import logging
from typing import Dict, List

from wtpsplit import SaT, WtP

from ..detect_lang.detector import (
    DEFAULT_LANG,
    LANG_MAP,
    detect_lang,
    detect_lang_combined,
)
from .model import SubString, SubStringSection
from .utils import DEFAULT_THRESHOLD, PUNCTUATION, contains_zh_ja, contains_hangul

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s  %(levelname)s [%(name)s]: %(message)s",
)
logger = logging.getLogger(__name__)


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

    def split(
        self, text: str, threshold: float = DEFAULT_THRESHOLD, verbose=False
    ) -> List[str]:
        """
        Split the given text into substrings.

        Args:
            text (str): The text to be split.
            threshold (float, optional): The threshold for splitting. Defaults to `DEFAULT_THRESHOLD`.
            verbose (bool, optional): If True, provides verbose output. Defaults to False.

        Returns:
            List[str]: A list of substrings.

        Note:
            Override this method to implement a custom splitter.
        """
        if text in PUNCTUATION or text.isdigit():
            return text
        return self.wtp_split_model.split(
            text_or_texts=text, threshold=threshold, verbose=verbose
        )


def split_by_lang(
    text: str,
    threshold: float = DEFAULT_THRESHOLD,
    lang_map: Dict = None,
    default_lang: str = DEFAULT_LANG,
    verbose=False,
    splitter: TextSplitter = TextSplitter(),
    merge_across_punctuation: bool = False,
    merge_across_digit: bool = True,
) -> List[SubString]:
    """_summary_

    Args:
        text (str): _description_
        threshold (float, optional): _description_. Defaults to DEFAULT_THRESHOLD.
        lang_map (Dict, optional): _description_. Defaults to None.
        default_lang (str, optional): default language to fallback. Defaults to `DEFAULT_LANG`.
        verbose (bool, optional): _description_. Defaults to False.
        splitter (TextSplitter, optional): _description_. Defaults to default_sentence_splitter.

    Returns:
        List[SubString]: substring with .lang and .text
    """
    if merge_across_digit is None:
        merge_across_digit = merge_across_punctuation

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

    substrings = _merge_digit(substrings=substrings)

    if merge_across_digit:
        substrings = _merge_substring_across_digit(substrings=substrings)

    if merge_across_punctuation:
        substrings = _merge_substrings_across_punctuation(
            substrings=substrings,
        )

    return substrings


def split(
    text: str,
    threshold: float = DEFAULT_THRESHOLD,
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
        threshold (float, optional): the lower the more separated (more) substring will return. Defaults to DEFAULT_THRESHOLD (if your text contains no Chinese, Japanese, Korean, 4.9e-4 is suggested)
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
        logger.info("---------pre_split_section:")
        for section in pre_split_section:
            logger.info(section)

    # MARK: wtpsplit

    section_index = 0
    for section in pre_split_section:
        section_len = len(section.text)
        if section.is_punctuation:
            section.substrings.append(
                SubString(
                    is_digit=False,
                    is_punctuation=True,
                    text=section.text,
                    lang="punctuation",
                    index=section_index,
                    length=section_len,
                )
            )
            if verbose:
                logger.info("---------wtpsplit")
                logger.info(section.substrings)
        elif section.is_digit:
            section.substrings.append(
                SubString(
                    is_digit=True,
                    is_punctuation=False,
                    text=section.text,
                    lang="digit",
                    index=section_index,
                    length=section_len,
                )
            )
            if verbose:
                logger.info("---------wtpsplit")
                logger.info(section.substrings)
        else:
            substrings = splitter.split(
                text=section.text, threshold=threshold, verbose=verbose
            )
            if verbose:
                logger.info("---------wtpsplit")
                logger.info(substrings)

            # MARK: initialize language detect
            substrings_with_lang = _init_substr_lang(
                texts=substrings, lang_map=lang_map, default_lang=default_lang
            )
            for substr in substrings_with_lang:
                substr.index += section_index
            section.substrings = substrings_with_lang

        section_index += section_len

    if verbose:
        logger.info("---------_init_substr_lang")
        for section in pre_split_section:
            logger.info(section)

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
        logger.info("---------smart_concat_result")
        for section in wtpsplit_section:
            logger.info(section)
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
            is_digit = concat_text.strip().isdigit()
            sections.append(
                SubStringSection(
                    text=concat_text,
                    is_punctuation=is_punctuation,
                    is_digit=is_digit,
                    substrings=[],
                )
            )
            # substrings.append("".join(current_text))
            current_text.clear()

    for char in text:
        if char.isspace() is False:
            if contains_zh_ja(char):
                if current_lang != "zh_ja":
                    add_substring()
                    current_lang = "zh_ja"
            elif contains_hangul(char):
                if current_lang != "ko":
                    add_substring()
                    current_lang = "ko"
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
    if lang_map is None:
        lang_map = LANG_MAP

    substring_index = 0
    for text in texts:
        length = len(text)
        if text in PUNCTUATION:
            substrings.append(
                SubString(
                    is_punctuation=True,
                    is_digit=False,
                    lang="punctuation",
                    text=text,
                    length=length,
                    index=substring_index,
                )
            )
        elif text.strip().isdigit():
            substrings.append(
                SubString(
                    is_punctuation=False,
                    is_digit=True,
                    lang="digit",
                    text=text,
                    length=length,
                    index=substring_index,
                )
            )
        else:
            cur_lang = detect_lang_combined(text)
            cur_lang = lang_map.get(cur_lang, "x")
            substrings.append(
                SubString(
                    is_digit=False,
                    is_punctuation=False,
                    lang=cur_lang,
                    text=text,
                    length=length,
                    index=substring_index,
                )
            )

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
    # Left
    is_lang_x = substrings[0].lang == "x"
    is_digit = substrings[0].is_digit
    is_too_short = len(substrings[0].text) <= 1

    is_need_merge_to_right = is_lang_x or is_digit or is_too_short

    if is_need_merge_to_right:
        substrings[0].lang = _find_nearest_lang_with_direction(
            substrings, 0, search_left=False
        )
    # Right
    is_lang_x = substrings[-1].lang == "x"
    is_digit = substrings[-1].is_digit
    is_too_short = len(substrings[-1].text) <= 1

    is_need_merge_to_left = is_lang_x or is_digit or is_too_short

    if is_need_merge_to_left:
        substrings[-1].lang = _find_nearest_lang_with_direction(
            substrings, len(substrings) - 1, search_left=True
        )
    return substrings


def _fill_missing_languages(substrings: List[SubString]):
    for index, substr in enumerate(substrings):
        if substr.lang == "x":
            if index == 0:
                # For head substring, find right substring
                substrings[index].lang = _find_nearest_lang_with_direction(
                    substrings, index, search_left=False
                )
            elif index == len(substrings) - 1:
                # For tail substring, find left substring
                substrings[index].lang = _find_nearest_lang_with_direction(
                    substrings, index, search_left=True
                )
            else:
                # For body (middle) substring, find based on rule
                is_left = _get_find_direction(substrings, index)
                substrings[index].lang = _find_nearest_lang_with_direction(
                    substrings, index, is_left
                )
    return substrings


def _find_nearest_lang_with_direction(
    substrings: List[SubString], index: int, search_left: bool
) -> str:
    if search_left:
        for i in range(1, len(substrings)):
            left_i_index = index - i
            if (
                left_i_index >= 0
                and substrings[left_i_index].lang != "x"
                and substrings[left_i_index].is_digit is False
            ):
                return substrings[left_i_index].lang
    else:
        for i in range(1, len(substrings)):
            right_i_index = index + i
            if (
                right_i_index < len(substrings)
                and substrings[right_i_index].lang != "x"
                and substrings[right_i_index].is_digit is False
            ):
                return substrings[right_i_index].lang
    return substrings[index].lang


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


def _merge_digit(substrings: List[SubString]) -> List[SubString]:
    new_substrings: List[SubString] = []

    substr_len = len(substrings)
    if substr_len >= 3:
        for index in range(substr_len - 2):
            left_block = substrings[index]
            middle_block = substrings[index + 1]
            right_block = substrings[index + 2]

            if (
                left_block.lang == right_block.lang
                and left_block.is_digit
                and middle_block.is_punctuation
            ):
                substrings[index + 1].lang = left_block.lang
    new_substrings = _merge_substrings(substrings=substrings)
    return new_substrings


def _merge_substring_across_digit(substrings: List[SubString]) -> List[SubString]:
    new_substrings: List[SubString] = []
    left_digit_index = 0
    is_left_has_digit = False

    for index, substring in enumerate(substrings):
        if substring.is_digit:
            if index == 0:
                is_left_has_digit = True
            if new_substrings:
                new_substrings[-1].text += substring.text
                new_substrings[-1].length += substring.length
        else:
            if left_digit_index == 0:
                left_digit_index = index
            new_substrings.append(substring)

    if is_left_has_digit:
        left_digit_text = "".join(
            substr.text for substr in substrings[0:left_digit_index]
        )
        if new_substrings:
            new_substrings[0].text = left_digit_text + new_substrings[0].text
            new_substrings[0].length = len(left_digit_text) + new_substrings[0].length
        else:
            new_substrings.append(
                SubString(
                    is_digit=True,
                    is_punctuation=False,
                    text=left_digit_text,
                    length=len(left_digit_text),
                    lang="digit",
                    index=0,
                )
            )
    new_substrings = _merge_substrings(substrings=new_substrings)
    return new_substrings


def _merge_substrings_across_punctuation(
    substrings: List[SubString],
) -> List[SubString]:
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


def _get_languages(
    lang_text_list: List[SubString],
    lang_map: Dict = None,
    default_lang: str = DEFAULT_LANG,
):
    if lang_map is None:
        lang_map = LANG_MAP

    for index, substr in enumerate(lang_text_list):
        if substr.is_punctuation or substr.is_digit:
            continue
        cur_lang = detect_lang_combined(substr.text)
        cur_lang = lang_map.get(cur_lang, default_lang)
        # if (
        #     cur_lang == "ko"
        # ):  # `langdetect` has problem distinguish ko among zh, ja and ko
        #     fast_lang = detect_lang_combined(substr.text, text_len_threshold=0)
        #     if fast_lang != cur_lang:
        #         is_left = _get_find_direction(lang_text_list, index)
        #         cur_lang = _find_nearest_lang_with_direction(
        #             lang_text_list, index, is_left
        #         )
        if cur_lang != "x":
            substr.lang = cur_lang
    return lang_text_list


def _smart_concat_logic(
    lang_text_list: List[SubString], lang_map: Dict = None, default_lang: str = None
):

    lang_text_list = _merge_middle_substr_to_two_side(lang_text_list)
    lang_text_list = _merge_substrings(lang_text_list)
    lang_text_list = _get_languages(
        lang_text_list=lang_text_list, lang_map=lang_map, default_lang="x"
    )
    lang_text_list = _merge_middle_substr_to_two_side(lang_text_list)
    lang_text_list = _fill_missing_languages(lang_text_list)
    lang_text_list = _merge_two_side_substr_to_near(lang_text_list)
    lang_text_list = _merge_substrings(lang_text_list)
    lang_text_list = _get_languages(
        lang_text_list=lang_text_list, lang_map=lang_map, default_lang=default_lang
    )

    return lang_text_list
