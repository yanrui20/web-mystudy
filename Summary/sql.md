[TOC]

# 绕过

## 1. select 被过滤 -- table

> TABLE table_name [ORDER BY column_name] [LIMIT number [OFFSET number]]

这个作用是列出表的全部内容，于是就可以利用这个语句来进行注入。

这个好像有版本要求