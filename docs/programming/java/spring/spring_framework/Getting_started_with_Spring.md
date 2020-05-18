# Spring入门

# 1 Spring概述
## 1.1 Spring简介

- Spring框架是一个容器,是一个对象的容器。
- Spring可以用来负责管理项目中的所有对象。
  - WEB层可以负责管理action对象那个
  - service层可以负责管理xxxService对象
  - dao层可以负责管理SessionFactory和xxxDao对象
- 可以将对象的依赖注入、生命周期维护都交给Spring管理，减少自己管理的麻烦
  - Spring框架可以将负责的对象关系简化。
  - 依赖注入的目的是解偶。
- Spring支持AOP开发，这是基于动态代理的。
- 市场占有率：3\~4成使用hibernate5\~6成使用Struts，9成都是用Spring
- Spring不仅可以用来WEB开发，其他程序都可以。



## 1.2 Spring的作用

- IOC和DI，即进行控制反转和依赖注入，也就是通过Spring工厂创建对象并管理对象之间的依赖关系。
  - 目的是解偶。
- 提供声明式事务，进行事务管理。
- 集成其他框架。



## 1.3 Spring框架的核心:loC和DI
### 1.3.1 IoC（Inverse Of Control）反转控制

- 没有Spring框架时，所有对象以及对象的依赖关系，都由我们开发人员手动维护
- 有了Spring框架后，对象的创建以及依赖关系的维护都反转了，程序（Spring）来维护
- 反转指的就是对象的创建以及依赖关系维护的反转。



### 1.3.2 DI（Dependency Injection）依赖注入

- 指的是技术，将依赖的属性注入到对象的技术。
- 注入方式：
  - set注入
  - 构造方法注入
  - 注解
### 1.3.3 loC与DI之间的关系

- IOC的概念范围更大一些
- 要想实现IOC思想，必须具有DI技术的支持。



### 1.3.4 loC容器系列的实现

- BeanFactory：
  - 是loC的顶层接口，功能相对较少。
  - 体现了loC容器的功能规范。
  - **特点**：使用对象时，容器先创建对象
- applicationContext：
  - 是Spring的底层接口。
  - **特点**：容器创建时，就会创建出所有对象。就是创建ApplicationContext创建时



