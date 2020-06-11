# Spring配置

# 1 注入bean参数说明


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">

	<!-- 将com.zh.springmaventest.entity.User的对象交给spring管理 -->
	<bean id="user" class="com.zh.springmaventest.entity.User" 
	init-method="init" destroy-method="destory">
	</bean>
</beans>
```
**配置说明：**

- **bean元素**: 将对象配置到spring容器中
  - **name属性**:	给配置到容器中的对象起一个标识，获得对象时要根据该标识获得；
  - **class属性**:   要放置到Spring容器中的对象的完整类名；
  - **id属性(一般不用，不用记)**：功能同name属性一样，名字规则必须符合id的规范。
    - id必须唯一
    - id中不能包含特殊字符
- **scope属性**：决定bean在容器中的域范围，整合struts2的Action时会使用，Action需要指定为多例的。
  - **singleton(默认值)**：单例的，该对象会在容器启动时创建。并且只会创建一个对象，容器关闭时销毁。
  - **prototype**：原型多例。每次获得时创建多例对象。每次获得都是全新的对象，每次获得时创建，Spring不负责对prototype对象的销毁。
  - **request(了解)：**在web环境中，对象与当前请求生命周期相同。
  - **session(了解)：**在web环境中，对象与当前会话生命周期相同。
- 指定对象生命周期方法的属性
  - init-method：指定对象的初始化方法；
  - destroy-method：指定对象的销毁方法。



# 2 引入其他配置文件
## 2.1 实体类
### 2.1.1 User类
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


### 2.1.2 User2类


```java
package com.zh.springmaventest.entity;

public class User2 {
	private String name;
	private Integer age;
	
	public User2() {
		System.out.println("User2 被创建了!");
	}

