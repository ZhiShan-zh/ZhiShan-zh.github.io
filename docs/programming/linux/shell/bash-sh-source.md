# 执行Shell脚本的方式sh、bash、./、source

# 1 source

命令格式：`source file_name`

作用：

- 在当前bash环境（当前Shell，而不是另外打开一个子Shell）下读取并执行file_name中的命令；
- 运行一个shell脚本时不会启动另一个命令解释器；
- 该file_name文件可以无"执行权限"。

# 2 bash和sh

命令格式：

- `bash file_name`
- `sh file_name`

作用：

- 在当前bash环境下，打开一个子Shell来执行file_name脚本的命令；
- 运行一个shell脚本时会启动另一个命令解释器；
- 该file_name文件可以无"执行权限"。

# 3 `./`

格式：`./file_name`

作用：

- 在当前bash环境下，打开一个子Shell来执行file_name脚本的命令；
- 运行一个shell脚本时会启动另一个命令解释器；
- file_name必须在当前bash的目录中。
- 该file_name文件需要有"执行权限"。

