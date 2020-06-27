# Java中编译时常量和运行时常量

根据编译器的不同行为，常量又分为编译时常量和运行时常量，其实编译时常量肯定就是运行时常量，只是编译时常量在编译的时候就被执行计算，并带入到程序中一切可能用到它的计算式中。

**编译时常量**：

- 编译时就可以确定其具体值的常量，并且此值不依赖于类。
- **用final关键字修饰的基本类型或String类型并直接赋值（非复杂运算的赋值）的变量（无论是否用static修饰）**
- 是编译器的一种优化，体现在字节码文件中
- **所有引用其他类中静态编译时常量（一般就叫静态常量，用static final修饰）的类在字节码中全部替换为相应常量的值，所以引用静态常量并不会触发该类的的初始化。**
- 运行是常量是由**运行时解释器解释完成的**

**运行时常量**：

- 编译时无法确定值的常量，并且其值依赖于类。
- **程序在运行时才能确定值的一种常量**

比如，Java示例代码：

```java
class Constant {
    public static final int compileConstant = 10;
    public static final int runtimeConstant = "test".length();
    static {
        System.out.println("Class Constant was loaded!");
    }
}

public class ConstantTest {
    public static void main(String[] args) {
        System.out.println(Constant.compileConstant);
        System.out.println("编译时常量加载完毕！");
        System.out.println(Constant.runtimeConstant);
    }
}
```

输出：

```
10
编译时常量加载完毕！
Class Constant was loaded!
4
```

- `static final int compileConstant = 1;`将是一个编译时常量，编译后的符号表中将找不到a，所有对a的引用都被替换成了1。
- `static final int b = “”.length();`将是一个运行时常量。

1. compileConstant被作为编译期全局常量，并不依赖于类，而runtimeConstant作为运行期的全局常量，其值还是依赖于类的。
2. 编译时常量在编译时就可以确定值，上例中的compileConstant可以确定值，但是runtimeConstant在编译期是不可能确定值的。
3. 由于编译时常量不依赖于类，所以对编译时常量的访问不会引发类的初始化。

示例：

```java
public class ConstantTest {
    public final int a = 1;     //编译时常量
    public final int b = 1+2;   //编译时常量 支持加减乘除等简单运算
    public final int c = b+3;   //编译时常量 
    public final static int d = 10;   //编译时常量 
    public final String str1 = "conpileConstant"; //编译时常量 
    public final String str2 = "com" + "pile";  //编译时常量 支持字符串的连接
    public final String str3 = str2 + "Constant";  //编译时常量 
    public final static String str4 = "final static string";  //编译时常量 
    public final double random = Math.random(); //运行时常量
    public final ConstantTest test = new ConstantTest(); //运行时常量
}
```

