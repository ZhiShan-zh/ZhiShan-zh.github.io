# 变量——Shell


# 1 定义


是shell传递数据的一种方法，用来代表每个取值的符号名。


# 2 分类


- 临时变量
  - 是shell程序内部定义的，其使用范围仅限于定义它的程序，对其它程序不可见。包括：
    - 用户自定义变量
    - 位置变量
- 永久变量
  - 是环境变量，其值不随shell脚本的执行结束而消失。



# 3 永久变量


```shell
[zh@zh-pc ~]$ echo $LANG
en_US.utf8
[zh@zh-pc ~]$ echo $PATH
/home/zh/.nvm/versions/node/v8.16.2/bin:/home/zh/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl
```


# 4 自定义变量


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


# 5 占位变量


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

如果超过9个参数，可以用 `${n}` 获取第n个参数：
如果n>=10， `$n` 也没问题，但最好不这么用。

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


# 6 特殊变量


- `$*`：这个程序的所有参数
- `$#`：这个程序的参数个数
- `$$`：这个程序的PID
- `$!`：执行上一个后台命令的PID
- `$?`：执行上一个命令的返回值
- `$(0-n)`：显示位置变量



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


# 7 read，键盘录入

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