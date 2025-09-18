<div align="center">

<img alt="VisActor Logo" width=50% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-logo.svg"/>

<img alt="VisActor Logo" width=70% src="https://github.com/DoodleBears/split-lang/blob/main/.github/profile/split-lang-banner.svg"/>
  
</div>
<div align="center">
  <h1>split-lang</h1>

**English** | [**中文简体**](./docs/zh/README.md) | [**日本語**](./docs/ja/README.md)

Split text by languages through concatenating over split substrings based on their language, powered by

splitting: [`budoux`](https://github.com/google/budoux) and rule-base splitting

language detection: [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect)

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

# Update History

## v2.1.1

- [2025-09-18] Bump fast_langdetect to 1.0+

## v2.1.0

- [2025-02-21] Modified merging logic

  - Significantly reduced the merging of `ja` strings containing kana into nearby `zh` (there are still misjudgments in cases of pure kanji Japanese and Chinese mixed together)
  - Processing speed increased by 6 to 7 times (removed the use of `wordfreq`)
  <details>
    <summary>Test results (highlighting improvement points)</summary>

  `python .\tests\split_acc.py`

  ### before

  ```
  correct_substrings   : ['  x|我的姓名', '  x|は', '  x|爱音']
  test_split_substrings: [' ja|我的姓名は', ' zh|爱音']
  correct_substrings   : ['  x|寂しい', '  x|的人']
  test_split_substrings: [' ja|寂しい的人']
  correct_substrings   : ['  x|真的很难分离', '  x|玉子焼き']
  test_split_substrings: [' zh|真的很难分离玉子焼き']
  correct_substrings   : ['  x|寝る', '  x|和蔬菜我都喜欢', 'pun|。']
  test_split_substrings: [' zh|寝る和蔬菜我都喜欢', 'pun|。']
  correct_substrings   : ['  x|すし', '  x|和蔬菜我都喜欢', 'pun|。']
  test_split_substrings: [' zh|すし和蔬菜我都喜欢', 'pun|。']
  correct_substrings   : ['  x|我喜欢', '  x|食べる', '  x|蔬菜和水果', 'pun|。']
  test_split_substrings: [' zh|我喜欢食べる蔬菜和水果', 'pun|。']
  ```

  ### after

  ```
  original_string: 我的姓名は爱音
  correct result : ['  x|我的姓名', '  x|は', '  x|爱音']
  test result    : [' zh|我的姓名', ' ja|は', ' zh|爱音']
  original_string: 寂しい的人
  correct result : ['  x|寂しい', '  x|的人']
  test result    : [' ja|寂しい', ' zh|的人']
  original_string: 真的很难分离玉子焼き
  correct result : ['  x|真的很难分离', '  x|玉子焼き']
  test result    : [' zh|真的很难分离', ' ja|玉子焼き']
  original_string: 寝る和蔬菜我都喜欢。
  correct result : ['  x|寝る', '  x|和蔬菜我都喜欢', 'pun|。']
  test result    : [' ja|寝る', ' zh|和蔬菜我都喜欢', 'pun|。']
  original_string: すし和蔬菜我都喜欢。
  correct result : ['  x|すし', '  x|和蔬菜我都喜欢', 'pun|。']
  test result    : [' ja|すし', ' zh|和蔬菜我都喜欢', 'pun|。']
  original_string: 我喜欢食べる蔬菜和水果。
  correct result : ['  x|我喜欢', '  x|食べる', '  x|蔬菜和水果', 'pun|。']
  test result    : [' zh|我喜欢', ' ja|食べる', ' zh|蔬菜和水果', 'pun|。']
  ```

  ### All Test Results (Execute `python .\tests\split_acc.py` to obtain)

  ```
  1✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅---------------------------------------------------------------------------------------------------
  original_string: 我是 VGroupChatBot，一个旨在支持多人通信的助手，通过可视化消息来帮助团队成员更好地交流。我可以帮助团队成员更好地整理和共享信息，特别是在讨论、会议和Brainstorming等情况下。你好我的名字是西野く まですmy name is bob很高兴认识你どうぞよろしくお願いいたします「こんにちは」是什么意思。
  correct result : ['  x|我是 ', '  x|VGroupChatBot', 'pun|，', '  x|一个旨在支持多人通信的助手', 'pun|，', '  x|通过可视化消息来帮助团队成员更好地交流', 'pun|。', '  x|我可以帮助团队成员更好地整理和共享信息', 'pun|，', '  x|特别是在讨论', 'pun|、', '  x|会议和', '  x|Brainstorming', '  x|等情况下', 'pun|。', '  x|你好我的名字是', '  x|西野くまです', '  x|my name is bob', '  x|很高兴认识你', '  x|どうぞよろしくお願いいたします', 'pun|「', '  x|こんにちは', 'pun|」', '  x|是什么意思', 'pun|。']
  test result    : [' zh|我是 ', ' en|VGroupChatBot', 'pun|，', ' zh|一个旨在支持多人通信的助手', 'pun|，', ' zh|通过可视化消息来帮助团队成员更好地交流', 'pun|。', ' zh|我可以帮助团队成员更好地整理和共享信息', 'pun|，', ' zh|特别是在讨论', 'pun|、', ' zh|会议和', ' en|Brainstorming', ' zh|等情况下', 'pun|。', ' zh|你好我的名字是', ' ja|西野くまです', ' en|my name is bob', ' zh|很高兴认识你', ' ja|どうぞよろしくお願いいたします', 'pun|「', ' ja|こんにちは', 'pun|」', ' zh|是什么意思', 'pun|。']
  acc                  : 25/25
  2✅✅✅✅✅✅✅✅---------------------------------------------------------------------------------------------------
  original_string: 我的名字是西野くまです。I am from Tokyo, 日本の首都。今天的天气非常好
  correct result : ['  x|我的名字是', '  x|西野くまです', 'pun|。', '  x|I am from Tokyo', 'pun|, ', '  x|日本の首都', 'pun|。', '  x|今天的天气非常好']
  test result    : [' zh|我的名字是', ' ja|西野くまです', 'pun|。', ' en|I am from Tokyo', 'pun|, ', ' ja|日本の首都', 'pun|。', ' zh|今天的天气非常好']
  acc                  : 8/8
  3✅✅✅✅---------------------------------------------------------------------------------------------------
  original_string: 你好，今日はどこへ行きますか？
  correct result : ['  x|你好', 'pun|，', '  x|今日はどこへ行きますか', 'pun|？']
  test result    : [' zh|你好', 'pun|，', ' ja|今日はどこへ行きますか', 'pun|？']
  acc                  : 4/4
  4✅✅✅---------------------------------------------------------------------------------------------------
  original_string: 你好今日はどこへ行きますか？
  correct result : ['  x|你好', '  x|今日はどこへ行きますか', 'pun|？']
  test result    : [' zh|你好', ' ja|今日はどこへ行きますか', 'pun|？']
  acc                  : 3/3
  5❌❌✅---------------------------------------------------------------------------------------------------
  original_string: 我的名字是田中さんです。
  correct result : ['  x|我的名字是', '  x|田中さんです', 'pun|。']
  test result    : [' zh|我的名字是田中', ' ja|さんです', 'pun|。']
  acc                  : 1/3
  6✅✅✅---------------------------------------------------------------------------------------------------
  original_string: 我喜欢吃寿司和拉面おいしいです。
  correct result : ['  x|我喜欢吃寿司和拉面', '  x|おいしいです', 'pun|。']
  test result    : [' zh|我喜欢吃寿司和拉面', ' ja|おいしいです', 'pun|。']
  acc                  : 3/3
  7✅✅✅---------------------------------------------------------------------------------------------------
  original_string: 今天の天気はとてもいいですね。
  correct result : ['  x|今天', '  x|の天気はとてもいいですね', 'pun|。']
  test result    : [' zh|今天', ' ja|の天気はとてもいいですね', 'pun|。']
  acc                  : 3/3
  8❌❌✅---------------------------------------------------------------------------------------------------
  original_string: 我在学习日本語少し難しいです。
  correct result : ['  x|我在学习', '  x|日本語少し難しいです', 'pun|。']
  test result    : [' zh|我在学习日本語少', ' ja|し難しいです', 'pun|。']
  acc                  : 1/3
  9✅✅✅---------------------------------------------------------------------------------------------------
  original_string: 日语真是おもしろい啊
  correct result : ['  x|日语真是', '  x|おもしろい', '  x|啊']
  test result    : [' zh|日语真是', ' ja|おもしろい', ' zh|啊']
  acc                  : 3/3
  10✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 你喜欢看アニメ吗？
  correct result : ['  x|你喜欢看', '  x|アニメ', '  x|吗', 'pun|？']
  test result    : [' zh|你喜欢看', ' ja|アニメ', ' zh|吗', 'pun|？']
  acc                  : 4/4
  11❌❌✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我想去日本旅行、特に京都に行きたいです。
  correct result : ['  x|我想去日本旅行', 'pun|、', '  x|特に京都に行きたいです', 'pun|。']
  test result    : [' zh|我想去', ' ja|日本旅行', 'pun|、', ' ja|特に京都に行きたいです', 'pun|。']
  acc                  : 3/4
  12✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 昨天見た映画はとても感動的でした。我朋友是日本人彼はとても優しいです。
  correct result : ['  x|昨天', '  x|見た映画はとても感動的でした', 'pun|。', '  x|我朋友是日本人', '  x|彼はとても優しいです', 'pun|。']
  test result    : [' zh|昨天', ' ja|見た映画はとても感動的でした', 'pun|。', ' zh|我朋友是日本人', ' ja|彼はとても優しいです', 'pun|。']
  acc                  : 6/6
  13✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我们一起去カラオケ吧、楽しそうです。
  correct result : ['  x|我们一起去', '  x|カラオケ', '  x|吧', 'pun|、', '  x|楽しそうです', 'pun|。']
  test result    : [' zh|我们一起去', ' ja|カラオケ', ' zh|吧', 'pun|、', ' ja|楽しそうです', 'pun|。']
  acc                  : 6/6
  14✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我的家在北京、でも、仕事で東京に住んでいます。
  correct result : ['  x|我的家在北京', 'pun|、', '  x|でも', 'pun|、', '  x|仕事で東京に住んでいます', 'pun|。']
  test result    : [' zh|我的家在北京', 'pun|、', ' ja|でも', 'pun|、', ' ja|仕事で東京に住んでいます', 'pun|。']
  acc                  : 6/6
  15✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我在学做日本料理、日本料理を作るのを習っています。
  correct result : ['  x|我在学做日本料理', 'pun|、', '  x|日本料理を作るのを習っています', 'pun|。']
  test result    : [' zh|我在学做日本料理', 'pun|、', ' ja|日本料理を作るのを習っています', 'pun|。']
  acc                  : 4/4
  16✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 你会说几种语言、何ヶ国語話せますか？
  correct result : ['  x|你会说几种语言', 'pun|、', '  x|何ヶ国語話せますか', 'pun|？']
  test result    : [' zh|你会说几种语言', 'pun|、', ' ja|何ヶ国語話せますか', 'pun|？']
  acc                  : 4/4
  17✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我昨天看了一本书、その本はとても面白かったです。
  correct result : ['  x|我昨天看了一本书', 'pun|、', '  x|その本はとても面白かったです', 'pun|。']
  test result    : [' zh|我昨天看了一本书', 'pun|、', ' ja|その本はとても面白かったです', 'pun|。']
  acc                  : 4/4
  18✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 你最近好吗、最近どうですか？
  correct result : ['  x|你最近好吗', 'pun|、', '  x|最近どうですか', 'pun|？']
  test result    : [' zh|你最近好吗', 'pun|、', ' ja|最近どうですか', 'pun|？']
  acc                  : 4/4
  19❌❌✅--------------------------------------------------------------------------------------------------
  original_string: 你最近好吗最近どうですか？
  correct result : ['  x|你最近好吗', '  x|最近どうですか', 'pun|？']
  test result    : [' zh|你最近好吗最近', ' ja|どうですか', 'pun|？']
  acc                  : 1/3
  20✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我在学做日本料理와 한국 요리、日本料理を作るのを習っています。
  correct result : ['  x|我在学做日本料理', '  x|와 한국 요리', 'pun|、', '  x|日本料理を作るのを習っています', 'pun|。']
  test result    : [' zh|我在学做日本料理', ' ko|와 한국 요리', 'pun|、', ' ja|日本料理を作るのを習っています', 'pun|。']
  acc                  : 5/5
  21✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 你会说几种语言、何ヶ国語話せますか？몇 개 언어를 할 수 있어요？
  correct result : ['  x|你会说几种语言', 'pun|、', '  x|何ヶ国語話せますか', 'pun|？', '  x|몇 개 언어를 할 수 있어요', 'pun|？']
  test result    : [' zh|你会说几种语言', 'pun|、', ' ja|何ヶ国語話せますか', 'pun|？', ' ko|몇 개 언어를 할 수 있어요', 'pun|？']
  acc                  : 6/6
  22✅✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我昨天看了一本书、その本はとても面白かったです。어제 책을 읽었는데, 정말 재미있었어요。
  correct result : ['  x|我昨天看了一本书', 'pun|、', '  x|その本はとても面白かったです', 'pun|。', '  x|어제 책을 읽었는데', 'pun|, ', '  x|정말 재미있었어요', 'pun|。']
  test result    : [' zh|我昨天看了一本书', 'pun|、', ' ja|その本はとても面白かったです', 'pun|。', ' ko|어제 책을 읽었는데', 'pun|, ', ' ko|정말 재미있었어요', 'pun|。']
  acc                  : 8/8
  23✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我们一起去逛街와 쇼핑、買い物に行きましょう。쇼핑하러 가요。
  correct result : ['  x|我们一起去逛街', '  x|와 쇼핑', 'pun|、', '  x|買い物に行きましょう', 'pun|。', '  x|쇼핑하러 가요', 'pun|。']
  test result    : [' zh|我们一起去逛街', ' ko|와 쇼핑', 'pun|、', ' ja|買い物に行きましょう', 'pun|。', ' ko|쇼핑하러 가요', 'pun|。']
  acc                  : 7/7
  24✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 你最近好吗、最近どうですか？요즘 어떻게 지내요？
  correct result : ['  x|你最近好吗', 'pun|、', '  x|最近どうですか', 'pun|？', '  x|요즘 어떻게 지내요', 'pun|？']
  test result    : [' zh|你最近好吗', 'pun|、', ' ja|最近どうですか', 'pun|？', ' ko|요즘 어떻게 지내요', 'pun|？']
  acc                  : 6/6
  25✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: Bonjour, wie geht's dir today?
  correct result : ['  x|Bonjour', 'pun|, ', "  x|wie geht's dir ", '  x|today', 'pun|?']
  test result    : [' fr|Bonjour', 'pun|, ', " de|wie geht's dir ", ' en|today', 'pun|?']
  acc                  : 5/5
  26❌❌✅✅--------------------------------------------------------------------------------------------------
  original_string: Vielen Dank merci beaucoup for your help.
  correct result : ['  x|Vielen Dank ', '  x|merci beaucoup ', '  x|for your help', 'pun|.']
  test result    : [' de|Vielen ', ' fr|Dank merci beaucoup ', ' en|for your help', 'pun|.']
  acc                  : 2/4
  27❌❌✅✅--------------------------------------------------------------------------------------------------
  original_string: Ich bin müde je suis fatigué and I need some rest.
  correct result : ['  x|Ich bin müde ', '  x|je suis fatigué ', '  x|and I need some rest', 'pun|.']
  test result    : [' de|Ich bin müde je ', ' fr|suis fatigué ', ' en|and I need some rest', 'pun|.']
  acc                  : 2/4
  28✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: Ich mag dieses Buch ce livre est intéressant and it has a great story.
  correct result : ['  x|Ich mag dieses Buch ', '  x|ce livre est intéressant ', '  x|and it has a great story', 'pun|.']
  test result    : [' de|Ich mag dieses Buch ', ' fr|ce livre est intéressant ', ' en|and it has a great story', 'pun|.']
  acc                  : 4/4
  29✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: Ich mag dieses Buch, ce livre est intéressant, and it has a great story.
  correct result : ['  x|Ich mag dieses Buch', 'pun|, ', '  x|ce livre est intéressant', 'pun|, ', '  x|and it has a great story', 'pun|.']
  test result    : [' de|Ich mag dieses Buch', 'pun|, ', ' fr|ce livre est intéressant', 'pun|, ', ' en|and it has a great story', 'pun|.']
  acc                  : 6/6
  30✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: The shirt is 9.15 dollars.
  correct result : ['  x|The shirt is ', 'digit|9', 'pun|.', 'digit|15 ', '  x|dollars', 'pun|.']
  test result    : [' en|The shirt is ', 'digit|9', 'pun|.', 'digit|15 ', ' en|dollars', 'pun|.']
  acc                  : 6/6
  31✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: The shirt is 233 dollars.
  correct result : ['  x|The shirt is ', 'digit|233 ', '  x|dollars', 'pun|.']
  test result    : [' en|The shirt is ', 'digit|233 ', ' en|dollars', 'pun|.']
  acc                  : 4/4
  32✅✅✅--------------------------------------------------------------------------------------------------
  original_string: lang-split
  correct result : ['  x|lang', 'pun|-', '  x|split']
  test result    : [' en|lang', 'pun|-', ' en|split']
  acc                  : 3/3
  33✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: I have 10, €
  correct result : ['  x|I have ', 'digit|10', 'pun|, ', '  x|€']
  test result    : [' en|I have ', 'digit|10', 'pun|, ', ' fr|€']
  acc                  : 4/4
  34✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 日本のメディアでは「匿名掲示板」であると紹介されることが多いが、2003年1月7日から全書き込みについてIPアドレスの記録・保存を始めており、厳密には匿名掲示板ではなくなっているとCNET Japanは報じている
  correct result : ['  x|日本のメディアでは', 'pun|「', '  x|匿名掲示板', 'pun|」', '  x|であると紹介されることが多いが', 'pun|、', 'digit|2003', '  x|年', 'digit|1', '  x|月', 'digit|7', '  x|日から全書き込みについて', '  x|IP', '  x|アドレスの記録・保存を始めており', 'pun|、', '  x|厳密には匿名掲示板ではなくなっていると', '  x|CNET Japan', '  x|は報じている']
  test result    : [' ja|日本のメディアでは', 'pun|「', ' ja|匿名掲示板', 'pun|」', ' ja|であると紹介されることが多いが', 'pun|、', 'digit|2003', ' ja|年', 'digit|1', ' ja|月', 'digit|7', ' ja|日から全書き込みについて', ' en|IP', ' ja|アドレスの記録・保存を始めており', 'pun|、', ' ja|厳密には匿名掲示板ではなくなっていると', ' en|CNET Japan', ' ja|は報じている']
  acc                  : 18/18
  35✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 日本語（にほんご、にっぽんご）は、日本国内や、かつての日本領だった国、そして国外移民や移住者を含む日本人同士の間で使用されている言語。日本は法令によって公用語を規定していないが、法令その他の公用文は全て日本語で記述され、各種法令において日本語を用いることが規定され、学校教育においては「国語」の教科として学習を行うなど、事実上日本国内において唯一の公用語となっている。
  correct result : ['  x|日本語', 'pun|（', '  x|にほんご', 'pun|、', '  x|にっぽんご', 'pun|）', '  x|は', 'pun|、', '  x|日本国内や', 'pun|、', '  x|かつての日本領だった国', 'pun|、', '  x|そして国外移民や移住者を含む日本人同士の間で使用されている言語', 'pun|。', '  x|日本は法令によって公用語を規定していないが', 'pun|、', '  x|法令その他の公用文は全て日本語で記述され', 'pun|、', '  x|各種法令において日本語を用いる ことが規定され', 'pun|、', '  x|学校教育においては', 'pun|「', '  x|国語', 'pun|」', '  x|の教科として学習を行うなど', 'pun|、', '  x|事実上日本国内において唯一の公用語となっている', 'pun|。']
  test result    : [' ja|日本語', 'pun|（', ' ja|にほんご', 'pun|、', ' ja|にっぽんご', 'pun|）', ' ja|は', 'pun|、', ' ja|日本国内や', 'pun|、', ' ja|かつての日本領だった国', 'pun|、', ' ja|そして国外移民や移住者を含む日本人同士の間で使用されている言語', 'pun|。', ' ja|日本は法令によって公用語を規定していないが', 'pun|、', ' ja|法令その他の公用文は全て日本語で記述され', 'pun|、', ' ja|各種法令において日本語を用いる ことが規定され', 'pun|、', ' ja|学校教育においては', 'pun|「', ' ja|国語', 'pun|」', ' ja|の教科として学習を行うなど', 'pun|、', ' ja|事実上日本国内において唯一の公用語となっている', 'pun|。']
  acc                  : 28/28
  36✅✅✅✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 日语是日本通用语及事实上的官方语言。没有精确的日语使用人口的统计，如果计算日本人口以及居住在日本以外的日本人、日侨和日裔，日语使用者应超过一亿三千万人。
  correct result : ['  x|日语是日本通用语及事实上的官方语言', 'pun|。', '  x|没有精确的日语使用人口的统计', 'pun|，', '  x|如果计算日本人口以及居住在日本以外的日本人', 'pun|、', '  x|日侨和日裔', 'pun|，', '  x|日语使用者应超过一亿三千万人', 'pun|。']
  test result    : [' zh|日语是日本通用语及事实上的官方语言', 'pun|。', ' zh|没有精确的日语使用人口的统计', 'pun|，', ' zh|如果计算日本人口以及居住在日本以外的日本人', 'pun|、', ' zh|日侨和日裔', 'pun|，', ' zh|日语使用者应超过一亿三千万人', 'pun|。']
  acc                  : 10/10
  37✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: MyGO?,你也喜欢まいご吗？
  correct result : ['  x|MyGO', '  x|?,', '  x|你也喜欢', '  x|まいご', '  x|吗', 'pun|？']
  test result    : [' en|MyGO', 'pun|?,', ' zh|你也喜欢', ' ja|まいご', ' zh|吗', 'pun|？']
  acc                  : 6/6
  38✅✅--------------------------------------------------------------------------------------------------
  original_string: まいご我可太喜欢了
  correct result : ['  x|まいご', '  x|我可太喜欢了']
  test result    : [' ja|まいご', ' zh|我可太喜欢了']
  acc                  : 2/2
  39✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我的名字is小明。
  correct result : ['  x|我的名字', '  x|is', '  x|小明', 'pun|。']
  test result    : [' zh|我的名字', ' en|is', ' ja|小明', 'pun|。']
  acc                  : 4/4
  40✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我的名字は小田です。
  correct result : ['  x|我的', '  x|名字は小田です', 'pun|。']
  test result    : [' zh|我的', ' ja|名字は小田です', 'pun|。']
  acc                  : 3/3
  41✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我喜欢食べる蔬菜和水果。
  correct result : ['  x|我喜欢', '  x|食べる', '  x|蔬菜和水果', 'pun|。']
  test result    : [' zh|我喜欢', ' ja|食べる', ' zh|蔬菜和水果', 'pun|。']
  acc                  : 4/4
  42✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 食べる蔬菜和水果我喜欢。
  correct result : ['  x|食べる', '  x|蔬菜和水果我喜欢', 'pun|。']
  test result    : [' ja|食べる', ' zh|蔬菜和水果我喜欢', 'pun|。']
  acc                  : 3/3
  43✅✅--------------------------------------------------------------------------------------------------
  original_string: 寿司和蔬菜我都喜欢。
  correct result : ['  x|寿司和蔬菜我都喜欢', 'pun|。']
  test result    : [' zh|寿司和蔬菜我都喜欢', 'pun|。']
  acc                  : 2/2
  44✅✅✅--------------------------------------------------------------------------------------------------
  original_string: すし和蔬菜我都喜欢。
  correct result : ['  x|すし', '  x|和蔬菜我都喜欢', 'pun|。']
  test result    : [' ja|すし', ' zh|和蔬菜我都喜欢', 'pun|。']
  acc                  : 3/3
  45✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 寝る和蔬菜我都喜欢。
  correct result : ['  x|寝る', '  x|和蔬菜我都喜欢', 'pun|。']
  test result    : [' ja|寝る', ' zh|和蔬菜我都喜欢', 'pun|。']
  acc                  : 3/3
  46✅✅--------------------------------------------------------------------------------------------------
  original_string: 料理私は大好きです。
  correct result : ['  x|料理私は大好きです', 'pun|。']
  test result    : [' ja|料理私は大好きです', 'pun|。']
  acc                  : 2/2
  47❌❌✅--------------------------------------------------------------------------------------------------
  original_string: 游戏大好きです。
  correct result : ['  x|游戏', '  x|大好きです', 'pun|。']
  test result    : [' zh|游戏大好', ' ja|きです', 'pun|。']
  acc                  : 1/3
  48❌❌✅--------------------------------------------------------------------------------------------------
  original_string: 游戏面白いです。
  correct result : ['  x|游戏', '  x|面白いです', 'pun|。']
  test result    : [' zh|游戏面', ' ja|白いです', 'pun|。']
  acc                  : 1/3
  49✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 初次见面，私の名前はDoodleです。
  correct result : ['  x|初次见面', 'pun|，', '  x|私の名前は', '  x|Doodle', '  x|です', 'pun|。']
  test result    : [' zh|初次见面', 'pun|，', ' ja|私の名前は', ' en|Doodle', ' ja|です', 'pun|。']
  acc                  : 6/6
  50✅✅--------------------------------------------------------------------------------------------------
  original_string: 中国語と日本語のミックス中文和日文的混合
  correct result : ['  x|中国語と日本語のミックス', '  x|中文和日文的混合']
  test result    : [' ja|中国語と日本語のミックス', ' zh|中文和日文的混合']
  acc                  : 2/2
  51✅✅--------------------------------------------------------------------------------------------------
  original_string: 真的很难分离玉子焼き
  correct result : ['  x|真的很难分离', '  x|玉子焼き']
  test result    : [' zh|真的很难分离', ' ja|玉子焼き']
  acc                  : 2/2
  52✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 真的很难分离すしリンゴ苹果
  correct result : ['  x|真的很难分离', '  x|すしリンゴ', '  x|苹果']
  test result    : [' zh|真的很难分离', ' ja|すしリンゴ', ' zh|苹果']
  acc                  : 3/3
  53❌--------------------------------------------------------------------------------------------------
  original_string: 全是汉字很难分离果物苹果
  correct result : ['  x|全是汉字很难分离', '  x|果物', '  x|苹果']
  test result    : [' zh|全是汉字很难分离果物苹果']
  acc                  : 0/3
  54✅✅--------------------------------------------------------------------------------------------------
  original_string: 寂しい的人
  correct result : ['  x|寂しい', '  x|的人']
  test result    : [' ja|寂しい', ' zh|的人']
  acc                  : 2/2
  55✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我的姓名は爱音
  correct result : ['  x|我的姓名', '  x|は', '  x|爱音']
  test result    : [' zh|我的姓名', ' ja|は', ' zh|爱音']
  acc                  : 3/3
  56✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我的名前は爱音
  correct result : ['  x|我的', '  x|名前は', '  x|爱音']
  test result    : [' zh|我的', ' ja|名前は', ' zh|爱音']
  acc                  : 3/3
  57✅✅✅--------------------------------------------------------------------------------------------------
  original_string: 我的名字は爱音
  correct result : ['  x|我的', '  x|名字は', '  x|爱音']
  test result    : [' zh|我的', ' ja|名字は', ' zh|爱音']
  acc                  : 3/3
  58✅❌❌--------------------------------------------------------------------------------------------------
  original_string: 我的名前是爱音
  correct result : ['  x|我的', '  x|名前', '  x|是爱音']
  test result    : [' zh|我的', ' ja|名前是', ' zh|爱音']
  acc                  : 1/3
  total substring num: 296
  test total substring num: 295
  text acc num: 276
  precision: 0.9324324324324325
  recall: 0.9355932203389831
  F1 Score: 0.9340101522842641
  time: 0.06800055503845215
  process speed char/s: 4352.905646617464
  ```

  </details>

## v2.0.6

- [2025-02-20] Fix merge japanese substring into near substring(s) (especially for Chinese and Japanese mixed text)
  <details>
    <summary>Test Result (Highlight Improvements)</summary>
    
    `python .\tests\split_acc.py`

  ### before

  ```
  correct_substrings   : ['  x|まいご', '  x|我可太喜欢了']
  test_split_substrings: [' zh|まいご我可太喜欢了']
  correct_substrings   : ['  x|MyGO', '  x|?,', '  x|你也喜欢', '  x|まいご', '  x|吗', 'pun|？']
  test_split_substrings: [' en|MyGO', 'pun|?,', ' zh|你也喜欢まいご吗', 'pun|？']
  ```

  ### after

  ```
  correct_substrings   : ['  x|まいご', '  x|我可太喜欢了']
  test_split_substrings: [' ja|まいご', ' zh|我可太喜欢了']
  correct_substrings   : ['  x|MyGO', '  x|?,', '  x|你也喜欢', '  x|まいご', '  x|吗', 'pun|？']
  test_split_substrings: [' en|MyGO', 'pun|?,', ' zh|你也喜欢', ' ja|まいご', ' zh|吗', 'pun|？']
  ```

  ### All test results

  ```
  1---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我是 ', '  x|VGroupChatBot', 'pun|，', '  x|一个旨在支持多人通信的助手', 'pun|，', '  x|通过可视化消息来帮助团队成员更好地交流', 'pun|。', '  x|我可以帮助团队成员更好地整理和共享信息', 'pun|，', '  x|特别是在讨论', 'pun|、', '  x|会议和', '  x|Brainstorming', '  x|等情况下', 'pun|。', '  x|你好我的名字是', '  x|西野くまです', '  x|my name is bob', '  x|很高兴认识你', '  x|どうぞよろしくお願いいたします', 'pun|「', '  x|こんにちは', 'pun|」', '  x|是什么意思', 'pun|。']
  test_split_substrings: [' zh|我是 ', ' en|VGroupChatBot', 'pun|，', ' zh|一个旨在支持多人通信的助手', 'pun|，', ' zh|通过可视化消息来帮助团队成员更好地交流', 'pun|。', ' zh|我可以帮助团队成员更好地整理和共享信息', 'pun|，', ' zh|特别是在讨论', 'pun|、', ' zh|会议和', ' en|Brainstorming', ' zh|等情况下', 'pun|。', ' zh|你好我的名字是', ' ja|西野くまです', ' en|my name is bob', ' zh|很高兴认识你', ' ja|どうぞよろしくお願いいたします', 'pun|「', ' ja|こんにちは', 'pun|」', ' zh|是什么意思', 'pun|。']
  acc                  : 25/25
  2---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我的名字是', '  x|西野くまです', 'pun|。', '  x|I am from Tokyo', 'pun|, ', '  x|日本の首都', 'pun|。', '  x|今天的天气非常好']
  test_split_substrings: [' zh|我的名字是', ' ja|西野くまです', 'pun|。', ' en|I am from Tokyo', 'pun|, ', ' ja|日本の首都', 'pun|。', ' zh|今天的天气非常好']
  acc                  : 8/8
  3---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|你好', 'pun|，', '  x|今日はどこへ行きますか', 'pun|？']
  test_split_substrings: [' zh|你好', 'pun|，', ' ja|今日はどこへ行きますか', 'pun|？']
  acc                  : 4/4
  4---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|你好', '  x|今日はどこへ行きますか', 'pun|？']
  test_split_substrings: [' zh|你好', ' ja|今日はどこへ行きますか', 'pun|？']
  acc                  : 3/3
  5---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我的名字是', '  x|田中さんです', 'pun|。']
  test_split_substrings: [' zh|我的名字是田中', ' ja|さんです', 'pun|。']
  acc                  : 1/3
  6---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我喜欢吃寿司和拉面', '  x|おいしいです', 'pun|。']
  test_split_substrings: [' zh|我喜欢吃寿司和拉面', ' ja|おいしいです', 'pun|。']
  acc                  : 3/3
  7---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|今天', '  x|の天気はとてもいいですね', 'pun|。']
  test_split_substrings: [' zh|今天', ' ja|の天気はとてもいいですね', 'pun|。']
  acc                  : 3/3
  8---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我在学习', '  x|日本語少し難しいです', 'pun|。']
  test_split_substrings: [' zh|我在学习日本語少', ' ja|し難しいです', 'pun|。']
  acc                  : 1/3
  9---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|日语真是', '  x|おもしろい', '  x|啊']
  test_split_substrings: [' zh|日语真是', ' ja|おもしろい', ' zh|啊']
  acc                  : 3/3
  10---------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|你喜欢看', '  x|アニメ', '  x|吗', 'pun|？']
  test_split_substrings: [' zh|你喜欢看', ' ja|アニメ', ' zh|吗', 'pun|？']
  acc                  : 4/4
  11--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我想去日本旅行', 'pun|、', '  x|特に京都に行きたいです', 'pun|。']
  test_split_substrings: [' zh|我想去日本旅行', 'pun|、', ' ja|特に京都に行きたいです', 'pun|。']
  acc                  : 4/4
  12--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|昨天', '  x|見た映画はとても感動的でした', 'pun|。', '  x|我朋友是日本人', '  x|彼はとても優しいです', 'pun|。']
  test_split_substrings: [' zh|昨天', ' ja|見た映画はとても感動的でした', 'pun|。', ' zh|我朋友是日本人', ' ja|彼はとても優しいです', 'pun|。']
  acc                  : 6/6
  13--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我们一起去', '  x|カラオケ', '  x|吧', 'pun|、', '  x|楽しそうです', 'pun|。']
  test_split_substrings: [' zh|我们一起去', ' ja|カラオケ', ' zh|吧', 'pun|、', ' ja|楽しそうです', 'pun|。']
  acc                  : 6/6
  14--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我的家在北京', 'pun|、', '  x|でも', 'pun|、', '  x|仕事で東京に住んでいます', 'pun|。']
  test_split_substrings: [' ja|我的家在北京', 'pun|、', ' ja|でも', 'pun|、', ' ja|仕事で東京に住んでいます', 'pun|。']
  acc                  : 6/6
  15--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我在学做日本料理', 'pun|、', '  x|日本料理を作るのを習っています', 'pun|。']
  test_split_substrings: [' ja|我在学做日本料理', 'pun|、', ' ja|日本料理を作るのを習っています', 'pun|。']
  acc                  : 4/4
  16--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|你会说几种语言', 'pun|、', '  x|何ヶ国語話せますか', 'pun|？']
  test_split_substrings: [' zh|你会说几种语言', 'pun|、', ' ja|何ヶ国語話せますか', 'pun|？']
  acc                  : 4/4
  17--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我昨天看了一本书', 'pun|、', '  x|その本はとても面白かったです', 'pun|。']
  test_split_substrings: [' zh|我昨天看了一本书', 'pun|、', ' ja|その本はとても面白かったです', 'pun|。']
  acc                  : 4/4
  18--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|你最近好吗', 'pun|、', '  x|最近どうですか', 'pun|？']
  test_split_substrings: [' zh|你最近好吗', 'pun|、', ' ja|最近どうですか', 'pun|？']
  acc                  : 4/4
  19--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|你最近好吗', '  x|最近どうですか', 'pun|？']
  test_split_substrings: [' zh|你最近好吗最近', ' ja|どうですか', 'pun|？']
  acc                  : 1/3
  20--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我在学做日本料理', '  x|와 한국 요리', 'pun|、', '  x|日本料理を作るのを習っています', 'pun|。']
  test_split_substrings: [' ja|我在学做日本料理', ' ko|와 한국 요리', 'pun|、', ' ja|日本料理を作るのを習っています', 'pun|。']
  acc                  : 5/5
  21--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|你会说几种语言', 'pun|、', '  x|何ヶ国語話せますか', 'pun|？', '  x|몇 개 언어를 할 수 있어요', 'pun|？']
  test_split_substrings: [' zh|你会说几种语言', 'pun|、', ' ja|何ヶ国語話せますか', 'pun|？', ' ko|몇 개 언어를 할 수 있어요', 'pun|？']
  acc                  : 6/6
  22--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我昨天看了一本书', 'pun|、', '  x|その本はとても面白かったです', 'pun|。', '  x|어제 책을 읽었는데', 'pun|, ', '  x|정말 재미있었어요', 'pun|。']
  test_split_substrings: [' zh|我昨天看了一本书', 'pun|、', ' ja|その本はとても面白かったです', 'pun|。', ' ko|어제 책을 읽었는데', 'pun|, ', ' ko|정말 재미있었어요', 'pun|。']
  acc                  : 8/8
  23--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|我们一起去逛街', '  x|와 쇼핑', 'pun|、', '  x|買い物に行きましょう', 'pun|。', '  x|쇼핑하러 가요', 'pun|。']
  test_split_substrings: [' zh|我们一起去逛街', ' ko|와 쇼핑', 'pun|、', ' ja|買い物に行きましょう', 'pun|。', ' ko|쇼핑하러 가요', 'pun|。']
  acc                  : 7/7
  24--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|你最近好吗', 'pun|、', '  x|最近どうですか', 'pun|？', '  x|요즘 어떻게 지내요', 'pun|？']
  test_split_substrings: [' zh|你最近好吗', 'pun|、', ' ja|最近どうですか', 'pun|？', ' ko|요즘 어떻게 지내요', 'pun|？']
  acc                  : 6/6
  25--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|Bonjour', 'pun|, ', "  x|wie geht's dir ", '  x|today', 'pun|?']
  test_split_substrings: [' fr|Bonjour', 'pun|, ', " de|wie geht's dir ", ' en|today', 'pun|?']
  acc                  : 5/5
  26--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|Vielen Dank ', '  x|merci beaucoup ', '  x|for your help', 'pun|.']
  test_split_substrings: [' de|Vielen ', ' fr|Dank merci beaucoup ', ' en|for your help', 'pun|.']
  acc                  : 2/4
  27--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|Ich bin müde ', '  x|je suis fatigué ', '  x|and I need some rest', 'pun|.']
  test_split_substrings: [' de|Ich ', ' en|bin ', ' de|müde ', ' fr|je suis fatigué ', ' en|and I need some rest', 'pun|.']
  acc                  : 3/4
  28--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|Ich mag dieses Buch ', '  x|ce livre est intéressant ', '  x|and it has a great story', 'pun|.']
  test_split_substrings: [' de|Ich mag dieses Buch ', ' fr|ce livre est intéressant ', ' en|and it has a great story', 'pun|.']
  acc                  : 4/4
  29--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|Ich mag dieses Buch', 'pun|, ', '  x|ce livre est intéressant', 'pun|, ', '  x|and it has a great story', 'pun|.']
  test_split_substrings: [' de|Ich mag dieses Buch', 'pun|, ', ' fr|ce livre est intéressant', 'pun|, ', ' en|and it has a great story', 'pun|.']
  acc                  : 6/6
  30--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|The shirt is ', '  x|9.15 ', '  x|dollars', 'pun|.']
  test_split_substrings: [' en|The shirt is ', 'digit|9', 'pun|.', 'digit|15 ', ' en|dollars', 'pun|.']
  acc                  : 3/4
  31--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|The shirt is ', 'digit|233 ', '  x|dollars', 'pun|.']
  test_split_substrings: [' en|The shirt is ', 'digit|233 ', ' en|dollars', 'pun|.']
  acc                  : 4/4
  32--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|lang', 'pun|-', '  x|split']
  test_split_substrings: [' en|lang', 'pun|-', ' en|split']
  acc                  : 3/3
  33--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|I have ', 'digit|10', 'pun|, ', '  x|€']
  test_split_substrings: [' en|I have ', 'digit|10', 'pun|, ', ' fr|€']
  acc                  : 4/4
  34--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|日本のメディアでは', 'pun|「', '  x|匿名掲示板', 'pun|」', '  x|であると紹介されることが多いが', 'pun|、', 'digit|2003', '  x|年', 'digit|1', '  x|月', 'digit|7', '  x|日から全書き込みについて', '  x|IP', '  x|アドレスの記録・保存を始めており', 'pun|、', '  x|厳密には匿名掲示板ではなくなっていると', '  x|CNET Japan', '  x|は報じている']
  test_split_substrings: [' ja|日本のメディアでは', 'pun|「', ' ja|匿名掲示板', 'pun|」', ' ja|であると紹介されることが多いが', 'pun|、', 'digit|2003', ' ja|年', 'digit|1', ' ja|月', 'digit|7', ' ja|日から全書き込みについて', ' en|IP', ' ja|アドレスの記録・保存を始めており', 'pun|、', ' ja|厳密には匿名掲示板ではなくなっていると', ' en|CNET Japan', ' ja|は報じている']
  acc                  : 18/18
  35--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|日本語', 'pun|（', '  x|にほんご', 'pun|、', '  x|にっぽんご', 'pun|）', '  x|は', 'pun|、', '  x|日本国内や', 'pun|、', '  x|かつての日本領だった国', 'pun|、', '  x|そして国外移民や移住者を含む日本人同士の間で使用されている言語', 'pun|。', '  x|日本は法令によって公用語を規定していないが', 'pun|、', '  x|法令その他の公用文は全て日本語で記述され', 'pun|、', '  x|各種法令において日本語を 用いることが規定され', 'pun|、', '  x|学校教育においては', 'pun|「', '  x|国語', 'pun|」', '  x|の教科として学習を行うなど', 'pun|、', '  x|事実上日本国内において唯一の公用語となっている', 'pun|。']
  test_split_substrings: [' ja|日本語', 'pun|（', ' ja|にほんご', 'pun|、', ' ja|にっぽんご', 'pun|）', ' ja|は', 'pun|、', ' ja|日本国内や', 'pun|、', ' ja|かつての日本領だった国', 'pun|、', ' ja|そして国外移民や移住者を含む日本人同士の間で使用されている言語', 'pun|。', ' ja|日本は法令によって公用語を規定していないが', 'pun|、', ' ja|法令その他の公用文は全て日本語で記述され', 'pun|、', ' ja|各種法令において日本語を 用いることが規定され', 'pun|、', ' ja|学校教育においては', 'pun|「', ' ja|国語', 'pun|」', ' ja|の教科として学習を行うなど', 'pun|、', ' ja|事実上日本国内において唯一の公用語となっている', 'pun|。']
  acc                  : 28/28
  36--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|日语是日本通用语及事实上的官方语言', 'pun|。', '  x|没有精确的日语使用人口的统计', 'pun|，', '  x|如果计算日本人口以及居住在日本以外的日本人', 'pun|、', '  x|日侨和日裔', 'pun|，', '  x|日语使用者应超过一亿三千万人', 'pun|。']
  test_split_substrings: [' zh|日语是日本通用语及事实上的官方语言', 'pun|。', ' zh|没有精确的日语使用人口的统计', 'pun|，', ' zh|如果计算日本人口以及居住在日本以外的日本人', 'pun|、', ' zh|日侨和日裔', 'pun|，', ' zh|日语使用者应超过一亿三千万人', 'pun|。']
  acc                  : 10/10
  37--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|MyGO', '  x|?,', '  x|你也喜欢', '  x|まいご', '  x|吗', 'pun|？']
  test_split_substrings: [' en|MyGO', 'pun|?,', ' zh|你也喜欢', ' ja|まいご', ' zh|吗', 'pun|？']
  acc                  : 6/6
  38--------------------------------------------------------------------------------------------------
  correct_substrings   : ['  x|まいご', '  x|我可太喜欢了']
  test_split_substrings: [' ja|まいご', ' zh|我可太喜欢了']
  acc                  : 2/2
  total substring num: 234
  test total substring num: 238
  text acc num: 224
  precision: 0.9572649572649573
  recall: 0.9411764705882353
  F1 Score: 0.9491525423728814
  time: 0.3950009346008301
  process speed char/s: 592.4036616178382
  ```

  </details>

# 1. 💡How it works

**Stage 1**: rule-based split (separate character, punctuation and digit)

- `hello, how are you` -> `hello` | `,` | `how are you`

**Stage 2**: over-split text to substrings by [`budoux`](https://github.com/google/budoux) for Chinese mix with Japanese, ` ` (space) for **not** [scripta continua](https://en.wikipedia.org/wiki/Scriptio_continua)

- `你喜欢看アニメ吗` -> `你` | `喜欢` | `看` | `アニメ` | `吗`
- `昨天見た映画はとても感動的でした` -> `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した`
- `how are you` -> `how ` | `are ` | `you`

**Stage 3**: concatenate substrings based on their languages using [`fast-langdetect`](https://github.com/LlmKira/fast-langdetect) and regex (rule-based)

- `你` | `喜欢` | `看` | `アニメ` | `吗` -> `你喜欢看` | `アニメ` | `吗`
- `昨天` | `見た` | `映画` | `は` | `とても` | `感動` | `的` | `で` | `した` -> `昨天` | `見た映画はとても感動的でした`
- `how ` | `are ` | `you` -> `how are you`

<details>
  <summary>More split examples</summary>
  
  ```python
1✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅---------------------------------------------------------------------------------------------------
original_string: 我是 VGroupChatBot，一个旨在支持多人通信的助手，通过可视化消息来帮助团队成员更好地交流。我可以帮助团队成员更好地整理和共享信息，特别是在讨论、会议和Brainstorming等情况下。你好我的名字是西野く まですmy name is bob很高兴认识你どうぞよろしくお願いいたします「こんにちは」是什么意思。
correct result : ['  x|我是 ', '  x|VGroupChatBot', 'pun|，', '  x|一个旨在支持多人通信的助手', 'pun|，', '  x|通过可视化消息来帮助团队成员更好地交流', 'pun|。', '  x|我可以帮助团队成员更好地整理和共享信息', 'pun|，', '  x|特别是在讨论', 'pun|、', '  x|会议和', '  x|Brainstorming', '  x|等情况下', 'pun|。', '  x|你好我的名字是', '  x|西野くまです', '  x|my name is bob', '  x|很高兴认识你', '  x|どうぞよろしくお願いいたします', 'pun|「', '  x|こんにちは', 'pun|」', '  x|是什么意思', 'pun|。']
test result    : [' zh|我是 ', ' en|VGroupChatBot', 'pun|，', ' zh|一个旨在支持多人通信的助手', 'pun|，', ' zh|通过可视化消息来帮助团队成员更好地交流', 'pun|。', ' zh|我可以帮助团队成员更好地整理和共享信息', 'pun|，', ' zh|特别是在讨论', 'pun|、', ' zh|会议和', ' en|Brainstorming', ' zh|等情况下', 'pun|。', ' zh|你好我的名字是', ' ja|西野くまです', ' en|my name is bob', ' zh|很高兴认识你', ' ja|どうぞよろしくお願いいたします', 'pun|「', ' ja|こんにちは', 'pun|」', ' zh|是什么意思', 'pun|。']
acc                  : 25/25
2✅✅✅✅✅✅✅✅---------------------------------------------------------------------------------------------------
original_string: 我的名字是西野くまです。I am from Tokyo, 日本の首都。今天的天气非常好
correct result : ['  x|我的名字是', '  x|西野くまです', 'pun|。', '  x|I am from Tokyo', 'pun|, ', '  x|日本の首都', 'pun|。', '  x|今天的天气非常好']
test result    : [' zh|我的名字是', ' ja|西野くまです', 'pun|。', ' en|I am from Tokyo', 'pun|, ', ' ja|日本の首都', 'pun|。', ' zh|今天的天气非常好']
acc                  : 8/8
3✅✅✅✅---------------------------------------------------------------------------------------------------
original_string: 你好，今日はどこへ行きますか？
correct result : ['  x|你好', 'pun|，', '  x|今日はどこへ行きますか', 'pun|？']
test result    : [' zh|你好', 'pun|，', ' ja|今日はどこへ行きますか', 'pun|？']
acc                  : 4/4
4✅✅✅---------------------------------------------------------------------------------------------------
original_string: 你好今日はどこへ行きますか？
correct result : ['  x|你好', '  x|今日はどこへ行きますか', 'pun|？']
test result    : [' zh|你好', ' ja|今日はどこへ行きますか', 'pun|？']
acc                  : 3/3
5❌❌✅---------------------------------------------------------------------------------------------------
original_string: 我的名字是田中さんです。
correct result : ['  x|我的名字是', '  x|田中さんです', 'pun|。']
test result    : [' zh|我的名字是田中', ' ja|さんです', 'pun|。']
acc                  : 1/3
6✅✅✅---------------------------------------------------------------------------------------------------
original_string: 我喜欢吃寿司和拉面おいしいです。
correct result : ['  x|我喜欢吃寿司和拉面', '  x|おいしいです', 'pun|。']
test result    : [' zh|我喜欢吃寿司和拉面', ' ja|おいしいです', 'pun|。']
acc                  : 3/3
7✅✅✅---------------------------------------------------------------------------------------------------
original_string: 今天の天気はとてもいいですね。
correct result : ['  x|今天', '  x|の天気はとてもいいですね', 'pun|。']
test result    : [' zh|今天', ' ja|の天気はとてもいいですね', 'pun|。']
acc                  : 3/3
8❌❌✅---------------------------------------------------------------------------------------------------
original_string: 我在学习日本語少し難しいです。
correct result : ['  x|我在学习', '  x|日本語少し難しいです', 'pun|。']
test result    : [' zh|我在学习日本語少', ' ja|し難しいです', 'pun|。']
acc                  : 1/3
9✅✅✅---------------------------------------------------------------------------------------------------
original_string: 日语真是おもしろい啊
correct result : ['  x|日语真是', '  x|おもしろい', '  x|啊']
test result    : [' zh|日语真是', ' ja|おもしろい', ' zh|啊']
acc                  : 3/3
10✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 你喜欢看アニメ吗？
correct result : ['  x|你喜欢看', '  x|アニメ', '  x|吗', 'pun|？']
test result    : [' zh|你喜欢看', ' ja|アニメ', ' zh|吗', 'pun|？']
acc                  : 4/4
11❌❌✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我想去日本旅行、特に京都に行きたいです。
correct result : ['  x|我想去日本旅行', 'pun|、', '  x|特に京都に行きたいです', 'pun|。']
test result    : [' zh|我想去', ' ja|日本旅行', 'pun|、', ' ja|特に京都に行きたいです', 'pun|。']
acc                  : 3/4
12✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 昨天見た映画はとても感動的でした。我朋友是日本人彼はとても優しいです。
correct result : ['  x|昨天', '  x|見た映画はとても感動的でした', 'pun|。', '  x|我朋友是日本人', '  x|彼はとても優しいです', 'pun|。']
test result    : [' zh|昨天', ' ja|見た映画はとても感動的でした', 'pun|。', ' zh|我朋友是日本人', ' ja|彼はとても優しいです', 'pun|。']
acc                  : 6/6
13✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我们一起去カラオケ吧、楽しそうです。
correct result : ['  x|我们一起去', '  x|カラオケ', '  x|吧', 'pun|、', '  x|楽しそうです', 'pun|。']
test result    : [' zh|我们一起去', ' ja|カラオケ', ' zh|吧', 'pun|、', ' ja|楽しそうです', 'pun|。']
acc                  : 6/6
14✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我的家在北京、でも、仕事で東京に住んでいます。
correct result : ['  x|我的家在北京', 'pun|、', '  x|でも', 'pun|、', '  x|仕事で東京に住んでいます', 'pun|。']
test result    : [' zh|我的家在北京', 'pun|、', ' ja|でも', 'pun|、', ' ja|仕事で東京に住んでいます', 'pun|。']
acc                  : 6/6
15✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我在学做日本料理、日本料理を作るのを習っています。
correct result : ['  x|我在学做日本料理', 'pun|、', '  x|日本料理を作るのを習っています', 'pun|。']
test result    : [' zh|我在学做日本料理', 'pun|、', ' ja|日本料理を作るのを習っています', 'pun|。']
acc                  : 4/4
16✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 你会说几种语言、何ヶ国語話せますか？
correct result : ['  x|你会说几种语言', 'pun|、', '  x|何ヶ国語話せますか', 'pun|？']
test result    : [' zh|你会说几种语言', 'pun|、', ' ja|何ヶ国語話せますか', 'pun|？']
acc                  : 4/4
17✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我昨天看了一本书、その本はとても面白かったです。
correct result : ['  x|我昨天看了一本书', 'pun|、', '  x|その本はとても面白かったです', 'pun|。']
test result    : [' zh|我昨天看了一本书', 'pun|、', ' ja|その本はとても面白かったです', 'pun|。']
acc                  : 4/4
18✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 你最近好吗、最近どうですか？
correct result : ['  x|你最近好吗', 'pun|、', '  x|最近どうですか', 'pun|？']
test result    : [' zh|你最近好吗', 'pun|、', ' ja|最近どうですか', 'pun|？']
acc                  : 4/4
19❌❌✅--------------------------------------------------------------------------------------------------
original_string: 你最近好吗最近どうですか？
correct result : ['  x|你最近好吗', '  x|最近どうですか', 'pun|？']
test result    : [' zh|你最近好吗最近', ' ja|どうですか', 'pun|？']
acc                  : 1/3
20✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我在学做日本料理와 한국 요리、日本料理を作るのを習っています。
correct result : ['  x|我在学做日本料理', '  x|와 한국 요리', 'pun|、', '  x|日本料理を作るのを習っています', 'pun|。']
test result    : [' zh|我在学做日本料理', ' ko|와 한국 요리', 'pun|、', ' ja|日本料理を作るのを習っています', 'pun|。']
acc                  : 5/5
21✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 你会说几种语言、何ヶ国語話せますか？몇 개 언어를 할 수 있어요？
correct result : ['  x|你会说几种语言', 'pun|、', '  x|何ヶ国語話せますか', 'pun|？', '  x|몇 개 언어를 할 수 있어요', 'pun|？']
test result    : [' zh|你会说几种语言', 'pun|、', ' ja|何ヶ国語話せますか', 'pun|？', ' ko|몇 개 언어를 할 수 있어요', 'pun|？']
acc                  : 6/6
22✅✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我昨天看了一本书、その本はとても面白かったです。어제 책을 읽었는데, 정말 재미있었어요。
correct result : ['  x|我昨天看了一本书', 'pun|、', '  x|その本はとても面白かったです', 'pun|。', '  x|어제 책을 읽었는데', 'pun|, ', '  x|정말 재미있었어요', 'pun|。']
test result    : [' zh|我昨天看了一本书', 'pun|、', ' ja|その本はとても面白かったです', 'pun|。', ' ko|어제 책을 읽었는데', 'pun|, ', ' ko|정말 재미있었어요', 'pun|。']
acc                  : 8/8
23✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我们一起去逛街와 쇼핑、買い物に行きましょう。쇼핑하러 가요。
correct result : ['  x|我们一起去逛街', '  x|와 쇼핑', 'pun|、', '  x|買い物に行きましょう', 'pun|。', '  x|쇼핑하러 가요', 'pun|。']
test result    : [' zh|我们一起去逛街', ' ko|와 쇼핑', 'pun|、', ' ja|買い物に行きましょう', 'pun|。', ' ko|쇼핑하러 가요', 'pun|。']
acc                  : 7/7
24✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 你最近好吗、最近どうですか？요즘 어떻게 지내요？
correct result : ['  x|你最近好吗', 'pun|、', '  x|最近どうですか', 'pun|？', '  x|요즘 어떻게 지내요', 'pun|？']
test result    : [' zh|你最近好吗', 'pun|、', ' ja|最近どうですか', 'pun|？', ' ko|요즘 어떻게 지내요', 'pun|？']
acc                  : 6/6
25✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: Bonjour, wie geht's dir today?
correct result : ['  x|Bonjour', 'pun|, ', "  x|wie geht's dir ", '  x|today', 'pun|?']
test result    : [' fr|Bonjour', 'pun|, ', " de|wie geht's dir ", ' en|today', 'pun|?']
acc                  : 5/5
26❌❌✅✅--------------------------------------------------------------------------------------------------
original_string: Vielen Dank merci beaucoup for your help.
correct result : ['  x|Vielen Dank ', '  x|merci beaucoup ', '  x|for your help', 'pun|.']
test result    : [' de|Vielen ', ' fr|Dank merci beaucoup ', ' en|for your help', 'pun|.']
acc                  : 2/4
27❌❌✅✅--------------------------------------------------------------------------------------------------
original_string: Ich bin müde je suis fatigué and I need some rest.
correct result : ['  x|Ich bin müde ', '  x|je suis fatigué ', '  x|and I need some rest', 'pun|.']
test result    : [' de|Ich bin müde je ', ' fr|suis fatigué ', ' en|and I need some rest', 'pun|.']
acc                  : 2/4
28✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: Ich mag dieses Buch ce livre est intéressant and it has a great story.
correct result : ['  x|Ich mag dieses Buch ', '  x|ce livre est intéressant ', '  x|and it has a great story', 'pun|.']
test result    : [' de|Ich mag dieses Buch ', ' fr|ce livre est intéressant ', ' en|and it has a great story', 'pun|.']
acc                  : 4/4
29✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: Ich mag dieses Buch, ce livre est intéressant, and it has a great story.
correct result : ['  x|Ich mag dieses Buch', 'pun|, ', '  x|ce livre est intéressant', 'pun|, ', '  x|and it has a great story', 'pun|.']
test result    : [' de|Ich mag dieses Buch', 'pun|, ', ' fr|ce livre est intéressant', 'pun|, ', ' en|and it has a great story', 'pun|.']
acc                  : 6/6
30✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: The shirt is 9.15 dollars.
correct result : ['  x|The shirt is ', 'digit|9', 'pun|.', 'digit|15 ', '  x|dollars', 'pun|.']
test result    : [' en|The shirt is ', 'digit|9', 'pun|.', 'digit|15 ', ' en|dollars', 'pun|.']
acc                  : 6/6
31✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: The shirt is 233 dollars.
correct result : ['  x|The shirt is ', 'digit|233 ', '  x|dollars', 'pun|.']
test result    : [' en|The shirt is ', 'digit|233 ', ' en|dollars', 'pun|.']
acc                  : 4/4
32✅✅✅--------------------------------------------------------------------------------------------------
original_string: lang-split
correct result : ['  x|lang', 'pun|-', '  x|split']
test result    : [' en|lang', 'pun|-', ' en|split']
acc                  : 3/3
33✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: I have 10, €
correct result : ['  x|I have ', 'digit|10', 'pun|, ', '  x|€']
test result    : [' en|I have ', 'digit|10', 'pun|, ', ' fr|€']
acc                  : 4/4
34✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 日本のメディアでは「匿名掲示板」であると紹介されることが多いが、2003年1月7日から全書き込みについてIPアドレスの記録・保存を始めており、厳密には匿名掲示板ではなくなっているとCNET Japanは報じている
correct result : ['  x|日本のメディアでは', 'pun|「', '  x|匿名掲示板', 'pun|」', '  x|であると紹介されることが多いが', 'pun|、', 'digit|2003', '  x|年', 'digit|1', '  x|月', 'digit|7', '  x|日から全書き込みについて', '  x|IP', '  x|アドレスの記録・保存を始めており', 'pun|、', '  x|厳密には匿名掲示板ではなくなっていると', '  x|CNET Japan', '  x|は報じている']
test result    : [' ja|日本のメディアでは', 'pun|「', ' ja|匿名掲示板', 'pun|」', ' ja|であると紹介されることが多いが', 'pun|、', 'digit|2003', ' ja|年', 'digit|1', ' ja|月', 'digit|7', ' ja|日から全書き込みについて', ' en|IP', ' ja|アドレスの記録・保存を始めており', 'pun|、', ' ja|厳密には匿名掲示板ではなくなっていると', ' en|CNET Japan', ' ja|は報じている']
acc                  : 18/18
35✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 日本語（にほんご、にっぽんご）は、日本国内や、かつての日本領だった国、そして国外移民や移住者を含む日本人同士の間で使用されている言語。日本は法令によって公用語を規定していないが、法令その他の公用文は全て日本語で記述され、各種法令において日本語を用いることが規定され、学校教育においては「国語」の教科として学習を行うなど、事実上日本国内において唯一の公用語となっている。
correct result : ['  x|日本語', 'pun|（', '  x|にほんご', 'pun|、', '  x|にっぽんご', 'pun|）', '  x|は', 'pun|、', '  x|日本国内や', 'pun|、', '  x|かつての日本領だった国', 'pun|、', '  x|そして国外移民や移住者を含む日本人同士の間で使用されている言語', 'pun|。', '  x|日本は法令によって公用語を規定していないが', 'pun|、', '  x|法令その他の公用文は全て日本語で記述され', 'pun|、', '  x|各種法令において日本語を用いる ことが規定され', 'pun|、', '  x|学校教育においては', 'pun|「', '  x|国語', 'pun|」', '  x|の教科として学習を行うなど', 'pun|、', '  x|事実上日本国内において唯一の公用語となっている', 'pun|。']
test result    : [' ja|日本語', 'pun|（', ' ja|にほんご', 'pun|、', ' ja|にっぽんご', 'pun|）', ' ja|は', 'pun|、', ' ja|日本国内や', 'pun|、', ' ja|かつての日本領だった国', 'pun|、', ' ja|そして国外移民や移住者を含む日本人同士の間で使用されている言語', 'pun|。', ' ja|日本は法令によって公用語を規定していないが', 'pun|、', ' ja|法令その他の公用文は全て日本語で記述され', 'pun|、', ' ja|各種法令において日本語を用いる ことが規定され', 'pun|、', ' ja|学校教育においては', 'pun|「', ' ja|国語', 'pun|」', ' ja|の教科として学習を行うなど', 'pun|、', ' ja|事実上日本国内において唯一の公用語となっている', 'pun|。']
acc                  : 28/28
36✅✅✅✅✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 日语是日本通用语及事实上的官方语言。没有精确的日语使用人口的统计，如果计算日本人口以及居住在日本以外的日本人、日侨和日裔，日语使用者应超过一亿三千万人。
correct result : ['  x|日语是日本通用语及事实上的官方语言', 'pun|。', '  x|没有精确的日语使用人口的统计', 'pun|，', '  x|如果计算日本人口以及居住在日本以外的日本人', 'pun|、', '  x|日侨和日裔', 'pun|，', '  x|日语使用者应超过一亿三千万人', 'pun|。']
test result    : [' zh|日语是日本通用语及事实上的官方语言', 'pun|。', ' zh|没有精确的日语使用人口的统计', 'pun|，', ' zh|如果计算日本人口以及居住在日本以外的日本人', 'pun|、', ' zh|日侨和日裔', 'pun|，', ' zh|日语使用者应超过一亿三千万人', 'pun|。']
acc                  : 10/10
37✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: MyGO?,你也喜欢まいご吗？
correct result : ['  x|MyGO', '  x|?,', '  x|你也喜欢', '  x|まいご', '  x|吗', 'pun|？']
test result    : [' en|MyGO', 'pun|?,', ' zh|你也喜欢', ' ja|まいご', ' zh|吗', 'pun|？']
acc                  : 6/6
38✅✅--------------------------------------------------------------------------------------------------
original_string: まいご我可太喜欢了
correct result : ['  x|まいご', '  x|我可太喜欢了']
test result    : [' ja|まいご', ' zh|我可太喜欢了']
acc                  : 2/2
39✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我的名字is小明。
correct result : ['  x|我的名字', '  x|is', '  x|小明', 'pun|。']
test result    : [' zh|我的名字', ' en|is', ' ja|小明', 'pun|。']
acc                  : 4/4
40✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我的名字は小田です。
correct result : ['  x|我的', '  x|名字は小田です', 'pun|。']
test result    : [' zh|我的', ' ja|名字は小田です', 'pun|。']
acc                  : 3/3
41✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我喜欢食べる蔬菜和水果。
correct result : ['  x|我喜欢', '  x|食べる', '  x|蔬菜和水果', 'pun|。']
test result    : [' zh|我喜欢', ' ja|食べる', ' zh|蔬菜和水果', 'pun|。']
acc                  : 4/4
42✅✅✅--------------------------------------------------------------------------------------------------
original_string: 食べる蔬菜和水果我喜欢。
correct result : ['  x|食べる', '  x|蔬菜和水果我喜欢', 'pun|。']
test result    : [' ja|食べる', ' zh|蔬菜和水果我喜欢', 'pun|。']
acc                  : 3/3
43✅✅--------------------------------------------------------------------------------------------------
original_string: 寿司和蔬菜我都喜欢。
correct result : ['  x|寿司和蔬菜我都喜欢', 'pun|。']
test result    : [' zh|寿司和蔬菜我都喜欢', 'pun|。']
acc                  : 2/2
44✅✅✅--------------------------------------------------------------------------------------------------
original_string: すし和蔬菜我都喜欢。
correct result : ['  x|すし', '  x|和蔬菜我都喜欢', 'pun|。']
test result    : [' ja|すし', ' zh|和蔬菜我都喜欢', 'pun|。']
acc                  : 3/3
45✅✅✅--------------------------------------------------------------------------------------------------
original_string: 寝る和蔬菜我都喜欢。
correct result : ['  x|寝る', '  x|和蔬菜我都喜欢', 'pun|。']
test result    : [' ja|寝る', ' zh|和蔬菜我都喜欢', 'pun|。']
acc                  : 3/3
46✅✅--------------------------------------------------------------------------------------------------
original_string: 料理私は大好きです。
correct result : ['  x|料理私は大好きです', 'pun|。']
test result    : [' ja|料理私は大好きです', 'pun|。']
acc                  : 2/2
47❌❌✅--------------------------------------------------------------------------------------------------
original_string: 游戏大好きです。
correct result : ['  x|游戏', '  x|大好きです', 'pun|。']
test result    : [' zh|游戏大好', ' ja|きです', 'pun|。']
acc                  : 1/3
48❌❌✅--------------------------------------------------------------------------------------------------
original_string: 游戏面白いです。
correct result : ['  x|游戏', '  x|面白いです', 'pun|。']
test result    : [' zh|游戏面', ' ja|白いです', 'pun|。']
acc                  : 1/3
49✅✅✅✅✅✅--------------------------------------------------------------------------------------------------
original_string: 初次见面，私の名前はDoodleです。
correct result : ['  x|初次见面', 'pun|，', '  x|私の名前は', '  x|Doodle', '  x|です', 'pun|。']
test result    : [' zh|初次见面', 'pun|，', ' ja|私の名前は', ' en|Doodle', ' ja|です', 'pun|。']
acc                  : 6/6
50✅✅--------------------------------------------------------------------------------------------------
original_string: 中国語と日本語のミックス中文和日文的混合
correct result : ['  x|中国語と日本語のミックス', '  x|中文和日文的混合']
test result    : [' ja|中国語と日本語のミックス', ' zh|中文和日文的混合']
acc                  : 2/2
51✅✅--------------------------------------------------------------------------------------------------
original_string: 真的很难分离玉子焼き
correct result : ['  x|真的很难分离', '  x|玉子焼き']
test result    : [' zh|真的很难分离', ' ja|玉子焼き']
acc                  : 2/2
52✅✅✅--------------------------------------------------------------------------------------------------
original_string: 真的很难分离すしリンゴ苹果
correct result : ['  x|真的很难分离', '  x|すしリンゴ', '  x|苹果']
test result    : [' zh|真的很难分离', ' ja|すしリンゴ', ' zh|苹果']
acc                  : 3/3
53❌--------------------------------------------------------------------------------------------------
original_string: 全是汉字很难分离果物苹果
correct result : ['  x|全是汉字很难分离', '  x|果物', '  x|苹果']
test result    : [' zh|全是汉字很难分离果物苹果']
acc                  : 0/3
54✅✅--------------------------------------------------------------------------------------------------
original_string: 寂しい的人
correct result : ['  x|寂しい', '  x|的人']
test result    : [' ja|寂しい', ' zh|的人']
acc                  : 2/2
55✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我的姓名は爱音
correct result : ['  x|我的姓名', '  x|は', '  x|爱音']
test result    : [' zh|我的姓名', ' ja|は', ' zh|爱音']
acc                  : 3/3
56✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我的名前は爱音
correct result : ['  x|我的', '  x|名前は', '  x|爱音']
test result    : [' zh|我的', ' ja|名前は', ' zh|爱音']
acc                  : 3/3
57✅✅✅--------------------------------------------------------------------------------------------------
original_string: 我的名字は爱音
correct result : ['  x|我的', '  x|名字は', '  x|爱音']
test result    : [' zh|我的', ' ja|名字は', ' zh|爱音']
acc                  : 3/3
58✅❌❌--------------------------------------------------------------------------------------------------
original_string: 我的名前是爱音
correct result : ['  x|我的', '  x|名前', '  x|是爱音']
test result    : [' zh|我的', ' ja|名前是', ' zh|爱音']
acc                  : 1/3
total substring num: 296
test total substring num: 295
text acc num: 276
precision: 0.9324324324324325
recall: 0.9355932203389831
F1 Score: 0.9340101522842641
time: 0.07000231742858887
process speed char/s: 4228.431441601302
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

- [Update History](#update-history)
  - [v2.1.1](#v211)
  - [v2.1.0](#v210)
    - [before](#before)
    - [after](#after)
    - [All Test Results (Execute `python .\tests\split_acc.py` to obtain)](#all-test-results-execute-python-testssplit_accpy-to-obtain)
  - [v2.0.6](#v206)
    - [before](#before-1)
    - [after](#after-1)
    - [All test results](#all-test-results)
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

---

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
- Language detection depends on [zafercavdar/fasttext-langdetect](https://github.com/zafercavdar/fasttext-langdetect)

# 5. ✨Star History

[![Star History Chart](https://api.star-history.com/svg?repos=DoodleBears/split-lang&type=Timeline)](https://star-history.com/#DoodleBears/split-lang&Timeline)
