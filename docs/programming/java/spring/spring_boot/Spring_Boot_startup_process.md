[TOC]



# Spring Boot启动流程

springboot是基于spring的新型的轻量级框架，最厉害的地方当属自动配置。那我们就可以根据启动流程和相关原理来看看，如何实现传奇的自动配置。

# 1 入口函数main

```java
package com.zh.eurekaclient;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class EurekaClientApplication {
	public static void main(String[] args) {
		SpringApplication.run(EurekaClientApplication.class, args);
	}
}
```

# 2 创建SpringApplication实例

`org.springframework.boot.SpringApplication`

```java
public static ConfigurableApplicationContext run(Class<?> primarySource, String... args) {
    return run(new Class<?>[] { primarySource }, args);
}
```

使用入口类的Class组成的数组

```java
public static ConfigurableApplicationContext run(Class<?>[] primarySources, String[] args) {
    return new SpringApplication(primarySources).run(args);
}
```

```java
public SpringApplication(Class<?>... primarySources) {
    this(null, primarySources);
}
```

```java
@SuppressWarnings({ "unchecked", "rawtypes" })
public SpringApplication(ResourceLoader resourceLoader, Class<?>... primarySources) {
    this.resourceLoader = resourceLoader;
    Assert.notNull(primarySources, "PrimarySources must not be null");
    //保存主类
    this.primarySources = new LinkedHashSet<>(Arrays.asList(primarySources));
    //推断应用的类型
    this.webApplicationType = WebApplicationType.deduceFromClasspath();
    //加载文件META-INF/spring.factories中配置的org.springframework.context.ApplicationContextInitializer的实现类,并用反射的方式创建对应的实例
    setInitializers((Collection) getSpringFactoriesInstances(ApplicationContextInitializer.class));
    //加载文件META-INF/spring.factories中配置的org.springframework.context.ApplicationListener实现类，,并用反射的方式创建对应的实例
    setListeners((Collection) getSpringFactoriesInstances(ApplicationListener.class));
    //通过new RuntimeException().getStackTrace()得到方法的调用栈的数组，然后通过判断是否为main方法，获取main方法，并以此获取主类名
    this.mainApplicationClass = deduceMainApplicationClass();
}
```

位置：`org/springframework/boot/spring-boot/2.2.5.RELEASE/spring-boot-2.2.5.RELEASE.jar!/META-INF/spring.factories`

```properties
# Application Context Initializers
org.springframework.context.ApplicationContextInitializer=\
org.springframework.boot.context.ConfigurationWarningsApplicationContextInitializer,\
org.springframework.boot.context.ContextIdApplicationContextInitializer,\
org.springframework.boot.context.config.DelegatingApplicationContextInitializer,\
org.springframework.boot.rsocket.context.RSocketPortInfoApplicationContextInitializer,\
org.springframework.boot.web.context.ServerPortInfoApplicationContextInitializer

# Application Listeners
org.springframework.context.ApplicationListener=\
org.springframework.boot.ClearCachesApplicationListener,\
org.springframework.boot.builder.ParentContextCloserApplicationListener,\
org.springframework.boot.cloud.CloudFoundryVcapEnvironmentPostProcessor,\
org.springframework.boot.context.FileEncodingApplicationListener,\
org.springframework.boot.context.config.AnsiOutputApplicationListener,\
org.springframework.boot.context.config.ConfigFileApplicationListener,\
org.springframework.boot.context.config.DelegatingApplicationListener,\
org.springframework.boot.context.logging.ClasspathLoggingApplicationListener,\
org.springframework.boot.context.logging.LoggingApplicationListener,\
org.springframework.boot.liquibase.LiquibaseServiceLocatorApplicationListener
```

解释：

- `org.springframework.boot.context.ConfigurationWarningsApplicationContextInitializer`：report warnings for common misconfiguration mistakes
  - 在其`initialize(ConfigurableApplicationContext context)`方法中在context加入BeanFactoryPostProcessor的方法来实现

- `org.springframework.boot.context.ContextIdApplicationContextInitializer`：sets the Spring ApplicationContext ID，The `spring.application.name` property is used to create the ID.
  - 通过environment实例过去`spring.application.name`属性的值。
- `org.springframework.boot.context.config.DelegatingApplicationContextInitializer`：delegates to other initializers that are specified under a literal `context.initializer.classes` environment property
- `org.springframework.boot.rsocket.context.RSocketPortInfoApplicationContextInitializer`：sets Environment properties for the ports that RSocketServer servers are actually listening on. 
- `org.springframework.boot.web.context.ServerPortInfoApplicationContextInitializer`：sets Environment properties for the ports that WebServer servers are actually listening on.
  - 实现：`applicationContext.addApplicationListener(this)`
