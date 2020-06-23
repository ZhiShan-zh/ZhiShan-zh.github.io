# 抽象工厂模式

# 1 抽象工厂模式概述


## 1.1 定义

提供一个创建一系列相关或相互依赖对象的接口，而无须指定它们具体的类。

## 1.2 应用场景

程序需要处理不同系列的相关产品，但是您不希望它依赖于这些产品的具体类时，可以使用抽象工厂。

## 1.3 优点


1. 可以确信你从工厂得到的产品彼此是兼容的。
1. 可以避免具体产品和客户端代码之间的紧密耦合。
1. 符合单一职责原则。
1. 符合开闭原则。
   1. 开：是指对于组件功能的扩展是开放的，是允许对其进行功能扩展的。
   1. 闭：是指对于原有代码的修改是封闭的，即不应该修改原有的代码。



## 1.4 源码中的应用


- `java.sql.Connection`
- `java.sql.Driver`



# 2 入门案例


```java
package com.zh.abstractfactory;

public class AbstractFactoryTest {
	public static void main(String[] args) {
		IDatabaseUtils iDatabaseUtils = new MysqlDatabaseUtils();
		IConnect connect = iDatabaseUtils.getConnect();
		connect.connect();
		ICommand command = iDatabaseUtils.getCommand();
		command.command();
	}
}

//抽象接口
interface IConnect{
	void connect();
}

interface ICommand{
	void command();
}

interface IDatabaseUtils{
	IConnect getConnect();
	ICommand getCommand();
}

//Mysql
class MysqlConnect implements IConnect{

	@Override
	public void connect() {
		System.out.println("Mysql connected!");
	}
	
}

class MysqlCommand implements ICommand{

	@Override
	public void command() {
		System.out.println("Mysql command!");
	}
}

class MysqlDatabaseUtils implements IDatabaseUtils{

	@Override
	public IConnect getConnect() {
		return new MysqlConnect();
	}

	@Override
	public ICommand getCommand() {
		return new MysqlCommand();
	}
	
}

//Oracle
class OracleConnect implements IConnect{

	@Override
	public void connect() {
		System.out.println("Oracle connected!");
	}
}

class OracleCommand implements ICommand{

	@Override
	public void command() {
		System.out.println("Oracle command!");
	}
}

class OracleDatabaseUtils implements IDatabaseUtils{

	@Override
	public IConnect getConnect() {
		return new OracleConnect();
	}

	@Override
	public ICommand getCommand() {
		return new OracleCommand();
	}	
}
```
