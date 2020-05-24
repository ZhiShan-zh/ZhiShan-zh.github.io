# Shell编程基础知识

# 1 Shell变量


## 1.1 定义


是shell传递数据的一种方法，用来代表每个取值的符号名。


## 1.2 分类


- 临时变量
  - 是shell程序内部定义的，其使用范围仅限于定义它的程序，对其它程序不可见。包括：
    - 用户自定义变量
    - 位置变量
- 永久变量
  - 是环境变量，其值不随shell脚本的执行结束而消失。



## 1.3 永久变量


```shell
[zh@zh-pc ~]$ echo $LANG
en_US.utf8
[zh@zh-pc ~]$ echo $PATH
/home/zh/.nvm/versions/node/v8.16.2/bin:/home/zh/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl
```


## 1.4 自定义变量


- 用户定义的变量由字母或下划线开头，由字母、数字或下划线序列组成，并且大小写字母意义不同。
- 变量名长度没有限制。
- 在使用变量值时，要在变量名前加前缀`$`。
- 一般变量使用大写字母表示，并且是英文字母开头，赋值号`=`两边没有空格，如`NUM=5`、`STR="A String"`。
- 可以将一个命令的执行结果赋值给变量，但是需要使用命令替换符号（`）。
```shell
[zh@zh-pc ~]$ ls
dapps    Documents  logs   Pictures  Public     Videos
Desktop  Downloads  Music  Postman   Templates
[zh@zh-pc ~]$ LS=`ls`
[zh@zh-pc ~]$ echo $LS
dapps Desktop Documents Downloads logs Music Pictures Postman Public Templates Videos
```

- 注意单引号和双引号的区别：
  - 双引号（""）会把里边的变量值进行输出。
  - 单引号（''）会把内容原封不动输出，不会识别里边的变量。
```shell
[zh@zh-pc ~]$ STR="string"
[zh@zh-pc ~]$ echo "I am $STR"
I am string
[zh@zh-pc ~]$ echo 'I am $STR'
I am $STR
```

- 使用`set`命令查看所有变量。
- 使用`unset`命令删除指定的变量。
```shell
[zh@zh-pc ~]$ NUM=5
[zh@zh-pc ~]$ echo $NUM
5
[zh@zh-pc ~]$ unset NUM
[zh@zh-pc ~]$ echo $NUM

[zh@zh-pc ~]$
```


## 1.5 占位变量


位置变量：`sh test.sh test1 test2 test3 ... testn`


- n<=9时，在代码里使用`$1 ... $9`进行替代



shell脚本：`test.sh`


```shell
#!/bin/sh
DATE=`/bin/date +%Y%m%d`
echo "TODAY IS $DATE"
/bin/ls -l $1
/bin/ls -l $2
/bin/ls -l $3
```


执行`test.sh`：


```shell
[zh@zh-pc test]$ ls
test1  test2  test3  test.sh
[zh@zh-pc test]$ sh test.sh test1 test2 test3
total 0
drwxrwxrwx 1 zh zh 0  3月 20 15:56 test1_1
drwxrwxrwx 1 zh zh 0  3月 20 15:56 test1_2
-rwxrwxrwx 1 zh zh 0  3月 20 15:58 test1_3.txt
total 0
drwxrwxrwx 1 zh zh 0  3月 20 15:58 test2_1
-rwxrwxrwx 1 zh zh 0  3月 20 15:58 test2_2.txt
total 0
drwxrwxrwx 1 zh zh 0  3月 20 15:59 test3_1
-rwxrwxrwx 1 zh zh 0  3月 20 15:58 test3_2.txt
```


如果超过9个参数，可以用 `${n}` 获取第n个参数：
如果n>=10， `$n` 也没问题，但最好不这么用。
```shell
#！/bin/bash

echo "第一个参数$1"
echo "第一个参数$2"
echo "第一个参数$3"
echo "第一个参数$4"
echo "第一个参数$5"
echo "第一个参数$6"
echo "第一个参数$7"
echo "第一个参数$8"
echo "第一个参数$9"
echo "第一个参数${10}"
echo "第一个参数${11}"
```


## 1.6 特殊变量


- `$*`：这个程序的所有参数
- `$#`：这个程序的参数个数
- `$$`：这个程序的PID
- `$!`：执行上一个后台命令的PID
- `$?`：执行上一个命令的返回值
- `$(0-9)`：显示位置变量



示例脚本：`test.sh`


```shell
#!/bin/sh
DATE=`/bin/date +%F`
echo "today is $DATE"
echo '$#：' $#
echo '$*：' $*
echo '$?：' $?
echo '$$：' $$
echo '$0：' $0
```


执行`test.sh`：


