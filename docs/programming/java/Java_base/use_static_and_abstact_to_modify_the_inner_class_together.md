# 使用static和abstract共同修饰内部类

以前一致人为static和abstact是不能同时出现的，但是后来发现，两者可以同时出现使用方法如下：

- 使用static和abstract共同修饰内部类（inner class A）
- 在此内部类的外部类中声明内部类（inner class B）来继承这个静态的抽象的内部类（inner class A）。

示例代码如下：

```java
public class Outer {
    static abstract class Inner1 {
        public abstract int fun(int len);
    }
    static class Inner2 extends Inner1 {
        public int fun(int len) {
            return len * 1024;
        }
    }
}
```

