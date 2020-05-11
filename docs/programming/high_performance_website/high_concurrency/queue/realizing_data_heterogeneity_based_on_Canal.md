# 基于Canal实现数据异构

# 1 概述

在大型网站架构中，DB都会采用分库分表来解决容量和性能问题，但是分库分表之后带来了新的问题，比如不同维度的查询或者聚合查询，此时就会非常棘手。一般我们会通过数据异构机制来解决此问题。

如下图所示，为了提升系统的接单能力，我们会对订单表进行分库分表，但是，随之而来的问题是：用户怎么查询自己的订单列表呢？

- 一种办法是扫描所有的订单表，然后进行聚合，但是这种方式在大流量系统架构中肯定是不行的。
- 另一种办法是双写，但是双写的一种一致性又没法保证。
- 还有一种办法就是订阅数据库变更日志，比如订阅MySQL的binlog日志模拟数据库的主从同步机制，然后解析变更日志将数据写到订单列表，从而实现数据异构，这种机制也能保证数据的一致性。

![image-20200508221116551](https://zhishan-zh.github.io/media/image-20200508221116551.png)除了可以进行订单列表的异构，像商家维度的异构、ES搜索异构、订单缓存异构等都可以通过这种方式解决。

在介绍Canal之前，我们先看一下MySQL的主从复制架构。

# 2 MySQL主从复制

MySQL主从复制架构如下图所示。

![image-20200508223019363](https://zhishan-zh.github.io/media/image-20200508223019363.png)

1. 首先MySQL客户端将数据写入master数据库。
2. master数据库会将变更的记录数据写入二进制日志中，即binlog。
3. slave数据库会订阅master数据库的binlog日志，通过一个I/O线程从binlog的指定位置拉取日志进行主从同步，此时master数据库会有一个Binlog Dump线程来读取binlog日志与slave I/O线程进行数据同步。
4. slave I/O线程读取到日志后会先写入relay log重放日志中。
5. slave数据库通过一个SQL线程读取relay log进行日志重放，这样就实现了主从数据库之间的同步。

可以把Canal看作slave数据库，其订阅主数据库的binlog日志，然后读取并解析日志，这样就实现了数据同步/异构。

# 3 Canal简介

Canal是阿里开源的一款基于MySQL数据库binlog的增量订阅和消费组件，通过它可以订阅数据库的binlog日志，然后进行一些数据消费，如数据镜像、数据异构、数据索引、缓存更新等。相对于消息队列，通过这种机制可以实现数据的有序性和一致性。

Canal架构如下图所示。

![image-20200508225253162](https://zhishan-zh.github.io/media/image-20200508225253162.png)

首先需要部署canal server，可以同时部署多台，但是只有一台是活跃的，其他的作为备机。canal server会通过slave机制订阅数据库的binlog日志。canal server的高可用是通过zk维护的。

然后canal client会订阅canal server，消费变更的表数据，然后写入到镜像数据库、异构数据库、缓存数据库，具体如何应用就看自己的场景了，同时也只有一台canal client是活跃的，其他的作为备机，当活跃的canal client不可用后，备机会被激活。canal client 的高可用也是通过zk来维护的，比如zk维护了当前消费到的日志位置。

canal server目前读取的binlog事件只存储在内存中，且只有一个canal client能进行消费，其他的作为备机。如果需要多消费客户端，则可以先写入ActiveMQ/kafka，然后进行消费。如果有多个消费者，那么也建议使用此种模式，而不是启动多个canal server读取binlog日志，这样会使得数据库的压力较大。ActiveMQ提供了虚拟主题的概念，支持同一份内容多消费者镜像消费的特性。

canal一个常见应用场景是同步缓存，当数据库变更后通过binlog进行缓存的增量更新。当缓存更新出现问题时，应能回退binlog到过去某个位置进行重新同步，并提供全量刷缓存的方法，如下图所示。

![image-20200509090553037](https://zhishan-zh.github.io/media/image-20200509090553037.png)

另一个常见应用场景是下发任务，当数据变更时需要通知其他依赖系统。其原理是任务系统监听数据库数据变更，然后将变更的数据写入MQ/Kafka进行任务下发，比如商品数据变更后需要通知商品详情页、列表页、搜索页等相关系统。这种方式可以保证数据下发的精确性，通过MQ发消息通知变更缓存是无法做到这一点的，而且业务系统中也不会散落着各种下发MQ的代码，从而实现了下发的归集，如下图所示。

![image-20200509091815659](https://zhishan-zh.github.io/media/image-20200509091815659.png)

类似与数据库触发器，只要想在数据库数据变更时进行一些处理，都可以使用Canal来完成。

在MySQL主从结构中，当有多个slave连接master数据库时，master数据库的压力比较大，为保障master数据库的性能，canal server可订阅slave的binlog日志即是slave的slave。

# 4 Canal示例

## 4.1 数据库配置

修改`my.ini`配置文件的如下信息：

```ini
[mysqld]
log-bin=mysql-bin	#开启二进制日志
binlog-format=ROW	#使用row模式，不要使用statement或者mixed模式
server_id=1	#配置主数据库ID，不能和从数据库重复
```

**binlog提供了三种记录模式**：

1. row：记录的是修改的记录信息，而不是执行的SQL，二进制日志文件会占用更大的空间，当执行alter table修改表结构造成记录变更时，该表的每一条记录都会被记录到日志中。
2. statement：每一条修改数据的SQL都会被记录在binlog中，其缺点很明显，比如我们使用了MySQL系统函数，可能会导致主从数据不一致。
3. mixed：一般SQL使用statement模式记录，特殊操作如一些系统函数则采用row模式记录。

在使用Canal时建议使用row模式。

另外，在MySQL中执行`show binary logs`将看到当前有哪些二进制日志文件及其大小。

接下来，我们要为Canal创建一个复制帐号，并为其授权查询和复制权限。

```sql
CREATE USER canal IDENTIFIED BY 'canal';
CREATE SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%';
```

这样我们就可以使用Canal这个数据库帐号进行主从复制了。

## 4.2 启动ZooKeeper

到zk官网下载ZooKeeper-3.4.9，如果需要修改`zoo.cfg`配置文件，则进行一些配置，然后执行如下命令启动单ZooKeeper服务器。

```shell
./bin/zkServer.sh start
```

为了简化演示，我们没有部署zk集群。

## 4.3 Canal Server

到Canal官网下载`canal.deployer-1.0.22.tar.gz`，首先需要进行数据库示例的配置，其提供了`conf/example/instance.properties`一个示例配置，我们复制一份到`conf/product/instance.properties`，然后修改以下配置。

```properties
## mysql serverId必须和master不一样
canal.instance.mysql.slaveId = 101

# prosition info 链接的数据库地址和从哪个二进制日志文件和从哪个位置开始
canal.instance.master.address = 192.168.0.10:3306
# MySQL主数据库链接时，起始的binlog文件
canal.instance.master.journal.name = 
# MySQL主库链接时，起始的binlog偏移量
canal.instance.master.position = 
# MySQL主库链接时，起始的binlog的时间戳
canal.instance.master.timestamp = 

# 用户名/密码/默认数据库/数据库编码（一定要配置正确）
canal.instance.dbUsername = canal
canal.instance.dbPassword = canal
canal.instance.defaultDatabaseName = 
canal.instance.connectionCharset = UTF-8
```

还可以通过如下配置过滤订阅哪些数据库中的哪些表，从而减少不必要的订阅，比如，我们只关注产品数据库，那么通过如下模式即可只订阅产品数据库。

```properties
canal.instance.filter.regex = product_\d+\\.*
```

如果有多个数据库可以进行多个`***/instance.properties`配置，则每个数据库设置一个配置文件。

接下来，进行canal server的设置，修改`conf/canal.properties`。

```properties
# canal id、地址、端口和使用的zk服务地址
canal.id = 1
canal.ip = 
canal.port = 11111
canal.zkServers=127.0.0.1:2181

# 当前canal server上部署的实例，配置多个时用逗号分割，此处配置了product
canal.destinations = product

# 使用zk持久化模式，这样可以保证集群数据共享，支持HA
canal.instance.global.spring.xml = classpath:spring/default-instance.xml
```

然后执行如下命令，启动一个canal server。

```shell
./bin/startup.sh
```

## 4.4 Canal Client

接着创建或在已有的Java应用中添加MySQL客户端依赖、Canal客户端依赖（`com.alibaba.otter# canal.client# 1.0.22`）。

订阅数据库变更的Java代码。

```java
public void test() throws Exception {
    //通过zookeeper连接cannal server
    String zkServers = "192.168.61.129:2181";
    //目标时product实例
    String destination = "product";
    CanalConnector connector = CanalConnector.newClusteConnector(zkServices, destination, "", "");
    
    //连接，并订阅product数据库下的product表（如果不写该模式，则订阅所有的）
    connector.connect();
    connector.subscribe("product_.*\\.product_.*");
    
    while(true){
        //批量获取1000个日志（不确认模式）
        Message message = connector.getWithoutAck(1000);
        for(Entry entry : message.getEntries()) {
            //如果是行数据
            if(entry.getEntryType() == EntryType.ROWDATA) {
                //则解析行变更
                RowChange row = RowChange.parseFrom(entry.getStroreValue());
                EventType rowEventType = row.getEventType();
                for(RowData rowData : row.getRowDatasList()) {
                    //如果时删除，则获取删除的数据，然后进行业务处理
                    if(rowEventType == EventType.DELETE) {
                        List<Column> columns = rowData.getBeforeColumnsList();
                        delete(columns);
                    }
                    //如果时新增/修改，则获取新增/修改的数据进行业务处理
                    if(rowEventType = EventType.INSERT || rowEventType == EventType.UPDATE) {
                        List<Column> columns = rowData.getAfterColumnsList();
                        save(columns);
                    }
                }
            }
        }
        //确认日志消费成功
        connector.ack(message.getId());
    }
}
private static void save(List<Column> columns) {
    columns.forEach((column -> {
        String name = column.getName();
        String value = column.getValue();
        //业务处理（省略）
    }));
}
```

通过以上代码，我就捕获了数据库日志变更，然后进行相关的业务处理即可。不管是数据库异构还是缓存更新，因为数据就在这里，怎么处理就在这里，怎么处理就是业务逻辑的事情了。

京东内部有一个类似的组件BinLake。Canal开源版本只提供了MySQL日志解析，如果想要Oracle日志解析，则可以使用LinkedIn的Databus。

