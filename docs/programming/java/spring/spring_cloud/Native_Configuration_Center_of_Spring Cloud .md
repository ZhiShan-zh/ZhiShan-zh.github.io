# Spring Cloud 本地配置中心

# 1 Spring Cloud配置中心简介
Spring Cloud Config，通过服务端可以为多个客户端提供配置服务。Spring Cloud Config 可以将配置文件存储在本地，也可以将配置文件存储在远程 Git 仓库，创建 Config Server，通过它管理所有的配置文件。<br />可以不重启微服务的情况下修改配置文件。

# 2 入门案例
## 2.1 创建Maven Module
![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-1583666188166-25db98d3.png)

初始pom文件内容：
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.zh</groupId>
    <artifactId>zhspringcloud-parent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
  </parent>
  <artifactId>nativeconfigserver</artifactId>
</project>
```

## 2.2 pom引入依赖
```xml
<dependencies>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-config-server</artifactId>
			<version>2.2.2.RELEASE</version>
		</dependency>
```

## 2.3 创建配置文件application.yml
```yaml
server:
  port: 8762
spring:
  application:
    name: nativeconfigserver
  profiles:
    active: native
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/shared
```
**注解说明:**

- `profiles.active` ：配置文件的获取方式
- `cloud.config.server.native.search-locations` ：本地配置文件存放的路径

## 2.4 resources 路径下创建 shared 文件夹，并在此路径下创建 configclient-dev.yml
```yaml
server:
  port: 8070
foo: foo version 1
```
配置说明：

- `foo`：版本

## 2.5 创建启动类
```java
package com.zh.nativeconfigserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;

@SpringBootApplication
@EnableConfigServer
public class NativeConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(NativeConfigServerApplication.class,args);
    }
}

```
**注解说明:**

- `@EnableConfigServer` ：声明配置中心。

## 2.6 创建客户端读取本地配置中心的配置文件
### 2.6.1 创建Maven Module
![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-1e8778338037.png)

初始pom文件内容：
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.zh</groupId>
    <artifactId>zhspringcloud-parent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
  </parent>
  <artifactId>nativeconfigclient</artifactId>
</project>
```

### 2.6.2 pom文件引入依赖

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>
</dependencies>
```


### 2.6.3 创建 bootstrap.yml，配置读取本地配置中心的相关信息
位置：/nativeconfigclient/src/main/resources/bootstrap.yml
```yaml
spring:
  application:
    name: configclient
  profiles:
    active: dev
  cloud:
    config:
      uri: http://localhost:8762
      fail-fast: true
```
注解说明:

- `cloud.config.uri` ：本地配置中心 Config Server 的访问路径
- `cloud.config.fail-fase` ：设置客户端优先判断 Config Server 获取是否正常。
- 通过 `spring.application.name`  结合 `spring.profiles.active` 拼接目标配置文件名，configclient-dev.yml，去 Config Server 中查找该文件。

### 2.6.4 创建启动类

```java
package com.zh.nativeconfigclient;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class NativeConfigClientApplication {
    public static void main(String[] args) {
        SpringApplication.run(NativeConfigClientApplication.class,args);
    }
}
```

### 2.6.5 创建Handler读取配置信息

```java
package com.zh.nativeconfigclient.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/native")
public class NativeConfigHandler {

    @Value("${server.port}")
    private String port;

    @Value("${foo}")
    private String foo;

    @GetMapping("/index")
    public String index(){
        return this.port+"-"+this.foo;
    }
}
```

## 2.7 测试本地配置中心

1. 依次启动注册中心（eurekaserver）、本地配置中心（nativeconfigserver)、本地配置中心客户端（nativeconfigclient）。
1. 访问注册中心（[http://localhost:8761/](http://localhost:8761/)），查看服务注册情况。
   1. 发现本地配置中心（nativeconfigserver)和本地配置中心客户端（nativeconfigclient）都没有注册到注册中心（eurekaserver）。
   1. ![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-a25b582c5d5b.png)
3. 访问本地配置中心客户端（nativeconfigclient）的接口（[http://localhost:8070/native/index](http://localhost:8070/native/index)）。
   1. 这里的端口号8070是本地配置中心（nativeconfigserver)中`/nativeconfigserver/src/main/resources/shared/configclient-dev.yml`配置的端口号。
   1. ![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-8830-dafe46797df6.png)

