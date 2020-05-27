# 分词器

# 1 分词理解

<br />在对Docuemnt中的内容进行索引之前，需要使用分词器进行分词 ，分词的目的是为了搜索。分词的主要过程就是先分词后过滤。<br />
<br />**分词**：采集到的数据会存储到document对象的Field域中，分词就是将Document中Field的value值切分成一个一个的词。<br />
**过滤**：包括去除标点符号过滤、去除停用词过滤（的、是、a、an、the等）、大写转小写、词形还原（复数形式转成单数形参、过去式转成现在式......）等。<br />
<br />**停用词**：停用词是为节省存储空间和提高搜索效率，搜索引擎在索引页面或处理搜索请求时会自动忽略某些字或词，这些字或词即被称为Stop Words(停用词)。比如语气助词、副词、介词、连接词等，通常自身并无明确的意义，只有将其放入一个完整的句子中才有一定作用，如常见的“的”、“在”、“是”、“啊”等。<br />
<br />对于分词来说，不同的语言，分词规则不同。Lucene作为一个工具包提供不同国家的分词器，本例子使用StandardAnalyzer，它可以对用英文进行分词。<br />
<br />如下是`org.apache.lucene.analysis.standard.standardAnalyzer`的部分源码：<br />

```java
@Override
protected TokenStreamComponents createComponents(final String fieldName, final Reader reader) {
    final StandardTokenizer src = new StandardTokenizer(getVersion(), reader);
    src.setMaxTokenLength(maxTokenLength);
    TokenStream tok = new StandardFilter(getVersion(), src);
    tok = new LowerCaseFilter(getVersion(), tok);
    tok = new StopFilter(getVersion(), tok, stopwords);
    return new TokenStreamComponents(src, tok) {
        @Override
        protected void setReader(final Reader reader) throws IOException {
            src.setMaxTokenLength(StandardAnalyzer.this.maxTokenLength);
            super.setReader(reader);
        }
    };
}
```

