# C语言概述

# 1 计算机介绍

## 1.1 计算机组成和计算机体系结构

### 1.1.1 概念

- 计算机体系结构
  -  是指那些能够被程序员所见到的计算机系统的属性，即概念性的结构与功能特性。
    - 计算机系统的属性：通常是指用机器语言编程的程序员（也包括汇编语言程序设计者和汇编程序设计者）所看到的系统机器的属性，包括指令集、数据类型、存储器寻址技术、I/O机理等，大都属于抽象的属性。
    - 由于计算机系统具有多级层次结构，因此，站在不同层次上编程的程序员所看到的计算机属性也是各不相同的。

- 计算机组成
  - 是指如何实现计算机体系结构所体现的属性，它包含了许多程序员来说是透明的硬件细节。

### 1.1.2 C语言的特点

1. 语言简洁，紧凑，使用方便灵活；

2. 运算符丰富；

3. 数据类型丰富；

   > - 基本类型
   >   - 整型
   >     - 短整型（short int）
   >     - 基本整型（int）
   >     - 长整型（long int）
   >   - 浮点型
   >     - 单精度型（float）
   >     - 双精度型（double）
   >     - 长双精度型（long double）
   >   - 字符型（char)
   >   - 枚举类型（enum）
   > - 构造类型
   >   - 数组类型
   >   - 结构体（struct）
   >   - 共用体（union）
   > - 指针类型（\*）
   > - 空类型（void）

4. 具有结构化控制语句；

5. 语法限制不太严格，程序设计自由灵活；

6. C语言允许直接访问物理地址，能进行位（bit）操作，能实现汇编语言大部分的功能，可以直接对硬件进行操作；

7. 生成目标代码质量高，程序执行效率高；

8. 用C语言编写的程序可移植性好（相对于汇编语言）。

# 2 程序的灵魂——算法

一个程序应包含两方面的内容：

- 对数据的描述。在程序中要指定数据的类型和数据的组织形式，即数据结构（data structure）
- 对操作的描述。即操作的步骤，也就是算法（algorithm）。

## 2.1 算法的概念

**算法**：广义地说，为解决一个问题而采取得方法和步骤。

**计算机算法分类**：

- 数值运算算法：数值求解
- 非数值运算算法：最常见于事务管理，如图书检索、人事管理、行车调度管理等。

## 2.2 结构化程序的设计方法

**结构化算法**：

- 定义：是由一些基本结构顺序组成的，在基本结构之间不存在向前或向后的跳转，流程的转移只存在于一个基本的结构范围内。
- 一个非结构化算法可以用一个结构化算法代替，其功能不变。
- 对比：和结构化算法相比，非结构化算法有一下缺点：
  - 流程不受限制地随意转来转去，使流程图毫无规律可言；
  - 使人在阅读时，难以理解算法的逻辑；难以阅读，难以修改，从而使程序的可靠性和可维护性难以保障。

**结构化程序的设计方法**：

1. 自顶向下，逐步细化：先进性整体规划，在进行各部分的设计，最后进行细节的设计。这种设计方法的过程是将问题求解由抽象逐步具体化的过程。
2. 模块化设计：尤其当程序比较复杂时，更有必要。
3. 结构化编码。

# 3 为什么要学习C语言

# 4 C语言入门

## 4.1 编写C语言程序

`test.c`：C语言的源代码文件是一个普通的文本文件，但扩展名必须是`.c`。

```c
#include <stdio.h>

int main()
{
    printf("Hello World!\n");
    return 0;
}
```

## 4.2 通过GCC编译C语言代码

### 4.2.1 GCC介绍

**编译器**：是将易于编写、阅读和维护的高级计算机语言翻译为计算机能解读、运行的低级机器语言的程序。

**GCC**：

- （GNU Compiler Collection，GNU 编译器套件），是由 GNU 开发的编程语言编译器。gcc原本作为GNU操作系统的官方编译器，现已被大多数类Unix操作系统（如Linux、BSD、Mac OS X等）采纳为标准的编译器，GCC同样适用于微软的Windows。
- GCC最初用于编译C语言，随着项目的发展GCC已经成为了能够编译C、C++、Java、Ada、fortran、Object C、Object C++、Go语言的编译器大家族。

### 4.2.2 GCC用法

# 5 system函数

语法：`int *system*(const char *command);`

功能：在已经运行的程序中执行另外一个外部程序
参数：外部可执行程序名字
返回值：

- 成功：不同系统返回值不一样
- 失败：通常是 - 1

注意：如果是linux平台，则需要头文件`#include <stdlib.h>`

示例：

- Windows平台：打开计算器

```c
int main()
{
    system("calc");
    return 0;
}
```

注：这里不需要任何头文件。

- Linux平台：

```c
#include <stdlib.h>

int main()
{
	system("ls"); //Linux平台, 需要头文件#include <stdlib.h>
	return 0;
}

```

# 6 C语言库函数返回值问题

C语言所有的库函数调用，**只能保证语法是一致的，但不能保证执行结果是一致的**，同样的库函数在不同的操作系统下执行结果可能是一样的，也可能是不一样的。

在学习Linux发展史时，我们得知Linux的发展离不开POSIX标准，只要符合这个标准的函数，在不同的系统下执行的结果就可以一致。

Unix和linux很多库函数都是支持POSIX的，但Windows支持的比较差。
如果将Unix代码移植到Linux一般代价很小，如果把Windows代码移植到Unix或者Linux就比较麻烦。