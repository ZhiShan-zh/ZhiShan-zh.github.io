# 自然语言理解概述

# 1 自然语言理解的概念

从微观角度，自然语言理解是指从自然语言到机器内部的一个映射。

从宏观角度，自然语言理解是指机器能够执行人类所期望的某种语言功能。这些功能主要包括如下几个方面：

- 回答问题：计算机能正确地回答用自然语言输入的有关问题。
- 文摘生成：机器能产生输入文本的摘要。
- 释义：机器能用不同的词语和句型来复述输入的自然语言信息。
- 翻译：机器能把一种语言翻译成另外一种语言。

# 2 语言处理过程的层次

语言虽然表示成一串文字符号或一串声音流，但其内部是一个层次化的结构，从语言的构成中就可以清楚地看出这种层次性。

- 文字表达的句子的层次：词素-->词或词形-->词组或句子

- 声音表达的句子的层次：音素-->音节-->音词-->音句

其中每个层次都受到文法规则的制约。因此，语言的处理过程也应当是一个层次化的过程。

语言处理过程的层次：

- **语音分析**：（可选：如果接收到的是语音流的话。）
  - 音素：构成单词发音的最小独立单元。
  - 对于一种语言，例如英语，必须将声音的不同单元识别出来并分组。在分组时，应该确保语言中的所有单词都能被划分，两个不同的单词最好由不同的音素组成。
- **词法分析**
- **句法分析**
- **语义分析**
- **语用分析**：（可选：对于更高层次的语言处理）
  - 语用分析就是研究语言所存在的外界环境对语言使用所产生的影响。

虽然这样划分的层次之间并非是完全的隔离的，但这种层次化的划分更好地体现了语言本身的构成，并在一定程度上使得自然语言处理系统的模块化成为可能。

**音素可能由于上下文不同而发音不同**。例如，单词three中音素th的发音不同于then中的th。相同音素的这些不同变异称为**音素变体**。有时，抽取读音的差别将其归入音位的通用分组中是很方便的。音位写在斜线中间，例如：/th/是一个音位，一句上下文的不同而有不同读音。单词可以在音位层表示，若需要更多信息，可在音素变体层表示。

**语音分析就是根据音位规则，从语音流中区分出一个个独立的音素，再根据音位形态规则找出一个个音节及其对应的词素或词。**

语音分析过程：词语以声波传送。语音分析系统传送声波这种模拟信号，并从中抽取诸如能量、频率等特征。然后，将这些特征映射为称为音素的单个语音单元。最后将音素序列转换成单词序列。

语音的产生：将单词映射为音素序列，然后传送给语音合成器，单词的声音通过说话者从语音合成器发出。