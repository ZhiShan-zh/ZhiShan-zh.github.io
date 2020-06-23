# ElasticSearch入门

# 1 ElasticSearch简介

## 1.1 什么是ElasticSearch

Elasticsearch是一个**实时的分布式搜索和分析引擎**。它可以帮助你用前所未有的速度去处理大规模数据。

ElasticSearch是一个基于Lucene的搜索服务器。它提供了一个分布式多用户能力的全文搜索引擎，基于RESTful web接口。Elasticsearch是用Java开发的，并作为Apache许可条款下的开放源码发布，是当前流行的企业级搜索引擎。设计用于云计算中，能够达到实时搜索，稳定，可靠，快速，安装使用方便。

Elasticsearch隐藏了Lucene的复杂性，对外提供Restful 接口来操作索引、搜索。

## 1.2 特点

1. 既可以作为一个大型分布式集群（数百台服务器）技术，处理PB级数据，服务大公司；也可以运行在单机上。
2. 将全文检索、数据分析以及分布式技术合并在了一起，才形成了独一无二的ElasticSearch；
3. 开箱即用的，部署简单；
4. 全文检索，同义词处理，相关度排名，复杂数据分析，海量数据的近实时处理

## 1.3 ElasticSearch和solr选择问题

1. 如果你公司现在用的solr可以满足需求就不要换了。
2. 如果你公司准备进行全文检索项目的开发，建议优先考虑elasticsearch，因为像Github这样大规模的搜索都在用它。

## 1.4 原理与应用

### 1.4.1 索引结构

