# 跨域

# 1 跨域概述

## 1.1 什么是跨域

跨域是指一个域下的文档或脚本试图去请求另一个域下的资源，这里跨域是广义的。

## 1.2 同源策略

同域：协议、域名和端口号都一致为同域

同源策略/SOP（Same origin policy）是一种约定，由Netscape公司1995年引入浏览器，它是浏览器最核心也最基本的安全功能，如果缺少了同源策略，浏览器很容易受到XSS、CSFR等攻击。所谓**同源是指"协议+域名+端口"三者相同**，即便**两个不同的域名指向同一个ip地址，也非同源**。

同源策略限制以下几种行为：

1. Cookie、LocalStorage 和 IndexDB 无法读取
2. DOM 和 Js对象无法获得
3. AJAX 请求不能发送

## 1.3 常见跨域场景
| 分类 | URL |
| --- | --- |
| 同一域名，不同文件或路径 | [http://www.domain.com/a.js](http://www.domain.com/a.js)<br />[http://www.domain.com/b.js](http://www.domain.com/b.js)<br />[http://www.domain.com/lab/c.js](http://www.domain.com/lab/c.js) |
| 同一域名，不同端口 | [http://www.domain.com:8000/a.js](http://www.domain.com:8000/a.js)<br />[http://www.domain.com/b.js](http://www.domain.com/b.js) |
| 同一域名，不同协议 | [http://www.domain.com/a.js](http://www.domain.com/a.js)<br />[https://www.domain.com/b.js](https://www.domain.com/b.js) |
| 同一协议，不同IP | [http://www.domain.com/a.js](http://www.domain.com/a.js)<br />[http://192.168.4.12/b.js](http://192.168.4.12/b.js) |
| 主域相同，子域不同 | [http://www.domain.com/a.js](http://www.domain.com/a.js)<br />[http://x.domain.com/b.js](http://x.domain.com/b.js)<br />[http://domain.com/c.js](http://domain.com/c.js) |
| 不同域名 | [http://www.domain1.com/a.js](http://www.domain1.com/a.js)<br />[http://www.domain2.com/b.js](http://www.domain2.com/b.js) |


# 2 跨域方案

1. 通过jsonp跨域
2. 跨域资源共享（CORS）
3. postMessage + iframe跨域
4. document.domain + iframe跨域
5. window.name + iframe跨域
6. location.hash + iframe
7. http-proxy代理跨域
8. nginx代理跨域
9. nodejs中间件代理跨域
10. WebSocket协议跨域

## 2.1 通过jsonp跨域

通常为了减轻web服务器的负载，我们把js、css，img等静态资源分离到另一台独立域名的服务器上，在html页面中再通过相应的标签从不同域名下加载静态资源，而被浏览器允许，基于此原理，我们可以通过动态创建script，再请求一个带参网址实现跨域通信。

**缺点**：

1. 只能发送get请求， 不支持post、put、delete；
2. 不安全，容易遭受xss攻击，一般不采用。

> 测试接口地址：[https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=b&cb=show](https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=b&cb=show)

> 参数：

> > wd：自定义参数

> cb：返回的函数名


> 返回：show({"q":"b","p":null,"s":[]})

> 可以看出这是这返回的是一个函数，函数里边的参数是一个字典。我们可以用这个来演示jsonp跨域


### 2.1.1 原生JS实现

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        function show(data){
            console.log(data)
        }
    </script>
    
    <!--通过动态创建js标签跨域，参数wd=a-->
    <script>
        var script = document.createElement("script");
        script.type = 'text/javascript';
        script.src = 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=a&cb=show';
        document.head.appendChild(script);
    </script>
    <!--通过静态js标签跨域，参数wd=b-->
    <script src="https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=b&cb=show"></script>
</body>
</html>
```

### 2.1.2 封装jsonp函数

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        // 封装jsonp函数
        function jsonp({url, params, cb}){
            return new Promise((resolve, reject)=>{
                let script = document.createElement('script');
                window[cb] = function (data){
                    resolve(data);
                    document.body.removeChild(script);
                }
                params = {...params, cb};//wd=jsonp&cb=show
                let arrs = [];
                for(let key in params){
                    arrs.push(`${key}=${params[key]}`);
                }
                script.src = (`${url}?${arrs.join('&')}`);
                document.body.appendChild(script);
            })
        }
        //调用jsonp函数
        jsonp({
            url:`https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=jsonp&cb=show`,
            params:{wd:'b'},
            cb:'show'
        }).then(data=>{
            console.log(data);
        })
    </script>
</body>
</html>
```

### 2.1.3 后端使用node

#### 2.1.3.1 安装express包

`npm install express`

#### 2.1.3.2 node代码

`server.js`代码内容：

```javascript
let express = require('express');
let app = express();

app.listen(3000);
```

#### 2.1.3.3 测试

执行`server.js`：`node server.js`

页面访问：`http://localhost:3000/`

![](/home/zh/%E6%96%87%E6%A1%A3/%E8%B7%A8%E5%9F%9F/%E8%B7%A8%E5%9F%9F%E9%97%AE%E9%A2%98_media/image-20200419102500844.png#alt=image-20200419102500844)

#### 2.1.3.4 改写后台：返回一个可执行函数调用

```javascript
let express = require('express');
let app = express();
app.get('/say', function(req, res){
    let {wd,cb} = req.query;
    console.log(wd);
    res.end(`${cb}('已经展示')`);
})
app.listen(3000);
```

#### 2.1.3.5 改写前端：调用本地的服务

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        // 封装jsonp函数
        function jsonp({url, params, cb}){
            return new Promise((resolve, reject)=>{
                let script = document.createElement('script');
                window[cb] = function (data){
                    resolve(data);
                    document.body.removeChild(script);
                }
                params = {...params, cb};//wd=jsonp&cb=show
                let arrs = [];
                for(let key in params){
                    arrs.push(`${key}=${params[key]}`);
                }
                script.src = (`${url}?${arrs.join('&')}`);
                document.body.appendChild(script);
            })
        }
        //调用jsonp函数
        jsonp({
            url:`http://localhost:3000/say`,
            params:{wd:'请求展示'},
            cb:'show'
        }).then(data=>{
            console.log(data);
        })
    </script>
</body>
</html>
```

## 2.2 cors：跨域资源共享

普通跨域请求：只要服务端设置Access-Control-Allow-Origin即可，前端无须设置，若要带cookie等请求，前后端都需要设置。

目前，所有浏览器都支持该功能(IE8+：IE8/9需要使用XDomainRequest对象来支持CORS）)，CORS也已经成为主流的跨域解决方案。

### 2.2.1 设置服务器静态资源

#### 2.2.1.1 创建node服务

`server.js`：位置`cors/server.js`

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(3000);
```

#### 2.2.1.2 index.html

位置：`cors/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    Hello
</body>
</html>
```

#### 2.2.1.3 测试服务器静态资源

页面访问：[http://localhost:3000/index.html](http://localhost:3000/index.html)

![](/home/zh/%E6%96%87%E6%A1%A3/%E8%B7%A8%E5%9F%9F/%E8%B7%A8%E5%9F%9F%E9%97%AE%E9%A2%98_media/image-20200419105426596.png#alt=image-20200419105426596)

### 2.2.2 创建跨域的服务，自定成可以跨域访问的源

#### 2.2.2.1 创建node跨域的服务

```javascript
let express = require('express');
let app = express();
let whiteList = ['http://localhost:3000']
app.use(function(req, res, next){
    let origin = req.headers.origin;
    if(whiteList.includes(origin)){
        // 设置哪个源可以访问本服务
        res.setHeader('Access-Control-Allow-Origin', origin);
    }
    next();
})
app.get('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

#### 2.2.2.2 改写`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        let xhr = new XMLHttpRequest;
        xhr.open('GET', 'http://localhost:4000/getData', true);
        xhr.onreadystatechange = function(){
            if(xhr.readyState === 4){
                if((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304){
                    console.log(xhr.response)
                }
            }
        }
        xhr.send();
    </script>
</body>
</html>
```

#### 2.2.2.3 测试cors跨域

页面访问：[http://localhost:3000/index.html](http://localhost:3000/index.html)

### 2.2.3 增加自定义请求头

#### 2.2.3.1 改写`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        let xhr = new XMLHttpRequest;
        xhr.open('GET', 'http://localhost:4000/getData', true);
        xhr.setRequestHeader('name', 'testHead1');
        xhr.onreadystatechange = function(){
            if(xhr.readyState === 4){
                if((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304){
                    console.log(xhr.response)
                }
            }
        }
        xhr.send();
    </script>
</body>
</html>
```

#### 2.2.3.2 改写跨域的服务代码

**注意**：如果Access-Control-Allow-Origin的值设定为*的话，将不能携带cookie，即使设置Access-Control-Allow-Headers为true也不行。

```javascript
let express = require('express');
let app = express();
let whiteList = ['http://localhost:3000']
app.use(function(req, res, next){
    let origin = req.headers.origin;
    if(whiteList.includes(origin)){
        // 设置哪个源可以访问本服务
        res.setHeader('Access-Control-Allow-Origin', origin);
        // 设置允许的自定义请求头，多个自定义请求头，以逗号分割，如res.setHeader('Access-Control-Allow-Headers', 'name,age');
        res.setHeader('Access-Control-Allow-Headers', 'name');
    }
    next();
})
app.get('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

### 2.2.4 设定自定义的访问方法

#### 2.2.4.1 改写`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        let xhr = new XMLHttpRequest;
        xhr.open('PUT', 'http://localhost:4000/getData', true);
        xhr.setRequestHeader('name', 'testHead1');
        xhr.onreadystatechange = function(){
            if(xhr.readyState === 4){
                if((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304){
                    console.log(xhr.response)
                }
            }
        }
        xhr.send();
    </script>
</body>
</html>
```

#### 2.2.4.2 改写跨域的服务代码

```javascript
let express = require('express');
let app = express();
let whiteList = ['http://localhost:3000']
app.use(function(req, res, next){
    let origin = req.headers.origin;
    if(whiteList.includes(origin)){
        // 设置哪个源可以访问本服务
        res.setHeader('Access-Control-Allow-Origin', origin);
        // 设置允许的自定义请求头，多个自定义请求头，以逗号分割，如res.setHeader('Access-Control-Allow-Headers', 'name,age');
        res.setHeader('Access-Control-Allow-Headers', 'name');
        // 设置允许的请求方法，多个请求方法，以逗号分割，如res.setHeader('Access-Control-Allow-Methods', 'PUT,DELETE');
        res.setHeader('Access-Control-Allow-Methods', 'PUT');
    }
    next();
})
app.get('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.put('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

### 2.2.5 cors跨域发送两次请求问题

浏览器的同源策略，就是出于安全考虑，浏览器会限制从脚本发起的跨域HTTP请求（比如异步请求GET, POST, PUT, DELETE, OPTIONS等等），所以浏览器会向所请求的服务器发起两次请求，第一次是浏览器使用OPTIONS方法发起一个预检请求，第二次才是真正的异步请求，第一次的预检请求获知服务器是否允许该跨域请求：如果允许，才发起第二次真实的请求；如果不允许，则拦截第二次请求。<br />
Access-Control-Max-Age用来指定本次预检请求的有效期，单位为秒，，在此期间不用发出另一条预检请求。<br />
例如：<br />
`resp.addHeader("Access-Control-Max-Age", "0")`，表示每次异步请求都发起预检请求，也就是说，发送两次请求。<br />
`resp.addHeader("Access-Control-Max-Age", "1800")`，表示隔30分钟才发起预检请求。也就是说，发送两次请求

为了资源的浪费，我们可以在后台对OPTIONS请求做特殊的处理。

```javascript
let express = require('express');
let app = express();
let whiteList = ['http://localhost:3000']
app.use(function(req, res, next){
    let origin = req.headers.origin;
    if(whiteList.includes(origin)){
        // 设置哪个源可以访问本服务
        res.setHeader('Access-Control-Allow-Origin', origin);
        // 设置允许的自定义请求头，多个自定义请求头，以逗号分割，如res.setHeader('Access-Control-Allow-Headers', 'name,age');
        res.setHeader('Access-Control-Allow-Headers', 'name');
        // 设置允许的请求方法，多个请求方法，以逗号分割，如res.setHeader('Access-Control-Allow-Methods', 'PUT,DELETE');
        res.setHeader('Access-Control-Allow-Methods', 'PUT');
        resp.addHeader("Access-Control-Max-Age", "1800");//表示隔30分钟才发起预检请求。也就是说，发送两次请求
        if(req.method === 'OPTIONS'){
            res.end();//OPTIONS请求不做任何处理
        }
    }
    next();
})
app.get('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.put('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

### 2.2.6 携带Cookie跨域

#### 2.2.6.1 改写`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        let xhr = new XMLHttpRequest;
        document.cookie = "name=zh";
        xhr.withCredentials = true;// 前端设置是否带cookie
        xhr.open('PUT', 'http://localhost:4000/getData', true);
        xhr.setRequestHeader('name', 'testHead1');
        xhr.onreadystatechange = function(){
            if(xhr.readyState === 4){
                if((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304){
                    console.log(xhr.response)
                }
            }
        }
        xhr.send();
    </script>
</body>
</html>
```

#### 2.2.6.2 改写跨域的服务代码

**注意**：如果Access-Control-Allow-Origin的值设定为*的话，将不能携带cookie，即使设置Access-Control-Allow-Headers为true也不行。

```javascript
let express = require('express');
let app = express();
let whiteList = ['http://localhost:3000']
app.use(function(req, res, next){
    let origin = req.headers.origin;
    if(whiteList.includes(origin)){
        // 设置哪个源可以访问本服务
        res.setHeader('Access-Control-Allow-Origin', origin);
        // 设置允许的自定义请求头，多个自定义请求头，以逗号分割，如res.setHeader('Access-Control-Allow-Headers', 'name,age');
        res.setHeader('Access-Control-Allow-Headers', 'name');
        // 设置允许的请求方法，多个请求方法，以逗号分割，如res.setHeader('Access-Control-Allow-Methods', 'PUT,DELETE');
        res.setHeader('Access-Control-Allow-Methods', 'PUT');
        //表示隔30分钟才发起预检请求。也就是说，发送两次请求
        resp.addHeader("Access-Control-Max-Age", "1800");
        // 设置允许跨域cookie
        resp.addHeader("Access-Control-Allow-Credentials", true);
        if(req.method === 'OPTIONS'){
            res.end();//OPTIONS请求不做任何处理
        }
    }
    next();
})
app.get('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.put('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

### 2.2.7 页面接受跨域服务的header信息

CORS请求时，XMLHttpRequest对象的getResponseHeader()方法只能拿到6个基本字段：Cache-Control、Content-Language、Content-Type、Expires、Last-Modified、Pragma。如果想拿到其他字段，就必须在跨域的服务器中用Access-Control-Expose-Headers指定。

#### 2.2.7.1 改写`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        let xhr = new XMLHttpRequest;
        document.cookie = "name=zh";
        xhr.withCredentials = true;// 前端设置是否带cookie
        xhr.open('PUT', 'http://localhost:4000/getData', true);
        xhr.setRequestHeader('name', 'testHead1');
        xhr.onreadystatechange = function(){
            if(xhr.readyState === 4){
                if((xhr.status >= 200 && xhr.status < 300) || xhr.status === 304){
                    console.log(xhr.response);
                    // 跨域获取服务器给出的头信息
                    console.log(xhr.getResponseHeader('name'));
                }
            }
        }
        xhr.send();
    </script>
</body>
</html>
```

#### 2.2.7.2 改写跨域的服务代码

```javascript
let express = require('express');
let app = express();
let whiteList = ['http://localhost:3000']
app.use(function(req, res, next){
    let origin = req.headers.origin;
    if(whiteList.includes(origin)){
        // 设置哪个源可以访问本服务
        res.setHeader('Access-Control-Allow-Origin', origin);
        // 设置允许的自定义请求头，多个自定义请求头，以逗号分割，如res.setHeader('Access-Control-Allow-Headers', 'name,age');
        res.setHeader('Access-Control-Allow-Headers', 'name');
        // 设置允许的请求方法，多个请求方法，以逗号分割，如res.setHeader('Access-Control-Allow-Methods', 'PUT,DELETE');
        res.setHeader('Access-Control-Allow-Methods', 'PUT');
        //表示隔30分钟才发起预检请求。也就是说，发送两次请求
        resp.addHeader("Access-Control-Max-Age", "1800");
        // 设置允许跨域cookie
        resp.addHeader("Access-Control-Allow-Credentials", true);
        //允许跨域获取本服务提供的头信息
        resp.addHeader("Access-Control-Expose-Headers", 'name');
        if(req.method === 'OPTIONS'){
            res.end();//OPTIONS请求不做任何处理
        }
    }
    next();
})
app.get('/getData', function(req, res){
    res.setHeader('name', '跨域响应的头信息');
    res.end("cors跨域响应");
});
app.put('/getData', function(req, res){
    res.end("cors跨域响应");
});
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

## 2.3 postMessage+iframe跨域

### 2.3.1 服务器a

位置：`postmessage/a/a.js`

端口号：3000

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(3000);
```

位置：`postmessage/a/a.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <iframe src="http://localhost:4000/b.html" frameborder="0" id="frame" onload="load()"></iframe>
    <script>
        function load(){
            let frame = document.getElementById("frame");
            frame.contentWindow.postMessage('postMessage', 'http://localhost:4000');
        }
        window.onmessage = function (e){
                console.log(e.data);
        }
    </script>
</body>
</html>
```

### 2.3.2 服务器b

位置：`postmessage/b/b.js`

端口号：4000

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

位置：`postmessage/b/b.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        window.onmessage = function (e){
            console.log(e.data);
            e.source.postMessage('postMessage返回信息', e.origin);
        }
    </script>
</body>
</html>
```

### 2.3.3 测试

页面访问：[http://localhost:3000/a.html](http://localhost:3000/a.html)

![](/home/zh/%E6%96%87%E6%A1%A3/%E8%B7%A8%E5%9F%9F/%E8%B7%A8%E5%9F%9F%E9%97%AE%E9%A2%98_media/image-20200419152243569.png#alt=image-20200419152243569)

## 2.4 `window.name` + iframe跨域

window.name属性的独特之处：name值在不同的页面（甚至不同域名）加载后依旧存在，并且可以支持非常长的 name 值（2MB）。

### 2.4.1 服务器a

位置：`windowname/ab/a.js`

端口号：3000

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(3000);
```

位置：`windowname/ab/a.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <iframe src="http://localhost:4000/c.html" frameboder="0" onload="load()" id="iframe"></iframe>
    <script>
        let first = true;
        function load(){
            let iframe = document.getElementById("iframe");
            if(first){
                iframe.src = 'http://localhost:3000/b.html';
                first = false;
            }else{
                console.log(iframe.contentWindow.name);
            }
        }
    </script>
</body>
</html>
```

位置：`windowname/ab/b.html`

中间代理页，与a.html同域，内容为空即可。

### 2.4.2 服务器c

位置：`windowname/c/c.js`

端口号：4000

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

位置：`windowname/c/c.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        window.name = "c.html window.name";
    </script>
</body>
</html>
```

### 2.4.3 测试

页面访问：[http://localhost:3000/a.html](http://localhost:3000/a.html)

![](/home/zh/%E6%96%87%E6%A1%A3/%E8%B7%A8%E5%9F%9F/%E8%B7%A8%E5%9F%9F%E9%97%AE%E9%A2%98_media/image-20200419160827050.png#alt=image-20200419160827050)

## 2.5 location.hash + iframe跨域

路径后面的hash值可以用来通信

实现原理： a欲与c跨域相互通信，通过中间页b来实现。 三个页面，不同域之间利用iframe的location.hash传值，相同域之间直接js访问来通信。

目的：`a.html`想访问`c.html`

具体实现：`a.html` 给`c.html`传递一个hash值，`c.html`收到hash值后，`c.html`把hash值传递给`b.html`，`b.html`将结果放到`a.html`的hash值中

### 2.5.1 服务器a

位置：`locationhash/ab/a.js`

端口号：3000

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(3000);
```

位置：`locationhash/ab/a.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <iframe src="http://localhost:4000/c.html#a.html"></iframe>
    <script>
        window.onhashchange = function () {
            console.log(location.hash);
        }
    </script>
</body>
</html>
```

位置：`locationhash/ab/b.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        window.parent.parent.location.hash = location.hash
    </script>
</body>
</html>
```

### 2.5.2 服务器c

位置：`locationhash/c/c.js`

端口号：4000

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(4000);
```

位置：`locationhash/c/c.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        console.log(location.hash);
        let iframe = document.createElement('iframe');
        iframe.src = 'http://localhost:3000/b.html#c.html';
        document.body.appendChild(iframe);
    </script>
</body>
</html>
```

### 2.5.3 测试

页面访问：[http://localhost:3000/a.html](http://localhost:3000/a.html)

![](/home/zh/%E6%96%87%E6%A1%A3/%E8%B7%A8%E5%9F%9F/%E8%B7%A8%E5%9F%9F%E9%97%AE%E9%A2%98_media/image-20200419163427619.png#alt=image-20200419163427619)

## 2.6 document.domain + iframe跨域

此方案仅限主域相同，子域不同的跨域应用场景。

实现原理：两个页面都通过js强制设置document.domain为基础主域，就实现了同域。

### 2.6.1 配置本机虚拟域名

修改hosts文件，加入两个虚拟域名：

> 127.0.0.1 a.zh.com

> 127.0.0.1 b.zh.com


### 2.6.2 服务器

位置：`locationhash/ab.js`

端口号：3000

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(3000);
```

### 2.6.3 页面a

位置：`locationhash/a.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <iframe src="http://b.zh.com:3000/b.html" id="iframe" onload="load()"></iframe>
    <script>
        document.domain = 'zh.com';
        function load(){
            console.log(iframe.contentWindow.b);
        }
    </script>
</body>
</html>
```

### 2.6.4 页面b

位置：`locationhash/b.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        document.domain = 'zh.com';
        var b = "b.html text";
    </script>
</body>
</html>
```

### 2.6.5 测试

页面访问：[http://a.zh.com:3000/a.html](http://a.zh.com:3000/a.html)

![](/home/zh/%E6%96%87%E6%A1%A3/%E8%B7%A8%E5%9F%9F/%E8%B7%A8%E5%9F%9F%E9%97%AE%E9%A2%98_media/image-20200419171223125.png#alt=image-20200419171223125)

## 2.7 WebSocket协议跨域

WebSocket protocol是HTML5一种新的协议。它实现了浏览器与服务器全双工通信，同时允许跨域通讯，是server push技术的一种很好的实现。<br />
原生WebSocket API使用起来不太方便，也不兼容，一般使用Socket.io，它很好地封装了webSocket接口，提供了更简单、灵活的接口，也对不支持webSocket的浏览器提供了向下兼容。

### 2.7.1 WebSocket API方式

#### 2.7.1.1 安装ws

```shell
npm install ws
```

#### 2.7.1.2 本地服务器

位置：`websocket/a/server.js`

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(3000);
```

位置：`websocket/a/socket.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script>
        let socket = new WebSocket('ws://localhost:4000');
        socket.onopen = function () {
            socket.send('socket.html 发送消息');
        }
        socket.onmessage = function (e) {
            console.log(e.data);
        }
    </script>
</body>
</html>
```

#### 2.7.1.3 远程服务器

位置：`websocket/b.js`

端口号：4000

```javascript
let express = require('express');
let app = express();
let WebSocket = require("ws");
let wss = new WebSocket.Server({port:4000});
wss.on('connection', function (ws) {
    ws.on('message', function (data) {
        console.log(data);
        ws.send("跨域服务端返回消息");
    });
});
```

#### 2.7.1.4 测试

页面访问：[http://localhost:3000/socket.html](http://localhost:3000/socket.html)

### 2.7.2 `Socket.io`方式

#### 2.7.2.1 安装依赖包

- `npm install http`
- `npm install socket.io`

#### 2.7.2.2 本地服务器

位置：`soketio/a/a.js`

```javascript
let express = require('express');
let app = express();
app.use(express.static(__dirname))//以当前目录作为静态资源目录
app.listen(3000);
```

位置：`websocket/a/a.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div>user input：<input type="text"></div>
    <script src="https://cdn.bootcss.com/socket.io/2.2.0/socket.io.js"></script>
    <script>
        var socket = io('http://localhost:4000');

        // 连接成功处理
        socket.on('connect', function() {
            // 监听服务端消息
            socket.on('message', function(msg) {
                console.log('data from server: ---> ' + msg); 
            });

            // 监听服务端关闭
            socket.on('disconnect', function() { 
                console.log('Server socket has closed.'); 
            });
        });

        document.getElementsByTagName('input')[0].onblur = function() {
            socket.send(this.value);
        };
    </script>
</body>
</html>
```

#### 2.7.2.3 远程服务器

位置：`soketio/server.js`

```javascript
var http = require('http');
var socket = require('socket.io');

// 启http服务
var server = http.createServer(function(req, res) {
    res.writeHead(200, {
        'Content-type': 'text/html'
    });
    res.end();
});

server.listen(4000);
console.log('Server is running at port 4000...');

// 监听socket连接
socket.listen(server).on('connection', function(client) {
    // 接收信息
    client.on('message', function(msg) {
        client.send('hello：' + msg);
        console.log('data from client: ---> ' + msg);
    });

    // 断开处理
    client.on('disconnect', function() {
        console.log('Client socket has closed.'); 
    });
});
```

#### 2.7.2.4 测试

页面访问：[http://localhost:3000/a.html](http://localhost:3000/a.html)

## 2.8 nginx代理跨域

### 2.8.1 nginx配置解决iconfont跨域

浏览器跨域访问js、css、img等常规静态资源被同源策略许可，但iconfont字体文件(eot|otf|ttf|woff|svg)例外，此时可在nginx的静态资源服务器中配置文件（`nginx根目录/conf/nginx.conf`）中加入以下配置。

```
location / {
  add_header Access-Control-Allow-Origin *;
}
```

### 2.8.2 nginx反向代理接口跨域
