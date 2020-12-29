# MapReduce&Yarn

Mapreduce是一个分布式运算程序的编程框架，是用户开发“基于hadoop的数据分析应用”的核心框架。

Mapreduce核心功能是将用户编写的业务逻辑代码和自带默认组件整合成一个完整的分布式运算程序，并发运行在一个hadoop集群上。

# 1 MapReduce

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
2. 客户端将每个block块切片（逻辑切分），每个切片都对应一个map任务，默认一个block块对应一个切片和一个map任务。split包含的信息：分片的元数据信息，包含起始位置，长度，和所在节点列表等；
3. maptask进程启动之后，根据给定的数据切片范围进行数据处理，主体流程为：
   1. 利用客户指定的inputformat来获取RecordReader读取数据，形成输入KV对
      - 按行读取切片数据，组成键值对，key为当前行在源文件中的字节偏移量，value为读到的字符串
   2. map函数对键值对进行计算，输出<key,value,partition（分区号）>格式数据，partition指定该键值对由哪个reducer进行处理。通过分区器，key的hashcode对reducer个数取模。
   3. map将kvp写入环形缓冲区内，环形缓冲区默认为100MB，阈值为80%，当环形缓冲区达到80%时，就向磁盘溢写小文件，该小文件先按照分区号排序，区号相同的再按照key进行排序，归并排序。溢写的小文件如果达到三个，则进行归并，归并为大文件，大文件也按照分区和key进行排序，目的是降低中间结果数据量（网络传输），提升运行效率
4. MRAppMaster监控到所有maptask进程任务完成之后，会根据客户指定的参数启动相应数量的reducetask进程，并告知reducetask进程要处理的数据范围（数据分区）
5. 如果map任务处理完毕，则reducer发送http get请求到map主机上下载数据，该过程被称为shuffle（洗牌）。
   - 可以设置combineclass（需要算法满足结合律），先在map端对数据进行一个压缩，再进行传输，map任务结束，reduce任务开始
   - **copy**：一个reduce任务需要多个map任务的输出，每个map任务完成时间很可能不同，当只要有一个map任务完成，reduce任务立即开始复制。
     - 复制线程数配置：`mapred-site.xml`参数`mapreduce.reduce.shuffle.parallelcopies`，默认为5。
   - **copy缓冲区**：如果map输出相当小，则数据先被复制到reduce所在节点的内存缓冲区，当内存缓冲区大小达到阀值或内存缓冲区文件数达到阀值时，则合并后溢写磁盘。
     - 内存缓冲区大小配置：`mapred-site.xml`的参数`mapreduce.reduce.shuffle.input.buffer.percent`，默认值为0.70。
     - 内存缓冲区大小阀值配置：`mapred-site.xml`的参数`mapreduce.reduce.shuffle.merge.percent`，默认值为0.66。
     - 内存缓冲区文件数阀值配置：`mapred-site.xml`的参数`mapreduce.reduce.merge.inmem.threshold`，默认值为1000。
   - **sort**：复制完成所有map输出后，合并map输出文件并归并排序。
   - **sort的合并**：将map输出文件合并，直至≤合并因子
     - 合并因子配置：`mapred-site.xml`的参数`mapreduce.task.io.sort.factor`，默认值为10。
     - 例如，有50个map输出文件，进行5次合并，每次将10各文件合并成一个文件，最后5个文件。
6. reduce会对洗牌获取的数据进行归并，如果有时间，会将归并好的数据落入磁盘（其他数据还在洗牌状态）
7. 每个分区对应一个reduce，每个reduce按照key进行分组，每个分组调用一次reduce方法，该方法迭代计算，将结果写到hdfs输出。

## 1.4 Shuffle

### 1.4.1 MapReduce Shuffle

Shuffle的本意是洗牌、混洗的意思，把一组有规则的数据尽量打乱成无规则的数据。而在MapReduce中，Shuffle更像是洗牌的逆过程，指的是将map端的无规则输出按指定的规则“打乱”成具有一定规则的数据，以便reduce端接收处理。或者说需要将各节点上同一类数据汇集到某一节点进行计算，把这些分布在不同节点的数据按照一定的规则聚集到一起的过程成为Shuffle.。其在MapReduce中所处的工作阶段是map输出后到reduce接收前，具体可以分为map端和reduce端前后两个部分。

在Shuffle之前，也就是在map阶段，MapReduce会对要处理的数据进行分片（split）操作，为每一个分片分配一个MapTask任务。接下来map会对每一个分片中的每一行数据进行处理得到键值对（key,value）此时得到的键值对又叫做“中间结果”。此后便进入reduce阶段，由此可以看出Shuffle阶段的作用是处理“中间结果”。

由于Shuffle涉及到了磁盘的读写和网络的传输，因此Shuffle性能的高低直接影响到了整个程序的运行效率。

Hadoop的核心思想是MapReduce，但Shuffle又是MapReduce的核心。Shuffle的主要工作是从Map结束到Reduce开始之间的过程。Shuffle阶段又可以分为Map端的Shuffle和Reduce端的Shuffle。

MapReduce Shuffle的核心机制：数据分区，排序，缓存

