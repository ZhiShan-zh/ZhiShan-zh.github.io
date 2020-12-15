# BeanDefinition

BeanDefinition即为Spring Bean的建模对象。

已经有了Java中的Class为什么还需要Spring Bean的建模对象呢？

>因为Class无法完成bean的抽象，比如bean的作用域，bean的注入模型，bean是否是懒加载等等信息，Class是无法抽象出来的，故而需要一个BeanDefinition类来抽象这些信息，以便于spring能够完美的实例化一个bean。
>
>简单理解spring当中的BeanDefinition就是java当中的Class：
>
>- Class可以用来描述一个类的属性和方法等等其他信息
>- BeanDefintion可以描述springbean当中的scope、lazy，以及属性和方法等等其他信息

继承关系：

BeanDefinition接口：

- 父
  - AttributeAccessor：用于附加和访问元数据的通用的接口，来自任意对象
  - BeanMetadataElement：