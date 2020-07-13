# Apache ShardingSphere 简介

# 1 ShardingSphere简介

- 一套开源的分布式数据库中间件解决方案组成的生态圈。
- 有三个产品： JDBC、Proxy 和 Sidecar(TODO)，这 3 款相互独立，却又能够混合部署配合使用的产品组成。
    - 它们均提供标准化的数据分片、分布式事务和数据库治理功能，可适用于如 Java 同构、异构语言、云原生等各种多样化的应用场景。
- 定位为关系型数据库中间件，旨在充分合理地在分布式的场景下利用关系型数据库的计算和存储能
    力，而并非实现一个全新的关系型数据库。
- Apache ShardingSphere 5.x 版本开始致力于可插拔架构，项目的功能组件能够灵活的以可插拔的方式进行扩展。

![ShardingSphere Scope](https://zhishan-zh.github.io/media/shardingsphere-scope_cn.png)