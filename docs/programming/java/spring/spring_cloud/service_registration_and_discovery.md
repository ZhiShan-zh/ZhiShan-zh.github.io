# 服务注册和发现

**服务注册**：服务实例在启动的时候将自身服务信息注册到注册中心。这部分服务信息包括服务所在主机IP和提供服务的端口号Port，以及暴露服务自身状态以及访问协议、别名等信息。
**服务发现**：服务实例请求注册中心获取所依赖服务信息（通过别名）。服务实例通过注册中心，获取到注册到其中的服务实例的信息，通过这些信息去请求它们提供的服务。

常用注册中心：

- Spring Cloud：
  - Redis
  - Zookeeper
- Dubbo：
  - Spring Cloud Netflix Eureka
  - Spring Cloud Zookeeper
  - Spring Cloud Consul