- `org.springframework.boot.ClearCachesApplicationListener`：to cleanup caches once the context is loaded.
- `org.springframework.boot.builder.ParentContextCloserApplicationListener`：closes the application context if its parent is closed.
- `org.springframework.boot.cloud.CloudFoundryVcapEnvironmentPostProcessor`：
- `org.springframework.boot.context.FileEncodingApplicationListener`：halts application startup if the system file encoding does not match an expected value set in the environment.
- `org.springframework.boot.context.config.AnsiOutputApplicationListener`：configures AnsiOutput depending on the value of the property `spring.output.ansi.enabled`.
- `org.springframework.boot.context.config.ConfigFileApplicationListener`：configures the context environment by loading properties from well known file locations.
- `org.springframework.boot.context.config.DelegatingApplicationListener`：delegates to other listeners that are specified under a `context.listener.classes` environment property.
- `org.springframework.boot.context.logging.ClasspathLoggingApplicationListener`：reacts to ApplicationEnvironmentPreparedEvent environment prepared events and to ApplicationFailedEvent failed events by logging the classpath of the thread context class loader (TCCL) at DEBUG level.
- `org.springframework.boot.context.logging.LoggingApplicationListener`：configures the LoggingSystem.
- `org.springframework.boot.liquibase.LiquibaseServiceLocatorApplicationListener`：replaces the liquibase ServiceLocator with a version that works with Spring Boot executable archives.



位置：`org/springframework/boot/spring-boot-autoconfigure/2.2.5.RELEASE/spring-boot-autoconfigure-2.2.5.RELEASE.jar!/META-INF/spring.factories`

```properties
# Initializers
org.springframework.context.ApplicationContextInitializer=\
org.springframework.boot.autoconfigure.SharedMetadataReaderFactoryContextInitializer,\
org.springframework.boot.autoconfigure.logging.ConditionEvaluationReportLoggingListener

# Application Listeners
org.springframework.context.ApplicationListener=\
org.springframework.boot.autoconfigure.BackgroundPreinitializer
```

解释：

- `org.springframework.boot.autoconfigure.SharedMetadataReaderFactoryContextInitializer`：create a shared CachingMetadataReaderFactory between the ConfigurationClassPostProcessor and Spring Boot.
  - 实现：`applicationContext.addBeanFactoryPostProcessor(new CachingMetadataReaderFactoryPostProcessor());`
- `org.springframework.boot.autoconfigure.logging.ConditionEvaluationReportLoggingListener`：writes the ConditionEvaluationReport to the log.
  - 实现：`applicationContext.addApplicationListener(new ConditionEvaluationReportListener());`
- `org.springframework.boot.autoconfigure.BackgroundPreinitializer`：trigger early initialization in a background thread of time consuming tasks.



## 2.1 推断应用类型：deduceFromClasspath()

`org.springframework.boot.WebApplicationType`的deduceFromClasspath方法：通过判断是否能加载指定的类来判断应用的类型

枚举类型WebApplicationType定义了三种应用类型：

- NONE：非Web应用程序
- SERVLET：基于J2EE Servlet API的编程模型，运行在Servlet容器上
- REACTIVE：Spring团队推出的Reactor编程模型的非阻塞异步Web编程框架WebFlux

```java
static WebApplicationType deduceFromClasspath() {
    /*
    private static final String WEBFLUX_INDICATOR_CLASS = "org.springframework.web.reactive.DispatcherHandler";
	private static final String WEBMVC_INDICATOR_CLASS = "org.springframework.web.servlet.DispatcherServlet";
	private static final String JERSEY_INDICATOR_CLASS = "org.glassfish.jersey.servlet.ServletContainer";
	能够加载WEBFLUX_INDICATOR_CLASS，且不能加载WEBMVC_INDICATOR_CLASS和JERSEY_INDICATOR_CLASS，则返回WebApplicationType.REACTIVE
    */
    if (ClassUtils.isPresent(WEBFLUX_INDICATOR_CLASS, null) && !ClassUtils.isPresent(WEBMVC_INDICATOR_CLASS, null)
        && !ClassUtils.isPresent(JERSEY_INDICATOR_CLASS, null)) {
        return WebApplicationType.REACTIVE;
    }
    /*
    private static final String[] SERVLET_INDICATOR_CLASSES = { "javax.servlet.Servlet", "org.springframework.web.context.ConfigurableWebApplicationContext" };
    不能加载SERVLET_INDICATOR_CLASSES，则返回WebApplicationType.NONE
    */
    for (String className : SERVLET_INDICATOR_CLASSES) {
        if (!ClassUtils.isPresent(className, null)) {
            return WebApplicationType.NONE;
        }
    }
    return WebApplicationType.SERVLET;
}
```

