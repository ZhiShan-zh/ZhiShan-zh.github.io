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

## 3.2 代码示例：在一堆给定的文本文件中统计输出每一个单词出现的总次数

### 3.2.1 Mapper类

```java
package com.lifeng.wordcount;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

/**
 * KEYIN: 默认情况下，是mr框架所读到的一行文本的起始偏移量，Long,
 * 但是在hadoop中有自己的更精简的序列化接口，所以不直接用Long，而用LongWritable
 * 
 * VALUEIN:默认情况下，是mr框架所读到的一行文本的内容，String，同上，用Text
 * 
 * KEYOUT：是用户自定义逻辑处理完成之后输出数据中的key，在此处是单词，String，同上，用Text
 * VALUEOUT：是用户自定义逻辑处理完成之后输出数据中的value，在此处是单词次数，Integer，同上，用IntWritable
 * 
 * @author
 *
 */

public class WordcountMapper extends Mapper<LongWritable, Text, Text, IntWritable>{

	/**
	 * map阶段的业务逻辑就写在自定义的map()方法中
	 * maptask会对每一行输入数据调用一次我们自定义的map()方法
	 */
	@Override
	protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		
		//将maptask传给我们的文本内容先转换成String
		String line = value.toString();
		//根据空格将这一行切分成单词
		String[] words = line.split(" ");
		
		//将单词输出为<单词，1>
		for(String word:words){
			//将单词作为key，将次数1作为value，以便于后续的数据分发，可以根据单词分发，以便于相同单词会到相同的reduce task
			context.write(new Text(word), new IntWritable(1));
		}
	}	
}
```

### 3.2.2 Reducer类

```java
package com.lifeng.wordcount;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

/**
 * KEYIN, VALUEIN 对应  mapper输出的KEYOUT,VALUEOUT类型对应
 * 
 * KEYOUT, VALUEOUT 是自定义reduce逻辑处理结果的输出数据类型
 * KEYOUT是单词
 * VLAUEOUT是总次数
 * @author
 *
 */
public class WordcountReducer extends Reducer<Text, IntWritable, Text, IntWritable>{

	/**
	 * <angelababy,1><angelababy,1><angelababy,1><angelababy,1><angelababy,1>
	 * <hello,1><hello,1><hello,1><hello,1><hello,1><hello,1>
	 * <banana,1><banana,1><banana,1><banana,1><banana,1><banana,1>
	 * 入参key，是一组相同单词kv对的key
	 */
	@Override
	protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {

		int count=0;
		/*Iterator<IntWritable> iterator = values.iterator();
		while(iterator.hasNext()){
			count += iterator.next().get();
		}*/
		
		for(IntWritable value:values){	
			count += value.get();
		}	
		context.write(key, new IntWritable(count));		
	}	
}
```

### 3.2.3 主类：描述job和提交job

```java
package com.lifeng.wordcount;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * 相当于一个yarn集群的客户端
 * 需要在此封装我们的mr程序的相关运行参数，指定jar包
 * 最后提交给yarn
 * @author
 */
public class WordcountDriver {
	
	public static void main(String[] args) throws Exception {
		
		if (args == null || args.length == 0) {
			args = new String[2];
			args[0] = "hdfs://hdp-01:9000/wordcount/input/somewords.txt";
			args[1] = "hdfs://hdp-01:9000/wordcount/output";
		}
		
		Configuration conf = new Configuration();
		
		//设置的没有用!  ??????
//		conf.set("HADOOP_USER_NAME", "hadoop");
//		conf.set("dfs.permissions.enabled", "false");
		
		
		/*conf.set("mapreduce.framework.name", "yarn");
		conf.set("yarn.resoucemanager.hostname", "mini1");*/
		Job job = Job.getInstance(conf);
		
		/*job.setJar("/home/hadoop/wc.jar");*/
		//指定本程序的jar包所在的本地路径
		job.setJarByClass(WordcountDriver.class);
		
		//指定本业务job要使用的mapper/Reducer业务类
		job.setMapperClass(WordcountMapper.class);
		job.setReducerClass(WordcountReducer.class);
		
		//指定mapper输出数据的kv类型
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(IntWritable.class);
		
		//指定最终输出的数据的kv类型
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		
		//指定job的输入原始文件所在目录
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		//指定job的输出结果所在目录
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		
		//将job中配置的相关参数，以及job所用的java类所在的jar包，提交给yarn去运行
		/*job.submit();*/
		boolean res = job.waitForCompletion(true);
		System.exit(res?0:1);
	}
}
```

### 3.2.4 运行job

首先使用maven打包项目为jar包：testHdfs-1.0-SNAPSHOT.jar

