---
title: Azkaban 
date: 2017-12-30
hidden: true
---

[Azkaban](https://azkaban.github.io)是由Linkedin开源的一个批量工作流任务调度器。用于在一个工作流内以一个特定的顺序运行一组工作和流程。Azkaban定义了一种KV文件格式来建立任务之间的依赖关系，并提供一个易于使用的web用户界面维护和跟踪你的工作流。

Azkaban由三个关键组件构成：
![Picture1](figures/Picture1.png)
1)	AzkabanWebServer：AzkabanWebServer是整个Azkaban工作流系统的主要管理者，它用户登录认证、负责project管理、定时执行工作流、跟踪工作流执行进度等一系列任务。
2)	AzkabanExecutorServer：负责具体的工作流的提交、执行，它们通过mysql数据库来协调任务的执行。
3)	关系型数据库（MySQL）：存储大部分执行流状态，AzkabanWebServer和AzkabanExecutorServer都需要访问数据库。



### 安装

 下载以后使用gradlew编译安装，

```
./gradlew build installDist -x test
```

随后准备mysql数据库

```sql
create database azkaban;
use azkaban;
CREATE USER 'azkaban'@'%' IDENTIFIED BY 'azkaban'; #创建用户noah_dba
grant all on azkaban.* to azkaban@'%' identified by 'azkaban'; #授权azkaban给azkaban
flush privileges;#刷新
source azkaban-db/create-all-sql-0.1.0-SNAPSHOT.sql
```

随后修改exec-server和web-server下的azkaban.properties文件

```text
default.timezone.id=Asia/Shanghai #默认时区为美国时区，需要修改不然时间对不上
mysql.host=centos #如果mysql服务器在本机可以改成localhost
```

随后使用`start-web.sh`和`start-exec.sh`命令分别启动。默认用户名和密码是azkaban。默认端口是8081

