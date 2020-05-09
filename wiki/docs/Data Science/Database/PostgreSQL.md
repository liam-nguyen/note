---
title: PostgreSQL
hidden: true
---

PostgreSQL是以加州大学伯克利分校计算机系开发的POSTGRES为基础的对象关系型数据库管理系统（ORDBMS）。POSTGRES 领先的许多概念在很久以后才出现在一些商业数据库系统中。



http://www.postgres.cn/docs/11/index.html

```bash
brew install postgresql
brew services start postgresql
psql postgres
```

常用控制台命令

```
\password：设置当前登录用户的密码
\h：查看SQL命令的解释，比如\h select。
\?：查看psql命令列表。
\l：列出所有数据库。
\c [database_name]：连接其他数据库。
\d：列出当前数据库的所有表格。
\d [table_name]：列出某一张表格的结构。
\du：列出所有用户。
\e：打开文本编辑器。
\conninfo：列出当前数据库和连接的信息。
\password [user]: 修改用户密码
\q：退出
```