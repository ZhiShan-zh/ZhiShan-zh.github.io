# HDFS

# 1 HDFS基础

Hadoop Distributed File System，简称HDFS，是一个分布式文件系统。

## 1.1 设计思想

分而治之：将大文件、大批量文件，分布式存放在大量服务器上，以便于采取分而治之的方式对海量数据进行运算分析。

## 1.2 在大数据系统中作用

为各类分布式运算框架（如：mapreduce，spark，tez，……）提供数据存储服务

## 1.3 体系结构

HDFS采用了主从（Master/Slave）结构模型，一个HDFS集群是由一个NameNode和若干个DataNode组成的。其中NameNode作为主服务器，管理文件系统的命名空间和客户端对文件的访问操作；集群中的DataNode管理存储的数据。

## 1.4 概念和特性

**HDFS是一个文件系统**，用于存储文件，**通过统一的命名空间——目录树来定位文件**；

**HDFS是分布式的**，由很多服务器联合起来实现其功能，集群中的服务器有各自的角色；



**重要特性**：

- HDFS中的文件在物理上是**分块存储（block）**，块的大小可以通过配置参数`dfs.blocksize`来规定，默认大小在hadoop2.x版本中是128M，老版本中是64M

- HDFS文件系统会给客户端**提供一个统一的抽象目录树**，客户端通过路径来访问文件，形如：`hdfs://namenode:port/dir-a/dir-b/dir-c/file.data`

- NameNode节点：负责目录结构及文件分块信息（元数据）的管理
  - NameNode是HDFS集群主节点，负责维护整个HDFS文件系统的目录树，以及每一个路径（文件）所对应的block块信息（block的id，及所在的DataNode服务器）

- DataNode节点：负责文件的各个block的存储管理
  - DataNode是HDFS集群从节点，每一个block都可以在多个datanode上存储多个副本
  - 副本数量也可以通过参数设置`dfs.replication`

- HDFS是设计成**适合一次写入，多次读出的场景**，且不支持文件的修改
  - 注：适合用来做数据分析，并不适合用来做网盘应用，因为，不便修改，延迟大，网络开销大，成本太高

# 2 HDFS基本操作——shell

## 2.1 HDFS命令行客户端的基本使用

**HDFS命令的基本使用方法**：`hadoop fs -hdfs提供的命令 参数列表`

例如：

```shell
[root@0fe37eebc9fb ~]# hadoop fs -ls /
Found 2 items
drwx------   - root supergroup          0 2020-10-16 12:41 /tmp
drwxr-xr-x   - root supergroup          0 2020-10-16 12:41 /wordcount
```

## 2.2 常用命令参数介绍

- `-help`：输出这个命令参数手册

- `-ls`：显示目录信息

  ```shell
  [root@0fe37eebc9fb ~]# hadoop fs -ls hdfs://hdp-node-01:9000/
  Found 2 items
  drwx------   - root supergroup          0 2020-10-16 12:41 hdfs://hdp-node-01:9000/tmp
  drwxr-xr-x   - root supergroup          0 2020-10-16 12:41 hdfs://hdp-node-01:9000/wordcount
  
  # 简写命令
  [root@0fe37eebc9fb ~]# hadoop fs -ls /
  Found 2 items
  drwx------   - root supergroup          0 2020-10-16 12:41 /tmp
  drwxr-xr-x   - root supergroup          0 2020-10-16 12:41 /wordcount
  ```

- `-mkdir`：在hdfs上创建目录

  - `-p`：子命令，可以迭代创建目录

    ```shell
    [root@0fe37eebc9fb ~]# hadoop fs -ls /
    Found 2 items
    drwx------   - root supergroup          0 2020-10-16 12:41 /tmp
    drwxr-xr-x   - root supergroup          0 2020-10-16 12:41 /wordcount
    
    [root@0fe37eebc9fb ~]# hadoop fs  -mkdir  -p  /aaa/bbb/cc/dd
    [root@0fe37eebc9fb ~]# hadoop fs -ls /
    Found 3 items
    drwxr-xr-x   - root supergroup          0 2020-10-16 13:12 /aaa
    drwx------   - root supergroup          0 2020-10-16 12:41 /tmp
    drwxr-xr-x   - root supergroup          0 2020-10-16 12:41 /wordcount
    
    [root@0fe37eebc9fb ~]# hadoop fs -ls /aaa/bbb/cc
    Found 1 items
    drwxr-xr-x   - root supergroup          0 2020-10-16 13:12 /aaa/bbb/cc/dd
    ```

- `-moveFromLocal`：从本地剪切粘贴到hdfs

  ```shell
  [root@0fe37eebc9fb ~]# ls
  a.txt  anaconda-ks.cfg  apps  run.sh
  [root@0fe37eebc9fb ~]# hadoop fs -moveFromLocal a.txt /aaa/bbb/cc/dd
  [root@0fe37eebc9fb ~]# hadoop fs -ls /aaa/bbb/cc/dd
  Found 1 items
  -rw-r--r--   2 root supergroup         11 2020-10-16 13:16 /aaa/bbb/cc/dd/a.txt
  ```

