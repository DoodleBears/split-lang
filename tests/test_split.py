from langsplit import split
from tests.data.generate_test_json import texts_de_fr_en, texts_zh_jp_ko_en


new_lang_map = {
    "zh": "zh",
    "zh-cn": "zh",
    "zh-tw": "x",
    "ko": "ko",
    "ja": "ja",
}

for text in texts_zh_jp_ko_en:
    substr_sections = split(
        text=text,
        verbose=False,
        lang_map=new_lang_map,
        threshold=4.9e-5,
        default_lang="en",
    )
    for index, section in enumerate(substr_sections):
        print(f"{index}: ", end="")
        if section.is_punctuation:
            print(f"{section.text}")
            continue
        for substr in section.substrings:
            print(f"{substr.lang}:{substr.text}", end="|")
        print()
    print("----------------------")

for text in texts_de_fr_en:
    substr_sections = split(
        text=text,
        verbose=False,
        # lang_map=new_lang_map,
        threshold=4.9e-4,
        default_lang="en",
    )
    for index, section in enumerate(substr_sections):
        print(f"{index}: ", end="")
        if section.is_punctuation:
            print(f"{section.text}")
            continue
        for substr in section.substrings:
            print(f"{substr.lang}:{substr.text}", end="|")
        print()
    print("----------------------")

# for text in texts_de_fr_en:
#     substr_list = split(text=text, verbose=False, lang_map=new_lang_map, threshold=1e-3)
#     for index, substr in enumerate(substr_list):
#         print(f"{substr.lang}|{index}: {substr.text}")
#     print("----------------------")
