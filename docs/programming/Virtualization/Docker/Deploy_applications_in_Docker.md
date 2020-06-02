# 在Docker中应用部署

# 1 MySQL部署

（1）拉取mysql镜像

```shell
docker pull centos/mysql-57-centos7
```

（2）创建容器

```shell
docker run -di --name=my_mysql -p 33306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql
```

- `-p`：代表端口映射，格式为`宿主机映射端口:容器运行端口`

- `-e`：代表添加环境变量`MYSQL_ROOT_PASSWORD`是root用户的登陆密码

（3）远程登录mysql

连接宿主机的IP，指定端口为33306。

 # 2 tomcat部署

（1）拉取镜像

```shell
docker pull tomcat:7-jre7
```

（2）创建容器

创建容器`-p`表示地址映射

```shell
docker run -di --name=mytomcat -p 9000:8080 
-v /usr/local/webapps:/usr/local/tomcat/webapps tomcat:7-jre7
```

# 3 Nginx部署 

（1）拉取镜像	

```shell
docker pull nginx
```

（2）创建Nginx容器

```shell
docker run -di --name=mynginx -p 80:80 nginx
```

# 4 Redis部署

（1）拉取镜像

```shell
docker pull redis
```

（2）创建容器

```shell
docker run -di --name=myredis -p 6379:6379 redis
```