# 3 `new SpringApplication(primarySources).run(args)`



```java
// 运行spring应用，创建和更新一个新的ApplicationContext
public ConfigurableApplicationContext run(String... args) {
    //StopWatch是位于org.springframework.util包下的一个工具类，通过它可方便的对程序部分代码进行计时(ms级别)，适用于同步单线程代码块。
    StopWatch stopWatch = new StopWatch();
    stopWatch.start();
    ConfigurableApplicationContext context = null;
    Collection<SpringBootExceptionReporter> exceptionReporters = new ArrayList<>();
    // 配置java.awt.headless参数
    configureHeadlessProperty();
    //加载META-INF/spring.factories文件中 SpringApplicationRunListener 的实现类，并用反射的方式创建对应的实例
    SpringApplicationRunListeners listeners = getRunListeners(args);
    //调用所有SpringApplicationRunListener中的starting()
    listeners.starting();
    try {
        // 把参数args封装成DefaultApplicationArguments
        ApplicationArguments applicationArguments = new DefaultApplicationArguments(args);
        //准备环境，并且把环境跟spring上下文绑定好，并且执行SpringApplicationRunListener中environmentPrepared()方法
        ConfigurableEnvironment environment = prepareEnvironment(listeners, applicationArguments);
        //判断一些环境的值，并设置一些环境的值
        configureIgnoreBeanInfo(environment);
        //打印banner
        Banner printedBanner = printBanner(environment);
        //创建上下文，根据项目类型创建上下文
        context = createApplicationContext();
        //加载文件META-INF/spring.factories中配置的org.springframework.boot.SpringBootExceptionReporter异常报告事件监听实现类
        exceptionReporters = getSpringFactoriesInstances(SpringBootExceptionReporter.class,
                                                         new Class[] { ConfigurableApplicationContext.class }, context);
        //准备上下文，执行完成后调用contextPrepared()方法,contextLoaded()方法
        prepareContext(context, environment, listeners, applicationArguments, printedBanner);
        //加载bean，启动内置web容器
        refreshContext(context);
        afterRefresh(context, applicationArguments);
        stopWatch.stop();
        if (this.logStartupInfo) {
            new StartupInfoLogger(this.mainApplicationClass).logStarted(getApplicationLog(), stopWatch);
        }
        //执行ApplicationRunListeners中的started()方法
        listeners.started(context);
        //执行Runner,ApplicationRunner和CommandLineRunner
        callRunners(context, applicationArguments);
    }
    catch (Throwable ex) {
        handleRunFailure(context, ex, exceptionReporters, listeners);
        throw new IllegalStateException(ex);
    }

    try {
        listeners.running(context);
    }
    catch (Throwable ex) {
        handleRunFailure(context, ex, exceptionReporters, null);
        throw new IllegalStateException(ex);
    }
    return context;
}
```

## 3.1 configureHeadlessProperty

```java
private void configureHeadlessProperty() {
    System.setProperty(SYSTEM_PROPERTY_JAVA_AWT_HEADLESS,
                       System.getProperty(SYSTEM_PROPERTY_JAVA_AWT_HEADLESS, Boolean.toString(this.headless)));
}
```

Headless模式是系统的一种配置模式。在该模式下，系统缺少了显示设备、键盘或鼠标。

Headless模式虽然不是我们愿意见到的，但事实上我们却常常需要在该模式下工作，尤其是服务器端程序开发者。因为服务器（如提供Web服务的主机）往往可能缺少前述设备，但又需要使用他们提供的功能，生成相应的数据，以提供给客户端（如浏览器所在的配有相关的显示设备、键盘和鼠标的主机）。

一般是在程序开始激活headless模式，告诉程序，现在你要工作在Headless mode下，就不要指望硬件帮忙了，你得自力更生，依靠系统的计算能力模拟出这些特性来

## 3.2 spring.factories：Run Listeners

位置：`org/springframework/boot/spring-boot/2.2.5.RELEASE/spring-boot-2.2.5.RELEASE.jar!/META-INF/spring.factories`

```properties
# Run Listeners
org.springframework.boot.SpringApplicationRunListener=\
org.springframework.boot.context.event.EventPublishingRunListener
```

- `org.springframework.boot.context.event.EventPublishingRunListener`：to publish  SpringApplicationEvent
  - 内部有一个容器，用来存储Listeners

