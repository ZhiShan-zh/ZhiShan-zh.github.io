# 传输模块

参考官方文档：[Transport](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-transport.html)

# 1 概述

传输模块用于集群内节点之间的内部通信。 从一个节点到另一个节点的每个调用都使用传输模块（例如，当一个节点处理HTTP GET请求，而实际上应由另一个保存数据的节点处理时）。 传输模块还用于Elasticsearch Java API中的`TransportClient`。

传输机制本质上是完全异步的，这意味着没有阻塞线程在等待响应。 使用异步通信的好处是首先解决了C10k问题，同时也是分散（广播）/收集操作（例如Elasticsearch中的搜索）的理想解决方案。

# 2 设置

Elasticsearch内部传输通过TCP进行通信。 您可以使用以下设置对其进行配置：

| 设置项                      | 描述                                                         |
| --------------------------- | ------------------------------------------------------------ |
| `transport.port`            | 绑定端口的范围。默认为`9300-9400`。                          |
| `transport.publish_port`    | 集群中其他节点与此节点通信时应使用的端口。 当群集节点位于代理服务器或防火墙后面并且无法从外部直接访问`transport.port`时，此选项很有用。 默认为通过`transport.port`分配的实际端口。 |
| `transport.bind_host`       | 绑定传输服务的主机地址。 默认为`transport.host`（如果设置）或`network.bind_host`。 |
| `transport.publish_host`    | 要发布以供集群中的节点连接的主机地址。 默认为`transport.host`（如果设置）或`network.publish_host`。 |
| `transport.host`            | 用于设置`transport.bind_host`和`transport.publish_host`。    |
| `transport.connect_timeout` | 新连接的连接超时时间（以时间设置格式）。默认为`30s`。        |
| `transport.compress`        | 如果设置为`true`则启用所有节点之间的压缩传输（DEFLATE）。默认为`false`。 |
| `transport.ping_schedule`   | 周期性发送应用程序级ping消息，以确保节点之间的传输连接保持活动状态。在transport client中默认为5s，在其他地方默认为-1（禁用）。最好正确地配置TCP心跳保活机制以替代此功能，因为TCP心跳保活机制不仅适用于传输连接，而且适用于所有种类的长连接。 |

它还使用通用[network settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html)。

# 3 Transport Profiles

Elasticsearch允许您使用Transport Profiles绑定到不同接口上的多个端口。查看此示例配置：

```yaml
transport.profiles.default.port: 9300-9400
transport.profiles.default.bind_host: 10.0.0.1
transport.profiles.client.port: 9500-9600
transport.profiles.client.bind_host: 192.168.0.1
transport.profiles.dmz.port: 9700-9800
transport.profiles.dmz.bind_host: 172.16.1.2
```

默认profile是特别重要的。 如果没有配置任何特定的配置设置，它将用作任何其他profiles的后备，这是此节点如何连接到群集中其他节点的方式。

可以在每个transport profile上配置以下参数，如上例所示：

- `port`：绑定的端口
- `bind_host`：绑定的主机
- `publish_host`：在信息性API中发布的主机
- `tcp.no_delay`：为这个套接字配置`TCP_NO_DELAY`选项
- `tcp.keep_alive`：为这个套接字配置`SO_KEEPALIVE`选项
- `tcp.keep_idle`：为此套接字配置`TCP_KEEPIDLE`选项，该选项决定了开始发送TCP Keepalive探测之前连接必须空闲的时间（以秒为单位）。 仅适用于Linux和Mac，并且需要JDK 11或更高版本。 默认值为`-1`，这将不会在套接字级别设置此选项，而是使用默认的系统配置。
- `tcp.keep_interval`：为此套接字配置`TCP_KEEPINTVL`选项，该选项决定了两次发送TCP Keepalive探测之间的时间（以秒为单位）。 仅适用于Linux和Mac，并且需要JDK 11或更高版本。 默认值为-1，这不会在套接字级别设置此选项，而是使用默认的系统配置。
- `tcp.keep_count`：为该套接字配置`TCP_KEEPCNT`选项，该选项决定了在断开连接之前可能在连接上发送的未经确认的TCP Keepalive探测的数量。 仅适用于Linux和Mac，并且需要JDK 11或更高版本。 默认值为-1，这不会在套接字级别设置此选项，而是使用默认的系统配置。
- `tcp.reuse_address`：为这个套接字配置`SO_REUSEADDR`选项
- `tcp.send_buffer_size`：配置套接字的发送缓冲区大小
- `tcp.receive_buffer_size`：配置套接字的接收缓冲区大小

# 4 空闲长连接

Elasticsearch在集群中每对节点之间打开许多TCP长连接，其中一些连接可能会长时间闲置。 但是，Elasticsearch要求这些连接保持打开状态，如果任何节点间的连接由于诸如防火墙之类的外部影响而关闭，它可能会破坏集群的运行。配置网络以保留Elasticsearch节点之间的空闲长连接很重要，例如，通过启用`tcp.keep_alive`并确保keepalive间隔短于可能导致空闲连接关闭的任何超时，或者如果无法配置keepalive的话，可以设置`transport.ping_schedule`。

# 5 请求压缩

默认情况下，`transport.compress`被设置为`false`，并且在集群中的节点之间也禁用了网络级请求压缩。 通常，此默认设置对本地群集通信有意义，因为压缩会占用大量CPU资源，并且本地群集倾向于通过节点之间的快速网络连接来建立。

`transport.compress`一般配置本地集群请求压缩，并且它也是远程集群请求压缩的后备设置。如果要配置与本地请求压缩不同的远程请求压缩，则可以基于一个远程集群使用[`cluster.remote.${cluster_alias}.transport.compress` setting](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-remote-clusters.html#remote-cluster-settings)来进行设置。

# 6 响应压缩

压缩设置不没有设置响应压缩。 如果入站请求被压缩-即使未启用压缩，Elasticsearch也会压缩响应。 同样，如果入站请求未压缩，即使响应启用了压缩，Elasticsearch也不会压缩响应。

# 7 传输追踪器

传输层具有专用的追踪日志记录器，该记录器在激活时会记录传入和传出的请求日志。 通过将`org.elasticsearch.transport.TransportService.tracer`日志记录器的级别设置为`TRACE`，可以动态激活日志。

```json
PUT _cluster/settings
{
   "transient" : {
      "logger.org.elasticsearch.transport.TransportService.tracer" : "TRACE"
   }
}
```

您还可以使用一组包含和排除通配符模式来控制要跟踪哪些操作。 默认情况下，将跟踪每个请求（故障检测ping除外）：

```json
PUT _cluster/settings
{
   "transient" : {
      "transport.tracer.include" : "*",
      "transport.tracer.exclude" : "internal:coordination/fault_detection/*"
   }
}
```

