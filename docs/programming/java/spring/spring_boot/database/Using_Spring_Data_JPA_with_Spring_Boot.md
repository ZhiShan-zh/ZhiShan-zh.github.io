# Spring Boot整合Spring Data JPA

# 1 Spring Data JPA简介
JPA Hibernate框架就是一个JPA的实现。

Spring Data JPA不是对JPA规范的具体实现，本身是一个抽象层。

# 2 入门案例
## 2.1 新建Maven project
![image.png](https://zhishan-zh.github.io/media/1583752728693-f5117f3e-adf8-4004-939d-d2f2027ae9dd.png)
初始pom文件内容：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.zh</groupId>
  <artifactId>jpaspringboot</artifactId>
  <version>0.0.1-SNAPSHOT</version>
</project>
```


## 2.2 pom加入依赖


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
    <artifactId>spring-boot-starter-data-jpa</artifactId>
  </dependency>

  <dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.15</version>
  </dependency>
</dependencies>
```


## 2.3 创建实体类


```java
package com.zh.jpaspringboot.entity;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class Student {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	@Column
	private String name;
	@Column
	private Double score;
	@Column
	private Date birthday;
	public Student() {
		super();
	}
	public Student(Long id, String name, Double score, Date birthday) {
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
	public Double getScore() {
		return score;
	}
	public void setScore(Double score) {
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
注解说明：

- `@Entity`：映射表
- `@Id`：声明主键
- `@GeneratedValue`：声明生成策略
- `@Column`：声明非主键字段

## 2.4 创建StudentRepository接口
需要继承`org.springframework.data.jpa.repository.JpaRepository`，`JpaRepository<Student, Long>`需要两个泛型

- 第一个泛型是实体类类名，比如这里的Student；
- 第二个泛型是实体类里边主键的类型，比如这里Student中主键id的类型为Long。

这样常用的增删改查已经继承，不需要自己单独实现。

这里可以定义一些符合命名规范的方法，且不需要自己实现。

```java
package com.zh.jpaspringboot.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import com.zh.jpaspringboot.entity.Student;

public interface StudentRepository extends JpaRepository<Student, Long>, JpaSpecificationExecutor<Student>{
}
```

- JpaRepository提供了基本的增删改查
- JpaSpecificationExecutor用于做复杂的条件查询

## 2.5 创建StudentHandler，注入StudentRepository


```java
package com.zh.jpaspringboot.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.zh.jpaspringboot.entity.Student;
import com.zh.jpaspringboot.repository.StudentRepository;

@RestController
public class StudentHandler {

	@Autowired
	private StudentRepository studentRepository;
	
	@GetMapping
	public List<Student> findAll(){
		return studentRepository.findAll();
	}
	
	@GetMapping("/findById/{id}")
	public Student findById(@PathVariable("id") Long id) {
		return studentRepository.findById(id).get();
	}
	
	@PostMapping("/save")
	public void save(@RequestBody Student student) {
		studentRepository.save(student);
	}
	
	@PutMapping("/update")
	public void update(@RequestBody Student student) {
		studentRepository.save(student);
	}
	
	@DeleteMapping("/deleteById/{id}")
	public void deleteById(@PathVariable("id") Long id) {
		studentRepository.deleteById(id);
	}
}
```

注：

- `@GetMapping` 是一个组合注解，相当与 `@RequestMapping(method="get")` 。
    - 类似的注解还有 `@PostMapping` ， `@PutMapping` ， `@DeleteMapping` 

## 2.6 创建配置文件application.yml


```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mytest?useUnicode=true&characterEncoding=UTF-8
    username: root
    password: 1106
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    properties:
      hibernate: 
        format_sql: true
```

配置说明：

- `spring.jpa.show-sql`：是否打印sql语句
- `spring.jpa.properties.hibernate.format_sql`：是否格式化sql语句

## 2.7 创建启动类


```java
package com.zh.jpaspringboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
	public static void main(String[] args) throws Exception {
		SpringApplication.run(Application.class, args);
	}
}
```


