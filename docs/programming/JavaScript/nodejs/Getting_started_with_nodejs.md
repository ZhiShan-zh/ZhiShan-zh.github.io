# Nodejs入门

# 1 控制台输出

方式一：通过nodejs运行js文件在控制台输出

文件`test.js`内容：

```js
var a=1;
var b=2;
console.log(a+b);
```

运行：

```shell
node test.js
```

方式二：只在在终端运行命令输出

```shell
[zh@zh-inspironn4050 ~]$ node
Welcome to Node.js v12.16.2.
Type ".help" for more information.
> var a = 1;
undefined
> var b = 2;
undefined
> console.log(a+b);
3
undefined
> 
```

# 2 函数

文件`test.js`内容：

```js
var c=add(100,200);
console.log(c);
function add(a,b){
	return a+b;
}
```

# 3 模块化编程

文件`test.js`内容：

```js
exports.add=function(a,b){
	return a+b;
}
```

文件`main.js`内容：

```js
var test= require('./test');
console.log(test.add(400,600));
```

# 4 内置web服务器——http

## 4.1 创建服务器

文件`server.js`内容：

```js
var http = require('http');
http.createServer(function (request, response) {
    // 发送 HTTP 头部
    // HTTP 状态值: 200 : OK
    // 内容类型: text/plain
    response.writeHead(200, {'Content‐Type': 'text/plain'});
    // 发送响应数据 "Hello World"
    response.end('Hello World\n');
}).listen(8888);
// 终端打印如下信息
console.log('Server running at http://127.0.0.1:8888/');
```

启动服务端：`node server.js`

浏览器访问：`http://localhost:8888/`

页面显示内容：Hello World

## 4.2 理解服务端渲染

文件`server.js`内容：

```js
var http = require('http');
http.createServer(function (request, response) {
    // 发送 HTTP 头部
    // HTTP 状态值: 200 : OK
    // 内容类型: text/plain
    response.writeHead(200, {'Content‐Type': 'text/plain'});
    // 发送响应数据 "Hello World"
    for(var i=0;i<3;i++){
   	 response.write('Hello World\n');
    } 
    response.end('');
}).listen(8888);
// 终端打印如下信息
console.log('Server running at http://127.0.0.1:8888/');
```

启动服务端：`node server.js`

浏览器访问：`http://localhost:8888/`

页面显示内容：

> Hello World
>
> Hello World
>
> Hello World

我们右键“查看源代码”发现，并没有我们写的for循环语句，而是直接的10条Hello World，这就说明这个循环是在服务端完成的，而非浏览器（客户端）来完成。这与我们原来的JSP很是相似。

## 4.3 接收参数

文件`server.js`内容：

```js
var http = require('http');
var url = require('url');
http.createServer(function(request, response){
    response.writeHead(200, {'Content‐Type': 'text/plain'});
    // 解析 url 参数
    var params = url.parse(request.url, true).query;
    response.write("name:" + params.name);
    response.write("\n");
    response.end();
}).listen(8888);
console.log('Server running at http://127.0.0.1:8888/');
```

启动服务端：`node server.js`