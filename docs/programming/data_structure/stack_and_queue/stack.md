[TOC]

# 栈

# 1 抽象数据类型栈的定义

**栈(stack)** 是限定仅在表尾进行插人或删除操作的线性表。因此， 对栈来说， 表尾端有其特殊含义， 称为**栈顶（ top ）**， 相应地， 表头端称为**栈底（ bottom ）** 。不含元素的空表称为**空栈**。

栈的抽象数据类型为：

```c
ADT Stack{
    /*
     * 数据对象：D = { a_i | a_i ∈ ElemSet, i = 1, 2, ..., n, n≧0}
     * 数据关系：R1 = {<a_i-1, a_>i | a_i-1, a_i ∈ D, i = 2, ..., n}
     *          约定a_n端为栈顶， a_id端为栈底
     * */
    //基本操作
    /*
     * 操作结果： 构造一个空栈
     * */
    InitStack(&S);

    /*
     * 初始条件： 栈s 已存在。
     * 操作结果： 栈s 被销毁。
     * */
    DestroyStack(&S);

    /*
     * 初始条件： 栈s 已存在。
     * 操作结果： 将s 清为空栈。
     * */
    C1earStack(&S);

    /*
     * 初始条件： 栈s 已存在。
     * 操作结果： 若栈s 为空栈， 则返回TRUE， 否则FALSE
     * */
    StackEmpty(S);

    /*
     * 初始条件： 栈s 已存在·
     * 操作结果： 返回s 的元素个数， 即栈的长度。
     * */
    StackLength(S);

    /*
     * 初始条件： 栈已存在且非空。
     * 操作结果： 用e 返回s 的栈顶元素。
     * */
    GetTop(S, &e);

    /*
     * 初始条件： 栈已存在。
     * 操作结果： 插人元素e 为新的栈顶元素。
     * */
    Push(&S, e);

    /*
     * 初始条件： 栈s 已存在且非空。
     * 操作结果： 删除的栈顶元素， 并用e 返回其值。
     * */
    Pop(&s, &e);

    /*
     * 初始条件： 栈s 已存在且非空。
     * 操作结果： 从栈底到栈顶依次对s 的每个数据元素调用函数visit()。一旦visit()失败，则操作失效。
     * */
    StackTraverse(S, visit());
}//ADT Stack
```

# 2 栈的表示和实现

算法描述：

```c
//------------栈的顺序存储表示----------
#define STACK_INIT_SIZE 100 //存储空间初始分配量
#define STACKINCREMENT 10 //存储空间分配增量


typedef struct {
    SE1emType *base;//在栈构造之前和销毁之后,base 的值为NULL
    SE1emType *top;//栈顶指针
    int stacksize;//当前已分配的存储空间， 以元素为单位
} SqStack;

//-------------基本操作的函数原型说明---------

/*
 * 操作结果： 构造一个空栈S
 * */
Status InitStack(SqStack &S);

/*
 * 初始条件： 栈S已存在。
 * 操作结果： 栈S被销毁。
 * */
Status DestroyStack(SqStack &S);

/*
 * 初始条件： 栈S已存在。
 * 操作结果： 将S清为空栈。
 * */
Status C1earStack(SqStack &S);

/*
 * 初始条件： 栈S已存在。
 * 操作结果： 若栈S为空栈，则返回TRUE，否则FALSE
 * */
Status StackEmpty(SqStack S);

/*
 * 初始条件： 栈s 已存在·
 * 操作结果： 返回s 的元素个数， 即栈的长度。
 * */
int StackLength(SqStack S);

/*
 * 初始条件： 栈已存在且非空。
 * 操作结果： 用e 返回s 的栈顶元素。
 * */
Status GetTop(SqStack S, SE1emType &e);

/*
 * 初始条件： 栈已存在。
 * 操作结果： 插人元素e 为新的栈顶元素。
 * */
Status Push(SqStack &S, SE1emType e);

/*
 * 初始条件： 栈s 已存在且非空。
 * 操作结果： 删除的栈顶元素， 并用e 返回其值。
 * */
Status Pop(SqStack &S, SE1emType &e);

/*
 * 初始条件： 栈s 已存在且非空。
 * 操作结果： 从栈底到栈顶依次对s 的每个数据元素调用函数visit()。一旦visit()失败，则操作失效。
 * */
Status StackTraverse(SqStack S, visit());

//----------基本操作的算法描述----------
/*
 * 操作结果： 构造一个空栈S
 * */
Status InitStack(SqStack &S){
    //构造一个空栈S
    S.base = (SE1emType *)malloc(STACK_INIT_SIZE * sizeof (SE1emType));
    if(!S.base) exit(OVERFLOW);//存储分配失败
    S.top = S.base;
    S.stacksize = STACK_INIT_SIZE;
    return OK;
}//InitStack

/*
 * 初始条件： 栈已存在且非空。
 * 操作结果： 用e 返回s 的栈顶元素。
 * */
Status GetTop(SqStack S, SE1emType &e){
    //若栈不空，则用e返回S的栈顶元素，并返回OK；否则返回ERROR
    if(S.top == S.base) return ERROR;
    e = *(S.top-1);
    return OK;
}//GetTop

/*
 * 初始条件： 栈已存在。
 * 操作结果： 插人元素e 为新的栈顶元素。
 * */
Status Push(SqStack &S, SE1emType e){
    //插入元素e为新的栈顶元素
    if(S.top - S.base >= S.stacksize) {//栈满，追加存储空间
        S.base = (SE1emType *)realloc(S.base, (S.stacksize + STACKINCREMENT) * sizeof (SE1emType));
        if(!S.base) exit(OVERFLOOW);//存储分配失败
        S.top = S.base + S.stacksize;
        S.stacksize += STACKINCREMENT;
    }
    *S.top++ = e;
    return OK;
}//Push

/*
 * 初始条件： 栈s 已存在且非空。
 * 操作结果： 删除的栈顶元素， 并用e 返回其值。
 * */
Status Pop(SqStack &S, SE1emType &e){
    //若栈不空，则删除S的栈顶元素，用e返回其值，并返回OK；否则返回ERROR
    if(S.top == S.base) return ERROR;
    e = *--S.top;
    return OK;
}//Pop
```

