#!/usr/bin/python
# _*_ coding:UTF-8 _*_
import os

current_path = os.getcwd()
def mkdir_empty_sidebarFile(path):
    sidebar_path = os.path.join(path, "_sidebar.md")
    if not os.path.exists(sidebar_path):
        f = open(sidebar_path,'w')
        f.close()
        print("创建文件：" + sidebar_path)
    if os.path.isdir(path):
        for x in os.listdir(path):
             sub_path = os.path.join(path, x)
             if os.path.isdir(sub_path):
                 mkdir_empty_sidebarFile(sub_path)

if __name__=="__main__":
    mkdir_empty_sidebarFile(os.path.join(current_path, "docs"))