# Java反射机制

# 1 概述

## 1.1 Java反射机制定义

Java反射机制：（源自：[百度百科]([https://baike.baidu.com/item/JAVA%E5%8F%8D%E5%B0%84%E6%9C%BA%E5%88%B6/6015990#2](https://baike.baidu.com/item/JAVA反射机制/6015990#2))）

- Java的反射（reflection）机制是指在程序的运行状态中，可以构造任意一个类的对象，可以了解任意一个对象所属的类，可以了解任意一个类的成员变量和方法，可以调用任意一个对象的属性和方法。这种动态获取程序信息以及动态调用对象的功能称为Java语言的反射机制。
- 反射被视为动态语言的关键。
    - **动态语言**：程序运行时，允许改变程序结构或变量类型的语言。

## 1.2 Java反射机制的功能

- 在运行时判断任意一个对象所属的类；
- 在运行时构造任意一个类的对象；
- 在运行时判断任意一个类所具有的成员变量和方法；
- 在运行时调用任意一个对象的方法；
- 生成动态代理。

# 2 反射包`java.lang.reflect`的常用类

## 2.1 `java.lang.reflect.Executable`

`java.lang.reflect.Executable`开始于JDK1.8，是一个抽象类，其类声明为：

```java
public abstract class Executable extends AccessibleObject implements Member, GenericDeclaration
```

Java 8以后在`java.lang.reflect`包中新增了一个Executable抽象类，该类对象代表可执行的类成员。Executable抽象类派生了Constructor和Method两个子类。

Executable类提供了大量方法用来获取参数、修饰符或注解等信息：

| 常用方法                                                     | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `Parameter[] getParameters()`                                | 以数组形式（`Parameter[]`）返回所有形参                      |
| `int getParameterCount()`                                    | 返回参数的个数                                               |
| `abstract Class<?>[] getParameterTypes()`                    | 按声明顺序以Class数组的形式返回各参数的类型                  |
| `Type[] getGenericParameterTypes()`                          | 按照声明顺序返回以Type数组的形式返回此 Method/Constructor 对象所表示的形参类型的。 |
| `abstract int getModifiers()`                                | 返回整数表示的修饰符public、protected、private、final、static、abstract等关键字所对应的常量 |
| `boolean isVarArgs()`                                        | 如果声明此方法采用可变数量的参数，则返回true; 否则返回false。 |
| `abstract Class<?>[] getExceptionTypes()`                    | 以Class对象数组返回此 Method/Constructor 对象表示的底层方法抛出的异常类型 |
| `Type[] getGenericExceptionTypes()`                          | 以Type对象数组返回此 Method/Constructor 对象抛出的异常的类型。 |
| `abstract String toGenericString()`                          | 返回描述此 Method/Constructor 的字符串，包括类型参数。       |
| `<T extends Annotation> T getAnnotation(Class<T> annotationClass)` | 如果存在这样的注释，则返回指定类型的此元素的注释，否则为null。<br />annotationClass：与注释类型对应的Class对象 |
| `Annotation[] getDeclaredAnnotations()`                      | 返回直接出现在此元素上的所有注释。 与此接口中的其他方法不同，此方法忽略继承的注释。 （如果此元素上没有直接出现注释，则返回长度为零的数组。）此方法的调用者可以自由修改返回的数组; 它对返回给其他调用者的数组没有影响。 |
| `abstract Annotation[][] getParameterAnnotations()`          | 返回一个数组数组，这些数组以声明顺序表示此Method对象表示的方法的形式参数的注释。 （如果基础方法是无参数的，则返回长度为零的数组。如果方法有一个或多个参数，则为没有注释的每个参数返回长度为零的嵌套数组。）返回数组中包含的注释对象是可序列化的。 此方法的调用者可以自由修改返回的数组; 它对返回给其他调用者的数组没有影响。 |
| `abstract AnnotatedType getAnnotatedReturnType();`           | 以一个AnnotatedType对象的形式返回此Method/Constructor 对象的返回类型 |
| `AnnotatedType[] getAnnotatedExceptionTypes()`               | 以一个AnnotatedType对象数组的形式返回此Method/Constructor 对象声明的异常类型 |
| `AnnotatedType getAnnotatedReceiverType()`                   | 以一个AnnotatedType对象的形式返回此Method/Constructor 对象的接收类型 |
| `AnnotatedType[] getAnnotatedParameterTypes()`               | 以一个AnnotatedType对象的形式返回此Method/Constructor 对象的接收类型 |
| `Object invoke(Object obj, Object... args)`                  | 在具有指定参数的指定对象上调用此Method对象表示的基础方法。 各个参数自动展开以匹配原始形式参数，并且原始参数和参考参数都根据需要进行方法调用转换。<br />参数**obj** - 从中调用基础方法的对象。<br />参数**args** - 用于方法调用的参数。 |

## 2.2 `java.lang.reflect.AccessibleObject`

`java.lang.reflect.AccessibleObject`类是Field，Method和Constructor对象的基类。 它提供了将反射对象标记为在使用时禁止默认Java语言访问控制检查的功能。 当使用Fields，Methods或Constructors设置或获取字段，调用方法或创建和初始化类的新实例时，将执行对公共，默认（包）访问，受保护和私有成员的访问检查。 在反射对象中设置可访问标志允许具有足够权限的复杂应用程序（例如Java对象序列化或其他持久性机制）以通常被禁止的方式操作对象。

| 常用方法                                                     | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `boolean isAccessible()`                                     | 获取此对象的可访问标志的值。                                 |
| `boolean isAnnotationPresent(Class<? extends Annotation> annotationClass)` | 如果此元素上存在指定类型的注释，则返回true，否则返回false。<br />参数**annotationClass** - 与注释类型对应的Class对象。 |
| `void setAccessible(boolean flag)`                           | 将此对象的可访问标志设置为指示的布尔值。 值true表示反射对象在使用时应禁止Java语言访问检查。 值false表示反射对象应强制执行Java语言访问检查。<br />参数**flag** - 每个对象中可访问标志的新值。 |
| `static void setAccessible(AccessibleObject[] array, boolean flag)` | 这是一种方便的方法，可以通过单个安全检查为了设置对象数组的可访问标志（为了提高效率）。<br />参数**array** - AccessibleObjects的数组。<br />参数**flag** - 每个对象中可访问标志的新值。 |

## 2.3 `java.lang.reflect.Modifier`

`java.lang.reflect.Modifier`类提供静态方法和常量来解码类和成员访问修饰符。 修饰符集表示为具有表示不同修饰符的不同位位置的整数。

此类的声明为：

```java
public class Modifier
   extends Object
```

|             字段（Field） | 说明                            |
| ------------------------: | :------------------------------ |
|     `static int ABSTRACT` | 表示abstract修饰符的int值。     |
|        `static int FINAL` | 表示final修饰符的int值。        |
|    `static int INTERFACE` | 表示接口修饰符的int值。         |
|       `static int NATIVE` | 表示本机修饰符的int值。         |
|      `static int PRIVATE` | 表示private修饰符的int值。      |
|    `static int PROTECTED` | 表示受保护修饰符的int值。       |
|       `static int PUBLIC` | 表示public修饰符的int值。       |
|       `static int STATIC` | 表示static修饰符的int值。       |
|       `static int STRICT` | 表示strictfp修饰符的int值。     |
| `static int SYNCHRONIZED` | 表示synchronized修饰符的int值。 |
|    `static int TRANSIENT` | 表示transient修饰符的int值。    |
|     `static int VOLATILE` | 表示volatile修饰符的int值。     |

| 常用方法                            | 说明                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| `static int classModifiers()`       | 返回一个int值，或者将可以应用于类的源语言修饰符组合在一起。  |
| `static int constructorModifiers()` | 返回一个int值，或者将可以应用于构造函数的源语言修饰符组合在一起。 |
| `static int fieldModifiers()`       | 返回一个int值，或者将可以应用于字段的源语言修饰符组合在一起。 |
| `static int interfaceModifiers()`   | 返回一个int值，或者将可以应用于接口的源语言修饰符组合在一起。 |
| `static boolean isXxx(int mod)`     | 如果整数参数包含Xxx修饰符（Xxx代表Abstract、Final、Native、Private、Protected、Public、Static、Strict、Synchronized、Transient、Volatile），则返回true，否则返回false。<br />参数**mod** - 一组修饰符。 |
| `static int methodModifiers()`      | 返回一个int值，或者将可以应用于方法的源语言修饰符组合在一起。 |

## 2.4 `java.lang.reflect.Constructor`

`java.lang.reflect.Constructor`类是`java.lang.reflect.Executable`类的直接子类，用于表示类的构造方法。通过Class对象的`getConstructors()`方法可以获得当前运行时类的构造方法。

类的声明为：

```java
public final class Constructor<T>
   extends AccessibleObject
      implements GenericDeclaration, Member
```

`java.lang.reflect.Constructor`类提供有关类的单个构造函数的信息和访问权限（继承自`java.lang.reflect.AccessibleObject`）：

| 常用方法                            | 说明                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| `String getName()`                  | 以字符串形式返回此构造函数的名称。 这是构造函数声明类的二进制名称。 |
| `T newInstance(Object... initargs)` | 使用此Constructor对象表示的构造函数，使用指定的初始化参数创建和初始化构造函数声明类的新实例。 各个参数自动展开以匹配原始形式参数，并且原始参数和参考参数都根据需要进行方法调用转换。<br />参数**initargs** - 要作为构造函数调用的参数传递的对象数组; 原始类型的值包装在适当类型的包装器对象中（例如Float中的float） |

## 2.5 `java.lang.reflect.Method`

`java.lang.reflect.Method`类提供有关类或接口上的单个方法的信息和访问权限。 反射的方法可以是类方法或实例方法（包括抽象方法）。 方法允许在将实际参数与基础方法的形式参数进行匹配时进行扩展转换，但如果发生缩小转换，则会抛出IllegalArgumentException。

此类声明为：

```java
public final class Method<T>
   extends AccessibleObject
      implements GenericDeclaration, Member
```

| 常用方法                                    | 说明                                                         |
| ------------------------------------------- | ------------------------------------------------------------ |
| `String getName()`                          | 以字符串形式返回此方法的名称。 这是方法声明类的二进制名称。  |
| `Class<?> getReturnType()`                  | 返回一个Class对象，该对象表示此Method对象表示的方法的正式返回类型。 |
| `Object invoke(Object obj, Object... args)` | 在具有指定参数的指定对象上调用此Method对象表示的基础方法。 各个参数自动展开以匹配原始形式参数，并且原始参数和参考参数都根据需要进行方法调用转换。<br />参数**obj** - 从中调用基础方法的对象。<br />参数**args** - 用于方法调用的参数。 |
| `boolean isBridge()`                        | 如果此方法是桥接方法，则返回true; 否则返回false。            |

## 2.6 `java.lang.reflect.Field`

`java.lang.reflect.Field`类提供有关类或接口的单个字段的信息和动态访问。 反射字段可以是类（静态）字段或实例字段。 Field允许在get或set访问操作期间进行扩展转换，但如果发生收缩转换则抛出IllegalArgumentException。

此类声明为：

```java
public final class Field
   extends AccessibleObject
      implements Member
```

| 常用方法                           | 说明                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| `String getName()`                 | 返回此Field对象表示的字段的名称。                            |
| `Xxx getXxx()`                     | 返回成员变量的值，其中Xxx代表基本类型，如果成员变量是引用类型，则直接使用`Object get(Object obj)`方法<br />参数**obj** - 从中提取所表示字段值的对象。 |
| `void setXxx(Object obj, Xxx val)` | 设置成员变量的值，其中Xxx代表基本类型，如果成员变量是引用类型，则直接使用`set(Object obj, Object val)`方法。<br />参数**obj** - 从中提取所表示字段值的对象。<br />参数**value** - 要修改的obj字段的新值。 |
| `Class<?> getType()`               | 返回一个Class对象，该对象标识由此Field对象表示的字段的声明类型。 |