	public User2(String name, Integer age) {
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


## 2.2 主配置文件springcontext.xml
位置：`/springmaventest/src/main/resources/springcontext.xml` （Maven项目）或`/springstart/src/applicationcontext.xml`（普通java项目）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<!-- 引入其他配置文件 -->
	<import resource="springcontext_bean.xml"/>
  	<import resource="com/zh/springmaventest/entity/springcontext_bean2.xml"/>
</beans>
```


## 2.3 需要引入的配置文件
需要引入的配置文件位置1：`/springmaventest/src/main/resources/springcontext_bean1.xml`（Maven项目）或`/springstart/src/applicationcontext_bean1.xml`（普通java项目）


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">

	<!-- 将com.zh.springmaventest.entity.User的对象交给spring管理 -->
	<bean id="user" class="com.zh.springmaventest.entity.User">
		<property name="name" value="张三"></property>
		<property name="age" value="22"></property>
	</bean>
</beans>
```


需要引入的配置文件位置2：`/springmaventest/src/main/resources/com/zh/springmaventest/entity/springcontext_bean2.xml`（Maven项目）或`/springstart/src/com/zh/springmaventest/entity/applicationcontext_bean2.xml`（普通java项目）


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">

	<!-- 将com.zh.springmaventest.entity.User2的对象交给spring管理 -->
	<bean id="user2" class="com.zh.springmaventest.entity.User2">
		<property name="name" value="李四"></property>
		<property name="age" value="20"></property>
	</bean>
</beans>
```


## 2.4 测试引入配置文件


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
		User2 user2 = (User2) applicationContext.getBean("user2");
		System.out.println(user2);
	}
}
```
输出：

```
User 被创建了!
User2 被创建了!
com.zh.springmaventest.entity.User@1e127982
com.zh.springmaventest.entity.User2@60c6f5b
```

# 3 Spring中对象的创建方式

- 构造方法创建（默认和推荐的方式）
- 静态工厂创建
- 动态工厂创建

## 3.1 构造方法创建（默认和推荐的方式）


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


## 3.2 静态工厂创建
### 3.2.3 静态工厂类


```java
package com.zh.springstart.testclass;

public class UserFactory {
	// 静态工厂方法
	public static User getUser() {
		System.out.println("调用静态工厂方法创建User!");
		return new User();
	}
}
```


### 3.2.2 配置文件配置
调用静态工厂方法创建User对象：调用指定工厂类(com.zh.springstart.testclass.UserFactory)的指定方法(getUser)创建User对象
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<bean name="user" class="com.zh.springstart.testclass.UserFactory" 
	factory-method="getUser"></bean>
</beans>
```


## 3.3 动态工厂创建
### 3.3.1 动态工厂类


```java
package com.zh.springstart.testclass;

public class UserFactory {
	// 动态工厂方法
	public User getUser2() {
		System.out.println("调用动态工厂方法创建User!");
		return new User();
	}
}

```


### 3.3.2 配置文件配置


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<!-- 动态工厂方法 -->
	<!-- 指定spring创建静态工厂类 -->
	<bean name="userFactory" class="com.zh.springstart.testclass.UserFactory"></bean>
	<!-- 指定spring创建user对象时,调用名为userFactory对象的getUser2方法 -->
	<bean name="user" factory-bean="userFactory" factory-method="getUser2"></bean>
</beans>
```

# 4 Spring属性注入

- 构造方法注入（推荐）
- set方法注入
    - property元素注入（推荐）
    - p命名空间注入
    - SPEL（Spring Expression ）Spring表达式注入
- 复杂类型注入
- IoC⾃动装载

## 4.1 构造方法注入（推荐）

1. 在实体类中创建相应的有参构造函数
1. 配置文件中配置注入的属性

### 4.1.1 实体类
User类：
```java
package com.zh.springstart.testclass;

public class User {
	private String name;
	private Integer age;
	private Car car;
	
	public User() {
		System.out.println("User 被创建了!");
	}

	public User(String name, Integer age, Car car) {
		super();
		this.name = name;
		this.age = age;
		this.car = car;
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

	public Car getCar() {
		return car;
	}

	public void setCar(Car car) {
		this.car = car;
	}
}
```


Car类：
```java
package com.zh.springstart.testclass;

public class Car {
	private String name;
	private String color;
	public Car() {
		super();
	}
	public Car(String name, String color) {
		super();
		this.name = name;
		this.color = color;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getColor() {
		return color;
	}
	public void setColor(String color) {
		this.color = color;
	}
}
```


### 4.1.2 配置文件配置


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
  <!-- 注册User对象,并使用构造方法注入属性 -->
	<bean name="user" class="com.zh.springstart.testclass.User">
		<constructor-arg name="name" index="0" value="john"></constructor-arg>
		<constructor-arg name="age" index="1" type="java.lang.Integer" value="16"></constructor-arg>
		<constructor-arg name="car" index="2" ref="car"></constructor-arg>
	</bean>
	<bean name="car" class="com.zh.springstart.testclass.Car">
		<property name="name" value="蓝跑"></property>
		<property name="color" value="blue"></property>
	</bean>
</beans>
```
**配置说明：**

- **constructor-arg**指定调用的构造函数的参数
  - **name**属性：指定参数名称
  - **index**属性：指定参数所在构造方法中的索引
    - 从0开始计数
    - index和name用一个就行。
  - **value**属性：指定参数的值
  - **type**属性：指定参数的类型
  - **ref**属性：注入对象类型的值，值为其他bean的name属性的值。
## 4.2 set方法注入
### 4.2.1 property元素注入（推荐）


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
  <!-- property元素   set方法注入 -->
	<bean name="user" class="com.zh.springstart.testclass.User">
		<property name="name" value="john"></property>
		<property name="age" value="16"></property>
		<property name="car" ref="car"></property>
	</bean>
	<bean name="car" class="com.zh.springstart.testclass.Car">
		<property name="name" value="蓝跑"></property>
		<property name="color" value="blue"></property>
	</bean>
</beans>
```
**配置说明：**

- **property**：
  - **name**属性：属性名
  - **value**属性：属性值
  - **ref**属性：注入对象类型的值
### 4.2.2 p命名空间注入
使用前先导入P命名空间：`xmlns:p="http://www.springframework.org/schema/p"`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
  xmlns:p="http://www.springframework.org/schema/p"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	 <!-- p命名空间注入 -->
	 <bean name="user" class="com.zh.springstart.testclass.User" 
	 p:name="john" p:age="16" p:car-ref="car">
	</bean>
	<bean name="car" class="com.zh.springstart.testclass.Car">
		<property name="name" value="蓝跑"></property>
		<property name="color" value="blue"></property>
	</bean>
</beans>
```


### 4.2.3 SPEL（Spring Expression ）Spring表达式注入


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xmlns:p="http://www.springframework.org/schema/p"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<!-- 注册User对象,并使用构造方法注入属性 -->
	<bean name="user" class="com.zh.springstart.testclass.User">
		<constructor-arg name="name" index="0" value="john"></constructor-arg>
		<constructor-arg name="age" index="1" type="java.lang.Integer" value="16"></constructor-arg>
		<constructor-arg name="car" index="2" ref="car"></constructor-arg>
	</bean>
	<!-- property元素   set方法注入 -->
	<bean name="user1" class="com.zh.springstart.testclass.User">
		<property name="name" value="john1"></property>
		<property name="age" value="17"></property>
		<property name="car" ref="car"></property>
	</bean>

	 <!-- p命名空间注入 -->
	 <bean name="user2" class="com.zh.springstart.testclass.User" 
	 p:name="john2" p:age="18" p:car-ref="car">
	</bean>
  
	<!-- spring Expression spring表达式 -->
	<bean name="user3" class="com.zh.springstart.testclass.User">
		<property name="name" value="#{user.name}"></property>
		<property name="age" value="#{user1.age}"></property>
		<property name="car" ref="car"></property>
	</bean>
	<bean name="car" class="com.zh.springstart.testclass.Car">
		<property name="name" value="蓝跑"></property>
		<property name="color" value="blue"></property>
	</bean>
</beans>
```


## 4.3 复杂类型注入
### 4.3.1 实体类


```java
package com.zh.springstart.testclass;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Properties;

public class CollectionBean {
	private Object[] arr;
	private List list;
	private Map map;
	private Properties props;
	public Object[] getArr() {
		return arr;
	}
	public void setArr(Object[] arr) {
		this.arr = arr;
	}
	public List getList() {
		return list;
	}
	public void setList(List list) {
		this.list = list;
	}
	public Map getMap() {
		return map;
	}
	public void setMap(Map map) {
		this.map = map;
	}
	public Properties getProps() {
		return props;
	}
	public void setProps(Properties props) {
		this.props = props;
	}
	@Override
	public String toString() {
		return "CollectionBean [arr=" + Arrays.toString(arr) + ", list=" + list + ", map=" + map + ", props=" + props
				+ "]";
	}
}
```


### 4.3.2 配置文件


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://www.springframework.org/schema/beans"
	xmlns:p="http://www.springframework.org/schema/p"
	xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<!-- 注册User对象,并使用构造方法注入属性 -->
	<bean name="user" class="com.zh.springstart.testclass.User">
		<constructor-arg name="name" index="0" value="john"></constructor-arg>
		<constructor-arg name="age" index="1"
			type="java.lang.Integer" value="16"></constructor-arg>
		<constructor-arg name="car" index="2" ref="car"></constructor-arg>
	</bean>
	<!-- property元素 set方法注入 -->
	<bean name="user1" class="com.zh.springstart.testclass.User">
		<property name="name" value="john1"></property>
		<property name="age" value="17"></property>
		<property name="car" ref="car"></property>
	</bean>
	<!-- spring Expression spring表达式 -->
	<bean name="user3" class="com.zh.springstart.testclass.User">
		<property name="name" value="#{user.name}"></property>
		<property name="age" value="#{user1.age}"></property>
		<property name="car" ref="car"></property>
	</bean>
	<bean name="car" class="com.zh.springstart.testclass.Car">
		<property name="name" value="蓝跑"></property>
		<property name="color" value="blue"></property>
	</bean>

	<bean name="collectionBean" class="com.zh.springstart.testclass.CollectionBean">
		<!-- 数组类型注入 1.数组中只注入一个元素,可以直接使用value或ref属性 <property name="arr" value="tom" 
			></property> 2.数组中包含多个值 -->
		<property name="arr">
			<array>
				<!-- 因为arr是Object类型的数组，所以可以同时用value和ref，这两个都能注入 -->
				<value>Tom</value>
				<ref bean="user" />
			</array>
		</property>
		<!-- list类型注入(跟数组玩法一样) 1.数组中只注入一个元素,可以直接使用value或ref属性 <property name="list" 
			value="tom" ></property> 2.数组中包含多个值 -->
		<property name="list">
			<list>
				<value>lucy</value>
				<ref bean="user1" />
			</list>
		</property>
		<!-- map类型注入 -->
		<property name="map">
			<map>
				<entry key="name" value="tom"></entry>
				<entry key="user" value-ref="user"></entry>
				<entry key-ref="user1" value-ref="user1"></entry>
			</map>
		</property>
		<!-- properties类型注入 -->
		<property name="props">
			<props>
				<prop key="jdbc.driver">com.mysql.jdbc.Driver</prop>
				<prop key="jdbc.url">jdbc:mysql:///hibernate34</prop>
			</props>
		</property>
	</bean>
</beans>
```


### 4.3.3 测试复杂属性注入


```java
package com.zh.springstart.testclass;

import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class ClassTest {
	public static void main1(String[] args) {
		// 1 创建Spring容器对象
		ApplicationContext ac = new ClassPathXmlApplicationContext("applicationcontext.xml");
		// 2 从容器中获得user对象
		User u = (User) ac.getBean("user");
		System.out.println(
				"user.name=" + u.getName() + "user.age=" + u.getAge() + ";user.car.name=" + u.getCar().getName());
		User u1 = (User) ac.getBean("user1");
		System.out.println(
				"user1.name=" + u1.getName() + "user1.age=" + u1.getAge() + ";user1.car.name=" + u1.getCar().getName());
		User u2 = (User) ac.getBean("user2");
		System.out.println(
				"user2.name=" + u2.getName() + "user2.age=" + u2.getAge() + ";user2.car.name=" + u2.getCar().getName());
	}

	public static void main(String[] args) {
		// 1 创建Spring容器对象
		ApplicationContext ac = new ClassPathXmlApplicationContext("applicationcontext.xml");
		CollectionBean collectionBean = (CollectionBean) ac.getBean("collectionBean");
		Object[] arr = collectionBean.getArr();
		for (int i = 0; i < arr.length; i++) {
			System.out.println(arr[i]);
		}
		List list = collectionBean.getList();
		for (int i = 0; i < list.size(); i++) {
			System.out.println(list.get(i));
		}
		Map map = collectionBean.getMap();
		Set keySet = map.keySet();
		Iterator iterator = keySet.iterator();
		while(iterator.hasNext()){
			Object object = iterator.next();
			System.out.println("key=" + object + ";value=" + map.get(object));
		}
		Properties props = collectionBean.getProps();
		Enumeration<Object> keys = props.keys();
		while (keys.hasMoreElements()) {
			Object object = keys.nextElement();
			System.out.println("key=" + object + ";value=" + props.get(object));
		}
	}
}
```


## 4.4 IoC⾃动装载
IoC 负责创建对象，DI 负责完成对象的依赖注⼊，通过配置 property 标签的 ref 属性来完成，同时Spring 提供了另外⼀种更加简便的依赖注⼊⽅式：⾃动装载，不需要⼿动配置 property，IoC 容器会⾃动选择 bean 完成注⼊。


⾃动装载有两种⽅式：

- **byName**：通过属性名⾃动装载
- **byType**：通过属性的数据类型⾃动装载

### 4.4.1 实体类


```java
package com.zh.springstart.testautowire;

public class Car {
	private Integer id;
	private String name;

	public Car() {
		System.out.println("创建了Car对象");
	}
	
	public Car(Integer id, String name) {
		this.id = id;
		this.name = name;
	}
	
	public void setId(Integer id) {
		this.id = id;
	}

	public void setName(String name) {
		this.name = name;
	}
	
	public Integer getId() {
		return id;
	}

	public String getName() {
		return name;
	}

	@Override
	public String toString() {
		return "Car{" + "id=" + id + ", name='" + name + '\'' + '}';
	}
}
```


```java
package com.zh.springstart.testautowire;

public class Person {
	private Integer id;
	private String name;
	private Car car;

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public Car getCar() {
		return car;
	}

	public void setCar(Car car) {
		this.car = car;
	}

	@Override
	public String toString() {
		return "Person{" + "id=" + id + ", name='" + name + '\'' + ", car=" + car + '}';
	}
}
```


### 4.4.1 byName方式
位置：`/springstart/src/com/zh/springstart/testautowire/autowirebyname.xml`


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:p="http://www.springframework.org/schema/p" 
xmlns="http://www.springframework.org/schema/beans" 
xsi:schemaLocation="http://www.springframework.org/schema/context 
http://www.springframework.org/schema/context/spring-context.xsd 
http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<!-- ByName -->
	<bean id="person" class="com.zh.springstart.testautowire.Person"
		autowire="byName">
		<property name="id" value="1"></property>
		<property name="name" value="张三"></property>
	</bean>
	<bean id="car" class="com.zh.springstart.testautowire.Car">
		<property name="id" value="1"></property>
		<property name="name" value="悍马"></property>
	</bean>
</beans>
```


### 4.4.3 byType
位置：`/springstart/src/com/zh/springstart/testautowire/autowirebytype.xml`
byType 需要注意，如果同时存在两个及以上的符合条件的 bean 时，⾃动装载会抛出异常。


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:p="http://www.springframework.org/schema/p" 
xmlns="http://www.springframework.org/schema/beans" 
xsi:schemaLocation="http://www.springframework.org/schema/context 
http://www.springframework.org/schema/context/spring-context.xsd 
http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<!-- ByType -->
	<bean id="person" class="com.zh.springstart.testautowire.Person"
		autowire="byType">
		<property name="id" value="1"></property>
		<property name="name" value="张三"></property>
	</bean>
	<bean id="carByType" class="com.zh.springstart.testautowire.Car">
		<property name="id" value="1"></property>
		<property name="name" value="悍马"></property>
	</bean>
</beans>
```


# 5 Spring的继承和依赖
## 5.1 Spring的继承
- Java 是类层⾯的继承，⼦类可以继承⽗类的内部结构信息；

- Spring 是对象层⾯的继承，⼦对象可以继承⽗对象的属性值。

Spring 的继承关注点在于具体的对象，⽽不在于类，即不同的两个类的实例化对象可以完成继承，前提是⼦对象必须包含⽗对象的所有属性，同时可以在此基础上添加其他的属性。

```xml
<bean id="student2" class="com.zh.entity.Student">
  <property name="id" value="1"></property>
  <property name="name" value="张三"></property>
  <property name="age" value="22"></property>
  <property name="addresses">
    <list>
      <ref bean="address"></ref>
      <ref bean="address2"></ref>
    </list>
  </property>
</bean>
<bean id="address" class="com.zh.entity.Address">
  <property name="id" value="1"></property>
  <property name="name" value="科技路"></property>
</bean>
<bean id="address2" class="com.zh.entity.Address">
  <property name="id" value="2"></property>
  <property name="name" value="⾼新区"></property>
</bean>
<bean id="stu" class="com.zh.entity.Student"
      parent="student2">
  <property name="name" value="李四"></property>
</bean>
```


## 5.2 Spring的依赖
与继承类似，依赖也是描述 bean 和 bean 之间的⼀种关系，配置依赖之后，被依赖的 bean ⼀定先创建，再创建依赖的 bean，比如A 依赖于 B，先创建 B，再创建 A。


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans
http://www.springframework.org/schema/beans/spring-beans-3.2.xsd
 ">
	<bean id="student" class="com.southwind.entity.Student" depends-on="user"></bean>
	<bean id="user" class="com.southwind.entity.User"></bean>
</beans>
```


# 6 Spring注解
## 6.1 Spring注解概述
### 6.1.1 Spring注解的功能
可以使用注解来代替xml配置。


### 6.1.2 Spring注解配置与XML配置对比
**选择原则**：无论xml或注解在企业开发中都有使用，选用哪种配置方式要以企业中项目规范来定。
**xml优点**：统一管理配置，便于后期维护。
**注解优点**：书写方便；书写类时注解可以一并完成；但是维护困难。


## 6.2 注解使用步骤

1. 除了Spring 4+2基础包外，还需要导入spring-aop包。
      1. `spring-framework-4.2.4.RELEASE\libs\spring-aop-4.2.4.RELEASE.jar`
2. 在Spring主配置文件中引入context约束
      1. 约束文件位置：`spring-framework-4.2.4.RELEASE\schema\context\spring-context-4.2.xsd`
3. 使用context约束中的元素打开注解配置开关。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:p="http://www.springframework.org/schema/p" 
xmlns="http://www.springframework.org/schema/context" 
xsi:schemaLocation="http://www.springframework.org/schema/beans 
http://www.springframework.org/schema/beans/spring-beans.xsd 
http://www.springframework.org/schema/context 
http://www.springframework.org/schema/context/spring-context.xsd ">
	<!-- component-scan:扫描指定包中的对象的注解 -->
	<context:component-scan base-package="com.zh"></context:component-scan>
</beans>
```
**配置说明：**

- **base-package**
  - 当要配置一个项目多个包是，可以配置这几个包上一层包名
  - 比如要配置com.zh.dao和com.zh.service这两个包下的注解配置时，可以直接使用com.zh
4. 在类中书写注解配置。

## 6.3 注册对象


```java
//@Component("userDao")，是最早出现的，已经不推荐使用，后来为了区分不同模块的注解出现了下边三个功能相同的注解。
//@Controller("userController")//web层
//@Service("userService")//Service层
@Repository("userDao")//Dao层注解，相当于XML中的： <bean name="userDao" class="com.zh.dao.UserDaoImpl" />
public class UserDaoImpl implements UserDao {
	//省略N行代码
}
```


```java
@Service("userService")
public class UserServiceImpl implements UserService {
    //省略N行代码
}
```
## 6.4 注解对象的作用范围


```java
@Repository("userDao")//Dao层
//对象的域范围,singleton是默认值，可以不写注解；prototype一般用在Action类上，需要注解
@Scope("prototype") 
public class UserDaoImpl implements UserDao {
    //省略N行代码
}
```


## 6.5 值类型属性注解


```java
package com.zh.springstart.testclass;

import org.springframework.beans.factory.annotation.Value;

public class User {
	@Value("tom")//直接对变量赋值,没有走set方法
	private String name;
	public String getName() {
		return name;
	}
}
```


```java
package com.zh.springstart.testclass;

import org.springframework.beans.factory.annotation.Value;

public class User {
	private String name;
	public String getName() {
		return name;
	}
	@Value("tom")//调用Set方法来注入值（技术上推荐）
	public void setName(String name) {
		this.name = name;
	}
}
```


## 6.6 对象类型属性注解
### 6.6.1 Autowired


```java
package com.zh.springstart.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.zh.springstart.dao.UserDao;
import com.zh.springstart.service.UserService;

@Service
public class UserServiceImpl implements UserService {
	@Autowired //自动装配，根据类型。
	private UserDao ud;
}
```


### 6.6.2 Autowired&Qualifier


```java
package com.zh.springstart.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.zh.springstart.dao.UserDao;
import com.zh.springstart.service.UserService;

@Service
public class UserServiceImpl implements UserService {
	//这两个和在一起不常用，如果需要指定装配的对象的名称，则会用@Resource
	@Autowired //自动装配,根据类型.（无法制定装配的对象的名称）
	@Qualifier("userDao")//辅助autowired注解,指定需要装配的对象名称
	private UserDao ud;
}
```


### 6.6.3 Resource


```java
package com.zh.springstart.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.zh.springstart.dao.UserDao;
import com.zh.springstart.service.UserService;

@Service
public class UserServiceImpl implements UserService {
	@Resource(name="userDao")//手动指定Bean名称注入
	private UserDao ud;
}
```


## 6.7 指定对象的生命周期


```java
package com.zh.springstart.service.impl;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.zh.springstart.dao.UserDao;
import com.zh.springstart.service.UserService;

@Service
public class UserServiceImpl implements UserService {
	@Autowired //自动装配,根据类型.	
	private UserDao ud;
	
	@PostConstruct //在对象构造之后调用的方法,init方法
	public void init(){
		System.out.println("UserServiceImpl 被创建了!");
	}
	@PreDestroy //容器销毁之前调用的释放资源方法
	public void destory(){
		System.out.println("UserServiceImpl 被销毁了!");
	}
}
```


