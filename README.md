# 互联网开发笔记

# 1 Java

## 1.1 Java基础

- [Java中的SPI机制](./docs/programming/java/Java_base/SPI_specification_in_Java.md)

## 1.2 网络编程

- [网络编程基础：BIO、NIO、AIO](./docs/programming/java/Network_programming/Network_programming_basics.md)
- [Netty](./docs/programming/java/Network_programming/Netty.md)

## 1.3 Tomcat

- [Tomcat介绍](./docs/programming/java/tomcat/Introduction_of_Tomcat.md)
- [Tomcat架构](./docs/programming/java/tomcat/Tomcat_architecture.md)

## 1.4 Spring

### 1.4.1 Spring FrameWork

- [后处理bean的接口BeanPostProcessor和BeanFactoryPostProcessor](./docs/programming/java/spring/spring_framework/Post-processing_bean_interfaces_BeanPostProcessor_and_BeanFactoryPostProcessor.md)
- [Spring AOP面向切面编程](./docs/programming/java/spring/spring_framework/Spring_AOP-Aspect_Oriented_Programming.md)
- [Spring入门](./docs/programming/java/spring/spring_framework/Getting_started_with_Spring.md)
- [Spring配置](./docs/programming/java/spring/spring_framework/Spring_configuration.md)
- [Spring中整合Junit4测试](./docs/programming/java/spring/spring_framework/Test_with_Junit4_in_Spring.md)
- [SpringMVC入门](./docs/programming/java/spring/spring_framework/Getting_started_with_SpringMVC.md)
- [SpringMVC架构](./docs/programming/java/spring/spring_framework/SpringMVC_architecture.md)

### 1.4.2 Spring Boot

- [Spring Boot中的自动装载](./docs/programming/java/spring/spring_boot/Automatic_loading_mechanism_in_Spring_Boot.md)
- [Spring Boot启动流程](./docs/programming/java/spring/spring_boot/Spring_Boot_startup_process.md)
- [Spring Boot启动流程监听器SpringApplicationRunListener](./docs/programming/java/spring/spring_boot/Spring_Boot_startup_process_monitor-SpringApplicationRunListener.md)
- [Spring Boot入门](./docs/programming/java/spring/spring_boot/Getting_started_with_Spring_Boot.md)
- [Spring Boot整合JSP](./docs/programming/java/spring/spring_boot/Use_JSP_in_Spring_Boot.md)

### 1.4.3 Spring Cloud

- [Spring Cloud介绍](./docs/programming/java/spring/spring_cloud/Introduction_to_Spring_Cloud.md)
- [服务调用方式](./docs/programming/java/spring/spring_cloud/Service_calling_method.md)
- [客户端负载均衡——Ribbon](./docs/programming/java/spring/spring_cloud/Load_balancing-Ribbon.md)
- [Ribbon中的负载均衡规则接口IRule](./docs/programming/java/spring/spring_cloud/Load_balancing_rules_interface-IRule_in_Ribbon.md)
- [Feign中的负载均衡和服务熔断](./docs/programming/java/spring/spring_cloud/Load_balancing_and_service_fuse_in_Feign.md)
- [Hystrix 容错机制和数据监控](./docs/programming/java/spring/spring_cloud/Fault_tolerance_mechanism_and_data_monitoring_in_Hystrix.md)
- [Zuul服务网关](./docs/programming/java/spring/spring_cloud/Service_Gateway-Zuul.md)
- [查看Zuul中每个过滤器的执行耗时](./docs/programming/java/spring/spring_cloud/View_the_execution_time_of_each_filter_in_Zuul.md)

# 2 Python

# 3 JavaScript

- [Javascript闭包](./docs/programming/JavaScript/Closures_in_JavaScript.md)
- [ES6](./docs/programming/JavaScript/ES6.md)

## 3.1 NodeJS

- [Nodejs入门](./docs/programming/JavaScript/nodejs/Getting_started_with_nodejs.md)
- [NodeJS包资源管理器NPM](./docs/programming/JavaScript/nodejs/Node_Package_Manager-NPM.md)
- [前端资源加载、打包工具——Webpack](./docs/programming/JavaScript/nodejs/Front-end_resource_loading_and_packaging_tools-Webpack.md)

## 3.2 VueJS

- [VueJS入门](./docs/programming/JavaScript/VueJS/Getting_started_with_VueJS.md)
- [VueJS常用指令](./docs/programming/JavaScript/VueJS/Common_commands-VueJS.md)
- [Vue实例的声明周期](./docs/programming/JavaScript/VueJS/Vue_instance_life_cycle.md)
- [VueJS中的Ajax](./docs/programming/JavaScript/VueJS/Ajax_in_VueJS.md)



# 4 Linux

## 4.1 Shell

- [Shell入门](./docs/programming/linux/shell/Getting_startted_with_Shell.md)
- [Shell基础知识](./docs/programming/linux/shell/Basic_knowledge_of_Shell_programming.md)
- [Shell函数](./docs/programming/linux/shell/Functions_in_Shell.md)
- [Shell文件包含](./docs/programming/linux/shell/Shell_file_contains.md)

### 4.1.1 Shell编程实践

- [使用Shell进行批量压缩](./docs/programming/linux/shell/Shell_programming_practice/Use_Shell_for_batch_compression.md)

# 5 设计模式

- [面向对象软件设计SOLID原则](./docs/programming/Design_Patterns/The_principles_of_object-oriented_software_design.md)
- [观察者模式](./docs/programming/Design_Patterns/Observer_pattern.md)
- [门面模式](./docs/programming/Design_Patterns/Facade_pattern.md)
- [装饰者模式](./docs/programming/Design_Patterns/Decorator_pattern.md)
- [责任链模式](./docs/programming/Design_Patterns/Chain_of_responsibility_pattern.md)
- [适配器模式](./docs/programming/Design_Patterns/Adapter_pattern.md)
- [Reactor反应堆模式](./docs/programming/Design_Patterns/Reactor_pattern.md)

