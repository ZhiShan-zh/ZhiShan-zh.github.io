# Spring Boot 整合 JSP

# 1 新建Maven Project
模板选择`org.apache.maven.archetypes:maven-archetype-webapp`.
![image.png](https://zhishan-zh.github.io/media/1583722275037-91bef1ba-c09a-435f-a679-52a38666ec6e.png)
![image.png](https://zhishan-zh.github.io/media/1583722312945-61f8cb5a-c963-497b-807c-1ced86129ab7.png)

初始pom文件内容：

```xml
<?xml version="1.0" encoding="UTF-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.zh</groupId>
  <artifactId>jspspringboot</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <packaging>war</packaging>

  <name>jspspringboot Maven Webapp</name>
  <!-- FIXME change it to the project's website -->
  <url>http://www.example.com</url>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.7</maven.compiler.source>
    <maven.compiler.target>1.7</maven.compiler.target>
  </properties>

  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.11</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <finalName>jspspringboot</finalName>
    <pluginManagement><!-- lock down plugins versions to avoid using Maven defaults (may be moved to parent pom) -->
      <plugins>
        <plugin>
          <artifactId>maven-clean-plugin</artifactId>
          <version>3.1.0</version>
        </plugin>
        <!-- see http://maven.apache.org/ref/current/maven-core/default-bindings.html#Plugin_bindings_for_war_packaging -->
        <plugin>
          <artifactId>maven-resources-plugin</artifactId>
          <version>3.0.2</version>
        </plugin>
        <plugin>
          <artifactId>maven-compiler-plugin</artifactId>
          <version>3.8.0</version>
        </plugin>
        <plugin>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>2.22.1</version>
        </plugin>
        <plugin>
          <artifactId>maven-war-plugin</artifactId>
          <version>3.2.2</version>
        </plugin>
        <plugin>
          <artifactId>maven-install-plugin</artifactId>
          <version>2.5.2</version>
        </plugin>
        <plugin>
          <artifactId>maven-deploy-plugin</artifactId>
          <version>2.8.2</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>
```
# 2 pom引入依赖删除单元测试依赖
删除单元测试的依赖：

```xml
<dependency>
  <groupId>junit</groupId>
  <artifactId>junit</artifactId>
  <version>4.11</version>
  <scope>test</scope>
</dependency>
```

添加的依赖：

```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>2.2.5.RELEASE</version>
</parent>

<dependencies>
  <!-- web -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>

  <!-- 整合JSP -->
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-tomcat</artifactId>
  </dependency>
  <dependency>
    <groupId>org.apache.tomcat.embed</groupId>
    <artifactId>tomcat-embed-jasper</artifactId>
  </dependency>

  <!-- JSTL -->
  <dependency>
    <groupId>jstl</groupId>
    <artifactId>jstl</artifactId>
    <version>1.2</version>
  </dependency>

  <dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.6</version>
    <scope>provided</scope>
  </dependency>
</dependencies>
```

# 3 创建配置文件application.yml
这个项目里`src/main`下没有java和resources文件夹的，这就需要手动创建，然后在resources下创建application.yml配置文件

```yaml
server:
  port: 8181
spring:
  mvc:
    view:
      prefix: /
      suffix: .jsp
```
配置说明：

- `spring.mvc.view.prefix`：视图解析器解析前缀
- `spring.mvc.view.suffix`：视图解析器解析后缀

# 4 创建测试返回模型的Handler
注意：因为要返回模型，所以之前的`@RestController`不能用，需要用`@Controller`
`return "index";`：映射的是`/jspspringboot/src/main/webapp/index.jsp`
```java
package com.zh.jspspringboot.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/hello")
public class HelloHandler {
	@GetMapping("/index")
	public String index() {
		System.out.println("index...");
		return "index";
	}
}
```

# 5 创建启动类

```java
package com.zh.jspspringboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
	public static void main(String[] args) throws Exception {
		SpringApplication.run(Application.class, args);
	}
}
```

# 6 测试返回模型

1. 以Spring Boot App的方式启动项目。
1. 访问测试返回模型的接口（[http://localhost:8181/hello/index](http://localhost:8181/hello/index)）。
1. ![image.png](https://zhishan-zh.github.io/media/1583725788939-1c838fbd-e962-4a59-b885-5765ca243460.png)
1. 控制台也有输出：![image.png](https://zhishan-zh.github.io/media/1583725837652-3611bbdb-808d-41e9-827f-8670596e44fc.png)

# 7 创建实体类

```java
package com.zh.jspspringboot.entity;

import lombok.Data;

@Data
public class Student {
    private long id;
    private String name;
    private int age;
}
```

# 8 创建StudentRepository

```java
package com.zh.jspspringboot.repository;

import java.util.Collection;

import com.zh.jspspringboot.entity.Student;

public interface StudentRepository {
	public Collection<Student> findAll();
    public Student findById(long id);
    public void saveOrUpdate(Student student);
    public void deleteById(long id);
}

```

# 9 创建StudentRepositoryImpl

```java
package com.zh.jspspringboot.repository.impl;

import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import org.springframework.stereotype.Repository;

import com.zh.jspspringboot.entity.Student;
import com.zh.jspspringboot.repository.StudentRepository;

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

# 10 重新编写Handler
这里的handler编写和SpringMVC一样。
```java
package com.zh.jspspringboot.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.zh.jspspringboot.entity.Student;
import com.zh.jspspringboot.repository.StudentRepository;

@Controller
@RequestMapping("/hello")
public class HelloHandler {

    @Autowired
    private StudentRepository studentRepository;

    @GetMapping("/index")
    public ModelAndView index(){
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("index");
        modelAndView.addObject("list",studentRepository.findAll());
        return modelAndView;
    }

    @GetMapping("/deleteById/{id}")
    public String deleteById(@PathVariable("id") long id){
        studentRepository.deleteById(id);
        return "redirect:/hello/index";
    }

    @PostMapping("/save")
    public String save(Student student){
        studentRepository.saveOrUpdate(student);
        return "redirect:/hello/index";
    }

    @PostMapping("/update")
    public String update(Student student){
        studentRepository.saveOrUpdate(student);
        return "redirect:/hello/index";
    }

    @GetMapping("/findById/{id}")
    public ModelAndView findById(@PathVariable("id") long id){
        ModelAndView modelAndView = new ModelAndView();
        modelAndView.setViewName("update");
        modelAndView.addObject("student",studentRepository.findById(id));
        return modelAndView;
    }
}
```

# 11 jsp内容编写
## 11.1 index.jsp
因为系统自动创建的index.jsp没有jsp的相关内容：
```html
<html>
<body>
<h2>Hello World!</h2>
</body>
</html>
```

删除这个index.jsp，然后在相同位置使用jsp的模板新建一个jsp。
位置：`/jspspringboot/src/main/webapp/index.jsp`
![image.png](https://zhishan-zh.github.io/media/1583726625868-9b5ea908-4c73-4024-9b6d-78414d001c2a.png)

```html
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>

</body>
</html>
```

在index.jsp中添加自定义内容后：

```html
<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ page isELIgnored="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
	<h1>学生信息</h1>
	<table>
		<tr>
			<th>学生编号</th>
			<th>学生姓名</th>
			<th>学生年龄</th>
			<th>操作</th>
		</tr>
		<c:forEach items="${list}" var="student">
			<tr>
				<td>${student.id}</td>
				<td>${student.name}</td>
				<td>${student.age}</td>
				<td><a href="/hello/findById/${student.id}">修改</a> <a
					href="/hello/deleteById/${student.id}">删除</a></td>
			</tr>
		</c:forEach>
	</table>
	<a href="/save.jsp">添加学生</a>
</body>
</html>
```

## 11.2 save.jsp
位置：`/jspspringboot/src/main/webapp/save.jsp`
```html
<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ page isELIgnored="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
	<form action="/hello/save" method="post">
		ID:<input type="text" name="id" />
 name:<input type="text"
			name="name" />
 age:<input type="text" name="age" />
 <input
			type="submit" value="提交" />
	</form>
</body>
</html>
```

## 11.3 update.jsp
位置：`/jspspringboot/src/main/webapp/update.jsp`
```html
<%@ page language="java" contentType="text/html; charset=UTF-8"
	pageEncoding="UTF-8"%>
<%@ page isELIgnored="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
	<form action="/hello/update" method="post">
		ID:<input type="text" name="id" value="${student.id}" readonly />

		name:<input type="text" name="name" value="${student.name}" />

		age:<input type="text" name="age" value="${student.age}" />
 <input
			type="submit" value="提交" />
	</form>
</body>
</html>
```

# 12 测试

1. 以Spring Boot App的方式启动项目。
1. 访问测试返回模型的接口（[http://localhost:8181/hello/index](http://localhost:8181/hello/index)）。
1. ![image.png](https://zhishan-zh.github.io/media/1583727900482-bab3234b-cbd8-4919-aa3b-712588b2f891.png)
