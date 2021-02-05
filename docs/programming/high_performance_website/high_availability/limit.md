# 限流

# 1 在Spring Boot中使用AOP和自定义限流注解的方式实现

## 1.1 思路

通过连接接口自定义注解的方法来记录和判断访问次数。

## 1.2 实现

### 1.2.1 springboot maven工程pom文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.zh</groupId>
    <artifactId>limitspringboot</artifactId>
    <version>1.0-SNAPSHOT</version>
    <!-- 继承父包 -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.2.5.RELEASE</version>
    </parent>
    <dependencies>
        <!-- web启动jar -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.aspectj</groupId>
            <artifactId>aspectjweaver</artifactId>
        </dependency>
    </dependencies>
</project>
```

### 1.2.2 spirng boot启动类

```java
package com.zh.limit;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * @Author: ZhangHai
 * @Date: 2021/2/1 16:49
 */
@SpringBootApplication
public class LimitApplication {
    public static void main(String[] args) {
        SpringApplication.run(LimitApplication.class, args);
    }
}
```

### 1.2.3 自定义限流注解

```java
package com.zh.limit.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * @Author: ZhangHai
 * @Date: 2021/2/1 16:54
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Limit {
    String name() default "";//资源名称，用于描述接口的功能
    String key() default "";//资源的key，用于记录访问记录等信息
    String prefix() default ""; //key的前缀，可以是模块名，用于整合key
    int period();//限流次数的计算时间段, 单位为秒
    int count();//限制次数，为period周期内的限制次数
    LimitType limitType() default LimitType.CUSTOMER;//限流类型
}
```

```java
package com.zh.limit.annotation;

/**
 * 限流类型枚举类
 * @Author: ZhangHai
 * @Date: 2021/2/1 17:00
 */
public enum LimitType {
    CUSTOMER,//默认值，用户自定义限流类型
    IP//ip限流类型
}
```

### 1.2.4 自定义注解通知类实现限流逻辑

#### 1.2.4.1 限流逻辑通知类

```java
package com.zh.limit.annotation;

import com.zh.limit.exception.BadRequestException;
import com.zh.limit.utils.ExpireHashMap;
import com.zh.limit.utils.RequestUtil;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import javax.servlet.http.HttpServletRequest;
import java.lang.reflect.Method;

/**
 * 限流通知类
 * @Author: ZhangHai
 * @Date: 2021/2/1 17:05
 */
@Aspect
@Component
public class LimitAdvice {
    private final ExpireHashMap<String, Integer> expireHashMap = new ExpireHashMap();

    @Pointcut("@annotation(com.zh.limit.annotation.Limit)")
    public void pointcut(){}

    @Around("pointcut()")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable{
        HttpServletRequest request = RequestUtil.getHttpServletRequest();
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        Method method = signature.getMethod();
        Limit limit = method.getAnnotation(Limit.class);
        LimitType limitType = limit.limitType();
        String key = limit.key();
        if(StringUtils.isEmpty(key)){
            if(limitType == LimitType.IP){
                key = RequestUtil.getIp(request);
            }else {
                key = method.getName();
            }
        }
        String map_key = limit.period() + "_" + key + "_" + request.getRequestURI().replaceAll("/", "_");
        Integer count = null;
        synchronized (this){
            count = this.expireHashMap.get(map_key);
            long expire = count == null? limit.period()*1000:this.expireHashMap.expire(map_key);
            count = count == null?1:++count;
            this.expireHashMap.put(map_key, count, expire);
        }
        if(null != count && count <= limit.count()){
            System.out.println("访问次数为：" + count);
            return joinPoint.proceed();
        }else{
            throw new BadRequestException("访问次数受限");
        }
    }
}
```

#### 1.2.4.2 自定义带过期时间的Map

```java
package com.zh.limit.utils;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * @Author: ZhangHai
 * @Date: 2021/2/5 16:36
 */
public class ExpireHashMap<K, V> {
    private Map<K, Map<String, Object>> _map = new HashMap<>();
    private final static String EXPIRE_KEY = "expire";
    private final static String VALUE_KEY = "value";
    public ExpireHashMap(){};
    public void put(K key, V value, long expire){
        this._map.put(key, new HashMap(){
            {
                put("value", value);
                put("expire", new Date().getTime() + expire);
            }
        });
    }
    public V get(K key){
        if(!this._map.containsKey(key)){
            return null;
        }
        if (this.isExpire(key)){
            this._map.remove(key);
            return null;
        }else {
            return (V)this._map.get(key).get(VALUE_KEY);
        }
    }

    public boolean isExpire(K key){
        Long expire = (Long) this._map.get(key).get(EXPIRE_KEY);
        if (new Date().getTime() > expire){
            return true;
        }else{
            return false;
        }
    }

    public long expire(K key){
        return this._map.containsKey(key)?(long)this._map.get(key).get(EXPIRE_KEY):0l;
    }
}
```

#### 1.2.4.3 获取ip地址的工具类

```java
package com.zh.limit.utils;

import org.omg.CORBA.UNKNOWN;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.Objects;

/**
 * @Author: ZhangHai
 * @Date: 2021/2/1 17:23
 */
