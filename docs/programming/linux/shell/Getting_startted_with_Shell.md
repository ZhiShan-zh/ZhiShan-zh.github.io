# Shell入门

# 1 Shell入门案例

```shell
#!/bin/sh
# This is to show what a example looks like.
echo "My First Shell!"
echo "This is current directory."
/bin/pwd
echo
echo "This is files"
/bin/ls
```

**注释：**

- `#!/bin/sh`：固定格式，位置在shell脚本开始位置
- `# xxx...`：单行注释
- `echo "xxxx"`：输出。echo后没有内容的化，相当于空行
- `/bin/pwd`：shell脚本中的命令一定是绝对路径的命令
- shell脚本以sh结尾
- `sh example.sh`：运行shell脚本，example是shell脚本的名称

# 2 计划任务

如果我们想使用Shell脚本，制定个计划任务，比如每周的周一到周五给管理员发一个信息（比如当前主机的信息，如内存使用情况，在线人数，磁盘空间等）：

```shell
#！/bin/sh
/bin/date +%F >> /test/log.info
echo "disk info" >> /test/log.info
/bin/df -h >> /test/log.info
echo >> /test/log.info
echo "online users" >> /test/log.info
/usr/bin/who | /bin/grep -v root >> /test/log.info
echo "memory info:" >> /test/log.info
/usr/bin/free -m >> /test/log.info
echo >> /test/log.info
"write root"
/usr/bin/write root < /test/log.info && /bin/rm /test/log.info
crontab -e
0 9 * * 1-5 /bin/sh /test/log.info
```

**注释：**

- `>>`：追加输出
- `|`：管道符号。用法为`command 1 |command 2`：
  - 把第一个命令command 1执行的结果作为command2的输入传给command 2
- `<`：输入
- `&&`：逻辑与。用法`command1 && command2`
  - 命令之间使用 && 连接，实现逻辑与的功能。
  - 只有在 && 左边的命令返回真（命令返回值 $? == 0），&& 右边的命令才会被执行。
  - 只要有一个命令返回假（命令返回值 $? == 1），后面的命令就不会被执行。