```shell
# 把jar包复制到docker容器中
PS D:\todo> docker cp .\testHdfs-1.0-SNAPSHOT.jar hdp-node-04:/root/apps/

# 进入目标容器
PS D:\todo> docker exec -it a138996be1a3 bash
[root@a138996be1a3 /]# cd root/apps/

# 任务目录和任务输入文件
[root@a138996be1a3 apps]# hadoop fs -ls /wordcount
Found 2 items
drwxr-xr-x   - root supergroup          0 2020-10-16 12:30 /wordcount/input
[root@a138996be1a3 apps]# hadoop fs -ls /wordcount/input
Found 1 items
-rw-r--r--   2 root supergroup         23 2020-10-16 12:30 /wordcount/input/somewords.txt
[root@a138996be1a3 apps]# hadoop fs -cat /wordcount/input/somewords.txt
test
get
input
put
set
[root@a138996be1a3 apps]# ls
hadoop-2.9.2         hdfs-0.0.1-SNAPSHOT.jar     jdk1.8.0_251  testHdfs-1.0-SNAPSHOT.jar
hadoop-2.9.2.tar.gz  jdk-8u251-linux-x64.tar.gz  test.txt

# 使用hadoop jar运行job
[root@a138996be1a3 apps]# hadoop jar testHdfs-1.0-SNAPSHOT.jar com.lifeng.wordcount.WordcountDriver
20/12/31 10:45:08 INFO client.RMProxy: Connecting to ResourceManager at hdp-01/172.18.0.5:8032
20/12/31 10:45:09 WARN mapreduce.JobResourceUploader: Hadoop command-line option parsing not performed. Implement the Tool interface and execute your application with ToolRunner to remedy this.
20/12/31 10:45:09 INFO input.FileInputFormat: Total input files to process : 1
20/12/31 10:45:09 INFO mapreduce.JobSubmitter: number of splits:1
20/12/31 10:45:09 INFO Configuration.deprecation: yarn.resourcemanager.system-metrics-publisher.enabled is deprecated. Instead, use yarn.system-metrics-publisher.enabled
20/12/31 10:45:10 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1609381914713_0001
20/12/31 10:45:10 INFO impl.YarnClientImpl: Submitted application application_1609381914713_0001
20/12/31 10:45:10 INFO mapreduce.Job: The url to track the job: http://hdp-01:8088/proxy/application_1609381914713_0001/
20/12/31 10:45:10 INFO mapreduce.Job: Running job: job_1609381914713_0001
20/12/31 10:45:15 INFO mapreduce.Job: Job job_1609381914713_0001 running in uber mode : false
20/12/31 10:45:15 INFO mapreduce.Job:  map 0% reduce 0%
20/12/31 10:45:20 INFO mapreduce.Job:  map 100% reduce 0%
20/12/31 10:45:24 INFO mapreduce.Job:  map 100% reduce 100%
20/12/31 10:45:24 INFO mapreduce.Job: Job job_1609381914713_0001 completed successfully
20/12/31 10:45:24 INFO mapreduce.Job: Counters: 49
        File System Counters
                FILE: Number of bytes read=59
                FILE: Number of bytes written=396879
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=136
                HDFS: Number of bytes written=33
                HDFS: Number of read operations=6
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
        Job Counters
                Launched map tasks=1
                Launched reduce tasks=1
                Data-local map tasks=1
                Total time spent by all maps in occupied slots (ms)=1929
                Total time spent by all reduces in occupied slots (ms)=1631
                Total time spent by all map tasks (ms)=1929
                Total time spent by all reduce tasks (ms)=1631
                Total vcore-milliseconds taken by all map tasks=1929
                Total vcore-milliseconds taken by all reduce tasks=1631
                Total megabyte-milliseconds taken by all map tasks=1975296
                Total megabyte-milliseconds taken by all reduce tasks=1670144
        Map-Reduce Framework
                Map input records=5
                Map output records=5
                Map output bytes=43
                Map output materialized bytes=59
                Input split bytes=113
                Combine input records=0
                Combine output records=0
                Reduce input groups=5
                Reduce shuffle bytes=59
                Reduce input records=5
                Reduce output records=5
                Spilled Records=10
                Shuffled Maps =1
                Failed Shuffles=0
                Merged Map outputs=1
                GC time elapsed (ms)=75
                CPU time spent (ms)=720
                Physical memory (bytes) snapshot=510189568
                Virtual memory (bytes) snapshot=3962249216
                Total committed heap usage (bytes)=351272960
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=23
        File Output Format Counters
                Bytes Written=33

# 查看运行输入文件
[root@a138996be1a3 apps]# hadoop fs -ls /wordcount
Found 2 items
drwxr-xr-x   - root supergroup          0 2020-10-16 12:30 /wordcount/input
drwxr-xr-x   - root supergroup          0 2020-12-31 10:45 /wordcount/output
[root@a138996be1a3 apps]# hadoop fs -ls /wordcount/output
Found 2 items
-rw-r--r--   2 root supergroup          0 2020-12-31 10:45 /wordcount/output/_SUCCESS
-rw-r--r--   2 root supergroup         33 2020-12-31 10:45 /wordcount/output/part-r-00000
[root@a138996be1a3 apps]# hadoop fs -cat /wordcount/output/part-r-00000
get     1
input   1
put     1
set     1
test    1
```

## 3.3 MapReduce中的Combiner

- Combiner是MR程序中Mapper和Reducer之外的一种组件；
- Combiner组件的父类就是Reducer；
- Combiner和Reducer的区别在于运行的位置：
  - Combiner是在每一个maptask所在的节点运行；
  - Reducer是接收全局所有Mapper的输出结果；
- Combiner的意义就是对每一个maptask的输出进行局部汇总，以减小网络传输量；
- Combiner能够应用的前提是不能影响最终的业务逻辑
  - 因为combiner在mapreduce过程中可能调用也可能不调用，可能调一次也可能调多次。
  - Combiner的输出kv应该跟Reducer的输入kv类型要对应起来

**实现步骤**：

1. 自定义一个Combiner继承Reducer，重写reduce方法
2. 在job中设置： ` job.setCombinerClass(CustomCombiner.class)`

# 4 案例

## 4.1 排序初步

### 4.1.1 需求

任务目标：对日志数据中的上下行流量信息汇总，并输出按照总流量倒序排序的结果

流量日志格式：

```
1363157985066 	13726230503	00-FD-07-A4-72-B8:CMCC	120.196.100.82          24	27	2481	24681	200
1363157995052 	13826544101	5C-0E-8B-C7-F1-E0:CMCC	120.197.40.4			4	0	264	0	200
1363157991076 	13926435656	20-10-7A-28-CC-0A:CMCC	120.196.100.99			2	4	132	1512	200
1363154400022 	13926251106	5C-0E-8B-8B-B1-50:CMCC	120.197.40.4			4	0	240	0	200
```

### 4.1.2 分析

**基本思路**：实现自定义的bean来封装流量信息，并将bean作为map输出的key来传输

- MR程序在处理数据的过程中会对数据排序（map输出的kv对传输到reduce之前，会排序），排序的依据是map输出的key。所以，我们如果要实现自己需要的排序规则，则可以考虑将排序因素放到key中，让key实现接口：WritableComparable，然后重写key的compareTo方法

### 4.1.3 代码实现

```java
package cn.itcast.bigdata.mr.flowsum;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

import org.apache.hadoop.io.WritableComparable;

public class FlowBean implements WritableComparable<FlowBean>{
	
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
	
	
	public void set(long upFlow, long dFlow) {
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
	
	@Override
	public String toString() {
		 
		return upFlow + "\t" + dFlow + "\t" + sumFlow;
	}

	@Override
	public int compareTo(FlowBean o) {
		return this.sumFlow>o.getSumFlow()?-1:1;	//从大到小, 当前对象和要比较的对象比, 如果当前对象大, 返回-1, 交换他们的位置(自己的理解)
	}
}
```

