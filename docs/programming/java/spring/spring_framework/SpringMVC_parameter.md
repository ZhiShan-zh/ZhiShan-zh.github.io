# SpringMVC中的参数传递

# 1 前端参数传递给后端

## 1.1 简单参数传递给后端

### 1.1.1 使用多个形参接收简单类型参数

请求：`.html`为自定义请求后缀。

```
### 使用简单数据类型请求
GET http://localhost:8080/springmvc/simpleParameters.html?name=name&num=2&price=5.1&isValid=true
```

controller:

```java
@RequestMapping("/simpleParameters")
public ModelAndView testStringParameters(String name, int num, double price, boolean isValid){
    ModelAndView modelAndView = new ModelAndView();
    // 将放回给页面的数据放入Model中
    modelAndView.addObject("name", name);
    modelAndView.addObject("num", num);
    modelAndView.addObject("price", price);
    modelAndView.addObject("isValid", isValid);
    // 将页面的地址放入view中
    modelAndView.setViewName("parameter/simple");
    return modelAndView;
}
```

### 1.1.2 使用对象接受简单类型参数

bean：

```java
public class Goods {
    private String name;
    private int num;
    private double price;
    private boolean isValid;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getNum() {
        return num;
    }

    public void setNum(int num) {
        this.num = num;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public boolean isValid() {
        return isValid;
    }

    public void setValid(boolean valid) {
        isValid = valid;
    }
}
```

controller：

```java
@RequestMapping("/simpleParameters")
public ModelAndView testStringParameters(Goods goods){
    ModelAndView modelAndView = new ModelAndView();
    // 将放回给页面的数据放入Model中
    modelAndView.addObject("goods", goods);
    // 将页面的地址放入view中
    modelAndView.setViewName("parameter/simple");
    return modelAndView;
}
```

### 1.1.3 使用字典接受多个简单类型参数

```java
@RequestMapping("/simpleParameters")
public ModelAndView testStringParameters(@RequestParam Map params){
    ModelAndView modelAndView = new ModelAndView();
    // 将放回给页面的数据放入Model中
    modelAndView.addObject("params", params);
    // 将页面的地址放入view中
    modelAndView.setViewName("parameter/simple");
    return modelAndView;
}
```

如果要使用map接受参数，则需要在此形参前边加上注解`@RequestParam`，并且map中的值都为字符串。

## 1.2 接受数组类型参数

```
### 数组类型POST
POST http://localhost:8080/springmvc/testArrayParameter.html
Content-Type: application/x-www-form-urlencoded

goods=name&goods=2&goods=5.1&goods=true

### 数组类型GET
GET http://localhost:8080/springmvc/testArrayParameter.html?goods=name&goods=2&goods=5.1&goods=true
```

controller:

```java
@RequestMapping("/testArrayParameter")
public ModelAndView testArrayParameter(String[] goods){
    ModelAndView modelAndView = new ModelAndView();
    // 将放回给页面的数据放入Model中
    modelAndView.addObject("goods", goods);
    // 将页面的地址放入view中
    modelAndView.setViewName("parameter/simple");
    return modelAndView;
}
```

## 1.3 接受请求路径上的参数

请求：

```
### 路径参数
GET http://localhost:8080/springmvc/pathParameter/name/2.html
```

controller

```java
@RequestMapping("/pathParameter/{name}/{num}")
public ModelAndView testStringParameters(@PathVariable String name, @PathVariable int num){
    ModelAndView modelAndView = new ModelAndView();
    // 将页面的地址放入view中
    modelAndView.setViewName("parameter/simple");
    return modelAndView;
}
```

## 1.4 时间类型参数

### 1.4.1 单字段转换时间String为Date

- 支持路径参数
- 支持普通传参方式
- 支持对象中的属性值

1. 在springmvc配置文件中开启注解扫描

   ```xml
   <!-- 开启注解 -->
   <mvc:annotation-driven />
   ```

2. 在需要进行转换的字段上使用

```java
@RequestMapping("/pathParameter/{date}")
public ModelAndView testStringParameters(@PathVariable @DateTimeFormat(pattern = "yyyy-MM-dd HH:mm:ss") Date date){
    ModelAndView modelAndView = new ModelAndView();
    // 将页面的地址放入view中
    modelAndView.setViewName("parameter/simple");
    return modelAndView;
}
```

### 1.4.2 局部（单个controller类）转换时间String为Date

- 支持路径参数
- 支持普通传参方式
- 支持对象中的属性值

下边已路径参数为例说明：

请求：

```
### 路径参数-时间类型
GET http://localhost:8080/springmvc/pathParameter/2020-08-20 20:20:20.html
```

controller:

```java
@Controller
public class SimpleParameterController {

    @InitBinder
    public void initBinder(WebDataBinder binder, WebRequest request) {
        //转换日期 注意这里的转化要和传进来的字符串的格式一直 如2015-9-9 就应该为yyyy-MM-dd
        DateFormat dateFormat=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        binder.registerCustomEditor(Date.class, new CustomDateEditor(dateFormat, true));// CustomDateEditor为自定义日期编辑器
    }

    @RequestMapping("/pathParameter/{date}")
    public ModelAndView testStringParameters(@PathVariable Date date){
        ModelAndView modelAndView = new ModelAndView();
        // 将页面的地址放入view中
        modelAndView.setViewName("parameter/simple");
        return modelAndView;
    }
}
```

