# 使用和定制Scheduler

# 1 概述

Scheduler是WebMagic中进行URL管理的组件。

一般来说，Scheduler包括两个作用：

1. 对待抓取的URL队列进行管理。
2. 对已抓取的URL进行去重。

在0.5.1版本里，WebMagic对Scheduler的内部实现进行了重构，去重部分被单独抽象成了一个接口：`DuplicateRemover`，从而可以为同一个Scheduler选择不同的去重方式，以适应不同的需要。

# 2 WebMagic内置的Scheduler

## 2.1 简述

| 类                        | 说明                                                         | 备注                                                         |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| DuplicateRemovedScheduler | 抽象基类，提供一些模板方法                                   | 继承它可以实现自己的功能                                     |
| QueueScheduler            | 使用内存队列保存待抓取URL                                    |                                                              |
| PriorityScheduler         | 使用带有优先级的内存队列保存待抓取URL                        | 耗费内存较QueueScheduler更大，但是当设置了request.priority之后，只能使用PriorityScheduler才可使优先级生效 |
| FileCacheQueueScheduler   | 使用文件保存抓取URL，可以在关闭程序并下次启动时，从之前抓取到的URL继续抓取 | 需指定路径，会建立.urls.txt和.cursor.txt两个文件             |
| RedisScheduler            | 使用Redis保存抓取队列，可进行多台机器同时合作抓取            | 需要安装并启动redis                                          |

## 2.2 简单使用

**内存队列QueueScheduler**：

```java
spider.setScheduler(new QueueScheduler())；
```

**文件队列FileCacheQueueScheduler**：

使用文件保存抓取URL，可以在关闭程序并下次启动时，从之前抓取到的URL继续抓取。

```java
spider.setScheduler(new FileCacheQueueScheduler("E:\\scheduler"))//设置文件队列
```

运行后文件夹`E:\scheduler`会产生两个文件`xxx.urls.txt`和`xxx.cursor.txt`，这里的xxx是爬取网站的域名。

**Redis队列RedisScheduler**：

使用Redis保存抓取队列，可进行多台机器同时合作抓取，运行之前需要先运行redis服务端。

```java
spider.setScheduler(new RedisScheduler("127.0.0.1"))//设置Redis队列
```

