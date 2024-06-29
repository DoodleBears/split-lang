# 1. `split-lang`

[![PyPI version](https://badge.fury.io/py/split-lang.svg)](https://badge.fury.io/py/split-lang)
[![wakatime](https://wakatime.com/badge/user/5728d95a-5cfb-4acb-b600-e34c2fc231b6/project/e06e0a00-9ba1-453d-8c62-a0b2604aaaad.svg)](https://wakatime.com/badge/user/5728d95a-5cfb-4acb-b600-e34c2fc231b6/project/e06e0a00-9ba1-453d-8c62-a0b2604aaaad)

splitting sentences by language (concatenating over-split substrings based on their language)

powered by [`wtpsplit`](https://github.com/segment-any-text/wtpsplit) and [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) and [`langdetect`](https://github.com/Mimino666/langdetect)

1. rule-based split using punctuation
   1. `hello, how are you` -> `hello` | `,` | `how are you`
2. then, over-split text to substrings by `wtpsplit`
   1. `你喜欢看アニメ吗` -> `你喜欢看` | `アニメ` | `吗`
3. concatenate substrings based on their languages using `fast-langdetect` and `langdetect`
   1. `我的名字是` | `西野` | `くまです` -> `我的名字是` | `西野くまです`

- [Example output of Chinese, Japanese, Korean, English](#3212-output)
- [Example output of French, German, English](#3222-output)
# 2. Motivation
1. TTS (Text-To-Speech) model often fails on multi-language sentence, separate sentence based on language will bring better result
2. Existed NLP toolkit (e.g. `SpaCy`) is helpful for parsing text in one language, however when it comes to multi-language texts like below are hard to deal with: 

```
你喜欢看アニメ吗？
```

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
    - [3.2.1. Basic](#321-basic)
    - [3.2.2. Chinese, Japanese, Korean, English (Simple Usage)](#322-chinese-japanese-korean-english-simple-usage)
      - [3.2.2.1. Code](#3221-code)
      - [3.2.2.2. Output](#3222-output)
    - [3.2.3. French, German, English (Advanced Usage)](#323-french-german-english-advanced-usage)
      - [3.2.3.1. Code](#3231-code)
      - [3.2.3.2. Output](#3232-output)
  - [3.3. usage of `lang_map` (for better result)](#33-usage-of-lang_map-for-better-result)


# 3. Usage

## 3.1. Installation

You can install the package using pip:

```bash
pip install split-lang
```

## 3.2. Sample Code

### 3.2.1. Basic

```python
from langsplit import split

texts = [
    "你喜欢看アニメ吗？",
]

for text in texts:
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
```

```
0: zh:你喜欢看|ja:アニメ|zh:吗|
1: ？
```

### 3.2.2. Chinese, Japanese, Korean, English (Simple Usage)
#### 3.2.2.1. Code
```python
from langsplit import split

texts = [
    "我是 VGroupChatBot，一个旨在支持多人通信的助手，通过可视化消息来帮助团队成员更好地交流。我可以帮助团队成员更好地整理和共享信息，特别是在讨论、会议和Brainstorming等情况下。你好我的名字是西野くまですmy name is bob很高兴认识你どうぞよろしくお願いいたします「こんにちは」是什么意思。",
    "你好，我的名字是西野くまです。I am from Tokyo, 日本の首都。今天的天气非常好，sky is clear and sunny。おはようございます、皆さん！我们一起来学习吧。Learning languages can be fun and exciting。昨日はとても忙しかったので、今日は少しリラックスしたいです。Let's take a break and enjoy some coffee。中文、日本語、and English are three distinct languages, each with its own unique charm。希望我们能一起进步，一起成长。Let's keep studying and improving our language skills together. ありがとう！",
    "你好，今日はどこへ行きますか？",
    "你好今日はどこへ行きますか？",
    "我的名字是田中さんです。",
    "我喜欢吃寿司和拉面おいしいです。",
    "今天の天気はとてもいいですね。",
    "我在学习日本語少し難しいです。",
    "日语真是おもしろい啊",
    "你喜欢看アニメ吗？",
    "我想去日本旅行、特に京都に行きたいです。",
    "昨天見た映画はとても感動的でした。我朋友是日本人彼はとても優しいです。",
    "我们一起去カラオケ吧、楽しそうです。",
    "我的家在北京、でも、仕事で東京に住んでいます。",
    "我在学做日本料理、日本料理を作るのを習っています。",
    "你会说几种语言、何ヶ国語話せますか？",
    "我昨天看了一本书、その本はとても面白かったです。",
    "你最近好吗、最近どうですか？",
    "我在学做日本料理와 한국 요리、日本料理を作るのを習っています。",
    "你会说几种语言、何ヶ国語話せますか？몇 개 언어를 할 수 있어요？",
    "我昨天看了一本书、その本はとても面白かったです。어제 책을 읽었는데, 정말 재미있었어요。",
    "我们一起去逛街와 쇼핑、買い物に行きましょう。쇼핑하러 가요。",
    "你最近好吗、最近どうですか？요즘 어떻게 지내요？",
]

for text in texts:
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
```
#### 3.2.2.2. Output
<details>
  <summary>Output</summary>

```
0: zh:我是 |
1: en:VGroupChatBot|
2: ，
3: zh:一个旨在支持多人通信的助手|
4: ，
5: zh:通过可视化消息来帮助团队成员更好地交流|
6: 。
7: zh:我可以帮助团队成员更好地整理和共享信息|
8: ，
9: zh:特别是在讨论|
10: 、
11: zh:会议和|
12: en:Brainstorming|
13: zh:等情况下|
14: 。
15: zh:你好我的名字是|ja:西野くまです|
16: en:my name is bob|
17: zh:很高兴认识你|ja:どうぞよろしくお願いいたします|
18: 「
19: ja:こんにちは|
20: 」
21: zh:是什么意思|
22: 。
----------------------
0: zh:你好|
1: ，
2: zh:我的名字是|ja:西野くまです|
3: 。
4: en:I am from Tokyo|
5: ,
6: ja:日本の首都|
7: 。
8: zh:今天的天气非常好|
9: ，
10: en:sky is clear and sunny|
11: 。
12: ja:おはようございます|
13: 、
14: ja:皆さん|
15: ！
16: zh:我们一起来学习吧|
17: 。
18: en:Learning languages can be fun and exciting|
19: 。
20: ja:昨日はとても忙しかったので|
21: 、
22: ja:今日は少しリラックスしたいです|
23: 。
24: en:Let's take a break and enjoy some coffee|
25: 。
26: zh:中文|
27: 、
28: ja:日本語|
29: 、
30: en:and English are three distinct languages|
31: ,
32: en:each with its own unique charm|
33: 。
34: zh:希望我们能一起进步|
35: ，
36: zh:一起成长|
37: 。
38: en:Let's keep studying and improving our language skills together|
39: .
40: ja:ありがとう|
41: ！
----------------------
0: zh:你好|
1: ，
2: ja:今日はどこへ行きますか|
3: ？
----------------------
0: zh:你好今|ja:日はどこへ行きますか|
1: ？
----------------------
0: zh:我的名字是|ja:田中さんです|
1: 。
----------------------
0: zh:我喜欢吃寿司和拉面|ja:おいしいです|
1: 。
----------------------
0: ja:今天の天気はとてもいいですね|
1: 。
----------------------
0: zh:我在学习|ja:日本語少し難しいです|
1: 。
----------------------
0: zh:日语真是|ja:おもしろい啊|
----------------------
0: zh:你喜欢看|ja:アニメ|zh:吗|
1: ？
----------------------
0: zh:我想去|ja:日本旅行|
1: 、
2: ja:特に京都に行きたいです|
3: 。
----------------------
0: ja:昨天見た映画はとても感動的でした|
1: 。
2: zh:我朋友是|ja:日本人彼はとても優しいです|
3: 。
----------------------
0: zh:我们一起去|ja:カラオケ吧|
1: 、
2: ja:楽しそうです|
3: 。
----------------------
0: zh:我的家在北京|
1: 、
2: ja:でも|
3: 、
4: ja:仕事で東京に住んでいます|
5: 。
----------------------
0: zh:我在学|ja:做日本料理|
1: 、
2: ja:日本料理を作るのを習っています|
3: 。
----------------------
0: zh:你会说几种语言|
1: 、
2: ja:何ヶ|zh:国語|ja:話せますか|
3: ？
----------------------
0: zh:我昨天看了一本书|
1: 、
2: ja:その本はとても面白かったです|
3: 。
----------------------
0: zh:你最近好吗|
1: 、
2: ja:最近どうですか|
3: ？
----------------------
0: zh:我在学|ko:做日本料理와 한국 요리|
1: 、
2: ja:日本料理を作るのを習っています|
3: 。
----------------------
0: zh:你会说几种语言|
1: 、
2: ja:何ヶ|zh:国語|ja:話せますか|
3: ？
4: ko:몇 개 언어를 할 수 있어요|
5: ？
----------------------
0: zh:我昨天看了一本书|
1: 、
2: ja:その本はとても面白かったです|
3: 。
4: ko:어제 책을 읽었는데|
5: ,
6: ko:정말 재미있었어요|
7: 。
----------------------
0: zh:我们一起去逛街|ko:와 쇼핑|
1: 、
2: ja:買い物に行きましょう|
3: 。
4: ko:쇼핑하러 가요|
5: 。
----------------------
0: zh:你最近好吗|
1: 、
2: ja:最近どうですか|
3: ？
4: ko:요즘 어떻게 지내요|
5: ？
----------------------
```
</details>

### 3.2.3. French, German, English (Advanced Usage)

> [!NOTE]
> `threshold`: if your text contains NO Chinese, Japanese and Korean, then `4.9e-4` is suggested, otherwise `4.9e-5`
> 
> `lang_map`: mapping different language to same language for better result, if you know the range of your target languages. Defaults to None. (see [3.3. usage of `lang_map` (for better result)](#33-usage-of-lang_map-for-better-result))

#### 3.2.3.1. Code
```python
from langsplit import split

texts = [
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
    "Ich liebe Paris c'est une belle ville and the food is amazing!",
    "Berlin ist wunderbar je veux y retourner and explore more.",
    "Bonjour wie geht's dir today?",
    "Die Musik hier ist fantastisch la musique est superbe and I enjoy it a lot.",
    "Guten Morgen je t'aime have a great day!",
    "Das Wetter ist heute schön il fait beau aujourd'hui and it's perfect for a walk.",
    "Ich mag dieses Buch ce livre est intéressant and it has a great story.",
    "Vielen Dank merci beaucoup for your help.",
    "Wir reisen nach Deutschland nous voyageons en Allemagne and we are excited.",
    "Ich bin müde je suis fatigué and I need some rest.",
]

for text in texts:
    substr_sections = split(
        text=text,
        verbose=False,
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
```
#### 3.2.3.2. Output

<details>
  <summary>Output</summary>

```
0: de:Ich liebe Paris|
1: ,
2: fr:c'est une belle ville|
3: ,
4: en:and the food is amazing|
5: !
----------------------
0: de:Berlin ist wunderbar|
1: ,
2: en:je |fr:veux |en:y |fr:retourner|
3: ,
4: en:and explore more|
5: .
----------------------
0: fr:Bonjour|
1: ,
2: de:wie geht's dir today|
3: ?
----------------------
0: de:Die Musik hier ist fantastisch|
1: ,
2: en:la |fr:musique est superbe|
3: ,
4: en:and I enjoy it a lot|
5: .
----------------------
0: de:Guten Morgen|
1: ,
2: fr:je t'aime|
3: ,
4: en:have a great day|
5: !
----------------------
0: de:Das Wetter ist heute schön|
1: ,
2: en:il |fr:fait beau aujourd'|en:hui|
3: ,
4: en:and it's perfect for a walk|
5: .
----------------------
0: de:Ich mag dieses Buch|
1: ,
2: fr:ce livre est intéressant|
3: ,
4: en:and it has a great story|
5: .
----------------------
0: de:Vielen |en:Dank|
1: ,
2: fr:merci beaucoup|
3: ,
4: en:for your help|
5: .
----------------------
0: de:Wir reisen nach Deutschland|
1: ,
2: fr:nous voyageons en Allemagne|
3: ,
4: en:and we are excited|
5: .
----------------------
0: de:Ich bin müde|
1: ,
2: en:je |fr:suis fatigué|
3: ,
4: en:and I need some rest|
5: .
----------------------
0: de:Ich liebe |fr:Paris c'est une belle ville and the food is amazing|
1: !
----------------------
0: de:Berlin ist wunderbar |fr:je veux y retourner and explore more|
1: .
----------------------
0: fr:Bonjour |de:wie geht's dir today|
1: ?
----------------------
0: de:Die Musik hier ist fantastisch |fr:la musique est superbe |en:and I enjoy it a lot|
1: .
----------------------
0: de:Guten |en:Morgen je t'aime have a great day|
1: !
----------------------
0: de:Das Wetter ist heute schön |fr:il fait beau aujourd'|en:hui and it's perfect for a walk|
1: .
----------------------
0: de:Ich mag dieses Buch |en:ce livre est intéressant and it has a great story|
1: .
----------------------
0: de:Vielen |fr:Dank merci beaucoup for your help|
1: .
----------------------
0: de:Wir reisen nach Deutschland |fr:nous voyageons en Allemagne |en:and we are excited|
1: .
----------------------
0: de:Ich bin müde |fr:je suis fatigué |en:and I need some rest|
1: .
----------------------
```
</details>

## 3.3. usage of `lang_map` (for better result)
- default `lang_map` looks like below
  - if `langdetect` or `fasttext` or any other language detector detect the language that is NOT included in `lang_map` will be set to `'x'`
  - every 'x' would be merge to the near substring
- default `default_lang` is `'en'`

```python
LANG_MAP = {
    "zh": "zh",
    "zh-cn": "zh",
    "zh-tw": "x",
    "ko": "ko",
    "ja": "ja",
    "de": "de",
    "fr": "fr",
    "en": "en",
}
DEFAULT_LANG = "en"
```
