# 路由框架vue-router

# 1 什么是vue-router

vue-router就是vue官方提供的一个路由框架。使用`Vue.js`，我们已经可以通过组合组件来组成应用程序，当你要把 vue-router 添加进来，我们需要做的是，将组件（components）映射到路由（routes），然后告诉 vue-router 在哪里渲染它们。

我们使用VUE开发搭建单页应用（SPA）（打包之后），路由的功能就是一个vue组件的映射，用于vue各组件之间的跳转。

官方文档：https://router.vuejs.org/zh/

# 2 快速入门

## 2.1 Vue CLI——Vue.js开发的标准化工具

Vue CLI老版本为[`vue-cli`](https://github.com/vuejs/vue-cli/tree/v2#vue-cli--)，新版本为[`@vue/cli`](https://cli.vuejs.org/zh/guide/)。

快速使用，参见对应指南。

使用[`@vue/cli`](https://cli.vuejs.org/zh/guide/)创建vue项目，选择Router模块。

## 2.2 路由定义

`src/App.vue`是我们的主界面，其中的`<router-view/>`标签用于显示各组件视图内容

`src/router/index.js`是定义路由的脚本：

- path：是路径；
- name：是名称 ；
- component：是跳转的组件 。

（1）我们现在定义两个页面组件，存放在`src/components`下

`list.vue`

```html
<template>
  <div>
    这是一个列表
  </div>
</template>
```

`about.vue`

```html
<template>
  <div>
    关于我们
  </div>
</template>
```

（2）定义路由

修改`src/router/index.js`

```js
import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import list from '@/components/list'
import about from '@/components/about'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/list',
      name: 'List',
      component: list
    },
    {
      path: '/about',
      name: 'About',
      component: about
    }
  ]
})
```

（3）放置跳转链接

修改`src/app.vue`，添加链接 

```html
<router-link to="/" >首页</router-link>
<router-link to="/list">列表</router-link>
<router-link to="/about">关于</router-link>
```

通过router-link标签实现路由的跳转

router-link标签属性如下：

| 属性    | 类型               | 含义                                                         |
| ------- | ------------------ | ------------------------------------------------------------ |
| to      | string \| Location | 表示目标路由的链接。当被点击后，内部会立刻把 `to` 的值传到 `router.push()`，所以这个值可以是一个字符串或者是描述目标位置的对象。 |
| replace | boolean            | 设置 `replace` 属性的话，当点击时，会调用 `router.replace()` 而不是 `router.push()`，于是导航后不会留下 history 记录。 |
| append  | boolean            | 设置 `append` 属性后，则在当前（相对）路径前添加基路径。例如，我们从 `/a` 导航到一个相对路径 `b`，如果没有配置 `append`，则路径为 `/b`，如果配了，则为 `/a/b` |

测试运行看是否可以跳转页面

# 3 深入了解

## 3.1 动态路由

我们经常会遇到这样的需求，有一个新闻列表，点击某一条进入新闻详细页，我们通常是传递新闻的ID给详细页，详细页根据ID进行处理。这时我们就会用到动态路由

一个『路径参数』使用冒号 `:` 标记。当匹配到一个路由时，参数值会被设置到 `this.$route.params`

看代码实现：

在`src/components`下创建`item.vue`

```html
<template>
  <div>
    详细页 {{ $route.params.id }}
  </div>
</template>
```

修改`src/router/index.js`，引入item组件

```js
import item from '@/components/item'
```

添加路由设置

```js
{
    path: '/item/:id',
    name: 'Item',
    component: item
}
```

修改`src/components/list.vue`,  增加链接

```html
<template>
  <div>
    这是一个列表
    <router-link to="/item/1">新闻1</router-link>
    <router-link to="/item/2">新闻2</router-link>
    <router-link to="/item/3">新闻3</router-link>
  </div>
</template>
```

## 3.2 嵌套路由

实际生活中的应用界面，通常由多层嵌套的组件组合而成。同样地，URL 中各段动态路径也按某种结构对应嵌套的各层组件，例如：

```
/about/address                        /about/linkman
+------------------+                  +-----------------+
| About            |                  | About           |
| +--------------+ |                  | +-------------+ |
| | address      | |  +------------>  | | linkman     | |
| |              | |                  | |             | |
| +--------------+ |                  | +-------------+ |
+------------------+                  +-----------------+
```

我们来看代码的实现

（1）在`src/components`下创建`address.vue`

```html
<template>
  <div>
    地址：北京
  </div>
</template>
```

创建`linkman.vue`

```html
<template>
  <div>
    联系人：植山
  </div>
</template>
```

（2）修改`src/router/index.js`

引入linkman和address

```js
import linkman from '@/components/linkman'
import address from '@/components/address'
```

配置嵌套路由:

```js
{
      path: '/about',
      name: 'About',
      component: about,
      children: [
        {path: 'linkman', component: linkman},
        {path: 'address', component: address}
      ]
    }
```

（3）修改`src/components/about.vue`

```html
<template>
  <div>
    关于我们
    <router-link to="/about/address" >地址</router-link>
    <router-link to="/about/linkman" >联系人</router-link>
    <router-view/>
  </div>
</template>
```



