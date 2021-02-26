# Tomcat架构

# 1 Http工作原理


HTTP协议是浏览器与服务器之间的数据传送协议。作为应用层协议，HTTP是基于TCP/IP协议来传递数据的（HTML文件、图片、查询结果等），HTTP协议不涉及数据包（Packet）传输，主要规定了客户端和服务器之间的通信格式。


![image-20200416133718278.png](./media/1587091946300-dcdca249-9b1d-4faf-9d69-6edfae335474.png)


从图上你可以看到，这个过程是：


1. 用户通过浏览器进行了一个操作，比如输入网址并回车，或者是点击链接，接着浏览器获取了这个事件。
2. 浏览器向服务端发出TCP连接请求。
3. 服务程序接受浏览器的连接请求，并经过TCP三次握手建立连接。
4. 浏览器将请求数据打包成一个HTTP协议格式的数据包。
5. 浏览器将该数据包推入网络，数据包经过网络传输，最终达到端服务程序。
6. 服务端程序拿到这个数据包后，同样以HTTP协议格式解包，获取到客户端的意图。
7. 得知客户端意图后进行处理，比如提供静态文件或者调用服务端程序获得动态结果。
8. 服务器将响应结果（可能是HTML或者图片等）按照HTTP协议格式打包。
9. 服务器将响应数据包推入网络，数据包经过网络传输最终达到到浏览器。
10. 浏览器拿到数据包后，以HTTP协议的格式解包，然后解析数据，假设这里的数据是HTML。
11. 浏览器将HTML文件展示在页面上。



那我们想要探究的Tomcat作为一个HTTP服务器，在这个过程中都做了些什么事情呢？主要是接受连接、解析请求数据、处理请求和发送响应这几个步骤。


# 2 Tomcat整体架构


## 2.1 Http服务器请求处理


浏览器发给服务端的是一个HTTP格式的请求，HTTP服务器收到这个请求后，需要调用服务端程序来处理，所谓的服务端程序就是你写的Java类，一般来说不同的请求需要由不同的Java类来处理。


![image-20200416140824967.png](./media/1587091965762-6d2551a9-0b9d-4781-ba00-2f2a3da6b670.png)


图-1 ， 表示HTTP服务器直接调用具体业务类，它们是紧耦合的。


图-2，HTTP服务器不直接调用业务类，而是把请求交给容器来处理，容器通过Servlet接口调用业务类。因此Servlet接口和Servlet容器的出现，达到了HTTP服务器与业务类解耦的目的。而Servlet接口和Servlet容器这一整套规范叫作Servlet规范。Tomcat按照Servlet规范的要求实现了Servlet容器，同时它们也具有HTTP服务器的功能。作为Java程序员，如果我们要实现新的业务功能，只需要实现一个Servlet，并把它注册到Tomcat（Servlet容器）中，剩下的事情就由Tomcat帮我们处理了。


## 2.2 Servlet容器工作流程


为了解耦，HTTP服务器不直接调用Servlet，而是把请求交给Servlet容器来处理，那Servlet容器又是怎么工作的呢？

当客户请求某个资源时，HTTP服务器会用一个ServletRequest对象把客户的请求信息封装起来，然后调用Servlet容器的service方法，Servlet容器拿到请求后，根据请求的URL和Servlet的映射关系，找到相应的Servlet，如果Servlet还没有被加载，就用反射机制创建这个Servlet，并调用Servlet的init方法来完成初始化，接着调用Servlet的service方法来处理请求，把ServletResponse对象返回给HTTP服务器，HTTP服务器会把响应发送给客户端。


![image-20200416141341006.png](./media/1587091985106-dca1d03f-7896-424b-85d0-a4d722cacceb.png)

## 2.3 Tomcat整体架构


我们知道如果要设计一个系统，首先是要了解需求，我们已经了解了Tomcat要实现两个核心功能：


1. 处理Socket连接，负责网络字节流与Request和Response对象的转化。
1. 加载和管理Servlet，以及具体处理Request请求。



因此Tomcat设计了两个核心组建连接器（Connector）和容器（Container）来分别做这两件事情。连接器负责对外交流，容器负责内部处理。


![image-20200416141929506.png](./media/1587092003169-947484a8-7d3d-45ec-8d7d-3b30de315745.png)

# 3 连接器 - Coyote

## 3.1 架构介绍


Coyote 是Tomcat的连接器框架的名称 , 是Tomcat服务器提供的供客户端访问的外部接口。客户端通过Coyote与服务器建立连接、发送请求并接受响应 。


Coyote 封装了底层的网络通信（Socket 请求及响应处理），为Catalina 容器提供了统一的接口，使Catalina 容器与具体的请求协议及IO操作方式完全解耦。Coyote 将Socket 输入转换封装为 Request 对象，交由Catalina 容器进行处理，处理请求完成后, Catalina 通过Coyote 提供的Response 对象将结果写入输出流 。


Coyote 作为独立的模块，只负责具体协议和IO的相关操作， 与Servlet 规范实现没有直接关系，因此即便是 Request 和 Response 对象也并未实现Servlet规范对应的接口， 而是在Catalina 中将他们进一步封装为ServletRequest 和 ServletResponse 。


![image-20200416143052457.png](./media/1587092021278-83140f4c-1d19-4c71-b50c-2af92fe48bab.png)


## 3.2 IO模型与协议


在Coyote中，Tomcat支持的多种I/O模型和应用层协议。

**Tomcat 支持的IO模型（自8.5/9.0 版本起，Tomcat 移除了 对 BIO 的支持）**：

| IO模型 | 描述 |
| --- | --- |
| NIO | 非阻塞I/O，采用Java NIO类库实现。 |
| NIO2 | 异步I/O，采用JDK 7最新的NIO2类库实现。 |
| APR | 采用Apache可移植运行库实现，是C/C++编写的本地库。如果选择该方案，需要单独安装APR库。 |

**Tomcat 支持的应用层协议** ：

| 应用层协议 | 描述 |
| --- | --- |
| HTTP/1.1 | 这是大部分Web应用采用的访问协议。 |
| A JP | 用于和Web服务器集成（如Apache），以实现对静态资源的优化以及集群部署，当前支持A JP/1.3。 |
| HTTP/2 | HTTP 2.0大幅度的提升了Web性能。下一代HTTP协议 ， 自8.5以及9.0版本之后支持。 |

