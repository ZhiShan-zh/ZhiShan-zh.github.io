#!/usr/bin/python
# _*_ coding:UTF-8 _*_
import os
import re
import traceback

current_path = os.getcwd()
docx_path = os.path.join(current_path, "docs")

def loop_path(path):
    """
    遍历目录，如果特定文件（以.md为后缀的文件）的话调用loop_file_media来处理
    :param path: 绝对路径
    :return:
    """
    if os.path.isdir(path):
        for x in os.listdir(path):
            sub_path = os.path.join(path, x)
            if os.path.isdir(sub_path):
                loop_path(sub_path)
            else:
                try:
                    if sub_path.lower().endswith(".md"):
                        loop_file_media(path, sub_path)
                        print("操作文件成功：" + sub_path)
                    else:
                        print("跳过文件：" + sub_path)
                except Exception as e:
                    print("操作文件出错：" + sub_path)
                    traceback.print_exc()

def loop_file_media(dir_path:str, file_path):
    """
    以行为单位遍历文件，如果行包含网络图片地址，则把图片从根目录中media文件夹从移动到文件所在目录的media文件夹中
    :param dir_path: 文件所在目录的绝对路径
    :param file_path: 文件的绝对路径
    :return:
    """
    if os.path.isdir(file_path):
        loop_path(file_path)
    if not os.path.isdir(dir_path):
        return
    dir_path_unix_sep = dir_path.replace(current_path + os.sep, "").replace(os.sep, "/") # 基于根路径项相对路径，路径分隔符统一为/
    file_content = ""
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in f:
            searchObj = re.search(r'.*!{1}\[{1}.*\]{1}\({1}https?://.*media/(.*)\.{1}(\w+)\){1}', line)
            if searchObj is not None:
                media_name = searchObj.group(1)  # 媒体文件名，不带后缀，如java_session-a1af-0ae08d9cc035
                media_suffix = searchObj.group(2)  # 媒体文件后缀，如png
                if not os.path.exists(dir_path + os.sep + "media"):
                    os.mkdir(dir_path + os.sep + "media")
                media_target_relative_path = dir_path_unix_sep + "/media/" + media_name # 目标相对路径
                media_target_absolute_path = dir_path + os.sep + "media" + os.sep + media_name + "." + media_suffix # 目标文件绝对路径
                media_source_absolute_path = current_path + os.sep + "media" + os.sep + media_name + "." + media_suffix # 源文件绝对路径
                if os.path.exists(media_source_absolute_path) and os.path.exists(media_target_absolute_path):
                    media_target_relative_path += "_1." + media_suffix  # 目标相对路径
                else:
                    media_target_relative_path += "." + media_suffix  # 目标相对路径
                # 使用git mv命令移动文件
                git_command = "git mv media/" + media_name + "." + media_suffix + " " + media_target_relative_path
                if not os.path.exists(media_source_absolute_path) or os.system(git_command) == 0:# 文件移动成功，则改变文本中标识的文件路径为相对路径
                    to_replace_str = re.search(r'.*!{1}\[{1}.*\]{1}\({1}(https?://.*media/.*\.{1}\w+)\){1}',
                                               line).group(1)
                    line = line.replace(to_replace_str, "./media/" + media_name + "." + media_suffix)
            file_content += line
    with open(file_path, 'w', encoding="utf-8") as f:
        if file_content is not None and file_content != "":
            f.write(file_content)

if __name__ == "__main__":
    loop_path(docx_path)
    # line = "![](https://ZhiShan-zh.github.io/media/springboot_shiro_20210114152559.jpg)"
    # searchObj = re.search(r'.*!{1}\[{1}.*\]{1}\({1}https?://.*media/(.*)\.{1}(\w+)\){1}', line)
    # media_name = searchObj.group(1)  # 媒体文件名，不带后缀，如java_session-a1af-0ae08d9cc035
    # media_suffix = searchObj.group(2)  # 媒体文件后缀，如png
    # media_source_absolute_path = current_path + os.sep + "media" + os.sep + media_name + "." + media_suffix
    # print(media_source_absolute_path)
    # if os.path.exists(media_source_absolute_path):
    #     print(media_name)
    #     print(media_suffix)