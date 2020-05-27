# 搜索

# 1 创建查询的两种方法

对要搜索的信息创建Query查询对象，Lucene会根据Query查询对象生成最终的查询语法。类似关系数据库Sql语法一样，Lucene也有自己的查询语法，比如：“name:lucene”表示查询名字为name的Field域中的“lucene”的文档信息。

## 1.1 使用Lucene提供Query子类

Query是一个抽象类，lucene提供了很多查询对象，比如TermQuery项精确查询，NumericRangeQuery数字范围查询等。

```java
Query query = new TermQuery(new Term("name", "lucene"));
```

## 1.2 使用QueryParse解析查询表达式

QueryParser会将用户输入的查询表达式解析成Query对象实例。

```java
QueryParser queryParser = new QueryParser("name", new IKAnalyzer());
Query query = queryParser.parse("name:lucene");
```

# 2 通过Query子类搜索

## 2.1 TermQuery

TermQuery词项查询，TermQuery不使用分析器，搜索关键词进行精确匹配Field域中的词，比如订单号、分类ID号等。

只支持文本类型的查询。<br />
不建议使用TermQuery，因为它的功能比QueryParser要弱。

### 2.1.1 创建搜索对象

```java
package com.zh.lucene;

import org.apache.lucene.index.Term;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TermQuery;
import org.junit.Test;

public class IndexManagerTest {
	@Test
	public void testSearchTermQuery() throws Exception {
		// 创建TermQuery搜索对象
		Query query = new TermQuery(new Term("name", "lucene"));

		doSearch(query);
	}
}
```

### 2.1.2 抽取搜索逻辑

```java
package com.zh.lucene;

import java.io.File;
import java.io.IOException;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

public class IndexManagerTest {
	private void doSearch(Query query) throws IOException {
		// 2. 执行搜索，返回结果集
		// 创建Directory流对象
		Directory directory = FSDirectory.open(new File("/home/zh/dic/index"));

		// 创建索引读取对象IndexReader
		IndexReader reader = DirectoryReader.open(directory);

		// 创建索引搜索对象
		IndexSearcher searcher = new IndexSearcher(reader);

		// 使用索引搜索对象，执行搜索，返回结果集TopDocs
		// 第一个参数：搜索对象，第二个参数：返回的数据条数，指定查询结果最顶部的n条数据返回
		TopDocs topDocs = searcher.search(query, 10);

		System.out.println("查询到的数据总条数是：" + topDocs.totalHits);

		// 获取查询结果集
		ScoreDoc[] docs = topDocs.scoreDocs;

		// 解析结果集
		for (ScoreDoc scoreDoc : docs) {
			// 获取文档id
			int docID = scoreDoc.doc;
			Document doc = searcher.doc(docID);

			System.out.println("======================================");

			System.out.println("docID:" + docID);
			System.out.println("bookId:" + doc.get("id"));
			System.out.println("name:" + doc.get("name"));
			System.out.println("price:" + doc.get("price"));
			System.out.println("pic:" + doc.get("pic"));
		}
		// 3. 释放资源
		reader.close();
	}
}
```

## 2.2 NumericRangeQuery

- 根据数字范围查询.
- 根据数字类型进行查询
- 在企业中，比如电商中，可以根据商品的价格进行查询。

```java
package com.zh.lucene;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.NumericRangeQuery;
import org.junit.Test;

public class IndexManagerTest {
	@Test
	public void testSearchNumericRangeQuery() throws Exception {
		// 创建NumericRangeQuery搜索对象,数字范围查询.
		// 五个参数分别是：域名、最小值、最大值、是否包含最小值，是否包含最大值
		Query query = NumericRangeQuery.newFloatRange("price", 54f, 56f, false, true);
		doSearch(query);
	}
}
```

## 2.3 BooleanQuery

布尔查询，实现组合条件查询。

