---
title: Git
toc: true
date: 2018-01-01
tags: [Git]
---

### 1 安装及配置

`git`在mac上已经默认安装了，使用之前只需要简单的配置即可。

#### 设置Git的user name和email

把下面的`username`和`email`替换成您的`Github`的用户名和地址。

```
$ git config --global user.name "username"
$ git config --global user.email "email"
```

#### 生成密钥

```
$ ssh-keygen -t rsa -C "email"
```

默认连续3个回车， 最后得到了两个文件：`～/.ssh/id_rsa`和`~/.ssh/id_rsa.pub`。注意这两个文件的保存地址(会输出在终端上，等下要用)。

其中公钥保存在`id_rsa.pub`内。

#### 添加密钥到ssh-agent

`ssh-agent`是一种控制用来保存公钥身份验证所使用的私钥的程序，其实`ssh-agent`就是一个密钥管理器，运行`ssh-agent`以后，使用`ssh-add`将私钥`id_rsa`交给`ssh-agent`保管，其他程序需要身份验证的时候可以将验证申请交给`ssh-agent`来完成整个认证过程。

```
$ eval "$(ssh-agent -s)"
```

添加生成的 `SSH key` 到 `ssh-agent`。

```
$ ssh-add ~/.ssh/id_rsa
```

#### 登陆`Github`, 添加`ssh`

复制`id_rsa.pub`文件里面的内容。

```
more .ssh/id_rsa.pub
```

打开[`GitHub`](https://github.com),依次选择`settings`-`SSH and GPG keys`-`New SSH key`。进入到如下界面，输入任意`Title`，在`Key`输入框内粘贴上`id_rsa.pub`文件里面的内容。

测试一下是否可以连接：

```
ssh -T git@github.com
```

测试成功后，在github页面的SSH keys上的钥匙符号会显示为绿色。


### 2 操作

#### 合并仓库

可以把两个仓库A、B进行合并，并且保存所有的提交历史：

```bash
# 进入A仓库
cd dir-A  
# 添加B仓库
git remote add -f Bproject <url-of-B>  
# 合并B仓库到A仓库，保留历史
git merge -s ours --allow-unrelated-histories --no-commit Bproject/master  
# 读取B仓库信息到dir-B
git read-tree --prefix=dir-B/ -u Bproject/master 
# 提交
git commit -m "Merge B project as our subdirectory" 
# 抽取B仓库作为子项目，使用subtree strategy
git pull -s subtree Bproject master  
```


#### 撤销

##### 撤销添加的文件

如果使用`git add <file>`添加了错误的文件, 可以使用`git reset HEAD`命令撤销添加的文件：

```bash
git reset HEAD #如果后面什么都不跟的话，就是上一次add里面的全部撤销
git reset HEAD XXX/XXX/XXX.java #对某个文件进行撤销
```

##### 撤销已经push的commit

使用`git reset`命令可以撤销已经push的commit。

```bash
git reset --soft/hard <commit-id>  # 撤销提交信息
git push origin master –force  ## 强制提交当前版本号，以达到撤销版本号的目的
# 重新提交和推送
git add .
git commit -m  <commit-message>
```

注意mixed/soft/hard区别：

* --mixed  会保留源码,只是将git commit和index信息回退到了某个版本.
* --soft   保留源码,只回退到commit信息到某个版本.不涉及index的回退,如果还需要提交,直接commit即可.
* --hard   源码也会回退到某个版本,commit和index 都会回退到某个版本.(注意,这种方式是改变本地代码仓库源码)


也可以使用`git revert`命令，但是它是把这次撤销作为一次最新的提交。

#### stash

https://blog.csdn.net/stone_yw/article/details/80795669

1. 当正在dev分支上开发某个项目，这时项目中出现一个bug，需要紧急修复，但是正在开发的内容只是完成一半，还不想提交，这时可以用git stash命令将修改的内容保存至堆栈区，然后顺利切换到hotfix分支进行bug修复，修复完成后，再次切回到dev分支，从堆栈中恢复刚刚保存的内容。 
2. 由于疏忽，本应该在dev分支开发的内容，却在master上进行了开发，需要重新切回到dev分支上进行开发，可以用git stash将内容保存至堆栈中，切回到dev分支后，再次恢复内容即可。 

总的来说，git stash命令的作用就是将目前还不想提交的但是已经修改的内容进行保存至堆栈中，后续可以在某个分支上恢复出堆栈中的内容。这也就是说，stash中的内容不仅仅可以恢复到原先开发的分支，也可以恢复到其他任意指定的分支上。git stash作用的范围包括工作区和暂存区中的内容，也就是说没有提交的内容都会保存至堆栈中。

### 3 .gitignore

```bash
# ignore single file
example.txt
# multiple files with the same extension
*.txt
# multiple files with the same name
example*
# all directories below the current level in a directory tree
examples/
# Ignoring files in every directory
**/example.txt
```


### 4 ISSUE

##### CRLF will be replaced by LF 

CRLF : windows 环境下的换行符 
LF ： linux 环境下的换行符

关闭自动转换即可

```
git config core.autocrlf false  //将设置中自动转换功能关闭
```


##### refuse to merge

在`git pull`时出现的问题`fatal: refusing to merge unrelated histories`。

处理方案，添加`--allow-unrelated-histories`.


##### 参考资料

[Pro Git](https://git-scm.com/about)