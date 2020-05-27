# Shell函数

# 1 Shell函数的格式
**说明**：

- `function`函数声明字段可以省略。
- 函数名后边的小括号里边不能有任何形式参数。
- 函数可以使用 `return` 字段饭后int类型的值（范围在0~255之间）；也可以不用 `return` ,函数将把最后一条命令的执行结果返回。
```shell
[function] fun[()]
{
	doSomething;
	[return int;]
}
```


# 2 入门案例


```shell
#!/bin/bash
function firstFun(){
	/bin/ls;
}

firstFun
```


```shell
#!/bin/bash
firstFun()
{
	/bin/ls;
}
firstFun

```


# 3 函数参数
调用函数可以向其传递0个或多个参数。各个参数和函数名之间以空格分割；函数内部使用 `$n` ，如果n >= 10的话 `${n}`  ，来获得第n个参数.



| $# | 传递到脚本或函数的参数个数 |
| --- | --- |
| $* | 以一个单字符串显示所有向脚本传递的参数 |
| $$ | 脚本运行的当前进程ID号 |
| $! | 后台运行的最后一个进程的ID号 |
| $@ | 与$*相同，但是使用时加引号，并在引号中返回每个参数。 |
| $- | 显示Shell使用的当前选项，与set命令功能相同。 |
| $? | 显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。 |
