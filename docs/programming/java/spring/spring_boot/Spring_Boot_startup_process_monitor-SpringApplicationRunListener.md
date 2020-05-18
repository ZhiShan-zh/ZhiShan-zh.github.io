# Spring Boot启动流程监听器SpringApplicationRunListener

# 1 概述

SpringApplicationRunListener 接口的作用主要就是在Spring Boot 启动初始化的过程中可以通过回调的方式调用SpringApplicationRunListener接口中相应的方法来让用户在启动的各个流程中加入自己的逻辑。

`org.springframework.boot.SpringApplicationRunListener`接口定义：

```java
package org.springframework.boot;

import org.springframework.context.ApplicationContext;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.core.env.ConfigurableEnvironment;
import org.springframework.core.io.support.SpringFactoriesLoader;

/**
 * Listener for the {@link SpringApplication} {@code run} method.
 * {@link SpringApplicationRunListener}s are loaded via the {@link SpringFactoriesLoader}
 * and should declare a public constructor that accepts a {@link SpringApplication}
 * instance and a {@code String[]} of arguments. A new
 * {@link SpringApplicationRunListener} instance will be created for each run.
 *
 * @author Phillip Webb
 * @author Dave Syer
 * @author Andy Wilkinson
 * @since 1.0.0
 */
public interface SpringApplicationRunListener {

	/**
	 * 当run()方法开始执行，可以用于最早期做一些准备工作
	 * Called immediately when the run method has first started. Can be used for very
	 * early initialization.
	 */
	default void starting() {
	}

	/**
	 * 当ConfigurableEnvironment构建完成，但是ApplicationContext还没有创建
	 * Called once the environment has been prepared, but before the
	 * {@link ApplicationContext} has been created.
	 * @param environment the environment
	 */
	default void environmentPrepared(ConfigurableEnvironment environment) {
	}

	/**
	 * 当ApplicationContext构建完成，但还未加载
	 * Called once the {@link ApplicationContext} has been created and prepared, but
	 * before sources have been loaded.
	 * @param context the application context
	 */
	default void contextPrepared(ConfigurableApplicationContext context) {
	}

	/**
	 * 当ApplicationContext加载完成，但还未刷新
	 * Called once the application context has been loaded but before it has been
	 * refreshed.
	 * @param context the application context
	 */
	default void contextLoaded(ConfigurableApplicationContext context) {
	}

	/**
	 * 当ApplicationContext刷新完成，应用已经启动，但是CommandLineRunners和ApplicationRunners还没被调用
	 * The context has been refreshed and the application has started but
	 * {@link CommandLineRunner CommandLineRunners} and {@link ApplicationRunner
	 * ApplicationRunners} have not been called.
	 * @param context the application context.
	 * @since 2.0.0
	 */
	default void started(ConfigurableApplicationContext context) {
	}

	/**
	 * 当应用启动完成前，ApplicationContext已经刷新完成，CommandLineRunners和ApplicationRunners已经被调用
	 * Called immediately before the run method finishes, when the application context has
	 * been refreshed and all {@link CommandLineRunner CommandLineRunners} and
	 * {@link ApplicationRunner ApplicationRunners} have been called.
	 * @param context the application context.
	 * @since 2.0.0
	 */
	default void running(ConfigurableApplicationContext context) {
	}

	/**
	 * 当运行应用出错时
	 * Called when a failure occurs when running the application.
	 * @param context the application context or {@code null} if a failure occurred before
	 * the context was created
	 * @param exception the failure
	 * @since 2.0.0
	 */
	default void failed(ConfigurableApplicationContext context, Throwable exception) {
	}
}
```

# 2 自定义SpringApplicationRunListener

我们可以通过实现接口`org.springframework.boot.SpringApplicationRunListener`来自定义SpringApplicationRunListener，以此监听Spring Boot的启动流程，并在各个流程中通过回调函数的方法调用实现类中对应的方法来实现自己的处理逻辑。

必须要提供一个参数列表为`(SpringApplication application, String[] args)`的构造函数。

还需要在工程`src/META-INF/spring.factories`文件中字段`org.springframework.boot.SpringApplicationRunListener`中加入自定义的SpringApplicationRunListener的实现类，示例：

```properties
# Run Listeners
org.springframework.boot.SpringApplicationRunListener=\
org.springframework.boot.context.event.EventPublishingRunListener
```
