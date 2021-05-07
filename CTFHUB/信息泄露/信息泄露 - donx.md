# 信息泄露

[TOC]

## 0. 注

这个由于是从我的pdf重制过来的（但是有一丢丢新加的内容），所以图片很糊。如果需要看原版pdf，欢迎去我的github。

[信息泄露 - donx.pdf](https://github.com/yanrui20/web-mystudy/blob/main/CTFHUB/信息泄露/信息泄露 - donx.pdf)

## 1. 目录遍历

![1.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/1.1.png)

直接多找找就能找到了，我这次是在：

![1.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/1.2.png)

## 2. PHPINFO

[phpinfo](https://www.php.net/manual/zh/function.phpinfo.php)一般记录了PHP的配置信息，很多敏感信息都能在里面找到，比如环境变量、加密用的Key啥的。

![2.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/2.1.png)

在PHPINFO的页面里面，直接查找flag就可以了，这里的flag就是被添加到了环境变量里面。

## 3. 备份文件下载

### 3.1 网站源码

![3.1.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.1.1.png)

根据网站的提示，用文件名+备份后缀去访问。

懒得一个一个的去输入，直接用burp爆破。

![3.1.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.1.2.png)

![3.1.3](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.1.3.png)

![3.1.4](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.1.4.png)

爆破结果：

![3.1.5](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.1.5.png)

所以网站上应该存在有www.zip， 去下载下来，发现三个文件

![3.1.6](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.1.6.png)

打开flag文件，发现里面什么都没有。

在网站上进入url/flag_2137417326.txt，发现了flag。

  ![3.1.7](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.1.7.png)

### 3.2 bak文件

![3.2.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.2.1.png)

网站上说flag在`index.php`的源码里面，估计是在php里面被注释了。

说是存在bak备份，于是尝试`index.php.bak`，果然存在，然后下载下来了备份文件。

打开便看到了flag。

![3.2.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.2.2.jpg)

### 3.3 vim缓存

> 如果意外退出就会保留，文件名为` .filename.swp`
> 第一次产生的交换文件名` .filename.txt.swp`
> 再次意外退出后，将会产生名为` .filename.txt.swo` 的交换文件
> 第三次产生的交换文件则为 `.filename.txt.swn`

![3.3.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.3.1.png)

说flag在index.php里面。尝试`.index.php.swp`

直接就下载下来了，但是用sublime打开发现是二进制文件（16进制表示），于是想到用vim来打开。

![3.3.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.3.2.png)

在CentOS8里面用vim打开之后，发现：

![3.3.3](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.3.3.png)

然后往下翻半天翻不到。。。。

于是我用sublime里面找了一下不全是`00`的部分，把中间全是`00`的给删了。

![3.3.4](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.3.4.png)


再把改了之后的文件在在CentOS8里面用vim打开。

![3.3.5](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.3.5.jpg)

终于找到了flag。

### 3.4 .DS_Store

![3.4.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.4.1.png)

直接下载.DS_Store。

发现还是二进制文件，删掉里面大部分`00`后，用vim打开。

![3.4.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.4.2.png)

隐隐约约还是可以看见flag  here，于是将中间所有的空字符删掉之后，大概可以看到一个文件名

![3.4.3](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.4.3.png)

于是去网站上试试。直接就拿到了flag。

![3.4.4](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/3.4.4.png)

## 4. Git泄露

Git是一个非常非常非常好用的版本管理工具。

他的版本控制信息都在`.git`目录下，一旦这个目录泄露，将可以看到或者恢复出整个工程。

### 4.1 Log

说是将.git文件夹直接部署到了线上环境。直接访问.git，发现被拒绝访问，说明文件是确实存在的。所以尝试用某种方法访问或者下载这个文件夹。这里尝试使用GitHack工具。（使用python2）

![4.1.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.1.1.png)

使用之后。。。发现clone成功。

![4.1.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.1.2.png)

因为clone下来了，直接在clone下来的文件夹里查看log

![4.1.3](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.1.3.png)

发现在最近的一次提交中移除了flag，直接比较两个版本就好。

![4.1.4](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.1.4.png)

也可以直接强行回到上一个版本：`git reset --hard 3884215`

就可以在文件夹里看到flag的文件了。打开文件就可以看到flag。

![4.1.5](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.1.5.png)

### 4.2 Stash

进去发现还是403：

![4.2.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.2.1.png)

还是用刚刚那个工具先clone下来再说。

![4.2.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.2.2.png)

然后对着log比较了几次都没发现flag。

想了想题目的要求是stash，所以猜测可能是把flag存到了stash里面。 

这里是[git stash的用法](https://blog.csdn.net/daguanjia11/article/details/73810577)。

使用`git stash list`命令之后发现有一个存档。

![4.2.3](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.2.3.png)

直接弹出存档。`git stash pop`

发现这个flag被弹出来了。直接打开文件，里面就是flag。

![4.2.4](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.2.4.png)

### 4.3 Index

老规矩，先clone下来。

![4.3.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.3.1.png)

唔，怎么clone下来就有flag了...去查查这道题怎么回事。

![4.3.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/4.3.2.png)

查了查好像也差不多，那就直接交吧。

## 5. SVN泄露

![5.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/5.1.png)

题目说flag在旧版本的源码里面，题目说的是用SVN进行版本控制，去找找.svn文件。

![5.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/5.2.png)

状态码 403 说明文件是存在的但是禁止访问。去找找有什么方法拿到文件。

这里使用`dvcs-ripper`工具中的`rip-svn.pl`进行clone。

![5.3](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/5.3.png)

发现多了一个文件和一个文件夹。

![5.4](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/5.4.png)

直接一通查找：

![5.5](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/5.5.png)

最终找到了flag。

## 6. HG泄露

![6.1](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/6.1.png)

尝试找.hg文件夹：

![6.2](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/6.2.png)

依旧是403，尝试使用`dvcs-ripper`工具中的`rip-hg.pl`进行clone。

```shell
./rip-hg.pl -v -u http://challenge-abe92eb262179135.sandbox.ctfhub.com:10080/.hg/
```

发现clone下来了一个.hg文件。里面有这些东西。

![6.3](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/6.3.png)

查看last-message.txt，说是加了一个flag，这就去找找在哪。

![6.4](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/6.4.png)

访问store文件夹里的fncache文件，发现了flag的位置。但是进入data之后却发现没有这个文件，估计 是被删了。

![6.5](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/6.5.png)

没办法，去看看网页上这个文件还有没有。还好，网页上这个文件存在。

![6.6](%E4%BF%A1%E6%81%AF%E6%B3%84%E9%9C%B2%20-%20donx.assets/6.6.png)

直接拿到flag。

