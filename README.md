# 开发笔记

# 1 Java

## 1.1 Java

| 类别        | 笔记                                                         |
| ----------- | ------------------------------------------------------------ |
| 关键字解释  | [final](./docs/programming/java/Java_base/final.md)          |
| 类的管理    | [Java中的SPI机制](./docs/programming/java/Java_base/SPI_specification_in_Java.md)<br />[Java中类的生命周期](./docs/programming/java/Java_base/Life_cycle_of_classes_in_Java.md)<br />[编译时常量和运行时常量](./docs/programming/java/Java_base/compile-constant_and_runtime-constant_in_Java.md)<br />[注解解释](./docs/programming/java/Java_base/Annotation_explanation.md) |
| 反射机制    | [Class类](./docs/programming/java/reflection/Class.md)<br />[Java反射机制](./docs/programming/java/reflection/Java_Reflection.md)<br />[JDK动态代理Proxy](./docs/programming/java/reflection/Proxy.md) |
| 网络编程    | [网络编程基础：BIO、NIO、AIO](./docs/programming/java/Network_programming/Network_programming_basics.md)<br />[Netty](./docs/programming/java/Network_programming/Netty.md) |
| Java8新特性 | [Java8新时间API](./docs/programming/java/java8/Date_and_time_API_in_Java8.md) |

## 1.2 JVM-HotSpot

| 类别           | 笔记                                                         |
| -------------- | ------------------------------------------------------------ |
| 虚拟机监控工具 | [虚拟机监控工具概述](./docs/programming/java/jvm/HotSpot/Overview.md)<br />[Attach 机制](./docs/programming/java/jvm/HotSpot/Attach_Mechanism.md)<br />[查看JVM进程](./docs/programming/java/jvm/HotSpot/View_JVM_process.md) |
|                |                                                              |
|                |                                                              |

## 1.3 Tomcat

- [Tomcat介绍](./docs/programming/java/tomcat/Introduction_of_Tomcat.md)
- [Tomcat架构](./docs/programming/java/tomcat/Tomcat_architecture.md)

## 1.4 Spring

### 1.4.1 Spring Framework

|          类别 | 笔记列表                                                     |
| ------------: | ------------------------------------------------------------ |
|    Spring基础 | [Spring入门](./docs/programming/java/spring/spring_framework/Getting_started_with_Spring.md)<br/>[Spring配置](./docs/programming/java/spring/spring_framework/Spring_configuration.md)<br/>[Spring AOP面向切面编程](./docs/programming/java/spring/spring_framework/Spring_AOP-Aspect_Oriented_Programming.md)<br/>[Spring中整合Junit4测试](./docs/programming/java/spring/spring_framework/Test_with_Junit4_in_Spring.md) |
|    Spring高级 | [后处理bean的接口BeanPostProcessor和BeanFactoryPostProcessor](./docs/programming/java/spring/spring_framework/Post-processing_bean_interfaces_BeanPostProcessor_and_BeanFactoryPostProcessor.md) |
| SpringMVC基础 | [SpringMVC入门](./docs/programming/java/spring/spring_framework/Getting_started_with_SpringMVC.md)<br/>[SpringMVC架构](./docs/programming/java/spring/spring_framework/SpringMVC_architecture.md) |

### 1.4.2 Spring Boot

[Spring Boot自测](./docs/programming/java/spring/spring_boot/self-test_in_Spring_Boot.md)

