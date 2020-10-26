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

## 1.5 查看镜像详情

### 1.5.1 语法

`docker inspect [OPTIONS] NAME|ID [NAME|ID...]`

- 作用：返回Docker对象的底层信息
- 选项：
    - `-f`,   `--format string` ：使用给定的Go模板格式化输出
        - 一级单字段值：`docker inspect --format='{{.属性}} 镜像名称或镜像ID'`或`docker inspect --f '{{.属性}} 镜像名称或镜像ID'`
        - 二级单字段值：`sudo docker inspect -f '{{.属性.属性}}' 镜像名称或镜像ID`
        - 多级单字段值：`sudo docker inspect -f '{{.属性.属性.省略N个属性}}' 镜像名称或镜像ID`
        - 多字段值：`sudo docker inspect -f '{{.属性.属性.省略N个属性}}自定义分隔符{{.属性.属性.省略N个属性}}' 镜像名称或镜像ID`
    - `-s`,  `--size` ：如果类型是container，则显示总文件大小　   
    - `--type string` ：返回指定类型的JSON

### 1.5.2 使用示例

- 查看镜像列表：`docker images`

    - ```
        REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
        zookeeper           latest              6982b35ff928        2 weeks ago         252MB
        ```

- 查看镜像详情：`sudo docker inspect 镜像名称`或`docker inspect 镜像id`

    - 示例：`sudo docker inspect zookeeper`或`sudo docker inspect 6982b35ff928`

    - ```json
        [
            {
                "Id": "sha256:6982b35ff928aa314b5fb9107edaabb5969039be9271222ef1aa5ae116f34830",
                "RepoTags": [
                    "zookeeper:latest"
                ],
                "RepoDigests": [
                    "zookeeper@sha256:fe31564f6864be074109cc70f6f70c66c111faf4cf8af1af943a678e0f35cd51"
                ],
                "Parent": "",
                "Comment": "",
                "Created": "2020-06-29T20:44:15.02618204Z",
                "Container": "1d09188d6a83fc7174c369ee87dc600b93104b7be5fe4685fb96ef7a3e4cd484",
                "ContainerConfig": {
                    "Hostname": "1d09188d6a83",
                    "Domainname": "",
                    "User": "",
                    "AttachStdin": false,
                    "AttachStdout": false,
                    "AttachStderr": false,
                    "ExposedPorts": {
                        "2181/tcp": {},
                        "2888/tcp": {},
                        "3888/tcp": {},
                        "8080/tcp": {}
                    },
                    "Tty": false,
                    "OpenStdin": false,
                    "StdinOnce": false,
                    "Env": [
                        "PATH=/usr/local/openjdk-11/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/apache-zookeeper-3.6.1-bin/bin",
                        "LANG=C.UTF-8",
                        "JAVA_HOME=/usr/local/openjdk-11",
                        "JAVA_VERSION=11.0.7",
                        "JAVA_BASE_URL=https://github.com/AdoptOpenJDK/openjdk11-upstream-binaries/releases/download/jdk-11.0.7%2B10/OpenJDK11U-jre_",
                        "JAVA_URL_VERSION=11.0.7_10",
                        "ZOO_CONF_DIR=/conf",
                        "ZOO_DATA_DIR=/data",
                        "ZOO_DATA_LOG_DIR=/datalog",
                        "ZOO_LOG_DIR=/logs",
                        "ZOO_TICK_TIME=2000",
                        "ZOO_INIT_LIMIT=5",
                        "ZOO_SYNC_LIMIT=2",
                        "ZOO_AUTOPURGE_PURGEINTERVAL=0",
                        "ZOO_AUTOPURGE_SNAPRETAINCOUNT=3",
                        "ZOO_MAX_CLIENT_CNXNS=60",
                        "ZOO_STANDALONE_ENABLED=true",
                        "ZOO_ADMINSERVER_ENABLED=true",
                        "ZOOCFGDIR=/conf"
                    ],
                    "Cmd": [
                        "/bin/sh",
                        "-c",
                        "#(nop) ",
                        "CMD [\"zkServer.sh\" \"start-foreground\"]"
                    ],
                    "ArgsEscaped": true,
                    "Image": "sha256:5838bca00d1e75879153e74937f5f749dbc1063d003f5214062e310f0a1d946c",
                    "Volumes": {
                        "/data": {},
                        "/datalog": {},
                        "/logs": {}
                    },
                    "WorkingDir": "/apache-zookeeper-3.6.1-bin",
                    "Entrypoint": [
                        "/docker-entrypoint.sh"
                    ],
                    "OnBuild": null,
                    "Labels": {}
                },
                "DockerVersion": "18.09.7",
                "Author": "",
                "Config": {
                    "Hostname": "",
                    "Domainname": "",
                    "User": "",
                    "AttachStdin": false,
                    "AttachStdout": false,
                    "AttachStderr": false,
                    "ExposedPorts": {
                        "2181/tcp": {},
                        "2888/tcp": {},
                        "3888/tcp": {},
                        "8080/tcp": {}
                    },
                    "Tty": false,
                    "OpenStdin": false,
                    "StdinOnce": false,
                    "Env": [
                        "PATH=/usr/local/openjdk-11/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/apache-zookeeper-3.6.1-bin/bin",
                        "LANG=C.UTF-8",
                        "JAVA_HOME=/usr/local/openjdk-11",
                        "JAVA_VERSION=11.0.7",
                        "JAVA_BASE_URL=https://github.com/AdoptOpenJDK/openjdk11-upstream-binaries/releases/download/jdk-11.0.7%2B10/OpenJDK11U-jre_",
                        "JAVA_URL_VERSION=11.0.7_10",
                        "ZOO_CONF_DIR=/conf",
                        "ZOO_DATA_DIR=/data",
                        "ZOO_DATA_LOG_DIR=/datalog",
                        "ZOO_LOG_DIR=/logs",
                        "ZOO_TICK_TIME=2000",
                        "ZOO_INIT_LIMIT=5",
                        "ZOO_SYNC_LIMIT=2",
                        "ZOO_AUTOPURGE_PURGEINTERVAL=0",
                        "ZOO_AUTOPURGE_SNAPRETAINCOUNT=3",
                        "ZOO_MAX_CLIENT_CNXNS=60",
                        "ZOO_STANDALONE_ENABLED=true",
                        "ZOO_ADMINSERVER_ENABLED=true",
                        "ZOOCFGDIR=/conf"
                    ],
                    "Cmd": [
                        "zkServer.sh",
                        "start-foreground"
                    ],
                    "ArgsEscaped": true,
                    "Image": "sha256:5838bca00d1e75879153e74937f5f749dbc1063d003f5214062e310f0a1d946c",
                    "Volumes": {
                        "/data": {},
                        "/datalog": {},
                        "/logs": {}
                    },
                    "WorkingDir": "/apache-zookeeper-3.6.1-bin",
                    "Entrypoint": [
                        "/docker-entrypoint.sh"
                    ],
                    "OnBuild": null,
                    "Labels": null
                },
                "Architecture": "amd64",
                "Os": "linux",
                "Size": 252290293,
                "VirtualSize": 252290293,
                "GraphDriver": {
                    "Data": {
                        "LowerDir": "/var/lib/docker/overlay2/df7f5169ef02c3685e581f3a6ad414ca742e6eead834daa680a21ff159a1b513/diff:/var/lib/docker/overlay2/16f40930e5bbd78fb168eb8c73e0e7a563270ccff346a79cc64d06d5946ed5fc/diff:/var/lib/docker/overlay2/de399ff6f05a0800d462fd2acb5bbacb2271ed2afd91634040326b786382140f/diff:/var/lib/docker/overlay2/31f8616052b0f04fa11c4ce34ce98ae36d11fab8219cd276d58bbb84a57df29a/diff:/var/lib/docker/overlay2/1582ae224eb7f173faef96e2e32f858c06fdbe5b8f3482dc01806f938df125c9/diff:/var/lib/docker/overlay2/dd0c4251088d178c6450f0584e72f5fcb8219290268729d0b6d40fcdfef87aff/diff:/var/lib/docker/overlay2/36df9c1dafeed4beb31a959889c28d430db77c6137b5fdd8adc0a62e9acff909/diff",
                        "MergedDir": "/var/lib/docker/overlay2/cba01815a6e1d3a787b79300abda731ed627168e5e4f8f1b862d1549b1da38e1/merged",
                        "UpperDir": "/var/lib/docker/overlay2/cba01815a6e1d3a787b79300abda731ed627168e5e4f8f1b862d1549b1da38e1/diff",
                        "WorkDir": "/var/lib/docker/overlay2/cba01815a6e1d3a787b79300abda731ed627168e5e4f8f1b862d1549b1da38e1/work"
                    },
                    "Name": "overlay2"
                },
                "RootFS": {
                    "Type": "layers",
                    "Layers": [
                        "sha256:13cb14c2acd34e45446a50af25cb05095a17624678dbafbcc9e26086547c1d74",
                        "sha256:94cf29cec5e1e69ddeef0d0e43648b0185e0931920a0b37eda718a5ebe25fa46",
                        "sha256:9fc268fda51763b2c26c12dd6d384ff8c9e2910cfa3f91df4503b24d90e6435e",
                        "sha256:65be02c43d237b5ce3748d20d99930d18019d0c738a4e85becee125a056ddcba",
                        "sha256:496c13efa3189b99bfc99c91eef6167821341b3d32059028db14a7fbeda75fd1",
                        "sha256:0d62495d84f0e2e02818c32458c4d05d01492c22a69be6c6d4b34ffd25acebaa",
                        "sha256:6d6fbf5bcd68dbc0bb4bc0fa8b7eb19fbbf3132730e0a85239b9f8a5abedb27d",
                        "sha256:1013800da1d472d6c2cffbb6c7312c31e5cebc5d39a4b66a2d9f7fd8a9d92edb"
                    ]
                },
                "Metadata": {
                    "LastTagTime": "0001-01-01T00:00:00Z"
                }
            }
        ]
        ```