```java
package cn.itcast.bigdata.mr.flowsum;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import cn.itcast.bigdata.mr.flowsum.FlowCount.FlowCountMapper;
import cn.itcast.bigdata.mr.flowsum.FlowCount.FlowCountReducer;

/**
 * 13480253104 180 180 360 13502468823 7335 110349 117684 13560436666 1116 954
 * 2070
 * 
 * @author
 * 
 */
public class FlowCountSort {

	static class FlowCountSortMapper extends Mapper<LongWritable, Text, FlowBean, Text> {

		FlowBean bean = new FlowBean();
		Text v = new Text();

		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			// 拿到的是上一个统计程序的输出结果，已经是各手机号的总流量信息
			String line = value.toString();

			String[] fields = line.split("\t");

			String phoneNbr = fields[0];

			long upFlow = Long.parseLong(fields[1]);
			long dFlow = Long.parseLong(fields[2]);

			bean.set(upFlow, dFlow);
			v.set(phoneNbr);

			context.write(bean, v);

		}

	}

	/**
	 * 根据key来掉, 传过来的是对象, 每个对象都是不一样的, 所以每个对象都调用一次reduce方法
	  * @author: 张政
	  * @date: 2016年4月11日 下午7:08:18
	  * @package_name: day07.sample
	 */
	static class FlowCountSortReducer extends Reducer<FlowBean, Text, Text, FlowBean> {

		// <bean(),phonenbr>
		@Override
		protected void reduce(FlowBean bean, Iterable<Text> values, Context context) throws IOException, InterruptedException {

			context.write(values.iterator().next(), bean);

		}

	}
	
	public static void main(String[] args) throws Exception {

		Configuration conf = new Configuration();
		/*conf.set("mapreduce.framework.name", "yarn");
		conf.set("yarn.resoucemanager.hostname", "mini1");*/
		Job job = Job.getInstance(conf);
		
		/*job.setJar("/home/hadoop/wc.jar");*/
		//指定本程序的jar包所在的本地路径
		job.setJarByClass(FlowCountSort.class);
		
		//指定本业务job要使用的mapper/Reducer业务类
		job.setMapperClass(FlowCountSortMapper.class);
		job.setReducerClass(FlowCountSortReducer.class);
		
		//指定mapper输出数据的kv类型
		job.setMapOutputKeyClass(FlowBean.class);
		job.setMapOutputValueClass(Text.class);
		
		//指定最终输出的数据的kv类型
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(FlowBean.class);
		
		//指定job的输入原始文件所在目录
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		//指定job的输出结果所在目录
		
		Path outPath = new Path(args[1]);
		/*FileSystem fs = FileSystem.get(conf);
		if(fs.exists(outPath)){
			fs.delete(outPath, true);
		}*/
		FileOutputFormat.setOutputPath(job, outPath);
		
		//将job中配置的相关参数，以及job所用的java类所在的jar包，提交给yarn去运行
		/*job.submit();*/
		boolean res = job.waitForCompletion(true);
		System.exit(res?0:1);
	}
}
```

## 4.2 自定义分组

### 4.2.1 需求

根据归属地输出流量统计数据结果到不同文件，以便于在查询统计结果时可以定位到省级范围进行

### 4.2.2 分析

- Mapreduce中会将map输出的kv对，按照相同key分组，然后分发给不同的reducetask。

- 默认的分发规则为：根据key的hashcode%reducetask数来分发。

- 所以如果要按照我们自己的需求进行分组，则需要改写数据分发（分组）组件Partitioner
  - 自定义一个CustomPartitioner，继承抽象类：Partitioner
  - 然后在job对象中，设置自定义partitioner：` job.setPartitionerClass(CustomPartitioner.class)`

### 4.2.3 实现

```java
package cn.itcast.bigdata.mr.provinceflow;

import java.util.HashMap;

import javax.security.auth.kerberos.KeyTab;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapreduce.Partitioner;

/**
 * K2  V2  对应的是map输出kv的类型
 * @author
 *
 */
public class ProvincePartitioner extends Partitioner<Text, FlowBean>{

	public static HashMap<String, Integer> proviceDict = new HashMap<String, Integer>();
	static{
		proviceDict.put("136", 0);
		proviceDict.put("137", 1);
		proviceDict.put("138", 2);
		proviceDict.put("139", 3);
	}
		
	@Override
	public int getPartition(Text key, FlowBean value, int numPartitions) {
		String prefix = key.toString().substring(0, 3);
		Integer provinceId = proviceDict.get(prefix);
		
		return provinceId==null?4:provinceId;
	}
}
```

```java
package cn.itcast.bigdata.mr.provinceflow;

import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import cn.itcast.bigdata.mr.wcdemo.WordcountDriver;
import cn.itcast.bigdata.mr.wcdemo.WordcountMapper;
import cn.itcast.bigdata.mr.wcdemo.WordcountReducer;

public class FlowCount {
	
	static class FlowCountMapper extends Mapper<LongWritable, Text, Text, FlowBean>{
		
		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			 
			//将一行内容转成string
			String line = value.toString();
			//切分字段
			String[] fields = line.split("\t");
			//取出手机号
			String phoneNbr = fields[1];
			//取出上行流量下行流量
			long upFlow = Long.parseLong(fields[fields.length-3]);
			long dFlow = Long.parseLong(fields[fields.length-2]);
			
			context.write(new Text(phoneNbr), new FlowBean(upFlow, dFlow));
			
			
		}
		
		
		
	}
	
	
	static class FlowCountReducer extends Reducer<Text, FlowBean, Text, FlowBean>{
		
		//<183323,bean1><183323,bean2><183323,bean3><183323,bean4>.......
		@Override
		protected void reduce(Text key, Iterable<FlowBean> values, Context context) throws IOException, InterruptedException {

			long sum_upFlow = 0;
			long sum_dFlow = 0;
			
			//遍历所有bean，将其中的上行流量，下行流量分别累加
			for(FlowBean bean: values){
				sum_upFlow += bean.getUpFlow();
				sum_dFlow += bean.getdFlow();
			}
			
			FlowBean resultBean = new FlowBean(sum_upFlow, sum_dFlow);
			context.write(key, resultBean);	
		}
		
	}
		
	
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		/*conf.set("mapreduce.framework.name", "yarn");
		conf.set("yarn.resoucemanager.hostname", "mini1");*/
		Job job = Job.getInstance(conf);
		
		/*job.setJar("/home/hadoop/wc.jar");*/
		//指定本程序的jar包所在的本地路径
		job.setJarByClass(FlowCount.class);
		
		//指定本业务job要使用的mapper/Reducer业务类
		job.setMapperClass(FlowCountMapper.class);
		job.setReducerClass(FlowCountReducer.class);
		
		//指定我们自定义的数据分区器
		job.setPartitionerClass(ProvincePartitioner.class);
		//同时指定相应“分区”数量的reducetask
		job.setNumReduceTasks(5);
		
		//指定mapper输出数据的kv类型
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(FlowBean.class);
		
		//指定最终输出的数据的kv类型
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(FlowBean.class);
		
		//指定job的输入原始文件所在目录
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		//指定job的输出结果所在目录
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		
		//将job中配置的相关参数，以及job所用的java类所在的jar包，提交给yarn去运行
		/*job.submit();*/
		boolean res = job.waitForCompletion(true);
		System.exit(res?0:1);		
	}
}
```

