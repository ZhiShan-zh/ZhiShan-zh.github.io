# Spring Cache

# 1 概述

自Spring Framework3.1起，提供了类似于`@Transactional`注解事务的注解Cache支持，且提供了Cache抽象工具，在此之前一般通过AOP实现。该Cache抽象工具可以透明的在使用 Spring 的应用中添加缓存机制，不会使应用的实现对具体的缓存方案产生依赖，因此**无需修改应用实现就能够方便的替换缓存方案**。

Spring Cache的核心就是对某个方法进行缓存，其实质就是缓存该方法的返回结果，并把方法参数和结果用键值对的方式存放到缓存中，当再次调用该方法使用相应的参数时，就会直接从缓存里面取出指定的结果进行返回。

## 1.1 使用Spring缓存抽象的好处

- 提供基本的Cache抽象，方便切换各种底层Cache；
- 通过注解Cache可以实现类似于事务一样，缓存逻辑透明的应用到我们的业务代码上，且只需要更少的代码就可以完成；
- 提供事务回滚时也自动回滚缓存；
- 支持比较复杂的缓存逻辑；

## 1.2 Spring缓存抽象主要接口

### 1.2.1 Cache

为缓存的组件规范定义，包含缓存的各种操作集合

```java
package org.springframework.cache;

import java.util.concurrent.Callable;
import org.springframework.lang.Nullable;
// 定义通用缓存操作的接口。
public interface Cache {
    // 返回缓存的名称，默认实现中一般是CacheManager创建Cache的bean时传入cacheName
	String getName();
    // 返回底层提供缓存的程序。
	Object getNativeCache();
    // 根据key得到一个值包装对象ValueWrapper，然后通过get方法返回真实的值
	@Nullable
	ValueWrapper get(Object key);
    // 根据key和值的类型直接获取值
	@Nullable
	<T> T get(Object key, @Nullable Class<T> type);
	// 从缓存中获取key对应的值，如果缓存没有命中，则添加缓存，此时可异步地从 valueLoader中获取对应的值（4.3版本新增）
	@Nullable
	<T> T get(Object key, Callable<T> valueLoader);
	// 缓存数据，如果缓存中已经有对应的key，则替换其value
	void put(Object key, @Nullable Object value);
	// 如果key不再缓存中，则以此key向缓存中存数据
	@Nullable
	ValueWrapper putIfAbsent(Object key, @Nullable Object value);
	// 从缓存中移除key对应的缓存
	void evict(Object key);
	// 清空缓存
	void clear();
	// 值的包装类型
	@FunctionalInterface
	interface ValueWrapper {

		// 获取真实的值
		@Nullable
		Object get();
	}

	// 当get(Object key, Callable<T> valueLoader)抛出异常时，会包装成此异常抛出
	@SuppressWarnings("serial")
	class ValueRetrievalException extends RuntimeException {

		@Nullable
		private final Object key;

		public ValueRetrievalException(@Nullable Object key, Callable<?> loader, Throwable ex) {
			super(String.format("Value for key '%s' could not be loaded using '%s'", key, loader), ex);
			this.key = key;
		}

		@Nullable
		public Object getKey() {
			return this.key;
		}
	}
}
```

#### 1.2.1.1 默认提供的实现

- ConcurrentMapCache：使用`java.util.concurrent.ConcurrentHashMap`实现的Cache；

- GuavaCache：从spring 4开始，对Guava的`com.google.common.cache.Cache`进行的Wrapper，需要Google Guava 12.0或更高版本；

- EhCacheCache：使用Ehcache实现

- JCacheCache：从spring3.2开始，对`javax.cache.Cache`进行的wrapper；spring4将此类更新到JCache 0.11版本；

### 1.2.2 CacheManager

缓存管理器，管理各种缓存（cache）组件

```java
package org.springframework.cache;

import java.util.Collection;
import org.springframework.lang.Nullable;

// Spring的中央缓存管理器SPI。
public interface CacheManager {

	// 根据指定的名称获取cache实例
	@Nullable
	Cache getCache(String name);

	// 返回当前cacheManager已知的所有缓存名称
	Collection<String> getCacheNames();
}
```

