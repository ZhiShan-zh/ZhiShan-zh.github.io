# Spring Boot 整合 JDBC

# 1 项目基础搭建
使用原有项目thymeleafspringboot。

# 2 pom里边新增依赖信息

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.11</version>
</dependency>
```

# 3 配置文件新增数据库有关配置
配置文件：`/thymeleafspringboot/src/main/resources/application.yml`

```yaml
server:
  port: 9090
spring:
  thymeleaf:
    prefix: classpath:/templates/
    suffix: .html
    mode: HTML5
    encoding: UTF-8
  datasource:
    url: jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=UTF-8
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
```

# 4 修改实体类

```java
package thymeleafspringboot.entity;

import lombok.Data;
import org.hibernate.validator.constraints.Length;

import javax.validation.constraints.Min;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Data
public class User {
    @NotNull(message = "id不能为空")
    private Long id;
    @NotEmpty(message = "姓名不能为空")
    @Length(min = 2,message = "姓名长度不能小于2位")
    private String name;
    @Min(value = 60,message = "成绩必须大于60分")
    private double score;
}
```

# 5 创建UserRepository

```java
package thymeleafspringboot.respository;

import java.util.List;

import thymeleafspringboot.entity.User;

public interface UserRepository {
    public List<User> findAll();
    public User findById(long id);
    public void save(User user);
    public void update(User user);
    public void deleteById(long id);
}
```

# 6 创建UserRepositoryImpl

```java
package thymeleafspringboot.respository.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;
import thymeleafspringboot.entity.User;
import thymeleafspringboot.respository.UserRepository;

@Repository
public class UserRepositoryImpl implements UserRepository {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Override
    public List<User> findAll() {
        return jdbcTemplate.query("select * from user",new BeanPropertyRowMapper<>(User.class));
    }

    @Override
    public User findById(long id) {
        return jdbcTemplate.queryForObject("select * from user where id = ?",new Object[]{id},new BeanPropertyRowMapper<>(User.class));
    }

    @Override
    public void save(User user) {
        jdbcTemplate.update("insert into user(name,score) values(?,?)",user.getName(),user.getScore());
    }

    @Override
    public void update(User user) {
        jdbcTemplate.update("update user set name = ?,score = ? where id = ?",user.getName(),user.getScore(),user.getId());
    }

    @Override
    public void deleteById(long id) {
        jdbcTemplate.update("delete from user where id = ?",id);
    }
}
```

# 7 创建Handler

```java
package thymeleafspringboot.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import thymeleafspringboot.entity.User;
import thymeleafspringboot.respository.UserRepository;

@RestController
@RequestMapping("/user")
public class UserHandler {

    @Autowired
    private UserRepository userRepository;

    @GetMapping("/findAll")
    public List<User> findAll(){
        return userRepository.findAll();
    }

    @GetMapping("/findById/{id}")
    public User findById(@PathVariable("id") long id){
        return userRepository.findById(id);
    }

    @PostMapping("/save")
    public void save(@RequestBody User user){
        userRepository.save(user);
    }

    @PutMapping("/update")
    public void update(@RequestBody User user){
        userRepository.update(user);
    }

    @DeleteMapping("/deleteById/{id}")
    public void deleteById(@PathVariable("id") long id){
        userRepository.deleteById(id);
    }
}
```