- `-copyFromLocal`和`-put`：从本地文件系统中拷贝文件到hdfs路径去

  ```shell
  #创建一个测试文件，随便输入一些内容
  [root@0fe37eebc9fb apps]# vi testCopyFromLocalFile.text
  [root@0fe37eebc9fb apps]# ls
  hadoop-2.9.2  hadoop-2.9.2.tar.gz  jdk-8u251-linux-x64.tar.gz  jdk1.8.0_251  testCopyFromLocalFile.text
  # 把本地文件上传到hdfs根路径下
  [root@0fe37eebc9fb apps]# hadoop fs -copyFromLocal testCopyFromLocalFile.text /
  #测试上传文件情况
  [root@0fe37eebc9fb apps]# hadoop fs -ls /
  Found 4 items
  drwxr-xr-x   - root supergroup          0 2020-10-16 13:12 /aaa
  -rw-r--r--   2 root supergroup         28 2020-10-19 10:01 /testCopyFromLocalFile.text
  drwx------   - root supergroup          0 2020-10-16 12:41 /tmp
  ```

- `-rm`：删除文件或文件夹

  - `-r`：子命令，可以迭代删除目录和文件

  ```shell
  [root@0fe37eebc9fb ~]# hadoop fs -mkdir -p /bbb/a/b
  [root@0fe37eebc9fb ~]# hadoop fs -ls /bbb/a
  Found 1 items
  drwxr-xr-x   - root supergroup          0 2020-10-19 11:42 /bbb/a/b
  [root@0fe37eebc9fb ~]# hadoop fs -rm /bbb
  rm: `/bbb': Is a directory
  [root@0fe37eebc9fb ~]# hadoop fs -rm -r /bbb
  Deleted /bbb
  [root@0fe37eebc9fb ~]# hadoop fs -ls /
  Found 5 items
  drwxr-xr-x   - root supergroup          0 2020-10-19 11:35 /aaa
  -rw-r--r--   3 root supergroup          0 2020-10-19 11:38 /ccc
  -rw-r--r--   2 root supergroup         28 2020-10-19 10:01 /testCopyFromLocalFile.text
  drwx------   - root supergroup          0 2020-10-16 12:41 /tmp
  drwxr-xr-x   - root supergroup          0 2020-10-16 12:41 /wordcount
  ```

- `-`：

- `-`：

- `-`：

- `-`：

- `-`：

- `-`：

- `-`：

# 3 HDFS工作机制

HDFS集群分为两大角色：

- NameNode：负责管理整个文件系统的元数据
- DataNode：负责管理用户的文件数据块

文件会按照固定的大小（blocksize）切成若干块后分布式存储在若干台DataNode上

- 每一个文件块可以有多个副本，并存放在不同的DataNode上

- DataNode会定期向NameNode汇报自身所保存的文件block信息，而NameNode则会负责保持文件的副本数量

HDFS的内部工作机制对客户端保持透明，客户端请求访问HDFS都是通过向NameNode申请来进行



## 3.1 机架感知

**机架感知**：机器感知的作用就是告诉Hadoop集群中哪台机器位于哪个机架。

- 涉及到机架感知一般是在Hadoop 集群规模很大的情况，一般情况下Hadoop 的机架感知是没有被启用的。也就是说在通常情况下，HDFS在选择机器时是随机选择的，有的时候随机选择存储节点会影响性能，所以有的时候我们需要配置机架感知。

- 配置hadoop机架感知的功能需要在NameNode所在机器的`core-site.xml`配置文件中增加一个选项

  ```xml
  <property>
    <name>topology.script.file.name</name>
    <value>XXXX</value>
  </property>
  ```

  - 这个配置选项的value指定为一个可执行程序，通常为一个脚本，该脚本接受一个参数，输出一个值。接受的参数通常为某台DataNode机器的ip地址，而输出的值通常为该ip地址对应的DataNode所在的rack，例如”/rack1”。
  - NameNode启动时，会判断该配置选项是否为空，如果非空，则表示已经用机架感知的配置，此时NameNode会根据配置寻找该脚本，并在接收到每一个DataNode的heartbeat时，将该DataNode的ip地址作为参数传给该脚本运行，并将得到的输出作为该DataNode所属的机架，保存到内存的一个map中。

**机架感知下副本存储节点选择策略**：

- **策略概述**：一般情况，当复制因子为3时，HDFS的放置策略是将一个副本放在本地机架中的一个节点上，另一个放在本地机架中的另一个节点上，最后一个放在不同机架中的另一个节点上。
- **策略优势**：
  - 此策略减少机架间写入通信量，这通常会提高写入性能。
    - 机架故障的几率远小于节点故障的几率；此策略不会影响数据可靠性和可用性保证。但是，它确实减少了读取数据时使用的聚合网络带宽，因为块只放置在两个唯一的机架中，而不是三个机架中。
  - 此策略在不影响数据可靠性或读取性能的情况下提高写入性能。
    - 使用此策略，文件的副本不会均匀分布在机架上：三分之一的副本位于一个节点上，三分之二的副本位于一个机架上，另三分之一的副本均匀分布在其余机架上。

- **副本分布**：
  - 第一个副本在Client所处的节点上。如果客户端在集群外，随机选一个。
  - 第二个副本和第一个副本位于相同机架，随机节点。
  - 第三个副本位于不同机架，随机节点。

![](https://zhishan-zh.github.io/media/hadoop_hdfs_20201016163150.png)

## 3.2 网络拓扑–节点距离计算

在HDFS写数据的过程中，NameNode会选择距离待上传数据最近距离的DataNode接收数据。

**节点距离计算方法**：两个节点到达最近的共同祖先的距离总和

在配置好机架感知后，NameNode就可以画出如下图所示的DataNode 网络拓扑图，根据此图就可以进行节点距离的计算了，集群$c_1$、$c_2$和机架$r_1$、$r_2$、$r_3$、$r_4$、$r_5$、$r_6$对应的是交换机，节点$n_0$、$n_1$、$n_2$对应的是DataNode，那么集群$c_1$中的机架$r_1$中的节点$n_0$就可以表示为`/c1/r1/n0`，有了这些信息就可以计算出任意两台datanode之间的距离。

![](https://zhishan-zh.github.io/media/hadoop_hdfs_20201016172717.png)

距离计算示例：

- 同一 节点上的进程：Distance(/d1/r1/n0, /d1/r1/n0)=0

- 同一机架上的不同节点：Distamnce(/d1/r1/n1, /d1/r1/n2)=2 
  - 共同祖先r1，距离为1+1=2

- 同一数据中心不同机架上的节点：Distance(/d1/r2/n0, /d1/r3/n2)=4 
  - 共同祖先为c1，距离为1+1+1+1=4

- 不同数据中心的节点：Distance(d1/r2/n1, /d2/r4/n1)=6 

## 3.3 HDFS写数据流程

**客户端要向HDFS写数据**：

- 首先要跟NameNode通信以确认可以写文件并获得接收文件block的DataNode；
- 然后，客户端按顺序将文件逐个block传递给相应DataNode，并由接收到block的DataNode负责向其他DataNode复制block的副本。

![](https://zhishan-zh.github.io/media/hadoop_hdfs_20201016185700.png)

1. 客户端通过Distributed FileSystem模块向NameNode请求上传文件，NameNode检查目标文件是否已存在，父目录是否存在。

2. NameNode返回是否可以上传。

3. 客户端收到可以上传的响应后将目标文件进行切块（hadoop2.x默认块大小为128M），然后请求第一个Block块上传到哪几个DataNode服务器上。

4. NameNode首先会检测其保存的DataNode信息，确定该文件块存储在那些节点上然后响应给客户端一组DataNode节点信息，这里返回3个DataNode节点，分别为dn1、dn2、dn3。

5. 客户端收到那组DataNode节点信息后，首先就近与某台DataNode建立网络连接；通过FSDataOutputStream模块请求dn1上传数据，dn1收到请求会继续调用dn2，然后dn2调用dn3，将这个通信管道建立完成。

6. dn1、dn2、dn3逐级应答客户端。

7. 客户端开始往dn1上传第一个Block，以Packet为单位，DataNode收到数据后，首先会缓存起来；然后将缓存里数据保存一份到本地（序列化到磁盘中），一份发送到传输通道；让剩下的DataNode做备份，并不是写好一个块或一整个文件后才向后分发，每个DataNode写完一个块后，会返回确认信息。
   - 当客户机将数据写入HDFS文件时，其数据首先写入本地文件。假设HDFS文件的复制因子为3。当本地文件累积完整的用户数据块时，客户端从NameNode检索数据节点列表。此列表包含将承载该块副本的数据节点。然后，客户端将数据块刷新到第一个数据节点。第一个数据节点开始接收小部分的数据，将每个部分写入其本地存储库，并将该部分传输到列表中的第二个数据节点。第二个数据节点依次开始接收数据块的每个部分，将该部分写入其存储库，然后将该部分刷新到第三个数据节点。最后，第三个数据节点将数据写入其本地存储库。因此，数据节点可以从管道中的前一个节点接收数据，同时将数据转发到管道中的下一个节点。因此，数据是从一个数据节点到下一个数据节点的流水线。
8. 当一个Block传输完成之后，客户端再次请求NameNode上传第二个Block的服务器。（重复执行3-7步）。
9. 写完数据，关闭FSDataOutputStream模块,发送完成信号给NameNode。

## 3.4 HDFS读数据流程

客户端将要读取的文件路径发送给NameNode，NameNode获取文件的元信息（主要是block的存放位置信息）返回给客户端，客户端根据返回的信息找到相应DataNode逐个获取文件的block并在客户端本地进行数据追加合并从而获得整个文件。

![](https://zhishan-zh.github.io/media/hadoop_hdfs_20201016192000.png)

1. 客户端通过Distributed FileSystem向NameNode请求下载文件，NameNode通过查询元数据，找到文件块所在的DataNode地址，并将每个block的DataNode地址返回客户端。

2. 客户端拿到block的位置信息后，就近挑选一台DataNode，请求读取数据。3、4和5、6过程是并发运行的（因为在不同的节点），默认block有3个副本，所以每一个block只需要从一个副本读取就可以。客户端开发库会选取离客户端最接近的DataNode来读取block。

3 DataNode开始传输数据给客户端（从磁盘里面读取数据输入流，以Packet为单位来做校验）。

4 客户端以Packet为单位接收，先在本地缓存，然后写入目标文件。

# 4 NameNode的工作机制

**NameNode的职责**：

- 负责客户端请求的响应
- 元数据的管理：查询、修改

## 4.1 元数据管理

- NameNode：在内存中储存 HDFS 文件的元数据信息（目录）
  - 这是一份完整的元数据；
  - 但是如果节点故障或断电，存在内存中的数据会丢失，显然只在内存中保存是不可靠的；
  - 实际在磁盘当中也有保存：Fsimage 和 Edits，一个 NameNode 节点在重启后会根据这磁盘上的这两个文件来恢复到之前的状态
- Fsimage：磁盘元数据镜像文件
  - 这是一个“准完整”的元数据镜像，存储在namenode的工作目录中
- Edits：数据操作日志文件
  - 如果每次对 HDFS 的操作都实时的把内存中的元数据信息往磁盘上传输，这样显然效率不够高，也不稳定；这时就出现了 Edits 文件，用来记录每次对 HDFS 的操作，这样在磁盘上每次就只用做很小改动（只进行追加操作）
  - 当  Edits 文件达到了一定大小或过了一定的时间，就需要把 Edits 文件转化 Fsimage 文件，然后清空 Edits，这样的 Fsimage 文件不会和内存中的元数据实时同步，需要加上 Edits 文件才相等。
- SecondaryNameNode：负责 Edits 转化成 Fsimage
  - SecondaryNameNode 不是 NameNode 的备份；
  - SecondaryNameNode 会定时定量的把集群中的 Edits 文件转化为 Fsimage 文件，来保证 NameNode 中数据的可靠性

## 4.2 查看元数据

Edits 和 Fsimage 并非明文存储，需要转换后才能查看，使用 hdfs 命令进行转换：

### 4.2.1 转换 Fsimage 文件

Fsimage文件存储位置：`${dfs.namenode.name.dir}/current/`

- 例如：

  ```shell
  [root@0fe37eebc9fb current]# pwd
  /root/apps/hadoop-2.9.2/namenode/current
  [root@0fe37eebc9fb current]# ls
  VERSION                                        edits_0000000000000000121-0000000000000000122  fsimage_0000000000000000130
  edits_0000000000000000001-0000000000000000002  edits_0000000000000000123-0000000000000000124  fsimage_0000000000000000130.md5
  edits_0000000000000000003-0000000000000000004  edits_0000000000000000125-0000000000000000126  fsimage_0000000000000000132
  edits_0000000000000000005-0000000000000000006  edits_0000000000000000127-0000000000000000128  fsimage_0000000000000000132.md5
  edits_0000000000000000007-0000000000000000106  edits_0000000000000000129-0000000000000000130  seen_txid
  edits_0000000000000000107-0000000000000000118  edits_0000000000000000131-0000000000000000132
  edits_0000000000000000119-0000000000000000120  edits_inprogress_0000000000000000133
  ```

语法格式：`bin/hdfs oiv -p FORMAT -i INPUTFILE -o OUTPUTFILE`

- `-p`：转换格式 (XML|FileDistribution|ReverseXML|Web|Delimited)
- `-i`：要转换的文件
- `-o`：转换后文件路径

```shell
[root@0fe37eebc9fb current]# ls
VERSION                                        edits_0000000000000000121-0000000000000000122  fsimage_0000000000000000130
edits_0000000000000000001-0000000000000000002  edits_0000000000000000123-0000000000000000124  fsimage_0000000000000000130.md5
edits_0000000000000000003-0000000000000000004  edits_0000000000000000125-0000000000000000126  fsimage_0000000000000000132
edits_0000000000000000005-0000000000000000006  edits_0000000000000000127-0000000000000000128  fsimage_0000000000000000132.md5
edits_0000000000000000007-0000000000000000106  edits_0000000000000000129-0000000000000000130  seen_txid
edits_0000000000000000107-0000000000000000118  edits_0000000000000000131-0000000000000000132
edits_0000000000000000119-0000000000000000120  edits_inprogress_0000000000000000133
[root@0fe37eebc9fb current]# hdfs oiv -p XML -i fsimage_0000000000000000132 -o ./fsimage_0000000000000000132.xml
20/10/18 22:34:19 INFO offlineImageViewer.FSImageHandler: Loading 3 strings
[root@0fe37eebc9fb current]# cat fsimage_0000000000000000132.xml
<?xml version="1.0"?>
<fsimage><version><layoutVersion>-63</layoutVersion><onDiskVersion>1</onDiskVersion><oivRevision>826afbeae31ca687bc2f8471dc841b66ed2c6704</oivRevision></version>
<NameSection><namespaceId>829857879</namespaceId><genstampV1>1000</genstampV1><genstampV2>1012</genstampV2><genstampV1Limit>0</genstampV1Limit><lastAllocatedBlockId>1073741836</lastAllocatedBlockId><txid>132</txid></NameSection>
<INodeSection><lastInodeId>16420</lastInodeId><numInodes>23</numInodes><inode><id>16385</id><type>DIRECTORY</type><name></name><mtime>1602825168395</mtime><permission>root:supergroup:0755</permission><nsquota>9223372036854775807</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16386</id><type>DIRECTORY</type><name>wordcount</name><mtime>1602823299297</mtime><permission>root:supergroup:0755</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16387</id><type>DIRECTORY</type><name>input</name><mtime>1602822622072</mtime><permission>root:supergroup:0755</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16388</id><type>FILE</type><name>somewords.txt</name><replication>2</replication><mtime>1602822622035</mtime><atime>1602822620946</atime><preferredBlockSize>134217728</preferredBlockSize><permission>root:supergroup:0644</permission><blocks><block><id>1073741825</id><genstamp>1001</genstamp><numBytes>23</numBytes></block>
</blocks>
<storagePolicyId>0</storagePolicyId></inode>
<inode><id>16389</id><type>DIRECTORY</type><name>tmp</name><mtime>1602823293108</mtime><permission>root:supergroup:0700</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16390</id><type>DIRECTORY</type><name>hadoop-yarn</name><mtime>1602823293108</mtime><permission>root:supergroup:0700</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16391</id><type>DIRECTORY</type><name>staging</name><mtime>1602823297704</mtime><permission>root:supergroup:0700</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16392</id><type>DIRECTORY</type><name>root</name><mtime>1602823293108</mtime><permission>root:supergroup:0700</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16393</id><type>DIRECTORY</type><name>.staging</name><mtime>1602823308553</mtime><permission>root:supergroup:0700</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16399</id><type>DIRECTORY</type><name>history</name><mtime>1602823297705</mtime><permission>root:supergroup:0755</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16400</id><type>DIRECTORY</type><name>done_intermediate</name><mtime>1602823297726</mtime><permission>root:supergroup:1777</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16401</id><type>DIRECTORY</type><name>root</name><mtime>1602823307498</mtime><permission>root:supergroup:0770</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16403</id><type>DIRECTORY</type><name>output</name><mtime>1602823307384</mtime><permission>root:supergroup:0755</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16409</id><type>FILE</type><name>part-r-00000</name><replication>2</replication><mtime>1602823307311</mtime><atime>1602823307223</atime><preferredBlockSize>134217728</preferredBlockSize><permission>root:supergroup:0644</permission><blocks><block><id>1073741832</id><genstamp>1008</genstamp><numBytes>33</numBytes></block>
</blocks>
<storagePolicyId>0</storagePolicyId></inode>
<inode><id>16411</id><type>FILE</type><name>_SUCCESS</name><replication>2</replication><mtime>1602823307387</mtime><atime>1602823307384</atime><preferredBlockSize>134217728</preferredBlockSize><permission>root:supergroup:0644</permission><storagePolicyId>0</storagePolicyId></inode>
<inode><id>16413</id><type>FILE</type><name>job_1602816131335_0001.summary</name><replication>2</replication><mtime>1602823307428</mtime><atime>1602823307411</atime><preferredBlockSize>134217728</preferredBlockSize><permission>root:supergroup:0770</permission><blocks><block><id>1073741833</id><genstamp>1009</genstamp><numBytes>347</numBytes></block>
</blocks>
<storagePolicyId>0</storagePolicyId></inode>
<inode><id>16414</id><type>FILE</type><name>job_1602816131335_0001-1602823294119-root-word+count-1602823307394-1-1-SUCCEEDED-default-1602823299288.jhist</name><replication>2</replication><mtime>1602823307461</mtime><atime>1602823307442</atime><preferredBlockSize>134217728</preferredBlockSize><permission>root:supergroup:0770</permission><blocks><block><id>1073741834</id><genstamp>1010</genstamp><numBytes>33570</numBytes></block>
</blocks>
<storagePolicyId>0</storagePolicyId></inode>
<inode><id>16415</id><type>FILE</type><name>job_1602816131335_0001_conf.xml</name><replication>2</replication><mtime>1602823307491</mtime><atime>1602823307470</atime><preferredBlockSize>134217728</preferredBlockSize><permission>root:supergroup:0770</permission><blocks><block><id>1073741835</id><genstamp>1011</genstamp><numBytes>196010</numBytes></block>
</blocks>
<storagePolicyId>0</storagePolicyId></inode>
<inode><id>16416</id><type>DIRECTORY</type><name>aaa</name><mtime>1602825168395</mtime><permission>root:supergroup:0755</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16417</id><type>DIRECTORY</type><name>bbb</name><mtime>1602825168395</mtime><permission>root:supergroup:0755</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16418</id><type>DIRECTORY</type><name>cc</name><mtime>1602825168395</mtime><permission>root:supergroup:0755</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16419</id><type>DIRECTORY</type><name>dd</name><mtime>1602825383414</mtime><permission>root:supergroup:0755</permission><nsquota>-1</nsquota><dsquota>-1</dsquota></inode>
<inode><id>16420</id><type>FILE</type><name>a.txt</name><replication>2</replication><mtime>1602825383410</mtime><atime>1602825383279</atime><preferredBlockSize>134217728</preferredBlockSize><permission>root:supergroup:0644</permission><blocks><block><id>1073741836</id><genstamp>1012</genstamp><numBytes>11</numBytes></block>
</blocks>
<storagePolicyId>0</storagePolicyId></inode>
</INodeSection>
<INodeReferenceSection></INodeReferenceSection><SnapshotSection><snapshotCounter>0</snapshotCounter><numSnapshots>0</numSnapshots></SnapshotSection>
<INodeDirectorySection><directory><parent>16385</parent><child>16416</child><child>16389</child><child>16386</child></directory>
<directory><parent>16386</parent><child>16387</child><child>16403</child></directory>
<directory><parent>16387</parent><child>16388</child></directory>
<directory><parent>16389</parent><child>16390</child></directory>
<directory><parent>16390</parent><child>16391</child></directory>
<directory><parent>16391</parent><child>16399</child><child>16392</child></directory>
<directory><parent>16392</parent><child>16393</child></directory>
<directory><parent>16399</parent><child>16400</child></directory>
<directory><parent>16400</parent><child>16401</child></directory>
<directory><parent>16401</parent><child>16414</child><child>16413</child><child>16415</child></directory>
<directory><parent>16403</parent><child>16411</child><child>16409</child></directory>
<directory><parent>16416</parent><child>16417</child></directory>
<directory><parent>16417</parent><child>16418</child></directory>
<directory><parent>16418</parent><child>16419</child></directory>
<directory><parent>16419</parent><child>16420</child></directory>
</INodeDirectorySection>
<FileUnderConstructionSection></FileUnderConstructionSection>
<SecretManagerSection><currentId>0</currentId><tokenSequenceNumber>0</tokenSequenceNumber><numDelegationKeys>0</numDelegationKeys><numTokens>0</numTokens></SecretManagerSection><CacheManagerSection><nextDirectiveId>1</nextDirectiveId><numDirectives>0</numDirectives><numPools>0</numPools></CacheManagerSection>
</fsimage>
```

### 4.2.2 转换 Edits 文件

Edits文件存储位置：`${dfs.namenode.name.dir}/current/`

- 例如：

  ```shell
  [root@0fe37eebc9fb current]# pwd
  /root/apps/hadoop-2.9.2/namenode/current
  [root@0fe37eebc9fb current]# ls
  VERSION                                        edits_0000000000000000121-0000000000000000122  fsimage_0000000000000000130
  edits_0000000000000000001-0000000000000000002  edits_0000000000000000123-0000000000000000124  fsimage_0000000000000000130.md5
  edits_0000000000000000003-0000000000000000004  edits_0000000000000000125-0000000000000000126  fsimage_0000000000000000132
  edits_0000000000000000005-0000000000000000006  edits_0000000000000000127-0000000000000000128  fsimage_0000000000000000132.md5
  edits_0000000000000000007-0000000000000000106  edits_0000000000000000129-0000000000000000130  seen_txid
  edits_0000000000000000107-0000000000000000118  edits_0000000000000000131-0000000000000000132
  edits_0000000000000000119-0000000000000000120  edits_inprogress_0000000000000000133
  ```

语法格式：`bin/hdfs oev -p FORMAT -i INPUTFILE -o OUTPUTFILE`

- `-p`：转换格式，binary (native binary format that Hadoop uses), xml (default, XML  format), stats (prints statistics about edits file)
- `-i`：要转换的文件
- `-o`：转换后文件路径

```shell
[root@0fe37eebc9fb current]# ls
VERSION                                        edits_0000000000000000121-0000000000000000122  fsimage_0000000000000000130
edits_0000000000000000001-0000000000000000002  edits_0000000000000000123-0000000000000000124  fsimage_0000000000000000130.md5
edits_0000000000000000003-0000000000000000004  edits_0000000000000000125-0000000000000000126  fsimage_0000000000000000132
edits_0000000000000000005-0000000000000000006  edits_0000000000000000127-0000000000000000128  fsimage_0000000000000000132.md5
edits_0000000000000000007-0000000000000000106  edits_0000000000000000129-0000000000000000130  fsimage_0000000000000000132.xml
edits_0000000000000000107-0000000000000000118  edits_0000000000000000131-0000000000000000132  seen_txid
edits_0000000000000000119-0000000000000000120  edits_inprogress_0000000000000000133
[root@0fe37eebc9fb current]# hdfs oev -p xml -i edits_inprogress_0000000000000000133 -o ./edits_inprogress_0000000000000000133.xml
[root@0fe37eebc9fb current]# cat edits_inprogress_0000000000000000133.xml
<?xml version="1.0" encoding="UTF-8"?>
<EDITS>
  <EDITS_VERSION>-63</EDITS_VERSION>
  <RECORD>
    <OPCODE>OP_START_LOG_SEGMENT</OPCODE>
    <DATA>
      <TXID>133</TXID>
    </DATA>
  </RECORD>
