# VueJS常用指令

# 1 `v-on`

可以用`v-on`指令监听 DOM 事件，并在触发时运行一些 JavaScript 代码。

## 1.1 ` v-on:click`

`test_vue.html`：

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>事件处理 v-on:click</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            {{message}}
            <button v-on:click="fun('good')">点击改变</button>
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                message:'hello world' //注意不要写分号结尾
            	},
                methods:{
                    fun:function(msg){
                        this.message=msg;
                    }
                }
            });
        </script>
    </body>
</html>
```

## 1.2 `v-on:keydown`

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>事件处理 v-on:keydown</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <input type="text" v-on:keydown="fun('good',$event)">
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                message:'hello world' //注意不要写分号结尾
                },
                methods:{
                    fun:function(msg, event){
                        // 如果不是数字或Backspace或Delete键的话，阻止输入
                        if(!((event.keyCode>=48&&event.keyCode<=57)||event.keyCode==8||event.keyCode==46)){
                            event.preventDefault();
                        }
                    }
                }
            });
        </script>
    </body>
</html>
```

## 1.3 `v-on:mouseover`

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>事件处理 v-on:mouseover</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <div v-on:mouseover="fun1" id="div">
                <textarea v-on:mouseover="fun2($event)">这是一个文件域</textarea>
            </div>
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                methods:{
                    fun1:function(){
                        alert("div");
                    },
                    fun2:function(event){
                        alert("textarea");
                        event.stopPropagation();//阻止冒泡
                    }
                }
            });
        </script>
    </body>
</html>
```

## 1.4 事件修饰符

VueJS为`v-on`提供了事件修饰符来处理 DOM 事件细节，如：`event.preventDefault()` 或`event.stopPropagation()`。

Vue.js通过由点(.)表示的指令后缀来调用修饰符。
- `.stop`
- `.prevent`
- `.capture`
- `.self`
- `.once`

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-on 事件修饰符</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <form @submit.prevent action="http://www.baidu.com" method="get">
                <input type="submit" value="提交"/>
            </form>
            <div @click="fun">
                <a @click.stop href="http://www.baidu.com">百度</a>
            </div>
        </div>
        <script>
        new Vue({
            el:'#app', //表示当前vue对象接管了div区域
            methods:{
                fun:function(){
                    alert("hello world");
                }
            }
        });
        </script>
    </body>
</html>
```

## 1.5 按键修饰符

Vue允许为`v-on`在监听键盘事件时添加按键修饰符

全部的按键别名为：

- `.enter`
- `.tab`
- `.delete`（捕获 "删除" 和 "退格" 键）
- `.esc`
- `.space`
- `.up`
- `.down`
- `.left`
- `.right`
- `.ctrl`
- `.alt`
- `.shift`
- `.meta`

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-on 按钮修饰符</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <input type="text" v-on:keyup.enter="fun">
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                methods:{
                    fun:function(){
                        alert("你按了回车");
                    }
                }
            });
        </script>
    </body>
</html>
```

v-on简写方式：

```html
<!-- 完整语法 -->
<a v-on:click="doSomething">...</a>
<!-- 缩写 -->
<a @click="doSomething">...</a>
<!-- Alt + C -->
<input @keyup.alt.67="clear">
<!-- Ctrl + Click -->
<div @click.ctrl="doSomething">Do something</div>
```

# 2 `v-text`与`v-html`

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-text与v-html</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <div v-text="message"></div>
            <div v-html="message"></div>
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                    message:"<h1>Hello World！</h1>"
                }
            });
        </script>
    </body>
</html>
```

# 3 `v-bind`

`v-bind`用于绑定数据和元素属性的

插值语法（两个大括号，即{{}}）不能作用在HTML中DOM的属性上，遇到这种情况应该使用`v-bind`指令。

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-bind</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <font size="5" v-bind:color="color1">ZhiShan</font>
            <font size="5" :color="color2">植山</font>
            <hr>
            <a v-bind={href:"https://www.baidu.com/s?wd="+wd}>百度-vue</a>
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                    color1:"red",
                    color2:"green",
                    wd:"vue"
                }
            });
        </script>
    </body>
</html>
```

v-bind简写方式：

```html
<!-- 完整语法 -->
<a v-bind:href="url">...</a>
<!-- 缩写 -->
<a :href="url">...</a>
```

# 4 `v-model`

v-model的作用是对应表单`<input>`、`<textarea>` 及 `<select>` 元素上创建双向数据绑定。但 v-model 本质上不过是语法糖。它负责监听用户的输入事件以更新数据，并对一些极端场景进行一些特殊处理。

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-model</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            姓名:<input type="text" id="username" v-model="user.username">输入的数据为：{{user.username}}<br>
            密码:<input type="password" id="password" v-model="user.password">输入的数据为：{{user.password}}<br>
            <input type="button" @click="fun" value="获取">
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                    user:{username:"",password:""}
                },
                methods:{
                    fun:function(){
                        alert(this.user.username+" "+this.user.password);
                        this.user.username="tom";
                        this.user.password="11111111";
                    }
                }
            });
        </script>
    </body>
</html>
```

# 5 `v-for`

## 5.1 遍历数组

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-for 1</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <ul>
                <li v-for="(item,index) in list">{{item+" "+index}}</li>
            </ul>
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                    list:[1,2,3,4,5,6]
                }
            });
        </script>
    </body>
</html>
```

## 5.2 遍历对象

```java
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-for 2</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <ul>
                <li v-for="(value,key) in product">{{key}}--{{value}}</li>
            </ul>
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                    product:{id:1,pname:"电脑",price:10000}
                }
            });
        </script>
    </body>
</html>
```



## 5.3 操作对象数组

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-for 3</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <table border="1">
                <tr>
                    <td>序号</td>
                    <td>名称</td>
                    <td>价格</td>
                </tr>
                <tr v-for="p in products">
                    <td>
                        {{p.id}}
                    </td>
                    <td>
                        {{p.pname}}
                    </td>
                    <td>
                        {{p.price}}
                    </td>
                </tr>
            </table>
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                    products:[{id:1,pname:"电脑",price:10000},
                        {id:2,pname:"手机",price:1000},
                        {id:3,pname:"相机",price:20000}
                    ]
                }
            });
        </script>
    </body>
</html>
```



# 6 `v-if`与`v-show`

相同点：`v-if`与`v-show`都可以动态控制dom元素显示隐藏

不同点：`v-if`显示隐藏是将dom元素整个添加或删除，而`v-show`隐藏则是为该元素添加`css--display:none`，dom元素还在。

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>v-if与v-show</title>
        <script src="js/vuejs-2.5.16.js"></script>
    </head>
    <body>
        <div id="app">
            <span v-if="flag">植山</span>
            <span v-show="flag">ZhiShan</span>
            <button @click="toggle">切换</button>
        </div>
        <script>
            new Vue({
                el:'#app', //表示当前vue对象接管了div区域
                data:{
                    flag:false
                },
                methods:{
                    toggle:function(){
                        this.flag=!this.flag;
                    }
                }
            });
        </script>
    </body>
</html>
```

