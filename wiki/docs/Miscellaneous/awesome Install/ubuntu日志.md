---
title: Ubuntu日志 
date: 2017-12-30
tags: [Linux]
---


使用VM Fusion 10在Mac Catalina上使用Ubuntu虚拟机的记录。首先需要解决的是VM Fusion 10在Catalina上的黑屏问题[^2]，正常安装以后，需要安装`open-vm`来安装VM Tools。

##### 更新系统

在「Software & Updates」(软件和更新)中选择国内的镜像。


```bash
# 更新本地报数据库
sudo apt update

# 更新所有已安装的包（也可以使用 full-upgrade）
sudo apt upgrade

# 自动移除不需要的包
sudo apt autoremove
```

##### 常用软件

```bash
# zsh
sudo apt install -y git vim zsh wget curl net-tools screenfetch

# ssh
sudo apt install -y openssh-server
sudo /etc/init.d/ssh start

# docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker your-user # 修改成你的用户名
```

安装oh-my-zsh

```bash
# 默认shell为zsh
chsh -s /bin/zsh
# 安装oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
sudo apt install -y autojump
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
# 打开 ~/.zshrc 文件，找到如下这行配置代码，在后面追加插件名
plugins=(其他插件名 autojump zsh-autosuggestions zsh-syntax-highlighting)
```


mysql

```bash
sudo apt install mysql-server
# 初始化配置
sudo mysql_secure_installation
# 检查mysql服务状态
systemctl status mysql.service
```


##### 文件夹共享

共享的文件夹设置以后，放置在虚拟机的`/mnt/hgfs`目录下。

##### 虚拟机

通过安装`open-vm`来安装VM Tools[^1]。

```bash
sudo apt install -y open-vm-tools-desktop open-vm-tools
```

随后开启在VM Fusion配置中选择Display-Use full resolution for Retina display支持4K分辨率。

##### 代理

https://www.cnblogs.com/mlh-bky/p/12356365.html

[^1]: https://linuxconfig.org/install-vmware-tools-on-ubuntu-20-04-focal-fossa-linux
[^2]: https://www.infosecgamer.com/2019/12/how-to-fix-vmfusion-blank-screen-on-mac-Catalina.html
