# Nginx高可用

# 1 概述


实现理念：要实现nginx的高可用，需要实现备份机。


## 1.1 为什么需要高可用


nginx作为负载均衡器，所有请求都到了nginx，可见nginx处于非常重点的位置，如果nginx服务器宕机后端web服务将无法提供服务，影响严重。


## 1.2 实现高可用的原理


- 为了屏蔽负载均衡服务器的宕机，需要建立一个备份机。
- 主服务器和备份机上都运行高可用（High Availability）监控程序，通过传送诸如“I am alive”这样的信息来监控对方的运行状况。
- 当备份机不能在一定的时间内收到这样的信息时，它就接管主服务器的服务IP并继续提供负载均衡服务；
- 当备份管理器又从主管理器收到“I am alive”这样的信息时，它就释放服务IP地址，这样的主服务器就开始再次提供负载均衡服务。



# 2 keepalived+nginx实现主备


## 2.1 什么是keepalived


keepalived是集群管理中保证集群高可用的一个服务软件，用来防止单点故障。

Keepalived的作用是检测web服务器的状态，如果有一台web服务器死机，或工作出现故障，Keepalived将检测到，并将有故障的web服务器从系统中剔除，当web服务器工作正常后Keepalived自动将web服务器加入到服务器群中，这些工作全部自动完成，不需要人工干涉，需要人工做的只是修复故障的web服务器。


## 2.2 keepalived工作原理


keepalived是以VRRP协议为实现基础的，VRRP全称Virtual Router Redundancy Protocol，即虚拟路由冗余协议。

虚拟路由冗余协议，可以认为是实现路由器高可用的协议，即将N台提供相同功能的路由器组成一个路由器组，这个组里面有一个master和多个backup，master上面有一个对外提供服务的vip（VIP = Virtual IP Address，虚拟IP地址，该路由器所在局域网内其他机器的默认路由为该vip），master会发组播，当backup收不到VRRP包时就认为master宕掉了，这时就需要根据VRRP的优先级来选举一个backup当master。这样的话就可以保证路由器的高可用了。

keepalived主要有三个模块，分别是core、check和VRRP。core模块为keepalived的核心，负责主进程的启动、维护以及全局配置文件的加载和解析。check负责健康检查，包括常见的各种检查方式。VRRP模块是来实现VRRP协议的。


## 2.3 keepalived+nginx实现主备过程


两台nginx，一主一备：192.168.101.3和192.168.101.4

两台tomcat服务器：192.168.101.5、192.168.101.6


1. **初始状态**：

![lu6087rggw61_tmp_2f78cda0909c407c.png](https://zhishan-zh.github.io/media/1586368063974-22dbf901-a600-4c6e-a424-adfdff1ed4fd.png)


2. **主机宕机**：

![lu6087rggw61_tmp_fd8bac4e8681e92.png](https://zhishan-zh.github.io/media/1586368084645-deca2c96-0968-435b-a3e2-17faa8bb163b.png)


3. **主机恢复**：

![lu6087rggw61_tmp_a1cc8886635dc56b.png](https://zhishan-zh.github.io/media/1586368124409-637b7e44-a06c-44b7-bcb9-a0cd440c0b93.png)


## 2.4 安装keepalived


安装包：`keepalived-1.2.15.tar.gz`


分别在主备nginx上安装keepalived，参考“安装手册”进行安装：

安装方法参见：


- keepalived安装手册.docx
- Keepalived权威指南中文.pdf