## 3.3 prepareEnvironment

查找并设置配置文件信息

```java
private ConfigurableEnvironment prepareEnvironment(SpringApplicationRunListeners listeners,
                                                   ApplicationArguments applicationArguments) {
    // 根据应用类型，创建应用环境：如得到系统的参数、JVM及Servlet等参数，等
    // Create and configure the environment
    ConfigurableEnvironment environment = getOrCreateEnvironment();
    //将 defaultProperties、commandLine及active-prifiles 属性加载到环境中
    //commandLine 在 args 中配置
    //其它参数可在如下4个路径中配置：servletConfigInitParams、servletContextInitParams、systemProperties、systemEnvironment
    configureEnvironment(environment, applicationArguments.getSourceArgs());
    // 将ConfigurationPropertySource放入environment的propertysource中的第一个
    ConfigurationPropertySources.attach(environment);
    //发布ConfigurableEnvironment准备完毕事件
    listeners.environmentPrepared(environment);
    //绑定ConfigurableEnvironment到当前的SpringApplication实例中
    bindToSpringApplication(environment);
    // 非SpringMVC项目的处理，暂时不研究
    if (!this.isCustomEnvironment) {
        environment = new EnvironmentConverter(getClassLoader()).convertEnvironmentIfNecessary(environment,
                                                                                               deduceEnvironmentClass());
    }
    ConfigurationPropertySources.attach(environment);
    return environment;
}
```

### 3.3.1 getOrCreateEnvironment

根据应用类型创建不同类型的环境

```java
private ConfigurableEnvironment getOrCreateEnvironment() {
    if (this.environment != null) {
        return this.environment;
    }
    switch (this.webApplicationType) {
        case SERVLET:
            return new StandardServletEnvironment();
        case REACTIVE:
            return new StandardReactiveWebEnvironment();
        default:
            return new StandardEnvironment();
    }
}
```

### 3.3.2 configureEnvironment

```java
protected void configureEnvironment(ConfigurableEnvironment environment, String[] args) {
    // 是否配置类型转换接口
    if (this.addConversionService) {
        ConversionService conversionService = ApplicationConversionService.getSharedInstance();
        environment.setConversionService((ConfigurableConversionService) conversionService);
    }
    // Add, remove or re-order any PropertySources in this application environment.
    configurePropertySources(environment, args);
    // Configure which profiles are active (or active by default) for this application environment.
    configureProfiles(environment, args);
}
```

### 3.3.3 ConfigurationPropertySources.attach(environment)

```java
public static void attach(Environment environment) {
    Assert.isInstanceOf(ConfigurableEnvironment.class, environment);
    MutablePropertySources sources = ((ConfigurableEnvironment) environment).getPropertySources();
    PropertySource<?> attached = sources.get(ATTACHED_PROPERTY_SOURCE_NAME);
    if (attached != null && attached.getSource() != sources) {
        sources.remove(ATTACHED_PROPERTY_SOURCE_NAME);
        attached = null;
    }
    if (attached == null) {
        sources.addFirst(new ConfigurationPropertySourcesPropertySource(ATTACHED_PROPERTY_SOURCE_NAME,
                                                                        new SpringConfigurationPropertySources(sources)));
    }
}
```

## 3.4 createApplicationContext()

根据应用类型，创建ConfigurableApplicationContext

```java
protected ConfigurableApplicationContext createApplicationContext() {
    Class<?> contextClass = this.applicationContextClass;
    if (contextClass == null) {
        try {
            switch (this.webApplicationType) {
                case SERVLET:
                    contextClass = Class.forName(DEFAULT_SERVLET_WEB_CONTEXT_CLASS);
                    break;
                case REACTIVE:
                    contextClass = Class.forName(DEFAULT_REACTIVE_WEB_CONTEXT_CLASS);
                    break;
                default:
                    contextClass = Class.forName(DEFAULT_CONTEXT_CLASS);
            }
        }
        catch (ClassNotFoundException ex) {
            throw new IllegalStateException(
                "Unable create a default ApplicationContext, please specify an ApplicationContextClass", ex);
        }
    }
    return (ConfigurableApplicationContext) BeanUtils.instantiateClass(contextClass);
}
```

## 3.5 prepareContext

