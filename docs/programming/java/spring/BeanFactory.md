# BeanFactory

Spring容器是Spring的核心，它可以创建对象，把他们关联在一起，配置各个对象，并管理每个对象的整个生命周期。Spring容器使用依赖注入（DI）来管理组成一个应用程序的组件。这些对象被称为Spring Beans （一个对象就是一个Bean）。

Spring中有两种容器：

- BeanFactory：一个最简单的Spring容器，给依赖注入（DI）提供了基础的支持。

- ApplicationContext：此容器添加以一些企业需要用到的东西，更加全面。它包含了BeanFactory容器中的东西。

BeanFactory的功能：

- 可以将原来硬编码的依赖，通过Spring这个beanFactory这个工厂来注入依赖，也就是说原来只有依赖方和被依赖方，现在我们引入了第三方——spring这个beanFactory，由它来解决bean之间的依赖问题，达到了松耦合的效果；
- 在没有spring这个beanFactory之前，我们都是直接通过new来实例化各种对象，现在各种对象bean的生产都是通过beanFactory来实例化的，这样的话，spring这个beanFactory就可以在实例化bean的过程中，做一些小动作——在实例化bean的各个阶段进行一些额外的处理，也就是说beanFactory会在bean的生命周期的各个阶段中对bean进行各种管理，并且spring将这些阶段通过各种接口暴露给我们，让我们可以对bean进行各种处理，我们只要让bean实现对应的接口，那么spring就会在bean的生命周期调用我们实现的接口来处理该bean。

因为bean的实例化必须在bean容器启动之后，所以BeanFactory的启动分为两个阶段：

- Bean容器（BeanFactory）的启动阶段；
- 容器中bean的实例化阶段。





# 1 BeanFactory

