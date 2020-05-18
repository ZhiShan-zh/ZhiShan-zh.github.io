# 1 Java中的SPI规范

# 1 SPI概述

## 1.1 什么是SPI

SPI全称（service provider interface），是JDK内置的一种服务提供发现机制，目前市面上有很多框架都是用它来做服务的扩展发现，如JDBC4中的`java.sql.Driver`的SPI实现(mysql驱动、oracle驱动等)、`common-logging`的日志接口实现、dubbo的扩展实现等等框架；

简单来说，它是一种动态替换发现的机制。举个简单的例子，如果我们定义了一个规范，需要第三方厂商去实现，那么对于我们应用方来说，只需要集成对应厂商的插件，就可以完成对应规范的实现机制，形成一种插拔式的扩展手段。

## 1.2 SPI规范

当服务的提供者，提供了服务接口的一种实现之后，在jar包的`META-INF/services/`目录里同时创建一个以服务接口全路径名称命名的文件，如`java.sql.Driver`文件。该文件里就是实现该服务接口的具体实现类，每一行为一个实现类的全路径名称。而当外部程序装配这个模块的时候，就能通过该jar包`META-INF/services/`里的配置文件找到具体的实现类名，并装载实例化，完成模块的注入。

基于这样一个约定就能很好的找到服务接口的实现类，而不需要再代码里写死指定。

JDK提供服务实现查找的一个工具类为`java.util.ServiceLoader`。

# 2 入门案例

## 2.1 创建普通的Java Project

Java Project的项目名称为：spitest

JDK：这里使用jdk1.8

## 2.2 创建服务接口

```java
package com.zh.spitest;

public interface SPIInterfacce {
	void service();
}
```

## 2.3 编写实现类

实现1:

```java
package com.zh.spitest.impl;

import com.zh.spitest.SPIInterfacce;

public class SPIImplement1 implements SPIInterfacce {

	@Override
	public void service() {
		System.out.println("SPIInterfacce接口的实现1提供服务");
	}
}
```

实现2:

```java
package com.zh.spitest.impl;

import com.zh.spitest.SPIInterfacce;

public class SPIImplement2 implements SPIInterfacce {

	@Override
	public void service() {
		System.out.println("SPIInterfacce接口的实现2提供服务");
	}
}
```

## 2.4 编写SPI规范配置文件

位置：`/spitest/src/META-INF/services/com.zh.spitest.SPIInterfacce`

```
com.zh.spitest.impl.SPIImplement1
com.zh.spitest.impl.SPIImplement2
```

## 2.5 测试SPI

```java
package com.zh.spitest;

import java.util.Iterator;
import java.util.ServiceLoader;

public class SPITest {
	public static void main(String[] args) {
		ServiceLoader<SPIInterfacce> s = ServiceLoader.load(SPIInterfacce.class);
		Iterator<SPIInterfacce> iterator = s.iterator();
		while (iterator.hasNext()) {
			SPIInterfacce spiInterfacce = iterator.next();
			spiInterfacce.service();
		}
	}
}
```

输出：

> SPIInterfacce接口的实现1提供服务

SPIInterfacce接口的实现2提供服务


# 3 SPI规范之路径规范

在`java.util.ServiceLoader`定义了一个私有静态常量来规范路径`private static final String PREFIX = "META-INF/services/";`。

# 4 SPI中实现类的加载时机

ServiceLoader是在内部类迭代器LazyIterator的hasNextService获取实现类的全路径名称，然后在LazyIterator的nextService里边创建实例并返回。

当程序中调用ServiceLoader的静态方法`public static <S> ServiceLoader<S> load(Class<S> service)`来初始化ServiceLoader，具体过程如下：

程序中调用：`ServiceLoader<SPIInterfacce> s = ServiceLoader.load(SPIInterfacce.class);`，load方法获取当前线程的类加载器后调用`public static <S> ServiceLoader<S> load(Class<S> service, ClassLoader loader)`方法

```java
public static <S> ServiceLoader<S> load(Class<S> service) {
        ClassLoader cl = Thread.currentThread().getContextClassLoader();
        return ServiceLoader.load(service, cl);
    }
```

`load(Class<S> service, ClassLoader loader)`方法ServiceLoader构造方法初始化ServiceLoader。

```java
public static <S> ServiceLoader<S> load(Class<S> service, ClassLoader loader)
{
    return new ServiceLoader<>(service, loader);
}
```

ServiceLoader构造方法：

```java
private ServiceLoader(Class<S> svc, ClassLoader cl) {
    //private final Class<S> service;
    service = Objects.requireNonNull(svc, "Service interface cannot be null");
    //private final ClassLoader loader;
    loader = (cl == null) ? ClassLoader.getSystemClassLoader() : cl;
    //private final AccessControlContext acc;
    acc = (System.getSecurityManager() != null) ? AccessController.getContext() : null;
    reload();
}
```

reload方法：

```java
public void reload() {
    //private LinkedHashMap<String,S> providers = new LinkedHashMap<>();
    providers.clear();
    //private LazyIterator lookupIterator;
    lookupIterator = new LazyIterator(service, loader);//初始化内部迭代器类LazyIterator
}
```

当程序调用`Iterator<SPIInterfacce> iterator = s.iterator();`

```java
public Iterator<S> iterator() {
    //返回一个迭代器
    return new Iterator<S>() {

        Iterator<Map.Entry<String,S>> knownProviders
            = providers.entrySet().iterator();

        public boolean hasNext() {
            //如果knownProviders已经初始化，则直接使用
            if (knownProviders.hasNext())
                return true;
            //如果knownProviders没有初始化，则调用ServiceLoader内部迭代器的hasNext()进行获取实现类，并创建实现类的实例，然后把实现类的实例放到knownProviders里边，并返回
            return lookupIterator.hasNext();
        }

        public S next() {
            if (knownProviders.hasNext())
                return knownProviders.next().getValue();
            return lookupIterator.next();
        }

        public void remove() {
            throw new UnsupportedOperationException();
        }

    };
}
```