**协议分层** ：


![image-20200416144013627.png](./media/1587092039392-841cdfd1-b508-488e-9e21-6a1c4ff71f64.png)


在 8.0 之前 ， Tomcat 默认采用的I/O方式为 BIO ， 之后改为 NIO。 无论 NIO、NIO2 还是 APR， 在性能方面均优于以往的BIO。 如果采用APR， 甚至可以达到 Apache HTTP Server 的影响性能。

Tomcat为了实现支持多种I/O模型和应用层协议，一个容器可能对接多个连接器，就好比一个房间有多个门。但是单独的连接器或者容器都不能对外提供服务，需要把它们组装起来才能工作，组装后这个整体叫作Service组件。这里请你注意，Service本身没有做什么重要的事情，只是在连接器和容器外面多包了一层，把它们组装在一起。Tomcat内可能有多个Service，这样的设计也是出于灵活性的考虑。通过在Tomcat中配置多个Service，可以实现通过不同的端口号来访问同一台机器上部署的不同应用。


## 3.3 连接器组件


![image-20200416144223872.png](./media/1587092056570-0d3ec503-4ab1-4aa1-9a55-1f7af72b3021.png)


- **EndPoint**
  - EndPoint ： Coyote 通信端点，即通信监听的接口，是具体Socket接收和发送处理器，是对传输层的抽象，因此EndPoint用来实现TCP/IP协议的。
  - Tomcat 并没有EndPoint 接口，而是提供了一个抽象类AbstractEndpoint ， 里面定义了两个内部类：Acceptor和SocketProcessor。Acceptor用于监听Socket连接请求。SocketProcessor用于处理接收到的Socket请求，它实现Runnable接口，在Run方法里调用协议处理组件Processor进行处理。为了提高处理能力，SocketProcessor被提交到线程池来执行。而这个线程池叫作执行器（Executor)，我在后面的专栏会详细介绍Tomcat如何扩展原生的Java线程池。
- **Processor**
  - Coyote 协议处理接口 ，如果说EndPoint是用来实现TCP/IP协议的，那么Processor用来实现HTTP协议，Processor接收来自EndPoint的Socket，读取字节流解析成Tomcat Request和Response对象，并通过Adapter将其提交到容器处理，Processor是对应用层协议的抽象。
- **ProtocolHandler**
  - Coyote 协议接口， 通过Endpoint 和 Processor ， 实现针对具体协议的处理能力。Tomcat 按照协议和I/O 提供了6个实现类 ： AjpNioProtocol ， AjpAprProtocol，AjpNio2Protocol ， Http11NioProtocol ，Http11Nio2Protocol ，Http11AprProtocol。我们在配置`tomcat/conf/server.xml`时 ， 至少要指定具体的ProtocolHandler , 当然也可以指定协议名称 ， 如 ：HTTP/1.1 ，如果安装了APR，那么将使用Http11AprProtocol ， 否则使用 Http11NioProtocol 。

- **Adapter**
  - 由于协议不同，客户端发过来的请求信息也不尽相同，Tomcat定义了自己的Request类来“存放”这些请求信息。ProtocolHandler接口负责解析请求并生成Tomcat Request类。但是这个Request对象不是标准的ServletRequest，也就意味着，不能用Tomcat Request作为参数来调用容器。Tomcat设计者的解决方案是引入CoyoteAdapter，这是适配器模式的经典运用，连接器调用CoyoteAdapter的Sevice方法，传入的是Tomcat Request对象，CoyoteAdapter负责将Tomcat Request转成ServletRequest，再调用容器的Service方法。

# 4 容器 - Catalina


Tomcat是一个由一系列可配置的组件构成的Web容器，而Catalina是Tomcat的servlet容器。


Catalina是Servlet容器实现，包含了之前说到的所有容器组件，以及后边会涉及到的安全、会话、管理等Servlet容器架构的各个方面，它通过松耦合的方式集成Coyote，以完成按照请求协议进行数据读写。同时，它还包括我们的启动入口、Shell程序等。

## 4.1 Catalina 地位


Tomcat 的模块分层结构图， 如下：


![image-20200416145518562.png](./media/1587092076276-999689dd-f928-45fa-b790-872364096596.png)


Tomcat 本质上就是一款 Servlet 容器， 因此Catalina 才是 Tomcat 的核心 ， 其他模块都是为Catalina提供支撑的。 比如 ： 通过Coyote 模块提供链接通信，Jasper 模块提供JSP引擎，Naming 提供JNDI 服务，Juli 提供日志服务。


## 4.2 Catalina 结构


Catalina 的主要组件结构如下：


![image-20200416145804262.png](./media/1587092089607-0149f0c4-a9ce-4825-aebc-3b355f548ca2.png)


如上图所示，Catalina负责管理Server，而Server表示着整个服务器。Server下面有多个服务Service，每个服务都包含着多个连接器组件Connector（Coyote 实现）和一个容器组件Container。在Tomcat启动的时候， 会初始化一个Catalina的实例。


Catalina 各个组件的职责：

| 组件      | 职责                                                         |
| --------- | ------------------------------------------------------------ |
| Catalina  | 负责解析Tomcat的配置文件 , 以此来创建服务器Server组件，并根据命令来对其进行管理 |
| Server    | 服务器表示整个Catalina Servlet容器以及其它组件，负责组装并启动Servlet引擎,Tomcat连接器。Server通过实现Lifecycle接口，提供了一种优雅的启动和关闭整个系统的方式 |
| Service   | 服务是Server内部的组件，一个Server包含多个Service。它将若干个Connector组件绑定到一个Container（Engine）上 |
| Connector | 连接器，处理与客户端的通信，它负责接收客户请求，然后转给相关的容器处理，最后向客户返回响应结果；<br/>Connector和Context是多对多的关系，因为一个应用Context可能不止一个连接，比如，HTTP连接和HTTPS连接。 |
| Container | 容器，负责处理用户的servlet请求，并返回对象给web用户的模块   |

## 4.3 Container 结构


Tomcat设计了4种容器，分别是Engine、Host、Context和Wrapper。这4种容器不是平行关系，而是父子关系。， Tomcat通过一种分层的架构，使得Servlet容器具有很好的灵活性。