```java
package org.springframework.beans.factory;

import org.springframework.beans.BeansException;
import org.springframework.core.ResolvableType;
import org.springframework.lang.Nullable;

/**
 * 用于访问Spring bean容器的基础接口。这是bean容器的基本客户端视图。 还有其他接口，例如{@link ListableBeanFactory}和{@link org.springframework.beans.factory.config.ConfigurableBeanFactory}可用于特定目的。
 *
 * 该接口由包含多个bean definition的对象实现，每个bean definition均由字符串名称唯一标识。 根据bean definition，工厂将返回所包含对象的独立实例（Prototype设计模式），或者返回单个共享实例（Singleton设计模式的替代方案，其中实例是作用域中的单例） 的工厂）。 将返回哪种类型的实例取决于bean工厂的配置：API是相同的。 从Spring 2.0开始，根据具体的应用程序上下文，可以使用更多作用域（例如，Web环境中的“request”和“session”作用域）。
 *
 * 这种方法的重点是BeanFactory是应用程序组件的中央注册表，并集中了应用程序组件的配置（例如，不再需要单个对象读取属性文件）。有关此方法的好处的讨论，请参见“一对一J2EE专家设计和开发”的第4章和第11章。
 *
 * 请注意，通常最好依赖于依赖注入（“push”配置）通过setter或constructor配置应用程序对象，而不是使用任何形式的“pull”配置（例如BeanFactory查找）。 Spring的依赖注入功能是使用此BeanFactory接口及其子接口实现的。
 *
 * 通常，BeanFactory将加载存储在配置源（例如XML文档）中的bean definition，并使用{@code org.springframework.beans}包来配置bean。但是，在实现中可以根据需要直接在Java代码中直接返回它创建的Java对象。definition的存储方式没有任何限制：LDAP，RDBMS，XML，propertie文件等。鼓励使用支持Bean之间的引用（依赖注入）的方式来实现。
 *
 * 与{@link ListableBeanFactory}中的方法相比，此接口中的所有操作还将检查父工厂是否为{@link HierarchicalBeanFactory}。 如果在此工厂实例中未找到bean，则将询问直接的父工厂。该工厂实例中的Bean会覆盖任何父工厂中的同名bean。
 *
 * Bean工厂实现应尽可能支持标准Bean生命周期接口。全部初始化方法及其标准顺序为：
 * 1. BeanNameAware's {@code setBeanName}
 * 2. BeanClassLoaderAware's {@code setBeanClassLoader}
 * 3. BeanFactoryAware's {@code setBeanFactory}
 * 4. EnvironmentAware's {@code setEnvironment}
 * 5. EmbeddedValueResolverAware's {@code setEmbeddedValueResolver}
 * 6. ResourceLoaderAware's {@code setResourceLoader}
 * （仅在应用程序上下文中运行时适用）
 * 7. ApplicationEventPublisherAware's {@code setApplicationEventPublisher}
 * （仅在应用程序上下文中运行时适用）
 * 8. MessageSourceAware's {@code setMessageSource}
 * （仅在应用程序上下文中运行时适用）
 * 9. ApplicationContextAware's {@code setApplicationContext}
 * （仅在应用程序上下文中运行时适用）
 * 10. ServletContextAware's {@code setServletContext}
 * （仅在WEB应用程序上下文中运行时适用）
 * 11. {@code postProcessBeforeInitialization} methods of BeanPostProcessors
 * 12. InitializingBean's {@code afterPropertiesSet}
 * 13. a custom init-method definition
 * 14. {@code postProcessAfterInitialization} methods of BeanPostProcessors
 *
 * 在关闭bean工厂时，以下生命周期方法适用：
 * 1. {@code postProcessBeforeDestruction} methods of DestructionAwareBeanPostProcessors
 * 2. DisposableBean's {@code destroy}
 * 3. a custom destroy-method definition
 */
public interface BeanFactory {

    // FactroyBean的前缀，如果getBean的时候BeanName有这个前缀，会去获取对应的FactroyBean, 而不是获取FactroyBean的getObject返回的Bean
	String FACTORY_BEAN_PREFIX = "&";

    // 获取指定的Bean:根据名称
	Object getBean(String name) throws BeansException;

	// 获取指定的Bean:根据名称和类型，类型可以为接口和父类的Class
	<T> T getBean(String name, Class<T> requiredType) throws BeansException;

	/**
	 * Return an instance, which may be shared or independent, of the specified bean.
	 * <p>Allows for specifying explicit constructor arguments / factory method arguments,
	 * overriding the specified default arguments (if any) in the bean definition.
	 * @param name the name of the bean to retrieve
	 * @param args arguments to use when creating a bean instance using explicit arguments
	 * (only applied when creating a new instance as opposed to retrieving an existing one)
	 * @return an instance of the bean
	 * @throws NoSuchBeanDefinitionException if there is no such bean definition
	 * @throws BeanDefinitionStoreException if arguments have been given but
	 * the affected bean isn't a prototype
	 * @throws BeansException if the bean could not be created
	 * @since 2.5
	 */
	Object getBean(String name, Object... args) throws BeansException;

	/**
	 * Return the bean instance that uniquely matches the given object type, if any.
	 * <p>This method goes into {@link ListableBeanFactory} by-type lookup territory
	 * but may also be translated into a conventional by-name lookup based on the name
	 * of the given type. For more extensive retrieval operations across sets of beans,
	 * use {@link ListableBeanFactory} and/or {@link BeanFactoryUtils}.
	 * @since 3.0
	 * @see ListableBeanFactory
	 */
	<T> T getBean(Class<T> requiredType) throws BeansException;

	/**
	 * Return an instance, which may be shared or independent, of the specified bean.
	 * <p>Allows for specifying explicit constructor arguments / factory method arguments,
	 * overriding the specified default arguments (if any) in the bean definition.
	 * <p>This method goes into {@link ListableBeanFactory} by-type lookup territory
	 * but may also be translated into a conventional by-name lookup based on the name
	 * of the given type. For more extensive retrieval operations across sets of beans,
	 * use {@link ListableBeanFactory} and/or {@link BeanFactoryUtils}.
	 * @param requiredType type the bean must match; can be an interface or superclass
	 * @param args arguments to use when creating a bean instance using explicit arguments
	 * (only applied when creating a new instance as opposed to retrieving an existing one)
	 * @since 4.1
	 */
	<T> T getBean(Class<T> requiredType, Object... args) throws BeansException;

	/**
	 * Return a provider for the specified bean, allowing for lazy on-demand retrieval
	 * of instances, including availability and uniqueness options.
	 * @param requiredType type the bean must match; can be an interface or superclass
	 * @return a corresponding provider handle
	 * @since 5.1
	 * @see #getBeanProvider(ResolvableType)
	 */
	<T> ObjectProvider<T> getBeanProvider(Class<T> requiredType);

	/**
	 * Return a provider for the specified bean, allowing for lazy on-demand retrieval
	 * of instances, including availability and uniqueness options.
	 * @param requiredType type the bean must match; can be a generic type declaration.
	 * Note that collection types are not supported here, in contrast to reflective
	 * injection points. For programmatically retrieving a list of beans matching a
	 * specific type, specify the actual bean type as an argument here and subsequently
	 * use {@link ObjectProvider#orderedStream()} or its lazy streaming/iteration options.
	 * @return a corresponding provider handle
	 * @since 5.1
	 * @see ObjectProvider#iterator()
	 * @see ObjectProvider#stream()
	 * @see ObjectProvider#orderedStream()
	 */
	<T> ObjectProvider<T> getBeanProvider(ResolvableType requiredType);

	/**
	 * Does this bean factory contain a bean definition or externally registered singleton
	 * instance with the given name?
	 * <p>If the given name is an alias, it will be translated back to the corresponding
	 * canonical bean name.
	 * <p>If this factory is hierarchical, will ask any parent factory if the bean cannot
	 * be found in this factory instance.
	 * <p>If a bean definition or singleton instance matching the given name is found,
	 * this method will return {@code true} whether the named bean definition is concrete
	 * or abstract, lazy or eager, in scope or not. Therefore, note that a {@code true}
	 * return value from this method does not necessarily indicate that {@link #getBean}
	 * will be able to obtain an instance for the same name.
	 * @param name the name of the bean to query
	 * @return whether a bean with the given name is present
	 */
	boolean containsBean(String name);

	/**
	 * Is this bean a shared singleton? That is, will {@link #getBean} always
	 * return the same instance?
	 * <p>Note: This method returning {@code false} does not clearly indicate
	 * independent instances. It indicates non-singleton instances, which may correspond
	 * to a scoped bean as well. Use the {@link #isPrototype} operation to explicitly
	 * check for independent instances.
	 * <p>Translates aliases back to the corresponding canonical bean name.
	 * Will ask the parent factory if the bean cannot be found in this factory instance.
	 * @param name the name of the bean to query
	 * @return whether this bean corresponds to a singleton instance
	 * @throws NoSuchBeanDefinitionException if there is no bean with the given name
	 * @see #getBean
	 * @see #isPrototype
	 */
	boolean isSingleton(String name) throws NoSuchBeanDefinitionException;

	/**
	 * Is this bean a prototype? That is, will {@link #getBean} always return
	 * independent instances?
	 * <p>Note: This method returning {@code false} does not clearly indicate
	 * a singleton object. It indicates non-independent instances, which may correspond
	 * to a scoped bean as well. Use the {@link #isSingleton} operation to explicitly
	 * check for a shared singleton instance.
	 * <p>Translates aliases back to the corresponding canonical bean name.
	 * Will ask the parent factory if the bean cannot be found in this factory instance.
	 * @param name the name of the bean to query
	 * @return whether this bean will always deliver independent instances
	 * @throws NoSuchBeanDefinitionException if there is no bean with the given name
	 * @since 2.0.3
	 * @see #getBean
	 * @see #isSingleton
	 */
	boolean isPrototype(String name) throws NoSuchBeanDefinitionException;

	/**
	 * Check whether the bean with the given name matches the specified type.
	 * More specifically, check whether a {@link #getBean} call for the given name
	 * would return an object that is assignable to the specified target type.
	 * <p>Translates aliases back to the corresponding canonical bean name.
	 * Will ask the parent factory if the bean cannot be found in this factory instance.
	 * @param name the name of the bean to query
	 * @param typeToMatch the type to match against (as a {@code ResolvableType})
	 * @return {@code true} if the bean type matches,
	 * {@code false} if it doesn't match or cannot be determined yet
	 * @throws NoSuchBeanDefinitionException if there is no bean with the given name
	 * @since 4.2
	 * @see #getBean
	 * @see #getType
	 */
	boolean isTypeMatch(String name, ResolvableType typeToMatch) throws NoSuchBeanDefinitionException;

	/**
	 * Check whether the bean with the given name matches the specified type.
	 * More specifically, check whether a {@link #getBean} call for the given name
	 * would return an object that is assignable to the specified target type.
	 * <p>Translates aliases back to the corresponding canonical bean name.
	 * Will ask the parent factory if the bean cannot be found in this factory instance.
	 * @param name the name of the bean to query
	 * @param typeToMatch the type to match against (as a {@code Class})
	 * @return {@code true} if the bean type matches,
	 * {@code false} if it doesn't match or cannot be determined yet
	 * @throws NoSuchBeanDefinitionException if there is no bean with the given name
	 * @since 2.0.1
	 * @see #getBean
	 * @see #getType
	 */
	boolean isTypeMatch(String name, Class<?> typeToMatch) throws NoSuchBeanDefinitionException;

	/**
	 * Determine the type of the bean with the given name. More specifically,
	 * determine the type of object that {@link #getBean} would return for the given name.
	 * <p>For a {@link FactoryBean}, return the type of object that the FactoryBean creates,
	 * as exposed by {@link FactoryBean#getObjectType()}. This may lead to the initialization
	 * of a previously uninitialized {@code FactoryBean} (see {@link #getType(String, boolean)}).
	 * <p>Translates aliases back to the corresponding canonical bean name.
	 * Will ask the parent factory if the bean cannot be found in this factory instance.
	 * @param name the name of the bean to query
	 * @return the type of the bean, or {@code null} if not determinable
	 * @throws NoSuchBeanDefinitionException if there is no bean with the given name
	 * @since 1.1.2
	 * @see #getBean
	 * @see #isTypeMatch
	 */
	@Nullable
	Class<?> getType(String name) throws NoSuchBeanDefinitionException;

	/**
	 * Determine the type of the bean with the given name. More specifically,
	 * determine the type of object that {@link #getBean} would return for the given name.
	 * <p>For a {@link FactoryBean}, return the type of object that the FactoryBean creates,
	 * as exposed by {@link FactoryBean#getObjectType()}. Depending on the
	 * {@code allowFactoryBeanInit} flag, this may lead to the initialization of a previously
	 * uninitialized {@code FactoryBean} if no early type information is available.
	 * <p>Translates aliases back to the corresponding canonical bean name.
	 * Will ask the parent factory if the bean cannot be found in this factory instance.
	 * @param name the name of the bean to query
	 * @param allowFactoryBeanInit whether a {@code FactoryBean} may get initialized
	 * just for the purpose of determining its object type
	 * @return the type of the bean, or {@code null} if not determinable
	 * @throws NoSuchBeanDefinitionException if there is no bean with the given name
	 * @since 5.2
	 * @see #getBean
	 * @see #isTypeMatch
	 */
	@Nullable
	Class<?> getType(String name, boolean allowFactoryBeanInit) throws NoSuchBeanDefinitionException;

	/**
	 * Return the aliases for the given bean name, if any.
	 * All of those aliases point to the same bean when used in a {@link #getBean} call.
	 * <p>If the given name is an alias, the corresponding original bean name
	 * and other aliases (if any) will be returned, with the original bean name
	 * being the first element in the array.
	 * <p>Will ask the parent factory if the bean cannot be found in this factory instance.
	 * @param name the bean name to check for aliases
	 * @return the aliases, or an empty array if none
	 * @see #getBean
	 */
	String[] getAliases(String name);

}
```