```java
private void prepareContext(ConfigurableApplicationContext context, ConfigurableEnvironment environment,
                            SpringApplicationRunListeners listeners, ApplicationArguments applicationArguments, Banner printedBanner) {
    // 把environment注入到ApplicationContext实例中
    context.setEnvironment(environment);
    // Apply any relevant post processing the {@link ApplicationContext}.
    postProcessApplicationContext(context);
    // Apply any {@link ApplicationContextInitializer}s to the context before it is refreshed.
    applyInitializers(context);
    // listeners处理context
    listeners.contextPrepared(context);
    // 打印启动日志
    if (this.logStartupInfo) {
        logStartupInfo(context.getParent() == null);
        logStartupProfileInfo(context);
    }
    // Add boot specific singleton beans
    ConfigurableListableBeanFactory beanFactory = context.getBeanFactory();
    beanFactory.registerSingleton("springApplicationArguments", applicationArguments);
    if (printedBanner != null) {
        beanFactory.registerSingleton("springBootBanner", printedBanner);
    }
    if (beanFactory instanceof DefaultListableBeanFactory) {
        ((DefaultListableBeanFactory) beanFactory)
        .setAllowBeanDefinitionOverriding(this.allowBeanDefinitionOverriding);
    }
    if (this.lazyInitialization) {
        context.addBeanFactoryPostProcessor(new LazyInitializationBeanFactoryPostProcessor());
    }
    // Load the sources
    Set<Object> sources = getAllSources();
    Assert.notEmpty(sources, "Sources must not be empty");
    // Load beans into the application context.
    load(context, sources.toArray(new Object[0]));
    listeners.contextLoaded(context);
}
```

### 3.5.1 load

```java
/**
 * Load beans into the application context.
 * @param context the context to load beans into
 * @param sources the sources to load
 */
protected void load(ApplicationContext context, Object[] sources) {
    if (logger.isDebugEnabled()) {
        logger.debug("Loading source " + StringUtils.arrayToCommaDelimitedString(sources));
    }
    BeanDefinitionLoader loader = createBeanDefinitionLoader(getBeanDefinitionRegistry(context), sources);
    if (this.beanNameGenerator != null) {
        loader.setBeanNameGenerator(this.beanNameGenerator);
    }
    if (this.resourceLoader != null) {
        loader.setResourceLoader(this.resourceLoader);
    }
    if (this.environment != null) {
        loader.setEnvironment(this.environment);
    }
    loader.load();
}
```



```java
/**
 * Get the bean definition registry.
 * @param context the application context
 * @return the BeanDefinitionRegistry if it can be determined
 */
private BeanDefinitionRegistry getBeanDefinitionRegistry(ApplicationContext context) {
    if (context instanceof BeanDefinitionRegistry) {
        return (BeanDefinitionRegistry) context;
    }
    if (context instanceof AbstractApplicationContext) {
        return (BeanDefinitionRegistry) ((AbstractApplicationContext) context).getBeanFactory();
    }
    throw new IllegalStateException("Could not locate BeanDefinitionRegistry");
}
```



createBeanDefinitionLoader:

```java
/**
 * Factory method used to create the {@link BeanDefinitionLoader}.
 * @param registry the bean definition registry
 * @param sources the sources to load
 * @return the {@link BeanDefinitionLoader} that will be used to load beans
 */
protected BeanDefinitionLoader createBeanDefinitionLoader(BeanDefinitionRegistry registry, Object[] sources) {
    return new BeanDefinitionLoader(registry, sources);
}
```



```java
/**
 * Create a new {@link BeanDefinitionLoader} that will load beans into the specified
 * {@link BeanDefinitionRegistry}.
 * @param registry the bean definition registry that will contain the loaded beans
 * @param sources the bean sources
 */
BeanDefinitionLoader(BeanDefinitionRegistry registry, Object... sources) {
    Assert.notNull(registry, "Registry must not be null");
    Assert.notEmpty(sources, "Sources must not be empty");
    this.sources = sources;
    // 注解
    this.annotatedReader = new AnnotatedBeanDefinitionReader(registry);
    //xml
    this.xmlReader = new XmlBeanDefinitionReader(registry);
    // groovy
    if (isGroovyPresent()) {
        this.groovyReader = new GroovyBeanDefinitionReader(registry);
    }
    // scanner
    this.scanner = new ClassPathBeanDefinitionScanner(registry);
    this.scanner.addExcludeFilter(new ClassExcludeFilter(sources));
}
```