- 就是将maptask输出的处理结果数据，分发给reducetask，并在分发的过程中，对数据按key进行了分区和排序。

shuffle是MR处理流程中的一个过程，它的每一个处理步骤是分散在各个map task和reduce task节点上完成的，整体来看，分为3个操作：

1. 分区partition；
2. Sort根据key排序；
3. Combiner进行局部value的合并。

### 1.4.2 MapReduce Shuffle流程

1. maptask收集我们的map()方法输出的kv对，放到内存缓冲区中
2. 从内存缓冲区不断溢出本地磁盘文件，可能会溢出多个文件
3. 多个溢出文件会被合并成大的溢出文件
4. 在溢出过程中，及合并的过程中，都要调用partitoner进行分组和针对key进行排序
5. reducetask根据自己的分区号，去各个maptask机器上取相应的结果分区数据
6. reducetask会取到同一个分区的来自不同maptask的结果文件，reducetask会将这些文件再进行合并（归并排序）
7. 合并成大文件后，shuffle的过程也就结束了，后面进入reducetask的逻辑运算过程（从文件中取出一个一个的键值对group，调用用户自定义的reduce()方法）

Shuffle中的缓冲区大小会影响到MapReduce程序的执行效率，原则上说，缓冲区越大，磁盘io的次数越少，执行速度就越快 
缓冲区的大小可以通过参数调整,  参数：`io.sort.mb`  默认100M。

## 1.5 MapTask并行度决定机制

### 1.5.1 并行度规划的基本逻辑

maptask的并行度决定map阶段的任务处理并发度，进而影响到整个job的处理速度。那么，mapTask并行实例是否越多越好呢？其并行度又是如何决定呢？

一个job的map阶段并行度由客户端在提交job时决定，而客户端对**map阶段并行度的规划的基本逻辑**为：将待处理数据执行逻辑切片（即按照一个特定切片大小，将待处理数据划分成逻辑上的多个split），然后每一个split分配一个MapTask并行实例处理。

### 1.5.2 切片机制

切片定义在InputFormat类中的getSplit()方法中。

FileInputFormat中默认的**切片机制**：

- 简单地按照文件的内容长度进行切片
- 切片大小，默认等于block大小
- 切片时不考虑数据集整体，而是逐个针对每一个文件单独切片

切片示例：

> 比如待处理数据有两个文件
>
> - file1.txt  320M
> - file2.txt  10M
>
> 经过FileInputFormat的切片机制运算后，形成的切片信息如下：
>
> - file1.txt.split1--  0~128
> - file1.txt.split2--  128~256
> - file1.txt.split3--  256~320
> - file2.txt.split1--  0~10M

FileInputFormat中**切片的大小的参数配置**：在FileInputFormat中，计算切片大小的逻辑：`Math.max(minSize, Math.min(maxSize, blockSize));`  切片主要由这几个值来运算决定：

- minsize：切片最小值。
  - 默认值为1。
  - 配置参数： `mapreduce.input.fileinputformat.split.minsize`
  - 参数调的比blockSize大，则可以让切片变得比blocksize还大
- maxsize：切片最大值。
  - 默认值：`Long.MAXValue`。
  - 配置参数：`mapreduce.input.fileinputformat.split.maxsize`
  - 参数如果调得比blocksize小，则会让切片变小，而且就等于配置的这个参数的值
- blocksize：默认情况下，切片大小=blocksize

### 1.5.3 MapTask并行度选择

选择并发数的影响因素：

- 运算节点的硬件配置
- 运算任务的类型：CPU密集型还是IO密集型
- 运算任务的数据量

**MapTask并行度选择**：如果硬件配置为2*12core + 64G，恰当的map并行度是大约每个节点20-100个map，最好每个map的执行时间至少一分钟。

- 如果job的每个map或者 reduce task的运行时间都只有30-40秒钟，那么就减少该job的map或者reduce数，每一task(map|reduce)的setup和加入到调度器中进行调度，这个中间的过程可能都要花费几秒钟，所以如果每个task都非常快就跑完了，就会在task的开始和结束的时候浪费太多的时间。
  - 配置task的JVM重用可以改善该问题：（`mapred.job.reuse.jvm.num.tasks`，默认是1，表示一个JVM上最多可以顺序执行的task数目（属于同一个Job）是1。也就是说一个task启一个JVM）

- 如果input的文件非常的大，比如1TB，可以考虑将hdfs上的每个block size设大，比如设成256MB或者512MB

**ReduceTask并行度的选择**：

- ReduceTask的并行度同样影响整个job的执行并发度和执行效率，但与MapTask的并发数由切片数决定不同，ReduceTask数量的决定是可以直接手动设置：
  - 默认值是1，手动设置为4：`job.setNumReduceTasks(4);`

- 如果数据分布不均匀，就有可能在reduce阶段产生数据倾斜。
- 注意： ReduceTask数量并不是任意设置，还要考虑业务逻辑需求，有些情况下，需要计算全局汇总结果，就只能有1个ReduceTask

- 尽量不要运行太多的reduce task。对大多数job来说，最好reduce的个数最多和集群中的reduce持平，或者比集群的 reduce slots小。这个对于小集群而言，尤其重要。

