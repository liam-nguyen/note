---
title: Python配置
toc: true
date: 2017-3-30
top: 8
---

### 1 Conda

* conda是一种通用包管理系统，旨在构建和管理任何语言和任何类型的软件。
* [Anaconda ](https://www.continuum.io/why-anaconda)(/ˌænə'kɑndə/)是一个用于科学计算的python发行版，支持各种系统，提供了包管理和环境管理的功能。里面预装好了conda、某个版本的python、众多packages、科学计算工具等等，就是把很多常用的不常用的库都给你装好了。
* Miniconda，顾名思义，它只包含最基本的内容——python与conda，以及相关的必须依赖项，对于空间要求严格的用户，Miniconda是一种选择。就只包含最基本的东西，其他的库得自己装。



#### Conda的包管理

`Conda`既是一个工具，也是一个可执行命令，其核心功能是包管理和环境管理。包管理与`pip`使用类似。

```python
# 安装package
conda install package

# 查看已经安装的packages
conda list

# 查找package信息
conda search package

# 更新package
conda update -n python27 package

# 删除package
conda remove -n python27 package
```

#### Conda的环境管理

Conda可以创建/激活/删除某一个环境。

```bash
# 创建一个名为python27的环境，指定Python版本是2.7
conda create --name python27 python=2.7
# 若想要在创建环境同时安装python的一些包：
conda create --name python27 python=2.7 numpy pandas

# 安装好后，使用activate激活某个环境
# 激活后，会发现terminal输入的地方多了python27的字样，
# 实际上，此时系统做的事情就是把默认环境从PATH中去除，再把2.7对应的命令加入PATH
source activate python27 

# 如果想返回python 2.7环境，运行
source deactivate python27 # for Linux & Mac

# 删除一个已有的环境
conda remove --name python27 --all
```

#### Channel

通过修改用户目录下的`.condarc`文件配置镜像。例如添加[TUNA镜像](https://mirror.tuna.tsinghua.edu.cn/help/anaconda/)：

```text
channels:
  - defaults
show_channel_urls: true
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```
  
运行`conda clean -i`清除索引缓存，保证用的是镜像站提供的索引。




#### 使用Requirement.txt 安装

```bash
conda install --yes --file requirements.txt
```

#### 使用Pycharm

在`Pycharm`配置里选用`Anaconda`的`python`编译器所在位置即可。 使用Jupyter notebook时，点击Run Cell，它会弹出提示框，要求输入token。接下来在Terminal里运行Jupyter Notebook, 拷贝token以后的字符串到提示框，等待连接完成。

如果已经有jupyter notebook在运行，而且你忘了token的话，可以输入`jupyter notebook list`查询当前运行的notebook。

#### 在PyCharm中配置anaconda的解释器 

选择project interpreter, 接着点击 project interpreter 的右边的小齿轮，选择 add local ，选择anaconda文件路径下的python。接着PyCharm会更新解释器，导入模块等，要稍等一点时间。

#### Resources

* [Conda Cheat Sheet](https://conda.io/docs/_downloads/conda-cheatsheet.pdf)

* [Installing the IPython kernel](https://ipython.readthedocs.io/en/latest/install/kernel_install.html)


### 2 Virtualenv


#### Install

Install `virtualenv` using `conda` instead of `pip`, because it might raise error (see on [StackOverflow](virtualenv --no-site-packages venv))

```bash
conda install virtualenv
```

#### create your environment

Now you can create your python environment for your particular programs. For example, under the folder `your project`, you create an environment called `.venv` by:

```bash
virtualenv --no-site-packages .venv
```

The command `--no-site-packages` requires the environment should not access to global site-packages (as default now).

Before running your program in your created environment, you need to activate it:

```bash
source .venv/bin/activate
```

And remember to deactivate it whenever you are done:

```bash
deactivate
```







