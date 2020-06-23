# 并发编程基础

# 1 线程安全
线程安全概念：当多个线程访问某一个类（对象或方法）时，这个对象始终都能表现出正确的行为，那么这个类（对象或方法）就是线程安全的。

synchronized：可以在任意对象及方法上加锁，而加锁的这段代码称为"互斥区"或"临界区"。

对于线程安全来说，需要满足两个特性：

- **原子性**
   - 原子性是指在一个操作中就是cpu不可以在中途暂停然后再调度，既不被中断操作，要不执行完成，要不就不执行。
- **可见性**
   - 可见性就是指当一个线程修改了线程共享变量的值，其它线程能够立即得知这个修改。
```java
package com.bjsxt.base.sync001;

import java.util.concurrent.atomic.AtomicInteger;

public class MyThread extends Thread{
	private int count = 5 ;	
	//synchronized加锁
	public void run(){
		count--;
		System.out.println(this.currentThread().getName() + " count = "+ count);
	}	
	public static void main(String[] args) {
		/**
		 * 分析：当多个线程访问myThread的run方法时，以排队的方式进行处理（这里排对是按照CPU分配的先后顺序而定的），
		 * 		一个线程想要执行synchronized修饰的方法里的代码：
		 * 		1 尝试获得锁
		 * 		2 如果拿到锁，执行synchronized代码体内容；拿不到锁，这个线程就会不断的尝试获得这把锁，直到拿到为止，而且是多个线程同时去竞争这把锁。（也就是会有锁竞争的问题）
		 */
		MyThread myThread = new MyThread();
		Thread t1 = new Thread(myThread,"t1");
		Thread t2 = new Thread(myThread,"t2");
		Thread t3 = new Thread(myThread,"t3");
		Thread t4 = new Thread(myThread,"t4");
		Thread t5 = new Thread(myThread,"t5");
		t1.start();
		t2.start();
		t3.start();
		t4.start();
		t5.start();
	}
}
```
输出：

```
t1 count = 3
t2 count = 4
t3 count = 2
t4 count = 1
t5 count = 0
```

# 2 原子性
原子性是指在一个操作中就是cpu不可以在中途暂停然后再调度，既不被中断操作，要不执行完成，要不就不执行。

原子操作是指，对于访问同一个状态的所有操作（包括操作本身）来说，这个操作是一个以原子方式执行的操作。

## 2.1 synchronized内存操作模型

1. 获得同步锁；
1. 清空工作内存；
1. 从主内存拷贝对象副本到工作内存；
1. 执行代码(计算或者输出等)；
1. 刷新主内存数据；
1. 释放同步锁。
## 2.2 多个线程多个锁
关键字synchronized取得的锁都是对象锁，而不是把一段代码（方法）当做锁，所以代码中哪个线程先执行synchronized关键字的方法，哪个线程就持有该方法所属对象的锁（Lock），在静态方法上加synchronized关键字，表示锁定.class类，类一级别的锁（独占.class类）。
```java
package com.bjsxt.base.sync002;

public class MultiThread {
	private int num = 0;
	
	/** static */
	public synchronized void printNum(String tag){
		try {			
			if(tag.equals("a")){
				num = 100;
				System.out.println("tag a, set num over!");
				Thread.sleep(1000);
			} else {
				num = 200;
				System.out.println("tag b, set num over!");
			}			
			System.out.println("tag " + tag + ", num = " + num);			
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	//注意观察run方法输出顺序
	public static void main(String[] args) {
		
		//俩个不同的对象
		final MultiThread m1 = new MultiThread();
		final MultiThread m2 = new MultiThread();
		
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				m1.printNum("a");
			}
		});
		
		Thread t2 = new Thread(new Runnable() {
			@Override 
			public void run() {
				m2.printNum("b");
			}
		});			
		t1.start();
		t2.start();		
	}	
}
```
输出：

```
tag a, set num over!
tag b, set num over!
tag b, num = 200
tag a, num = 100
```

## 2.3 对象锁的同步和异步

**同步**：synchronized

- 同步的概念就是共享。如果不是共享的资源，就没有必要进行同步。
- 同步的目的就是线程安全

**异步**：asynchronized

- 异步的概念就是独立，相互之间不受到任何制约。

