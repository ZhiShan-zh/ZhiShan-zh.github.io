# Spring Boot 整合Spring Data Redis

# 1 Redis概述

Redis简介、安装和集群搭建参见：[https://www.yuque.com/zhishan/bttt5g/uweqhq](https://www.yuque.com/zhishan/bttt5g/uweqhq)<br />java中使用Redis以及Redis与Spring整合参见：[https://www.yuque.com/zhishan/bttt5g/wmdrk2](https://www.yuque.com/zhishan/bttt5g/wmdrk2)

# 2 入门案例
## 2.1 新建Maven project
![image.png](https://zhishan-zh.github.io/media/spring-data-redis-a434-a96046c6daef.png)

初始pom文件内容：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.zh</groupId>
  <artifactId>redisspringboot</artifactId>
  <version>0.0.1-SNAPSHOT</version>
</project>
```

## 2.2 pom文件引入依赖

```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-parent</artifactId>
  <version>2.2.5.RELEASE</version>
</parent>
<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
  </dependency>
  <dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
  </dependency>
</dependencies>
```

## 2.3 创建实体类
实体类需要实现序列化接口：`java.io.Serializable`
```java
package com.zh.redisspringboot.entity;

import java.io.Serializable;
import java.util.Date;

public class Student implements Serializable{
	private Long id;
	private String name;
	private Long score;
	private Date birthday;
	public Student() {
		super();
	}
	public Student(Long id, String name, Long score, Date birthday) {
		super();
		this.id = id;
		this.name = name;
		this.score = score;
		this.birthday = birthday;
	}
	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public Long getScore() {
		return score;
	}
	public void setScore(Long score) {
		this.score = score;
	}
	public Date getBirthday() {
		return birthday;
	}
	public void setBirthday(Date birthday) {
		this.birthday = birthday;
	}
}
```

## 2.4 创建StudentHandler
注意：这里用key为stu存到redis，但是从终端连接redis查询发现没有这个key，是因为spring data redis对可以进行了序列化，redis库里边的key和stu是由区别的。
```java
package com.zh.redisspringboot.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import com.zh.redisspringboot.entity.Student;

@RestController
public class StudentHandler {
	
	@Autowired
	private RedisTemplate redisTemplate;
	@PostMapping("/set")
	public void set(@RequestBody Student student) {
		redisTemplate.opsForValue().set("stu", student);
	}
	@GetMapping("/get/{key}")
	public Student get(@PathVariable("key") String key) {
		return (Student)redisTemplate.opsForValue().get(key);
	}
	
	@GetMapping("/delete/{key}")
	public boolean delete(@PathVariable("key") String key) {
		redisTemplate.delete(key);
		return redisTemplate.hasKey(key);
	}
}
```

## 2.7 创建配置文件application.yml

```yaml
spring:
  redis:
    database: 0
    host: localhost
    port: 6379
```

## 2.6 创建启动类

```java
package com.zh.redisspringboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
	public static void main(String[] args) throws Exception {
		SpringApplication.run(Application.class, args);
	}
}
```