# 6 高性能网站

## 6.1 概述

### 6.1.1 架构

- [CAP原则](./docs/programming/high_performance_website/overview/Architecture/CAP_Principle.md)

## 6.2 高并发

### 6.2.1 队列

- [队列的常见应用场景](./docs/programming/high_performance_website/high_concurrency/queue/common_application_scenarios_of_Nginx.md)
- [常见队列类型](./docs/programming/high_performance_website/high_concurrency/queue/common_queue_types.md)
- [基于Canal实现数据异构](./docs/programming/high_performance_website/high_concurrency/queue/realizing_data_heterogeneity_based_on_Canal.md)

#### 6.2.1.1 消息队列

##### 6.2.1.1.1 RabbitMQ

- [RabbitMQ入门](./docs/programming/high_performance_website/high_concurrency/queue/message_queue/RabbitMQ/Getting_started_with_RabbitMQ.md)

### 6.2.2 并发编程

- [并发编程概述](./docs/programming/high_performance_website/high_concurrency/asynchronous_concurrency/Overview.md)
- [Future模式](./docs/programming/high_performance_website/high_concurrency/asynchronous_concurrency/Future_mode.md)

## 6.3 高可用

### 6.3.1 负载均衡与反向代理

- [负载均衡与反向代理](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/load_balancing_and_reverse_proxy.md)

#### 6.3.1.1 Nginx

- [Nginx入门](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/Getting_started_with_nginx.md)
- [在Nginx中设置虚拟主机](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/Set_up_virtual_hosts_in_Nginx.md)
- [在Nginx设置负载均衡和反向代理](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/the_configuration_of_load_balancing_and_reverse_prohigh_concurrencyxy_in_Nginx.md)
- [Nginx高可用](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/Nginx_high_availability.md)
- [Nginx负载均衡算法](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/Load_balancing_algorithm-Nginx.md)

### 6.3.2 隔离

- 

# 7 数据库

## 7.1 关系型数据库

### 7.1.1 MySQL

- [MySQL数据库优化](./docs/programming/database/relational_database/MySQL_optimization.md)
- [事务的隔离级别](./docs/programming/database/relational_database/The_isolation_level_of_transaction.md)
- [使用explain和`show profile`来分析SQL语句](./docs/programming/database/relational_database/Use_explain_and_show-profile_to_analyze_SQL_statements.md)
- [`ORDER BY`的工作原理](./docs/programming/database/relational_database/How_order_by_works.md)

## 7.2 非关系型数据库

### 7.2.1 Redis

- [Redis入门](./docs/programming/database/NoSQL/redis/getting_started_with_redis.md)
- [Redis为什么这么快](./docs/programming/database/NoSQL/redis/Reasons_why_Redis_is_so_fast.md)
- [Redis中过期键的删除策略](./docs/programming/database/NoSQL/redis/Deletion_strategy_of_expired_keys_in_Redis.md)
- [Redis中的数据逐出策略](./docs/programming/database/NoSQL/redis/Data_eviction_strategy_in_Redis.md)
- [Jedis中的管道Pipeline](./docs/programming/database/NoSQL/redis/Jedis_pipeline.md)
- [在Spring中整合Redis](./docs/programming/database/NoSQL/redis/Use_redis_in_Spring_Framework.md)

# 8 数据结构

# 9 常用算法

- [缓存替换算法](./docs/programming/algorithm/Cache_algorithm.md)

# 10 检索技术

## 10.1 Lucene

- [Lucene全文检索技术概述](./docs/programming/Retrieval_technology/Lucene/The_overview_of_full-text_search_technology-Lucene.md)
- [Lucene入门](./docs/programming/Retrieval_technology/Lucene/Getting_started_with_Lucene.md)
- [分词器](./docs/programming/Retrieval_technology/Lucene/Analyzer.md)
- [Field域](./docs/programming/Retrieval_technology/Lucene/Field.md)
- [索引维护](./docs/programming/Retrieval_technology/Lucene/Index_maintenance.md)
- [搜索](./docs/programming/Retrieval_technology/Lucene/Search.md)
- [相关度排序](./docs/programming/Retrieval_technology/Lucene/Relevance_ranking.md)

## 10.2 ElasticSearch

- [ElasticSearch入门](./docs/programming/Retrieval_technology/ElasticSearch/Getting_started_with_ElasticSearch.md)
- [IK分词器](./docs/programming/Retrieval_technology/ElasticSearch/analysis_ik.md)
- [映射](./docs/programming/Retrieval_technology/ElasticSearch/mapping.md)
- [在Java中使用ElasticSearch](./docs/programming/Retrieval_technology/ElasticSearch/Using_ElasticSearch_in_Java.md)
- [ElasticSearch集群管理](./docs/programming/Retrieval_technology/ElasticSearch/Cluster_management-ElasticSearch.md)
- [节点](./docs/programming/Retrieval_technology/ElasticSearch/node-ElasticSearch.md)
- [传输模块](./docs/programming/Retrieval_technology/ElasticSearch/transport-ElasticSearch.md)

# 11 开发工具的使用

## 11.1 VSCode

- [前端插件](./docs/programming/The_use_of_development_tools/VSCode/Front-end_plugin.md)

## 11.2 Sublime

- [多位置同时编辑——Sublime3](./docs/programming/The_use_of_development_tools/Sublime/Simultaneous_editing_in_multiple_locations-Sublime3.md)