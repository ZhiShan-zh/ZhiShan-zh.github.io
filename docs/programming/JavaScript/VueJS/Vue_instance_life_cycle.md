# Vue实例的生命周期

# 1 概述

## 1.1 什么是生命周期

从Vue实例创建、运行、到销毁期间，总是伴随着各种各样的事件，这些事件，统称为生命周期！

生命周期钩子 = 生命周期函数 = 生命周期事件

## 1.2 主要的生命周期函数分类

![img](https://zhishan-zh.github.io/media/vuejs-1534300915m15X343009a415.png)

- **创建期间的生命周期函数**
  - `beforeCreate`：实例刚在内存中被创建出来，此时，还没有初始化好 data 和 methods 属性
  - `created`：实例已经在内存中创建OK，此时 data 和 methods 已经创建OK，此时还没有开始编译模板
  - `beforeMount`：此时已经完成了模板的编译，但是还没有挂载到页面中
  - `mounted`：此时，已经将编译好的模板，挂载到了页面指定的容器中显示
- **运行期间的生命周期函数**
  - `beforeUpdate`：状态更新之前执行此函数， 此时 data 中的状态值是最新的，但是界面上显示的 数据还是旧的，因为此时还没有开始重新渲染DOM节点
  - `updated`：实例更新完毕之后调用此函数，此时 data 中的状态值 和 界面上显示的数据，都已经完成了更新，界面已经被重新渲染好了！
- **销毁期间的生命周期函数**
  - `beforeDestroy`：实例销毁之前调用。在这一步，实例仍然完全可用。
  - `destroyed`：Vue 实例销毁后调用。调用后，Vue 实例指示的所有东西都会解绑定，所有的事件监听器会被移除，所有的子实例也会被销毁。

# 1 入门案例

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>vue实例的生命周期</title>
        <script src="js/vuejs-2.5.16.js"></script>
        </head>
        <body>
        <div id="app">
            {{message}}
        </div>
        <script>
            var vm = new Vue({
                el: "#app",
                data: {
                    message: 'hello world'
                },
                beforeCreate: function() {
                    console.log(this);
                    showData('创建vue实例前', this);
                },
                created: function() {
                    showData('创建vue实例后', this);
                },
                beforeMount: function() {
                    showData('挂载到dom前', this);
                },
                mounted: function() {
                    showData('挂载到dom后', this);
                },
                beforeUpdate: function() {
                    showData('数据变化更新前', this);
                },
                updated: function() {
                    showData('数据变化更新后', this);
                },
                beforeDestroy: function() {
                    vm.test = "3333";
                    showData('vue实例销毁前', this);
                },
                destroyed: function() {
                    showData('vue实例销毁后', this);
                }
            });
            function realDom() {
                console.log('真实dom结构：' + document.getElementById('app').innerHTML);
            } 
            function showData(process, obj) {
                console.log(process);
                console.log('data 数据：' + obj.message)
                console.log('挂载的对象：')
                console.log(obj.$el)
                realDom();
                console.log('------------------')
                console.log('------------------')
            }
            vm.message="good...";
            vm.$destroy();
        </script>
    </body>
</html>    
```

输出：

```
创建vue实例前
data 数据：undefined
挂载的对象：
undefined
真实dom结构：
            {{message}}
        
------------------
------------------
创建vue实例后
data 数据：hello world
挂载的对象：
undefined
真实dom结构：
            {{message}}
        
------------------
------------------
挂载到dom前
data 数据：hello world
挂载的对象：
<div id=​"app">​
            {{message}}
        ​</div>​
真实dom结构：
            {{message}}
        
------------------
------------------
挂载到dom后
data 数据：hello world
挂载的对象：
<div id=​"app">​
            hello world
        ​</div>​
真实dom结构：
            hello world
        
------------------
------------------
vue实例销毁前
data 数据：good...
挂载的对象：
<div id=​"app">​
            hello world
        ​</div>​
真实dom结构：
            hello world
        
------------------
------------------
vue实例销毁后
data 数据：good...
挂载的对象：
<div id=​"app">​
            hello world
        ​</div>​
真实dom结构：
            hello world
        
------------------
------------------
数据变化更新后
data 数据：good...
挂载的对象：
<div id=​"app">​
            hello world
        ​</div>​
真实dom结构：
            hello world
        
------------------
------------------
```

