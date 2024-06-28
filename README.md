# 1. `split-lang`

[![PyPI version](https://badge.fury.io/py/split-lang.svg)](https://badge.fury.io/py/split-lang)
[![wakatime](https://wakatime.com/badge/user/5728d95a-5cfb-4acb-b600-e34c2fc231b6/project/e06e0a00-9ba1-453d-8c62-a0b2604aaaad.svg)](https://wakatime.com/badge/user/5728d95a-5cfb-4acb-b600-e34c2fc231b6/project/e06e0a00-9ba1-453d-8c62-a0b2604aaaad)

splitting sentences by language (concatenating over-split substrings based on their language

# 2. Motivation
1. TTS (Text-To-Speech) model often fail on multi-language sentence, separate sentence based on language will bring better result
2. Existed NLP toolkit (e.g. SpaCy) is helpful for parsing text in one language, however when it comes to multi-language texts like below are hard to deal with: 

```
你最近好吗、最近どうですか？요즘 어떻게 지내요？sky is clear and sunny。
```
```
Vielen Dank, merci beaucoup, for your help.
```

- [1. `split-lang`](#1-split-lang)
- [2. Motivation](#2-motivation)
- [3. Usage](#3-usage)
  - [3.1. Installation](#31-installation)
  - [3.2. Sample Code](#32-sample-code)
    - [3.2.1. Chinese, Japanese, Korean, English (Simple Usage)](#321-chinese-japanese-korean-english-simple-usage)
      - [3.2.1.1. Code](#3211-code)
      - [3.2.1.2. Output](#3212-output)
    - [3.2.2. French, German, English (Advanced Usage)](#322-french-german-english-advanced-usage)
      - [3.2.2.1. Code](#3221-code)
      - [3.2.2.2. Output](#3222-output)
  - [3.3. `lang_map`](#33-lang_map)


# 3. Usage

## 3.1. Installation

You can install the package using pip:

```bash
pip install split-lang
```

## 3.2. Sample Code

### 3.2.1. Chinese, Japanese, Korean, English (Simple Usage)
#### 3.2.1.1. Code
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
    substr_list = split(text)
    for index, substr in enumerate(substr_list):
        print(f"{substr.lang}|{index}: {substr.text}")
    print("----------------------")
```
#### 3.2.1.2. Output
```
zh|0: 我是 
en|1: VGroupChatBot
zh|2: ，一个旨在支持多人通信的助手，通过可视化消息来帮助团队成员更好地交流。我可以帮助团队成员更好地整理和共享信息，特别是在讨论、会议和Brainstorming等情况下。你好我的名字是西野
ja|3: くまです
en|4: my name is bob
zh|5: 很高兴认识你
ja|6: どうぞよろしくお願いいたします「こんにちは」
zh|7: 是什么意思。
----------------------
zh|0: 你好，我的名字是西野
ja|1: くまです。
en|2: I am from Tokyo,
ja|3: 日本の首都
zh|4: 。今天的天气非常好，
en|5: sky is clear and sunny。
ja|6: おはようございます、皆さん！
zh|7: 我们一起来学习吧。
en|8: Learning languages can be fun and exciting。
ja|9: 昨日はとても忙しかったので、今日は少しリラックスしたいです。
en|10: Let's take a break and enjoy some coffee。
zh|11: 中文、
ja|12: 日本語、
en|13: and English are three distinct languages, each with its own unique charm。
zh|14: 希望我们能一起进步，一起成长。
en|15: Let's keep studying and improving our language skills together.
ja|16: ありがとう！
----------------------
zh|0: 你好，今
ja|1: 日はどこへ行きますか？
----------------------
zh|0: 我的名字是
ja|1: 田中さんです。
----------------------
zh|0: 我喜欢吃寿司和拉面
ja|1: おいしいです。
----------------------
ja|0: 今天の天気はとてもいいですね。
----------------------
zh|0: 我在学习
ja|1: 日本語少し難しいです。
----------------------
zh|0: 日语真是
ja|1: おもしろい啊
----------------------
zh|0: 你喜欢看
ja|1: アニメ
zh|2: 吗？
----------------------
zh|0: 我想去日本
ja|1: 旅行、特に京都に行きたいです。
----------------------
ja|0: 昨天見た映画はとても感動的でした。
zh|1: 我朋友是日本人、
ja|2: 彼はとても優しいです。
----------------------
zh|0: 我们一起去
ja|1: カラオケ吧、楽しそうです。
----------------------
zh|0: 你今天吃了什么、
ja|1: 朝ごはんは何ですか？
----------------------
zh|0: 我的家在北京、
ja|1: でも、仕事で東京に住んでいます。
----------------------
zh|0: 我在学做日本料理、
ja|1: 日本料理を作るのを習っています。
----------------------
zh|0: 你会说几种语言、
ja|1: 何ヶ国語話せますか？
----------------------
zh|0: 我昨天看了一本书、
ja|1: その本はとても面白かったです。
----------------------
zh|0: 我们一起去逛街、
ja|1: 買い物に行きましょう。
----------------------
zh|0: 你最近好吗、最近
ja|1: どうですか？
----------------------
zh|0: 我在学做日本料理
ko|1: 와 한국 요리
ja|2: 、日本料理を作るのを習っています。
----------------------
zh|0: 你会说几种语言、
ja|1: 何ヶ国語話せますか？
ko|2: 몇 개 언어를 할 수 있어요？
----------------------
zh|0: 我昨天看了一本书、
ja|1: その本はとても面白かったです。
ko|2: 어제 책을 읽었는데, 정말 재미있었어요。
----------------------
zh|0: 我们一起去逛街
ko|1: 와 쇼핑
zh|2: 、
ja|3: 買い物に行きましょう。
ko|4: 쇼핑하러 가요。
----------------------
zh|0: 你最近好吗、最近
ja|1: どうですか？
ko|2: 요즘 어떻게 지내요？
----------------------
```

### 3.2.2. French, German, English (Advanced Usage)
#### 3.2.2.1. Code
```python

texts_2 = [
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


for text in texts_2:
    substr_list = split(text=text, verbose=False, lang_map=new_lang_map, threshold=1e-3)
    # `threshold`: if your text contains no Chinese, Japanese, Korean, `threshold=1e-3` is suggested
    # `lang_nap`: mapping different language to same language for better result, if you know the range of your target languages. Defaults to None.
    for index, substr in enumerate(substr_list):
        print(f"{substr.lang}|{index}: {substr.text}")
    print("----------------------")
```
#### 3.2.2.2. Output
```
de|0: Ich liebe 
en|1: Paris,
fr|2: c'est une belle ville,
en|3: and the food is amazing!
----------------------
de|0: Berlin ist wunderbar, 
fr|1: je veux y retourner,
en|2: and explore more.
----------------------
fr|0: Bonjour,
de|1: wie geht's dir today?
----------------------
de|0: Die Musik hier ist fantastisch, 
fr|1: la musique est superbe,
en|2: and I enjoy it a lot.
----------------------
de|0: Guten Morgen, 
fr|1: je t'aime,
en|2: have a great day!
----------------------
de|0: Das Wetter ist heute schön, 
fr|1: il fait beau aujourd'hui,
en|2: and it's perfect for a walk.
----------------------
de|0: Ich mag dieses Buch, 
fr|1: ce livre est intéressant,
en|2: and it has a great story.
----------------------
de|0: Vielen Dank, 
fr|1: merci beaucoup,
en|2: for your help.
----------------------
de|0: Wir reisen nach Deutschland, 
fr|1: nous voyageons en Allemagne,
en|2: and we are excited.
----------------------
de|0: Ich bin müde, 
fr|1: je suis fatigué,
en|2: and I need some rest.
----------------------
```

## 3.3. `lang_map`
- default `lang_map` looks like below
  - if `langdetect` or `fasttext` or any other language detector detect the language that is NOT included in `lang_map` will be set to `'x'`
  - every 'x' would be merge to the near substring

> [!NOTE]
> if you include `key:value` (e.g. `'x':"en"`), then `'x'` will be set to `'en'` and merge will based on language

```python
lang_map = {
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
```
