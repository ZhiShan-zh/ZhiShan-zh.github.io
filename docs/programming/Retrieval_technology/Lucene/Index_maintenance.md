# 索引维护

# 1 索引库

- 结构化数据

  - 有固定格式和有限长度，以二维表形式
- 非结构化数据

  - 可以序列化到磁盘的数据

# 2 需求

管理人员通过电商系统更改图书信息，这时更新的是关系数据库，如果使用lucene搜索图书信息，需要在数据库表book信息变化时及时更新lucene索引库。

# 3 添加索引

调用 `indexWriter.addDocument(doc)`添加索引。<br />
参考入门程序的创建索引。

# 3 删除索引

## 3.1 删除指定索引

根据Term项删除索引，满足条件的将全部删除。

```java
package com.zh.lucene;

import java.io.File;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.junit.Test;

public class IndexManagerTest {
	@Test
	public void testIndexDelete() throws Exception {
		// 创建Directory流对象
		Directory directory = FSDirectory.open(new File("/home/zh/dic/index"));
		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_4_10_3, null);
		// 创建写入对象
		IndexWriter indexWriter = new IndexWriter(directory, config);

		// 根据Term删除索引库，name:java
		indexWriter.deleteDocuments(new Term("name", "java"));
		
		// 释放资源
		indexWriter.close();
	}
}
```

## 3.2 删除全部索引（慎用）

将索引目录的索引信息全部删除，直接彻底删除，无法恢复。

建议参照关系数据库基于主键删除方式，所以在创建索引时需要创建一个主键Field，删除时根据此主键Field删除。<br />
索引删除后将放在Lucene的回收站中，Lucene3.X版本可以恢复删除的文档，3.X之后无法恢复。

```java
package com.zh.lucene;

import java.io.File;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.junit.Test;

public class IndexManagerTest {
	@Test
	public void testIndexDelete() throws Exception {
		// 创建Directory流对象
		Directory directory = FSDirectory.open(new File("/home/zh/dic/index"));
		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_4_10_3, null);
		// 创建写入对象
		IndexWriter indexWriter = new IndexWriter(directory, config);

		// 根据Term删除索引库，name:java
		//indexWriter.deleteDocuments(new Term("name", "java"));
        // 全部删除
		indexWriter.deleteAll();
		
		// 释放资源
		indexWriter.close();
	}
}
```

# 4 修改索引

更新索引是先删除再添加，建议对更新需求采用此方法并且要保证对已存在的索引执行更新，可以先查询出来，确定更新记录存在执行更新操作。

如果更新索引的目标文档对象不存在，则执行添加。

```java
package com.zh.lucene;

import java.io.File;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field.Store;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.junit.Test;

public class IndexManagerTest {
	@Test
	public void testIndexUpdate() throws Exception {
		// 创建分词器
		//Analyzer analyzer = new IKAnalyzer();
		Analyzer analyzer = new StandardAnalyzer();
		// 创建Directory流对象
		Directory directory = FSDirectory.open(new File("/home/zh/dic/index"));
		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_4_10_3, analyzer);
		// 创建写入对象
		IndexWriter indexWriter = new IndexWriter(directory, config);

		// 创建Document
		Document document = new Document();
		document.add(new TextField("id", "1002", Store.YES));
		document.add(new TextField("name", "lucene测试test 002", Store.YES));

		// 执行更新，会把所有符合条件的Document删除，再新增。
		indexWriter.updateDocument(new Term("name", "test"), document);

		// 释放资源
		indexWriter.close();
	}
}
```
