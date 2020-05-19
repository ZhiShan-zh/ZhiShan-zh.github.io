# Hystrix 容错机制&amp;数据监控

# 1 Hystrix 容错机制介绍
## 1.1 什么是容错机制
在不改变各个微服务调用关系的前提下，针对错误情况进行预先处理。

## 1.2 设计原则

1. **服务隔离机制**：防止某个服务提供者出现问题，而影响到整个服务的运行。
1. **服务降级机制**：服务出现问题的时候，向服务访问者返回fallback
1. **熔断机制**：当服务消费者请求失败率达到某个特定的数值的时候，会迅速启动熔断机制对错误进行修复
1. **提供实时的监控和报警功能**：保证能迅速地修复错误
1. **提供实时的配置修改功能**：保证能迅速地修复错误

## 1.3 数据监控功能
Hystrix 数据监控需要结合 Spring Boot Actuator 来使用，Actuator 提供了对服务的健康进监控、数据统计，可以通过 hystrix.stream 节点获取监控的请求数据，提供了可视化的监控界面。

# 2 入门案例
## 2.1 创建Maven Module
![image.png](https://zhishan-zh.github.io/media/1583661256880-6f61a7f3-d33b-4a58-8f49-6863c4b8ca6e.png)

初始pom内容：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.zh</groupId>
    <artifactId>zhspringcloud-parent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
  </parent>
  <artifactId>hystrix</artifactId>
</project>
```
## 2.2 pom添加相关依赖

```xml
<dependencies>
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>

  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>

  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
    <version>2.2.5.RELEASE</version>
  </dependency>

  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>
	<!-- 可视化监控组件 -->
  <dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix-dashboard</artifactId>
    <version>2.2.2.RELEASE</version>
  </dependency>
</dependencies>
```

## 2.4 创建配置文件 application.yml
```yaml
server:
  port: 8060
spring:
  application:
    name: hystrix
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
  instance:
    prefer-ip-address: true
feign:
  hystrix:
    enabled: true
management:
  endpoints:
    web:
      exposure:
        include: 'hystrix.stream'
```
配置说明：

- `management.endpoints.web.exposure.include` :配置监控节点

## 2.5 创建启动类

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.circuitbreaker.EnableCircuitBreaker;
import org.springframework.cloud.netflix.hystrix.dashboard.EnableHystrixDashboard;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
@EnableCircuitBreaker
@EnableHystrixDashboard
public class HystrixApplication {
    public static void main(String[] args) {
        SpringApplication.run(HystrixApplication.class,args);
    }
}
```
**注解说明：**

- `@EnableCircuitBreaker` ：声明启用数据监控
- `@EnableHystrixDashboard` ：声明启用可视化数据监控

## 2.6 创建实体类
没有实体类也可以访问，建立实体类只是为了接收数据。
```java
package com.zh.hystrix.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Student {
	private long id;
    private String name;
    private int age;   
}
```

## 2.7 创建声明式接口
```java
package com.zh.hystrix.feign;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import com.zh.hystrix.entity.Student;
import java.util.Collection;

@FeignClient(value = "provider")
public interface FeignProviderClient {
    @GetMapping("/student/findAll")
    public Collection<Student> findAll();

    @GetMapping("/student/index")
    public String index();
}

```

## 2.8 创建Handler
```java
package com.zh.hystrix.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.zh.hystrix.entity.Student;
import com.zh.hystrix.feign.FeignProviderClient;

import java.util.Collection;

@RestController
@RequestMapping("/hystrix")
public class HystrixHandler {
    @Autowired
    private FeignProviderClient feignProviderClient;

    @GetMapping("/findAll")
    public Collection<Student> findAll(){
        return feignProviderClient.findAll();
    }

    @GetMapping("/index")
    public String index(){
        return feignProviderClient.index();
    }
}
```

## 2.9 测试Hystrix数据监控

1. 依次启动注册中心（eurekaserver）、服务提供者（eurekaClient）、数据监控（hystrix）。
1. 访问注册中心（[http://localhost:8761/](http://localhost:8761/)），查看服务注册情况。
  1. ![image.png](https://zhishan-zh.github.io/media/1583664274390-07d07ebf-fbf6-4a15-9b8f-0f6c96b32c13.png)
3. 访问Hystrix数据监控中心（[http://localhost:8060/actuator/hystrix.stream](http://localhost:8060/actuator/hystrix.stream)）。
  1. ![image.png](https://zhishan-zh.github.io/media/1583664502972-963e8224-2cb6-4b4b-8f4c-b775f6cbc222.png)
  1. 数据监控中心是一直在刷新。
4. 调用监控中心的服务接口（[http://localhost:8060/actuator/hystrix.stream](http://localhost:8060/actuator/hystrix.stream)）
  1. ![image.png](https://zhishan-zh.github.io/media/1583664629552-c9111ff5-9878-4096-a02c-18efbb93b7e6.png)
5. 再次查看数据监控中心（[http://localhost:8060/actuator/hystrix.stream](http://localhost:8060/actuator/hystrix.stream)），看网页后边。
  1. ![image.png](https://zhishan-zh.github.io/media/1583664789780-9ee92929-fa78-4efa-8b59-30dbc091a268.png)
  1. 这个监控中心是以json字符串展示的。
6. 访问Hystrix可视化数据监控中心（[http://localhost:8060/hystrix](http://localhost:8060/hystrix)）。
  1. ![image.png](https://zhishan-zh.github.io/media/1583664961153-000f0832-a2e0-4512-8f54-eb6e975f24a0.png)
7. 然后在搜索栏中输入数据监控中心的网址（[http://localhost:8060/actuator/hystrix.stream](http://localhost:8060/actuator/hystrix.stream)），并在Title栏中写入一个监控数据的名字，还可以
  1. ![image.png](https://zhishan-zh.github.io/media/1583665252845-90232ff4-924d-40ae-a600-c50008494bb7.png)
  1. ![image.png](https://zhishan-zh.github.io/media/1583665375971-cfb78be7-278e-4710-8cbf-bd63997cc8bd.png)
