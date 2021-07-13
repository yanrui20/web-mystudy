[TOC]

# php弱比较

* md5绕过

```
if($a != $b && md5($a) == md5($b))
a[]=1&b[]=2
```

* 正则


```
if($c && ereg ("^[a-zA-Z0-9]+$", $c) === FALSE)
c=%001
```

