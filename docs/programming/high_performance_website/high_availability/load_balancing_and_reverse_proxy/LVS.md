# LVS

# 1 LVS概述

## 1.1 LVS是什么

1. LVS的英文全称是Linux Virtual Server，即Linux虚拟服务器。
2. LVS是我们国家的章文嵩博士的一个开源项目。

## 1.2 LVS能干什么

1. LVS主要用于多服务器的负载均衡。
2. 它工作在网络层，可以实现高性能，高可用的服务器集群技术。
3. 它可把许多低性能的服务器组合在一起形成一个超级服务器。
4. 它配置非常简单，且有多种负载均衡的方法。
5. 它稳定可靠，即使在集群的服务器中某台服务器无法正常工作，也不影响整体效果。
6. 可扩展性也非常好。

## 1.3 Nginx和LVS对比

- Nginx工作在网络的应用层，主要做反向代理；LVS工作在网络层，主要做负载均衡。
  - Nginx也同样能承受很高负载且稳定，但负载度和稳定度不及LVS。  
- Nginx对网络的依赖较小，LVS就比较依赖于网络环境。
- 在使用上，一般最前端所采取的策略应是LVS。
  - Nginx可作为LVS节点机器使用。

## 1.4 负载均衡机制

LVS是工作在网络层。相对于其它负载均衡的解决办法，它的效率是非常高的。LVS的通过控制IP来实现负载均衡。IPVS是其具体的实现模块。

IPVS的主要作用：安装在Director Server上面，在Director Server虚拟一个对外访问的IP（VIP）。用户访问VIP，到达Director Server，Director Server根据一定的规则选择一个Real Server，处理完成后然后返回给客户端数据。这些步骤产生了一些具体的问题，比如如何选择具体的Real Server，Real Server如果返回给客户端数据等等。IPVS为此有三种机制：

### 1.4.1 VS/NAT

VS/NAT(Virtual Server via Network Address Translation)，即网络地址翻转技术实现虚拟服务器。

当请求来到时，Diretor server上处理的程序将数据报文中的目标地址（即虚拟IP地址）改成具体的某台Real Server，端口也改成Real Server的端口，然后把报文发给Real Server。

Real Server处理完数据后，需要返回给Diretor Server，然后Diretor server将数据包中的源地址和源端口改成VIP的地址和端口，最后把数据发送出去。

