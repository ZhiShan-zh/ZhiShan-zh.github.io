# final关键词

# 1 final概述
遇到final时请记住一句话一旦被赋值则不可另外再改变。如果final修饰变量指向对象，则对象中的成员变量可以改变。

final修饰的变量在编译的时候已经分配内存。

# 2 final修饰参数
**概述：** 在方法参数前面加final关键字就是为了防止数据在方法体中被修改。

**主要分两种情况：**

1. 用final修饰基本数据类型；
1. 用final修饰引用类型。

## 2.1 修饰基本类型（非引用类型）
这时参数的值在方法体内是不能被修改的，即不能被重新赋值。否则编译就通不过。 并且数据类型不会自动提升。 例如：
```java
public static void valid(final int ag){
    ag=9;
}
```
错误提示： `The final local variable ag cannot be assigned.It must be blank and not using a compound assignment`

## 2.2 修饰引用类型
这时参数变量所引用的对象是不能被改变的。作为引用的拷贝，参数在方法体里面不能再引用新的对象。否则编译通不过。例如：
```java
public static void valid(final String[] ag){
    ag=new String[9];
}
```
这个的提示和上面是一样的。：`The final local variable param2 cannot be assigned. It must be blank and not using a compound assignment.`

但是对于引用，如果我是这样，则不会报任何错，完全能编译通过。

```java
public static void valid(final String[] ag){
    ag[0]="5";
    System.out.println(ag);
}
```
所以，final这个关键字，想用的话就用基本类型，还是很有作用的。引用类型，还是算了吧。

# 3 final修饰类、方法

1. final 修饰类时表明该类不能被继承，自然类中的方法默认是final型的。
1. final 修饰方法时不允许被子类重写，但可以被继承。一个final类中，一个final方法只能被实现一次。

**父类：**
```java
public class Test1 {  
  public final void show(){  
      System.out.println("this is super class");  
  }  
}
```
**子类：**
```java
public class Test extends Test1 {  
//  public void show(){   //这里如果企图重写覆盖父类中final修饰的方法会报错。      
//  }  
    public static void main(String[] args){  
        Test t=new Test();  
        t.show();  
    }  
}
```


# 4 final修饰变量
final 修饰的成员变量只能被赋值一次。如果是引用类型的变量，则不能让该变量再去指向其他对象。

**引用类型错误例子：**

```java
Object a=new Object();  
final Object  b=a; //b为a的引用变量，当改变b的指向时，如下一行会报错  
b=new Object();  //报错
```
**变量类型错误：** 如果所指的变量重新赋值会出现什么情况呢，如下面中的a变化时，b会如何呢？
```java
public static void main(String[] args){  
    int a=1;  
    final int b=a;  
    System.out.println(a);  
    System.out.println(b);  
    a=2;  
    System.out.println(a);  
    System.out.println(b); 
}
```
输出：

```
1
1
2
1
```

**final类中的成员变量：**

```java
public final class Test {  
    int a=3;  
    public static void main(String[] args){  
        Test b=new Test();  
        b.a=4; //如果a添加final修饰则会报错  
        System.out.println(b.a); //这里输出值为4.  
    }  
}
```
**final在修饰类中成员变量时可以不给初值，但是必须保证在使用前初始化**。尽管如此，这也提供了很大的灵活性。尽管初始化之后不能再改变，但通过构造函数，我们可以让final变量依据使用对象而改变。如下：
```java
public class Test1 {  
    public final int a; //这里声明的final型变量可以不赋值，但是必须给出一个类似的构造函数，不能使用普通方法赋值。如果子类继承该类则必须在构造方法中给出一个确定的值。这都是因为final类型变量必须在使用之前初始化 
    public Test1(int a){  
        this.a=a;  
    }  
}
```


