# 在Java中使用ElasticSearch

# 1 索引管理

## 1.1 搭建工程

### 1.1.1 ElasticSearch客户端选择

ES提供多种不同的客户端：

- TransportClient：ES提供的传统客户端，官方计划8.0版本删除此客户端。
- RestClient
  - RestClient是官方推荐使用的，它包括两种：`Java Low Level REST Client`和 `Java High Level REST Client`。
  - ES在6.0之后提供 `Java High Level REST Client`， 两种客户端官方更推荐使用` Java High Level REST Client`，不过当
    前它还处于完善中，有些功能还没有。
  - 这里准备采用 `Java High Level REST Client`，如果它有不支持的功能，则使用`Java Low Level REST Client`。

`Java High Level REST Client`依赖为（maven）：

```xml
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch‐rest‐high‐level‐client</artifactId>
    <version>6.2.1</version>
</dependency>
<dependency>
    <groupId>org.elasticsearch</groupId>
    <artifactId>elasticsearch</artifactId>
    <version>6.2.1</version>
</dependency>
```

### 1.1.2 创建maven工程，并添加依赖

工程名称：service-search

添加依赖：

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring‐boot‐starter‐web</artifactId>
</dependency>
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring‐boot‐starter‐web</artifactId>
</dependency>
<dependency>
	<groupId>org.elasticsearch.client</groupId>
	<artifactId>elasticsearch‐rest‐high‐level‐client</artifactId>
	<version>6.2.1</version>
</dependency>
<dependency>
	<groupId>org.elasticsearch</groupId>
	<artifactId>elasticsearch</artifactId>
	<version>6.2.1</version>
</dependency>
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring‐boot‐starter‐test</artifactId>
	<scope>test</scope>
</dependency>
<dependency>
	<groupId>com.alibaba</groupId>
	<artifactId>fastjson</artifactId>
</dependency>
<dependency>
	<groupId>org.apache.commons</groupId>
	<artifactId>commons‐io</artifactId>
</dependency>
<dependency>
	<groupId>org.apache.commons</groupId>
	<artifactId>commons‐lang3</artifactId>
</dependency>
```

### 1.1.3 配置文件

`application.yml`：

```yaml
server:
	port: ${port:40100}
spring:
	application:
		name: search‐service
index_library:
	elasticsearch:
		hostlist: ${eshostlist:127.0.0.1:9200} #多个结点中间用逗号分隔
```

### 1.1.4 配置类

```java
package com.index_library.search.config;

import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ElasticsearchConfig {
	@Value("${index_library.elasticsearch.hostlist}")
	private String hostlist;
	
	@Bean
	public RestHighLevelClient restHighLevelClient(){
		//解析hostlist配置信息
		String[] split = hostlist.split(",");
		//创建HttpHost数组，其中存放es主机和端口的配置信息
		HttpHost[] httpHostArray = new HttpHost[split.length];
		for(int i=0;i<split.length;i++){
			String item = split[i];
			httpHostArray[i] = new HttpHost(item.split(":")[0], Integer.parseInt(item.split(":")[1]), "http");
		} 
		//创建RestHighLevelClient客户端
		return new RestHighLevelClient(RestClient.builder(httpHostArray));
	} 

	//项目主要使用RestHighLevelClient，对于低级的客户端暂时不用
	@Bean
	public RestClient restClient(){
		//解析hostlist配置信息
		String[] split = hostlist.split(",");
		//创建HttpHost数组，其中存放es主机和端口的配置信息
		HttpHost[] httpHostArray = new HttpHost[split.length];
		for(int i=0;i<split.length;i++){
			String item = split[i];
			httpHostArray[i] = new HttpHost(item.split(":")[0], Integer.parseInt(item.split(":")[1]), "http");
		} 
		return RestClient.builder(httpHostArray).build();
	}
}
```

### 1.1.5 启动类

```java
package com.index_library.search;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@EntityScan("com.index_library.framework.domain.search")//扫描实体类
@ComponentScan(basePackages={"com.index_library.api"})//扫描接口
@ComponentScan(basePackages={"com.index_library.search"})//扫描本项目下的所有类
@ComponentScan(basePackages={"com.index_library.framework"})//扫描common下的所有类
public class SearchApplication {
	public static void main(String[] args) throws Exception {
		SpringApplication.run(SearchApplication.class, args);
	}
}
```

## 1.2 索引管理代码

```java
package com.indexlibrary.search;

