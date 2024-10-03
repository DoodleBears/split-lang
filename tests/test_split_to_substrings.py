from split_lang import LangSplitter
from tests.data.test_data import (
    texts_de_fr_en,
    texts_with_digit,
    texts_with_newline,
    texts_zh_jp_ko_en,
)

lang_splitter = LangSplitter()


def test_split_to_substring():
    for text in texts_zh_jp_ko_en:
        substr = lang_splitter.split_by_lang(
            text=text,
        )
        for _, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")

    for text in texts_de_fr_en:
        substr = lang_splitter.split_by_lang(
            text=text,
        )
        for _, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")

    lang_splitter.merge_across_digit = False
    for text in texts_with_digit:
        substr = lang_splitter.split_by_lang(
            text=text,
        )
        for _, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")

    lang_splitter.merge_across_digit = True
    lang_splitter.merge_across_punctuation = True
    for text in texts_with_digit:
        substr = lang_splitter.split_by_lang(
            text=text,
        )
        for _, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")


def test_split_to_substring_newline():
    for text in texts_with_newline:
        substr = lang_splitter.split_by_lang(
            text=text,
        )
        for _, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")


def main():
    test_split_to_substring()
    test_split_to_substring_newline()


if __name__ == "__main__":
    main()
