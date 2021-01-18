# 语义分析

**语义分析**是把分析得到句法成分与应用领域中的目标表示相关联。

句法分析后还不能理解所分析的句子，至少还需要进行语义分析。简单的做法是依次使用独立的句法分析程序和语义解释程序。但这样做使得句法分析和语义分析相分离，在很多情况下无法决定句子的结构。扩充转移网络ATN允许把语义分析加进句法分析，并充分支持语义解释。

# 1 语义文法

**语义文法**是将文法知识和语义知识组合起来，以统一的方式定义为文法规则集。

语义文法是**上下文无关的**，形态上与面向自然语言的常见文法相同，只是不采用NP、VP及PP等表示句法成分的非终止符，而是**使用能表示语义类型的符号，从而可以定义包含语义信息的文法规则**。

下面给出一个关于舰船信息的例子，可以看出语义文法在语义分析中的作用：
$$
\begin{array}{l}
S & \rightarrow PRESENT \quad the \quad ATTRIBUTE \quad of \quad SHIP \\
PRESENT & \rightarrow What \quad is|can \quad you \quad tell \quad me \\
ATTRIBUTE & \rightarrow length|class \\
SHIP & \rightarrow the SHIPNAME | CLASSNAME \quad class \quad ship \\
SHIPNAME & \rightarrow Huanghe|Changjiang \\
CLASSNAME & \rightarrow carrier | submarine
\end{array}
$$
说明：

- 用全是大写的英文字母表示的单词代表非终止符，用全是小写的英文字母表示的单词代表终止符。