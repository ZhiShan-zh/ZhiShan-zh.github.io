# Spring Cloud简介

# 1 Spring Cloud 概述
Spring Cloud是一系列框架的有序集合（业界也戏称为“肯德基缤纷全家桶”）。它利用Spring Boot的开发便利性巧妙地简化了分布式系统基础实施的开发，如服务注册发现、配置中心、消息总线、负载均衡、断路器、数据监控等，都可以用Spring Boot的开发风格做到一键启动和部署。Spring并没有重复制造轮子，它只是将目前各家公司开发的比较成熟、经得起实际考验的服务框架组合起来，通过Spring Boot分割进行在封装屏蔽掉了复杂的配置和实现原理，最终给开发者留出了一套简单易懂、易部署和易维护的分布式系统开发工具包。
![image.png](https://zhishan-zh.github.io/media/1583723078875-e4b77c9d-9554-4355-94e8-9688cb01c2c5.png)


# 2 Spring Cloud特点
Spring cloud当然也遵循约定优于配置的原则，这很Spring！
Spring cloud开箱即用、配置简单、编写代码简单、部署简单。
Spring cloud适用于各种环境，即可单独部署，又可集中部署，轻量级的组件。
Spring cloud支持丰富的组件集成、并且有90%的主流框架配置项参数提供。
Spring cloud实现了一套完整的微服务流程，各个方面考虑周全。


# 3 微服务中的相关概念
## 3.1 服务注册与发现
**服务注册**：服务实例将自身服务信息注册到注册中心。这部分服务信息包括服务所在主机IP和提供服务的Port，以及暴露服务自身状态以及访问协议等信息。
**服务发现**：服务实例请求注册中心获取所依赖服务信息。服务实例通过注册中心，获取到注册到其中的服务实例的信息，通过这些信息去请求它们提供的服务。
## 3.2 负载均衡
负载均衡是高可用网络基础架构的关键组件，通常用于将工作负载分布到多个服务器来提高网站、应用、数据库或其他服务的性能和可靠性。
## 3.3 熔断
**熔断**这一概念来源于电子工程中的断路器（Circuit Breaker）。在互联网系统中，当下游服务因访问压力过大而响应变慢或失败，上游服务为了保护系统整体的可用性，可以暂时切断对下游服务的调用。这种牺牲局部，保全整体的措施就叫做熔断。
## 3.4 链路追踪
随着微服务架构的流行，服务按照不同的维度进行拆分，一次请求往往需要涉及到多个服务。互联网应用构建在不同的软件模块集上，这些软件模块，有可能是由不同的团队开发、可能使用不同的编程语言来实现、有可能布在了几千台服务器，横跨多个不同的数据中心。因此，就需要对一次请求涉及的多个服务链路进行日志记录，性能监控即链路追踪。
## 3.5 API网关
随着微服务的不断增多，不同的微服务一般会有不同的网络地址，而外部客户端可能需要调用多个服务的接口才能完成一个业务需求，如果让客户端直接与各个微服务通信可能出现：

- 客户端需要调用不同的url地址，增加难度
- 再一定的场景下，存在跨域请求的问题
- 每个微服务都需要进行单独的身份认证

针对这些问题，API网关顺势而生。

**API网关**直面意思是将所有API调用统一接入到API网关层，由网关层统一接入和输出。一个网关的基本功能有：统一接入、安全防护、协议适配、流量管控、长短链接支持、容错能力。有了网关之后，各个API服务提供团队可以专注于自己的的业务逻辑处理，而API网关更专注于安全、流量、路由等问题。
![image.png](https://zhishan-zh.github.io/media/1588129234131-e0ecdec5-634d-4f18-b2ca-4f03a16350ee.png)

# 3 Spring Cloud组成
Spring Cloud的子项目，大致可分为两类，一类是对现有成熟框架“Spring Boot化”的封装和抽象，也是数量最多的项目；第二类是开发了一部分分布式系统的基础设施的实现，如Spring Cloud Stream扮演的就是kafka，ActiveMQ这样的角色。对于我们想快速实践微服务的开发者来说，第一类子项目就已经足够使用，如：

- Spring Cloud Netflix是对Netflix开发的一套分布式服务框架的封装，包括服务的发现和注册，负载均衡、断路器、REST客户端、请求路由等。
- Spring Cloud Config将配置信息中央化保存，配置Spring Cloud Bus可以实现动态修改配置文件。
- Spring Cloud Bus分布式消息队列，是对Kafka，MQ的封装
- Spring Cloud Security是对Spring Security的封装，并能配合Netflix使用。
- Spring Cloud Zookeeper是对Zookeeper的封装，使之能配置其他Spring Cloud子项目使用
- Spring Cloud Eureka是Spring Cloud Netflix微服务套件中的一部分，它基于Netflix Eureka做了二次封装，主要负责完成微服务架构中的服务治理功能。



# 4 Spring Cloud架构
## 4.1 SpringCloud中的核心组件
Spring Cloud的本质是在 Spring Boot 的基础上，增加了一堆微服务相关的规范，并对应用上下文（Application Context）进行了功能增强。既然 Spring Cloud 是规范，那么就需要去实现，目前Spring Cloud 规范已有 Spring官方，Spring Cloud Netflix，Spring Cloud Alibaba等实现。通过组件化的方式，Spring Cloud将这些实现整合到一起构成全家桶式的微服务技术栈。
### 4.1.1 Spring Cloud Netflix组件
| **组件名称** | **作用** |
| ---: | :--- |
| Eureka | 服务注册中心 |
| Ribbon | 客户端负载均衡 |
| Feign | 声明式服务调用 |
| Hystrix | 客户端容错保护 |
| Zuul | API服务网关 |

### 4.1.2 Spring Cloud Alibaba组件
| **组件**名称**** | **作用** |
| ---: | :--- |
| Nacos | 服务注册中心 |
| Sentinel | 客户端容错保护 |

### 4.1.3 Spring Cloud原生及其他组件
| **组件名称** | **作用** |
| ---: | :--- |
| Consul | 服务注册中心 |
| Config | 分布式配置中心 |
| Gateway | API服务网关 |
| Sleuth/Zipkin | 分布式链路追踪 |



## 4.2 Spring Cloud的体系结构
![image.png](https://zhishan-zh.github.io/media/1588134805141-60706907-b6f5-4081-affb-6fd4c9173478.png)
从上图可以看出SpringCloud各个组件相互配合，合作支持了一套完整的微服务架构。


- **注册中心**负责服务的注册与发现，很好将各服务连接起来；
- **断路器**负责监控服务之间的调用情况，连续多次失败进行熔断保护；
- **API网关**负责转发所有对外的请求和服务；
- **配置中心**提供了统一的配置信息管理服务,可以实时的通知各个服务获取最新的配置信息；
- **链路追踪技术**可以将所有的请求数据记录下来，方便我们进行后续分析；
- 各个组件又提供了功能完善的**dashboard监控平台**,可以方便的监控各组件的运行状况。


