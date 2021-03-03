# ZAB原子消息广播协议

ZooKeeper为高可用的一致性协调框架，使用ZAB（ZooKeeper Atomic Broadcast ）原子消息广播协议作为数据一致性的算法。

ZAB可以说是在Paxos算法基础上进行了扩展改造而来的，ZAB协议设计了支持崩溃恢复，ZooKeeper使用单一主进程Leader用于处理客户端所有事务请求，采用ZAB协议将服务器数状态以事务形式广播到所有Follower上；由于事务间可能存在着依赖关系，ZAB协议保证Leader广播的变更序列被顺序的处理：一个状态被处理那么它所依赖的状态也已经提前被处理；ZAB协议支持的崩溃恢复可以保证在Leader进程崩溃的时候可以重新选出Leader并且保证数据的完整性；

在ZooKeeper中所有的事务请求都由一个主服务器也就是Leader来处理，其他服务器为Follower，Leader将客户端的事务请求转换为事务Proposal，并且将Proposal分发给集群中其他所有的Follower，然后Leader等待Follwer反馈，当有过半数（>=N/2+1）的Follower反馈信息后，Leader将再次向集群内Follower广播Commit信息，Commit为将之前的Proposal提交；

# 1 Paxos 算法

## 1.1 概述

Paxos算法是Lamport提出的一种基于消息传递的分布式一致性算法。Paxos 算法解决的问题是一个分布式系统如何就某个值（决议）达成一致。

共识(Consensus)是多个节点就某个提案(n, v)达成统一结果的过程。因为参与者本身会失败，或者参与者之间的通信会失败，比如网络分区，消息延迟，节点故障，所以这是个棘手的问题。

一个典型的场景是，在一个分布式数据库系统中，如果各节点的初始状态一致，每个节点执行相同的操作序列，那么他们最后能得到一个一致的状态。为保证每个节点执行相同的命令序列，需要在每一条指令上执行一个“一致性算法”以保证每个节点看到的指令一致。一个通用的一致性算法可以应用在许多场景中，是分布式计算中的重要问题。节点通信存在两种模型：共享内存（Shared memory）和消息传递（Messages passing）。Paxos 算法就是一种基于消息传递模型的一致性算法。

不仅仅是分布式系统中，凡是多个过程需要达成某种一致的场合都可以使用Paxos 算法。一致性算法可以通过共享内存（需要锁）或者消息传递实现，Paxos 算法采用的是后者。

Paxos 算法适用的几种情况：

- 一台机器中多个进程/线程达成数据一致；
- 分布式文件系统或者分布式数据库中多客户端并发读写数据；
- 分布式存储中多个副本响应读写请求的一致性。

## 1.2 拜占庭问题

拜占庭将军问题：是指拜占庭帝国军队的将军们必须全体一致的决定是否攻击某一支敌军。问题是这些将军在地理上是分隔开来的，只能依靠通讯员进行传递命令，但是通讯员中存在叛徒，它们可以篡改消息，叛徒可以欺骗某些将军采取进攻行动；促成一个不是所有将军都同意的决定，如当将军们不希望进攻时促成进攻行动；或者迷惑某些将军，使他们无法做出决定。
Paxos算法的前提假设是不存在拜占庭将军问题，即：信道是安全的（信道可靠），发出的信号不会被篡改，因为Paxos算法是基于消息传递的。此问题由Lamport提出，它也是 Paxos算法的提出者。
从理论上来说，在分布式计算领域，试图在异步系统和不可靠信道上来达到一致性状态是不可能的。因此在对一致性的研究过程中，都往往假设信道是可靠的，而事实上，大多数系统都是部署在一个局域网中，因此消息被篡改的情况很罕见；另一方面，由于硬件和网络原因而造成的消息不完整问题，只需要一套简单的校验算法即可。因此，在实际工程中，可以假设所有的消息都是完整的，也就是没有被篡改。

## 1.3 Basic Paxos

就单个值达成共识，如果大多数节点就**单个值**达成共识，值就不会再变了。不涉及连续多个值的共识协商。

### 1.3.1 角色

- **客户端(Client)**：向分布式系统发送请求，并接收回复。
- **提议者(Proposer)**：接受客户端的一个请求并支持该请求，之后尝试让其他接受者支持相同的请求。 
  - 接入和协调功能，收到客户端请求后，发起 二阶段提交 ，进行共识协商
- **接受者(Acceptor)**：对提案进行投票，存储接受的提案。
- **学习者(Learner)**：不参与投票，在接受者达成共识之后，存储保存。 

一个节点可以同时扮演多个角色，不影响算法正确性，一个节点扮演多个角色可以降低延迟，减少节点间消息发送

### 1.3.2 提案

提案的形式：`(n, v)`

- n为提案编号
  - 提案编号特性：原子，递增，持久存储
- v为提案值

### 1.3.3 Quorum

本义指的是出席议会议事的最低议员数量。 在Paxos中，接受者组成Quorums。发送给某一个接受者的消息必须发送给Quorum中的所有其他接受者。

### 1.3.4 二阶段提交