<br />Tokenizer就是分词器，负责将reader转换为语汇单元即进行分词处理，Lucene提供了很多的分词器，也可以使用第三方的分词，比如IKAnalyzer一个中文分词器。<br />
<br />TokenFilter是分词过滤器，负责对语汇单元进行过滤，TokenFilter可以是一个过滤器链儿，Lucene提供了很多的分词器过滤器，比如大小写转换、去除停用词等。<br />
<br />如下图是语汇单元的生成过程：<br />
<br />![image-20200410160551272.png](https://zhishan-zh.github.io/media/lucene-1586507982916-94e1b835-b771-401b-bb43-d32ef1c27edb.png)<br />
<br />从一个Reader字符流开始，创建一个基于Reader的Tokenizer分词器，经过三个TokenFilter生成语汇单元Token。<br />
<br />比如下边的文档经过分析器分析如下：原文档内容为`Lucene is a Java full-test search engine.`，分析后得到的多个语汇单元`lucene、java、full、text、search、engine`。<br />

# 2 Analyzer使用时机


## 2.1 索引时使用Analyzer

<br />输入关键字进行搜索，当需要让该关键字与文档域内容所包含的词进行匹配时需要对文档域内容进行分析，需要经过Analyzer分析器处理生成语汇单元（Token）。分析器分析的对象是文档中的Field域。当Field的属性tokenized（是否分词）为true时会对Field值进行分析，如下图：<br />
<br />![image-20200410161013785.png](https://zhishan-zh.github.io/media/lucene-1586508006099-c10c75e7-117a-413c-8724-58358746aaeb.png)<br />
<br />一些Field可以不用分析：<br />

1. 不作为查询条件的内容，比如文件路径；
2. 不是匹配内容中的词而匹配Field的整体内容，比如订单号、身份证号等。



## 2.2 搜索时使用Analyzer

<br />对搜索关键字进行分析和索引分析一样，使用Analyzer对搜索关键字进行分析、分词处理，使用分析后每个词语进行搜索。比如：搜索关键字：spring web ，经过分析器进行分词，得出：spring web拿词去索引词典表查找 ，找到索引链接到Document，解析Document内容。<br />
<br />对于匹配整体Field域的查询可以在搜索时不分析，比如根据订单号、身份证号查询等。<br />
<br />**注意：搜索使用的分析器要和索引使用的分析器一致。**<br />

# 3 中文分词器


## 3.1 什么是中文分词器

<br />学过英文的都知道，英文是以单词为单位的，单词与单词之间以空格或者逗号句号隔开。所以对于英文，我们可以简单以空格判断某个字符串是否为一个单词，比如I love China，love 和 China很容易被程序区分开来。<br />
<br />而中文则以字为单位，字又组成词，字和词再组成句子。中文“我爱中国”就不一样了，电脑不知道“中国”是一个词语还是“爱中”是一个词语。<br />
<br />把中文的句子切分成有意义的词，就是中文分词，也称切词。我爱中国，分词的结果是：我、爱、中国。<br />

## 3.2 Lucene自带中文分词器

<br />StandardAnalyzer：<br />

> 单字分词：就是按照中文一个字一个字地进行分词。如：“我爱中国”，<br />
效果：“我”、“爱”、“中”、“国”。


<br />CJKAnalyzer<br />

> 二分法分词：按两个字进行切分。如：“我是中国人” ，效果：“我是”、“是中”、“中国”“国人”。


<br />SmartChineseAnalyzer<br />

> 上边两个分词器无法满足需求。
> 对中文支持较好，但扩展性差，扩展词库，禁用词库和同义词库等不好处理



## 3.3 第三方中文分词器


- **paoding**： 庖丁解牛最新版在https://code.google.com/p/paoding/中最多支持Lucene 3.0，且最新提交的代码在 2008-06-03，在svn中最新也是2010年提交，已经过时，不予考虑。
- **mmseg4j**：最新版已从https://code.google.com/p/mmseg4j/移至https://github.com/chenlb/mmseg4j-solr，支持Lucene 4.10，且在github中最新提交代码是2014年6月，从09年～14年一共有：18个版本，也就是一年几乎有3个大小版本，有较大的活跃度，用了mmseg算法。
- **IK-analyzer**： 最新版在https://code.google.com/p/ik-analyzer/上，支持Lucene 4.10从2006年12月推出1.0版开始， IKAnalyzer已经推出了4个大版本。最初，它是以开源项目Luence为应用主体的，结合词典分词和文法分析算法的中文分词组件。从3.0版本开 始，IK发展为面向Java的公用分词组件，独立于Lucene项目，同时提供了对Lucene的默认优化实现。在2012版本中，IK实现了简单的分词 歧义排除算法，标志着IK分词器从单纯的词典分词向模拟语义分词衍化。 但是也就是2012年12月后没有在更新。
- **ansj_seg**：最新版本在https://github.com/NLPchina/ansj_segtags仅有1.1版本，从2012年到2014年更新了大小6次，但是作者本人在2014年10月10日说明：“可能我以后没有精力来维护ansj_seg了”，现在由”nlp_china”管理。2014年11月有更新。并未说明是否支持Lucene，是一个由CRF（条件随机场）算法所做的分词算法。
- **imdict-chinese-analyzer**：最新版在https://code.google.com/p/imdict-chinese-analyzer/， 最新更新也在2009年5月，下载源码，不支持Lucene 4.10 。是利用HMM（隐马尔科夫链）算法。
- **Jcseg**：最新版本在git.oschina.net/lionsoul/jcseg，支持Lucene 4.10，作者有较高的活跃度。利用mmseg算法。



## 3.4 使用中文分词器IKAnalyzer

<br />IKAnalyzer继承Lucene的Analyzer抽象类，使用IKAnalyzer和Lucene自带的分析器方法一样，将Analyzer测试代码改为IKAnalyzer测试中文分词效果。<br />
<br />如果使用中文分词器ik-analyzer，就需要在索引和搜索程序中使用一致的分词器：IK-analyzer。<br />

### 3.4.1 添加jar包

<br />`IKAnalyzer2012FF_u1.jar`<br />

### 3.4.2 修改分词器代码

<br />**查看**：实现索引流程和搜索流程中的代码<br />

## 3.5 扩展中文词库

<br />如果想配置扩展词和停用词，就创建扩展词的文件和停用词的文件。<br />
<br />注意：不要用window自带的记事本保存扩展词文件和停用词文件，那样的话，格式中是含有bom的。<br />
<br />从ikanalyzer包中拷贝配置文件：比如IKAnalyzer的从官网下载的压缩包中的`ext.dic`、`IKAnalyzer.cfg.xml`、`stopword.dic`，把这三个文件拷贝到项目根目录的配置文件夹config（`lucene/config`）中。<br />

### 3.5.1 IKAnalyzer.cfg.xml


```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">  
<properties>  
	<comment>IK Analyzer 扩展配置</comment>
	<!--用户可以在这里配置自己的扩展字典 	-->
	<entry key="ext_dict">ext.dic;</entry> 

	<!--用户可以在这里配置自己的扩展停止词字典-->
	<entry key="ext_stopwords">stopword.dic;</entry> 
</properties>
```


### 3.5.2 扩展词库ext.dic

<br />中文词库，添加新词的地方<br />

```
全文搜索
砺锋科技
```


### 3.5.3 停用词库stopword.dic

<br />存放停用词的地方<br />

```
a
an
and
are
as
at
be
......
```
