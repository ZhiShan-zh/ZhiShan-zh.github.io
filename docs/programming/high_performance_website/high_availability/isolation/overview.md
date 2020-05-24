# 隔离概述

# 1 简介

隔离是指将系统或资源分割开，系统隔离是为了在系统发生故障时，能限定传播范围和影响范围，即发生故障后不会出现滚雪球效应，从而保证只有出问题的服务不可用，其他服务还是可用的。资源隔离通过隔离来减少资源竞争，保障服务键的相互不影响和可用性。

# 2 隔离类型

## 2.1 线程隔离

线程隔离主要是指线程池隔离，在实际使用时，我们会请求分类，然后交给不同的线程池处理。当一种业务的请求处理发生问题时，不会将故障扩散到其他线程池，从而保障其他服务可用。

![image-20200521200032494](https://zhishan-zh.github.io/media/isolation_20200521200016.png)

我们会根据服务等级划分两个线程池，一下是池的抽象。

```xml
<bean id="zeroLevelAsyncContext" class="com.jd.noah.base.web.DynamicAsyncContext" destroy-method="stop">
	<property name="asyncTimeoutInSeconds" value="${zero.level.request.async.timeout.seconds}"/>
    <property name="poolSize" value="${zero.level.request.async.pool.size}"/>
    <property name="keepaliveTimeInSeconds" value="${zero.level.request.async.pool.keepalive.seconds}"/>
    <property name="queueCapacity" value="${zero.level.request.async.pool.queue.capacity}"/>
</bean>
<bean id="oneLevelAsyncContext" class="com.jd.noah.base.web.DynamicAsyncContext" destroy-method="stop">
	<property name="asyncTimeoutInSeconds" value="${one.level.request.async.timeout.seconds}"/>
    <property name="poolSize" value="${one.level.request.async.pool.size}"/>
    <property name="keepaliveTimeInSeconds" value="${one.level.request.async.pool.keepalive.seconds}"/>
    <property name="queueCapacity" value="${one.level.request.async.pool.queue.capacity}"/>
</bean>
```

## 2.2 进程隔离

在公司发展初期，一般是先进行从零到一，不会一上来就进行系统拆分，这样就会开发出一些大而全的系统，系统中的一个模块/功能出现问题，整个系统就不可用了。首先，想到的解决方案是通过部署多个实例，通过负载均衡进行路由转发。但是，这种情况无法避免某个模块因BUG而出现如OOM导致整个系统不可用的风险。因此，此种方案只是一个过度，较好的解决方案是通过将系统拆分为多个子系统来实现物理隔离。通过进程隔离使得某一个子系统出现问题时不会影响到其他子系统。

![image-20200522104034809](https://zhishan-zh.github.io/media/isolation_20200522104015.png)

## 2.3 集群隔离

随着系统的发展，单实例服务无法满足需求，此时需要服务化技术，通过部署多个服务形成服务集群，来提升系统容量，如下图所示。

![isolation_20200522105100](https://zhishan-zh.github.io/media/isolation_20200522105100.png)

随着调用方的增多，当秒杀服务被会影响到其他服务的稳定性时，应该考虑为秒杀服务提供单独的服务集群，即为服务分组，这样当某一个分组出现问题时，不会影响到其他分组，从而实现了故障隔离，如下图所示。

![isolation_20200522105813](https://zhishan-zh.github.io/media/isolation_20200522105813.png)

比如，注册生产者时提供分组名。

```xml
<jsf:provider id="myService" interface="com.jd.MyService" alias="${分组名}" ref="myServiceImpl"/>
```

消费时提供相关的分组名即可。

```xml
<jsf:consumer id="myService" interface="com.jd.MyService" alias="${分组名}"/>
```

## 2.4 机房隔离

随着对系统可用性的要求，会进行多机房部署，每个机房的服务都有自己的服务分组，本机房的服务应该只调用本机房服务，不进行跨机房调用。其中，一个机房服务发生问题时，可以通过DNS/负载均衡将请求全部切换到另一个机房，或者考虑服务能自动重试其他机房的服务，从而提升系统可用性。

![isolation_20200522110713](https://zhishan-zh.github.io/media/isolation_20200522110713.png)

一种办法是根据IP（不同机房IP段不一样）自动分组，还有一种较灵活的办法是通过在分组名上加上机房名。

```xml
<jsf:provider id="myService" interface="com.jd.MyService" alias="${机房名}-${分组名}" ref="myServiceImpl"/>
```

```xml
<jsf:consumer id="myService" interface="com.jd.MyService" alias="${机房名}-${分组名}"/>
```

## 2.5 读写隔离

如下图所示，通过主从模式将读和写集群分离，读服务只从Redis集群获取数据，当主Redis集群出现问题时，从Redis集群还是可用的，从而不影响用户访问。而当从Redis集群出现问题时，可以进行其他集群的重试。

![isolation_20200522111829](https://zhishan-zh.github.io/media/isolation_20200522111829.png)

```sql
--先读取从
status, resp = slave_get(key)
if status == STATUS_OK then
	return status, value
end
--如果从获取失败了，从主获取
status, resp = master_get(key)
```

## 2.6 动静隔离

当用户访问如结算页，如果JS/CSS等静态资源也在结算页系统中时，很可能因为访问量太大导致带宽被打满，从而出现不可用。

因此，应该将动态内容和静态内容资源分离，一般应该将静态资源放在CDN上或静态资源服务器上（如FastDFS）。

## 2.7 爬虫隔离

系统因为爬虫访问量太大而导致服务不可用的解决办法：

- 通过限流解决；
- 在负载均衡层面将爬虫路由到单独的集群，从而保障正常流量可用，爬虫流量尽量可用。

### 2.7.1 使用Nginx

![](https://zhishan-zh.github.io/media/isolation_20200522115549.png)

```
set $flag 0;
if($http_user_agent ~* "spider") {
	set $flag "1";
}
if($flag = "0") {
	// 代理到正常集群
}
if($flag = "1") {
	// 代理到爬虫集群
}
```

### 2.7.2 使用OpenResty

实际场景我们使用了OpenResty，不仅对爬虫user-agent过滤，还会过滤一些恶意IP（通过统计IP访问量来配置阀值），将它们分流到固定分组，这种情况会存在一定程度的误杀，因为公司的公网IP一般情况下是同一个，大家使用同一个公网出口IP访问网站，因此，可以考虑IP+Cookie的方式，在用户浏览器中植入表示用户身份的统一Cookie。访问服务前先植入Cookie，访问服务时验证该Cookie，如果没有或者不正确，则可以考虑分流到固定分组，或者提示输入验证码后访问。

## 2.8 热点隔离

秒杀、抢购属于非常合适的热点例子，对于这种热点，是能提前知道的，所以可以将秒杀和抢购做成独立系统或服务进行隔离，从而保证秒杀/抢购流程出现问题时不影响主流程。

还存在一些热点，可能是因为架构或突发时间引起的。对于读热点，可以使用多级缓存来搞定，而写热点一般通过缓存+队列牧师削峰。

## 2.9 资源隔离

最常见存在竞争的资源如磁盘、CPU、网络。

**磁盘**：在”构建需求响应式亿级商品详情页“中，我们使用JIMDB（京东分布式缓存系统）数据同步时要dump数据，SSD盘容量永乐50%以上，dump到同一块磁盘时遇到了容量不足的问题，我们通过单独挂一块SAS盘来专门同步数据。还有，使用Docker容器时，有的容器写磁盘非常频繁，因此，要考虑为不同的容器挂载不同的磁盘。

**CPU**：默认CPU的调度策略在一些追求极致性能的场景下可能并不太适合，我们希望通过绑定CPU到特定进行来提升性能。当一台机器启动很多Redis实例时，将CPU通过taskset绑定到Redis实例上可以提升一些性能。还有，Nginx提供了worker_processes和worker_cpu_affinity来绑定CPU。如系统网络应用比较繁忙，可以考虑将网卡IRQ绑定到指定的CPU来提升系统处理中断的能力，从而提升整体性能。

可以通过cat/proc/interrupts查看中断情况，然后通过proc/irq/N/smp_affinity手动设置中断要绑定的CPU。或者开启irqbalance优化中断分配，将中断均匀地分发给CPU。

**网络**：如大数据计算集群、数据库集群应该和应用集群隔离到不同的机架或机房，实现网络的隔离；因为大数据计算或数据库同步时会占用比较大的网络带宽，可能会拥塞网络导致应用响应变慢。

## 2.10 其他隔离类型

环境隔离：测试环境、预发布环境/灰度环境、正式环境。

压测隔离：真实数据、压测数据隔离

AB测试：为不同的用户提供不同版本的服务。

缓存隔离：有些系统混用缓存，而有些系统会扔大字节值到Redis，造成Redis慢查询。

查询隔离：简单、批量、复杂条件查询分别路由到不同的集群。