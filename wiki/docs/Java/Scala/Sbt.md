---
title: Sbt
toc: true
date: 2017-3-30
top: 8
---

[Sbt](https://www.scala-sbt.org/1.x/docs/zh-cn/Getting-Started.html)是scala默认的构建工具。默认情况下，sbt使用的目录与Maven相同

![](figures/15722253872962.png)

项目根目录中的`build.sbt`文件定义了工程的构建：例如指定工程名称(name)，指定依赖列表(libraryDependencies)。sbt构建使用Scala代码定义，并且sbt是迭代的：`project`文件夹是构建里面的构建，也就是说构建定义本身就是sbt项目。


## 配置源

默认情况下，国内下载速度很慢，一般需要配置国内源。创建配置文件`~/.sbt/repositories`为

```text
[repositories]
local
aliyun: http://maven.aliyun.com/nexus/content/groups/public/
typesafe: http://repo.typesafe.com/typesafe/ivy-releases/, [organization]/[module]/(scala_[scalaVersion]/)(sbt_[sbtVersion]/)[revision]/[type]s/[artifact](-[classifier]).[ext], bootOnly
sonatype-oss-releases
maven-central
sonatype-oss-snapshots
```