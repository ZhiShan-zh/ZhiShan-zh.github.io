# 流程控制——Shell

# 1 判断语句

## 1.1 if语句

### 1.1.1 if语法

#### 1.1.1.1 if语法格式

```shell
if condition
then
	command1
	command2
	# 省略N行代码
	commandN
fi    
```

#### 1.1.1.2 if else 语法格式

```shell
if condition
then
	command1_1
	command1_2
	# 省略N行代码
	command1_N
else
	command2_1
	command2_2
	# 省略N行代码
	command2_N
fi 
```

#### 1.1.1.3 if elif else 语法格式

```shell
if condition1
then
	command1_1
	command1_2
	# 省略N行代码
	command1_N
elif condition2
then
	command2_1
	command2_2
	# 省略N行代码
	command2_N
else
	command3_1
	command3_2
	# 省略N行代码
	command3_N
fi 
```

### 1.1.2 判断条件语法

#### 1.1.2.1 `test`&`[]`

- 在命令行里`test expr`和`[ expr ]`的效果相同；
  - `test`的语法参看`test`相应部分。
- 基本作用是判断文件、判断字符串、判断整数。
- 支持使用 ”与或非“ 将表达式连接起来。
- 比较运算符只有`==`和`!=`，两者都是用于字符串比较的，不可用于整数比较，整数比较只能使用`-eq`, `-gt`这种形式。
- 对于字符串判断，如果需要使用大于号（`>`）和小于号（`<`）形式，需要配合转义字符使用。
  - `if [ "ab" \< "dc" ]; then echo "1"; fi`
  - 如果使用`[[]]`，则不需要转义字符，如：`if [[ "ab" < "dc" ]]; then echo "1"; fi`
- 对于整数判断，如果需要使用大于号（`>`）和小于号（`<`）形式，需要使用双括号形式`(())`
  - `if (( 3 > 2 )); then echo "1"; fi`
  - 此中情况，还可以使用大于等于`>=`，小于等于`<=`，如`if (( 3 >= 2 )); then echo "1"; fi`
- 多条件判断可以使用`&&`、`||`，也可以使用`-a`、`-o`
  - `a=3; if [ $a != 1 ] && [ $a != 2 ]; then echo "1"; fi`
  - `a=3; if [ $a != 1 -a $a != 2 ]; then echo "1"; fi`

#### 1.1.2.2 `[[ ]]`

- `[[`是 bash 程序语言的关键字。并不是一个命令，`[[ ]]`结构比`[ ]`结构更加通用。在`[[`和`]]`之间所有的字符都不会发生文件名扩展或者单词分割，但是会发生参数扩展和命令替换。
- 字符串比较使用`=~`时可以把右边的作为一个模式，而不仅仅是一个字符串（这是右边的字符串不加双引号的情况下。如果右边的字符串加了双引号，则认为是一个文本字符串。）如：`if [[ zhishan =~ zhi? ]]; then echo "1"; fi`
  - `[[ ]]`中匹配字符串或通配符，不需要引号。
- 使用`[[  ]]`条件判断结构，而不是`[  ]`，能够防止脚本中的许多逻辑错误。比如，`&&`、`||`、`<`和`>` 操作符能够正常存在于`[[ ]]`条件判断结构中，但是如果出现在`[ ]`结构中的话，会报错。
  - 比如可以直接使用`a=3; if [[ $a != 1 && $a != 2 ]]; then echo "1"; fi`
  - 其实如果使用`[]`，也可以使用，如`a=3; if [ $a != 1 ] && [ $a != 2 ]; then echo "1"; fi`，或`a=3; if [ $a != 1 -a $a != 2 ]; then echo "1"; fi`
  - `[[ ... && ... && ... ]]` 和 `[ ... -a ... -a ...]`  不一样，`[[ ]]`是逻辑短路操作，而`[ ]`不会进行逻辑短路。

## 1.2 case语句

