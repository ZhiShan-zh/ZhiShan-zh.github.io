# Hadoop概述

# 1 Hadoop简介

## 1.1 什么是Hadoop

1. Hadoop是apache旗下的一套开源软件平台
2. Hadoop提供的功能：利用服务器集群，根据用户的自定义业务逻辑，对海量数据进行分布式处理
3. Hadoop的核心组件有
    - HDFS：分布式文件系统
    - YARN：运算资源调度系统
    - MAPREDUCE：分布式运算编程框架
4. 广义上来说，Hadoop通常是指一个更广泛的概念——Hadoop生态圈

## 1.2 Hadoop产生背景

1. Hadoop最早起源于Nutch。Nutch的设计目标是构建一个大型的全网搜索引擎，包括网页抓取、索引、查询等功能，但随着抓取网页数量的增加，遇到了严重的可扩展性问题——如何解决数十亿网页的存储和索引问题。
2. 2003年、2004年谷歌发表的两篇论文为该问题提供了可行的解决方案。

    - 分布式文件系统（GFS），可用于处理海量网页的存储

    - 分布式计算框架MAPREDUCE，可用于处理海量网页的索引计算问题。

3. Nutch的开发人员完成了相应的开源实现HDFS和MAPREDUCE，并从Nutch中剥离成为独立项目Hadoop，到2008年1月，Hadoop成为Apache顶级项目，迎来了它的快速发展期。

## 1.3 Hadoop在大数据、云计算中的位置和关系

1. 云计算是分布式计算、并行计算、网格计算、多核计算、网络存储、虚拟化、负载均衡等传统计算机技术和互联网技术融合发展的产物。借助IaaS(基础设施即服务)、PaaS(平台即服务)、SaaS（软件即服务）等业务模式，把强大的计算能力提供给终端用户。
2. 现阶段，云计算的两大底层支撑技术为“虚拟化”和“大数据技术”
3. 而Hadoop则是云计算的PaaS层的解决方案之一，并不等同于PaaS，更不等同于云计算本身。

## 1.4 Hadoop生态圈以及各组成部分的简介

- **HDFS**：分布式文件系统
- **MapReduce**：分布式运算程序开发框架
- **Hive**：基于大数据技术（文件系统+运算框架）的SQL数据仓库工具
- **HBase**：基于HADOOP的分布式海量数据库
- **Zookeeper**：分布式协调服务基础组件
- **Mahout**：基于MapReduce/Spark/Flink等分布式运算框架的机器学习算法库
- **Oozie**：工作流调度框架
- **Sqoop**：(发音：skup)，数据导入导出工具，是一款开源的工具，主要用于在Hadoop(Hive)与传统的数据库(mysql、postgresql...)间进行数据的传递，可以将一个关系型数据库*（例如 ： MySQL ,Oracle ,Postgres等）*中的数据导进到Hadoop的HDFS中，也可以将HDFS的数据导进到关系型数据库中。
- **Flume**：日志数据采集框架

# 2 大数据技术应用示例：Web日志数据挖掘

注：本环节主要感受数据分析系统的宏观概念及处理流程，初步理解hadoop等框架在其中的应用环节，不用过于关注代码细节。

## 2.1 项目概述

“Web点击流日志”包含着网站运营很重要的信息，通过日志分析，我们可以知道网站的访问量，哪个网页访问人数最多，哪个网页最有价值，广告转化率、访客的来源信息，访客的终端信息等。

- 一般中型的网站(10W的PV以上)，每天会产生1G以上Web日志文件。大型或超大型的网站，可能每小时就会产生10G的数据量。
- 具体来说，比如某电子商务网站，在线团购业务。每日PV数100w，独立IP数5w。用户通常在工作日上午10:00-12:00和下午15:00-18:00访问量最大。日间主要是通过PC端浏览器访问，休息日及夜间通过移动设备访问较多。网站搜索浏量占整个网站的80%，PC用户不足1%的用户会消费，移动用户有5%会消费。

- 对于日志的这种规模的数据，用HADOOP进行日志分析，是最适合不过的了。

## 2.2 数据来源

- 目标：本案例的数据主要由用户的点击行为记录
- 获取方式：在页面预埋一段js程序，为页面上想要监听的标签绑定事件，只要用户点击或移动到标签，即可触发ajax请求到后台servlet程序，用log4j记录下事件信息，从而在web服务器（nginx、tomcat等）上形成不断增长的日志文件。

## 2.3 数据处理流程

### 2.3.1 数据处理流程图

