from split_lang import LangSplitter

texts = [
    "你喜欢看アニメ吗？",
    "衬衫的价格是9.15便士",
]

lang_splitter = LangSplitter()


def test_split():
    for text in texts:
        pre_split_sections = lang_splitter.pre_split(
            text=text,
        )
        for section in pre_split_sections:
            print(section)

        split_sections = lang_splitter._split(
            pre_split_section=pre_split_sections,
        )
        for section in split_sections:
            print(section)


def main():
    test_split()
    pass


if __name__ == "__main__":
    main()
