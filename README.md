# 1. `split-lang`

[![PyPI version](https://badge.fury.io/py/split-lang.svg)](https://badge.fury.io/py/split-lang)
[![Downloads](https://static.pepy.tech/badge/split-lang)](https://pepy.tech/project/split-lang)
[![Downloads](https://static.pepy.tech/badge/split-lang/month)](https://pepy.tech/project/split-lang)

[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)

[![wakatime](https://wakatime.com/badge/user/5728d95a-5cfb-4acb-b600-e34c2fc231b6/project/e06e0a00-9ba1-453d-8c62-a0b2604aaaad.svg)](https://wakatime.com/badge/user/5728d95a-5cfb-4acb-b600-e34c2fc231b6/project/e06e0a00-9ba1-453d-8c62-a0b2604aaaad)

Splitting sentences by concatenating over-split substrings based on their language

powered by [`wtpsplit`](https://github.com/segment-any-text/wtpsplit) and [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) and [`langdetect`](https://github.com/Mimino666/langdetect)

## Idea

**Stage 1**: rule-based split using punctuation
- `hello, how are you` -> `hello` | `,` | `how are you`

**Stage 2**: then, over-split text to substrings by `wtpsplit`
- `你喜欢看アニメ吗` -> `你` | `喜欢` | `看` | `アニメ` | `吗`

**Stage 3**: concatenate substrings based on their languages using `fast-langdetect` and `langdetect`
- `你` | `喜欢` | `看` | `アニメ` | `吗` -> `你喜欢看` | `アニメ` | `吗`

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
Vielen Dank merci beaucoup for your help.
```

- [1. `split-lang`](#1-split-lang)
  - [Idea](#idea)
- [2. Motivation](#2-motivation)
- [3. Usage](#3-usage)
  - [3.1. Installation](#31-installation)
  - [3.2. Basic](#32-basic)
    - [3.2.1. `split_by_lang`](#321-split_by_lang)
  - [3.3. Advanced](#33-advanced)
    - [`threshold`](#threshold)
    - [3.3.1. usage of `lang_map` (for better result)](#331-usage-of-lang_map-for-better-result)


# 3. Usage

## 3.1. Installation

You can install the package using pip:

```bash
pip install split-lang
```



## 3.2. Basic
### 3.2.1. `split_by_lang`

```python
from split_lang import split_by_lang

texts = [
    "你喜欢看アニメ吗？",
]

for text in texts:
    substr = split_by_lang(
        text=text,
        threshold=4.9e-5,
        default_lang="en",
    )
    for index, item in enumerate(substr):
        print(f"{index}|{item.lang}:{item.text}")
    print("----------------------")
```

```
0|zh:你喜欢看
1|ja:アニメ
2|zh:吗
3|punctuation:？
```

## 3.3. Advanced

### `threshold`

the threshold used in `wtpsplit`, default to 1e-4, the smaller the more substring you will get in `wtpsplit` stage

> [!NOTE]
> Check GitHub Repo `tests/split_acc.py` to find best threshold for your use case


### 3.3.1. usage of `lang_map` (for better result)

> [!IMPORTANT]
> Add lang code for your usecase if other languages are needed

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
