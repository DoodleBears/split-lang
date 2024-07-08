import logging
from typing import Dict, List

import budoux

zh_budoux_parser = budoux.load_default_simplified_chinese_parser()
jp_budoux_parser = budoux.load_default_japanese_parser()

from ..config import DEFAULT_LANG, DEFAULT_LANG_MAP
from ..detect_lang.detector import detect_lang_combined, possible_detection_list
from ..model import LangSectionType, SubString, SubStringSection
from .utils import PUNCTUATION, contains_hangul, contains_zh_ja, contains_ja

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s  %(levelname)s [%(name)s]: %(message)s",
)
logger = logging.getLogger(__name__)


class LangSplitter:

    def __init__(
        self,
        lang_map: Dict = None,
        default_lang: str = DEFAULT_LANG,
        punctuation: str = PUNCTUATION,
        not_merge_punctuation: str = "",
        merge_across_punctuation: bool = True,
        merge_across_digit: bool = True,
        debug: bool = False,
    ) -> None:
        """
        1. pre-split stage will use `punctuation` and `digit` to split text then leave substring that contains language character
        2. rule-based and machine learning model will be used for extract words from substring
        3. if language detection of words are same, concat the words into a new substring

        Args:
            lang_map (Dict, optional): `{"zh-tw": "zh"}` will map `zh-tw` to `zh`. Defaults to `DEFAULT_LANG_MAP`.
            default_lang (str, optional): when `lang_map` did not have the language key detected, fallback to default_lang. Defaults to `DEFAULT_LANG`.
            punctuation (str, optional): character that should be treat as punctuation. Defaults to `PUNCTUATION`.
            not_merge_punctuation (str, optional): usually been set to `.。?？！!` if you do not want to concat all substrings together. Defaults to "".
            merge_across_punctuation (bool, optional): merge substring across punctuation. Defaults to True.
            merge_across_digit (bool, optional): merge substring across number (e.g. `233`, `9.15`) will be concat to near substring. Defaults to True.
            debug (bool, optional): print process for debug. Defaults to False.
        """
        self.lang_map = lang_map if lang_map is not None else DEFAULT_LANG_MAP
        self.default_lang = default_lang
        self.debug = debug
        self.punctuation = punctuation
        self.not_merge_punctuation = not_merge_punctuation
        self.merge_across_punctuation = merge_across_punctuation
        self.merge_across_digit = merge_across_digit

    # MARK: split_by_lang
    def split_by_lang(
        self,
        text: str,
    ) -> List[SubString]:
        """
        1. pre-split stage will use `punctuation` and `digit` to split text then leave substring that contains language character
        2. rule-based and machine learning model will be used for extract words from substring
        3. if language detection of words are same, concat the words into a new substring

        Args:
            text (str): text to split

        Returns:
            List[SubString]: which contains language, text, index, length, is_punctuation and is_digit data of substring text
        """

        sections = self._split(text=text)
        substrings: List[SubString] = []
        for section in sections:
            substrings.extend(section.substrings)

        substrings = self._merge_digit(substrings=substrings)

        if self.merge_across_digit:
            substrings = self._merge_substring_across_digit(substrings=substrings)

        if self.merge_across_punctuation:
            substrings = self._merge_substrings_across_punctuation(
                substrings=substrings,
            )

        return substrings

    # MARK: _split
    def _split(
        self,
        text: str,
    ) -> List[SubStringSection]:
        # MARK: pre split by languages
        # NOTE: since some language share some characters (e.g. Chinese and Japanese)
        # NOTE: while Korean has their own characters,
        # NOTE: For Cyrillic alphabet, Latin alphabet, a lot of languages share the alphabet
        pre_split_section = self._pre_split(text=text)
        if self.debug:
            logger.info("---------pre_split_section:")
            for section in pre_split_section:
                logger.info(section)

        section_index = 0
        for section in pre_split_section:
            section_len = len(section.text)
            if section.lang_section_type is LangSectionType.PUNCTUATION:
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
            elif section.lang_section_type is LangSectionType.DIGIT:
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
            else:
                substrings: List[str] = []
                lang_section_type = LangSectionType.OTHERS
                if section.lang_section_type is LangSectionType.OTHERS:
                    substrings = self._parse_without_zh_ja(section.text)
                elif section.lang_section_type is LangSectionType.KO:
                    substrings = [section.text]
                    lang_section_type = LangSectionType.KO
                elif section.lang_section_type is LangSectionType.ZH_JA:
                    substrings = self._parse_zh_ja(section.text)
                    lang_section_type = LangSectionType.ZH_JA

                substrings_with_lang = self._init_substr_lang(
                    texts=substrings,
                    lang_section_type=lang_section_type,
                )
                for substr in substrings_with_lang:
                    substr.index += section_index
                section.substrings = substrings_with_lang

            section_index += section_len

        if self.debug:
            logger.info("---------_init_substr_lang")
            for section in pre_split_section:
                logger.info(section)

        # MARK: smart merge substring together
        wtpsplit_section = pre_split_section
        for section in wtpsplit_section:
            if section.lang_section_type is LangSectionType.PUNCTUATION:
                continue
            smart_concat_result = self._smart_merge(
                substr_list=section.substrings,
                lang_section_type=section.lang_section_type,
            )
            section.substrings.clear()
            section.substrings = smart_concat_result
        if self.debug:
            logger.info("---------smart_concat_result")
            for section in wtpsplit_section:
                logger.info(section)
        return wtpsplit_section

    # MARK: _parse_without_zh_ja
    def _parse_without_zh_ja(self, text: str):
        words: List[str] = []
        exist_space = False
        chars = []
        for char in text:
            if char.isspace() is False:
                if exist_space:
                    words.append("".join(chars))
                    chars.clear()
                    exist_space = False
                chars.append(char)
            else:
                exist_space = True
                chars.append(char)
        if len(chars) > 0:
            words.append("".join(chars))

        return words

    # MARK: _parse_zh_ja
    def _parse_zh_ja(self, text):
        splitted_texts_jp = []
        splitted_texts_jp = jp_budoux_parser.parse(text)

        splitted_texts_zh_jp = []
        for substring in splitted_texts_jp:
            splitted_texts_zh_jp.extend(zh_budoux_parser.parse(substring))

        new_substrings = [splitted_texts_zh_jp[0]]
        for substring in splitted_texts_zh_jp[1:]:
            is_left_ja = contains_ja(new_substrings[-1])
            is_cur_ja = contains_ja(substring)
            is_both_same_lang = is_left_ja == is_cur_ja
            is_both_ja = is_left_ja is True and is_both_same_lang
            is_both_zh = is_left_ja is False and is_both_same_lang
            if is_both_ja:  # both substring is katakana or hiragana, then concat
                new_substrings[-1] += substring
            elif is_both_zh and len(substring) == 1:
                # NOTE: both substring is full Chinese character, and current one is only one character
                # NOTE: 90% is because we first use ja_parser then zh_parser (from `budoux`)
                # NOTE: Since kanji in Japanese usually not appear by them self, Single character is CAUSED BY zh_parser
                # NOTE: So we let single character concat together, if both substring did not contain kana
                new_substrings[-1] += substring
            else:
                new_substrings.append(substring)

        if len(new_substrings) >= 2 and len(new_substrings[0]) == 1:
            new_substrings[1] = new_substrings[0] + new_substrings[1]
            new_substrings = new_substrings[1:]

        return new_substrings

    # MARK: _pre_split
    def _pre_split(self, text: str) -> List[SubStringSection]:
        sections = []
        current_lang: LangSectionType = LangSectionType.OTHERS
        current_text = []

        def add_substring(lang_section_type: LangSectionType):
            if current_text:
                concat_text = "".join(current_text)

                sections.append(
                    SubStringSection(
                        lang_section_type=lang_section_type,
                        text=concat_text,
                        substrings=[],
                    )
                )
                current_text.clear()

        for index, char in enumerate(text):
            is_space = char.isspace()
            if is_space is False:
                if contains_zh_ja(char):
                    if current_lang != LangSectionType.ZH_JA:
                        add_substring(current_lang)
                        current_lang = LangSectionType.ZH_JA
                elif contains_hangul(char):
                    if current_lang != LangSectionType.KO:
                        add_substring(current_lang)
                        current_lang = LangSectionType.KO
                elif char.isdigit():
                    if current_lang != LangSectionType.DIGIT:
                        add_substring(current_lang)
                        current_lang = LangSectionType.DIGIT
                elif char in self.punctuation:
                    if char == "'" and index > 0 and text[index - 1].isspace() is False:
                        pass
                    else:
                        add_substring(current_lang)
                        current_lang = LangSectionType.PUNCTUATION
                else:
                    if current_lang != LangSectionType.OTHERS:
                        add_substring(current_lang)
                        current_lang = LangSectionType.OTHERS
            current_text.append(char)

        add_substring(current_lang)
        return sections

    # MARK: _smart_merge
    def _smart_merge(
        self,
        substr_list: List[SubString],
        lang_section_type: LangSectionType,
    ):
        substr_list = self._smart_concat_logic(
            substr_list,
            lang_section_type=lang_section_type,
        )
        return substr_list

    # MARK: _init_substr_lang
    def _init_substr_lang(
        self,
        texts: List[str],
        lang_section_type: LangSectionType,
    ) -> List[SubString]:
        substrings = []

        substring_index = 0
        for text in texts:
            length = len(text)
            if text in self.punctuation:
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
                cur_lang = detect_lang_combined(
                    text, lang_section_type=lang_section_type
                )
                cur_lang = self.lang_map.get(cur_lang, self.default_lang)
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

    def _is_middle_short_and_two_side_long(
        self, left: SubString, middle: SubString, right: SubString
    ):
        return middle.length <= 3 and left.length + right.length >= 6

    def _is_cur_short_and_near_long(self, cur: SubString, near: SubString):
        return cur.length <= 2 and near.length >= 6 and near.lang == "zh"

    # MARK: _merge_middle_substr_to_two_side
    def _merge_middle_substr_to_two_side(self, substrings: List[SubString]):
        substr_len = len(substrings)
        if substr_len <= 2:
            return substrings
        for index in range(substr_len - 2):
            left_block = substrings[index]
            middle_block = substrings[index + 1]
            right_block = substrings[index + 2]

            if left_block.lang == right_block.lang and left_block.lang != "x":
                # if different detectors results contains near block's language, then combine

                if (
                    left_block.lang in possible_detection_list(middle_block.text)
                    or self._is_middle_short_and_two_side_long(
                        left_block, middle_block, right_block
                    )
                    or middle_block.lang == "x"
                ):
                    substrings[index + 1].lang = left_block.lang
        return substrings

    # MARK: _merge_side_substr_to_near
    def _merge_side_substr_to_near(self, substrings: List[SubString]):
        # NOTE: Merge leftest substr
        is_lang_x = substrings[0].lang == "x"
        is_cur_short_and_near_long = False
        is_possible_same_lang_with_near = False
        if len(substrings) >= 2:
            is_cur_short_and_near_long = self._is_cur_short_and_near_long(
                substrings[0], substrings[1]
            )

            is_possible_same_lang_with_near = substrings[
                1
            ].lang in possible_detection_list(substrings[0].text)

        is_need_merge_to_right = (
            is_lang_x or is_cur_short_and_near_long or is_possible_same_lang_with_near
        )

        if is_need_merge_to_right:
            substrings[0].lang = self._get_nearest_lang_with_direction(
                substrings, 0, search_left=False
            )
        # NOTE: Merge rightest substr
        is_lang_x = substrings[-1].lang == "x"
        is_cur_short_and_near_long = False
        is_possible_same_lang_with_near = False
        if len(substrings) >= 2:
            is_cur_short_and_near_long = self._is_cur_short_and_near_long(
                substrings[-1], substrings[-2]
            )
            is_possible_same_lang_with_near = substrings[
                -2
            ].lang in possible_detection_list(substrings[-1].text)

        is_need_merge_to_left = is_lang_x or is_cur_short_and_near_long

        if is_need_merge_to_left:
            substrings[-1].lang = self._get_nearest_lang_with_direction(
                substrings, len(substrings) - 1, search_left=True
            )
        return substrings

    # MARK: _fill_unknown_language
    def _fill_unknown_language(
        self,
        substrings: List[SubString],
    ):
        for index, substr in enumerate(substrings):
            if substr.lang == "x":
                if index == 0:
                    # For head substring, find right substring
                    substrings[index].lang = self._get_nearest_lang_with_direction(
                        substrings, index, search_left=False
                    )
                elif index == len(substrings) - 1:
                    # For tail substring, find left substring
                    substrings[index].lang = self._get_nearest_lang_with_direction(
                        substrings, index, search_left=True
                    )
                else:
                    # For body (middle) substring, find based on rule
                    substrings[index].lang = self._get_nearest_lang_with_direction(
                        substrings, index, self._get_merge_direction(substrings, index)
                    )
        return substrings

    # MARK: _find_nearest_lang_with_direction
    def _get_nearest_lang_with_direction(
        self, substrings: List[SubString], index: int, search_left: bool
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

    # MARK: _get_merge_direction
    def _get_merge_direction(self, substrings: List[SubString], index: int) -> bool:
        is_left = False
        if index == 0:
            is_left = False
            return is_left
        elif index == len(substrings) - 1:
            is_left = True
            return is_left
        left_block = substrings[index - 1]
        right_block = substrings[index + 1]
        if len(left_block.text) >= len(right_block.text):
            is_left = True
        else:
            is_left = False
        return is_left

    # MARK: _merge_substrings
    def _merge_substrings(
        self,
        substrings: List[SubString],
    ):
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

    # MARK: _merge_digit
    def _merge_digit(
        self,
        substrings: List[SubString],
    ) -> List[SubString]:
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
        new_substrings = self._merge_substrings(substrings=substrings)
        return new_substrings

    # MARK: _merge_substring_across_digit
    def _merge_substring_across_digit(
        self,
        substrings: List[SubString],
    ) -> List[SubString]:
        new_substrings: List[SubString] = []

        for _, substring in enumerate(substrings):
            if substring.is_digit:

                if new_substrings and new_substrings[-1].lang != "punctuation":
                    new_substrings[-1].text += substring.text
                    new_substrings[-1].length += substring.length
                else:
                    new_substrings.append(substring)
            else:
                if new_substrings and new_substrings[-1].lang == "digit":
                    substring.text = new_substrings[-1].text + substring.text
                    substring.index = new_substrings[-1].index
                    substring.length = new_substrings[-1].length + substring.length

                    new_substrings.pop()
                new_substrings.append(substring)

        new_substrings = self._merge_substrings(substrings=new_substrings)
        return new_substrings

    # MARK: _merge_substrings_across_punctuation
    def _merge_substrings_across_punctuation(
        self,
        substrings: List[SubString],
    ) -> List[SubString]:
        new_substrings: List[SubString] = []
        lang = ""
        for substring in substrings:
            if (
                substring.is_punctuation
                and substring.text.strip() not in self.not_merge_punctuation
            ):
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

    # MARK: _get_languages
    def _get_languages(
        self,
        lang_text_list: List[SubString],
        lang_section_type: LangSectionType,
    ):

        if lang_section_type in [
            LangSectionType.DIGIT,
            LangSectionType.KO,
            LangSectionType.PUNCTUATION,
        ]:
            return lang_text_list

        for _, substr in enumerate(lang_text_list):
            cur_lang = detect_lang_combined(
                text=substr.text, lang_section_type=lang_section_type
            )
            cur_lang = self.lang_map.get(cur_lang, self.default_lang)

            if cur_lang != "x":
                substr.lang = cur_lang
        return lang_text_list

    # MARK: _smart_concat_logic
    def _smart_concat_logic(
        self,
        lang_text_list: List[SubString],
        lang_section_type: LangSectionType,
    ):

        lang_text_list = self._merge_middle_substr_to_two_side(lang_text_list)
        lang_text_list = self._merge_substrings(lang_text_list)
        lang_text_list = self._get_languages(
            lang_text_list=lang_text_list,
            lang_section_type=lang_section_type,
        )
        lang_text_list = self._merge_middle_substr_to_two_side(lang_text_list)
        lang_text_list = self._fill_unknown_language(lang_text_list)
        lang_text_list = self._merge_side_substr_to_near(lang_text_list)
        lang_text_list = self._merge_substrings(lang_text_list)
        lang_text_list = self._get_languages(
            lang_text_list=lang_text_list,
            lang_section_type=lang_section_type,
        )

        return lang_text_list