![image-20200416150315998.png](./media/1587092113410-176f2630-2487-4255-86f7-74fd359ad984.png)


各个组件的含义 ：

| 容器    | 描述                                                         |
| ------- | ------------------------------------------------------------ |
| Engine  | 表示整个Catalina的Servlet引擎，用来管理多个虚拟站点，一个Service最多只能有一个Engine，但是一个引擎可包含多个Host |
| Host    | 代表一个虚拟主机，或者说一个站点，可以给Tomcat配置多个虚拟主机地址，而一个虚拟主机下可包含多个Context |
| Context | 表示一个Web应用程序， 一个Web应用可包含多个Wrapper。<br/>Connector和Context是多对多的关系，因为一个应用Context可能不止一个连接，比如，HTTP连接和HTTPS连接。 |
| Wrapper | 表示一个Servlet，Wrapper 作为容器中的最底层，不能包含子容器  |

我们也可以再通过Tomcat的`server.xml`配置文件来加深对Tomcat容器的理解。Tomcat采用了组件化的设计，它的构成组件都是可配置的，其中最外层的是Server，其他组件按照一定的格式要求配置在这个顶层容器中。


```xml
<Server>
	<Service>
    	<Connector/>
        <Connector/>
    	<Connector/>
        <Engine>
        	<Host>
            	<Context></Context>
                <Context></Context>
            </Host>
            <Host>
            	<Context></Context>
                <Context></Context>
            </Host>
        </Engine>
    </Service>
</Server>
```


那么，Tomcat是怎么管理这些容器的呢？你会发现这些容器具有父子关系，形成一个树形结构，你可能马上就想到了设计模式中的组合模式。没错，Tomcat就是用组合模式来管理这些容器的。具体实现方法是，所有容器组件都实现了Container接口，因此组合模式可以使得用户对单容器对象和组合容器对象的使用具有一致性。这里单容器对象指的是最底层的Wrapper，组合容器对象指的是上面的Context、Host或者Engine。


![image-20200416153659245.png](./media/1587092134602-25468397-7266-413f-bf56-443ac1615668.png)


Container 接口中提供了以下方法（截图中知识一部分方法） ：


![image-20200416154014018.png](./media/1587092145841-49a615a4-e6a6-45de-8a4d-96c8cbfaf6c8.png)


在上面的接口看到了getParent、SetParent、addChild和removeChild等方法。


Container接口扩展了LifeCycle接口，LifeCycle接口用来统一管理各组件的生命周期。


# 5 Tomcat 启动流程


## 5.1 流程


![image-20200416154941031.png](./media/1587092165213-bf378569-2755-465b-8754-258a5b23e7f5.png)


步骤 :


1. 启动tomcat ， 需要调用 `bin/startup.bat` (在linux 目录下 , 需要调用 `bin/startup.sh`) ， 在`startup.bat` 脚本中, 调用了`catalina.bat`。
2. 在`catalina.bat` 脚本文件中，调用了BootStrap 中的main方法。
3. 在BootStrap 的main 方法中调用了 init 方法 ， 来创建Catalina 及 初始化类加载器。
4. 在BootStrap 的main 方法中调用了 load 方法 ， 在其中又调用了Catalina的load方法。
5. 在Catalina 的load 方法中 , 需要进行一些初始化的工作, 并需要构造Digester 对象, 用于解析 XML。
6. 然后在调用后续组件的初始化操作 ......



加载Tomcat的配置文件，初始化容器组件 ，监听对应的端口号， 准备接受客户端请求 。


## 5.2 源码解析


### 5.2.1 Lifecycle


由于所有的组件均存在初始化、启动、停止等生命周期方法，拥有生命周期管理的特性， 所以Tomcat在设计的时候， 基于生命周期管理抽象成了一个接口 Lifecycle ，而组件 Server、Service、Container、Executor、Connector 组件 ， 都实现了一个生命周期的接口，从而具有了以下生命周期中的核心方法：


1. init（）：初始化组件
2. start（）：启动组件
3. stop（）：停止组件
4. destroy（）：销毁组件



![image-20200416160110210.png](./media/1587092185532-b87364b6-2104-43af-8735-16b7008cbc86.png)


### 5.2.2 各组件的默认实现


上面我们提到的Server、Service、Engine、Host、Context都是接口， 下图中罗列了这些接口的默认实现类。当前对于 Endpoint组件来说，在Tomcat中没有对应的Endpoint接口， 但是有一个抽象类AbstractEndpoint ，其下有三个实现类： NioEndpoint、Nio2Endpoint、AprEndpoint ， 这三个实现类，分别对应于前面讲解链接器 Coyote 时， 提到的链接器支持的三种IO模型：NIO，NIO2，APR ，Tomcat8.5版本中，默认采用的是 NioEndpoint。


![image-20200416160325863.png](./media/1587092212336-3d560d2e-1b7b-4c8e-96a2-02d67bb56b35.png)


ProtocolHandler ： Coyote协议接口，通过封装Endpoint和Processor ， 实现针对具体协议的处理功能。Tomcat按照协议和IO提供了6个实现类。

**AJP协议**：


1. AjpNioProtocol ：采用NIO的IO模型。
2. AjpNio2Protocol：采用NIO2的IO模型。
3. AjpAprProtocol ：采用APR的IO模型，需要依赖于APR库。

**HTTP协议**：


1. Http11NioProtocol ：采用NIO的IO模型，默认使用的协议（如果服务器没有安装APR）。
2. Http11Nio2Protocol：采用NIO2的IO模型。
3. Http11AprProtocol ：采用APR的IO模型，需要依赖于APR库。



![image-20200416160728099.png](./media/1587092280687-1ea3237d-4e75-4c21-866e-2363daa51555.png)


## 5.3 源码跟踪


MainClass：`org.apache.catalina.startup.Bootstrap`


### 5.3.1 Bootstrap中的入口函数