import org.elasticsearch.action.DocWriteResponse;
import org.elasticsearch.action.admin.indices.create.CreateIndexRequest;
import org.elasticsearch.action.admin.indices.create.CreateIndexResponse;
import org.elasticsearch.action.admin.indices.delete.DeleteIndexRequest;
import org.elasticsearch.action.admin.indices.delete.DeleteIndexResponse;
import org.elasticsearch.action.delete.DeleteRequest;
import org.elasticsearch.action.delete.DeleteResponse;
import org.elasticsearch.action.get.GetRequest;
import org.elasticsearch.action.get.GetResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.update.UpdateRequest;
import org.elasticsearch.action.update.UpdateResponse;
import org.elasticsearch.client.IndicesClient;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.rest.RestStatus;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Administrator
 * @version 1.0
 **/
@SpringBootTest
@RunWith(SpringRunner.class)
public class TestIndex {

	@Autowired
	RestHighLevelClient client;

	@Autowired
	RestClient restClient;

	// 创建索引库
	@Test
	public void testCreateIndex() throws IOException {
		// 创建索引对象
		CreateIndexRequest createIndexRequest = new CreateIndexRequest("index_library");
		// 设置参数
		createIndexRequest.settings(Settings.builder().put("number_of_shards", "1").put("number_of_replicas", "0"));
		// 指定映射
		createIndexRequest.mapping("doc",
				" {\n" + " \t\"properties\": {\n" + "            \"studymodel\":{\n"
						+ "             \"type\":\"keyword\"\n" + "           },\n" + "            \"name\":{\n"
						+ "             \"type\":\"keyword\"\n" + "           },\n" + "           \"description\": {\n"
						+ "              \"type\": \"text\",\n" + "              \"analyzer\":\"ik_max_word\",\n"
						+ "              \"search_analyzer\":\"ik_smart\"\n" + "           },\n"
						+ "           \"pic\":{\n" + "             \"type\":\"text\",\n"
						+ "             \"index\":false\n" + "           }\n" + " \t}\n" + "}",
				XContentType.JSON);
		// 操作索引的客户端
		IndicesClient indices = client.indices();
		// 执行创建索引库
		CreateIndexResponse createIndexResponse = indices.create(createIndexRequest);
		// 得到响应
		boolean acknowledged = createIndexResponse.isAcknowledged();
		System.out.println(acknowledged);

	}

	// 删除索引库
	@Test
	public void testDeleteIndex() throws IOException {
		// 删除索引对象
		DeleteIndexRequest deleteIndexRequest = new DeleteIndexRequest("index_library");
		// 操作索引的客户端
		IndicesClient indices = client.indices();
		// 执行删除索引
		DeleteIndexResponse delete = indices.delete(deleteIndexRequest);
		// 得到响应
		boolean acknowledged = delete.isAcknowledged();
		System.out.println(acknowledged);

	}

	// 添加文档
	@Test
	public void testAddDoc() throws IOException {
		// 文档内容
		// 准备json数据
		Map<String, Object> jsonMap = new HashMap<>();
		jsonMap.put("name", "spring cloud实战");
		jsonMap.put("description", "本课程主要从四个章节进行讲解： 1.微服务架构入门 2.spring cloud 基础入门 3.实战Spring Boot 4.注册中心eureka。");
		jsonMap.put("studymodel", "201001");
		SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		jsonMap.put("timestamp", dateFormat.format(new Date()));
		jsonMap.put("price", 5.6f);

		// 创建索引创建对象
		IndexRequest indexRequest = new IndexRequest("index_library", "doc");
		// 文档内容
		indexRequest.source(jsonMap);
		// 通过client进行http的请求
		IndexResponse indexResponse = client.index(indexRequest);
		DocWriteResponse.Result result = indexResponse.getResult();
		System.out.println(result);

	}

	// 查询文档
	@Test
	public void testGetDoc() throws IOException {
		// 查询请求对象
		GetRequest getRequest = new GetRequest("index_library", "doc", "tzk2-mUBGsEnDOUe482B");
		GetResponse getResponse = client.get(getRequest);
		// 得到文档的内容
		Map<String, Object> sourceAsMap = getResponse.getSourceAsMap();
		System.out.println(sourceAsMap);
	}

