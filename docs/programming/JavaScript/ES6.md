# ES6

# 1 概述

编程语言JavaScript是ECMAScript的实现和扩展 。ECMAScript是由ECMA（一个类似W3C的标准组织）参与进行标准化的语法规范。

ECMAScript定义了：

- 语言语法 – 语法解析规则、关键字、语句、声明、运算符等。
- 类型 – 布尔型、数字、字符串、对象等。
- 原型和继承

- 内建对象和函数的标准库 – JSON、Math、数组方法、对象自省方法等。

ECMAScript标准不定义HTML或CSS的相关功能，也不定义类似DOM（文档对象模型）的Web API，这些都在独立的标准中进行定义。

ECMAScript涵盖了各种环境中JS的使用场景，无论是浏览器环境还是类似node.js的非浏览器环境。
ECMAScript标准的历史版本分别是1、2、3、5。

- 那么为什么没有第4版？其实，在过去确实曾计划发布提出巨量新特性的第4版，但最终却因想法太过激进而惨遭废除（这一版标准中曾经有一个极其复杂的支持泛型和类型推断的内建静态类型系统）。
- ES4饱受争议，当标准委员会最终停止开发ES4时，其成员同意发布一个相对谦和的ES5版本，随后继续制定一些更具实质性的新特性。这一明确的协商协议最终命名
  为“Harmony”，因此，ES5规范中包含这样两句话：
  - ECMAScript是一门充满活力的语言，并在不断进化中。
  - 未来版本的规范中将持续进行重要的技术改进

2009年发布的改进版本ES5，引入了`Object.create()`、`Object.defineProperty()`、`getters`和`setters`、严格模式以及JSON对象。

ECMAScript 6.0（以下简称ES6）是JavaScript语言的下一代标准，2015年6月正式发布。它的目标，是使得JavaScript语言可以用来编写复杂的大型应用程序，成为企业级开发语言。

# 2 NodeJS中使用ES6

ES6中很多高级功能Node是不支持的，如果需要在NodeJS中使用ES6就需要使用babel把代码转换成ES5。

babel转换配置，项目根目录添加`.babelrc`文件

```json
{
	"presets" : ['es2015']
}
```

安装ES6转换模块：`cnpm install babel‐preset‐es2015 ‐‐save‐dev`

全局安装命令行工具：`cnpm install babel‐cli ‐g`

使用：`babel‐node js_filename`

# 3 语法新特性

## 3.1 变量声明——`let`

在ES6以前，使用var关键字来声明变量。无论声明在何处，都会被视为声明在函数的最顶部(不在函数内即在全局作用域的最顶部）。这就是函数变量提升，例如：

```js
function aa() {
    if(bool) {
    	var test = 'hello man'
    } else {
    	console.log(test)
    }
}
```

以上的代码实际上是:

```javascript
function aa() {
    var test // 变量提升
    if(bool) {
    	test = 'hello man'
    } else {
        //此处访问test 值为undefined
        console.log(test)
    } 
    //此处访问test 值为undefined
}
```

我们通常用let和const来声明，let表示变量、const表示常量。let和const都是块级作用域。

```javascript
function aa() {
    if(bool) {
    	let test = 'hello man'
    } else {
        //test 在此处访问不到
        console.log(test)
    }
}
```

## 3.2 常量声明

const 用于声明常量：

```javascript
const name = 'lux'
name = 'joe' //再次赋值此时会报错
```

## 3.3 模板字符串

ES6模板字符解决了ES5在字符串功能上的痛点。
第一个用途，基本的字符串格式化。将表达式嵌入字符串中进行拼接。用${}来界定。

```javascript
//ES5
var name = 'lux'
console.log('hello' + name)
//ES6
const name = 'lux'
console.log(`hello ${name}`) //hello lux
```

第二个用途，在ES5时我们通过反斜杠（`\`）来做多行字符串或者字符串一行行拼接。ES6反引号（``）直接搞定。

```javascript
// ES5
var msg = "Hi \
man!"
// ES6
const template = `<div>
	<span>hello world</span>
</div>`
```

## 3.4 函数默认参数

ES6为参数提供了默认值。在定义函数时便初始化了这个参数，以便在参数没有被传递进去时使用。

```javascript
function action(num = 200) {
	console.log(num)
} 
action() //200
action(300) //300
```

## 3.5 箭头函数

ES6很有意思的一部分就是函数的快捷写法。也就是箭头函数。
箭头函数最直观的三个特点。

1. 不需要function关键字来创建函数；
2. 省略return关键字；
3. 继承当前上下文的 this 关键字；

看下面代码（ES6）

```javascript
(response,message) => {
	//.......
}
```

相当于ES5代码：

```javascript
function(response,message){
	//......
}
```

## 3.6 对象初始化简写

ES5我们对于对象都是以键值对的形式书写，是有可能出现键值对重名的。例如：

```javascript
function people(name, age) {
    return {
        name: name,
        age: age
    };
}
```

以上代码可以简写为：

```javascript
function people(name, age) {
    return {
        name,
        age
    };
}
```

## 3.7 解构

数组和对象是JS中最常用也是最重要表示形式。为了简化提取信息，ES6新增了解构，这是将一个数据结构分解为更小的部分的过程。

ES5我们提取对象中的信息形式如下：

```java
const people = {
    name: 'lux',
    age: 20
} 
const name = people.name
const age = people.age
console.log(name + ' ‐‐‐ ' + age)
```

在ES6之前我们就是这样获取对象信息的，一个一个获取。现在，ES6的解构能让我们从对象或者数组里取出数据存为变量，例如

```javascript
//对象
const people = {
    name: 'lux',
    age: 20
} 
const { name, age } = people
console.log(`${name} ‐‐‐ ${age}`)
//数组
const color = ['red', 'blue']
const [first, second] = color
console.log(first) //'red'
console.log(second) //'blue'
```

## 3.8 Spread Operator

Spread Operator 也就是三个点儿（`...`）

```javascript
//组装数组
const color = ['red', 'yellow']
const colorful = [...color, 'green', 'pink']
console.log(colorful) //[red, yellow, green, pink]
//组装对象
const alp = { fist: 'a', second: 'b'}
const alphabets = { ...alp, third: 'c' }
console.log(alphabets) //{ "fist": "a", "second": "b", "third": "c"
```

## 3.9 import 和 export

- import：导入模块

- export：导出模块

`lib.js`：

```javascript
let fn0=function(){
	console.log('fn0...');
} 
export {fn0}
```

`test.js`

```javascript
import {fn0} from './lib'
fn0();
```

注意：node（v8.x）本身并不支持import关键字，所以我们需要使用babel的命令行工具来执行：`babel‐node test`

## 3.10 Promise

Promise 是异步编程的一种解决方案，比传统的解决方案–回调函数和事件－－更合理和更强大。它由社区最早提出和实现，ES6将其写进了语言标准，统一了语法，原生提供了Promise。