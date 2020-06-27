# JavaScript中的小括号`()`

# 1 提高运算符的优先级

如：

- $(1+2)*3=3*3=9$
- $1 + 2 * 3 = 1 + 6 = 7$

# 2 函数形参和函数调用传参

```javascript
function fun(a, b) {// 函数定义形参
    return a + b;
}
fun(1, 2);//函数调用传递参数
```

# 3 与特定关键字形成特定语句

if语句：

```javascript
if(i < 5) {
    //此处省略N行代码
}
```

while语句：

```javascript
while(i < 5) {
    //此处省略N行代码
}
```

for语句：

```javascript
for(var i=0; i<5; i++){
    //此处省略N行代码
}
```

# 4 执行一个或多个表达式

此格式的语句将返回最后一个表达式的值，多个表达式之间使用逗号`,`分割，如 ：

```java
(1, 2+3, 4*5, 6/5, 8%7, 9);//输出：9
(1, 2+3, 4*5, 6/5, a=8%7, 9)//输出：9
console.log(a);//输出：1
b = (1, 2+3, 4*5, 6/5, a=8%7, 9);//b=9,a=1
```

# 5 自执行函数表达式

## 5.1 在不赋值的情形下，在小括号中的函数或者函数表达式，被阻止声明为一个全局的变量，同时其内部是可执行的

```javascript
//函数声明置于小括号中，没有自执行
( function fun(){console.log("aaa");return "bbb"} );
console.log("fun is " + fun);// fun is not defined

//函数声明置于小括号中，且自执行
( function fun(){console.log("aaa");return "bbb"}() );//输出aaa
console.log("fun is " + fun);// fun is not defined

//函数声明置于小括号中，且自执行，注意，负责执行的一对小括号移到了外部
( function fun(){console.log("aaa");return "bbb"} )();//输出aaa
console.log("res is " + fun);// fun is not defined
```

## 5.2 如果其在小括号中，被赋值给了某一变量，那么该函数或者函数表达式就会被曝露出去，可以在外部调用

```javascript
//函数声明置于小括号中，函数未执行但将其赋值给fun
( fun = function aaa(){console.log("aaa");return "bbb"} )
console.log("fun is " + fun());//fun is bbb

//函数声明置于小括号中，函数执行，并且将其赋值给fun
( fun = function aaa(){console.log("aaa");return "bbb"}() );//输出aaa
console.log("fun is " + fun);//fun is bbb

//函数声明置于小括号中，将其赋值给fun，并且在外部执行之(注意末尾小括号位置)
( fun = function aaa(){console.log("aaa");return "bbb"} )();//输出aaa
console.log("fun is " + fun());//再次输出aaa，并输出fun is bbb
```

## 5.3 在括号外赋值的函数表达式

```javascript
// node中运行
> fun = function test(){return "a"};
[Function: test]
> fun = function test(){return "a"}();
'a'
> fun
'a'
> fun = (function test(){return "a"})();
'a'
> fun
'a'
> fun = (function (){return "a"})();
'a'
> fun
'a'
```

