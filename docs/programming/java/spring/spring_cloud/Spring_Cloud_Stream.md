# Spring Cloud Stream

# 1 概述

## 1.1 引入

在实际的企业开发中，消息中间件是至关重要的组件之一。消息中间件主要解决应用解耦，异步消息，流量削锋等问题，实现高性能，高可用，可伸缩和最终一致性架构。不同的中间件其实现方式，内部结构是不一样的。如常见的RabbitMQ和Kafka，由于这两个消息中间件的架构上的不同，像RabbitMQ有exchange，kafka有Topic，partitions分区，这些中间件的差异性导致我们实际项目开发给我们造成了一定的困扰，我们如果用了两个消息队列的其中一种，后面的业务需求，我想往另外一种消息队列进行迁移，这时候无疑就是一个灾难性的，一大堆东西都要重新推倒重新做，因为它跟我们的系统耦合了，这时候 springcloud Stream 给我们提供了一种解耦合的方式。

## 1.2 Spring Cloud Stream介绍

Spring Cloud Stream由一个中间件中立的核组成。应用通过Spring Cloud Stream插入的

- **input**：相当于消费者consumer，它是从队列中接收消息的
- **output**：相当于生产者producer，它是从队列中发送消息的。

通道与外界交流。通道通过指定中间件的Binder实现与外部代理连接。业务开发者不再关注具体消息中间件，只需关注Binder对应用程序提供的抽象概念来使用消息中间件实现业务即可。