# 2 Java普通项目整合Spring入门案例
## 2.1 新建Java Project
![深度截图_选择区域_20200324211343.png](https://zhishan-zh.github.io/media/1585055714436-f5031479-75d7-4222-a866-26456fe7aa75.png)




## 2.1 添加基础包（4+2）
注意：**spring-framework-3.0.2.RELEASE之后Spring不再提供依赖包，可以自行查找具体的包**。
在项目更目录下新建lib文件夹，并一下一个基础包（4+2）添加到lib中。
**注意**：spring-framework-3.0.2.RELEASE就不再发布依赖包了。

- spring-framework-4.2.4.RELEASE\libs下（4个）：
  - spring-beans-4.2.4.RELEASE.jar
  - spring-context-4.2.4.RELEASE.jar
  - spring-core-4.2.4.RELEASE.jar
  - spring-expression-4.2.4.RELEASE.jar
- spring-framework-3.0.2.RELEASE-dependencies\org.apache.commons\com.springsource.org.apache.commons.logging\1.1.1下：
  - com.springsource.org.apache.commons.logging-1.1.1.jar
- spring-framework-3.0.2.RELEASE-dependencies\org.apache.log4j\com.springsource.org.apache.log4j\1.2.15下：
  - com.springsource.org.apache.log4j-1.2.15.jar



右键项目名， build path-- configure...libraries --add jars..选目录lib工程包，把以上包添加到工程中。


## 2.3 随便创建一个类


```java
package com.zh.springstart.testclass;

public class User {

	public User() {
		System.out.println("User 被创建了!");
	}

	private String name;
	private Integer age;

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Integer getAge() {
		return age;
	}

	public void setAge(Integer age) {
		this.age = age;
	}
}
```


## 2.4 书写配置文件，将上边创建的对象交给Spring管理
### 2.4.1 在src下创建applicationcontext.xml

- 位置可以随意，但最好放到src下
- 名字随意，但最好用`applicationcontext.xml`



### 2.4.2 Spring的约束导入到eclipse

1. 在applicationcontext.xml中书写跟元素<beans></beans>，然后把xml的视图切换到Design视图（设计视图）
1. 选中beans，然后单击右键选择Edit Namespaces…选择Add勾选xsi，添加xsi命名空间（这是一个使用Spring XML约束必导的命名空间）
1. ![image.png](https://zhishan-zh.github.io/media/1585056741366-691ee50f-c554-4efb-bd4c-702e150a55a5.png)
1. ![image.png](https://zhishan-zh.github.io/media/1585056765809-bde16351-db31-4a00-abc3-41a5e6e83bd3.png)
1. 然后把Spring的xsd约束文件导入到eclipse中，这里以spring-framework-4.2.4.RELEASE\schema\beans下的spring-beans-4.2.xsd为例：
1. ![image.png](https://zhishan-zh.github.io/media/1585057284491-d43f3657-2052-4bcb-864d-6fac5f6ef181.png)
1. ![image.png](https://zhishan-zh.github.io/media/1585057298007-1c203448-6ab4-4cee-bc59-e468a86a741d.png)
1. 然后回到XML设计视图，选中beans，单击右键还是选中Edit Namespaces… 选择Add 选中Specify New Namespace  单击Browse… 选中Select XML Catalog entry，然后选中刚才导入的spring-beans-4.2.xsd 单击OK
1. ![image.png](https://zhishan-zh.github.io/media/1585057353643-fc9e6161-ed11-4270-a4c7-788b663bf22b.png)
1. 复制Location Hint框中中beans之前的内容到Namespace Name框中，然后单击OK
1. ![image.png](https://zhishan-zh.github.io/media/1585057379245-ed7e02ea-bed5-4836-8625-4e9cd3edf10e.png)
1. 测试是否导入成功：然后回到XML的Source视图，输入<看是否有该有的提示，有则配置成功。



### 2.4.3 把我们创建的类交给Spring管理


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<!-- 将com.zh.springstart.testclass.User的对象交给spring管理 -->
	<bean id="user" class="com.zh.springstart.testclass.User"></bean>
</beans>
```


### 2.4.4 编写测试代码
```java
package com.zh.springstart.testclass;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class ClassTest {
	public static void main(String[] args) {
		// 1 创建Spring容器对象
		ApplicationContext ac = new ClassPathXmlApplicationContext("applicationcontext.xml");
		// 2 从容器中获得user对象
		User u = (User) ac.getBean("user");
		System.out.println(u);
	}
}
```
输出：
User 被创建了!
com.zh.springstart.testclass.User@4cf777e8


# 3 Java Maven整合Spring入门案例
## 3.1 创建Maven Project
![image.png](https://zhishan-zh.github.io/media/1585098124488-50c95e68-30c2-4e00-9112-4337bd091632.png)


初始pom文件内容：


```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.zh</groupId>
  <artifactId>mavenspringtest</artifactId>
  <version>0.0.1-SNAPSHOT</version>
</project>
```


## 3.2 pom文件中加入依赖


```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>com.zh</groupId>
	<artifactId>springmaventest</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<dependencies>
		<dependency>
			<groupId>org.springframework</groupId>
			<artifactId>spring-context</artifactId>
			<version>5.1.14.RELEASE</version>
		</dependency>
	</dependencies>
</project>
```


## 3.3 创建实体类


```java
package com.zh.springmaventest.entity;

public class User {
	private String name;
	private Integer age;
	
	public User() {
		System.out.println("User 被创建了!");
	}

	public User(String name, Integer age) {
		super();
		this.name = name;
		this.age = age;
	}
	
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Integer getAge() {
		return age;
	}

	public void setAge(Integer age) {
		this.age = age;
	}
}
```




## 3.4 传统开发模式创建对象


```java
package com.zh.springmaventest.entity;

public class PrimitiveWay {
	public static void main(String[] args) {
		User user = new User();
		user.setName("张三");
		user.setAge(22);
		System.out.println(user);
	}
}
```


## 3.5 通过IoC方式
通过 IoC 方式创建对象，在配置⽂件中添加需要管理的对象，XML 格式的配置⽂件，⽂件名可以⾃定义。
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<bean id="user" class="com.zh.springmaventest.entity.User">
		<property name="name" value="张三"></property>
		<property name="age" value="22"></property>
	</bean>
</beans>
```


## 3.6 测试IoC方式
通过 id 获取对象。
```java
package com.zh.springmaventest.entity;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class SpringWay {
	public static void main(String[] args) {
		//加载配置⽂件
		ApplicationContext applicationContext = new ClassPathXmlApplicationContext("springcontext.xml");
		User user = (User) applicationContext.getBean("user");
		System.out.println(user);
	}
}
```


