# 服务调用方式

# 1 概述
一般微服务提供了供人调用的HTTP接口。故服务之间调用的时候可以使用http请求的相关工具类完成，如常见的HttpClient，OkHttp，当然也可以使用Spring提供的RestTemplate。
## 1.1 什么是RestTemplate
Spring框架提供的RestTemplate类可用于在应用中调用rest服务，它简化了与http服务的通信方式，统一了RESTful的标准，封装了http链接， 我们只需要传入url及返回值类型即可。相较于之前常用的HttpClient，RestTemplate是一种更优雅的调用RESTful服务的方式。


RestTemplate默认依赖JDK提供http连接的能力（HttpURLConnection），如果有需要的话也可以通`setRequestFactory` 方法替换为例如 Apache HttpComponents、Netty或OkHttp等其它HTTP library。


## 1.2 RestTemplate方法介绍
该模板类的主要切入点为一下几个方法（对应HTTP的6个主要调用方法）：

| **HTTP method** | **RestTemplate methods**                                     |
| --------------: | :----------------------------------------------------------- |
|             GET | - `public <T> T getForObject(String url, Class<T> responseType, Object... uriVariables)` <br/>- `public <T> ResponseEntity<T> getForEntity(String url, Class<T> responseType, Object... uriVariables)` |
|            POST | - `public URI postForLocation(String url, @Nullable Object request, Object... uriVariables)`<br/>- `public <T> T postForObject(String url, @Nullable Object request, Class<T> responseType, Object... uriVariables)` |
|             PUT | `public void put(String url, @Nullable Object request, Object... uriVariables)` |
|          DELETE | `public void delete(String url, Object... uriVariables)`     |
|            HEAD | `public HttpHeaders headForHeaders(String url, Object... uriVariables)` |
|         OPTIONS | `public Set<HttpMethod> optionsForAllow(String url, Object... uriVariables)` |
|             any | - `public <T> ResponseEntity<T> exchange(String url, HttpMethod method, @Nullable HttpEntity<?> requestEntity, Class<T> responseType, Object... uriVariables)`<br/>- `public <T> T execute(String url, HttpMethod method, @Nullable RequestCallback requestCallback, @Nullable ResponseExtractor<T> responseExtractor, Object... uriVariables)` |

# 2 如何使用RestTemplate
此测试项目不属于严格意义上的服务消费者，因为服务消费者也需要在注册中心上进行注册。
## 2.1 创建Maven Module项目
此项目基于《[Spring Cloud Eureka服务治理、服务发现](https://www.yuque.com/zhishan/bttt5g/wox6l8)》父工程的子项目。
![image.png](https://zhishan-zh.github.io/media/1583636535345-482256ea-d24b-45f5-bd2b-3e620941fdd6.png)
初始pom文件内容：

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.zh</groupId>
    <artifactId>zhspringcloud-parent</artifactId>
    <version>0.0.1-SNAPSHOT</version>
  </parent>
  <artifactId>resttemplate</artifactId>
</project>
```


## 2.4 创建启动类并注入RestTemplate
```java
package com.zh.resttemplate;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
public class RestTemplateApplication {
	public static void main(String[] args) {
		SpringApplication.run(RestTemplateApplication.class, args);
	}
	
	@Bean
	public RestTemplate restTemplate() {
		return new RestTemplate();
	}
}
```


## 2.3 创建实体类
```java
package com.zh.resttemplate.entity;

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


## 2.4 Handler：访问服务提供者的接口
```java
package com.zh.resttemplate.controller;

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
import org.springframework.web.client.RestTemplate;

import com.zh.resttemplate.entity.Student;

@RestController
@RequestMapping("/rest")
public class RestHandler {
	@Autowired
	private RestTemplate restTemplate;
	
	@GetMapping("/findAll")
    public Collection<Student> findAll(){
        return restTemplate.getForEntity("http://localhost:8010/student/findAll",Collection.class).getBody();
    }

    @GetMapping("/findAll2")
    public Collection<Student> findAll2(){
        return restTemplate.getForObject("http://localhost:8010/student/findAll",Collection.class);
    }

    @GetMapping("/findById/{id}")
    public Student findById(@PathVariable("id") long id){
        return restTemplate.getForEntity("http://localhost:8010/student/findById/{id}",Student.class,id).getBody();
    }

    @GetMapping("/findById2/{id}")
    public Student findById2(@PathVariable("id") long id){
        return restTemplate.getForObject("http://localhost:8010/student/findById/{id}",Student.class,id);
    }

    @PostMapping("/save")
    public void save(@RequestBody Student student){
        restTemplate.postForEntity("http://localhost:8010/student/save",student,null).getBody();
    }

    @PostMapping("/save2")
    public void save2(@RequestBody Student student){
        restTemplate.postForObject("http://localhost:8010/student/save",student,null);
    }

    @PutMapping("/update")
    public void update(@RequestBody Student student){
        restTemplate.put("http://localhost:8010/student/update",student);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        restTemplate.delete("http://localhost:8010/student/deleteById/{id}",id);
    }
}
```


