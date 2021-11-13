# RCE 奇妙绕过

[TOC]

## 1. Linux命令

### 1.1 读命令

```bash
cat
more
less
head
tac
tail
nl
od -c
vi
vim
sort
uniq
file -f
bash -v file 2>&1
rev

# 配合
ls
find
dir
```

### 1.2 写shell

```bash
# find(ls,dir) (+ sed/cut...) + bash(sh)
find /usr/bin -name l? | sed -n 1p | bash
find /usr/bin -name l? | bash

# write one byte + bash(sh)
echo -n l > a
echo -n s > a
bash a

# 修改文件
sed

# 访问网页
wget 
curl
```

### 1.3 编码相关

```bash
xxd
od
base64
hexdump
```

