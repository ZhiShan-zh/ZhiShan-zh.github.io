# Ribbon中的负载均衡规则接口IRule

# 1 概述

Ribbon是客户端负载均衡，它内部提供了一个叫做ILoadBalance的接口负责负载均衡器的操作。`com.netflix.loadbalancer.ILoadBalance`的继承关系如下：

![image-20200519105746340](https://zhishan-zh.github.io/media/image-20200519105746340.png)

Ribbon通过`ILoadBalancer`接口对外提供统一的选择服务器(Server)的功能，此接口会根据不同的负载均衡策略（IRule）选择合适的Server返回给使用者。

```java
package com.netflix.loadbalancer;

/**
 * Interface that defines a "Rule" for a LoadBalancer. A Rule can be thought of
 * as a Strategy for loadbalacing. Well known loadbalancing strategies include
 * Round Robin, Response Time based etc.
 * 
 * @author stonse
 * 
 */
public interface IRule{
    /*
     * choose one alive server from lb.allServers or
     * lb.upServers according to key
     * 
     * @return choosen Server object. NULL is returned if none
     *  server is available 
     */

    public Server choose(Object key);
    
    public void setLoadBalancer(ILoadBalancer lb);
    
    public ILoadBalancer getLoadBalancer();    
}
```

![image-20200519110501462](https://zhishan-zh.github.io/media/image-20200519110501462.png)

# 2 Ribbon负载均衡策略

## 2.1 随机策略RandomRule

```java
/**
 * Randomly choose from all living servers
 * 从存活的服务器中随机选择一个
 */
@edu.umd.cs.findbugs.annotations.SuppressWarnings(value = "RCN_REDUNDANT_NULLCHECK_OF_NULL_VALUE")
public Server choose(ILoadBalancer lb, Object key) {
    if (lb == null) {
        return null;
    }
    Server server = null;

    while (server == null) {
        if (Thread.interrupted()) {
            return null;
        }
        List<Server> upList = lb.getReachableServers();
        List<Server> allList = lb.getAllServers();

        int serverCount = allList.size();
        if (serverCount == 0) {
            /*
             * No servers. End regardless of pass, because subsequent passes
             * only get more restrictive.
             */
            return null;
        }

        int index = chooseRandomInt(serverCount);
        server = upList.get(index);

        if (server == null) {
            /*
             * The only time this should happen is if the server list were
             * somehow trimmed. This is a transient condition. Retry after
             * yielding.
             */
            Thread.yield();
            continue;
        }

        if (server.isAlive()) {
            return (server);
        }

        // Shouldn't actually happen.. but must be transient or a bug.
        server = null;
        Thread.yield();
    }

    return server;

}
```

## 2.2 轮询策略RoundRobinRule

每次都取下一个服务器。

```java
public Server choose(ILoadBalancer lb, Object key) {
    if (lb == null) {
        log.warn("no load balancer");
        return null;
    }

    Server server = null;
    int count = 0;
    while (server == null && count++ < 10) {
        List<Server> reachableServers = lb.getReachableServers();
        List<Server> allServers = lb.getAllServers();
        int upCount = reachableServers.size();
        int serverCount = allServers.size();

        if ((upCount == 0) || (serverCount == 0)) {
            log.warn("No up servers available from load balancer: " + lb);
            return null;
        }
		// 获取下一台服务器的指针
        int nextServerIndex = incrementAndGetModulo(serverCount);
        server = allServers.get(nextServerIndex);

        if (server == null) {
            /* Transient. */
            Thread.yield();
            continue;
        }

        if (server.isAlive() && (server.isReadyToServe())) {
            return (server);
        }

        // Next.
        server = null;
    }

    if (count >= 10) {
        log.warn("No available alive servers after 10 tries from load balancer: "
                + lb);
    }
    return server;
}
```

使用原子类`private AtomicInteger nextServerCyclicCounter;`保存当前服务器的指针，需要下一台的时候使用原子类无锁的方式获取下一台服务器的指针。

```java
/**
 * Inspired by the implementation of {@link AtomicInteger#incrementAndGet()}.
 *
 * @param modulo The modulo to bound the value of the counter.
 * @return The next value.
 */
private int incrementAndGetModulo(int modulo) {
    for (;;) {
        int current = nextServerCyclicCounter.get();
        int next = (current + 1) % modulo;
        if (nextServerCyclicCounter.compareAndSet(current, next))
            return next;
    }
}
```

## 2.3 轮询动态权重WeightedResponseTimeRule

WeightedResponseTimeRule继承了RoundRobinRule，开始的时候还没有权重列表，采用父类的轮询方式，有一个默认每30秒（`public static final int DEFAULT_TIMER_INTERVAL = 30 * 1000;`）更新一次权重列表的定时任务，该定时任务会根据实例的响应时间来更新权重列表。

开启更新权重的定时任务：

```java
void initialize(ILoadBalancer lb) {        
    if (serverWeightTimer != null) {
        serverWeightTimer.cancel();
    }
    serverWeightTimer = new Timer("NFLoadBalancer-serverWeightTimer-"
                                  + name, true);
    serverWeightTimer.schedule(new DynamicServerWeightTask(), 0,
                               serverWeightTaskTimerInterval);
    // do a initial run
    ServerWeight sw = new ServerWeight();
    sw.maintainWeights();

    Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
        public void run() {
            logger
                .info("Stopping NFLoadBalancer-serverWeightTimer-"
                      + name);
            serverWeightTimer.cancel();
        }
    }));
}
```

choose方法做的事情就是，用一个(0,1)的随机double数乘以最大的权重得到randomWeight，然后遍历权重列表，找出第一个比randomWeight大的实例下标，然后返回该实例，代码略。

```java
@edu.umd.cs.findbugs.annotations.SuppressWarnings(value = "RCN_REDUNDANT_NULLCHECK_OF_NULL_VALUE")
@Override
public Server choose(ILoadBalancer lb, Object key) {
    if (lb == null) {
        return null;
    }
    Server server = null;

    while (server == null) {
        // get hold of the current reference in case it is changed from the other thread
        List<Double> currentWeights = accumulatedWeights;
        if (Thread.interrupted()) {
            return null;
        }
        List<Server> allList = lb.getAllServers();

        int serverCount = allList.size();

        if (serverCount == 0) {
            return null;
        }

        int serverIndex = 0;

        // last one in the list is the sum of all weights
        double maxTotalWeight = currentWeights.size() == 0 ? 0 : currentWeights.get(currentWeights.size() - 1); 
        // No server has been hit yet and total weight is not initialized
        // fallback to use round robin
        if (maxTotalWeight < 0.001d || serverCount != currentWeights.size()) {
            server =  super.choose(getLoadBalancer(), key);
            if(server == null) {
                return server;
            }
        } else {
            // generate a random weight between 0 (inclusive) to maxTotalWeight (exclusive)
            double randomWeight = random.nextDouble() * maxTotalWeight;
            // pick the server index based on the randomIndex
            int n = 0;
            for (Double d : currentWeights) {
                if (d >= randomWeight) {
                    serverIndex = n;
                    break;
                } else {
                    n++;
                }
            }

            server = allList.get(serverIndex);
        }

        if (server == null) {
            /* Transient. */
            Thread.yield();
            continue;
        }

        if (server.isAlive()) {
            return (server);
        }

        // Next.
        server = null;
    }
    return server;
}
```

## 2.4 最少并发量策略BestAvailableRule

选取最少并发量请求的服务器。

```java
@Override
public Server choose(Object key) {
    if (loadBalancerStats == null) {
        return super.choose(key);
    }
    // 获取所有的服务器的列表
    List<Server> serverList = getLoadBalancer().getAllServers();
    int minimalConcurrentConnections = Integer.MAX_VALUE;
    long currentTime = System.currentTimeMillis();
    Server chosen = null;
    for (Server server: serverList) {// 遍历每个服务器
        // 获取当前遍历的服务器的状态
        ServerStats serverStats = loadBalancerStats.getSingleServerStat(server);
        if (!serverStats.isCircuitBreakerTripped(currentTime)) {// 如果当前遍历的服务器没有触发断路器的话继续执行
            // 获取当前遍历的服务器的请求个数
            int concurrentConnections = serverStats.getActiveRequestsCount(currentTime);
            // 和已经遍历过的服务器中最少的请求数（minimalConcurrentConnections）进行比较，如果更小的的话，把当前服务器的请求数赋值给最少的请求数minimalConcurrentConnections变量，并把当前服务器赋值给chosen变量
            if (concurrentConnections < minimalConcurrentConnections) {
                minimalConcurrentConnections = concurrentConnections;
                chosen = server;
            }
        }
    }
    // 如果没有选上，调用父类（ClientConfigEnabledRoundRobinRule）的choose方法，也就是使用RoundRobinRule轮询的方式进行负载均衡 
    if (chosen == null) {
        return super.choose(key);
    } else {
        return chosen;
    }
}
```

# 3 项目中使用负载均衡策略

基于《客户端负载均衡 Ribbon》中的项目。

在启动类中加入负载均衡策略的配置，不配置的话默认策略是轮询策略。因为Feign基于Ribbon，锁英超这种方式对Feign也有效。

```java
package com.zh.ribbon;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;

import com.netflix.loadbalancer.BestAvailableRule;
import com.netflix.loadbalancer.IRule;

@SpringBootApplication
public class RibbonApplication {
	public static void main(String[] args) {
		SpringApplication.run(RibbonApplication.class, args);
	}
	
	@Bean
	@LoadBalanced
	public RestTemplate restTemplate() {
		return new RestTemplate();
	}
	@Bean
	public IRule ribbonRule() {
	    return new BestAvailableRule();
	}
}
```

# 4 自定义负载均衡策略

自定义负载均衡策略类必须继承`com.netflix.loadbalancer.AbstractLoadBalanceRule`类。