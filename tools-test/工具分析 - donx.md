[TOC]

# 子域名扫描工具

子域名扫描工具都以`uestc.edu.cn`为例。

## 1. **oneforall**

* 生成了688条记录

* 每条元数据都包含22列，其中有21列是有效信息。

    ![1](%E5%B7%A5%E5%85%B7%E5%88%86%E6%9E%90%20-%20donx.assets/1.png)

* 在结果文件夹里自动生成了CSV文件，比较方便，并且temp目录下也有子域名的txt文件。

* 用时近四分钟
* 没有找到和高并发有关的东西
* 有效性：多次手动访问，发现有效性高。

## 2. sublist3r

我拿python3跑的，中间报了个Error，说是无法连接Virustotal。然后python语句也报错了。

不过还是把结果跑了出来。

* 生成了186条记录，且都包含在了**oneforall**里面。

* 没有生成CSV文件，只在终端输出。

    ![2](%E5%B7%A5%E5%85%B7%E5%88%86%E6%9E%90%20-%20donx.assets/2.png)

* 每条信息只有一个子域名，没有更多的信息。

* 用时...不到一分钟，具体多少我不知道，但是他在我还没反应过来的时候就结束了。

* 高并发：这个东西可以自己设定thread。

* 有效性：因为都包含在了**oneforall**里面，所以我直接去看的**oneforall**里的记录，发现还是**oneforall**的信息多，更加好用。

## 3. subdomainsBrute

* 只找到19个，不知道是不是我的dns_server那个文件的问题。
* 每个元数据有子域名和ip地址两条信息。
* 时间应该在1分40秒左右。
* 高并发：可以设置thread和process。
* 有效性：有一些域名`oneforall`没有，且可以进去，比如`antivirus.uestc.edu.cn`。

## 4. subfinder

* 找到245条信息。
* 每条信息只有子域名。
* 用时21秒。
* 没有找到和高并发有关的东西。
* 有效性：有一些域名`oneforall`没有，但不能进去。

## 5. layer

* 太慢了，并且找到的大多数都不能用

## 总结

香还是`oneforall`香，但是在`oneforall`之后还可以用`subdomainsBrute`和`subfinder`查漏补缺。

至于速度的话，除了layer是直接暴力破解，实在太慢了以外，其他的都在接受范围之内。



# 路径扫描工具

路径扫描工具都以`https://bbs.uestc.edu.cn`为例。（迫害清水河畔）

## 1. **dirsearch**

* 用时三十秒
* 每一个元数据有三列，包含状态码、网页大小和路径
* 高并发：可以设置线程

## 2. **ffuf**

* 这个需要自己用字典去爆破？**差评**。

> 推荐的字典资源：https://github.com/danielmiessler/SecLists/
>
> 新手字典：https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/directory-list-2.3-big.txt

## 总结

`dirsearch`还是好用啊，如果`ffuf`也有一个比较好的字典，应该也是可以用的。

