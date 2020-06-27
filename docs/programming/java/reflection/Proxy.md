# JDK动态代理API

# 1 概述

`java.lang.reflect.Proxy`类提供了用于创建动态代理类和实例的静态方法，它也是由这些方法创建的所有动态代理类的超类。

`java.lang.reflect.Proxy`类的声明为：

```java
public class Proxy
   extends Object
      implements Serializable
```

`java.lang.reflect.InvocationHandler`接口是proxy代理实例的调用处理程序实现的一个接口，每一个proxy代理实例都有一个关联的调用处理程序；在代理实例调用方法时，方法调用被编码分派到调用处理程序的invoke方法。

每一个动态代理类的调用处理程序都必须实现InvocationHandler接口，并且每个代理类的实例都关联到了实现该接口的动态代理类调用处理程序中，当我们通过动态代理对象调用一个方法时候，这个方法的调用就会被转发到实现InvocationHandler接口类的invoke方法来调用。
```java
package java.lang.reflect;
public interface InvocationHandler {
	/**
	* proxy:代理类代理的真实代理对象com.sun.proxy.$Proxy0
    * method:我们所要调用某个对象真实的方法的Method对象
    * args:指代代理对象方法传递的参数
	*/
    public Object invoke(Object proxy, Method method, Object[] args)
        throws Throwable;
}
```



# 2 `java.lang.reflect.Proxy`类字段

`protected InvocationHandler h`：此代理实例的调用处理程序。

# 3 `java.lang.reflect.Proxy`类方法

| 方法                                                         | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `static InvocationHandler getInvocationHandler(Object proxy)` | 返回指定代理实例的调用处理程序。<br />参数**proxy** - 返回调用处理程序的代理实例。 |
| `static Class<?> getProxyClass(ClassLoader loader, Class<?>... interfaces)` | 在给定类加载器和接口数组的情况下返回代理类的`java.lang.Class`对象。 代理类将由指定的类加载器定义，并将实现所有提供的接口。 如果类加载器已经定义了相同的接口排列的代理类，那么将返回现有的代理类; 否则，将动态生成这些接口的代理类，并由类加载器定义。 |
| `static boolean isProxyClass(Class<?> cl)`                   | 当且仅当使用getProxyClass方法或newProxyInstance方法动态生成指定的类作为代理类时，才返回true。<br />参数**cl** - 要测试的类 |
| `static Object newProxyInstance(ClassLoader loader, Class<?>[] interfaces, InvocationHandler h)` | 返回指定接口的代理类的实例，该接口将方法调用分派给指定的调用处理程序。<br />参数**loader** - 用于定义代理类的类加载器。<br />参数**interfaces** - 要实现的代理类的接口列表。<br />参数**h** - 调度方法调用的调用处理程序。 |

# 4 JDK动态代理使用

```java
package com.zh.proxytest.jdkproxy.dao;

public interface UserDao {
	void save();

	void delete();

	void update();

	void find();
}
```

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

