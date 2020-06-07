# LVS+Nginx+Keepalived

# 1 概述

1. LVS主要用于多服务器的负载均衡。
2. LVS工作在网络层，可以实现高性能，高可用的服务器集群技术。
3. LVS配置非常简单，且有多种负载均衡的方法。
4. Nginx工作在网络的应用层，主要做反向代理；LVS工作在网络层，主要做负载均衡。
   - Nginx也同样能承受很高负载且稳定，但负载度和稳定度不及LVS。
5. 在使用上，一般最前端所采取的策略应是LVS。
   - Nginx可作为LVS节点机器使用。

# 2 Nginx安装

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
        server_name  tomcat.xxx.com;#域名可以有多个，用空格隔开

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

# 3 安装LVS

**编写脚本**：`vim /usr/local/lvs/lvs_dr.sh`

- 和之前对比，变化之处就是vip和转发的端口。

```
#!/bin/bash
#description:start lvs server
echo "1" >/proc/sys/net/ipv4/ip_forward
 
WEB1=192.168.56.200
WEB2=192.168.56.201
 
VIP1=192.168.56.90
 
/etc/rc.d/init.d/functions
 
case "$1" in
start)
    echo "start LVS of directorServer"
    #set the Virtual address and sysctl parameter
    /sbin/ifconfig eth1:0 $VIP1 broadcast $VIP1 netmask 255.255.255.255 up
    #clear ipvs table
    /sbin/ipvsadm -C

    #set LVS
    #web apache or tomcat
    /sbin/ipvsadm -A -t $VIP1:80 -s rr
    /sbin/ipvsadm -a -t $VIP1:80 -r $WEB1:80  -g
    /sbin/ipvsadm -a -t $VIP1:80 -r $WEB2:80  -g

    #run LVS
    /sbin/ipvsadm
    ;;
stop)
    echo "close LVS directorserver"
    echo "0" >/proc/sys/net/ipv4/ip_forward
    /sbin/ipvsadm -C
    /sbin/ipvsadm -Z
    ;;
*)
    echo "usage:$0 {start|stop}"
    exit 1
esac
```

**编写脚本**：`vim /usr/local/lvs/lvs-rs.sh`

- 与之前的不同在于修改了vip

```
#!/bin/sh
#description start realserver
#chkconfig 235 26 26
VIP1=192.168.56.90
/etc/rc.d/init.d/functions
case "$1" in
start)
    echo "start LVS of realserver"
    /sbin/ifconfig lo:0 $VIP1 broadcast $VIP1 netmask 255.255.255.255 up

    echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce
    echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
    ;;
stop)
    /sbin/ifconfig lo:0 down
    echo "close lvs dirctorserver"
    echo "0" >/proc/sys/net/ipv4/conf/lo/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/lo/arp_announce
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_ignore
    echo "0" >/proc/sys/net/ipv4/conf/all/arp_announce
    ;;
*)
    echo "usage:$0{start|stop}"
    exit 1
esac
```

# 4 安装keepalived

注意：在用keepalived做tomcat和nginx的热备时，需要加入realserver的配置。但是做lvs的热备则不需要配置realserver，因为keepalived有lvs的配置参数。

## 4.1 backup

```
! Configuration File for keepalived
global_defs {
   notification_email {
     #acassen@firewall.loc
     #failover@firewall.loc
     #sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   #smtp_server 192.168.200.1
   #smtp_connect_timeout 30
   router_id LVS_DEVEL
}

vrrp_instance VI_1 {
    state BACKUP
    interface eth1
	lvs_sync_daemon_inteface eth1
    virtual_router_id 51
    priority 100
	nopreempt
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.56.90
    }
}

virtual_server 192.168.56.90 80 {
    delay_loop 6
    lb_algo rr
    lb_kind DR
    #nat_mask 255.255.255.0
    persistence_timeout 1
    protocol TCP
}
```

## 4.2 master

```
! Configuration File for keepalived

global_defs {
   notification_email {
     #acassen@firewall.loc
     #failover@firewall.loc
     #sysadmin@firewall.loc
   }
   notification_email_from Alexandre.Cassen@firewall.loc
   #smtp_server 192.168.200.1
   #smtp_connect_timeout 30
   router_id LVS_DEVEL
}

vrrp_instance VI_1 {
    state MASTER
    interface eth1
	lvs_sync_daemon_inteface eth1
    virtual_router_id 51
    priority 200

    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.56.90
    }
}

virtual_server 192.168.56.90 80 {
    delay_loop 6
    lb_algo rr
    lb_kind DR
    #nat_mask 255.255.255.0
    persistence_timeout 1
    protocol TCP
}
```

