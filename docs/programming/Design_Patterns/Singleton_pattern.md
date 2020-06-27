# 单例设计模式

# 1 单例设计模式概述
## 1.1 模式定义
保证一个类只有一个实例，并且提供一个全局访问点
## 1.2 应用场景
- 重量级的对象，不需要多个实例，如线程池，数据库连接池。
- 共享状态给多个目标，需要单实例。

# 2 实现模式
## 2.1 懒汉模式

### 2.1.1 定义
延迟加载，只有在真正使用的时候，才开始实例化。
### 2.1.2 单线程模式
```java
package com.zh.singletonpattern.lazysingleton;

public class LazySingletonTest {	
	/**
	 * 单线程测试单例懒汉模式
	 * 打印结果为：true
	 */
	public static void main1(String[] args) {
		LazySingleton instance = LazySingleton.getInstance();
		LazySingleton instance2 = LazySingleton.getInstance();
		System.out.println(instance == instance2);
	}
}

class LazySingleton{
	private static LazySingleton instance;

	private LazySingleton() {
	}
	/**
	 * 配合单线程测试，没有休眠
	 * @return
	 */
	public static LazySingleton getInstance() {
		if(instance == null) instance = new LazySingleton();
		return instance;
	}
}
```

### 2.1.3 多线程情况下需要加锁

```java
package com.zh.singletonpattern.lazysingleton;

public class LazySingletonTest {
	
	/**
	 * 单线程测试单例懒汉模式
	 * 打印结果为：true
	 */
	public static void main1(String[] args) {
		LazySingleton instance = LazySingleton.getInstance();
		LazySingleton instance2 = LazySingleton.getInstance();
		System.out.println(instance == instance2);
	}
	
	/**
	 * 多线程测试单例懒汉模式
	 * 运行结果：
	 * com.zh.singletonpattern.lazysingleton.LazySingleton@25531342
	 * com.zh.singletonpattern.lazysingleton.LazySingleton@1be7a5f
	 */
	public static void main2(String[] args) {
		new Thread(()->{
			LazySingleton instance = LazySingleton.getInstance2();
			System.out.println(instance);
		}).start();
		new Thread(()->{
			LazySingleton instance = LazySingleton.getInstance2();
			System.out.println(instance);
		}).start();
	}
	
	/**
	 * 多线程测试单例懒汉模式，有synchronized关键修饰方法
	 * 运行结果：
	 * com.zh.singletonpattern.lazysingleton.LazySingleton@50ae6479
	 * com.zh.singletonpattern.lazysingleton.LazySingleton@50ae6479
	 */
	public static void main3(String[] args) {
		new Thread(()->{
			LazySingleton instance = LazySingleton.getInstance3();
			System.out.println(instance);
		}).start();
		new Thread(()->{
			LazySingleton instance = LazySingleton.getInstance3();
			System.out.println(instance);
		}).start();
	}
	
	/**
	 * 多线程测试单例懒汉模式，细粒度加锁优化
	 * 运行结果：
	 * com.zh.singletonpattern.lazysingleton.LazySingleton@3f51bb76
	 * com.zh.singletonpattern.lazysingleton.LazySingleton@3f51bb76
	 */
	public static void main(String[] args) {
		new Thread(()->{
			LazySingleton instance = LazySingleton.getInstance4();
			System.out.println(instance);
		}).start();
		new Thread(()->{
			LazySingleton instance = LazySingleton.getInstance4();
			System.out.println(instance);
		}).start();
	}
}

class LazySingleton{
	private static LazySingleton instance;

	private LazySingleton() {
	}
	/**
	 * 配合单线程测试，没有休眠
	 * @return
	 */
	public static LazySingleton getInstance() {
		if(instance == null) instance = new LazySingleton();
		return instance;
	}
	/**
	 * 配合多线程测试，有休眠
	 * @return
	 */
	public static LazySingleton getInstance2() {
		if(instance == null) {
			try {
				Thread.sleep(200);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			instance = new LazySingleton();
		}
		return instance;
	}
	
	/**
	 * 配合多线程测试，有休眠，有synchronized关键字修饰方法
	 * @return
	 */
	public synchronized static LazySingleton getInstance3() {
		if(instance == null) {
			try {
				Thread.sleep(200);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			instance = new LazySingleton();
		}
		return instance;
	}
	
	/**
	 * 配合多线程测试，有休眠，进行细粒度加锁优化(double check 加锁优化)
	 * @return
	 */
	public static LazySingleton getInstance4() {
		if(instance == null) {
			synchronized(LazySingleton.class) {
				if(instance == null) instance = new LazySingleton();
			}
		}
		return instance;
	}
}
```