```java
/**
  * Main method and entry point when starting Tomcat via the provided
  * scripts.
  *
  * @param args Command line arguments to be processed
  */
public static void main(String args[]) {

    if (daemon == null) {
        // Don't set daemon until init() has completed
        Bootstrap bootstrap = new Bootstrap();//初始化Bootstrap
        try {
            bootstrap.init();//调用Bootstrap中的init方法
        } catch (Throwable t) {
            handleThrowable(t);
            t.printStackTrace();
            return;
        }
        daemon = bootstrap;
    } else {
        // When running as a service the call to stop will be on a new
        // thread so make sure the correct class loader is used to prevent
        // a range of class not found exceptions.
        Thread.currentThread().setContextClassLoader(daemon.catalinaLoader);
    }

    try {
        String command = "start";
        if (args.length > 0) {
            command = args[args.length - 1];
        }

        if (command.equals("startd")) {
            args[args.length - 1] = "start";
            daemon.load(args);
            daemon.start();
        } else if (command.equals("stopd")) {
            args[args.length - 1] = "stop";
            daemon.stop();
        } else if (command.equals("start")) {
            daemon.setAwait(true);//daemon就是bootstrap
            daemon.load(args);//调用bootstrap的load方法
            daemon.start();//调用bootstrap的start方法
            if (null == daemon.getServer()) {
                System.exit(1);
            }
        } else if (command.equals("stop")) {
            daemon.stopServer(args);
        } else if (command.equals("configtest")) {
            daemon.load(args);
            if (null == daemon.getServer()) {
                System.exit(1);
            }
            System.exit(0);
        } else {
            log.warn("Bootstrap: command \"" + command + "\" does not exist.");
        }
    } catch (Throwable t) {
        // Unwrap the Exception for clearer error reporting
        if (t instanceof InvocationTargetException &&
            t.getCause() != null) {
            t = t.getCause();
        }
        handleThrowable(t);
        t.printStackTrace();
        System.exit(1);
    }

}
```


### 5.3.2 Bootstrap中的init方法


init方法主要作用就是通过反射创建了`org.apache.catalina.startup.Catalina`对象


```java
/**
 * Initialize daemon.
 * @throws Exception Fatal initialization error
 */
public void init() throws Exception {

    initClassLoaders();//初始化类加载器

    Thread.currentThread().setContextClassLoader(catalinaLoader);

    SecurityClassLoad.securityClassLoad(catalinaLoader);

    // Load our startup class and call its process() method
    if (log.isDebugEnabled())
        log.debug("Loading startup class");
    Class<?> startupClass = catalinaLoader.loadClass("org.apache.catalina.startup.Catalina");
    Object startupInstance = startupClass.getConstructor().newInstance();//通过反射的方式Catalina对象

    // Set the shared extensions class loader
    if (log.isDebugEnabled())
        log.debug("Setting startup class properties");
    String methodName = "setParentClassLoader";
    Class<?> paramTypes[] = new Class[1];
    paramTypes[0] = Class.forName("java.lang.ClassLoader");
    Object paramValues[] = new Object[1];
    paramValues[0] = sharedLoader;
    Method method =
        startupInstance.getClass().getMethod(methodName, paramTypes);
    method.invoke(startupInstance, paramValues);

    catalinaDaemon = startupInstance;//private Object catalinaDaemon

}
```


### 5.3.3 Bootstrap中的load方法


```java
/**
 * Load daemon.
 */
private void load(String[] arguments)
    throws Exception {

    // Call the load() method
    String methodName = "load";
    Object param[];
    Class<?> paramTypes[];
    if (arguments==null || arguments.length==0) {
        paramTypes = null;
        param = null;
    } else {
        paramTypes = new Class[1];
        paramTypes[0] = arguments.getClass();
        param = new Object[1];
        param[0] = arguments;
    }
    Method method =
        catalinaDaemon.getClass().getMethod(methodName, paramTypes);
    if (log.isDebugEnabled())
        log.debug("Calling startup class " + method);
    method.invoke(catalinaDaemon, param);//通过反射方式调用catalina的load方法

}
```


### 5.3.4 catalina中的load方法


```java
/*
 * Load using arguments
 */
public void load(String args[]) {

    try {
        if (arguments(args)) {
            load();
        }
    } catch (Exception e) {
        e.printStackTrace(System.out);
    }
}
```


```java
/**
 * Start a new server instance.
 */
public void load() {

    if (loaded) {
        return;
    }
    loaded = true;

    long t1 = System.nanoTime();

    initDirs();

    // Before digester - it may be needed
    initNaming();

    // Create and execute our Digester
    Digester digester = createStartDigester();//Digester是Tomcat的XML文件（server.xml）解析工具

    InputSource inputSource = null;
    InputStream inputStream = null;
    File file = null;
    try {
        try {
            file = configFile();
            inputStream = new FileInputStream(file);
            inputSource = new InputSource(file.toURI().toURL().toString());
        } catch (Exception e) {
            if (log.isDebugEnabled()) {
                log.debug(sm.getString("catalina.configFail", file), e);
            }
        }
        if (inputStream == null) {
            try {
                inputStream = getClass().getClassLoader()
                    .getResourceAsStream(getConfigFile());
                inputSource = new InputSource
                    (getClass().getClassLoader()
                     .getResource(getConfigFile()).toString());
            } catch (Exception e) {
                if (log.isDebugEnabled()) {
                    log.debug(sm.getString("catalina.configFail",
                            getConfigFile()), e);
                }
            }
        }

        // This should be included in catalina.jar
        // Alternative: don't bother with xml, just create it manually.
        if (inputStream == null) {
            try {
                inputStream = getClass().getClassLoader()
                        .getResourceAsStream("server-embed.xml");
                inputSource = new InputSource
                (getClass().getClassLoader()
                        .getResource("server-embed.xml").toString());
            } catch (Exception e) {
                if (log.isDebugEnabled()) {
                    log.debug(sm.getString("catalina.configFail",
                            "server-embed.xml"), e);
                }
            }
        }


        if (inputStream == null || inputSource == null) {
            if  (file == null) {
                log.warn(sm.getString("catalina.configFail",
                        getConfigFile() + "] or [server-embed.xml]"));
            } else {
                log.warn(sm.getString("catalina.configFail",
                        file.getAbsolutePath()));
                if (file.exists() && !file.canRead()) {
                    log.warn("Permissions incorrect, read permission is not allowed on the file.");
                }
            }
            return;
        }

        try {
            inputSource.setByteStream(inputStream);
            digester.push(this);
            digester.parse(inputSource);
        } catch (SAXParseException spe) {
            log.warn("Catalina.start using " + getConfigFile() + ": " +
                    spe.getMessage());
            return;
        } catch (Exception e) {
            log.warn("Catalina.start using " + getConfigFile() + ": " , e);
            return;
        }
    } finally {
        if (inputStream != null) {
            try {
                inputStream.close();
            } catch (IOException e) {
                // Ignore
            }
        }
    }

    getServer().setCatalina(this);
    getServer().setCatalinaHome(Bootstrap.getCatalinaHomeFile());
    getServer().setCatalinaBase(Bootstrap.getCatalinaBaseFile());

    // Stream redirection
    initStreams();

    // Start the new server
    try {
        getServer().init();//调用Server实现类的init方法（即StandardServer的initInternal方法）
    } catch (LifecycleException e) {
        if (Boolean.getBoolean("org.apache.catalina.startup.EXIT_ON_INIT_FAILURE")) {
            throw new java.lang.Error(e);
        } else {
            log.error("Catalina.start", e);
        }
    }

    long t2 = System.nanoTime();
    if(log.isInfoEnabled()) {
        log.info("Initialization processed in " + ((t2 - t1) / 1000000) + " ms");
    }
}
```


