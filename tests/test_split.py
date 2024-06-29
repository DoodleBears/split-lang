from langsplit import split
from tests.generate_test_json import texts_de_fr_en, texts_zh_jp_ko_en


new_lang_map = {
    "zh": "zh",
    "zh-cn": "zh",
    "zh-tw": "x",
    "ko": "ko",
    "ja": "ja",
    "de": "de",
    "fr": "fr",
    "en": "en",
    "x": "en",
}

for text in texts_zh_jp_ko_en:
    substr_list = split(text=text, verbose=False, lang_map=new_lang_map, threshold=5e-5)
    for index, substr in enumerate(substr_list):
        print(f"{substr.lang}|{index}: {substr.text}")
    print("----------------------")

for text in texts_de_fr_en:
    substr_list = split(text=text, verbose=False, lang_map=new_lang_map, threshold=1e-3)
    for index, substr in enumerate(substr_list):
        print(f"{substr.lang}|{index}: {substr.text}")
    print("----------------------")
