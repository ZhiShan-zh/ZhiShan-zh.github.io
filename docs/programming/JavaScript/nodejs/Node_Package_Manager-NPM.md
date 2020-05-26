# NodeJS包资源管理器NPM

# 1 概述

npm全称Node Package Manager，他是node包管理和分发工具。
通过npm可以很方便地下载js库和管理前端工程。

# 2 NPM命令

## 2.1 初始化工程

init命令是工程初始化命令。

建立一个空文件夹，在终端中进入该文件夹，然后执行工程初始化命令：`npm init`；

按照提示输入相关信息，如果是用默认值则直接回车即可。

- name: 项目名称
- version: 项目版本号
- description: 项目描述
- keywords: {Array}关键词，便于用户搜索到我们的项目

最后会生成`package.json`文件，这个是包的配置文件，相当于maven的`pom.xml`
我们之后也可以根据需要进行修改。

## 2.2 本地安装

install命令用于安装某个模块，会将js库安装在当前目录。

- 比如安装express模块（node的web框架）：`npm install express`
- 出现黄色的是警告信息，可以忽略，请放心，你已经成功执行了该命令。
- 在该目录下会出现一个`node_modules`文件夹和`package-lock.json`文件。
  - `node_modules`：文件夹，用于存放下载的js库（相当于maven的本地仓库）
  - `package-lock.json`：是当`node_modules`或`package.json`发生变化时自动生成的文件。
    - 这个文件主要功能是确定当前安装的包的依赖，以便后续重新安装的时候生成相同的依赖，而忽略项目开发过程中有些依赖已经发生的更新。
- 我们再打开package.json文件，发现刚才下载的express已经添加到依赖列表中了



关于版本号定义：

- 指定版本：比如1.2.2，遵循“大版本.次要版本.小版本”的格式规定，安装时只安装指定版
  本。
- 波浪号（`~`）+ 指定版本：安装时不改变大版本号和次要版本号
  - 比如~1.2.2，表示安装1.2.x的最新版本（不低于1.2.2），但是不安装1.3.x。
- 插入号（`^`）+ 指定版本：安装时不改变大版本号
  - 比如ˆ1.2.2，表示安装1.x.x的最新版本（不低于1.2.2），但是不安装2.x.x.
  - 需要注意的是，如果大版本号为0，则插入号的行为与波浪号相同，这是因为此时处于开发阶段，即使是次要版本号变动，也可能带来程序的不兼容。
- latest：安装最新版本。

## 2.3 全局安装

全局安装会将库安装到你的全局目录下。

- 查看全局目录位置：`npm root ‐g`

- 全局安装命令：`npm install package_name ‐g`
  - 比如全局安装jquery：`npm install jquery ‐g`

## 2.4 批量下载

我们从网上下载某些代码，发现只有`package.json`，没有node_modules文件夹，这时我
们需要通过命令重新下载这些js库。
进入目录（package.json所在的目录）输入命令`npm install`，此时，npm会自动下载`package.json`中依赖的js库。

## 2.6 淘宝NPM镜像

有时我们使用npm下载资源会很慢，所以我们可以安装一个cnpm（淘宝镜像）来加快下载
速度。

输入命令（`npm install ‐g cnpm ‐‐registry=https://registry.npm.taobao.org`），进行全局安装淘宝镜像。

安装后，我们可以使用命令（`cnpm ‐v`）来查看cnpm的版本

使用cnpm：`cnpm install 需要下载的js库`

## 2.7 运行工程

使用run命令运行某个工程。

如果`package.json`中定义的脚本如下

- dev是开发阶段测试运行
- build是构建编译工程
- lint 是运行js代码检测

我们现在来试一下运行dev：`npm run dev`

## 2.8 编译工程

因为编译后的代码会放在dist文件夹中，所以首先我们需要先删除dist文件夹中的文件，然后进入终端输入命令`npm run build`来编译代码。这其实是调用webpack来实现打包的。

编译后我们就可以将工程部署到nginx中。


生成后我们会发现只有个静态页面和一个static文件夹，这种工程我们称之为单页Web应用（single page web application，SPA），就是只有一张Web页面的应用，是加载单个HTML 页面并在用户与应用程序交互时动态更新该页面的Web应用程序。
