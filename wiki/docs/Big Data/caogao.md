---
title: 草稿
date: 2017-12-30
hidden: true
---


### 1ElasticSearch入门介绍

#### 常见术语：

        A、Document        文档

                用户存储在ES中的数据文档。

        B、Index                索引

                由具有相同字段的文档列表组成。在当前版本，不在推荐下设Type，在后续版本，不再设立Type。

        C、field                  字段

                包含具体数据。

        D、Node                节点

                一个ES的实例，构成clister的单元

        E、Cluster              集群  

                对外服务的一个/多个节点

#### Document介绍：

        A、常用数据类型：字符串、数值型、布尔型、日期型、二进制、范围类型

        B、每个文档都有一个唯一ID标识。（可以自行指定，也可由ES自动生成）

        C、元数据，用于标注文档的相关信息：

            a、_index:            文档所在的索引名

            b、_type：           文档所在的类型名

            c、_id：                文档唯一标识

            d、_uid：              组合id、由_type和_id组成，后续版本中_type不再有用，同_id

            e、_source：        文档的原始JSON数据，可从这获取每个字段的内容

            f、_all：                 整合所有字段内容到该字段。（默认禁用）

            g、_version：       文档字段版本号，标识被操作了几次

#### Index介绍：

        A、索引中存储相同结构的文档，且每个index都有自己的Mapping定义，用于定义字段名和类型；

        B、一个集群中可以有多个inex，类似于可以有多个table。

#### RESTful API：

        A、有两种交互方式：

          a、CURL命令行——————curl -XPUT xxx

          b、Kibana DevTools————PUT xxx{ }

        B、本次学习使用DevTools方式进行开发。

#### Index API：

        用户创建、删除、获取索引配置等。

        A、创建索引：

```
PUT /test_index #创建一个名为test_index的索引
```
        B、查看索引：

```
GET _cat/indices #查看所有的索引
```
        C、删除索引：

```
DELETE /test_index #删除名为test_index的索引
```
#### Document API：

        A、创建文档：

          a、指定ID创建Document

```
#创建ID为1的文档
PUT /test_index/doc/1
{
 "username":"alfred",
 "age":"24"
}
```
          返回结果：



          b、不指定ID创建Document

```
POST /test_index/doc
{
 "username":"buzhiding",
 "age":"1"
}
```
返回结果：



          可以看到，ES自动指定了id，为rZDAU2cBYarvGujXMyXg。

        B、查询文档：

```
#查看名为test_index的索引中id为1的文档
GET /test_index/doc/1
```
        C、查询所有文档：

```
#查询名为test_index的索引中所有文档,用到endpoint：_search，默认返回符合的前10条
GET /test_index/doc/_search
{
 "query":{
  "term":{
   "_id":"1"
  }
 }
}
#term和match的区别：term完全匹配，不进行分词器分析；match模糊匹配，进行分词器分析，包含即返回
```
        D、批量创建文档：

        ES运行一次创建多个文档，从而减少网络传输开销，提升写入速率。

```
#批量创建文档，用到endpoint：_bulk
POST _bulk
{"index":{"_index":"test_index","_type":"doc","_id":"3"}}
{"username":"alfred","age":"20"}
{"delete":{"_index":"test_index","_type":"doc","_id":"1"}}
{"update":{"_id":"2","_index":"test_index","_type":"doc"}}
{"doc":{"age":"30"}}
#index和create的区别，如果文档存在时，使用create会报错，而index会覆盖
```
        E、批量查询文档：

```
#批量查询文档，使用endpoint:_mget
GET _mget
{
 "doc":[
  {
   "_index":"test_index",
   "_type":"doc",
   "_id":"1"
  },
  {
   "_index":"test_index",
   "_type":"doc",
   "_id":"2"
  }
 ]
}
```
F、根据搜索内容删除文档：

```
#根据搜索内容删除文档,使用endpoint:_delete_by_query
POST /test_index/doc/_delete_by_query
{
 "query":{
  "match":{
   "username":"buzhiding"
  }
 }
}
#删除名为test_index的索引中的username为不指定的文档
```
G、删除整个Type：

```
#直接删除整个type,依然使用endpoint:_delete_by_query
POST /test_index/doc/_delete_by_query
{
 "query":{
  "match_all":{}
 }
}
#会直接删除名为test_index的索引下的所有type
```


### 2 ElasticSearch倒排索引与分词

#### 倒排索引概念

1）百度百科：倒排索引源于实际应用中需要根据属性的值来查找记录。这种索引表中的每一项都包括一个属性值和具有该属性值的各记录的地址。由于不是由记录来确定属性值，而是由属性值来确定记录的位置，因而称为倒排索引(inverted index)。带有倒排索引的文件我们称为倒排索引文件，简称倒排文件(inverted file)。

2）以书举例：

目录页   ===>   正排索引

索引页   ===>   倒排索引

3）正排索引和倒排索引：

 A、正排索引：文档ID到文档内容、单词的关联关系

| 文档ID	| 文档内容 |
| --- | --- |
| 1	 | elasticsearch是最流行的搜索引擎 |
| 2	 | php是世界上最好的语言 |
| 3	 | 搜索引擎是如何产生的 |
    
