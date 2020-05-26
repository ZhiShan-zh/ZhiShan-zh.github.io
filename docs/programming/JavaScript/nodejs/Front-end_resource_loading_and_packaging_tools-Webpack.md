# 前端资源加载、打包工具——Webpack

# 1 Webpack介绍

Webpack 是一个前端资源加载/打包工具。它将根据模块的依赖关系进行静态分析，然后将这些模块按照指定的规则生成对应的静态资源。

Webpack 可以将多种静态资源 js、css、less 转换成一个静态文件，减少了页面的请求。

# 2 Webpack安装

全局安装：

```shell
npm install webpack ‐g
npm install webpack‐cli ‐g
```

安装后查看版本号：

```shell
webpack ‐v
```

# 3 快速入门

## 3.1 JS打包

创建src文件夹，创建`bar.js`：

```js
exports.info=function(str){
	document.write(str);
}
```

src下创建`logic.js`：

```shell
exports.add=function(a,b){
	return a+b;
}
```

src下创建`main.js`：

```shell
var bar= require('./bar');
var logic= require('./logic');
bar.info( 'Hello world!'+ logic.add(100,200));
```

创建配置文件`webpack.config.js`，该文件与src处于同级目录

```js
// 读取当前目录下src文件夹中的main.js（入口文件）内容，把对应的js文件打包，打包后的文件放入当前目录的dist文件夹下，打包后的js文件名为bundle.js
var path = require("path");
module.exports = {
    entry: './src/main.js',
    output: {
        path: path.resolve(__dirname, './dist'),
        filename: 'bundle.js'
    }
};
```

执行编译命令`webpack`，执行后查看bundle.js 会发现里面包含了上面两个js文件的内容

创建`index.html` ,引用`bundle.js`：

```html
<!doctype html>
<html>
    <head>
    </head>
    <body>
    	<script src="dist/bundle.js"></script>
    </body>
</html>
```

## 3.2 CSS打包

安装style-loader和css-loader Webpack本身只能处理JavaScript模块，如果要处理其他类型的文件，就需要使用loader进行转换。

Loader 可以理解为是模块和资源的转换器，它本身是一个函数，接受源文件作为参数，返回转换的结果。这样，我们就可以通过 require 来加载任何类型的模块或文件，比如CoffeeScript、 JSX、 LESS 或图片。

首先需要安装相关Loader插件（`cnpm install style‐loader css‐loader ‐‐save‐dev`）：

- `css-loader`：将 css 装载到 javascript；
- `style-loader `：让 javascript 认识css

修改`webpack.config.js`：

```js
var path = require("path");
module.exports = {
    entry: './src/main.js',
    output: {
        path: path.resolve(__dirname, './dist'),
        filename: 'bundle.js'
    },
    module: {
    	rules: [
            {
                test: /\.css$/,
                use: ['style‐loader', 'css‐loader']
            }
        ]
    }
};
```

在src文件夹创建css文件夹，css文件夹下创建`test.css`

```css
body{
	background:red;
}
```

修改main.js ，引入`test.css`

```js
require('./test.css');
```

重新运行webpack，然后访问`index.html`看看其背景是不是已经变成红色？