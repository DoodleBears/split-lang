from split_lang import split_by_lang
from split_lang.split.utils import DEFAULT_THRESHOLD
from tests.data.test_data import texts_de_fr_en, texts_with_digit, texts_zh_jp_ko_en


def test_split_to_substring():
    for text in texts_zh_jp_ko_en:
        substr = split_by_lang(
            text=text,
            verbose=False,
            threshold=4.9e-5,
            # threshold=DEFAULT_THRESHOLD,
            # default_lang="en",
            merge_across_punctuation=True,
        )
        for index, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")

    for text in texts_de_fr_en:
        substr = split_by_lang(
            text=text,
            verbose=False,
            # lang_map=new_lang_map,
            threshold=DEFAULT_THRESHOLD,
            # default_lang="en",
        )
        for index, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")

    for text in texts_with_digit:
        substr = split_by_lang(
            text=text,
            verbose=False,
            threshold=4.9e-5,
            # merge_across_punctuation=False,
            merge_across_digit=False,
        )
        for index, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")

    for text in texts_with_digit:
        substr = split_by_lang(
            text=text,
            verbose=False,
            threshold=4.9e-5,
            merge_across_punctuation=True,
        )
        for index, item in enumerate(substr):
            print(item)
            # print(f"{index}|{item.lang}:{item.text}")
        print("----------------------")


def main():
    test_split_to_substring()


if __name__ == "__main__":
    main()