|            类别 | 笔记列表                                                     |
| --------------: | ------------------------------------------------------------ |
| Spring Boot基础 | [Spring Boot入门](./docs/programming/java/spring/spring_boot/Getting_started_with_Spring_Boot.md)<br/>[Spring Boot整合JSP](./docs/programming/java/spring/spring_boot/Use_JSP_in_Spring_Boot.md)<br/>[Spring Boot 怎么处理异常](./docs/programming/java/spring/spring_boot/How_SpringBoot_handles_exceptions.md)<br/>[Spring Boot开启CORS跨域支持](./docs/programming/java/spring/spring_boot/Spring_Boot_opens_CORS_cross-domain_support.md) |
|      整合数据库 | [SpringBoot整合JDBC](./docs/programming/java/spring/spring_boot/database/Using_JDBC_with_Spring_Boot.md)<br/>[SpringBoot中整合SpringDataJPA](./docs/programming/java/spring/spring_boot/database/Using_Spring_Data_JPA_with_Spring_Boot.md)<br/>[SpringBoot中整合SpringDataRedis](./docs/programming/java/spring/spring_boot/database/Using_Spring_Data_Redis_with_Spring_Boot.md)<br/>[使用SpringCache抽象工具](./docs/programming/java/spring/spring_boot/database/Spring_cache.md) |
| Spring Boot高级 | [Spring Boot启动流程](./docs/programming/java/spring/spring_boot/Spring_Boot_startup_process.md)<br/>[Spring Boot启动流程监听器SpringApplicationRunListener](./docs/programming/java/spring/spring_boot/Spring_Boot_startup_process_monitor-SpringApplicationRunListener.md)<br/>[Spring Boot中的自动装载](./docs/programming/java/spring/spring_boot/Automatic_loading_mechanism_in_Spring_Boot.md) |

### 1.4.3 Spring Cloud

|             类别 | 笔记列表                                                     |
| ---------------: | ------------------------------------------------------------ |
| Spring Cloud基础 | [Spring Cloud介绍](./docs/programming/java/spring/spring_cloud/Introduction_to_Spring_Cloud.md)<br/>[服务调用方式](./docs/programming/java/spring/spring_cloud/Service_calling_method.md) |
|   服务注册和发现 |                                                              |
|   软负载均衡调用 | [客户端负载均衡——Ribbon](./docs/programming/java/spring/spring_cloud/Load_balancing-Ribbon.md)<br/>[Ribbon中的负载均衡规则接口IRule](./docs/programming/java/spring/spring_cloud/Load_balancing_rules_interface-IRule_in_Ribbon.md)<br/>[Feign中的负载均衡和服务熔断](./docs/programming/java/spring/spring_cloud/Load_balancing_and_service_fuse_in_Feign.md) |
|         熔断机制 | [Hystrix 容错机制和数据监控](./docs/programming/java/spring/spring_cloud/Fault_tolerance_mechanism_and_data_monitoring_in_Hystrix.md) |
|         配置中心 | [配置中心](./docs/programming/java/spring/spring_cloud/Configuration_Center.md)<br/>[Spring Cloud Config](./docs/programming/java/spring/spring_cloud/Spring_Cloud_Config.md) |
|          API网关 | [Zuul服务网关](./docs/programming/java/spring/spring_cloud/Service_Gateway-Zuul.md)<br/>[查看Zuul中每个过滤器的执行耗时](./docs/programming/java/spring/spring_cloud/View_the_execution_time_of_each_filter_in_Zuul.md) |
|     服务优化工具 | [Zipkin分布式跟踪系统](./docs/programming/java/spring/spring_cloud/Zipkin-a_distributed_tracing_system.md) |

# 2 Python

## 2.1 Python基础

- [Python内置函数之eval()、exec()、compile()函数](./docs/programming/python/Basic_knowledge_of_Python/Functions_eval_exec_compile_in_python.md)

# 3 JavaScript

- [Javascript闭包](./docs/programming/JavaScript/Closures_in_JavaScript.md)
- [ES6](./docs/programming/JavaScript/ES6.md)
- [模块化相关规范](./docs/programming/JavaScript/Module_Definition_Specifications.md)
- [JavaScript中的小括号](./docs/programming/JavaScript/parentheses_in_JavaScript.md)
- [JavaScript 自执行函数表达式](./docs/programming/JavaScript/self-executing_function_expression-JavaScript.md)
- [跨域](./docs/programming/JavaScript/Cross-domain.md)

## 3.1 NodeJS

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Nodejs入门](./docs/programming/JavaScript/nodejs/Getting_started_with_nodejs.md) | [NodeJS包资源管理器NPM](./docs/programming/JavaScript/nodejs/Node_Package_Manager-NPM.md) |
| [前端资源加载、打包工具——Webpack](./docs/programming/JavaScript/nodejs/Front-end_resource_loading_and_packaging_tools-Webpack.md) |                                                              |

