# 使用explain和`show profile`来分析SQL语句

# 1 概述

explain

- 查看SQL的执行计划。
- MySql Query Optimizer是MySql中专门负责优化select语句的优化器模块，其主要功能是**通过计算分析系统中收集到的系统信息，为客户端请求的Query提供他认为最优的执行计划**
  - 系统认为最优的数据检索方式，但不见得是真正最优的。

`show profile`：

- 查看SQL的执行的资源开销信息。

# 2 explain

## 2.1 用法

explain  展示mysql执行计划使用方法，在select语句前加上explain就可以了：

```sql
explain sql语句；
```

## 2.2 项目详解

|          项目 | 解释                                                         |
| ------------: | ------------------------------------------------------------ |
|            id | SELECT识别符，也就是SELECT的查询序列号，这个不重要,查询序号即为sql语句执行的顺序 |
|   select_type | SELECT类型,可以为以下任何一种：<br/><br/>- **SIMPLE**：简单SELECT，表示不需要union操作或者不包含子查询的简单select查询。有连接查询时，外层的查询为simple，且只有一个<br/>- **PRIMARY**：一个需要union操作或者含有子查询的select，位于最外层的单位查询的select_type即为primary，且只有一个<br/>- **UNION**：UNION连接的两个select查询，第一个查询是DERIVED派生表，除了第一个表外，第二个以后的表select_type都是UNION<br/>- **DEPENDENT UNION**：与UNION一样，出现在union 或union all语句中，但是这个查询要受到外部查询的影响<br/>- **UNION RESULT**：包含union的结果集，在union和union all语句中，因为它不需要参与查询，所以id字段为null<br/>- **SUBQUERY**：子查询中的第一个SELECT<br/>- **DEPENDENT SUBQUERY**：与DEPENDENT UNION类似，表示这个SUBQUERY的查询要受到外部表查询的影响<br/>- **DERIVED**：from子句中出现的子查询，也叫做衍生表，其他数据库中可能叫做内联视图或嵌套select |
|         table | 显示的查询表名。<br/>如果查询使用了别名，那么这里显示的是别名；<br/>如果不涉及对数据表的操作，那么这显示为null；<br/>如果显示为尖括号括起来的`<derived N>`就表示这个是临时表，后边的N就是执行计划中的id，表示结果来自于这个查询产生；<br/>如果是尖括号括起来的`<union M,N>`，与`<derived N>`类似，也是一个临时表，表示这个结果来自于union查询的id为M,N的结果集。 |
|          type | 联接类型。下面给出各种联接类型，按照从最佳类型到最坏类型进行排序：<br/><br/>- **system**：表中只有一行数据或者是空表，且只能用于myisam和memory表。如果是Innodb引擎表，type列在这个情况通常都是all或者index<br/>- **const**：表最多有一个匹配行，它将在查询开始时被读取。因为仅有一行，在这行的列值可被优化器剩余部分认为是常数。const表很快，因为它们只读取一次！使用唯一索引或者主键，返回记录一定是1行记录的等值where条件时，通常type是const。<br/>- **eq_ref**：出现在要连接过个表的查询计划中，驱动表只返回一行数据，且这行数据是第二个表的主键或者唯一索引，且必须为not null，唯一索引和主键是多列时，只有所有的列都用作比较时才会出现eq_ref。<br/>- **ref**：不像eq_ref那样要求连接顺序，也没有主键和唯一索引的要求，只要使用相等条件检索时就可能出现，常见与辅助索引的等值查找。或者多列主键、唯一索引中，使用第一个列之外的列作为等值查找也会出现，总之，返回数据不唯一的等值查找就可能出现。<br/>- **fulltext**：全文索引检索，要注意，全文索引的优先级很高，若全文索引和普通索引同时存在时，mysql不管代价，优先选择使用全文索引<br/>- **ref_or_null**：该联接类型如同ref，只是增加了null值的比较，实际用的不多。<br/>- **unique_subquery**：用于where中的in形式子查询，子查询返回不重复值唯一值。 `value IN (SELECT primary_key FROM single_table WHERE some_expr) `<br/>- **index_subquery**：该联接类型类似于unique_subquery，用于in形式子查询使用到了辅助索引或者in常数列表，子查询可能返回重复值，可以使用索引将子查询去重。<br/>- **range**：索引范围扫描，常见于使用>，<，is null，between，in，like等运算符的查询中。<br/>- **index_merge**：表示查询使用了两个以上的索引，最后取交集或者并集，常见and ，or的条件使用了不同的索引，官方排序这个在ref_or_null之后，但是实际上由于要读取所个索引，性能可能大部分时间都不如range<br/>- **index**：该联接类型与ALL相同，除了只有索引树被扫描。这通常比ALL快,因为索引文件通常比数据文件小。<br/>- **ALL**：对于每个来自于先前的表的行组合，进行完整的表扫描。 |
| possible_keys | 查询可能使用到的索引都会在这里列出来                         |
|           key | 显示MySQL实际决定使用的索引。如果没有使用索引，为NULL。<br/>select_type为index_merge时，这里可能出现两个以上的索引，其他的select_type这里只会出现一个。 |
|       key_len | 用于处理查询的索引长度。<br/>如果是单列索引，那就整个索引长度算进去。<br/>如果是多列索引，那么查询不一定都能使用到所有的列，具体使用到了多少个列的索引，这里就会计算进去，没有使用到的列，这里不会计算进去。留意下这个列的值，算一下你的多列索引总长度就知道有没有使用到所有的列了。<br/>注意：mysql的ICP特性使用到的索引不会计入其中。<br/>注意：key_len只计算where条件用到的索引长度，而排序和分组就算用到了索引，也不会计算到key_len中。 |
|           ref | 显示使用哪个列或常数与索引一起从表中选择行。<br/>如果是使用的常数等值查询，这里会显示const。<br/>如果是连接查询，被驱动表的执行计划这里会显示驱动表的关联字段。<br/>如果是条件使用了表达式或者函数，或者条件列发生了内部隐式转换，这里可能显示为func |
|          rows | 这里是执行计划中估算的扫描行数，但不是精确值。               |
|      filtered | 使用explain extended时会出现这个列，5.7之后的版本默认就有这个字段，不需要使用explain extended了。<br/>这个字段表示存储引擎返回的数据在server层过滤后，剩下多少满足查询的记录数量的比例，注意是百分比，不是具体记录数。 |
|         Extra | 常用的有：<br/>- **distinct**：在select部分使用了distinc关键字<br/>- **no tables used**：不带from字句的查询或者From dual查询<br/>- **using filesort**：排序时无法使用到索引时，就会出现这个。常见于order by和group by语句中<br/>- **using index**：查询时不需要回表查询，直接通过索引就可以获取查询的数据。<br/>- **using join buffer（block nested loop），using join buffer（batched key accss）**：5.6.x之后的版本优化关联查询的BNL，BKA特性。主要是减少内表的循环数量以及比较顺序地扫描查询。<br/>- **using intersect**：表示使用and的各个索引的条件时，该信息表示是从处理结果获取交集<br/>- **using union**：表示使用or连接各个使用索引的条件时，该信息表示从处理结果获取并集<br/>- **using sort_union**和**using sort_intersection**：与前面两个对应的类似，只是他们是出现在用and和or查询信息量大时，先查询主键，然后进行排序合并后，才能读取记录并返回。<br/>- **using temporary**：表示使用了临时表存储中间结果。临时表可以是内存临时表和磁盘临时表，执行计划中看不出来，需要查看status变量，used_tmp_table，used_tmp_disk_table才能看出来。<br/>- **using where**：表示存储引擎返回的记录并不是所有的都满足查询条件，需要在server层进行过滤。查询条件中分为限制条件和检查条件，5.6之前，存储引擎只能根据限制条件扫描数据并返回，然后server层根据检查条件进行过滤再返回真正符合查询的数据。5.6.x之后支持ICP（Index Condition Pushdown）特性，可以把检查条件也下推到存储引擎层，不符合检查条件和限制条件的数据，直接不读取，这样就大大减少了存储引擎扫描的记录数量。extra列显示using index condition<br/>- **firstmatch(tb_name)**：5.6.x开始引入的优化子查询的新特性之一，常见于where字句含有in()类型的子查询。如果内表的数据量比较大，就可能出现这个。<br/>- **loosescan(m..n)**：5.6.x之后引入的优化子查询的新特性之一，在in()类型的子查询中，子查询返回的可能有重复记录时，就可能出现这个。 |

