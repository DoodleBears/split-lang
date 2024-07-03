from split_lang import split
from split_lang.split.model import LangSectionType
from tests.data.generate_test_json import texts_de_fr_en, texts_zh_jp_ko_en


texts = [
    "你喜欢看アニメ吗？",
    "衬衫的价格是9.15便士",
]


def test_split():
    for text in texts:
        substr_sections = split(
            text=text,
            verbose=True,
        )
        for index, section in enumerate(substr_sections):
            print(f"{index}:{section.text}")
            if section.lang_section_type is LangSectionType.PUNCTUATION:
                print(f"\t|——punctuation:{section.text}")
                continue
            for _, substr in enumerate(section.substrings):
                print(f"\t|——{substr.lang}:{substr.text}")
        print("----------------------")

    # for text in texts_de_fr_en:
    #     substr_sections = split(
    #         text=text,
    #         verbose=True,
    #         # lang_map=new_lang_map,
    #         threshold=4.9e-4,
    #         default_lang="en",
    #     )
    #     for index, section in enumerate(substr_sections):
    #         print(f"{index}:{section.text}")
    #         if section.is_punctuation:
    #             print(f"\t|——punctuation:{section.text}")
    #             continue
    #         for _, substr in enumerate(section.substrings):
    #             print(f"\t|——{substr.lang}:{substr.text}")
    #     print("----------------------")


def main():
    test_split()
    pass


if __name__ == "__main__":
    main()
