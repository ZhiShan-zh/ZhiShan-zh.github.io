# 装饰者模式

# 1 装饰者模式概述

## 1.1 定义

在不改变原有对象的基础上，将功能附加到对象上。

## 1.2 优点

1. 不改变原有对象的情况下给一个对象扩展功能。
1. 使用不同的组合可以实现不同的效果。
1. 复合开闭原则。

## 1.3 应用场景

扩展一个类的功能或给一个类添加附加职责

## 1.4 源码应用

- `javax.servlet.http.HttpServletRequestWrapper`
- `javax.servlet.http.HttpServletResponseWrapper`

# 2 入门案例

```java
package com.zh.decorator;

public class DecoratorTest {
	//单层装饰
	public static void main1(String[] args) {
		Component component = new ConcreteDecorator(new ConcreteComponent());
		component.operation();
	}
	//多层装饰
	public static void main(String[] args) {
		Component component = new ConcreteDecorator2(new ConcreteDecorator(new ConcreteComponent()));
		component.operation();
	}
}

interface Component{
	void operation();
}

class ConcreteComponent implements Component{

	@Override
	public void operation() {
		System.out.println("拍照");
	}
}

abstract class Decorator implements Component{
	Component component;

	public Decorator(Component component) {
		super();
		this.component = component;
	}
}

class ConcreteDecorator extends Decorator{

	public ConcreteDecorator(Component component) {
		super(component);
	}

	@Override
	public void operation() {
		component.operation();
		System.out.println("添加美颜");
	}
	
}

class ConcreteDecorator2 extends Decorator{

	public ConcreteDecorator2(Component component) {
		super(component);
	}

	@Override
	public void operation() {
		component.operation();
		System.out.println("添加滤镜");
	}
	
}
```
