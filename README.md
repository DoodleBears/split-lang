<div align="center">

<img alt="VisActor Logo" width=50% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-logo.svg"/>

<img alt="VisActor Logo" width=50% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-banner.svg"/>
  
</div>
<div align="center">
  <h1>split-lang</h1>

Splitting sentences by concatenating over-split substrings based on their language
powered by [`wtpsplit`](https://github.com/segment-any-text/wtpsplit) and language detection ([`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) and [`langdetect`](https://github.com/Mimino666/langdetect)) 

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




# 1. Idea

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
Vielen Dank merci beaucoup for your help.
你最近好吗、最近どうですか？요즘 어떻게 지내요？sky is clear and sunny。
```

- [1. Idea](#1-idea)
- [2. Motivation](#2-motivation)
- [3. Usage](#3-usage)
  - [3.1. Installation](#31-installation)
  - [3.2. Basic](#32-basic)
    - [3.2.1. `split_by_lang`](#321-split_by_lang)
  - [3.3. Advanced](#33-advanced)
    - [3.3.1. `TextSplitter` and `threshold`](#331-textsplitter-and-threshold)
    - [3.3.2. usage of `lang_map` and `default_lang` (for better result)](#332-usage-of-lang_map-and-default_lang-for-better-result)
- [4. Acknowledgement](#4-acknowledgement)


# 3. Usage

## 3.1. Installation

You can install the package using pip:

```bash
pip install split-lang
```



## 3.2. Basic
### 3.2.1. `split_by_lang`

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DoodleBears/split-lang/blob/main/split-lang-demo.ipynb)

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

```python
from split_lang import split_by_lang

texts = [
    "Please star this project on GitHub, Thanks you. I love you请加星这个项目，谢谢你。我爱你この項目をスターしてください、ありがとうございます！愛してる",
]

for text in texts:
    substr = split_by_lang(
        text=text,
        threshold=4.9e-5,
        default_lang="en",
        merge_across_punctuation=True,
    )
    for index, item in enumerate(substr):
        print(f"{index}|{item.lang}:{item.text}")
```


```
0|en:Please star this project on GitHub, Thanks you. I love you
1|zh:请加星这个项目，谢谢你。我爱你
2|ja:この項目をスターしてください、ありがとうございます！愛してる
----------------------
```

```python
from split_lang import split_by_lang

texts = [
    "Please star this project on GitHub, Thanks you. I love you请加星这个项目，谢谢你。我爱你この項目をスターしてください、ありがとうございます！愛してる",
]

for text in texts:
    substr = split_by_lang(
        text=text,
        threshold=4.9e-5,
        default_lang="en",
        merge_across_punctuation=False,
    )
    for index, item in enumerate(substr):
        print(f"{index}|{item.lang}:{item.text}")
```

```
0|en:Please star this project on GitHub
1|punctuation:, 
2|en:Thanks you
3|punctuation:. 
4|en:I love you
5|zh:请加星这个项目
6|punctuation:，
7|zh:谢谢你
8|punctuation:。
9|zh:我爱你
10|ja:この項目をスターしてください
11|punctuation:、
12|ja:ありがとうございます
13|punctuation:！
14|ja:愛してる
```
## 3.3. Advanced

### 3.3.1. `TextSplitter` and `threshold`

`TextSplitter` is a class which implement `split()` method to split the text after splitting with rule-based logic ([Idea-Stage 2](#1-idea)).

By default, it using `WtP` model from `wtpsplit`. (since `WtP` is faster and more accurate in SHORT TEXT situation, switch to `SaT` model for long paragraph).

the `threshold` is used for `WtP` and `SaT` models, default to `1e-4`, the smaller the more substring you will get in `wtpsplit` stage.

> [!NOTE]
> Check GitHub Repo `tests/split_acc.py` to find best threshold for your use case


### 3.3.2. usage of `lang_map` and `default_lang` (for better result)

> [!IMPORTANT]
> Add lang code for your usecase if other languages are needed

- default `lang_map` looks like below
  - if `langdetect` or `fasttext` or any other language detector detect the language that is NOT included in `lang_map` will be set to `default_lang`
  - if you set `default_lang` or `value` of `key:value` in `lang_map` to `x`, this substring will be merged to the near substring
    - `zh` | `x` | `jp` -> `zh` | `jp` (`x` been merged to one side)
    - In example below, `zh-tw` is set to `x` because character in `zh` and `jp` sometimes been detected as Traditional Chinese
- default `default_lang` is `x`

```python
LANG_MAP = {
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
}
DEFAULT_LANG = "x"
```

# 4. Acknowledgement

- Inspired by [LlmKira/fast-langdetect](https://github.com/LlmKira/fast-langdetect)
- Text segmentation depends on [segment-any-text/wtpsplit](https://github.com/segment-any-text/wtpsplit)
- Language detection depends on [zafercavdar/fasttext-langdetect](https://github.com/zafercavdar/fasttext-langdetect) and [Mimino666/langdetect](https://github.com/Mimino666/langdetect) (fix miss detecting Chinese as Korean in [DoodleBears/langdetect](https://github.com/DoodleBears/langdetect))
