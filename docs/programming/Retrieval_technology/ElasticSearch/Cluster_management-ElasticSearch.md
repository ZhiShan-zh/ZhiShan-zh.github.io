# ElasticSearch集群管理

# 1 概述

## 1.1 简介

ElasticSearch通常以集群方式工作，这样做不仅能够提高ElasticSearch的搜索能力还可以处理大数据搜索的能力，同时也增加了系统的容错能力及高可用，ElasticSearch可以实现PB级数据的搜索。

ElasticSearch集群是一个P2P（peer-to-peer意即个人对个人（伙伴对伙伴））类型（使用Gossip协议）的分布式系统，除了集群状态管理以外，其他所有的请求都可以发送到集群内任意一台结点上，这个节点可以自己找到需要转发给哪些节点，并且直接跟这些结点通信。所以，从网络架构及服务配置上来说，构建集群所需要的配置极其简单。在ElasticSearch2.0之前，无阻碍的网络下，所有配置了相同`cluster.name`的节点都自动归属到一个集群中。2.0版本之后，基于安全考虑避免开发环境过于随便造成的麻烦，从2.0版本开始，默认的自动发现方式改为了单播（unicast）方式。配置里提供几台结点的地址，ElasticSearch将其视作gossip router角色，借以完成集群的发现。由于这只是ElasticSearch内一个很小的功能，所以gossip router角色并不需要单独配置，每个ElasticSearch结点都可以担任。所以，采用单播方式的集群，各节点都配置相同的几个节点列表作为router即可。

集群中节点数量没有限制，一般大于等于2个节点就可以看作是集群了。一般处于性能及高可用方面来考虑一般集群中的节点数量都是3个及3各以上。

Gossip协议基本思想就是：一个节点想要分享一些信息给网络中的其他的一些节点。于是，它**周期性**的**随机**选择一些节点，并把信息传递给这些节点。这些收到信息的节点接下来会做同样的事情，即把这些信息传递给其他一些随机选择的节点。一般而言，信息会周期性的传递给N个目标节点，而不只是一个。这个N被称为**fanout**（这个单词的本意是扇出）。

## 1.2 ElasticSearch相关概念

### 1.2.1 集群cluster

一个集群就是由一个或多个结点组织在一起，它们共同持有整个的数据，并一起提供索引和搜索功能。

一个集群由一个唯一的名称标识（有配置`cluster.name`指定），这个名称默认是“elasticsearch”。这个名字很重要，因为一个结点只能通过指定某个集群的名字，来加入这个集群。

### 1.2.2 节点node

一个节点是集群中的一个服务器，作为集群的一部分，它存储数据，参与集群的索引和搜索功能，和集群类似，一个结点也是由一个名字来标识的，默认情况下，这个名字是一个搜集的漫威漫画角色的名字，这个名字会在启动的时候赋予节点，这个名字对于管理工作来说挺重要的，因为在这个管理过程中，你会确定网络中的哪些服务器对于ElasticSearch集群中的哪些节点。

一个节点可以通过配置集群名称的方式来加入一个指定的集群，默认情况下，每个节点都会被安排加入到一个叫做“elasticsearch”的集群中，这意味着，如果你在网络中启动了若干个节点，并假定它们能够相互发现彼此，它们将会自动地形成并加入到一个叫做“elasticsearch”的集群中。

在一个集群里，只要你想，可以拥有任意多个节点。而且，如果当你的网络中没有运行任何ElasticSearch节点，这时启动一个节点，会默认创建并加入一个叫做“elasticsearch”的集群。

### 1.2.3 分片和复制shards&replicas

一个索引可以存储超过单个节点硬件限制的大量数据，比如，一个具有10亿文档的索引占据1TB的磁盘空间，而任一节点都没有这样大的磁盘空间；或者单个节点处理搜索请求，响应太慢，为了解决这个问题，ElasticSearch提供了将索引划分成多份的能力，这些份就叫做分片。当你创建一个索引的时候，你可以指定想要的分片的数量，每个分片本身也是一个功能完善并且独立的“索引”，这个“索引”可以被放置到集群中的任何节点上，分片很重要，主要有两个方面的原因：

1. 允许你水平分割/扩展你的内容容量；
2. 允许你在分片（潜在地，位于多个节点上）之上进行分布式的、并行的操作，进而提高性能/吞吐量。