- **准备（Prepare）阶段**

  - **Prepare**：提议者(Proposer)创建一个提案(n, v)，发起二阶段提交, n必须是递增的。将Prepare message(只包含提案编号n，不需要包含v)发给a quorum of acceptors

  - **Promise**：接受者比较n和自己已经响应的提案的最大提案编号：

    - 如果小于等于已经响应的最大提案编号，则忽略，可以不响应，也可以响应以防止提议者反复提交提案编号为n的Prepare message。    

    - 如果大于已经响应的所有Prepare请求的最大提案编号，接受者返回给提议者Promise，并忽略所有提案编号小于n的提案；
    - 如果接受者之前接受了某个提案(m, w)，则接受者必须将这个提案信息返回给提议者。

- **接受（Accept）阶段**

  - **Accept**：
    - 如果接受者已经达成共识(m, w)，则Accept message为(n, w) 
      - 提案值不变为w，提案编号变为n
    - 如果提议者接收到a quorum of acceptors中大多数节点的Promises，会设置节点值为提案值v，提议者发送Accept message(n, v)
  - **Accepted**：
    - 接受者之前尚未达成共识，Accept message(n, v) 
    - 接受者之前已达成共识(m, w), Accept message(n, w)
      - 提案值不变为w，提案编号变为n
      - 如果大多数接受者对某个提案达成共识，那么提案值就不会再变了，而提案编号会因为少数节点(尚未通过任何提案)接收到新的准备请求而使用递增的更大的提案编号。

### 1.3.5 学习者(Learner)怎么学习被选定的value

- 方案一：接受者(Acceptor)接收一个提案，就将该提案发送给所有Learner
  - 优点：Learner能快速获取被选定的value
  - 缺点：通信的次数为（M*N）
- 方案二：接受者(Acceptor)接受了一个提案，就将该提案发送给主Learner，主Learner再通知其他Learner。
  - 优点：通信次数为M+N-1
  - 缺点：单点故障问题，主Learner可能出现故障
- 方案三：接受者(Acceptor)接受了一个提案，就将该提案发送给一个Learner集合，Learner集合再通知其他Learner。
  - 优点：集合中Learner个数越多，可靠性越好
  - 缺点：网络通信复杂度越高

### 1.3.6 如何保证Paxos算法的活性

**无法保障活性**的问题：在算法运行过程中，可能还会存在一种极端情况，当有两个proposer**依次提出**一系列编号递增的议案，那么会陷入**死循环**，无法完成第二阶段，也就是无法选定一个提案。

> - Proposer1发出编号为M1的Prepare请求，受到过半响应，完成了阶段一（Prepare阶段）的流程。
>   - 同时，Proposer2发出编号为M2（M2 > M1）的Prepare请求，也受到过半响应，也完成了阶段一的流程。于是Acceptor承若不再接受编号小于M2的提案。
> - Proposer1进入第二个阶段的时候，发出的Accept请求被Acceptor忽略，于是Proposer1再次进入阶段以并发出编号为M3（M3 > M2）的Prepare的请求。
>   - 这又导致Proposer2再阶段二Accept请求被忽略。于是Proposer2再次进入阶段一，发出编号为M4（M4 > M3）的Prepare请求...
> - .....（陷入死循环，都无法完成阶段二，没有value被选定。）

解决方案：**选取一个主Proposer，只有主Proposer才能提出提案。**

问题：如果主Proposer挂掉怎么办？可以使用心跳检测来解决这个问题。

## 1.4 Multi-Paxos

# 2 ZAB原子广播协议

ZAB（ZooKeeper Atomic Broadcast ）原子消息广播协议是专门为Zookeeper实现分布式协调功能而设计。Zookeeper主要是根据ZAB协议是实现分布式系统数据一致性。

Zookeeper根据ZAB协议建立了主备模型完成Zookeeper集群中数据的同步。这里所说的主备系统架构模型是指，在Zookeeper集群中，只有一台leader负责处理外部客户端的事物请求(或写操作)，然后leader服务器将客户端的写操作数据同步到所有的follower节点中。

ZAB的协议核心是在整个Zookeeper集群中只有一个节点即Leader将客户端的写操作转化为事物(或提议proposal)。Leader节点在数据写完之后，将向所有的follower节点发送数据广播请求(或数据复制)，等待所有的follower节点反馈。在ZAB协议中，只要超过半数follower节点反馈OK，Leader节点就会向所有的follower服务器发送commit消息。即将leader节点上的数据同步到follower节点之上。

## 2.1 基本概念

- serverId：服务器ID 即 myid
  - 比如有三台服务器，编号分别是1,2,3。
  - 编号越大在选择算法中的权重越大。

- zxid：最新的事物ID 既 LastLoggedZxid
  - 服务器中存放的最大数据ID。
  - ID值越大说明数据越新，在选举算法中数据越新权重越大。

- epoch：逻辑时钟 既 PeerEpoch
  - 每个服务器都会给自己投票，或者叫投票次数，同一轮投票过程中的逻辑时钟值是相同的。
  - 每投完一次票这个数据就会增加，然后与接收到的其它服务器返回的投票信息中的数值相比。
  - 如果收到低于当前轮次的投票结果，该投票无效，需更新到当前轮次和当前的投票结果。

