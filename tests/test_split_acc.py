import json
import os
from typing import Dict, List

from langsplit import split
from langsplit.split.splitter import SentenceSplitter, SubString

from tests.data.test_data import TestData, texts_zh_jp_ko_en, texts_de_fr_en
from tests.test_config import TEST_DATA_FOLDER


def verify_split(data: TestData, json_file: str) -> bool:
    """
    Verify the split of the text against the expected JSON output.
    """
    referred_data: List[List[SubString]] = []
    with open(json_file, "r", encoding="utf-8") as f:
        texts_result = json.load(f)
        for text in texts_result:
            substr_list: List[SubString] = []
            for substr in text:
                substr_obj = SubString(**substr)
                substr_list.append(substr_obj)
            referred_data.append(substr_list)

    test_data: List[List[SubString]] = []
    for text in data.texts:
        substr_list = split(
            text=text,
            verbose=False,
            lang_map=data.lang_map,
            threshold=data.threshold,
            default_lang=data.default_lang,
            splitter=data.splitter,
        )
        test_data.append(substr_list)

    calculate_test_result(test_data=test_data, referred_data=referred_data)


# MARK: calculate test result
def calculate_test_result(
    test_data: List[List[SubString]], referred_data: List[List[SubString]]
):
    referred_substr_len = 0
    test_substr_len = 0
    acc_num = 0

    for index, _test in enumerate(test_data):
        test_substr_len += len(_test)
        _referred = referred_data[index]
        referred_substr_len += len(_referred)
        for _test_substring in _test:
            if _test_substring in _referred:
                acc_num += 1
    print(f"test_substr_len: {test_substr_len}")
    print(f"referred_substr_len: {referred_substr_len}")
    print(f"acc_num: {acc_num}")
    acc_percentage = acc_num / test_substr_len
    print(f"acc_percentage: {acc_percentage}")


def main():
    zh_jp_ko_en_lang_map = {
        "zh": "zh",
        "zh-cn": "zh",
        "zh-tw": "x",
        "ko": "ko",
        "ja": "ja",
    }
    data = TestData(
        filename="zh_jp_ko_en",
        texts=texts_zh_jp_ko_en,
        threshold=5e-5,
        splitter=SentenceSplitter(),
        lang_map=zh_jp_ko_en_lang_map,
        default_lang="en",
    )

    verify_split(data=data, json_file=f"{TEST_DATA_FOLDER}/{data.filename}.json")

    data = TestData(
        filename="de_fr_en",
        texts=texts_de_fr_en,
        threshold=1e-3,
        splitter=SentenceSplitter(),
        lang_map=None,
        default_lang="x",
    )

    verify_split(data=data, json_file=f"{TEST_DATA_FOLDER}/{data.filename}.json")

    return
    pass


if __name__ == "__main__":
    main()
