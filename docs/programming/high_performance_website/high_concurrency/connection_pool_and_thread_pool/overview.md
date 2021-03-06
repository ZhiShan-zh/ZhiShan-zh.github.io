# 连接池和线程池概述

在应用系统开发过程中，我们经常用到池化技术，如对象池、连接池、线程池等，通过池化来减少一些消耗，以提升性能。

**池化的目的就是通过复用技术提升性能**：

- **对象池**
  - 通过复用对象从而减少创建对象、垃圾回收的开销。
  - 池不能太大，太大影响GC时的扫描时间。
- **连接池**：如数据库连接池、Redis连接池、HTTP连接池
  - 通过服用TCP连接来减少创建和释放连接的时间来提升性能。
- **线程池**
  - 通过复用线程提升性能。

池化可以使用Apache commons-pool 2来实现，比如DBCP、Jedis连接池都是使用commons-pool 2实现的。不建议使用commons-pool 1.x版本。也可以写自己的连接池来使用特定的场景。