#### 1.2.2.1 默认的实现

- ConcurrentMapCacheManager/ConcurrentMapCacheFactoryBean

- GuavaCacheManager；

- EhCacheCacheManager/EhCacheManagerFactoryBean；

- JCacheCacheManager/JCacheManagerFactoryBean；

从Spring3.1开始还提供了`org.springframework.cache.support.CompositeCacheManager`用于组合CacheManager，即可以从多个CacheManager中轮询得到相应的Cache。

注意：

- 除了GuavaCacheManager之外，其他Cache都支持Spring事务的，即如果事务回滚了，Cache的数据也会移除掉。

- Spring不进行Cache的缓存策略的维护，这些都是由底层Cache自己实现，Spring只是提供了一个Wrapper，提供一套对外一致的API。

# 2 Spring Boot中使用缓存的步骤

1. 开始使用前需要导入依赖：

    ```xml
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-cache</artifactId>
    </dependency>
    <!-- 如果使用redis缓存，注释掉spring-boot-starter-cache，打开这个注释
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring‐boot‐starter‐data‐redis</artifactId>
    </dependency>
     -->
    ```

2. 在启动类注解`@EnableCaching`开启缓存

    ```java
    @SpringBootApplication
    @EnableCaching  //开启缓存
    public class DemoApplication{
        public static void main(String[] args) {
            SpringApplication.run(DemoApplication.class, args);
        }
    }
    ```

3. 使用缓存注解：

    - `@Cacheable`：主要针对方法配置，能够根据方法的请求参数对其进行缓存

    - `@CacheEvict`：清空缓存

    - `@CachePut`：保证方法被调用，又希望结果被缓存。与`@Cacheable`区别在于是否每次都调用方法，常用于更新

    - `@CacheConfig`：统一配置本类的缓存注解的属性

    - `@Caching`：组合多个Cache注解使用，如：

        ```java
        @Caching(cacheable = {
                @Cacheable(value = "emp",key = "#p0"),
                //...
        },
        put = {
                @CachePut(value = "emp",key = "#p0"),
                //...
        },evict = {
                @CacheEvict(value = "emp",key = "#p0"),
                //...
        })
        public User save(User user) {
            //...
        }
        ```

# 3 注解`@Cacheable`、`@CacheEvict`、`@CachePut`参数说明

| 名称                                                     | 解释                                                         |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| value                                                    | **解释**：缓存的名称，就是Cache示例的名称，在 spring配置文件中定义，必须指定至少一个。<br/>例如：`@Cacheable(value=“mycache”) `或者`@Cacheable(value={”cache1”,”cache2”}` |
| key                                                      | **解释**：缓存的 key，可以为空，如果指定要按照 SpEL 表达式编写，如果不指定，则缺省按照方法的所有参数进行组合。<br/>例如：`@Cacheable(value=”testcache”,key=”#id”)` |
| condition                                                | **解释**：缓存的条件，可以为空，使用 SpEL 编写。<br/>**值的意义**：可以返回true或者false，只有为 true 才进行缓存/清除缓存。<br/>**执行时机**：在调用方法之前之后都能判断。<br/>例如：`@Cacheable(value=”testcache”,condition=”#userName.length()>2”)` |
| unless<br/>（适用于<br/>`@Cacheable`、<br/>`@CachePut`） | **作用**：否决缓存。<br/>**执行时机**：表达式只在方法执行之后判断。<br/>**值的意义**：当条件结果为TRUE时，就不会缓存。`@Cacheable(value=”testcache”,unless=”#userName.length()>2”)` |
| allEntries<br/>（适用于<br/>`@CacheEvict`）              | **作用**：是否清空所有缓存内容，缺省为 false，<br/>**值的意义**：如果指定为true，则方法调用后将立即清空所有缓存。<br/>例如：`@CachEvict(value=”testcache”,allEntries=true)` |
| beforeInvocation<br/>（适用于<br/>`@CacheEvict`）        | 是否在方法执行前就清空，缺省值为false；<br/>如果指定为true，则在方法执行之前就清空缓存。<br/>缺省情况下，如果方法执行抛出异常，则不会清空缓存。 |

