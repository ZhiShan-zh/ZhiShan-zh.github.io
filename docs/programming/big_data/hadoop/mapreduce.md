# MapReduce

Mapreduce是一个分布式运算程序的编程框架，是用户开发“基于hadoop的数据分析应用”的核心框架。

Mapreduce核心功能是将用户编写的业务逻辑代码和自带默认组件整合成一个完整的分布式运算程序，并发运行在一个hadoop集群上。

# 1 MapReduce原理

## 1.1 为什么需要MapReduce

1. 海量数据在单机上处理因为硬件资源限制，无法胜任；
2. 而一旦将单机版程序扩展到集群来分布式运行，将极大增加程序的复杂度和开发难度；
3. 引入MapReduce框架后，开发人员可以将绝大部分工作集中在业务逻辑的开发上，而将分布式计算中的复杂性交由框架来处理。

## 1.2 MapReduce的框架结构

一个完整的MapReduce程序在分布式运行时有三类实例进程：

- **MRAppMaster**：负责整个程序的过程调度及状态协调；
- **mapTask**：负责map阶段的整个数据处理流程；
- **ReduceTask**：负责reduce阶段的整个数据处理流程。

## 1.3 MapReduce的工作流程

![](https://zhishan-zh.github.io/media/hadoop_mapreduce_202010201659.png)

![](https://zhishan-zh.github.io/media/hadoop_mapreduce_202010201702.png)

1. 一个MapReduce程序启动的时候，最先启动的是MRAppMaster，MRAppMaster启动后根据本次job的描述信息，计算出需要的maptask实例数量，然后向集群申请机器启动相应数量的maptask进程；
2. 客户端将每个block块切片（逻辑切分），每个切片都对应一个map任务，默认一个block块对应一个切片和一个map任务，split包含的信息：分片的元数据信息，包含起始位置，长度，和所在节点列表等；
3. maptask进程启动之后，根据给定的数据切片范围进行数据处理，主体流程为：
   1. 利用客户指定的inputformat来获取RecordReader读取数据，形成输入KV对
      - 按行读取切片数据，组成键值对，key为当前行在源文件中的字节偏移量，value为读到的字符串
   2. map函数对键值对进行计算，输出<key,value,partition（分区号）>格式数据，partition指定该键值对由哪个reducer进行处理。通过分区器，key的hashcode对reducer个数取模。
   3. map将kvp写入环形缓冲区内，环形缓冲区默认为100MB，阈值为80%，当环形缓冲区达到80%时，就向磁盘溢写小文件，该小文件先按照分区号排序，区号相同的再按照key进行排序，归并排序。溢写的小文件如果达到三个，则进行归并，归并为大文件，大文件也按照分区和key进行排序，目的是降低中间结果数据量（网络传输），提升运行效率
   4. MRAppMaster监控到所有maptask进程任务完成之后，会根据客户指定的参数启动相应数量的reducetask进程，并告知reducetask进程要处理的数据范围（数据分区）
   5. 如果map任务处理完毕，则reducer发送http get请求到map主机上下载数据，该过程被称为洗牌shuffle
      - 可以设置combinclass（需要算法满足结合律），先在map端对数据进行一个压缩，再进行传输，map任务结束，reduce任务开始
   6. 