## 1.6 MapReduce中的序列化

Java的序列化是一个重量级序列化框架（Serializable），一个对象被序列化后，会附带很多额外的信息（各种校验信息，header，继承体系等等），不便于在网络中高效传输。所以，hadoop自己开发了一套序列化机制（Writable），相比于Java原生序列化，它显得精简和高效。

具体bean对象实现序列化的步骤：

- 必须实现Writable接口；

- 必须有空的构造方法：反序列化时，需要反射调用空参构造函数，所以必须有空参构造
- 重写序列化方法：`public void write(DataOutput out) throws IOException`
- 重写反序列化方法：`public void readFields(DataInput in) throws IOException`
  - 注意反序列化的操作顺序和序列化的操作顺序要完全一致。
- 如果把结果显示在文件中或打印出来，需要重写`toString()`。
- 如果需要将自定义的bean放在key中传输，则还需要实现Comparable接口，因为MapReduce框中的Shuffle过程要求对key必须能排序。

示例：

```java
package com.lifeng.hdfs.bean;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.io.Writable;

public class FlowBean implements Writable, Comparable<FlowBean>{
	
	private long upFlow;
	private long dFlow;
	private long sumFlow;
	
	//反序列化时，需要反射调用空参构造函数，所以要显示定义一个
	public FlowBean(){}
	
	public FlowBean(long upFlow, long dFlow) {
		this.upFlow = upFlow;
		this.dFlow = dFlow;
		this.sumFlow = upFlow + dFlow;
	}

	public long getUpFlow() {
		return upFlow;
	}
	public void setUpFlow(long upFlow) {
		this.upFlow = upFlow;
	}
	public long getdFlow() {
		return dFlow;
	}
	public void setdFlow(long dFlow) {
		this.dFlow = dFlow;
	}
	public long getSumFlow() {
		return sumFlow;
	}
	public void setSumFlow(long sumFlow) {
		this.sumFlow = sumFlow;
	}

	/**
	 * 序列化方法
	 */
	@Override
	public void write(DataOutput out) throws IOException {
		out.writeLong(upFlow);
		out.writeLong(dFlow);
		out.writeLong(sumFlow);
	}

	/**
	 * 反序列化方法
	 * 注意：反序列化的顺序跟序列化的顺序完全一致
	 */
	@Override
	public void readFields(DataInput in) throws IOException {
		 upFlow = in.readLong();
		 dFlow = in.readLong();
		 sumFlow = in.readLong();
	}

	/**
	 * 如果把结果显示在文件中或打印出来，需要重写此方法
	 * @return
	 */
	@Override
	public String toString() {
		return upFlow + "\t" + dFlow + "\t" + sumFlow;
	}

	/**
	 * 如果需要将自定义的bean放在key中传输，则还需要实现Comparable接口，然后重写此方法。
	 * 因为MapReduce框中的Shuffle过程要求对key必须能排序。
	 * @param o
	 * @return
	 */
	@Override
	public int compareTo(FlowBean o) {
		//实现按照sumflow的大小倒序排序
		return sumFlow>o.getSumFlow()?-1:1;
	}
}
```

# 2 Yarn

## 2.1 Yarn概述

Yarn是一个资源调度平台，负责为运算程序提供服务器运算资源，相当于一个分布式的操作系统平台，而mapreduce等运算程序则相当于运行于操作系统之上的应用程序。

## 2.2 Yarn的原理

Yarn并不清楚用户提交的程序的运行机制，**Yarn只提供运算资源的调度（用户程序向Yarn申请资源，Yarn就负责分配资源）**。Yarn中的主管角色叫ResourceManager，具体提供运算资源的角色叫NodeManager。这样一来，Yarn就与运行的用户程序完全解耦，就意味着**Yarn上可以运行各种类型的分布式运算程序**（mapreduce只是其中的一种），比如mapreduce、storm程序，spark程序，tez ……）。所以，spark、storm等运算框架都可以整合在yarn上运行，只要他们各自的框架中有**符合Yarn规范的资源请求机制即可**。Yarn就成为一个通用的资源调度平台，从此，企业中以前存在的各种运算集群都可以整合在一个物理集群上，提高资源利用率，方便数据共享。

# 3 MapReduce的编程规范

## 3.1 MapReduce的编程规范

**MapReduce程序包含三个部分**：用户自定义的Mapper和Reducer都要继承各自的父类

- Mapper
  - Mapper的输入数据是KV对的形式（KV的类型可自定义）
  - Mapper的输出数据是KV对的形式（KV的类型可自定义）
  - Mapper中的业务逻辑写在map()方法中
  - MapTask进程对每一个<K,V>调用一次map()方法
- Reducer
  - Reducer的输入数据类型对应Mapper的输出数据类型，也是KV
  - Reducer的业务逻辑写在reduce()方法中
  - ReduceTask进程对每一组相同k的<k,v>组调用一次reduce()方法
- Driver：提交运行MapReduce程序的客户端
  - 整个程序需要一个Drvier来进行提交，提交的是一个描述了各种必要信息的job对象