</EDITS>
```

## 4.3 元数据的CheckPoint

每隔一段时间，会由SecondaryNameNode将NameNode上积累的所有edits和一个最新的fsimage下载到本地，并加载到内存进行merge，这个过程称为CheckPoint

### 4.3.1 CheckPoint的设置

#### 4.3.1.1 以时间为准

SecondaryNameNode 默认每隔一小时执行一次

查看默认配置：http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml

```xml
<property>
    <name>dfs.namenode.checkpoint.period</name>
    <value>3600</value>
</property>
```

#### 4.3.1.2 以次数为准

```xml
<property>
    <name>dfs.namenode.checkpoint.txns</name>
    <value>10000</value>
    <description>作次数到达一万次就发起合并</description>
</property>
<property>
    <name>dfs.namenode.checkpoint.check.period</name>
    <value>600</value>
    <description>每间隔10分钟检查一次操作次数是否到达</description>
</property>
```

### 4.3.2 CheckPoint的附带作用

NameNode和SecondaryNameNode的工作目录存储结构完全相同，所以，当NameNode故障退出需要重新恢复时，可以从SecondaryNameNode的工作目录中将fsimage拷贝到NameNode的工作目录，以恢复NameNode的元数据。

# 5 DataNode的工作机制

## 5.1 DataNode的工作机制

![](https://zhishan-zh.github.io/media/hadoop_hdfs_20201019092548.png)

1. 一个数据块在DataNode上以文件的形式存储在磁盘上，包括两个文件，一个是数据本身，一个元数据（包括数据块的长度、块数据的校验和、以及时间戳 （这个时候是安全机制））；

2. DataNode启动后向NameNode注册，注册通过后，DataNode周期性(1小时)地向NameNode上报所有块的信息；

   > 这点很重要，因为当集群中发生某些block副本失效时，集群如何恢复block初始副本数量的问题。
   >
   > 上报时间间隔的配置：
   >
   > ```xml
   > <property>
   > 	<name>dfs.blockreport.intervalMsec</name>
   > 	<value>3600000</value>
   > 	<description>Determines block reporting interval in milliseconds.</description>
   > </property>
   > 
   > ```

3. 心跳每3秒一次。心跳返回的结果带有NameNode给DataNode的命令（如复制块数据到另外一台机器，或删除某个数据块），如果超过10分钟没有收到某个DataNode的心跳，则认为该节点不可用；

   > DataNode进程死亡或者网络故障造成DataNode无法与namenode通信，namenode不会立即把该节点判定为死亡，要经过一段时间，这段时间暂称作超时时长。HDFS默认的超时时长为10分钟+30秒。如果定义超时时间为timeout，则超时时长的计算公式为：$timeout  = 2 * heartbeat.recheck.interval + 10 * dfs.heartbeat.interval$。
   > 而默认的`heartbeat.recheck.interval`大小为5分钟，`dfs.heartbeat.interval`默认为3秒。
   > 需要注意的是`hdfs-site.xml`配置文件中的`heartbeat.recheck.interval`的单位为毫秒，dfs.heartbeat.interval的单位为秒。举个例子，如果`heartbeat.recheck.interval`设置为5000（毫秒），`dfs.heartbeat.interval`设置为3（秒，默认），则总的超时时间为40秒。
   >
   > ```xml
   > <property>
   >         <name>heartbeat.recheck.interval</name>
   >         <value>2000</value>
   > </property>
   > <property>
   >         <name>dfs.heartbeat.interval</name>
   >         <value>1</value>
   > </property>
   > ```

4. 集群运行中可以安全加入和退出一些机器。

## 5.2 数据完整性

1. DataNode在读取block块的时候会先进行checksum（数据块校验和）；如果client发现本次计算的校验和跟创建时的校验和不一致，则认为该block块已损坏；
2. 客户端在抛出ChecksumException之前上报该block信息给NameNode进行标记（“已损坏”），这样NameNode就不会把客户端指向这个block，也不会复制这个block到其他的DataNode。
3. client重新读取另外的DataNode上的block。
4. 在心跳返回时NameNode将块的复制任务交给DataNode，从完好的block副本进行复制以达到默认的备份数3；
5. NameNode删除掉坏的block。
6. DataNode在一个block块被创建之日起三周后开始进行校验

## 5.3 观察验证DataNode的功能

上传一个文件，观察文件的block具体的物理存放情况：（在每一台datanode机器上的这个目录中能找到文件的切块）

```shell
#创建一个测试文件，随便输入一些内容
[root@0fe37eebc9fb apps]# vi testCopyFromLocalFile.text
[root@0fe37eebc9fb apps]# ls
hadoop-2.9.2  hadoop-2.9.2.tar.gz  jdk-8u251-linux-x64.tar.gz  jdk1.8.0_251  testCopyFromLocalFile.text
# 把本地文件上传到hdfs根路径下
[root@0fe37eebc9fb apps]# hadoop fs -copyFromLocal testCopyFromLocalFile.text /
#测试上传文件情况
[root@0fe37eebc9fb apps]# hadoop fs -ls /
Found 4 items
drwxr-xr-x   - root supergroup          0 2020-10-16 13:12 /aaa
-rw-r--r--   2 root supergroup         28 2020-10-19 10:01 /testCopyFromLocalFile.text
drwx------   - root supergroup          0 2020-10-16 12:41 /tmp
#登录DataNode节点hdp-node-02查看查看文件切块：
PS C:\Users\ZhangHai> docker exec -it 6f13fa25269a bash
[root@49abcf5aad57 finalized]# pwd
/root/apps/hadoop-2.9.2/datanode/current/BP-227589413-172.18.0.2-1602811079315/current/finalized
[root@49abcf5aad57 finalized]# ls
subdir0
#登录DataNode节点hdp-node-03查看查看文件切块：
PS C:\Users\ZhangHai> docker exec -it 6f13fa25269a bash
[root@6f13fa25269a finalized]# pwd
/root/apps/hadoop-2.9.2/datanode/current/BP-227589413-172.18.0.2-1602811079315/current/finalized
[root@6f13fa25269a finalized]# ls
subdir0
```

# 6 在开发中使用HDFS

HDFS在生产应用中主要是客户端的开发，其核心步骤是从HDFS提供的api中构造一个HDFS的访问客户端对象，然后通过该客户端对象操作（增删改查）HDFS上的文件。

## 6.1 Java操作HDFS

### 6.1.1 搭建开发环境

1. 在idea中使用Spring Initializr工具创建Spring Boot项目

   ![](https://zhishan-zh.github.io/media/hadoop_hdfs_java_20201019102936.png)

2. 配置项目信息：

   ![](https://zhishan-zh.github.io/media/hadoop_hdfs_java_20201019103116.png)

3. 选择依赖项：这里只选择web以来，一边提供调用接口

   ![](https://zhishan-zh.github.io/media/hadoop_hdfs_java_202012281435.png)

4. 添加项目名称

   ![](https://zhishan-zh.github.io/media/hadoop_hdfs_java_202012281438.png)

5. pom文件中加入hadoop的依赖：

   ![](https://zhishan-zh.github.io/media/hadoop_hdfs_java_20201019103637.png)

   ```xml
   <dependency>
       <groupId>org.apache.hadoop</groupId>
       <artifactId>hadoop-client</artifactId>
       <version>2.9.2</version>
   </dependency>
   ```

注：如需手动引入jar包，hdfs的jar包在hadoop的安装目录的share下

### 6.1.3 获取api中的客户端对象

在java中操作hdfs，首先要获得一个客户端实例：

```java
Configuration config = new Configuration();
FileSystem fileSystem = FileSystem.get(config);
```

- 我们的操作目标是HDFS，所以获取到的fs对象应该是DistributedFileSystem的实例；

- 这里的`FileSystem.get(config)`方法是config配置对象中的参数`fs.defaultFS`的配置值来判断具体实例化那种客户端类。
  - 如果我们的代码中没有指定`fs.defaultFS`，并且工程classpath下也没有给定相应的配置，conf中的默认值就来自于hadoop的jar包中的`core-default.xml`，默认值为： `file:///`，则获取的将不是一个DistributedFileSystem的实例，而是一个本地文件系统的客户端对象。

  - 如果要获取DistributedFileSystem的实例，则代码需要改为：

    ```java
    Configuration config = new Configuration();
    config.set("fs.defaultFS", "hdfs://localhost:9000");
    FileSystem fileSystem = FileSystem.get(config);//这里还有问题，请往下看
    ```

