# nginx入门

# 1 nginx概述

## 1.1 什么是nginx

Nginx是一款高性能的**http 服务器**/**反向代理服务器**及**电子邮件（IMAP/POP3）代理服务器**。

由俄罗斯的程序设计师Igor Sysoev所开发，官方测试nginx**能够支撑5万并发连接**，并且cpu、内存等**资源消耗却非常低**，**运行非常稳定**。

## 1.2 应用场景

- **http服务器**：Nginx是一个http服务可以独立提供http服务。可以做网页静态服务器。
- **虚拟主机**：可以实现在一台服务器虚拟出多个网站。例如个人网站使用的虚拟主机。
- **反向代理，负载均衡**：当网站的访问量达到一定程度后，单台服务器不能满足用户的请求时，需要用多台服务器集群可以使用nginx做反向代理。并且多台服务器可以平均分担负载，不会因为某台服务器负载高宕机而某台服务器闲置的情况。

# 2 nginx安装

## 2.1 安装准备和注意事项

**官方网站**：[http://nginx.org/](http://nginx.org/)

**使用版本注意的问题**：

- 使用的版本是1.8.0版本。
- 安装包中stable的是稳定版本。
- nginx的window版本一般就测试用
- 不要用太新的版本
- nginx提供源代码

**要求的安装环境（测试环境：CentOS）**：

- 需要安装**gcc**的环境。`yum install gcc-c++`
- 第三方的开发包。

  - **PCRE**

    - PCRE(Perl Compatible Regular Expressions)是一个Perl库，包括 perl 兼容的正则表达式库。nginx的http模块使用pcre来解析正则表达式，所以需要在linux上安装pcre库。
    - 安装命令：`yum install -y pcre pcre-devel`

      - 注：pcre-devel是使用pcre开发的一个二次开发库。nginx也需要此库。
  - **zlib**

    - zlib库提供了很多种压缩和解压缩的方式，nginx使用zlib对http包的内容进行gzip，所以需要在linux上安装zlib库。
    - 安装命令：`yum install -y zlib zlib-devel`
  - **openssl**

    - OpenSSL 是一个强大的安全套接字层密码库，囊括主要的密码算法、常用的密钥和证书封装管理功能及SSL协议，并提供丰富的应用程序供测试或其它目的使用。
    - nginx不仅支持http协议，还支持https（即在ssl协议上传输http），所以需要在linux安装openssl库。
    - 安装命令：`yum install -y openssl openssl-devel`

## 2.2 安装步骤

第一步：把nginx的源码包上传到linux系统

第二步：解压缩

```shell
[root@localhost ~]# tar zxf nginx-1.8.0.tar.gz
```

第三步：使用configure命令创建一makeFile文件。

```
./configure \
--prefix=/usr/local/nginx \
--pid-path=/var/run/nginx/nginx.pid \
--lock-path=/var/lock/nginx.lock \
--error-log-path=/var/log/nginx/error.log \
--http-log-path=/var/log/nginx/access.log \
--with-http_gzip_static_module \
--http-client-body-temp-path=/var/temp/nginx/client \
--http-proxy-temp-path=/var/temp/nginx/proxy \
--http-fastcgi-temp-path=/var/temp/nginx/fastcgi \
--http-uwsgi-temp-path=/var/temp/nginx/uwsgi \
--http-scgi-temp-path=/var/temp/nginx/scgi
```

**注意**：启动nginx之前，上边makeFile文件将临时文件目录指定为了`/var/temp/nginx`，故需要在`/var`下创建temp及nginx目录

```shell
[root@localhost sbin]# mkdir /var/temp/nginx/client -p
```

第四步：make

第五步：make install

执行万make install后：

```shell
[root@localhost nginx-1.8.0]# cd /usr/local/nginx/
[root@localhost nginx-1.8.0]# ll
total 12
drwxr-xr-x. 2 root root 4096 Mar 30 20:34 conf
drwxr-xr-x. 2 root root 4096 Mar 30 20:34 html
drwxr-xr-x. 2 root root 4096 Mar 30 20:34 sbin
[root@localhost nginx-1.8.0]#
```

查询命令：`ps aux|grep nginx`

- a：all
- u：用户
- x：
- |：前一个命令的输入作为后面命令的输入

# 3 nginx使用

## 3.1 启动nginx

```shell
[root@localhost sbin]# ./nginx
```

## 3.2 关闭nginx

```shell
[root@localhost sbin]# ./nginx -s stop
```

推荐使用：

```shell
[root@localhost sbin]# ./nginx -s quit
```

## 3.3 重启nginx

- 
先关闭后启动。

- 
  刷新配置文件：

```shell
[root@localhost sbin]# ./nginx -s reload
```



## 3.4 访问nginx

直接在浏览器nginx主机的ip地址，就能访问nginx。默认是80端口。

**注意**：需要查看是否关闭防火墙。



# 4 配置nginx

Nginx配置文件路径：`/usr/local/nginx/nginx.conf`

```
user  nobody nobody;	#定义Nginx运行的用户和用户组
worker_processes  4;	#nginx进程数，建议设置为等于CPU总核心数。
error_log  logs/error.log	info;	#全局错误日志定义类型，[ debug | info | notice | warn | error | crit ]
worker_rlimit_nofile 1024;	#一个nginx进程打开的最多文件描述符数目，所以建议与ulimit -n的值保持一致。
pid	logs/nginx.pid;	#进程文件

#工作模式及连接数上限
events {
		use epoll;#参考事件模型，use [ kqueue | rtsig | epoll | /dev/poll | select | poll ]; epoll模型是Linux 2.6以上版本内核中的高性能网络I/O模型
	    worker_connections  1024;#单个进程最大连接数（最大连接数=连接数*进程数）
}

#设定http服务器，利用它的反向代理功能提供负载均衡支持
http {
    include       mime.types;#文件扩展名与文件类型映射表
    default_type  application/octet-stream;#默认文件类型
    #设定负载均衡的服务器列表
    upstream  tomcatxxxcom  {  
         server   192.168.56.200:8080;  
         server   192.168.56.201:8080; 	 
    }
	#设定日志格式
    log_format  www_xy_com  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
					  
    sendfile        on;#开启高效文件传输模式，sendfile指令指定nginx是否调用sendfile函数来输出文件，对于普通应用设为 on，如果用来进行下载等应用磁盘IO重负载应用，可设置为off，以平衡磁盘与网络I/O处理速度，降低系统的负载。注意：如果图片显示不正常把这个改成off。
    keepalive_timeout  65; #长连接超时时间，单位是秒

    #gzip  on;
	#设定虚拟主机，默认为监听80端口
    server {
        listen       80;
        server_name  tomcat.xxx.com; # 域名可以有多个，用空格隔开

        #charset koi8-r;
		#设定本虚拟主机的访问日志
        access_log  /data/logs/access.log  www_xy_com;
		#对 "/" 启用反向代理 
	   	location / {
			   proxy_pass        http://tomcatxxxcom;  
               proxy_set_header   Host             $host;  
               proxy_set_header   X-Real-IP        $remote_addr;  
               proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        }
        
        #error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

