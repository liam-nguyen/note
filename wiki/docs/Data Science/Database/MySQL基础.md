---
title: MySQL基础
---

MySQL is an open source, multithread, relational database management system.


### 1 basics

#### client and server

The `server` maintains, controls and protects your data, storing it in files on the computer where the server is running in various formats. It listens for requests from `client`.

For MySQL, `mysqld`(the *d* stands for *daemon*) is the server. `mysql` is a standard MySQL client. With its text-based interface, a user can log in and execute SQL queries.

#### basic command

* The `mysql_safe` script is the most common way to start `mysqld`, because this script can restart the daemon if it crashes.
* The `mysqlaccess` tool creates user accounts and sets their privileges.
* The`mysqladmin` utility can be used to manage the database server itself from the command-line. 
* The `mysqlshow` tool may be used to examine a server’s status, as well as information about databases and tables.
* The `mysqldump` utility is the most popular one for exporting data and table structures to a plain-text file, known as a `dump` file. 
* The command `mysql -u root -p` is usually used to start the client `mysql`, after which the passport should be filled.
* The command `mysql -u root -p -e "SELECT User,Host FROM mysql.user;"` gives a list of username and host combination on the server.

#### GUI

[Sequel Pro](https://sequelpro.com) is a fast, easy-to-use Mac database management application for working with MySQL databases. see [detail in Chinese](https://segmentfault.com/a/1190000006255923)

[WorkBench](https://www.mysql.com/products/workbench) provides data modeling, SQL development, and comprehensive administration tools for server configuration, user administration, backup, and much more.

Although GUIs are easy-to-use, in the long run they're not useful. The text-based `mysql` client causes you to think and remember more, and it's not that difficult to use or confusing. And the command-line method of using `mysql` allows you to interact with the server without much overhead.


#### auto-completion and syntax highlighting

[Mycli](http://www.mycli.net) is a command-line interface which support MariaDB, MySQL with auto-completion and syntax highlighting.

![](figures/mycli.jpg)

### 2 SQL commands

Glossary of commonly used SQL commands:

`ALTER TABLE`

```SQL
ALTER TABLE table_name ADD column datatype;
```
**ALTER TABLE** lets you add columns to a table in a database.


`AND`

```SQL
SELECT column_name(s)
FROM table_name
WHERE column_1 = value_1
AND column_2 = value_2;
```
AND is an operator that combines two conditions. Both conditions must be true for the row to be included in the result set.


`AS`

```SQL
SELECT column_name AS 'Alias'
FROM table_name;
```
**AS** is a keyword in SQL that allows you to rename a column or table using an alias.

`AVG`

```SQL
SELECT AVG(column_name)
FROM table_name;
```
**AVG()** is an aggregate function that returns the average value for a numeric column.


`BETWEEN`

```SQL
SELECT column_name(s)
FROM table_name
WHERE column_name BETWEEN value_1 AND value_2;
```
The BETWEEN operator is used to filter the result set within a certain range. The values can be numbers, text or dates.


`COUNT`

```SQL
SELECT COUNT(column_name)
FROM table_name;
```
**COUNT()** is a function that takes the name of a column as an argument and counts the number of rows where the column is not NULL.

`CREATE TABLE`

```SQL
CREATE TABLE table_name (column1 datatype, column2 datatype, column3 datatype);
```
**CREATE TABLE** creates a new table in the database. It allows you to specify the name of the table and the name of each column in the table.

`DELETE`

```SQL
DELETE FROM table_name WHERE some_column = some_value;
```
**DELETE** statements are used to remove rows from a table.


`GROUP BY`

```SQL
SELECT COUNT(*)
FROM table_name
GROUP BY column_name;
```
**GROUP BY** is a clause in SQL that is only used with aggregate functions. It is used in collaboration with the SELECT statement to arrange identical data into groups.


`INNER JOIN`

```SQL
SELECT column_name(s) FROM table_1
JOIN table_2
ON table_1.column_name = table_2.column_name;
```
An **inner join** will combine rows from different tables if the join condition is true.

`INSERT`

```SQL
INSERT INTO table_name (column_1, column_2, column_3) VALUES (value_1, value_2, value_3);
```
**INSERT** statements are used to add a new row to a table.


`LIKE`

```SQL
SELECT column_name(s)
FROM table_name
WHERE column_name LIKE pattern;
```
**LIKE** is a special operator used with the WHERE clause to search for a specific pattern in a column. SQL `pattern` matching enables you to use `_` to match any single character and `%` to match an arbitrary number of characters (including zero characters).


`LIMIT`

```SQL
SELECT column_name(s)
FROM table_name
LIMIT number;
```
**LIMIT** is a clause that lets you specify the maximum number of rows the result set will have.


`MAX`

```SQL
SELECT MAX(column_name)
FROM table_name;
```
**MAX()** is a function that takes the name of a column as an argument and returns the largest value in that column.


`MIN`

```SQL
SELECT MIN(column_name)
FROM table_name;
```

`MIN()` is a function that takes the name of a column as an argument and returns the smallest value in that column.


`OR`

```SQL
SELECT column_name
FROM table_name
WHERE column_name = value_1
OR column_name = value_2;
```
**OR** is an operator that filters the result set to only include rows where either condition is true.


`ORDER BY`

```SQL
SELECT column_name
FROM table_name
ORDER BY column_name1, column_name2 ASC|DESC;
```
**ORDER BY** is a clause that indicates you want to sort the result set by a particular column either alphabetically or numerically.


`OUTER JOIN`

```SQL
SELECT column_name(s) FROM table_1
LEFT JOIN table_2
ON table_1.column_name = table_2.column_name;
```
An **outer join** will combine rows from different tables even if the the join condition is not met. Every row in the left table is returned in the result set, and if the join condition is not met, then NULL values are used to fill in the columns from the right table.


`ROUND`

```SQL
SELECT ROUND(column_name, integer)
FROM table_name;
```
**ROUND()** is a function that takes a column name and an integer as an argument. It rounds the values in the column to the number of decimal places specified by the integer.


`SELECT`

```SQL
SELECT column_name FROM table_name;
```
**SELECT** statements are used to fetch data from a database. Every query will begin with SELECT.

`SELECT DISTINCT`

```SQL
SELECT DISTINCT column_name FROM table_name;
```
**SELECT DISTINCT** specifies that the statement is going to be a query that returns unique values in the specified column(s).


`SUM`

```SQL
SELECT SUM(column_name)
FROM table_name;
```
**SUM()** is a function that takes the name of a column as an argument and returns the sum of all the values in that column.


`UPDATE`

```SQL
UPDATE table_name
SET some_column = some_value
WHERE some_column = some_value;
```
**UPDATE** statments allow you to edit rows in a table.


`WHERE`

```SQL
SELECT column_name(s)
FROM table_name
WHERE column_name operator value;
```
**WHERE** is a clause that indicates you want to filter the result set to include only rows where the following condition is true. eg. `SELECT * FROM customers WHERE ID=7`;

#### SQL Operators

Comparison Operators and Logical Operators are used in the `WHERE` clause to filter the data to be selected.

**Comparison Operators**

The following comparison operators can be used in the `WHERE` clause:


| Operator | Description |
| --- | --- |
| = | Equal |
| != | Not equal  |
| > | Greater than  |
| < | Less than   |
| >= | Greater than or equal  |
| <= | Less than or equal |
| BETWEEN | Between an inclusive range |

`BETWEEN` Operator:

```SQL
SELECT * FROM customers
WHERE ID BETWEEN 3 AND 7;
```

**Logical Operators**

Logical operators can be used to combine two Boolean values and return a result of **true**, **false**, or **null**.

The following operators exists in SQL:

| Operator | Description |
| --- | --- |
| AND | TRUE if both expressions are TRUE |
| OR | TRUE if either expression is TRUE |
| IN | TRUE if the operand is equal to one of a list of expressions |
| NOT | Returns TRUE if expression is not TRUE  |



The `IN` Operator:

```SQL
SELECT * FROM customers 
WHERE City IN ('New York', 'Los Angeles', 'Chicago');
```

The `NOT IN` Operator:

```SQL
SELECT * FROM customers 
WHERE City NOT IN ('New York', 'Los Angeles', 'Chicago');
```

#### Functions

The `UPPER` function converts all letters in the specified string to uppercase. 
The `LOWER` function converts the string to lowercase.

The following SQL query selects all *Lastnames* as uppercase:

```SQL
SELECT FirstName, UPPER(LastName) AS LastName 
FROM employees;
```

The `SQRT` function returns the square root of given value in the argument.
Similarly, the `AVG` function returns the average value of a numeric column.
The `SUM` function is used to calculate the sum for a column's values.

The `MIN` function is used to return the minimum value of an expression in a `SELECT` statement.

E.g. you might wish to know the minimum salary among the employees:

```SQL
SELECT MIN(salary) AS Salary FROM employees;
```

#### Subqueries

A subquery is a query within another query. Enclose the subquery in parentheses. 

E.g.

```SQL
SELECT FirstName, Salary FROM employees 
WHERE  Salary > (SELECT AVG(Salary) FROM employees) 
ORDER BY Salary DESC;
```

#### Joining Tables

SQL can combine data from multiple tables. In SQL, 'joining tables' means combining data from two or more tables. A table join creates a `temporary table` showing the data from the joined tables.

To join tables, specify them as a comma-separated list in the `FROM` clause:

```SQL
SELECT customers.ID, customers.Name, orders.Name, orders.Amount 
FROM customers, orders
WHERE customers.ID = orders.Customer_ID
ORDER BY customers.ID
```

**Types of Join**

```SQL
SELECT table1.column1, table2.column2...
FROM table1 [INNER | LEFT | RIGHT | FULL OUTER] JOIN table2
ON table1.column_name = table2.column_name;
```
    

The following are types of `JOIN` that can be used in SQL:

* `INNER JOIN`: returns rows when there is a match between the tables.
* `LEFT JOIN`: returns rows from the left table, even if there are no matches in the right table. 
* `RIGHT JOIN`: returns rows from the right table, even if there are no matches in the left table. 
* `FULL OUTER JOIN`: return rows from the both left and right tables even if there’s no match

![](figures/sql_joins.jpg)


!!! Example "Example: Left, Right, Outer, Inner, Cross Joins"

    Simple Example: Let's say you have a `Students` table, and a `Lockers` table. In SQL, the first table you specify in a join, `Students`, is the LEFT table, and the second one, `Lockers`, is the RIGHT table.
    
    Each student can be assigned to a locker, so there is a `LockerNumber` column in the `Student` table. More than one student could potentially be in a single locker, but especially at the beginning of the school year, you may have some incoming students without lockers and some lockers that have no students assigned.
    
    For the sake of this example, let's say you have 100 students, 70 of which have lockers. You have a total of 50 lockers, 40 of which have at least 1 student and 10 lockers have no student.
    
    **INNER JOIN**(内连接) is equivalent to "show me all students with lockers".
    Any students without lockers, or any lockers without students are missing.
    Returns 70 rows.
    
    **LEFT OUTER JOIN**(左连接) would be "show me all students, with their corresponding locker if they have one". 
    This might be a general student list, or could be used to identify students with no locker. 
    Returns 100 rows.
    
    **RIGHT OUTER JOIN**(右连接) would be "show me all lockers, and the students assigned to them if there are any". 
    This could be used to identify lockers that have no students assigned, or lockers that have too many students. 
    Returns 80 rows (list of 70 students in the 40 lockers, plus the 10 lockers with no student).
    
    **FULL OUTER JOIN**(全连接) would be silly and probably not much use. 
    Something like "show me all students and all lockers, and match them up where you can" .
    Returns 110 rows (all 100 students, including those without lockers. Plus the 10 lockers with no student).
    
    **CROSS JOIN** is also fairly silly in this scenario.
    It doesn't use the linked `lockernumber` field in the students table, so you basically end up with a big giant list of every possible student-to-locker pairing, whether or not it actually exists.
    Returns 5000 rows (100 students x 50 lockers). Could be useful (with filtering) as a starting point to match up the new students with the empty lockers.

!!! note "cartesian product"
    
    When you do cross join you will get cartesian product(笛卡尔积) of rows from tables in the join. In other words, it will produce rows which combine each row from the first table with each row from the second table.

#### Backing up and Restoring

**Backing up**

```bash
mysqldump -u user -p database_name > /data/backups/all-dbs.sql
```
**Restoring**

```bash
mysql -u user -p < all-dbs.sql
```

#### 创建数据库

创建数据库时设置字符集，可以避免出现中文乱码：

```sql
CREATE DATABASE database_name DEFAULT CHARACTER SET utf8;
```

类似的，创建表时，使用`DEFULAT CHARSET=utf8`：

```mysql
CREATE TABLE table_name () DEFAULT CHARSET=utf-8;
```


#### 远程登录

MySQL默认情况下只允许本地连接。想要远程连接MySQL数据库，需要授权。

```sql
grant all privileges on 库名.表名 to '用户名'@'IP地址' identified by '密码' with grant option;
flush privileges; //刷新MySQL的系统权限相关表­
```

例如给在远程登录的root用户授予所有权限：

```sql
mysql> use mysql;
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;
mysql> flush privileges;  
```