## 3.2 VueJS

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [VueJS入门](./docs/programming/JavaScript/VueJS/Getting_started_with_VueJS.md) | [VueJS常用指令](./docs/programming/JavaScript/VueJS/Common_commands-VueJS.md) |
| [Vue实例的声明周期](./docs/programming/JavaScript/VueJS/Vue_instance_life_cycle.md) | [VueJS中的Ajax](./docs/programming/JavaScript/VueJS/Ajax_in_VueJS.md) |
| [路由框架vue-router](./docs/programming/JavaScript/VueJS/vue-router.md) |                                                              |

# 4 Linux

## 4.1 Shell

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Shell入门](./docs/programming/linux/shell/Getting_startted_with_Shell.md) | [Shell变量](./docs/programming/linux/shell/variable-Shell.md) |
| [Shell数组](./docs/programming/linux/shell/array_in_Shell.md) | [Shell字符串](./docs/programming/linux/shell/string-Shell.md) |
| [Shell中流程控制](./docs/programming/linux/shell/Process_control_in_Shell.md) | [Shell中的test](./docs/programming/linux/shell/test-Shell.md) |
| [Shell文件包含](./docs/programming/linux/shell/Shell_file_contains.md) | [Shell函数](./docs/programming/linux/shell/Functions_in_Shell.md) |
| [Shell中的()、(())以及{}](./docs/programming/linux/shell/parenthesis_and_double-parenthesis_big-parantheses.md) | [执行Shell脚本的方式sh、bash、./、source](./docs/programming/linux/shell/bash-sh-source.md) |

### 4.1.1 Shell编程实践

- [使用Shell进行批量压缩](./docs/programming/linux/shell/Shell_programming_practice/Use_Shell_for_batch_compression.md)
- [使用Shell进行迭代重命名](./docs/programming/linux/shell/Shell_programming_practice/Use_Shell_for_batch_renaming.md)
- [便利使用virtualenv](./docs/programming/linux/shell/Shell_programming_practice/Easy_to_use_virtualenv.md)

# 5 设计模式

| 类别     | 笔记                                                         |
| -------- | ------------------------------------------------------------ |
| 概述     | [设计模式自测](./docs/programming/Design_Patterns/self-test_for_design_pattern.md)<br />[面向对象软件设计SOLID原则](./docs/programming/Design_Patterns/The_principles_of_object-oriented_software_design.md) |
| 创建模式 | [工厂方法模式](./docs/programming/Design_Patterns/Factory_method_pattern.md)<br />[抽象工厂模式](./docs/programming/Design_Patterns/Abstract_factory_pattern.md)<br />[单例模式](./docs/programming/Design_Patterns/Singleton_pattern.md)<br />[建造者模式](./docs/programming/Design_Patterns/Builder_pattern.md)<br />[原型模式]() |
| 结构模式 | [适配器模式](./docs/programming/Design_Patterns/Adapter_pattern.md)<br />[门面模式](./docs/programming/Design_Patterns/Facade_pattern.md)<br />[装饰者模式](./docs/programming/Design_Patterns/Decorator_pattern.md)<br />[桥接模式]()<br />[过滤器模式]()<br />[组合模式]()<br />[享元模式]()<br />[代理模式]() |
| 行为模式 | [模板方法模式](./docs/programming/Design_Patterns/Template_method_pattern.md)<br />[策略模式](./docs/programming/Design_Patterns/Strategy_pattern.md)<br />[责任链模式](./docs/programming/Design_Patterns/Chain_of_responsibility_pattern.md)<br />[观察者模式](./docs/programming/Design_Patterns/Observer_pattern.md)<br />[Reactor反应堆模式](./docs/programming/Design_Patterns/Reactor_pattern.md)<br />[解释器模式]()<br />[命令模式]()<br />[迭代器模式]()<br />[参观者模式]() |

# 6 高性能网站

## 6.1 概述

- [分布式和集群系统下的身份认证](./docs/programming/java/Java_base/Identity_authentication_in_distributed_and_cluster_systems.md)

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
- [并发编程基础](./docs/programming/high_performance_website/high_concurrency/asynchronous_concurrency/Basics_of_concurrent_programming.md)
- [Future模式](./docs/programming/high_performance_website/high_concurrency/asynchronous_concurrency/Future_mode.md)

## 6.3 高可用

### 6.3.1 负载均衡与反向代理

- [负载均衡与反向代理](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/load_balancing_and_reverse_proxy.md)
- [LVS](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/LVS.md)
- [LVS+Nginx+Keepalived](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/LVS+Nginx+Keepalived.md)

