# `()`、`(())`以及`{}`

# 1 小括号`()`

- **命令组**
  - 括号中的命令将会新开一个子shell进行中顺序执行，所以括号中的变量不能够被脚本余下的部分使用，因为子Shell执行完毕后子Shell进行就会被销毁，环境副本也会消失。括号中多个命令之间用分号隔开，最后一个命令可以没有分号，各命令和括号之间不必有空格。
  - 例如：`(ls;pwd)`
  - `{ command1;command2;}`为代码块，又被称为内部组，这个结构事实上创建了一个匿名函数 。
    - 与小括号中的命令不同，大括号内的命令不会新开一个子shell运行，即脚本余下部分仍可使用括号内变量。括号内的命令间用分号隔开，最后一个也必须有分号。`{}`的第一个命令和左括号之间必须要有一个空格。
    - 如：`{ ls;pwd;}`或`{ ls;pwd; }`
    - 使用`{}`比使用`()`更受欢迎，并且`{}`的进行速度更快，占用的内存更少。

- **命令替换**
  - 等同于`command`，shell扫描一遍命令行，发现了`$(command)`结构，便将`$(command)`中的command执行一次，得到其标准输出，再将此输出放到原来命令。有些shell不支持，如`tcsh`。

- **初始化数组**
  - 如：`array=(a b c d)`

# 2 双小括号`(( ))`

- **整数扩展**：`(( ))`及`[[ ]] `分别是`[ ]`的针对数学比较表达式和字符串表达式的加强版。

  - `[[ ]]`中增加模式匹配特效；

  - `(( ))`不需要再将表达式里面的大小于符号转义，除了可以使用标准的数学运算符外，还增加了以下符号：
    - `val++`、`++val`、`val--`、`--val`：后增、先增、先减、后减；
    - `!`：逻辑求反；
    - `~`：位求反；
    - `**`：幂运算；
    - `<<`、`>>`：左位移、右位移；
    - `&`、`|`：位布尔和、位布尔或；
    - `&&`、`||`：逻辑和、逻辑或；
  - 如：`echo $((1>0)) `，输出：1
  - bash只能作整数运算，对于浮点数是当作字符串处理的。

- 只要括号中的运算符、表达式符合C语言运算规则，都可用在`$((exp))`中，甚至是三目运算符。
  - `echo $((1>0?1:2)) `，输出：1
- 在作不同进位（如二进制、八进制、十六进制）运算时，输出结果全都自动转化成了十进制。如：`echo $((16#5f))` 结果为95（16进位转十进制）

- 单纯用 `(())` 也可重定义变量值，比如 `a=5; ((a++))` 可将 `$a` 重定义为6；

- 常用于算术运算比较，双括号中的变量可以不使用`$`符号前缀。

  - `a=5; b=7; c=2; echo $(( a+b*c ))`。
  - `a=5; b=7; c=2; echo $(( $a+$b*$c ))`

- 括号内支持多个表达式用逗号分开。 只要括号中的表达式符合C语言运算规则，比如可以直接使用`for((i=0;i<5;i++))`，如果不使用双括号, 则为

  - ```shell
    for i in `seq 0 4`
    do
    	echo $i
    done
    ```

  - 或

  - ```shell
    for i in {0..4}
    do
    	echo $i
    done
    ```

  - 再如可以直接使用`if (($i<5))`, 如果不使用双括号, 则为`if [ $i -lt 5 ]`。

# 3 大括号`{}`

## 3.1 `${}`变量替换