```java
package com.zh.lucene;

import org.apache.lucene.index.Term;
import org.apache.lucene.search.BooleanClause.Occur;
import org.apache.lucene.search.BooleanQuery;
import org.apache.lucene.search.NumericRangeQuery;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TermQuery;
import org.junit.Test;

public class IndexManagerTest {
	@Test
	public void testSearchBooleanQuery() throws Exception {
		// 创建TermQuery搜索对象
		Query query1 = new TermQuery(new Term("name", "lucene"));
		// 创建NumericRangeQuery搜索对象,数字范围查询.
		// 四个参数分别是：域名、最小值、最大值、是否包含最小值，是否包含最大值
		Query query2 = NumericRangeQuery.newFloatRange("price", 54f, 66f, false, true);

		// 创建BooleanQuery搜索对象,组合查询条件
		BooleanQuery boolQuery = new BooleanQuery();

		// 组合条件,
		// 第一个参数，查询条件，第二个参数，组合方式
		boolQuery.add(query1, Occur.MUST_NOT);
		boolQuery.add(query2, Occur.MUST);

		doSearch(boolQuery);
	}
}
```

组合关系代表的意思如下:

- MUST和MUST表示“与”的关系，即“交集”。

  - MUST ：包含，AND
- MUST和MUST_NOT前者包含后者不包含。

  - MUST_NOT ：不包含，NOT
- MUST_NOT和MUST_NOT没意义 ，单独使用MUST_NOT也是没有意义的。
- SHOULD与MUST表示MUST，SHOULD失去意义；

  - SHOULD ：或，OR
- SHOULD与MUST_NOT相当于MUST与MUST_NOT。
- SHOULD与SHOULD表示“或”的关系，即“并集”。

# 3 通过QueryParser搜索

通过QueryParser也可以创建Query，QueryParser提供一个Parse方法，此方法可以直接根据查询语法来查询。可以通过打印Query对象的方式，查看生成的查询语句。

## 3.1 查询语法

**基础的查询语法，关键词查询**：

> 域名+“:”+搜索的关键字

> 例如：name:java


**范围查询**

> 域名+“:”+[最小值 TO 最大值]

> 例如：size:[1 TO 1000]

> 注意：QueryParser不支持对数字范围的搜索，它支持字符串范围。数字范围搜索建议使用NumericRangeQuery。


**组合条件查询**：

| Occur.MUST 		查询条件必须满足，相当于AND | +（加号） |
| --- | --- |
| Occur.SHOULD 		查询条件可选，相当于OR | 空（不用符号） |
| Occur.MUST_NOT 		查询条件不能满足，相当于NOT非 | -（减号） |


## 3.2 QueryParser

```java
@Test
public void testSearchIndex() throws Exception {
	// 创建分词器
	Analyzer analyzer = new StandardAnalyzer();
	// 1. 创建Query搜索对象
	// 创建搜索解析器，第一个参数：默认Field域，第二个参数：分词器
	QueryParser queryParser = new QueryParser("desc", analyzer);

	// 创建搜索对象
	// Query query = queryParser.parse("desc:java学习");
	Query query = queryParser.parse("desc:java AND lucene");

	// 打印生成的搜索语句
	System.out.println(query);
	// 执行搜索
	doSearch(query);
}
```

## 3.3 MultiFieldQueryParser

- 从多个域中进行查询
- 域与域之间是或的关系

```java
@Test
public void testSearchMultiFieldQueryParser() throws Exception {
	// 创建分词器
	Analyzer analyzer = new IKAnalyzer();
	// 1. 创建MultiFieldQueryParser搜索对象
	String[] fields = { "name", "desc" };
	MultiFieldQueryParser multiFieldQueryParser = new MultiFieldQueryParser(fields, analyzer);
	// 创建搜索对象
	Query query = multiFieldQueryParser.parse("lucene");

	// 打印生成的搜索语句
	System.out.println(query);
	// 执行搜索
	doSearch(query);
}
```

生成的查询语句：`name:lucene desc:lucene`

# 4 TopDocs

Lucene搜索结果可通过TopDocs遍历，TopDocs类提供了少量的属性，如下：

| 方法或属性 | 说明 |
| --- | --- |
| totalHits | 匹配搜索条件的总记录数 |
| scoreDocs | 顶部匹配记录 |


注意：<br />
Search方法需要指定匹配记录数量n：`indexSearcher.search(query, n)`<br />
`TopDocs.totalHits`：是匹配索引库中所有记录的数量<br />
`TopDocs.scoreDocs`：匹配相关度高的前边记录数组，scoreDocs的长度小于等于search方法指定的参数n
