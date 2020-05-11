# RabbitMQ入门

# 1 概述


## 1.1 简介

<br />MQ全称为Message Queue，即消息队列，RabbitMQ是由erlang语言开发，基于AMQP（Advanced Message Queuing Protocol 高级消息队列协议）协议实现的消息队列，它是一种应用程序之间的通信方法，消息队列在分布式系统开发中应用非常广泛。RabbitMQ官方地址：[http://www.rabbitmq.com/](http://www.rabbitmq.com/)<br />
<br />其他消息队列：ActiveMQ，RabbitMQ，ZeroMQ，Kafka，MetaMQ，RocketMQ、Redis<br />

## 1.2 消息队列常应用场景


### 1.2.1 任务异步处理

<br />将不需要同步处理的并且耗时长的操作由消息队列通知消息接收方进行异步处理。提高了应用程序的响应时间。<br />

### 1.2.2 系统解耦合

<br />MQ相当于一个中介，生产方通过MQ与消费方交互，它将应用程序进行解耦合。<br />

## 1.3 为什么使用RabbitMQ


1. 使得简单，功能强大。
2. 基于AMQP协议。
3. 社区活跃，文档完善。
4. 高并发性能好，这主要得益于Erlang语言。
5. Spring Boot默认已集成RabbitMQ



## 1.4 AMQP

<br />AMQP，即Advanced Message Queuing Protocol，一个提供统一消息服务的应用层标准高级消息队列协议，是应用层协议的一个开放标准，为面向消息的中间件设计。基于此协议的客户端与消息中间件可传递消息，并不受客户端/中间件不同产品，不同的开发语言等条件的限制。Erlang中的实现有RabbitMQ等。<br />

## 1.5 JMS

<br />JMS即Java消息服务（Java Message Service）应用程序接口，是一个Java平台中关于面向消息中间件（MOM）的API，用于在两个应用程序之间，或分布式系统中发送消息，进行异步通信。Java消息服务是一个与具体平台无关的API，绝大多数MOM提供商都对JMS提供支持。<br />

## 1.6 RabbitMQ的工作原理

<br />![](https://zhishan-zh.github.io/media/image-rabbitmq-20200508153335374.png#align=left&display=inline&margin=%5Bobject%20Object%5D&originHeight=312&originWidth=994&status=done&style=none)<br />
**组成部分说明**：<br />

- Broker：消息队列服务进程，此进程包括两个部分：Exchange和Queue。
  - Exchange：消息队列交换机，按一定的规则将消息路由转发到某个队列，对消息进行过虑。
  - Queue：消息队列，存储消息的队列，消息到达队列并转发给指定的消费方。
- Producer：消息生产者，即生产方客户端，生产方客户端将消息发送到MQ。
- Consumer：消息消费者，即消费方客户端，接收MQ转发的消息。


<br />**消息发布流程：**<br />

1. 生产者和Broker建立TCP连接。
2. 生产者和Broker建立通道。
3. 生产者通过通道消息发送给Broker，由Exchange将消息进行转发。
4. Exchange将消息转发到指定的Queue（队列）


<br />**消息接收流程：**<br />

1. 消费者和Broker建立TCP连接
2. 消费者和Broker建立通道
3. 消费者监听指定的Queue（队列）
4. 当有消息到达Queue时Broker默认将消息推送给消费者。
5. 消费者接收到消息。



# 2 RabbitMQ安装（待完成）


# 3 入门案例（待完成）
