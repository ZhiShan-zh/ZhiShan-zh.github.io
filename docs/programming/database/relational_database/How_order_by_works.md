# `ORDER BY`的工作原理

# 1 概述

`ORDER BY`排序有两种实现方法：

1. 索引排序：利用有序索引获取有序数据；
2. 文件排序：利用内存或磁盘文件排序算法获取结果
   - 双路排序：是首先根据相应的条件取出相应的排序字段和可以直接定位行数据的行指针信息，然后在sort buffer 中进行排序。 
   - 单路排序：是一次性取出满足条件行的所有字段，然后在sort buffer中进行排序。

# 2 使用索引满足`ORDER BY`

以下内容参见[ORDER BY Optimization](https://dev.mysql.com/doc/refman/8.0/en/order-by-optimization.html)

在某些情况下，MySQL可以使用索引来满足ORDER BY子句，并避免执行文件排序操作时涉及的额外排序。



## 2.1 `ORDER BY`使用联合索引情况

The index may also be used even if the ORDER BY does not match the index exactly, as long as all unused portions of the index and all extra ORDER BY columns are constants in the WHERE clause. If the index does not contain all columns accessed by the query, the index is used only if index access is cheaper than other access methods.

只要索引的所有未使用部分和所有额外的ORDER BY列在WHERE子句中都是常量，即使ORDER BY与索引不完全匹配，也可以使用索引。 如果索引不包含查询访问的所有列，则仅当索引访问比其他访问方法代价低时才使用索引。

假设在 `(key_part1, key_part2)`上有一个索引，以下查询可以使用该索引来解析`ORDER BY`部分。 如果还必须读取索引中没有的列，优化器实际上是否这样做读取决于读取索引是否比表扫描效率更好。

- 在此查询中， `(key_part1, key_part2)`上的索引使优化器避免排序：

```sql
SELECT * FROM t1
  ORDER BY key_part1, key_part2;
```

但是，查询使用 `SELECT *`，这可能会选择比 `key_part1` 和`key_part2`更多的列。 在这种情况下，扫描整个索引并查找表中不在索引中的列可能比扫描表并排序代价要高。 如果是这样的话，优化器可能不会使用索引。 如果`SELECT *`仅选择索引列，则将使用索引并避免排序。

如果`t1`是`InnoDB`表，则表主键隐式属于索引的一部分，并且该索引可用于解析此查询的 `ORDER BY` ：

```sql
SELECT pk, key_part1, key_part2 FROM t1
  ORDER BY key_part1, key_part2;
```

- 在此查询中，`key_part1`是常量，因此通过索引访问的所有行均按`key_part2`顺序排列，并且如果`WHERE`子句的选择性足以使索引范围扫描比表扫描代价低，则`(key_part1，key_part2)`上的索引可以避免排序：

```sql
SELECT * FROM t1
  WHERE key_part1 = constant
  ORDER BY key_part2;
```

- 在接下来的两个查询中，是否使用索引和前面没有DESC的查询类似：

```sql
SELECT * FROM t1
  ORDER BY key_part1 DESC, key_part2 DESC;

SELECT * FROM t1
  WHERE key_part1 = constant
  ORDER BY key_part2 DESC;
```

- Two columns in an `ORDER BY` can sort in the same direction (both `ASC`, or both `DESC`) or in opposite directions (one `ASC`, one `DESC`). A condition for index use is that the index must have the same homogeneity, but need not have the same actual direction.

-  `ORDER BY` 中的两列可以按相同方向（都是`ASC`或都是`DESC`）或相反方向（一个`ASC`，一个`DESC`）排序。 使用索引的条件是索引必须具有相同的同质性，但不必具有相同的实际方向。

如果查询将 `ASC` 和`DESC`混合使用，则只有索引还使用了相应的混合升序和降序列，优化器才可以在列上使用索引：

```sql
SELECT * FROM t1
  ORDER BY key_part1 DESC, key_part2 ASC;
```

如果`key_part1`递减而`key_part2`递增，则优化器可以在`(key_part1, key_part2)`上使用索引。 如果`key_part1`递增而`key_part2`递减，它也可以在这些列上使用索引（向后扫描）。参见[Section 8.3.13, “Descending Indexes”](https://dev.mysql.com/doc/refman/8.0/en/descending-indexes.html)

- 在接下来的两个查询中，将`key_part1`与常量进行比较。 如果`WHERE`子句的选择性足以使索引范围扫描比表扫描代价低，那么将使用索引：

```sql
SELECT * FROM t1
  WHERE key_part1 > constant
  ORDER BY key_part1 ASC;

SELECT * FROM t1
  WHERE key_part1 < constant
  ORDER BY key_part1 DESC;
```

- 在下一个查询中，`ORDER BY`不使用`key_part1`，但是所有选择的行都具有恒定的`key_part1`值，因此仍可以使用索引：

```sql
SELECT * FROM t1
  WHERE key_part1 = constant1 AND key_part2 > constant2
  ORDER BY key_part2;
```

## 2.2 `ORDER BY`不使用索引的情况

在某些情况下，尽管可是可以使用索引来查找与WHERE子句匹配的行，但是MySQL不能使用索引来解析`ORDER BY`。 

- 在不同的索引上使用`ORDER BY`：

```sql
SELECT * FROM t1 ORDER BY key1, key2;
```

- 对索引的非连续字段上使用`ORDER BY`：

```sql
SELECT * FROM t1 WHERE key2=constant ORDER BY key1_part1, key1_part3;
```

- 用于获取数据的索引和`ORDER BY`上使用的索引不同:

```sql
SELECT * FROM t1 WHERE key2=constant ORDER BY key1;
```

-  `ORDER BY` 使用除索引列名之外的表达式:

  ```sql
  SELECT * FROM t1 ORDER BY ABS(key);
  SELECT * FROM t1 ORDER BY -key;
  ```

- 该查询联接了许多表，`ORDER BY`中的列并非全部来自用于检索行的第一个非恒定表。 （这是 [`EXPLAIN`](https://dev.mysql.com/doc/refman/8.0/en/explain.html) 输出中的第一个不具有[`const`](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html#jointype_const)联接类型的表。）

-  `ORDER BY` 和 `GROUP BY` 的表达式不同。

- There is an index on only a prefix of a column named in the `ORDER BY` clause. In this case, the index cannot be used to fully resolve the sort order. For example, if only the first 10 bytes of a [`CHAR(20)`](https://dev.mysql.com/doc/refman/8.0/en/char.html) column are indexed, the index cannot distinguish values past the 10th byte and a `filesort` is needed.

- 仅在ORDER BY子句中命名的列的前缀上存在索引。 在这种情况下，索引不能用于完全解析排序顺序。 例如，如果仅索引 [`CHAR(20)`](https://dev.mysql.com/doc/refman/8.0/en/char.html)列的前10个字节，则索引无法区分第10个字节之后的值，因此需要进行`filesort`。

- 索引不按顺序存储行。 例如， `MEMORY` 表中的`HASH`索引就是这种情况。

使用列别名可能会影响索引排序的可用性。 假设索引是`t1.a`。 在此语句中，选择列表中列的名称为`a`，它引用`t1.a`，就像在`ORDER BY`中引用a一样，因此可以使用`t1.a`上的索引：

```sql
SELECT a FROM t1 ORDER BY a;
```

在此语句中，选择列表中列的名称也为`a`，但这里的`a`是一个别名，它引用的是`ABS（a）`，就像`ORDER BY`子句中引用的`a`一样，因此这里不能使用`t1.a`上的索引：

```sql
SELECT ABS(a) AS a FROM t1 ORDER BY a;
```

在下面的语句中，`ORDER BY`引用的名称不是选择列表中列的名称。 但是在`t1`中有一个名为`a`的列，因此`ORDER BY`指向`t1.a`，并且这里可以使用`t1.a`上的索引。 （当然，生成的排序顺序可能与`ABS(a)`的顺序完全不同。）

```sql
SELECT ABS(a) AS b FROM t1 ORDER BY a;
```

以前（MySQL 5.7及更低版本），`GROUP BY`在某些条件下隐式排序。 在MySQL 8.0中，不再发生这种情况，因此不再需要在末尾指定`ORDER BY NULL`以抑制隐式排序（如前所述）。 但是，查询结果可能与以前的MySQL版本不同。 要产生给定的排序顺序，请提供一个ORDER BY子句。

# 3 使用文件排序满足ORDER BY

如果不能使用索引来满足`ORDER BY`子句，则MySQL执行`filesort`操作来读取表行并对它们进行排序。 文件排序在查询执行中构成了额外的排序阶段。

为了获得用于`filesort`操作的内存，从MySQL 8.0.12开始，优化器根据需要以增量方式分配内存缓冲区，最大可达`sort_buffer_size`系统变量指示的大小，而不是像在MySQL 8.0.12之前的版本做的那样在开始的时候就分配`sort_buffer_size`固定数量的字节。这使用户可以将[`sort_buffer_size`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sort_buffer_size) 设置为较大的值以加快大型排序的速度，而不必担心小型排序会占用过多的内存。 （在具有弱多线程`malloc`的Windows上，对于多个并发排序可能不会有此效果。）

如果结果集太大而无法容纳在内存中，则`filesort`操作会根据需要使用临时磁盘文件。某些类型的查询特别适合完全在内存中的`filesort`操作。 例如，对以下形式的查询（和子查询）执行`ORDER BY`操作，优化器可以使用`filesort`在内存中（没有临时文件）来有效地处理内存：

```sql
SELECT ... FROM single_table ... ORDER BY non_index_column [DESC] LIMIT [M,]N;
```

如此只显示较大结果集中的几行的查询在web应用程序中很常见。例如：

```sql
SELECT col1, ... FROM t1 ... ORDER BY name LIMIT 10;
SELECT col1, ... FROM t1 ... ORDER BY RAND() LIMIT 15;
```

# 4 优化ORDER BY

对于没有使用`filesort`的慢速 `ORDER BY` 查询，请尝试将 [`max_length_for_sort_data`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_length_for_sort_data) 系统变量降低到适合于触发“文件排序”的值。 （将此变量的值设置得太高带来的后遗症就是磁盘活动过多和CPU活动较低。）此技术仅在MySQL 8.0.20之前适用。 从8.0.20版本开始，由于优化程序的更改而使[`max_length_for_sort_data`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_length_for_sort_data)变得过时且不起作用，因此不建议使用[`max_length_for_sort_data`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_length_for_sort_data)。

为了提高`ORDER BY`的速度，请检查是否可以使MySQL使用索引而不是额外的排序阶段。 如果这不可能，请尝试以下策略：

- 增加[`sort_buffer_size`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sort_buffer_size)变量值。 理想情况下，该值应足够大以使排序缓存正好适合整个结果集（以避免写入磁盘和合并过程）。

  应该注意的是存储在排序缓冲区中的列值的大小受系统变量[`max_sort_length`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_sort_length)的值的影响。例如，如果元组存储长字符串值列，并且你增加了[`max_sort_length`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_sort_length)的值，则排序缓冲区元组的大小也会增加，并且可能会要求你增加[`sort_buffer_size`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sort_buffer_size)。

  To monitor the number of merge passes (to merge temporary files), check the [`Sort_merge_passes`](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Sort_merge_passes) status variable.

  要监视合并次数（合并临时文件），请检查[`Sort_merge_passes`](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Sort_merge_passes)状态变量。

- 增加[`read_rnd_buffer_size`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_read_rnd_buffer_size)变量值，以便一次能读取更多行。

- 更改[`tmpdir`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_tmpdir)系统变量，使其指向具有大量可用空间的专用文件系统。 变量值可以配置多个路径并以循环方式使用它们；你可以使用此特性将负载分散到多个目录中。 在Unix上用冒号（`:`)分隔多个路径，在Windows上用分号（`;`）分隔多个路径。 路径应选择位于不同物理磁盘上的文件系统中的目录，而不是同一磁盘上的不同分区。

# 5 使用执行计划来了解`ORDER BY`的优化信息

你可以使用[`EXPLAIN`](https://dev.mysql.com/doc/refman/8.0/en/explain.html)（请参见[Section 8.8.1, “Optimizing Queries with EXPLAIN”](https://dev.mysql.com/doc/refman/8.0/en/using-explain.html)）来检查MySQL是否可以使用索引来解析`ORDER BY`子句：

- 如果[`EXPLAIN`](https://dev.mysql.com/doc/refman/8.0/en/explain.html)输出的`Extra`列不包含`Using filesort`，则使用索引，并且不执行`filesort`。
- 如果[`EXPLAIN`](https://dev.mysql.com/doc/refman/8.0/en/explain.html)输出的`Extra`列包含`Using filesort`，则不使用索引，而是执行`filesort`。

另外，如果执行`filesort`，优化程序跟踪输出将包含`filesort_summary`内容。例如：

```json
"filesort_summary": {
  "rows": 100,
  "examined_rows": 100,
  "number_of_tmp_files": 0,
  "peak_memory_used": 25192,
  "sort_mode": "<sort_key, packed_additional_fields>"
}
```

`peak_memory_used`表示排序期间使用的最大内存。 该值最大为系统变量[`sort_buffer_size`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sort_buffer_size)的值，但不一定等于其值。 在MySQL 8.0.12之前，输出为`sort_buffer_size`，指示[`sort_buffer_size`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html #sysvar_sort_buffer_size)的值。 （在MySQL 8.0.12之前，优化器始终分配[`sort_buffer_size`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sort_buffer_size)大小的字节进行排序。但是从8.0.12开始，优化器刚开始分配比较小的排序缓存区内存，然后根据需要分配更多的内存，但最大分配[`sort_buffer_size`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sort_buffer_size)数量的字节的内存。）

`sort_mode`的值提供了有关排序缓冲区中元组内容的信息：

- `<sort_key, rowid>`：这表明排序缓冲区元组是包含排序键的值和原始表中的行ID。 元组按排序键的值排序，然后使用行ID用于从表中读取行。
- `<sort_key, additional_fields>`：这表明排序缓冲区元组包含排序键的值和查询中所引用的列。 元组通过排序键值进行排序，然后直接从元组中读取列的值。
- `<sort_key, packed_additional_fields>`：是上一模式的变体，但是不一样的其他列被紧密地打包在一起，而不是使用固定长度的编码。

[`EXPLAIN`](https://dev.mysql.com/doc/refman/8.0/en/explain.html)不能区分优化器是否是在内存中执行`filesort`。 在优化器跟踪输出中可以看到是否是在内存中进行`filesort`。 可以查看`filesort_priority_queue_optimization`，来获取此信息。 有关优化程序跟踪的信息，参见[MySQL Internals: Tracing the Optimizer](https://dev.mysql.com/doc/internals/en/optimizer-tracing.html)。