### 1.4.3 全局转换时间String为Date

- 支持路径参数
- 支持普通传参方式
- 支持对象中的属性值

全局时间转换器：

```java
package com.lifeng.springmvc.parameter.simple.config;


import org.springframework.core.convert.converter.Converter;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class DateConverter implements Converter<String, Date> {
    @Override
    public Date convert(String source) {
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

        //设置不会对日期进行计算
        simpleDateFormat.setLenient(false);

        try {
            return simpleDateFormat.parse(source);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return null;
    }
}
```

在SpringMVC配置文件中配置全局时间转换器（`spring-mvc.xml`）：

```xml
<!--配置注解处理器适配器-->
<mvc:annotation-driven conversion-service="conversionService"></mvc:annotation-driven>
<!--配置自定义日期转换器，并且在mvc:annotation-driven 标签中加上conversion-service属性-->
<bean id="conversionService" class="org.springframework.format.support.FormattingConversionServiceFactoryBean">
    <property name="converters">
        <list>
            <bean class="com.lifeng.springmvc.parameter.simple.config.DateConverter"></bean>
        </list>
    </property>
</bean>
```

## 1.5 `@RequestParam`和`@RequestBody`注解的使用

### 1.5.1 `@RequestParam`

**作用**：

- 将请求参数绑定到你控制器的方法参数上（是springmvc中接收普通参数的注解）
- 用来处理`Content-Type`为`application/x-www-form-urlencoded`编码的内容，`Content-Type`默认为该属性。

**接受数据类型**：简单类型和对象类型。

**语法**：`@RequestParam(value="参数名",required="true/false",defaultValue="")`

- `value`：参数名，指定该注解的形参接受的参数的key名称，如果指定该值，则会忽略形参名。
- `required`：是否包含该参数，默认为true，表示该请求路径中必须包含该参数，如果不包含就报错。
- `defaultValue`：默认参数值，如果设置了该值，required=true将失效，自动为false,如果没有传该参数，就使用默认值

### 1.5.2 `@RequestBody`

- 注解@RequestBody接收的参数是**来自requestBody**中，即**请求体**。一般用于处理非 `Content-Type: application/x-www-form-urlencoded`编码格式的数据，比如：`application/json`、`application/xml`等类型的数据。
  - GET方式无请求体，所以使用``@RequestBody`接收数据时，前端不能使用GET方式提交数据，而是用POST方式进行提交。
- 在后端的同一个接收方法里，`@RequestBody`与`@RequestParam()`可以同时使用，`@RequestBody`最多只能有一个，而`@RequestParam()`可以有多个。
- 当同时使用`@RequestParam()`和`@RequestBody`时，`@RequestParam()`指定的参数可以是普通元素、数组、集合、对象等等
  - 当`@RequestBody` 与`@RequestParam()`可以同时使用时，原SpringMVC接收参数的机制不变，只不过`@RequestBody` 接收的是请求体里面的数据；而`@RequestParam`接收的是key-value里面的参数，所以它会被切面进行处理从而可以用普通元素、数组、集合、对象等接收。
  - 如果参数时放在请求体中，传入后台的话，那么后台要用`@RequestBody`才能接收到；如果不是放在请求体中的话，那么后台接收前台传过来的参数时，要用`@RequestParam`来接收，或则形参前
           什么也不写也能接收。
- Content-Type为`application/json`时：
  - 后台在接收JSON数据的时候一定要用自定义的对象或者Map对象去接收，不要用JDK中的简单对象(String/Integer/Long)来接收。
  - 会根据json字符串中的key来匹配对应实体类的属性，如果匹配一致且json中的该key对应的值符合(或可转换为)实体类的对应属性的类型要求时，会调用实体类的setter方法将值赋给该属性。
  - json字符串中，如果value为""的话，后端对应属性如果是String类型的，那么接受到的就是""，如果是后端属性的类型是Integer、Double等类型，那么接收到的就是null。
  - json字符串中，如果value为null的话，后端对应收到的就是null。
  - 如果某个参数没有value的话，在传json字符串给后端时，要么干脆就不把该字段写到json字符串中；要么写value时， 必须有值，null  或""都行
  - 属性注解`@JsonProperty`和`@JsonAlias`的区别
    - `@JsonProperty`
      - 这个注解提供了序列化和反序列化过程中该java属性所对应的名称。
      - Json-->bean和bean-->Json中Json中的key都由注解规定。
    - `@JsonAlias`
      - 这个注解只只在反序列化时起作用，指定该java属性可以接受的更多名称。
      - Json-->bean时Json的key由注解规定。
      - bean-->Json时Json的key有getter规定。

## 1.6 文件类型参数接收（TODO）

超大大文件（支持断点续传）：

- 编码
- 分割

## 1.7 SpringMVC接收和处理参数的流程（TODO）

# 2 给前端返回数据（TODO）