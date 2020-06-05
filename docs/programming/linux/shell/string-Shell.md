# 字符串——Shell

# 1 概述

- 字符串是shell编程中最常用最有用的数据类型（除了数字和字符串，也没啥其它类型好用了）。

- 字符串可以用单引号，也可以用双引号，也可以不用引号。
- 如：`str='zhishan'`或``str="zhishan"``或`str=zhishan`。

# 2 双引号和单引号

**单引号字符串的限制**：

- 单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的；
- 单引号字串中不能出现单独一个的单引号（对单引号使用转义符后也不行），但可成对出现，作为字符串拼接使用。

**双引号的优点**：

- 双引号里可以有变量；
- 双引号里可以出现转义字符。

示例：

```shell
[zh@zh-pc ~]$ STR="string"
[zh@zh-pc ~]$ echo "I am $STR"
I am string
[zh@zh-pc ~]$ echo 'I am $STR'
I am $STR
```

```shell
[zh@zh-inspironn4050 test]$ str='zhi\'shan''
[zh@zh-inspironn4050 test]$ echo $str 
zhi\shan
```

# 3 拼接字符串

```shell
#!/bin/bash
str="zhishan"
echo "hello $str"
echo "hello "$str""
echo "hello ${str}"
echo
echo 'hello $str'
echo 'hello '$str''
echo 'hello ${str}'
```

输出：

```
hello zhishan
hello zhishan
hello zhishan

hello $str
hello zhishan
hello ${str}
```

# 4 获取字符串长度

```shell
#!/bin/bash
str="zhishan"
echo ${#str}
```

输出：7

# 5 提取子字符串

```shell
#!/bin/bash
str="zhishan"
echo ${str:3}
echo ${str:3:2}
```

输出：

```
shan
sh
```

# 6 查找子字符串

参见expr中index相关内容：获取子串中任一字符在字符串中第一次出现的位置。

```shell
#!/bin/bash
str="zhishan"
echo `expr index $str ha`
```

输出：2

# 7 分割字符串为数组

要将字符串列表转变为数组，只需要在前面加()，所以关键是将分隔符转变为空格分隔，常见方法如下：

##  7.1 使用`{str//,/}`

```shell
[zh@zh-inspironn4050 ~]$ str="ONE,TWO,THREE,FOUR"
[zh@zh-inspironn4050 ~]$ arr=(${str//,/ })
[zh@zh-inspironn4050 ~]$ echo ${arr[@]}
ONE TWO THREE FOUR
```

## 7.2 使用tr命令

```shell
[zh@zh-inspironn4050 ~]$ str="ONE,TWO,THREE,FOUR"
[zh@zh-inspironn4050 ~]$ arr=(`echo $str | tr ',' ' '`)
[zh@zh-inspironn4050 ~]$ echo ${arr[@]}
ONE TWO THREE FOUR
```

或

```shell
[zh@zh-inspironn4050 ~]$ str="ONE,TWO,THREE,FOUR"
[zh@zh-inspironn4050 ~]$ arr=(`tr ',' ' ' <<< $str`)
[zh@zh-inspironn4050 ~]$ echo ${arr[@]}
ONE TWO THREE FOUR
```

## 7.3 使用awk命令

```shell
[zh@zh-inspironn4050 ~]$ str="ONE,TWO,THREE,FOUR"
[zh@zh-inspironn4050 ~]$ arr=($(echo $str | awk 'BEGIN{FS=",";OFS=" "} {print $1,$2,$3,$4}'))
[zh@zh-inspironn4050 ~]$ echo ${arr[@]}
ONE TWO THREE FOUR
```

## 7.4 使用IFS分隔符

```shell
[zh@zh-inspironn4050 ~]$ str="ONE,TWO,THREE,FOUR"
[zh@zh-inspironn4050 ~]$ IFS=","
[zh@zh-inspironn4050 ~]$ arr=($str)
[zh@zh-inspironn4050 ~]$ echo ${arr[@]}
ONE TWO THREE FOUR
```

