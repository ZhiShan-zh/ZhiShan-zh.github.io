# ElasticSearch自测

# 1 问题

## 1.1 说一下ElasticSearch的使用流程？

[跳转到答案](# 2.1 说一下ElasticSearch的使用流程？)

## 1.2 列举一下ElasticSearch的数据类型？

[跳转到答案](# 2.2 列举一下ElasticSearch的数据类型？)

## 1.3 说明一下ElasticSearch怎么排名？怎么高亮？

[跳转到答案](# 2.3 说明一下ElasticSearch怎么排名？怎么高亮？)

## 1.4 简述一下ElasticSearch怎么实现对文件的检索？

[跳转到答案](# 2.4 简述一下ElasticSearch怎么实现对文件的检索？)

# 2 答案

## 2.1 说一下ElasticSearch的使用流程？

## 2.2 列举一下ElasticSearch的数据类型？

核心数据类型（Core datatypes）：

- 字符型（String datatype）：
    - string（这个是2.x版本的，5.x版本之后是text，并没有string类型了。）
    - 当一个字段是要被全文搜索的，比如Email内容、产品描述，应该使用text类型。设置text类型以后，字段内容会被分析，在生成倒排索引以前，字符串会被分析器分成一个一个词项。text类型的字段不用于排序，很少用于聚合。
    - keyword类型适用于索引结构化的字段，比如email地址、主机名、状态码和标签。如果字段需要进行过滤(比如查找已发布博客中status属性为published的文章)、排序、聚合。keyword类型的字段只能通过精确值搜索到。
- 数字型（Numeric datatypes）：long, integer, short, byte, double, float
- 日期型（Date datatype）：date
    - 日期格式的字符串，比如 “2018-01-13” 或 “2018-01-13 12:10:30”
    - long类型的毫秒数( milliseconds-since-the-epoch，epoch就是指UNIX诞生的UTC时间1970年1月1日0时0分0秒)
    - integer的秒数(seconds-since-the-epoch)
- 布尔型（Boolean datatype）：boolean
    - true和false
- 二进制型（Binary datatype）：binary
    - 进制字段是指用base64来表示索引中存储的二进制数据，可用来存储二进制形式的数据，例如图像。默认情况下，该类型的字段只存储不索引。二进制类型只支持index_name属性。
- 复杂数据类型（Complex datatypes）

数组类型（Array datatype）：数组类型不需要专门指定数组元素的type，例如：

- 字符型数组: [ "one", "two" ]
- 整型数组：[ 1, 2 ]
- 数组型数组：[ 1, [ 2, 3 ]] 等价于[ 1, 2, 3 ]
- 对象数组：[ { "name": "Mary", "age": 12 }, { "name": "John", "age": 10 }]
- elasticSearch不支持元素为多个数据类型：[ 10, “some string” ]

对象类型（Object datatype）： object 用于单个JSON对象；

嵌套类型（Nested datatype）： nested 用于JSON数组；
地理位置类型（Geo datatypes）

地理坐标类型（Geo-point datatype）： geo_point 用于经纬度坐标；
地理形状类型（Geo-Shape datatype）： geo_shape 用于类似于多边形的复杂形状；

特定类型（Specialised datatypes）

- IPv4 类型（IPv4 datatype）： ip 用于IPv4 地址；
- Completion 类型（Completion datatype）： completion 提供自动补全建议；
- Token count 类型（Token count datatype）： token_count 用于统计做了标记的字段的index数目，该值会一直增加，不会因为过滤条件而减少。
- mapper-murmur3类型：通过插件，可以通过 murmur3 来计算 index 的 hash 值；
- 附加类型（Attachment datatype）：采用 mapper-attachments 插件，可支持 attachments 索引，例如 Microsoft Office 格式，Open Document 格式，ePub, HTML 等。

## 2.3 说明一下ElasticSearch怎么排名？怎么高亮？

## 2.4 简述一下ElasticSearch怎么实现对文件的检索？

ElasticSearch只能处理文本，不能直接处理文档。要实现 ElasticSearch 的附件导入需要以下两个步骤：

1. 对多种主流格式的文档进行文本抽取；
2. 将抽取出来的文本内容导入 ElasticSearch。

Ingest-Attachment是一个开箱即用的插件，替代了较早版本的Mapper-Attachment插件，使用它可以实现对（PDF,DOC等）主流格式文件的文本抽取及自动导入。

Elasticsearch5.x 新增一个新的特性 Ingest Node，此功能支持定义命名处理器管道 pipeline，pipeline中可以定义多个处理器，在数据插入 ElasticSearch 之前进行预处理。而 Ingest Attachment Processor Plugin 提供了关键的预处理器 attachment，支持自动对入库文档的指定字段作为文档文件进行文本抽取，并将抽取后得到的文本内容和相关元数据加入原始入库文档。

由于 ElasticSearch 是基于 JSON 格式的文档数据库，所以附件文档在插入 ElasticSearch 之前必须进行 Base64 编码。

具体实现步骤：

1. 建立自己的文本抽取管道pipeline

```shell
curl -X PUT "localhost:9200/_ingest/pipeline/attachment" -d '{
 "description" : "Extract attachment information",
 "processors":[
 {
    "attachment":{
        "field":"data",
        "indexed_chars" : -1,
        "ignore_missing":true
     }
 },
 {
     "remove":{"field":"data"}
 }]}'
```

2. 创建新的索引

    ```shell
    curl -X PUT “localhost:9200/estest” -d’{
    “settings”:{
        “index”:{
        “number_of_shards”:1,
        “number_of_replicas”:0
    }}}’
    ```

3. 载入数据

方法一：直接载入base64源码

首先要确定base64编码正确，否则因为乱码可能无法正确生成attachment。

```shell
curl -X PUT "localhost:9200/pdftest/pdf/1?pipeline=attachment" -d '
{
   "data":"QmFzZTY057yW56CB6K+05piOCuOAgOOAgEJhc2U2NOe8lueggeimgeaxguaKijPkuKo45L2N5a2X6IqC77yIMyo4PTI077yJ6L2s5YyW5Li6NOS4qjbkvY3nmoTlrZfoioLvvIg0KjY9MjTvvInvvIzkuYvlkI7lnKg25L2N55qE5YmN6Z2i6KGl5Lik5LiqMO+8jOW9ouaIkDjkvY3kuIDkuKrlrZfoioLnmoTlvaLlvI/jgIIg5aaC5p6c5Ymp5LiL55qE5a2X56ym5LiN6LazM+S4quWtl+iKgu+8jOWImeeUqDDloavlhYXvvIzovpPlh7rlrZfnrKbkvb/nlKgnPSfvvIzlm6DmraTnvJbnoIHlkI7ovpPlh7rnmoTmlofmnKzmnKvlsL7lj6/og73kvJrlh7rnjrAx5oiWMuS4qic9J+OAggoK44CA44CA5Li65LqG5L+d6K+B5omA6L6T5Ye655qE57yW56CB5L2N5Y+v6K+75a2X56ym77yMQmFzZTY05Yi25a6a5LqG5LiA5Liq57yW56CB6KGo77yM5Lul5L6/6L+b6KGM57uf5LiA6L2s5o2i44CC57yW56CB6KGo55qE5aSn5bCP5Li6Ml42PTY077yM6L+Z5Lmf5pivQmFzZTY05ZCN56ew55qE55Sx5p2l44CC"
}'
```

方法二：载入PDF的同时进行转码导入

首先跳转至指定文件目录

```shell
curl -X PUT "localhost:9200/estest/pdf/10?pipeline=attachment" -d '
{
   "data":" '`base64 -w 0 ABC.pdf | perl -pe's/\n/\\n/g'`' "
}'
```

说明：

- 使用perl脚本的解码功能：'`base64 -w 0 ABC.pdf | perl -pe's/\n/\\n/g'`'