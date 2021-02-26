# Hive

# 1 Hive简介

## 1.1 什么是Hive

Hive是基于Hadoop的一个数据仓库工具，可以将结构化的数据文件映射为一张数据库表，并提供类SQL查询功能。

## 1.2 为什么要用Hive

直接使用hadoop所面临的问题：

- 人员学习成本太高

- 项目周期要求太短

- MapReduce实现复杂查询逻辑开发难度太大

 

为什么要使用Hive ：

- 操作接口采用类SQL语法，提供快速开发的能力。

- 避免了去写MapReduce，减少开发人员的学习成本。 

- 扩展功能很方便。

## 1.3 Hive的特点

- 可扩展 ：Hive可以自由的扩展集群的规模，一般情况下不需要重启服务。

- 延展性 ：Hive支持用户自定义函数，用户可以根据自己的需求来实现自己的函数。

- 容错 ：良好的容错性，节点出现问题SQL仍可完成执行。

## 1.4 Hive架构

![image-20201231163232922](./media/hadoop_hive_20201231163232922.png)

- Jobtracker是hadoop1.x中的组件，它的功能相当于： Resourcemanager+AppMaster

- TaskTracker 相当于：  Nodemanager  +  yarnchild

基本组成:

- 用户接口：
  - CLI：shell命令行
  - JDBC/ODBC：Hive的JAVA实现，与传统数据库JDBC类似
  - WebGUI：通过浏览器访问Hive
- 元数据存储：
  - Hive 将元数据存储在数据库中，通常是存储在关系数据库如 mysql , derby中。
  - Hive 中的元数据包括表的名字，表的列和分区及其属性，表的属性（是否为外部表等），表的数据所在目录等。
- 解释器、编译器、优化器、执行器：完成 HQL 查询语句从词法分析、语法分析、编译、优化以及查询计划的生成。
  - 生成的查询计划存储在 HDFS 中，并在随后有 MapReduce 调用执行。

## 1.5 Hive与Hadoop的关系

Hive利用HDFS存储数据，利用MapReduce查询数据

![image-20201231164128441](./media/hadoop_hive_20201231164128441.png)

## 1.6 Hive与传统数据库对比

hive具有sql数据库的外表，但应用场景完全不同，hive只适合用来做批量数据统计分析

![image-20201231164304974](./media/hadoop_hive_20201231164304974.png)

## 1.7 Hive的数据存储

- Hive中所有的数据都存储在 HDFS 中，没有专门的数据存储格式（可支持Text，SequenceFile，ParquetFile，RCFILE等）
- 只需要在创建表的时候告诉 Hive 数据中的列分隔符和行分隔符，Hive 就可以解析数据。
- Hive 中包含以下数据模型：DB、Table，External Table，Partition，Bucket。
  - DB：在HDFS中表现为`${hive.metastore.warehouse.dir}`目录下一个文件夹
  - Table：在HDFS中表现所属DB目录下一个文件夹
  - External Table：外部表, 与Table类似，不过其数据存放位置可以在任意指定路径
    - 普通表: 删除表后, HDFS上的文件都删了
    - External外部表删除后, HDFS上的文件没有删除, 只是把文件删除了
  - Partition：在HDFS中表现为Table目录下的子目录
  - Bucket：桶, 在HDFS中表现为同一个表目录下根据hash散列之后的多个文件, 会根据不同的文件把数据放到不同的文件中