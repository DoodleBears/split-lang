import json
import os
from pydantic import BaseModel
from typing import Dict, List, Optional

from wtpsplit import SaT, WtP

from langsplit import split
from langsplit.split.splitter import SentenceSplitter, SubString


class TestData(BaseModel):
    filename: str
    texts: List[str]
    threshold: float
    splitter: SentenceSplitter
    lang_map: Optional[Dict]
    default_lang: str

    class Config:
        arbitrary_types_allowed = True


texts_zh_jp_ko_en = [
    "我是 VGroupChatBot，一个旨在支持多人通信的助手，通过可视化消息来帮助团队成员更好地交流。我可以帮助团队成员更好地整理和共享信息，特别是在讨论、会议和Brainstorming等情况下。你好我的名字是西野くまですmy name is bob很高兴认识你どうぞよろしくお願いいたします「こんにちは」是什么意思。",
    "你好，我的名字是西野くまです。I am from Tokyo, 日本の首都。今天的天气非常好，sky is clear and sunny。おはようございます、皆さん！我们一起来学习吧。Learning languages can be fun and exciting。昨日はとても忙しかったので、今日は少しリラックスしたいです。Let's take a break and enjoy some coffee。中文、日本語、and English are three distinct languages, each with its own unique charm。希望我们能一起进步，一起成长。Let's keep studying and improving our language skills together. ありがとう！",
    "你好，今日はどこへ行きますか？",
    "我的名字是田中さんです。",
    "我喜欢吃寿司和拉面おいしいです。",
    "今天の天気はとてもいいですね。",
    "我在学习日本語少し難しいです。",
    "日语真是おもしろい啊",
    "你喜欢看アニメ吗？",
    "我想去日本旅行、特に京都に行きたいです。",
    "昨天見た映画はとても感動的でした。" "我朋友是日本人、彼はとても優しいです。",
    "我们一起去カラオケ吧、楽しそうです。",
    "你今天吃了什么、朝ごはんは何ですか？",
    "我的家在北京、でも、仕事で東京に住んでいます。",
    "我在学做日本料理、日本料理を作るのを習っています。",
    "你会说几种语言、何ヶ国語話せますか？",
    "我昨天看了一本书、その本はとても面白かったです。",
    "我们一起去逛街、買い物に行きましょう。",
    "你最近好吗、最近どうですか？",
    "我在学做日本料理와 한국 요리、日本料理を作るのを習っています。",
    "你会说几种语言、何ヶ国語話せますか？몇 개 언어를 할 수 있어요？",
    "我昨天看了一本书、その本はとても面白かったです。어제 책을 읽었는데, 정말 재미있었어요。",
    "我们一起去逛街와 쇼핑、買い物に行きましょう。쇼핑하러 가요。",
    "你最近好吗、最近どうですか？요즘 어떻게 지내요？",
]

texts_de_fr_en = [
    "Ich liebe Paris, c'est une belle ville, and the food is amazing!",
    "Berlin ist wunderbar, je veux y retourner, and explore more.",
    "Bonjour, wie geht's dir today?",
    "Die Musik hier ist fantastisch, la musique est superbe, and I enjoy it a lot.",
    "Guten Morgen, je t'aime, have a great day!",
    "Das Wetter ist heute schön, il fait beau aujourd'hui, and it's perfect for a walk.",
    "Ich mag dieses Buch, ce livre est intéressant, and it has a great story.",
    "Vielen Dank, merci beaucoup, for your help.",
    "Wir reisen nach Deutschland, nous voyageons en Allemagne, and we are excited.",
    "Ich bin müde, je suis fatigué, and I need some rest.",
]


def generate_json(data: TestData) -> List[Dict]:
    """
    Generate json for accuracy calculation
    """
    result: List[Dict] = []
    for text in data.texts:
        text_result = []
        substr_list = split(
            text=text,
            threshold=data.threshold,
            splitter=data.splitter,
            lang_map=data.lang_map,
            default_lang=data.default_lang,
            verbose=True,
        )
        for _, substr in enumerate(substr_list):
            text_result.append({"lang": substr.lang, "text": substr.text})
        result.append(text_result)

    return result


TEST_DATA_FOLDER = "tests/data"


def generate_test_data(test_data: TestData):
    # Create the tests/data directory if it doesn't exist
    os.makedirs(TEST_DATA_FOLDER, exist_ok=True)

    result = generate_json(test_data)
    with open(
        f"{TEST_DATA_FOLDER}/{test_data.filename}.json", "w", encoding="utf-8"
    ) as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


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


if __name__ == "__main__":
    main()