```shell
[zh@zh-pc test]$ sh test.sh /aa /bb /cc
today is 2020-03-20
$#： 3
$*： /aa /bb /cc
$?： 0
$$： 12214
$0： test.sh
```


## 1.7 read，键盘录入

`read`：从键盘读入数据，赋值给变量


shell脚本：`test.sh`


```shell
#!/bin/sh
read f s t
echo "the first is $f"
echo "the second is $s"
echo "the third is $t"
```


运行`test.sh`：


```shell
[zh@zh-pc test]$ sh test.sh
10 20 30
the first is 10
the second is 20
the third is 30
[zh@zh-pc test]$ sh -x test.sh
+ read f s t
10 20 30
+ echo 'the first is 10'
the first is 10
+ echo 'the second is 20'
the second is 20
+ echo 'the third is 30'
the third is 30
```


**注释：**


- `-x`：表示跟踪



# 2 Shell的运算


## 2.1 expr

`expr`命令，表示对整数进行运算


1. expr的运算必须用空格间隔开
1. `\`：转移字符
1. 保持先算乘除再算加减，如果需要优先运算则需要加命令替换符
1. 也可以对变量进行运算操作



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


# 3 测试命令


使用`test`命令可以对文件、字符串等进行测试，一般配合控制语句是用，不应该单独使用。


## 3.1 字符串测试


- `test str1=str2`：测试字符串是否相等
- `test str1!=str2`：测试字符串是否不相等
- `test str`：测试字符串是否不为空
- `test -n str`：测试字符串是否不为空
- `test -z str`：测试字符串是否为空



## 3.2 int测试


- `test int1 -eq int2`：测试整数是否相等
- `test int1 -ne int2`：测试整数是否不相等
- `test int1 -ge int2`：测试int1是否>=int2
- `test int1 -gt int2`：测试int1是否>int2
- `test int1 -le int2`：测试int1是否<=int2
- `test int1 -lt int2`：测试int1是否<int2



## 3.3 文件测试


- `test -d file`：判断指定文件是否为目录
- `test -f file`：判断指定文件是否为常规文件
- `test -x file`：判断指定文件是否可执行
- `test -r file`：判断指定文件是否为可读
- `test -w file`：判断指定文件是否为可写
- `test -a file`：判断指定文件是否为存在
- `test -s file`：判断指定文件大小是否非0



# 4 判断语句


## 4.1 if语句


语法格式：`if test -d $1 then ... else ...fi`


变量测试语句可用`[]`进行简化，如`test -d $1`等价于`[ -d $1 ]`


注意：`["空格"-d $1"空格"]`


脚本：`test.sh`


```shell
#!/bin/sh
# if test $1 then ... else ... fi
if [ -d $1 ]
then
	echo "this is a directory!"
else
	echo "this is not a directory!"
fi
```


执行`test.sh`：


```shell
[zh@zh-pc test]$ sh test.sh test
this is not a directory!
```


## 4.2 if elif语句


语法格式：


```shell
if [ -d $1 ]
then ...
elif [-f $1 ]
	then ...
else ...
fi
```


脚本：`test.sh`


```shell
#!/bin/sh
# if test $1 then ... else ... fi
if [ -d $1 ]
then
	echo "this is a directory!"
elif [ -d $1 ]
	then 
		echo "this is not a directory!"

else
	echo "error!"
fi
```


## 4.3 case语句


格式：


```shell
case 变量 in
	字符串 1) 命令列表1;;
	...
	字符串 n) 命令列表n;;
esac
```


脚本：`test.sh`


```shell
#!/bin/sh
read op
case $op in
	a)
	echo "you selected a";;
	b)
	echo "you selected b";;
	c)
	echo "you selected c";;
	*)
	echo "error"
esac
```


执行脚本：


```shell
[zh@zh-pc test]$ sh test.sh
a
you selected a
```


# 5 逻辑与和逻辑或


我们使用`-a`和`-o`表示逻辑与和逻辑或。


```shell
#!/bin/sh
# -a -o
if [ $1 -eq $2 -a $1 = 1 ]
then
	echo "param1 == param2 and param1 = 1"
elif [ $1 -ne $2 -o $1 = 2 ]
	then 
		echo "param1 != param2 or param1 =2"

else
	echo "others"
fi
```


# 6 循环


## 6.1 for循环（名字列表循环）


`for ... done`语句格式：


```shell
for 变量 in 名字表
do
	命令列表
done
```


脚本：`test.sh`


```shell
#!/bin/sh
# for var in [params] do ... done
for var in 1 2 3 4 5 6 7 8 9 10
do
	echo "number is saver"
done
```


## 6.2 select循环


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


## 6.3 while循环


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


## 6.4 break和continue


脚本：`test.sh`


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


测试脚本：`test.sh`


```shell
[zh@zh-pc test]$ sh test.sh
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
