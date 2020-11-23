# zookeeper

# 1 zookeeper简介
## 1.1 什么是zookeeper
zookeeper是一个高效的**分布式协调服务**，它暴露了一些共用服务，比如命名/配置管理/同步控制/群组服务等。我们可以使用ZK来实现比如达成共识/集群管理/leader选举等。

zookeeper是一个高可用的分布式管理与协调框架，基于ZAB算法（原子消息广播协议）的实现。该框架能够很好地保证分布式环境中数据的一致性。也正是基于这样的特性，使得zookeeper成为了解决分布式一致性问题的利器。

Zookeeper是为别的分布式程序服务的，并且Zookeeper本身就是一个分布式程序（只要有半数以上节点存活，zk就能正常服务）。

- Zookeeper集群的角色：  Leader 和  follower  （Observer）
- 只要集群中有半数以上节点存活，集群就能提供服务

Zookeeper所提供的服务涵盖：主从协调、服务器节点动态上下线、统一配置管理、分布式共享锁、统一名称服务等等。

虽然说可以提供各种服务，但是zookeeper在底层其实只提供了两个功能：

- 管理（存储，读取）用户程序提交的数据；
- 并为用户程序提供数据节点监听服务；

## 1.2 zookeeper的特点

- **顺序一致性**
   - 从一个客户端发起的事务请求，最终将会严格地按照其发起的顺序被应用到zookeeper中去。
- **原子性**
   - 所有事务请求的处理结果在整个集群中的所有机器上的应用情况是一致的，也就是说，要么整个集群所有的机器都成功应用了某一事务，要么都没有应用，一定不会出现部分机器应用了该事务，而另一部分没有应用的情况。
- **单一视图**
   - 无论客户端连接的是哪一个zookeeper服务器，其看到的服务器端数据模型都是一致的。
- **可靠性**
   - 一旦服务器成功地应用了一个事务，并完成对客户端的响应，那么该事务所引起的服务器端状态将会被一致包留下来。除非有另外一个事务对其更改。
- **实时性**
   - 通常所说的实时性就是指一旦事务被成功应用，那么客户端就能立刻从服务器上获取变更后的新数据，zookeeper仅仅能保证在一段时间内，客户端最终一定能从服务器端读取最新的数据状态。
## 1.3 zookeeper的作用

- zookeeper不适合存储大量的信息，适合存储配置信息等。
- 可以作为集群的管理工具使用。
- 可以集中管理配置文件。

虽然说可以提供各种服务，但是zookeeper在底层其实只提供了两个功能：

- 管理（存储，读取）用户程序提交的数据；
- 并为用户程序提供数据节点监听服务；

## 1.4 zookeeper特性

1. Zookeeper：一个leader，多个follower组成的集群
2. 全局数据一致：每个server保存一份相同的数据副本，client无论连接到哪个server，数据都是一致的
3. 分布式读写，更新请求转发，由leader实施
4. 更新请求顺序进行，来自同一个client的更新请求按其发送顺序依次执行
5. 数据更新原子性，一次数据更新要么成功，要么失败
6. 实时性，在一定时间范围内，client能读到最新数据

## 1.5 zookeeper数据结构

### 1.5.1 zookeeper数据结构概述

