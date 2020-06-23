# Tomcat简介

# 1 常见的Web服务器


## 1.1 概念


- **服务器**：安装了服务器软件的计算机
- **服务器软件**：接收用户的请求，处理请求，做出响应
- **web服务器软件**：接收用户的请求，处理请求，做出响应。
  - 在web服务器软件中，可以部署web项目，让用户通过浏览器来访问这些项目



## 1.2 常见web服务器软件


- **webLogic**：oracle公司，大型的JavaEE服务器，支持所有的JavaEE规范，收费的。
- **webSphere**：IBM公司，大型的JavaEE服务器，支持所有的JavaEE规范，收费的。
- **JBOSS**：JBOSS公司的，大型的JavaEE服务器，支持所有的JavaEE规范，收费的。
- **Tomcat**：Apache基金组织，中小型的JavaEE服务器，仅仅支持少量的JavaEE规范servlet/jsp。开源的，免费的。

# 2 Tomcat 目录结构


**`apache-tomcat-8.5.42`**：


- `bin`：存放Tomcat的启动、停止等批处理脚本文件
  - `startup.bat`，`startup.sh`：用于在windows和linux下的启动脚本
  - `shutdown.bat`，`shutdown.sh`：用于在windows和linux下的停止脚本
- `conf`：用于存放Tomcat的相关配置文件
  - `Catalina`：用于存储针对每个虚拟机的Context配置
  - `context.xml`：用于定义所有web应用均需加载的Context配置，如果web应用指定了自己的context.xml ，该文件将被覆盖
  - `catalina.properties`：Tomcat 的环境变量配置
  - `catalina.policy`：Tomcat 运行的安全策略配置
  - `logging.properties`：Tomcat 的日志配置文件， 可以通过该文件修改Tomcat 的日志级别及日志路径等
  - `server.xml`：Tomcat 服务器的核心配置文件
  - `tomcat-users.xml`：定义Tomcat默认的用户及角色映射信息配置
  - `web.xml`：Tomcat 中所有应用默认的部署描述文件， 主要定义了基础Servlet和MIME映射。
- `lib`：Tomcat 服务器的依赖包
- `logs`：Tomcat 默认的日志存放目录
- `webapps`：Tomcat 默认的Web应用部署目录
- `work`：Web 应用JSP代码生成和编译的临时目录

# 3 Tomcat源码运行


## 3.1 Tomcat源码在idea中运行


**第一步：解压zip压缩包。**


```shell
[zh@zh-inspironn4050 安装包及源码]$ unzip apache-tomcat-8.5.42-src.zip 
Archive:  apache-tomcat-8.5.42-src.zip
   creating: apache-tomcat-8.5.42-src/
   ......
  inflating: apache-tomcat-8.5.42-src/webapps/manager/index.jsp  
  inflating: apache-tomcat-8.5.42-src/webapps/manager/status.xsd  
  inflating: apache-tomcat-8.5.42-src/webapps/manager/xform.xsl 
[zh@zh-inspironn4050 安装包及源码]$
```


**第二步：进入解压目录`apache-tomcat-8.5.42-src`，并创建一个目录，命名为home（可以自定义） ， 并将conf、webapps目录移入home 目录中。**


**第三步：在当前目录（`apache-tomcat-8.5.42-src`）下创建一个 pom.xml 文件，引入tomcat的依赖包。**


