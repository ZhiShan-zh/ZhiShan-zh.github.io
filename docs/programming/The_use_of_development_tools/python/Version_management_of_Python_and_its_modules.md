# Python及其模块版本控制

# 1 python版本控制
## 1.1 pyenv
由于 python 拥有众多的版本，以及不同模块也有不同的版本。如果每个版本之间相互都不兼容那也就无所谓什么版本控制了，可是同一机器上各个版本的 python 可以相互兼容并存，而且同一模块不同版本有时需要的 python 版本是不相同的，所以 python 的版本控制显得尤为重要。<br />`pyenv` 是个 shell 脚本，能够轻松得实现各个不同版本 python 的相互间切换，而且各个版本的 python 切换不限于全局切换，甚至不同文件夹都可以拥有不同的 python 版本。<br />下面我们就来看看如何使用 `pyenv`。<br />
<br />如果你既需要使用 `python2`，也需要使用 `python3`，`pyenv` 将是一个很高效的 python 版本管理工具。<br />由于 `pyenv` 是脚本插件，所以只能在类 UNIX 系统上使用。所以，如果你想在 windows 上安装，那就点击左上角去隔壁 `virtualenv` 瞧瞧。
### 1.1.1 安装 pyenv（Ubuntu）

1. **确定你想把 `pyenv` 安装在哪。**推荐安装在 `$HOME/.pyenv`，但你也可以安装在任意位置。
```powershell
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

1. **定义你 `PYENV_ROOT` 的环境变量**来指定你把 pyenv 仓库克隆到了哪，并把 `$PYENV_ROOT/bin` 添加到你的 `$PATH` 中，这样就能在命令行使用 `pyenv` 命令。
```powershell
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
```

1. **设置启动 shell 时自动加载 pyenv 脚本。**在 shell 配置文件的最后面加上 `eval "$(pyenv init -)"`。
```powershell
$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

1. **重启 shell，使脚本生效。**
```powershell
$ exec $SHELL
```

1. **安装不同的 python 版本到 `$(pyenv root)/versions` 文件夹。**  <br />
在 `pyenv` 安装之前的所有 python 版本都归为 `system` 版本。 （可以用 `pyenv versions` 查看当前安装的 python 版本）<br />
在安装 python 之前，可以使用 `pyenv install -l` 查看当前可以安装哪些 python 版本。<br />
然后使用 `pyenv install 选择的版本` 来安装你所选择的 python 版本。比如 `pyenv install 3.6.1` 安装 python 官网的版本。
### 1.1.2 使用 git 更新 pyenv
如果你是按照上面的方法安装的 `pyenv`，那你可以使用 git 来更新。
#### 更新为最新的开发版


```powershell
$ cd $(pyenv root)
$ git pull
```
#### 更新为指定的版本
```powershell
$ cd $(pyenv root)
$ git fetch
$ git tag
v0.1.0
$ git checkout v0.1.0
```
### 1.1.3 pyenv 的基本操作命令

- `pyenv versions` 查看当前已安装的 python 版本
- `pyenv install ...` 安装指定版本的 python
   - 安装位置为 `/home/zh/.pyenv/versions/3.6.10` 
      - zh：当前用户名
      - 2.6.10：为当前安装的python版本号
- `pyenv global python版本` 切换全局 python 版本
- `pyenv local python版本` 切换当前文件夹下的 python 版本
- `pyenv shell python版本` 切换当前 shell 中的 python 版本
- `pyenv version` 查看当前使用的 python 版本
### 1.1.4 pyenv离线安装python

1. 进入pyenv目录：`cd ~/.pyenv/`

2. 在pyenv目录下创建cache目录：`mkdir cache`

3. 把从python官网下载python版本放到cache目录中。
4. 比如下载连接：`https://www.python.org/ftp/python/3.6.10/Python-3.6.10.tar.xz`
5. 需要的Python版本下载完毕，并放到`~/.pyenv/chache`目录之后，可以使用安装`pyenv install ...`python版本。比如`pyenv install 3.6.10`

### 1.1.5 卸载 pyenv

