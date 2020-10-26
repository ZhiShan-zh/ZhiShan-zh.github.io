# Spring整合Redis

# 1 java使用redis
## 1.1 需要的包
### 1.1.1 普通工程
需要把jedis依赖的jar包添加到工程中。比如：`jedis-2.7.2.jar`

### 1.1.2 Maven工程
Maven工程中需要把jedis的坐标添加到依赖。

```xml
<!-- Redis客户端 -->
<dependency>
	<groupId>redis.clients</groupId>
	<artifactId>jedis</artifactId>
	<version>2.7.2</version>
</dependency>
```

## 1.2 代码中操作redis单机版
第一步：创建一个Jedis对象。需要指定服务端的ip及端口。
第二步：使用Jedis对象操作数据库，每个redis命令对应一个方法。
第三步：打印结果。
第四步：关闭Jedis

```java
@Test
public void testJedis() throws Exception {
	// 第一步：创建一个Jedis对象。需要指定服务端的ip及端口。
	Jedis jedis = new Jedis("192.168.25.10", 6379);
	// 第二步：使用Jedis对象操作数据库，每个redis命令对应一个方法。
	String result = jedis.get("string");
	// 第三步：打印结果。
	System.out.println(result);
	// 第四步：关闭Jedis
	jedis.close();
}
```

## 1.3 使用连接池操作单机版redis
第一步：创建一个JedisPool对象。需要指定服务端的ip及端口。
第二步：从JedisPool中获得Jedis对象。
第三步：使用Jedis操作redis服务器。
第四步：操作完毕后关闭jedis对象，连接池回收资源。
第五步：关闭JedisPool对象。

```java
@Test
public void testJedisPool() throws Exception {
	// 第一步：创建一个JedisPool对象。需要指定服务端的ip及端口。
	JedisPool jedisPool = new JedisPool("192.168.25.10", 6379);
	// 第二步：从JedisPool中获得Jedis对象。
	Jedis jedis = jedisPool.getResource();
	// 第三步：使用Jedis操作redis服务器。
	jedis.set("jedis", "test");
	String result = jedis.get("jedis");
	System.out.println(result);
	// 第四步：操作完毕后关闭jedis对象，连接池回收资源。
	jedis.close();
	// 第五步：关闭JedisPool对象。
	jedisPool.close();
}
```

## 1.4 连接集群版redis
第一步：使用JedisCluster对象。需要一个`Set<HostAndPort>`参数。Redis节点的列表。
第二步：直接使用JedisCluster对象操作redis。在系统中单例存在。
第三步：打印结果
第四步：系统关闭前，关闭JedisCluster对象。

```java
@Test
public void testJedisCluster() throws Exception {
	// 第一步：使用JedisCluster对象。需要一个Set<HostAndPort>参数。Redis节点的列表。
	Set<HostAndPort> nodes = new HashSet<>();
	nodes.add(new HostAndPort("192.168.25.10", 7001));
	nodes.add(new HostAndPort("192.168.25.10", 7002));
	nodes.add(new HostAndPort("192.168.25.10", 7003));
	nodes.add(new HostAndPort("192.168.25.10", 7004));
	nodes.add(new HostAndPort("192.168.25.10", 7005));
	nodes.add(new HostAndPort("192.168.25.10", 7006));
	JedisCluster jedisCluster = new JedisCluster(nodes);
	// 第二步：直接使用JedisCluster对象操作redis。在系统中单例存在。
	jedisCluster.set("hello", "100");
	String result = jedisCluster.get("hello");
	// 第三步：打印结果
	System.out.println(result);
	// 第四步：系统关闭前，关闭JedisCluster对象。
	jedisCluster.close();
}
```

# 2 封装redis操作接口并与spring整合
常用的操作redis的方法提取出一个接口，分别对应单机版和集群版创建两个实现类。
**策略模式**：一个接口，一个实现类
实现单击版和集群版无缝变换。
## 2.1 接口定义

```java
public interface JedisClient {

	String set(String key, String value);
	String get(String key);
	Boolean exists(String key);
	Long expire(String key, int seconds);
	Long ttl(String key);
	Long incr(String key);
	Long hset(String key, String field, String value);
	String hget(String key, String field);
	Long hdel(String key, String... field);
	Boolean hexists(String key, String field);
	List<String> hvals(String key);
	Long del(String key);
}
```