## 2.1 协议状态

- LOOKING：不确定Leader的“寻找”状态，即当前节点认为集群中没有Leader，进而发起选举；
- LEADING：“领导”状态，即当前节点就是Leader，并维护与Follower和Observer的通信；
- FOLLOWING：“跟随”状态，即当前节点是Follower，且正在保持与Leader的通信；
- OBSERVING：“观察”状态，即当前节点是Observer，且正在保持与Leader的通信，但是不参与Leader选举。

ZooKeeper启动时所有节点初始状态为Looking，这时集群会尝试选举出一个Leader节点，选举出的Leader节点切换为Leading状态；当节点发现集群中已经选举出Leader则该节点会切换到Following状态，然后和Leader节点保持同步；当Follower节点与Leader失去联系时Follower节点则会切换到Looking状态，开始新一轮选举；在ZooKeeper的整个生命周期中每个节点都会在Looking、Following、Leading状态间不断转换；

选举出Leader节点后ZAB进入原子广播阶段，这时Leader为和自己同步的每个节点Follower创建一个操作序列，一个时期一个Follower只能和一个Leader保持同步，Leader节点与Follower节点使用心跳检测来感知对方的存在；当Leader节点在超时时间内收到来自Follower的心跳检测那Follower节点会一直与该节点保持连接；若超时时间内Leader没有接收到来自过半Follower节点的心跳检测或TCP连接断开，那Leader会结束当前周期的领导，切换到Looking状态，所有Follower节点也会放弃该Leader节点切换到Looking状态，然后开始新一轮选举；

## 2.2 算法阶段

ZAB协议定义了选举（election）、发现（discovery）、同步（sync）、广播(Broadcast)四个阶段。ZAB选举（election）时当Follower存在ZXID（事务ID）时判断所有Follower节点的事务日志，只有lastZXID的节点才有资格成为Leader，这种情况下选举出来的Leader总有最新的事务日志，基于这个原因所以ZooKeeper实现的时候把发现（discovery）与同步（sync）合并为恢复（recovery）阶段；

ZAB协议中使用ZXID作为事务编号，ZXID为64位数字，低32位为一个递增的计数器，每一个客户端的一个事务请求时Leader产生新的事务后该计数器都会加1，高32位为Leader周期epoch编号，当新选举出一个Leader节点时Leader会取出本地日志中最大事务Proposal的ZXID解析出对应的epoch把该值加1作为新的epoch，将低32位从0开始生成新的ZXID；ZAB使用epoch来区分不同的Leader周期。

- Election：在Looking状态中选举出Leader节点，Leader的lastZXID总是最新的；

- Discovery：Follower节点向准Leader推送FOllOWERINFO，该信息中包含了上一周期的epoch，接受准Leader的NEWLEADER指令，检查newEpoch有效性，准Leader要确保Follower的epoch与ZXID小于或等于自身的；

- sync：将Follower与Leader的数据进行同步，由Leader发起同步指令，最终保持集群数据的一致性；

- Broadcast：Leader广播Proposal与Commit，Follower接受Proposal与Commit；

- Recovery：在Election阶段选举出Leader后本阶段主要工作就是进行数据的同步，使Leader具有highestZXID，集群保持数据的一致性；

### 2.2.1 选举（Election）

Election阶段必须确保选出的Leader具有highestZXID，否则在Recovery阶段没法保证数据的一致性，Recovery阶段Leader要求Follower向自己同步数据没有Follower要求Leader保持数据同步，所有选举出来的Leader要具有最新的ZXID；

在选举的过程中会对每个Follower节点的ZXID进行对比只有highestZXID的Follower才可能当选Leader；



- electionEpoch：“选民”的选举轮次，在每个节点中以逻辑时钟logicalclock的形式存储。每发起一轮新的选举，该值会加1。若节点重启，此值会归零。
- sid：“选民”自己的服务器ID，是一个正整数，由各个ZK实例中的$dataDir/myid指定。
- state：“选民”的状态。
- votedLeaderSid：这一票推选的“候选人”的服务器ID。在代码中直接命名为leader，为了防止混淆，这里稍作更改。
- votedLeaderZxid：这一票推选的“候选人”的事务ID。所谓事务ID即写操作的proposal ID，其高32位是Leader纪元值，低32位是当前Leader纪元下的操作序号，亦即zxid肯定是单调递增的。在代码中直接命名为zxid，为了防止混淆，这里稍作更改。
- recvset：“选民”的票箱，其中存储有自己的和其他节点的选票。注意，每张选票都包含上述的electionEpoch、sid、state、leader和zxid信息，并且票箱中都只会记录每个“选民”的最近一次投票信息。



选举流程：

　　1. 每个Follower都向其他节点发送选自身为Leader的Vote投票请求，等待回复；
　　2. Follower接受到的Vote如果比自身的大（ZXID更新）时则投票，并更新自身的Vote，否则拒绝投票；
　　3. 每个Follower中维护着一个投票记录表，当某个节点收到过半的投票时，结束投票并把该Follower选为Leader，投票结束；