至于一个分片怎么分布，它的文档怎样聚合会搜索请求，是完全由ElasticSearch管理的，对于作为用户的你来说，这些都是透明的。

在一个网络/云的环境里，失败随时都可能发生，在某个分片/节点不知怎么的就处于离线状态，或者由于任何原因消失了，这种情况下，有一个故障转移机制是非常有用并且是强烈推荐的，为此目的，ElasticSearch允许你创建分片的一份或多份拷贝，这些拷贝叫做复制分片，或者直接叫做复制。

复制之所以重要，有两个主要的原因：

- 在分片/节点失败的情况下，提供了高可用性。
  - 因为这个原因，需要注意到复制分片从不与原/主要（original/primary）分片置于同一节点上是非常重要的。
- 扩展你的搜索量/吞吐量，因为搜索可以在所有的复制上并行运行。

总之，每个索引可以被分成多个分片。一个索引也可以被复制0次（意思是没有复制）或多次。一旦复制了，每个索引就有了主分片（作为复制源的原来的分片）和复制分片（主分片的拷贝）之别。分片和复制的数量可以在索引创建的时候指定。**在索引创建之后，你可以在任何时候动态地改变复制的数量，但是你事后不能改变分片的数量。**

默认情况下，ElasticSearch中的每个索引被分片5个主分片和1个复制，这意味着，如果你的集群中至少有两个节点，你的索引将会有5个主分片和另外5个复制分片（1个完全拷贝），这样的话每个索引总共就有10个分片。

## 1.3 集群的结构（逻辑结构和物理结构）

逻辑结构：

