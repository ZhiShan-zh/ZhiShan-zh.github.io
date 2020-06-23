# URL去重接口DuplicateRemover

# 1 概述

在0.5.1版本里，WebMagic对Scheduler的内部实现进行了重构，去重部分被单独抽象成了一个接口：`DuplicateRemover`，从而可以为同一个Scheduler选择不同的去重方式，以适应不同的需要。

# 2 WebMagic内置的DuplicateRemover

| 类                          | 说明                                                      |
| --------------------------- | --------------------------------------------------------- |
| HashSetDuplicateRemover     | 使用HashSet来进行去重，占用内存较大对待                   |
| BloomFilterDuplicateRemover | 使用BloomFilter来进行去重，占用内存较小，但是可能漏抓页面 |

所有默认的Scheduler都使用HashSetDuplicateRemover来进行去重，（除开RedisScheduler是使用Redis的set进行去重）。如果你的URL较多，使用HashSetDuplicateRemover会比较占用内存，所以也可以尝试以下BloomFilterDuplicateRemover，使用方式：

```java
spider.setScheduler(new QueueScheduler()
.setDuplicateRemover(new BloomFilterDuplicateRemover(10000000)) //10000000是估计的页面数量
)
```

注意：0.6.0版本后，如果使用BloomFilterDuplicateRemover，需要单独引入Guava依赖包。