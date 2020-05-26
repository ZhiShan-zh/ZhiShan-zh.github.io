# VueJS中的Ajax

# 1 vue-resource

vue-resource是Vue.js的插件提供了使用XMLHttpRequest或JSONP进行Web请求和处理响应的服务。 当vue更新到2.0之后，作者就宣告不再对vue-resource更新，而是推荐的axios。

vue-resource的[github](https://github.com/pagekit/vue-resource)。

# 2 axios

Axios 是一个基于 promise 的 HTTP 库，可以用在浏览器和`node.js`中。
axios的[github](https://github.com/axios/axios)。

## 2.1 安装axios

`npm install axios`或`bower install axios`。

## 2.2 引入axios

如果使用的是ES6，则可以使用如下两种方式引入axios：

- `import axios from 'axios';`
- `<script src="https://unpkg.com/axios/dist/axios.min.js"></script>`

## 2.3 使用

可以通过向 `axios` 传递相关配置来创建请求。

为方便起见，为所有支持的请求方法提供了别名：

- `axios.request(config)`
- `axios.get(url[, config])`
- `axios.delete(url[, config])`
- `axios.head(url[, config])`
- `axios.post(url[, data[, config]])`
- `axios.put(url[, data[, config]])`
- `axios.patch(url[, data[, config]])`

在使用别名方法时， `url`、`method`、`data` 这些属性都不必在配置中指定。

### 2.3.1 get请求

```javascript
// 发送 GET 请求（默认的方法）
axios('/user/12345');
```

使用别名：

```js
//通过给定的ID来发送请求
axios.get('/user?ID=12345')
.then(function(response){
	console.log(response);
})
.catch(function(err){
	console.log(err);
});

//以上请求也可以通过这种方式来发送
axios.get('/user',{
    params:{
    	ID:12345
    }
})
.then(function(response){
	console.log(response);
})
.catch(function(err){
	console.log(err);
});
```

### 2.3.2 post请求

```javascript
// 发送 POST 请求
axios({
  method: 'post',
  url: '/user/12345',
  data: {
    firstName: 'Fred',
    lastName: 'Flintstone'
  }
});
```

使用别名：

```javascript
axios.post('/user',{
    firstName:'Fred',
    lastName:'Flintstone'
})
.then(function(res){
	console.log(res);
})
.catch(function(err){
	console.log(err);
});
```

