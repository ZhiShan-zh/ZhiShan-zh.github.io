# test测试命令——Shell


使用`test`命令可以对文件、字符串等进行测试，一般配合控制语句是用，不应该单独使用。


# 1 字符串测试


- `test str1=str2`：测试字符串是否相等
- `test str1!=str2`：测试字符串是否不相等
- `test str`：测试字符串是否不为空
- `test -n str`：测试字符串是否不为空
- `test -z str`：测试字符串是否为空



# 2 int测试


- `test int1 -eq int2`：测试整数是否相等
- `test int1 -ne int2`：测试整数是否不相等
- `test int1 -ge int2`：测试int1是否>=int2
- `test int1 -gt int2`：测试int1是否>int2
- `test int1 -le int2`：测试int1是否<=int2
- `test int1 -lt int2`：测试int1是否<int2



# 3 文件测试


- `test -d file`：判断指定文件是否为目录
- `test -f file`：判断指定文件是否为常规文件
- `test -x file`：判断指定文件是否可执行
- `test -r file`：判断指定文件是否为可读
- `test -w file`：判断指定文件是否为可写
- `test -a file`：判断指定文件是否为存在
- `test -s file`：判断指定文件大小是否非0