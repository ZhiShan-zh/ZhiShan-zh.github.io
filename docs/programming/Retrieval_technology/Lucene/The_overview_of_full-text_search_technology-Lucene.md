# Lucene全文检索技术概述

# 1 搜索技术理论基础


## 1.1 为什么要学习Lucene


### 1.1.1 原始搜索引擎技术

原始搜索引擎技术就是使用数据库中like，我们的搜索流程如下图：![](https://zhishan-zh.github.io/media/lucene-1586492721863-15cc380c-90b8-4c9f-bfcd-4ca9b7111e53.png)上图就是原始搜索引擎技术，如果用户比较少而且数据库的数据量比较小，那么这种方式实现搜索功能在企业中是比较常见的。

但是数据量过多时，数据库的压力就会变得很大，查询速度会变得非常慢。我们需要使用更好的解决方案来分担数据库的压力。

### 1.1.2 现在的搜索技术方案

现在的方案（使用Lucene），如下图<br />
![](https://zhishan-zh.github.io/media/lucene-1586492732524-7da11b6e-0147-4377-adee-2c8a21eed8c2.png)为了解决数据库压力和速度的问题，我们的数据库就变成了索引库，我们使用Lucene的API的来操作服务器上的索引库。这样完全和数据库进行了隔离。

**Lucene的作用**：优化查询速度。由于数据库搜索使用顺序扫描法，查询非常慢，尤其是在互联网中，使用sql语句中的like关键字模糊查询，随着数据量变大，查询的效率越来越低，所以需要使用lucene来优化查询速度。

## 1.2 数据查询方法


### 1.2.1 顺序扫描法

**顺序扫扫描法**：拿着需要搜索的关键字，去要搜索的内容中逐字匹配，直到找到位置，如果没有找到则到文件结尾位置。

- **优点**：不管数据有多少，只要包含关键字始终都能查到。
- **缺点**：慢、很慢，数据越大越慢。



### 1.2.2 全文检索算法

**倒排索引**：倒排索引源于实际应用中需要根据属性的值来查找记录。这种索引表中的每一项都包括一个属性值和具有该属性值的各记录的地址。由于不是由记录来确定属性值，而是由属性值来确定记录的位置，因而称为倒排索引（inverted index）。带有倒排索引的文件我们称为倒排索引文件，简称倒排文件（inverted file）。

**全文检索算法**：（**倒排索引表算法**）将需要查询的内容拿出来，进行分词、组成目录（索引），查询的时候可以先查询目录（索引），通过索引找文档的这个过程叫做全文检索。

- **优点**：快，查询非常快。
- **缺点**：占用额外的磁盘空间。
- **是用空间换时间的算法。**

**分词**：就是把一句话分成一个一个的词，去掉空格，去掉标点符号，大写转小写，去掉停用词（的、啊、恩、the、a、an等没有实际意义的词）。

## 1.3 搜索技术应用场景


- 单机软件的搜索（word中的搜索）
- 站内搜索 （baidu贴吧、论坛、 京东、 taobao）
- 垂直领域的搜索 （818工作网）
  - 数据来自域某个领域或行业
- 专业搜索引擎公司 （google、baidu）



# 2 Lucene介绍


## 2.1 什么是全文索引

计算机索引程序通过扫描文章中的每一个词，对每一个词建立一个索引，指明该词在文章中出现的次数和位置，当用户查询时，检索程序就根据事先建立的索引进行查找，并将查找的结果反馈给用户的检索方式。

## 2.2 什么是Lucene

Lucene是apache软件基金会4 jakarta项目组的一个子项目，是一个开放源代码的全文检索引擎工具包，但它不是一个完整的全文检索引擎，而是一个全文检索引擎的架构，提供了完整的查询引擎和索引引擎，部分文本分析引擎（英文与德文两种西方语言）。

Lucene的目的是为软件开发人员提供一个简单易用的工具包，以方便的在目标系统中实现全文检索的功能，或者是以此为基础建立起完整的全文检索引擎。

目前已经有很多应用程序的搜索功能是基于 Lucene 的，比如 Eclipse 的帮助系统的搜索功能。Lucene 能够为文本类型的数据建立索引，所以你只要能把你要索引的数据格式转化的文本的，Lucene 就能对你的文档进行索引和搜索。比如你要对一些 HTML 文档，PDF 文档进行索引的话你就首先需要把 HTML 文档和 PDF 文档转化成文本格式的，然后将转化后的内容交给 Lucene 进行索引，然后把创建好的索引文件保存到磁盘或者内存中，最后根据用户输入的查询条件在索引文件上进行查询。不指定要索引的文档的格式也使 Lucene 能够几乎适用于所有的搜索应用程序。

- Lucene是一套用于全文检索和搜寻的开源程式库，由Apache软件基金会支持和提供；
- Lucene提供了一个简单却强大的应用程序接口，能够做全文索引和搜寻，在Java开发环境里Lucene是一个成熟的免费开放源代码工具；
- **Lucene并不是现成的搜索引擎产品，但可以用来制作搜索引擎产品**。

# 3 Lucene与搜索引擎的区别

全文检索系统是按照全文检索理论建立起来的用于提供全文检索服务的软件系统，包括建立索引、处理查询返回结果集、增加索引、优化索引结构等功能。例如：百度搜索、eclipse帮助搜索、淘宝网商品搜索等。

搜索引擎是全文检索技术最主要的一个应用，例如百度。搜索引擎起源于传统的信息全文检索理论：

1. 计算机程序通过扫描每一篇文章中的每一个词，建立以词为单位的倒排文件，
2. 检索程序根据检索词在每一篇文章中出现的频率和每一个检索词在一篇文章中出现的概率，对包含这些检索词的文章进行排序，最后输出排序的结果。

全文检索技术是搜索引擎的核心支撑技术。

Lucene和搜索引擎不同，Lucene是一套用java或其它语言写的全文检索的工具包，为应用程序提供了很多个api接口去调用，可以简单理解为是一套实现全文检索的类库，搜索引擎是一个全文检索系统，它是一个单独运行的软件系统。

# 4 Lucene全文检索的流程


## 4.1 Lucene全文检索的流程图

![](https://zhishan-zh.github.io/media/lucene-1586492757393-3d462f79-a9c8-4424-a7d0-123143038acc.png)**解释**：

1. 绿色表示索引过程，对要搜索的原始内容进行索引构建一个索引库，索引过程包括：确定原始内容即要搜索的内容、获得文档、创建文档 、分析文档、索引文档
2. 红色表示搜索过程，从索引库中搜索内容，搜索过程包括：用户通过搜索界面、创建查询、执行搜索，从索引库搜索、渲染搜索结果

**注意**：

- 原始文档格式不限。
- 索引库：在硬盘中创建一个文件夹，包含索引文档和文档文件

## 4.2 索引文件格式

Lucene版本：8.5.2

参考：https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/package-summary.html#package.description

### 4.2.1 定义

Lucene中的基本概念是索引（index），文档（document），字段（field）和项（term）。

索引包含一系列文档。

- 文档包含一系列的字段。
- 字段是用来命名一些列的项。
- 项包含一系列的字节。

两个不同字段中相同的字节序列被视为不同的项。因此，项成对出现：命名字段的字符串和字段中的字节。

### 4.2.2 字段的类型

在Lucene中，

- 可以存储字段，在这种情况下，它们的文本将以非反转的方式按字面意义存储在索引中。 
- 反转的字段称为索引。 字段可以被存储和被索引。

### 4.2.3 段

Lucene索引可以由多个子索引或段组成。 每个段都是完全独立的索引，可以分别进行搜索。索引按以下方式演变：

1. 为新添加的文档创建新的段。
2. 合并现有的段。

搜索可能涉及多个段和/或多个索引，每个索引可能由一组段组成。

### 4.2.4 文档编号

在内部，Lucene通过整数文档号引用文档。 添加到索引的第一个文档编号为零，并且随后添加的每个文档的编号都比前一个大。

请注意，文档编号可能会更改，因此在将这些编号存储在Lucene之外时应格外小心。 特别是，在以下情况下编号可能会更改：

- 存储在每个段中的编号仅在该段内是唯一的，并且必须进行转换才能在更大的上下文中使用它们。
    - 标准技术是根据该段中使用的数字范围为每个段分配一个值范围。 
    - 要将文档编号从段内值转换为外部值，需要添加段的基本文档编号。 
    - 要将外部值转换回特定段的值，可以通过外部值所在的范围来标识段，然后减去段的基值。
    - 例如，可以合并两个五个文档的段，若第一个段的基值为0，第二个段的基值为5，则第二个段的第三个文档的外部值为8。
        - 不应该是7吗？
- 删除文档后，在编号中会留出空白。随着索引通过合并的发展，这些空白最终被删除。 合并段时会删除已删除的文档。 因此，新合并的段在编号上没有间隙。

### 4.2.5 索引结构概述

每个索引段包含如下内容：

- [`Segment info`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene70/Lucene70SegmentInfoFormat.html). 其中包含有关段的元数据，例如文档数量，使用的文件，
- [`Field names`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene60/Lucene60FieldInfosFormat.html). 它包含索引中使用的一组字段名。
- [`Stored Field values`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50StoredFieldsFormat.html). 每个文档都包含一个属性-值对列表，其中属性是字段名称。 这些列表被用于存储有关文档的辅助信息，例如其标题，URL或用于访问数据库的标识符。 搜索时，每个命中将返回存储的字段集。 这些返回的字段集由文件编号被查出。
- [`Term dictionary`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/Lucene84PostingsFormat.html). 这个字典包含所有文档的所有索引字段中使用的所有的项。 词典还包含包含该项的文档编号，以及指向该项的频率和相似数据的指针。
- [`Term Frequency data`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/Lucene84PostingsFormat.html). For each term in the dictionary, the numbers of all the documents that contain that term, and the frequency of the term in that document, unless frequencies are omitted ([`IndexOptions.DOCS`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/index/IndexOptions.html#DOCS))
- [`Term Proximity data`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/Lucene84PostingsFormat.html). For each term in the dictionary, the positions that the term occurs in each document. Note that this will not exist if all fields in all documents omit position data.
- [`Normalization factors`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene80/Lucene80NormsFormat.html). For each field in each document, a value is stored that is multiplied into the score for hits on that field.
- [`Term Vectors`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50TermVectorsFormat.html). For each field in each document, the term vector (sometimes called document vector) may be stored. A term vector consists of term text and term frequency. To add Term Vectors to your index see the [`Field`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/document/Field.html) constructors
- [`Per-document values`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene80/Lucene80DocValuesFormat.html). Like stored values, these are also keyed by document number, but are generally intended to be loaded into main memory for fast access. Whereas stored values are generally intended for summary results from searches, per-document values are useful for things like scoring factors.
- [`Live documents`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50LiveDocsFormat.html). An optional file indicating which documents are live.
- [`Point values`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene60/Lucene60PointsFormat.html). Optional pair of files, recording dimensionally indexed fields, to enable fast numeric range filtering and large numeric values like BigInteger and BigDecimal (1D) and geographic shape intersection (2D, 3D).

### 4.2.6 文件命名

属于一个段的所有文件都具有相同的名称，但具有不同的扩展名。 扩展名对应于以下描述的不同文件格式。 使用“复合文件”格式（小段的默认设置）时，这些文件（段信息文件，锁定文件和已删除的文档文件除外）将折叠为单个`.cfs`文件（有关详细信息，请参见下文）

通常，索引中的所有段都存储在一个目录中，但这并不是必需的。

文件名永远不会重复使用。 也就是说，将任何文件保存到目录时，都将获得一个从未使用过的文件名。 这是通过简单的生成方法实现的。 例如，第一个句段文件名是`segment_1`，然后是`segment_2`，依此类推。生成的是一个连续的长整数，以文字数的（基数36）形式表示。

### 4.2.7 文件扩展名概述

| Name                                                         | Extension  | Brief Description                                            |
| ------------------------------------------------------------ | ---------- | ------------------------------------------------------------ |
| [`Segments File`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/index/SegmentInfos.html) | segments_N | Stores information about a commit point                      |
| [Lock File](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/package-summary.html#Lock_File) | write.lock | The Write lock prevents multiple IndexWriters from writing to the same file. |
| [`Segment Info`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene70/Lucene70SegmentInfoFormat.html) | .si        | Stores metadata about a segment                              |
| [`Compound File`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50CompoundFormat.html) | .cfs, .cfe | An optional "virtual" file consisting of all the other index files for systems that frequently run out of file handles. |
| [`Fields`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene60/Lucene60FieldInfosFormat.html) | .fnm       | Stores information about the fields                          |
| [`Field Index`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50StoredFieldsFormat.html) | .fdx       | Contains pointers to field data                              |
| [`Field Data`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50StoredFieldsFormat.html) | .fdt       | The stored fields for documents                              |
| [`Term Dictionary`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/Lucene84PostingsFormat.html) | .tim       | The term dictionary, stores term info                        |
| [`Term Index`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/Lucene84PostingsFormat.html) | .tip       | The index into the Term Dictionary                           |
| [`Frequencies`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/Lucene84PostingsFormat.html) | .doc       | Contains the list of docs which contain each term along with frequency |
| [`Positions`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/Lucene84PostingsFormat.html) | .pos       | Stores position information about where a term occurs in the index |
| [`Payloads`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene84/Lucene84PostingsFormat.html) | .pay       | Stores additional per-position metadata information such as character offsets and user payloads |
| [`Norms`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene80/Lucene80NormsFormat.html) | .nvd, .nvm | Encodes length and boost factors for docs and fields         |
| [`Per-Document Values`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene80/Lucene80DocValuesFormat.html) | .dvd, .dvm | Encodes additional scoring factors or other per-document information. |
| [`Term Vector Index`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50TermVectorsFormat.html) | .tvx       | Stores offset into the document data file                    |
| [`Term Vector Data`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50TermVectorsFormat.html) | .tvd       | Contains term vector data.                                   |
| [`Live Documents`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene50/Lucene50LiveDocsFormat.html) | .liv       | Info about what documents are live                           |
| [`Point values`](https://lucene.apache.org/core/8_5_2/core/org/apache/lucene/codecs/lucene60/Lucene60PointsFormat.html) | .dii, .dim | Holds indexed points, if any                                 |

### 4.2.8 锁文件

默认情况下，存储在索引目录中的写锁名为“ write.lock”。 如果锁目录与索引目录不同，则写锁将被命名为“ XXXX-write.lock”，其中XXXX是从索引目录的完整路径派生的唯一前缀。 存在此文件时，编写者当前正在修改索引（添加或删除文档）。 该锁文件可确保一次只有一个写程序正在修改索引。

## 4.3 索引流程

对文档索引的过程，将用户要搜索的文档内容进行索引，索引存储在索引库（index）中。

### 4.3.1 原始内容


- 原始内容是指要索引和搜索的内容。
- 原始文档格式不限。
- 原始内容包括互联网上的网页、数据库中的数据、磁盘上的文件等。



### 4.3.2 获得文档（采集数据）

<br />从互联网上、数据库、文件系统中等获取需要搜索的原始信息，这个过程就是信息采集，采集数据的目的是为了对原始内容进行索引。<br />

#### 4.3.2.1 采集数据分类


- 对于互联网上网页，可以使用工具将网页抓取到本地生成html文件。
- 数据库中的数据，可以直接连接数据库读取表中的数据。
- 文件系统中的某个文件，可以通过I/O操作读取文件的内容。



#### 4.3.2.2 采集数据技术

<br />在Internet上采集信息的软件通常称为爬虫或蜘蛛，也称为网络机器人，爬虫访问互联网上的每一个网页，将获取到的网页内容存储起来。<br />
<br />**Lucene不提供信息采集的类库**，需要自己编写一个爬虫程序实现信息采集，也可以通过一些开源软件实现信息采集，如下：<br />

- **Solr**（http://lucene.apache.org/solr） ，solr是apache的一个子项目，支持从关系数据库、xml文档中提取原始数据。
- **Nutch**（http://lucene.apache.org/nutch）, Nutch是apache的一个子项目，包括大规模爬虫工具，能够抓取和分辨web网站数据。
- **jsoup**（[http://jsoup.org/](http://jsoup.org/) ），jsoup 是一款Java 的HTML解析器，可直接解析某个URL地址、HTML文本内容。它提供了一套非常省力的API，可通过DOM，CSS以及类似于jQuery的操作方法来取出和操作数据。



#### 4.3.2.3 lucene和solr的区别


- lucene是一个全文检索工具包，它就是一堆jar包可以用它来做像百度这样的全文检索系统。
- solr是一个现成的全文检索系统, 它放到tomcat下可以独立运行。



### 4.3.3 创建文档

<br />获取原始内容的目的是为了索引，在索引前需要将原始内容创建成文档（Document），文档中包括一个一个的域（Field），域中存储内容。<br />
这里我们可以将磁盘上的一个文件当成一个document，Document中包括一些Field。<br />
<br />注意：每个Document可以有多个Field，不同的Document可以有不同的Field，同一个Document可以有相同的Field（域名和域值都相同）<br />

### 4.3.4 分析文档

<br />将原始内容创建为包含域（Field）的文档（document），需要再对域中的内容进行分析，分析成为一个一个的单词。<br />
<br />比如下边的文档经过分析如下：<br />
原文档内容：<br />

> Lucene is a Java full-text search engine.  Lucene is not a complete<br />
application, but rather a code library and API that can easily be used<br />
to add search capabilities to applications.


<br />分析后得到的词：<br />

> lucene、java、full、search、engine......



### 4.3.5 索引文档

<br />对所有文档分析得出的语汇单元进行索引，，最终要实现只搜索被索引的语汇单元从而找到Document（文档）。<br />
<br />创建索引是对语汇单元索引，通过词语找文档，这种索引的结构叫倒排索引结构。<br />
<br />倒排索引结构是根据内容（词汇）找文档，如下图：<br />
<br />![](https://zhishan-zh.github.io/media/lucene-1586492793063-3ff45491-3455-4823-b58c-4632af8c0d14.png)**倒排索引结构也叫反向索引结构，包括索引和文档两部分，索引即词汇表，它的规模较小，而文档集合较大。**

## 4.4 搜索流程

搜索就是用户输入关键字，从索引中进行搜索的过程。根据关键字搜索索引，根据索引找到对应的文档，从而找到要搜索的内容。<br />

### 4.4.1 用户

就是使用搜索的角色，用户可以是自然人，也可以是远程调用的程序。

### 4.4.2 用户搜索界面

全文检索系统提供用户搜索的界面供用户提交搜索的关键字，搜索完成展示搜索结果。如下图：![image-20200410120551789.png](https://zhishan-zh.github.io/media/lucene-1586492806776-79e6f132-d6d4-4a68-9f8b-dfe277f9fa3c.png)**注意**：Lucene不提供制作用户搜索界面的功能，需要根据自己的需求开发搜索界面。

### 4.4.3 创建查询

用户输入查询关键字执行搜索之前需要先构建一个查询对象，查询对象中可以指定查询要查询关键字、要搜索的Field文档域等，查询对象会生成具体的查询语法，比如：

- name:lucene表示要搜索name这个Field域中，内容为“lucene”的文档。
- desc:lucene AND desc:java 表示要搜索即包括关键字“lucene”也包括“java”的文档。

### 4.4.4 执行搜索


1. 根据查询语法在倒排索引词典表中分别找出对应搜索词的索引，从而找到索引所链接的文档链表。例如搜索语法为“desc:lucene AND desc:java”表示搜索出的文档中既要包括lucene也要包括java。
2. 由于是AND，所以要对包含lucene或java词语的链表进行交集，得到文档链表应该包括每一个搜索词语
3. 获取文档中的Field域数据。

### 4.4.5 渲染结果

以一个友好的界面将查询结果展示给用户，用户根据搜索结果找自己想要的信息，为了帮助用户很快找到自己的结果，提供了很多展示的效果，比如搜索结果中将关键字高亮显示，百度提供的快照等。![](https://zhishan-zh.github.io/media/lucene-1586492818362-eecb14db-347f-4ca6-80c0-fb33b46f8d95.png)