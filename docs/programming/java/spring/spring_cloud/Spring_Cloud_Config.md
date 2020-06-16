# Spring Cloud Config

# 1 简介
Spring Cloud Config项目是一个解决分布式系统的配置管理方案。它包含了Client和Server两个部分，server提供配置文件的存储、以接口的形式将配置文件的内容提供出去，client通过接口获取数据、并依据此数据初始化自己的应用。

Spring Cloud Config通过服务端可以为多个客户端提供配置服务。Spring Cloud Config 可以将配置文件存储在本地，也可以将配置文件存储在远程 Git 仓库，创建 Config Server，通过它管理所有的配置文件。

可以不重启微服务的情况下修改配置文件。

**Spring Cloud Config服务端特性**：

- 以HTTP为外部配置提供基于资源的API（键值对，或者等价的YAML内容）
- 属性值的加密和解密（对称加密和非对称加密）

- 通过使用`@EnableConfigServer`在Spring Boot应用中非常简单的嵌入。

**Config客户端的特性（特指Spring应用）**

- 绑定Config服务端，并使用远程的属性源初始化Spring环境。
- 属性值的加密和解密（对称加密和非对称加密）

# 2 入门案例——本地配置中心
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

# 3 入门案例——远程配置中心

![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-183b7fe568e5.png)

## 3.1 创建配置文件

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

## 3.2 创建配置中心（Config Server）Maven Module

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

