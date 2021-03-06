# 分库分表

# 1 为什么需要分库分表

读写分离分散了数据库的读写操作的压力，但是没有分散存储的压力，当数据量达到千万甚至上亿条数据的时候，单台数据库服务器的存储能力会成为系统的瓶颈，主要体现在以下几个方面。

- 数据量太大，读写的性能就会下降，即使有索引，索引也会变得很大，性能同样会下降。(可以考虑表分区)
- 数据文件会变得很大，数据库备份和恢复需要耗费很长时间。
- 数据文件越大，极端情况下丢失数据的风险越高。(数据库服务器文件损毁，服务器启动不了，机房失火等)

基于上述原因，单个数据库服务存储的数据量不能太大，需要控制在一定的范围内，为了满足业务数据存储的需求，就需要将存储分散到多台数据库服务器上。

# 2 业务分库

业务分库就是按照业务模块将数据分散到不同的数据库服务器。例如央企电商平台，可以将用户数据、商品数据、订单数据分开放到三台不同的数据库服务器上，而不是将所有的数据都放到一台数据库服务器上。但是会产生新的问题，如下

- join操作问题：需要业务层使用业务数据去关联
- 事务问题：使用Mysql提供的XA，阿里巴巴中间件Seata，但是会有性能问题
- 成本：多数据源维护

# 3 分表

将不同的业务分散存储到不同的数据库服务器，能够支撑百万甚至千万用户规模的业务，但是如果业务继续发展，同一个业务的单表的数据也会达到单台数据库服务器的处理瓶颈。

单表的数据拆分有两种方式：垂直分表和水平分表。

## 3.1 垂直分表

适合将表中某些不常用且占用大量空间的列拆分出去。

## 3.2 水平分表

适合表行数特别大的表。

水平分表后，某条数据具体属于哪个切分后的字表，需要增加路由算法进行计算。

### 3.2.1 范围路由

1. 选取有序的数据列（整型、时间戳等）作为路由条件，不同的分段分散到不同的数据库表中，以最常见的用户ID为例，路由算法可以按照100000的范围大小进行分段，1~99999放到数据库1中，100000~199999放到第二个表中，以此类推。
2. **范围路由设计的复杂点**主要体现在分段大小的选取上，分段太小会导致切分后的子表的数量过多，增加维护的复杂度，分段太大的话，可能会导致单表的性能仍然存在问题，具体要根据业务去选取合适的分段大小。

3. 范围路由的**优点**是可以随着数据的增加平滑的扩充新的表。
4. 范围路由一个比较隐含的**缺点**就是分布不均匀，假如按照1000万来进行分表，可能某个分段只有100条数据，另外的分段实际存储的数据有900万条。

### 3.2.2 Hash路由

1. 选取某个列（或者几个列的组合）的值进行hash运算，然后根据hash结果分散到不同的数据库表中，同样以用户ID为例子，假如我们一开始就规划了10个数据库表，路由算法可以简单的使用user_id%10的值来表示数据所有的表编号，ID为1005的用户放到编号为5的子表中,ID为1006放到编号为6的字表中。
2. **Hash路由设计的复杂点**主要体现在初始表数量的选取上，表数量太多维护比较麻烦，表数量太少的话，单表的性能又存在问题。使用Hash路由后，增加子表数量是比较麻烦的，所有的数据都要重新分布。
3. Hash路由的**优点**就是表数据分布比较均匀。
4. Hash路由的**缺点**就是扩充新表比较麻烦，所有的数据要重新分布。

### 3.2.3 配置路由

1. 配置路由就是路由表，用一张独立的表来记录路由信息，同样以用户ID为例，我们新增一张user_router表，这个表包含user_id和table_id，根据user_id可以查询出对应的table_id。
2. 配置路由的设计简单，使用起来非常灵活，尤其是在扩充表的时候，只需要迁移指定的数据，然后修改路由表就可以了。
3. 配置路由的**缺点**就是必须多查询一次，会影响整体性能。而且如果路由表本身如果太大的话，性能同样成为瓶颈。如果我们再次将路由表分库分表，则又面临一个死循环式的路由算法选择的问题。

# 4 分库分表后一些SQL操作的解决方案

## 4.1 join

水平分表后，数据分散到多个表中，如果需要与其他的表进行join查询，需要在业务代码或数据库中间件中进行多次join查询，然后将结果合并。

## 4.2 `count()`

- `count()`相加，即:对所有的业务表都进行`count()`操作，然后将结果相加。
    - 性能低

- 记录数表，即：维护一张记录数表，包好table_name、row_count两个字段。需要每次插入或者删除子表数据成功后，更新这个记录数表。不是很重要的表，可以使用定时任务，定期的维护。

## 4.3 `order by`

水平分表后，数据分散到多个子表中，排序操作无法在数据库中完成，只能有业务代码或者数据库中间件分表查询每个子表的数据，然后进行汇总排序。