#### 6.3.1.1 Nginx

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Nginx入门](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/Getting_started_with_nginx.md) | [在Nginx中设置虚拟主机](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/Set_up_virtual_hosts_in_Nginx.md) |
| [在Nginx设置负载均衡和反向代理](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/the_configuration_of_load_balancing_and_reverse_proxy_in_Nginx.md) | [Nginx高可用](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/Nginx_high_availability.md) |
| [Nginx负载均衡算法](./docs/programming/high_performance_website/high_availability/load_balancing_and_reverse_proxy/nginx/Load_balancing_algorithm-Nginx.md) |                                                              |

### 6.3.2 隔离

- [隔离概述](./docs/programming/high_performance_website/high_availability/isolation/overview.md)

### 6.3.3 限流

### 6.3.4 降级

### 6.3.5 超时和重试机制

- [超时和重试机制概述](./docs/programming/high_performance_website/high_availability/timeout_and_retry_mechanism/overview.md)

# 7 数据库

## 7.1 关系型数据库

### 7.1.1 MySQL

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [MySQL数据库优化](./docs/programming/database/relational_database/MySQL_optimization.md) | [事务的隔离级别](./docs/programming/database/relational_database/The_isolation_level_of_transaction.md) |
| [使用explain和`show profile`来分析SQL语句](./docs/programming/database/relational_database/Use_explain_and_show-profile_to_analyze_SQL_statements.md) | [`ORDER BY`的工作原理](./docs/programming/database/relational_database/How_order_by_works.md) |
| [MySQL索引](./docs/programming/database/relational_database/MySQL-index.md) | [MySQL中的锁机制](./docs/programming/database/relational_database/Lock_mechanism_MySQL.md) |

## 7.2 非关系型数据库

### 7.2.1 Redis

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Redis入门](./docs/programming/database/NoSQL/redis/getting_started_with_redis.md) | [在Spring中整合Redis](./docs/programming/database/NoSQL/redis/Use_redis_in_Spring_Framework.md) |
| [Redis为什么这么快](./docs/programming/database/NoSQL/redis/Reasons_why_Redis_is_so_fast.md) | [Redis中过期键的删除策略](./docs/programming/database/NoSQL/redis/Deletion_strategy_of_expired_keys_in_Redis.md) |
| [Redis中的数据逐出策略](./docs/programming/database/NoSQL/redis/Data_eviction_strategy_in_Redis.md) | [Jedis中的管道Pipeline](./docs/programming/database/NoSQL/redis/Jedis_pipeline.md) |
| [Redis缓存乱码问题](./docs/programming/database/NoSQL/redis/Chinese_garbled_in_Redis.md) |                                                              |

# 8 数据结构

## 查找（Searching）

| 笔记                                                         | 笔记 |
| ------------------------------------------------------------ | ---- |
| [动态查找表（Dynamic Search Table）](./docs/programming/data_structure/searching/Dynamic_Search_Table.md) |      |
|                                                              |      |
|                                                              |      |

# 9 常用算法

- [缓存替换算法](./docs/programming/algorithm/Cache_algorithm.md)

# 10 检索技术

## 10.1 Lucene

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Lucene全文检索技术概述](./docs/programming/Retrieval_technology/Lucene/The_overview_of_full-text_search_technology-Lucene.md) | [Lucene入门](./docs/programming/Retrieval_technology/Lucene/Getting_started_with_Lucene.md) |
| [分词器](./docs/programming/Retrieval_technology/Lucene/Analyzer.md) | [Field域](./docs/programming/Retrieval_technology/Lucene/Field.md) |
| [索引维护](./docs/programming/Retrieval_technology/Lucene/Index_maintenance.md) | [搜索](./docs/programming/Retrieval_technology/Lucene/Search.md) |
| [相关度排序](./docs/programming/Retrieval_technology/Lucene/Relevance_ranking.md) |                                                              |

## 10.2 ElasticSearch