```java
package com.bjsxt.base.sync003;

public class MyObject {
	public synchronized void method1(){
		try {
			System.out.println(Thread.currentThread().getName());
			Thread.sleep(4000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	/** synchronized */
	public void method2(){
			System.out.println(Thread.currentThread().getName());
	}
	
	public static void main(String[] args) {		
		final MyObject mo = new MyObject();
		
		/**
		 * 分析：
		 * t1线程先持有object对象的Lock锁，t2线程可以以异步的方式调用对象中的非synchronized修饰的方法
		 * t1线程先持有object对象的Lock锁，t2线程如果在这个时候调用对象中的同步（synchronized）方法则需等待，也就是同步
		 */
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				mo.method1();
			}
		},"t1");
		
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				mo.method2();
			}
		},"t2");
		
		t1.start();
		t2.start();		
	}	
}
```
输出：

```
t1
t2
```

## 2.4 脏读

对于对象的同步和异步的方法，我们在设计程序的时候，一定要考虑问题的整体，不然就会出现数据不一致的错误，很经典的错误就是脏读（dirtyread）。

```java
package com.bjsxt.base.sync004;

public class DirtyRead {

	private String username = "bjsxt";
	private String password = "123";
	
	public synchronized void setValue(String username, String password){
		this.username = username;
		
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		this.password = password;
		
		System.out.println("setValue最终结果：username = " + username + " , password = " + password);
	}
	
	public void getValue(){
		System.out.println("getValue方法得到：username = " + this.username + " , password = " + this.password);
	}
		
	public static void main(String[] args) throws Exception{
		
		final DirtyRead dr = new DirtyRead();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				dr.setValue("z3", "456");		
			}
		});
		t1.start();
		Thread.sleep(1000);
		
		dr.getValue();
	}	
}
```
输出：

```
getValue方法得到：username = z3 , password = 123
setValue最终结果：username = z3 , password = 456
```

注：

在我们对一个对象的方法加锁的时候，需要考虑业务的整体性，即为setValue/getValue方法同时加锁synchronized同步关键字，保证业务（service）的原子性，不然会出现业务错误（也从侧面保证业务的一致性）。

## 2.5 synchronized重入
关键字synchronized拥有锁重入的功能，也就是在使用synchronized时，当一个线程得到了一个对象的锁后，再次请求此对象时可以再次得到该对象的锁。

“重入”意味着获取锁的操作的粒度是”线程“，而不是”调用“。

重入的一种实现方法是，为每个锁关联一个获取计数值和一个所有者线程：

当线程请求一个未被持有的锁时，JVM将记下锁的持有者，并且将获取计数值置为1，如果同一个线程再次获取这个锁，计数值将递增，而当线程退出同步代码块时，计数器会相应地递减。当计数值为0时，这个锁将被释放。

示例：同步方法调用同一对象锁的方法。

```java
package com.bjsxt.base.sync005;

public class SyncDubbo1 {

	public synchronized void method1(){
		System.out.println("method1..");
		method2();
	}
	public synchronized void method2(){
		System.out.println("method2..");
		method3();
	}
	public synchronized void method3(){
		System.out.println("method3..");
	}
	
	public static void main(String[] args) {
		final SyncDubbo1 sd = new SyncDubbo1();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				sd.method1();
			}
		});
		t1.start();
	}
}
```
输出：

```
method1..
method2..
method3..
```

示例：子类对象锁的同步方法调用父类对象锁的同步方法

```java
package com.bjsxt.base.sync005;

public class SyncDubbo2 {
	static class Main {
		public int i = 10;
		public synchronized void operationSup(){
			try {
				i--;
				System.out.println("Main print i = " + i);
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}	
	static class Sub extends Main {
		public synchronized void operationSub(){
			try {
				while(i > 0) {
					i--;
					System.out.println("Sub print i = " + i);
					Thread.sleep(100);		
					this.operationSup();
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}	
	public static void main(String[] args) {	
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				Sub sub = new Sub();
				sub.operationSub();
			}
		});		
		t1.start();
	}	
}
```
输出：

```
Sub print i = 9
Main print i = 8
Sub print i = 7
Main print i = 6
Sub print i = 5
Main print i = 4
Sub print i = 3
Main print i = 2
Sub print i = 1
Main print i = 0
```

## 2.6 异常导致锁释放
如果一个线程在获取锁后执行同步代码的时候抛出异常，这个线程的锁将被释放，在编写代码的时候一定要考虑周全。

特别是对于web应用程序异常释放锁的情况，如果不及时处理，很可能对你的应用程序业务逻辑产生严重的错误，比如你现在执行一个队列任务，很多对象都在等待第一个对象正确执行完毕再去释放锁，但是第一个对象由于异常的出现，导致业务逻辑没有正常执行完毕就释放了锁，那么可想而知后续的对象执行的都是错误的逻辑。

