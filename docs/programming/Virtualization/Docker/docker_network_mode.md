# docker网络模式

# 1 概述

| Docker网络模式 | 配置                      | 说明                                                         |
| -------------: | :------------------------ | :----------------------------------------------------------- |
|           host | –net=host                 | 容器和宿主机共享Network namespace。                          |
|      container | –net=container:NAME_or_ID | 容器和另外一个容器共享Network namespace。 kubernetes中的pod就是多个容器共享一个Network namespace。 |
|           none | –net=none                 | 容器有独立的Network namespace，但并没有对其进行任何网络设置，如分配veth pair 和网桥连接，配置IP等。 |
|         bridge | –net=bridge               | （默认为该模式）                                             |

# 2 host模式

- 特点
    - 和宿主机共用一个Network Namespace：容器将不会获得一个独立的Network Namespace，而是和宿主机共用一个Network Namespace。
    - 使用宿主机的IP和端口：容器将不会虚拟出自己的网卡，配置自己的IP等，而是使用宿主机的IP和端口。
    - 隔离性：容器的文件系统、进程列表等其他方面是和宿主机隔离的。

- 优点：网络性能比较好。
- 缺点：docker host上已经使用的端口就不能再用了，网络的隔离性不好。

# 3 container模式

- 特点
    - 容器共享Network Namespace：新创建的容器和已经存在的一个容器共享一个 Network Namespace，而不是和宿主机共享。
    - 容器共享IP和端口：新创建的容器不会创建自己的网卡，配置自己的 IP，而是和一个指定的容器共享 IP、端口范围等。
    - 隔离性：两个容器除了网络方面，其他的如文件系统、进程列表等还是隔离的。
- 优点：
    - 便于容器间的通信：
        - container网络模式，可以用来更好的服务于容器间的通信。
        - 在这种模式下的容器可以通过localhost来访问namespace下的其他容器，传输效率较高。
            - 同一namespace下容器的进程可以通过 lo 网卡设备通信。
        - 节约了一定数量的网络资源。
- 缺点：
    - 没有改善容器与宿主机以外世界通信的情况。

# 4 none模式

- 特点
    - 单独的Network Namespace：Docker容器拥有自己的Network Namespace。
    - 不为Docker容器进行任何网络配置：
        - 此模式并不为Docker容器进行任何网络配置。也就是说，这个Docker容器没有网卡、IP、路由等信息。需要我们自己为Docker容器添加网卡、配置IP等。
        - 可以说 none 模式为 Docker Container 做了极少的网络设定，没有网络配置的情况下，作为 Docker开发者,才能在这基础做其他无限多可能的网络定制开发。这也恰巧体现了 Docker 设计理念的开放。

# 5 bridge模式

当Docker进程启动时，会在主机上创建一个名为docker0的虚拟网桥，此主机上启动的Docker容器会连接到这个虚拟网桥上。虚拟网桥的工作方式和物理交换机类似，这样主机上的所有容器就通过交换机连在了一个二层网络中。

从docker0子网中分配一个IP给容器使用，并设置docker0的IP地址为容器的默认网关。Docker Daemon 利用 veth pair 技术,在宿主机上创建两个虚拟网络接口设备,假设为veth0 和 veth1。而 veth pair 技术的特性可以保证无论哪一个 veth 接收到网络报文，都会将报文传输给另一方。Docker将veth pair设备的一端（veth1）放在新创建的容器中，并命名为eth0（容器的网卡），另一端（veth0）放在主机中，以vethxxx这样类似的名字命名，并将这个网络设备加入到docker0网桥中。可以通过brctl show命令查看。

bridge模式是docker的默认网络模式，不写--net参数，就是bridge模式。使用docker run -p时，docker实际是在iptables做了DNAT规则，实现端口转发功能。可以使用iptables -t nat -vnL查看。

bridge 桥接模式下的 Docker Container 在使用时，并非为开发者包办了一切。最明显的是，该模式下 Docker Container 不具有一个公有 IP，即和宿主机的 eth0 不处于同一个网段。导致的结果是宿主机以外的世界不能直接和容器进行通信。虽然 NAT 模式经过中间处理实现了这一点，但是 NAT 模式仍然存在问题与不便，如：容器均需要在宿主机上竞争端口，容器内部服务的访问者需要使用服务发现获知服务的外部端口等。另外 NAT 模式由于是在三层网络上的实现手段，故肯定会影响网络的传输效率。

