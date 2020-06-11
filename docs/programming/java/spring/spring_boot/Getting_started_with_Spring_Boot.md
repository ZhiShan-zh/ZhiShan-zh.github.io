# Spring Boot入门

# 1 Spring Boot简介
## 1.1 什么是Spring Boot
Spring Boot 是一个快速开发框架，可以迅速搭建出一套基于 Spring 框架体系的应用，是 Spring Cloud 的基础。

Spring Boot 开启了各种自动装配，从而简化代码的开发，不需要编写各种配置文件，只需要引入相关依赖就可以迅速搭建一个应用。

Spring Boot的设计目的是用来简化Spring应用的初始搭建以及开发过程，该框架使用了特定的方式来进行配置，从而使开发人员不再需要定义样板化的配置。

Spring Boot默认配置了很多框架的使用方式，就像Maven整合了所有的jar包，Spring Boot整合了所有的框架，通过少量的代码就能创建一个独立的、产品级别的Spring应用。

简单理解Spring Boot是一个集成了Spring各种组件的快速开发框架。
![image.png](https://zhishan-zh.github.io/media/1583722936665-daa1a9c7-8852-45b0-b274-9b065b4bbed6.png)

## 1.2 Spring Boot特点

1. 不需要 web.xml
1. 不需要 springmvc.xml
1. 不需要 tomcat，Spring Boot 内嵌了 tomcat
1. 不需要配置 JSON 解析，支持 REST 架构
1. 个性化配置非常简单

详细特点：

-  使用Spring项目引导页面可以在几秒构建一个项目
- 方便对外输出各种形式的服务，如REST API、WebSocket、Web、Streaming、Tasks
- 非常简介的安全策略集成
- 支持关系型数据库和非关系型数据库
- 支持运行期内嵌容器，如Tomcat、Jetty
- 自动管理依赖

## 1.3 SpringBoot与微服务

- Spring Boot的一系列特性有助于实现微服务架构的落地，从目前众多的技术栈对比来看它是Java领域微服务架构最优落地技术，没有之一。
- Spring Cloud依赖与Spring Boot。
- Spring Boot专注于快速开发个体微服务，Spring Cloud是关注全局的微服务协调治理框架。

# 2 入门案例
## 2.1 新建Maven Project，打包方式jar
![image.png](https://zhishan-zh.github.io/media/1583719653571-63d4db13-4b96-43a9-a2ba-343f8875776b.png)

初始pom文件内容：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.zh</groupId>
  <artifactId>beginspringboot</artifactId>
  <version>0.0.1-SNAPSHOT</version>
</project>
```

## 2.2 pom文件引入依赖

```xml
<!-- 继承父包 -->
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>2.2.5.RELEASE</version>
</parent>

<dependencies>
  <!-- web启动jar -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.6</version>
    <scope>provided</scope>
  </dependency>
</dependencies>
```

## 2.3 创建实体类

```java
package com.zh.beginspringboot.entity;

import lombok.Data;

@Data
public class Student {
    private long id;
    private String name;
    private int age;
}
```

## 2.4 创建StudentRepository

```java
package com.zh.beginspringboot.repository;

import java.util.Collection;

import com.zh.beginspringboot.entity.Student;

public interface StudentRepository {
	public Collection<Student> findAll();
    public Student findById(long id);
    public void saveOrUpdate(Student student);
    public void deleteById(long id);
}
```

## 2.5 创建StudentRepositoryImpl

```java
package com.zh.beginspringboot.repository.impl;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import org.springframework.stereotype.Repository;
import com.zh.beginspringboot.entity.Student;
import com.zh.beginspringboot.repository.StudentRepository;

@Repository
public class StudentRepositoryImpl implements StudentRepository {

    private static Map<Long,Student> studentMap;

    static{
        studentMap = new HashMap<>();
        studentMap.put(1L,new Student(1L,"张三",22));
        studentMap.put(2L,new Student(2L,"李四",23));
        studentMap.put(3L,new Student(3L,"王五",24));
    }

    @Override
    public Collection<Student> findAll() {
        return studentMap.values();
    }

    @Override
    public Student findById(long id) {
        return studentMap.get(id);
    }

    @Override
    public void saveOrUpdate(Student student) {
        studentMap.put(student.getId(),student);
    }

    @Override
    public void deleteById(long id) {
        studentMap.remove(id);
    }
}
```

## 2.6 创建StudentHandler

```java
package com.zh.beginspringboot.controller;

import java.util.Collection;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.zh.beginspringboot.entity.Student;
import com.zh.beginspringboot.repository.StudentRepository;

@RestController
@RequestMapping("/student")
public class StudentHandler {

    @Autowired
    private StudentRepository studentRepository;

    @GetMapping("/findAll")
    public Collection<Student> findAll(){
        return studentRepository.findAll();
    }

    @GetMapping("/findById/{id}")
    public Student findById(@PathVariable("id") long id){
        return studentRepository.findById(id);
    }

    @PostMapping("/save")
    public void save(@RequestBody Student student){
        studentRepository.saveOrUpdate(student);
    }

    @PutMapping("/update")
    public void update(@RequestBody Student student){
        studentRepository.saveOrUpdate(student);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        studentRepository.deleteById(id);
    }
}
```

## 2.7 创建启动类

```java
package com.zh.beginspringboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
```
注解说明：

- `@SpringBootApplication`  表示当前类是 Spring Boot 的入口，Application 类的存放位置必须是其他相关业务类的存放位置的父级。

## 2.8 创建配置文件application.yml
配置文件位置：`/beginspringboot/src/main/resources/application.yml`
如果进行测试，可以创建这个配置文件，默认的端口号是8080.

```yaml
server:
  port: 9090
```

## 2.9 测试

1. 启动beginspringboot项目。
1. 访问测试接口（[http://localhost:9090/student/findAll](http://localhost:9090/student/findAll)）。
1. ![image.png](https://zhishan-zh.github.io/media/1583721561763-d34f0408-5843-4be6-a8ce-9d709c766f2d.png)
