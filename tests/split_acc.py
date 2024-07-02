from typing import List

from split_lang import split_by_lang
from split_lang.split.splitter import SubString, TextSplitter, _get_languages
from split_lang.split.utils import PUNCTUATION, DEFAULT_THRESHOLD
from tests.test_config import TEST_DATA_FOLDER
from wtpsplit import SaT, WtP

import time

new_lang_map = {
    "zh": "zh",
    "zh-cn": "zh",
    "zh-tw": "x",
    "ko": "ko",
    "ja": "ja",
}


def get_corrected_split_result(text_file_path: str) -> List[List[SubString]]:
    """
    # 1. split by `|`
    # 2. convert to SubString, concat to list
    """
    corrected_split_result: List[List[SubString]] = []

    with open(text_file_path, "r", encoding="utf-8") as file:
        for line in file:
            substrings = line.strip().split("|")
            # print(substrings)

            substring_objects: List[SubString] = []

            current_index = 0

            for substring in substrings:
                is_punctuation = substring.strip() in PUNCTUATION
                substring_objects.append(
                    SubString(
                        lang="punctuation" if is_punctuation else "x",
                        text=substring,
                        index=current_index,
                        length=len(substring),
                        is_punctuation=is_punctuation,
                    )
                )

                current_index += len(substring)
            substring_objects = _get_languages(
                lang_text_list=substring_objects,
                lang_map=new_lang_map,
                default_lang="en",
            )
            corrected_split_result.append(substring_objects)

    return corrected_split_result


# splitter = TextSplitter()
sat = SaT("sat-1l-sm")
sat.half().to("cuda")
wtp = WtP("wtp-bert-tiny")
# wtp.half().to("cuda")
splitter = TextSplitter(wtp_split_model=wtp)


def simple_test(threshold: float = DEFAULT_THRESHOLD, verbose: bool = False):
    zh_jp_ko_en_lang_map = {
        "zh": "zh",
        "zh-cn": "zh",
        "zh-tw": "x",
        "ko": "ko",
        "ja": "ja",
    }

    text_file_name = "correct_split.txt"
    correct_split = get_corrected_split_result(
        text_file_path=f"{TEST_DATA_FOLDER}/{text_file_name}"
    )
    correct_total_substring_len = 0
    test_total_substring_len = 0
    correct_split_num = 0

    original_strings = []
    test_split: List[List[SubString]] = []
    time_1 = time.time()
    # MARK: collect original_strings from .txt and test `split()`
    for correct_substrings in correct_split:
        current_correct_num = 0
        correct_total_substring_len += len(correct_substrings)
        substrings_text = []
        for correct_substring in correct_substrings:
            substrings_text.append(correct_substring.text)
        original_string = "".join(substrings_text)
        original_strings.append(original_string)
        # print(original_string)

        test_split_substrings = split_by_lang(
            text=original_string,
            lang_map=zh_jp_ko_en_lang_map,
            default_lang="en",
            splitter=splitter,
            threshold=threshold,
        )
        test_split.append(test_split_substrings)
        test_total_substring_len += len(test_split_substrings)
        correct_substrings_text = [
            f"{item.index}|{item.text}" for item in correct_substrings
        ]
        test_split_substrings_text = [
            f"{item.index}|{item.text}" for item in test_split_substrings
        ]

        for test_substring in test_split_substrings:
            for correct_substring in correct_substrings:
                if (
                    test_substring.text == correct_substring.text
                    and test_substring.index == correct_substring.index
                ):
                    correct_split_num += 1
                    current_correct_num += 1
                    break
        if verbose:
            print(f"correct_substrings   : {correct_substrings_text}")
            print(f"test_split_substrings: {test_split_substrings_text}")
            print(
                f"acc                  : {current_correct_num}/{len(correct_substrings_text)}"
            )
            print("--------------------------")

    time_2 = time.time()
    precision = correct_split_num / correct_total_substring_len
    recall = correct_split_num / test_total_substring_len
    f1_score = 2 * precision * recall / (precision + recall)
    if verbose:
        print(f"total substring num: {correct_total_substring_len}")
        print(f"test total substring num: {test_total_substring_len}")
        print(f"text acc num: {correct_split_num}")
        print(f"precision: {precision}")
        print(f"recall: {recall}")
        print(f"F1 Score: {f1_score}")
        print(f"time: {time_2-time_1}")
    return f1_score


def find_best_threshold():
    best_f1_score = 0
    best_threshold = 0
    for times in range(2, 6):
        for i in range(1, 10):
            threshold = i / (10**times)
            # Call your function to test the threshold and get the F1 score
            f1_score = simple_test(threshold=threshold, verbose=False)
            if f1_score > best_f1_score:
                best_f1_score = f1_score
                best_threshold = threshold
                print(f"updated: best_f1_score: {best_f1_score}")
                print(f"updated: best_threshold: {best_threshold}")
                print("------")

    print(f"best_f1_score: {best_f1_score}")
    print(f"best_threshold: {best_threshold}")


def main():
    # find_best_threshold()
    simple_test(verbose=True)


if __name__ == "__main__":
    main()
