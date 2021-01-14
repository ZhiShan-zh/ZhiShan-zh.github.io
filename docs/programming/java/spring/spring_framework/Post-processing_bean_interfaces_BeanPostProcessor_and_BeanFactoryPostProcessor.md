# 后处理bean的接口BeanPostProcessor和BeanFactoryPostProcessor

# 1 概述



spring会自动从它的所有的bean定义中检测BeanPostProcessor类型的bean定义，然后实例化它们，再将它们应用于随后创建的每一个bean实例。

## 1.1 作用

- **BeanFactoryPostProcessor**：在所有的bean definition信息已经加载但还没有实例化时，执行方法postProcessBeanFactory()

- **BeanPostProcessor**：在bean的初始化前后进行一些操作

# 2 BeanPostProcessor

运行顺序：

1. Spring IOC容器实例化Bean
2. 调用BeanPostProcessor的postProcessBeforeInitialization方法
3. 调用bean实例的初始化方法
4. 调用BeanPostProcessor的postProcessAfterInitialization方法

```java
package org.springframework.beans.factory.config;

import org.springframework.beans.BeansException;

public interface BeanPostProcessor {

	/**
	 * 运行时机：Spring IOC容器实例化Bean之后，调用bean实例的初始化方法之前调用
	 * 注意：返回值必须为此给定bean，或其包装类型，否则我们在程序中将获取不到bean
	 */
	@Nullable
	default Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
		return bean;
	}

	/**
	 * 运行时机：Spring IOC容器实例化Bean并且调用bean实例的初始化方法之后调用
	 * 注意：返回值必须为此给定bean，或其包装类型，否则我们在程序中将获取不到bean
	 */
	@Nullable
	default Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
		return bean;
	}
}
```

# 3 BeanFactoryPostProcessor

BeanFactoryPostProcessor可以与bean definitions打交道，但是千万不要进行bean实例化，进行了实例化操作的后果：

- **使用注解进行依赖注入失败**；
- 在Spring Boot启动的时候调用`org.springframework.context.support.AbstractApplicationContext`的`refresh()`，此方法中`postProcessBeanFactory(beanFactory);`在`registerBeanPostProcessors(beanFactory);`之前调用。
  - `@AutoWired`起作用依赖AutowiredAnnotationBeanPostProcessor，`@Resource`依赖CommonAnnotationBeanPostProcessor，这俩都是BeanPostProcessor的实现。
  - 如果bean被提前实例化，则AutowiredAnnotationBeanPostProcessor和CommonAnnotationBeanPostProcessor还没注册，也就无法执行了。

```java
package org.springframework.beans.factory.config;

import org.springframework.beans.BeansException;

@FunctionalInterface
public interface BeanFactoryPostProcessor {

	/**
	 * 在bean definitions已经加载，但还未被实例化之前调用，在这个方法里可以修改bean definitions，可以对其修改和增加属性
	 */
	void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) throws BeansException;
}
```
