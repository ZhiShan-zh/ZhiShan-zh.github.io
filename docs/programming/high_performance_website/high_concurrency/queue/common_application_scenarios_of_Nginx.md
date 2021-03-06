# 队列的常见应用场景

# 1 异步处理

通过异步处理，可以提升主流程相应速度，而非主流程/非重要处理可以集中处理，这样还可以将任务聚合批量处理。

- 用户注册成功后，需要发送注册成功邮件、新用户积分、优惠券等；
- 缓存过期时，先返回过期数据，然后异步更新缓存、异步写日志等。

可以使用消息队列/任务队列进行异步处理。

# 2 系统解偶

比如，用户成功支付完成订单后，要通知生产配货系统、发票系统、库存系统、推荐系统、搜索系统等进行业务处理，而未来需要支持那些业务是不知道的，并且这些业务不需要实时处理，不需要强一致，只需要保证最终一致性即可。

可以通过消息队列/任务队列进行系统解偶。

# 3 数据同步

比如，想把MySQL变更的数据同步到Redis，或者将MySQL的数据同步到Mongodb，或者让机房之间的数据同步，或者主从数据同步等，此时可以考虑使用databus、canal、otter等。

使用数据总线队列进行数据同步的好处是可以保证数据更改的有序性。

# 4 流量削峰

系统瓶颈一般在数据库上，比如扣减库存、下单等。此时可以考虑使用队列将变更请求暂时放入队列，通过缓存+队列暂存的方式将数据流量削峰。

同样，对于秒杀系统，下单服务会是该系统的瓶颈，此时，可以使用队列进行排队和限流，从而保护下单服务，通过队列暂存或者队列限流进行流量削峰。
