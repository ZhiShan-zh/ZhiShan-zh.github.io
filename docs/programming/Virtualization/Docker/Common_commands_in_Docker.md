# Docker中的常用命令

# 1 镜像相关命令

## 1.1 查看镜像

```shell
docker images
```

输出字段说明：

- REPOSITORY：镜像名称
- TAG：镜像标签
- IMAGE ID：镜像ID
- CREATED：镜像的创建日期（不是获取该镜像的日期）
- SIZE：镜像大小

这些镜像都是存储在Docker宿主机的`/var/lib/docker` 目录下

## 1.2 搜索镜像

如果你需要从网络中查找需要的镜像，可以通过以下命令搜索

```shell
docker search 镜像名称
```

输出字段说明：

- NAME：仓库名称
- DESCRIPTION：镜像描述
- STARS：用户评价，反应一个镜像的受欢迎程度
- OFFICIAL：是否官方
- AUTOMATED：自动构建，表示该镜像由Docker Hub自动构建流程创建的

## 1.3 拉取镜像

拉取镜像就是从中央仓库中下载镜像到本地

```shell
docker pull 镜像名称
```

例如，我要下载centos7镜像：`docker pull centos:7`

## 1.4 删除镜像

按镜像ID删除镜像：

```shell
docker rmi 镜像ID
```

删除所有镜像：

```shell
docker rmi `docker images -q`
```

# 2 容器相关命令

## 2.1 查看容器

查看正在运行的容器

```
docker ps
```

查看所有容器

```
docker ps –a
```

查看最后一次运行的容器

```
docker ps –l
```

查看停止的容器

```
docker ps -f status=exited
```

## 2.2 创建与启动容器

创建容器命令：`docker run`

创建容器常用的参数说明：

- `-i`：表示运行容器
- `-t`：表示容器启动后会进入其命令行。加入`-i -t`参数后，容器启动后就能登录进去。即分配一个伪终端。
- `--name`：为创建的容器命名。
- `-v`：表示目录映射关系（前者是宿主机目录，后者是映射到宿主机上的目录），可以使用多个`－v`做多个目录或文件映射。注意：最好做目录映射，在宿主机上做修改，然后共享到容器上。
- `-d`：在run后面加上`-d`参数，则会创建一个守护式容器在后台运行（这样创建容器后不会自动登录容器，如果只加`-i -t`两个参数，创建后就会自动进去容器）。
- `-p`：表示端口映射，前者是宿主机端口，后者是容器内的映射端口。可以使用多个`-p`做多个端口映射

### 2.2.1 交互式方式创建容器

```shell
docker run -it --name=容器名称 镜像名称:标签 /bin/bash
```

这时我们通过ps命令查看，发现可以看到启动的容器，状态为启动状态  

退出当前容器

```shell
exit
```

### 2.2.2 守护式方式创建容器：

```shell
docker run -di --name=容器名称 镜像名称:标签
```

登录守护式容器方式：

```shell
docker exec -it 容器名称 (或者容器ID)  /bin/bash
```

## 2.3 停止与启动容器

停止容器：

```shell
docker stop 容器名称（或者容器ID）
```

启动容器：

```shell
docker start 容器名称（或者容器ID）
```

## 2.4 文件拷贝

如果我们需要将文件拷贝到容器内可以使用cp命令：

```shell
docker cp 需要拷贝的文件或目录 容器名称:容器目录
```

也可以将文件从容器内拷贝出来：

```shell
docker cp 容器名称:容器目录 需要拷贝的文件或目录
```

## 2.5 目录挂载

我们可以在创建容器的时候，将宿主机的目录与容器内的目录进行映射，这样我们就可以通过修改宿主机某个目录的文件从而去影响容器。
创建容器 添加-v参数 后边为   宿主机目录:容器目录，例如：

```shell
docker run -di -v /usr/local/myhtml:/usr/local/myhtml --name=mycentos3 centos:7
```

如果你共享的是多级的目录，可能会出现权限不足的提示。

这是因为CentOS7中的安全模块selinux把权限禁掉了，我们需要添加参数`--privileged=true`来解决挂载的目录没有权限的问题

## 2.6 查看容器IP地址

我们可以通过以下命令查看容器运行的各种数据

```shell
docker inspect 容器名称（容器ID） 
```

也可以直接执行下面的命令直接输出IP地址

```shell
docker inspect --format='{{.NetworkSettings.IPAddress}}' 容器名称（容器ID）
```

## 2.7 删除容器 

删除指定的容器：

```shell
docker rm 容器名称（容器ID）
```
