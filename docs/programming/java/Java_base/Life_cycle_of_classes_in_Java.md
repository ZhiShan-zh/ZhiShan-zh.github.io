# Java中类的生命周期

# 1 JVM中内存区域


- **方法区：** 在Java的虚拟机中有一块专门用来存放已经加载的类元数据、常量、静态变量以及方法代码的内存区域。
   - **常量池：** 常量池是方法区的一部分，主要用来存放常量和类中的符号引用等信息。
- **堆区：** 用来分配Java对象和数组的空间。
- **栈区：** 也叫Java虚拟机栈，是由一个一个的栈帧组成的后进先出的栈式结构，栈桢中存放方法运行时产生的局部变量、方法出口等信息。当调用一个方法时，虚拟机栈中就会创建一个栈帧存放这些数据，当方法调用完成时，栈帧消失，如果方法中调用了其他方法，则继续在栈顶创建新的栈桢。


除了以上四个内存区域之外，JVM中的运行时内存区域还包括本地方法栈和程序计数器，这两个区域与Java类的生命周期关系不是很大，在这里就不说了，感兴趣的朋友可以自己百度一下。

# 2 类的生命周期
当我们编写一个Java的源文件后，经过编译会生成一个后缀名为class的文件，这种文件叫做字节码文件，只有这种字节码文件才能够在java虚拟机中运行，**Java类的生命周期**就是指一个class文件从加载到卸载的全过程。<br />一个Java类的完整的生命周期会经历加载、连接、初始化、使用、和卸载五个阶段，当然也有在加载或者连接之后没有被初始化就直接被使用的情况，如图所示：