`${ }`用于**变量替换**。一般情况下，`$var` 与`${var}` 并没有什么不一样，但是用${ }`会比较精确的界定变量名称的范围。

## 3.2 大括号拓展

- 在这里，大括号中不允许有空白，除非这个空白被引用或转义。

- 对大括号中的以逗号分割的内容进行拓展：

  - ```shell
    [zh@zh-inspironn4050 test]$ echo {zh1,zh2,zh3}.txt
    zh1.txt zh2.txt zh3.txt
    ```

- 对大括号中以点点`..`分割的顺序列表起拓展作用:

  - ```shell
    [zh@zh-inspironn4050 test]$ echo zh{1..3}.txt
    zh1.txt zh2.txt zh3.txt
    [zh@zh-inspironn4050 test]$ echo {zh{1..3},zh5}.txt
    zh1.txt zh2.txt zh3.txt zh5.txt
    ```

  - 这个效果也可以在`[]`中使用`-`来达到：

    - ```shell
      [zh@zh-inspironn4050 test]$ echo {zh[1-3],zh5}.txt
      zh1.txt zh2.txt zh3.txt zh5.txt
      ```

## 3.3 代码块

`{ command1;command2;}`代码块，又被称为内部组，这个结构事实上创建了一个匿名函数 。与小括号中的命令不同，大括号内的命令不会新开一个子shell运行，即脚本余下部分仍可使用括号内变量。括号内的命令间用分号隔开，最后一个也必须有分号。`{}`的第一个命令和左括号之间必须要有一个空格。

示例：`{ ls;pwd;}`或`{ ls;pwd; }`

`{ command1;command2;}`和小括号命令组类似，区别和联系参见小括号部分。

## 3.4 模式匹配替换结构

### 3.4.1 `${variable%pattern}`

- Shell在variable中查找，看它是否以给的模式pattern结尾，如果是，就从命令行把variable中的内容去掉右边最短的匹配模式。

- variable：不能直接给定字符串，必须是变量。

- 如果`${variable%pattern}`单独使用，则会执行匹配结果所代表的方法

  - ```shell
    #!/bin/bash
    function zh(){
    	echo "执行方法zh()";
    }
    str="zhishan"
    ${str%ishan}
    ```

    - 输出：执行方法zh()

  - ```shell
    #!/bin/bash
    function zh(){
    	echo "执行方法zh()";
    }
    str=zhishan
    ${str%ishan}
    ```

    - 输出：执行方法zh()

- 也可以使用`echo`等把`${variable%pattern}`的匹配结果输出

  - ```shell
    #!/bin/bash
    function zh(){
    	echo "执行方法zh()";
    }
    str=zhishan
    echo ${str%ishan}
    ```

  - 输出：zh

###  3.4.2 `${variable%%pattern}`

- shell在variable中查找，看它是否以给的模式pattern结尾，如果是，就从命令行把variable中的内容去掉右边最长的匹配模式

  - ```shell
    [zh@zh-inspironn4050 test]$ str=zhishan
    [zh@zh-inspironn4050 test]$ echo ${str%%h*n}
    z
    [zh@zh-inspironn4050 test]$ echo ${str%h*n}
    zhis
    ```

- variable：不能直接给定字符串，必须是变量。

- 如果`${variable%%pattern}`单独使用，则会执行匹配结果所代表的方法；

- 也可以使用`echo`等把`${variable%%pattern}`的匹配结果输出。

### 3.4.3 `${variable#pattern}`

- shell在variable中查找，看它是否以给的模式pattern开始，如果是，就从命令行把variable中的内容去掉左边最短的匹配模式；
- variable：不能直接给定字符串，必须是变量。
- 如果`${variable#pattern}`单独使用，则会执行匹配结果所代表的方法；
- 也可以使用`echo`等把`${variable#pattern}`的匹配结果输出。

### 3.4.4 `${variable##pattern}`

- shell在variable中查找，看它是否一给的模式pattern结尾，如果是，就从命令行把variable中的内容去掉右边最长的匹配模式
- variable：不能直接给定字符串，必须是变量。
- 如果`${variable##pattern}`单独使用，则会执行匹配结果所代表的方法；
- 也可以使用`echo`等把`${variable##pattern}`的匹配结果输出。

## 3.5 特殊的替换结构

- `${variable:-string}`
  - 若变量variable为空，则用在命令行中用string来替换；
  - 变量variable不为空时，则用变量var的值来替换。
  - variable：不能直接给定字符串，必须是变量。
- `${variable:=string}`
  - 若变量variable为空，则用在命令行中用string来替换，把string赋给变量variable；
  - 变量variable不为空时，则用变量var的值来替换。
  - variable：不能直接给定字符串，必须是变量。
- `${variable:+string}`
  - 当variable不是空的时候才替换成string；
  - 若variable为空时则不替换或者说是替换成变量variable的值，即空值。
  - variable：不能直接给定字符串，必须是变量。
- `${variable:?string}`
  - 若变量variable不为空，则用变量var的值来替换；
  - 若变量variable为空，则把string输出到标准错误中，并从脚本中退出。
  - 我们可利用此特性来检查是否设置了变量的值。
  - variable：不能直接给定字符串，必须是变量。

注意：string不一定是常值的，可用另外一个变量的值或是一种命令的输出。

## 3.6 字符串提取和替换

- `${variable:num}`

  - shell在var中提取第num个字符到末尾的所有字符。

  - 最左为0，最右为-1。

  - 若num为正数，从左边开始；若num为负数，从右边开始提取子串，但必须使用在冒号后面加空格或一个数字或整个num加上括号

  - variable：不能直接给定字符串，必须是变量。

  - ```shell
    [zh@zh-inspironn4050 test]$ str=zhishan
    [zh@zh-inspironn4050 test]$ echo $str
    zhishan
    [zh@zh-inspironn4050 test]$ echo ${str:2}
    ishan
    [zh@zh-inspironn4050 test]$ echo ${str: -5}
    ishan
    [zh@zh-inspironn4050 test]$ echo ${str:(-5)}
    ishan
    [zh@zh-inspironn4050 test]$ echo ${str:1-5}
    shan
    ```

- `${variable:num:len}`

  - num是截取的起始位置，len是长度。表示从`$var`字符串的第`$num`个位置开始提取长度为`$len`的子串。

  - num和len不能为负数。

  - variable：不能直接给定字符串，必须是变量。

  - ```shell
    [zh@zh-inspironn4050 test]$ str=zhishan
    [zh@zh-inspironn4050 test]$ echo ${str:2:2}
    is
    [zh@zh-inspironn4050 test]$ echo ${str:-2:2}
    zhishan
    [zh@zh-inspironn4050 test]$ echo ${str:-5:2}
    zhishan
    ```

- `${variable/pattern/pattern}`

  - 将variable字符串的第一个匹配的pattern替换为另一个pattern；

  - variable：不能直接给定字符串，必须是变量。

  - ```shell
    [zh@zh-inspironn4050 test]$ str=zHisHan
    [zh@zh-inspironn4050 test]$ echo ${str/H/h}
    zhisHan
    ```

- `${variable//pattern/pattern}`

  - 将variable字符串中的所有能匹配的pattern替换为另一个pattern。

  - variable：不能直接给定字符串，必须是变量。

  - ```shell
    [zh@zh-inspironn4050 test]$ str=zHisHan
    [zh@zh-inspironn4050 test]$ echo ${str/H/h}
    zhisHan
    [zh@zh-inspironn4050 test]$ echo ${str//H/h}
    zhishan
    ```