### 6.1.4 文件的增删改查

```java
package com.lifeng;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;
import org.junit.Before;
import org.junit.Test;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URI;

public class HdfsClient {
    FileSystem fs = null;

    @Before
    public void init() throws Exception{
        /*
            构造一个配置参数对象，设置一个参数：我们要访问的hdfs的URI,从而FileSystem.get(conf)方法就知道应该是去构造一个访问hdfs文件系统的客户端，以及hdfs的访问地址
            创建配置对象（new Configuration();）的时候，它就会去加载jar包中的hdfs-default.xml，然后再加载classpath下的hdfs-site.xml
            参数优先级： 1、客户端代码中设置的值 2、classpath下的用户自定义配置文件 3、然后是服务器的默认配置
         */
        Configuration conf = new Configuration();
//        conf.set("fs.defaultFS", "hdfs://localhsot:9000");
        conf.set("dfs.replication", "2");

        // 获取一个hdfs的访问客户端，根据参数，这个实例应该是DistributedFileSystem的实例
        // fs = FileSystem.get(conf);

        // 如果这样去获取，那conf里面就可以不要配"fs.defaultFS"参数，而且这个客户端的身份标识已经是root用户
        fs = FileSystem.get(new URI("hdfs://localhost:9000"), conf, "root");
    }

    /**
     * 上传文件
     * @throws Exception
     */
    @Test
    public void testAddFileToHdfs() throws Exception{
        // 要上传的文件所在的本地路径
        Path src = new Path("D:/todo/testFile.txt");
        // 要上传到hdfs的目标路径，这个路径需要在hdfs中已经存在
        Path dst = new Path("/aaa");
        fs.copyFromLocalFile(src, dst);
        fs.close();
    }

    /**
     * 从hdfs下载文件到本地
     * @throws IllegalArgumentException
     * @throws IOException
     */
    @Test
    public void testDownloadFileToLocal() throws IllegalArgumentException, IOException {
        fs.copyToLocalFile(new Path("/aaa/testFile.txt"), new Path("D:\\todo\\testFile_fromHdfs.txt"));
        fs.close();
    }

    /**
     * 在hdfs上迭代创建目录，删除目录和重命名目录
     * @throws IllegalArgumentException
     * @throws IOException
     */
    @Test
    public void testMkdirAndDeleteAndRename() throws IllegalArgumentException, IOException {
        // 创建目录
        fs.mkdirs(new Path("/a1/b1/c1"));
        // 删除文件夹 ，如果是非空文件夹，参数2必须给值true
        fs.delete(new Path("/aaa"), true);
        // 重命名文件或文件夹
        fs.rename(new Path("/a1"), new Path("/a2"));
    }

    /**
     * 查看目录信息，只显示文件
     *
     * @throws IOException
     * @throws IllegalArgumentException
     * @throws FileNotFoundException
     */
    @Test
    public void testListFiles() throws FileNotFoundException, IllegalArgumentException, IOException {

        // 返回迭代器
        RemoteIterator<LocatedFileStatus> listFiles = fs.listFiles(new Path("/"), true);

        while (listFiles.hasNext()) {
            LocatedFileStatus fileStatus = listFiles.next();
            System.out.println(fileStatus.getPath().getName());
            System.out.println(fileStatus.getBlockSize());
            System.out.println(fileStatus.getPermission());
            System.out.println(fileStatus.getLen());
            BlockLocation[] blockLocations = fileStatus.getBlockLocations();
            for (BlockLocation bl : blockLocations) {
                System.out.println("block-length:" + bl.getLength() + "--" + "block-offset:" + bl.getOffset());
                String[] hosts = bl.getHosts();
                for (String host : hosts) {
                    System.out.println(host);
                }
            }
            System.out.println("--------------分割线--------------");
        }
    }

    /**
     * 查看文件及文件夹信息
     *
     * @throws IOException
     * @throws IllegalArgumentException
     * @throws FileNotFoundException
     */
    @Test
    public void testListAll() throws FileNotFoundException, IllegalArgumentException, IOException {

        FileStatus[] listStatus = fs.listStatus(new Path("/"));

        String flag = "目录：";
        for (FileStatus fstatus : listStatus) {
            if (fstatus.isFile())  flag = "文件：";
            System.out.println(flag + fstatus.getPath().getName());
        }
    }
}
```

### 6.1.5 通过流的方式访问HDFS

# 7 在idea中远程调试docker的hadoop项目

**外部客户端可以获取文件元数据信息，可以获取空的文本文件，但是无法获取有内容的文件。应该是不在一个网络的原因，后续需要研究DistributedFileSystem和DFSClient**

## 7.1 spring boot项目打包maven插件

```xml
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
</plugin>
```

## 7.2 DockerFile

位置：和`pom.xml`位置相同

```
FROM java:8
VOLUME /opt/mydockerwork/docker-test-work
#为jar包起别名
ADD docker-test-1.0-SNAPSHOT.jar /docker-test.jar
#暴露调试端口，容器内部
EXPOSE 60006
#下面的address和上面的EXPOSE一致
ENTRYPOINT ["java","-jar","-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=60006","-Dspring.profiles.active=sit","/docker-test.jar"]
```

./jdk1.8.0_251/bin/java -jar -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -Dspring.profiles.active=sit hdfs-0.0.1-SNAPSHOT.jar