![spring_cloud_stream_20200615203911](https://zhishan-zh.github.io/media/spring_cloud_stream_20200615203911.png)

**说明**：最底层是消息服务中间件，中间层是绑定层，绑定层和底层的消息服务中间件进行绑定，顶层是消息生产者和消息消费者，顶层可以向绑定层生产消息和和获取消息消费。

## 1.3 核心概念

### 1.3.1 绑定器
Binder 绑定器是Spring Cloud Stream中一个非常重要的概念。在没有绑定器这个概念的情况下，我们的Spring Boot应用要直接与消息中间件进行信息交互的时候，由于各消息中间件构建的初衷不同，它们的实现细节上会有较大的差异性，这使得我们实现的消息交互逻辑就会非常笨重，因为对具体的中间件实现细节有太重的依赖，当中间件有较大的变动升级、或是更换中间件的时候，我们就需要付出非常大的代价来实施。

通过定义绑定器作为中间层，实现了应用程序与消息中间（Middleware）细节之间的隔离。通过向应用程序暴露统一的Channel通过，使得应用程序不需要再考虑各种不同的消息中间件的实现。当需要升级消息中间件，或者是更换其他消息中间件产品时，我们需要做的就是更换对应的Binder绑定器而不需要修改任何应用逻辑 。甚至可以任意的改变中间件的类型而不需要修改一行代码。

Spring Cloud Stream支持各种binder实现，下表包含GitHub项目的链接。

- [RabbitMQ](https://github.com/spring-cloud/spring-cloud-stream-binder-rabbit)
- [Apache Kafka](https://github.com/spring-cloud/spring-cloud-stream-binder-kafka)
- [Amazon Kinesis](https://github.com/spring-cloud/spring-cloud-stream-binder-aws-kinesis)
- [Google PubSub (partner maintained)](https://github.com/spring-cloud/spring-cloud-gcp/tree/master/spring-cloud-gcp-pubsub-stream-binder)
- [Solace PubSub+ (partner maintained)](https://github.com/SolaceProducts/spring-cloud-stream-binder-solace)
- [Azure Event Hubs (partner maintained)](https://github.com/Microsoft/spring-cloud-azure/tree/master/spring-cloud-azure-eventhub-stream-binder)

通过配置把应用和spring cloud stream 的 binder 绑定在一起，之后我们只需要修改 binder 的配置来达到动态修改topic、exchange、type等一系列信息而不需要修改一行代码。

### 1.3.2 发布/订阅模型

在Spring Cloud Stream中的消息通信方式遵循了发布-订阅模式，当一条消息被投递到消息中间件之后，它会通过共享的 Topic 主题进行广播，消息消费者在订阅的主题中收到它并触发自身的业务逻辑处理。这里所提到的 Topic 主题是Spring Cloud Stream中的一个抽象概念，用来代表发布共享消息给消费者的地方。在不同的消息中间件中， Topic 可能对应着不同的概念，比如：在RabbitMQ中的它对应了Exchange、而在Kakfa中则对应了Kafka中的Topic。

![spring_cloud_stream_20200615205129](https://zhishan-zh.github.io/media/spring_cloud_stream_20200615205129.png)

# 2 入门案例

这里使用rabbitMQ作为消息中间件，rabbitMQ中间件需要另外安装。

## 2.1 消息生产者

### 2.1.1 创建工程引入依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-stream-rabbit</artifactId>
</dependency>
```

### 2.1.2 定义bingding

发送消息时需要定义一个接口，不同的是接口方法的返回对象是 MessageChannel，下面是 Spring Cloud Stream 内置的接口：

```java
package org.springframework.cloud.stream.messaging;

import org.springframework.cloud.stream.annotation.Output;
import org.springframework.messaging.MessageChannel;

// Bindable interface with one output channel.
public interface Source {

	String OUTPUT = "output";

	@Output(Source.OUTPUT)
	MessageChannel output();
}
```

这就接口声明了一个 binding 命名为 “output”。这个binding 声明了一个消息输出流，也就是消息的生产者。

### 2.1.3 配置application.yml

```yaml
spring:
    cloud:
        stream:
            bindings:
                output:
                    destination: test-default
                    contentType: text/plain
```

配置说明：

- contentType：用于指定消息的类型。
- destination：指定了消息发送的目的地，对应 RabbitMQ，会发送到 exchange 是 test-default 的所有消息队列中。

### 2.1.4 测试发送消息

```java
@SpringBootApplication
@EnableBinding(Source.class)
public class Application implements CommandLineRunner {
    @Autowired
    @Qualifier("output")
    MessageChannel output;
    
    @Override
    public void run(String... strings) throws Exception {
        //发送MQ消息
        output.send(MessageBuilder.withPayload("hello world").build());
    }
    
    public static void main(String[] args) {
    	SpringApplication.run(Application.class);
    }
}
```

## 2.2 消息消费者

### 2.2.1 创建工程引入依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-stream-rabbit</artifactId>
</dependency
```

### 2.2.2 定义bingding

同发送消息一致，在Spring Cloud Stream中接受消息，需要定义一个接口，如下是内置的一个接口。

```java
package org.springframework.cloud.stream.messaging;

import org.springframework.cloud.stream.annotation.Input;
import org.springframework.messaging.SubscribableChannel;

// Bindable interface with one input channel.
public interface Sink {

	String INPUT = "input";

	@Input(Sink.INPUT)
	SubscribableChannel input();
}
```

注释` @Input` 对应的方法，需要返回 SubscribableChannel ，并且参入一个参数值。
这就接口声明了一个 binding 命名为 “input” 。

### 2.2.3 配置application.yml

```yaml
spring:
    cloud:
        stream:
            bindings:
                input:
                	destination: test-default
```

配置说明：

- destination：指定了消息获取的目的地，对应于MQ就是 exchange，这里的exchange就是test-default

### 2.2.4 测试

1. 定义一个 class （这里直接在启动类），并且添加注解`@EnableBinding(Sink.class)` ，其中Sink 就是上述的接口。同时定义一个方法（此处是 input）标明注解为`@StreamListener(Processor.INPUT)`，方法参数为 Message 。
    - `@EnableBinding`注释将一个或多个接口作为参数（在本例中，参数是单个`Sink`接口）。接口声明输入和输出通道。
2. 启动后，默认是会创建一个临时队列，临时队列绑定的exchange为 “test-default”，routing key为 “#”。
3. 所有发送 exchange 为“test-default ” 的MQ消息都会被投递到这个临时队列，并且触发下述述的方法。

```java
@SpringBootApplication
@EnableBinding(Sink.class)
public class Application {
    
    // 监听 binding 为 Sink.INPUT 的消息
    @StreamListener(Sink.INPUT)
    public void input(Message<String> message) {
    	System.out.println("监听收到：" + message.getPayload());
    }
    
    public static void main(String[] args) {
    	SpringApplication.run(Application.class);
    }
}
```

# 3 自定义消息通道

Spring Cloud Stream 内置了两种接口，分别定义了 binding 为 “input” 的输入流，和 “output” 的输出流，而在我们实际使用中，往往是需要定义各种输入输出流。自定义输入输出流很简单：

1. 定义一个接口，接口中可以定义无数个输入输出流，可以根据实际业务情况划分。比如下面的接口，定义了一个订单输入，和订单输出两个 binding。

```java
interface OrderProcessor {
    String INPUT_ORDER = "inputOrder";
    String OUTPUT_ORDER = "outputOrder";
    
    @Input(INPUT_ORDER)
    SubscribableChannel inputOrder();
    
    @Output(OUTPUT_ORDER)
    MessageChannel outputOrder();
}
```

2. 使用时，需要在`@EnableBinding`注解中，添加自定义的接口。

    - `@EnableBinding`注释将一个或多个接口作为参数。接口声明输入和输出通道。Spring Cloud Stream提供`Source`，`Sink`和`Processor`接口。还可以自定义的接口。

3. 使用`@StreamListener`做监听的时候，需要指定参数为`OrderProcessor.INPUT_ORDER`。

4. 配置文件中配置

    ```yaml
    spring:
        cloud:
            stream:
                defaultBinder: defaultRabbit
                bindings:
                    inputOrder:
                        destination: mqTestOrder
                    outputOrder:
                        destination: mqTestOrder
    ```

    如上配置，指定了 destination 为 mqTestOrder 的输入输出流

# 4 消息分组

通常在生产环境，我们的每个服务都不会以单节点的方式运行在生产环境，当同一个服务启动多个实例的时候，这些实例都会绑定到同一个消息通道的目标主题（Topic）上。默认情况下，当生产者发出一条消息到绑定通道上，这条消息会产生多个副本被每个消费者实例接收和处理，但是有些业务场景之下，我们希望生产者产生的消息只被其中一个实例消费，这个时候我们需要为这些消费者设置消费组来实现这样的功能。

![SCSt groups](https://zhishan-zh.github.io/media/spring_cloud_stream_SCSt-groups.png)

实现的方式非常简单，我们只需要在服务消费者端设置
`spring.cloud.stream.bindings.input.group` 属性即可，比如：

```yaml
server:
	port: 7003 #服务端口
spring:
    application:
    	name: rabbitmq-consumer #指定服务名
    rabbitmq:
        addresses: 127.0.0.1
        username: root
        password: root
        virtual-host: myhost
    cloud:
        stream:
            bindings:
                input:
                	destination: test-default
                inputOrder:
                    destination: testChannel
                    group: group-1
            binders:
                defaultRabbit:
                type: rabbit
```

在同一个group中的多个消费者只有一个可以获取到消息并消费。

# 5 消息分区

有一些场景需要满足，同一个特征的数据被同一个实例消费，比如同一个id的传感器监测数据必须被同一个实例统计计算分析，否则可能无法获取全部的数据。又比如部分异步任务，首次请求启动task，二次请求取消task，此场景就必须保证两次请求至同一实例。

![SCSt-partitioning](https://zhishan-zh.github.io/media/spring_cloud_stream_SCSt-partitioning.png)

消息消费者配置：

```yaml
spring:
    cloud:
        stream:
            instance-count: 2
            instance-index: 0
            bindings:
                input:
                    destination: test-default
                inputOrder:
                    destination: testChannel
                    group: group-1
                consumer:
                    partitioned: true
            binders:
                defaultRabbit:
                    type: rabbit
```

**配置说明**：

- `spring.cloud.stream.bindings.input.consumer.partitioned` ：通过该参数开启消费者分区功能；
- `spring.cloud.stream.instance-count `：该参数指定了当前消费者的总实例数量；
- `spring.cloud.stream.instance-index` ：该参数设置当前实例的索引号，从0开始，最大值为`spring.cloud.stream.instance-count` 的值 - 1。我们试验的时候需要启动多个实例，可以通过运行参数来为不同实例设置不同的索引值。

消息生产者配置：

```yaml
spring:
    application:
    	name: rabbitmq-producer #指定服务名
    rabbitmq:
        addresses: 127.0.0.1
        username: root
        password: root
        virtual-host: myhost
    cloud:
        stream:
            bindings:
                input:
                	destination: test-default
                outputOrder:
                	destination: testChannel
                    producer:
                        partition-key-expression: payload
                        partition-count: 2
            binders:
                defaultRabbit:
                	type: rabbit
```

配置说明：

- `spring.cloud.stream.bindings.output.producer.partition-key-expression` ：通过该参数指定了分区键的表达式规则，我们可以根据实际的输出消息规则来配置SpEL来生成合适的分区键；

- `spring.cloud.stream.bindings.output.producer.partition-count` ：该参数指定了消息分区的数量。

到这里消息分区配置就完成了，我们可以再次启动这两个应用，同时消费者启动多个，但需要注意的是要为消费者指定不同的实例索引号，这样当同一个消息被发给消费组时，我们可以发现只有一个消费实例在接收和处理这些相同的消息。