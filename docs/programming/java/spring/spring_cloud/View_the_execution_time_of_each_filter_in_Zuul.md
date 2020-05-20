# 查看Zuul中每个过滤器的执行耗时

只需开启Zuul的Debug功能，则可查看Zuul中经过的每个过滤器的执行耗时。

# 1 开启Debug

yml配置文件增加配置：

```yaml
zuul:
  include-debug-header: true
management:
  endpoints:
    web:
      exposure:
        include: '*'
```

使用方法：

- 访问Zuul的接口的时候，后边增加`?debug=true`即可。
- 示例：`http://localhost:8080/zuul/provider/findall?debug=true`

查看请求过滤器耗时：

- `http://localhost:8080/actuator/httptrace`

# 2 去除debug尾巴

yml配置中增加：

```yaml
zuul:
  debug:
    request: true
```

这样，即使不添加debug=true ，Zuul也会Debug。