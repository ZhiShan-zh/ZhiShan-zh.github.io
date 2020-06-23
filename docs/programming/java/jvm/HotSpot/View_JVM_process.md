# 查看JVM进程

# 1 概述

与UNIX命令ps类似，jps工具用来列举系统中正在运行的Java进程。从JDK1.5开始，jps工具随Oracle JDK发布。

# 2 用jps查看Java进程

jps命令格式：`jps [option] [hostid]`

- option：表示命令选项
    - `-q`：不输出类命令、JAR文件名称和应用程序主方法的参数，仅列出本地虚拟机标识符。
    - `-m`：输出传递到应用程序主方法的参数。
    - `-l`：输出应用程序主类的完整包名，或JAR文件的完整路径。
    - `-v`：输出虚拟机参数。
    - `-V`：输出通过标识文件传递给虚拟机的参数。标识文件（flags file）为`.hotspotrc`文件或者在虚拟机参数中指定的文件名（`-XX:Flags=<filename>argument`）。
- hostid：即主机标识符（host identifier），是用来定位目的主机位置的一串字符。
    - hostid字符串的语法类似URI的语法，其形式为：`[protocol:][[//][:port][/servername]]`
        - protocol：标识通信协议。
            - 如果省略protocol，且不指定hostname，则默认采用一个依赖于平台的本地协议。
            - 如果省略protocol，但指定hostname，那么默认采用RMI协议（即Remote Method Invoke 远程方法调用）。
        - hostname：指定主机名
            - 一个主机名或IP地址知识目标主机。
            - 如果省略hostname，则默认目标主机为本地主机。
        - port：指定端口号，与远程服务器通信的默认端口。
            - 如果省略hostname或者protocol指定为本地协议，则端口号将被忽略，
            - 否则，端口号依赖于特定实现，对于默认RMI协议，端口号为远程主机上注册RMI服务的端口号，如果省略端口，且协议指定为RMI，那么默认RMI服务注册端口为1099。
        - servername：这个参数依赖于具体实现。
            - 对于本地协议，该参数被忽略。
            - 对于RMI协议，该参数是一个以字符串表示的在远程主机上的RMI远程对象。详情请参考jstatd命令（`-n`选项）。

**注意**：在不同版本的JDK中，jps的选项即参数的含义可能会有所区别。

# 3 jps的实现

MonitoredVmUtil实现了一系列获取虚拟机监视器（monitor）信息的接口方法，这些方法通过读取并解析共享内存PerfMemory的命名变量。能够捕获虚拟机监视器信息。这些监视器包括以下几项：

- 虚拟机版本（vmVersion）：对应monitor名字`java.property.java.vm.version`。
- 命令行（commandLine）：对应monitor名字`sun.rt.javaCommand`。
- 主程序参数（mainArgs）：通过解析`sun.rt.javaCommand`得到的命令行细分信息。
- 主程序（mainClass）：通过解析`sun.rt.javaCommand`得到的命令行细分信息。
- 虚拟机参数（jvmArgs）：对应monitor名字`sjava.rt.vmArgs`。
- 虚拟机选项（jvmFlags）：对应monitor名字`sjava.rt.vmFlags`。
- 虚拟机功能集（jvmCapabilities）：对应monitor名字`sun.rt.jvmCapabilities`。在虚拟机内表示中，`sun.rt.jvmCapabilities`是由一串64位二进制串表示的，其格式形如1000000000000000000000000000000000000000000000000000000000000000。其中每一位均为有特定含义的标志位，例如，通过检测第0号位置的标志位，就可以判断目标JVM是否允许连接。

MonitoredVmUtil能够查询上述监视器，通过解析监视器内容，获得jps所关心的主要数据。

获取监视器的实现步骤如下：

1. 获得MonitoredVm：通过MonitoredHost的具体实现类可以得到MonitoredVm。MonitoredHost是一个抽象类，定义了一些抽象函数成员，包括`getMonitoredHost()`、`getMonitoredVm（）`等函数。根据目标虚拟机的host类型，系统提供了三种不同的MonitoredHostProvider。这三种MonitoredHostProvider虽然同名，但分别位于不同的包中以作区分。
    - 根据host的三种类型（RMI、local和file），这三个MonitoredHostProvider类分别位于包`sun.jvmstat.perfdata.monitor.protocol.<ProtocolType>`中（`<ProtocolType>`分别为rmi、local、file）。依次调用MonitoredHostProvider对象的`getMonitoredHost()`和`getMonitoredVm（）`方法，可以分别获得特定host类型的MonitoredHost和MonitoredVm。
2. 创建PerfData缓存：在创建具体类型的MonitoredVm的同时，也会创建一个具体类型为rmi、local、file的PerfDataBuffer对象实例。
    - PerfDataBuffer继承自AbstractPerfDataBuffer，拥有其继承自父类的成员变量impl。impl将在运行期绑定具体类型（例如`sun.jvmstat.perfdata.monitor.v2_0.PerfDataBuffer`）。impl继承了父类PerfDataBufferImpl的一些成员，如buffer、monitors、lvmid、aliasMap、aliasCache等，围绕这些成员，impl拥有buildMonitorMap、findByName和findByPattern等方法，可以提供监视器map的创建、数据获取和查找功能。
    - 在PerfDataBuffer的构造函数中，将调用抽象类AbstractPerfDataBuffer实现的公共函数createPerfDataBuffer，创建出一个PerfDataBufferImpl对象实例impl。这个过程对于RMI、local或file类型，都是一样的，区别在于createPerfDataBuffer如参paramByteBuffer（ByteBuffer）的赋值来源不一样，这个与目标JVM的PerfData数据共享的机制差别有关。
3. 