由此可以看出，用户的请求和返回都要经过Diretor Server，如果数据过多，Diretor Server肯定会不堪重负。

  ![img](https://zhishan-zh.github.io/media/lvs_557ef25508f0d0f3.png)

### 1.4.2 VS/TUN

VS/TUN（Virtual Server via IP Tunneling）,即IP隧道技术实现虚拟服务器。

IP隧道（IP tunneling）是将一个IP报文封装在另一个IP报文的技术，这可以使得目标为一个IP地址的数据报文能被封装和转发到另一个IP地址。IP隧道技术亦称为IP封装技术（IP encapsulation）。它跟VS/NAT基本一样，但是Real server是直接返回数据给客户端，不需要经过Diretor server，这大大降低了Diretor server的压力。

### 1.4.3 VS/DR

VS/DR（Virtual Server via Direct Routing），即用直接路由技术实现虚拟服务器。

跟前面两种方式，它的报文转发方法有所不同，VS/DR通过改写请求报文的MAC地址，将请求发送到Real Server，而Real Server将响应直接返回给客户，免去了VS/TUN中的IP隧道开销。

这种方式是三种负载调度机制中性能最高最好的，但是必须要求Director Server与Real Server都有一块网卡连在同一物理网段上。

![img](https://zhishan-zh.github.io/media/lvs_46743f3d8e1ff89d.png)

# 2 安装LVS

## 2.1 依赖包ipvs

**安装ipvs**：`yum -y install ipvs*`

**验证本机ip_vs模块是否加载**：

```shell
[root@client lvs]# grep -i 'ip_vs' /boot/config-2.6.32-431.el6.x86_64 
CONFIG_IP_VS=m 
CONFIG_IP_VS_IPV6=y 
# CONFIG_IP_VS_DEBUG is not set 
CONFIG_IP_VS_TAB_BITS=12 
CONFIG_IP_VS_PROTO_TCP=y 
CONFIG_IP_VS_PROTO_UDP=y 
CONFIG_IP_VS_PROTO_AH_ESP=y 
CONFIG_IP_VS_PROTO_ESP=y 
CONFIG_IP_VS_PROTO_AH=y 
CONFIG_IP_VS_PROTO_SCTP=y 
CONFIG_IP_VS_RR=m 
CONFIG_IP_VS_WRR=m 
CONFIG_IP_VS_LC=m 
CONFIG_IP_VS_WLC=m 
CONFIG_IP_VS_LBLC=m 
CONFIG_IP_VS_LBLCR=m 
CONFIG_IP_VS_DH=m 
CONFIG_IP_VS_SH=m 
CONFIG_IP_VS_SED=m 
CONFIG_IP_VS_NQ=m 
CONFIG_IP_VS_FTP=m 
CONFIG_IP_VS_PE_SIP=m
```

## 2.2 安装LVS

### 2.2.1 lvs drsrever脚本

**修改functions权限**：`chmod 755 /etc/rc.d/init.d/functions`（functions这个脚本是给/etc/init.d里边的文件使用的（可理解为全局文件））

**创建lvs文件夹**：

```shell
cd /usr/local 
mkdir –m 755 lvs
cd /lvs
```

**编写脚本**：`vim /usr/local/lvs/lvs_dr.sh`

```shell
#!/bin/bash
#description:start lvs server
echo "1" >/proc/sys/net/ipv4/ip_forward  		#开启ip转发
WEB1=192.168.56.200						#真实的webip
WEB2=192.168.56.201						#真实的webip
VIP1=192.168.56.80						#虚拟lvs的ip
/etc/rc.d/init.d/functions 					#初始化function
case "$1" in								#第一个参数
start)									#第一个参数是start
    echo "start LVS of directorServer"				#打印
    /sbin/ifconfig eth0:0 $VIP1 broadcast $VIP1 netmask 255.255.255.255 up		#设置虚拟网络
    /sbin/ipvsadm –C					#清除内核虚拟服务器表中的所有记录，清除lvs设置
    /sbin/ipvsadm -A -t $VIP1:8080 -s rr	#设置rr模式，轮询模式
    /sbin/ipvsadm -a -t $VIP1:8080 -r $WEB1:8080 –g		#轮询的机器，-g采用DR模式
    /sbin/ipvsadm -a -t $VIP1:8080 -r $WEB2:8080 –g
    /sbin/ipvsadm								#启动lvs
    ;;
stop)							#如果第一个参数是stop
    echo "close LVS directorserver"		#打印
    echo "0" >/proc/sys/net/ipv4/ip_forward	#关闭ip转发
    /sbin/ipvsadm –C					#清除内核虚拟服务器表中的所有记录
    /sbin/ipvsadm –Z					#虚拟服务表计数器清零（清空当前的连接数量等）
    ;;
*)								#如果第一个参数是其他任何值
    echo "usage:$0 {start|stop}"			#打印：提示输入start或者stop
    exit 1							#退出
esac					
```

**执行脚本**：

```shell
chmod 755 lvs_dr.sh
./lvs-dr.sh  start
```

![image-20200606160314652](https://zhishan-zh.github.io/media/lvs-20200606160314652.png)

**查看**：`ipvsadm –ln`

![image-20200606160525359](https://zhishan-zh.github.io/media/lvs-20200606160525359.png)

看到上面信息说明ipvsadm启动成功。

### 2.2.2 lvs realserver脚本

**在web1 和web2机器上修改functions权限**：`chmod 755 /etc/rc.d/init.d/functions`（functions这个脚本是给/etc/init.d里边的文件使用的（可理解为全局文件））

**在分别在web1 和web2服务器上创建lvs文件夹**：

```shell
cd /usr/local
mkdir –m 755 lvs
cd lvs
```

**编写脚本**：`vim /usr/local/lvs/lvs-rs.sh`

```shell
#!/bin/sh
VIP1=192.168.56.80					#虚拟ip
/etc/rc.d/init.d/functions				#初始化function
case "$1" in							#第一个参数
start)								#如果第一个参数是start
    echo "start LVS of realserver"				#打印
    /sbin/ifconfig lo:0 $VIP1 broadcast $VIP1 netmask 255.255.255.255 up	#设置虚拟网络
    echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore		#定义接收到ARP请求时的响应级别
    echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce	#定义将自己的地址向外通告时的级别
    echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
    ;;
stop)								#如果第一个参数是stop
    /sbin/ifconfig lo:0 down					#停止网卡
    echo "close lvs dirctorserver"				#打印
    echo "0" >/proc/sys/net/ipv4/conf/lo/arp_ignore		#定义接收到ARP请求时的响应级别
    echo "0" >/proc/sys/net/ipv4/conf/lo/arp_announce	#定义将自己的地址向外通告时的级别
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_announce
    ;;
*)
    echo "usage:$0{start|stop}"
    exit 1
esac
```

**启动在web1 和web2机器上lvs**：

```shell
chmod 755 lvs-rs.sh
./lvs-rs.sh start 
```

### 2.2.3 其他命令

**设置dr机器上设置连接超时值(秒)** ：`ipvsadm --set 1 1 1`

**关闭**：

- `./lvs-rs.sh stop`
- `./lvs-dr.sh stop`