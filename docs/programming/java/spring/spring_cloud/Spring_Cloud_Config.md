# Spring Cloud远程配置中心

# 1 远程配置中心简介

![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-183b7fe568e5.png)

# 2 入门案例
## 2.1 创建配置文件
位置：`/zhspringcloud-parent/config/configclient.yml`

位置不一定要在父工程下边，但文件需要上传到github（或自己搭建的私服）

上传到github的方法参见《[git的使用](https://www.yuque.com/zhishan/bttt5g/ozw0b3)》，上传后`configclient.yml`在github的网址为：

```yaml
server:
  port: 8070
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
spring:
  application:
    name: configclient
```

## 2.2 创建配置中心（Config Server）Maven Module
![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-f39e49ae5b86.png)

初始pom文件内容：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.zh</groupId>
    <artifactId>zhspringcloud-parent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
  </parent>
  <artifactId>configserver</artifactId>
</project>
```

## 2.3 pom添加依赖

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-config-server</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>
</dependencies>
```

## 2.4 创建配置文件 application.yml

```yaml
server:
  port: 8888
spring:
  application:
    name: configserver
  cloud:
    config:
      server:
        git:
          uri: https://github.com/ZhiShan-zh/Spring-Cloud-learning
          searchPaths: zhspringcloud-parent/config
          username: root
          password: root
      label: master
eureka:
  client:
    serviceUrl:
      defaultZone: http://localhost:8761/eureka/
```
配置说明：

- `cloud.config.server.git.uri`:github仓库网址
- `cloud.config.server.git.searchPaths`：配置相对与仓库根目录的相对路径，将会在这写目录下寻找配置文件
- `cloud.config.server.git.username`：github的用户名
- `cloud.config.server.git.password`：github的密码
- `cloud.config.label`：Git Repository  的分支

## 2.5 创建启动类

```java
package com.zh.configserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;

@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class,args);
    }
}
```

## 2.6 创建 Config Client
此项目同时是一个服务提供者。
### 2.6.1 新建Maven Module
![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-afc2-eef4076a1c9f.png)

初始pom文件内容：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.zh</groupId>
    <artifactId>zhspringcloud-parent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
  </parent>
  <artifactId>configclient</artifactId>
</project>
```

### 2.6.2 pom引入依赖

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>

  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>
</dependencies>
```

### 2.6.3 创建 bootstrap.yml
注意这里的配置文件不是`application.yml`

```yaml
spring:
  cloud:
    config:
      name: configclient
      label: master
      discovery:
        enabled: true
        service-id: configserver
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
```

**配置解释：**

- `spring.cloud.config.name`：当前服务注册在 Eureka Server 上的名称，与远程仓库的配置文件名对应。
- `spring.cloud.config.discovery.enabled`：是否开启 Config 服务发现支持。
- `spring.cloud.config.discovery.service-id`：配置中心在 Eureka Server 上注册的名称。
- `spring.cloud.config.label` ：Git Repository  的分支。

### 2.6.4 创建启动类

```java
package com.zh.configclient;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ConfigClientApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigClientApplication.class,args);
    }
}
```

### 2.6.5 创建Handler，以读取配置信息

```java
package com.zh.configclient.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/hello")
public class HelloHandler {

    @Value("${server.port}")
    private String port;

    @GetMapping("/index")
    public String index(){
        return this.port;
    }
}
```

## 2.7 测试远程配置中心

1. 依次启动注册中心（eurekaserver）、远程配置中心（configserver）、远程配置中心客户端（configclient）。
1. 访问注册中心（[http://localhost:8761/](http://localhost:8761/)），查看服务注册情况。
   1. 发现远程配置中心（configserver）和远程配置中心客户端（configclient）都没有注册到注册中心（eurekaserver）。
   1. ![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-9585-dce9dd4562d0.png)
3. 访问远程配置中心客户端（configclient）的接口（[http://localhost:8070/hello/index](http://localhost:8070/native/index)）。
   1. 这里的端口号`https://github.com/ZhiShan-zh/Spring-Cloud-learning/blob/master/zhspringcloud-parent/config/configclient.yml`配置的端口号
   1. ![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-b723-773679fb6d8c.png)
   1. ![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-ab06-f30781b072a9.png)