B、倒排索引：单词到文档ID的关联关系

| 单词	文档 | ID列表 |
| --- | --- |
| elasticsearch | 	1 |
| 流行	 | 1 |
| 搜索引擎 | 1，3 |
|  php	 | 2 |
| 世界	 | 2 |
| 最好 | 	2 |
|  语言	 | 2 |
| 如何	 | 3 |
|  诞生	 | 3 |

C、查询包含“搜索引擎”的文档流程：

    a. 通过倒排索引，获得对应的文档ID：1，3；
    b. 通过文档ID，查询完整内容；
    c. 返回最终结果。

#### 倒排索引详解

1）组成：

    A. 单词词典（Term Dictionary）
    B. 倒排列表（Posting List）

2）单词词典：

    记录所有文档的单词，一般都比较大，记录了单词到倒排列表的关联信息，一般使用B + Tree实现。构造方法见如下网址：https://www.cs.usfca.edu/~galles/visualization/BPlusTree.html。

3）倒排列表：

    记录单词对应的文档集合，由倒排索引项Posting List组成。

A、倒排索引项主要包含：

    a. 文档ID。用于获取原始信息。
    b. 词频TF。记录该单词在该文档中的出现次数，用于计算相关性得分。
    c. 位置Position。记录单词在文档中的分词位置(多个)，用于词语搜索。
    d. 偏移Offset。记录单词在文档的开始和结束位置，用于高亮显示。

B、如上的数据中，“搜索引擎”的Posting List为：

    DocID	TF	Position	Offset
    1	1	2	<18,22>
    3	1	0	<0,4>

#### 分词介绍

分词指：将文本转换成一系列单词Term/Token的过程，也可称作文本分析，ES中叫作：Analysis。

分词器(Analyzer)： ES中专门处理分词的组件，组成和执行顺序如下：

    * Character Filters(多个)。针对原始文本进行处理，如：去除html特使标记符</p>等。
    * Tokenizer(一个)。将原始文本按一定规则划分为单词。
    * Token Filters(多个)。针对Tokenizer处理的单词进行再加工，如：转小写、删除、新增等。

#### 分词API

ES提供了一个测试分词的API接口，使用endpoint：_analyze。并且：可以指定分词器进行测试，还可以直接指定索引中的字段，甚至自定义分词器进行测试。

1）指定分词器：

```json
#指定分词器进行分词测试
POST _analyze
{
 "analyzer":"standard",
 "text":"hello world!"
}
```

返回结果：



      可以看到：a、分词结果；b、起始偏移；c、结束偏移；d、分词位置。

        2）直接指定索引中字段：

```json
#直接指定索引中字段
POST test_index/_analyze
{
 "field":"username",
 "text":"hello world!"
}
```
      使用username字段的分词方式对text进行分词。

        3）自定义分词器：

```json
#自定义分词器，自定义Tokenizer、filter、等进行分词，举例：
POST _analyze
{
 "tokenizer":"standard",
 "filter":["lowercase"],
 "text":"Hello World!"
}
```
返回结果：


可以看到：a、分词结果(已经变为小写)；b、起始偏移；c、结束偏移；d、分词位置。

#### ES自带分词器

1. standard(默认分词器)            按词划分、支持多语言、小写处理。
2. simple                                      按非字母划分、小写处理。
3. whitespace                             按空格划分。
4. stop                                         按非字母划分、小写处理、按StopWord（语气助词：the、an、的、这等）处理。
5. keyword                                  不分词，作为一个单词输出。
6. pattern                                    通过正则表达式自定义分隔符，默认\w+，即：非字词的符号作为分隔符。
7. Language                                 另外还有30+常见语言的分词器（如：arabic、armenian、basque等）
      
#### 中文分词器

中文分词的难点在于：汉语中的分词没有一个形式上的分隔符，上下文不同，分词的结果也就不同，比如交叉歧义问题就会导致这样一个笑话：“南京市长江大桥欢迎你”，到底是“南京市长/江大桥/欢迎你”，还是“南京市/长江大桥/欢迎你”？

 目前，常用的中文分词器有：
 
 常用分词系统

    * IK。实现中英文分词，支持多模式，可自定义词库，支持热更新分词词典。
    * jieba。python中流行，支持繁体分词、并行分词，可自定义词典、词性标记等。

基于自然语言的分词系统
    
    * Hanlp: https://github.com/hankcs/HanLP
    * THULAC，https://github.com/microbun/elasticsearch-thulac-plugin

#### 自定义分词

通过自定义：Character Filters、Tokenizer、Token Filter实现。格式：

```json
PUT index名
{
  "setting":{
    "analysis":{
      "char_filter":{},
      "tokenizer":{},
      "filter":{},
      "analyzer":{}     
    }
  }
}
```
举例：


```json
#自定义分词
POST test_index
{
 "settings":{
  "analysis":{
   "analyzer":{
    "my_custom_analyzer":{
     "type":"custom",
     "tokenzier":"standartd",
     "char_filter":"[
      "html_strip"
     ],
     "filter":[
      "lowercase",
      "asciifolding"
]}} } }}
```