# expr

# 1 概述

expr命令可以实现数值运算、数值或字符串比较、字符串匹配、字符串提取、字符串长度计算等功能。它还具有几个特殊功能，判断变量或参数是否为整数、是否为空、是否为0等。

语法：`expr 表达式`

表达式说明：

1. expr的运算必须用空格间隔开每个项
1. `\`：转移字符
1. 保持先算乘除再算加减，如果需要优先运算则需要加命令替换符
1. 也可以对变量进行运算操作

# 2 字符表达式

## 2.1 模式匹配

语法：`expr match STRING REGEX`或`expr STRING : REGEX`

参数说明：

- STRING：待匹配字符串
- REGEX：正则表达式(GNU基本正则)，它默认会隐含前缀"^"。

如果匹配成功，且REGEX使用了'\('和'\)'，则此表达式返回匹配到的，如果未使用'\('和'\)'，则返回匹配的字符数。

如果匹配失败，如果REGEX中使用了'\('和'\)'，则此表达式返回空字符串，否则返回为0。

只有第一个'\(...\)'会引用返回的值；其余的'\(...\)'只在正则表达式分组时有意义。

示例：

```shell
[zh@zh-inspironn4050 ~]$ expr zhishan : 'zh\(.*\)'
ishan
[zh@zh-inspironn4050 ~]$ expr zhishan : 'zh.*'
7
[zh@zh-inspironn4050 ~]$ expr zhishan : 'zh.'
3
[zh@zh-inspironn4050 ~]$ expr zhishan : 'sh.'
0
```

## 2.2 抓取子串

语法：`expr substr STRING POSITION LENGTH`

返回STRING字符串中从POSITION开始，长度最大为LENGTH的子串。如果POSITION或LENGTH为负数，0或非数值，则返回空字符串。

示例：

```shell
[zh@zh-inspironn4050 ~]$ expr substr zhishan 2 5
hisha
[zh@zh-inspironn4050 ~]$ expr substr zhishan 2 0

[zh@zh-inspironn4050 ~]$ expr substr zhishan 2 -1
```

## 2.3 获取子串任一个字符在字符串的位置

语法：`expr index STRING CHARSET`

CHARSET中**任意单个字符**在STRING中最前面的字符位置。如果在STRING中完全不存在CHARSET中的字符，则返回0。见后文示例。如果在STRING中完全不存在CHARSET中的字符，则返回0。

示例：

```shell
[zh@zh-inspironn4050 ~]$ expr index zhishan sh
2
[zh@zh-inspironn4050 ~]$ expr index zhishan 12
0
[zh@zh-inspironn4050 ~]$ expr index zhishan hs
2
```

## 2.4 计算字符串的长度

语法：`expr length STRING`

计算字符串STRING的长度并返回。

示例：

```shell
[zh@zh-inspironn4050 ~]$ expr length zhishan
7
[zh@zh-inspironn4050 ~]$ expr length 12345678
8
[zh@zh-inspironn4050 ~]$ str="zhishan"
[zh@zh-inspironn4050 ~]$ expr length $str
7
```

# 3 算术表达式

```shell
[zh@zh-pc test]$ expr 10 + 5
15
[zh@zh-pc test]$ expr 10 - 5
5
[zh@zh-pc test]$ expr 10 / 3
3
[zh@zh-pc test]$ expr 10 \* 3
30
[zh@zh-pc test]$ expr 10 - 3 \* 2
4
[zh@zh-pc test]$ expr `expr 10 - 3` \* 2
14
[zh@zh-pc test]$ NUM=30
[zh@zh-pc test]$ echo `expr $NUM + 8`
38
```

# 4 逻辑关系表达式

- `'|'`：如果第一个参数非空且非0，则返回第一个参数的值，否则返回第二个参数的值，但要求第二个参数的值也是非空或非0，否则返回0。如果第一个参数是非空或非0时，不会计算第二个参数。

- `'&'`：如果两个参数都非空且非0，则返回第一个参数，否则返回0。如果第一个参为0或为空，则不会计算第二个参数。

- `'<'`、`'<='`、`'='`、`'=='`、`'!='`、`'>='`、`'>'`：
  - 比较两端的参数，如果为true，则返回1，否则返回0。
  - `"=="`是`"="`的同义词。
  - "expr"首先尝试将两端参数转换为整数，并做算术比较，如果转换失败，则按字符集排序规则做字符比较。

示例：

```shell
[zh@zh-inspironn4050 ~]$ expr zhishan '|' 0
zhishan
[zh@zh-inspironn4050 ~]$ expr zhishan '&' 0
0
[zh@zh-inspironn4050 ~]$ expr zhishan '&' zh
zhishan
```