![zookeeper目录结构](https://zhishan-zh.github.io/media/zookeeper_datastructure_20200716180723.png)

- 层次化的目录结构，命名符合常规文件系统规范(见上图)
- 每个节点在zookeeper中叫做znode,并且其有一个唯一的路径标识
- 节点Znode可以包含数据和子节点（但是EPHEMERAL类型的节点不能有子节点）
- 客户端应用可以在节点上设置监视器。

### 1.5.2 Zookeeper节点类型

Znode有两种类型：

- 短暂（ephemeral）（断开连接自己删除）
- 持久（persistent）（断开连接不删除）

Znode有四种形式的目录节点（默认是persistent ）：

- PERSISTENT
- PERSISTENT_SEQUENTIAL（持久序列/test0000000019 ）
- EPHEMERAL
- EPHEMERAL_SEQUENTIAL

创建znode时设置顺序标识，znode名称后会附加一个值，顺序号是一个单调递增的计数器，由父节点维护。

在分布式系统中，顺序号可以被用于为所有的事件进行全局排序，这样客户端可以通过顺序号推断事件的顺序。

## 1.6 zookeeper原理

Zookeeper虽然在配置文件中并没有指定master和slave。但是，zookeeper工作时，是有一个节点为leader，其他则为follower，Leader是通过内部的选举机制临时产生的。

### 1.6.1 zookeeper的选举机制（全新集群paxos）

以一个简单的例子来说明整个选举的过程：

假设有5台服务器组成的zookeeper集群，它们的id从1-5，同时它们都是最新启动的，也就是没有历史数据，在存放数据量这一点上，都是一样的。假设这些服务器依序启动，来看看会发生什么：

1. 服务器1启动，此时只有它一台服务器启动了，它发出去的报没有任何响应，所以它的选举状态一直是LOOKING状态；
2. 服务器2启动，它与最开始启动的服务器1进行通信，互相交换自己的选举结果，由于两者都没有历史数据，所以id值较大的服务器2胜出，但是由于没有达到超过半数以上的服务器都同意选举它（这个例子中的半数以上是3），所以服务器1、2还是继续保持LOOKING状态。
3. 服务器3启动，根据前面的理论分析，服务器3成为服务器1、2、3中的老大，而与上面不同的是，此时有三台服务器选举了它，所以它成为了这次选举的leader。
4. 服务器4启动，根据前面的分析，理论上服务器4应该是服务器1、2、3、4中最大的，但是由于前面已经有半数以上的服务器选举了服务器3，所以它只能接收当小弟的命了。
5. 服务器5启动，同4一样当小弟。

### 1.6.2 非全新集群的选举机制（数据恢复）

那么，初始化的时候，是按照上述的说明进行选举的，但是zookeeper运行了一段时间之后，有机器down掉，重新选举时，选举过程就相对复杂了，需要加入数据id、leader id和逻辑时钟。

- 数据id：数据新的id就大，数据每次更新都会更新id。
- Leader id：就是我们配置的myid中的值，每个机器一个。
- 逻辑时钟：这个值从0开始递增，每次选举对应一个值，也就是说:  如果在同一次选举中，那么这个值应该是一致的 ;  逻辑时钟值越大，说明这一次选举leader的进程更新。

选举的标准就变成：

1. 逻辑时钟小的选举结果被忽略，重新投票；
2. 统一逻辑时钟后，数据id大的胜出；
3. 数据id相同的情况下，leader id大的胜出。

根据这个规则选出leader。

## 1.5 zookeeper应用场景

### 1.5.1 数据发布与订阅（配置中心）

发布与订阅模型，即所谓的配置中心，顾名思义就是发布者将数据发布到 ZK 节点上，供订阅者动态获取数据，实现配置信息的集中式管理和动态更新。例如全局的配置信息，服务式服务框架的服务地址列表等就非常适合使用。

- 应用中用到的一些配置信息放到 ZK 上进行集中管理。这类场景通常是这样：应用在启动的时候会主动来获取一次配置，同时，在节点上注册一个 Watcher，这样一来，以后每次配置有更新的时候，都会实时通知到订阅的客户端，从来达到获取最新配置信息的目的。
- 分布式搜索服务中，索引的元信息和服务器集群机器的节点状态存放在 ZK 的一些指定节点，供各个客户端订阅使用。
- 分布式日志收集系统。这个系统的核心工作是收集分布在不同机器的日志。收集器通常是按照应用来分配收集任务单元，因此需要在 ZK 上创建一个以应用名作为 path 的节点 P，并将这个应用的所有机器 ip，以子节点的形式注册到节点 P 上，这样一来就能够实现机器变动的时候，能够实时通知到收集器调整任务分配。
- 系统中有些信息需要动态获取，并且还会存在人工手动去修改这个信息的发问。 通常是暴露出接口，例如 JMX 接口， 来获取一些运行时的信息。
- 引入 ZK之后， 就不用自己实现一套方案了， 只要将这些信息存放到指定的 ZK 节点上即可。

**注意**： 在上面提到的应用场景中，有个默认前提是： 数据量很小，但是数据更新可能会比较快的场景。

### 1.5.2 负载均衡

这里说的负载均衡是指软负载均衡。 在分布式环境中， 为了保证高可用性，通常同一个应用或同一个服务的提供方都会部署多份， 达到对等服务。而消费者就须要在这些对等的服务器中选择一个来执行相关的业务逻辑，其中比较典型的是消息中间件中的生产者，消费者负载均衡。

- 消息中间件中发布者和订阅者的负载均衡， linkedin 开源的 KafkaMQ 和阿里开源的 metaq 都是通过 zookeeper 来做到生产者、 消费者的负载均衡。这里以 metaq 为例如讲下：
   - **生产者负载均衡**：
      - metaq 发送消息的时候，生产者在发送消息的时候必须选择一台 broker 上的一个分区来发送消息，因此 metaq 在运行过程中，会把所有 broker和对应的分区信息全部注册到 ZK 挃定节点上，默认的策略是一个依次轮询的过程， 生产者在通过 ZK 获取分区列表之后，会按照 brokerId 和partition 的顺序排列组织成一个有序的分区列表，发送的时候按照从头到尾循环往复的方式选择一个分区来发送消息。
   - **消费负载均衡**：
      - 在消费过程中， 一个消费者会消费一个或多个分区中的消息，但是一个分区只会由一个消费者来消费。 MetaQ 的消费策略是：
         1. 每个分区针对同一个 group 只挂载一个消费者。
         1. 如果同一个 group 的消费者数目大于分区数目，则多出来的消费者将不参与消费。
         1. 如果同一个 group 的消费者数目小于分区数目，则有部分消费者需要额外承担消费任务。
      - 在某个消费者故障或者重启等情况下，其他消费者会感知到这一变化（通过 zookeeper watch 消费者列表），然后重新进行负载均衡，保证所有的分区都有消费者迚行消费。

### 1.5.3 命名服务(Naming Service)

命名服务也是分布式系统中比较常见的一类场景。 在分布式系统中， 通过使用命名服务， 客户端应用能够根据指定名字来获取资源或服务的地址，提供者等信息。 被命名的实体通常可以是集群中的机器，提供的服务地址，进程对象等等——这些我们都可以统称他们为名字（ Name）。其中较为常见的就是一些分布式服务框架中的服务地址列表。 通过调用 ZK 提供的创建节点的 API， 能够很容易创建一个全局唯一的 path，这个 path 就可以作为一个名称。

- 阿里开源的分布式服务框架 Dubbo 中使用 ZooKeeper 来作为其命名服务， 维护全局的服务地址列表， 点击这里查看 Dubbo 开源项目。 在Dubbo 实现中：
   - 服务提供者在启动的时候，向 ZK 上的指定节点/dubbo/${serviceName}/providers 目录下写入自己的 URL 地址，这个操作就完成了服务的发布。
   - 服务消费者启动的时候， 订阅/dubbo/${serviceName}/providers 目录下的提供者 URL 地址， 并向/dubbo/${serviceName} /consumers目录下写入自己的 URL 地址。
   - 注意，所有向 ZK 上注册的地址都是临时节点，这样就能够保证服务提供者和消费者能够自动感应资源的变化。

另外， Dubbo 还有针对服务粒度的监控，方法是订阅/dubbo/${serviceName}目录下所有提供者和消费者的信息。

### 1.5.4 分布式通知/协调

ZooKeeper 中特有 watcher 注册与异步通知机制，能够很好的实现分布式环境下不同系统之间的通知与协调，实现对数据变更的实时处理。使用方法通常是不同系统都对 ZK 上同一个 znode 进行注册，监听 znode 的变化（包括 znode 本身内容及子节点的），其中一个系统 update 了 znode，那么另一个系统能够收到通知，并作出相应处理。

- 另一种心跳检测机制：检测系统和被检测系统之间并不直接关联起来，而是通过 zk 上某个节点关联，大大减少系统耦合。
- 另一种系统调度模式：某系统有控制台和推送系统两部分组成，控制台的职责是控制推送系统进行相应的推送工作。管理人员在控制台作的一些操作，实际上是修改了 ZK 上某些节点的状态，而 ZK 就把这些变化通知给他们注册 Watcher 的客户端，即推送系统，于是，作出相应的推送任务。
- 另一种工作汇报模式：一些类似于任务分发系统，子任务启动后，到 zk 来注册一个临时节点，并且定时将自己的进度进行汇报（将进度写回这个临时节点），这样任务管理者就能够实时知道任务进度。

总之，使用 zookeeper 来进行分布式通知和协调能够大大降低系统之间的耦合。

### 1.5.5 集群管理与 Master 选举

**集群机器监控：**

这通常用于那种对集群中机器状态，机器在线率有较高要求的场景，能够快速对集群中机器变化作出响应。这样的场景中，往往有一个监控系统，实时检测集群机器是否存活。过去的做法通常是：监控系统通过某种手段（比如 ping）定时检测每个机器，或者每个机器自己定时向监控系统汇报“我还活着” 。 这种做法可行，但是存在两个比较明显的问题：

1. 集群中机器有变劢的时候，牵连修改的东西比较多。
1. 有一定的延时。


利用 ZooKeeper 有两个特性，就可以实时另一种集群机器存活性监控系统：

1. 客户端在节点 x 上注册一个 Watcher，那么如果 x 的子节点变化了，会通知该客户端。
1. 创建 EPHEMERAL 类型的节点，一旦客户端和服务器的会话结束或过期，那么该节点就会消失。

例如，监控系统在 /clusterServers 节点上注册一个 Watcher，以后每动态加机器，那么就往 /clusterServers 下创建一个 EPHEMERAL 类型的节点： /clusterServers/{hostname}. 这样，监控系统就能够实时知道机器的增减情况，至于后续处理就是监控系统的业务了。

**Master选举：**

Master 选举则是 zookeeper 中最为经典的应用场景了。

在分布式环境中，相同的业务应用分布在不同的机器上，有些业务逻辑（例如一些耗时的计算，网络 I/O 处理），往往只需要让整个集群中的某一台机器进行执行，其余机器可以共享这个结果，这样可以大大减少重复劳动，提高性能，于是这个 master 选举便是这种场景下的碰到的主要问题。

利用 ZooKeeper 的强一致性，能够保证在分布式高并发情况下节点创建的全局唯一性，即：同时有多个客户端请求创建 /currentMaster 节点，最终一定只有一个客户端请求能够创建成功。 利用这个特性，就能很轻易的在分布式环境中进行集群选取了。

另外，这种场景演化一下，就是动态 Master 选举。这就要用到 EPHEMERAL_SEQUENTIAL 类型节点的特性了。

上文中提到，所有客户端创建请求，最终只有一个能够创建成功。在这里稍微变化下，就是允许所有请求都能够创建成功，但是得有个创建顺序，于是所有的请求最终在 ZK 上创建结果的一种可能情况是这样：<br />/currentMaster/{sessionId}-1 , /currentMaster/{sessionId}-2 , /currentMaster/{sessionId}-3 ….. 每次选取序列号最小的那个机器作为Master，如果这个机器挂了，由于他创建的节点会马上消失，那么之后最小的那个机器就是 Master 了。

在搜索系统中，如果集群中每个机器都生成一份全量索引，不仅耗时，而且不能保证彼此之间索引数据一致。因此让集群中的 Master 来进行全量索引的生成，然后同步到集群中其它机器。 另外， Master 选举的容灾措施是，可以随时进行手动指定 master，就是说应用在 zk 在无法获取 master 信息时，可以通过比如 http 方式，向一个地方获取 master。

在 Hbase 中，也是使用 ZooKeeper 来实现动态 HMaster 的选举。在 Hbase 实现中，会在 ZK 上存储一些 ROOT 表的地址和 HMaster 的地址，HRegionServer 也会把自己以临时节点（ Ephemeral）的方式注册到 Zookeeper 中，使得 HMaster 可以随时感知到各个 HRegionServer的存活状态，同时，一旦 HMaster 出现问题，会重新选举出一个 HMaster 来运行，从而避免了 HMaster 的单点问题

### 1.5.6 分布式锁

分布式锁，这个主要得益于 ZooKeeper 为我们保证了数据的强一致性。 锁服务可以分为两类，一个是**保持独占**，另一个是**控制时序**。

- 所谓保持独占，就是所有试图来获取这个锁的客户端，最终只有一个可以成功获得这把锁。 通常的做法是把 zk 上的一个 znode 看作是一把锁，通过 create znode 的方式来实现。所有客户端都去创建 /distribute_lock 节点，最终成功创建的那个客户端也即拥有了这把锁。
- 控制时序，就是所有试图来获取这个锁的客户端，最终都是会被安排执行，只是有个全局时序了。做法和上面基本类似，只是这里/distribute_lock 已经 预 先 存 在 ， 客 户 端 在 它 下 面 创 建 临 时 有 序 节 点 （ 这 个 可 以 通 过 节 点 的 属 性 控 制 ：CreateMode.EPHEMERAL_SEQUENTIAL 来指定）。 Zk 的父节点（ /distribute_lock）维持一份 sequence,保证子节点创建的时序性，从而也形成了每个客户端的全局时序。

### 1.5.7 分布式队列

队列方面， 简单地讲有两种，一种是常规的先进先出队列，另一种是要等到队列成员聚齐之后的才统一按序执行。对于第一种先进先出队列，和分布式锁服务中的控制时序场景基本原理一致，这里不再赘述。第二种队列其实是在 FIFO 队列的基础上作了一个增强。通常可以在 /queue 这个 znode 下预先建立一个/queue/num 节点，并且赋值为 n（或者直接给/queue 赋值 n），表示队列大小，之后每次有队列成员加入后，就判断下是否已经到达队列大小，决定是否可以开始执行了。这种用法的典型场景是，分布式环境中，一个大任务 Task A，需要在很多子任务完成（或条件就绪）情况下才能进行。这个时候，凡是其中一个子任务完成（就绪），那么就去 /taskList 下建立自己的临时时序节点（ CreateMode.EPHEMERAL_SEQUENTIAL），当 /taskList 发现自己下面的子节点满足指定个数，就可以进行下一步按序进行处理了。

# 2 搭建zookeeper服务器集群

Zookeeper集群机制为半数机制：集群中半数以上机器存活，集群可用。

## 2.1 结构：一共三个节点

- zk服务器集群规模不小于3个节点，一般要求奇数个节点。
- 要求服务器之间系统时间保持一致。

## 2.2 安装zookeeper

1. 进行解压： `tar zookeeper-3.4.5.tar.gz`
1. 重命名： `mv zookeeper-3.4.5 zookeeper`
1. 修改环境变量：
   1. `vi /etc/profile`
   1. `export ZOOKEEPER_HOME=/usr/local/zookeeper`
   1. `export PATH=.:$HADOOP_HOME/bin:$ZOOKEEPER_HOME/bin:$JAVA_HOME/...`
4. 刷新： `source /etc/profile`
4. 到zookeeper下修改配置文件
   1. `cd /usr/local/zookeeper/conf`
   1. `mv zoo_sample.cfg zoo.cfg`
6. 修改conf: `vi zoo.cfg` 修改两处
   1. `dataDir=/usr/local/zookeeper/data`
   1. 最后面添加
      1. `server.0=zh:2888:3888`
      1. `server.1=hadoop1:2888:3888`
      1. `server.2=hadoop2:2888:3888`
7. 服务器标识配置：
   1. 创建文件夹： `mkdir data` 
   1. 创建文件myid并填写内容为0： `vi myid`  (内容为服务器标识 ： 0)
8. 进行复制zookeeper目录到hadoop01和hadoop02还有/etc/profile文件
8. 把hadoop01、 hadoop02中的myid文件里的值修改为1和2路径( `vi /usr/local/zookeeper/data/myid` )
8. 启动zookeeper：
   1. 路径： `/usr/local/zookeeper/bin` 
   1. 执行： `zkServer.sh start` (注意这里3台机器都要进行启动)
11. 状态： `zkServer.sh status` (在三个节点上检验zk的mode,一个leader和俩个follower)

## 2.3 zoo.cfg详解

- `tickTime`
   - 基本事件单元，以毫秒为单位。这个时间是作为 Zookeeper服务器之间或客户端与服务器之间维持心跳的时间间隔
   - 也就是每隔 tickTime时间就会发送一个心跳。
- `dataDir`
   - 存储内存中数据库快照的位置，顾名思义就是 Zookeeper
   - 保存数据的目录，默认情况下， Zookeeper
   - 将写数据的日志文件也保存在这个目录里。
- `clientPort`
   - 这个端口就是客户端连接 Zookeeper 服务器的端口， Zookeeper
   - 会监听这个端口，接受客户端的访问请求。
- `initLimit`
   - 这个配置项是用来配置 Zookeeper接受客户端初始化连接时最长能忍受多少个心跳时间间隔数，当已经超过 10 个心跳的时间（也就是 tickTime）长度后Zookeeper 服务器还没有收到客户端的返回信息，那么表明这个客户端连接失败。总的时间长度就是10*2000=20 秒。
- `syncLimit`
   - 这个配置项标识 Leader 与 Follower之间发送消息，请求和应答时间长度，最长不能超过多少个 tickTime的时间长度，总的时间长度就是 5*2000=10 秒
- `server.A = B:C:D`
   - A表示这个是第几号服务器,
   - B 是这个服务器的 ip 地址；
   - C 表示的是这个服务器与集群中的 Leader服务器交换信息的端口；
   - D 表示的是万一集群中的 Leader服务器挂了，需要一个端口来重新进行选举，选出一个新的 Leader

# 3 Docker方式安装Zookeeper（单机和集群）

## 3.1 拉取zookeeper镜像

- 启动docker（manjaro）：`systemctl start docker`

- 使用docker查询zookeeper镜像：`sudo docker search zookeeper`

- 拉取zookeeper镜像：`sudo docker pull zookeeper`

    - ```shell
        Using default tag: latest
        latest: Pulling from library/zookeeper
        8559a31e96f4: Pull complete 
        65306eca6b8e: Pull complete 
        ddbf88050b6e: Pull complete 
        0cb03c61bf26: Pull complete 
        0fae52060f18: Pull complete 
        a0d6ea5c70b0: Pull complete 
        7130f613f7ed: Pull complete 
        9a21e49a5bd3: Pull complete 
        Digest: sha256:fe31564f6864be074109cc70f6f70c66c111faf4cf8af1af943a678e0f35cd51
        Status: Downloaded newer image for zookeeper:latest
        docker.io/library/zookeeper:latest
        ```

- 查看镜像列表：`sudo docker images`

    - ```shell
        REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
        zookeeper           latest              6982b35ff928        2 weeks ago         252MB
        ```

- 查看镜像详情：`sudo docker inspect zookeeper`或`sudo docker inspect 6982b35ff928`

    - ```json
        [
            {
                "Id": "sha256:6982b35ff928aa314b5fb9107edaabb5969039be9271222ef1aa5ae116f34830",
                "RepoTags": [
                    "zookeeper:latest"
                ],
                "RepoDigests": [
                    "zookeeper@sha256:fe31564f6864be074109cc70f6f70c66c111faf4cf8af1af943a678e0f35cd51"
                ],
                "Parent": "",
                "Comment": "",
                "Created": "2020-06-29T20:44:15.02618204Z",
                "Container": "1d09188d6a83fc7174c369ee87dc600b93104b7be5fe4685fb96ef7a3e4cd484",
                "ContainerConfig": {
                    "Hostname": "1d09188d6a83",
                    "Domainname": "",
                    "User": "",
                    "AttachStdin": false,
                    "AttachStdout": false,
                    "AttachStderr": false,
                    "ExposedPorts": {
                        "2181/tcp": {},
                        "2888/tcp": {},
                        "3888/tcp": {},
                        "8080/tcp": {}
                    },
                    "Tty": false,
                    "OpenStdin": false,
                    "StdinOnce": false,
                    "Env": [
                        "PATH=/usr/local/openjdk-11/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/apache-zookeeper-3.6.1-bin/bin",
                        "LANG=C.UTF-8",
                        "JAVA_HOME=/usr/local/openjdk-11",
                        "JAVA_VERSION=11.0.7",
                        "JAVA_BASE_URL=https://github.com/AdoptOpenJDK/openjdk11-upstream-binaries/releases/download/jdk-11.0.7%2B10/OpenJDK11U-jre_",
                        "JAVA_URL_VERSION=11.0.7_10",
                        "ZOO_CONF_DIR=/conf",
                        "ZOO_DATA_DIR=/data",
                        "ZOO_DATA_LOG_DIR=/datalog",
                        "ZOO_LOG_DIR=/logs",
                        "ZOO_TICK_TIME=2000",
                        "ZOO_INIT_LIMIT=5",
                        "ZOO_SYNC_LIMIT=2",
                        "ZOO_AUTOPURGE_PURGEINTERVAL=0",
                        "ZOO_AUTOPURGE_SNAPRETAINCOUNT=3",
                        "ZOO_MAX_CLIENT_CNXNS=60",
                        "ZOO_STANDALONE_ENABLED=true",
                        "ZOO_ADMINSERVER_ENABLED=true",
                        "ZOOCFGDIR=/conf"
                    ],
                    "Cmd": [
                        "/bin/sh",
                        "-c",
                        "#(nop) ",
                        "CMD [\"zkServer.sh\" \"start-foreground\"]"
                    ],
                    "ArgsEscaped": true,
                    "Image": "sha256:5838bca00d1e75879153e74937f5f749dbc1063d003f5214062e310f0a1d946c",
                    "Volumes": {
                        "/data": {},
                        "/datalog": {},
                        "/logs": {}
                    },
                    "WorkingDir": "/apache-zookeeper-3.6.1-bin",
                    "Entrypoint": [
                        "/docker-entrypoint.sh"
                    ],
                    "OnBuild": null,
                    "Labels": {}
                },
                "DockerVersion": "18.09.7",
                "Author": "",
                "Config": {
                    "Hostname": "",
                    "Domainname": "",
                    "User": "",
                    "AttachStdin": false,
                    "AttachStdout": false,
                    "AttachStderr": false,
                    "ExposedPorts": {
                        "2181/tcp": {},
                        "2888/tcp": {},
                        "3888/tcp": {},
                        "8080/tcp": {}
                    },
                    "Tty": false,
                    "OpenStdin": false,
                    "StdinOnce": false,
                    "Env": [
                        "PATH=/usr/local/openjdk-11/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/apache-zookeeper-3.6.1-bin/bin",
                        "LANG=C.UTF-8",
                        "JAVA_HOME=/usr/local/openjdk-11",
                        "JAVA_VERSION=11.0.7",
                        "JAVA_BASE_URL=https://github.com/AdoptOpenJDK/openjdk11-upstream-binaries/releases/download/jdk-11.0.7%2B10/OpenJDK11U-jre_",
                        "JAVA_URL_VERSION=11.0.7_10",
                        "ZOO_CONF_DIR=/conf",
                        "ZOO_DATA_DIR=/data",
                        "ZOO_DATA_LOG_DIR=/datalog",
                        "ZOO_LOG_DIR=/logs",
                        "ZOO_TICK_TIME=2000",
                        "ZOO_INIT_LIMIT=5",
                        "ZOO_SYNC_LIMIT=2",
                        "ZOO_AUTOPURGE_PURGEINTERVAL=0",
                        "ZOO_AUTOPURGE_SNAPRETAINCOUNT=3",
                        "ZOO_MAX_CLIENT_CNXNS=60",
                        "ZOO_STANDALONE_ENABLED=true",
                        "ZOO_ADMINSERVER_ENABLED=true",
                        "ZOOCFGDIR=/conf"
                    ],
                    "Cmd": [
                        "zkServer.sh",
                        "start-foreground"
                    ],
                    "ArgsEscaped": true,
                    "Image": "sha256:5838bca00d1e75879153e74937f5f749dbc1063d003f5214062e310f0a1d946c",
                    "Volumes": {
                        "/data": {},
                        "/datalog": {},
                        "/logs": {}
                    },
                    "WorkingDir": "/apache-zookeeper-3.6.1-bin",
                    "Entrypoint": [
                        "/docker-entrypoint.sh"
                    ],
                    "OnBuild": null,
                    "Labels": null
                },
                "Architecture": "amd64",
                "Os": "linux",
                "Size": 252290293,
                "VirtualSize": 252290293,
                "GraphDriver": {
                    "Data": {
                        "LowerDir": "/var/lib/docker/overlay2/df7f5169ef02c3685e581f3a6ad414ca742e6eead834daa680a21ff159a1b513/diff:/var/lib/docker/overlay2/16f40930e5bbd78fb168eb8c73e0e7a563270ccff346a79cc64d06d5946ed5fc/diff:/var/lib/docker/overlay2/de399ff6f05a0800d462fd2acb5bbacb2271ed2afd91634040326b786382140f/diff:/var/lib/docker/overlay2/31f8616052b0f04fa11c4ce34ce98ae36d11fab8219cd276d58bbb84a57df29a/diff:/var/lib/docker/overlay2/1582ae224eb7f173faef96e2e32f858c06fdbe5b8f3482dc01806f938df125c9/diff:/var/lib/docker/overlay2/dd0c4251088d178c6450f0584e72f5fcb8219290268729d0b6d40fcdfef87aff/diff:/var/lib/docker/overlay2/36df9c1dafeed4beb31a959889c28d430db77c6137b5fdd8adc0a62e9acff909/diff",
                        "MergedDir": "/var/lib/docker/overlay2/cba01815a6e1d3a787b79300abda731ed627168e5e4f8f1b862d1549b1da38e1/merged",
                        "UpperDir": "/var/lib/docker/overlay2/cba01815a6e1d3a787b79300abda731ed627168e5e4f8f1b862d1549b1da38e1/diff",
                        "WorkDir": "/var/lib/docker/overlay2/cba01815a6e1d3a787b79300abda731ed627168e5e4f8f1b862d1549b1da38e1/work"
                    },
                    "Name": "overlay2"
                },
                "RootFS": {
                    "Type": "layers",
                    "Layers": [
                        "sha256:13cb14c2acd34e45446a50af25cb05095a17624678dbafbcc9e26086547c1d74",
                        "sha256:94cf29cec5e1e69ddeef0d0e43648b0185e0931920a0b37eda718a5ebe25fa46",
                        "sha256:9fc268fda51763b2c26c12dd6d384ff8c9e2910cfa3f91df4503b24d90e6435e",
                        "sha256:65be02c43d237b5ce3748d20d99930d18019d0c738a4e85becee125a056ddcba",
                        "sha256:496c13efa3189b99bfc99c91eef6167821341b3d32059028db14a7fbeda75fd1",
                        "sha256:0d62495d84f0e2e02818c32458c4d05d01492c22a69be6c6d4b34ffd25acebaa",
                        "sha256:6d6fbf5bcd68dbc0bb4bc0fa8b7eb19fbbf3132730e0a85239b9f8a5abedb27d",
                        "sha256:1013800da1d472d6c2cffbb6c7312c31e5cebc5d39a4b66a2d9f7fd8a9d92edb"
                    ]
                },
                "Metadata": {
                    "LastTagTime": "0001-01-01T00:00:00Z"
                }
            }
        ]
        ```

## 3.2 单机版

- 创建和启动zookeeper容器：`sudo docker run -d -p 2181:2181 --name single-zookeeper --restart always 6982b35ff928`

- 查看正在运行的容器：`sudo docker ps`

    - ```
        CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                                  NAMES
        0a00b15c20e3        6982b35ff928        "/docker-entrypoint.…"   43 seconds ago      Up 40 seconds       2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp   single-zookeeper
        ```

    - 登录守护式容器single-zookeeper：`sudo docker exec -it 0a00b15c20e3 /bin/bash`

        - 在容器single-zookeeper的终端中运行zookeeper shell：`./bin/zkCli.sh`

## 3.3 集群版

- 创建zookeeper自定义网络（网络模式为bridge）：`sudo docker network create --driver bridge zoo_cluster`

    - 查看已经存在的网络：`sudo docker network ls`

        - ```
            NETWORK ID          NAME                DRIVER              SCOPE
            c55394e95167        bridge              bridge              local
            3855964aa18e        host                host                local
            757ba10e775c        none                null                local
            c585bb0778cc        zoo_cluster         bridge              local
            ```

- 创建zookeeper集群容器节点1：

    - ```shell
        sudo docker run -d -p 2181:2181 --name zookeeper_node1 --privileged --restart always --network zoo_cluster --network-alias zoo_1 \
        -v /usr/local/zookeeper-cluster/node1/volumes/data:/data \
        -v /usr/local/zookeeper-cluster/node1/volumes/datalog:/datalog \
        -v /usr/local/zookeeper-cluster/node1/volumes/logs:/logs \
        -e ZOO_MY_ID=1 \
        -e "ZOO_SERVERS=server.1=zoo_1:2888:3888;2181 server.2=zoo_2:2888:3888;2182 server.3=zoo_3:2888:3888;2183" 6982b35ff928
        ```

- 创建zookeeper集群容器节点2：

    - ```shell
      sudo docker run -d -p 2182:2181 --name zookeeper_node2 --privileged --restart always --network zoo_cluster --network-alias zoo_2 \
        -v /usr/local/zookeeper-cluster/node2/volumes/data:/data \
-v /usr/local/zookeeper-cluster/node2/volumes/datalog:/datalog \
      -v /usr/local/zookeeper-cluster/node2/volumes/logs:/logs \
      -e ZOO_MY_ID=2 \
      -e "ZOO_SERVERS=server.1=zoo_1:2888:3888;2181 server.2=zoo_2:2888:3888;2182 server.3=zoo_3:2888:3888;2183" 6982b35ff928  
      ```
      
    
- 创建zookeeper集群容器节点3：

    - ```shell
        sudo docker run -d -p 2183:2181 --name zookeeper_node3 --privileged --restart always --network zoo_cluster --network-alias zoo_3 \
        -v /usr/local/zookeeper-cluster/node3/volumes/data:/data \
        -v /usr/local/zookeeper-cluster/node3/volumes/datalog:/datalog \
        -v /usr/local/zookeeper-cluster/node3/volumes/logs:/logs \
        -e ZOO_MY_ID=3 \
        -e "ZOO_SERVERS=server.1=zoo_1:2888:3888;2181 server.2=zoo_2:2888:3888;2182 server.3=zoo_3:2888:3888;2183" 6982b35ff928  
        ```

- 查看正在运行的容器：`sudo docker ps`

    - ```
        CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                                  NAMES
        45c4d5107c83        6982b35ff928        "/docker-entrypoint.…"   22 seconds ago      Up 21 seconds       2888/tcp, 3888/tcp, 8080/tcp, 0.0.0.0:2183->2181/tcp   zookeeper_node3
        13591868f57f        6982b35ff928        "/docker-entrypoint.…"   29 seconds ago      Up 28 seconds       2888/tcp, 3888/tcp, 8080/tcp, 0.0.0.0:2182->2181/tcp   zookeeper_node2
        025d815ddf7a        6982b35ff928        "/docker-entrypoint.…"   36 seconds ago      Up 35 seconds       2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp   zookeeper_node1
        ```

- 进入其中一个容器进行验证：`sudo docker exec -it 45c4d5107c83 bash`

    - ```shell
        root@45c4d5107c83:/apache-zookeeper-3.6.1-bin# ./bin/zkServer.sh status
        ZooKeeper JMX enabled by default
        Using config: /conf/zoo.cfg
        Client port found: 2183. Client address: localhost.
        Mode: leader
        ```

- 在主机连接zookeeper集群：`sudo ./zkCli.sh -server localhost:2181,localhost2182,localhost:2183`

    - ```
        /usr/bin/java
        Connecting to localhost:2181,localhost2182,localhost:2183
        2020-07-21 09:48:16,582 [myid:] - INFO  [main:Environment@98] - Client environment:zookeeper.version=3.6.1--104dcb3e3fb464b30c5186d229e00af9f332524b, built on 04/21/2020 15:01 GMT
        2020-07-21 09:48:16,586 [myid:] - INFO  [main:Environment@98] - Client environment:host.name=zh-inspironn4050
        2020-07-21 09:48:16,586 [myid:] - INFO  [main:Environment@98] - Client environment:java.version=1.8.0_252
        2020-07-21 09:48:16,589 [myid:] - INFO  [main:Environment@98] - Client environment:java.vendor=Oracle Corporation
        2020-07-21 09:48:16,589 [myid:] - INFO  [main:Environment@98] - Client environment:java.home=/usr/lib/jvm/java-8-openjdk/jre
        2020-07-21 09:48:16,589 [myid:] - INFO  [main:Environment@98] - Client environment:java.class.path=/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../zookeeper-server/target/classes:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../build/classes:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../zookeeper-server/target/lib/*.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../build/lib/*.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/zookeeper-prometheus-metrics-3.6.1.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/zookeeper-jute-3.6.1.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/zookeeper-3.6.1.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/snappy-java-1.1.7.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/slf4j-log4j12-1.7.25.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/slf4j-api-1.7.25.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/simpleclient_servlet-0.6.0.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/simpleclient_hotspot-0.6.0.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/simpleclient_common-0.6.0.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/simpleclient-0.6.0.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/netty-transport-native-unix-common-4.1.48.Final.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/netty-transport-native-epoll-4.1.48.Final.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/netty-transport-4.1.48.Final.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/netty-resolver-4.1.48.Final.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/netty-handler-4.1.48.Final.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/netty-common-4.1.48.Final.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/netty-codec-4.1.48.Final.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/netty-buffer-4.1.48.Final.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/metrics-core-3.2.5.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/log4j-1.2.17.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/json-simple-1.1.1.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jline-2.11.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jetty-util-9.4.24.v20191120.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jetty-servlet-9.4.24.v20191120.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jetty-server-9.4.24.v20191120.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jetty-security-9.4.24.v20191120.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jetty-io-9.4.24.v20191120.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jetty-http-9.4.24.v20191120.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/javax.servlet-api-3.1.0.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jackson-databind-2.10.3.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jackson-core-2.10.3.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/jackson-annotations-2.10.3.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/commons-lang-2.6.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/commons-cli-1.2.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../lib/audience-annotations-0.5.0.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../zookeeper-*.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../zookeeper-server/src/main/resources/lib/*.jar:/home/zh/下载/apache-zookeeper-3.6.1-bin/bin/../conf:
        2020-07-21 09:48:16,589 [myid:] - INFO  [main:Environment@98] - Client environment:java.library.path=/usr/java/packages/lib/amd64:/usr/lib64:/lib64:/lib:/usr/lib
        2020-07-21 09:48:16,589 [myid:] - INFO  [main:Environment@98] - Client environment:java.io.tmpdir=/tmp
        2020-07-21 09:48:16,589 [myid:] - INFO  [main:Environment@98] - Client environment:java.compiler=<NA>
        2020-07-21 09:48:16,590 [myid:] - INFO  [main:Environment@98] - Client environment:os.name=Linux
        2020-07-21 09:48:16,590 [myid:] - INFO  [main:Environment@98] - Client environment:os.arch=amd64
        2020-07-21 09:48:16,590 [myid:] - INFO  [main:Environment@98] - Client environment:os.version=5.4.52-1-MANJARO
        2020-07-21 09:48:16,590 [myid:] - INFO  [main:Environment@98] - Client environment:user.name=root
        2020-07-21 09:48:16,590 [myid:] - INFO  [main:Environment@98] - Client environment:user.home=/root
        2020-07-21 09:48:16,590 [myid:] - INFO  [main:Environment@98] - Client environment:user.dir=/home/zh/下载/apache-zookeeper-3.6.1-bin/bin
        2020-07-21 09:48:16,590 [myid:] - INFO  [main:Environment@98] - Client environment:os.memory.free=81MB
        2020-07-21 09:48:16,592 [myid:] - INFO  [main:Environment@98] - Client environment:os.memory.max=228MB
        2020-07-21 09:48:16,593 [myid:] - INFO  [main:Environment@98] - Client environment:os.memory.total=88MB
        2020-07-21 09:48:16,598 [myid:] - INFO  [main:ZooKeeper@1005] - Initiating client connection, connectString=localhost:2181,localhost2182,localhost:2183 sessionTimeout=30000 watcher=org.apache.zookeeper.ZooKeeperMain$MyWatcher@1175e2db
        2020-07-21 09:48:16,603 [myid:] - INFO  [main:X509Util@77] - Setting -D jdk.tls.rejectClientInitiatedRenegotiation=true to disable client-initiated TLS renegotiation
        2020-07-21 09:48:16,615 [myid:] - INFO  [main:ClientCnxnSocket@239] - jute.maxbuffer value is 1048575 Bytes
        2020-07-21 09:48:16,630 [myid:] - INFO  [main:ClientCnxn@1703] - zookeeper.request.timeout value is 0. feature enabled=false
        Welcome to ZooKeeper!
        2020-07-21 09:48:16,647 [myid:localhost:2181] - INFO  [main-SendThread(localhost:2181):ClientCnxn$SendThread@1154] - Opening socket connection to server localhost/0:0:0:0:0:0:0:1:2181.
        2020-07-21 09:48:16,647 [myid:localhost:2181] - INFO  [main-SendThread(localhost:2181):ClientCnxn$SendThread@1156] - SASL config status: Will not attempt to authenticate using SASL (unknown error)
        JLine support is enabled
        2020-07-21 09:48:16,754 [myid:localhost:2181] - INFO  [main-SendThread(localhost:2181):ClientCnxn$SendThread@986] - Socket connection established, initiating session, client: /0:0:0:0:0:0:0:1:37212, server: localhost/0:0:0:0:0:0:0:1:2181
        2020-07-21 09:48:16,793 [myid:localhost:2181] - INFO  [main-SendThread(localhost:2181):ClientCnxn$SendThread@1420] - Session establishment complete on server localhost/0:0:0:0:0:0:0:1:2181, session id = 0x1000020875b0004, negotiated timeout = 30000
        
        WATCHER::
        
        WatchedEvent state:SyncConnected type:None path:null
        [zk: localhost:2181,localhost2182,localhost:2183(CONNECTED) 0] ls /
        [zookeeper]
        [zk: localhost:2181,localhost2182,localhost:2183(CONNECTED) 1] 
        ```

# 4 操作Zoookeeper

## 4.1 shell客户端

使用`zkCli.sh –server <ip>`进入命令行工具。

根据提示命令进行操作：

- 使用 ls 命令来查看当前 ZooKeeper 中所包含的内容： `ls /`

- 创建了一个新的znode节点“ zk ”以及与它关联的字符串： `create /zk "myData"`

- 使用get命令来确认znode是否包含我们所创建的字符串： `get /zk`

- 监听节点的变化：

    - `get /zk watch`

    - 当另外一个客户端改变`/zk`时，它会打出下面的内容：

    - ```
        WATCHER::
        WatchedEvent state:SyncConnected type:NodeDataChanged path:/zk
        ```

- 通过 set 命令来对 zk 所关联的字符串进行设置： `set /zk "zsl"`

- 删除节点：

    - `delete /zk`
    - `rmr /zk`
    - 删除节点命令，rmr命令与delete命令不同的是delete不可删除有子节点的节点，但是rmr命令可以删除，注意路径为绝对路径。

可以看到zookeeper集群的数据一致性

创建节点有俩种类型：短暂（ephemeral）持久（persistent）

## 4.2 zookeeper-java

`org.apache.zookeeper.Zookeeper`是客户端入口主类，负责建立与server的会话。其主要方法如下：

|            方法 | 描述                              |
| --------------: | :-------------------------------- |
|          create | 在本地目录树中创建一个节点        |
|          delete | 删除一个节点                      |
|          exists | 测试本地是否存在目标节点          |
| getData/setData | 从目标节点上读取 / 写数据         |
|   getACL/setACL | 获取/设置目标节点访问控制列表信息 |
|     getChildren | 检索一个子节点上的列表            |
|            sync | 等待要被传送的数据                |

### 4.2.1 需要的jar包

- `zookeeper-3.6.1.jar`
- `zookeeper-jute-3.6.1.jar`
- `log4j-1.2.17.jar`
- `slf4j-api-1.7.25.jar`
- `slf4j-log4j12-1.7.25.jar`

### 4.2.2 增删改查

```java
package com.lifeng.zookeeper;

import org.apache.zookeeper.*;

import java.io.IOException;

public class Demo {
    // 会话超时时间，设置为与系统默认时间一致
    private static final int SESSION_TIMEOUT = 30000;
    // 创建 ZooKeeper 实例
    ZooKeeper zk;
    // 创建 Watcher 实例
    Watcher watcher = new Watcher() {
        public void process(WatchedEvent event) {
            System.out.println(event.toString());
        }
    };

    // 初始化 ZooKeeper 实例
    private void createZKInstance() throws IOException {
        //连接集群
        //zk = new ZooKeeper("localhost:2181,localhost2182,localhost:2183", Demo.SESSION_TIMEOUT, this.watcher);
        //连接单机
        zk = new ZooKeeper("localhost:2181", Demo.SESSION_TIMEOUT, this.watcher);
    }

    private void zkOperations() throws IOException, InterruptedException, KeeperException {
        System.out.println("1. 创建 ZooKeeper 节点 (znode ： zoo2, 数据： myData2 ，权限： OPEN_ACL_UNSAFE ，节点类型： Persistent");
        zk.create("/zoo2", "myData2".getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
        System.out.println("2. 查看是否创建成功： ");
        System.out.println(new String(zk.getData("/zoo2", false, null)));
        System.out.println("3. 修改节点数据 ");
        zk.setData("/zoo2", "zhishan".getBytes(), -1);
        System.out.println("4. 查看是否修改成功： ");
        System.out.println(new String(zk.getData("/zoo2", false, null)));
        System.out.println("5. 删除节点 ");
        zk.delete("/zoo2", -1);
        System.out.println("6. 查看节点是否被删除： ");
        System.out.println(" 节点状态： [" + zk.exists("/zoo2", false) + "]");
    }

    private void zkClose() throws InterruptedException {
        zk.close();
    }

    public static void main(String[] args) throws IOException, InterruptedException, KeeperException {
        Demo demo = new Demo();
        demo.createZKInstance();
        demo.zkOperations();
        demo.zkClose();
    }
}
```

问题：

- 在连接集群版的时候报如下错误：

    - ```
        log4j:WARN No appenders could be found for logger (org.apache.zookeeper.ZooKeeper).
        log4j:WARN Please initialize the log4j system properly.
        log4j:WARN See http://logging.apache.org/log4j/1.2/faq.html#noconfig for more info.
        1. 创建 ZooKeeper 节点 (znode ： zoo2, 数据： myData2 ，权限： OPEN_ACL_UNSAFE ，节点类型： Persistent
        Exception in thread "main" org.apache.zookeeper.KeeperException$ConnectionLossException: KeeperErrorCode = ConnectionLoss for /zoo2
        	at org.apache.zookeeper.KeeperException.create(KeeperException.java:102)
        	at org.apache.zookeeper.KeeperException.create(KeeperException.java:54)
        	at org.apache.zookeeper.ZooKeeper.create(ZooKeeper.java:1733)
        	at com.lifeng.zookeeper.Demo.zkOperations(Demo.java:29)
        	at com.lifeng.zookeeper.Demo.main(Demo.java:49)
        ```

    - 解决方案：把超时时间改的大一点，这里把`private static final int SESSION_TIMEOUT = 30000;`改为`private static final int SESSION_TIMEOUT = 50000;`即可解决问题。

### 4.2.3 Zookeeper的监听器工作机制

监听器是一个接口，我们的代码中可以实现Wather这个接口，实现其中的process方法，方法中即我们自己的业务逻辑监听器的注册是在获取数据的操作中实现： 

- `byte[] getData(String path, Watcher watcher, Stat stat)`：监听的事件是节点数据变化事件
- `List<String> getChildren(String path, Watcher watcher)`：监听的事件是节点下的子节点增减变化事件

### 4.2.4 应用：实现分布式应用的(主节点HA)及客户端动态更新主节点状态

描述：

- 某分布式系统中，主节点可以有多台，可以动态上下线
- 任意一台客户端都能实时感知到主节点服务器的上下线

![](https://zhishan-zh.github.io/media/zookeeper_20200721111012.png)

服务端代码：

```java
package com.lifeng.zookeeper.demo;

import org.apache.zookeeper.*;

public class AppServer {
    private String groupNode = "myserver";
    private String subNode = "sub";

    /**
     * 连接zookeeper
     *
     * @param address server的地址
     */
    public void connectZookeeper(String address) throws Exception {
        ZooKeeper zk = new ZooKeeper("localhost:2181,localhost2182,localhost:2183", 50000, new Watcher() {
            public void process(WatchedEvent event) {
                // 不做处理
            }
        });
        // 在"/myserver"下创建子节点
        // 子节点的类型设置为EPHEMERAL_SEQUENTIAL, 表明这是一个临时节点, 且在子节点的名称后面加上一串数字后缀
        // 将server的地址数据关联到新创建的子节点上
        String createdPath = zk.create("/" + groupNode + "/" + subNode, address.getBytes("utf-8"),
                ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL_SEQUENTIAL);
        System.out.println("create: " + createdPath);
    }

    /**
     * server的工作逻辑写在这个方法中
     * 此处不做任何处理, 只让server sleep
     */
    public void handle() throws InterruptedException {
        Thread.sleep(Long.MAX_VALUE);
    }

    public static void main(String[] args) throws Exception {
        AppServer as = new AppServer();
        as.connectZookeeper("server1");
        as.handle();
    }
}
```

- 报错：

    - ```
        Exception in thread "main" org.apache.zookeeper.KeeperException$NoNodeException: KeeperErrorCode = NoNode for /myserver/sub
        	at org.apache.zookeeper.KeeperException.create(KeeperException.java:118)
        	at org.apache.zookeeper.KeeperException.create(KeeperException.java:54)
        	at org.apache.zookeeper.ZooKeeper.create(ZooKeeper.java:1733)
        	at com.lifeng.zookeeper.demo.AppServer.connectZookeeper(AppServer.java:23)
        	at com.lifeng.zookeeper.demo.AppServer.main(AppServer.java:38)
        ```

    - 原因是缺少上级节点`/myserver`，解决访问是先创建节点`/myserver`，在创建节点`/myserver/sub`。

客户端：

```java
package com.lifeng.zookeeper.demo;

import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;

import java.util.ArrayList;
import java.util.List;

public class AppClient {
    private String groupNode = "myserver";
    private ZooKeeper zk;
    private Stat stat = new Stat();
    private volatile List<String> serverList;

    /**
     * 连接zookeeper
     */
    public void connectZookeeper() throws Exception {
        zk = new ZooKeeper("localhost:2181,localhost2182,localhost:2183", 50000, new Watcher() {
            public void process(WatchedEvent event) {
                // 如果发生了"/myserver"节点下的子节点变化事件, 更新server列表, 并重新注册监听
                if (event.getType() == Event.EventType.NodeChildrenChanged
                        && ("/" + groupNode).equals(event.getPath())) {
                    try {
                        updateServerList();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        });

        updateServerList();
    }

    /**
     * 更新server列表
     */
    private void updateServerList() throws Exception {
        List<String> newServerList = new ArrayList<>();

        // 获取并监听groupNode的子节点变化
        // watch参数为true, 表示监听子节点变化事件.
        // 每次都需要重新注册监听, 因为一次注册, 只能监听一次事件, 如果还想继续保持监听, 必须重新注册
        List<String> subList = zk.getChildren("/" + groupNode, true);
        for (String subNode : subList) {
            // 获取每个子节点下关联的server地址
            byte[] data = zk.getData("/" + groupNode + "/" + subNode, false, stat);
            newServerList.add(new String(data, "utf-8"));
        }

        // 替换server列表
        serverList = newServerList;
        System.out.println("server list updated: " + serverList);
    }

    /**
     * client的工作逻辑写在这个方法中
     * 此处不做任何处理, 只让client sleep
     */
    public void handle() throws InterruptedException {
        Thread.sleep(Long.MAX_VALUE);
    }

    public static void main(String[] args) throws Exception {
        AppClient ac = new AppClient();
        ac.connectZookeeper();
        ac.handle();
    }
}
```

### 4.2.5 应用：分布式共享锁的简单实现

代码1：

```java
package com.lifeng.zookeeper.distributedlock;

import org.apache.zookeeper.*;
import org.apache.zookeeper.data.Stat;

import java.util.Collections;
import java.util.List;
import java.util.concurrent.CountDownLatch;

public class DistributedClient {
    // 超时时间
    private static final int SESSION_TIMEOUT = 5000;
    // zookeeper server列表
    private String hosts = "localhost:2181,localhost2182,localhost:2183";
    private String groupNode = "locks";
    private String subNode = "sub";

    private ZooKeeper zk;
    // 当前client创建的子节点
    private String thisPath;
    // 当前client等待的子节点
    private String waitPath;

    private CountDownLatch latch = new CountDownLatch(1);

    /**
     * 连接zookeeper
     */
    public void connectZookeeper() throws Exception {
        zk = new ZooKeeper(hosts, SESSION_TIMEOUT, new Watcher() {
            public void process(WatchedEvent event) {
                try {
                    // 连接建立时, 打开latch, 唤醒wait在该latch上的线程
                    if (event.getState() == Event.KeeperState.SyncConnected) {
                        latch.countDown();
                    }

                    // 发生了waitPath的删除事件
                    if (event.getType() == Event.EventType.NodeDeleted && event.getPath().equals(waitPath)) {
                        doSomething();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        // 等待连接建立
        latch.await();

        // 创建子节点
        thisPath = zk.create("/" + groupNode + "/" + subNode, null, ZooDefs.Ids.OPEN_ACL_UNSAFE,
                CreateMode.EPHEMERAL_SEQUENTIAL);

        // wait一小会, 让结果更清晰一些
        Thread.sleep(10);

        // 注意, 没有必要监听"/locks"的子节点的变化情况
        List<String> childrenNodes = zk.getChildren("/" + groupNode, false);

        // 列表中只有一个子节点, 那肯定就是thisPath, 说明client获得锁
        if (childrenNodes.size() == 1) {
            doSomething();
        } else {
            String thisNode = thisPath.substring(("/" + groupNode + "/").length());
            // 排序
            Collections.sort(childrenNodes);
            int index = childrenNodes.indexOf(thisNode);
            if (index == -1) {
                // never happened
            } else if (index == 0) {
                // inddx == 0, 说明thisNode在列表中最小, 当前client获得锁
                doSomething();
            } else {
                // 获得排名比thisPath前1位的节点
                this.waitPath = "/" + groupNode + "/" + childrenNodes.get(index - 1);
                // 在waitPath上注册监听器, 当waitPath被删除时, zookeeper会回调监听器的process方法
                zk.getData(waitPath, true, new Stat());
            }
        }
    }

    private void doSomething() throws Exception {
        try {
            System.out.println("gain lock: " + thisPath);
            Thread.sleep(2000);
            // do something
        } finally {
            System.out.println("finished: " + thisPath);
            // 将thisPath删除, 监听thisPath的client将获得通知
            // 相当于释放锁
            zk.delete(this.thisPath, -1);
        }
    }

    public static void main(String[] args) throws Exception {
        for (int i = 0; i < 10; i++) {
            new Thread() {
                public void run() {
                    try {
                        DistributedClient dl = new DistributedClient();
                        dl.connectZookeeper();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }.start();
        }

        Thread.sleep(Long.MAX_VALUE);
    }
}
```

代码2:

```java
package com.lifeng.zookeeper.distributedlock;

import org.apache.zookeeper.*;

import java.util.Collections;
import java.util.List;
import java.util.Random;

public class DistributedClientMy {
    // 超时时间
    private static final int SESSION_TIMEOUT = 5000;
    // zookeeper server列表
    private String hosts = "localhost:2181,localhost2182,localhost:2183";
    private String groupNode = "locks";
    private String subNode = "sub";
    private boolean haveLock = false;

    private ZooKeeper zk;
    // 当前client创建的子节点
    private volatile String thisPath;

    /**
     * 连接zookeeper
     */
    public void connectZookeeper() throws Exception {
        zk = new ZooKeeper(hosts, SESSION_TIMEOUT, new Watcher() {
            public void process(WatchedEvent event) {
                try {
                    // 子节点发生变化
                    if (event.getType() == Watcher.Event.EventType.NodeChildrenChanged && event.getPath().equals("/" + groupNode)) {
                        // thisPath是否是列表中的最小节点
                        List<String> childrenNodes = zk.getChildren("/" + groupNode, true);
                        String thisNode = thisPath.substring(("/" + groupNode + "/").length());
                        // 排序
                        Collections.sort(childrenNodes);
                        if (childrenNodes.indexOf(thisNode) == 0) {
                            doSomething();
                            thisPath = zk.create("/" + groupNode + "/" + subNode, null, ZooDefs.Ids.OPEN_ACL_UNSAFE,
                                    CreateMode.EPHEMERAL_SEQUENTIAL);
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        // 创建子节点
        thisPath = zk.create("/" + groupNode + "/" + subNode, null, ZooDefs.Ids.OPEN_ACL_UNSAFE,
                CreateMode.EPHEMERAL_SEQUENTIAL);

        // wait一小会, 让结果更清晰一些
        Thread.sleep(new Random().nextInt(1000));

        // 监听子节点的变化
        List<String> childrenNodes = zk.getChildren("/" + groupNode, true);

        // 列表中只有一个子节点, 那肯定就是thisPath, 说明client获得锁
        if (childrenNodes.size() == 1) {
            doSomething();
            thisPath = zk.create("/" + groupNode + "/" + subNode, null, ZooDefs.Ids.OPEN_ACL_UNSAFE,
                    CreateMode.EPHEMERAL_SEQUENTIAL);
        }
    }

    /**
     * 共享资源的访问逻辑写在这个方法中
     */
    private void doSomething() throws Exception {
        try {
            System.out.println("gain lock: " + thisPath);
            Thread.sleep(2000);
            // do something
        } finally {
            System.out.println("finished: " + thisPath);
            // 将thisPath删除, 监听thisPath的client将获得通知
            // 相当于释放锁
            zk.delete(this.thisPath, -1);
        }
    }

    public static void main(String[] args) throws Exception {
        DistributedClientMy dl = new DistributedClientMy();
        dl.connectZookeeper();
        Thread.sleep(Long.MAX_VALUE);
    }
}
```

