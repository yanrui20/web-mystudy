# Linux 文件下载

[toc]

## wget

`wget http://192.168.8.111/test/test.txt`

## nc

```bash
接收端：
nc -lvnp 8888 > test.txt
发送端：
nc 47.100.64.189 8888 < test.txt
```

这个传输完成之后不会自动关闭，需要手动关闭。

## curl

`curl -O http://192.168.8.111/test/test.txt`，这里注意是大写的O

## ssh

需要用到的是`scp`命令，`scp`是基于`ssh`登录进行安全的远程文件拷贝，所以需要确保`ssh`服务是正常运行的

```bash
本地文件复制到远程：
scp /var/www/html/test/test.txt root@192.168.8.112:/root
远程文件复制到本地：
scp root@192.168.8.111:/var/www/html/test/test.txt /root
```

## rsync

Rsync是Linux系统中一个镜像备份工具，可以远程同步，文件复制，默认系统自带且运行。

```bash
本地到远程：
rsync -r 本地目录 远程ip:远程目录
```

