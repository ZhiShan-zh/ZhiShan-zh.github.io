# Spring Boot开启CORS跨域支持

跨域相关知识参见：[跨域](./docs/programming/JavaScript/Cross-domain.md)

# 1 概述

CORS（Cross-Origin Resource Sharing, 跨源资源共享）是W3C出的一个标准，其思想是使用自定义的HTTP头部让浏览器与服务器进行沟通，从而决定请求或响应是应该成功，还是应该失败。因此，要想实现CORS进行跨域，需要服务器进行一些设置，同时前端也需要做一些配置和分析。

## 1.1 Spring Boot支持CORS跨域的方法

- **单接口跨域支持**：使用`@CrossOrigin`注解接口方法。
- **单Controller类跨域支持**：使用`@CrossOrigin`注解该Controller。
- **全局跨域支持**：添加一个配置类，对该Application有效。

## 1.2 `@CrossOrigin`参数说明

|             属性 | 说明                                                         |
| ---------------: | ------------------------------------------------------------ |
|          origins | 允许可访问的域列表。 其值放置在HTTP协议的响应header的`Access-Control-Allow-Origin` 。 如果未定义或给一个通配符`*`，则意味着所有的源都是被允许的。 |
|   allowedHeaders | 实际请求期间可以使用的请求头列表。 其值用于预检的响应head的`Access-Control-Allow-Headers`。 如果未定义或给一个通配符`*`，则意味允许客户端请求的所有头文件。 |
|          methods | 支持的HTTP请求方法列表。  如果未定义，则使用由RequestMapping注释定义的方法。 |
|   exposedHeaders | 可以让用户拿到的头字段。有几个字段无论设置与否都可以拿到的，包括：`Cache-Control`、`Content-Language`、`Content-Type`、`Expires`、`Last-Modified`、`Pragma`。 |
| allowCredentials | 用户是否可以发送、处理 `cookie`。                            |
|           maxAge | 预响应的高速缓存持续时间的最大时间（以秒为单位）。 值在标题`Access-Control-Max-Age`中设置。 如果未定义，最大时间设置为1800秒（30分钟）。 |

# 2 单接口跨域支持

如果想要对某一接口配置 `CORS`，可以在方法上添加 `@CrossOrigin` 注解。

默认情况下，`@CrossOrigin`（没有参数）允许在`@RequestMapping`注解中指定的所有源和HTTP方法。

```java
@CrossOrigin
@RequestMapping("/test")
String test() {
    //此处省略N行代码
}
```

有参数情况：

```java
//@CrossOrigin(origins = "http://localhost:9000", maxAge = 3600)
@CrossOrigin(origins = {"http://localhost:9000", "null"})
@RequestMapping("/test")
String test() {
    //此处省略N行代码
}
```

# 3 单Controller类跨域支持

如果想对一系列接口添加 CORS 配置，可以在Controller类上添加`@CrossOrigin`注解，对该类的所有接口都有效。

```java
@CrossOrigin(origins = "http://localhost:8080",maxAge = 3600)
@RestController
public class UserController {
	//省略N行代码
}
```

# 4 全局跨域支持：继承WebMvcConfigurerAdapter

```java
@Configuration
public class WebMvcConfig extends WebMvcConfigurerAdapter {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("*")
                .allowedMethods("POST", "GET", "PUT", "OPTIONS", "DELETE")
                .maxAge(3600)
                .allowCredentials(true);
    }
}
```

# 5 全局跨域支持：定制Filter

```java
@Bean
public FilterRegistrationBean corsFilter() {
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowCredentials(true);	config.addAllowedOrigin("http://localhost:8080");
    config.addAllowedOrigin("null");
    config.addAllowedHeader("*");
    config.addAllowedMethod("*");
    source.registerCorsConfiguration("/**", config); // CORS 配置对所有接口都有效
    FilterRegistrationBean bean = newFilterRegistrationBean(new CorsFilter(source));
    bean.setOrder(0);
    return bean;
}
```

# 6 Spring Security下跨域支持

```java
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
 
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.cors().and()//此处省略N多其他config
    }
 
    @Bean
    CorsConfigurationSource corsConfigurationSource()
    {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(Arrays.asList("https://example.com"));
        configuration.setAllowedMethods(Arrays.asList("GET","POST"));
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}
```

# 7 原理解析

无论是通过哪种方式配置 `CORS`，其实都是在构造 `CorsConfiguration`。 一个 `CORS` 配置用一个 `CorsConfiguration`类来表示，它的配置项如下：

```java
public class CorsConfiguration {
    private List<String> allowedOrigins;
    private List<String> allowedMethods;
    private List<String> allowedHeaders;
    private List<String> exposedHeaders;
    private Boolean allowCredentials;
    private Long maxAge;
}
```

Spring 中对CORS规则的校验，都是通过委托给`org.springframework.web.cors.DefaultCorsProcessor`实现的。

DefaultCorsProcessor 处理过程如下：

```java
@Override
@SuppressWarnings("resource")
public boolean processRequest(@Nullable CorsConfiguration config, HttpServletRequest request, HttpServletResponse response) throws IOException {
	// 判断请求中是否有“Origin”的Header，没有的话，直接返回true
    if (!CorsUtils.isCorsRequest(request)) {
        return true;
    }

    ServletServerHttpResponse serverResponse = new ServletServerHttpResponse(response);
    // 判断响应response中Header是否有“Access-Control-Allow-Origin”，有的话直接返回true
    if (responseHasCors(serverResponse)) {
        logger.debug("Skip CORS processing: response already contains \"Access-Control-Allow-Origin\" header");
        return true;
    }

    ServletServerHttpRequest serverRequest = new ServletServerHttpRequest(request);
    // 判断是否同源，如果是同源，直接返回true
    if (WebUtils.isSameOrigin(serverRequest)) {
        logger.debug("Skip CORS processing: request is from same origin");
        return true;
    }

    boolean preFlightRequest = CorsUtils.isPreFlightRequest(request);
    /*
      判断是否配置了CORS规则：
      	如果没有配置，且是预检请求，则拒绝该请求；
      	如果没有配置，且不是预检请求，则交给负责该请求的类处理。
      	如果配置了，则对该请求进行校验。
    */
    if (config == null) {
        if (preFlightRequest) {
            rejectRequest(serverResponse);
            return false;
        }
        else {
            return true;
        }
    }

    return handleInternal(serverRequest, serverResponse, config, preFlightRequest);
}
```