```shell
case 值 in
模式1)
    command1
    command2
    ...
    commandN
    ;;
模式2）
    command1
    command2
    ...
    commandN
    ;;
esac
```

- Shell case语句为多选择语句。可以用case语句匹配一个值与一个模式，如果匹配成功，执行相匹配的命令。
- 取值后面必须为单词`in`，每一模式必须以右括号结束。取值可以为变量或常数。匹配发现取值符合某一模式后，其间所有命令开始执行直至`;;`。
- 取值将检测匹配的每一个模式。一旦模式匹配，则执行完匹配模式相应命令后不再继续其他模式。如果无一匹配模式，使用星号`*`捕获该值，再执行后面的命令。

# 2 循环语句

## 2.1 for循环

### 2.1.1 基本使用

语法格式：

```shell
for 变量 in 名字表
do
	命令列表
done
```

示例：

```shell
#!/bin/bash
for var in 1 2 3 4 5 6 7 8 9 10
do
	echo "number is $var"
done
```

输出：

```
number is 1
number is 2
number is 3
number is 4
number is 5
number is 6
number is 7
number is 8
number is 9
number is 10
```



```shell
#!/bin/bash
for str in "This is a string"
do
    echo $str
    echo "-"
done
```

输出：

```
This is a string
-
```

### 2.1.2 无限循环

语法：

```shell
for (( ; ; ))
do
	commad
done
```

示例：

```shell
#!/bin/sh
for (( ; ; ))
do
	echo 1
done
```

## 2.2 select循环

格式：


```shell
select 变量 in 列表
do
	cmd...
done
```


脚本：`test.sh`


```shell
#!/bin/sh
# select var in [params] do ... done
select var in "java" "C++" "php" "linux" "ruby" "python" "C#"
do
	break
done
echo "you selected $var"
```


执行`test.sh`：


```shell
[zh@zh-pc test]$ sh test.sh
1) java
2) C++
3) php
4) linux
5) ruby
6) python
7) C#
#? 6
you selected python
```

## 2.3 while循环

### 2.3.1 基本使用

格式：


```shell
while 条件
do
	命令
done
```


脚本：`test.sh`


```shell
#!/bin/sh
# while test do ... done
num=1
sum=0
while [ $num -le 100 ]
do
	sum=`expr $sum + $num`
	num=`expr $num + 1`
done
# 可以休眠
sleep 5
echo $sum
```

输出：5050

### 2.3.2 无限循环

格式：

```shell
while :
do
    command
done
```

或

```shell
while true
do
    command
done
```

示例：

```shell
#!/bin/sh
while :
do
	echo 1
done
```

## 2.4 until循环

语法格式：

```shell
until condition
do
    command
done
```

- until 循环执行一系列命令直至条件为 true 时停止。
- until 循环与 while 循环在处理方式上刚好相反。
- 一般 while 循环优于 until 循环，但在极少数情况下，until 循环更加有用。
- condition 一般为条件表达式，如果返回值为 false，则继续执行循环体内的语句，否则跳出循环。

示例：

```shell
#!/bin/sh
num=100
until [ $num -lt 95 ]
do
   echo $num
   num=`expr $num - 1`
done
```

输出：

```
100
99
98
97
96
95
```

## 2.5 跳出循环

- break命令允许跳出所有循环（终止执行后面的所有循环）
- continue命令与break命令类似，只有一点差别，它不会跳出所有循环，仅仅跳出当前循环。

示例：

```shell
#!/bin/sh
i=0
while [ $i -le 100 ]
do
	i=`expr $i + 1`
	if [ $i -eq 5 -o $i -eq 10 ]
		then continue;
	else
		echo "this number is $i"
	fi

	if [ $i -eq 15 ]
		then break;
	fi
done
```

输出：

```
this number is 1
this number is 2
this number is 3
this number is 4
this number is 6
this number is 7
this number is 8
this number is 9
this number is 11
this number is 12
this number is 13
this number is 14
this number is 15
```