```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<groupId>org.apache.tomcat</groupId>
	<artifactId>apache-tomcat-8.5.42-src</artifactId>
	<name>Tomcat8.5</name>
	<version>8.5</version>
	<build>
		<sourceDirectory>java</sourceDirectory>
		<!-- <testSourceDirectory>test</testSourceDirectory> -->
		<resources>
			<resource>
				<directory>java</directory>
			</resource>
		</resources>
		<!-- <testResources> <testResource> <directory>test</directory> </testResource> 
			</testResources> -->
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-compiler-plugin</artifactId>
				<version>2.3</version>
				<configuration>
					<encoding>UTF-8</encoding>
					<source>1.8</source>
					<target>1.8</target>
				</configuration>
			</plugin>
		</plugins>
	</build>
	<dependencies>
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>4.12</version>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>org.easymock</groupId>
			<artifactId>easymock</artifactId>
			<version>3.4</version>
		</dependency>
		<dependency>
			<groupId>ant</groupId>
			<artifactId>ant</artifactId>
			<version>1.7.0</version>
		</dependency>
		<dependency>
			<groupId>wsdl4j</groupId>
			<artifactId>wsdl4j</artifactId>
			<version>1.6.2</version>
		</dependency>
		<dependency>
			<groupId>javax.xml</groupId>
			<artifactId>jaxrpc</artifactId>
			<version>1.1</version>
		</dependency>
		<dependency>
			<groupId>org.eclipse.jdt.core.compiler</groupId>
			<artifactId>ecj</artifactId>
			<version>4.5.1</version>
		</dependency>
	</dependencies>
</project>
```


**第四步： 导入该工程。**


创建空的project：


![image-20200416084103748.png](https://zhishan-zh.github.io/media/tomcat-9b74-8d066434a1e9.png)

把项目拷贝到idea空工程`zh_empty_project`（`/run/media/zh/data/projects/tomcat2/zh_empty_project/`）目录下
![image-20200415222812196.png](https://zhishan-zh.github.io/media/tomcat-bfb2-f92db9b8e94e.png)

**第五步：在idea中配置启动类， 配置 MainClass（`org.apache.catalina.startup.Bootstrap`） ， 并配置 VM 参数。**


虽然说Tomcat是服务器，但是任何Java项目，在进行运行的时候的它的入口main方法。


![image-20200416101256442.png](https://zhishan-zh.github.io/media/tomcat-ac02-d1c33e642aca.png)


```properties
-Dcatalina.home=/run/media/zh/data/projects/tomcat2/zh_empty_project/apache-tomcat-8.5.42-src/home
-Dcatalina.base=/run/media/zh/data/projects/tomcat2/zh_empty_project/apache-tomcat-8.5.42-src/home
-Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
-Djava.util.logging.config.file=/run/media/zh/data/projects/tomcat2/zh_empty_project/apache-tomcat-8.5.42-src/home/conf/logging.properties
```
![image-20200416101305860.png](https://zhishan-zh.github.io/media/tomcat-bcb0-7f8c6f3fa9bf.png)



**第六步：启动主方法， 运行Tomcat ， 访问Tomcat 。**
![image-20200416101435698.png](https://zhishan-zh.github.io/media/tomcat-89bd-5c0266dd45e0.png)

```
/usr/lib/jvm/java-8-openjdk/bin/java -agentlib:jdwp=transport=dt_socket,address=127.0.0.1:58743,suspend=y,server=n -Dcatalina.home=/run/media/zh/data/projects/tomcat2/zh_empty_project/apache-tomcat-8.5.42-src/home -（此处省略N行打印信息）16-Apr-2020 10:52:46.509 信息 [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["http-nio-8080"]

16-Apr-2020 10:52:46.671 信息 [main] org.apache.coyote.AbstractProtocol.start Starting ProtocolHandler ["ajp-nio-8009"]

16-Apr-2020 10:52:46.701 信息 [main] org.apache.catalina.startup.Catalina.start Server startup in 5722 ms
```

## 3.2 页面测试Tomcat源码运行


页面访问：http://localhost:8080/，页面输出报错信息


![image-20200416110025320.png](https://zhishan-zh.github.io/media/tomcat-8a29-b57eab2d0ae7.png)

**出现上述异常的原因**，是我们直接启动`org.apache.catalina.startup.Bootstrap`的时候没有加载JasperInitializer，从而无法编译JSP。


**解决办法**是在tomcat的源码`org.apache.catalina.startup.ContextConfig`中的configureStart函数中手动将JSP解析器初始化：`context.addServletContainerInitializer(new JasperInitializer(), null);`


![image-20200416110643444.png](https://zhishan-zh.github.io/media/tomcat-495c-b7cf-b564bb525f51.png)


重启tomcat就可以正常访问了。


![image-20200416111002968.png](https://zhishan-zh.github.io/media/tomcat-9ca1-d8e465191b75.png)