# 4 SpEL上下文数据

| 名称          | 位置       | 描述                                                         | 示例                 |
| ------------- | ---------- | ------------------------------------------------------------ | -------------------- |
| methodName    | root对象   | 当前被调用的方法名                                           | #root.methodname     |
| method        | root对象   | 当前被调用的方法                                             | #root.method.name    |
| target        | root对象   | 当前被调用的目标对象实例                                     | #root.target         |
| targetClass   | root对象   | 当前被调用的目标对象的类                                     | #root.targetClass    |
| args          | root对象   | 当前被调用的方法的参数列表                                   | #root.args[0]        |
| caches        | root对象   | 当前方法调用使用的缓存列表                                   | #root.caches[0].name |
| Argument Name | 执行上下文 | 当前被调用的方法的参数，如`find(User user)`，可以通过`#user.id`获得参数 | #user.id             |
| result        | 执行上下文 | 方法执行后的返回值（仅当方法执行后的判断有效，如 unless cacheEvict的beforeInvocation=false） | #result              |

**注意：**

1、当我们要使用`root`对象的属性作为`key`时我们也可以将“`#root`”省略，因为`Spring`默认使用的就是`root`对象的属性。 如

```
@Cacheable(key = "targetClass + methodName +#p0")
```

2、使用方法参数时我们可以直接使用“#参数名”或者“#p参数index”。 如：

```
@Cacheable(value="users", key="#id")
@Cacheable(value="users", key="#p0")
```

`SpEL`提供了多种运算符

| 类型       | 运算符                                         |
| ---------- | ---------------------------------------------- |
| 关系       | <，>，<=，>=，==，!=，lt，gt，le，ge，eq，ne   |
| 算术       | +，- ，* ，/，%，^                             |
| 逻辑       | &&，\|\|，!，and，or，not，between，instanceof |
| 条件       | ?: (ternary)，?: (elvis)                       |
| 正则表达式 | matches                                        |
| 其他类型   | ?.，?[…]，![…]，^[…]，$[…]                     |

# 5 定制CacheManager

1. 在Spring Boot中可以实现CacheManagerCustomizer接口，在方法`customize(T cacheManager)`中来对CacheManager做一些设置。

```java
package org.springframework.boot.autoconfigure.cache;

import org.springframework.cache.CacheManager;

@FunctionalInterface
public interface CacheManagerCustomizer<T extends CacheManager> {
	// 定制cacheManager
	void customize(T cacheManager);
}
```

2. 在配置类里边把此CacheManagerCustomizer示例返回。

示例：

```java
package com.zh.testcache.redis.config;
 
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.boot.autoconfigure.cache.CacheManagerCustomizer;
import org.springframework.data.redis.cache.RedisCacheManager;
 
public class RedisCacheManagerCustomizer implements CacheManagerCustomizer<RedisCacheManager> {
    @Override
    public void customize(RedisCacheManager cacheManager) {
        // 默认过期时间，单位秒
        cacheManager.setDefaultExpiration(1000);
        cacheManager.setUsePrefix(false);
        Map<String, Long> expires = new ConcurrentHashMap<String, Long>();
        expires.put("userIdCache", 2000L);
        cacheManager.setExpires(expires);
    }
}
```

```java
package com.zh.testcache.redis.config;
 
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RedisCacheConfiguration {
    @Bean
    public RedisCacheManagerCustomizer redisCacheManagerCustomizer() {
        return new RedisCacheManagerCustomizer();
    }
}
```

# 6 问题

## 6.1 RedisCache缓存失效瞬间返回null的问题

RedisCache获取缓存的步骤：

1. 判断缓存中是否有key的缓存。
2. 如果存在key的缓存，在通过key真正地获取缓存数据。

问题复现逻辑：

1. 判断key的缓存是否存在：返回true，存在；
2. 缓存key失效；
3. 通过key获取缓存，发现没有数据，就返回null。

