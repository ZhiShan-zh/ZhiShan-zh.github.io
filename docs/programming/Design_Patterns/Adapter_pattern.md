# 适配器模式

# 1 适配器模式概述


## 1.1 定义


将一个类的接口转换成客户端希望的另一个接口。Adapter模式使得原本由于接口不兼容而不能一起工作的那些类可以一起工作。


## 1.2 应用场景


- 当你希望使用某些现有类，但其接口与您的其他代码不兼容时，请使用适配器类。
- 当你希望重用几个现有的子类，这些子类缺少一些不能添加到超类中的公共功能时，请使用该模式。



## 1.3 优点


1. 符合单一职责原则
1. 符合开闭原则。



## 1.2 源码中的应用


- `org.springframework.context.event.GenericApplicationListenerAdapter`
- `java.util.Arrays#asList()`
- `java.util.Collections#List()`



# 2 入门案例


## 2.1 对象适配器模式


没有原类的方法。


```java
package com.zh.adapter.v1;

public class AdapterTest1 {
	public static void main(String[] args) {
		Adaptee adaptee = new Adaptee();
		Target target = new Adapter(adaptee);
		target.output5v();
	}
}

class Adaptee{
	public int output220v() {
		return 220;
	}
}

interface Target{
	int output5v();
}

// 对象适配器 Object Adapter
class Adapter implements Target{
	private Adaptee adaptee;
	
	public Adapter(Adaptee adaptee) {
		this.adaptee = adaptee;
	}
	
	@Override
	public int output5v() {
		int output220v = this.adaptee.output220v();
		System.out.println(String.format("原始电压：%d v ——〉 目标电压：%d v", output220v, 5));
		return 5;
	}
	
}
```


## 2.2 类适配器模式


适配器中拥有原类的方法。


```java
package com.zh.adapter.v2;

public class AdapterTest2 {
	public static void main(String[] args) {
		Adapter adapter = new Adapter();
		adapter.output5v();
	}
}

class Adaptee{
	public int output220v() {
		return 220;
	}
}

interface Target{
	int output5v();
}

//类的适配器模式 Class Adapter
class Adapter extends Adaptee implements Target{

	@Override
	public int output5v() {
		int output220v = output220v();
		System.out.println(String.format("原始电压：%d v ——〉 目标电压：%d v", output220v, 5));
		return 5;
	}
	
}
```