- 查询镜像的Id信息：`sudo docker inspect -f {{.Id}} 6982b35ff928`
  
    - `sha256:6982b35ff928aa314b5fb9107edaabb5969039be9271222ef1aa5ae116f34830`
- 查看镜像的Metadata信息：`sudo docker inspect -f {{.Metadata.LastTagTime}} 6982b35ff928`
  
    - `0001-01-01 00:00:00 +0000 UTC`
- 同时查看镜像Id和Metadata信息：`sudo docker inspect -f {{.Id}}{{.Metadata.LastTagTime}} 6982b35ff928`
    - `sha256:6982b35ff928aa314b5fb9107edaabb5969039be9271222ef1aa5ae116f34830`
    - 如果需要多字段有自定义分割符的话，需要用引号（英文半角单引号或双引号）把`-f`的值包括起来：
        - 使用空格分割：`sudo docker inspect -f '{{.Id}} {{.Metadata.LastTagTime}}' 6982b35ff928`
            - `sha256:6982b35ff928aa314b5fb9107edaabb5969039be9271222ef1aa5ae116f34830 0001-01-01T00:00:00Z`

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

- `--ip`：设定自定义ip（IPv4）。

- `-p`：表示端口映射，前者是宿主机端口，后者是容器内的映射端口。可以使用多个`-p`做多个端口映射。