### 5.3.5 catalina中的getServer方法


```java
public Server getServer() {
    return server;
}
```


### 5.3.6 StandardServer的initInternal方法


```java
/**
 * Invoke a pre-startup initialization. This is used to allow connectors
 * to bind to restricted ports under Unix operating environments.
 */
@Override
protected void initInternal() throws LifecycleException {

    super.initInternal();

    // Register global String cache
    // Note although the cache is global, if there are multiple Servers
    // present in the JVM (may happen when embedding) then the same cache
    // will be registered under multiple names
    onameStringCache = register(new StringCache(), "type=StringCache");

    // Register the MBeanFactory
    MBeanFactory factory = new MBeanFactory();
    factory.setContainer(this);
    onameMBeanFactory = register(factory, "type=MBeanFactory");

    // Register the naming resources
    globalNamingResources.init();

    // Populate the extension validator with JARs from common and shared
    // class loaders
    if (getCatalina() != null) {
        ClassLoader cl = getCatalina().getParentClassLoader();
        // Walk the class loader hierarchy. Stop at the system class loader.
        // This will add the shared (if present) and common class loaders
        while (cl != null && cl != ClassLoader.getSystemClassLoader()) {
            if (cl instanceof URLClassLoader) {
                URL[] urls = ((URLClassLoader) cl).getURLs();
                for (URL url : urls) {
                    if (url.getProtocol().equals("file")) {
                        try {
                            File f = new File (url.toURI());
                            if (f.isFile() &&
                                    f.getName().endsWith(".jar")) {
                                ExtensionValidator.addSystemResource(f);
                            }
                        } catch (URISyntaxException e) {
                            // Ignore
                        } catch (IOException e) {
                            // Ignore
                        }
                    }
                }
            }
            cl = cl.getParent();
        }
    }
    // Initialize our defined Services
    // 遍历Services，调用service的init方法
    for (int i = 0; i < services.length; i++) {
        services[i].init();
    }
}
```


### 5.3.7 StandardService的initInternal方法


```java
/**
 * Invoke a pre-startup initialization. This is used to allow connectors
 * to bind to restricted ports under Unix operating environments.
 */
@Override
protected void initInternal() throws LifecycleException {

    super.initInternal();

    if (engine != null) {
        engine.init();//初始化engine
    }

    // Initialize any Executors
    for (Executor executor : findExecutors()) {
        if (executor instanceof JmxEnabled) {
            ((JmxEnabled) executor).setDomain(getDomain());
        }
        executor.init();//初始化executor
    }

    // Initialize mapper listener
    mapperListener.init();

    // Initialize our defined Connectors
    synchronized (connectorsLock) {
        for (Connector connector : connectors) {
            try {
                connector.init();//初始化connector
            } catch (Exception e) {
                String message = sm.getString(
                        "standardService.connector.initFailed", connector);
                log.error(message, e);

                if (Boolean.getBoolean("org.apache.catalina.startup.EXIT_ON_INIT_FAILURE"))
                    throw new LifecycleException(message);
            }
        }
    }
}
```


### 5.3.8 Connector的initInternal方法


```java
@Override
protected void initInternal() throws LifecycleException {

    super.initInternal();

    // Initialize adapter
    adapter = new CoyoteAdapter(this);
    protocolHandler.setAdapter(adapter);

    // Make sure parseBodyMethodsSet has a default
    if (null == parseBodyMethodsSet) {
        setParseBodyMethods(getParseBodyMethods());
    }

    if (protocolHandler.isAprRequired() && !AprLifecycleListener.isAprAvailable()) {
        throw new LifecycleException(sm.getString("coyoteConnector.protocolHandlerNoApr",
                getProtocolHandlerClassName()));
    }
    if (AprLifecycleListener.isAprAvailable() && AprLifecycleListener.getUseOpenSSL() &&
            protocolHandler instanceof AbstractHttp11JsseProtocol) {
        AbstractHttp11JsseProtocol<?> jsseProtocolHandler =
                (AbstractHttp11JsseProtocol<?>) protocolHandler;
        if (jsseProtocolHandler.isSSLEnabled() &&
                jsseProtocolHandler.getSslImplementationName() == null) {
            // OpenSSL is compatible with the JSSE configuration, so use it if APR is available
            jsseProtocolHandler.setSslImplementationName(OpenSSLImplementation.class.getName());
        }
    }

    try {
        protocolHandler.init();//初始化protocolHandler
    } catch (Exception e) {
        throw new LifecycleException(
                sm.getString("coyoteConnector.protocolHandlerInitializationFailed"), e);
    }
}
```


### 5.3.9 AbstractProtocol的init方法


```java
/*
 * NOTE: There is no maintenance of state or checking for valid transitions
 * within this class. It is expected that the connector will maintain state
 * and prevent invalid state transitions.
 */

@Override
public void init() throws Exception {
    if (getLog().isInfoEnabled()) {
        getLog().info(sm.getString("abstractProtocolHandler.init", getName()));
    }

    if (oname == null) {
        // Component not pre-registered so register it
        oname = createObjectName();
        if (oname != null) {
            Registry.getRegistry(null, null).registerComponent(this, oname, null);
        }
    }

    if (this.domain != null) {
        rgOname = new ObjectName(domain + ":type=GlobalRequestProcessor,name=" + getName());
        Registry.getRegistry(null, null).registerComponent(
                getHandler().getGlobal(), rgOname, null);
    }

    String endpointName = getName();
    endpoint.setName(endpointName.substring(1, endpointName.length()-1));
    endpoint.setDomain(domain);

    endpoint.init();//初始化endpoint
}
```


