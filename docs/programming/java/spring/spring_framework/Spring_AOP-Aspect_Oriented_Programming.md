# Spring AOP面向切面编程

# 1 Spring AOP概述


## 1.1 Spring AOP简介


AOP：Aspect Oriented Programming ⾯向切⾯编程。


AOP 是对⾯向对象编程的⼀个补充，在运⾏时，动态地将代码切⼊到类的指定⽅法、指定位置上的编程思想就是⾯向切⾯编程。将不同⽅法的同⼀个位置抽象成⼀个切⾯对象，对该切⾯对象进⾏编程就是AOP。


## 1.2 AOP思想


- 可以使用很多技术来实现
- 纵向重复代码，横向抽取。

### 1.2.1 AOP思想的体现


#### 1.2.1.1 过滤器


![aop_filter.png](https://zhishan-zh.github.io/media/1585288512812-812c9545-121d-4183-a1d6-2ba8c9293d1c.png)


#### 1.2.1.2 动态代理


![aop_agent.png](https://zhishan-zh.github.io/media/1585288527804-67be8c50-44fb-4d11-87e9-9cbed0651d24.png)


#### 1.2.1.3 拦截器


![aop_interceptor.png](https://zhishan-zh.github.io/media/1585288537388-3f6c76cf-052e-4161-a944-41ed1906bea4.png)


## 1.3 AOP优点


- 降低模块之间的耦合度。
- 使系统更容易扩展。
- 更好的代码复⽤。
- ⾮业务代码更加集中，不分散，便于统⼀管理。
- 业务代码更加简洁存粹，不参杂其他代码的影响。



## 1.4 Spring AOP


- Spring帮我们把AOP进行了封装。
- Spring封装了动态代理技术
  - 只需要按规则进行配置，Spring就可以帮我们“书写”动态代理代码



## 1.5 Spring实现AOP的代理方式


- **JDK动态代理**
  - 特点：被代理对象必须实现接口，否则不能进行代理
- **第三方CGLib代理**
  - 特点：不需要接口也可以进行代理，CGLib属于继承代理，该类是被代理类的子类。
- **总结**：支持两种代理就可以对所有类生成代理对象。



### 1.5.1 AOP思想中的名词解释


**目标对象（target）**：被代理对象。


**连接点（JoinPoint）**：代理对象中可以被代理的方法。


**切入点（PointCut）**：真正需要代理的方法或已经被代理的方法。


**通知（advice）**：需要对切入点增强的代码。


**代理对象（proxy）**：对目标对象执行代理后生成的对象。


**切面（aspect）**：通知+切点。


**织入（weaving）**：动词，将通知织入目标对象生成代理对象的过程。


因此：动态代理就是将通知织入目标对象的切点生成代理对象。


### 1.5.2 使用原生Java实现两种代理方式


#### 1.5.2.1 JDK动态代理


特点：被代理对象必须实现接口，否则不能进行代理


##### 1.5.2.1.1 目标对象接口


```java
package com.zh.proxytest.jdkproxy.dao;

public interface UserDao {
	void save();

	void delete();

	void update();

	void find();
}
```


##### 1.5.2.1.2 目标对象类


```java
package com.zh.proxytest.jdkproxy.dao.impl;


import com.zh.proxytest.jdkproxy.dao.UserDao;

public class UserDaoImpl implements UserDao{

	@Override
	public void save() {
		System.out.println("UserDaoImpl.save()");
	}

	@Override
	public void delete() {
		System.out.println("UserDaoImpl.delete()");
	}

	@Override
	public void update() {
		System.out.println("UserDaoImpl.update()");
	}

	@Override
	public void find() {
		System.out.println("UserDaoImpl.find()");
	}
}
```


##### 1.5.2.1.3 执行代理类


```java
package com.zh.proxytest.jdkproxy.dao;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

import com.zh.proxytest.jdkproxy.dao.impl.UserDaoImpl;

public class UserDaoProxyFactory implements InvocationHandler {
	// 被代理对象
	private UserDao targetUserDao;

	public UserDaoProxyFactory(UserDao targetUserDao) {
		this.targetUserDao = targetUserDao;
	}

	// 生成UserDao的代理对象
	public UserDao getUserDaoProxy() {
		UserDao userDaoProxy = (UserDao) Proxy.newProxyInstance(UserDaoProxyFactory.class.getClassLoader(),
				UserDaoImpl.class.getInterfaces(), this);
		return userDaoProxy;
	}

	@Override
	public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
		// 目标方法调用之前开启事务
		System.out.println("开启事务!");
		// 执行目标方法
		Object invoke = method.invoke(targetUserDao, args);
		// 目标方法调用之后关闭事务
		System.out.println("关闭事务!");
		return invoke;
	}
}
```


##### 1.5.2.1.4 测试JDK动态代理


```java
package com.zh.proxytest.jdkproxy.dao;

import com.zh.proxytest.jdkproxy.dao.impl.UserDaoImpl;

public class JdkProxyTest {
	public static void main(String[] args) {
		UserDao userDao = new UserDaoImpl();
		
		UserDaoProxyFactory factory = new UserDaoProxyFactory(userDao);
		
		UserDao userDaoProxy = factory.getUserDaoProxy();
		
		userDaoProxy.save();
		userDaoProxy.delete();
		
		System.out.println(userDaoProxy instanceof UserDao);//true
		System.out.println(userDaoProxy instanceof UserDaoImpl);//false
	}
}
```


输出：


> 开启事务!

UserDaoImpl.save()

关闭事务!

开启事务!

UserDaoImpl.delete()

关闭事务!

true

false



#### 1.5.2.2 CGLib代理


动态生成一个要代理类的子类，子类重写要代理的类的所有不是final的方法。


特点：不需要接口也可以进行代理，CGLib属于继承代理，该类是被代理的对象的子类。


CGLib代理=> 依赖包在spring-core中已经整合了


CGLIB的缺点：对于final方法无法进行代理。


##### 1.5.2.2.1 代理对象


和JDK动态代理相同


##### 1.5.2.2.2 执行代理类


```java
package com.zh.proxytest.cglib;

import java.lang.reflect.Method;

import org.springframework.cglib.proxy.Enhancer;
import org.springframework.cglib.proxy.MethodInterceptor;
import org.springframework.cglib.proxy.MethodProxy;

import com.zh.proxytest.jdkproxy.dao.UserDao;
import com.zh.proxytest.jdkproxy.dao.impl.UserDaoImpl;

public class UserDaoProxyFactory2 implements MethodInterceptor {
	// 生成UserDao的代理对象
	public UserDao getUserDaoProxy() {
		// 创建生成代理核心类
		Enhancer en = new Enhancer();
		// 指定对谁进行继承代理
		en.setSuperclass(UserDaoImpl.class);
		// 指定在代理方法中需要完成的事情，
		// 用this的话，this这个类需要实现MethodInterceptor接口，并实现intercept方法，在方法里书写通知代码
		en.setCallback(this);
		UserDao userDao = (UserDao) en.create();
		return userDao;
	}

	@Override
	public Object intercept(Object obj, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
		// 目标方法调用之前开启事务
		System.out.println("cglib开启事务!");
		// 执行目标方法
		Object invokeSuper = methodProxy.invokeSuper(obj, args);
		// 目标方法调用之后关闭事务
		System.out.println("cglib关闭事务!");
		return invokeSuper;
	}
}
```


##### 1.5.2.2.3 测试CGLIB


```java
package com.zh.proxytest.cglib;

import com.zh.proxytest.jdkproxy.dao.UserDao;
import com.zh.proxytest.jdkproxy.dao.impl.UserDaoImpl;

public class CglibTest {
	public static void main(String[] args) {
		UserDaoProxyFactory2 factory = new UserDaoProxyFactory2();

		UserDao userDaoProxy = factory.getUserDaoProxy();

		userDaoProxy.save();
		userDaoProxy.delete();

		System.out.println(userDaoProxy instanceof UserDaoImpl);// 继承代理,true
	}
}
```


### 1.5.3 Spring中使用AOP的步骤


#### 1.5.3.1 需要的jar包


- Spring基础包4+2
- spring-aop和spring-aspect
  - `spring-aop-4.2.4.RELEASE.jar`
  - `spring-aspects-4.2.4.RELEASE.jar`
- aop联盟+aspect织入包
  - `com.springsource.org.aopalliance-1.0.0.jar`
    - 位置：`spring-framework-3.0.2.RELEASE-dependencies\org.aopalliance\com.springsource.org.aopalliance\1.0.0`
  - `aspectjrt-1.8.9.jar`
  - `aspectjweaver-1.8.9.jar`
- spring-test+junit4类库
  - `spring-test-4.2.4.RELEASE.jar`
  - `junit-4.13.jar`
  - `hamcrest-core-1.3.jar`



#### 1.5.3.2 dao


```java
package com.zh.springaop.dao;

public interface UserDao {
	void save();

	void delete();

	void update();

	void find();
}
```


```java
package com.zh.springaop.dao.impl;

import com.zh.springaop.dao.UserDao;

public class UserDaoImpl implements UserDao{
	@Override
	public void save() {
		System.out.println("UserDaoImpl.save()");
	}

	@Override
	public void delete() {
		System.out.println("UserDaoImpl.delete()");
	}

	@Override
	public void update() {
		System.out.println("UserDaoImpl.update()");
	}

	@Override
	public void find() {
		System.out.println("UserDaoImpl.find()");
	}
}
```


#### 1.5.3.3 service


```java
package com.zh.springaop.service;

public interface UserService {
	void save();

	void delete();

	void update();

	void find();
}
```


```java
package com.zh.springaop.service.impl;

import com.zh.springaop.dao.UserDao;
import com.zh.springaop.service.UserService;

public class UserServiceImpl implements UserService {

	private UserDao ud;
	
	public void save() {
		ud.save();
		
		int i = 1/0;
	}

	public void delete() {
		ud.delete();
	}

	public void update() {
		ud.update();
	}

	public void find() {
		ud.find();
	}

	public void setUd(UserDao ud) {
		this.ud = ud;
	}
}
```


#### 1.5.3.4 通知类


spring一共支持5中通知类型：


- 前置通知	在目标方法执行之前调用。
- 环绕通知	在目标方法执行之前和之后调用。
- 后置通知	在目标方法执行之后调用.如果目标方法抛出异常,通知不会执行。
- 后置通知	在目标方法执行之后调用.如果目标方法抛出异常,通知仍然执行。
- 异常拦截通知  在目标方法执行出现异常时执行的代码。



```java
package com.zh.springaop.advice;

import org.aspectj.lang.ProceedingJoinPoint;

//通知类,书写需要为目标对象加入的通知
public class MyAdvice {
	//	|-前置通知	在目标方法执行之前调用
	public void before(){
		System.out.println("我是前置通知!");
	}
	//	|-环绕通知	在目标方法执行之前和之后调用
	public Object around(ProceedingJoinPoint  pjp){
		System.out.println("我是环绕通知,前置部分!");
		try {
			//执行目标方法
			Object proceed = pjp.proceed();
			System.out.println("我是环绕通知,后置部分!");
			return proceed;
		} catch (Throwable e) {
			e.printStackTrace();
			System.out.println("我是环绕通知,出现异常后执行");
			throw new RuntimeException(e.getMessage());
		}
	}
	
	//	|-后置通知	在目标方法执行之后调用.如果目标方法抛出异常,通知不会执行.
	public void afterReturning(){
		System.out.println("我是后置通知!,出现异常就不执行!");
	}
	
	//	|-后置通知	在目标方法执行之后调用.如果目标方法抛出异常,通知仍然执行.
	public void after(){
		System.out.println("我是后置通知!,出现异常仍然执行!");
	}
	
	//	|-异常拦截通知  在目标方法执行出现异常时执行的代码.
	public void afterThrowing(){
		System.out.println("我是异常拦截通知!,出大事了!!");
	}
}
```


#### 1.5.3.5 Spring配置文件


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p" xmlns:context="http://www.springframework.org/schema/context" xmlns:aop="http://www.springframework.org/schema/aop" xmlns="http://www.springframework.org/schema/beans" xsi:schemaLocation="http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<!-- component-scan:扫描指定包中的对象的注解
	<context:component-scan base-package="com.zh"></context:component-scan> 
	-->
	<bean name="userDao" class="com.zh.springaop.dao.impl.UserDaoImpl"></bean>
	<!-- 第一步：配置目标对象 -->
	<bean name="userService" class="com.zh.springaop.service.impl.UserServiceImpl">
		<property name="ud" ref="userDao"></property>
	</bean>
	<!-- 第二步：配置通知对象 -->
	<bean name="myAdvice" class="com.zh.springaop.advice.MyAdvice"></bean>
	<!-- 第三步：配置切面（切点+通知） -->
	<aop:config>
		<!-- 配置切点 -->
		<!-- 
			execution(public void cn.zh.springaop.service.impl.UserServiceImpl.save()) 
			execution(void com.zh.springaop.service.impl.UserServiceImpl.save())	什么方法限定都可以
			execution(* com.zh.springaop.service.impl.UserServiceImpl.save())	任意返回值
			execution(* com.zh.springaop.service.impl.*ServiceImpl.save())	指定包下任意以ServiceImpl结尾的类
			execution(* com.zh.springaop.service.impl.*ServiceImpl.*())		类中的所有方法(空参)
			execution(* com.zh.springaop.service.impl.*ServiceImpl.*(..))	类中的所有方法(任意参数)
			execution(* com.zh.springaop.service..*ServiceImpl.*(..))  cn.zh.springaop.service后代包中的符合规则的类
		 -->
		 <aop:pointcut id="pc" expression="execution(* com.zh.springaop.service..*ServiceImpl.*(..))" />
		 <!-- 配置切面 
			ref属性:指定哪个对象是通知对象
		-->
		<aop:aspect ref="myAdvice" >
			<!-- 前置通知切面
				method属性:通知方法名
				pointcut-ref属性:指定使用哪个切点
			 -->
			<aop:before method="before" pointcut-ref="pc" />
			<aop:around method="around" pointcut-ref="pc" />
			<aop:after-returning method="afterReturning" pointcut-ref="pc"/>
			<aop:after method="after" pointcut-ref="pc"  />
			<aop:after-throwing method="afterThrowing" pointcut-ref="pc"/>
		</aop:aspect>
	</aop:config>
</beans>
```


#### 1.5.3.6 测试


```java
package com.zh.test;

import javax.annotation.Resource;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.zh.springaop.service.UserService;

@RunWith(SpringJUnit4ClassRunner.class) // 由SpringJUnit4ClassRunner创建spring容器
@ContextConfiguration("classpath:applicationcontext.xml") // 指定配置文件位置
public class SpringAOPTest{
	@Resource(name = "userService") // 从spring容器中取出名为userService的对象注入us变量中
	private UserService us;

	@Test
	public void fun1() {
		us.save();
	}

	@Test
	public void fun2() {
		us.delete();
	}

	@Test
	public void fun3() {
		us.update();
	}

	@Test
	public void fun4() {
		us.find();
	}
}
```


**执行`fun1()`输出**：


> log4j:WARN No appenders could be found for logger (org.springframework.test.context.junit4.SpringJUnit4ClassRunner).

log4j:WARN Please initialize the log4j system properly.

我是前置通知!

java.lang.ArithmeticException: / by zero

我是环绕通知,前置部分!

UserDaoImpl.save()

at com.zh.springaop.service.impl.UserServiceImpl.save(UserServiceImpl.java:13)

at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)

at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)

(此处省略N行输出)at org.eclipse.jdt.internal.junit.runner.TestExecution.run(TestExecution.java:41)

at org.eclipse.jdt.internal.junit.runner.RemoteTestRunner.runTests(RemoteTestRunner.java:542)

我是环绕通知,出现异常后执行

我是后置通知!,出现异常仍然执行!

我是异常拦截通知!,出大事了!!

	at org.eclipse.jdt.internal.junit.runner.RemoteTestRunner.runTests(RemoteTestRunner.java:770)

at org.eclipse.jdt.internal.junit.runner.RemoteTestRunner.run(RemoteTestRunner.java:464)

at org.eclipse.jdt.internal.junit.runner.RemoteTestRunner.main(RemoteTestRunner.java:210)



#### 1.5.4 注解代替XML的AOP


#### 1.5.4.1 依赖包


和XML配置AOP的依赖包一致


#### 1.5.4.2 目标类


就是XML配置AOP中的dao和service曾代码。


#### 1.5.4.3 通知类


```java
package com.zh.springaop.advice;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;

//通知类,书写需要为目标对象加入的通知
@Aspect // 表达这是一个通知类.需要在类中配置切面
public class MyAdvice2 {
	/**
	 * 抽取出切点表达式，提高代码的复用性。
	 * 作用：如果不提供这个方法，并在这个方法上书写这个配置，
	 * 		则下边每个注解括号里边的【"MyAdvice.myPc()"】都要配置
	 * 		【"execution(* com.zh.springaop.service..*ServiceImpl.*(..))"】
	 */
	@Pointcut("execution(* com.zh.springaop.service..*ServiceImpl.*(..))")
	public void myPc() {}

	// |-前置通知 在目标方法执行之前调用
	// 可以配置MyAdvice2.myPc()或直接myPc()
	@Before("myPc()")
	public void before() {
		System.out.println("我是前置通知!");
	}

	// |-环绕通知 在目标方法执行之前和之后调用
	// 可以配置MyAdvice2.myPc()或直接myPc()
	@Around("MyAdvice2.myPc()")
	public Object around(ProceedingJoinPoint pjp) {
		System.out.println("我是环绕通知,前置部分!");
		try {
			// 执行目标方法
			Object proceed = pjp.proceed();
			System.out.println("我是环绕通知,后置部分!");
			return proceed;
		} catch (Throwable e) {
			e.printStackTrace();
			System.out.println("我是环绕通知,出现异常后执行");
			throw new RuntimeException(e.getMessage());
		}
	}

	// |-后置通知 在目标方法执行之后调用.如果目标方法抛出异常,通知不会执行.
	// 这是没有抽取切点表达式时候用的注解方式
	@AfterReturning("execution(* com.zh.springaop.service..*ServiceImpl.*(..))")
	public void afterReturning() {
		System.out.println("我是后置通知!,出现异常就不执行!");
	}

	// |-后置通知 在目标方法执行之后调用.如果目标方法抛出异常,通知仍然执行.
	// 可以配置MyAdvice2.myPc()或直接myPc()
	@After("myPc()")
	public void after() {
		System.out.println("我是后置通知!,出现异常仍然执行!");
	}

	// |-异常拦截通知 在目标方法执行出现异常时执行的代码.
	// 可以配置MyAdvice2.myPc()或直接myPc()
	@AfterThrowing("MyAdvice2.myPc()")
	public void afterThrowing() {
		System.out.println("我是异常拦截通知!,出大事了!!");
	}
}
```


#### 1.5.4.4 Spring配置文件


位置：`/springaop/src/applicationcontext2.xml`


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:p="http://www.springframework.org/schema/p" xmlns:context="http://www.springframework.org/schema/context" xmlns:aop="http://www.springframework.org/schema/aop" xmlns="http://www.springframework.org/schema/beans" xsi:schemaLocation="http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd ">
	<bean name="userDao" class="com.zh.springaop.dao.impl.UserDaoImpl"></bean>
	<!-- 第一步：配置目标对象 -->
	<bean name="userService" class="com.zh.springaop.service.impl.UserServiceImpl">
		<property name="ud" ref="userDao"></property>
	</bean>
	<!-- 第二步：配置通知对象 -->
	<bean name="myAdvice2" class="com.zh.springaop.advice.MyAdvice2"></bean>
	<!-- 第三步：开启注解aop配置，自动根据通知中的注解进行自动代理. -->
	<aop:aspectj-autoproxy></aop:aspectj-autoproxy>
</beans>
```


#### 1.5.4.5 测试


```java
package com.zh.test;

import javax.annotation.Resource;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import com.zh.springaop.service.UserService;

@RunWith(SpringJUnit4ClassRunner.class) // 由SpringJUnit4ClassRunner创建spring容器
@ContextConfiguration("classpath:applicationcontext2.xml") // 指定配置文件位置
public class SpringAOPTest2{
	@Resource(name = "userService") // 从spring容器中取出名为userService的对象注入us变量中
	private UserService us;

	@Test
	public void fun1() {
		us.save();
	}
	//这里省略N行代码
}
```
