# Spring技术栈简介

**Spring 框架**就像一个家族，有众多衍生产品例如 boot、security、jpa等等；但他们的基础都是Spring 的ioc和 aop，ioc 提供了依赖注入的容器， aop解决了面向切面编程，然后在此两者的基础上实现了其他延伸产品的高级功能。

**Spring MVC**提供了一种轻度耦合的方式来开发web应用；它是Spring的一个模块，是一个web框架；通过DispatcherServlet, ModelAndView 和 View Resolver，开发web应用变得很容易；解决的问题领域是网站应用程序或者服务开发——URL路由、Session、模板引擎、静态Web资源等等。

**Spring Boot**实现了auto-configuration**自动配置**（另外三大神器actuator监控，cli命令行接口，starter依赖），降低了项目搭建的复杂度。它主要是为了解决使用Spring框架需要进行大量的配置太麻烦的问题，所以它并不是用来替代Spring的解决方案，而是和Spring框架紧密结合用于提升Spring开发者体验的工具；同时它集成了大量常用的第三方库配置(例如Jackson, JDBC, Mongo, Redis, Mail等等)，Spring Boot应用中这些第三方库几乎可以零配置的开箱即用(out-of-the-box)。

 

所以，用最简练的语言概括就是:

- Spring 是一个“引擎”;
- Spring MVC 是基于Spring的一个 MVC 框架;
- Spring Boot 是基于Spring4的条件注册的一套快速开发整合包。