### 5.3.10 AbstractEndpoint的init方法


```java
public void init() throws Exception {
    if (bindOnInit) {
        bind();//使用模板设计模式调用子类（如NioEndpoint）的bind方法
        bindState = BindState.BOUND_ON_INIT;
    }
    if (this.domain != null) {
        // Register endpoint (as ThreadPool - historical name)
        oname = new ObjectName(domain + ":type=ThreadPool,name=\"" + getName() + "\"");
        Registry.getRegistry(null, null).registerComponent(this, oname, null);

        ObjectName socketPropertiesOname = new ObjectName(domain +
                ":type=ThreadPool,name=\"" + getName() + "\",subType=SocketProperties");
        socketProperties.setObjectName(socketPropertiesOname);
        Registry.getRegistry(null, null).registerComponent(socketProperties, socketPropertiesOname, null);

        for (SSLHostConfig sslHostConfig : findSslHostConfigs()) {
            registerJmx(sslHostConfig);
        }
    }
}
```


### 5.3.11 NioEndpoint的bind方法


```java
/**
 * Initialize the endpoint.
 */
@Override
public void bind() throws Exception {
	//调用nio的API绑定对应的端口号来监听对应的端口
    if (!getUseInheritedChannel()) {
        serverSock = ServerSocketChannel.open();
        socketProperties.setProperties(serverSock.socket());
        InetSocketAddress addr = (getAddress()!=null?new InetSocketAddress(getAddress(),getPort()):new InetSocketAddress(getPort()));
        serverSock.socket().bind(addr,getAcceptCount());//绑定端口号
    } else {
        // Retrieve the channel provided by the OS
        Channel ic = System.inheritedChannel();
        if (ic instanceof ServerSocketChannel) {
            serverSock = (ServerSocketChannel) ic;
        }
        if (serverSock == null) {
            throw new IllegalArgumentException(sm.getString("endpoint.init.bind.inherited"));
        }
    }
    serverSock.configureBlocking(true); //mimic APR behavior

    // Initialize thread count defaults for acceptor, poller
    if (acceptorThreadCount == 0) {
        // FIXME: Doesn't seem to work that well with multiple accept threads
        acceptorThreadCount = 1;
    }
    if (pollerThreadCount <= 0) {
        //minimum one poller thread
        pollerThreadCount = 1;
    }
    setStopLatch(new CountDownLatch(pollerThreadCount));

    // Initialize SSL if needed
    initialiseSsl();

    selectorPool.open();
}
```


### 5.3.12 Bootstrap中的start方法


```java
/**
 * Start the Catalina daemon.
 * @throws Exception Fatal start error
 */
public void start()
    throws Exception {
    if( catalinaDaemon==null ) init();

    Method method = catalinaDaemon.getClass().getMethod("start", (Class [] )null);
    method.invoke(catalinaDaemon, (Object [])null);//通过反射方式调用catalina的start方法

}
```


### 5.1.13 catalina的start方法


```java
/**
 * Start a new server instance.
 */
public void start() {

    if (getServer() == null) {
        load();
    }

    if (getServer() == null) {
        log.fatal("Cannot start server. Server instance is not configured.");
        return;
    }

    long t1 = System.nanoTime();

    // Start the new server
    try {
        getServer().start();//调用server实现类（如StandardServer）的start方法
    } catch (LifecycleException e) {
        log.fatal(sm.getString("catalina.serverStartFail"), e);
        try {
            getServer().destroy();
        } catch (LifecycleException e1) {
            log.debug("destroy() failed for failed Server ", e1);
        }
        return;
    }

    long t2 = System.nanoTime();
    if(log.isInfoEnabled()) {
        log.info("Server startup in " + ((t2 - t1) / 1000000) + " ms");
    }

    // Register shutdown hook
    if (useShutdownHook) {
        if (shutdownHook == null) {
            shutdownHook = new CatalinaShutdownHook();
        }
        Runtime.getRuntime().addShutdownHook(shutdownHook);

        // If JULI is being used, disable JULI's shutdown hook since
        // shutdown hooks run in parallel and log messages may be lost
        // if JULI's hook completes before the CatalinaShutdownHook()
        LogManager logManager = LogManager.getLogManager();
        if (logManager instanceof ClassLoaderLogManager) {
            ((ClassLoaderLogManager) logManager).setUseShutdownHook(
                    false);
        }
    }

    if (await) {
        await();
        stop();
    }
}
```


### 5.3.14 StandardServer的startInternal方法


```java
/**
 * Start nested components ({@link Service}s) and implement the requirements
 * of {@link org.apache.catalina.util.LifecycleBase#startInternal()}.
 *
 * @exception LifecycleException if this component detects a fatal error
 *  that prevents this component from being used
 */
@Override
protected void startInternal() throws LifecycleException {

    fireLifecycleEvent(CONFIGURE_START_EVENT, null);
    setState(LifecycleState.STARTING);

    globalNamingResources.start();

    // Start our defined Services
    // 遍历Services，调用service的start方法
    synchronized (servicesLock) {
        for (int i = 0; i < services.length; i++) {
            services[i].start();
        }
    }
}
```


### 5.3.15 StandardService的startInternal方法


```java
/**
 * Start nested components ({@link Executor}s, {@link Connector}s and
 * {@link Container}s) and implement the requirements of
 * {@link org.apache.catalina.util.LifecycleBase#startInternal()}.
 *
 * @exception LifecycleException if this component detects a fatal error
 *  that prevents this component from being used
 */
@Override
protected void startInternal() throws LifecycleException {

    if(log.isInfoEnabled())
        log.info(sm.getString("standardService.start.name", this.name));
    setState(LifecycleState.STARTING);

    // Start our defined Container first
    if (engine != null) {
        synchronized (engine) {
            engine.start();//调用engine的start方法
        }
    }

    synchronized (executors) {
        for (Executor executor: executors) {
            executor.start();//调用executor的start方法
        }
    }

    mapperListener.start();

    // Start our defined Connectors second
    synchronized (connectorsLock) {
        for (Connector connector: connectors) {
            try {
                // If it has already failed, don't try and start it
                if (connector.getState() != LifecycleState.FAILED) {
                    connector.start();//调用connector的start方法
                }
            } catch (Exception e) {
                log.error(sm.getString(
                        "standardService.connector.startFailed",
                        connector), e);
            }
        }
    }
}
```


