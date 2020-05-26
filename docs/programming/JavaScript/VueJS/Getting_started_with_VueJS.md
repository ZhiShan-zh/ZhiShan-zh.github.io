# VueJS入门

# 1 VueJS概述

## 1.1 VueJS介绍
`Vue.js`是一个构建数据驱动的 web 界面的渐进式JavaScript框架。Vue.js 的目标是通过尽可能简单的 API 实现响应的数据绑定和组合的视图组件。它不仅易于上手，还便于与第三方库或既有项目整合。

官网：https://cn.vuejs.org/		官方教程：https://cn.vuejs.org/v2/guide/

## 1.2 MVVM模式
MVVM是Model-View-ViewModel的简写。它本质上就是MVC 的改进版。MVVM 就是将其中的View 的状态和行为抽象化，让我们将视图 UI 和业务逻辑分开。

MVVM模式和MVC模式一样，主要目的是分离视图（View）和模型（Model）。

`Vue.js`是一个提供了 MVVM 风格的双向数据绑定的 Javascript 库，专注于View 层。它的核心是 MVVM 中的 VM，也就是 ViewModel。 ViewModel负责连接 View 和 Model，保证视图和数据的一致性，这种轻量级的架构让前端开发更加高效、便捷。

# 2 VueJS入门

`test_vuejs.html`：

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>VueJS入门</title>
            <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
        	{{message}}
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                	message:'hello world' //注意不要写分号结尾
                }
            });
        </script>
    </body>
</html>
```

页面访问`test_vuejs.html`：

![](https://zhishan-zh.github.io/media/vuejs_20200526163826.png)

# 3 插值表达式

数据绑定最常见的形式就是使用”Mustache”语法（双大括号）的文本插值，Mustache 标签将会被替代为对应数据对象上属性的值。无论何时，绑定的数据对象上属性发生了改变，插值处的内容都会更新。

VueJS提供了完全的 JavaScript 表达式支持。

```html
{{ number + 1 }}
{{ ok ? 'YES' : 'NO' }}
```

这些表达式会在所属 Vue 实例的数据作用域下作为 JavaScript 被解析。有个限制就是，每个绑定都只能包含单个表达式，所以下面的例子都不会生效

```html
<!-- 这是语句，不是表达式 -->
{{ var a = 1 }}
<!-- 流控制也不会生效，请使用三元表达式 -->
{{ if (ok) { return message } }}
```