```java
/**
 * Load the sources into the reader.
 * @return the number of loaded beans
 */
int load() {
    int count = 0;
    for (Object source : this.sources) {
        count += load(source);
    }
    return count;
}

private int load(Object source) {
    Assert.notNull(source, "Source must not be null");
    if (source instanceof Class<?>) {
        return load((Class<?>) source);
    }
    if (source instanceof Resource) {
        return load((Resource) source);
    }
    if (source instanceof Package) {
        return load((Package) source);
    }
    if (source instanceof CharSequence) {
        return load((CharSequence) source);
    }
    throw new IllegalArgumentException("Invalid source type " + source.getClass());
}

private int load(Class<?> source) {
    if (isGroovyPresent() && GroovyBeanDefinitionSource.class.isAssignableFrom(source)) {
        // Any GroovyLoaders added in beans{} DSL can contribute beans here
        GroovyBeanDefinitionSource loader = BeanUtils.instantiateClass(source, GroovyBeanDefinitionSource.class);
        load(loader);
    }
    if (isComponent(source)) {
        this.annotatedReader.register(source);
        return 1;
    }
    return 0;
}
```



## 3.6 refreshContext

加载bean，启动内置web容器：

```java
private void refreshContext(ConfigurableApplicationContext context) {
    refresh(context);
    if (this.registerShutdownHook) {
        try {
            context.registerShutdownHook();
        }
        catch (AccessControlException ex) {
            // Not allowed in some environments.
        }
    }
}
```

```java
protected void refresh(ApplicationContext applicationContext) {
    Assert.isInstanceOf(AbstractApplicationContext.class, applicationContext);
    ((AbstractApplicationContext) applicationContext).refresh();
}
```

`org.springframework.context.support.AbstractApplicationContext`的refresh()方法：

```java
@Override
public void refresh() throws BeansException, IllegalStateException {
    synchronized (this.startupShutdownMonitor) {
        // Prepare this context for refreshing.
        // 初始化PropertySource，验证Enrivonment中必要的属性
        prepareRefresh();

        // Tell the subclass to refresh the internal bean factory.
        // 使用模板方法模式调用org.springframework.context.support.AbstractApplicationContext子类refreshBeanFactory()做beanFactory的初始化工作，这个初始化工作在其他初始化工作之前
        ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();

        // Prepare the bean factory for use in this context.
        prepareBeanFactory(beanFactory);

        try {
            // Allows post-processing of the bean factory in context subclasses.
            // 允许在上下文的子类中对bean factory进行后处理
            postProcessBeanFactory(beanFactory);

            // Invoke factory processors registered as beans in the context.
            // 执行容器中的BeanFactoryPostProcessor
            invokeBeanFactoryPostProcessors(beanFactory);

            // Register bean processors that intercept bean creation.
            registerBeanPostProcessors(beanFactory);

            // Initialize message source for this context.
            initMessageSource();

            // Initialize event multicaster for this context.
            initApplicationEventMulticaster();

            // 实现类中启动了Web容器
            // Initialize other special beans in specific context subclasses.
            onRefresh();

            // Check for listener beans and register them.
            registerListeners();

            // Instantiate all remaining (non-lazy-init) singletons.
            finishBeanFactoryInitialization(beanFactory);

            // Last step: publish corresponding event.
            finishRefresh();
        }

        catch (BeansException ex) {
            if (logger.isWarnEnabled()) {
                logger.warn("Exception encountered during context initialization - " +
                            "cancelling refresh attempt: " + ex);
            }

            // Destroy already created singletons to avoid dangling resources.
            destroyBeans();

            // Reset 'active' flag.
            cancelRefresh(ex);

            // Propagate exception to caller.
            throw ex;
        }

        finally {
            // Reset common introspection caches in Spring's core, since we
            // might not ever need metadata for singleton beans anymore...
            resetCommonCaches();
        }
    }
}
```

```java
/**
	 * Prepare this context for refreshing, setting its startup date and
	 * active flag as well as performing any initialization of property sources.
	 */
protected void prepareRefresh() {
    // Switch to active.
    this.startupDate = System.currentTimeMillis();
    this.closed.set(false);
    this.active.set(true);

    if (logger.isDebugEnabled()) {
        if (logger.isTraceEnabled()) {
            logger.trace("Refreshing " + this);
        }
        else {
            logger.debug("Refreshing " + getDisplayName());
        }
    }

    // Initialize any placeholder property sources in the context environment.
    //初始化PropertySources
    initPropertySources();

    // Validate that all properties marked as required are resolvable:
    // see ConfigurablePropertyResolver#setRequiredProperties
    // 验证Environment中必要的属性
    getEnvironment().validateRequiredProperties();

    // Store pre-refresh ApplicationListeners...
    if (this.earlyApplicationListeners == null) {
        this.earlyApplicationListeners = new LinkedHashSet<>(this.applicationListeners);
    }
    else {
        // Reset local application listeners to pre-refresh state.
        this.applicationListeners.clear();
        this.applicationListeners.addAll(this.earlyApplicationListeners);
    }

    // Allow for the collection of early ApplicationEvents,
    // to be published once the multicaster is available...
    this.earlyApplicationEvents = new LinkedHashSet<>();
}
```

