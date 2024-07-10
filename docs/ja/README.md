<div align="center">

<img alt="VisActor Logo" width=50% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-logo.svg"/>

<img alt="VisActor Logo" width=70% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-banner.svg"/>
  
</div>
<div align="center">
  <h1>split-lang</h1>

[**English**](../../README.md) | [**中文简体**](../zh/README.md) | **日本語**

文字を言語ごとに分割し、極小のサブストリングに分割してから言語に基づいて再結合する

テキスト分割: [`budoux`](https://github.com/google/budoux) およびルールベースの判断

言語認識: [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) と [`lingua-py`](https://github.com/pemistahl/lingua-py)

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

**ステージ 3**: 言語認識に基づいてサブストリングを結合し、[`fast-langdetect`](https://github.com/LlmKira/fast-langdetect)、 [`lingua-py`](https://github.com/pemistahl/lingua-py) と regex (ルールベース) を使用
- `你` | `喜欢` | `看` | `アニメ` | `吗` -> `你喜欢看` | `アニメ` | `吗`
- `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した` -> `昨天` | `見た映画はとても感動的でした`
- `how ` | `are ` | `you` -> `how are you`

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
- 言語認識に [zafercavdar/fasttext-langdetect](https://github.com/zafercavdar/fasttext-langdetect) と [lingua-py](https://github.com/pemistahl/lingua-py) を利用
