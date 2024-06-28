# `langsplit`

splitting sentences by language (concatenating over-split substrings based on their language)

# Motivation
1. TTS (Text-To-Speech) model often fail on multi-language sentence, separate sentence based on language will bring better result
2. Existed NLP toolkit (e.g. SpaCy) is helpful for parsing text in one language, however when it comes to multi-language text like below is hard to deal with: 

```
你最近好吗、最近どうですか？요즘 어떻게 지내요？sky is clear and sunny。
```

# Usage

## Installation

You can install the package using pip:

```bash
pip install langsplit
```

```python
texts = [
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

for text in texts:
    substr_list = split(text, verbose=True)
    for index, substr in enumerate(substr_list):
        print(f"{substr.lang}|{index}: {substr.text}")
    print("----------------------")
```