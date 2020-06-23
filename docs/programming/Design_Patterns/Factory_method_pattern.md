# 工厂方法模式

# 1 工厂方法模式概述
## 1.1 工厂方法模式定义
定义一个用于创建对象的接口，让子类决定实例化哪一个类，Factory Method使得一个类的实例化延迟到子类。
## 1.2 应用场景

1. 当你不知道该使用对象的确切类型的时候
1. 当你希望为库或框架提供扩展其内部组件的方法时
## 1.3 主要优点

1. 将具体产品和创建者解耦
1. 复合单一职责原则
1. 复合开闭原则
## 1.4 源代码中的应用
静态工厂方法：

- `Calendar.getInstance()`
- `java.text.NumberFormat.getInstance()`
- `java.util.ResourceBundle.getBundle()`

工厂方法：

- `java.net.URLStreamHandlerFactory`
- `javax.xml.bind.JAXBContext.createMarshaller`
# 2 简单工厂
## 2.1 简单工厂概述
它不算是一个设计模式，只算是一个编程的习惯。

不用每次都new它的实现，简单工厂是把实例化的过程封装起来，便于统一的管理。

## 2.2 简单工厂入门案例

```java
package com.zh.factorymethod;
public class SimpleProductTest {
    public static void main(String[] args) {
        ProductB productB = SimpleProduct.createProduct("0");
        productB.method();
    }
}
interface ProductB{
    public void method();
}
class ProductB1 implements ProductB{
    public void method() {
        System.out.println("ProductB1.method executed!");
    }
}
class ProductB2 implements ProductB{
    public void method() {
        System.out.println("ProductB2.method executed!");
    }
}
class SimpleProduct{
    public static ProductB createProduct(String type) {
        if(type.equals("0")) {
            return new ProductB1();
        }else if (type.equals("1")) {
            return new ProductB2();
        }else {
            return null;
        }
    }
}
```

# 3 工厂方法模式实现

```java
package com.zh.factorymethod;
public class FactoryMethod {
    public static void main(String[] args) {
        Application application = new ConcreteProductA();
        Product product = application.getObject();
        product.method1();
    }
}
interface Product{
    public void method1();
}
class ProductA implements Product{
    public void method1() {
        System.out.println("ProductA.method1 executed!");
    }
}
class ProductA1 implements Product{
    public void method1() {
        System.out.println("ProductA1.method1 executed!");
    }
}
abstract class Application{
    abstract Product createProduct();
    
    /**
     * 稳定部分
     * @param type
     * @return
     */
    Product getObject() {
        Product product = createProduct();
        return product;
    }
}
class ConcreteProductA extends Application{
    @Override
    Product createProduct() {
        return new ProductA();
    }
}
class ConcreteProductA1 extends Application{
    @Override
    Product createProduct() {
        return new ProductA1();
    }
}
```



