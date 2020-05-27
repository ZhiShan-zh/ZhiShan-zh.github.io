# Field域

# 1 Field属性

Field是文档中的域，包括Field名和Field值两部分，一个文档可以包括多个Field，Document只是Field的一个承载体，Field值即为要索引的内容，也是要搜索的内容。

## 1.1 tokenized：是否分词

- 是：作分词处理，即将Field值进行分词，分词的目的是为了创建索引。

  - 需要创建索引的时候并且分词后有意义的字段可以分词。
  - 比如：商品名称、商品描述等，这些内容用户要输入关键字搜索，由于搜索的内容格式大、内容多需要分词后将语汇单元建立索引
- 否：不作分词处理。

  - 不需要进行创建索引的域就不需要分词，分词后无意义的域不要分词。
  - 比如：商品id、订单号、身份证号等

## 1.2 indexed：是否索引

- 是：进行索引。将Field分词后的词或整个Field值进行索引，存储到索引域，索引的目的是为了搜索。

  - 我们需要用这个域来进行查询，那么就需要索引。
  - 比如：商品名称、商品描述分析后进行索引，订单号、身份证号不用分词但也要索引，这些将来都要作为查询条件。
- 否：不索引。

  - 如果不需要对这个域进行查询就可以不索引。
  - 比如：图片路径、文件路径等，不用作为查询条件的不用索引。

## 1.3 stored：是否存储

- 指的是存储在文档对象中的Doucument。
- 是：将Field值存储在文档域中，存储在文档域中的Field才可以从Document中获取。

  - 存储的目的是为了显示。
  - 比如：商品名称、订单号，凡是将来要从Document中获取的Field都要存储。
- 否：不存储Field值

  - 比如：商品描述，内容较大不用存储。如果要向用户展示商品描述可以从系统的关系数据库中获取。

# 2 Field常用类型

下边列出了开发中常用 的Filed类型，注意Field的属性，根据需求选择：

| Field类 | 数据类型 | Analyzed是否分词 | Indexed是否索引 | Stored是否存储 | 说明 |
| :--- | --- | --- | --- | --- | --- |
| `StringField(FieldName, 		FieldValue,Store.YES))` | 字符串 | N | Y | Y或N | 这个Field用来构建一个字符串Field，但是不会进行分词，会将整个串存储在索引中，比如(订单号,身份证号等) 		是否存储在文档中用Store.YES或Store.NO决定 |
| LongField(FieldName, 		FieldValue,Store.YES) | Long型 | Y | Y | Y或N | 这个Field用来构建一个Long数字型Field，进行分词和索引，比如(价格)是否存储在文档中用Store.YES或Store.NO决定<br />**注意**：由于lucene底层的算法，对价格对比进行了一系列的算法封装，所以对于需要价格进行对比的域，进行分词，对于数字的分词我们是控制不了的，是lucene底层的要求。 |
| `StoredField(FieldName, 		FieldValue)` | 重载方法，支持多种类型 | N | N | Y | 这个Field用来构建不同类型Field 不分析，不索引，但要Field存储在文档中 |
| `TextField(FieldName, 		FieldValue, Store.NO)` <br />或<br />`TextField(FieldName, 		reader)` | 字符串或流 | Y | Y | Y或N | 如果是一个Reader, lucene猜测内容比较多,会采用Unstored的策略。 |


## 3 Field修改

## 3.1 修改分析

图书id：<br />
是否分词：不用分词，因为不会根据商品id来搜索商品<br />
是否索引：不索引，因为不需要根据图书ID进行搜索<br />
是否存储：要存储，因为id是主键，又不会占用很大的磁盘空间，所以要存储，存储后可以进行后续操作。

图书名称：<br />
是否分词：要分词，因为要根据图书名称的关键词搜索。<br />
是否索引：要索引，因为我们需要根据名称进行搜索。<br />
是否存储：要存储，因为我们需要将名称拿出来在页面显示。

图书价格：<br />
是否分词：要分词，lucene对数字型的值只要有搜索需求的都要分词和索引，因为lucene对数字型的内容要特殊分词处理，需要分词和索引。<br />
是否索引：要索引，因为需要根据价格进行查询。<br />
是否存储：要存储，因为列表页需要显示出来。

图书图片地址：<br />
是否分词：不分词，图片路径分词无意义<br />
是否索引：不索引，不需要根据图片路径进行查询<br />
是否存储：要存储，因为需要显示图片。

图书描述：<br />
是否分词：要分词，因为需要根据描述进行查询，而描述分词后有意义。<br />
是否索引：要索引，因为我们需要根据描述进行查询。<br />
是否存储：不存储，查询后的列表没有直接显示出来，所以不需要存储，而详情页需要的时候可以将这条数据的主键查出来后些sql语句，再去数据库进行查询，因为根据主机拿查询非常快，所以这么设计可以节省大量的磁盘空间，又不会特别慢，性价比高。

不存储是不在lucene的索引域中记录，节省lucene的索引文件空间。

如果要在详情页面显示描述，解决方案：<br />
从lucene中取出图书的id，根据图书的id查询关系数据库（MySQL）中book表得到描述信息。

## 3.2 代码修改

对之前编写的testCreateIndex()方法进行修改。

修改部分代码：

```java
// Document文档中添加域
// 图书Id
// Store.YES:表示存储到文档域中
// 不分词，不索引，储存
document.add(new StoredField("id", book.getId().toString()));
// 图书名称
// 分词，索引，储存
document.add(new TextField("name", book.getName().toString(), Store.YES));
// 图书价格
// 分词，索引，储存
document.add(new FloatField("price", book.getPrice(), Store.YES));
// 图书图片地址
// 不分词，不索引，储存
document.add(new StoredField("pic", book.getPic().toString()));
// 图书描述
// 分词，索引，不储存
document.add(new TextField("desc", book.getDesc().toString(), Store.NO));
```