## 2.3 SQL需要优化的情况

1. 出现了Using temporary，一般临时表排序，需要优化
2. 出现了Using filesort，排序时无法使用到索引时，就会出现这个
3. rows过多，或者几乎是全表的记录数
4. key 是 (NULL)
5. possible_keys 出现过多（待选）索引

# 3 `show profile`

在MySQL数据库中，可以通过配置profiling参数来启用SQL剖析。该参数可以在全局和session级别来设置。对于全局级别则作用于整个MySQL实例，而session级别紧影响当前session。该参数开启后，后续执行的SQL语句都将记录其资源开销，诸如IO，上下文切换，CPU，Memory等等。根据这些开销进一步分析当前SQL瓶颈从而进行优化与调整。

## 3.1 开启功能

查看profiling是否开启：`select @@profiling;`

- 0：表示profiling功能是关闭；
- 1：表示打开的。

profiling功能的开启和关闭：

- 开启：`set profiling=1;`
- 关闭：`set profiling=0;`

**注**：开启profiling后，我们可以通过show profile等方式查看，其实质是这些开销信息被记录到information_schema.profiling表

## 3.2 查看最近执行的SQL的资源消耗

```sql
--先执行需要查看资源消耗的SQL语句，然后执行show profile;查看上一条SQL语句的开销信息
show profile;
```

## 3.3 详细用法

可以使用`help profile;`查看`show profile`的详细用法：

```
SHOW PROFILE [type [, type] ... ] 
[FOR QUERY n] 
[LIMIT row_count [OFFSET offset]] 
```

- type：可以一次查看多个type，多个type使用逗号`,`分割
  - ALL：显示所有的开销信息 
  - BLOCK IO：显示块IO相关开销 
  - CONTEXT SWITCHES：上下文切换相关开销 
  - CPU：显示CPU相关开销信息 
  - IPC：显示发送和接收相关开销信息 
  - MEMORY：显示内存相关开销信息 
  - PAGE FAULTS：显示页面错误相关开销信息 
  - SOURCE：显示和Source_function，Source_file，Source_line相关的开销信息 
  - SWAPS：显示交换次数相关开销的信息 

- QUERY n：
  - SQL语句的Query_ID，表示显示哪条SQL的资源开销信息；
  - 使用`show profiles;`查看SQL的Query_ID；