[ElasticSearch自测](./docs/programming/Retrieval_technology/ElasticSearch/self-test_of_ElasticSearch.md)

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [ElasticSearch入门](./docs/programming/Retrieval_technology/ElasticSearch/Getting_started_with_ElasticSearch.md) | [IK分词器](./docs/programming/Retrieval_technology/ElasticSearch/analysis_ik.md) |
| [映射](./docs/programming/Retrieval_technology/ElasticSearch/mapping.md) | [在Java中使用ElasticSearch](./docs/programming/Retrieval_technology/ElasticSearch/Using_ElasticSearch_in_Java.md) |
| [ElasticSearch集群管理](./docs/programming/Retrieval_technology/ElasticSearch/Cluster_management-ElasticSearch.md) | [节点](./docs/programming/Retrieval_technology/ElasticSearch/node-ElasticSearch.md) |
| [传输模块](./docs/programming/Retrieval_technology/ElasticSearch/transport-ElasticSearch.md) |                                                              |

# 11 虚拟化

## 11.1 Docker

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [Docker入门](./docs/programming/Virtualization/Docker/Getting_started_with_Docker.md) | [Docker中的常用命令](./docs/programming/Virtualization/Docker/Common_commands_in_Docker.md) |
| [在Docker中应用部署](./docs/programming/Virtualization/Docker/Deploy_applications_in_Docker.md) | [迁移与备份——Docker](./docs/programming/Virtualization/Docker/Migration_and_backup-docker.md) |
| [Dockerfile](./docs/programming/Virtualization/Docker/Dockerfile.md) | [Docker私有仓库](./docs/programming/Virtualization/Docker/private_registry-Docker.md) |

# 12 网络爬虫

- [网络爬虫概述](./docs/programming/web_crawler/the_overview_of_web_crawl.md)

## 12.1 Webmagic——Java

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [WebMagic架构](./docs/programming/web_crawler/Webmagic/webmagic_architecture.md) | [WebMagic的项目组成](./docs/programming/web_crawler/Webmagic/webmagic_project_composition.md) |
| [WebMagic入门](./docs/programming/web_crawler/Webmagic/getting_started_with_webmagic.md) | [实现PageProcessor](./docs/programming/web_crawler/Webmagic/PageProcessor.md) |
| [使用Pipeline保存结果](./docs/programming/web_crawler/Webmagic/Pipeline.md) | [设置代理ProxyProvider](./docs/programming/web_crawler/Webmagic/ProxyProvider.md) |
| [使用和定制Scheduler](./docs/programming/web_crawler/Webmagic/Scheduler.md) | [URL去重接口DuplicateRemover](./docs/programming/web_crawler/Webmagic/DuplicateRemover.md) |

## 12.2 Selenium与PhantomJS

- [在Python中使用Selenium做爬虫](./docs/programming/web_crawler/Selenium_PhantomJS/Selenium_and_PhantomJS_in_Python.md)

# 13 人工智能

- [人工智能概述](./docs/programming/Artificial_Intelligence/The_overview_of_Artificial_Intelligence.md)
- [机器学习概述](./docs/programming/Artificial_Intelligence/The_overview_of_Machine_learning.md)

## 13.1 基础知识

### 13.1.1 知识表示

| 分项                                                         | 分项 |
| ------------------------------------------------------------ | ---- |
| [知识和知识表示的相关概念](./docs/programming/Artificial_Intelligence/basic_knowledge/knowledge_representation/Related_concepts_of_knowledge_and_knowledge_representation.md) |      |
|                                                              |      |

## 13.2 机器学习算法

### 13.2.1 K-近邻算法

| 分项                                                         | 分项                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [K-近邻算法概述](./docs/programming/Artificial_Intelligence/algorithm-Machine_learning/KNN/KNN_overview.md) | [KNN入门](./docs/programming/Artificial_Intelligence/algorithm-Machine_learning/KNN/Getting_started_with_KNN.md) |
| [距离度量](./docs/programming/Artificial_Intelligence/algorithm-Machine_learning/KNN/distance_measure.md) |                                                              |

# 14 开发工具的使用

## 14.1 VSCode

- [前端插件](./docs/programming/The_use_of_development_tools/VSCode/Front-end_plugin.md)

## 14.2 Sublime

- [多位置同时编辑——Sublime3](./docs/programming/The_use_of_development_tools/Sublime/Simultaneous_editing_in_multiple_locations-Sublime3.md)

## 14.3 Python

- [pip](./docs/programming/The_use_of_development_tools/python/pip.md)
- [Python及其模块版本控制](./docs/programming/The_use_of_development_tools/python/Version_management_of_Python_and_its_modules.md)