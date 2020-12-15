# BeanFactory

BeanFactory的功能：

- 可以将原来硬编码的依赖，通过Spring这个beanFactory这个工厂来注入依赖，也就是说原来只有依赖方和被依赖方，现在我们引入了第三方——spring这个beanFactory，由它来解决bean之间的依赖问题，达到了松耦合的效果；
- 在没有spring这个beanFactory之前，我们都是直接通过new来实例化各种对象，现在各种对象bean的生产都是通过beanFactory来实例化的，这样的话，spring这个beanFactory就可以在实例化bean的过程中，做一些小动作——在实例化bean的各个阶段进行一些额外的处理，也就是说beanFactory会在bean的生命周期的各个阶段中对bean进行各种管理，并且spring将这些阶段通过各种接口暴露给我们，让我们可以对bean进行各种处理，我们只要让bean实现对应的接口，那么spring就会在bean的生命周期调用我们实现的接口来处理该bean。

因为bean的实例化必须在bean容器启动之后，所以BeanFactory的启动分为两个阶段：

- Bean容器（BeanFactory）的启动阶段；
- 容器中bean的实例化阶段。

# 1 Bean容器（BeanFactory）的启动阶段

## 1.1 XML方式

读取bean的xml配置文件，然后解析xml文件中的各种bean的定义，将xml文件中的每一个`<bean />`元素分别转换成一个BeanDefinition对象，其中保存了从配置文件中读取到的该bean的各种信息：



## 1.2 注解方式



