# Maven错误文件清理工具（Pyhton实现）

使用方法：`python clean_repository_maven D:\programs\maven\respository\.m2\repo_kstore `

文件名：`clean_repository_maven`

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import os.path

if len(sys.argv) >= 2:
    path = sys.argv[1]
else:
    path = os.getcwd()

path = path.replace("\\", "/")# 替换windows路径分隔符

def clean_file(path):
    """
    清理maven错误文件
    :param path: 待请立文件或目录的路径
    :return:
    """
    if os.path.isfile(path):
        path_split = os.path.split(path)  # 分割出目录与文件
        file_split = path_split[1].split('.')  # 分割出文件与文件扩展名
        if file_split[1] and ("lastUpdated" in file_split or "repositories" in file_split):
            os.remove(path)
            print("删除文件：" + path)
    elif os.path.isdir(path):
        for x in os.listdir(path):
            clean_file(os.path.join(path, x))  # os.path.join()在路径处理上很有用
print("开始清理maven仓库目录：" + path)
clean_file(path)
```

