<div align="center">

<img alt="VisActor Logo" width=50% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-logo.svg"/>

<img alt="VisActor Logo" width=70% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-banner.svg"/>
  
</div>
<div align="center">
  <h1>split-lang</h1>

[**English**](../../README.md) | [**中文简体**](../zh/README.md) | **日本語**

文字を言語ごとに分割し、極小のサブストリングに分割してから言語に基づいて再結合する

テキスト分割: [`budoux`](https://github.com/google/budoux) およびルールベースの判断

言語認識: [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) と [`wordfreq`](https://github.com/rspeer/wordfreq)

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




# 1. 💡動作原理

**ステージ 1**: ルールベースの分割（文字、句読点、数字を区別）
- `hello, how are you` -> `hello` | `,` | `how are you`

**ステージ 2**: 残りの文字サブストリングをさらに分割し、[`budoux`](https://github.com/google/budoux) を使用して中日混合テキストを分割し、 ` ` (space) を使用して**非**[連続書記言語](https://en.wikipedia.org/wiki/Scriptio_continua)を分割
- `你喜欢看アニメ吗` -> `你` | `喜欢` | `看` | `アニメ` | `吗`
- `昨天見た映画はとても感動的でした` -> `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した`
- `how are you` -> `how ` | `are ` | `you`

**ステージ 3**: 言語認識に基づいてサブストリングを結合し、[`fast-langdetect`](https://github.com/LlmKira/fast-langdetect)、 [`wordfreq`](https://github.com/rspeer/wordfreq) と regex (ルールベース) を使用
- `你` | `喜欢` | `看` | `アニメ` | `吗` -> `你喜欢看` | `アニメ` | `吗`
- `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した` -> `昨天` | `見た映画はとても感動的でした`
- `how ` | `are ` | `you` -> `how are you`

<details>
  <summary>分割例</summary>
  
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
test_split_substrings: ['en|The shirt is ', 'digit|9', 'punctuation|.', 'digit|15 ', 'en|dollars', 'punctuation|.']
acc                  : 3/4
--------------------------
correct_substrings   : ['x|The shirt is ', 'digit|233 ', 'x|dollars', 'punctuation|.']
test_split_substrings: ['en|The shirt is ', 'digit|233 ', 'en|dollars', 'punctuation|.']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|lang', 'punctuation|-', 'x|split']
test_split_substrings: ['en|lang', 'punctuation|-', 'en|split']
acc                  : 3/3
--------------------------
correct_substrings   : ['x|I have ', 'digit|10', 'punctuation|, ', 'x|€']
test_split_substrings: ['en|I have ', 'digit|10', 'punctuation|, ', 'fr|€']
acc                  : 4/4
--------------------------
correct_substrings   : ['x|日本のメディアでは', 'punctuation|「', 'x|匿名掲示板', 'punctuation|」', 'x|であると紹介されることが多いが', 'punctuation|、', 'x|2003年1月7日から全書き込みについて', 'x|IP', 'x|アドレスの記録・保存を始めており', 'punctuation|、', 'x|厳密には匿名掲示板ではなくなっていると', 'x|CNET Japan', 'x|は報じている']
test_split_substrings: ['ja|日本のメディアでは', 'punctuation|「', 'ja|匿名掲示板', 'punctuation|」', 'ja|であると紹介されることが多いが', 'punctuation|、', 'digit|2003', 'ja|年', 'digit|1', 'ja|月', 'digit|7', 'ja|日から全書き込みについて', 'en|IP', 'ja|アドレスの記録・保存を始めており', 'punctuation|、', 'ja|厳密には匿名掲示板ではなくなっていると', 'en|CNET Japan', 'ja|は報じている']
acc                  : 12/13
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
test total substring num: 230
text acc num: 205
precision: 0.9447004608294931
recall: 0.8913043478260869
F1 Score: 0.9172259507829977
time: 0.3573117256164551
  ```
</details>

# 2. 🪨動機（なぜこのパッケージがいる）
- `TTS (Text-To-Speech)` 文字音声変換モデルは、多言語混合テキストを処理するのはなかなかできない。現在の解決策には以下の2つがあります:
  - 複数の言語で発音できる TTS モデルをトレーニングする（しかし、複数の言語の発音規則と文法は異なるため、音声の一貫性を保つためにコストが高くなります）
  - **（このパッケージ）** テキスト内の異なる言語のテキストを分割し、それぞれ異なる TTS モデルを使用して生成
- 既存の自然言語処理（NLP）パッケージ（例：`SpaCy`、 `jieba`）は通常、**1つ**の言語に対してのみ処理します（異なる言語の文法や語彙の特性を考慮するため）。したがって、多言語のテキストでは、以下のように事前に言語分割の前処理が必要です: 

```
你喜欢看アニメ吗？
Vielen Dank merci beaucoup for your help.
你最近好吗、最近どうですか？요즘 어떻게 지내요？sky is clear and sunny。
```

- [1. 💡動作原理](#1-動作原理)
- [2. 🪨動機（なぜこのパッケージがいる）](#2-動機なぜこのパッケージがいる)
- [3. 📕利用方法](#3-利用方法)
  - [3.1. 🚀インストール](#31-インストール)
  - [3.2. 基礎利用方法](#32-基礎利用方法)
    - [3.2.1. `split_by_lang`](#321-split_by_lang)
    - [3.2.2. `merge_across_digit`](#322-merge_across_digit)
  - [3.3. 上級利用方法](#33-上級利用方法)
    - [3.3.1.  `lang_map` と `default_lang` の使用法 (多言語対応)](#331--lang_map-と-default_lang-の使用法-多言語対応)
- [4. 謝辞](#4-謝辞)
- [5. ✨スタータイムライン](#5-スタータイムライン)


# 3. 📕利用方法

## 3.1. 🚀インストール

pip でインストール:

```bash
pip install split-lang
```


****
## 3.2. 基礎利用方法
### 3.2.1. `split_by_lang`

デモ：[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DoodleBears/split-lang/blob/main/split-lang-demo.ipynb)

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

## 3.3. 上級利用方法

### 3.3.1.  `lang_map` と `default_lang` の使用法 (多言語対応)

> [!IMPORTANT]
> 必要な言語コードを追加してください（デフォルトではあなたのシナリオに対応する言語が含まれていない場合があります）[対応言語を確認する](https://github.com/zafercavdar/fasttext-langdetect#supported-languages)

- デフォルトの `lang_map` の設定は以下の通り
  - `langua-py` または `fasttext` 言語認識器が検出した言語が `lang_map` のキーに含まれていない場合、デフォルト言語 `default_lang` に設定されます
  - `default_lang` を `x` に設定したり、`lang_map` の `キーの値` を `x` に設定したり場合, そのサブストリングは隣接するサブストリングと結合されます
    - `zh` | `x` | `jp` -> `zh` | `jp` (`x` はルールに基づいてどちらかに結合されます)
    - 以下の例では、 `zh-tw` 繁体中文を `x` に設定しています。これは中文と日文の漢字が繁体中文を含むためです
- `default_lang` のデフォルト値は `x`

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

# 4. 謝辞

- プロジェクト [LlmKira/fast-langdetect](https://github.com/LlmKira/fast-langdetect) に啓発され
- 中日テキスト分割に [google/budoux](https://github.com/google/budoux) を利用
- 言語認識に [zafercavdar/fasttext-langdetect](https://github.com/zafercavdar/fasttext-langdetect) と [rspeer/wordfreq](https://github.com/rspeer/wordfreq) を利用

# 5. ✨スタータイムライン

[![Star History Chart](https://api.star-history.com/svg?repos=DoodleBears/split-lang&type=Timeline)](https://star-history.com/#DoodleBears/split-lang&Timeline)