- 如果你只是想禁用 `pyenv`，那么把 `pyenv init` 从 shell 的配置文件中移除，然后重启 shell 就行了（移除后 `pyenv` 命令仍然能使用，但是版本切换命令不会生效）。
- 完整卸载 pyenv。执行上一步，然后把 pyenv 的根目录删除即可全部删除 pyenv（通过 `pyenv install ...` 安装的 python 版本都会删除）。
```powershell
rm -rf $(pyenv root)
```
### 1.1.6 卸载 pyenv 安装的 python 版本

- 使用 `pyenv uninstall ...` 命令。
- 直接删除 `versions` 文件夹下的对应 python 版本文件夹。
### 1.1.7 pyenv 其他操作命令
参见 [commands.md](https://link.jianshu.com?t=https://github.com/pyenv/pyenv/blob/master/COMMANDS.md)<br />
<br />

# 2 python模块版本管理 
使用 `virtualenv` 和 `virtualenvwrapper` 管理 python 虚拟环境，每次都需要手动激活或退出。对于懒癌晚期患者，`pyenv-virtualenv`的自动激活和退出虚拟环境功能简直不能再赞。另外搭配 `pyenv` 食用效果更佳。
## 2.1 pyenv-virtualenv
### 2.1.1 安装 pyenv-virtualenv（Ubuntu）
由于 `pyenv-virtualenv` 是 `pyenv` 的一个插件，所以安装之前需要先安装 `pyenv`。<br />**注意：**如果 `pyenv` 的安装目录不是 `$HOME/.pyenv` 需要确保克隆下来的仓库位于你所安装的 `pyenv` 目录下的 `plugin` 文件夹下。<br />接下来就可以执行安装步骤了：

1. 克隆 `pyenv-virtual` 仓库到 `plugin` 文件夹下。
1. （可选/重点）添加 `pyenv virtualenv-init` 到你的 shell 配置文件中，这样进入指定文件夹自动进入虚拟环境，离开文件夹退出虚拟环境。
```powershell
$ echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
```

1. 重启 shell。
### 2.1.2 创建 pyenv-virtualenv 虚拟环境

- `pyenv virtualenv 指定python版本 虚拟环境名字`
- `pyenv virtualenv 虚拟环境名字`

如果不指定 python 版本，则默认使用当前 `pyenv version` 的 python 版本。<br />创建的虚拟环境位于 `$(pyenv root)/versions/` 下的指定 python 版本的文件夹中 `envs/` 文件夹下。
### 2.1.3 激活虚拟环境

- 自动激活/退出
- 手动激活/退出

自动激活环境：

- 在 `.bashrc` 文件的最后添加 `eval "$(pyenv virtualenv-init -)"`，然后在 shell 中输入 `exec "$SHELL"` 重启 shell，或者手动重启 shell。
- 在想要激活虚拟环境的文件夹中新建 `.python-version` 文件，并写入虚拟环境的名字（`pyenv local python版本` 该命令也是通过创建该文件来达到进入该文件夹后自动使用指定 python 版本的目的）。
- 以后进入该的文件夹就会自动激活虚拟环境，离开该文件夹就会退出虚拟环境。

手动激活环境：

- `pyenv activate 虚拟环境名字` 激活虚拟环境。
- `pyenv deactivate` 退出虚拟环境。
### 2.1.4 删除虚拟环境
有 2 种方法：

1. 删除 `$(pyenv root)/versions` 和 `$(pyenv root)/versions/{version}/envs` 的相关文件夹即可。
1. 命令行运行 `pyenv uninstall 虚拟环境的名字`



## 2.2 virtualenv
**安装virtualenv**：`pip3 install virtualenv`**<br />**创建指定Python版本的Python运行环境**：`virtualenv -p /usr/bin/python3 env_name`（env_name为Python运行环境名称）

- 如：`virtualenv -p /home/zh/.pyenv/versions/3.6.10/bin/python ai`

**激活虚拟环境**： `source env_name/bin/activate` （env_name为Python运行环境名称）<br />

- 如果env_name不再当前命令行所在目录，则需要写env_name绝对路径。比如： `source /home/zh/ai/bin/activate`

**推出当前虚拟环境**： `deactivate` 