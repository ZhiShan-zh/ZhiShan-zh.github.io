# 负载均衡与反向代理

当我们的应用单实例不能支撑用户请求时，此时就需要扩容，从一台服务器扩容到两台、几十台、几百台。然而，用户访问时是通过`http://www.jd.com`的方式访问，在请求时，浏览器首先会查询DNS服务器获取对应的IP，然后通过此IP访问对应的服务。

因此，一种方式是`www.jd.com`域名映射多个IP，但是，存在一个最简单的问题，假设某台服务器重启或者出现故障，DNS会有一定的缓存时间，故障后切换时间长，而且没有对后端服务进行心跳检查和失败重试的机制。

因此，外网DNS应该用来实现用GSLB（全局负载均衡）进行流量调度，如将用户分配到离他最近的服务器上以提升体验。而且当某一区域的机房出现问题时（如被挖断了光缆），可以通过DNS指向其他区域的IP来使服务可用。

可以在站长之家使用“DNS查询”，查询`c.3.cn`可以看到类似如下的结果。

| DNS所在地          | 响应IP                                                       | TTL值     |
| ------------------ | ------------------------------------------------------------ | --------- |
| 湖南[联通]         | 120.52.148.153 [河北省廊坊市 联通]<br/>111.206.227.153 [北京市 联通] | 60<br/>60 |
| 台湾中华电信[海外] | 202.77.129.230 [香港 电讯盈科有限公司PowerBase数据中心]      | 60        |

即不同的运营商返回的公网IP是不一样的。

对于内网DNS，可以实现简单的轮询负载均衡。但是，还是那句话，会有一定的缓存时间并且没有失败重试机制。因此，我们可以考虑选择如HaProxy和Nginx。

而对于一般应用来说，有Nginx就可以了。单Nginx一般用于七层负载均衡，其吞吐量有一定限制的。为了提升整体吞吐量，会在DNS和Nginx之间引入接入层，如使用LVS（软件负载均衡器）、F5（硬件负载均衡器）可以做四层负载均衡，即首先DNS解析到LVS/F5，然后LVS/F5转发给Nginx，再由Nginx转发给后端Real Server。

![image-20200509160644186](./media/image-20200509160644186.png)

对于一般应用开发人员来说，我们只需要关心到Nginx层面就够了，LVS/F5一般有系统/运维工程师来维护。Nginx目前提供了HTTP（ngx_http_upstream_module）七层负载均衡，而1.9.0版本也开始支持TCP（ngx_stream_upstream_module）四层负载均衡。

此处在澄清几个概念。

- 二层负载均衡：通过改写报文的目标MAC地址为上游服务器MAC地址，源IP地址和目标IP地址是没有改变的，负载均衡服务器和真实服务器共享同一个VIP，如LVS DR工作模式。
- 四层负载均衡：根据端口号将报文转发到上游服务器（不同的IP地址+端口），如LVS NAT模式、HaProxy。
- 七层负载均衡：根据端口号和应用层协议如HTTP协议的主机名、URL，转发报文到上游服务器（不同的IP地址+端口），如HaProxy、Nginx。

这里在介绍一下LVS DR工作模式，其工作在数据链路层，LVS和上游服务器共享一个VIP（VIP = Virtual IP Address，虚拟IP地址，该路由器所在局域网内其他机器的默认路由为该vip），通过改写报文的目标MAC地址为上游服务器MAC地址实现负载均衡，上游服务器直接响应报文到客户端，不经过LVS，从而提升性能。但因为LVS和上游服务器必须在同一个子网，为了解决跨子网问题而又不影响负载性能，可以选择在LVS后挂HaProxy，通过四层到七层服务均衡器HaProxy集群来解决跨网和性能问题。这两个“半成品”的东西相互取长补短，组合起来就变成了一个“完整”的负载均衡器。现在Nginx的stream也支持TCP，所以Nginx也算是一个四层到七层的负载均衡器，一般场景下可以用Nginx取代HaProxy。

本文中接入层、反向代理服务器、负载均衡服务器一般指Nginx。upstream server即上游服务器，指Nginx负载均衡到的处理业务的服务器，也可以称之为real server，即真实处理业务的服务器。

对于负载均衡我们要关心的几个方面如下：

- **上游服务器配置**：使用upstream server配置上游服务器。
- **负载均衡算法**：配置多个上游服务器时的负载均衡机制。
- **失败重试机制**：配置当超时或上游服务器不存活时，是否需要重试其他上游服务器。
- **服务器心跳检查**：上游服务器的健康检查/心跳检查。

Nginx提供的负载均衡可以实现上游服务器的负载均衡、故障转移、失败重试、容错、健康检查等，当某些上游服务器出现问题时可以将请求转到其他上游服务器以保障高可用，并且通过OpenResty实现更智能的负载均衡，如热点与非热点流量分离，正常流量与爬虫流量分离等。Nginx负载均衡器本身也是一台反向代理服务器，将用户请求通过Nginx代理到内网中的某台上游服务器处理，反向代理服务器可以对响应结果进行缓存、压缩等处理以提升性能。Nginx作为负载均衡器/反向代理服务器如下图所示：

![image-20200511125245160](./media/image-20200511125245160.png)