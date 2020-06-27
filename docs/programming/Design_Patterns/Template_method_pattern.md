# 模板方法模式

# 1 模板方法模式概述

## 1.1 定义
定义一个操作的算法骨架，而将一些步骤延迟到子类中。Template Method使得子类可以不改变一个算法的结构即可重定义该算法的某些特定步骤。

## 1.2 源码应用

- `javax.servlet.http.HttpServlet`
- `org.springframework.web.servlet.mvc.AbstractController`

## 1.3 应用场景

- 比如项目中需要对PDF和word文档进行处理，整个流程是一样的，但对与这两种文档的处理方法不同，此时则可使用模板方法模式。

# 2 入门案例

```java
package com.zh.templatemethod;
public class TemplateMethodTest {
    public static void main(String[] args) {
        AbstractClass subClass = new SubClass();
        subClass.operation();
    }
}
abstract class AbstractClass{
    public void operation() {
        System.out.println("pre ...");
        System.out.println("step1");
        System.out.println("step2");
        templateMethod();
        System.out.println("end ...");
    }
    
    abstract protected void templateMethod();
}
class SubClass extends AbstractClass{
    @Override
    protected void templateMethod() {
        System.out.println("SubClass.templateMethod executed");
    }
}
```

