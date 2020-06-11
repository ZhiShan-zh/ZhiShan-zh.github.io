# 模块化相关规范

# 1 模块化概述

**传统开发模式的主要问题**：

- 命名冲突
- 文件依赖

**通过模块化解决上述问题**：

- **模块化**就是把单独的一个功能封装到一个模块（文件）中，模块之间相互隔离，但是可以通过特定的接口公开内部成员，也可以依赖别的模块。
- 模块化开发的好处：方便代码的重用，从而提升开发效率，并且方便后期的维护。

# 2 模块化的分类

## 2.1 浏览器端的模块化

- AMD（Asynchronous Module Definition，异步模块定义）
    - 代表产品为：[Require.js](https://requirejs.org/)
- CMD（Common Module Definition，通用模块定义）
    - 代表产品为：[Sea.js](https://seajs.github.io/seajs/docs/)

## 2.2 服务器端模块化规范

服务器端的模块化规范是使用CommonJS规范：

- 模块分为**单文件模块**与**包**
- 模块成员导出：使用`exports`或者`module.exports`
- 模块成员导入：`require('模块标识符')`
- 一个文件就是一个模块，都拥有独立的作用域

## 2.3 ES6模块化——大一统的模块化规范

在 ES6 模块化规范诞生之前， Javascript 社区已经尝试并提出了AMD、 CMD、 CommonJS 等模块化规范。

但是，这些社区提出的模块化标准，还是存在一定的差异性与局限性、 并不是浏览器与服务器通用的模块化标准，例如：

- AMD 和 CMD 适用于浏览器端的 Javascript 模块化
- CommonJS 适用于服务器端的 Javascript 模块化

因此，ES6 语法规范中，在语言层面上定义了 ES6 模块化规范，是浏览器端与服务器端通用的模块化开发规范。

ES6模块化规范中定义：

- 每个 js 文件都是一个独立的模块
- 导入模块成员使用 import 关键字
- 暴露模块成员使用 export 关键字

# 3 NodeJS中通过babel体验ES6模块化

- `npm install --save-dev @babel/core @babel/cli @babel/preset-env @babel/node`

- `npm install --save @babel/polyfill`

- 项目跟目录创建文件`babel.config.js`
    - `babel.config.js`文件内容为：

    - ```javascript
        const presets = [
            ["@babel/env", {
                targets: {
                    edge: "17",
                    firefox: "60",
                    chrome: "67",
                    safari: "11.1"
                }
            }]
        ];
        //暴露
        module.exports = { presets };
        ```

- 创建`index.js`文件

    - 在项目目录中创建`index.js`文件作为入口文件

    - 在`index.js`中输入需要执行的js代码

    - ```javascript
        console.log("ok");
        ```

- 使用npx执行文件：`npx babel-node ./index.js`

# 4 ES6模块化的基本语法

## 4.1 默认导出 与 默认导入

- 默认导出语法：`export default 默认导出的成员`
- 默认导入语法：`import 接收名称 from '模块标识符'`
- 注意：每个模块中，只允许使用唯一的一次`export default`，否则会报错！

测试代码：

- 需要导出的模块：`m.js`

    - ```javascript
        // 定义私有成员 a 和 c
        let a = 10
        let c = 20
        // 外界访问不到变量 d ,因为它没有被暴露出去
        let d = 30
        function show() {}
        // 将本模块中的私有成员暴露出去，供其它模块使用
        export default {
            a,
            c,
            show
        }
        ```

- 测试导入模块

    - ```javascript
        // 导入模块成员
        import m from './m.js'
        console.log(m)
        // 打印输出的结果为：
        // { a: 10, c: 20, show: [Function: show] }
        ```

## 4.2 按需导出 与 按需导入

- 按需导出语法：`export let s1 = 10`
- 按需导入语法：`import { s1 } from '模块标识符'`
- 注意：每个模块中，可以使用多次按需导出

测试：

- 待导出模块：`m.js`

    - ```javascript
        // 向外按需导出变量 s1
        export let s1 = 'aaa'
        // 向外按需导出变量 s2
        export let s2 = 'ccc'
        // 向外按需导出方法 say
        export function say = function() {}
        ```

- 测试导入模块：

    - ```javascript
        // 导入模块成员
        import { s1, s2 as ss2, say } from './m.js'
        console.log(s1) // 打印输出 aaa
        console.log(ss2) // 打印输出 ccc
        console.log(say) // 打印输出 [Function: say]
        ```

## 4.3 直接导入并执行模块代码

有时候，我们**只想单纯执行某个模块中的代码，并不需要得到模块中向外暴露的成员**，此时，可以直接导入并执行模块代码。

测试：

- 待导出模块：`m.js`

    - ```javascript
        // 在当前模块中执行一个 for 循环操作
        for(let i = 0; i < 3; i++) {
        	console.log(i)
        }
        ```

- 测试：

    - ```javascript
        // 直接导入并执行模块代码
        import './m.js'
        ```