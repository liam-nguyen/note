---
title: Zeppelin 
date: 2017-12-30
hidden: true
---

[Apache Zeppelin](http://zeppelin.apache.org) 是一个基于网页的notebook，可以进行数据交互式分析，支持SQL，Scala等。启动后默认地址为[http://localhost:8080](http://localhost:8080)。



##### Hive

在设置Hive之前，需要确保能够远程连接Hive。Hadoop引入了一个安全伪装机制，使得Hadoop不允许上层系统直接将实际用户传递到Hadoop层，而是将实际用户传递给一个超级代理，由此代理在hadoop上执行操作，避免任意客户端随意操作hadoop。所以需要添加hadoop配置：

```xml tab="core-site.xml"
<property>
    <name>hadoop.proxyuser.root.hosts</name>
    <value>*</value>
</property>
<property>
    <name>hadoop.proxyuser.rot.groups</name>
    <value>*</value>
</property>
```

```xml tab="hdfs-site.xml"
<property>
    <name>dfs.webhdfs.enabled</name>
    <value>true</value>
</property>
```

随后配置interpreter, 类型选择jdbc。

* `driver`: `org.apache.hive.jdbc.HiveDriver`
* `default.url`: `jdbc:hive2://centos1:10000/`
* `default.user`:`root`
* `dependencies`: `hive-jdbc-2.3.6.jar`, `mysql-connector-java-5.1.48.jar`, `hadoop-common-2.7.7.jar`, `hive-service-2.3.6.jar`, `curator-client-2.7.1.jar`, `hive-service-rpc-2.3.6.jar`

##### spark

使用自己的Spark，在配置文件`zeppelin-env.sh`中加上`JAVA_HOME`和`SPARK_HOME`的地址。由于可能会有netty的冲突。在Dependencies中excludes栏中填上`io.netty:netty-all`。


##### mysql

配置interpreter, 类型选择jdbc。

* `driver`: `com.mysql.jdbc.Driver`
* `default.url`: `jdbc:mysql://127.0.0.1:3306/`
* `default.user`:`root`
* `dependencies`: `mysql-connector-java-8.0.13.jar`

##### HBase

在配置文件`zeppelin-env.sh`中加上`Hive_HOME`的地址。并添加Dependencies。
