# SQL中的条件语句

# 1 case_when_then

## 1.1 case简单函数

```sql
case column_name
	when value_1 then customized_value_1
	when value_2 then customized_value_2
	else else_value end
```

示例：

```sql
select name,
	case sex
        when '1' then '男'
        when '2' then '女’
        else '其他' end
from user;		
```

## 1.2 case搜索函数

```sql
case when condition_1 then value_1
	when condition_2 then value_2
	else else_value end
```

**提示**：condition中可以添加并且条件，如or或and，可以参见where

示例：

```sql
select name,
	case when sex = '1' then '男'
        when sex = '2' then '女’
        else '其他' end
from user; 
```

# 2 MySQL中的IF和IFNULL

## 2.1 IF

```sql
IF(expr1:any, expr2:any, expr3:any)
```

- 如果 expr1 是TRUE (expr1 <> 0 and expr1 <> NULL)，返回值为expr1；否则返回值则为 expr2。
- IF() 的返回值为数字值或字符串值，具体情况视其所在语境而定。

示例：

```sql
mysql> SELECT IF(1>2,2,3);
        -> 3
mysql> SELECT IF(12,'yes','no');
        -> 'yes'
mysql> SELECT IF(STRCMP('test','test1'),'no','yes');
        -> 'no'
```

注意：**expr1被评估为整数值，这意味着，如果要测试浮点或字符串值，则应使用比较操作来进行测试。**

·

```sql
mysql> SELECT IF(1, 1, '0');
		-> '1'
mysql> SELECT IF(1, 1, 0.5);
		-> 1.0
mysql> SELECT IF(1, 1, NULL);
		-> 1
```

关于返回值：

- 如果expr2或expr3返回的是字符串，则返回值为字符串；
- 如果expr2或expr3返回的是浮点型，则返回值为浮点型；
- 如果expr2或expr3返回的是整型，则返回值为整型；

## 2.2 IFNULL

```sql
IFNULL(expr1:any, expr2:any)
```

- 假如expr1 不为 NULL（不包括0），则 IFNULL() 的返回值为 expr1; 否则其返回值为 expr2。
- IFNULL()的返回值是数字或是字符串，具体情况取决于其所使用的语境。

示例：

```sql
mysql> SELECT IFNULL(1,0);
        -> 1
mysql> SELECT IFNULL(NULL,10);
        -> 10
mysql> SELECT 1/0;
        -> NULL
mysql> SELECT IFNULL(1/0,10);
        -> 10
mysql> SELECT IFNULL(1/0,'yes');
        -> 'yes'
mysql> SELECT IFNULL(0,'yes');
        -> 0
```

# 3 Oracle中的decode

## 3.1 简单版

```sql
decode(expression,value,result1,result2)
```

- 如果expression=value，则输出result1，否则输出result2

```sql
mysql> SELECT decode(1+2, 3, 'a', 'b') from dual;
        -> 'a'
mysql> SELECT decode(1+1, 3, 'a', 'b') from dual;
        -> 'b'
```

## 3.2 复杂版

```sql
decode(expression,value1,result1,value2,result2,value3,result3......,default)
```

- 如果expression=value1，则输出result1，expression=value2，输出reslut2，expression=value3，输出result3，

    若expression不等于所列出的所有value，则输出为default

```sql
mysql> SELECT decode(1+2, 1, 'a', 2, 'b', 3, 'c', 'd') from dual;
        -> 'c'
mysql> SELECT decode(1+5, 1, 'a', 2, 'b', 3, 'c', 'd') from dual;
        -> 'd'
```



# 4 DECODE 与CASE WHEN 的比较

1. DECODE 只有Oracle 才有，其它数据库不支持;
2. CASE WHEN的用法， Oracle、SQL Server、 MySQL 都支持;
3. DECODE 只能用做相等判断,但是可以配合sign函数进行大于，小于，等于的判断，CASE when可用于=,>=,<,<=,<>,is null,is not null 等的判断;
4. DECODE 使用其来比较简洁，CASE 虽然复杂但更为灵活;
5. 另外，在decode中，null和null是相等的，但在case when中，只能用is null来判断。