![](https://zhishan-zh.github.io/media/elasticsearch-20200531162827.png)

单Node多分片物理结构：

![A cluster with one node and three primary shards](https://zhishan-zh.github.io/media/elasticsearch-0202.png)

3个Node ，3个主分片和1个复制分片物理结构：

![A cluster with three nodes](https://zhishan-zh.github.io/media/elasticsearch-0204.png)

物理存储单元：

- 一个物理存储单元就是一个Lucene创建的索引库。
- 一个服务器（一个Node）可以有N个物理的存储单元。
- 每一分片的数据都保存到一个Lucene创建的索引库里边。

# 2 搭建集群

集群情况：

- 节点：2

- 索引分片：2

- 副本分片：1

## 2.1 节点的三个角色

- **主结点**：master节点主要用于集群的管理及索引 比如新增结点、分片分配、索引的新增和删除等。
- **数据结点**：data 节点上保存了数据分片，它负责索引和搜索操作。 
- **客户端结点**：client 节点仅作为请求客户端存在，client的作用也作为负载均衡器，client 节点不存数据，只是将请求均衡转发到其它结点。

通过下边两项参数来配置结点的功能：

- `node.master`：是否允许为主结点
- `node.data`：允许存储数据作为数据结点
- `node.ingest`：是否允许成为ingest节点

四种组合方式：

- master=true，data=true：即是主结点又是数据结点
- master=false，data=true：仅是数据结点
- master=true，data=false：仅是主结点，不存储数据
- master=false，data=false：即不是主结点也不是数据结点，此时可设置ingest为true表示它是一个客户端。



## 2.2 创建结点

新的节点，在Elasticsearch根目录下的data目录不能有内容。

每个节点需要更改Elasticsearch更目录下config目录中的配置文件`elasticsearch.yml`。

配置完成之后，分别启动节点1和节点2。

```yaml
#节点1的配置信息
#集群名称，保证唯一
cluster.name: elasticsearch
#节点名称，必须不一样
node.name: node_1
#必须为本机的ip地址
network.host: 0.0.0.0
#服务端口号，在同一机器下必须不一样
http.port: 9200
#集群键通信端口号，在同一机器下必须不一样
transport.tcp.port: 9300
node.master: true
node.data: true
#设置集群自动发现机器ip集合
discovery.zen.ping.unicast.hosts: ["0.0.0.0:9300", "0.0.0.0:9301"]
discovery.zen.minimum_master_nodes: 1
node.ingest: true
node.max_local_storage_nodes: 2
path.data: D:\ElasticSearch\elasticsearch‐6.2.1‐1\data
path.logs: D:\ElasticSearch\elasticsearch‐6.2.1‐1\logs
#跨域访问
http.cors.enabled: true
http.cors.allow‐origin: /.*/
```



```yaml
#节点2的配置信息
#集群名称，保证唯一
cluster.name: elasticsearch
#节点名称，必须不一样
node.name: node_2
#必须为本机的ip地址
network.host: 0.0.0.0
#服务端口号，在同一机器下必须不一样
http.port: 9201
#集群键通信端口号，在同一机器下必须不一样
transport.tcp.port: 9301
node.master: true
node.data: true
#设置集群自动发现机器ip集合
discovery.zen.ping.unicast.hosts: ["0.0.0.0:9300", "0.0.0.0:9301"]
discovery.zen.minimum_master_nodes: 1
node.ingest: true
node.max_local_storage_nodes: 2
path.data: D:\ElasticSearch\elasticsearch‐6.2.1‐2\data
path.logs: D:\ElasticSearch\elasticsearch‐6.2.1‐2\logs
#跨域访问
http.cors.enabled: true
http.cors.allow‐origin: /.*/
```

## 2.3 创建索引库

使用head连上其中一个结点，创建索引库，共2个分片，每个分片一个副本，创建成功，刷新head。

索引名称：`index_library`

分片数：2

副本数：1

每个结点安装IK分词器。

## 2.4 集群的健康

通过发送GET请求`/_cluster/health` 来查看Elasticsearch 的集群健康情况。

用三种颜色来展示健康状态：

- green：所有的主分片和副本分片都正常运行。 

- yellow：所有的主分片都正常运行，但有些副本分片运行不正常。
- red：存在主分片运行不正常。

GET请求：http://localhost:9200/_cluster/health

响应结果：

```json
{
	"cluster_name": "elasticsearch",
	"status": "green",
	"timed_out": false,
	"number_of_nodes": 2,
	"number_of_data_nodes": 2,
	"active_primary_shards": 2,
	"active_shards": 4,
	"relocating_shards": 0,
	"initializing_shards": 0,
	"unassigned_shards": 0,
	"delayed_unassigned_shards": 0,
	"number_of_pending_tasks": 0,
	"number_of_in_flight_fetch": 0,
	"task_max_waiting_in_queue_millis": 0,
	"active_shards_percent_as_number": 100
}
```

## 2.5 测试

### 2.5.1 创建映射并写入文档

连接 其中任意一台结点，创建映射写入文档。

POST请求：http://localhost:9200/index_library/doc/3

携带参数：

```json
{ 
    "name": "spring开发基础",
    "description": "spring 在java领域非常流行，java软件开发人员都在用。",
    "studymodel": "201001",
    "price":66.6
}
```

响应结果：

```json
{
	"_index": "index_library",
	"_type": "doc",
	"_id": "3",
	"_version": 1,
	"result": "created",
	"_shards": {
		"total": 2,
		"successful": 2,
		"failed": 0
	},
	"_seq_no": 0,
	"_primary_term": 1
}
```

从响应结果可看出，两个分片都保存成功。

### 2.5.2 搜索

向其它一个结点发起搜索请求，查询全部数据。

### 2.5.3 关闭一个节点

ElasticSearch会重新选中一个主节点（前提在配置结点时允许它可以为主结点），此时向活的结点发起搜索请求，仍然正常。

### 2.5.4 添加一个节点

添加结点3，端口设置为：

```json
#节点3的配置信息
#集群名称，保证唯一
cluster.name: elasticsearch
#节点名称，必须不一样
node.name: node_3
#必须为本机的ip地址
network.host: 0.0.0.0
#服务端口号，在同一机器下必须不一样
http.port: 9202
#集群键通信端口号，在同一机器下必须不一样
transport.tcp.port: 9302
node.master: false
node.data: true
#设置集群自动发现机器ip集合
discovery.zen.ping.unicast.hosts: ["0.0.0.0:9300", "0.0.0.0:9301","0.0.0.0:9302"]
discovery.zen.minimum_master_nodes: 1
node.ingest: true
node.max_local_storage_nodes: 2
path.data: D:\ElasticSearch\elasticsearch‐6.2.1‐3\data
path.logs: D:\ElasticSearch\elasticsearch‐6.2.1‐3\logs
#跨域访问
http.cors.enabled: true
http.cors.allow‐origin: /.*/
```

启动结点3，刷新head，可看出ElasticSearch将分片分在了3个结点

向结点3发起搜索，GET请求：http://127.0.0.1:9202/index_library/doc/_search

全部数据可被正常搜索到。