	// 更新文档
	public void updateDoc() throws IOException {
		UpdateRequest updateRequest = new UpdateRequest("index_library", "doc", "4028e581617f945f01617f9dabc40000");
		Map<String, String> map = new HashMap<>();
		map.put("name", "spring cloud实战");
		updateRequest.doc(map);
		UpdateResponse update = client.update(updateRequest);
		RestStatus status = update.status();
		System.out.println(status);
	}

	// 根据id删除文档
	public void testDelDoc() throws IOException {
		// 删除文档id
		String id = "eqP_amQBKsGOdwJ4fHiC";
		// 删除索引请求对象
		DeleteRequest deleteRequest = new DeleteRequest("index_library", "doc", id);
		// 响应对象
		DeleteResponse deleteResponse = client.delete(deleteRequest);
		// 获取响应结果
		DocWriteResponse.Result result = deleteResponse.getResult();
		System.out.println(result);
	}
}
```

# 2 搜索管理

## 2.1 准备环境

### 2.1.1 创建映射

创建index_library索引库。

创建如下映射，POST请求：http://localhost:9200/index_library/doc/_mapping

```json
{
	"properties": {
		"description": {
			"type": "text",
			"analyzer": "ik_max_word",
			"search_analyzer": "ik_smart"
		},
		"name": {
			"type": "text",
			"analyzer": "ik_max_word",
			"search_analyzer": "ik_smart"
		},
		"pic":{
			"type":"text",
			"index":false
		},
		"price": {
			"type": "float"
		},
		"studymodel": {
			"type": "keyword"
		},
		"timestamp": {
			"type": "date",
			"format": "yyyy‐MM‐dd HH:mm:ss||yyyy‐MM‐dd||epoch_millis"
		}
	}
}
```

### 2.1.2 插入原始数据

向`index_library/doc`中插入数据：

POST请求：http://localhost:9200/index_library/doc/1

```json
{ 
	"name": "Bootstrap开发",
	"description": "Bootstrap是由Twitter推出的一个前台页面开发框架，是一个非常流行的开发框架，此框架集成了多种页面效果。此开发框架包含了大量的CSS、JS程序代码，可以帮助开发者（尤其是不擅长页面开发的程序人员）轻松的实现一个不受浏览器限制的精美界面效果。",
	"studymodel": "201002",
	"price":38.6,
	"timestamp":"2018‐04‐25 19:11:35",
	"pic":"group1/M00/00/00/wKhlQFs6RCeAY0pHAAJx5ZjNDEM428.jpg"
}
```

POST请求：http://localhost:9200/index_library/doc/2

```json
{ 
	"name": "java编程基础","description": "java语言是世界第一编程语言，在软件开发领域使用人数最多。",
	"studymodel": "201001",
	"price":68.6,
	"timestamp":"2018‐03‐25 19:11:35",
	"pic":"group1/M00/00/00/wKhlQFs6RCeAY0pHAAJx5ZjNDEM428.jpg"
}
```

POST请求：http://localhost:9200/index_library/doc/3

```json
{ 
	"name": "spring开发基础",
	"description": "spring 在java领域非常流行，java程序员都在用。",
	"studymodel": "201001",
	"price":88.6,
	"timestamp":"2018‐02‐24 19:11:35",
	"pic":"group1/M00/00/00/wKhlQFs6RCeAY0pHAAJx5ZjNDEM428.jpg"
}
```

### 2.1.3 简单搜索

简单搜索就是通过url进行查询，以get方式请求ElasticSearch。
格式：

- `get ../_search?q=.....`
- q：搜索字符串。

例子：

- `?q=name:spring`
- 搜索name中包括spring的文档。

## 2.2 DSL搜索

DSL（Domain Specific Language）是ES提出的基于json的搜索方式，在搜索时传入特定的json格式的数据来完成不同的搜索需求。
DSL比URI搜索方式功能强大，在项目中建议使用DSL方式来完成搜索。

### 2.2.1 API

#### 2.2.1.1 查询所有文档

查询所有索引库的文档，发送post请求：http://localhost:9200/_search

查询指定索引库指定类型下的文档，发送post请求：http://localhost:9200/index_library/doc/_search

```json
{
	"query": {
		"match_all": {}
	},
	"_source" : ["name","studymodel"]
}
```

字段说明：

- `_source`：source源过虑设置，指定结果中所包括的字段有哪些。



结果说明：

- `took`：本次操作花费的时间，单位为毫秒。
- `timed_out`：请求是否超时
- `_shards`：说明本次操作共搜索了哪些分片
-  `hits`：搜索命中的记录
- `hits.total` ： 符合条件的文档总数 hits.hits ：匹配度较高的前N个文档
- `hits.max_score`：文档匹配得分，这里为最高分
- `_score`：每个文档都有一个匹配度得分，按照降序排列。
- `_source`：显示了文档的原始内容。

#### 2.2.1.2 分页查询

POST请求：http://localhost:9200/index_library/doc/_search

携带参数：

```json
{ 
	"from" : 0, "size" : 1,
	"query": {
		"match_all": {}
	},
	"_source" : ["name","studymodel"]
}
```

参数说明：

- form：表示起始文档的下标，从0开始。
- size：查询的文档数量。

#### 2.2.1.3 精确查询Term Query

Term Query为精确查询，在搜索时会整体匹配关键字，不再将关键字分词。

如查询name包括“spring”这个词的文档，POST请求：http://localhost:9200/index_library/doc/_search

携带参数：

```json
{
	"query": {
		"term" : {
			"name": "spring"
		}
	},
	"_source" : ["name","studymodel"]
}
```

#### 2.2.1.4 根据id精确匹配

根据多个id值匹配，POST请求： http://127.0.0.1:9200/index_library/doc/_search

携带参数：

```json
{
	"query": {
		"ids" : {
			"type" : "doc",
			"values" : ["3", "4", "100"]
		}
	}
}
```

#### 2.2.1.5 match Query

##### 2.2.1.5.1 基本使用

match Query即全文检索，它的搜索方式是先将搜索字符串分词，再使用各各词条从索引中搜索。

match Query以此只能匹配一个字段。

match query与Term query区别是match query在搜索前先将搜索关键字分词，再拿各各词语去索引中搜索。

POST请求：http://localhost:9200/index_library/doc/_search

携带参数：

```json
{
	"query": {
		"match" : {
			"description" : {
				"query" : "spring开发",
				"operator" : "or"
			}
		}
	}
}
```

参数说明：

- query：搜索的关键字，对于英文关键字如果有多个单词则中间要用半角逗号分隔，而对于中文关键字中间可以用逗号分隔也可以不用。
- operator：
  - or：表示只要有一个词在文档中出现则就符合条件；
  - and：表示每个词都在文档中出现则才符合条件。

搜索的执行过程是：

1. 将“spring开发”分词，分为spring、开发两个词
2. 再使用spring和开发两个词去匹配索引中搜索。
3. 由于设置了operator为or，只要有一个词匹配成功则就返回该文档。

##### 2.2.1.5.2 minimum_should_match

使用minimum_should_match可以指定文档匹配词的占比。

携带参数：

```json
{
	"query": {
		"match" : {
			"description" : {
				"query" : "spring开发框架",
				"minimum_should_match": "80%"
			}
		}
	}
}
```

“spring开发框架”会被分为三个词：spring、开发、框架；

设置`"minimum_should_match": "80%"`表示，三个词在文档的匹配占比为80%，即3*0.8=2.4，向上取整得2，表示至少有两个词在文档中要匹配成功。

#### 2.2.1.6 multi Query

multiQuery，一次可以匹配多个字段。

##### 2.2.1.6.1 基本使用

单项匹配是在一个field中去匹配，多项匹配是拿关键字去多个Field中匹配。

拿关键字 “spring css”去匹配name 和description字段，POST请求：http://localhost:9200/index_library/doc/_search

```json
{
	"query": {
		"multi_match" : {
			"query" : "spring css",
			"minimum_should_match": "50%",
			"fields": [ "name", "description" ]
		}
	}
}
```

##### 2.2.1.6.2 提升boost

匹配多个字段时可以提升字段的boost（权重）来提高得分。

对name的权重提升，携带参数：

```json
{
	"query": {
		"multi_match" : {
			"query" : "spring框架",
			"minimum_should_match": "50%",
			"fields": [ "name^10", "description" ]
		}
	}
}
```

参数说明：

- “name^10”：表示权重提升10倍，执行上边的查询，发现name中包括spring关键字的文档排在前边。

#### 2.2.1.7 布尔查询

布尔查询对应于Lucene的BooleanQuery查询，实现将多个查询组合起来。

三个参数：

- must：文档必须匹配must所包括的查询条件，相当于 “AND” 
- should：文档应该匹配should所包括的查询条件其中的一个或多个，相当于 "OR" 
- must_not：文档不能匹配must_not所包括的该查询条件，相当于“NOT”

携带参数示例（使用must）：

```json
{
	"_source" : [ "name", "studymodel", "description"],
	"from" : 0, "size" : 1,
	"query": {
		"bool" : {
			"must":[
                {
                    "multi_match" : {
                        "query" : "spring框架",
                        "minimum_should_match": "50%",
                        "fields": [ "name^10", "description" ]
                    } 
                },
                {
                    "term":{
                        "studymodel" : "201001"
                    }
                }
            ]
        }
    }
}
```

#### 2.2.1.8 过虑器

过虑是针对搜索的结果进行过虑，过虑器主要判断的是文档是否匹配，不去计算和判断文档的匹配度得分，所以过
虑器性能比查询要高，且方便缓存，推荐尽量使用过虑器去实现查询或者过虑器和查询共同使用。

过虑器在布尔查询中使用，下边是在搜索结果的基础上进行过虑：

```json
{
	"_source" : [ "name", "studymodel", "description","price"],
	"query": {
		"bool" : {
			"must":[
				{
					"multi_match" : {
						"query" : "spring框架",
						"minimum_should_match": "50%",
						"fields": [ "name^10", "description" ]
					} 
				}
			],
			"filter": [
				{ 
					"term": { "studymodel": "201001" }
				},
				{ 
					"range": { 
						"price": { "gte": 60 ,"lte" : 100}
					}
				}
			]
		}
	}
}
```

参数说明：

- range：范围过虑，保留大于等于60 并且小于等于100的记录。
- term：项匹配过虑，保留studymodel等于"201001"的记录。
- 注意：range和term一次只能对一个Field设置范围过虑。

#### 2.2.1.9 排序

可以在字段上添加一个或多个排序，支持在keyword、date、float等类型上添加，text类型的字段上不允许添加排
序。
比如过虑0--10元价格范围的文档，并且对结果进行排序，先按studymodel降序，再按价格升序，发送POST请求：http://localhost:9200/index_library/doc/_search

携带参数：

```json
{
	"_source" : [ "name", "studymodel", "description","price"],
	"query": {
		"bool" : {
			"filter": [
				{ 
					"range": { 
						"price": { "gte": 0 ,"lte" : 100}
					}
				}
			]
		}
	},
	"sort" : [
		{
			"studymodel" : "desc"
		},
		{
			"price" : "asc"
		}
	]
}
```

#### 2.2.1.10 高亮显示

高亮显示可以将搜索结果一个或多个字突出显示，以便向用户展示匹配关键字的位置。

在搜索语句中添加highlight即可实现。

POST请求：http://127.0.0.1:9200/index_library/doc/_search

携带参数：

```json
{
	"_source" : [ "name", "studymodel", "description","price"],
	"query": {
		"bool" : {
			"must":[
				{
					"multi_match" : {
						"query" : "开发框架",
						"minimum_should_match": "50%",
						"fields": [ "name^10", "description" ],
						"type":"best_fields"
					} 
				}
			],
			"filter": [
				{ 
					"range": { 
						"price": { "gte": 0 ,"lte" : 100}
					}
				}
			]
		}
	},
	"sort" : [
		{
			"price" : "asc"
		}
	],
	"highlight": {
		"pre_tags": ["<tag1>"],
		"post_tags": ["</tag2>"],
		"fields": {
			"name": {},
			"description":{}
		}
	}
}
```

### 2.2.2 Java

```java
package com.indexlibrary.search;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.text.Text;
import org.elasticsearch.index.query.BoolQueryBuilder;
import org.elasticsearch.index.query.MatchQueryBuilder;
import org.elasticsearch.index.query.MultiMatchQueryBuilder;
import org.elasticsearch.index.query.Operator;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.index.query.TermQueryBuilder;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.SearchHits;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.elasticsearch.search.fetch.subphase.highlight.HighlightBuilder;
import org.elasticsearch.search.fetch.subphase.highlight.HighlightField;
import org.elasticsearch.search.sort.FieldSortBuilder;
import org.elasticsearch.search.sort.SortOrder;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@SpringBootTest
@RunWith(SpringRunner.class)
public class TestSearch {
	@Autowired
	RestHighLevelClient client;
	@Autowired
	RestClient restClient;

