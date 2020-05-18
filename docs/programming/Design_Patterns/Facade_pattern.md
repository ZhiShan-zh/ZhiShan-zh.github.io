# 门面模式

# 1 门面模式概述

## 1.1 定义

为子系统中的一组接口提供一个一致的接口，Facade模式定义了一个高层接口，这个接口使得这一子系统更容易使用。

## 1.2 应用场景

1. 当您需要使用复杂子系统的有限但直接的接口时，请使用Facade模式。
1. 当您想要将子系统组织成层时，请使用Facade。

## 1.3 优点

简化客户端的调用

## 1.4 源码中的应用

- `org.apache.catalina.connector.RequestFacade`

# 2 入门案例

```java
package com.zh.facade;

public class FacadeTest {
	public static void main(String[] args) {
		Client client = new Client();
		client.doSomething();
	}
}

class Client{
	Facade facade = new Facade();
	public void doSomething() {
		facade.doSomethingFacade();
	}
}

class Facade{
	SubSystem1 subSystem1 = new SubSystem1();
	SubSystem2 subSystem2 = new SubSystem2();
	SubSystem3 subSystem3 = new SubSystem3();
	
	public void doSomethingFacade() {
		subSystem1.method1();
		subSystem2.method2();
		subSystem3.method3();
	}
}

class SubSystem1{
	public void method1() {
		System.out.println("SubSystem1.method1 executed!");
	}
}

class SubSystem2{
	public void method2() {
		System.out.println("SubSystem2.method2 executed!");
	}
}

class SubSystem3{
	public void method3() {
		System.out.println("SubSystem3.method3 executed!");
	}
}
```
