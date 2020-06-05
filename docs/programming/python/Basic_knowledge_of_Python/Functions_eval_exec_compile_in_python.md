# Python内置函数之eval()、exec()、compile()函数

# 1 eval()
## 1.1 官方解释
> eval(source, globals=None, locals=None, /)
>    Evaluate the given source in the context of globals and locals.
>    
>    The source may be a string representing a Python expression or a code object as returned by compile().

>    The globals must be a dictionary and locals can be any mapping, defaulting to the current globals and locals.

>    If only globals is given, locals defaults to it.



## 1.2 eval()入门案例


```shell
>>> eval("3 + 4")
7
>>> eval("3 * 4")
12
>>> n = 4
>>> eval("3 * n")
12
>>> eval("type(n)")
<class 'int'>
```


# 2 exec()
## 2.1 官方解释
> exec(source, globals=None, locals=None, /)

>    Execute the given source in the context of globals and locals.

>    

>    The source may be a string representing one or more Python statements or a code object as returned by compile().

>    The globals must be a dictionary and locals can be any mapping, defaulting to the current globals and locals.

>    If only globals is given, locals defaults to it.

## 2.2 入门案例
### 2.2.1 单行代码执行
```shell
>>> exec("3 + 4")
>>> exec("print(3 + 4)")
7
>>> n = 4
>>> exec("print(3 * n)")
12
>>> exec("t1 = 5")
>>> print(t1)
5
```


### 2.2.2 多行代码放在一行


```shell
>>> str = "for i in range(5):\n\tprint('this num is:', i)"
>>> exec(str)
this num is: 0
this num is: 1
this num is: 2
this num is: 3
this num is: 4
```


### 2.2.3 多行代码
test.py文件内容：<br />

```python
n = 5
str = """
for i in range(n):
	print("this num is:", i)
"""
exec(str)
```

<br />执行test.py代码：<br />

```shell
[zh@zh-inspironn4050 文档]$ python test.py
this num is: 0
this num is: 1
this num is: 2
this num is: 3
this num is: 4
```


# 3 compile()
## 3.1 官方解释
> compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1, *, _feature_version=-1)

>    Compile source into a code object that can be executed by exec() or eval().

>    

>    The source code may represent a Python module, statement or expression.

>    The filename will be used for run-time error messages.

>    The mode must be 'exec' to compile a module, 'single' to compile a single (interactive) statement, or 'eval' to compile an expression.

>    The flags argument, if present, controls which future statements influence the compilation of the code.

>    The dont_inherit argument, if true, stops the compilation inheriting the effects of any future statements in effect in the code calling compile; if absent or false these statements do influence the compilation,
 in addition to any features explicitly specified.


## 3.2 mode为exec


```shell
>>> str = "for i in range(5):\n\tprint('this num is:', i)"
>>> com = compile(str, '', 'exec')
>>> com
<code object <module> at 0x7eff8b6c8710, file "", line 1>
>>> exec(com)
this num is: 0
this num is: 1
this num is: 2
this num is: 3
this num is: 4
```


## 3.3 mode为eval


```shell
>>> com = compile("3 + 4", '', 'eval')
>>> eval(com)
7
```

<br />

