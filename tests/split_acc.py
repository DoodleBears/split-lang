import time
from typing import List

from split_lang.config import DEFAULT_LANG
from split_lang.model import LangSectionType
from split_lang.split.splitter import (
    SubString,
    LangSplitter,
)
from split_lang.split.utils import PUNCTUATION
from tests.test_config import TEST_DATA_FOLDER


def get_corrected_split_result(
    splitter: LangSplitter, text_file_path: str
) -> List[List[SubString]]:
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
                is_digit = substring.strip().isdigit()
                lang = DEFAULT_LANG
                if is_punctuation:
                    lang = "punctuation"
                elif is_digit:
                    lang = "digit"

                substring_objects.append(
                    SubString(
                        lang=lang,
                        text=substring,
                        index=current_index,
                        length=len(substring),
                        is_punctuation=is_punctuation,
                        is_digit=is_digit,
                    )
                )

                current_index += len(substring)
            substring_objects = splitter._get_languages(
                lang_text_list=substring_objects,
                lang_section_type=LangSectionType.ALL,
            )
            corrected_split_result.append(substring_objects)

    return corrected_split_result


def simple_test(splitter: LangSplitter, debug: bool = False):

    text_file_name = "correct_split_merge_punc.txt"
    correct_split = get_corrected_split_result(
        splitter=splitter, text_file_path=f"{TEST_DATA_FOLDER}/{text_file_name}"
    )
    correct_total_substring_len = 0
    test_total_substring_len = 0
    correct_split_num = 0

    original_strings = []
    test_split: List[List[SubString]] = []
    original_strings.clear()
    test_split.clear()
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

        test_split_substrings = splitter.split_by_lang(
            text=original_string,
        )
        test_split.append(test_split_substrings)
        test_total_substring_len += len(test_split_substrings)
        correct_substrings_text = [
            f"{item.lang}|{item.text}" for item in correct_substrings
        ]
        test_split_substrings_text = [
            f"{item.lang}|{item.text}" for item in test_split_substrings
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
        if debug:
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
    if debug:
        print(f"total substring num: {correct_total_substring_len}")
        print(f"test total substring num: {test_total_substring_len}")
        print(f"text acc num: {correct_split_num}")
        print(f"precision: {precision}")
        print(f"recall: {recall}")
        print(f"F1 Score: {f1_score}")
        print(f"time: {time_2-time_1}")

    return precision


def find_best_threshold(splitter: LangSplitter):
    best_score = 0
    best_threshold = 0
    for times in range(5):
        for i in range(1, 10):
            zeros = "0" * times
            threshold = float(f"0.{zeros}{str(i)}")
            score = simple_test(splitter=splitter, debug=False)
            if score > best_score:
                best_score = score
                best_threshold = threshold
                print(f"updated: best_f1_score: {best_score}")
                print(f"updated: best_threshold: {best_threshold}")
                print("------")

    print(f"best_score: {best_score}")
    print(f"best_threshold: {best_threshold}")


def main():
    splitter = LangSplitter(merge_across_punctuation=True)
    # find_best_threshold(splitter=splitter)
    simple_test(splitter=splitter, debug=True)


if __name__ == "__main__":
    main()