```java
/**
	 * Configure the factory's standard context characteristics,
	 * such as the context's ClassLoader and post-processors.
	 * @param beanFactory the BeanFactory to configure
	 */
protected void prepareBeanFactory(ConfigurableListableBeanFactory beanFactory) {
    // Tell the internal bean factory to use the context's class loader etc.
    //设置类加载器：存在则直接设置/不存在则新建一个默认类加载器
    beanFactory.setBeanClassLoader(getClassLoader());
    //设置EL表达式解析器（Bean初始化完成后填充属性时会用到）
    beanFactory.setBeanExpressionResolver(new StandardBeanExpressionResolver(beanFactory.getBeanClassLoader()));
    //设置属性注册解析器PropertyEditor
    beanFactory.addPropertyEditorRegistrar(new ResourceEditorRegistrar(this, getEnvironment()));

    // Configure the bean factory with context callbacks.
    // 将当前的ApplicationContext对象交给ApplicationContextAwareProcessor类来处理，从而在Aware接口实现类中的注入applicationContext
    beanFactory.addBeanPostProcessor(new ApplicationContextAwareProcessor(this));
    //设置忽略自动装配的接口
    beanFactory.ignoreDependencyInterface(EnvironmentAware.class);
    beanFactory.ignoreDependencyInterface(EmbeddedValueResolverAware.class);
    beanFactory.ignoreDependencyInterface(ResourceLoaderAware.class);
    beanFactory.ignoreDependencyInterface(ApplicationEventPublisherAware.class);
    beanFactory.ignoreDependencyInterface(MessageSourceAware.class);
    beanFactory.ignoreDependencyInterface(ApplicationContextAware.class);

    // BeanFactory interface not registered as resolvable type in a plain factory.
    // MessageSource registered (and found for autowiring) as a bean.
    //注册可以解析的自动装配
    beanFactory.registerResolvableDependency(BeanFactory.class, beanFactory);
    beanFactory.registerResolvableDependency(ResourceLoader.class, this);
    beanFactory.registerResolvableDependency(ApplicationEventPublisher.class, this);
    beanFactory.registerResolvableDependency(ApplicationContext.class, this);

    // Register early post-processor for detecting inner beans as ApplicationListeners.
    beanFactory.addBeanPostProcessor(new ApplicationListenerDetector(this));

    // Detect a LoadTimeWeaver and prepare for weaving, if found.
    //如果当前BeanFactory包含loadTimeWeaver Bean，说明存在类加载期织入AspectJ，则把当前BeanFactory交给类加载期BeanPostProcessor实现类LoadTimeWeaverAwareProcessor来处理，从而实现类加载期织入AspectJ的目的。
    if (beanFactory.containsBean(LOAD_TIME_WEAVER_BEAN_NAME)) {
        beanFactory.addBeanPostProcessor(new LoadTimeWeaverAwareProcessor(beanFactory));
        // Set a temporary ClassLoader for type matching.
        beanFactory.setTempClassLoader(new ContextTypeMatchClassLoader(beanFactory.getBeanClassLoader()));
    }

    // Register default environment beans.
    //注册当前容器环境environment组件Bean
    if (!beanFactory.containsLocalBean(ENVIRONMENT_BEAN_NAME)) {
        beanFactory.registerSingleton(ENVIRONMENT_BEAN_NAME, getEnvironment());
    }
    //注册系统配置systemProperties组件Bean
    if (!beanFactory.containsLocalBean(SYSTEM_PROPERTIES_BEAN_NAME)) {
        beanFactory.registerSingleton(SYSTEM_PROPERTIES_BEAN_NAME, getEnvironment().getSystemProperties());
    }
    //注册系统环境systemEnvironment组件Bean
    if (!beanFactory.containsLocalBean(SYSTEM_ENVIRONMENT_BEAN_NAME)) {
        beanFactory.registerSingleton(SYSTEM_ENVIRONMENT_BEAN_NAME, getEnvironment().getSystemEnvironment());
    }
}
```

# 2 `@SpringBootApplication`注解都做了什么事？

## 2.1 `@SpringBootApplication`注解的声明

```java
package org.springframework.boot.autoconfigure;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Inherited;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import org.springframework.beans.factory.support.BeanNameGenerator;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.context.TypeExcludeFilter;
import org.springframework.context.annotation.AnnotationBeanNameGenerator;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.ComponentScan.Filter;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.FilterType;
import org.springframework.core.annotation.AliasFor;
import org.springframework.data.repository.Repository;

@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = { @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
		@Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {
	//此处省略N行代码
}
```