### 2.1.4 编译器（JIT），CPU有可能对指令进程重排序问题
编译器（JIT），CPU有可能对指令进程重排序，导致使用到尚未实例化的实例，可以通过添加volatile关键字进行修饰，对于volatile修饰的字段，可以防止指令重排。
#### 2.1.4.1 指令重排
多条汇编指令执行时, 考虑性能因素, 会导致执行乱序。

`Demo demo = new Demo();`此代码字解码层面需要完成：

1. 分配空间
1. 初始化
1. 引用赋值

其实JVM在执行上述代码的时候，考虑到性能因素，会进行指令重排，第2步和第3步可能颠倒过来。

```java
package com.zh.singletonpattern.lazysingleton;

public class Demo {
	public static void main(String[] args) {
		Demo demo = new Demo();
	}
}
```
```shell
[zh@zh-pc lazysingleton]$ javap -v Demo.class 
Classfile /run/media/zh/data/projects/sts_workspace/designpatterns/singletonpattern/target/classes/com/zh/singletonpattern/lazysingleton/Demo.class
  Last modified Mar 11, 2020; size 465 bytes
  MD5 checksum 93481d8996ed7415cd315583a487e6b4
  Compiled from "Demo.java"
public class com.zh.singletonpattern.lazysingleton.Demo
  minor version: 0（zh注解：java的版本）
  major version: 52
  flags: ACC_PUBLIC, ACC_SUPER（zh注解：访问修饰符）
Constant pool:（zh注解：常量池信息）
   #1 = Class              #2             // com/zh/singletonpattern/lazysingleton/Demo
   #2 = Utf8               com/zh/singletonpattern/lazysingleton/Demo
   #3 = Class              #4             // java/lang/Object
   #4 = Utf8               java/lang/Object
   #5 = Utf8               <init>
   #6 = Utf8               ()V
   #7 = Utf8               Code
   #8 = Methodref          #3.#9          // java/lang/Object."<init>":()V
   #9 = NameAndType        #5:#6          // "<init>":()V
  #10 = Utf8               LineNumberTable
  #11 = Utf8               LocalVariableTable
  #12 = Utf8               this
  #13 = Utf8               Lcom/zh/singletonpattern/lazysingleton/Demo;
  #14 = Utf8               main
  #15 = Utf8               ([Ljava/lang/String;)V
  #16 = Methodref          #1.#9          // com/zh/singletonpattern/lazysingleton/Demo."<init>":()V
  #17 = Utf8               args
  #18 = Utf8               [Ljava/lang/String;
  #19 = Utf8               demo
  #20 = Utf8               SourceFile
  #21 = Utf8               Demo.java
{
  public com.zh.singletonpattern.lazysingleton.Demo();（zh注解：JVM生成的默认构造函数）
    descriptor: ()V（zh注解：修饰符是不接收任何参数，返回为空）
    flags: ACC_PUBLIC
    Code:
      stack=1, locals=1, args_size=1
         0: aload_0
         1: invokespecial #8                  // Method java/lang/Object."<init>":()V
         4: return
      LineNumberTable:
        line 3: 0
      LocalVariableTable:
        Start  Length  Slot  Name   Signature
            0       5     0  this   Lcom/zh/singletonpattern/lazysingleton/Demo;

  public static void main(java.lang.String[]);（zh注解：main函数）
    descriptor: ([Ljava/lang/String;)V
    flags: ACC_PUBLIC, ACC_STATIC
    Code:
      stack=2, locals=2, args_size=1
         0: new           #1 （zh注解：#1为常量池索引）  // class com/zh/singletonpattern/lazysingleton/Demo
         3: dup（zh注解：将操作数栈定的数据复制一份，并压入栈）
         4: invokespecial #16  （zh注解：调用初始化方法） // Method "<init>":()V
         7: astore_1（zh注解：变量赋值）
         8: return
      LineNumberTable:
        line 5: 0
        line 6: 8
      LocalVariableTable:
        Start  Length  Slot  Name   Signature
            0       9     0  args   [Ljava/lang/String;
            8       1     1  demo   Lcom/zh/singletonpattern/lazysingleton/Demo;
}
SourceFile: "Demo.java"
```