![](https://zhishan-zh.github.io/media/ElasticSearch-20200527165557.png)

逻辑结构部分是一个倒排索引表：

1. 将要搜索的文档内容分词，所有不重复的词组成分词列表。
2. 将搜索的文档最终以Document方式存储起来。
3. 每个词和docment都有关联。

例如：

| Term   | Doc_1 | Doc_2 |
| ------ | ----- | ----- |
| Quick  |       | X     |
| The    | X     |       |
| brown  | X     | X     |
| dog    | X     |       |
| dogs   |       | X     |
| fox    | X     |       |
| foxes  |       | X     |
| jumped | X     |       |
| lazy   | X     | X     |
| leap   |       | X     |
| over   | X     | X     |
| quick  | X     |       |
| summer |       | X     |
| the    | X     |       |

现在，如果我们想搜索`quick brown`，我们只需要查找包含每个词条的文档：

| Term  | Doc_1 | Doc_2 |
| ----- | ----- | ----- |
| brown | X     | X     |
| quick | X     |       |
| Total | 2     | 1     |

两个文档都匹配，但是第一个文档比第二个匹配度更高。如果我们使用仅计算匹配词条数量的简单的相似性算法 ，那么对于查询的相关性来讲，第一个文档比第二个文档更佳。

### 1.4.2 RESTful

ElasticSearch提供 RESTful API接口进行索引、搜索，并且支持多种客户端。

Elasticsearch使用的是标准的RESTful API和JSON。此外，Elasticsearch还构建和维护了很多其他语言的客户端，例如Java、Python、.NET和PHP。与此同时，其社区也贡献了很多的客户端。

![](https://zhishan-zh.github.io/media/ElasticSearch-20200527221649.png)

1. 用户在前端搜索关键字
2. 项目前端通过http方式请求项目服务端
3. 项目服务端通过Http RESTful方式请求ES集群进行搜索
4. ES集群从索引库检索数据。

# 2 ElasticSearch的安装和配置

## 2.1 安装

版本：Elasticsearch 6.2.1

要求：JDK1.8及以上

安装方式：

- 支持tar、zip、rpm等多种安装方式。
  - 在windows下开发建议使用ZIP安装方式。
- 支持docker方式安装
  - 参见：https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html

下载：https://www.elastic.co/downloads/past-releases

目录结构：

- bin：脚本目录，包括：启动、停止等可执行脚本
- config：配置文件目录
- data：索引目录，存放索引文件的地方
- lib
- logs：日志目录
- modules：模块目录，包括了es的功能模块
- plugins :插件目录，es支持插件机制
- LICENSE.txt
- NOTICE.txt
- README.textile

## 2.2 配置文件

ES的配置文件的地址根据安装形式的不同而不同：

- 使用zip、tar安装，配置文件的地址在安装目录的config下。
- 使用RPM安装，配置文件在`/etc/elasticsearch`下。
- 使用MSI安装，配置文件的地址在安装目录的config下，并且会自动将config目录地址写入环境变量`ES_PATH_CONF`。

本教程使用的zip包安装，配置文件在ES安装目录的config下。配置文件如下：

- `elasticsearch.yml `： 用于配置Elasticsearch运行参数 
- `jvm.options`： 用于配置Elasticsearch JVM设置
- `log4j2.properties`： 用于配置Elasticsearch日志

### 2.2.1 `elasticsearch.yml`

配置格式是YAML，可以采用如下两种方式：

- 层次方式
  - `path: data: /var/lib/elasticsearch logs: /var/log/elasticsearch`
- 属性方式
  - `path.data: /var/lib/elasticsearch `
  - `path.logs: /var/log/elasticsearch`

属性配置方式示例：

```yaml
cluster.name: elasticsearch
node.name: es_node_1
network.host: 0.0.0.0
http.port: 9200
transport.tcp.port: 9300
node.master: true
node.data: true
#discovery.zen.ping.unicast.hosts: ["0.0.0.0:9300", "0.0.0.0:9301", "0.0.0.0:9302"]
discovery.zen.minimum_master_nodes: 1
bootstrap.memory_lock: false
node.max_local_storage_nodes: 1
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
http.cors.enabled: true
http.cors.allow‐origin: /.*/
```

常用配置解析：

- `cluster.name:`
  - 配置elasticsearch的集群名称，默认是elasticsearch。建议修改成一个有意义的名称。

- `node.name:`
  - 节点名，通常一台物理服务器就是一个节点，es会默认随机指定一个名字，建议指定一个有意义的名称，方便管理 
  - 一个或多个节点组成一个cluster集群，集群是一个逻辑的概念，节点是物理概念，后边章节会详细介绍。

- `path.conf:` 
  - 设置配置文件的存储路径，tar或zip包安装默认在es根目录下的config文件夹，rpm安装默认在`/etc/elasticsearch`
- `path.data: `
  - 设置索引数据的存储路径，默认是es根目录下的data文件夹，可以设置多个存储路径，用逗号隔开。 
- `path.logs:` 
  - 设置日志文件的存储路径，默认是es根目录下的logs文件夹 
- `path.plugins: `
  - 设置插件的存放路径，默认是es根目录下的plugins文件夹
- `bootstrap.memory_lock: true`
  - 设置为true可以锁住ES使用的内存，避免内存与swap分区交换数据。
- `network.host:` 
  - 设置绑定主机的ip地址，设置为0.0.0.0表示绑定任何ip，允许外网访问，生产环境建议设置为具体的ip。
- `http.port: 9200` 
  - 设置对外服务的http端口，默认为9200。
- `transport.tcp.port: 9300` 
  - 集群结点之间通信端口
- `node.master:`
  - 指定该节点是否有资格被选举成为master结点，默认是true，如果原来的master宕机会重新选举新的master。 
- `node.data: `
  - 指定该节点是否存储索引数据，默认为true。
- `discovery.zen.ping.unicast.hosts: ["host1:port", "host2:port", "..."]` 
  - 设置集群中master节点的初始列表。
- `discovery.zen.ping.timeout: 3s` 
  - 设置ES自动发现节点连接超时的时间，默认为3秒，如果网络延迟高可设置大些。
- `discovery.zen.minimum_master_nodes:`
  - 主结点数量的最少值 ,此值的公式为：`(master_eligible_nodes / 2) + 1`，比如：有3个符合要求的主结点，那么这里要设置为2。
- `node.max_local_storage_nodes:`
  - 单机允许的最大存储结点数，通常单机启动一个结点建议设置为1，开发环境如果单机启动多个节点可设置大于1.

### 2.2.2 `jvm.options`

设置最小及最大的JVM堆内存大小：
在`jvm.options`中设置`-Xms`和`-Xmx`：

1. 两个值设置为相等
2. 将 Xmx 设置为不超过物理内存的一半。

### 2.2.3 `log4j2.properties`

日志文件设置，ES使用log4j，注意日志级别的配置。

### 2.2.4 系统配置

在linux上根据系统资源情况，可将每个进程最多允许打开的文件数设置大些。

查询当前文件数：`su limit -n`

方式一：使用命令设置limit，先切换到root，设置完成再切回elasticsearch用户。

```shell
sudo su
ulimit ‐n 65536
su elasticsearch
```

方式二：修改文件进行持久设置，在`/etc/security/limits.conf`文件中加入`elasticsearch ‐ nofile 65536`配置。

### 2.2.5 启动ElasticSearch

Windows系统：

- 进入bin目录，在cmd下运行`elasticsearch.bat`
- 浏览器输入：http://localhost:9200
- 显示结果如下（配置不同内容则不同）说明ElasticSearch启动成功。

```json
{
    "name" : "xc_node_1",
    "cluster_name" : "xuecheng",
    "cluster_uuid" : "J18wPybJREyx1kjOoH8T‐g",
    "version" : {
        "number" : "6.2.1",
        "build_hash" : "7299dc3",
        "build_date" : "2018‐02‐07T19:34:26.990113Z",
        "build_snapshot" : false,
        "lucene_version" : "7.2.1",
        "minimum_wire_compatibility_version" : "5.6.0",
        "minimum_index_compatibility_version" : "5.0.0"
    },
    "tagline" : "You Know, for Search"
}
```

# 3 可视化管理插件——head

## 3.1 概述

head插件是ES的一个可视化管理插件，用来监视ElasticSearch的状态，并通过head客户端和ElasticSearch服务进行交互，比如创建映射、创建索引等。

head的项目地址：https://github.com/mobz/elasticsearch-head 。

## 3.2 安装和运行

从ElasticSearch6.0开始，head插件支持使得`node.js`运行。

1. 安装node.js
2. 下载head并运行

```shell
git clone https://github.com/mobz/elasticsearch-head.git 

cd elasticsearch-head

npm install

npm run start 
```

浏览器访问：http://localhost:9100/

![](https://zhishan-zh.github.io/media/ElasticSearch-20200527235552.png)

## 3.3 报错：Origin null is not allowed by Access-Control-Allow-Origin

打开浏览器调试工具发现报错：

>Origin null is not allowed by Access-Control-Allow-Origin.

**报错原因**：head插件作为客户端要连接ElasticSearch服务（localhost:9200），此时存在跨域问题，ElasticSearch默认不允许跨
域访问。
**解决方案**：设置ElasticSearch允许跨域访问。
在`config/elasticsearch.yml`后面增加以下参数：

```properties
#开启cors跨域访问支持，默认为false 
http.cors.enabled: true 

#跨域访问允许的域名地址，(允许所有域名)以上使用正则 
http.cors.allow-origin: /.*/
```

注意：将`config/elasticsearch.yml`另存为utf-8编码格式。

# 4 入门案例

## 4.1 创建索引库

ElasticSearch的索引库是一个逻辑概念，它包括了分词列表及文档列表，同一个索引库中存储了相同类型的文档。它就相当于MySQL中的表，或相当于Mongodb中的集合。

关于索引这个语：

- 索引（名词）：ElasticSearch是基于Lucene构建的一个搜索服务，它要从索引库搜索符合条件索引数据。
- 索引（动词）：索引库刚创建起来是空的，将数据添加到索引库的过程称为索引。

创建索引库都是客户端以RESTful的方式向ElasticSearch服务发送命令。

### 4.1.1 使用postman、curl等工具创建

以put的方式访问：`http://localhost:9200/索引库名称`

携带的参数：

```json
{
    "settings":{
        "index":{
            "number_of_shards":1,
            "number_of_replicas":0
        }
    }
}
```

参数说明：

- `number_of_shards`：设置分片的数量，在集群中通常设置多个分片，表示一个索引库将拆分成多片分别存储不同的结点，提高了ElasticSearch的处理能力和高可用性，如果使用单机环境，则设置为1。
    - 索引库创建之后，分片的数量不能随意变更，但副本的数量可以改变。
- `number_of_replicas`：设置副本的数量，设置副本是为了提高ElasticSearch的高可靠性，单机环境设置为0.

返回值：

```json
{
    "acknowledged": true,
    "shards_acknowledged": true,
    "index": "Index_library"
}
```

### 4.1.2 使用head插件创建

## 4.2 创建映射

### 4.2.1 概念说明

在索引中每个文档都包括了一个或多个field，创建映射就是向索引库中创建field的过程。

与关系数据库的概念的类比，ElasticSearch的文档（Document）就相当于Row记录，ElasticSearch的字段（Field）相当于Columns 列。

注意：6.0之前的版本有type（类型）概念，type相当于关系数据库的表，ElasticSearch官方将在ElasticSearch9.0版本中彻底删除type。

那ElasticSearch创建的索引库相当于关系数据库中的数据库还是表？

1. 如果相当于数据库就表示一个索引库可以创建很多不同类型的文档，这在ES中也是允许的。
2. 如果相当于表就表示一个索引库只能存储相同类型的文档，ES官方建议在一个索引库中只存储相同类型的文档。

### 4.2.2 创建映射

我们要把课程信息存储到ES中，这里我们创建课程信息的映射，先来一个简单的映射，如下：
发送：`post http://localhost:9200/索引库名称/类型名称/_mapping`

创建类型为Index_library的映射，共包括三个字段：name、description、studymondel，由于ES6.0版本还没有将type彻底删除，所以暂时把type起一个没有特殊意义的名字。

post 请求：http://localhost:9200/Index_library/doc/_mapping
表示：在Index_library索引库下的doc类型下创建映射。doc是类型名，可以自定义，在ES6.0中要弱化类型的概念，给它起一个没有具体业务意义的名称。

参数：

```json
{
    "properties": {
        "name": {
        	"type": "text"
        },
        "description": {
        	"type": "text"
        },
        "studymodel": {
        	"type": "keyword"
        }
    }
}
```

## 4.3 创建文档

ES中的文档相当于MySQL数据库表中的记录。
发送PUT或POST：`http://localhost:9200/Index_library/doc/id值`（如果不指定id值ES会自动生成ID）

如：http://localhost:9200/Index_library/doc/4028e58161bcf7f40161bcf8b77c0000

参数：

```json
{
    "name":"Bootstrap开发框架",
    "description":"Bootstrap是由Twitter推出的一个前台页面开发框架，在行业之中使用较为广泛。此开发框架包含了大量的CSS、JS程序代码，可以帮助开发者（尤其是不擅长页面开发的程序人员）轻松的实现一个不受浏览器限制的精美界面效果。",
    "studymodel":"201001"
}
```

返回：

```json
{
    "_index": "Index_library",
    "_type": "doc",
    "_id":"4028e58161bcf7f40161bcf8b77c0000",
    "_version":1,
    "result":"created",
    "_shards":{
        "total":1,
        "successful":1,
        "failed":0
    },
    "_seq_no":0,
    "_primary_term":1
}
```

## 4.4 搜索文档

### 4.4.1 根据课程id查询文档
发送get：http://localhost:9200/Index_library/doc/4028e58161bcf7f40161bcf8b77c0000

### 4.4.2 查询所有记录

发送get：http://localhost:9200/Index_library/doc/_search

### 4.4.3 查询名称中包括spring关键字的的记录

发送get：http://localhost:9200/Index_library/doc/_search?q=name:spring

### 4.4.4 查询学习模式为201001的记录

发送get：http://localhost:9200/Index_library/doc/_search?q=studymodel:201001

### 4.4.5 查询结果分析

```json
{
    "took": 1,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": 1,
        "max_score": 0.2876821,
        "hits": [
            {
                "_index": "Index_library",
                "_type": "doc",
                "_id": "4028e58161bcf7f40161bcf8b77c0000",
                "_score": 0.2876821,
                "_source": {
                    "name": "Bootstrap开发框架",
                    "description": "Bootstrap是由Twitter推出的一个前台页面开发框架，在行业之中使用较 为广泛。此开发框架包含了大量的CSS、JS程序代码，可以帮助开发者（尤其是不擅长页面开发的程序人员）轻松的实现一个不受浏览器限制的精美界面效果。",
                    "studymodel": "201001"
                }
            }
        ]
    }
}
```

参数解析：

- `took`：本次操作花费的时间，单位为毫秒。
- `timed_out`：请求是否超时
- `_shards`：说明本次操作共搜索了哪些分片
- `hits`：搜索命中的记录
- `hits.total` ： 符合条件的文档总数 
- `hits.hits` ：匹配度较高的前N个文档
- `hits.max_score`：文档匹配得分，这里为最高分
- `_score`：每个文档都有一个匹配度得分，按照降序排列。
- `_source`：显示了文档的原始内容。