[TOC]

## Linux History

### History查看

```
history
```

### History存储文件

```
~/.bash_history
```

### History清理

* 编辑存储文件，删除痕迹

* `history -c` 删除当前用户的记录

* 在`vim`中执行命令，并设置不记录。

    ```bash
    :set history=0
    :!command
    ```

* 通过修改配置文件`/etc/profile`，使系统不再保存命令记录。

    ```
    HISTSIZE=0
    ```

## 系统日志痕迹

* `/var/log/btmp`            记录所有登录失败信息，使用`lastb`命令查看
* `/var/log/lastlog`       记录系统中所有用户最后一次登录时间的日志，使用`lastlog`命令查看
* `/var/log/wtmp`            记录所有用户的登录、注销信息，使用`last`命令查看
* `/var/log/utmp`            记录当前已经登录的用户信息，使用`w`,`who`,`users`等命令查看
* `/var/log/secure`         记录与安全相关的日志信息 **没找到**
* `/var/log/message`       记录系统启动后的信息和错误日志 **没找到**

### 清除日志

* 直接清空，简单粗暴 `> /var/log/...`
* 使用`sed`命令替换IP等信息。

## Web入侵痕迹

### 找到Web日志

* `nginx`  --- `/var/log/nginx/access.log`

### 清理日志

1. 替换IP地址。
2. 将没有痕迹的部分提取出来，覆盖原本的日志。



## 隐藏远程SSH登陆记录

* `-T Disable pseudo-terminal allocation.`，不会被w、who、last等指令检测到，执行命令也不会在history中记录。

    ```bash
    ssh -T user@ip /bin/bash
    ```

* 不记录ssh公钥在本地.ssh目录中

    ```bash
    ssh -o UserKnownHostsFile=/dev/null -T user@ip /bin/bash -i
    ```

    

## 文件安全删除工具

### shred

实现安全的从硬盘上擦除数据，默认覆盖3次，通过`-n`指定数据覆盖次数。

```bash
-f, --force    change permissions to allow writing if necessary
-n, --iterations=N  overwrite N times instead of the default (3)
--random-source=FILE  get random bytes from FILE
-s, --size=N   shred this many bytes (suffixes like K, M, G accepted)
-u             deallocate and remove file after overwriting
--remove[=HOW]  like -u but give control on HOW to delete;  See below
-v, --verbose  show progress
-x, --exact    do not round file sizes up to the next full block;
this is the default for non-regular files
-z, --zero     add a final overwrite with zeros to hide shredding
--help     display this help and exit
--version  output version information and exit
```

```
root@donx:~# shred -f -n 8 -v -z -u flag
shred: flag: pass 1/9 (random)...
shred: flag: pass 2/9 (aaaaaa)...
shred: flag: pass 3/9 (ffffff)...
shred: flag: pass 4/9 (random)...
shred: flag: pass 5/9 (000000)...
shred: flag: pass 6/9 (random)...
shred: flag: pass 7/9 (555555)...
shred: flag: pass 8/9 (random)...
shred: flag: pass 9/9 (000000)...
shred: flag: removing
shred: flag: renamed to 0000
shred: 0000: renamed to 000
shred: 000: renamed to 00
shred: 00: renamed to 0
shred: flag: removed
```

### dd

可用于安全地清除硬盘或者分区的内容。

[linux命令--磁盘命令dd - milkty - 博客园 (cnblogs.com)](https://www.cnblogs.com/kongzhongqijing/articles/9049336.html)

```bash
dd if=输入文件 of=输出文件 bs=块大小 count=块数
```

### wipe

Wipe 使用特殊的模式来重复地写文件，从**磁性**介质中安全擦除文件。（**固态或内存不保证正确性和效果**）

```bash
wipe filename
```

### Secure-Delete

> [Secure-Delete讲解](https://linux.cn/article-8123-1.html#toc_3)

工具集合，提供`srm`、`sdmem`、`sfill`、`sswap`，4个安全删除文件的命令行工具。

```bash
apt install secure-delete
srm filename
sfill filename
sswap /dev/sda1
sdmem
```

`srm`安全删除目录或文件。

`sfill`安全填充文件、目录或磁盘，并且清理`inode`，使用`/dev/urandom`。

`sswap`安全擦除`swap`分区。

> 请记住在使用 `sswap` 之前卸载 swap 分区！ 否则你的系统可能会崩溃！

`sdmem`内存擦除器，其设计目的是以安全的方式删除存储器（RAM）中的数据。

