# pip

# 1 换源

## 1.1 类linux系统

1. 切换到家目录：`cd ~`
2. 创建文件夹`.pip`：`mkdir .pip`
3. 在`.pip`文件夹下创建pip的配置文件`pip.conf`，输入一下内容并保存。

```
[global] 
index-url = http://mirrors.aliyun.com/pypi/simple/
[install] 
trusted-host=mirrors.aliyun.com
```

## 1.2 windows系统
1. 在当前用户目录下新建目录pip：如`C:\Users\xx\pip`（xx是当前用户的用户名）
2. 在新建的pip目录中新建文件`pip.ini`（路径为：`C:\Users\xx\pip\pip.ini`），输入一下内容并保存。

```
[global] 
index-url = http://mirrors.aliyun.com/pypi/simple/
[install] 
trusted-host=mirrors.aliyun.com
```