注解说明：

- `@ComponentScan`
    - spring里有四大注解：`@Service`，`@Repository`，`@Component`，`@Controller`用来定义一个bean。
    - `@ComponentScan`注解就是用来自动扫描被这些注解标识的类，最终生成ioc容器里的bean。
    - 可以通过设置`@ComponentScan`的basePackages，includeFilters，excludeFilters属性来动态确定自动扫描范围，类型已经不扫描的类型．默认情况下:它扫描所有类型，并且扫描范围是`@ComponentScan`注解所在配置类包及子包的类。
- `@SpringBootConfiguration`
    - 这个注解的作用与`@Configuration`作用相同，都是用来声明当前类是一个配置类。
    - 在配置类里可以通过`＠Bean`注解生成IOC容器管理的bean。
- `@EnableAutoConfiguration`：参见[`@EnableAutoConfiguration`](# 2.2 `@EnableAutoConfiguration`)

## 2.2 `@EnableAutoConfiguration`

`@EnableAutoConfiguration`是springboot实现自动化配置的核心注解，通过这个注解把spring应用所需的bean注入容器中。

`@EnableAutoConfiguration`源码通过`@Import`注入了一个ImportSelector的实现类
AutoConfigurationImportSelector，这个ImportSelector最终实现根据我们的配置，动态加载所需的bean。

参见[Spring Boot中的自动装载](./docs/programming/java/spring/spring_boot/Automatic_loading_mechanism_in_Spring_Boot.md)

```java
package org.springframework.boot.autoconfigure;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Inherited;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

import org.springframework.boot.autoconfigure.condition.ConditionalOnBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory;
import org.springframework.boot.web.servlet.server.ServletWebServerFactory;
import org.springframework.context.annotation.Conditional;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.core.io.support.SpringFactoriesLoader;

/**
 * Enable auto-configuration of the Spring Application Context, attempting to guess and
 * configure beans that you are likely to need. Auto-configuration classes are usually
 * applied based on your classpath and what beans you have defined. For example, if you
 * have {@code tomcat-embedded.jar} on your classpath you are likely to want a
 * {@link TomcatServletWebServerFactory} (unless you have defined your own
 * {@link ServletWebServerFactory} bean).
 * <p>
 * When using {@link SpringBootApplication @SpringBootApplication}, the auto-configuration
 * of the context is automatically enabled and adding this annotation has therefore no
 * additional effect.
 * <p>
 * Auto-configuration tries to be as intelligent as possible and will back-away as you
 * define more of your own configuration. You can always manually {@link #exclude()} any
 * configuration that you never want to apply (use {@link #excludeName()} if you don't
 * have access to them). You can also exclude them via the
 * {@code spring.autoconfigure.exclude} property. Auto-configuration is always applied
 * after user-defined beans have been registered.
 * <p>
 * The package of the class that is annotated with {@code @EnableAutoConfiguration},
 * usually via {@code @SpringBootApplication}, has specific significance and is often used
 * as a 'default'. For example, it will be used when scanning for {@code @Entity} classes.
 * It is generally recommended that you place {@code @EnableAutoConfiguration} (if you're
 * not using {@code @SpringBootApplication}) in a root package so that all sub-packages
 * and classes can be searched.
 * <p>
 * Auto-configuration classes are regular Spring {@link Configuration @Configuration}
 * beans. They are located using the {@link SpringFactoriesLoader} mechanism (keyed
 * against this class). Generally auto-configuration beans are
 * {@link Conditional @Conditional} beans (most often using
 * {@link ConditionalOnClass @ConditionalOnClass} and
 * {@link ConditionalOnMissingBean @ConditionalOnMissingBean} annotations).
 *
 * @author Phillip Webb
 * @author Stephane Nicoll
 * @since 1.0.0
 * @see ConditionalOnBean
 * @see ConditionalOnMissingBean
 * @see ConditionalOnClass
 * @see AutoConfigureAfter
 * @see SpringBootApplication
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage
@Import(AutoConfigurationImportSelector.class)
public @interface EnableAutoConfiguration {

	String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";

	/**
	 * Exclude specific auto-configuration classes such that they will never be applied.
	 * @return the classes to exclude
	 */
	Class<?>[] exclude() default {};

	/**
	 * Exclude specific auto-configuration class names such that they will never be
	 * applied.
	 * @return the class names to exclude
	 * @since 1.3.0
	 */
	String[] excludeName() default {};

}
```