## 4.3 数据压缩

这是mapreduce的一种优化策略：通过压缩编码对mapper或者reducer的输出进行压缩，以减少磁盘IO，提高MR程序运行速度（但相应增加了cpu运算负担）：

- Mapreduce支持将map输出的结果或者reduce输出的结果进行压缩，以减少网络IO或最终输出数据的体积
- 压缩特性运用得当能提高性能，但运用不当也可能降低性能
- 基本原则：
  - 运算密集型的job，少用压缩
  - IO密集型的job，多用压缩

MapReduce支持的压缩编码：

![](https://zhishan-zh.github.io/media/hadoop_mapreduce_java_20201231142722145.png)

### 4.3.1 Reducer输出压缩

设置Reduce的输出压缩的两种方式：

- 在配置参数中设置

  ```properties
  mapreduce.output.fileoutputformat.compress=false
  mapreduce.output.fileoutputformat.compress.codec=org.apache.hadoop.io.compress.DefaultCodec
  mapreduce.output.fileoutputformat.compress.type=RECORD
  ```

- 在代码中设置

  ```java
  Job job = Job.getInstance(conf);
  FileOutputFormat.setCompressOutput(job, true);
  FileOutputFormat.setOutputCompressorClass(job, (Class<? extends CompressionCodec>) Class.forName(""));
  ```

### 4.3.2 Mapper输出压缩

设置Mapper的输出压缩的两种方式：

- 在配置参数中设置

  ```properties
  mapreduce.map.output.compress=false
  mapreduce.map.output.compress.codec=org.apache.hadoop.io.compress.DefaultCodec
  ```

- 在代码中设置

  ```java
  conf.setBoolean(Job.MAP_OUTPUT_COMPRESS, true);
  conf.setClass(Job.MAP_OUTPUT_COMPRESS_CODEC, GzipCodec.class, CompressionCodec.class);
  ```

### 4.3.3 压缩文件的读取

```java

```

## 4.4 join算法

### 4.4.1 Reducer端join算法

#### 4.4.1.1 需求

订单数据表t_order：

| id   | date     | pid   | amount |
| ---- | -------- | ----- | ------ |
| 1001 | 20150710 | P0001 | 2      |
| 1002 | 20150710 | P0001 | 3      |
| 1002 | 20150710 | P0002 | 3      |

 

商品信息表t_product

| id    | name   | category_id | price |
| ----- | ------ | ----------- | ----- |
| P0001 | 小米5  | C01         | 2     |
| P0002 | 锤子T1 | C01         | 3     |

假如数据量巨大，两表的数据是以文件的形式存储在HDFS中，需要用mapreduce程序来实现一下SQL查询运算：

```sql
select  a.id,a.date,b.name,b.category_id,b.price from t_order a join t_product b on a.pid = b.id
```

#### 4.4.1.2 分析

通过将关联的条件作为map输出的key，将两表满足join条件的数据并携带数据所来源的文件信息，发往同一个reduce task，在reduce中进行数据的串联

#### 4.4.1.3 实现

缺点：这种方式中，join的操作是在reduce阶段完成，reduce端的处理压力太大，map节点的运算负载则很低，资源利用率不高，且在reduce阶段极易产生数据倾斜

解决方案： map端join实现方式

```java
public class OrderJoin {

	static class OrderJoinMapper extends Mapper<LongWritable, Text, Text, OrderJoinBean> {

		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			// 拿到一行数据，并且要分辨出这行数据所属的文件
			String line = value.toString();

			String[] fields = line.split("\t");
			// 拿到itemid
			String itemid = fields[0];
			// 获取到这一行所在的文件名（通过inpusplit）
			String name = "你拿到的文件名";
			// 根据文件名，切分出各字段（如果是a，切分出两个字段，如果是b，切分出3个字段）
			OrderJoinBean bean = new OrderJoinBean();
			bean.set(null, null, null, null, null);
			context.write(new Text(itemid), bean);

		}

	}

	static class OrderJoinReducer extends Reducer<Text, OrderJoinBean, OrderJoinBean, NullWritable> {

		@Override
		protected void reduce(Text key, Iterable<OrderJoinBean> beans, Context context) throws IOException, InterruptedException {
			
			 //拿到的key是某一个itemid,比如1000
			//拿到的beans是来自于两类文件的bean
			//  {1000,amount} {1000,amount} {1000,amount}   ---   {1000,price,name}
			
			//将来自于b文件的bean里面的字段，跟来自于a的所有bean进行字段拼接并输出
		}
	}
}
```

### 4.4.2 Mapper端实现join

适用于关联表中有小表的情形；可以将小表分发到所有的map节点，这样，map节点就可以在本地对自己所读到的大表数据进行join并输出最终结果，可以大大提高join操作的并发度，加快处理速度

先在Mapper类中预先定义好小表，进行join

引入实际场景中的解决方案：一次加载数据库或者用distributedcache

```java
public class TestDistributedCache {
	static class TestDistributedCacheMapper extends Mapper<LongWritable, Text, Text, Text>{
		FileReader in = null;
		BufferedReader reader = null;
		HashMap<String,String> b_tab = new HashMap<String, String>();
		String localpath =null;
		String uirpath = null;
		
		//是在map任务初始化的时候调用一次
		@Override
		protected void setup(Context context) throws IOException, InterruptedException {
			//通过这几句代码可以获取到cache file的本地绝对路径，测试验证用
			Path[] files = context.getLocalCacheFiles();
			localpath = files[0].toString();
			URI[] cacheFiles = context.getCacheFiles();
			
			//缓存文件的用法——直接用本地IO来读取
			//这里读的数据是map task所在机器本地工作目录中的一个小文件
			in = new FileReader("b.txt");
			reader =new BufferedReader(in);
			String line =null;
			while(null!=(line=reader.readLine())){
				
				String[] fields = line.split(",");
				b_tab.put(fields[0],fields[1]);
				
			}
			IOUtils.closeStream(reader);
			IOUtils.closeStream(in);
			
		}
		
		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			//这里读的是这个map task所负责的那一个切片数据（在hdfs上）
			 String[] fields = value.toString().split("\t");
			 
			 String a_itemid = fields[0];
			 String a_amount = fields[1];
			 
			 String b_name = b_tab.get(a_itemid);
			 
			 // 输出结果  1001	98.9	banan
			 context.write(new Text(a_itemid), new Text(a_amount + "\t" + ":" + localpath + "\t" +b_name ));		 
		}	
	}
	
	
	public static void main(String[] args) throws Exception {
		
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf);
		
		job.setJarByClass(TestDistributedCache.class);
		
		job.setMapperClass(TestDistributedCacheMapper.class);
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(LongWritable.class);
		
		//这里是我们正常的需要处理的数据所在路径
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		
		//不需要reducer
		job.setNumReduceTasks(0);
		//分发一个文件到task进程的工作目录
		job.addCacheFile(new URI("hdfs://hadoop-server01:9000/cachefile/b.txt"));
		
		//分发一个归档文件到task进程的工作目录
//		job.addArchiveToClassPath(archive);

		//分发jar包到task节点的classpath下
//		job.addFileToClassPath(jarfile);
		
		job.waitForCompletion(true);
	}
}
```

## 4.5 Web日志预处理

### 4.5.1 需求

对web访问日志中的各字段识别切分

去除日志中不合法的记录

根据KPI统计需求，生成各类访问请求过滤数据

### 4.5.2 实现

#### 4.5.2.1 定义一个bean，用来记录日志数据中的各数据字段

```java
public class WebLogBean {
	
    private String remote_addr;// 记录客户端的ip地址
    private String remote_user;// 记录客户端用户名称,忽略属性"-"
    private String time_local;// 记录访问时间与时区
    private String request;// 记录请求的url与http协议
    private String status;// 记录请求状态；成功是200
    private String body_bytes_sent;// 记录发送给客户端文件主体内容大小
    private String http_referer;// 用来记录从那个页面链接访问过来的
    private String http_user_agent;// 记录客户浏览器的相关信息
    private boolean valid = true;// 判断数据是否合法
  
	public String getRemote_addr() {
		return remote_addr;
	}

	public void setRemote_addr(String remote_addr) {
		this.remote_addr = remote_addr;
	}

	public String getRemote_user() {
		return remote_user;
	}

	public void setRemote_user(String remote_user) {
		this.remote_user = remote_user;
	}

	public String getTime_local() {
		return time_local;
	}

	public void setTime_local(String time_local) {
		this.time_local = time_local;
	}

	public String getRequest() {
		return request;
	}

	public void setRequest(String request) {
		this.request = request;
	}

	public String getStatus() {
		return status;
	}

	public void setStatus(String status) {
		this.status = status;
	}

	public String getBody_bytes_sent() {
		return body_bytes_sent;
	}

	public void setBody_bytes_sent(String body_bytes_sent) {
		this.body_bytes_sent = body_bytes_sent;
	}

	public String getHttp_referer() {
		return http_referer;
	}

	public void setHttp_referer(String http_referer) {
		this.http_referer = http_referer;
	}

	public String getHttp_user_agent() {
		return http_user_agent;
	}

	public void setHttp_user_agent(String http_user_agent) {
		this.http_user_agent = http_user_agent;
	}

	public boolean isValid() {
		return valid;
	}

	public void setValid(boolean valid) {
		this.valid = valid;
	}
    
    
	@Override
	public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.valid);
        sb.append("\001").append(this.remote_addr);
        sb.append("\001").append(this.remote_user);
        sb.append("\001").append(this.time_local);
        sb.append("\001").append(this.request);
        sb.append("\001").append(this.status);
        sb.append("\001").append(this.body_bytes_sent);
        sb.append("\001").append(this.http_referer);
        sb.append("\001").append(this.http_user_agent);
        return sb.toString();
	}
}
```

#### 4.5.2.2 定义一个parser用来解析过滤web访问日志原始记录：

```java
public class WebLogParser {
    public static WebLogBean parser(String line) {
        WebLogBean webLogBean = new WebLogBean();
        String[] arr = line.split(" ");
        if (arr.length > 11) {
        	webLogBean.setRemote_addr(arr[0]);
        	webLogBean.setRemote_user(arr[1]);
        	webLogBean.setTime_local(arr[3].substring(1));
        	webLogBean.setRequest(arr[6]);
        	webLogBean.setStatus(arr[8]);
        	webLogBean.setBody_bytes_sent(arr[9]);
        	webLogBean.setHttp_referer(arr[10]);
            
            if (arr.length > 12) {
            	webLogBean.setHttp_user_agent(arr[11] + " " + arr[12]);
            } else {
            	webLogBean.setHttp_user_agent(arr[11]);
            }
            if (Integer.parseInt(webLogBean.getStatus()) >= 400) {// 大于400，HTTP错误
            	webLogBean.setValid(false);
            }
        } else {
        	webLogBean.setValid(false);
        }
        return webLogBean;
    }
   
    public static String parserTime(String time) {
    	
    	time.replace("/", "-");
    	return time;
    	
    }
}
```

#### 4.5.2.3 MapReduce程序

```java
public class WeblogPreProcess {

	static class WeblogPreProcessMapper extends Mapper<LongWritable, Text, Text, NullWritable> {
		Text k = new Text();
		NullWritable v = NullWritable.get();

		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			String line = value.toString();
			WebLogBean webLogBean = WebLogParser.parser(line);
			if (!webLogBean.isValid())
				return;
			k.set(webLogBean.toString());
			context.write(k, v);
		}
	}

	public static void main(String[] args) throws Exception {	
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf);
		job.setJarByClass(WeblogPreProcess.class);
		job.setMapperClass(WeblogPreProcessMapper.class);
		
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(NullWritable.class);
		
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		
		job.waitForCompletion(true);		
	}
}
```

## 4.6 大量小文件

### 4.6.1 需求

无论hdfs还是mapreduce，对于小文件都有损效率，实践中，又难免面临处理大量小文件的场景，此时，就需要有相应解决方案。

### 4.6.2 分析

小文件的优化无非以下几种方式：

- 在数据采集的时候，就将小文件或小批数据合成大文件再上传HDFS

- 在业务处理之前，在HDFS上使用MapReduce程序对小文件进行合并

- 在MapReduce处理时，可采用combineInputFormat提高效率

### 4.6.3 实现方案：在HDFS上使用MapReduce程序对小文件进行合并

程序的核心机制：

- 自定义一个InputFormat

- 改写RecordReader，实现一次读取一个完整文件封装为KV

- 在输出时使用SequenceFileOutPutFormat输出合并文件

#### 4.6.3.1 自定义InputFormat

```java
public class WholeFileInputFormat extends FileInputFormat<NullWritable, BytesWritable> {
	//设置每个小文件不可分片,保证一个小文件生成一个key-value键值对
	@Override
	protected boolean isSplitable(JobContext context, Path file) {
		return false;
	}

	@Override
	public RecordReader<NullWritable, BytesWritable> createRecordReader(
			InputSplit split, TaskAttemptContext context) throws IOException,
			InterruptedException {
		WholeFileRecordReader reader = new WholeFileRecordReader();
		reader.initialize(split, context);
		return reader;
	}
}
```

#### 4.6.3.2 自定义RecordReader

```java
class WholeFileRecordReader extends RecordReader<NullWritable, BytesWritable> {
	private FileSplit fileSplit;
	private Configuration conf;
	private BytesWritable value = new BytesWritable();
	private boolean processed = false;

	@Override
	public void initialize(InputSplit split, TaskAttemptContext context)
			throws IOException, InterruptedException {
		this.fileSplit = (FileSplit) split;
		this.conf = context.getConfiguration();
	}

	@Override
	public boolean nextKeyValue() throws IOException, InterruptedException {
		if (!processed) {
			byte[] contents = new byte[(int) fileSplit.getLength()];
			Path file = fileSplit.getPath();
			FileSystem fs = file.getFileSystem(conf);
			FSDataInputStream in = null;
			try {
				in = fs.open(file);
				IOUtils.readFully(in, contents, 0, contents.length);
				value.set(contents, 0, contents.length);
			} finally {
				IOUtils.closeStream(in);
			}
			processed = true;
			return true;
		}
		return false;
	}

	@Override
	public NullWritable getCurrentKey() throws IOException,
			InterruptedException {
		return NullWritable.get();
	}

	@Override
	public BytesWritable getCurrentValue() throws IOException,
			InterruptedException {
		return value;
	}

	@Override
	public float getProgress() throws IOException {
		return processed ? 1.0f : 0.0f;
	}

	@Override
	public void close() throws IOException {
		// do nothing
	}
}
```

#### 4.6.3.3 定义mapreduce处理流程

```java
public class SmallFilesToSequenceFileConverter extends Configured implements
		Tool {
	static class SequenceFileMapper extends Mapper<NullWritable, BytesWritable, Text, BytesWritable> {
		private Text filenameKey;

		@Override
		protected void setup(Context context) throws IOException,
				InterruptedException {
			InputSplit split = context.getInputSplit();
			Path path = ((FileSplit) split).getPath();
			filenameKey = new Text(path.toString());
		}

		@Override
		protected void map(NullWritable key, BytesWritable value,
				Context context) throws IOException, InterruptedException {
			context.write(filenameKey, value);
		}
	}

	@Override
	public int run(String[] args) throws Exception {
		Configuration conf = new Configuration();
		System.setProperty("HADOOP_USER_NAME", "hdfs");
		String[] otherArgs = new GenericOptionsParser(conf, args)
				.getRemainingArgs();
		if (otherArgs.length != 2) {
			System.err.println("Usage: combinefiles <in> <out>");
			System.exit(2);
		}
		
		Job job = Job.getInstance(conf,"combine small files to sequencefile");
//		job.setInputFormatClass(WholeFileInputFormat.class);
		job.setOutputFormatClass(SequenceFileOutputFormat.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(BytesWritable.class);
		job.setMapperClass(SequenceFileMapper.class);
		return job.waitForCompletion(true) ? 0 : 1;
	}

	public static void main(String[] args) throws Exception {
		int exitCode = ToolRunner.run(new SmallFilesToSequenceFileConverter(),
				args);
		System.exit(exitCode);		
	}
}
```

## 4.7 输出增强处理

### 4.7.1 需求

现有一些原始日志需要做增强解析处理，流程：

1. 从原始日志文件中读取数据
2. 根据日志中的一个URL字段到外部知识库中获取信息增强到原始日志
3. 如果成功增强，则输出到增强结果目录；如果增强失败，则抽取原始数据中URL字段输出到待爬清单目录

### 4.7.2 分析

程序的关键点是要在一个MapReduce程序中根据数据的不同输出两类结果到不同目录，这类灵活的输出需求可以通过自定义outputformat来实现。

### 4.7.3 实现

实现要点：

1. 在MapReduce中访问外部资源
2. 自定义outputformat，改写其中的recordwriter，改写具体输出数据的方法write()

#### 4.7.3.1 数据库获取数据

```java
public class DBLoader {

	public static void dbLoader(HashMap<String, String> ruleMap) {
		Connection conn = null;
		Statement st = null;
		ResultSet res = null;
		
		try {
			Class.forName("com.mysql.jdbc.Driver");
			conn = DriverManager.getConnection("jdbc:mysql://hdp-node01:3306/urlknowledge", "root", "root");
			st = conn.createStatement();
			res = st.executeQuery("select url,content from urlcontent");
			while (res.next()) {
				ruleMap.put(res.getString(1), res.getString(2));
			}
		} catch (Exception e) {
			e.printStackTrace();
			
		} finally {
			try{
				if(res!=null){
					res.close();
				}
				if(st!=null){
					st.close();
				}
				if(conn!=null){
					conn.close();
				}

			}catch(Exception e){
				e.printStackTrace();
			}
		}
	}
	
	
	public static void main(String[] args) {
		DBLoader db = new DBLoader();
		HashMap<String, String> map = new HashMap<String,String>();
		db.dbLoader(map);
		System.out.println(map.size());
	}
}
```

#### 4.7.3.2 自定义outputformat

```java
public class LogEnhancerOutputFormat extends FileOutputFormat<Text, NullWritable>{

	@Override
	public RecordWriter<Text, NullWritable> getRecordWriter(TaskAttemptContext context) throws IOException, InterruptedException {
		FileSystem fs = FileSystem.get(context.getConfiguration());
		Path enhancePath = new Path("hdfs://hdp-node01:9000/flow/enhancelog/enhanced.log");
		Path toCrawlPath = new Path("hdfs://hdp-node01:9000/flow/tocrawl/tocrawl.log");
		
		FSDataOutputStream enhanceOut = fs.create(enhancePath);
		FSDataOutputStream toCrawlOut = fs.create(toCrawlPath);
		return new MyRecordWriter(enhanceOut,toCrawlOut);
	}
	
	
	
	static class MyRecordWriter extends RecordWriter<Text, NullWritable>{
		
		FSDataOutputStream enhanceOut = null;
		FSDataOutputStream toCrawlOut = null;
		
		public MyRecordWriter(FSDataOutputStream enhanceOut, FSDataOutputStream toCrawlOut) {
			this.enhanceOut = enhanceOut;
			this.toCrawlOut = toCrawlOut;
		}

		@Override
		public void write(Text key, NullWritable value) throws IOException, InterruptedException {
			 
			//有了数据，你来负责写到目的地  —— hdfs
			//判断，进来内容如果是带tocrawl的，就往待爬清单输出流中写 toCrawlOut
			if(key.toString().contains("tocrawl")){
				toCrawlOut.write(key.toString().getBytes());
			}else{
				enhanceOut.write(key.toString().getBytes());
			}	
		}

		@Override
		public void close(TaskAttemptContext context) throws IOException, InterruptedException {
			if(toCrawlOut!=null){
				toCrawlOut.close();
			}
			if(enhanceOut!=null){
				enhanceOut.close();
			}	
		}		
	}
}
```

#### 4.7.3.3 MapReduce

```java
/**
 * 这个程序是对每个小时不断产生的用户上网记录日志进行增强(将日志中的url所指向的网页内容分析结果信息追加到每一行原始日志后面)
 * 
 * @author
 * 
 */
public class LogEnhancer {
	static class LogEnhancerMapper extends Mapper<LongWritable, Text, Text, NullWritable> {
		HashMap<String, String> knowledgeMap = new HashMap<String, String>();

		/**
		 * maptask在初始化时会先调用setup方法一次 利用这个机制，将外部的知识库加载到maptask执行的机器内存中
		 */
		@Override
		protected void setup(org.apache.hadoop.mapreduce.Mapper.Context context) throws IOException, InterruptedException {
			DBLoader.dbLoader(knowledgeMap);
		}

		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String line = value.toString();
			String[] fields = StringUtils.split(line, "\t");
			try {
				String url = fields[26];
				// 对这一行日志中的url去知识库中查找内容分析信息
				String content = knowledgeMap.get(url);

				// 根据内容信息匹配的结果，来构造两种输出结果
				String result = "";
				if (null == content) {
					// 输往待爬清单的内容
					result = url + "\t" + "tocrawl\n";
				} else {
					// 输往增强日志的内容
					result = line + "\t" + content + "\n";
				}

				context.write(new Text(result), NullWritable.get());
			} catch (Exception e) {

			}
		}

	}

	public static void main(String[] args) throws Exception {

		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf);
		job.setJarByClass(LogEnhancer.class);
		job.setMapperClass(LogEnhancerMapper.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(NullWritable.class);

		// 要将自定义的输出格式组件设置到job中
		job.setOutputFormatClass(LogEnhancerOutputFormat.class);

		FileInputFormat.setInputPaths(job, new Path(args[0]));

		// 虽然我们自定义了outputformat，但是因为我们的outputformat继承自fileoutputformat
		// 而fileoutputformat要输出一个_SUCCESS文件，所以，在这还得指定一个输出目录
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.waitForCompletion(true);
		System.exit(0);
	}
}
```

## 4.8 求出每一个订单中成交金额最大的一笔交易

### 4.8.1 需求

有如下订单数据

| 订单id        | 商品id | 成交金额 |
| ------------- | ------ | -------- |
| Order_0000001 | Pdt_01 | 222.8    |
| Order_0000001 | Pdt_05 | 25.8     |
| Order_0000002 | Pdt_03 | 522.8    |
| Order_0000002 | Pdt_04 | 122.4    |
| Order_0000003 | Pdt_01 | 222.8    |

现在需要求出每一个订单中成交金额最大的一笔交易

### 4.8.2 分析

1. 利用“订单id和成交金额”作为key，可以将map阶段读取到的所有订单数据按照id分区，按照金额排序，发送到reduce

2. 在reduce端利用groupingcomparator将订单id相同的kv聚合成组，然后取第一个即是最大值。

### 4.8.3 实现

#### 4.8.3.1 自定义groupingcomparator

```java
/**
 * 用于控制shuffle过程中reduce端对kv对的聚合逻辑
 * @author duanhaitao@itcast.cn
 *
 */
public class ItemidGroupingComparator extends WritableComparator {

	protected ItemidGroupingComparator() {
		super(OrderBean.class, true);
	}
	
	@Override
	public int compare(WritableComparable a, WritableComparable b) {
		OrderBean abean = (OrderBean) a;
		OrderBean bbean = (OrderBean) b;	
		//将item_id相同的bean都视为相同，从而聚合为一组
		return abean.getItemid().compareTo(bbean.getItemid());
	}
}
```

#### 4.8.3.2 定义订单信息bean

```java
/**
 * 订单信息bean，实现hadoop的序列化机制
 * @author duanhaitao@itcast.cn
 *
 */
public class OrderBean implements WritableComparable<OrderBean>{
	private Text itemid;
	private DoubleWritable amount;

	public OrderBean() {
	}
	public OrderBean(Text itemid, DoubleWritable amount) {
		set(itemid, amount);
	}

	public void set(Text itemid, DoubleWritable amount) {
		this.itemid = itemid;
		this.amount = amount;

	}

	public Text getItemid() {
		return itemid;
	}

	public DoubleWritable getAmount() {
		return amount;
	}

	@Override
	public int compareTo(OrderBean o) {
		int cmp = this.itemid.compareTo(o.getItemid());
		if (cmp == 0) {
			cmp = -this.amount.compareTo(o.getAmount());
		}
		return cmp;
	}

	@Override
	public void write(DataOutput out) throws IOException {
		out.writeUTF(itemid.toString());
		out.writeDouble(amount.get());
		
	}

	@Override
	public void readFields(DataInput in) throws IOException {
		String readUTF = in.readUTF();
		double readDouble = in.readDouble();
		
		this.itemid = new Text(readUTF);
		this.amount= new DoubleWritable(readDouble);
	}


	@Override
	public String toString() {
		return itemid.toString() + "\t" + amount.get();
	}
}
```

#### 4.8.3.3 mapreduce

```java
/**
 * 利用secondarysort机制输出每种item订单金额最大的记录
 * @author duanhaitao@itcast.cn
 *
 */
public class SecondarySort {
	
	static class SecondarySortMapper extends Mapper<LongWritable, Text, OrderBean, NullWritable>{
		
		OrderBean bean = new OrderBean();
		
		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String line = value.toString();
			String[] fields = StringUtils.split(line, "\t");
			bean.set(new Text(fields[0]), new DoubleWritable(Double.parseDouble(fields[1])));
			context.write(bean, NullWritable.get());
			
		}
		
	}
	
	static class SecondarySortReducer extends Reducer<OrderBean, NullWritable, OrderBean, NullWritable>{
		//在设置了groupingcomparator以后，这里收到的kv数据 就是：  <1001 87.6>,null  <1001 76.5>,null  .... 
		//此时，reduce方法中的参数key就是上述kv组中的第一个kv的key：<1001 87.6>
		//要输出同一个item的所有订单中最大金额的那一个，就只要输出这个key
		@Override
		protected void reduce(OrderBean key, Iterable<NullWritable> values, Context context) throws IOException, InterruptedException {
			context.write(key, NullWritable.get());
		}
	}
	
	
	public static void main(String[] args) throws Exception {
		
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf);
		
		job.setJarByClass(SecondarySort.class);
		
		job.setMapperClass(SecondarySortMapper.class);
		job.setReducerClass(SecondarySortReducer.class);
		
		
		job.setOutputKeyClass(OrderBean.class);
		job.setOutputValueClass(NullWritable.class);
		
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		//指定shuffle所使用的GroupingComparator类
		job.setGroupingComparatorClass(ItemidGroupingComparator.class);
		//指定shuffle所使用的partitioner类
		job.setPartitionerClass(ItemIdPartitioner.class);
		
		job.setNumReduceTasks(3);
		
		job.waitForCompletion(true);	
	}
}
```

## 4.9 计数器

### 4.9.1 需求

在实际生产代码中，常常需要将数据处理过程中遇到的不合规数据行进行全局计数，类似这种需求可以借助mapreduce框架中提供的全局计数器来实现

### 4.9.2 实现

```java
public class MultiOutputs {
	//通过枚举形式定义自定义计数器
	enum MyCounter{MALFORORMED,NORMAL}

	static class CommaMapper extends Mapper<LongWritable, Text, Text, LongWritable> {
		@Override
		protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String[] words = value.toString().split(",");
			for (String word : words) {
				context.write(new Text(word), new LongWritable(1));
			}
			//对枚举定义的自定义计数器加1
			context.getCounter(MyCounter.MALFORORMED).increment(1);
			//通过动态设置自定义计数器加1
			context.getCounter("counterGroupa", "countera").increment(1);
		}
    }
}
```

## 4.10 多job串联

### 4.10.1 需求

一个稍复杂点的处理逻辑往往需要多个mapreduce程序串联处理，多job的串联可以借助mapreduce框架的JobControl实现

### 4.10.2 实现

```java
ControlledJob cJob1 = new ControlledJob(job1.getConfiguration());
ControlledJob cJob2 = new ControlledJob(job2.getConfiguration());
ControlledJob cJob3 = new ControlledJob(job3.getConfiguration());

// 设置作业依赖关系
cJob2.addDependingJob(cJob1);
cJob3.addDependingJob(cJob2);

JobControl jobControl = new JobControl("RecommendationJob");
jobControl.addJob(cJob1);
jobControl.addJob(cJob2);
jobControl.addJob(cJob3);

cJob1.setJob(job1);
cJob2.setJob(job2);
cJob3.setJob(job3);

// 新建一个线程来运行已加入JobControl中的作业，开始进程并等待结束
Thread jobControlThread = new Thread(jobControl);
jobControlThread.start();
while (!jobControl.allFinished()) {
    Thread.sleep(500);
}
jobControl.stop();
return 0;
```

# 5 MapReduce参数优化

## 5.1 资源相关参数

- `mapreduce.map.memory.mb`: 一个Map Task可使用的资源上限（单位:MB），默认为1024。如果Map Task实际使用的资源量超过该值，则会被强制杀死。

- `mapreduce.reduce.memory.mb`: 一个Reduce Task可使用的资源上限（单位:MB），默认为1024。如果Reduce Task实际使用的资源量超过该值，则会被强制杀死。

- `mapreduce.map.java.opts`: Map Task的JVM参数，你可以在此配置默认的java heap size等参数, e.g.
  -. x1024m -verbose:gc -Xloggc:/tmp/@taskid@.gc” （@taskid@会被Hadoop框架自动换为相应的taskid）, 默认值: “”

- `mapreduce.reduce.java.opts`: Reduce Task的JVM参数，你可以在此配置默认的java heap size等参数, e.g.
  -. x1024m -verbose:gc -Xloggc:/tmp/@taskid@.gc”, 默认值: “”

- `mapreduce.map.cpu.vcores`: 每个Map task可使用的最多cpu core数目, 默认值: 1

- `mapreduce.reduce.cpu.vcores`: 每个Reduce task可使用的最多cpu core数目, 默认值: 1

## 5.2 容错相关参数

- `mapreduce.map.maxattempts`: 每个Map Task最大重试次数，一旦重试参数超过该值，则认为Map Task运行失败，默认值：4。

- `mapreduce.reduce.maxattempts`: 每个Reduce Task最大重试次数，一旦重试参数超过该值，则认为Map Task运行失败，默认值：4。

- `mapreduce.map.failures.maxpercent`: 当失败的Map Task失败比例超过该值为，整个作业则失败，默认值为0. 如果你的应用程序允许丢弃部分输入数据，则该该值设为一个大于0的值，比如5，表示如果有低于5%的Map Task失败（如果一个Map Task重试次数超过mapreduce.map.maxattempts，则认为这个Map Task失败，其对应的输入数据将不会产生任何结果），整个作业扔认为成功。

- `mapreduce.reduce.failures.maxpercent`: 当失败的Reduce Task失败比例超过该值为，整个作业则失败，默认值为0.

- `mapreduce.task.timeout`: Task超时时间，经常需要设置的一个参数，该参数表达的意思为：如果一个task在一定时间内没有任何进入，即不会读取新的数据，也没有输出数据，则认为该task处于block状态，可能是卡住了，也许永远会卡主，为了防止因为用户程序永远block住不退出，则强制设置了一个该超时时间（单位毫秒），默认是300000。如果你的程序对每条输入数据的处理时间过长（比如会访问数据库，通过网络拉取数据等），建议将该参数调大，该参数过小常出现的错误提示是“AttemptID:attempt_14267829456721_123456_m_000224_0 Timed out after 300 secsContainer killed by the ApplicationMaster.”。

## 5.3 本地运行mapreduce 作业

```
mapreduce.framework.name=local
mapreduce.jobtracker.address=local
fs.defaultFS=local
```

## 5.4 效率和稳定性相关参数

- `mapreduce.map.speculative`: 是否为Map Task打开推测执行机制，默认为false
- `mapreduce.reduce.speculative`: 是否为Reduce Task打开推测执行机制，默认为false
- `mapreduce.job.user.classpath.first` & `mapreduce.task.classpath.user.precedence`：当同一个class同时出现在用户jar包和hadoop jar中时，优先使用哪个jar包中的class，默认为false，表示优先使用hadoop jar中的class。
- `mapreduce.input.fileinputformat.split.minsize`: 每个Map Task处理的数据量（仅针对基于文件的Inputformat有效，比如TextInputFormat，SequenceFileInputFormat），默认为一个block大小，即 134217728。