## 2.2 单机版实现
### 2.2.1 实现类
```java
public class JedisClientPool implements JedisClient {
	
	private JedisPool jedisPool;

	public JedisPool getJedisPool() {
		return jedisPool;
	}

	public void setJedisPool(JedisPool jedisPool) {
		this.jedisPool = jedisPool;
	}

	@Override
	public String set(String key, String value) {
		Jedis jedis = jedisPool.getResource();
		String result = jedis.set(key, value);
		jedis.close();
		return result;
	}

	@Override
	public String get(String key) {
		Jedis jedis = jedisPool.getResource();
		String result = jedis.get(key);
		jedis.close();
		return result;
	}

	@Override
	public Boolean exists(String key) {
		Jedis jedis = jedisPool.getResource();
		Boolean result = jedis.exists(key);
		jedis.close();
		return result;
	}

	@Override
	public Long expire(String key, int seconds) {
		Jedis jedis = jedisPool.getResource();
		Long result = jedis.expire(key, seconds);
		jedis.close();
		return result;
	}

	@Override
	public Long ttl(String key) {
		Jedis jedis = jedisPool.getResource();
		Long result = jedis.ttl(key);
		jedis.close();
		return result;
	}

	@Override
	public Long incr(String key) {
		Jedis jedis = jedisPool.getResource();
		Long result = jedis.incr(key);
		jedis.close();
		return result;
	}

	@Override
	public Long hset(String key, String field, String value) {
		Jedis jedis = jedisPool.getResource();
		Long result = jedis.hset(key, field, value);
		jedis.close();
		return result;
	}

	@Override
	public String hget(String key, String field) {
		Jedis jedis = jedisPool.getResource();
		String result = jedis.hget(key, field);
		jedis.close();
		return result;
	}

	@Override
	public Long hdel(String key, String... field) {
		Jedis jedis = jedisPool.getResource();
		Long result = jedis.hdel(key, field);
		jedis.close();
		return result;
	}

	@Override
	public Boolean hexists(String key, String field) {
		Jedis jedis = jedisPool.getResource();
		Boolean result = jedis.hexists(key, field);
		jedis.close();
		return result;
	}

	@Override
	public List<String> hvals(String key) {
		Jedis jedis = jedisPool.getResource();
		List<String> result = jedis.hvals(key);
		jedis.close();
		return result;
	}

	@Override
	public Long del(String key) {
		Jedis jedis = jedisPool.getResource();
		Long result = jedis.del(key);
		jedis.close();
		return result;
	}
}
```

### 2.2.2 整合spring
applicationContext-redis.xml内容：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:context="http://www.springframework.org/schema/context" xmlns:p="http://www.springframework.org/schema/p"
	xmlns:aop="http://www.springframework.org/schema/aop" xmlns:tx="http://www.springframework.org/schema/tx"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans4.2.xsd
	http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context4.2.xsd
	http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop4.2.xsd http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx4.2.xsd
	http://www.springframework.org/schema/util http://www.springframework.org/schema/util/spring-util4.2.xsd">

	<!-- 配置单机版的连接 -->
	<bean id="jedisPool" class="redis.clients.jedis.JedisPool">
		<constructor-arg name="host" value="192.168.25.10"></constructor-arg>
		<constructor-arg name="port" value="6379"></constructor-arg>
	</bean>
	<bean id="jedisClientPool" class="com.zh.jedis.JedisClientPool"/>
	
</beans>
```

## 2.3 集群版实现
### 2.3.1 实现类

```java
public class JedisClientCluster implements JedisClient {
	
	private JedisCluster jedisCluster;
	
	public JedisCluster getJedisCluster() {
		return jedisCluster;
	}

	public void setJedisCluster(JedisCluster jedisCluster) {
		this.jedisCluster = jedisCluster;
	}

	@Override
	public String set(String key, String value) {
		return jedisCluster.set(key, value);
	}

	@Override
	public String get(String key) {
		return jedisCluster.get(key);
	}

	@Override
	public Boolean exists(String key) {
		return jedisCluster.exists(key);
	}

	@Override
	public Long expire(String key, int seconds) {
		return jedisCluster.expire(key, seconds);
	}

	@Override
	public Long ttl(String key) {
		return jedisCluster.ttl(key);
	}

	@Override
	public Long incr(String key) {
		return jedisCluster.incr(key);
	}

	@Override
	public Long hset(String key, String field, String value) {
		return jedisCluster.hset(key, field, value);
	}

	@Override
	public String hget(String key, String field) {
		return jedisCluster.hget(key, field);
	}

	@Override
	public Long hdel(String key, String... field) {
		return jedisCluster.hdel(key, field);
	}

	@Override
	public Boolean hexists(String key, String field) {
		return jedisCluster.hexists(key, field);
	}

	@Override
	public List<String> hvals(String key) {
		return jedisCluster.hvals(key);
	}

	@Override
	public Long del(String key) {
		return jedisCluster.del(key);
	}
}
```

### 2.3.2 整合spring
**注意**：单机版和集群版不能共存，使用单机版时注释集群版的配置。使用集群版，把单机版注释。
applicationContext-redis.xml内容：

```xml
<!-- 集群版的配置 -->
	<bean id="jedisCluster" class="redis.clients.jedis.JedisCluster">
		<constructor-arg>
			<set>
				<bean class="redis.clients.jedis.HostAndPort">
					<constructor-arg name="host" value="192.168.25.10"></constructor-arg>
					<constructor-arg name="port" value="7001"></constructor-arg>
				</bean>
				<bean class="redis.clients.jedis.HostAndPort">
					<constructor-arg name="host" value="192.168.25.10"></constructor-arg>
					<constructor-arg name="port" value="7002"></constructor-arg>
				</bean>
				<bean class="redis.clients.jedis.HostAndPort">
					<constructor-arg name="host" value="192.168.25.10"></constructor-arg>
					<constructor-arg name="port" value="7003"></constructor-arg>
				</bean>
				<bean class="redis.clients.jedis.HostAndPort">
					<constructor-arg name="host" value="192.168.25.10"></constructor-arg>
					<constructor-arg name="port" value="7004"></constructor-arg>
				</bean>
				<bean class="redis.clients.jedis.HostAndPort">
					<constructor-arg name="host" value="192.168.25.10"></constructor-arg>
					<constructor-arg name="port" value="7005"></constructor-arg>
				</bean>
				<bean class="redis.clients.jedis.HostAndPort">
					<constructor-arg name="host" value="192.168.25.10"></constructor-arg>
					<constructor-arg name="port" value="7006"></constructor-arg>
				</bean>
			</set>
		</constructor-arg>
	</bean>
	<bean id="jedisClientCluster" class="com.zh.jedis.JedisClientCluster"/>
```