![image.png](https://zhishan-zh.github.io/media/java_base-7225d6ea4dc9.png)

下面我们就依次来说一说这五个阶段。

## 2.1 加载

**加载阶段就是找到需要加载的类并把类的信息加载到JVM的方法区中，然后在堆区中实例化一个`java.lang.Class`对象，作为方法区中这个类的信息的入口。**

### 2.1.1 类加载方式

- 根据类的全路径名找到相应的class文件，然后从class文件中读取文件内容。
- 从jar文件中读取。
- 从网络中获取：比如10年前十分流行Applet。
- 根据一定的规则实时生成，比如设计模式中的动态代理模式，就是根据相应的类自动生成它的代理类。
- 从非class文件中获取，其实这与直接从class文件中获取的方式本质上是一样的，这些非class文件在JVM中运行之前会被转换为可被JVM所识别的字节码文件。
### 2.1.2 类的加载时机
**对于加载的时机，各个虚拟机的做法并不一样，但是有一个原则，就是当JVM“预期”到一个类将要被使用时，就会在使用它之前对这个类进行加载。** 比如说，在一段代码中出现了一个类的名字，JVM在执行这段代码之前并不能确定这个类是否会被使用到，于是，有些JVM会在执行前就加载这个类，而有些则在真正需要用的时候才会去加载它，这取决于具体的JVM实现。我们常用的hotspot虚拟机是采用的后者，就是说当真正用到一个类的时候才对它进行加载。

加载阶段是类的生命周期中的第一个阶段，加载阶段之后，是连接阶段。有一点需要注意，就是有时**连接阶段并不会等加载阶段完全完成之后才开始，而是交叉进行，可能一个类只加载了一部分之后，连接阶段就已经开始了。但是这两个阶段总的开始时间和完成时间总是固定的：加载阶段总是在连接阶段之前开始，连接阶段总是在加载阶段完成之后完成。**

## 2.2 连接
连接阶段比较复杂，**一般会跟加载阶段和初始化阶段交叉进行**，这个阶段的主要任务就是做一些加载后的验证工作以及一些初始化前的准备工作，可以细分为三个步骤：验证、准备和解析。

1. **验证：** 当一个类被加载之后，必须要验证一下这个类是否合法，比如这个类是不是符合字节码的格式、变量与方法是不是有重复、数据类型是不是有效、继承与实现是否合乎标准等等。总之，**这个阶段的目的就是保证加载的类是能够被JVM所运行**。
1. **准备：** 准备阶段的工作就是为类的静态变量分配内存并设为JVM默认的初值，对于非静态的变量，则不会为它们分配内存。有一点需要注意，这时候，**静态变量的初值为JVM默认的初值，而不是我们在程序中设定的初值（还有一个意思是，JVM会先去类中查找所有的静态声明，而先不关心我们的赋值操作）**。**JVM默认的初值是规则：**
   - 基本类型（int、long、short、char、byte、boolean、float、double）的默认值为0。
   - 引用类型的默认值为null。
   - 常量的默认值为我们程序中设定的值，比如我们在程序中定义`final static int a = 100`，则准备阶段中a的初值就是100。
       - final修饰的变量，但为进行初始化，怎么在准备阶段操作呢？
3. **解析：** 这一阶段的任务就是把常量池中的符号引用转换为直接引用。
> 那么什么是符号引用，什么又是直接引用呢？我们来举个例子：我们要找一个人，我们现有的信息是这个人的身份证号是1234567890。只有这个信息我们显然找不到这个人，但是通过公安局的身份系统，我们输入1234567890这个号之后，就会得到它的全部信息：比如安徽省黄山市余暇村18号张三，通过这个信息我们就能找到这个人了。这里，123456790就好比是一个符号引用，而安徽省黄山市余暇村18号张三就是直接引用。在内存中也是一样，比如我们要在内存中找一个类里面的一个叫做show的方法，显然是找不到。但是在解析阶段，JVM就会把show这个名字转换为指向方法区的的一块内存地址，比如c17164，通过c17164就可以找到show这个方法具体分配在内存的哪一个区域了。这里show就是符号引用，而c17164就是直接引用。在解析阶段，jvm会将所有的类或接口名、字段名、方法名转换为具体的内存地址。

连接阶段完成之后会根据使用的情况（是直接引用还是被动引用）来选择是否对类进行初始化。

注意：**在准备阶段，JVM会先去类中查找所有的静态声明，而先不关心我们的赋值操作，静态成员的赋值是在初始化阶段完成的，所以下面的程序是合法的**：

```java
package com.zh.classloadtest.staticvariable;

public class StaticVariableTest {
	static {
		i = 100;
	}
	public static int i = 1;
	public static void main(String[] args) {
		System.out.println(i);
	}
}
```
输出：
> 1

**注释**：因为静态成员的赋值是在初始化阶段完成，而初始化阶段对静态成员的初始化是根据类中的书写顺序来完成的。

注意：**静态成员是在初始化阶段进行赋值的，但在非静态方法（包括构造方法）中重新赋值是也是可以的**。

```java
package com.zh.classloadtest.staticvariable;

public class StaticVariableTest {
	static {
		i = 100;
	}
	public static int i = 1;
	public StaticVariableTest() {
		i = 100;
	}
	public static void main(String[] args) {
		System.out.println(i);
	}
}
```
输出：
> 100



## 2.3 初始化
如果一个类被直接引用，就会触发类的初始化。

**Java中直接引用分为：**

- 通过new关键字实例化对象、读取或设置类的静态变量、调用类的静态方法。
    - 注：读取类的常量不会引起类的初始化。
- 通过反射方式执行以上三种行为。
- 初始化子类的时候，会触发父类的初始化。
- 作为程序入口直接运行时（就是直接调用main函数）。

**除了以上四种情况，其他使用类的方式叫做被动引用，而被动引用不会触发类的初始化。** 在Java代码中，有些类看上去初始化了，但其实没有。例如定义一定长度某一类型的数组，看上去数组中所有的元素已经被初始化，实际上一个都没有。

**总体规律：**

1. 初始化构造时，先父后子；只有在父类所有都构造完后子类才被初始化；
1. 类加载先是静态、后非静态、最后是构造函数：
   1. 静态构造块、静态类属性按出现在类定义里面的先后顺序初始化，同理非静态的也是一样的；
   1. 只是静态的只在加载字节码是执行一次，不管你new多少次，非静态会在new多少次就执行多少次。
3. Java中的类只有在被用到的时候才会被加载；
3. Java类只有在类字节码被加载后才可以被构造成对象实例。

**大概顺序：**初始化父类的静态代码（静态构造块和静态类属性按定义顺序执行，非静态的同理）--->初始化子类的静态代码--> (注：如果不创建实例,则后面的不执行)初始化父类的非静态代码（变量定义等）--->初始化父类构造函数--->初始化子类非静态代码（变量定义，代码块等）--->初始化子类构造函数

```java
import java.lang.reflect.Field;
import java.lang.reflect.Method;
class InitClass{
	static {
		System.out.println("初始化InitClass");
	}
	public static String a = null;
	public static void method(){}
}

class SubInitClass extends InitClass{}

public class Test1 {
    /**
    * 主动引用引起类的初始化的第四种情况就是运行Test1的main方法时
    * 导致Test1初始化，这一点很好理解，就不特别演示了。
    * 本代码演示了前三种情况，以下代码都会引起InitClass的初始化，
    * 但由于初始化只会进行一次，运行时请将注解消掉，依次运行查看结果。
    * \@param args
    * \@throws Exception
    */
	public static void main(String[] args) throws Exception{
	// 主动引用引起类的初始化一: new对象、读取或设置类的静态变量、调用类的静态方法。
	// new InitClass();
	// InitClass.a = "";
	// String a = InitClass.a;
	// InitClass.method();
        
	//主动引用引起类的初始化二：通过反射实例化对象、读取或设置类的静态变量、调用类的静态方法。
	// Class cls = InitClass.class;
	// cls.newInstance();
	// Field f = cls.getDeclaredField("a");
	// f.get(null);
	// f.set(null, "s");
	// Method md = cls.getDeclaredMethod("method");
	// md.invoke(null, null);
        
	// 主动引用引起类的初始化三：实例化子类，引起父类初始化。
	// new SubInitClass();
	}
}
```
上面的程序演示了主动引用触发类的初始化的四种情况。

类的初始化过程是这样的： **按照顺序自上而下运行类中的变量赋值语句和静态语句，如果有父类，则首先按照顺序运行父类中的变量赋值语句和静态语句。** 先看一个例子：

首先建两个类用来显示赋值操作：

```java
public class Field1{
	public Field1(){
		System.out.println("Field1构造方法");
	}
}

```


```java
public class Field2{
	public Field2(){
		System.out.println("Field2构造方法");
	}
}
```

下面是演示初始化顺序的代码：
```java
package com.zh.classloadtest;

class InitClass{
	static{
		System.out.println("运行父类静态代码");//2
	}
	public static Field1 f1 = new Field1();//3
	public static Field1 f2;//4 只是声明，没有赋值，所以不初始化
}

class SubInitClass extends InitClass{
	static{
		System.out.println("运行子类静态代码");// 5
	}
	public static Field2 f2 = new Field2();//6
}

public class ClassLoadSequence {
	public static void main(String[] args) throws ClassNotFoundException{
		new SubInitClass();//1
	}
}
```
**程序输出：**

```
运行父类静态代码                            
Field1构造方法                                
运行子类静态代码                            
Field2构造方法                                
```


而下面的代码：

```java
package com.zh.classloadtest;

class InitClass2{
	public static Field1 f1 = new Field1();//2
	public static Field1 f2;//3 只是声明，没有赋值，所以不初始化
	static{
		System.out.println("运行父类静态代码");//4
	}
}
class SubInitClass2 extends InitClass2{
	public static Field2 f2 = new Field2();//5
	static{
		System.out.println("运行子类静态代码");//6
	}
}
public class ClassLoadSequence2 {
	public static void main(String[] args) throws ClassNotFoundException{
		new SubInitClass2();//1
	}
}

```
程序输出：

```
Field1构造方法                
运行父类静态代码            
Field2构造方法                
运行子类静态代码            
```

**在类的初始化阶段，只会初始化与类相关的赋值语句和静态语句，也就是有static关键字修饰的信息，没有static修饰的赋值语句和静态语句在实例化对象的时候才会运行。**

## 2.4 使用

**被动引用：**

- 引用父类的静态字段，只会引起父类的初始化，而不会引起子类的初始化。
- 定义类数组，不会引起类的初始化。
- **引用类的常量，不会引起类的初始化**。

```java
class InitClass{
	static {
		System.out.println("初始化InitClass");
	}
	public static String a = null;
	public final static String b = "b";
	public static void method(){}
}
class SubInitClass extends InitClass{
	static {
		System.out.println("初始化SubInitClass");
	}
}
public class Test4 {
	public static void main(String[] args) throws Exception{
    //引用父类的静态字段，只会引起父类初始化，而不会引起子类的初始化
	// String a = SubInitClass.a;
    // 使用类的常量不会引起类的初始化
	// String b = InitClass.b;
	// 定义类数组不会引起类的初始化
	SubInitClass[] sc = new SubInitClass[10];
	}
}
```
最后总结一下使用阶段，使用阶段包括主动引用和被动引用，主动引用会引起类的初始化，而被动引用不会引起类的初始化。

当使用阶段完成之后，java类就进入了卸载阶段。

## 2.5 卸载
类的卸载过程其实就是在方法区中清空类信息，Java类的整个生命周期就结束了。

类使用完之后，三个条件全部满足，JVM就会在方法区垃圾回收的时候对类进行卸载：

- 该类所有的实例都已经被回收，也就是java堆中不存在该类的任何实例。
- 加载该类的ClassLoader已经被回收。
- 该类对应的`java.lang.Class`对象没有任何地方被引用，无法在任何地方通过反射访问该类的方法。



