# 串的自测

# 1 串类型的定义

## 1.1 应用题：名词解释： 串  

【答】串是零个至多个字符组成的有限序列。从数据结构角度讲， 串属于线性结构。与线性表的特殊性在于串的元素是字符。

## 1.2 填空题：一个字符串中________称为该串的子串 。  

【答】任意个连续的字符组成的子序列。

## 1.3 描述以下概念的区别：空格串与空串。

【答】空格是一个字符，其 ASCII 码值是 32。空格串是由空格组成的串，其长度等于空格的个数。空串是不含任何字符的串，即空串的长度是零。

## 1.2 填空题：INDEX（‘ DATASTRUCTURE’， ‘ STR’） =________。  

【答】5

## 1.3 若串 S=‘software’ ,其子串的数目是多少？

【解析】

子串的定义是： 串中任意个连续的字符组成的子序列，并规定空串是任意串的子串，任意串是其自身的子串。

> S总共有8个字符：则（如果串中有相等字符需要减去重复的子串）
>
> - 以s开头的子串有8个分别为：s、so、sof、soft、softw、softwa、softwar、software
> - 以o开头的子串有7个分别为：o、of、oft、oftw、oftwa、oftwar、oftware
> - 以f开头的子串有6个分别为：f、ft、ftw、ftwa、ftwar、ftware
> - 以t开头的子串有5个分别为：t、tw、twa、twar、tware
> - 以w开头的子串有4个分别为：w、wa、war、ware
> - 以a开头的子串有3个分别为：a、ar、are
> - 以r开头的子串有2个分别为：r、re
> - 以e开头的子串有1个分别为：e
> - 空串为1个
>
> 结果：8 + 7 + 6 + 5 + 4 + 3 + 2 + 1 + 1 = 37

# 2 串的表示和实现

## 1.2 在以链表存储串值时，存储密度是结点大小和串长的函数。假设每个字符占一个字节，每个指针占4个字节，每个结点的大小为4的整数倍。求结点大小为4k，串长尾l时的存储密度d(4k,l)（用公式表示）。

答案：$\frac{L}{(4(K+1)* \lceil \frac{L}{4K} \rceil)}$

【解析】

串的块链存储表示为：

```c
#define CHUNKSIZE 80	//可由用户定义块的大小
typedef struct Chunk {
    char ch[CHUNKSIZE];
    struct Chunk *next;
} Chunk;
typedef struct {
    Chunk *head, *tail;//串的头和尾指针
    int curlen;//串的当前长度
}LString;
```

1. 计算块链的存储密度只考虑Chunk结构，不考虑LString；
2. 一个Chunk包含两部分内容，一个是一个字符数组，大小为$4k$，用于存储$l$的一部分；一个是下一个Chunk的指针，每个指针不分指针类型占用4个字节；最后一个Chunk的char数组可能没有占满，故需要$\lceil \frac{L}{4K} \rceil$（向上取整）
3. 计算全部Chunk占用的空间为：$(4(K+1)* \lceil \frac{L}{4K} \rceil)$

# 3 串的模式匹配算法

## 3.1 判断：KMP 算法的特点是在模式匹配时指示主串的指针不会变小。

【答】对

## 3.2 模式串 P=’abaabcac‘的 next 函数值序列为：

【答】01122312

【解析】

```c
void get_next(SString T, int next[]){
    //求模式串T的next函数值并存入数组next
    i = 1; next[1] = 0; j = 0;
    while(i < T[0]){
        if(j == 0 || T[i] == T[j]){
            ++i; ++j; next[i] = j;
        }else{
            j = next[j];
        }
        
    }
}
```

> P：abaabcac
> i：12345678
> j：01122312
> cur_j：2

## 3.3 字符串’ababaaab’的 nextval 函数值为：

【答】01010421

【解析】

```c
void get_nextval(SString T, int nextval[]){
    //求模式串T的next函数修正值并存入数组nextval
    i = 1; nextval[1] = 0; j = 0;
    while(i < T[0]){
        if(j == 0 || T[i] == T[j]){
            ++i; ++j;
            if(T[i] != T[j]){
                nextval[i] = j;
            }else{
                 nextval[i] = nextval[j];
            }
        }else{
            j = nextval[j];
        }
    }
}
```

> P：ababaaab
> i：12345678
> j：01010421
> cur_j：2