- `-e username="ritchie"`: 设置环境变量。

- `--env-file`: 从指定文件读入环境变量。

- `-h`, `--hostname=""`：指定容器的主机名

- `--restart`：容器的重启策略
    - `no`：默认值，表示容器退出时，docker不自动重启容器；
    - `on-failure`：若容器的退出状态非0，则docker自动重启容器，还可以指定重启次数，若超过指定次数未能启动容器则放弃
    - `always`：只要容器退出，则docker将自动重启容器。
    
- `--privileged`：是否让docker应用容器获取宿主机root权限。
    - 使用该参数，container内的root拥有真正的root权限。否则，container内的root只是外部的一个普通用户权限。
    - `--privileged=true`或`--privileged`：表示让docker应用容器获取宿主机root权限。
    - 默认不加此参数，或`--privileged=false`：表示不让docker应用容器获取宿主机root权限。
    
- `--network`：指定使用的网络

    - 查看已经存在的网络：`docker network ls`

        - ```
            NETWORK ID          NAME                DRIVER              SCOPE
            c55394e95167        bridge              bridge              local
            3855964aa18e        host                host                local
            757ba10e775c        none                null                local
            ```

- `--network-alias`：设置当前容器的网络别名，可以代替ip

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
docker cp 本地文件或目录路径 容器名称:容器目录
```

将文件从容器内拷贝出来：

```shell
docker cp 容器名称:容器目录或文件路径 本地目录
```

## 2.5 目录挂载

我们可以在创建容器的时候，将宿主机的目录与容器内的目录进行映射，这样我们就可以通过修改宿主机某个目录的文件从而去影响容器。
创建容器 添加-v参数 后边为   宿主机目录:容器目录，例如：

```shell
docker run -di -v /usr/local/myhtml:/usr/local/myhtml --name=mycentos3 centos:7
```

如果你共享的是多级的目录，可能会出现权限不足的提示。

这是因为CentOS7中的安全模块selinux把权限禁掉了，我们需要添加参数`--privileged=true`来解决挂载的目录没有权限的问题

## 2.6 查看正在运行的容器IP地址

我们可以通过以下命令查看容器运行的各种数据

```shell
docker inspect 容器名称（容器ID） 
```

也可以直接执行下面的命令直接输出IP地址

```shell
docker inspect --format='{{.NetworkSettings.IPAddress}}' 容器名称（或容器ID）
```

## 2.7 删除容器 

删除指定的容器：

```shell
docker rm 容器名称（容器ID）
```

## 2.8 设定容器的重启策略

创建容器的时候设定：`docker run --restart always 3487af26dee9`

更新容器信息的时候设定：`docker update --restart=always [容器名]`或`docker container update --restart=always [容器名]`

## 2.9 容器间的通信：共同加入一个bridge类型的网络

- 查看已经存在的网络：`docker network ls`

    - ```
        NETWORK ID          NAME                DRIVER              SCOPE
        c55394e95167        bridge              bridge              local
        3855964aa18e        host                host                local
        757ba10e775c        none                null                local
        ```

- 创建一个自定义bridge类型的网络test_network：`docker network create -d bridge test_network`

    - 查看已经存在的网络：`docker network ls`

        - ```
            NETWORK ID          NAME                DRIVER              SCOPE
            c55394e95167        bridge              bridge              local
            3855964aa18e        host                host                local
            757ba10e775c        none                null                local
            7e034d10f6c2        test_network        bridge              local
            ```

- 创建容器的时候指定连接的网络和当前容器的网络别名：`sudo docker run -d -p 2181:2181 --name single-zookeeper --network test_network --network-alias s-zoo --restart always 6982b35ff928`

    - 如果容器已创建好但是之前没有指定自己的网络：`docker network connect --alias s-zoo test_network 0a00b15c20e3`

- 然后就可以其他加入到test_network的容器中通过网络别名访问当前容器了。

    - 进入容器：`ping s-zoo`