# 迁移与备份——Docker

# 1 容器保存为镜像

我们可以通过以下命令将容器保存为镜像

```shell
docker commit mynginx mynginx_i
```

# 2 镜像备份

我们可以通过以下命令将镜像保存为`tar`文件

```shell
docker save -o mynginx.tar mynginx_i
```

# 3 镜像恢复与迁移

首先我们先删除掉mynginx_img镜像  然后执行此命令进行恢复

```shell
docker load -i mynginx.tar
```

`-i`：输入的文件

执行后再次查看镜像，可以看到镜像已经恢复