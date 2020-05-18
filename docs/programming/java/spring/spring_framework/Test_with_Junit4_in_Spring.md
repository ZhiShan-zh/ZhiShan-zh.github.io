# Spring中整合Junit4测试

# 1 依赖包
- Spring基础4+2包
- aop+test+junit4类库
  - `spring-aop-4.2.4.RELEASE.jar`
  - `spring-test-4.2.4.RELEASE.jar`
  - `junit-4.13.jar`
  - `hamcrest-core-1.3.jar`



# 2 书写Spring配置文件


位置：`/springtest/src/applicationcontext.xml`


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p" xmlns:context="http://www.springframework.org/schema/context" xmlns:aop="http://www.springframework.org/schema/aop" xmlns="http://www.springframework.org/schema/beans" xsi:schemaLocation="http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd ">
</beans>
```


# 3 测试


```java
package com.zh.springtest;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

//由SpringJUnit4ClassRunner创建spring容器
@RunWith(SpringJUnit4ClassRunner.class)
//指定配置文件位置，
@ContextConfiguration(locations = "classpath:applicationcontext.xml")
public class SpringTest {
	@Test
	public void test1() {
		System.out.println("test1");
	}
}
```


注解


- `@RunWith`：用于指定junit运行环境，是junit提供给其他框架测试环境接口扩展，为了便于使用spring的依赖注入，spring提供了`org.springframework.test.context.junit4.SpringJUnit4ClassRunner`作为Junit测试环境
- `@ContextConfiguration({"classpath:applicationcontext.xml","classpath:spring/buyer/applicationcontext-service.xml"})`

导入配置文件，这里我的applicationcontext配置文件是根据模块来分类的。如果有多个模块就引入多个“applicationcontext-service.xml”文件。如果所有的都是写在“applicationcontext.xml”中则这样导入：

`@ContextConfiguration("classpath:applicationcontext.xml")`
