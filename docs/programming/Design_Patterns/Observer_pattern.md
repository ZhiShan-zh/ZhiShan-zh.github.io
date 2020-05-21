# 观察者模式

# 1 观察者模式概述

## 1.1 定义

定义了对象之间的一对多依赖，让多个观察者对象同时监听某一个主题对象，当主题对象发生改变的时候，它的所有依赖者都会收到通知并更新。

有时也被称作发布/订阅模式。

## 1.2 优点

1. 复合开闭原则。
1. 可以在运行时建立对象之间的关系。

## 1.3 应用场景

当更改一个对象的状态可能需要更改其他对象，并且实际的对象集事先未知或动态更改时，请使用观察者模式。

## 1.4 源码应用

- `java.util.Observable`
- `org.springframework.context.ApplicationListener`

# 2 入门案例

```java
package com.zh.observer;

import java.util.ArrayList;
import java.util.List;

public class ObserverTest {
	public static void main(String[] args) {
		Subject subject = new Subject();
		Task1 task1 = new Task1();
		subject.addObserver(task1);
		Task2 task2 = new Task2();
		subject.addObserver(task2);
		subject.notifyObserver("xxxx");
		System.out.println("-------------");
		subject.remove(task2);
		subject.notifyObserver("yyyyyy");
	}
}

class Subject{
	//容器
	private List<Observer> container = new ArrayList<>();
	
	//add
	public void addObserver(Observer observer) {
		container.add(observer);
	}
	//remove
	public void remove(Observer observer) {
		container.remove(observer);
	}
	
	public void notifyObserver(Object obj) {
		for(Observer observer:container) {
			observer.update(obj);
		}
	}
}

interface Observer{
	public void update(Object obj);
}

class Task1 implements Observer{

	@Override
	public void update(Object obj) {
		System.out.println("Task1 received:" + obj);
	}
}

class Task2 implements Observer{

	@Override
	public void update(Object obj) {
		System.out.println("Task2 received:" + obj);
	}
	
}
```
