# 相关度排序

# 1 什么是相关度排序

相关度排序是查询结果按照与查询关键字的相关性进行排序，越相关的越靠前。比如搜索“Lucene”关键字，与该关键字最相关的文章应该排在前边。

# 2 相关度打分

Lucene对查询关键字和索引文档的相关度进行打分，得分高的就排在前边。

## 2.1 怎么打分

如何打分呢？Lucene是在用户进行检索时实时根据搜索的关键字计算出来的，分两步：

1. 计算出词（Term）的权重；
2. 根据词的权重值，计算文档相关度得分。

## 2.2 词的权重

通过索引部分的学习，明确索引的最小单位是一个Term(索引词典中的一个词)。搜索也是从索引域中查询Term，再根据Term找到文档。

Term对文档的重要性称为权重，影响Term权重有两个因素：

- `Term Frequency (tf)`：

  - 指此Term在此文档中出现了多少次。tf 越大说明越重要。
  - 词(Term)在文档中出现的次数越多，说明此词(Term)对该文档越重要，如“Lucene”这个词，在文档中出现的次数很多，说明该文档主要就是讲Lucene技术的。
- `Document Frequency (df)`：

  - 指有多少文档包含此Term。df 越大说明越不重要。
  - 比如，在一篇英语文档中，this出现的次数更多，就说明越重要吗？不是的，有越多的文档包含此词(Term), 说明此词(Term)太普通，不足以区分这些文档，因而重要性越低。

# 3 设置boost值影响相关度排序

boost是一个加权值（默认加权值为1.0f），它可以影响权重的计算。在索引时对某个文档中的field设置加权值，设置越高，在搜索时匹配到这个文档就可能排在前边。

先清空索引库，然后修改创建索引的代码，添加设置加权值的逻辑

修改创建索引代码：

```java
@Test
public void testCreateIndex() throws Exception {
	// 1. 采集数据
	BookDao bookDao = new BookDaoImpl();
	List<Book> bookList = bookDao.queryBookList();

	// 2. 创建Document文档对象
	List<Document> documents = new ArrayList<>();
	for (Book book : bookList) {
		Document document = new Document();

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
		TextField descField = new TextField("desc", book.getDesc().toString(), Store.NO);
		// 给id为4的文档设置加权值
		if (4 == book.getId()) {
			descField.setBoost(100f);
		}
		document.add(descField);

		// 把Document放到list中
		documents.add(document);

	}

	// 3. 创建Analyzer分词器,分析文档，对文档进行分词
	Analyzer analyzer = new StandardAnalyzer();

	// 4. 创建IndexWrite，需要directory流对象
	// 创建流对象
	Directory directory = FSDirectory.open(new File("D:/itcast/lucene/index"));

	// 创建IndexWriteConfig对象
	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_4_10_3, analyzer);

	// 创建IndexWriter写入对象
	IndexWriter indexWriter = new IndexWriter(directory, config);

	// 通过IndexWriter添加文档对象document
	for (Document doc : documents) {
		indexWriter.addDocument(doc);
	}
	// 释放资源
	indexWriter.close();
}
```
