# Shell引入脚本

# 1 Shell脚本中引入其他脚本的方法
`.[这是一个空格]other.sh`
```shell
. other.sh
```
或
`source[这是一个空格]other.sh`
```shell
source other.sh
```


# 2 入门案例
test.sh内容：
```shell
#！/bin/bash
echo "第一个脚本"
```


test2.sh的内容：


```shell
#！/bin/bash
. ./test.sh

echo "第二个脚本"
```


测试：


```shell
[zh@zh-inspironn4050 文档]$ bash test2.sh 
第一个脚本
第二个脚本
```