```java
package com.bjsxt.base.sync005;

public class SyncException {
	private int i = 0;
	public synchronized void operation(){
		while(true){
			try {
				i++;
				Thread.sleep(100);
				System.out.println(Thread.currentThread().getName() + " , i = " + i);
				if(i == 20){
					//Integer.parseInt("a");
					throw new RuntimeException();
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	public static void main(String[] args) {
		
		final SyncException se = new SyncException();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				se.operation();
			}
		},"t1");
		t1.start();
	}		
}
```
输出：

```
t1 , i = 1
t1 , i = 2
t1 , i = 3
t1 , i = 4
t1 , i = 5
t1 , i = 6
t1 , i = 7
t1 , i = 8
t1 , i = 9
t1 , i = 10
t1 , i = 11
t1 , i = 12
t1 , i = 13
t1 , i = 14
t1 , i = 15
t1 , i = 16
t1 , i = 17
t1 , i = 18
t1 , i = 19
t1 , i = 20
Exception in thread "t1" java.lang.RuntimeException
at com.bjsxt.base.sync005.SyncException.operation(SyncException.java:18)
at com.bjsxt.base.sync005.SyncException$1.run(SyncException.java:32)
at java.lang.Thread.run(Thread.java:748)
```

## 2.7 synchronized代码块
使用synchronized声明的方法在某些情况下是有弊端的，比如A线程调用同步的方法执行一个很长时间的任务，那么B线程就必须等待比较长的时间才能执行，这样的情况下可以使用synchronized代码块去优化执行时间，也就是通常所说的减小锁的粒度。
```java
package com.bjsxt.base.sync006;

public class Optimize {
	public void doLongTimeTask(){
		try {		
			System.out.println("当前线程开始：" + Thread.currentThread().getName() + 
					", 正在执行一个较长时间的业务操作，其内容不需要同步");
			Thread.sleep(2000);
			
			synchronized(this){
				System.out.println("当前线程：" + Thread.currentThread().getName() + 
					", 执行同步代码块，对其同步变量进行操作");
				Thread.sleep(1000);
			}
			System.out.println("当前线程结束：" + Thread.currentThread().getName() +
					", 执行完毕");			
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		final Optimize otz = new Optimize();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				otz.doLongTimeTask();
			}
		},"t1");
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				otz.doLongTimeTask();
			}
		},"t2");
		t1.start();
		t2.start();		
	}	
}
```
输出：

```
当前线程开始：t2, 正在执行一个较长时间的业务操作，其内容不需要同步
当前线程开始：t1, 正在执行一个较长时间的业务操作，其内容不需要同步
当前线程：t2, 执行同步代码块，对其同步变量进行操作
当前线程结束：t2, 执行完毕
当前线程：t1, 执行同步代码块，对其同步变量进行操作
当前线程结束：t1, 执行完毕
```

### 2.7.1 synchronized可以使用任意的Object进行加锁

```java
package com.bjsxt.base.sync006;

public class ObjectLock {
	public void method1(){
		synchronized (this) {	//对象锁
			try {
				System.out.println("do method1..");
				Thread.sleep(2000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	public void method2(){		//类锁
		synchronized (ObjectLock.class) {
			try {
				System.out.println("do method2..");
				Thread.sleep(2000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	private Object lock = new Object();
	public void method3(){		//任何对象锁
		synchronized (lock) {
			try {
				System.out.println("do method3..");
				Thread.sleep(2000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	public static void main(String[] args) {		
		final ObjectLock objLock = new ObjectLock();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				objLock.method1();
			}
		});
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				objLock.method2();
			}
		});
		Thread t3 = new Thread(new Runnable() {
			@Override
			public void run() {
				objLock.method3();
			}
		});		
		t1.start();
		t2.start();
		t3.start();		
	}	
}
```
输出：

```
do method1..
do method2..
do method3..
```

### 2.7.2 不要使用String常量加锁
另外一个特别要注意的一个问题，就是不要使用String的常量加锁，会出现死循环问题。

