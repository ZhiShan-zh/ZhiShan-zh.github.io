# Java Config

# 1 概述

Java Config是指基于java配置的spring。传统的Spring一般都是基本xml配置的，后来Spring3.0新增了许多Java Config的注解，特别是spring boot，使用的基本都是Java Config。

Spring IOC有一个非常核心的概念——Bean。由Spring容器来负责对Bean的实例化，装配和管理。XML是用来描述Bean最为流行的配置方式，Spring可以从XML配置文件中读取任何类型的元数据并自动转换成相应的Java代码。

当随着JAVA EE 5.0的发布，其中引入了一个非常重要的特性——Annotations(注释)。注释是源代码的标签，这些标签可以在源代码层进行处理或通过编译器把它熔入到class文件中。在JAVA EE 5以后的版本中，注释成为了一个主要的配置选项。Spring使用注释来描述Bean的配置与采用XML相比，因类注释是在一个类源代码中，可以获得类型安全检查的好处。可以良好的支持重构。

JavaConfig就是使用注释来描述Bean配置的组件。

# 2 XML和Java Config对比示例

## 2.1 XML

```xml
<?xml version="1.0" encoding="UTF-8"?>   
<beans xmlns="http://www.springframework.org/schema/beans"  
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
       xsi:schemaLocation="http://www.springframework.org/schema/beans   
                           http://www.springframework.org/schema/beans/spring-beans-3.2.xsd">   

    <bean id="button" class="javax.swing.JButton">   
        <constructor-arg value="Hello World" />   
    </bean>   

    <bean id="anotherButton" class="javax.swing.JButton">   
        <property name="icon" ref="icon" />   
    </bean>   

    <bean id="icon" class="javax.swing.ImageIcon">   
        <constructor-arg>   
            <bean class="java.net.URL">   
                <constructor-arg value="http://morevaadin.com/assets/images/learning_vaadin_cover.png" />   
            </bean>   
        </constructor-arg>   
    </bean>   
</beans> 
```

## 2.2 Java Config

```java
import java.net.MalformedURLException;  
import java.net.URL;  
import javax.swing.Icon;  
import javax.swing.ImageIcon;  
import javax.swing.JButton;  
import org.springframework.context.annotation.Bean;  
import org.springframework.context.annotation.Configuration;  

@Configuration  
public class MigratedConfiguration {  
    @Bean  
    public JButton button() {  
        return new JButton("Hello World");  
    }  

    @Bean  
    public JButton anotherButton(Icon icon) {  
        return new JButton(icon);  
    }  

    @Bean  
    public Icon icon() throws MalformedURLException {  
        URL url = new URL(  
            "http://morevaadin.com/assets/images/learning_vaadin_cover.png");  
        return new ImageIcon(url);  
    }  
} 
```

用法步骤：

1. 任何一个标注了@Configuration的Java类定义都是一个JavaConfig配置类。@Configuration的注解类标识这个类可以使用Spring IoC容器作为bean定义的来源。

2. 任何一个标注了@Bean的方法，其返回值将作为一个bean定义注册到Spring的IoC容器，方法名将默认成该bean定义的name。

注意在Web环境中，需要在web.xml中加入如下代码：

```xml
<context-param>  
    <param-name>contextClass</param-name>  
    <param-value>org.springframework.web.context.support.AnnotationConfigWebApplicationContext</param-value>  
</context-param>  
<context-param>  
    <param-name>contextConfigLocation</param-name>  
    <param-value>com.packtpub.learnvaadin.springintegration.SpringIntegrationConfiguration</param-value>  
</context-param> 
```

