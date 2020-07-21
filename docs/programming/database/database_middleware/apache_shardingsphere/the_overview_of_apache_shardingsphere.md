# Apache ShardingSphere 简介

# 1 ShardingSphere简介

- 一套开源的分布式数据库中间件解决方案组成的生态圈。
- 有三个产品： JDBC、Proxy 和 Sidecar(TODO)，这 3 款相互独立，却又能够混合部署配合使用的产品组成。
    - 它们均提供标准化的数据分片、分布式事务和数据库治理功能，可适用于如 Java 同构、异构语言、云原生等各种多样化的应用场景。
- 定位为关系型数据库中间件，旨在充分合理地在分布式的场景下利用关系型数据库的计算和存储能
    力，而并非实现一个全新的关系型数据库。
- Apache ShardingSphere 5.x 版本开始致力于可插拔架构，项目的功能组件能够灵活的以可插拔的方式进行扩展。

![ShardingSphere Scope](https://zhishan-zh.github.io/media/shardingsphere-scope_cn.png)

**核心功能**：

- 数据分片
    - 分库 & 分表
    - 读写分离
    - 分片策略定制化
    - 无中心化分布式主键
- 分布式事务
    - 标准化事务接口
    - XA 强一致事务
    - 柔性事务
- 数据库治理
    - 分布式治理
    - 数据迁移 & 弹性伸缩
    - 可视化链路追踪支持
    - 数据脱敏

# 2 ShardingSphere-JDBC

## 2.1 概述

定位为轻量级 Java 框架，在 Java 的 JDBC 层提供的额外服务。 它使用客户端直连数据库，以 jar 包形式提供服务，无需额外部署和依赖，可理解为增强版的 JDBC 驱动，完全兼容 JDBC 和各种 ORM 框架。

- 适用于任何基于 JDBC 的 ORM 框架，如：JPA, Hibernate, Mybatis, Spring JDBC Template 或直接使用 JDBC。
- 支持任何第三方的数据库连接池，如：DBCP, C3P0, BoneCP, Druid, HikariCP 等。
- 支持任意实现 JDBC 规范的数据库，目前支持 MySQL，Oracle，SQLServer，PostgreSQL 以及任何遵循 SQL92 标准的数据库。

![ShardingSphere-JDBC Architecture](https://zhishan-zh.github.io/media/shardingsphere-jdbc-brief.png)

## 2.2 入门案例

### 2.2.1 引入maven依赖

```xml
<dependency>
    <groupId>org.apache.shardingsphere</groupId>
    <artifactId>sharding-jdbc-core</artifactId>
    <version>4.1.1</version>
</dependency>
```

### 2.2.2 规则配置

配置是整个Sharding-JDBC的核心，是Sharding-JDBC中唯一与应用开发者打交道的模块。配置模块也是Sharding-JDBC的门户，通过它可以快速清晰的理解Sharding-JDBC所提供的功能。

Sharding-JDBC可以通过Java，YAML，Spring命名空间和Spring Boot Starter四种方式配置，开发者可根据场景选择适合的配置方式。详情请参见[配置手册](https://shardingsphere.apache.org/document/legacy/4.x/document/cn/manual/sharding-jdbc/configuration/)。

### 2.2.3 创建DataSource

通过ShardingDataSourceFactory工厂和规则配置对象获取ShardingDataSource，ShardingDataSource实现自JDBC的标准接口DataSource。然后即可通过DataSource选择使用原生JDBC开发，或者使用JPA, MyBatis等ORM工具。

```java
DataSource dataSource = ShardingDataSourceFactory.createDataSource(dataSourceMap, shardingRuleConfig, props);
```

# 3 ShardingSphere-Proxy

## 3.1 概述

定位为透明化的数据库代理端，提供封装了数据库二进制协议的服务端版本，用于完成对异构语言的支持。 目前提供 MySQL 和 PostgreSQL 版本，它可以使用任何兼容 MySQL/PostgreSQL 协议的访问客户端(如：MySQL Command Client, MySQL Workbench, Navicat 等)操作数据，对 DBA 更加友好。

- 向应用程序完全透明，可直接当做 MySQL/PostgreSQL 使用。
- 适用于任何兼容 MySQL/PostgreSQL 协议的的客户端。

![ShardingSphere-Proxy Architecture](https://zhishan-zh.github.io/media/shardingsphere-proxy-brief.png)

## 3.2 入门案例

### 3.2.1 规则配置

编辑`%SHARDING_PROXY_HOME%\conf\config-xxx.yaml`。详情请参见[配置手册](https://shardingsphere.apache.org/document/legacy/4.x/document/cn/manual/sharding-proxy/configuration/)。

编辑`%SHARDING_PROXY_HOME%\conf\server.yaml`。详情请参见[配置手册](https://shardingsphere.apache.org/document/legacy/4.x/document/cn/manual/sharding-proxy/configuration/)。

### 3.2.2 引入依赖

如果后端连接PostgreSQL数据库，不需要引入额外依赖。

如果后端连接MySQL数据库，需要下载[MySQL Connector/J](https://cdn.mysql.com//Downloads/Connector-J/mysql-connector-java-5.1.47.tar.gz)， 解压缩后，将`mysql-connector-java-5.1.47.jar`拷贝到`${sharding-proxy}\lib`目录。

### 3.2.3 启动服务

- 使用默认配置项：`${sharding-proxy}\bin\start.sh`
- 配置端口：`${sharding-proxy}\bin\start.sh ${port}`