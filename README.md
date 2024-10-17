<div align="center">

<img alt="VisActor Logo" width=50% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-logo.svg"/>

<img alt="VisActor Logo" width=70% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-banner.svg"/>
  
</div>
<div align="center">
  <h1>split-lang</h1>

**English** | [**中文简体**](./docs/zh/README.md) | [**日本語**](./docs/ja/README.md)

Split text by languages through concatenating over split substrings based on their language, powered by

splitting: [`budoux`](https://github.com/google/budoux) and rule-base splitting

language detection: [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) and [`wordfreq`](https://github.com/rspeer/wordfreq)

</div>

<br/>

<div align="center">

[![PyPI version](https://badge.fury.io/py/split-lang.svg)](https://badge.fury.io/py/split-lang)
[![Downloads](https://static.pepy.tech/badge/split-lang)](https://pepy.tech/project/split-lang)
[![Downloads](https://static.pepy.tech/badge/split-lang/month)](https://pepy.tech/project/split-lang)


[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DoodleBears/split-lang/blob/main/split-lang-demo.ipynb)


[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/DoodleBears/split-lang/blob/main/LICENSE)
![GitHub Repo stars](https://img.shields.io/github/stars/DoodleBears/split-lang)
[![wakatime](https://wakatime.com/badge/user/5728d95a-5cfb-4acb-b600-e34c2fc231b6/project/e06e0a00-9ba1-453d-8c62-a0b2604aaaad.svg)](https://wakatime.com/badge/user/5728d95a-5cfb-4acb-b600-e34c2fc231b6/project/e06e0a00-9ba1-453d-8c62-a0b2604aaaad)

</div>




# 1. 💡How it works

**Stage 1**: rule-based split (separate character, punctuation and digit)
- `hello, how are you` -> `hello` | `,` | `how are you`

**Stage 2**: over-split text to substrings by [`budoux`](https://github.com/google/budoux) for Chinese mix with Japanese, ` ` (space) for **not** [scripta continua](https://en.wikipedia.org/wiki/Scriptio_continua)
- `你喜欢看アニメ吗` -> `你` | `喜欢` | `看` | `アニメ` | `吗`
- `昨天見た映画はとても感動的でした` -> `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した`
- `how are you` -> `how ` | `are ` | `you`

**Stage 3**: concatenate substrings based on their languages using [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect), [`wordfreq`](https://github.com/rspeer/wordfreq) and regex (rule-based)
- `你` | `喜欢` | `看` | `アニメ` | `吗` -> `你喜欢看` | `アニメ` | `吗`
- `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した` -> `昨天` | `見た映画はとても感動的でした`
- `how ` | `are ` | `you` -> `how are you`

<details>
  <summary>More split examples</summary>
  
  ```python
  correct_substrings   : ['x|我是 ', 'x|VGroupChatBot', 'punctuation|，', 'x|一个旨在支持多人通信的助手', 'punctuation|，', 'x|通过可视化消息来帮助团队成员更好地交流', 'punctuation|。', 'x|我可以帮助团队成员更好地整理和共享信息', 'punctuation|，', 'x|特别是在讨论', 'punctuation|、', 'x|会议和', 'x|Brainstorming', 'x|等情况下', 'punctuation|。', 'x|你好我的名字是', 'x|西野くまです', 'x|my name is bob', 'x|很高兴认识你', 'x|どうぞよろしくお願いいたします', 'punctuation|「', 'x|こんにちは', 'punctuation|」', 'x|是什么意思', 'punctuation|。']
test_split_substrings: ['zh|我是 ', 'en|VGroupChatBot', 'punctuation|，', 'zh|一个旨在支持多人通信的助手', 'punctuation|，', 'zh|通过可视化消息来帮助团队成员更好地交流', 'punctuation|。', 'zh|我可以帮助团队成员更好地整理和共享信息', 'punctuation|，', 'zh|特别是在讨论', 'punctuation|、', 'zh|会议和', 'en|Brainstorming', 'zh|等情况下', 'punctuation|。', 'zh|你好我的名字是', 'ja|西野くまです', 'en|my name is bob', 'zh|很高兴认识你', 'ja|どうぞよろしくお願いいたします', 'punctuation|「', 'ja|こんにち は', 'punctuation|」', 'zh|是什么意思', 'punctuation|。']
acc                  : 25/25
--------------------------
correct_substrings   : ['x|我的名字是', 'x|西野くまです', 'punctuation|。', 'x|I am from Tokyo', 'punctuation|, ', 'x|日本の首都', 'punctuation|。', 'x|今天的天气非常好']
test_split_substrings: ['zh|我的名字是', 'ja|西野くまです', 'punctuation|。', 'en|I am from Tokyo', 'punctuation|, ', 'ja|日本の首都', 'punctuation|。', 'zh|今天的天气非常好']
acc                  : 8/8
--------------------------
correct_substrings   : ['x|你好', 'punctuation|，', 'x|今日はどこへ行きますか', 'punctuation|？']
test_split_substrings: ['zh|你好', 'punctuation|，', 'ja|今日はどこへ行きますか', 'punctuation|？']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|你好', 'x|今日はどこへ行きますか', 'punctuation|？']
test_split_substrings: ['zh|你好', 'ja|今日はどこへ行きますか', 'punctuation|？']
acc                  : 3/3
--------------------------
correct_substrings   : ['x|我的名字是', 'x|田中さんです', 'punctuation|。']
test_split_substrings: ['zh|我的名字是田中', 'ja|さんです', 'punctuation|。']
acc                  : 1/3
--------------------------
correct_substrings   : ['x|我喜欢吃寿司和拉面', 'x|おいしいです', 'punctuation|。']
test_split_substrings: ['zh|我喜欢吃寿司和拉面', 'ja|おいしいです', 'punctuation|。']
acc                  : 3/3
--------------------------
correct_substrings   : ['x|今天', 'x|の天気はとてもいいですね', 'punctuation|。']
test_split_substrings: ['zh|今天', 'ja|の天気はとてもいいですね', 'punctuation|。']
acc                  : 3/3
--------------------------
correct_substrings   : ['x|我在学习', 'x|日本語少し難しいです', 'punctuation|。']
test_split_substrings: ['zh|我在学习日本語少', 'ja|し難しいです', 'punctuation|。']
acc                  : 1/3
--------------------------
correct_substrings   : ['x|日语真是', 'x|おもしろい', 'x|啊']
test_split_substrings: ['zh|日语真是', 'ja|おもしろい', 'zh|啊']
acc                  : 3/3
--------------------------
correct_substrings   : ['x|你喜欢看', 'x|アニメ', 'x|吗', 'punctuation|？']
test_split_substrings: ['zh|你喜欢看', 'ja|アニメ', 'zh|吗', 'punctuation|？']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|我想去日本旅行', 'punctuation|、', 'x|特に京都に行きたいです', 'punctuation|。']
test_split_substrings: ['zh|我想去日本旅行', 'punctuation|、', 'ja|特に京都に行きたいです', 'punctuation|。']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|昨天', 'x|見た映画はとても感動的でした', 'punctuation|。', 'x|我朋友是日本人', 'x|彼はとても優しいです', 'punctuation|。']
test_split_substrings: ['zh|昨天', 'ja|見た映画はとても感動的でした', 'punctuation|。', 'zh|我朋友是日本人', 'ja|彼はとても優しいです', 'punctuation|。']
acc                  : 6/6
--------------------------
correct_substrings   : ['x|我们一起去', 'x|カラオケ', 'x|吧', 'punctuation|、', 'x|楽しそうです', 'punctuation|。']
test_split_substrings: ['zh|我们一起去', 'ja|カラオケ', 'zh|吧', 'punctuation|、', 'ja|楽しそうです', 'punctuation|。']
acc                  : 6/6
--------------------------
correct_substrings   : ['x|我的家在北京', 'punctuation|、', 'x|でも', 'punctuation|、', 'x|仕事で東京に住んでいます', 'punctuation|。']
test_split_substrings: ['ja|我的家在北京', 'punctuation|、', 'ja|でも', 'punctuation|、', 'ja|仕事で東京に住んでいます', 'punctuation|。']
acc                  : 6/6
--------------------------
correct_substrings   : ['x|我在学做日本料理', 'punctuation|、', 'x|日本料理を作るのを習っています', 'punctuation|。']
test_split_substrings: ['ja|我在学做日本料理', 'punctuation|、', 'ja|日本料理を作るのを習っています', 'punctuation|。']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|你会说几种语言', 'punctuation|、', 'x|何ヶ国語話せますか', 'punctuation|？']
test_split_substrings: ['zh|你会说几种语言', 'punctuation|、', 'ja|何ヶ国語話せますか', 'punctuation|？']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|我昨天看了一本书', 'punctuation|、', 'x|その本はとても面白かったです', 'punctuation|。']
test_split_substrings: ['zh|我昨天看了一本书', 'punctuation|、', 'ja|その本はとても面白かったです', 'punctuation|。']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|你最近好吗', 'punctuation|、', 'x|最近どうですか', 'punctuation|？']
test_split_substrings: ['zh|你最近好吗', 'punctuation|、', 'ja|最近どうですか', 'punctuation|？']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|你最近好吗', 'x|最近どうですか', 'punctuation|？']
test_split_substrings: ['zh|你最近好吗最近', 'ja|どうですか', 'punctuation|？']
acc                  : 1/3
--------------------------
correct_substrings   : ['x|我在学做日本料理', 'x|와 한국 요리', 'punctuation|、', 'x|日本料理を作るのを習っています', 'punctuation|。']
test_split_substrings: ['ja|我在学做日本料理', 'ko|와 한국 요리', 'punctuation|、', 'ja|日本料理を作るのを習っています', 'punctuation|。']
acc                  : 5/5
--------------------------
correct_substrings   : ['x|你会说几种语言', 'punctuation|、', 'x|何ヶ国語話せますか', 'punctuation|？', 'x|몇 개 언어를 할 수 있어요', 'punctuation|？']
test_split_substrings: ['zh|你会说几种语言', 'punctuation|、', 'ja|何ヶ国語話せますか', 'punctuation|？', 'ko|몇 개 언어를 할 수 있어요', 'punctuation|？']
acc                  : 6/6
--------------------------
correct_substrings   : ['x|我昨天看了一本书', 'punctuation|、', 'x|その本はとても面白かったです', 'punctuation|。', 'x|어제 책을 읽었는데', 'punctuation|, ', 'x|정말 재미있었어요', 'punctuation|。']
test_split_substrings: ['zh|我昨天看了一本书', 'punctuation|、', 'ja|その本はとても面白かったです', 'punctuation|。', 'ko|어제 책을 읽었는데', 'punctuation|, ', 'ko|정말 재미있었어요', 'punctuation|。']
acc                  : 8/8
--------------------------
correct_substrings   : ['x|我们一起去逛街', 'x|와 쇼핑', 'punctuation|、', 'x|買い物に行きましょう', 'punctuation|。', 'x|쇼핑하러 가요', 'punctuation|。']
test_split_substrings: ['zh|我们一起去逛街', 'ko|와 쇼핑', 'punctuation|、', 'ja|買い物に行きましょう', 'punctuation|。', 'ko|쇼핑하러 가요', 'punctuation|。']
acc                  : 7/7
--------------------------
correct_substrings   : ['x|你最近好吗', 'punctuation|、', 'x|最近どうですか', 'punctuation|？', 'x|요즘 어떻게 지내요', 'punctuation|？']
test_split_substrings: ['zh|你最近好吗', 'punctuation|、', 'ja|最近どうですか', 'punctuation|？', 'ko|요즘 어떻게 지내요', 'punctuation|？']
acc                  : 6/6
--------------------------
correct_substrings   : ['x|Bonjour', 'punctuation|, ', "x|wie geht's dir ", 'x|today', 'punctuation|?']
test_split_substrings: ['fr|Bonjour', 'punctuation|, ', "de|wie geht's dir ", 'en|today', 'punctuation|?']
acc                  : 5/5
--------------------------
correct_substrings   : ['x|Vielen Dank ', 'x|merci beaucoup ', 'x|for your help', 'punctuation|.']
test_split_substrings: ['de|Vielen ', 'fr|Dank merci beaucoup ', 'en|for your help', 'punctuation|.']
acc                  : 2/4
--------------------------
correct_substrings   : ['x|Ich bin müde ', 'x|je suis fatigué ', 'x|and I need some rest', 'punctuation|.']
test_split_substrings: ['de|Ich ', 'en|bin ', 'de|müde ', 'fr|je suis fatigué ', 'en|and I need some rest', 'punctuation|.']
acc                  : 3/4
--------------------------
correct_substrings   : ['x|Ich mag dieses Buch ', 'x|ce livre est intéressant ', 'x|and it has a great story', 'punctuation|.']
test_split_substrings: ['de|Ich mag dieses Buch ', 'fr|ce livre est intéressant ', 'en|and it has a great story', 'punctuation|.']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|Ich mag dieses Buch', 'punctuation|, ', 'x|ce livre est intéressant', 'punctuation|, ', 'x|and it has a great story', 'punctuation|.']
test_split_substrings: ['de|Ich mag dieses Buch', 'punctuation|, ', 'fr|ce livre est intéressant', 'punctuation|, ', 'en|and it has a great story', 'punctuation|.']
acc                  : 6/6
--------------------------
correct_substrings   : ['x|The shirt is ', 'x|9.15 ', 'x|dollars', 'punctuation|.']
test_split_substrings: ['en|The shirt is 9', 'punctuation|.15 ', 'en|dollars', 'punctuation|.']
acc                  : 2/4
--------------------------
correct_substrings   : ['x|The shirt is ', 'digit|233 ', 'x|dollars', 'punctuation|.']
test_split_substrings: ['en|The shirt is 233 dollars', 'punctuation|.']
acc                  : 1/4
--------------------------
correct_substrings   : ['x|lang', 'punctuation|-', 'x|split']
test_split_substrings: ['en|lang', 'punctuation|-', 'en|split']
acc                  : 3/3
--------------------------
correct_substrings   : ['x|I have ', 'digit|10', 'punctuation|, ', 'x|€']
test_split_substrings: ['en|I have 10', 'punctuation|, ', 'fr|€']
acc                  : 2/4
--------------------------
correct_substrings   : ['x|日本のメディアでは', 'punctuation|「', 'x|匿名掲示板', 'punctuation|」', 'x|であると紹介されることが多いが', 'punctuation|、', 'x|2003年1月7日から全書き込みについて', 'x|IP', 'x|アドレスの記録・保存を始めており', 'punctuation|、', 'x|厳密には匿名掲示板ではなくなっていると', 'x|CNET Japan', 'x|は報じている']
test_split_substrings: ['ja|日本のメディアでは', 'punctuation|「', 'ja|匿名掲示板', 'punctuation|」', 'ja|であると紹介されることが多いが', 'punctuation|、2003', 'ja|年1月7日から全書き込みについて', 'en|IP', 'ja|アドレスの記録・保存を始めており', 'punctuation|、', 'ja|厳密には匿名掲示板ではなくなっていると', 'en|CNET Japan', 'ja|は報じている']
acc                  : 11/13
--------------------------
correct_substrings   : ['x|日本語', 'punctuation|（', 'x|にほんご', 'punctuation|、', 'x|にっぽんご', 'punctuation|）', 'x|は', 'punctuation|、', 'x|日本国内や', 'punctuation|、', 'x|かつての日本領だった国', 'punctuation|、', 'x|そして国外移民や移住者を含む日本人同士の間で使用されている言語', 'punctuation|。', 'x|日本は法令によって公用語を規定していないが', 'punctuation|、', 'x|法令その他の公用文は全て日本語で記述され', 'punctuation|、', 'x|各種法令において日本語を用いることが規定され', 'punctuation|、', 'x|学校教育においては「国語」の教科として学習を行うなど', 'punctuation|、', 'x|事実上日本国内において唯一の公用語となっている', 'punctuation|。']
test_split_substrings: ['ja|日本語', 'punctuation|（', 'ja|にほんご', 'punctuation|、', 'ja|にっぽんご', 'punctuation|）', 'ja|は', 'punctuation|、', 'ja|日本国内や', 'punctuation|、', 'ja|かつての日本領だった国', 'punctuation|、', 'ja|そして国外移民 や移住者を含む日本人同士の間で使用されている言語', 'punctuation|。', 'ja|日本は法令によって公用語を規定していないが', 'punctuation|、', 'ja|法令その他の公用文は全て日本語で記述され', 'punctuation|、', 'ja|各種法令において日本語を用いることが規定され', 'punctuation|、', 'ja|学校教育においては', 'punctuation|「', 'ja|国語', 'punctuation|」', 'ja|の教科として学習を行うなど', 'punctuation|、', 'ja|事実上日本国内において唯一の公用語となっている', 'punctuation|。']
acc                  : 23/24
--------------------------
correct_substrings   : ['x|日语是日本通用语及事实上的官方语言', 'punctuation|。', 'x|没有精确的日语使用人口的统计', 'punctuation|，', 'x|如果计算日本人口以及居住在日本以外的日本人', 'punctuation|、', 'x|日侨和日裔', 'punctuation|，', 'x|日语使用者应超过一亿三千万人', 'punctuation|。']
test_split_substrings: ['zh|日语是日本通用语及事实上的官方语言', 'punctuation|。', 'zh|没有精确的日语使用人口的统计', 'punctuation|，', 'zh|如果计算日本人口以及居住在日本以外的日本人', 'punctuation|、', 'zh|日侨和日裔', 'punctuation|，', 'zh|日语使用 者应超过一亿三千万人', 'punctuation|。']
acc                  : 10/10
--------------------------
total substring num: 217
test total substring num: 220
text acc num: 198
precision: 0.9124423963133641
recall: 0.9
F1 Score: 0.9061784897025171
time: 0.39931821823120117
  ```
</details>


# 2. 🪨Motivation
- `TTS (Text-To-Speech)` model often **fails** on multi-language speech generation, there are two ways to do:
  - Train a model can pronounce multiple languages
  - **(This Package)** Separate sentence based on language first, then use different language models
- Existed models in NLP toolkit (e.g. `SpaCy`, `jieba`) is usually helpful for dealing with text in **ONE** language for each model. Which means multi-language texts need pre-process, like texts below: 

```
你喜欢看アニメ吗？
Vielen Dank merci beaucoup for your help.
你最近好吗、最近どうですか？요즘 어떻게 지내요？sky is clear and sunny。
```

- [1. 💡How it works](#1-how-it-works)
- [2. 🪨Motivation](#2-motivation)
- [3. 📕Usage](#3-usage)
  - [3.1. 🚀Installation](#31-installation)
  - [3.2. Basic](#32-basic)
    - [3.2.1. `split_by_lang`](#321-split_by_lang)
    - [3.2.2. `merge_across_digit`](#322-merge_across_digit)
  - [3.3. Advanced](#33-advanced)
    - [3.3.1. usage of `lang_map` and `default_lang` (for your languages)](#331-usage-of-lang_map-and-default_lang-for-your-languages)
- [4. Acknowledgement](#4-acknowledgement)
- [5. ✨Star History](#5-star-history)


# 3. 📕Usage

## 3.1. 🚀Installation

You can install the package using pip:

```bash
pip install split-lang
```


****
## 3.2. Basic
### 3.2.1. `split_by_lang`

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DoodleBears/split-lang/blob/main/split-lang-demo.ipynb)

```python
from split_lang import LangSplitter
lang_splitter = LangSplitter()
text = "你喜欢看アニメ吗"

substr = lang_splitter.split_by_lang(
    text=text,
)
for index, item in enumerate(substr):
    print(f"{index}|{item.lang}:{item.text}")
```

```
0|zh:你喜欢看
1|ja:アニメ
2|zh:吗
```

```python
from split_lang import LangSplitter
lang_splitter = LangSplitter(merge_across_punctuation=True)
import time
texts = [
    "你喜欢看アニメ吗？我也喜欢看",
    "Please star this project on GitHub, Thanks you. I love you请加星这个项目，谢谢你。我爱你この項目をスターしてください、ありがとうございます！愛してる",
]
time1 = time.time()
for text in texts:
    substr = lang_splitter.split_by_lang(
        text=text,
    )
    for index, item in enumerate(substr):
        print(f"{index}|{item.lang}:{item.text}")
    print("----------------------")
time2 = time.time()
print(time2 - time1)
```

```
0|zh:你喜欢看
1|ja:アニメ
2|zh:吗？我也喜欢看
----------------------
0|en:Please star this project on GitHub, Thanks you. I love you
1|zh:请加星这个项目，谢谢你。我爱你
2|ja:この項目をスターしてください、ありがとうございます！愛してる
----------------------
0.007998466491699219
```

### 3.2.2. `merge_across_digit`

```python
lang_splitter.merge_across_digit = False
texts = [
    "衬衫的价格是9.15便士",
]
for text in texts:
    substr = lang_splitter.split_by_lang(
        text=text,
    )
    for index, item in enumerate(substr):
        print(f"{index}|{item.lang}:{item.text}")
```

```
0|zh:衬衫的价格是
1|digit:9.15
2|zh:便士
```

## 3.3. Advanced

### 3.3.1. usage of `lang_map` and `default_lang` (for your languages)

> [!IMPORTANT]
> Add lang code for your usecase if other languages are needed. [See Support Language](https://github.com/zafercavdar/fasttext-langdetect#supported-languages)

- default `lang_map` looks like below
  - if `langua-py` or `fasttext` or any other language detector detect the language that is NOT included in `lang_map` will be set to `default_lang`
  - if you set `default_lang` or `value` of `key:value` in `lang_map` to `x`, this substring will be merged to the near substring
    - `zh` | `x` | `jp` -> `zh` | `jp` (`x` been merged to one side)
    - In example below, `zh-tw` is set to `x` because character in `zh` and `jp` sometimes been detected as Traditional Chinese
- default `default_lang` is `x`

```python
DEFAULT_LANG_MAP = {
    "zh": "zh",
    "yue": "zh",  # 粤语
    "wuu": "zh",  # 吴语
    "zh-cn": "zh",
    "zh-tw": "x",
    "ko": "ko",
    "ja": "ja",
    "de": "de",
    "fr": "fr",
    "en": "en",
    "hr": "en",
}
DEFAULT_LANG = "x"

```

# 4. Acknowledgement

- Inspired by [LlmKira/fast-langdetect](https://github.com/LlmKira/fast-langdetect)
- Text segmentation depends on [google/budoux](https://github.com/google/budoux)
- Language detection depends on [zafercavdar/fasttext-langdetect](https://github.com/zafercavdar/fasttext-langdetect) and [rspeer/wordfreq](https://github.com/rspeer/wordfreq)

# 5. ✨Star History

[![Star History Chart](https://api.star-history.com/svg?repos=DoodleBears/split-lang&type=Timeline)](https://star-history.com/#DoodleBears/split-lang&Timeline)