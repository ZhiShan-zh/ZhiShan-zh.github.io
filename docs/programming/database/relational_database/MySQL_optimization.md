# MySQL数据库优化

# 1 MySQL数据库优化综述


![image-20200429151724171.png](https://zhishan-zh.github.io//media/1588507531981-1861946c-118b-4b22-a750-6a01cad8ce99.png)


# 2 硬件、操作系统、⽂件系统（待完成）


# 3 数据库表结构


## 3.1 概述


数据库架构：


- 单实例无法解决空间或性能需求时考虑拆分；
- 垂直拆分；
- 水平拆分；
- 引入缓存系统。



## 3.2 表数据压缩优化


### 3.2.1 表压缩概述


表压缩可以在创建表时开启，压缩表能够使表中的数据以压缩格式存储，压缩能够显著提高原生性能和可伸缩性。


压缩意味着在硬盘和内存之间传输的数据更小且占用相对少的内存及硬盘，对于辅助索引，这种压缩带来更加明显的好处，因为索引数据也被压缩了。压缩对于硬盘是SSD的存储设备尤为重要，因为它们相对普通的HDD硬盘比较贵且容量有限。


我们都知道，CPU和内存的速度远远大于磁盘，因为对于数据库服务器，磁盘IO可能会成为紧要资源或者瓶颈。数据压缩能够让数据库变得更小，从而减少磁盘的I/O，还能提高系统吞吐量，以很小的成本（耗费较多的CPU资源）。对于读比重比较多的应用，压缩是特别有用。压缩能够让系统拥有足够的内存来存储热数据。


在创建innodb表时带上ROW_FORMAT=COMPRESSED参数能够使用比默认的16K更小的页。这样在读写时需要更少的I/O，对于SSD磁盘更有价值。


页的大小通过KEY_BLOCK_SIZE参数指定。不同大小的页意味着需要使用独立表空间，不能使用系统共享表空间，可以通过innodb_file_per_table指定。KEY_BLOCK_SIZE的值越小，你获得I/O好处就越多，但是如果因为你指定的值太小，当数据被压缩到不足够满足每页多行数据记录时，会产生额外的开销来重组页。对于一个表，KEY_BLOCK_SIZE的值有多小是有严格的限制的，一般是基于每个索引键的长度。有时指定值过小，当create table或者alter table会失败。


在缓冲池中，被压缩的数据是存储在小页中的，这个小页的实际大小就是KEY_BLOCK_SIZE的值。为了提取和更新列值，mysql也会在缓冲池中创建一个未压缩的16k页。任何更新到未压缩的页也需要重新写入到压缩的页，这时你需要估计缓冲池的大小以满足压缩和未压缩的页，尽管当缓冲空间不足时，未压缩的页会被挤出缓冲池。在下次访问时，不压缩的页还会被创建。


### 3.2.2使用表的压缩


在创建一个压缩表之前，需要启用独立表空间参数`innodb_file_per_table=1`；也需要设置`innodb_file_format=Barracuda`，你可以写到`my.cnf`文件中不需要重启mysql服务。


```sql
SET GLOBAL innodb_file_per_table=1;
SET GLOBAL innodb_file_format=Barracuda;
CREATE TABLE t1
 (c1 INT PRIMARY KEY) 
 ROW_FORMAT=COMPRESSED  
 KEY_BLOCK_SIZE=8;
```


- 如果你指定`ROW_FORMAT=COMPRESSED`，那么可以忽略`KEY_BLOCK_SIZE`的值，这时使用默认innodb页的一半，即8kb；
- 如果你指定了`KEY_BLOCK_SIZE`的值，那么你可以忽略`ROW_FORMAT=COMPRESSED`，因为这时会自动启用压缩；
- 为了指定最合适`KEY_BLOCK_SIZE`的值，你可以创建表的多个副本，使用不同的值进行测试，比较他们的`.ibd`文件的大小；
- `KEY_BLOCK_SIZE`的值作为一种提示，如必要，Innodb也可以使用一个不同的值。0代表默认压缩页的值，Innodb页的一半。`KEY_BLOCK_SIZE`的值只能小于等于innodb page size。如果你指定了一个大于innodb page size的值，mysql会忽略这个值然后产生一个警告，这时`KEY_BLOCK_SIZE`的值是Innodb页的一半。如果设置了`innodb_strict_mode=ON`，那么指定一个不合法的`KEY_BLOCK_SIZE`的值是返回报错。



InnoDB未压缩的数据页是16K，根据选项组合值，mysql为每个表的`.ibd`文件使用1kb,2kb,4kb,8kb,16kb页大小，实际的压缩算法并不会受`KEY_BLOCK_SIZE`值影响，这个值只是决定每个压缩块有多大，从而影响多少行被压缩到每个页。设置`KEY_BLOCK_SIZE`值等于16k并不能有效的进行压缩，因为默认的innodb页就是16k，但是对于拥有很多BLOB,TEXT,VARCHAR类型字段的表可能会有效果的。


### 3.2.3 InnoDB表的压缩优化


在进行表压缩时需要考虑影响压缩性能的因素，如：


- 哪些表需要压缩
- 如何选择压缩表的页大小
- 基于运行时性能特征是否需要调整buffer pool大小，如系统在压缩和解压缩数据所花费的时间量，系统负载更像一个数据仓库还是OLTP事务性系统。
- 如果在压缩表上执行DML操作，由于数据分布的方式，可能导致压缩失败，这时你可能需要配置额外的更高级的配置选项



#### 3.2.3.1 何时用压缩表


一般而言，对于读远远大于写的应用以及拥有合理数量的字符串列的表，使用压缩效果会更好。


#### 3.2.3.2 数据特性及压缩率


影响数据文件压缩效率的一个关键因素是数据本身的结构，在块数据中，压缩是通过识别重复字符进行压缩的，对于完全随机的数据是一个糟糕的情况，一般而言，有重复数据的压缩更好。对于字符串的列压缩就不错，无论是string还是blob、text等类型的。另一方面，如果表中的数据是二进制类型，如整形、浮点型等或者之前别压缩过的如jpg、png类型的，压缩效果一般不好，但也不是绝对的。


为了决定是否对某个表进行压缩，你需要进行试验，可以对比未压缩与压缩后的数据文件的大小，以及监控系统对于压缩表的工作负载进行决定。具体试验：


```shell
#没有设置压缩前的数据大小
-rw-rw----. 1 mysql mysql 368M 12月 29 11:05 test.ibd
#设置KEY_BLOCK_SIZE=1
(product)root@localhost [sakila]> alter table test KEY_BLOCK_SIZE=1;
Query OK, 0 rows affected (14 min 49.30 sec)
Records: 0  Duplicates: 0  Warnings: 0

-rw-rw----. 1 mysql mysql 204M 1月  11 21:43 test.ibd      #####压缩率44.5%

#设置KEY_BLOCK_SIZE=2
(product)root@localhost [sakila]> alter table test KEY_BLOCK_SIZE=2;
Query OK, 0 rows affected (9 min 55.60 sec)
Records: 0  Duplicates: 0  Warnings: 0

-rw-rw----. 1 mysql mysql 180M 1月  12 13:40 test.ibd      #####压缩率51%
     
#设置KEY_BLOCK_SIZE=4
(product)root@localhost [sakila]> alter table test KEY_BLOCK_SIZE=4;
Query OK, 0 rows affected (7 min 24.52 sec)
Records: 0  Duplicates: 0  Warnings: 0

-rw-rw----. 1 mysql mysql 172M 1月  11 21:09 test.ibd      #####压缩率53.2%

#设置KEY_BLOCK_SIZE=8
(product)root@localhost [sakila]> alter table test KEY_BLOCK_SIZE=8;
Query OK, 0 rows affected (5 min 16.34 sec)
Records: 0  Duplicates: 0  Warnings: 0

-rw-rw----. 1 mysql mysql 172M 1月  11 21:00 test.ibd      #####压缩率53.2%

#设置KEY_BLOCK_SIZE=16
(product)root@localhost [sakila]> alter table test KEY_BLOCK_SIZE=16;
Query OK, 0 rows affected (2 min 47.48 sec)
Records: 0  Duplicates: 0  Warnings: 0

-rw-rw----. 1 mysql mysql 336M 1月  12 13:54 test.ibd      #####压缩率8.6%
```


查看监控压缩表的负载，如下：


- 对于简单的测试，如一个mysql实例上没有其他的压缩表了，直接查询`INFORMATION_SCHEMA.INNODB_CMP`表数据即可，该表存一些压缩表的数据状态，结构如下：
| Column name | Description |
| --- | --- |
| `PAGE_SIZE` | 采用压缩页大小（字节数）. |
| `COMPRESS_OPS` | Number of times a B-tree page of the size `PAGE_SIZE` has been compressed. Pages are compressed whenever an empty page is created or the space for the uncompressed modification log runs out. |
| `COMPRESS_OPS_OK` | Number of times a B-tree page of the size `PAGE_SIZE` has been successfully compressed. This count should never exceed `COMPRESS_OPS`. |
| `COMPRESS_TIME` | Total time in seconds spent in attempts to compress B-tree pages of the size `PAGE_SIZE`. |
| `UNCOMPRESS_OPS` | Number of times a B-tree page of the size `PAGE_SIZE` has been uncompressed. B-tree pages are uncompressed whenever compression fails or at first access when the uncompressed page does not exist in the buffer pool. |
| `UNCOMPRESS_TIME` | Total time in seconds spent in uncompressing B-tree pages of the size `PAGE_SIZE`. |



- 对于精细的测试，如多个压缩表，查询`INFORMATION_SCHEMA.INNODB_CMP_PER_INDEX`表数据，由于该表收集数据需要付出昂贵得代价，所以必须启动`innodb_cmp_per_index_enabled`选项才能查询。一般不要在生产环境下开启该选项。
- 还可以针对压缩运行一些测试SQL看看效率如何。
- 如果发现很多压缩失败，那么你可以调整`innodb_compression_level`, `innodb_compression_failure_threshold_pct`, 和`innodb_compression_pad_pct_max`参数。



#### 3.2.3.3 数据库压缩和应用程序压缩


不需要在应用端和数据库同时压缩相同的数据，那样效果并不明显而且还消耗很多CPU资源。对于数据库压缩，是在server端进行的。如果你在插入数据前通过代码进行数据压缩，然后插入数据库，这样耗费很多CPU资源，当然如果你的CPU有大量结余。你也可以结合两者，对于某些表进行应用程序压缩，而对其他数据采用数据库压缩。


#### 3.2.3.4 工作负载特性和压缩率


为了选择哪些表可以使用压缩，工作负载是另一个决定因素，一般而言，如果你的系统是I/O瓶颈，那么可以使用CPU进行压缩与解压缩，以CPU换取I/O。


### 3.2.4 INNODB表是如何压缩的？


#### 3.2.4.1 压缩算法


mysql进行压缩是借助于zlib库，采用L777压缩算法，这种算法在减少数据大小、CPU利用方面是成熟的、健壮的、高效的。同时这种算法是无失真的，因此原生的未压缩的数据总是能够从压缩文件中重构，LZ777实现原理是查找重复数据的序列号然后进行压缩，所以数据模式决定了压缩效率，一般而言，用户的数据能够被压缩50%以上。


不同于应用程序压缩或者其他数据库系统的压缩，InnoDB压缩是同时对数据和索引进行压缩，很多情况下，索引能够占数据库总大小的40%-50%。如果压缩效果很好，一般innodb文件会减少25%-50%或者更多，而且减少I/O增加系统吞吐量，但是会增加CPU的占用，你可通过设置innodb_compression_level参数来平衡压缩级别和CPU占用。


#### 3.2.4.2 InnoDB数据存储及压缩


所有数据和`b-tree`索引都是按页进行存储的，每行包含主键和表的其他列。辅助索引也是`b-tree`结构的，包含对值：索引值及指向每行记录的指针，这个指针实际上就是表的主键值。


在innodb压缩表中，每个压缩页（1,2,4,8）都对应一个未压缩的页16K，为了访问压缩页中的数据，如果该页在buffer pool中不存在，那么就从硬盘上读到这个压缩页，然后进行解压到原来的数据结构。为了最小化I/O和减少解压页的次数，有时，buffer pool中包括压缩和未压缩的页，为给其他页腾出地方，buffer pool会驱逐未压缩页，仅仅留下压缩页在内存中。或者如果一个页一段时间没有被访问，那么会被写到硬盘上。这样一来，任何时候，buffer pool中都可以包含压缩页和未压缩页，或者只有压缩页或者两者都没有。


Mysql采用LRU算法来保证哪些页应该在内存中还是被驱逐。因此热数据一般都会在内存中。

### 3.2.5 OLTP系统压缩负载优化


一般而言，innodb压缩对于只读或者读比重比较多的应用效果更好，SSD的出现，使得压缩更加吸引我们，尤其对于OLTP（On-Line Transaction Processing联机事务处理过程）系统。对于经常update、delete、insert的应用，通过压缩表能够减少他们的存储需求和每秒I/O操作。


下面是针对写密集的应用，设置压缩表的一些有用参数：


- `innodb_compression_level`：决定压缩程度的参数，如果你设置比较大，那么压缩比较多，耗费的CPU资源也较多；相反，如果设置较小的值，那么CPU占用少。默认值6，可以设置0-9
- `innodb_compression_failure_threshold_pct`：默认值5，范围0到100.设置中断点避免高昂的压缩失败率。
- `innodb_compression_pad_pct_max`：指定在每个压缩页面可以作为空闲空间的最大比例，该参数仅仅应用在设置了`innodb_compression_failure_threshold_pct`不为零情况下，并且压缩失败率通过了中断点。默认值50，可以设置范围是0到75。



## 3.3 范式


目前，主要有六种范式：第一范式、第二范式、第三范式、BC范式、第四范式和第五范式。满足最低要求的叫第一范式，简称1NF。在第一范式基础上进一步满足一些要求的为第二范式，简称2NF。其余依此类推。


范式可以避免数据冗余，减少数据库的空间，减轻维护数据完整性的麻烦，但是操作困难，因为需要联系多个表才能得到所需要数据，而且范式越高性能就会越差。要权衡是否使用更高范式是比较麻烦的，，我认为使用到第三范式也就足够了，性能好而且方便管理数据。


**第一范式**：对于表中的每一行，必须且仅仅有唯一的行值，在一行中的每一列仅有唯一的值并且具有原子性。（第一范式是通过把重复的组放到每个独立的表中，把这些表通过一对多关联联系起来这种方式来消除重复组的）

**第二范式**：非主键列是主键的子集，非主键列活动必须完全依赖整个主键。主键必须有唯一性的元素,一个主键可以由一个或更多的组成唯一值的列组成。一旦创建，主键无法改变，外键关联一个表的主键。主外键关联意味着一对多的关系。（第二范式处理冗余数据的删除问题。当某张表中的信息依赖于该表中其它的不是主键部分的列的时候，通常会违反第二范式）

**第三范式**：非主键列互不依赖。（第三范式规则查找以消除没有直接依赖于第一范式和第二范式形成的表的主键的属性。我们为没有与表的主键关联的所有信息建立了一张新表。每张新表保存了来自源表的信息和它们所依赖的主键）

**第四范式**：禁止主键列和非主键列一对多关系不受约束。

**第五范式**：将表分割成尽可能小的块，为了排除在表中所有的冗余。


**主要三范式** ：消除歧义，消除冗余，消除依赖。


> 第一范式：列不可分，eg:【联系人】（姓名，性别，电话），一个联系人有家庭电话和公司电话，那么这种表结构设计就没有达到 1NF，达到第一个规范式即为关系型数据库



> 第二范式：有主键，保证完全依赖。eg:订单明细表【OrderDetail】（OrderID，ProductID，UnitPrice，Discount，Quantity，ProductName），Discount（折扣），Quantity（数量）完全依赖（取决）于主键（OderID，ProductID），而 UnitPrice，ProductName 只依赖于 ProductID，不符合2NF；



> 第三范式：无传递依赖(非主键列 A 依赖于非主键列 B，非主键列 B 依赖于主键的情况)，eg:订单表【Order】（OrderID，OrderDate，CustomerID，CustomerName，CustomerAddr，CustomerCity）主键是（OrderID），CustomerName，CustomerAddr，CustomerCity 直接依赖的是 CustomerID（非主键列），而不是直接依赖于主键，它是通过传递才依赖于主键，所以不符合 3NF。



## 3.4 垂直拆分


把含有多个列的表拆分成多个表，解决表宽度问题，好处，拆分后业务清晰，拆分规则明确、系统之间整合或扩展容易、数据维护简单，下⾯是⽅法：


- 把不常⽤的字段单独放在同⼀个表中；
- 把⼤字段独⽴放⼊⼀个表中；
- 把经常使⽤的字段放在⼀起；



## 3.5 ⽔平拆分


### 3.5.1 水平拆分实现思路


表的⽔平拆分⽤于解决数据表中数据过⼤的问题，⽔平拆分每⼀个表的结构都是完全⼀致的。⼀般地，将数据平分到N张表中的常⽤⽅法：


- **范围**：根据ID所在的规定范围写入不同的表中；
- **哈希**：对ID进⾏hash运算，如果要拆分成5个表， mod(id,5)取出0~4个值，针对不同的hashID将数据存⼊不同的表中；
- **时间**：根据插入数据的时间来确定写入哪装表中，比如1个月一张表；
- **取模**：对id进行取模运算，如果要拆分成5个表， mod(id,5)取出0~4个值，针对不同的mod值将数据存⼊不同的表中；
- **指定**：根据数据和业务的特征来定义写入规则。



### 3.5.2 ⽔平拆分表的优缺点


**优点：**


- 表分割后可以降低在查询时需要读的数据和索引的⻚数，同时也降低了索引的层数，提⾼查询速度；
- 表中的数据本来就有独⽴性，例如表中分别记录各个地区的数据或不同时期的数据，特别是有些数据常⽤，⽽另外⼀些数据不常⽤。
- 需要把数据存放到多个数据库中，提⾼系统的总体可⽤性(分库，鸡蛋不能放在同⼀个篮⼦⾥)。

**缺点：**


- 跨分区表的数据查询；
- 统计及后台报表的操作等问题。



## 3.6 选择合适数据类型


- 使⽤较⼩、较简单的数据类型解决问题；
- 尽可能的使⽤not null 定义字段；
- 尽量避免使⽤text类型，⾮⽤不可时最好考虑分表。



# 4 索引优化


## 4.1 概述


建议在经常作查询选择的字段、经常作表连接的字段以及经常出现在order by、 group by、distinct 后⾯的字段中建⽴索引。


## 4.2 建立索引的目标


利用最小的索引成本找到最需要的行记录。


## 4.3 索引原则


### 4.3.1 最左前缀原则


最左优先，以最左边的为起点任何连续的索引都能匹配上。同时遇到范围查询(>、<、between、like)就会停止匹配。


范围列可以用到索引，但是范围列后面的列无法用到索引。即，索引最多用于一个范围列，因此如果查询条件中有两个范围列则无法全用到索引。


理论上索引对顺序是敏感的，但是由于 MySQL 的查询优化器会自动调整 where 子句的条件顺序以使用适合的索引，所以 MySQL 不存在 where 子句的顺序问题而造成索引失效。


例如：b = 2 如果建立(a,b)顺序的索引，是匹配不到(a,b)索引的；但是如果查询条件是`a = 1 and b = 2`或者`a=1`，又或者是`b = 2 and a = 1`就可以，因为优化器会自动调整a,b的顺序。再比如`a = 1 and b = 2 and c > 3 and d = 4` 如果建立(a,b,c,d)顺序的索引，d是用不到索引的，因为c字段是一个范围查询，它之后的字段会停止匹配。


### 4.3.2 避免单列索引


尽量使用组合索引，精确确定where条件对应的行。


### 4.3.3 避免重复索引


`idx_abc`多列索引，相当于创建了(a)列索引、(a,b)组合索引以及(a,b,c)组合索引。


### 4.3.4 不在索引列使用函数、算术运算或其他表达式运算


如`max(id)>10`，`id+1>3`等。


### 4.3.5 **尽量选择区分度高的列作为前缀索引**


区分度的公式是`count(distinct col)/count(*)`，表示字段不重复的比例，比例越大我们扫描的记录越少。


### 4.3.6 适当数量的索引


- 怎样建索引需要视具体情况⽽定，索引可以提⾼ select 的效率，但同时会降低 insert及 update 的效率，因为这两个操作有可能会重建索引。
- ⼀个表的索引数最好不要超过6个，尽量只在常⽤的列上建⽴索引。



## 4.4 索引失效的情况


### 4.4.1 以%开头的LIKE语句

以`%`（表示任意0个或多个字符）开头的LIKE语句，无法使用索引；

- 但是在覆盖索引的情况下是可以使用索引的。参见：[MySQL索引](./docs/programming/database/relational_database/MySQL-index.md)

**原因**：


> InnoDB存储引擎是以B+树为索引的存储结构的，如果我们以通配符%为查询条件，B+树是无法进行查找操作的，所以这种情况下无法使用索引。

### 4.4.2 在索引字段上进⾏函数、算术运算或其他表达式运算


在“=”左边进⾏函数、算术运算或其他表达式运算，⽆法正确使⽤索引。


1. 应尽量避免在 where ⼦句中对字段进⾏表达式操作，这将导致引擎放弃使⽤索引⽽进⾏全表扫描：

```sql
select id from t where num/2=100;
```


应改为:


```sql
select id from t where num=100*2;
```


2. 应尽量避免在where⼦句中对字段进⾏函数操作，这将导致引擎放弃使⽤索引⽽进⾏全表扫描:

```sql
--name以abc开头的id
select id from t where substring(name,1,3)='abc';
--'2005-11-30'⽣成的id
select id from t where datediff(day,createdate,'2005-11-30')=0;
```


应改为:


```sql
select id from t where name like 'abc%';
select id from t where createdate>='2005-11-30' and createdate<'2005-12-1';
```


### 4.4.3 or语句


使用or的时候，必须满足一下两个条件才能走索引：


1. 要求使用的所有字段，都必须建立索引；
2. 确保mysql版本5.0以上，且查询优化器开启了`index_merge_union=on`, 也就是变量`optimizer_switch`里存在`index_merge_union`且为`on`；

实际开发中要少用or：


- 当 where ⼦句中存在多个条件以“或”并存的时候， MySQL 的优化器并没有很好的解决其执⾏计划优化问题；
- 再加上MySQL 特有的 SQL 与 Storage 分层架构⽅式，造成了其性能⽐较低下；
- 使⽤ union all 或者是union（必要的时候）的⽅式来代替“or”会得到更好的效果。

### 4.4.4 对索引字段进⾏null值判断


在索引列上使⽤IS NULL 或IS NOT NULL操作。索引是不索引空值的，所以这样的操作不能使⽤索引，可以⽤其他的办法处理。


```sql
select id from t where num is null；
```


可以在num上设置默认值0，确保表中num列没有null值，然后这样查询：


```sql
select id from t where num=0；
```


### 4.4.5 多列索引错误使用


需要符合最左前缀原则。


### 4.4.6 在索引字段上使⽤not， <>， !=， eg<> 操作符（不等于）


不等于操作符是永远不会⽤到索引的，因此对它的处理只会产⽣全表扫描。


### 4.4.7 索引列有大量重复数据


SQL是根据表中数据来进⾏查询优化的，当索引列有⼤量数据重复时， SQL查询可能不会去利⽤索引。


⽐如：⼀表中有字段 sex， male、 female⼏乎各⼀半，那么即使在sex上建了索引也对查询效率起不了作⽤。


### 4.4.8 类型转换的情况


指 where⼦句中出现column字段的类型和传⼊的参数类型不⼀致⽽发⽣的转换，分两种情况：


- **⼈为在column_name上使⽤转换函数**：直接导致MySQL⽆法使⽤索引（实际上其他数据库也有同样的问题）。 如果⾮要转换，应该在传⼊的参数上进⾏转换。
- **由数据库⾃⼰进⾏转换**：如果传⼊的数据和字段两者类型不⼀致，同时⼜没有做任何类型转换处理，MySQL 可能会⾃⼰对数据进⾏类型转换操作，也可能不进⾏处理⽽交由存储引擎去处理， 这样会导致索引⽆法使⽤⽽造成执⾏计划问题。
  - 比如：`select * from user_info where mobile = xxx;`
  - 应该为：`select * from user_info where mobile = 'xxx';`

### 4.4.9 使⽤参数


如果在 where ⼦句中使⽤参数，也会导致全表扫描。因为SQL只有在运⾏时才会解析局部变量，但优化程序不能将访问计划的选择推迟到运⾏时；它必须在编译时进⾏选择。

然⽽，如果在编译时建⽴访问计划，变量的值还是未知的，因⽽⽆法作为索引选择的输⼊项。如下⾯语句将进⾏全表扫：`select id from t where num=@num`


可以改为强制查询使⽤索引：

`select id from t with(index(索引名)) where num=@num`


### 4.4.10 慎⽤in和not in


in 和 not in 也要慎⽤，很多时候⽤ exists 代替 in， not exists代表not in。


#### 4.4.10.1 连续的值用between替代


比如`select id from t where num in(1,2,3);`对于连续的数值，能⽤ between 就不要⽤ in 了`select id from t where num between 1 and 3；`


#### 4.4.10.2 很多时候⽤ exists 代替 in


in是把外表和内表作hash连接，而exists是对外表作loop循环，每次loop循环再对内表进行查询，一直以来认为exists比in效率高的说法是不准确的。如果查询的两个表大小相当，那么用in和exists差别不大；如果两个表中一个较小一个较大，则子查询表大的用exists，子查询表小的用in，原因是IN 和 NOT IN并不是针对索引的。


例如：表A(小表)，表B(大表)


```sql
select * from A where cc in(select cc from B)；--效率低，用到了A表上cc列的索引；

select * from A where exists(select cc from B where cc=A.cc)；--效率高，用到了B表上cc列的索引。
```


相反的：


```sql
select * from B where cc in(select cc from A)；--效率高，用到了B表上cc列的索引

select * from B where exists(select cc from A where cc=B.cc)；--效率低，用到了A表上cc列的索引。
```


另外**in时不对NULL进行处理**：`select 1 from dual where null in (0,1,2,null);`结果为空


#### 4.4.10.3 ⽤not exists 代替not in


not in 逻辑上不完全等同于not exists，如果你误用了not in，小心你的程序存在致命的BUG，请看下面的例子：


```sql
create table t1(c1 int,c2 int);
create table t2(c1 int,c2 int);

insert into t1 values(1,2);
insert into t1 values(1,3);
insert into t2 values(1,2);
insert into t2 values(1,null);

select * from t1 where c2 not in(select c2 from t2);--执行结果：无
select * from t1 where not exists(select 1 from t2 where t2.c2=t1.c2);--执行结果：1　　3
```


正如所看到的，not in出现了不期望的结果集，存在逻辑错误。如果看一下上述两个select 语句的执行计划，也会不同，后者使用了hash_aj，所以，请尽量不要使用not in（它会调用子查询），而尽量使用not exists（它会调用关联子查询）。


not in中如果子查询中返回的任意一条记录含有空值，则查询将不返回任何记录。如果子查询字段有非空限制，这时可以使用not in，并且可以通过提示让它用hash_aj或merge_aj连接。


如果查询语句使用了not in，那么对内外表都进行全表扫描，没有用到索引；而not exists的子查询依然能用到表上的索引。所以无论哪个表大，用not exists都比not in 要快。


注意：**NOT EXISTS 与 NOT IN 不能完全互相替换，看具体的需求。如果选择的列可以为空，则不能被替换。**

### 4.4.11 如果mysql估计使用全表扫描要比使用索引快,则不使用索引。


# 5 SQL优化


## 5.1 怎么发现有问题的SQL?


### 5.1.1 通过MySQL慢查询⽇志对有效率问题的SQL进⾏监控


- 慢查询⽇志是MySQL的⼀种⽇志记录， 记录在MySQL中响应时间超过阀值的语句，即运⾏时间超过`long_query_time`值的SQL，记录到慢查询⽇志中。
- `long_query_time`的默认值为10s。
- 查询出执⾏的次数多占⽤时间⻓的SQL、 通过`pt_query_disgest`（⼀种mysql慢⽇志分析⼯具）分析Rows examine（MySQL执⾏器需要检查的⾏数）项去找出IO⼤的SQL以及发现未命中索引的SQL，这些SQL，是我们优化的对象。

### 5.1.2 通过explain查询和分析SQL的执⾏计划


- explain 关键字可以知道MySQL是如何处理SQL语句的， 以此来分析查询语句、表结构的性能瓶颈。
- 通过explain命令可以得到表的读取顺序、数据读取操作的操作类型、哪些索引可以使⽤、哪些索引被实际使⽤、表之间的引⽤、每张表有多少⾏被优化器查询等问题。
- 扩展列extra出现Using filesort和Using temporay，则往往表示SQL需要优化了。

## 5.2 SQL语句优化


### 5.2.1 使用执行计划explain


- 尽量对数据库中的每⼀条SQL进⾏explain，收集他们的执⾏计划。
- ⼤多都需要去发掘，需要进⾏⼤量的explain操作收集执⾏计划，并判断是否需要进⾏优化。
- 优化SQL，需要做到⼼中有数，知道SQL的执⾏计划才能判断是否有优化余地，才能判断是否存在执⾏计划问题。

### 5.2.2 少计算


- MySQL的作⽤是⽤来存取数据的，不是做计算的。
- 做计算的话可以⽤其他⽅法去实现， MySQL做计算是很耗资源的。

### 5.2.3 少排序


- 排序会消耗较多 CPU 资源，所以减少排序可以在缓存命中率⾼、 IO 能⼒⾜够的场景下会影响 SQL 的响应时间。
- MySQL减少排序有多种办法：
  - 通过利⽤索引来排序的⽅式进⾏优化；
  - 减少参与排序的记录条数；
  - ⾮必要不对数据进⾏排序；

### 5.2.4 少⽤or


- 当 where ⼦句中存在多个条件以“或”并存的时候， MySQL 的优化器并没有很好的解决其执⾏计划优化问题，
- 再加上MySQL 特有的 SQL 与 Storage 分层架构⽅式，造成了其性能⽐较低下，
- 使⽤ union all 或者是union(必要的时候)的⽅式来代替“or”会得到更好的效果。



### 5.2.5 少⽤join


- 对于复杂的多表 Join，第⼀是优化器受限，第⼆在Join这⽅⾯性能表现离Oracle还有⼀定距离。
- MySQL的优势在于简单，但这在某些⽅⾯其实也是其劣势。
- MySQL 优化器效率⾼，但是由于其统计信息的量有限，优化器⼯作过程出现偏差的可能性也就更多。
- 但如果是简单的单表查询，这⼀差距就会极⼩甚⾄在有些场景下要优于这些数据库前辈。

### 5.2.6 ⽤ union all 代替 union


- union需要将两个(或者多个)结果集合并后再进⾏唯⼀性过滤操作，这就会涉及到排序，增加⼤量的CPU运算，加⼤资源消耗及延迟。
- 所以当我们可以确认不可能出现的时候，尽量使⽤ union all代替union。

### 5.2.7 尽量早过滤


- 该优化策略最常⻅于索引的优化设计中。
- 在 SQL 编写中使⽤这⼀原则来优化⼀些 Join 的 SQL。
  - ⽐如在多个表进⾏分⻚数据查询时，最好是能够在⼀个表上先过滤好数据并分好⻚。
  - 然后再⽤分好⻚的结果集与另外的表 Join，这样可以尽可能多的减少不必要的 IO 操作，⼤⼤节省 IO 操作所消耗的时间。

### 5.2.8 使用索引


需要遵循索引的使用原则，还需要注意一些不走索引的一些情况，这部分参见《索引优化部分》。


### 5.2.9 避免更新clustered（聚集）索引数据列


- 因为 ，⼀旦该列值改变将导致整个表记录的顺序的调整，会耗费相当⼤的资源。
- 如果应⽤系统需要频繁更新 clustered 索引数据列，那么需要考虑是否应将该索引建为clustered 索引。

> 聚集索引也称为聚簇索引（Clustered Index），聚类索引，簇集索引。
> 聚集索引是指数据库表行中数据的物理顺序与键值的逻辑（索引）顺序相同。一个表只能有一个聚集索引，因为一个表的物理顺序只有一种情况，所以，对应的聚集索引只能有一个。如果某索引不是聚集索引，则表中的行物理顺序与索引顺序不匹配，与非聚集索引相比，聚集索引有着更快的检索速度。

### 5.2.10 尽量使⽤数字类型字段


- 若只含数值信息的字段尽量不要设计为字符型，这会降低查询和连接的性能，并会增加存储开销。
  - 这是因为引擎在处理查询和连接时会逐个⽐较字符串中每⼀个字符，⽽对于数字型⽽⾔只需要⽐较⼀次就够了。

### 5.2.11 尽量⽤ varchar/nvarchar 代替char/nchar


- 变⻓字段存储空间灵活不固定。
- 其次对于查询来说，在⼀个相对较⼩的字段内搜索效率显然要⾼些。

> **char**是定长的，也就是当你输入的字符小于你指定的数目时，char(8)，你输入的字符小于8时，它会再后面补空值。当你输入的字符大于指定的数时，它会截取超出的字符。
> **varchar(n)** 长度为 n 个字节的可变长度且非 Unicode 的字符数据。n 必须是一个介于 1 和 8,000 之间的数值。存储大小为输入数据的字节的实际长度，而不是 n 个字节。所输入的数据字符长度可以为零。
> **nvarchar(n)** 包含 n 个字符的可变长度 Unicode 字符数据。n 的值必须介于 1 与 4,000 之间。字节的存储大小是所输入字符个数的两倍。所输入的数据字符长度可以为零。
> **text**存储可变长度的非Unicode数据，最大长度为2^31-1(2,147,483,647)个字符。
> nchar、nvarchar、ntext。这三种从名字上看比前面三种多了个“N”。它表示存储的是Unicode数据类型的字符。我们知道字符中，英文字符只需要一个字节存储就足够了，但汉字众多，需要两个字节存储，英文与汉字同时存在时容易造成混乱，Unicode字符集就是为了解决字符集这种不兼容的问题而产生的，它所有的字符都用两个字节表示，即英文字符也是用两个字节表示。nchar、nvarchar的长度是在1到4000之间。和char、varchar比较起来，nchar、nvarchar则最多存储4000个字符，不论是英文还是汉字；而char、varchar最多能存储8000个英文，4000个汉字。可以看出使用nchar、nvarchar数据类型时不用担心输入的字符是英文还是汉字，较为方便，但在存储英文时数量上有些损失。



### 5.2.12 用具体的字段列表代替通配符


任何地⽅都不要使⽤`select * from table_naem`，⽤什么字段取什么字段，减少不必要的资源浪费，不要返回⽤不到的任何字段。


### 5.2.13 避免使⽤临时表


- 除⾮确有需要，否则应尽量避免使⽤临时表，相反，可以使⽤表变量代替；
  - 如果表变量包含⼤量数据，请注意索引⾮常有限（只有主键索引）。
  - **临时表并不是不可使⽤**， 有时候它可以使某些例程更有效
    - 例如，当需要重复引⽤⼤型表或常⽤表中的某个数据集时。但是，对于⼀次性事件，最好使⽤导出表。
    - 在新建临时表时，如果⼀次性插⼊数据量很⼤， **可以使⽤ select into（MySQL不支持） 代替**
  **create table**，避免造成⼤量log，以提⾼速度；
    - 如果数据量不⼤，为了缓和系统表的资源，应先create table，然后insert。
  - 如果使⽤到了临时表，**在存储过程的最后务必将所有的临时表显式删除** ， 先truncate table ，然后 drop table ，这样可以避免系统表的较⻓时间锁定。
  - 避免频繁创建和删除临时表，以减少系统表资源的消耗。
- ⼤多数时候(99%)，表变量驻扎在内存中，因此速度⽐临时表更快，临时表驻扎在TempDb数据库中，因此临时表上的操作需要跨数据库通信，速度⾃然慢。
- 可以使⽤联合(UNION)来代替⼿动创建的临时表。
  - UNION 查询，它可以把需要使⽤临时表的两条或更多的 SELECT 查询合并的⼀个查询中；
  - 在客户端的查询会话结束的时候，临时表会被⾃动删除，从⽽保证数据库整⻬、⾼效；
  - 使⽤ UNION 来创建查询的时候，我们只需要⽤UNION作为关键字把多个SELECT语句连接起来就可以了，要注意的是所有 SELECT 语句中的字段数⽬要相同。
  - ```sql
  SELECT Name, Phone FROM client 
  UNION 
  SELECT Name, BirthDate FROM author
  UNION
  SELECT Name, Supplier FROM product;
    ```
> **表变量**
> - 存储在内存中，作用域是脚本的执行过程中，脚本执行完毕之后就会释放内存，适合短时间内存储数据量小的数据集。
> - **优点**：使用灵活，使用完之后立即释放，不占用物理存储空间；
> - **缺点**：只适合较小数据量的暂时存储，不能建索引，数据量稍大时查询效率慢，占内存
>
>   
>
> **临时表**
> - 临时表是存储在物理硬盘中的，建表位置在**tempdb**库中， 可以长久存储数据
> - **优点**：能够长久存储数据，可以建立索引，和普通的物理表一样，能存储大量数据
> - **缺点**：不方便使用，使用完之后要手动的drop,不然就会一直存在（此次连接关闭后就没了）
> - MySQL不支持select into 方式，替代方案：
>   - ```sql
>   Create TEMPORARY table new_table_name (Select * from old_table_name);
>     ```

> - create table方式：
>   - ```sql
>   create TEMPORARY table temptbone
>   (
>   id int,
>   name varchar(200)
>   );
>     insert into temptbone(id,name) values(1,'one');
>     
>     select * from temptbone; --临时表一直存在，直到链接关闭
>     
>     DROP TABLE IF EXISTS temptbone; --必须手动drop
>     ```

>
> 使用临时表和表变量的数据量大小没有具体的临界值，DBA建议1000条数据，查询列不要太多的情况下。

### 5.2.14 尽量少使⽤游标


- 游标是⼀种能从包括多条数据记录的结果集中每次提取⼀条记录的数据处理⼿段或者说机制 ，是指向查询结果集的⼀个指针。
- 因为游标的效率较差，如果游标操作的数据超过1万⾏，那么就应该考虑改写（游标是⼀个集合，使⽤存储过程需要使⽤游标）。
- 基于集的⽅法通常更有效，因此使⽤基于游标的⽅法或临时表⽅法之前，应先寻找基于集的解决⽅案来解决问题。
- **与临时表⼀样，游标并不是不可使⽤**：
  - 对⼩型数据集使⽤ FAST_FORWARD游标通常要优于其他逐⾏处理⽅法，尤其是在必须引⽤⼏个表才能获得所需的数据时。
  - 在结果集中包括“合计”的例程通常要⽐使⽤游标执⾏的速度快。如果开发时间允许，基于游标的⽅法和基于集的⽅法都可以尝试⼀下，看哪⼀种⽅法的效果更好。



### 5.2.15 优先优化⾼并发SQL


优先优化⾼并发SQL，⽽不是执⾏频率低某些“⼤”SQL。


SQL优化充分考虑系统中所有的SQL，尤其是在通过调整索引优化SQL的执⾏计划的时候，千万不能顾此失彼，因⼩失⼤。


### 5.2.16 尽量避免⼤数据量、⼤事务


尽量避免⼤事务操作，提⾼系统并发能⼒。


尽量避免向客户端返回⼤数据量，若数据量过⼤，应该考虑相应需求是否合理。


### 5.2.17 关于存储过程和触发器


在所有的存储过程和触发器的开始处设置 set nocount on，在结束时设置 set nocount on。

⽆需在执⾏存储过程和触发器的每个语句后向客户端发送 done_in_proc 。


### 5.2.18 尽量少做重复的⼯作


- 控制同⼀语句的多次执⾏，特别是⼀些基础数据的多次执⾏。
- 减少多次的数据转换。
- 杜绝不必要的⼦查询和连接表，⼦查询在执⾏计划⼀般解释成外连接，多余的连接表带来额外的开销。
- update操作不要拆成 delete + insert 的形式，虽然功能相同，但是性能差别是很⼤的。
- 不要写⼀些没有意义的查询： ⽐如： `SELECT * FROM EMPLOYEE WHERE 1=2`
- 优化insert语句：⼀次插⼊多值；
- 合并对同⼀表同⼀条件的多次update。