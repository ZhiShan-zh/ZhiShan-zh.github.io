# JavaScript 自执行函数表达式

# 1 基本语法

JavaScript自执行（立即执行）函数表达式的的格式为：

- `(function(){})();`
- `(function(){})();`
- `!function(){}();`

# 2 详解

## 2.1 在不赋值的情形下，在小括号中的函数或者函数表达式，被阻止声明为一个全局的变量，同时其内部是可执行的

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

## 2.2 如果其在小括号中，被赋值给了某一变量，那么该函数或者函数表达式就会被曝露出去，可以在外部调用

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