## 3.3 pom添加依赖

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-config-server</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>
</dependencies>
```

## 3.4 创建配置文件 application.yml

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
- `cloud.config.label`：Git Repository  的分支

## 3.5 创建启动类

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

## 3.6 创建 Config Client

此项目同时是一个服务提供者。

### 3.6.1 新建Maven Module

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

### 3.6.2 pom引入依赖

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

### 3.6.3 创建 bootstrap.yml

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
- `spring.cloud.config.label` ：Git Repository  的分支。

### 3.6.4 创建启动类

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

### 3.6.5 创建Handler，以读取配置信息

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

## 3.7 测试远程配置中心

1. 依次启动注册中心（eurekaserver）、远程配置中心（configserver）、远程配置中心客户端（configclient）。
2. 访问注册中心（[http://localhost:8761/](http://localhost:8761/)），查看服务注册情况。
    1. 发现远程配置中心（configserver）和远程配置中心客户端（configclient）都没有注册到注册中心（eurekaserver）。
    1. ![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-9585-dce9dd4562d0.png)
3. 访问远程配置中心客户端（configclient）的接口（[http://localhost:8070/hello/index](http://localhost:8070/native/index)）。
    1. 这里的端口号`https://github.com/ZhiShan-zh/Spring-Cloud-learning/blob/master/zhspringcloud-parent/config/configclient.yml`配置的端口号
    1. ![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-b723-773679fb6d8c.png)
    1. ![image.png](https://zhishan-zh.github.io/media/spring-cloud-config-ab06-f30781b072a9.png)

# 4 配置中心高可用

如果客户端是直接调用配置中心的server端来获取配置文件信息会存在了一个问题，客户端和服务端的耦合性太高，如果server端要做集群，客户端只能通过原始的方式来路由，server端改变IP地址的时候，客户端也需要修改配置，不符合springcloud服务治理的理念。springcloud提供了这样的解决方案，我们只需要将server端当做一个服务注册到eureka中，client端去eureka中去获取配置中心server端的服务既可。

## 4.1 从注册中心获取配置中心的地址

### 4.1.1 添加依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-config</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-eureka</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### 4.1.2 配置文件修改

```yaml
server:
	port: 9002
eureka:
    client:
        serviceUrl:
            defaultZone: http://localhost:8000/eureka/ ## 注册中心eurka地址
spring:
    cloud:
        config:
            name: product
            profile: dev
            label: master
            uri: http://localhost:8080
            discovery:
                enabled: true #从eureka中获取配置中心信息
                service-id: config-server
```

## 4.2 注册中心高可用

可以启动两个注册中心实例，两个注册中心实例的服务名称一样。

# 5 手动刷新服务配置

我们已经在客户端取到了配置中心的值，但当我们修改GitHub上面的值时，服务端（Config Server）能实时获取最新的值，但客户端（Config Client）读的是缓存，无法实时获取最新值。SpringCloud已经为我们解决了这个问题，那就是客户端使用post去触发refresh，获取最新数据，需要依赖`springboot-starter-actuator`。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

对应的controller类加上`@RefreshScope`：

```java
@RefreshScope
@RestController
public class TestController{
    @Value("${myvalue}")
    private String productValue;
    
    // 访问首页
    @GetMapping("/index")
    public String index(){
    	return "Hello Spring Boot！productValue：" + productValue;
    }
}
```

修改Spring Cloud Config客户端的配置文件中暴露`/refresh`：

```yaml
server:
	port: 9006
myvalue: first_value
management: # 改变将那个端点暴露出来，可以使用特定的技术include和exclude属性
    endpoints:
        web:
            exposure:
                include: /refresh # 列出暴露的端点，多个以英文逗号分割
```

单独引入 `spring-boot-starter-actuator`或者`spring-cloud-starter-config`（spring cloud config的客户端） 是不会暴露`/refresh`端点的，两者同时引入之后才能暴露`/refresh`端点。

- spring cloud config客户端结合actuator还可以刷新本地的配置文件到内存中。

测试：

1. 重启Spring Cloud Config客户端，访问测试接口`http://localhost9006/index`，打印数据为：`Hello Spring Boot！productValue：first_value`；

2. 修改配置文件中的myvalue的值为：second_value，然后使用POST请求方法`/refresh`（`http://localhost9006/actuator/refresh`）端点，然后访问测试接口`http://localhost9006/index`，打印数据为：`Hello Spring Boot！productValue：second_value`。

# 6 消息总线整合配置中心实现自动刷新配置

## 6.1 概述

在微服务架构中，通常会使用轻量级的消息代理来构建一个共用的消息主题来连接各个微服务实例，它广播的消息会被所有在注册中心的微服务实例监听和消费，也称消息总线。

SpringCloud中也有对应的解决方案，SpringCloud Bus 将分布式的节点用轻量的消息代理连接起来，可以很容易搭建消息总线，配合SpringCloud config 实现微服务应用配置信息的动态更新。

## 6.2 消息总线实现配置信息的动态更新的方式

### 6.2.1 某个微服务承担配置刷新的职责

![](https://zhishan-zh.github.io/media/spring_cloud_bus_20200616002944.png)

1. 提交配置并发送POST请求调用客户端A的`/bus/refresh`接口；
2. 客户端A收到请求从配置中心Server端更新配置并且发送给Spring Cloud Bus消息总线；
3. Spring Cloud Bus接收消息并通知给其他连线在总线上的客户端，所有总线上的客户端均能接收到消息；
4. 其他客户端接收到消息，请求配置中心端获取最新配置；
5. 全部客户端均获取到最新的配置。

**此方案的问题**：打破微服务的单一原则。微服务本身是业务模块，本不应该承担配置刷新的职责。

**实现思路**：

1. 在配置中心Client端上暴露消息总线的接口`/bus-refresh`；
    - 需要确定是否不需要在配置中心Server端上暴露消息总线接口？
2. 在配置中心客户端需要使用配置的类上加上`@RefreshScope`注解。
3. 在配置更新的时候发送POST请求，访问消息总线接口`/bus-refresh`。

### 6.2.2 配置中心Server端承担起配置刷新的职责

![](https://zhishan-zh.github.io/media/spring_cloud_bus_20200616004359.png)

1. 提交配置发送POST请求调用配置中心Server端的`/bus-refresh`接口；
2. 配置中心Server端收到请求后发送给Spring Cloud Bus消息总线；
3. Spring Cloud Bus接收消息并通知连线在总线上的客户端，所有总线上的客户端均能接收到消息。
4. 客户端接收到消息，请求配置中心端获取最新配置。
5. 全部客户端均获取到最新的配置。

**实现思路**：

1. 在配置中心Server端和Client端上暴露消息总线的接口`/bus-refresh`；
2. 在配置中心客户端需要使用配置的类上加上`@RefreshScope`注解。
3. 在配置更新的时候发送POST请求，访问配置中心Server端消息总线接口`/bus-refresh`。

