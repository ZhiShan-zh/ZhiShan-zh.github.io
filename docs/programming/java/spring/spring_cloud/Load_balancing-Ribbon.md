# 客户端负载均衡 Ribbon

# 1 Ribbon概述
Spring Cloud Ribbon是一个负载均衡解决方案，Ribbon 是 Netflix 发布的负载均衡器，Spring Cloud Ribbon 是基于 Netflix Ribbon 实现的，是一个用于对 HTTP 请求进行控制的客户端负载均衡。

在注册中心对 Ribbon 进行注册之后，Ribbon 就可以基于某种负载均衡算法，如轮询、随机、加权轮询、加权随机等自动帮助服务消费者调用接口，开发者也可以根据具体需求自定义 Ribbon 负载均衡算法。实际开发中，Spring Cloud Ribbon 需要结合 Spring Cloud Eureka 来使用，Eureka Server 提供所有可以调用的服务提供者列表，Ribbon 基于特定的负载均衡算法从这些服务提供者中选择要调用的具体实例。
![image.png](https://zhishan-zh.github.io/media/1583651797304-c9a60d87-0e59-4fe1-b60a-1397f5500823.png)

我们通常所说的负载均衡都指的是服务端负载均衡，而Ribbon是一个客户端的负载均衡。客户端负载均衡和服务端负载均衡最大的不同点在于服务清单所存储的位置。在客户端负载均衡中，所有客户端节点都维护着自己要访问的服务端清单，而这些服务端端清单来自于服务注册中心，比如Eureka服务端。同服务端负载均衡的架构类似，在客户端负载均衡中也需要心跳去维护服务端清单的健康性，默认会创建针对各个服务治理框架的Ribbon自动化整合配置，比如Eureka中的`org.springframework.cloud.netflix.ribbon.eureka.RibbonEurekaAutoConfiguration`，Consul中的`org.springframework.cloud.consul.discovery.RibbonConsulAutoConfiguration`。

通过Spring Cloud Ribbon的封装，我们在Spring Cloud微服务架构中使用客户端负载均衡调用非常简单，只需要如下两步：

- 服务提供者启动多个服务实例并注册到一个注册中心或是多个相关联的服务注册中心。

- 服务消费者通过调用被`@LoadBalanced`注解修饰过的RestTemplate来实现面向服务的接口调用。



# 2 入门案例
Ribbon项目不提供服务。
## 2.1 创建Maven Module
![image.png](https://zhishan-zh.github.io/media/1583651919174-8b995c56-41da-47be-8929-a798bb5f4d0d.png)

初始pom文件内容：
```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.zh</groupId>
    <artifactId>zhspringcloud-parent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
  </parent>
  <artifactId>ribbon</artifactId>
</project>
```

## 2.2 pom中添加相关依赖
因为ribbon需要注册到注册中心EurekaServer，所以需要添加 `spring-cloud-starter-netflix-eureka-client` :
```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>
</dependencies>
```

## 2.3 创建配置文件 application.yml
```yaml
server:
  port: 8040
spring:
  application:
    name: ribbon
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
```

## 2.4 创建启动类
因为所有请求都使用RestTemplate访问服务提供者的请求，所以网关中也需要引入RestTemplage。

```java
package com.zh.ribbon;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class RibbonApplication {
	public static void main(String[] args) {
		SpringApplication.run(RibbonApplication.class, args);
	}
	
	@Bean
	@LoadBalanced
	public RestTemplate restTemplate() {
		return new RestTemplate();
	}
}
```

**注解说明：**

- `@LoadBalanced` ：声明一个基于 Ribbon 的负载均衡。

## 2.5 Handler
这里的请求ip和端口号可以利用服务提供者配置的服务名称替代，比如这里的provider.
```java
package com.zh.ribbon.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.zh.ribbon.entity.Student;

import java.util.Collection;

@RestController
@RequestMapping("/ribbon")
public class RibbonHandler {
    @Autowired
    private RestTemplate restTemplate;

    @GetMapping("/findAll")
    public Collection<Student> findAll(){
        return restTemplate.getForObject("http://provider/student/findAll",Collection.class);
    }

    @GetMapping("/index")
    public String index(){
        return restTemplate.getForObject("http://provider/student/index",String.class);
    }
}

```

## 2.6 测试负载均衡

1. 启动注册中心（eurekaserver）、以不同端口的方法（方法参见：《[服务网关Zuul**-**测试Zuul负载均衡](https://www.yuque.com/zhishan/bttt5g/ndnlvu#482Q4)》）启动两个服务提供者（eurekaClient）。
1. 访问注册中心（[http://localhost:8761/](http://localhost:8761/)），查看服务注册情况。
  1. ![image.png](https://zhishan-zh.github.io/media/1583653653811-6affd61f-7545-4f4d-9bba-38260c04faca.png)
3. 启动负载均衡ribbon。
3. 访问注册中心（[http://localhost:8761/](http://localhost:8761/)），查看服务注册情况。
  1. ![image.png](https://zhishan-zh.github.io/media/1583653850172-a7f3003e-a0d7-43d2-afa3-c7fc0e4072ba.png)
5. 访问ribbon接口（[http://localhost:8040/ribbon/findAll](http://localhost:8040/ribbon/findAll)）
  1. ![image.png](https://zhishan-zh.github.io/media/1583653931537-ed8ad58b-8da1-4ff7-bb33-1b0205003ca2.png)
  1. 其实此时已经时间负载均衡，只是看不到效果。
6. 访问ribbon中index服务（[http://localhost:8040/ribbon/index](http://localhost:8040/ribbon/index)）查看负载均衡效果
  1. ![image.png](https://zhishan-zh.github.io/media/1583654009663-35e551ce-f6b0-401d-bec6-2475555227c6.png)
  1. ![image.png](https://zhishan-zh.github.io/media/1583654030440-8888a8e1-1bb2-4c23-b32f-b189a7856335.png)

