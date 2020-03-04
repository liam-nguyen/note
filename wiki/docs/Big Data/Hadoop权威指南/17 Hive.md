---
title: 17 Hive
toc: false
date: 2017-10-30
---

> The [Apache Hive ™](http://hive.apache.org/) data warehouse software facilitates reading, writing, and managing large datasets residing in distributed storage using SQL. Structure can be projected onto data already in storage. A command line tool and JDBC driver are provided to connect users to Hive. 

Hive是一个构建在Hadoop上的*数据仓库*(data warehouse)框架，其设计目的是让精通SQL技能但Java编程相对较弱的分析师能够对存放在HDFS中的大规模数据集进行查询。

!!! note "Data WareHouse v.s. Database"

    | Parameter  | Database  | Data Warehouse  | 
    | --- | --- | --- |
    | Parameter  | Database  | Data Warehouse  | 
    | Purpose  | Is designed to *record*  | Is designed to *analyze*  | 
    | Processing Method  | The database uses the Online *Transactional* Processing (OLTP, 联机事务处理)  | Data warehouse uses Online *Analytical* Processing (OLAP, 联机分析处理).  | 
    | Tables and Joins  | Tables and joins of a database are *complex* as they are normalized.  | Table and joins are *simple* in a data warehouse because they are denormalized.  | 
    | Orientation  | Is an *application*-oriented collection of data  | It is a *subject*-oriented collection of data  | 
    | Storage limit  | Generally limited to a single application  | Stores data from any number of applications  | 
    | Availability  | Data is available real-time  | Data is refreshed from source systems as and when needed  | 
    | Data Type  | Data stored in the Database is up to date.  | Current and *Historical* Data is stored in Data Warehouse. May not be up to date.  | 
    | Query Type  | Simple transaction queries are used.  | Complex queries are used for analysis purpose.  | 


### 2 与传统数据库相比

#### 读时模式v.s写时模式


传统数据库是在写入时对照模式(schema)进行检查，称之为**写时模式**(schema on write)。Hive只在查询时对数据进行验证，称之为**读时模式**(schema on read)。


#### 更新、事务和索引

更新、事务和索引是传统数据库最重要的特性。而Hive是不支持这些特性的。对于Hive，全表扫描(full-table scan)是常态操作，表更新则是通过把数据变换后放入新表实现的。

### 2 运行Hive

#### 执行引擎
Hive的默认执行引擎是MapReduce。它还支持Apache Tez和Spark执行引擎，可以由属性`hive.execution.engin`来控制。

#### Hive服务

Hive服务包括：

* cli：命令行界面，默认的服务，使用`hive`命令启动
* hiveserver: 以提供Thrift服务的服务器形式运行，使用`hive --service hiveserver2`命令启动
* hwi：hive的web接口(默认端口9999)，使用`hive –-service hwi`命令启动


![](figures/hive_architecture.jpg)

如果以hive server的方式运行hive服务，则可以通过以下方式进行客户端连接：

```bash
# mini1是hiverserver2所启动的那台主机名，端口默认是10000
> beeline -u jdbc:hive2://mini1:10000 -n hadoop
```


#### MetaStore

metastore包含metastore服务和后台数据，有以下三种运行方式：

* **内嵌metastore**(embedded metastore): 默认情况下，metastore服务和Hive服务运行在同一个JVM中，包含一个内嵌的以本地磁盘作为存储的Derby数据库实例。由于仅有一个Derby数据库，所以仅支持一个hive会话。
* **本地metastore**(local metastore): metastore服务仍然和Hive服务运行在同一个JVM中，但是连接的却是在另一个进程中的数据库(可以在本机或远程机器上)。支持多个hive会话。任何JDBC兼容的数据库都可以供metastore使用，最流行的是MySQL数据库。
* **远程metastore**(remote metastore): metastore服务和Hive服务运行在不同JVM中。


![](figures/metascore_configurations.jpg)

#### 架构

![](figures/hive_architecture_Ok.jpg)


### 5 HiveQL

Hive的SQL方言称为HiveQL。


#### 数据类型

Hive支持基本和复杂数据类型。基本数据类型(primitive data type)基本对应于Java中的类型，包括：

* 数值型：TINYINT, SMALLINT, INT, BIGINT, FLOAT, DOUBLE, DECIMAL
* 布尔型：BOOLEAN
* 字符串类型：STRING(无上限可变长度字符串), VARCHAR(可变长度字符串), CHAR(固定长度字符串)
* 时间戳类型：TIMESTAMP(时间戳)，DATE(日期)

复杂数据类型(complex data type)包括：

* 数组：ARRAY
* 映射： MAP
* 结构：STRUCT, UNION

#### 操作符与函数

Hive提供的操作符基本与MySQL匹配：

* 关系操作符： 等值判断： x='a', 空值判断： x is null, 模式匹配: x like 'a%'
* 算术操作符： +, -
* 逻辑操作符: or, and 


### 6 表

Hive的表在逻辑上由存储的数据和描述表中数据形式的相关元数据组成。

* 数据可以存放在任何Hadoop文件系统中，包括HDFS、本地文件系统等；
* 元数据存放在关系型数据库中，例如Derby, MySql中。


#### 托管表和外部表

加载数据到**托管表**(managed table)时，Hive会把原始数据移到仓库目录(warehouse directory)；表被丢弃后，其元数据和数据都会被删除。

```sql
create table managed_table (dummy string);
load data inpath '/user/tom/data.txt' into table managed_table;
```

对于**外部表**(external table)，Hive不会把数据移到仓库目录；并且表被丢弃后，Hive只会删除其元数据。

普遍的做法是把存放在HDFS的初始数据集用作外部表使用，然后用Hive的变换功能把数据移动到托管表。


#### 分区和桶

Hive把表组织成**分区**(partition)，可以加快数据分片(slice)的查询速度。表或分区进一步分为**桶**(bucket)，为数据提供额外的结构以获得更高效的查询处理。

![](figures/hive_partitions_buckets.jpg)

分区是在创建表时用`PARTITION BY`子句定义的。`PARTITION BY`子句中的列定义是表中正式的列，称为**分区列**(partition column)，但是*数据文件并不包含这些列的值*，因为它们源自目录名。把数据加载到分区表时，需要显式指定分区值。


!!! example "日志文件"

    例如每条记录包含一个时间戳的日志文件，可以根据日期来进行分区；除此之外，还可以进一步根据国家对每个分区进行**子分区**(subpartition)。对于特定日期的查询，只需要扫描范围内的分区中的文件即可。
    
    ```sql
    create table logs(ts bigint, line string)
    partitioned by (dt string, country string)
    
    LOAD DATA LOCAL INPATH 'input/hive/partitions/file1' 
    INTO TABLE logs PARTITION (dt='2001-01-01', country='GB');
    ```
    
    ![hive_partitions_examples](figures/hive_partitions_examples.png)
    
    使用`show partitions`命令展示分区：
    
    ```sql
    hive> show partitions logs;
    OK
    dt=2001-01-01/country=GB
    dt=2001-01-01/country=US
    dt=2001-01-02/country=GB
    dt=2001-01-02/country=US
    ```
    
    分区列是表中正式的列，但是并不包含在数据中：
    
    ```sql
    hive> select * from logs;
    OK
    1	Log line 1	2001-01-01	GB
    2	Log line 2	2001-01-01	GB
    3	Log line 3	2001-01-01	US
    4	Log line 4	2001-01-02	GB
    5	Log line 5	2001-01-02	US
    6	Log line 6	2001-01-02	US
    ```

把表或分区组织成**桶**(bucket)有两个理由：

* 获得更高的查询处理效率。桶为表加上了额外的结构，Hive在处理有些查询时能利用这个结构。具体而言，连接两个在（包含连接列的）相同列上划分了桶的表，可以使用Map端连接(Map-side join)高效的实现。比如JOIN操作。对于JOIN操作两个表有一个相同的列，如果对这两个表都进行了桶操作。那么将保存相同列值的桶进行JOIN操作就可以，可以大大较少JOIN的数据量。
* 使取样（sampling）更高效。在处理大规模数据集时，在开发和修改查询的阶段，如果能在数据集的一小部分数据上试运行查询，会带来很多方便。

使用`CLUSTERED BY`子句来指定划分桶所用的列和要划分的桶的个数：

```sql
create table bucketed_users (id int, name string)
clustered by (id) into 4 buckets;
```


!!! example "student"

    ![](figures/hive_buckets_example.jpg)

#### 存储格式

Hive使用的默认存储格式是分隔的文本，每行存储一个数据行。默认的行内分隔符是`CONTROL-A`。集合类的分隔符是`CONTROL-B`，用于分隔ARRAY或STRUCT或MAP的键值对中的元素。表中各行之间用换行符分隔。

等价于：

```hiveql
create table ...
row format delimited
    fields terminated by '\001'
    collection items terminated by '\002'
    map keys terminated by '\003'
    lines terminated by '\n'
stored as textfile;
```
#### 导入数据

Load DATA操作把文件复制或移动到表的目录中：

```sql
LOAD DATA [LOCAL] INPATH 'filepath' [OVERWRITE] INTO
TABLE tablename [PARTITION (partcol1=val1, partcol2=val2 ...)]
```

* filepath: 支持绝对路径和相对路径
* local关键字：如果使用了local关键字，则去本地文件系统中寻找；否则默认去HDFS中查找
* overwrite：如果使用了overwrite关键字，则目标表或者分区中的内容会被删除，然后将filepath指向的文件/目录中的内容添加到表/分区中

INSERT语句把数据从一个Hive表填充到另一个：

```sql
INSERT OVERWRITE TABLE tablename1 [PARTITION (partcol1=val1, partcol2=val2 ...)] 
select_statement1 FROM from_statement
```


#### 创建表

```sql
CREATE [EXTERNAL] TABLE [IF NOT EXISTS] table_name
    [(col_name data_type [COMMENT col_comment], ...)]
    [COMMENT table_comment]
    [PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)]
    [CLUSTERED BY (col_name, col_name, ...)
    [SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS]
    [ROW FORMAT row_format]
    [STORED AS file_format]
    [LOCATION hdfs_path]
```

1. `CREATE TABLE` 创建一个指定名字的表。如果相同名字的表已经存在，则抛出异常；用户可以用`IF NOT EXISTS`选项来忽略这个异常。
2. `EXTERNAL`关键字可以让用户创建一个外部表
3. `LIKE`允许用户复制现有的表结构，但是不复制数据。
4. `ROW FORMAT DELIMITED [FIELDS TERMINATED BY char] [COLLECTION ITEMS TERMINATED BY char] [MAP KEYS TERMINATED BY char] [LINES TERMINATED BY char] | SERDE serde_name [WITH SERDEPROPERTIES (property_name=property_value, property_name=property_value, ...)]` 
   
       * 用户在建表的时候可以自定义 SerDe 或者使用自带的 SerDe。
       * 如果没有指定`ROW FORMAT`或者`ROW FORMAT DELIMITED`，将会使用自带的 SerDe。在建表的时候，用户还需要为表指定列，用户在指定表的列的同时也会指定自定义的SerDe，Hive通过 SerDe 确定表的具体的列的数据。
       
5. `STORED AS SEQUENCEFILE|TEXTFILE|RCFILE`如果文件数据是纯文本，可以使用`STORED AS TEXTFILE`。如果数据需要压缩，使用 `STORED AS SEQUENCEFILE`。
6. `PARTITIONED BY` 分区
7. `CLUSTERED BY`桶





### 7 查询数据
#### 排序和聚集
#### 连接

内连接
```sql
select sales.*, things.*
from sales joins things 
on sales.id = things.id;
```

外连接

```sql
select sales.*, things.*
from sales [left| right | full] outer join things 
on sales.id = things.id;
```