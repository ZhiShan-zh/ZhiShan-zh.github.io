# 便利使用virtualenv

# 1 便捷切换环境命令workon

## 1.1 V1.0

安装了Python虚拟环境命令virtualenv之后，创建虚拟环境是挺方便的，但是切换环境有时候需要写虚拟环境的路径才能切换，这挺不方便的。网上有workon切换工具，还需要查资料安装，便手写一个。

使用这个工具，需要把虚拟环境目录放在当前用户的家目录下，并且定义为`vitualenvs`，路径为`~/vitualens/env_name`；如果虚拟环境目录没有设为`vitualenvs`，则需要配置一个环境变量`echo export ENV_HOME=~/env_home > ~/.bash_profile`

文件名称：`workon`

运行方式：`source workon env_name`

- source：为当前Shell中运行脚本里的命令
- bash：为另外打开一个子Shell来运行脚本
  - 如果使用bash的话，只是在子shell中激活了虚拟环境，脚本执行完毕则关闭子Shell，则虚拟环境也就退出了。

代码：

```shell
#!/bin/bash
# 脚本里边无法识别~，需要使用全局变量（$HOME）获取家目录
env_home="$HOME/virtualenvs"
if [ ! -d "$env_home" ]; then
	env_home=$ENV_HOME;
fi
if [ ! -d "$env_home" ]; then
	env_home=$HOME;
fi
if [ ! -d "$env_home" ]; then
	echo "找不到虚拟环境目录:$env_home"
	echo "请把虚拟环境目录设定在当前用户家目录的virtualenvs目录下；或运行命令"
	echo 'echo export ENV_HOME=~/env_home > ~/.bash_profile'
	echo "并把其中的~/env_home替换为您自己的虚拟环境目录。"
	echo"然后运行source ~/.bash_profile"
else
	if test $1; then
		source "$env_home/$1/bin/activate"
	else
		echo "缺少参数，命令格式为workon env_name"
	fi
fi
```