	// 搜索type下的全部记录
	@Test
	public void testSearchAll() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("doc");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		searchSourceBuilder.query(QueryBuilders.matchAllQuery());
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel" }, new String[] {});
		searchRequest.source(searchSourceBuilder);
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			String name = (String) sourceAsMap.get("name");
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}

	// 分页查询
	@Test
	public void testSearchLimit() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("doc");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		searchSourceBuilder.query(QueryBuilders.matchAllQuery());
		// 分页查询，设置起始下标，从0开始
		searchSourceBuilder.from(0);
		// 每页显示个数
		searchSourceBuilder.size(10);
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel" }, new String[] {});
		searchRequest.source(searchSourceBuilder);
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			String name = (String) sourceAsMap.get("name");
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}

	// Term Query
	@Test
	public void testTermQuery() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("index_library");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		searchSourceBuilder.query(QueryBuilders.termQuery("name", "spring"));
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel" }, new String[] {});
		searchRequest.source(searchSourceBuilder);
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			String name = (String) sourceAsMap.get("name");
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}

	// 根据id精确匹配
	@Test
	public void testSearchById() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("index_library");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();

		String[] split = new String[] { "1", "2" };
		List<String> idList = Arrays.asList(split);
		searchSourceBuilder.query(QueryBuilders.termsQuery("_id", idList));
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel" }, new String[] {});
		searchRequest.source(searchSourceBuilder);
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			String name = (String) sourceAsMap.get("name");
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}

	// 根据关键字搜索
	@Test
	public void testMatchQuery() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("index_library");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel" }, new String[] {});
		// 匹配关键字
		searchSourceBuilder.query(QueryBuilders.matchQuery("description", "spring开发").operator(Operator.OR));
		searchRequest.source(searchSourceBuilder);
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			String name = (String) sourceAsMap.get("name");
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}

	// 根据关键字搜索 minimum_should_match
	@Test
	public void testMinimumShouldMatchQuery() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("index_library");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel" }, new String[] {});

		// 匹配关键字
		MatchQueryBuilder matchQueryBuilder = QueryBuilders.matchQuery("description", "前台页面开发框架 架构")
				.minimumShouldMatch("80%");// 设置匹配占比
		searchSourceBuilder.query(matchQueryBuilder);

		searchRequest.source(searchSourceBuilder);
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			String name = (String) sourceAsMap.get("name");
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}

	// BoolQuery，将搜索关键字分词，拿分词去索引库搜索
	@Test
	public void testBoolQuery() throws IOException {
		// 创建搜索请求对象
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("doc");
		// 创建搜索源配置对象
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		searchSourceBuilder.fetchSource(new String[] { "name", "pic", "studymodel" }, new String[] {});
		// multiQuery
		String keyword = "spring开发框架";
		MultiMatchQueryBuilder multiMatchQueryBuilder = QueryBuilders.multiMatchQuery("spring框架", "name", "description")
				.minimumShouldMatch("50%");
		multiMatchQueryBuilder.field("name", 10);
		// TermQuery
		TermQueryBuilder termQueryBuilder = QueryBuilders.termQuery("studymodel", "201001");
		// 布尔查询
		BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
		boolQueryBuilder.must(multiMatchQueryBuilder);
		boolQueryBuilder.must(termQueryBuilder);
		// 设置布尔查询对象
		searchSourceBuilder.query(boolQueryBuilder);
		searchRequest.source(searchSourceBuilder);// 设置搜索源配置
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			System.out.println(sourceAsMap);
		}
	}

	// 布尔查询使用过虑器
	@Test
	public void testFilter() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("doc");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel", "price", "description" }, new String[] {});
		searchRequest.source(searchSourceBuilder);
		// 匹配关键字
		MultiMatchQueryBuilder multiMatchQueryBuilder = QueryBuilders.multiMatchQuery("spring框架", "name",
				"description");
		// 设置匹配占比
		multiMatchQueryBuilder.minimumShouldMatch("50%");
		// 提升另个字段的Boost值
		multiMatchQueryBuilder.field("name", 10);
		searchSourceBuilder.query(multiMatchQueryBuilder);
		// 布尔查询
		BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
		boolQueryBuilder.must(searchSourceBuilder.query());
		// 过虑
		boolQueryBuilder.filter(QueryBuilders.termQuery("studymodel", "201001"));
		boolQueryBuilder.filter(QueryBuilders.rangeQuery("price").gte(60).lte(100));
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			String name = (String) sourceAsMap.get("name");
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}

	// 排序
	@Test
	public void testSort() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("doc");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel", "price", "description" }, new String[] {});
		searchRequest.source(searchSourceBuilder);
		// 布尔查询
		BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
		// 过虑
		boolQueryBuilder.filter(QueryBuilders.rangeQuery("price").gte(0).lte(100));
		// 排序
		searchSourceBuilder.sort(new FieldSortBuilder("studymodel").order(SortOrder.DESC));
		searchSourceBuilder.sort(new FieldSortBuilder("price").order(SortOrder.ASC));
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			String name = (String) sourceAsMap.get("name");
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}

    // 高亮显示
	@Test
	public void testHighlight() throws IOException {
		SearchRequest searchRequest = new SearchRequest("index_library");
		searchRequest.types("doc");
		SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
		// source源字段过虑
		searchSourceBuilder.fetchSource(new String[] { "name", "studymodel", "price", "description" }, new String[] {});
		searchRequest.source(searchSourceBuilder);
		// 匹配关键字
		MultiMatchQueryBuilder multiMatchQueryBuilder = QueryBuilders.multiMatchQuery("开发", "name", "description");
		searchSourceBuilder.query(multiMatchQueryBuilder);
		// 布尔查询
		BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
		boolQueryBuilder.must(searchSourceBuilder.query());
		// 过虑
		boolQueryBuilder.filter(QueryBuilders.rangeQuery("price").gte(0).lte(100));
		// 排序
		searchSourceBuilder.sort(new FieldSortBuilder("studymodel").order(SortOrder.DESC));
		searchSourceBuilder.sort(new FieldSortBuilder("price").order(SortOrder.ASC));
		// 高亮设置
		HighlightBuilder highlightBuilder = new HighlightBuilder();
		highlightBuilder.preTags("<tag>");// 设置前缀
		highlightBuilder.postTags("</tag>");// 设置后缀
		// 设置高亮字段
		highlightBuilder.fields().add(new HighlightBuilder.Field("name"));
		// highlightBuilder.fields().add(new HighlightBuilder.Field("description"));
		searchSourceBuilder.highlighter(highlightBuilder);
		SearchResponse searchResponse = client.search(searchRequest);
		SearchHits hits = searchResponse.getHits();
		SearchHit[] searchHits = hits.getHits();
		for (SearchHit hit : searchHits) {
			Map<String, Object> sourceAsMap = hit.getSourceAsMap();
			// 名称
			String name = (String) sourceAsMap.get("name");
			// 取出高亮字段内容
			Map<String, HighlightField> highlightFields = hit.getHighlightFields();
			if (highlightFields != null) {
				HighlightField nameField = highlightFields.get("name");
				if (nameField != null) {
					Text[] fragments = nameField.getFragments();
					StringBuffer stringBuffer = new StringBuffer();
					for (Text str : fragments) {
						stringBuffer.append(str.string());
					}
					name = stringBuffer.toString();
				}
			}
			String index = hit.getIndex();
			String type = hit.getType();
			String id = hit.getId();
			float score = hit.getScore();
			String sourceAsString = hit.getSourceAsString();
			String studymodel = (String) sourceAsMap.get("studymodel");
			String description = (String) sourceAsMap.get("description");
			System.out.println(name);
			System.out.println(studymodel);
			System.out.println(description);
		}
	}
}
```