- synchronized代码块对字符串的锁，注意String常量池的缓存功能。（[参见String常量池解释](https://droidyue.com/blog/2014/12/21/string-literal-pool-in-java/)）
   - 相同的字符串常量是一个地址，用其作为同步锁的话只有第一个线程释放锁之后第二个线程才能执行。
```java
package com.bjsxt.base.sync006;

public class StringLock {
	public void method() {
		//new String("字符串常量")
		synchronized ("字符串常量") {
			try {
				while(true){
					System.out.println("当前线程 : "  + Thread.currentThread().getName() + "开始");
					Thread.sleep(1000);		
					System.out.println("当前线程 : "  + Thread.currentThread().getName() + "结束");
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	public static void main(String[] args) {
		final StringLock stringLock = new StringLock();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				stringLock.method();
			}
		},"t1");
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				stringLock.method();
			}
		},"t2");
		
		t1.start();
		t2.start();
	}
}
```


### 2.7.3 锁对象改变问题
锁对象的改变问题，当使用一个对象进行加锁的时候，要注意对象发生改变的时候，持有的锁就不同。如果对象本身不发生改变，那么依然是同步的，即时对象的属性发生了改变。
```java
package com.bjsxt.base.sync006;

public class ChangeLock {

	private String lock = "lock";
	
	private void method(){
		synchronized (lock) {
			try {
				System.out.println("当前线程 : "  + Thread.currentThread().getName() + "开始");
				lock = "change lock";
				Thread.sleep(2000);
				System.out.println("当前线程 : "  + Thread.currentThread().getName() + "结束");
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	public static void main(String[] args) {
	
		final ChangeLock changeLock = new ChangeLock();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				changeLock.method();
			}
		},"t1");
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				changeLock.method();
			}
		},"t2");
		t1.start();
		try {
			Thread.sleep(100);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		t2.start();
	}	
}
```

输出：

```
当前线程 : t1开始
当前线程 : t2开始
当前线程 : t1结束
当前线程 : t2结束
```

同一对象属性的修改不会影响锁的情况

```java
package com.bjsxt.base.sync006;

public class ModifyLock {	
	private String name ;
	private int age ;
	
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public int getAge() {
		return age;
	}
	public void setAge(int age) {
		this.age = age;
	}
	
	public synchronized void changeAttributte(String name, int age) {
		try {
			System.out.println("当前线程 : "  + Thread.currentThread().getName() + " 开始");
			this.setName(name);
			this.setAge(age);
			
			System.out.println("当前线程 : "  + Thread.currentThread().getName() + " 修改对象内容为： " 
					+ this.getName() + ", " + this.getAge());
			
			Thread.sleep(2000);
			System.out.println("当前线程 : "  + Thread.currentThread().getName() + " 结束");
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		final ModifyLock modifyLock = new ModifyLock();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				modifyLock.changeAttributte("张三", 20);
			}
		},"t1");
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				modifyLock.changeAttributte("李四", 21);
			}
		},"t2");
		
		t1.start();
		try {
			Thread.sleep(100);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		t2.start();
	}	
}
```
输出：

```
当前线程 : t1 开始
当前线程 : t1 修改对象内容为： 张三, 20
当前线程 : t1 结束
当前线程 : t2 开始
当前线程 : t2 修改对象内容为： 李四, 21
当前线程 : t2 结束
```

### 2.7.4 死锁
死锁问题，在设计程序时就应该避免双方相互持有对方的锁的情况
```java
package com.bjsxt.base.sync006;

public class DeadLock implements Runnable{
	private String tag;
	private static Object lock1 = new Object();
	private static Object lock2 = new Object();
	
	public void setTag(String tag){
		this.tag = tag;
	}
	
	@Override
	public void run() {
		if(tag.equals("a")){
			synchronized (lock1) {
				try {
					System.out.println("当前线程 : "  + Thread.currentThread().getName() + " 进入lock1执行");
					Thread.sleep(2000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				synchronized (lock2) {
					System.out.println("当前线程 : "  + Thread.currentThread().getName() + " 进入lock2执行");
				}
			}
		}
		if(tag.equals("b")){
			synchronized (lock2) {
				try {
					System.out.println("当前线程 : "  + Thread.currentThread().getName() + " 进入lock2执行");
					Thread.sleep(2000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				synchronized (lock1) {
					System.out.println("当前线程 : "  + Thread.currentThread().getName() + " 进入lock1执行");
				}
			}
		}
	}
	
	public static void main(String[] args) {	
		DeadLock d1 = new DeadLock();
		d1.setTag("a");
		DeadLock d2 = new DeadLock();
		d2.setTag("b");
		 
		Thread t1 = new Thread(d1, "t1");
		Thread t2 = new Thread(d2, "t2");
		 
		t1.start();
		try {
			Thread.sleep(500);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		t2.start();
	}		
}
```
输出：

```
当前线程 : t1 进入lock1执行
当前线程 : t2 进入lock2执行

```

## 2.8 ReentrantLock

重入锁，建议应用的同步方式。 相对效率比 synchronized 高。量级较轻。

synchronized 在 JDK1.5 版本开始，尝试优化。到 JDK1.7 版本后，优化效率已经非常好了。在绝对效率上，不比 reentrantLock 差多少。

使用重入锁， 必须手工释放锁标记。 一般都是在 finally 代码块中定义释放锁标记的 unlock 方法。

```java
/**
 * 生产者消费者
 * 重入锁&条件
 * 条件 - Condition， 为Lock增加条件。当条件满足时，做什么事情，如加锁或解锁。如等待或唤醒
 */
import java.io.IOException;
import java.util.LinkedList;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class TestContainer02<E> {

	private final LinkedList<E> list = new LinkedList<>();
	private final int MAX = 10;
	private int count = 0;
	
	private Lock lock = new ReentrantLock();
	private Condition producer = lock.newCondition();
	private Condition consumer = lock.newCondition();
	
	public int getCount(){
		return count;
	}
	
	public void put(E e){
		lock.lock();
		try {
			while(list.size() == MAX){
				System.out.println(Thread.currentThread().getName() + " 等待。。。");
				// 进入等待队列。释放锁标记。
				// 借助条件，进入的等待队列。
				producer.await();
			}
			System.out.println(Thread.currentThread().getName() + " put 。。。");
			list.add(e);
			count++;
			// 借助条件，唤醒所有的消费者。
			consumer.signalAll();
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		} finally {
			lock.unlock();
		}
	}
	
	public E get(){
		E e = null;

		lock.lock();
		try {
			while(list.size() == 0){
				System.out.println(Thread.currentThread().getName() + " 等待。。。");
				// 借助条件，消费者进入等待队列
				consumer.await();
			}
			System.out.println(Thread.currentThread().getName() + " get 。。。");
			e = list.removeFirst();
			count--;
			// 借助条件，唤醒所有的生产者
			producer.signalAll();
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		} finally {
			lock.unlock();
		}
		
		return e;
	}
	
	public static void main(String[] args) {
		final TestContainer02<String> c = new TestContainer02<>();
		for(int i = 0; i < 10; i++){
			new Thread(new Runnable() {
				@Override
				public void run() {
					for(int j = 0; j < 5; j++){
						System.out.println(c.get());
					}
				}
			}, "consumer"+i).start();
		}
		try {
			TimeUnit.SECONDS.sleep(2);
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		}
		for(int i = 0; i < 2; i++){
			new Thread(new Runnable() {
				@Override
				public void run() {
					for(int j = 0; j < 25; j++){
						c.put("container value " + j); 
					}
				}
			}, "producer"+i).start();
		}
	}	
}
```


# 3 可见性
可见性就是指当一个线程修改了线程共享变量的值，其它线程能够立即得知这个修改。
## 3.1 volatile关键字
volatile关键字的主要作用是使变量在多个线程间可见。

在java中，每一个线程都会有一块工作内存区，其中存放着所有线程共享的主内存中的变量值的拷贝。当线程执行时，他在自己的工作内存区中操作这些变量。为了存取一个共享的变量，一个线程通常先获取锁定并去清除它的内存工作区，把这些共享变量从所有线程的共享内存区中正确的装入到他自己所在的工作内存区中，当线程解锁时保证该工作内存区中变量的值写回到共享内存中。

一个线程可以执行的操作有使用（use）、赋值（assign）、装载（load）、存储（store）、锁定（lock）、解锁（unlock）。

而主内存可以执行的操作有读（read）、写（write）、锁定（lock）、解锁（unlock），每个操作都是原子的。

volatile的作用就是强制线程到主内存（共享内存）里去读取变量，而不去线程工作内存区里去读取，从而实现了多个线程间的变量可见。也就是满足线程安全的可见性。

```java
package com.bjsxt.base.sync007;

public class RunThread extends Thread{
	//没有volatile关键字
    private boolean isRunning = true;
    //有volatile关键字
	//private volatile boolean isRunning = true;
	private void setRunning(boolean isRunning){
		this.isRunning = isRunning;
	}
	
	public void run(){
		System.out.println("进入run方法..");
		int i = 0;
		while(isRunning == true){
            //pringln使用了一个对象锁以保证print()和newLine()方法
            //的原子性操作（可以参见println()源码）。因为锁的原因println()刷新了主内存
            //实现了线程的可见性。
			//System.out.println("======");
		}
		System.out.println("线程停止");
	}
	
	public static void main(String[] args) throws InterruptedException {
		RunThread rt = new RunThread();
		rt.start();
		Thread.sleep(1000);
		rt.setRunning(false);
		System.out.println("isRunning的值已经被设置了false");
	}	
}
```
没有volatile关键字输出：

```
进入run方法..
isRunning的值已经被设置了false

```

有volatile关键字输出：

```
进入run方法..
isRunning的值已经被设置了false
线程停止
```

没有volatile关键字，但在循环中有`System.out.println("=====")`语句：

```
进入run方法..
======
======
（此处省略N个======）
======
======
isRunning的值已经被设置了false
线程停止
```

## 3.2 volatile关键字的非原子性

volatile关键字虽然拥有多个线程之间的可见性，但是却不具备原子性，可以算上是一个轻量级的synchronized，性能要比synchronized强很多，不会造成阻塞（在很多开源的架构里，比如netty的底层代码就大量使用volatile，可见netty性能一定是非常不错的。）这里需要注意：一般volatile用于只针对于多个线程可见的变量操作，并不能代替synchronized的同步功能。

volatile关键字只具有可见性，没有原子性。要实现原子性建议使用atomic类的系列对象，支持原子性操作。

```java
package com.bjsxt.base.sync007;

import java.util.concurrent.atomic.AtomicInteger;

public class VolatileNoAtomic extends Thread{
	private static volatile int count;
	//private static AtomicInteger count = new AtomicInteger(0);
	private static void addCount(){
		for (int i = 0; i < 1000; i++) {
			count++ ;
			//count.incrementAndGet();
		}
		System.out.println(count);
	}
	
	public void run(){
		addCount();
	}
	
	public static void main(String[] args) {
		
		VolatileNoAtomic[] arr = new VolatileNoAtomic[100];
		for (int i = 0; i < 10; i++) {
			arr[i] = new VolatileNoAtomic();
		}
		
		for (int i = 0; i < 10; i++) {
			arr[i].start();
		}
	}	
}
```
使用volatile变量输出结果：

```
1000
2010
2773
4205
4359
4649
5649
6649
7649
8649
```

使用AtomicInteger变量输出结果：

```
1000
2000
3000
4000
5000
6000
7000
8000
9656
10000
```

## 3.3 Atomic类

使用锁时，线程获取锁是一种悲观锁策略，即假设每一次执行临界区代码都会产生冲突，所以当前线程获取到锁的时候同时也会阻塞其他线程获取该锁。而CAS操作（又称为无锁操作）是一种乐观锁策略，它假设所有线程访问共享资源的时候不会出现冲突，既然不会出现冲突自然而然就不会阻塞其他线程的操作。因此，线程就不会出现阻塞停顿的状态。那么，如果出现冲突了怎么办？无锁操作是使用CAS(compare and swap)又叫做比较交换来鉴别线程是否出现冲突，出现冲突就重试当前操作直到没有冲突为止。

**CAS的操作过程：**

CAS比较交换的过程可以通俗的理解为CAS(V,O,N)，包含三个值分别为：V 内存地址存放的实际值；O 预期的值（旧值）；N 更新的新值。当V和O相同时，也就是说旧值和内存中实际的值相同表明该值没有被其他线程更改过，即该旧值O就是目前来说最新的值了，自然而然可以将新值N赋值给V。反之，V和O不相同，表明该值已经被其他线程改过了则该旧值O不是最新版本的值了，所以不能将新值N赋给V，返回V即可。当多个线程使用CAS操作一个变量是，只有一个线程会成功，并成功更新，其余会失败。失败的线程会重新尝试，当然也可以选择挂起线程。

CAS的实现需要硬件指令集的支撑，在JDK1.5后虚拟机才可以使用处理器提供的CMPXCHG指令实现。

元老级的Synchronized(未优化前)最主要的问题是：在存在线程竞争的情况下会出现线程阻塞和唤醒锁带来的性能问题，因为这是一种互斥同步（阻塞同步）。而CAS并不是武断的间线程挂起，当CAS操作失败后会进行一定的尝试，而非进行耗时的挂起唤醒的操作，因此也叫做非阻塞同步。这是两者主要的区别。

**CAS的问题：**

- ABA问题
   - 因为CAS会检查旧值有没有变化，这里存在这样一个有意思的问题。比如一个旧值A变为了成B，然后再变成A，刚好在做CAS时检查发现旧值并没有变化依然为A，但是实际上的确发生了变化。解决方案可以沿袭数据库中常用的乐观锁方式，添加一个版本号可以解决。原来的变化路径A->B->A就变成了1A->2B->3C。<br />
- 自旋时间过长
   - 使用CAS时非阻塞同步，也就是说不会将线程挂起，会自旋（无非就是一个死循环）进行下一次尝试，如果这里自旋时间过长对性能是很大的消耗。如果JVM能支持处理器提供的pause指令，那么在效率上会有一定的提升。

注意：Atomic类只保证本身方法的原子性，并不保证多次操作的原子性。<br />

```java
package com.bjsxt.base.sync007;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

public class AtomicUse {
	private static AtomicInteger count = new AtomicInteger(0);
	
    //多个addAndGet在一个方法内是非原子性的，需要加synchronized进行修饰，
    //保证4个addAndGet整体原子性
	//public synchronized int multiAdd(){
    public int multiAdd(){
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			count.addAndGet(1);
			count.addAndGet(2);
			count.addAndGet(3);
			count.addAndGet(4); //+10
			return count.get();
	}
		
	public static void main(String[] args) {		
		final AtomicUse au = new AtomicUse();

		List<Thread> ts = new ArrayList<Thread>();
		for (int i = 0; i < 100; i++) {
			ts.add(new Thread(new Runnable() {
				@Override
				public void run() {
					System.out.println(au.multiAdd());
				}
			}));
		}

		for(Thread t : ts){
			t.start();
		}		
	}
}
```
没有synchronized关键字输出：

```
10
100
20
......
61
......
1000
......
950
890
```

有synchronized关键字输出：

```
10
20
30
......
980
990
1000
```

# 4 线程之间通信
线程通信概念：线程是操作系统中独立的个体，但这些个体如果不经过特殊的处理就不可能称为一个整体，线程间的通信就称为整体的比用方式之一。当线程存在通信指挥，系统间的交互性会更强大，在提高CPU利用率的同时还会使开发人员对线程任务在处理的过程中进行有效的把握与监督。

## 4.1 wait-notify&CountDownLatch

使用wait/notify方法实现线程间的通信。（注意这两个方法都是object的类的方法，换据话说java为所有的对象都提供了这两个方法）：

- wait和notify必须配合synchronized关键字使用
- wait方法释放锁，notify方法不释放锁。

```java
package com.bjsxt.base.conn008;

import java.util.ArrayList;
import java.util.List;

public class ListAdd1 {	
	private static List list = new ArrayList();
    //private volatile static List list = new ArrayList();
	
	public void add(){
		list.add("bjsxt");
	}
	public int size(){
		return list.size();
	}	
	public static void main(String[] args) {		
		final ListAdd1 list1 = new ListAdd1();		
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				try {
					for(int i = 0; i <10; i++){
						list1.add();
						System.out.println("当前线程：" + Thread.currentThread().getName() + "添加了一个元素..");
						Thread.sleep(500);
					}	
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}, "t1");
		
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				while(true){
					if(list1.size() == 5){
						System.out.println("当前线程收到通知：" + Thread.currentThread().getName() + " list size = 5 线程停止..");
						throw new RuntimeException();
					}
				}
			}
		}, "t2");				
		t1.start();
		t2.start();
	}	
}
```
没有volatile修饰输出：

```
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..

```

有volatile修饰输出：

```
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程收到通知：t2 list size = 5 线程停止..
Exception in thread "t2" java.lang.RuntimeException
 at com.bjsxt.base.conn008.ListAdd1$2.run(ListAdd1.java:43)
 at java.lang.Thread.run(Thread.java:748)
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
```



```java
package com.bjsxt.base.conn008;

import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.LinkedBlockingQueue;

public class ListAdd2 {
	private volatile static List list = new ArrayList();		
	public void add(){
		list.add("bjsxt");
	}
	public int size(){
		return list.size();
	}
	
	public static void main(String[] args) {		
		final ListAdd2 list2 = new ListAdd2();	
		// 1 实例化出来一个 lock
		// 当使用wait 和 notify 的时候，一定要配合着synchronized关键字去使用
        // 两个线程是同一把锁，故不能同时运行
		final Object lock = new Object();
        
		//CountDownLatch不用锁，两个线程可以同时运行
		//final CountDownLatch countDownLatch = new CountDownLatch(1);
		
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				try {
					synchronized (lock) {
						for(int i = 0; i <10; i++){
							list2.add();
							System.out.println("当前线程：" + Thread.currentThread().getName() + "添加了一个元素..");
							Thread.sleep(500);
							if(list2.size() == 5){
								System.out.println("已经发出通知..");
								//countDownLatch.countDown();//重启阻塞线程
								lock.notify();
							}
						}						
					}
				} catch (InterruptedException e) {
					e.printStackTrace();
				}

			}
		}, "t1");
		
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				synchronized (lock) {
					if(list2.size() != 5){
						try {
							System.out.println("t2进入...");
							lock.wait();
							//countDownLatch.await();//阻塞当前线程
						} catch (InterruptedException e) {
							e.printStackTrace();
						}
					}
					System.out.println("当前线程：" + Thread.currentThread().getName() + "收到通知线程停止..");
					throw new RuntimeException();
				}
			}
		}, "t2");			
		t2.start();
		t1.start();		
	}	
}
```
同步+wait+notify输出：

```
t2进入...
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
已经发出通知..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t2收到通知线程停止..
Exception in thread "t2" java.lang.RuntimeException
 at com.bjsxt.base.conn008.ListAdd2$2.run(ListAdd2.java:71)
 at java.lang.Thread.run(Thread.java:748)
```

CountDownLatch输出：

```
t2进入...
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
已经发出通知..
当前线程：t1添加了一个元素..
当前线程：t2收到通知线程停止..
Exception in thread "t2" java.lang.RuntimeException 
 at com.bjsxt.base.conn008.ListAdd2$2.run(ListAdd2.java:71)
 at java.lang.Thread.run(Thread.java:748)
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
当前线程：t1添加了一个元素..
```

# 5 ThreadLocal

ThreadLocal概念：线程局部变量，是一种多线程并发访问变量的解决方案。

与synchronized等加锁的方式不同，ThreadLocal完全不提供锁，而是用以空间换时间的手段，为每个线程提供变量的独立副本，以保障线程安全。

从性能上说，ThreadLocal不具有绝对的优势，在并发不是很高的时候，加锁的性能会更好，但作为一套与锁安全无关的线程安全解决方案，在高并发量或者竞争激烈的场景，使用ThreadLocal可以在一定程度上减少锁竞争。

```java
package com.bjsxt.base.conn010;

public class ConnThreadLocal {
	public static ThreadLocal<String> th = new ThreadLocal<String>();	
	public void setTh(String value){
		th.set(value);
	}
	public void getTh(){
		System.out.println(Thread.currentThread().getName() + ":" + this.th.get());
	}	
	public static void main(String[] args) throws InterruptedException {		
		final ConnThreadLocal ct = new ConnThreadLocal();
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				ct.setTh("张三");
				ct.getTh();
			}
		}, "t1");
		
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				try {
					Thread.sleep(1000);
					ct.getTh();
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}, "t2");		
		t1.start();
		t2.start();
	}	
}
```
输出：

```
t1:张三
t2:null
```

# 6 单例&多线程

单例模式，最常见的就是饥饿模式（直接实例化对象）和懒汉模式（在调用方法时进行实例化对象）。

在多线程模式中，考虑到性能和线程安全问题，我们一般选择下面两种比较经典的单例模式，在性能提高的同时，又保证了线程安全。

- static inner class
- double check instance

**static inner class：**

```java
package bhz.base.conn011;

public class Singletion {	
	private static class InnerSingletion {
		private static Singletion single = new Singletion();
	}
	
	public static Singletion getInstance(){
		return InnerSingletion.single;
	}
}

```

**dubble check instance：**

```java
package com.bjsxt.base.conn011;

public class DubbleSingleton {
	private static DubbleSingleton ds;	
	public  static DubbleSingleton getDs(){
		if(ds == null){
			try {
				//模拟初始化对象的准备时间...
				Thread.sleep(3000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			synchronized (DubbleSingleton.class) {
				if(ds == null){
					ds = new DubbleSingleton();
				}
			}
		}
		return ds;
	}
	
	public static void main(String[] args) {
		Thread t1 = new Thread(new Runnable() {
			@Override
			public void run() {
				System.out.println(DubbleSingleton.getDs().hashCode());
			}
		},"t1");
		Thread t2 = new Thread(new Runnable() {
			@Override
			public void run() {
				System.out.println(DubbleSingleton.getDs().hashCode());
			}
		},"t2");
		Thread t3 = new Thread(new Runnable() {
			@Override
			public void run() {
				System.out.println(DubbleSingleton.getDs().hashCode());
			}
		},"t3");		
		t1.start();
		t2.start();
		t3.start();
	}	
}
```
输出：

```
1073218074
1073218074
1073218074
```

# 7 锁的种类
Java中锁的种类大致分为偏向锁、自选锁、轻量级锁、重量级锁。

锁的使用方式为：先提供偏向锁，如果不满足的时候，升级为轻量级锁，再不满足，升级为重量级锁。自选锁是一个过度的锁状态，不是一中实际的锁类型。

锁只能升级，不能降级。

