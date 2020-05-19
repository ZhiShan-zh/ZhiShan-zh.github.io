# 负载均衡算法——Nginx

负载均衡用来解决用户请求到来时如何选择upstream server进行处理，Nginx默认采用的是round-robin（轮询）

，同时支持以下几种算法：

# 1 `round-robin`

`round-robin`：轮询，默认的负载均衡算法，即以轮询的方式将请求转发到上游服务器，通过配置weight配置可以实现基于权重的轮询。

# 2 `ip_hash`

根据客户IP进行负载均衡，即相同的IP将负载均衡到同一个upstream server。

```
upstream backend {
	ip_hash;
	server 192.168.61.1.9080 weight=1;
	server 192.168.61.1.9090 weight=2;
}
```

# 3 `hash key [consistent]`

对某一个key进行哈希或者使用一致性哈希算法进行负载均衡。使用Hash算法进行存在的问题是，当添加/删除一台服务器时，将导致很多key被重新均衡到不同的服务器（从而导致后端可能出现问题）；因此建议使用一致性哈希算法，这样当添加/删除一台服务器时，只有少数的key将被重新负载均衡到不同的服务器。

## 3.1 哈希算法

此处是根据uri进行负载均衡，可以使用Nginx变量，因此，可以实现复杂的算法。

```
upstream backend {
	hash $uri;
	server 192.168.61.1.9080 weight=1;
	server 192.168.61.1.9090 weight=2;
}
```

## 3.2 一致性哈希算法

consistent_key动态指定：

```
upstream nginx_local_server {
	hash $consistent_key consistent;
	server 192.168.61.1.9080 weight=1;
	server 192.168.61.1.9090 weight=2;
}
```

如下location指定了一致性哈希key，此处会优先考虑请求参数cat（类目），如果没有，则再根据请求uri进行负载均衡。

```
location / {
	set $consistent_key $arg_cat;
	if($consistent_key = "") {
		set $consistent_key $request_uri;
	}
}
```

而实际我们是通过Lua设置一致性哈希key。

```
set_by_lua_file $consistent_key "lua_balancing.lua"
```

`lua_balancing.lua`代码：

```lua
local consistent_key = args.cat
if not consistent_key or consistent_key == '' then
    consistent_key = ngx_var.request_uri
end

local value = balancing_cache:get(consistent_key)
if not value then
    success, err = balancing_cache:set(consistent_key, 1, 60)
else
    newval, err = balancing_cache:incr(consistent_key, 1)
end
```

如果某一个分类请求量太大，上游服务器可能处理不了这么多的请求，此时可以在一致性哈希key后加上递增的技术以实现类似轮询的算法。

```lua
if newval > 5000 then
	consistent_key = consistent_key .. '_' .. newval
end
```

# 4 least_conn

将请求负载均衡到最少活跃连接的上游服务器。如果配置的服务器较少，则将转而使用基于权重的轮询算法。

# 5 least_time

Nginx商业版还提供了least_time，即基于最小响应时间进行负载均衡。

