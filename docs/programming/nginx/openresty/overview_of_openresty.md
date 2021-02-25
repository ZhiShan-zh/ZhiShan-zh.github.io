# OpenResty概述

# 1 简介

OpenResty® 是一个基于 Nginx 与 Lua 的高性能 Web 平台，其内部集成了大量精良的 Lua 库、第三方模块以及大多数的依赖项。用于方便地搭建能够处理超高并发、扩展性极高的动态 Web 应用、Web 服务和动态网关。

OpenResty® 通过汇聚各种设计精良的 Nginx 模块（主要由 OpenResty 团队自主开发），从而将 Nginx 有效地变成一个强大的通用 Web 应用平台。这样，Web 开发人员和系统工程师可以使用 Lua 脚本语言调动 Nginx 支持的各种 C 以及 Lua 模块，快速构造出足以胜任 10K 乃至 1000K 以上单机并发连接的高性能 Web 应用系统。

OpenResty® 的目标是让你的Web服务直接跑在 Nginx 服务内部，充分利用 Nginx 的非阻塞 I/O 模型，不仅仅对 HTTP 客户端请求,甚至于对远程后端诸如 MySQL、PostgreSQL、Memcached 以及 Redis 等都进行一致的高性能响应。

## 1.1 Nginx的优点

Nginx设计为一个主进程多个工作进程的工作模式，每个进程是单线程来处理多个连接，而且每个工作进程采用了非阻塞I/O来处理多个连接，从而减少了线程上下文切换，实现了工人的高性能、高并发。因此，在生产环境中通常把CPU绑定给Nginx工作进程，从而提升性能。另外，因为单线程工作模式的特点，内存占用就非常少了。

Nginx更改配置后重启速度非常快，可以达到毫秒级，而且支持不停止Nginx进行升级Nginx版本、动态加载Nginx配置。

Nginx模块非常多，功能也很强劲，可以作为HTTP负载均衡，TCP负载均衡，还可以很容易地实现内容缓存、Web服务器、反向代理、访问控制等功能。

## 1.2 Lua的优点

- Lua是一种轻量级、可嵌入的脚本语言，可以非常容易地嵌入到其他语言中使用。
- Lua提供了协程并发，即以同步调用的方式进行异步执行，从而实现并发，比起回调机制的并发来说代码更容易编写和理解，排查问题也更容易。
- Lua还提供了闭包机制，函数可以作为First Class Value进行参数传递。
- 实现了标记清楚垃圾收集。

- 因为Lua的小巧轻量级，可以在Nginx从嵌入Lua VM，请求的时候创建一个VM，请求结束的时候回收VM。

## 1.3 什么是ngx_lua

ngx_lua是章亦春编写的Nginx的一个模块，将Lua嵌入到Nginx中，从而可以使用Lua来编写脚本，部署到Nginx中运行，即Nginx变成了一个Web容器。这样开发人员可以使用Lua语言开发高性能Web应用了。

ngx_lua提供了与Nginx交互的很多API，对于开发人员来说只需要学习这些API就可以进行功能开发，而对于开发Web应用来说，其和Servlet类似，无外乎就是知道接收请求、参数解析、功能处理、返回响应这几步的API是什么样子的。



## 1.4 OpenResty生态

OpenResty提供了常用的ngx_lua开发模块，如：

- `lua-resty-memcached`：memcached
- `lua-resty-mysql`：mysql
- `lua-resty-redis`：redis
- `lua-resty-dns`：dns
- `lua-resty-traffic`：限流
- `lua-resty-template`：模板渲染

## 1.5 OpenResty使用场景

目前CDN厂商使用OpenResty较多。

- **Web应用**：会进行一些业务逻辑处理，甚至进行耗CPU的模板渲染，一般流程包括MySQL、Redis、HTTP获取数据、业务处理、产生Json、XML、模板渲染内容，比如京东的列表页、商品详情页。
- **接入网关**：实现如数据校验前置、缓存前置、数据过滤、API请求聚合、A/B测试、灰度发布、降级、监控等功能，比如，京东的交易大Nginx节点、无线部门正在开发的无线网关、单品页统一服务、实时价格、动态服务。
- **Web防火墙**：可以进行IP、URL、UserAgent、Referer黑名单、限流等功能。
- **缓存服务器**：可以对相应内容进行缓存，减少到达后端的请求，从而提升性能。
- **其他**：如静态资源服务器、消息推送服务、缩略图剪裁等。

# 2 OpenResty常用架构

## 2.1 架构模式

### 2.1.1 负载均衡

![](https://ZhiShan-zh.github.io/media/nginx_openresty_20210208131408.png)

基本流程：

- LVS+HAProxy将流量转发给核心Nginx1和核心Nginx2，实现流量负载均衡，此处可以使用如轮询、一致性哈希等调度算法来实现负载的转发。

- 核心Nginx会根据请求特征如“Host:item.jd.com”，转发给相应的业务Nginx节点，如单品页Nginx1。
  - 核心Nginx：本层是无状态的，可以在这一层实现：
    - 流量分组：内网和外网隔离、爬虫和非爬虫流量隔离
    - 内容缓存
    - 请求头过滤
    - 故障切换：机房故障切换到其他机房
    - 限流
    - 防火墙
  - 业务Nginx：这一层的Nginx和业务有关联，实现业务的一些通用逻辑，如单品页Nginx
    - 业务逻辑
    - 反向代理到如Tomcat
    - 内容压缩：放在这一层的目的是减少核心Nginx的CPU压力，将压力分散到各业务Nginx
    - A/B测试
    - 降级

不管是核心Nginx还是业务Nginx，都应该是无状态设计，可以水平扩容。

![](https://ZhiShan-zh.github.io/media/nginx_openresty_20210224110525.png)

业务Nginx一般会把请求直接转发给后端的业务应用，如Tomcat、PHP，即将请求内部转发到相应的业务应用。当有的Tomcat出现问题时，可以在这一层摘掉。或者有的业务路径变了在这一层进行重写。或者有的后端Tomcat压力太大也可以在这一层降级，减少对后端的冲击。或者业务需要灰度发布时，也可以在这一层Nginx上控制。

### 2.1.2 单机闭环

所谓单机闭环即所有想要的数据都能从本服务器中直接获取，在大多数时候无需通过网络去其他服务器获取。

![](https://ZhiShan-zh.github.io/media/nginx_openresty_20210224145510.png)

- 左图的应用场景是Nginx应用谁也不依赖。直接使用lua处理一些请求。
- 中图的应用场景是读取本机文件系统，如静态资源合并。

## 2.2 关键节点解释

