# SpringMVC入门

# 1 SpringMVC概述


## 1.1 什么是SpringMVC


SpringMVC是spring组织出品的一个前端表现层框架


## 1.2 SpringMVC的作用


- 接收请求中的参数
- 将处理好的数据返回给页面



## 1.3 SpringMVC处理流程


![springmvc1.png](https://zhishan-zh.github.io/media/1586166588890-d29ca180-2447-4a2b-8676-f6b1aebcd167.png)


## 1.4 SpringMVC和Struts2对比


- springmvc的入口是一个servlet即前端控制器，而struts2入口是一个filter过虑器。
- springmvc是基于方法开发(一个url对应一个方法)，请求参数传递到方法的形参，可以设计为单例或多例(建议单例)，struts2是基于类开发，传递参数是通过类的属性，只能设计为多例。
  - springMvc使用方法级别的局部变量来接收参数, 由于局部变量用完就销毁, 所以线程安全, 所以springMvc中的controller使用的是单例
- Struts采用值栈存储请求和响应的数据，通过OGNL存取数据，springmvc通过参数解析器是将request请求内容解析，并给方法形参赋值，将数据和视图封装成ModelAndView对象，最后又将ModelAndView中的模型数据通过request域传输到页面。Jsp视图解析器默认使用jstl。



# 2 SpringMVC入门案例


## 2.1 新建Dynamic Web project

![javawebproject1.png](https://zhishan-zh.github.io/media/1586166603219-bca5d5c3-1bf9-4b04-a289-1f1a24b981fc.png)
![javawebproject2.png](https://zhishan-zh.github.io/media/1586166620775-e96aef73-5022-4e18-a1e8-40e90e39fcd3.png)
![javawebproject3.png](https://zhishan-zh.github.io/media/1586166696642-b69d11b8-a48d-4010-8c29-873ae5b8e2e0.png)


## 2.2 导包


导包位置：`/springmvc/WebContent/WEB-INF/lib`


- `commons-logging-1.1.1.jar`
- `jstl-1.2.jar`
- `spring-aop-4.2.4.RELEASE.jar`
- `spring-aspects-4.2.4.RELEASE.jar`
- `spring-beans-4.2.4.RELEASE.jar`
- `spring-context-4.2.4.RELEASE.jar`
- `spring-context-support-4.2.4.RELEASE.jar`
- `spring-core-4.2.4.RELEASE.jar`
- `spring-expression-4.2.4.RELEASE.jar`
- `spring-jdbc-4.2.4.RELEASE.jar`
- `spring-jms-4.2.4.RELEASE.jar`
- `spring-messaging-4.2.4.RELEASE.jar`
- `spring-tx-4.2.4.RELEASE.jar`
- `spring-web-4.2.4.RELEASE.jar`
- `spring-webmvc-4.2.4.RELEASE.jar`



## 2.3 jsp页面


```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt"  prefix="fmt"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
</head>
<body>
	<c:forEach items="${itemList }" var="item">
		<tr>
			<td>${item.name }</td>
			<td>${item.price }</td>
			<td><fmt:formatDate value="${item.createtime}" pattern="yyyy-MM-dd HH:mm:ss"/></td>
			<td>${item.detail }</td>
			<!--省略-->
			<td><a href="${pageContext.request.contextPath }/toEdit.action?id=${item.id}">修改</a></td>
		</tr>
	</c:forEach>
</body>
</html>
```


## 2.4 entity


```java
package com.zh.springmvc.entity;

import java.util.Date;

public class Items {
	private Integer id;
	private String name;
	private double price;
	private Date createtime;
	private String detail;
	public Items() {
		super();
	}
	public Items(Integer id, String name, double price, Date createtime, String detail) {
		super();
		this.id = id;
		this.name = name;
		this.price = price;
		this.createtime = createtime;
		this.detail = detail;
	}
	public Integer getId() {
		return id;
	}
	public void setId(Integer id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public double getPrice() {
		return price;
	}
	public void setPrice(double price) {
		this.price = price;
	}
	public Date getCreatetime() {
		return createtime;
	}
	public void setCreatetime(Date createtime) {
		this.createtime = createtime;
	}
	public String getDetail() {
		return detail;
	}
	public void setDetail(String detail) {
		this.detail = detail;
	}
}
```


## 2.5 controller


```java
package com.zh.springmvc.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.zh.springmvc.entity.Items;
import com.zh.springmvc.service.ItemsService;

@Controller
public class ItemsController {
	@Autowired
	private ItemsService itemsService;

	@RequestMapping("/list")
	public ModelAndView list() throws Exception {
		List<Items> itemsList = itemsService.findItemsList();

		ModelAndView modelAndView = new ModelAndView();
		// 将放回给页面的数据放入Model中
		modelAndView.addObject("itemList", itemsList);
		// 将页面的地址放入view中
		modelAndView.setViewName("itemList");
		return modelAndView;
	}
}
```


## 2.6 service


```java
package com.zh.springmvc.service;

import java.util.List;

import com.zh.springmvc.entity.Items;

public interface ItemsService {
	List<Items> findItemsList();
}
```


```java
package com.zh.springmvc.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.zh.springmvc.dao.ItemsDao;
import com.zh.springmvc.entity.Items;
import com.zh.springmvc.service.ItemsService;

@Service
public class ItemsServiceImpl implements ItemsService{
	@Autowired
	public ItemsDao itemsDao;
	
	@Override
	public List<Items> findItemsList() {
		return itemsDao.findItemsList();
	}
}
```


## 2.7 dao


```java
package com.zh.springmvc.dao;

import java.util.List;

import com.zh.springmvc.entity.Items;

public interface ItemsDao {
	List<Items> findItemsList();
}
```


```java
package com.zh.springmvc.dao.impl;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.springframework.stereotype.Repository;

import com.zh.springmvc.dao.ItemsDao;
import com.zh.springmvc.entity.Items;

@Repository
public class ItemsDaoImpl implements ItemsDao{
	private static List<Items> list = new ArrayList<>();
	static {
		list.add(new Items(1, "华为Mate40", 9999.99, new Date(), "强大的手机"));
		list.add(new Items(2, "荣耀9X", 1999.99, new Date(), "不错的手机"));
	}

	@Override
	public List<Items> findItemsList() {
		return list;
	}
}
```


## 2.8 springmvc.xml


位置：`/springmvc/src/springmvc.xml`


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:p="http://www.springframework.org/schema/p"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:dubbo="http://code.alibabatech.com/schema/dubbo"
	xmlns:mvc="http://www.springframework.org/schema/mvc"
	xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.0.xsd
        http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc-4.0.xsd
        http://code.alibabatech.com/schema/dubbo http://code.alibabatech.com/schema/dubbo/dubbo.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.0.xsd">
	<!-- 开启注解扫描 -->
	<context:component-scan
		base-package="com.zh.springmvc" />
	<!-- 视图解析器 -->
	<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
		<property name="viewClass"
			value="org.springframework.web.servlet.view.JstlView" />
		<!-- 前缀，注意配置中的“/” -->
		<property name="prefix" value="/WEB-INF/jsp/" />
		<!-- 后缀 -->
		<property name="suffix" value=".jsp" />
	</bean>
</beans>
```


## 2.9 web.xml


位置：`/springmvc/WebContent/WEB-INF/web.xml`


```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns="http://java.sun.com/xml/ns/javaee"
	xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
	id="WebApp_ID" version="2.5">
	<display-name>springmvc</display-name>
	<welcome-file-list>
		<welcome-file>index.html</welcome-file>
		<welcome-file>index.htm</welcome-file>
		<welcome-file>index.jsp</welcome-file>
		<welcome-file>default.html</welcome-file>
		<welcome-file>default.htm</welcome-file>
		<welcome-file>default.jsp</welcome-file>
	</welcome-file-list>
	<!-- 配置SpringMvc前端控制器 -->
	<servlet>
		<servlet-name>springMvc</servlet-name>
		<servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
		<init-param>
			<param-name>contextConfigLocation</param-name>
			<param-value>classpath:springmvc.xml</param-value>
		</init-param>
		<load-on-startup>1</load-on-startup>
	</servlet>

	<servlet-mapping>
		<servlet-name>springMvc</servlet-name>
		<url-pattern>*.action</url-pattern>
	</servlet-mapping>
</web-app>
```


## 2.10 测试


1. 把项目springmvc加入到tomcat中

![springmvcservers1.png](https://zhishan-zh.github.io/media/1586166737050-45886820-2698-4acc-96f8-a5089ef965a7.png)
![springmvcservers2.png](https://zhishan-zh.github.io/media/1586166748549-3fbf6c00-9530-4e4b-a58e-30ec3b182757.png)
![springmvcservers3.png](https://zhishan-zh.github.io/media/1586166762023-15ab71a3-94f0-4c55-8079-2ce196c043da.png)
![springmvcservers4.png](https://zhishan-zh.github.io/media/1586166773805-681d004d-6830-437e-b532-1272d536e948.png)

2. 启动项目:debug或Run



![startwebproject.png](https://zhishan-zh.github.io/media/1586166814428-b8b0a56b-fc34-4c4a-bab4-0d442650a4fc.png)

3. 测试项目：在浏览器访问测试接口（http://localhost:8080/springmvc/list.action）

![testwebproject.png](https://zhishan-zh.github.io/media/1586166846459-e6784111-b415-4601-b775-10d179e8a8b9.png)
