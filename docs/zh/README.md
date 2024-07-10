<div align="center">

<img alt="VisActor Logo" width=50% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-logo.svg"/>

<img alt="VisActor Logo" width=70% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-banner.svg"/>
  
</div>
<div align="center">
  <h1>split-lang</h1>

[**English**](../../README.md) | **中文简体** | [**日本語**](../ja/README.md)

基于语言拆分文本：通过拆分字串为极小子字串再基于语言合并，使用

文本分割: [`budoux`](https://github.com/google/budoux) 以及规则判断

语言识别: [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) 和 [`lingua-py`](https://github.com/pemistahl/lingua-py)

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




# 1. 💡运作原理

**阶段 1**: 基于规则切分（区别文字、标点、数字）
- `hello, how are you` -> `hello` | `,` | `how are you`

**阶段 2**: 进一步拆分剩余的文字子字串，通过 [`budoux`](https://github.com/google/budoux) 拆分中日混合文本, 通过 ` ` (space) 拆分**非**[连写语言](https://en.wikipedia.org/wiki/Scriptio_continua)
- `你喜欢看アニメ吗` -> `你` | `喜欢` | `看` | `アニメ` | `吗`
- `昨天見た映画はとても感動的でした` -> `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した`
- `how are you` -> `how ` | `are ` | `you`

**阶段 3**: 连接子字串基于语言识别，通过 [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect), [`lingua-py`](https://github.com/pemistahl/lingua-py) 和正则表达式 (基于规则)
- `你` | `喜欢` | `看` | `アニメ` | `吗` -> `你喜欢看` | `アニメ` | `吗`
- `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した` -> `昨天` | `見た映画はとても感動的でした`
- `how ` | `are ` | `you` -> `how are you`

# 2. 🪨动机（为什么有这个包）
- `TTS (Text-To-Speech)` 文字转语言模型往往无法处理多语种混合的文本, 目前的解决方案通常有以下2种:
  - 训练一个 TTS 模型可以同时发音多种语言（但多种语言的发音规则和语法不同，为了达到音色一致，该种方案成本往往偏高）
  - **(这个包)** 将文本中不同语言的文本切分, 之后使用不同的 TTS 模型进行生成
- 现存的自然语音处理（NLP）包 (如：`SpaCy`, `jieba`) 通常每1个模型只针对 **1种** 语言处理（考虑到不同语言的语法、词汇特性）。所以在多语言的文本上，需要进行语言切分的预处理，如以下情况: 

```
你喜欢看アニメ吗？
Vielen Dank merci beaucoup for your help.
你最近好吗、最近どうですか？요즘 어떻게 지내요？sky is clear and sunny。
```

- [1. 💡运作原理](#1-运作原理)
- [2. 🪨动机（为什么有这个包）](#2-动机为什么有这个包)
- [3. 📕使用方法](#3-使用方法)
  - [3.1. 🚀安装](#31-安装)
  - [3.2. 基础用法](#32-基础用法)
    - [3.2.1. `split_by_lang`](#321-split_by_lang)
    - [3.2.2. `merge_across_digit`](#322-merge_across_digit)
  - [3.3. 进阶用法](#33-进阶用法)
    - [3.3.1.  `lang_map` 和 `default_lang` 的使用方式 (针对你的多语言场景)](#331--lang_map-和-default_lang-的使用方式-针对你的多语言场景)
- [4. 致谢](#4-致谢)
- [5. ✨星星时间线](#5-星星时间线)


# 3. 📕使用方法

## 3.1. 🚀安装

通过 pip 安装:

```bash
pip install split-lang
```


****
## 3.2. 基础用法
### 3.2.1. `split_by_lang`

线上体验：[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DoodleBears/split-lang/blob/main/split-lang-demo.ipynb)

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

## 3.3. 进阶用法

### 3.3.1.  `lang_map` 和 `default_lang` 的使用方式 (针对你的多语言场景)

> [!IMPORTANT]
> 请添加你需要的语言代码（默认可能不包含你的使用场景的语言）[查看支持语言](https://github.com/zafercavdar/fasttext-langdetect#supported-languages)

- 默认 `lang_map` 的设定如下方代码
  - 如果 `langua-py` 或 `fasttext` 语言识别器所检测到的语言不包含在 `lang_map` 的 key 中，会被设定为默认语言 `default_lang`
  - 如果你将 `default_lang` 或将 `lang_map` 中 `键值对` 的 `值` 设为 `x`, 该子字串会和相邻的子字串相连
    - `zh` | `x` | `jp` -> `zh` | `jp` (`x` 会被合并到其中一方（基于规则）)
    - 在下面的例子中, `zh-tw` 繁体中文被设置为 `x` 因为中文和日文的汉字包含了繁体中文
- `default_lang` 的默认值是 `x`

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

# 4. 致谢

- 受项目 [LlmKira/fast-langdetect](https://github.com/LlmKira/fast-langdetect) 启发
- 中日文文本分割基于 [google/budoux](https://github.com/google/budoux)
- 语言识别基于 [zafercavdar/fasttext-langdetect](https://github.com/zafercavdar/fasttext-langdetect) 和 [lingua-py](https://github.com/pemistahl/lingua-py)

# 5. ✨星星时间线

[![Star History Chart](https://api.star-history.com/svg?repos=DoodleBears/split-lang&type=Timeline)](https://star-history.com/#DoodleBears/split-lang&Timeline)