#### 2.1.4.2 指令重排导致多线程下单例懒汉模式下的问题

1. 如果线程1调用`LazySingleton.getInstance4()`的时候，执行到标号1代码，这是如果（instance=null），则线程1就会进入if内部。
1. 线程1执行标号2代码，获取到锁，进入同步代码块，并执行标号3代码，如果此时instance还是null，则会执行标号4代码，如果此时标号4代码在字解码层面进行了指令重排，先分配了空间，然后进行到引用赋值。如果此时线程2调用`LazySingleton.getInstance4()`，执行到标号1代码，因为上边线程1已经进行了引用赋值，所以此时的instance不为null，则不会进入if内部，而会直接执行标号5代码，返回instance。此时呢线程1还没有完成初始化，则此时会发生空指针的问题。
```java
package com.zh.singletonpattern.lazysingleton;

public class LazySingletonTest {
	/**
	 * 多线程测试单例懒汉模式，细粒度加锁优化
	 * 运行结果：
	 * com.zh.singletonpattern.lazysingleton.LazySingleton@3f51bb76
	 * com.zh.singletonpattern.lazysingleton.LazySingleton@3f51bb76
	 */
	public static void main(String[] args) {
		new Thread(()->{//线程1
			LazySingleton instance = LazySingleton.getInstance4();
			System.out.println(instance);
		}).start();
		new Thread(()->{//线程2
			LazySingleton instance = LazySingleton.getInstance4();
			System.out.println(instance);
		}).start();
	}
}

class LazySingleton{
	private static LazySingleton instance;

	private LazySingleton() {
	}
	/**
	 * 配合多线程测试，有休眠，进行细粒度加锁优化
	 * @return
	 */
	public static LazySingleton getInstance4() {
		if(instance == null) {//标号1
			synchronized(LazySingleton.class) {//标号2
				if(instance == null) //标号3
                    instance = new LazySingleton();//标号4
			}
		}
		return instance;//标号5
	}
}
```

#### 2.1.4.3 使用volatile关键字解决重排序问题
volatile关键字的一个作用就是禁止进行指令重排序。（实现有序性）。

```java
package com.zh.singletonpattern.lazysingleton;

public class LazyVolatileSingletonTest {
	public static void main(String[] args) {
		new Thread(()->{
			LazyVolatileSingleton instance = LazyVolatileSingleton.getInstance();
			System.out.println(instance);
		}).start();
		new Thread(()->{
			LazyVolatileSingleton instance = LazyVolatileSingleton.getInstance();
			System.out.println(instance);
		}).start();
	}
}

class LazyVolatileSingleton{
	private volatile static LazyVolatileSingleton instance;

	private LazyVolatileSingleton() {
	}

	public static LazyVolatileSingleton getInstance() {
		if(instance == null) {
			synchronized(LazyVolatileSingleton.class) {
				if(instance == null) instance = new LazyVolatileSingleton();
			}
		}
		return instance;
	}
}
```