### 5.3.16 Connector的startInternal方法


```java
/**
 * Begin processing requests via this Connector.
 *
 * @exception LifecycleException if a fatal startup error occurs
 */
@Override
protected void startInternal() throws LifecycleException {

    // Validate settings before starting
    if (getPort() < 0) {
        throw new LifecycleException(sm.getString(
                "coyoteConnector.invalidPort", Integer.valueOf(getPort())));
    }

    setState(LifecycleState.STARTING);

    try {
        protocolHandler.start();//调用protocolHandler的start方法
    } catch (Exception e) {
        throw new LifecycleException(
                sm.getString("coyoteConnector.protocolHandlerStartFailed"), e);
    }
}
```


### 5.3.17 AbstractProtocol的start方法


```java
@Override
public void start() throws Exception {
    if (getLog().isInfoEnabled()) {
        getLog().info(sm.getString("abstractProtocolHandler.start", getName()));
    }

    endpoint.start();//调用endpoint实现类（如NioEndpoint）的start方法

    // Start async timeout thread
    asyncTimeout = new AsyncTimeout();
    Thread timeoutThread = new Thread(asyncTimeout, getNameInternal() + "-AsyncTimeout");
    int priority = endpoint.getThreadPriority();
    if (priority < Thread.MIN_PRIORITY || priority > Thread.MAX_PRIORITY) {
        priority = Thread.NORM_PRIORITY;
    }
    timeoutThread.setPriority(priority);
    timeoutThread.setDaemon(true);
    timeoutThread.start();
}
```


### 5.3.18 NioEndpoint的startInternal方法


```java
/**
 * Start the NIO endpoint, creating acceptor, poller threads.
 */
@Override
public void startInternal() throws Exception {

    if (!running) {
        running = true;
        paused = false;

        processorCache = new SynchronizedStack<>(SynchronizedStack.DEFAULT_SIZE,
                socketProperties.getProcessorCache());
        eventCache = new SynchronizedStack<>(SynchronizedStack.DEFAULT_SIZE,
                        socketProperties.getEventCache());
        nioChannels = new SynchronizedStack<>(SynchronizedStack.DEFAULT_SIZE,
                socketProperties.getBufferPool());

        // Create worker collection
        if ( getExecutor() == null ) {
            createExecutor();
        }

        initializeConnectionLatch();

        // Start poller threads
        pollers = new Poller[getPollerThreadCount()];
        for (int i=0; i<pollers.length; i++) {
            pollers[i] = new Poller();
            Thread pollerThread = new Thread(pollers[i], getName() + "-ClientPoller-"+i);
            pollerThread.setPriority(threadPriority);
            pollerThread.setDaemon(true);
            pollerThread.start();
        }

        startAcceptorThreads();//开启接受请求的线程
    }
}
```


### 5.3.19 NioEndpoint的startAcceptorThreads方法


```java
protected final void startAcceptorThreads() {
    int count = getAcceptorThreadCount();
    acceptors = new Acceptor[count];

    for (int i = 0; i < count; i++) {
        acceptors[i] = createAcceptor();//创建自己的Acceptor，以接受符合自身协议的用户请求
        String threadName = getName() + "-Acceptor-" + i;
        acceptors[i].setThreadName(threadName);
        Thread t = new Thread(acceptors[i], threadName);
        t.setPriority(getAcceptorThreadPriority());
        t.setDaemon(getDaemon());
        t.start();
    }
}
```


### 5.3.20 NioEndpoint的createAcceptor方法


```java
@Override
protected AbstractEndpoint.Acceptor createAcceptor() {
    return new Acceptor();
}
```


### 5.3.21 NioEndpoint的Acceptor内部类


为了在Thread中运行，其实现了run方法


```java
// --------------------------------------------------- Acceptor Inner Class
/**
 * The background thread that listens for incoming TCP/IP connections and
 * hands them off to an appropriate processor.
 */
protected class Acceptor extends AbstractEndpoint.Acceptor {

    @Override
    public void run() {

        int errorDelay = 0;

        // Loop until we receive a shutdown command
        while (running) {

            // Loop if endpoint is paused
            while (paused && running) {
                state = AcceptorState.PAUSED;
                try {
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    // Ignore
                }
            }

            if (!running) {
                break;
            }
            state = AcceptorState.RUNNING;

            try {
                //if we have reached max connections, wait
                countUpOrAwaitConnection();

                SocketChannel socket = null;
                try {
                    // Accept the next incoming connection from the server
                    // socket
                    socket = serverSock.accept();//接受客户端的请求
                } catch (IOException ioe) {
                    // We didn't get a socket
                    countDownConnection();
                    if (running) {
                        // Introduce delay if necessary
                        errorDelay = handleExceptionWithDelay(errorDelay);
                        // re-throw
                        throw ioe;
                    } else {
                        break;
                    }
                }
                // Successful accept, reset the error delay
                errorDelay = 0;

                // Configure the socket
                if (running && !paused) {
                    // setSocketOptions() will hand the socket off to
                    // an appropriate processor if successful
                    if (!setSocketOptions(socket)) {
                        closeSocket(socket);
                    }
                } else {
                    closeSocket(socket);
                }
            } catch (Throwable t) {
                ExceptionUtils.handleThrowable(t);
                log.error(sm.getString("endpoint.accept.fail"), t);
            }
        }
        state = AcceptorState.ENDED;
    }


    private void closeSocket(SocketChannel socket) {
        countDownConnection();
        try {
            socket.socket().close();
        } catch (IOException ioe)  {
            if (log.isDebugEnabled()) {
                log.debug(sm.getString("endpoint.err.close"), ioe);
            }
        }
        try {
            socket.close();
        } catch (IOException ioe) {
            if (log.isDebugEnabled()) {
                log.debug(sm.getString("endpoint.err.close"), ioe);
            }
        }
    }
}
```


## 5.4 总结


