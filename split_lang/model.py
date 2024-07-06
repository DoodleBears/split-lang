from enum import Enum
from typing import List

from pydantic import BaseModel


class LangSectionType(Enum):
    ZH_JA = "zh_ja"
    KO = "ko"
    PUNCTUATION = "punctuation"
    DIGIT = "digit"
    OTHERS = "others"
    ALL = "all"


class SubString(BaseModel):
    lang: str
    """language of `text`"""
    text: str
    """text of substring"""
    index: int
    """index of `text` of original string"""
    length: int
    """length of `text`"""
    is_punctuation: bool
    """if `text` is punctuation"""
    is_digit: bool
    """if `text` is punctuation"""


class SubStringSection(BaseModel):
    lang_section_type: LangSectionType
    """
    Used for deal with different type of languages
    1. Chinese and Japanese both have characters will be processed together
    """
    text: str
    """original text of this section (combines all of the substrings)"""
    substrings: List[SubString]
    """substrings that splitted from `text`"""
