# Nginx配置虚拟主机

# 1 概述

**配置虚拟主机**：就是在一台服务器启动多个网站。

比如通过域名访问一台服务器上不同的网站：浏览器输入`www.zh.com`访问本机的网站xxx，浏览器输入`image.zh.com`访问的是本机的网站yyy。

有比如通过端口号不同访问一台服务器上不同的网站：浏览器输入`http://localhost:8080`访问本机的网站xxx，浏览器输入`http://localhost:8081`访问的是本机的网站yyy。

**区分不同的网站**：

- 域名不同：
- 端口不同

# 2通过端口区分不同虚拟机

Nginx的配置文件：`/usr/local/nginx/conf/nginx.conf`

```
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {	#一个server节点就是一个虚拟主机
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;	#html是nginx安装目录下的html
            index  index.html index.htm;
        }
    }
}
```

**添加虚拟主机**：

```
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }
    }
    server {
        listen       81;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html-81;
            index  index.html index.htm;
        }
    }
}
```

**重新加载配置文件**：

```shell
[root@localhost nginx]# sbin/nginx -s reload
```

# 3 通过域名区分虚拟主机

## 3.1 什么是域名

域名就是网站，如：

- `www.baidu.com`
- `www.taobao.com`
- `www.jd.com`

**DNS服务器**：（域名解析服务器）把域名解析为ip地址。保存的就是域名和ip的映射关系。

如：8.8.8.8是google DNS服务器

**顶级域名**：

- `.com`
- `.cn`

**一级域名**：（新买域名，配置好映射关系后，DNS服务器24小时内都可以更新上，一般是5、6个小时）

- `baidu.com`
- `taobao.com`
- `jd.com`

**二级域名**：（有了一级域名，二三级域名可以随意定义）

- `www.baidu.com`
- `image.baidu.com`
- `item.baidu.com`

**三级域名**：

- `1.image.baidu.com`
- `aaa.image.baidu.com`

一个域名对应一个ip地址，一个ip地址可以被多个域名绑定。

## 3.2 本地测试域名

本地测试域名可以修改hosts文件。

Windows平台hosts文件位置：`C:\Windows\System32\drivers\etc\hosts`

Linux和Mac平台hosts文件位置：`/etc/hosts`

可以配置域名和ip的映射关系（如`127.0.0.1 www.baidu.com`），如果hosts文件中配置了域名和ip的对应关系，不需要走dns服务器。

## 3.3 nginx的配置

**指出**：此时端口号都是80，配置其他端口号默认都访问80端口

```
#user  nobody;
worker_processes  1;
 
#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;
 
#pid        logs/nginx.pid;
 
 
events {
    worker_connections  1024;
}
 
 
http {
    include       mime.types;
    default_type  application/octet-stream;
 
    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
 
    #access_log  logs/access.log  main;
 
    sendfile        on;
    #tcp_nopush     on;
 
    #keepalive_timeout  0;
    keepalive_timeout  65;
 
    #gzip  on;
 
    server {
        listen       80;
        server_name  localhost;
 
        #charset koi8-r;
 
        #access_log  logs/host.access.log  main;
 
        location / {
            root   html;
            index  index.html index.htm;
        }
    }
    server {
        listen       81;
        server_name  localhost;
 
        #charset koi8-r;
 
        #access_log  logs/host.access.log  main;
 
        location / {
            root   html-81;
            index  index.html index.htm;
        }
    }
    server {
        listen       80;
        server_name  www.taobao.com;
 
        #charset koi8-r;
 
        #access_log  logs/host.access.log  main;
 
        location / {
            root   html-taobao;
            index  index.html index.htm;
        }
    }
    server {
        listen       80;
        server_name  www.baidu.com;
 
        #charset koi8-r;
 
        #access_log  logs/host.access.log  main;
 
        location / {
            root   html-baidu;
            index  index.html index.htm;
        }
    }
}
```
