# 映射

# 1 映射维护方法

**查询所有索引的映射**，GET请求：http://localhost:9200/_mapping

**创建映射**，POST请求：http://localhost:9200/Index_library/doc/_mapping

参数：

```json
{
    "properties": {
        "name": {
        	"type": "text"
        },
        "description": {
             "type": "text"
        },
        "studymodel": {
        	"type": "keyword"
        }
    }
}
```

**更新映射**：映射创建成功可以添加新字段，已有字段不允许更新。

**删除映射**：通过删除索引来删除映射。

# 2 常用映射类型

Field datatypes：https://www.elastic.co/guide/en/elasticsearch/reference/7.7/mapping-types.html

字符串包括text和keyword两种类型。

## 2.1 text文本字段

### 2.1.1 analyzer

通过analyzer属性指定分词器。

下边指定name的字段类型为text，使用ik分词器的`ik_max_word`分词模式。

```json
"name": {
    "type": "text",
    "analyzer":"ik_max_word"
}
```

上边指定了analyzer是指在索引和搜索都使用`ik_max_word`，如果单独想定义搜索时使用的分词器则可以通过`search_analyzer`属性来指定。

对于ik分词器建议是索引时使用`ik_max_word`将搜索内容进行细粒度分词，搜索时使用`ik_smart`提高搜索精确性。

```json
"name": {
    "type": "text",
    "analyzer":"ik_max_word",
    "search_analyzer":"ik_smart"
}
```

### 2.1.2 index

通过index属性指定是否索引。

默认为`index=true`，即要进行索引，只有进行索引才可以从索引库搜索到。

但是也有一些内容不需要索引，比如：商品图片地址只被用来展示图片，不进行搜索图片，此时可以将index设置为false。

删除索引，重新创建映射，将pic的index设置为false，尝试根据pic去搜索，结果搜索不到数据

```json
"pic": {
    "type": "text",
    "index":false
}
```

### 2.1.3 store

是否在source之外存储，每个文档索引后会在ElasticSearch中保存一份原始文档，存放在"_source"中，一般情况下不需要设置store为true，因为在_source中已经有一份原始文档了。

### 2.1.4 测试

创建新映射，POST请求：http://localhost:9200/Index_library/doc/_mapping

```json
{
    "properties": {
        "name": {
            "type": "text",
            "analyzer":"ik_max_word",
            "search_analyzer":"ik_smart"
        },
        "description": {
            "type": "text",
            "analyzer":"ik_max_word",
            "search_analyzer":"ik_smart"
        },
        "pic":{
            "type":"text",
            "index":false
        },
        "studymodel":{
            "type":"text"
        }
    }
}
```

插入文档：POST请求：http://localhost:9200/Index_library/doc/4028e58161bcf7f40161bcf8b77c0000

```json
{
    "name":"Bootstrap开发框架",
    "description":"Bootstrap是由Twitter推出的一个前台页面开发框架，在行业之中使用较为广泛。此开发框架包含了大量的CSS、JS程序代码，可以帮助开发者（尤其是不擅长页面开发的程序人员）轻松的实现一个不受浏览器限制的精美界面效果。",
    "pic":"group1/M00/00/01/wKhlQFqO4MmAOP53AAAcwDwm6SU490.jpg",
    "studymodel":"201002"
}
```

查询测试：

Get http://localhost:9200/Index_library/_search?q=name:开发
Get http://localhost:9200/Index_library/_search?q=description:开发
Get http://localhost:9200/Index_library/_search?q=pic:group1/M00/00/01/wKhlQFqO4MmAOP53AAAcwDwm6SU490.jpg
Get http://localhost:9200/Index_library/_search?q=studymodel:201002

通过测试发现：name和description都支持全文检索，pic不可作为查询条件。

## 2.2  keyword关键字字段

keyword字段为关键字字段，通常搜索keyword是按照整体搜索，所以创建keyword字段的索引时是不进行分词的，比如：邮政编码、手机号码、身份证等。

keyword字段通常用于过虑、排序、聚合等。

### 2.2.1 测试

更改映射：

```json
{
    "properties": {
        "studymodel":{
        	"type":"keyword"
        },
        "name":{
        	"type":"keyword"
        }
    }
}
```

插入文档：

```json
{
    "name": "java编程基础",
    "description": "java语言是世界第一编程语言，在软件开发领域使用人数最多。",
    "pic":"group1/M00/00/01/wKhlQFqO4MmAOP53AAAcwDwm6SU490.jpg",
    "studymodel": "201001"
}
```

根据studymodel查询文档
搜索：http://localhost:9200/Index_library/_search?q=name:java
name是keyword类型，所以查询方式是精确查询。

## 2.3 date日期类型

日期类型不用设置分词器。

通常日期类型的字段用于排序。

format：通过format设置日期格式

例如：

下边的设置允许date字段存储年月日时分秒、年月日及毫秒三种格式。

```json
{
    "properties": {
            "timestamp": {
            "type": "date",
            "format": "yyyy‐MM‐dd HH:mm:ss||yyyy‐MM‐dd"
        }
    }
}
```

插入文档，POST请求 :http://localhost:9200/Index_library/doc/3

```json
{ 
    "name": "spring开发基础",
    "description": "spring 在java领域非常流行，java程序员都在用。",
    "studymodel": "201001",
    "pic":"group1/M00/00/01/wKhlQFqO4MmAOP53AAAcwDwm6SU490.jpg",
    "timestamp":"2018‐07‐04 18:28:58"
}
```

## 2.4 数值类型

- 尽量选择范围小的类型，提高搜索效率

- 对于浮点数尽量用比例因子，因为整型比浮点型更易压缩，节省磁盘空间。

  - 比如一个价格字段，单位为元，我们将比例因子设置为100，这在ElasticSearch中会按分存储，映射如下：

  - ```json
    "price": {
        "type": "scaled_float",
        "scaling_factor": 100
    },
    ```

  - 由于比例因子为100，如果我们输入的价格是23.45则ElasticSearch中会将23.45乘以100存储在ES中。

  - 如果输入的价格是23.456，ES会将23.456乘以100再取一个接近原始值的数，得出2346。

更新已有映射，并插入文档：http://localhost:9200/Index_library/doc/3

```json
{ 
    "name": "spring开发基础",
    "description": "spring 在java领域非常流行，java程序员都在用。",
    "studymodel": "201001",
    "pic":"group1/M00/00/01/wKhlQFqO4MmAOP53AAAcwDwm6SU490.jpg",
    "timestamp":"2018‐07‐04 18:28:58",
    "price":38.6
}
```

## 2.5 综合例子

创建如下映射，POST请求：http://localhost:9200/Index_library/doc/_mapping

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

插入文档，POST请求: http://localhost:9200/Index_library/doc/1 

```json
{ 
    "name": "Bootstrap开发", "description": "Bootstrap是由Twitter推出的一个前台页面开发框架，是一个非常流行的开发框架，此框架集成了多种页面效果。此开发框架包含了大量的CSS、JS程序代码，可以帮助开发者（尤其是不擅长页面开发的程序人员）轻松的实现一个不受浏览器限制的精美界面效果。", 
    "studymodel": "201002", 
    "price":38.6, 
    "timestamp":"2018-04-25 19:11:35",
	"pic":"group1/M00/00/00/wKhlQFs6RCeAY0pHAA Jx5ZjNDEM428.jpg" 
}
```