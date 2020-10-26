# Docker 常见故障

# 1 容器启动后自动退出、或进入“restarting”状态

使用Docker经常遇到的一个问题是Docker容器启动后自动退出，使用docker的logs命令也没有关于容器的任何日志输出。如果容器的启动参数包含“restart=always” 或“--restart”则会不停重启。

这个问题常见的原因是容器的PID1进程(初始化进程)不是一个长时间运行的进程，或者它启动了一个后台进程就退出。由于容器服务是以“detach”方式运行容器，这样当PID1进程结束后就会导致整个容器退出。

参考解决思路为：在服务的“command”在“更多设置”中将其修改为/bin/sh -c "while true; do sleep 10; done" 这样的死循环；这样可以保证容器的持续运行。

# 2 容器中使用systemctl启动服务报错：Failed to get D-Bus connection: Operation not permitted

**产生的原因**：这从Docker的设计理念说起，Docker的设计理念是在容器里面不运行后台服务，容器本身就是宿主机上的一个独立的主进程，也可以间接的理解为就是容器里运行服务的应用进程。一个容器的生命周期是围绕这个主进程存在的，所以正确的使用容器方法是将里面的服务运行在前台。

**解决方法**：

- 在启动容器时，需要加上`--privileged`参数来添加权限。
- 不能使用默认的bash，而需要执行`/usr/sbin/init`

示例命令：`docker run -dit --privileged <image_id> /usr/sbin/init`