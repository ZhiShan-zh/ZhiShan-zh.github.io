# Spring Boot 怎么处理异常

# 1 默认异常处理和自定义异常页面

## 1.1 Spring Boot默认异常处理

Spring Boot已经提供了默认的异常处理机制： 一旦程序中出现了异常，Spring Boot请求路径`/error`的URL。Spring Boot中提供了一个异常处理类`org.springframework.boot.autoconfigure.web.servlet.error.BasicErrorController`来处理`/error` 请求，然后跳转到默认显示异常的页面来展示异常信息。

## 1.2 自定义异常页面

如果需要将所有的异常统一跳转到一个自定义的错误页面，一个比较好的方法是利用Spring Boot的默认异常处理Controller来跳转到自定义的错误页面。

这个自定义的错误的页面**路径和名称是固定的**为：`src/main/resources/templates/error.html`

在这个页面中，我们可以显示异常信息，错误页面如下：

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org"></html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>error！！！</title>
    </head>
    <body>
        <!--SpringBoot默认存储异常信息的key为exception-->
        <span th:text="${exception}" />
    </body>
</html>
```

# 2 局部异常处理：`@ExceptionHandler`

**优点**：

- 可以自定义异常类型。
- 可以自定义异常信息存储的key。
- 自定义跳转视图的名称。
- 可以自定义异常信息的显示。

**缺点**：需要编写大量的异常处理方法，异常处理不能跨Controller，如果有另一Controller中出现同样的异常，需要在另一Controller中重新编写异常处理的方法。

```java
@Controller
public class DemoController {
    
	@RequestMapping("/str")
	public String str() {
		String str = null;
		str.length();
		return "index";
	}
	@RequestMapping("/index")
	public String index() {
		int a = 10 / 0;
		return "index";
	}

	/**
	 * @ExceptionHandler的参数value可以自定义异常类型
	 * 参数e：会将产生的异常对象注入到此方法中
	 */
	@ExceptionHandler(value = { java.lang.ArithmeticException.class })
	public ModelAndView arithmeticExceptionHandler(Exception e) {
		ModelAndView modelAndView = new ModelAndView();
		modelAndView.addObject("exception", e.toString());//可以自定义异常信息存储的key
		modelAndView.setViewName("error");//可以自定义异常页面
		return modelAndView;
	}
    // 一个Controller可以有多个异常处理方法
	@ExceptionHandler(value = { java.lang.NullPointerException.class })
	public ModelAndView nullPointerExceptionHandler(Exception e) {
		ModelAndView modelAndView = new ModelAndView();
		modelAndView.addObject("exception", e.toString());//可以自定义异常信息存储的key
		modelAndView.setViewName("error");//可以自定义异常页面
		return modelAndView;
	}
}
```

# 3 全局异常处理：`@ControllerAdvice`/`@RestControllerAdvice`+`@ExceptionHandler`

**优点**：

- 可以处理全局异常；
- 可以自定义异常类型；
- 可以自定义异常信息存储的key；
- 自定义跳转视图的名称；
- 可以自定义异常信息的显示。

**缺点**：编写大量的异常处理方法，代码冗余。

**使用方法**：

1. 定义一个异常处理类，使用`@ControllerAdvice`（或`@RestControllerAdvice`）注解该类；
    1. `@RestControllerAdvice`：统一处理REST接口的异常信息
    2. `@ControllerAdvice`：统一处理异常
2. 在这个类中定义异常处理方法，使用`@ExceptionHandler`注解该方法。

```java
@ControllerAdvice
public class GlobalExceptionController {
	/**
	 * @ExceptionHandler的参数value可以自定义异常类型
	 * 参数e：会将产生的异常对象注入到此方法中
	 */
	@ExceptionHandler(value = { java.lang.ArithmeticException.class })
	public ModelAndView arithmeticExceptionHandler(Exception e) {
		ModelAndView modelAndView = new ModelAndView();
		modelAndView.addObject("exception", e.toString());//可以自定义异常信息存储的key
		modelAndView.setViewName("error");//可以自定义异常页面
		return modelAndView;
	}
    // 一个Controller可以有多个异常处理方法
	@ExceptionHandler(value = { java.lang.NullPointerException.class })
	public ModelAndView nullPointerExceptionHandler(Exception e) {
		ModelAndView modelAndView = new ModelAndView();
		modelAndView.addObject("exception", e.toString());//可以自定义异常信息存储的key
		modelAndView.setViewName("error");//可以自定义异常页面
		return modelAndView;
	}
}
```

# 4 简单全局异常处理：SimpleMappingExceptionResolver

**优点**：

- 可以处理全局异常；
- 可以配置多个异常类型和异常视图名称对。

**缺点**：

- 不能显示具体异常信息。

**使用方法**：

1. 对SimpleMappingExceptionResolver进行自定义配置：
    - 配置多个异常类型和异常页面对。
2. 将SimpleMappingExceptionResolver类注入到Spring容器中。

```java
package com.zh.springboot.exception;

import java.util.Properties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.handler.SimpleMappingExceptionResolver;

@Configuration//表明该类是一个配置类
public class GlobalException {
	
	@Bean//bean的注入
	public SimpleMappingExceptionResolver getSimpleMappingExceptionResolver(){
		SimpleMappingExceptionResolver resolver = new SimpleMappingExceptionResolver();
		Properties mappings = new Properties();

        //参数一：异常的类型，注意必须是异常类型的全名
        //参数二：视图名称
		mappings.put("java.lang.ArithmeticException", "error1");
		mappings.put("java.lang.NullPointerException", "error2");
		
		//把异常与视图映射信息配置到SimpleMappingExceptionResolver中
		resolver.setExceptionMappings(mappings);
		return resolver;
	}
}
```

# 5 自定义全局异常处理：实现`HandlerExceptionResolver`接口

**优点**：

- 可以处理全局异常；
- 可以根据不同的异常类型跳转不同的视图；
- 可以自定义异常信息的显示。

使用步骤：

1. 自定义全局异常处理类，并实现接口`org.springframework.web.servlet.HandlerExceptionResolver`；
2. 使用注解`@Configuration`声明该类；
3. 实现HandlerExceptionResolver的`public ModelAndView resolveException(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)`的方法。

```java
package com.zh.springboot.exception;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.HandlerExceptionResolver;
import org.springframework.web.servlet.ModelAndView;

@Configuration//表明该类是一个配置类
public class MyHandlerExceptionResolver implements HandlerExceptionResolver {
	@Override
	public ModelAndView resolveException(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
		ModelAndView modelAndView = new ModelAndView();
		// 可以自定义异常信息
		modelAndView.addObject("exception", "自定义异常信息");
		//可以根据不同类型异常，跳转不同异常视图
		if(ex instanceof ArithmeticException){
			modelAndView.setViewName("error1");
		}else if(ex instanceof NullPointerException){
            modelAndView.setViewName("error2");
        }else{
            modelAndView.setViewName("error");
        }
		return modelAndView;
	}
}

```