从启动流程图中以及源码中，我们可以看出Tomcat的启动过程非常标准化， 统一按照生命周期管理接口Lifecycle的定义进行启动。首先调用`init()`方法进行组件的逐级初始化操作，然后再调用`start()`方法进行启动。


每一级的组件除了完成自身的处理外，还要负责调用子组件响应的生命周期管理方法， 组件与组件之间是松耦合的，因为我们可以很容易的通过配置文件进行修改和替换。


# 6 Tomcat 请求处理流程


## 6.1 创建Module测试Tomcat请求流程


### 6.1.1 新建Module


![image-20200416203759254.png](./media/1587092349958-cf4e987b-4eb8-4147-b26d-bf8cb6288868.png)


### 6.1.2 BbsServlet


```java
package cn.zh.web;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

public class BbsServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        System.out.println("==========>>GET:BbsServlet findAll......");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        System.out.println("==========>>POST:BbsServlet findAll......");
    }
}
```


### 6.1.3 `web.xml`


位置：`zh_empty_project/servlet_demo01/web/WEB-INF/web.xml`


```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
    <servlet>
        <servlet-name>bbsServlet</servlet-name>
        <servlet-class>cn.zh.web.BbsServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>bbsServlet</servlet-name>
        <url-pattern>/bbs/findAll</url-pattern>
    </servlet-mapping>
</web-app>
```


### 6.1.6 配置Tomcat服务器


![image-20200416212222421.png](./media/1587092376378-d0d4c04e-4ddf-4868-b076-5f46c7c8a9e7.png)


### 6.1.5 测试


浏览器访问：[http://localhost:8080/servlet_demo01_war_exploded/bbs/findAll](http://localhost:8080/servlet_demo01_war_exploded/bbs/findAll)


后台打印：`==========>>GET:BbsServlet findAll......`


## 6.2 请求流程


设计了这么多层次的容器，Tomcat是怎么确定每一个请求应该由哪个Wrapper容器里的Servlet来处理的呢？答案是，Tomcat是用Mapper组件来完成这个任务的。


Mapper组件的功能就是将用户请求的URL定位到一个Servlet，它的工作原理是：Mapper组件里保存了Web应用的配置信息，其实就是容器组件与访问路径的映射关系，比如Host容器里配置的域名、Context容器里的Web应用路径，以及Wrapper容器里Servlet映射的路径，你可以想象这些配置信息就是一个多层次的Map。


当一个请求到来时，Mapper组件通过解析请求URL里的域名和路径，再到自己保存的Map里去查找，就能定位到一个Servlet。请你注意，一个请求URL最后只会定位到一个Wrapper容器，也就是一个Servlet。


下面的示意图中，就描述了当用户请求连接`http://www.zh.cn/bbs/findAll`之后，是如何找到最终处理业务逻辑的servlet。


![image-20200416213406321.png](./media/1587092396774-420a97f1-cbad-49fc-ab33-6f4e231de087.png)


那上面这幅图只是描述了根据请求的URL如何查找到需要执行的Servlet ， 那么下面我们再来解析一下， 从Tomcat的设计架构层面来分析Tomcat的请求处理。


![image-20200416215144929.png](./media/1587092428825-1c7e8445-4732-4bce-852a-e8dea6df460a.png)


步骤如下：


1. Connector组件Endpoint中的Acceptor监听客户端套接字连接并接收Socket。
2. 将连接交给线程池Executor处理，开始执行请求响应任务。
3. Processor组件读取消息报文，解析请求行、请求体、请求头，封装成Request对象。
4. Mapper组件根据请求行的URL值和请求头的Host值匹配由哪个Host容器、Context容器、Wrapper容器处理请求。
5. CoyoteAdaptor组件负责将Connector组件和Engine容器关联起来，把生成的Request对象和响应对象Response传递到Engine容器中，调用 Pipeline。
6. Engine容器的管道开始处理，管道中包含若干个Valve、每个Valve负责部分处理逻辑。执行完Valve后会执行基础的 Valve--StandardEngineValve，负责调用Host容器的Pipeline。
7. Host容器的管道开始处理，流程类似，最后执行 Context容器的Pipeline。
8. Context容器的管道开始处理，流程类似，最后执行 Wrapper容器的Pipeline。
9. Wrapper容器的管道开始处理，流程类似，最后执行 Wrapper容器对应的Servlet对象的 处理方法。



## 6.3 请求流程源码解析


### 6.3.1 把测试项目servlet_demo01部署到Tomcat源码里面


找到编译后servlet_demo01的项目，位置为`/run/media/zh/data/projects/tomcat2/zh_empty_project/out/artifacts/servlet_demo01_war_exploded`


![image-20200416220824504.png](./media/1587092450390-ae301913-ed79-4a14-a9ee-7a297b9e01b0.png)


把此项目复制到Tomcat源码项目apache-tomcat-8.5.42-src根目录下的`home/webapps`下并改测试项目文件夹名为servlet_demo01，最后项目的位置为`/run/media/zh/data/projects/tomcat2/zh_empty_project/apache-tomcat-8.5.42-src/home/webapps/servlet_demo01`。


重启Tomcat源码apache-tomcat-8.5.42-src项目。


浏览器访问：[http://localhost:8080/servlet_demo01/bbs/findAll](http://localhost:8080/servlet_demo01/bbs/findAll)


后台打印：`==========>>GET:BbsServlet findAll......`


### 6.3.2 源码跟踪请求处理流程


![image-20200417104254873.png](./media/1587092465928-e164de51-0847-4fee-8400-67c74d8a0ee4.png)


在前面所讲解的Tomcat的整体架构中，我们发现Tomcat中的各个组件各司其职，组件之间松耦合，确保了整体架构的可伸缩性和可拓展性，那么在组件内部，如何增强组件的灵活性和拓展性呢？ 在Tomcat中，每个Container组件采用责任链模式来完成具体的请求处理。


在Tomcat中定义了Pipeline 和 Valve 两个接口，Pipeline 用于构建责任链， 后者代表责任链上的每个处理器。Pipeline 中维护了一个基础的Valve，它始终位于Pipeline的末端（最后执行），封装了具体的请求处理和输出响应的过程。当然，我们也可以调用addValve()方法， 为Pipeline 添加其他的Valve，后添加的Valve 位于基础的Valve之前，并按照添加顺序执行。Pipiline通过获得首个Valve来启动整合链条的执行 。
