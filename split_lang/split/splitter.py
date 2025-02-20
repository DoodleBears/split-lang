import logging
from typing import Dict, List

import budoux

zh_budoux_parser = budoux.load_default_simplified_chinese_parser()
jp_budoux_parser = budoux.load_default_japanese_parser()

from ..config import (DEFAULT_LANG, DEFAULT_LANG_MAP, NO_ZH_JA_LANG_MAP,
                      ZH_JA_LANG_MAP)
from ..detect_lang.detector import (detect_lang_combined,
                                    is_word_freq_higher_in_lang_b,
                                    possible_detection_list)
from ..model import LangSectionType, SubString, SubStringSection
from .utils import (PUNCTUATION, contains_hangul, contains_ja_kana,
                    contains_only_kana, contains_zh_ja)

logger = logging.getLogger(__name__)


class LangSplitter:
    def __init__(
        self,
        lang_map: Dict[str, str] = DEFAULT_LANG_MAP,
        default_lang: str = DEFAULT_LANG,
        punctuation: str = PUNCTUATION,
        not_merge_punctuation: str = "",
        merge_across_punctuation: bool = True,
        merge_across_digit: bool = True,
        merge_across_newline: bool = True,
        debug: bool = True,
        log_level: int = logging.INFO,
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
        self.lang_map = lang_map
        self.default_lang = default_lang
        self.debug = debug
        self.punctuation = punctuation
        self.not_merge_punctuation = not_merge_punctuation
        self.merge_across_punctuation = merge_across_punctuation
        self.merge_across_digit = merge_across_digit
        self.merge_across_newline = merge_across_newline
        self.log_level = log_level
        logging.basicConfig(
            level=self.log_level,
            format="%(asctime)s  %(levelname)s [%(name)s]: %(message)s",
        )

    # MARK: split_by_lang
    def split_by_lang(
        self,
        text: str,
    ) -> List[SubString]:
        """
        Args:
            text (str): text to split

        Returns:
            List[SubString]: which contains language, text, index, length, is_punctuation and is_digit data of substring text
        """
        # FIXME: 调整 merge 顺序，最后合并 punctuation
        pre_split_section = self.pre_split(text=text)

        sections = self._split(pre_split_section=pre_split_section)

        if self.merge_across_digit:  # 合并跨数字的 SubString
            sections = self._merge_substrings_across_digit_based_on_sections(
                sections=sections
            )
            # sections = self._smart_merge_all(pre_split_section=pre_split_section)

        if self.merge_across_punctuation:  # 合并跨标点符号的 SubString
            sections = self._merge_substrings_across_punctuation_based_on_sections(
                sections=sections
            )
            # sections = self._smart_merge_all(pre_split_section=pre_split_section)

        if self.merge_across_newline:
            sections = self._merge_substrings_across_newline_based_on_sections(
                sections=sections
            )
            # sections = self._smart_merge_all(pre_split_section=pre_split_section)

        for section in sections:
            if section.lang_section_type == LangSectionType.ZH_JA:
                section.substrings = self._special_merge_for_zh_ja(section.substrings)

        substrings: List[SubString] = []
        for section in sections:
            substrings.extend(section.substrings)

        return substrings

    # MARK: pre_split
    def pre_split(self, text: str) -> List[SubStringSection]:
        # NOTE: since some language share some characters (e.g. Chinese and Japanese)
        # NOTE: while Korean has their own characters,
        # NOTE: For Cyrillic alphabet, Latin alphabet, a lot of languages share the alphabet
        text = text.strip()
        if self.debug:
            logger.debug("---------before pre_split:")
            logger.debug(text)
        sections: List[SubStringSection] = []
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
                    # For English, "'" is a part of word
                    pass
                # elif current_lang != LangSectionType.PUNCTUATION:
                else:
                    # [, ] \n .都会单独作为一个 SubString
                    add_substring(current_lang)
                    current_lang = LangSectionType.PUNCTUATION
            elif char.isspace():
                # concat space to current text
                if char in ["\n", "\r"]:
                    add_substring(current_lang)
                    current_lang = LangSectionType.NEWLINE
                else:
                    pass
            else:
                if current_lang != LangSectionType.OTHERS:
                    add_substring(current_lang)
                    current_lang = LangSectionType.OTHERS

            current_text.append(char)

        add_substring(current_lang)
        if self.debug:
            logger.debug("---------after pre_split:")
            for section in sections:
                logger.debug(section)
        return sections

    # MARK: _split
    def _split(
        self,
        pre_split_section: List[SubStringSection],
    ) -> List[SubStringSection]:
        # TODO: 针对不同语言 set 进行不同处理
        section_index = 0
        for section in pre_split_section:
            section_len = len(section.text)
            if section.lang_section_type is LangSectionType.PUNCTUATION:
                # NOTE: 标点符号作为单独的 SubString
                section.substrings.append(
                    SubString(
                        text=section.text,
                        lang="punctuation",
                        index=section_index,
                        length=section_len,
                    )
                )
            elif section.lang_section_type is LangSectionType.DIGIT:
                # NOTE: 数字作为单独的 SubString
                section.substrings.append(
                    SubString(
                        text=section.text,
                        lang="digit",
                        index=section_index,
                        length=section_len,
                    )
                )
            elif section.lang_section_type is LangSectionType.NEWLINE:
                # NOTE: 换行作为单独的 SubString
                section.substrings.append(
                    SubString(
                        text=section.text,
                        lang="newline",
                        index=section_index,
                        length=section_len,
                    )
                )
            else:
                substrings_with_lang: List[SubString] = []
                if section.lang_section_type is LangSectionType.ZH_JA:
                    temp_substrings = self._parse_zh_ja(section.text)
                    substrings_with_lang = self._init_substr_lang(
                        texts=temp_substrings,
                        lang_map=ZH_JA_LANG_MAP,
                        lang_section_type=LangSectionType.ZH_JA,
                    )

                elif section.lang_section_type is LangSectionType.KO:
                    substrings_with_lang = [
                        SubString(
                            text=section.text,
                            lang="ko",
                            index=section_index,
                            length=section_len,
                        )
                    ]

                else:
                    temp_substrings = self._parse_without_zh_ja(section.text)
                    substrings_with_lang = self._init_substr_lang(
                        texts=temp_substrings,
                        lang_section_type=LangSectionType.OTHERS,
                    )
                # 更新 index
                for substr in substrings_with_lang:
                    substr.index += section_index
                if self.debug:
                    logger.debug("---------after _init_substr_lang:")
                    for substr in substrings_with_lang:
                        logger.debug(substr)

                section.substrings = substrings_with_lang

            section_index += section_len

        pre_split_section = self._smart_merge_all(pre_split_section)
        if self.debug:
            logger.debug("---------after split:")
            for section in pre_split_section:
                logger.debug(section)

        return pre_split_section

        # MARK: smart merge substring together

    def _smart_merge_all(self, pre_split_section: List[SubStringSection]):
        for section in pre_split_section:
            if (
                section.lang_section_type is LangSectionType.PUNCTUATION
                or section.lang_section_type is LangSectionType.NEWLINE
            ):
                # print(section.text)
                continue
            smart_concat_result = self._smart_merge(
                substr_list=section.substrings,
                lang_section_type=section.lang_section_type,
            )
            section.substrings.clear()
            section.substrings = smart_concat_result
        
        if self.debug:
            logger.debug("---------after smart_merge_all:")
            for section in pre_split_section:
                logger.debug(section)

        return pre_split_section

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
    def _parse_zh_ja(self, text) -> List[str]:
        splitted_texts_jp = []
        splitted_texts_jp = jp_budoux_parser.parse(text)
        if self.debug:
            logger.debug("---------after jp_budoux_parser:")
            logger.debug(splitted_texts_jp)

        splitted_texts_zh_jp = []
        for substring in splitted_texts_jp:
            splitted_texts_zh_jp.extend(zh_budoux_parser.parse(substring))
        if self.debug:
            logger.debug("---------after zh_budoux_parser:")
            logger.debug(splitted_texts_zh_jp)

        new_substrings = [splitted_texts_zh_jp[0]]
        for substring in splitted_texts_zh_jp[1:]:
            is_left_ja_kana = contains_ja_kana(new_substrings[-1])
            is_cur_ja_kana = contains_ja_kana(substring)
            is_both_same_lang = is_left_ja_kana == is_cur_ja_kana
            is_both_ja_kana = is_left_ja_kana is True and is_both_same_lang
            is_both_zh = is_left_ja_kana is False and is_both_same_lang
            if is_both_ja_kana:  # both substring is katakana or hiragana, then concat
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

        if self.debug:
            logger.debug("---------after parse_zh_ja:")
            logger.debug(new_substrings)

        return new_substrings

    # MARK: _smart_merge
    def _smart_merge(
        self,
        substr_list: List[SubString],
        lang_section_type: LangSectionType,
    ) -> List[SubString]:
        lang_text_list = substr_list
        lang_text_list = self._merge_substrings(lang_text_list)
        lang_text_list = self._merge_middle_substr_to_two_side(lang_text_list)
        lang_text_list = self._merge_substrings(lang_text_list)
        # NOTE: get_languages 需要根据不同语言进行不同处理
        lang_text_list = self._get_languages(
            lang_text_list=lang_text_list,
            lang_section_type=lang_section_type,
            lang_map=ZH_JA_LANG_MAP
            if lang_section_type is LangSectionType.ZH_JA
            else NO_ZH_JA_LANG_MAP,
        )
        lang_text_list = self._merge_middle_substr_to_two_side(lang_text_list)
        lang_text_list = self._merge_substrings(lang_text_list)
        lang_text_list = self._fill_unknown_language(lang_text_list)
        lang_text_list = self._merge_side_substr_to_near(lang_text_list)
        lang_text_list = self._merge_substrings(lang_text_list)
        lang_text_list = self._get_languages(
            lang_text_list=lang_text_list,
            lang_section_type=lang_section_type,
            lang_map=ZH_JA_LANG_MAP
            if lang_section_type is LangSectionType.ZH_JA
            else NO_ZH_JA_LANG_MAP,
        )
        lang_text_list = self._merge_middle_substr_to_two_side(lang_text_list)
        lang_text_list = self._merge_substrings(lang_text_list)

        return lang_text_list

    def _is_merge_middle_to_two_side(
        self, left: SubString, middle: SubString, right: SubString
    ):
        
        is_middle_only_kana = contains_only_kana(middle.text)
        
        middle_lang_is_possible_the_same_as_left = left.lang in possible_detection_list(
            middle.text
        ) and not is_middle_only_kana
        middle_lang_is_x = middle.lang == "x"
        is_middle_short_and_two_side_long = (
            middle.length <= 3 and left.length + right.length >= 6 and not is_middle_only_kana
        )
        
        is_middle_zh_side_ja_and_middle_is_high_freq_in_ja = (
            left.lang == "ja"
            and middle.lang == "zh"
            and is_word_freq_higher_in_lang_b(middle.text, middle.lang, "ja")
        )

        return (
            middle_lang_is_possible_the_same_as_left
            or middle_lang_is_x
            or is_middle_short_and_two_side_long
            or is_middle_zh_side_ja_and_middle_is_high_freq_in_ja
        )

    def _is_cur_short_and_near_long(self, cur: SubString, near: SubString):
        is_cur_short_and_near_is_zh_and_long = (
            cur.length <= 2 and near.length >= 6 and near.lang == "zh"
        )
        # e.g. 日本人, 今晚, 国外移民
        cur_lang_is_possible_the_same_as_near = near.lang in possible_detection_list(
            cur.text
        )
        is_cur_short_and_near_is_ja_and_middle_is_high_freq_in_ja = (
            cur.length <= 4
            and cur.lang == "zh"
            and near.lang == "ja"
            and is_word_freq_higher_in_lang_b(cur.text, cur.lang, "ja")
        )
        is_cur_short_and_near_is_zh_and_middle_is_high_freq_in_zh = (
            cur.length <= 4
            and cur.lang == "ja"
            and near.lang == "zh"
            and is_word_freq_higher_in_lang_b(cur.text, cur.lang, "zh")
        )
        return (
            is_cur_short_and_near_is_zh_and_long
            or cur_lang_is_possible_the_same_as_near
            or is_cur_short_and_near_is_ja_and_middle_is_high_freq_in_ja
            or is_cur_short_and_near_is_zh_and_middle_is_high_freq_in_zh
        )

    # MARK: _merge_middle_substr_to_two_side
    def _merge_middle_substr_to_two_side(self, substrings: List[SubString]):
        substr_len = len(substrings)
        if substr_len <= 2:
            return substrings
        for index in range(substr_len - 2):
            left_block = substrings[index]
            middle_block = substrings[index + 1]
            right_block = substrings[index + 2]

            if (
                left_block.lang == right_block.lang
                and left_block.lang != "x"
                and left_block.lang != "newline"
            ):
                # if different detectors results contains near block's language, then combine

                if self._is_merge_middle_to_two_side(
                    left_block, middle_block, right_block
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

            is_possible_same_lang_with_near = (
                substrings[1].lang in possible_detection_list(substrings[0].text)
                and substrings[1].length <= 5
            )

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
            is_possible_same_lang_with_near = (
                substrings[-2].lang in possible_detection_list(substrings[-1].text)
                and substrings[-2].length <= 5
            )

        is_need_merge_to_left = (
            is_lang_x or is_cur_short_and_near_long or is_possible_same_lang_with_near
        )

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
                    and substrings[left_i_index].lang != "digit"
                ):
                    return substrings[left_i_index].lang
        else:
            for i in range(1, len(substrings)):
                right_i_index = index + i
                if (
                    right_i_index < len(substrings)
                    and substrings[right_i_index].lang != "x"
                    and substrings[right_i_index].lang != "digit"
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

    # MARK: _special_merge_for_zh_ja
    def _special_merge_for_zh_ja(
        self,
        substrings: List[SubString],
    ) -> List[SubString]:
        new_substrings: List[SubString] = []

        if len(substrings) == 1:
            return substrings
        # NOTE: 统计每个语言的字符串长度
        substring_text_len_by_lang = {
            "zh": 0,
            "ja": 0,
            "x": 0,
            "digit": 0,
            "punctuation": 0,
            "newline": 0,
        }
        index = 0
        while index < len(substrings):
            current_block = substrings[index]
            substring_text_len_by_lang[current_block.lang] += current_block.length
            if index == 0:
                if (
                    substrings[index + 1].lang in ["zh", "ja"]
                    and substrings[index].lang in ["zh", "ja", "x"]
                    and substrings[index].length * 10 < substrings[index + 1].length
                ):
                    right_block = substrings[index + 1]
                    new_substrings.append(
                        SubString(
                            is_digit=False,
                            is_punctuation=False,
                            lang=right_block.lang,
                            text=current_block.text + right_block.text,
                            length=current_block.length + right_block.length,
                            index=current_block.index,
                        )
                    )
                    index += 1
                else:
                    new_substrings.append(substrings[index])
            elif index == len(substrings) - 1:
                left_block = new_substrings[-1]
                if (
                    left_block.lang in ["zh", "ja"]
                    and current_block.lang in ["zh", "ja", "x"]
                    and current_block.length * 10 < left_block.length
                ):
                    new_substrings[-1].text += current_block.text
                    new_substrings[-1].length += current_block.length

                    index += 1
                else:
                    new_substrings.append(substrings[index])
            else:
                if (
                    new_substrings[-1].lang == substrings[index + 1].lang
                    and new_substrings[-1].lang in ["zh", "ja"]
                    # and substrings[index].lang in ["zh", "ja", "x"]
                    and substrings[index].lang != "en"
                    and substrings[index].length * 10
                    < new_substrings[-1].length + substrings[index + 1].length
                ):
                    left_block = new_substrings[-1]
                    right_block = substrings[index + 1]
                    current_block = substrings[index]
                    new_substrings[-1].text += current_block.text + right_block.text
                    new_substrings[-1].length += (
                        current_block.length + right_block.length
                    )
                    index += 1
                else:
                    new_substrings.append(substrings[index])
            index += 1

        # NOTE: 如果 substring_count 中 存在 x，则将 x 设置为最多的 lang
        if substring_text_len_by_lang["x"] > 0:
            max_lang = max(
                substring_text_len_by_lang, key=substring_text_len_by_lang.get
            )
            for index, substr in enumerate(new_substrings):
                if substr.lang == "x":
                    new_substrings[index].lang = max_lang
        # NOTE: 如果 ja 数量是 zh 数量的 10 倍以上，则该 zh 设置为 ja
        if substring_text_len_by_lang["ja"] >= substring_text_len_by_lang["zh"] * 10:
            for index, substr in enumerate(new_substrings):
                if substr.lang == "zh":
                    new_substrings[index].lang = "ja"
        new_substrings = self._merge_substrings(substrings=new_substrings)
        return new_substrings

    # MARK: _merge_substrings_across_newline
    def _merge_substrings_across_newline(
        self,
        substrings: List[SubString],
    ) -> List[SubString]:
        new_substrings: List[SubString] = []
        last_lang = ""

        for _, substring in enumerate(substrings):
            if new_substrings:
                if substring.lang == "newline":
                    # If the last substring is also a newline, merge them
                    new_substrings[-1].text += substring.text
                    new_substrings[-1].length += substring.length
                else:
                    if substring.lang == last_lang or last_lang == "":
                        new_substrings[-1].text += substring.text
                        new_substrings[-1].length += substring.length
                        new_substrings[-1].lang = (
                            substring.lang
                            if new_substrings[-1].lang == "newline"
                            else new_substrings[-1].lang
                        )
                    else:
                        new_substrings.append(substring)
            else:
                new_substrings.append(substring)
            last_lang = substring.lang

        return new_substrings

    # MARK: _merge_substrings_across_newline_based_on_sections
    def _merge_substrings_across_newline_based_on_sections(
        self,
        sections: List[SubStringSection],
    ) -> List[SubStringSection]:
        new_sections: List[SubStringSection] = [sections[0]]
        # NOTE: 将 sections 中的 newline 合并到临近的非 punctuation 的 section
        for index, _ in enumerate(sections):
            if index == 0:
                continue
            if index >= len(sections):
                break

            current_section = sections[index]
            if new_sections[-1].lang_section_type == LangSectionType.NEWLINE:
                # NOTE: 如果前一个 section 是 newline，则合并
                new_sections[-1].lang_section_type = current_section.lang_section_type
                new_sections[-1].text += current_section.text
                new_sections[-1].substrings.extend(current_section.substrings)
                for index, substr in enumerate(new_sections[-1].substrings):
                    if index == 0:
                        continue
                    else:
                        substr.index = (
                            new_sections[-1].substrings[index - 1].index
                            + new_sections[-1].substrings[index - 1].length
                        )

            elif current_section.lang_section_type == LangSectionType.NEWLINE:
                # NOTE: 如果前一个 section 不是 punctuation，则合并
                new_sections[-1].text += current_section.text
                new_sections[-1].substrings.extend(current_section.substrings)
                new_sections[-1].substrings[-1].index = (
                    new_sections[-1].substrings[-2].index
                    + new_sections[-1].substrings[-2].length
                )
            else:
                new_sections.append(current_section)
        # NOTE: 将相同类型的 section 合并
        new_sections_merged: List[SubStringSection] = [new_sections[0]]
        for index, _ in enumerate(new_sections):
            if index == 0:
                continue
            if (
                new_sections_merged[-1].lang_section_type
                == new_sections[index].lang_section_type
            ):
                new_sections_merged[-1].text += new_sections[index].text
                new_sections_merged[-1].substrings.extend(
                    new_sections[index].substrings
                )
            else:
                new_sections_merged.append(new_sections[index])
        # NOTE: 重新计算 index
        for section_index, section in enumerate(new_sections_merged):
            if section_index == 0:
                for substr_index, substr in enumerate(section.substrings):
                    if substr_index == 0:
                        continue
                    else:
                        substr.index = (
                            section.substrings[substr_index - 1].index
                            + section.substrings[substr_index - 1].length
                        )
            else:
                for substr_index, substr in enumerate(section.substrings):
                    if substr_index == 0:
                        substr.index = (
                            new_sections_merged[section_index - 1].substrings[-1].index
                            + new_sections_merged[section_index - 1]
                            .substrings[-1]
                            .length
                        )
                    else:
                        substr.index = (
                            section.substrings[substr_index - 1].index
                            + section.substrings[substr_index - 1].length
                        )
        # NOTE: 合并 sections 中的 substrings 里面的 text
        for section in new_sections_merged:
            section.substrings = self._merge_substrings_across_newline(
                substrings=section.substrings
            )
        if self.debug:
            logger.debug(
                "---------------------------------after_merge_newline_sections:"
            )
            for section in new_sections_merged:
                logger.debug(section)
        return new_sections_merged

    # MARK: _merge_substring_across_digit
    def _merge_substrings_across_digit(
        self,
        substrings: List[SubString],
    ) -> List[SubString]:
        new_substrings: List[SubString] = []
        last_lang = ""

        for _, substring in enumerate(substrings):
            if new_substrings:
                if substring.lang == "digit":
                    new_substrings[-1].text += substring.text
                    new_substrings[-1].length += substring.length
                else:
                    if substring.lang == last_lang or last_lang == "":
                        new_substrings[-1].text += substring.text
                        new_substrings[-1].length += substring.length
                        if substring.lang != "punctuation":
                            new_substrings[-1].lang = substring.lang
                    else:
                        new_substrings.append(substring)
            else:
                new_substrings.append(substring)
            last_lang = substring.lang

        return new_substrings

    # MARK: _merge_substrings_across_digit_based_on_sections
    def _merge_substrings_across_digit_based_on_sections(
        self,
        sections: List[SubStringSection],
    ) -> List[SubStringSection]:
        new_sections: List[SubStringSection] = [sections[0]]
        # NOTE: 将 sections 中的 digit 合并到临近的非 digit 的 section
        for index, _ in enumerate(sections):
            if index == 0:
                continue
            if index >= len(sections):
                break

            current_section = sections[index]
            # print(f"当前 section：{current_section.lang_section_type}")
            # 如果前一个 section 和当前的 section 类型不同，则合并
            one_of_section_is_digit = (
                new_sections[-1].lang_section_type == LangSectionType.DIGIT
                or current_section.lang_section_type == LangSectionType.DIGIT
            )
            if one_of_section_is_digit:
                # print(f"测试：{new_sections[-1].text} | {current_section.text}")
                if new_sections[-1].lang_section_type == LangSectionType.DIGIT:
                    if current_section.lang_section_type != LangSectionType.PUNCTUATION:
                        new_sections[
                            -1
                        ].lang_section_type = current_section.lang_section_type
                    new_sections[-1].text += current_section.text
                    new_sections[-1].substrings[-1].text += current_section.substrings[
                        0
                    ].text
                    new_sections[-1].substrings[
                        -1
                    ].length += current_section.substrings[0].length
                    new_sections[-1].substrings[-1].lang = (
                        current_section.substrings[0].lang
                        if current_section.substrings[0].lang != "punctuation"
                        else new_sections[-1].substrings[-1].lang
                    )
                    new_sections[-1].substrings.extend(current_section.substrings[1:])
                    for index, substr in enumerate(new_sections[-1].substrings):
                        if index == 0:
                            continue
                        else:
                            substr.index = (
                                new_sections[-1].substrings[index - 1].index
                                + new_sections[-1].substrings[index - 1].length
                            )
                elif current_section.lang_section_type == LangSectionType.DIGIT:
                    new_sections[-1].text += current_section.text
                    new_sections[-1].substrings[-1].text += current_section.substrings[
                        0
                    ].text
                    new_sections[-1].substrings[
                        -1
                    ].length += current_section.substrings[0].length
                    if new_sections[-1].substrings[-1].lang == "punctuation":
                        new_sections[-1].substrings[-1].lang = "digit"

                    if (
                        new_sections[-1].lang_section_type
                        == LangSectionType.PUNCTUATION
                    ):
                        new_sections[-1].lang_section_type = LangSectionType.DIGIT

            else:
                new_sections.append(current_section)
        # NOTE: 将相同类型的 section 合并
        new_sections_merged: List[SubStringSection] = [new_sections[0]]
        for index, _ in enumerate(new_sections):
            if index == 0:
                continue
            if (
                new_sections_merged[-1].lang_section_type
                == new_sections[index].lang_section_type
            ):
                new_sections_merged[-1].text += new_sections[index].text
                new_sections_merged[-1].substrings.extend(
                    new_sections[index].substrings
                )
            else:
                new_sections_merged.append(new_sections[index])
        # NOTE: 重新计算 index
        for section_index, section in enumerate(new_sections_merged):
            if section_index == 0:
                for substr_index, substr in enumerate(section.substrings):
                    if substr_index == 0:
                        continue
                    else:
                        substr.index = (
                            section.substrings[substr_index - 1].index
                            + section.substrings[substr_index - 1].length
                        )
            else:
                for substr_index, substr in enumerate(section.substrings):
                    if substr_index == 0:
                        substr.index = (
                            new_sections_merged[section_index - 1].substrings[-1].index
                            + new_sections_merged[section_index - 1]
                            .substrings[-1]
                            .length
                        )
                    else:
                        substr.index = (
                            section.substrings[substr_index - 1].index
                            + section.substrings[substr_index - 1].length
                        )
        # NOTE: 再次合并 sections 中的 substrings 里面的 text
        for section in new_sections_merged:
            section.substrings = self._merge_substrings_across_digit(section.substrings)
        if self.debug:
            logger.debug("---------------------------------after_merge_digit_sections:")
            for section in new_sections_merged:
                logger.debug(section)
        return new_sections_merged

    def _merge_substrings_across_punctuation(
        self,
        substrings: List[SubString],
    ) -> List[SubString]:
        new_substrings: List[SubString] = []
        last_lang = ""  # Changed from 'lang' to 'last_lang' for consistency

        for _, substring in enumerate(substrings):
            if new_substrings:
                if substring.lang == "punctuation":
                    # If the last substring is also a punctuation, merge them
                    new_substrings[-1].text += substring.text
                    new_substrings[-1].length += substring.length
                else:
                    if substring.lang == last_lang or last_lang == "":
                        new_substrings[-1].text += substring.text
                        new_substrings[-1].length += substring.length
                        new_substrings[-1].lang = (
                            substring.lang
                            if new_substrings[-1].lang == "punctuation"
                            else new_substrings[-1].lang
                        )
                    else:
                        new_substrings.append(substring)
            else:
                new_substrings.append(substring)
            last_lang = substring.lang

        return new_substrings

    # MARK: _merge_substrings_across_punctuation based on sections
    def _merge_substrings_across_punctuation_based_on_sections(
        self,
        sections: List[SubStringSection],
    ) -> List[SubStringSection]:
        new_sections: List[SubStringSection] = [sections[0]]
        # NOTE: 将 sections 中的 punctuation 合并到临近的非 punctuation 的 section
        for index, _ in enumerate(sections):
            if index == 0:
                continue
            # 检查当前 section 和前一个 section 是否可以合并
            if index >= len(sections):
                break

            current_section = sections[index]
            # 如果前一个 section 和当前的 section 类型不同，且其中一个是 punctuation，则合并
            one_of_section_is_punctuation = (
                new_sections[-1].lang_section_type == LangSectionType.PUNCTUATION
                or current_section.lang_section_type == LangSectionType.PUNCTUATION
            )
            if one_of_section_is_punctuation:
                # 如果当前 section 是 punctuation，且第一个元素不是 not_merge_punctuation，则合并

                if (
                    new_sections[-1].lang_section_type == LangSectionType.PUNCTUATION
                    and new_sections[-1].substrings[0].text
                    not in self.not_merge_punctuation
                ):
                    # 将前一个 punctuation section 和当前的 section 合并
                    new_sections[-1].text += current_section.text
                    new_sections[
                        -1
                    ].lang_section_type = current_section.lang_section_type
                    new_sections[-1].substrings[-1].text += current_section.substrings[
                        0
                    ].text
                    new_sections[-1].substrings[
                        -1
                    ].length += current_section.substrings[0].length
                    new_sections[-1].substrings[-1].lang = current_section.substrings[
                        0
                    ].lang
                    new_sections[-1].substrings.extend(current_section.substrings[1:])
                    for index, substr in enumerate(new_sections[-1].substrings):
                        if index == 0:
                            # 第一个元素是前一个 punctuation section 的最后一个元素，不需要修改
                            continue
                        else:
                            # 其他元素是当前 section 的元素，需要修改 index
                            substr.index = (
                                new_sections[-1].substrings[index - 1].index
                                + new_sections[-1].substrings[index - 1].length
                            )
                elif (
                    current_section.lang_section_type == LangSectionType.PUNCTUATION
                    and current_section.substrings[0].text
                    not in self.not_merge_punctuation
                ):
                    # 将当前的 punctuation section 和前一个 section 合并
                    new_sections[-1].text += current_section.text
                    new_sections[-1].substrings[-1].text += current_section.substrings[
                        0
                    ].text
                    new_sections[-1].substrings[
                        -1
                    ].length += current_section.substrings[0].length

                    new_sections[-1].substrings.extend(current_section.substrings[1:])
                    for index, substr in enumerate(new_sections[-1].substrings):
                        if index == 0:
                            continue
                        else:
                            substr.index = (
                                new_sections[-1].substrings[index - 1].index
                                + new_sections[-1].substrings[index - 1].length
                            )
                else:
                    new_sections.append(current_section)
            else:
                new_sections.append(current_section)

        # NOTE: 将相同类型的 section 合并
        new_sections_merged: List[SubStringSection] = [new_sections[0]]
        for index, _ in enumerate(new_sections):
            if index == 0:
                continue
            if (
                new_sections_merged[-1].lang_section_type
                == new_sections[index].lang_section_type
            ):
                new_sections_merged[-1].text += new_sections[index].text
                new_sections_merged[-1].substrings.extend(
                    new_sections[index].substrings
                )
            else:
                new_sections_merged.append(new_sections[index])
        # NOTE: 重新计算 index
        for section_index, section in enumerate(new_sections_merged):
            if section_index == 0:
                for substr_index, substr in enumerate(section.substrings):
                    if substr_index == 0:
                        continue
                    else:
                        substr.index = (
                            section.substrings[substr_index - 1].index
                            + section.substrings[substr_index - 1].length
                        )
            else:
                for substr_index, substr in enumerate(section.substrings):
                    if substr_index == 0:
                        substr.index = (
                            new_sections_merged[section_index - 1].substrings[-1].index
                            + new_sections_merged[section_index - 1]
                            .substrings[-1]
                            .length
                        )
                    else:
                        substr.index = (
                            section.substrings[substr_index - 1].index
                            + section.substrings[substr_index - 1].length
                        )
        # NOTE: 再次合并 sections 中的 substrings 里面的 text
        for section in new_sections_merged:
            section.substrings = self._merge_substrings_across_punctuation(
                section.substrings
            )
        if self.debug:
            logger.debug(
                "---------------------------------after_merge_punctuation_sections:"
            )
            for section in new_sections_merged:
                logger.debug(section)
        return new_sections_merged

    # MARK: _init_substr_lang
    def _init_substr_lang(
        self,
        texts: List[str],
        lang_section_type: LangSectionType,
        lang_map: Dict[str, str] = None,
    ) -> List[SubString]:
        substrings: List[SubString] = []
        substring_index = 0
        lang_map = self.lang_map if lang_map is None else lang_map
        if self.debug:
            logger.debug("---------lang_map:")
            logger.debug(lang_map)
        for text in texts:
            length = len(text)

            cur_lang = detect_lang_combined(text, lang_section_type=lang_section_type)
            cur_lang = lang_map.get(cur_lang, self.default_lang)
            temp_substr = SubString(
                lang=cur_lang,
                text=text,
                length=length,
                index=substring_index,
            )
            if self.debug:
                logger.debug(
                    f"---------lang_map: {lang_map}, temp_substr: {temp_substr}"
                )
            substrings.append(temp_substr)

            substring_index += length
        return substrings

    # MARK: _get_languages
    def _get_languages(
        self,
        lang_text_list: List[SubString],
        lang_section_type: LangSectionType,
        lang_map: Dict[str, str] = None,
    ):
        if lang_section_type in [
            LangSectionType.DIGIT,
            LangSectionType.KO,
            LangSectionType.PUNCTUATION,
        ]:
            return lang_text_list

        if lang_map is None:
            lang_map = self.lang_map

        for _, substr in enumerate(lang_text_list):
            cur_lang = detect_lang_combined(
                text=substr.text, lang_section_type=lang_section_type
            )
            cur_lang = lang_map.get(cur_lang, self.default_lang)

        return lang_text_list
