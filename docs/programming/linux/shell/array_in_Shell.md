# Shell中的数组

# 1 概述

- 数组中可以存放多个值。Bash Shell 只支持一维数组（不支持多维数组），初始化时不需要定义数组大小。

- 数组元素的下标由0开始。
- Shell 数组用括号来表示，元素用"空格"符号分割开。

# 2 数组的初始化

```shell
array_name=(value1 ... valuen)
```

或

```shell
array_name[index]=value
```

示例：

```shell
#!/bin/bash
arr=(z h)

echo ${arr[0]}
echo ${arr[1]}
```

或

```shell
#!/bin/bash
arr[0]=z
arr[1]=h

echo ${arr[0]}
echo ${arr[1]}
```

# 3 数组的读取

## 3.1 单个读取元素

数组读取的格式：`${array_name[index]}`

示例：

```shell
#!/bin/bash
arr=(z h)

echo ${arr[0]}
echo ${arr[1]}
```

## 3.2 批量读取元素

使用`@`或`*`可以获取数组中的所有元素：`${array_name[@]}`或`${array_name[*]}`

示例：

```shell
#!/bin/bash
arr[0]=z
arr[1]=h

echo ${arr[@]}
echo ${arr[*]}
```

输出：

```
z h
z h
```

# 4 获取数组的长度

获取数组长度的方法与获取字符串长度的方法相同：`${#array_name[@]}`或`${#array_name[*]}`

示例：

```shell
#!/bin/bash
arr[0]=z
arr[1]=h

echo ${#arr[@]}
echo ${#arr[*]}
```

输出：

```
2
2
```

