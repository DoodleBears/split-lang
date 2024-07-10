<div align="center">

<img alt="VisActor Logo" width=50% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-logo.svg"/>

<img alt="VisActor Logo" width=70% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-banner.svg"/>
  
</div>
<div align="center">
  <h1>split-lang</h1>

**English** | [**中文简体**](./docs/zh/README.md) | [**日本語**](./docs/ja/README.md)

Split text by languages through concatenating over split substrings based on their language, powered by

splitting: [`budoux`](https://github.com/google/budoux) and rule-base splitting

language detection: [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) and [`lingua-py`](https://github.com/pemistahl/lingua-py)

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

**Stage 3**: concatenate substrings based on their languages using [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect), [`lingua-py`](https://github.com/pemistahl/lingua-py) and regex (rule-based)
- `你` | `喜欢` | `看` | `アニメ` | `吗` -> `你喜欢看` | `アニメ` | `吗`
- `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した` -> `昨天` | `見た映画はとても感動的でした`
- `how ` | `are ` | `you` -> `how are you`

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
- Language detection depends on [zafercavdar/fasttext-langdetect](https://github.com/zafercavdar/fasttext-langdetect) and [lingua-py](https://github.com/pemistahl/lingua-py)

# 5. ✨Star History

[![Star History Chart](https://api.star-history.com/svg?repos=DoodleBears/split-lang&type=Timeline)](https://star-history.com/#DoodleBears/split-lang&Timeline)