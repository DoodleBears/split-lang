from typing import List

from pydantic import BaseModel


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


class SubStringSection(BaseModel):
    text: str
    """original text of this section (combines all of the substrings)"""
    substrings: List[SubString]
    """substrings that splitted from `text`"""
    is_punctuation: bool = False
    """is `text` of this sections is punctuation"""