## 2.2 饿汉模式
### 2.2.1 定义
类加载的初始化阶段（参见：[https://www.yuque.com/zhishan/bttt5g/xg3ixg](https://www.yuque.com/zhishan/bttt5g/xg3ixg)）完成了实例化的初始化。本质上就是借助于JVM类加载机制，保证实例的唯一性。

因为直接创建了对象，在获取对象的时候不需要再创建，故为线程安全的。

### 2.2.2 实现代码

```java
package com.zh.singletonpattern.hungrysingleton;

public class HungrySingletonTest {
	/**
	 * 输出结果：true
	 * @param args
	 */
	public static void main(String[] args) {
		HungrySingleton instance = HungrySingleton.getinstance();
		HungrySingleton instance2 = HungrySingleton.getinstance();
		System.out.println(instance == instance2);
	}
}

class HungrySingleton{
	private static HungrySingleton instance = new HungrySingleton();
	
	private HungrySingleton() {};
	
	public static HungrySingleton getinstance() {
		return instance;
	}
}
```

### 2.2.3 使用反射方式攻击

```java
package com.zh.singletonpattern.hungrysingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class HungrySingletonTest {
	/**
	 * 使用反射方式攻击
	 * @param args
	 * @throws NoSuchMethodException
	 * @throws SecurityException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws IllegalArgumentException
	 * @throws InvocationTargetException
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<HungrySingleton> declaredConstructor = HungrySingleton.class.getDeclaredConstructor();
		declaredConstructor.setAccessible(true);
		HungrySingleton hungrySingleton = declaredConstructor.newInstance();
		HungrySingleton instance = hungrySingleton.getinstance();
		System.out.println(hungrySingleton == instance);
	}
}

class HungrySingleton{
	private static HungrySingleton instance = new HungrySingleton();
	
	private HungrySingleton() {};
	
	public static HungrySingleton getinstance() {
		return instance;
	}
}
```
输出：false            

### 2.2.4 解决反射方式获取存在的问题

```java
package com.zh.singletonpattern.hungrysingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class HungrySingletonTest {
	/**
	 * 使用反射方式攻击
	 * @param args
	 * @throws NoSuchMethodException
	 * @throws SecurityException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws IllegalArgumentException
	 * @throws InvocationTargetException
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<HungrySingleton> declaredConstructor = HungrySingleton.class.getDeclaredConstructor();
		declaredConstructor.setAccessible(true);
		HungrySingleton hungrySingleton = declaredConstructor.newInstance();
		HungrySingleton instance = hungrySingleton.getinstance();
		System.out.println(hungrySingleton == instance);
	}
}

class HungrySingleton{
	private static HungrySingleton instance = new HungrySingleton();
	
	private HungrySingleton() {
		//解决反射方式攻击
		if(instance != null)
			throw new RuntimeException("单例模式不允许多个实例！");
	};
	
	public static HungrySingleton getinstance() {
		return instance;
	}
}
```
输出：

```
Exception in thread "main" java.lang.reflect.InvocationTargetException
 at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
 at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
 at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
 at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
 at com.zh.singletonpattern.hungrysingleton.HungrySingletonTest.main(HungrySingletonTest.java:30)
Caused by: java.lang.RuntimeException: 单例模式不允许多个实例！
 at com.zh.singletonpattern.hungrysingleton.HungrySingleton.<init>(HungrySingletonTest.java:42)
... 5 more
```



## 2.3 静态内部类

1. 本质上是利用类的加载机制来保证线程安全。
1. 只有在实际使用的时候，才会触发类的初始化，所以也是懒加载的一种形式。

### 2.3.1 单线程模式

```java
package com.zh.singletonpattern.innerclasssingleton;

public class InnerClassSingletonTest {
	public static void main(String[] args) {
		InnerClassSingleton instance = InnerClassSingleton.getInstance();
		InnerClassSingleton instance2 = InnerClassSingleton.getInstance();
		System.out.println(instance == instance2);
	}
}

class InnerClassSingleton{
	private static class InnerClassHolder{
		private static InnerClassSingleton instance = new InnerClassSingleton();
	}
	private InnerClassSingleton() {};
	
	public static InnerClassSingleton getInstance() {
		return InnerClassHolder.instance;
	}
}
```
程序输出：true                   

### 2.3.2 多线程模式

```java
package com.zh.singletonpattern.innerclasssingleton;

public class InnerClassSingletonTest {
	public static void main(String[] args) {
		new Thread(()->{
			InnerClassSingleton instance = InnerClassSingleton.getInstance();
			System.out.println(instance);
		}).start();
		
		new Thread(()->{
			InnerClassSingleton instance = InnerClassSingleton.getInstance();
			System.out.println(instance);
		}).start();
	}
}

class InnerClassSingleton{
	private static class InnerClassHolder{
		private static InnerClassSingleton instance = new InnerClassSingleton();
	}
	private InnerClassSingleton() {};
	
	public static InnerClassSingleton getInstance() {
		return InnerClassHolder.instance;
	}
}
```
输出：

```
com.zh.singletonpattern.innerclasssingleton.InnerClassSingleton@77dba4f                    
com.zh.singletonpattern.innerclasssingleton.InnerClassSingleton@77dba4f                    
```

### 2.3.3 反射方式攻击

```java
package com.zh.singletonpattern.innerclasssingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class InnerClassSingletonTest {
	/**
	 * 反射获取
	 * @param args
	 * @throws SecurityException 
	 * @throws NoSuchMethodException 
	 * @throws InvocationTargetException 
	 * @throws IllegalArgumentException 
	 * @throws IllegalAccessException 
	 * @throws InstantiationException 
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<InnerClassSingleton> declaredConstructor = InnerClassSingleton.class.getDeclaredConstructor();
		declaredConstructor.setAccessible(true);//获取访问权
		//使用反射的方式创建一个对象
		InnerClassSingleton innerClassSingleton = declaredConstructor.newInstance();
		//使用类中提供的方法获取一个对象
		InnerClassSingleton instance = innerClassSingleton.getInstance();
		System.out.println(innerClassSingleton == instance);
	}
}

class InnerClassSingleton{
	private static class InnerClassHolder{
		private static InnerClassSingleton instance = new InnerClassSingleton();
	}
	private InnerClassSingleton() {};
	
	public static InnerClassSingleton getInstance() {
		return InnerClassHolder.instance;
	}
}
```
输出：false            

### 2.3.4 解决反射方式获取存在的问题

```java
package com.zh.singletonpattern.innerclasssingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class InnerClassSingletonTest {
	/**
	 * 反射获取
	 * @param args
	 * @throws SecurityException 
	 * @throws NoSuchMethodException 
	 * @throws InvocationTargetException 
	 * @throws IllegalArgumentException 
	 * @throws IllegalAccessException 
	 * @throws InstantiationException 
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<InnerClassSingleton> declaredConstructor = InnerClassSingleton.class.getDeclaredConstructor();
		declaredConstructor.setAccessible(true);//获取访问权
		//使用反射的方式创建一个对象
		InnerClassSingleton innerClassSingleton = declaredConstructor.newInstance();
		//使用类中提供的方法获取一个对象
		InnerClassSingleton instance = innerClassSingleton.getInstance();
		System.out.println(innerClassSingleton == instance);
	}
}

class InnerClassSingleton{
	private static class InnerClassHolder{
		private static InnerClassSingleton instance = new InnerClassSingleton();
	}
	private InnerClassSingleton() {
		//解决反射方式攻击
		if(InnerClassHolder.instance != null) 
			throw new RuntimeException("单例模式不允许多个实例！");
	};
	
	public static InnerClassSingleton getInstance() {
		return InnerClassHolder.instance;
	}
}
```
输出：

```
Exception in thread "main" java.lang.reflect.InvocationTargetException
at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
at com.zh.singletonpattern.innerclasssingleton.InnerClassSingletonTest.main(InnerClassSingletonTest.java:49)        
Caused by: java.lang.RuntimeException: 单例模式不允许多个实例！
at com.zh.singletonpattern.innerclasssingleton.InnerClassSingleton.<init>(InnerClassSingletonTest.java:63)
... 5 more
```

## 2.4 使用final方式
### 2.4.1 通过反射攻破final单例模式

```java
package com.zh.singletonpattern.finalsingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class FinalSingletonTest {
	/**
	 * 通过反射获取实例
	 * 输出：false
	 * @param args
	 * @throws NoSuchMethodException
	 * @throws SecurityException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws IllegalArgumentException
	 * @throws InvocationTargetException
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<FinalSingleton> declaredConstructor = FinalSingleton.class.getDeclaredConstructor();
		declaredConstructor.setAccessible(true);
		FinalSingleton newInstance = declaredConstructor.newInstance();
		FinalSingleton instance = newInstance.instance;
		System.out.println(newInstance == instance);
	}
}

class FinalSingleton{
	public static final FinalSingleton instance = new FinalSingleton();
	private FinalSingleton() {};
}
```

### 2.4.2 解决反射方式攻破final模式的单例模式

```java
package com.zh.singletonpattern.finalsingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class FinalSingletonTest {
	/**
	 * 通过反射获取实例
	 * 输出：false
	 * @param args
	 * @throws NoSuchMethodException
	 * @throws SecurityException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws IllegalArgumentException
	 * @throws InvocationTargetException
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<FinalSingleton> declaredConstructor = FinalSingleton.class.getDeclaredConstructor();
		declaredConstructor.setAccessible(true);
		FinalSingleton newInstance = declaredConstructor.newInstance();
		FinalSingleton instance = newInstance.instance;
		System.out.println(newInstance == instance);
	}
}

class FinalSingleton{
	public static final FinalSingleton instance = new FinalSingleton();
	private FinalSingleton() {
		//解决反射模式暴力创建实例
		if(instance != null) 
			throw new RuntimeException("单例模式不允许多个实例！");
	};
}
```
输出：

```
Exception in thread "main" java.lang.reflect.InvocationTargetException
at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
at com.zh.singletonpattern.finalsingleton.FinalSingletonTest.main(FinalSingletonTest.java:21)<br />Caused by: java.lang.RuntimeException: 单例模式不允许多个实例！
at com.zh.singletonpattern.finalsingleton.FinalSingleton.<init>(FinalSingletonTest.java:32)
... 5 more
```

### 2.4.3 反序列化方式攻破final单例模式
解决方案参见:《[2.6 反序列化攻破](https://www.yuque.com/zhishan/bttt5g/oqd3df/edit#6yQWL)》

## 2.5 登记式
### 2.5.1 登记式一般形式

```java
package com.zh.singletonpattern.registrationsingleton;

import java.util.HashMap;
import java.util.Map;

public class RegistrationSingletonTest {
	public static void main(String[] args) {
		RegistrationSingleton instance = RegistrationSingleton.getInstance(null);
		RegistrationSingleton instance2 = RegistrationSingleton.getInstance(null);
		System.out.println(instance == instance2);
	}
}

class RegistrationSingleton{
	private static Map<String, RegistrationSingleton> map = new HashMap<>();
	static {
		RegistrationSingleton instance = new RegistrationSingleton();
		map.put(instance.getClass().getName(), instance);
	}
	protected RegistrationSingleton() {}
	public static RegistrationSingleton getInstance(String name) {
		if(name == null) name = RegistrationSingleton.class.getName();
		RegistrationSingleton instance = map.get(name);
		if(instance == null) {
			try {
				instance = (RegistrationSingleton) Class.forName(name).newInstance();
				map.put(name, instance);
			} catch (InstantiationException e) {
				e.printStackTrace();
			} catch (IllegalAccessException e) {
				e.printStackTrace();
			} catch (ClassNotFoundException e) {
				e.printStackTrace();
			}
		}
		return instance;
		
	}
}
```
输出：true            

### 2.5.2 反射方式攻破注册式单例一般式

```java
package com.zh.singletonpattern.registrationsingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.Map;

public class RegistrationSingletonTest {
	/**
	 * 测试登记式
	 * 输出：true
	 * @param args
	 */
	public static void main1(String[] args) {
		RegistrationSingleton instance = RegistrationSingleton.getInstance(null);
		RegistrationSingleton instance2 = RegistrationSingleton.getInstance(null);
		System.out.println(instance == instance2);
	}
	
	/**
	 * 反射方式测试注册式单例模式
	 * 输出：false
	 * @param args
	 * @throws NoSuchMethodException
	 * @throws SecurityException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws IllegalArgumentException
	 * @throws InvocationTargetException
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<RegistrationSingleton> declaredConstructor = RegistrationSingleton.class.getDeclaredConstructor();
		declaredConstructor.setAccessible(true);
		RegistrationSingleton newInstance = declaredConstructor.newInstance();
		RegistrationSingleton instance = newInstance.getInstance(null);
		System.out.println(newInstance == instance);
	}
}

class RegistrationSingleton{
	private static Map<String, RegistrationSingleton> map = new HashMap<>();
	static {
		RegistrationSingleton instance = new RegistrationSingleton();
		map.put(instance.getClass().getName(), instance);
	}
	protected RegistrationSingleton() {}
	public static RegistrationSingleton getInstance(String name) {
		if(name == null) name = RegistrationSingleton.class.getName();
		RegistrationSingleton instance = map.get(name);
		if(instance == null) {
			try {
				instance = (RegistrationSingleton) Class.forName(name).newInstance();
				map.put(name, instance);
			} catch (InstantiationException e) {
				e.printStackTrace();
			} catch (IllegalAccessException e) {
				e.printStackTrace();
			} catch (ClassNotFoundException e) {
				e.printStackTrace();
			}
		}
		return instance;
		
	}
}
```
输出：false        

### 2.5.3 解决注册式一般式可以被反射攻破的问题

```java
package com.zh.singletonpattern.registrationsingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.util.HashMap;
import java.util.Map;

public class RegistrationSingletonTest {
	/**
	 * 反射方式测试注册式单例模式
	 * 输出：false
	 * @param args
	 * @throws NoSuchMethodException
	 * @throws SecurityException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws IllegalArgumentException
	 * @throws InvocationTargetException
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<RegistrationSingleton> declaredConstructor = RegistrationSingleton.class.getDeclaredConstructor();
		declaredConstructor.setAccessible(true);
		RegistrationSingleton newInstance = declaredConstructor.newInstance();
		RegistrationSingleton instance = newInstance.getInstance(null);
		System.out.println(newInstance == instance);
	}
}

class RegistrationSingleton{
	private static Map<String, RegistrationSingleton> map = new HashMap<>();
	static {
		RegistrationSingleton instance = new RegistrationSingleton();
		map.put(instance.getClass().getName(), instance);
	}
	protected RegistrationSingleton() {
		//解决反射暴力创建对象实例的问题
		if(RegistrationSingleton.getInstance(null) != null)
			throw new RuntimeException("单例模式不允许多个实例");
	}
	public static RegistrationSingleton getInstance(String name) {
		if(name == null) name = RegistrationSingleton.class.getName();
		RegistrationSingleton instance = map.get(name);
		if(instance == null) {
			try {
				instance = (RegistrationSingleton) Class.forName(name).newInstance();
				map.put(name, instance);
			} catch (InstantiationException e) {
				e.printStackTrace();
			} catch (IllegalAccessException e) {
				e.printStackTrace();
			} catch (ClassNotFoundException e) {
				e.printStackTrace();
			}
		}
		return instance;
		
	}
}
```
输出：

```
Exception in thread "main" java.lang.StackOverflowError
at java.lang.ReflectiveOperationException.<init>(ReflectiveOperationException.java:89)
at java.lang.reflect.InvocationTargetException.<init>(InvocationTargetException.java:72)
at sun.reflect.GeneratedConstructorAccessor1.newInstance(Unknown Source)
at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
at java.lang.Class.newInstance(Class.java:442)

```

### 2.5.4 反序列化方式攻破注册式单例模式

解决方案参见:《[2.6 反序列化攻破](https://www.yuque.com/zhishan/bttt5g/oqd3df/edit#6yQWL)》

## 2.6 反序列化攻破
### 2.6.1 序列化反序列化方式攻击

```java
package com.zh.singletonpattern.innerclasssingleton;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class InnerClassSingletonTest {
	/**
	 * 序列化反序列方式获取单例模式对象
	 * @param args
	 * @throws FileNotFoundException
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	public static void main(String[] args) throws FileNotFoundException, IOException, ClassNotFoundException {
		InnerClassSingleton instance = InnerClassSingleton.getInstance();
		ObjectOutputStream objectOutputStream = new ObjectOutputStream(new FileOutputStream("testSerializable"));
		objectOutputStream.writeObject(instance);
		objectOutputStream.close();
		
		ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream("testSerializable"));
		InnerClassSingleton objectClassSingleton = (InnerClassSingleton) objectInputStream.readObject();
		objectInputStream.close();
		
		System.out.println(instance == objectClassSingleton);
		
	}
}

class InnerClassSingleton implements Serializable{
	private static class InnerClassHolder{
		private static InnerClassSingleton instance = new InnerClassSingleton();
	}
	private InnerClassSingleton() {
		//解决反射方式攻击
		if(InnerClassHolder.instance != null) 
			throw new RuntimeException("单例模式不允许多个实例！");
	};
	
	public static InnerClassSingleton getInstance() {
		return InnerClassHolder.instance;
	}
}
```
输出：false    

### 2.6.2 解决反序列化获取对象攻破单例模式的问题
解决方案：

- 使用`java.io.Serializable`接口说明中提供的解决方案，方式反序列化获取的对象攻破单例模式
   - 可序列化类中提供`Object readResolve() throws ObjectStreamException`方法
   - 注意一定要序列化的一定要加上版本好，不然在序列化的时候JVM会会根据这个Class有关信息自动生成一个版本号，并把这个版本号存到序列化文件中。然后在反序列化的时候再根据这个Class生成一个序列号，再用这个序列号和序列化文件中的版本号进行对比，如果两个版本号不一致，就会报错。如果加上了版本号，只要没有改动这个版本号，JVM就不会报错。

```java
package com.zh.singletonpattern.innerclasssingleton;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.ObjectStreamException;
import java.io.Serializable;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class InnerClassSingletonTest {
	/**
	 * 序列化反序列方式获取单例模式对象
	 * @param args
	 * @throws FileNotFoundException
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	public static void main(String[] args) throws FileNotFoundException, IOException, ClassNotFoundException {
		InnerClassSingleton instance = InnerClassSingleton.getInstance();
		ObjectOutputStream objectOutputStream = new ObjectOutputStream(new FileOutputStream("testSerializable"));
		objectOutputStream.writeObject(instance);
		objectOutputStream.close();
		
		ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream("testSerializable"));
		InnerClassSingleton objectClassSingleton = (InnerClassSingleton) objectInputStream.readObject();
		objectInputStream.close();
		
		System.out.println(instance == objectClassSingleton);
		
	}
}

class InnerClassSingleton implements Serializable{
	
	static final long serialVersionUID = 42L;
	
	private static class InnerClassHolder{
		private static InnerClassSingleton instance = new InnerClassSingleton();
	}
	private InnerClassSingleton() {
		//解决反射方式攻击
		if(InnerClassHolder.instance != null) 
			throw new RuntimeException("单例模式不允许多个实例！");
	};
	
	public static InnerClassSingleton getInstance() {
		return InnerClassHolder.instance;
	}
	
	//实现java.io.Serializable接口说明中提供的解决方案，方式反序列化获取的对象攻破单例模式
	Object readResolve() throws ObjectStreamException{
		return InnerClassHolder.instance;
	}
}
```
输出：true        

## 2.7 枚举类型
### 2.7.1 直接实例化两个对象，判断Enum类型是否是单例

```java
package com.zh.singletonpattern.enumsingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class EnumSingletonTest {
	/**
	 * 直接获取两个对象，判断Enum类型是否是单例
	 * 输出：true
	 * @param args
	 */
	public static void main1(String[] args) {
		EnumSingleton instance = EnumSingleton.INSTANCE;
		EnumSingleton instance2 = EnumSingleton.INSTANCE;
		System.out.println(instance == instance2);
	}
}

enum EnumSingleton{
	INSTANCE;
	
	public void print() {
		System.out.println(this.hashCode());
	}
}
```

### 2.7.2 通过反射验证Enum类型单例模式

```java
package com.zh.singletonpattern.enumsingleton;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class EnumSingletonTest {
	/**
	 * 通过反射获取枚举类型实例
	 * @param args
	 * @throws NoSuchMethodException
	 * @throws SecurityException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws IllegalArgumentException
	 * @throws InvocationTargetException
	 */
	public static void main(String[] args) throws NoSuchMethodException, SecurityException, InstantiationException, IllegalAccessException, IllegalArgumentException, InvocationTargetException {
		Constructor<EnumSingleton> declaredConstructor = EnumSingleton.class.getDeclaredConstructor(String.class, int.class);
		declaredConstructor.setAccessible(true);
		EnumSingleton newInstance = declaredConstructor.newInstance("INSTANCE", 0);
		
	}
}

enum EnumSingleton{
	INSTANCE;
	
	public void print() {
		System.out.println(this.hashCode());
	}
}
```
输出：

```
Exception in thread "main" java.lang.IllegalArgumentException: Cannot reflectively create enum objects
at java.lang.reflect.Constructor.newInstance(Constructor.java:417)
at com.zh.singletonpattern.enumsingleton.EnumSingletonTest.main(EnumSingletonTest.java:21)
```

### 2.7.3 通过反序列化验证Enum类型的单例模式

```java
package com.zh.singletonpattern.enumsingleton;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class EnumSingletonTest {
	/**
	 * 以序列化反序列化验证Enum类型单例模式
	 * 输出：true
	 * @param args
	 * @throws FileNotFoundException
	 * @throws IOException
	 * @throws ClassNotFoundException
	 */
	public static void main(String[] args) throws FileNotFoundException, IOException, ClassNotFoundException {
		EnumSingleton instance = EnumSingleton.INSTANCE;
		
		ObjectOutputStream objectOutputStream = new ObjectOutputStream(new FileOutputStream("testenumsingle"));
		objectOutputStream.writeObject(instance);
		objectOutputStream.close();

		ObjectInputStream objectInputStream = new ObjectInputStream(new FileInputStream("testenumsingle"));
		EnumSingleton instance2 = (EnumSingleton) objectInputStream.readObject();
		objectInputStream.close();
		
		System.out.println(instance == instance2);
	}
}

enum EnumSingleton{
	INSTANCE;
	
	public void print() {
		System.out.println(this.hashCode());
	}
}
```
输出：true         