![image-20200721171618305](https://zhishan-zh.github.io/media/bigdata_Data_processing_flow_20200721171618305.png)

1. 数据采集：定制开发采集程序，或使用开源框架Flume
2. 数据预处理：定制开发MapReduce程序运行于hadoop集群
3. 数据仓库技术：基于hadoop之上的Hive
4. 数据导出：基于hadoop的Sqoop数据导入导出工具
5. 数据可视化：定制开发web程序或使用kettle等产品
6. 整个过程的流程调度：hadoop生态圈中的oozie工具或其他类似开源产品

### 2.3.2 项目技术架构图

![image-20200721172108890](https://zhishan-zh.github.io/media/bigdata_technology_20200721172108890.png)

# 3 Hadoop配置

如果配置目录被重新放在文件系统的其他地方（Hadoop安装在外面，以便升级），但是守护进程启动时需要使用--config选项，以指向本地文件系统的目录。

| 配置文件                                            | 说明                                                         |
| --------------------------------------------------- | ------------------------------------------------------------ |
| `hadoop-2.9.2/etc/hadoop/hadoop-env.sh`             | Hadoop运行中需要用到的环境变量。对文件的运行环境进行配置，hadoop是基于java的，所以同样需要JDK |
| `hadoop-2.9.2/etc/hadoop/core-site.xml`             | hadoop的核心配置文件，配置指定集群NameNode，设置hadoop公用变量，创建hadoop的临时目录等。Hadoop Core的配置项，例如HDFS和MapReduce常用的I/O设置等 |
| `hadoop-2.9.2/etc/hadoop/hdfs-site.xml`             | 分布式文件系统配置，包含对存储文件时的文件设置，比如副本数量。配置DataNode的本地路径，dataNode节点路径等。Hadoop守护进程的配置项，包括namenode, secondary namenode, 和datanode等 |
| `hadoop-2.9.2/etc/hadoop/mapred-site.xml`           | MapReduce守护进程的配置项，包括jobtracker和tasktracker       |
| `hadoop-2.9.2/etc/hadoop/master`                    | 并不是所有的配置文件中都包含这个文件，运行secondary namenode的机器列表的IP，一个一行 |
| `hadoop-2.9.2/etc/hadoop/slaves`                    | 运行datanode和tasktracker的机器列表IP，一个一行              |
| `hadoop-2.9.2/etc/hadoop/hadoop-metrics.properties` | 控制如何在Hadoop上发布度量的属性                             |
| `hadoop-2.9.2/etc/hadoop/log4j.properties`          | 系统日志文件、namenode审计日志，tasktracker子进程的任务日志的属性 |
| `hadoop-2.9.2/etc/hadoop/yarn-site.xml`             | 配置yarn，yarn用于管理分布式系统的CPU利用率，磁盘使用情况等。shuffle过程使用的执行器（可以使用不同的执行器，比如spark） |

## 3.1 `hadoop-env.sh`

`hadoop-env.sh`文件中定义了Hadoop运行时使用的环境变量，其中只有`JAVA_HOME`环境变量是用户需要配置的，使之指向Java安装目录。其它环境变量在默认配置下都可以很好的工作。在逐步熟悉Hadoop后，可以通过修改这个文件来做个性化设置（如日志目录的位置、Java类所在目录等）。

- `HADOOP_LOG_DIR`：日志文件的存放目录，可以设置为`/var/log/hadoop`
- `HADOOP_SLAVES`：slaves文件的位置，一般无需修改
- `HADOOP_SSH_OPTS`：P335
- `HADOOP_SLAVE_SLEEP`：P335
- `HADOOP_IDEN_STRING`：影响日志文件的名称

`hadoop-2.9.2/etc/hadoop/hadoop-env.sh`文件详解：

```shell
# Set Hadoop-specific environment variables here.
# 在这里设置Hadoop具体的环境变量

# The only required environment variable is JAVA_HOME.  All others are
# optional.  When running a distributed configuration it is best to
# set JAVA_HOME in this file, so that it is correctly defined on
# remote nodes.
# JAVA_HOME是唯一一个必须要设置的环境变量。其余的均为可选项。在运行分布式配置时，最好在此文件中设置JAVA_HOME，以便在远程节点上正确定义它。


# The java implementation to use.
export JAVA_HOME=${JAVA_HOME}

# The jsvc implementation to use. Jsvc is required to run secure datanodes
# that bind to privileged ports to provide authentication of data transfer
# protocol.  Jsvc is not required if SASL is configured for authentication of
# data transfer protocol using non-privileged ports.
#export JSVC_HOME=${JSVC_HOME}

# 配置文件的路径，如果HADOOP_CONF_DIR没有值时，会赋予默认值/etc/hadoop
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-"/etc/hadoop"}

# Extra Java CLASSPATH elements.  Automatically insert capacity-scheduler.
for f in $HADOOP_HOME/contrib/capacity-scheduler/*.jar; do
  if [ "$HADOOP_CLASSPATH" ]; then
    export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$f
  else
    export HADOOP_CLASSPATH=$f
  fi
done

# The maximum amount of heap to use, in MB. Default is 1000.
# 分配给各个守护进程的内存大小，单位是MB，默认为1000MB
# 另外，可以使用HADOOP_NAMENODE_OPTS等单独设置某一守护进行的内存大小
# 大型集群一般设置2000M或以上，开发环境中设置500M足够了。
# namenode,secondarynamenode,jobtracker,datanode,tasktracker守护进程内存
#export HADOOP_HEAPSIZE=
# NameNode的初始化堆内存大小，默认也是1000M
#export HADOOP_NAMENODE_INIT_HEAPSIZE=""

# Enable extra debugging of Hadoop's JAAS binding, used to set up
# Kerberos security.
# 设置jaas绑定、开启Kerberos 安全认证
# export HADOOP_JAAS_DEBUG=true

# Extra Java runtime options.  Empty by default.
# For Kerberos debugging, an extended option set logs more invormation
# export HADOOP_OPTS="-Djava.net.preferIPv4Stack=true -Dsun.security.krb5.debug=true -Dsun.security.spnego.debug"
# 使用Ipv4禁用Ipv6
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"

# 大部分情况下，这个统一设置的值可能并不适合。例如对于namenode节点，
# 1000M的内存只能存储几百万个文件的数据块的引用。
# 单独设置namenode、secondrynamenode、datanode、blancer 、jobtrackerde 的内存，可以通过下面的参数来设置
HADOOP_NAMENODE_OPTS=2048
HADOOP_SECONDARYNAMENODE_OPTS
HADOOP_DATANODE_OPTS
HADOOP_BALANCER_OPTS
HADOOP_JOBTRACKER_OPTS

# Command specific options appended to HADOOP_OPTS when specified
# DataNode、NameNode、secondrynamenode、nfs3、 的JVM参数设置
export HADOOP_NAMENODE_OPTS="-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} -Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,NullAppender} $HADOOP_NAMENODE_OPTS"
export HADOOP_DATANODE_OPTS="-Dhadoop.security.logger=ERROR,RFAS $HADOOP_DATANODE_OPTS"

export HADOOP_SECONDARYNAMENODE_OPTS="-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} -Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,NullAppender} $HADOOP_SECONDARYNAMENODE_OPTS"

export HADOOP_NFS3_OPTS="$HADOOP_NFS3_OPTS"
# 这个是在HDFS格式化时需要的JVM配置，也就是执行hdfs namenode -format时的JVM配置　
export HADOOP_PORTMAP_OPTS="-Xmx512m $HADOOP_PORTMAP_OPTS"

# The following applies to multiple commands (fs, dfs, fsck, distcp etc)
# 设置HADOOP_CLIENT参数    fs, dfs, fsck,distcp etc 命令涉及
export HADOOP_CLIENT_OPTS="$HADOOP_CLIENT_OPTS"
# set heap args when HADOOP_HEAPSIZE is empty
# 如果未设置HADOOP_CLIENT_OPTS，则会设置默认值512m
if [ "$HADOOP_HEAPSIZE" = "" ]; then
  export HADOOP_CLIENT_OPTS="-Xmx512m $HADOOP_CLIENT_OPTS"
fi
#HADOOP_JAVA_PLATFORM_OPTS="-XX:-UsePerfData $HADOOP_JAVA_PLATFORM_OPTS"

# On secure datanodes, user to run the datanode as after dropping privileges.
# This **MUST** be uncommented to enable secure HDFS if using privileged ports
# to provide authentication of data transfer protocol.  This **MUST NOT** be
# defined if SASL is configured for authentication of data transfer protocol
# using non-privileged ports.
export HADOOP_SECURE_DN_USER=${HADOOP_SECURE_DN_USER}

# Where log files are stored.  $HADOOP_HOME/logs by default.
# 日志文件的存放目录。$HADOOP_HOME/logs为默认位置
#export HADOOP_LOG_DIR=${HADOOP_LOG_DIR}/$USER

# Where log files are stored in the secure data environment.
#export HADOOP_SECURE_DN_LOG_DIR=${HADOOP_LOG_DIR}/${HADOOP_HDFS_USER}

###
# HDFS Mover specific parameters
###
# Specify the JVM options to be used when starting the HDFS Mover.
# These options will be appended to the options specified as HADOOP_OPTS
# and therefore may override any similar flags set in HADOOP_OPTS
#
# export HADOOP_MOVER_OPTS=""

###
# Router-based HDFS Federation specific parameters
# Specify the JVM options to be used when starting the RBF Routers.
# These options will be appended to the options specified as HADOOP_OPTS
# and therefore may override any similar flags set in HADOOP_OPTS
#
# export HADOOP_DFSROUTER_OPTS=""
###

###
# Advanced Users Only!
###

# The directory where pid files are stored. /tmp by default.
# NOTE: this should be set to a directory that can only be written to by 
#       the user that will run the hadoop daemons.  Otherwise there is the
#       potential for a symlink attack.
# 配置hadoop pid文件路径
export HADOOP_PID_DIR=${HADOOP_PID_DIR}
export HADOOP_SECURE_DN_PID_DIR=${HADOOP_PID_DIR}

# A string representing this instance of hadoop. $USER by default.
# hadoop默认用户$USER为当前用户
export HADOOP_IDENT_STRING=$USER
```

## 3.2 Hadoop的工作模式

`core-site.xml`、`hdfs-site.xml`、`mapred-site.xml`、`yarn-site.xml`这几个配置文件的配置与Hadoop的工作模式有关：本地模式、伪分布式模式、分布式(集群)模式。

### 3.2.1 本地（单机）模式

单机模式是Hadoop的默认模式。当首次解压Hadoop的源码包时，Hadoop无法了解硬件安装环境，便保守地选择了最小配置。在这种默认模式下`core-site.xml`、`hdfs-site.xml`、`mapred-site.xml`文件均为空，即使用系统的缺省最小配置。

当配置文件为空时，Hadoop会完全运行在本地。因为不需要与其他节点交互，单机模式就不使用HDFS，也不加载任何Hadoop的守护进程。该模式**主要用于开发调试MapReduce程序的应用逻辑**。

`hadoop-2.9.2/etc/hadoop/core-site.xml`文件详解：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!-- Put site-specific property overrides in this file. -->
<configuration>
</configuration>
```

### 3.2.2 伪分布式模式

伪分布式模式在“单节点集群”上运行Hadoop， 所有的守护进程都运行在同一台机器上。**该模式在单机模式之上增加了代码调试功能，允许你检查内存使用的情况、HDFS输入输出，以及其它守护进程的交互**。

#### 3.2.2.1 `core-site.xml`配置

- `fs.defaultFS`：指定NameNode的主机名和端口号
- `hadoop.tmp.dir`：定义了临时目录，缺省为`/tmp/hadoop-${user.name}`。

```xml

<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
 
<!-- Put site-specific property overrides in this file. -->
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>file:/usr/local/hadoop/tmp</value>
        <description>A base for other temporary directories.</description>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

#### 3.2.2.2 `mapred-site.xml`配置

可以使用系统默认的最小配置。

#### 3.2.2.3 `hdfs-site.xml`配置

- `dfs.replication`：指定HDFS的默认副本数
    - 因为仅运行在一个节点上，这里副本数为1。
- `dfs.namenode.name.dir`：NameNode的工作目录。
- `dfs.datanode.data.dir`：DataNode的工作目录。

```xml

<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
 
<!-- Put site-specific property overrides in this file. -->
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/data</value>
    </property>
</configuration>
```

### 3.2.3 全分布式(集群)模式

集群模式能够充分利用分布式存储和分布式计算带来的好处。

#### 3.2.3.1 `core-site.xml`配置

既然Hadoop工作在集群下，那么工作在集群下的节点需要知道主节点master的主机和端口信息。

- `fs.defaultFS`：主节点master的主机和端口信息。
    - 对比伪分布式工作模式，主机名是使用的localhost，但集群模式下，需要为工作节点slave提供主节点的信息，这里使用的是主机名。因此我们需要提供主机名与IP地址之间的转换服务，可提供静态的DNS转换服务，通过修改`/etc/hosts`的配置来提供；另外一种就是提供动态的DNS服务器来负责主机名和IP地址的解析服务。
- `hadoop.tmp.dir`：定义了临时目录，缺省为`/tmp/hadoop-${user.name}`。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
 
<!-- Put site-specific property overrides in this file. -->
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>file:/usr/local/hadoop/tmp</value>
        <description>Abase for other temporary directories.</description>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop-master-vm:9000</value>
    </property>
</configuration>
```

#### 3.2.3.2 slaves

hadoop3.0 以后 slaves 更名为 workers 了。

一般在集群中你唯一地选择一台机器作为 NameNode ，一台机器作为 ResourceManager，这是 master  (主)。

那么 ，集群中剩下的机器作为 DataNode 和 NodeManager。这些是 slaves  (从)。

当主节点master启动时，需要启动工作节点slave的守护进程，这里就需要知道工作节点的地址信息，因此，我们需要在`$HADOOP_INSTALL/etc/hadoop`目录下提供slaves配置文件，提供slaves主机名列表。格式为每行一条主机名。

```
hadoop-slave_1
hadoop-slave_2
hadoop-slave_3
```

#### 3.2.3.3 `hdfs-site.xml`配置

我们可以配置Secondary NameNode，以提供NameNode的冗余。

- `dfs.replication`：指定HDFS的副本数
    - 在集群情况下，我们需要使用HDFS的冗余功能，因此副本配置就不像伪分布式模式那样设置为1，我们这里采取了缺省的副本数为3的配置。
    - 指定dataNode存储block的副本数量，默认值是3个，该值应该不大于4。
- `dfs.namenode.secondary.http-address`：secondary namenode HTTP服务器地址和端口。
- `dfs.namenode.name.dir`：NameNode的工作目录。
- `dfs.datanode.data.dir`：DataNode的工作目录。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
 
<!-- Put site-specific property overrides in this file. -->
<configuration>
    <property>
        <name>dfs.namenode.secondary.http-address</name>
        <value>hadoop-master:50090</value>
    </property>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/data</value>
    </property>
</configuration>
```

#### 3.2.3.4 第二代MapReduce框架Yarn配置

如果我们选择第二代MapReduce框架Yarn，那么需要修改`mapred-site.xml`和`yarn-site.xml`配置文件。在下面的mapred-site.xml配置文件中，我们提供了Job History的配置，以方便用户查询作业的历史信息。

`mapred-site.xml`配置：

- `mapreduce.framework.name`：执行框架设置
- `mapreduce.jobhistory.address`：
    - MapReduce作业历史信息IPC接口地址。
    - 对于当前工作模式为可选配置。
- `mapreduce.jobhistory.webapp.address`：
    - MapReduce作业历史信息HTTP接口地址。
    - 对于当前工作模式为可选配置。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
 
<!-- Put site-specific property overrides in this file. -->
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.address</name>
        <value>hadoop-master:10020</value>
    </property>
    <property>
        <name>mapreduce.jobhistory.webapp.address</name>
        <value>hadoop-master:19888</value>
    </property>
</configuration>
```

`yarn-site.xml`配置：

- `yarn.resourcemanager.hostname`：ResourceManager的主机名
- `yarn.nodemanager.aux-services`：NodeManager上运行的附属服务。需配置成mapreduce_shuffle，才可运行MapReduce程序。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
 
<configuration>
	<!-- Site specific YARN configuration properties -->
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>hadoop-master</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

# 4 Hadoop集群搭建

HADOOP集群具体来说包含两个集群：

- HDFS集群
    - 负责海量数据的存储，集群中的角色主要有NameNode、DataNode
- YARN集群
    - 负责海量数据运算时的资源调度，集群中的角色主要有ResourceManager、NodeManager
- 两者逻辑上分离，但物理上常在一起。

注意：mapreduce其实是一个应用程序开发包。



节点和角色分配：

- hdp-node-01    NameNode  SecondaryNameNode ResourceManager 
- hdp-node-02   DataNode   NodeManager
- hdp-node-03		DataNode   NodeManager



SSH免密登录原理：每台主机`authorized_keys`文件里面包含的主机（ssh密钥），该主机都能无密码登录，所以只要每台主机的`authorized_keys`文件里面都放入其他主机（需要无密码登录的主机）的ssh密钥就行了。

让Master节点可以无密码 SSH 登陆到各个 Slave 节点上：

- 首先生成 Master 节点的公匙，在 Master 节点的终端中执行

  ```shell
  cd ~/.ssh               # 如果没有该目录，先执行一次ssh localhost
  rm ./id_rsa*            # 删除之前生成的公匙（如果有）
  ssh-keygen -t rsa       # 一直按回车就可以
  cat ./id_rsa.pub >> ./authorized_keys
  ```

-  完成后可执行 `ssh Master的ip` 验证一下（可能需要输入 yes，成功后执行 `exit` 返回原来的终端）

- 在 Master 节点将上公匙传输到 全部的Slave节点

- 接着在 Slave1 节点上，将 ssh 公匙加入授权：

  ```shell
  mkdir ~/.ssh       # 如果不存在该文件夹需先创建，若已存在则忽略
  cat ~/id_rsa.pub >> ~/.ssh/authorized_keys
  rm ~/id_rsa.pub    # 用完就可以删掉了
  ```

  

## 4.1 使用centos:centos7(docker)搭建

- 拉取镜像：`docker pull centos:centos7`

- 创建hadoop自定义网络（网络模式为bridge）：`docker network create --driver bridge hadoop_cluster`

    ```
    NETWORK ID          NAME                DRIVER              SCOPE
    7b9502d261b5        bridge              bridge              local
    041a8525b1c7        hadoop_cluster      bridge              local
    4631a046c450        host                host                local
    cbc887db2441        none                null                local
    ```

    

### 4.1.1 使用centos:centos7创建基础镜像

- 查询镜像：`docker images`

    ```
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    centos              centos7             7e6257c9f8d8        2 months ago        203MB
    ```

- 启动容器加载镜像，然后进入启动的容器

    ```shell
    PS C:\Users\ZhangHai> docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    centos              centos7             7e6257c9f8d8        2 months ago        203MB
    PS C:\Users\ZhangHai> docker run -dit --privileged --name centos-hadoop 7e6257c9f8d8 /usr/sbin/init
    43da14944c58d4181eb4a9bb34ba11657b3b15ffb5176b460c0f60a60d06f738
    PS C:\Users\ZhangHai> docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
    43da14944c58        7e6257c9f8d8        "/usr/sbin/init"    36 seconds ago      Up 35 seconds                           centos-hadoop
    PS C:\Users\ZhangHai> docker exec -it 43da14944c58 bash
    [root@43da14944c58 /]#
    ```

- 配置时区：`[root@43da14944c58 /]# ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime`

- 配置ifconfig：`[root@43da14944c58 /]# yum install net-tools.x86_64`

- 查看网卡信息：`ifconfig`

- 安装openssh：`yum install openssh-server -y`

- 安装ssh客户端和which：

    - `yum -y install openssh-clients`
    - `yum -y install which`

- 测试ssh：

    - ```shell
        # 查看ssh启动状态
        [root@43da14944c58 /]# systemctl status sshd
        ● sshd.service - OpenSSH server daemon
           Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
           Active: active (running) since Thu 2020-10-15 17:49:32 CST; 11s ago
             Docs: man:sshd(8)
                   man:sshd_config(5)
         Main PID: 209 (sshd)
           CGroup: /docker/43da14944c58d4181eb4a9bb34ba11657b3b15ffb5176b460c0f60a60d06f738/system.slice/sshd.service
                   └─209 /usr/sbin/sshd -D
                   ‣ 209 /usr/sbin/sshd -D
        
        Oct 15 17:49:32 43da14944c58 systemd[1]: Starting OpenSSH server daemon...
        Oct 15 17:49:32 43da14944c58 sshd[209]: Server listening on 0.0.0.0 port 22.
        Oct 15 17:49:32 43da14944c58 sshd[209]: Server listening on :: port 22.
        Oct 15 17:49:32 43da14944c58 systemd[1]: Started OpenSSH server daemon.
        
        # 使用ssh登录本机，在用户目录下生成.ssh目录
        [root@43da14944c58 /]# ssh localhost
        The authenticity of host 'localhost (127.0.0.1)' can't be established.
        ECDSA key fingerprint is SHA256:01+HeXUKJK7YHgpYTGTbTkSocs43xlGN81B1rRrsufw.
        ECDSA key fingerprint is MD5:c6:61:36:05:62:fc:1d:c7:0b:71:a0:ed:88:9c:98:77.
        Are you sure you want to continue connecting (yes/no)? yes
        Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
        root@localhost's password:
        Permission denied, please try again.
        root@localhost's password:
        Permission denied, please try again.
        root@localhost's password:
        Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password).
        [root@43da14944c58 /]# cd ~/.ssh
        
        # 生成ssh密钥，一路回车就可以
        [root@43da14944c58 .ssh]# ssh-keygen -t rsa
        Generating public/private rsa key pair.
        Enter file in which to save the key (/root/.ssh/id_rsa):
        Enter passphrase (empty for no passphrase):
        Enter same passphrase again:
        Your identification has been saved in /root/.ssh/id_rsa.
        Your public key has been saved in /root/.ssh/id_rsa.pub.
        The key fingerprint is:
        SHA256:uJD26ah4cZ8RlyNcsFbsjr5JBnAMIidtZg7xhjqqho0 root@43da14944c58
        The key's randomart image is:
        +---[RSA 2048]----+
        |=oo   .o.        |
        |o*=o   oo        |
        |.*+ o.oo .       |
        |...o o+.=        |
        |o   = .*S.       |
        |.....+oo.        |
        |oo o o*o         |
        |Eoo  =+.         |
        |+.... +.         |
        +----[SHA256]-----+
        
        # 使用cat把ssh公钥追加到authorized_keys中
        [root@43da14944c58 .ssh]# cat ./id_rsa.pub >> ./authorized_keys
        
        # 测试本机免密登录
        [root@43da14944c58 .ssh]# ssh localhost
        Last failed login: Thu Oct 15 17:51:14 CST 2020 from localhost on ssh:notty
        There were 2 failed login attempts since the last successful login.
        ```

    - 编写启动脚本：`vi /root/run.sh`

        ```shell
        #!/bin/bash
        /usr/sbin/sshd -D
        ```

    - 更改脚本权限：`[root@43da14944c58 ~]# chmod +x ./run.sh`

- 把hadoop复制到容器中：`docker cp hadoop-2.9.2.tar.gz 43da14944c58:/root/apps`

- 把jdk复制到容器中：`docker cp jdk-8u251-linux-x64.tar.gz 43da14944c58:/root/apps`

    ```shell
    [root@43da14944c58 apps]# ls
    hadoop-2.9.2.tar.gz  jdk-8u251-linux-x64.tar.gz
    [root@43da14944c58 apps]# tar -xzf jdk-8u251-linux-x64.tar.gz
    [root@43da14944c58 apps]# tar -xzf hadoop-2.9.2.tar.gz
    [root@43da14944c58 apps]# ls
    hadoop-2.9.2  hadoop-2.9.2.tar.gz  jdk-8u251-linux-x64.tar.gz  jdk1.8.0_251
    ```

- 配置系统环境变量：修改`~/.bashrc`文件。在文件末尾加入下面配置信息：

    ```
    export JAVA_HOME=/root/apps/jdk1.8.0_251
    export HADOOP_HOME=/root/apps/hadoop-2.9.2
    export HADOOP_CONFIG_HOME=$HADOOP_HOME/etc/hadoop
    export PATH=$PATH:$HADOOP_HOME/bin
    export PATH=$PATH:$HADOOP_HOME/sbin
    ```

- 配置hadoop的JAVA_HOME：修改文件`/root/apps/hadoop-2.9.2/etc/hadoop/hadoop-env.sh`

    - `export JAVA_HOME=/root/apps/jdk1.8.0_251`

- 修改配置文件：`/root/apps/hadoop-2.9.2/etc/hadoop/core-site.xml`

    - ```xml
        <?xml version="1.0" encoding="UTF-8"?>
        <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
        <configuration>
            <property>
                <name>fs.defaultFS</name>
                <value>hdfs://hdp-01:9000</value>
            </property>
            <property>
                <name>hadoop.tmp.dir</name>
                <value>/root/apps/hadoop-2.9.2/tmp</value>
            </property>
        </configuration>
        ```

    - 创建`hadoop.tmp.dir`目录：`mkdir /root/apps/hadoop-2.9.2/tmp `

- 修改配置文件：`/root/apps/hadoop-2.9.2/etc/hadoop/hdfs-site.xml`

    - ```xml
        <?xml version="1.0" encoding="UTF-8"?>
        <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
        <configuration>
            <property>
                <name>dfs.namenode.name.dir</name>
                <value>/root/apps/hadoop-2.9.2/namenode</value>
            </property>
            <property>
                <name>dfs.datanode.data.dir</name>
                <value>/root/apps/hadoop-2.9.2/datanode</value>
            </property>
            
            <property>
                <name>dfs.replication</name>
                <value>2</value>
            </property>
        
            <property>
                <name>dfs.secondary.http.address</name>
                <value>hdp-01:50090</value>
            </property>
        </configuration>
        ```

    - 创建目录：

        - `mkdir /root/apps/hadoop-2.9.2/namenode`
        -  `mkdir /root/apps/hadoop-2.9.2/datanode `

- 修改配置文件：`/root/apps/hadoop-2.9.2/etc/hadoop/mapred-site.xml`

    - ```xml
        <?xml version="1.0"?>
        <?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
        <configuration>
            <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
            </property>
        </configuration>
        ```

- 修改配置文件：`/root/apps/hadoop-2.9.2/etc/hadoop/yarn-site.xml`

    - ```xml
        <?xml version="1.0"?>
        <configuration>
            <property>
                <name>yarn.resourcemanager.hostname</name>
                <value>hdp-01</value>
            </property>
        
            <property>
                <name>yarn.nodemanager.aux-services</name>
                <value>mapreduce_shuffle</value>
            </property>
        </configuration>
        ```

- 退出并保存容器：

    - 退出容器：`exit`

    - 停止运行容器：`docker stop 43da14944c58`

    - 保存当前容器：`docker commit 43da14944c58 centos7-hadoop-zh:v1.0`

    - 查询镜像：`docker images`

        ```
        REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
        centos7-hadoop-zh   v1.0                3ef2f5a18237        3 seconds ago       2.12GB
        centos              centos7             7e6257c9f8d8        2 months ago        203MB
        ```

### 4.1.1 创建主节点

- 创建主节点容器

    ```shell
    docker run -d -p 5002:22 -p 9000:9000 -p 50090:50090 --name hdp-node-01 --privileged --restart always --network hadoop_cluster --network-alias hdp-01 3ef2f5a18237 /usr/sbin/init -c "while true; do sleep 10; done" /root/run.sh
    ```

    - `-c "while true; do sleep 10; done"`：防止容器启动后立马退出
    - `/usr/sbin/init`和`--privileged`：解决在容器中不能使用systemctl命令的问题

- 查看正在运行的容器：`docker ps`

    - ```
        CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS
                              NAMES
        0fe37eebc9fb        3ef2f5a18237        "/usr/sbin/init -c '…"   11 seconds ago      Up 11 seconds       0.0.0.0:9000->9000/tcp, 0.0.0.0:50090->50090/tcp, 0.0.0.0:5002->22/tcp   hdp-node-01
        ```

- 进入容器hdp-node-01：`docker exec -it 0fe37eebc9fb bash`

- 配置ssh：

    ```shell
    # 查看ssh启动状态
    [root@0fe37eebc9fb /]# systemctl status sshd
    ● sshd.service - OpenSSH server daemon
       Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
       Active: active (running) since Fri 2020-10-16 09:04:49 CST; 2min 59s ago
         Docs: man:sshd(8)
               man:sshd_config(5)
     Main PID: 61 (sshd)
       CGroup: /docker/0fe37eebc9fbc9f759c6d622ec310e2194d50677a6dbb333876a49e11d46f68c/system.slice/sshd.service
               └─61 /usr/sbin/sshd -D
               ‣ 61 /usr/sbin/sshd -D
    
    Oct 16 09:04:49 0fe37eebc9fb systemd[1]: Starting OpenSSH server daemon...
    Oct 16 09:04:49 0fe37eebc9fb sshd[61]: Server listening on 0.0.0.0 port 22.
    Oct 16 09:04:49 0fe37eebc9fb sshd[61]: Server listening on :: port 22.
    Oct 16 09:04:49 0fe37eebc9fb systemd[1]: Started OpenSSH server daemon.
    
    # 进入~/.ssh目录，如果没有该目录，先执行一次ssh localhost
    [root@0fe37eebc9fb /]# cd ~/.ssh
    
    # 删除之前生成的公匙（如果有）
    [root@0fe37eebc9fb .ssh]# rm ./id_rsa*
    rm: remove regular file './id_rsa'? y
    rm: remove regular file './id_rsa.pub'? y
    
    # 生成ssh密钥，一路直接回车
    [root@0fe37eebc9fb .ssh]# ssh-keygen -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/root/.ssh/id_rsa):
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /root/.ssh/id_rsa.
    Your public key has been saved in /root/.ssh/id_rsa.pub.
    The key fingerprint is:
    SHA256:x4h0CoZqY/qQ6PubUZVOOBWzpBSp6sHs3+HYLf7yx9Q root@0fe37eebc9fb
    The key's randomart image is:
    +---[RSA 2048]----+
    |     oo=.        |
    |   ...= +        |
    |  . ++.=.        |
    | . o o=+ o       |
    |++.  .o.S +      |
    |=*. .    o E     |
    |B .. .  o        |
    |.=  Boo  o       |
    | o=*o==+.        |
    +----[SHA256]-----+
    
    # 使用cat把ssh公钥追加到authorized_keys中
    [root@0fe37eebc9fb .ssh]# cat ./id_rsa.pub >> ./authorized_keys
    
    # 测试本机免密登录
    [root@0fe37eebc9fb .ssh]# ssh localhost
    Last login: Thu Oct 15 17:56:12 2020 from localhost
    
    # 退出ssh登录
    [root@0fe37eebc9fb ~]# exit
    logout
    Connection to localhost closed.
    [root@0fe37eebc9fb .ssh]#
    
    # 在创建好从结点之后，需要把主节点的ssh公钥配置到从节点中
    ```

- 修改配置文件：`/root/apps/hadoop-2.9.2/etc/hadoop/slaves`

    - ```
        hdp-02
        hdp-03
        ```

    - 格式化NameNode：
        - `cd /root/apps/hadoop-2.9.2/bin`
        - `hadoop namenode -format`

### 4.1.2 创建从节点

- 创建从节点容器：

    ```shell
    # 创建从节点hdp-node-02
    PS D:\todo> docker run -d -p 5003:22 --name hdp-node-02 --privileged --restart always --network hadoop_cluster --network-alias hdp-02 3ef2f5a18237 /usr/sbin/init -c "while true; do sleep 10; done" /root/run.sh
    49abcf5aad570caf369257235609f76eb2d928ab0e3ed7eec60a3969461fa4b8
    
    # 创建从节点hdp-node-03
    PS D:\todo> docker run -d -p 5004:22 --name hdp-node-03 --privileged --restart always --network hadoop_cluster --network-alias hdp-03 3ef2f5a18237 /usr/sbin/init -c "while true; do sleep 10; done" /root/run.sh
    6f13fa25269a02d7c408a3c237110d5ec50a9eb20a8a9eee4a3bdf684c85cd9f
    ```

    - `-c "while true; do sleep 10; done"`：防止容器启动后立马退出
    - `/usr/sbin/init`和`--privileged`：解决在容器中不能使用systemctl命令的问题

- 查看正在运行的容器：`docker ps`

    ```shell
    PS D:\todo> docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS
                          NAMES
    6f13fa25269a        3ef2f5a18237        "/usr/sbin/init -c '…"   4 seconds ago       Up 3 seconds        0.0.0.0:5004->22/tcp
                          hdp-node-03
    49abcf5aad57        3ef2f5a18237        "/usr/sbin/init -c '…"   12 seconds ago      Up 11 seconds       0.0.0.0:5003->22/tcp
                          hdp-node-02
    0fe37eebc9fb        3ef2f5a18237        "/usr/sbin/init -c '…"   14 minutes ago      Up 14 minutes       0.0.0.0:9000->9000/tcp, 0.0.0.0:50090->50090/tcp, 0.0.0.0:5002->22/tcp   hdp-node-01
    ```

- 配置主节点的ssh公钥到所有从节点：

    ```shell
    # 登录所有从节点，删除之前生成的ssh公匙（如果有）
    PS D:\todo> docker exec -it 49abcf5aad57 bash
    [root@49abcf5aad57 /]# cd ~/.ssh
    [root@49abcf5aad57 .ssh]# rm ./id_rsa*
    rm: remove regular file './id_rsa'? y
    rm: remove regular file './id_rsa.pub'? y
    [root@49abcf5aad57 .ssh]# exit
    exit
    PS D:\todo> docker exec -it 6f13fa25269a bash
    [root@6f13fa25269a /]# cd ~/.ssh
    [root@6f13fa25269a .ssh]# rm ./id_rsa*
    rm: remove regular file './id_rsa'? y
    rm: remove regular file './id_rsa.pub'? y
    [root@6f13fa25269a .ssh]# exit
    exit
    
    # 登录主节点，把主节点的ssh公钥复制本地，然后从本地复制到所有的从节点
    PS D:\todo> docker cp hdp-node-01:/root/.ssh/id_rsa.pub ./
    PS D:\todo> ls
    
    
        目录: D:\todo
    
    
    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----       2020/10/16      9:12            399 id_rsa.pub
    
    PS D:\todo> docker cp id_rsa.pub hdp-node-02:/root/.ssh
    PS D:\todo> docker cp id_rsa.pub hdp-node-03:/root/.ssh
    
    # 登录从节点，使用cat把ssh公钥追加到authorized_keys中
    PS D:\todo> docker exec -it 49abcf5aad57 bash
    [root@49abcf5aad57 /]# cd ~/.ssh
    [root@49abcf5aad57 .ssh]# ls
    authorized_keys  id_rsa.pub  known_hosts
    [root@49abcf5aad57 .ssh]# cat ./id_rsa.pub >> ./authorized_keys
    [root@49abcf5aad57 .ssh]# exit
    exit
    
    PS D:\todo> docker exec -it 6f13fa25269a bash
    [root@6f13fa25269a /]# cd ~/.ssh
    [root@6f13fa25269a .ssh]# ls
    authorized_keys  id_rsa.pub  known_hosts
    [root@6f13fa25269a .ssh]# cat ./id_rsa.pub >> ./authorized_keys
    [root@6f13fa25269a .ssh]# exit
    exit
    
    # 登录主节点，验证免密登录从节点
    (base) PS D:\todo> docker exec -it 0fe37eebc9fb bash
    [root@0fe37eebc9fb /]# ssh root@hdp-02
    Last failed login: Fri Oct 16 09:32:19 CST 2020 from hdp-node-01.hadoop_cluster on ssh:notty
    There were 5 failed login attempts since the last successful login.
    Last login: Thu Oct 15 17:56:12 2020 from localhost
    [root@49abcf5aad57 ~]# exit
    logout
    Connection to hdp-02 closed.
    [root@0fe37eebc9fb /]# ssh root@hdp-03
    The authenticity of host 'hdp-03 (172.18.0.4)' can't be established.
    ECDSA key fingerprint is SHA256:01+HeXUKJK7YHgpYTGTbTkSocs43xlGN81B1rRrsufw.
    ECDSA key fingerprint is MD5:c6:61:36:05:62:fc:1d:c7:0b:71:a0:ed:88:9c:98:77.
    Are you sure you want to continue connecting (yes/no)? yes
    Warning: Permanently added 'hdp-03,172.18.0.4' (ECDSA) to the list of known hosts.
    Last login: Thu Oct 15 17:56:12 2020 from localhost
    [root@6f13fa25269a ~]# exit
    logout
    Connection to hdp-03 closed.
    [root@0fe37eebc9fb /]#
    ```

### 4.1.3 在主节点启动hadoop

- 进入主节点容器：`docker exec -it 0fe37eebc9fb bash`

    ```shell
    PS D:\todo> docker exec -it 0fe37eebc9fb bash
    [root@0fe37eebc9fb /]# 
    ```

- 启动HDFS：

    ```shell
    [root@0fe37eebc9fb /]# cd /root/apps/hadoop-2.9.2/sbin
    [root@0fe37eebc9fb sbin]# ./start-dfs.sh
    Starting namenodes on [hdp-01]
    The authenticity of host 'hdp-01 (172.18.0.2)' can't be established.
    ECDSA key fingerprint is SHA256:01+HeXUKJK7YHgpYTGTbTkSocs43xlGN81B1rRrsufw.
    ECDSA key fingerprint is MD5:c6:61:36:05:62:fc:1d:c7:0b:71:a0:ed:88:9c:98:77.
    Are you sure you want to continue connecting (yes/no)? yes
    hdp-01: Warning: Permanently added 'hdp-01,172.18.0.2' (ECDSA) to the list of known hosts.
    hdp-01: starting namenode, logging to /root/apps/hadoop-2.9.2/logs/hadoop-root-namenode-0fe37eebc9fb.out
    localhost: starting datanode, logging to /root/apps/hadoop-2.9.2/logs/hadoop-root-datanode-0fe37eebc9fb.out
    hdp-03: starting datanode, logging to /root/apps/hadoop-2.9.2/logs/hadoop-root-datanode-6f13fa25269a.out
    hdp-02: starting datanode, logging to /root/apps/hadoop-2.9.2/logs/hadoop-root-datanode-49abcf5aad57.out
    Starting secondary namenodes [hdp-01]
    hdp-01: starting secondarynamenode, logging to /root/apps/hadoop-2.9.2/logs/hadoop-root-secondarynamenode-0fe37eebc9fb.out
    ```

- 启动YARN：

  ```shell
  [root@0fe37eebc9fb sbin]# ./start-yarn.sh
  starting yarn daemons
  starting resourcemanager, logging to /root/apps/hadoop-2.9.2/logs/yarn--resourcemanager-0fe37eebc9fb.out
  localhost: starting nodemanager, logging to /root/apps/hadoop-2.9.2/logs/yarn-root-nodemanager-0fe37eebc9fb.out
  hdp-03: starting nodemanager, logging to /root/apps/hadoop-2.9.2/logs/yarn-root-nodemanager-6f13fa25269a.out
  hdp-02: starting nodemanager, logging to /root/apps/hadoop-2.9.2/logs/yarn-root-nodemanager-49abcf5aad57.out
  ```

  

### 4.1.4 测试Hadoop

#### 4.1.4.1 上传文件到HDFS

```shell
# 列出hdfs根目录下的文件
[root@0fe37eebc9fb apps]# hadoop fs -ls /
# 在hdfs根目录创建文件路径/wordcount/input
[root@0fe37eebc9fb apps]# hadoop fs -mkdir -p /wordcount/input
[root@0fe37eebc9fb apps]# hadoop fs -ls /
Found 1 items
drwxr-xr-x   - root supergroup          0 2020-10-16 12:26 /wordcount
# 创建一个文件 内容为一些英文单词,每行一个词
[root@0fe37eebc9fb apps]# vi somewords.txt
# 上传此文本文件到hdfs的/wordcount/input目录下
[root@0fe37eebc9fb apps]# hadoop fs -put somewords.txt /wordcount/input
[root@0fe37eebc9fb apps]# hadoop fs -ls /wordcount/input
Found 1 items
-rw-r--r--   2 root supergroup         23 2020-10-16 12:30 /wordcount/input/somewords.txt
```

#### 4.1.4.2 运行一个mapreduce程序

```shell
[root@0fe37eebc9fb mapreduce]# pwd
/root/apps/hadoop-2.9.2/share/hadoop/mapreduce

[root@0fe37eebc9fb mapreduce]# hadoop jar hadoop-mapreduce-examples-2.9.2.jar wordcount /wordcount/input /wordcount/output
20/10/16 12:41:32 INFO client.RMProxy: Connecting to ResourceManager at hdp-01/172.18.0.2:8032
20/10/16 12:41:33 INFO input.FileInputFormat: Total input files to process : 1
20/10/16 12:41:33 INFO mapreduce.JobSubmitter: number of splits:1
20/10/16 12:41:33 INFO Configuration.deprecation: yarn.resourcemanager.system-metrics-publisher.enabled is deprecated. Instead, use yarn.system-metrics-publisher.enabled
20/10/16 12:41:33 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1602816131335_0001
20/10/16 12:41:34 INFO impl.YarnClientImpl: Submitted application application_1602816131335_0001
20/10/16 12:41:34 INFO mapreduce.Job: The url to track the job: http://hdp-01:8088/proxy/application_1602816131335_0001/
20/10/16 12:41:34 INFO mapreduce.Job: Running job: job_1602816131335_0001
20/10/16 12:41:40 INFO mapreduce.Job: Job job_1602816131335_0001 running in uber mode : false
20/10/16 12:41:40 INFO mapreduce.Job:  map 0% reduce 0%
20/10/16 12:41:44 INFO mapreduce.Job:  map 100% reduce 0%
20/10/16 12:41:48 INFO mapreduce.Job:  map 100% reduce 100%
20/10/16 12:41:48 INFO mapreduce.Job: Job job_1602816131335_0001 completed successfully
20/10/16 12:41:48 INFO mapreduce.Job: Counters: 49
        File System Counters
                FILE: Number of bytes read=59
                FILE: Number of bytes written=396887
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
                Total time spent by all maps in occupied slots (ms)=1623
                Total time spent by all reduces in occupied slots (ms)=1838
                Total time spent by all map tasks (ms)=1623
                Total time spent by all reduce tasks (ms)=1838
                Total vcore-milliseconds taken by all map tasks=1623
                Total vcore-milliseconds taken by all reduce tasks=1838
                Total megabyte-milliseconds taken by all map tasks=1661952
                Total megabyte-milliseconds taken by all reduce tasks=1882112
        Map-Reduce Framework
                Map input records=5
                Map output records=5
                Map output bytes=43
                Map output materialized bytes=59
                Input split bytes=113
                Combine input records=5
                Combine output records=5
                Reduce input groups=5
                Reduce shuffle bytes=59
                Reduce input records=5
                Reduce output records=5
                Spilled Records=10
                Shuffled Maps =1
                Failed Shuffles=0
                Merged Map outputs=1
                GC time elapsed (ms)=75
                CPU time spent (ms)=900
                Physical memory (bytes) snapshot=517210112
                Virtual memory (bytes) snapshot=3962376192
                Total committed heap usage (bytes)=349700096
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
[root@0fe37eebc9fb mapreduce]# hadoop fs -ls /wordcount/output
Found 2 items
-rw-r--r--   2 root supergroup          0 2020-10-16 12:41 /wordcount/output/_SUCCESS
-rw-r--r--   2 root supergroup         33 2020-10-16 12:41 /wordcount/output/part-r-00000
```

#### 4.1.4.3 当前集群存在的问题TODO

**外部客户端可以获取文件元数据信息，可以获取空的文本文件，但是无法获取有内容的文件。应该是不在一个网络的原因，后续需要研究DistributedFileSystem和DFSClient**