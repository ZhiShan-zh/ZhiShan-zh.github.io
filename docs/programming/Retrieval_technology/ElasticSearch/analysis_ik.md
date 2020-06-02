# IK分词器

# 1 测试分词器

在添加文档时会进行分词，索引中存放的就是一个一个的词（term），当你去搜索时就是拿关键字去匹配词，最终找到词关联的文档。

测试当前索引库使用的分词器，发送POST请求：http://localhost:9200/_analyze，参数为：`{"text":"测试分词器，后边是测试内容：spring cloud实战"}`，返回结果如下：

```json
{
    "tokens": [
        {
            "token": "测",
            "start_offset": 0,
            "end_offset": 1,
            "type": "<IDEOGRAPHIC>",
            "position": 0
        },
        {
            "token": "试",
            "start_offset": 1,
            "end_offset": 2,
            "type": "<IDEOGRAPHIC>",
            "position": 1
        },
        ......
    ]
}
```

因为当前索引库使用的分词器对中文就是单字分词，所以将 “测试” 这个词拆分成两个单字“测”和“试”。

# 2 安装IK分词器

下载IK分词器：（Github地址：https://github.com/medcl/elasticsearch-analysis-ik/releases）

下载zip包并解压此zip包，并将解压的文件拷贝到ElasticSearch安装目录的plugins下的ik目录下，

测试当前索引库使用的分词器，发送POST请求：http://localhost:9200/_analyze，参数为：`{"text":"测试分词器，后边是测试内容：spring cloud实战","analyzer":"ik_max_word" }`，返回结果如下：

```json
{
    "tokens": [
        {
            "token": "测试",
            "start_offset": 0,
            "end_offset": 2,
            "type": "CN_WORD",
            "position": 1
        },
        {
            "token": "分词器",
            "start_offset": 2,
            "end_offset": 5,
            "type": "CN_WORD",
            "position": 2
        },
        ......
    ]
}
```

# 3 两种分词模式

ik分词器有两种分词模式：

- `ik_max_word`：会将文本做最细粒度的拆分，比如会将“中华人民共和国人民大会堂”拆分为“中华人民共和国、中华人民、中华、华人、人民共和国、人民、共和国、大会堂、大会、会堂等词语。
- `ik_smart`：会做最粗粒度的拆分，比如会将“中华人民共和国人民大会堂”拆分为中华人民共和国、人民大会堂。

# 4 自定义词库

如果要让分词器支持一些专有词语，可以自定义词库。

iK分词器自带一个`Elasticsearch/6.2.1/plugins/ik/config/main.dic`的文件，此文件为词库文件。

则自定义词库的步骤为：

1. 新建自定义词库文件`Elasticsearch/6.2.1/plugins/ik/config/my.dic`，注意文件格式为`utf-8`（不要选择`utf-8 BOM`）。
2. 可以根据`main.dic`内容在其中自定义词汇，比如`测试分词器`。
3. 配置文件`Elasticsearch/6.2.1/plugins/ik/config/IKAnalyzer.cfg.xml`中配置`my.dic`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
	<comment>IK Analyzer 扩展配置</comment>
	<!--用户可以在这里配置自己的扩展字典 -->
	<entry key="ext_dict">my.dic</entry>
	 <!--用户可以在这里配置自己的扩展停止词字典-->
	<entry key="ext_stopwords"></entry>
	<!--用户可以在这里配置远程扩展字典 -->
	<!-- <entry key="remote_ext_dict">words_location</entry> -->
	<!--用户可以在这里配置远程扩展停止词字典-->
	<!-- <entry key="remote_ext_stopwords">words_location</entry> -->
</properties>
```

重启ElasticSearch，测试分词效果，发送POST请求：http://localhost:9200/_analyze，参数为：`{"text":"测试分词器，后边是测试内容：spring cloud实战","analyzer":"ik_max_word" }`，返回结果如下：

```json
{
    "tokens": [
        {
            "token": "测试分词器",
            "start_offset": 0,
            "end_offset": 5,
            "type": "CN_WORD",
            "position": 0
        },
        {
            "token": "测试",
            "start_offset": 0,
            "end_offset": 2,
            "type": "CN_WORD",
            "position": 1
        },
        ......
    ]
}
```