public class RequestUtil {
    public static HttpServletRequest getHttpServletRequest(){
        return ((ServletRequestAttributes) Objects.requireNonNull(RequestContextHolder.getRequestAttributes())).getRequest();
    }
    public static String getIp(HttpServletRequest request){
        String ip = request.getHeader("x-forwarded-for");
        if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)){
            ip = request.getHeader("Proxy-Client-IP");
        }
        if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)){
            ip = request.getHeader("WL-Proxy-Client-IP");
        }
        if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)){
            ip = request.getRemoteAddr();
        }
        String comma = ",";
        String localhost = "127.0.0.1";
        if(ip.contains(comma)){
            ip = ip.split(",")[0];
        }
        if(localhost.equals(ip)){
            try{
                ip = InetAddress.getLocalHost().getHostAddress();
            }catch (UnknownHostException e){
                e.printStackTrace();
            }
        }
        return ip;
    }
}
```

#### 1.2.4.4 自定义限流异常类

```java
package com.zh.limit.exception;

import org.springframework.http.HttpStatus;

/**
 * @Author: ZhangHai
 * @Date: 2021/2/4 17:18
 */
public class BadRequestException extends RuntimeException{
    private Integer status = HttpStatus.BAD_REQUEST.value();
    public BadRequestException(String msg){
        super(msg);
    }
    public BadRequestException(HttpStatus status, String msg){
        super(msg);
        this.status = status.value();
    }

    public Integer getStatus() {
        return status;
    }
}
```

### 1.2.5 测试接口:使用自定义限流注解标注

```java
package com.zh.limit.controller;

import com.zh.limit.annotation.Limit;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * @Author: ZhangHai
 * @Date: 2021/2/1 16:50
 */
@Controller
public class LimitTestController {
    private static final AtomicInteger ATOMIC_INTEGER = new AtomicInteger();

    @GetMapping("/testLimit")
    @ResponseBody
    @Limit(key = "test", period = 60, count = 10, name = "testLimit", prefix = "limit")
    public int testLimit(){
        return ATOMIC_INTEGER.incrementAndGet();
    }
}
```

### 1.2.6 测试

接口：`GET http://localhost:8080/testLimit`

- 为达到限流标准时

  - 接口返回值：`1`
  - 控制台输出：`访问次数为：1`

- 达到限流标准：

  - 接口返回：

    ```
    {
      "timestamp": "2021-02-05T09:30:09.658+0000",
      "status": 500,
      "error": "Internal Server Error",
      "message": "访问次数受限",
      "path": "/testLimit"
    }
    ```

  - 控制台输出：

    ```
    访问次数为：10
    2021-02-05 17:30:09.658 ERROR 17384 --- [nio-8080-exec-1] o.a.c.c.C.[.[.[/].[dispatcherServlet]    : Servlet.service() for servlet [dispatcherServlet] in context with path [] threw exception [Request processing failed; nested exception is com.zh.limit.exception.BadRequestException: 访问次数受限] with root cause
    
    com.zh.limit.exception.BadRequestException: 访问次数受限
    	at com.zh.limit.annotation.LimitAdvice.around(LimitAdvice.java:57) ~[classes/:na]
    	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[na:1.8.0_261]
    	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62) ~[na:1.8.0_261]
    	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[na:1.8.0_261]
    	at java.lang.reflect.Method.invoke(Method.java:498) ~[na:1.8.0_261]
    	at org.springframework.aop.aspectj.AbstractAspectJAdvice.invokeAdviceMethodWithGivenArgs(AbstractAspectJAdvice.java:644) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.aop.aspectj.AbstractAspectJAdvice.invokeAdviceMethod(AbstractAspectJAdvice.java:633) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.aop.aspectj.AspectJAroundAdvice.invoke(AspectJAroundAdvice.java:70) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:175) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:747) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.aop.interceptor.ExposeInvocationInterceptor.invoke(ExposeInvocationInterceptor.java:95) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:186) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:747) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:689) ~[spring-aop-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at com.zh.limit.controller.LimitTestController$$EnhancerBySpringCGLIB$$d7cf6d33.testLimit(<generated>) ~[classes/:na]
    	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method) ~[na:1.8.0_261]
    	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62) ~[na:1.8.0_261]
    	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43) ~[na:1.8.0_261]
    	at java.lang.reflect.Method.invoke(Method.java:498) ~[na:1.8.0_261]
    	at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:190) ~[spring-web-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:138) ~[spring-web-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:106) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:879) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:793) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1040) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:943) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:898) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at javax.servlet.http.HttpServlet.service(HttpServlet.java:634) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883) ~[spring-webmvc-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at javax.servlet.http.HttpServlet.service(HttpServlet.java:741) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53) ~[tomcat-embed-websocket-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100) ~[spring-web-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93) ~[spring-web-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201) ~[spring-web-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119) ~[spring-web-5.2.4.RELEASE.jar:5.2.4.RELEASE]
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:202) ~[tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:96) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:541) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:139) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:74) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:367) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:868) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1639) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149) [na:1.8.0_261]
    	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624) [na:1.8.0_261]
    	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61) [tomcat-embed-core-9.0.31.jar:9.0.31]
    	at java.lang.Thread.run(Thread.java:748) [na:1.8.0_261]
    
    Disconnected from the target VM, address: '127.0.0.1:54886', transport: 'socket'
    2021-02-05 17:31:47.622  INFO 17384 --- [extShutdownHook] o.s.s.concurrent.ThreadPoolTaskExecutor  : Shutting down ExecutorService 'applicationTaskExecutor'
    
    ```

    