C语言实现版：

```c
typedef int Status;
#define OK 1
#define ERROR -1
#define OVERFLOOW -1

typedef int SE1emType;

//------------栈的顺序存储表示----------
#define STACK_INIT_SIZE 100 //存储空间初始分配量
#define STACKINCREMENT 10 //存储空间分配增量


typedef struct {
    SE1emType *base;//在栈构造之前和销毁之后,base 的值为NULL
    SE1emType *top;//栈顶指针
    int stacksize;//当前已分配的存储空间， 以元素为单位
} SqStack;

//-------------基本操作的函数原型说明---------

/*
 * 操作结果： 构造一个空栈S
 * */
Status InitStack(SqStack *S);

/*
 * 初始条件： 栈S已存在。
 * 操作结果： 栈S被销毁。
 * */
Status DestroyStack(SqStack *S);

/*
 * 初始条件： 栈S已存在。
 * 操作结果： 将S清为空栈。
 * */
Status C1earStack(SqStack *S);

/*
 * 初始条件： 栈S已存在。
 * 操作结果： 若栈S为空栈，则返回TRUE，否则FALSE
 * */
Status StackEmpty(SqStack S);

/*
 * 初始条件： 栈s 已存在·
 * 操作结果： 返回s 的元素个数， 即栈的长度。
 * */
int StackLength(SqStack S);

/*
 * 初始条件： 栈已存在且非空。
 * 操作结果： 用e 返回s 的栈顶元素。
 * */
Status GetTop(SqStack S, SE1emType *e);

/*
 * 初始条件： 栈已存在。
 * 操作结果： 插人元素e 为新的栈顶元素。
 * */
Status Push(SqStack *S, SE1emType e);

/*
 * 初始条件： 栈s 已存在且非空。
 * 操作结果： 删除的栈顶元素， 并用e 返回其值。
 * */
Status Pop(SqStack *S, SE1emType *e);

/*
 * 初始条件： 栈s 已存在且非空。
 * 操作结果： 从栈底到栈顶依次对s 的每个数据元素调用函数visit()。一旦visit()失败，则操作失效。
 * */
Status StackTraverse(SqStack S, Status (*visit)(SE1emType *e));
```

```c
#include <stdlib.h>
#include "stack.h"

//----------基本操作的算法描述----------
/*
 * 操作结果： 构造一个空栈S
 * */
Status InitStack(SqStack *S){
    //构造一个空栈S
    (*S).base = (SE1emType *)malloc(STACK_INIT_SIZE * sizeof (SE1emType));
    if(!(*S).base) exit(OVERFLOOW);//存储分配失败
    (*S).top = (*S).base;
    (*S).stacksize = STACK_INIT_SIZE;
    return OK;
}//InitStack

/*
 * 初始条件： 栈已存在且非空。
 * 操作结果： 用e 返回s 的栈顶元素。
 * */
Status GetTop(SqStack S, SE1emType *e){
    //若栈不空，则用e返回S的栈顶元素，并返回OK；否则返回ERROR
    if(S.top == S.base) return ERROR;
    *e = *(S.top-1);
    return OK;
}//GetTop

/*
 * 初始条件： 栈已存在。
 * 操作结果： 插人元素e 为新的栈顶元素。
 * */
Status Push(SqStack *S, SE1emType e){
    //插入元素e为新的栈顶元素
    if((*S).top - (*S).base >= (*S).stacksize) {//栈满，追加存储空间
        (*S).base = (SE1emType *)realloc((*S).base, ((*S).stacksize + STACKINCREMENT) * sizeof (SE1emType));
        if(!(*S).base) exit(OVERFLOOW);//存储分配失败
        (*S).top = (*S).base + (*S).stacksize;
        (*S).stacksize += STACKINCREMENT;
    }
    *(*S).top++ = e;
    return OK;
}//Push

/*
 * 初始条件： 栈s 已存在且非空。
 * 操作结果： 删除的栈顶元素， 并用e 返回其值。
 * */
Status Pop(SqStack *S, SE1emType *e){
    //若栈不空，则删除S的栈顶元素，用e返回其值，并返回OK；否则返回ERROR
    if((*S).top == (*S).base) return ERROR;
    *e = *--((*S).top);
    return OK;
}//Pop
```

