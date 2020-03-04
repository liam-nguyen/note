---
title: CentOS日志 
date: 2017-12-30
tags: [Linux]
---

Centos是追求稳定的程序员首选的Linux桌面版本。下面以Centos 6.10, VirtualBox为例。


### 1 安装与基础配置

新建虚拟机。在配置选项卡中，网络选择NAT和Host-Only选项。选择minimal安装项，在网络连接里设置静态IP，创建用户名和密码。安装大概2分钟。

#### 网络配置

安装完的Centos系统是无法连接网络的。用`ip addr`命令查看本机网卡。根据获得网卡Mac地址等信息修改`/etc/sysconfig/network-scripts/ifcfg-eth3`(eth3为对应host-only-adapter网卡名字)中的内容，设置`BOOTPROTO`, `IPADDR`，`NETMASK`，`GATEWAY`。例如：

```text
TYPE=Ethernet
BOOTPROTO=none
ONBOOT=yes
IPADDR=192.168.56.106
NETMASK=255.255.255.0
NAME="eth3"
HWADDR=08:00:27:73:6D:33
```

随后重启网络服务: `service network restart`(Centos7命令为`systemctl restart network.service`)。随后运行`yum install net-tools`来安装`ifconfig`工具。

#### SSH
CentOS默认是不启动SSH服务的。所以需要安装，启动、配置。

```bash
# 安装SSH
yum install openssh-server
# 开启-centos6
service sshd start
# 开启服务的自动启动-centos6
chkconfig sshd on
# 开启服务的自动启动-centos7
systemctl enable sshd.service
``` 

配置SSH免密登陆, 首先在主机上利用`ifconfig`命令查看虚拟机Ip地址，例如192.168.56.103,然后将Ip地址增加到本机host文件中.

```text
192.168.56.103 centos
```

然后利用`ssh-copy-id`命令将密钥拷贝到虚拟机，过程中选择yes，并输入密码。

```bash
ssh-copy-id centos
```

然后在主机上登陆虚拟机

```bash
ssh centos
```



#### 源

配置国内的阿里、网易的安装源能够大大加快包的下载速度。

```bash
# 备份，为了更新失败时切换回去
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
# 根据centos版本下载对应的新源，centos6
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
# 根据centos版本下载对应的新源，centos7
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
# 生成缓存，会把新下载CentOS-Base.repo源生效。
yum makecache
```

#### 常用软件

安装常用开发软件
```bash
yum -y install vim git wget 
```

#### 配置用户

为用户user添加sudo权限。修改`/etc/sudoers`文件

```text
root ALL=(ALL) ALL
user ALL=(ALL) ALL #user改成您的用户名
```

#### 修改主机名

默认安装的主机名往往非常怪异，需要修改。修改`/etc/sysconfig/network`文件中的HOSTNAME属性，重新启动后生效。centos7的主机名需要修改`/etc/hostname`文件。

#### oh-my-zsh

使用流行的oh-my-zsh使目录跳转、文字输入更加快捷。

```
# zsh
yum -y install zsh
yum -y install  git
# 安装oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

由于往往有多台虚拟机，所以希望显示[登陆用户，主机名，路径]这样的信息，否则很容易搞混虚拟机，产生误操作。在`～/.zshrc`文件中添加

```bash
PROMPT='%{$fg_bold[yellow]%}%n@%m ${ret_status} %{$fg[cyan]%}%d%{$reset_color%} $(git_prompt_info)'
```

使用`source ~/.zshrc`生效。

#### mysql

启动mysql服务

```bash
sudo service mysqld start
```

设置管理员密码

```bash
mysqladmin -u root  password 'new-password';
```

如果想重新设置密码，用原先密码登陆数据库

```sql
#使用mysql数据库        
 use mysql；
#修改          
update user set password=password("new-password") where user="root";
#刷新权限        
flush privileges;
```

设置mysql开机启动

```bash
chkconfig mysqld on
```

#### 开关机

Centos虚拟机的操作一般是通过主机的终端来操作的，所以就希望虚拟机在后台运行而不显示UI。

```
# 开启虚拟机在后台运行
VBoxManage startvm <vm_name> -type headless
```

或者直接将Centos的图形界面关闭，配置文件`/etc/inittab`, 在`id:5:initdefault`这一行中，将其改成`id:3:initdefault:`。

使用`shutdown -h now`关机，其中`-h`指令是halt的意思。


#### 关闭防火墙

Centos的防火墙默认是开着的，这在Hadoop通信过程中会产生错误。所以最简单的方法是直接把它关了。

```bash
# Centos6
service iptables stop
chkconfig iptables off
# Centos 7
systemctl stop firewalld.service

```

或者把Hadoop、Mysql等常用端口开放了，但是端口有点多，稍嫌麻烦：

```bash
# 例如开放Mysql端口
iptables -A INPUT -p tcp -m tcp --dport 3306 -j ACCEPT
```

#### 时间同步

分布式应用如Hadoop往往要求时间同步。而且虚拟机关闭以后，往往有很大的时间差。使用`ntpdate`工具可以同步服务器的时间。

```bash
sudo yum -y install ntp ntpdate
sudo ntpdate  time.apple.com
```

使用`crontab`定时更新时间

```bash
vim /etc/crontab
# 每分钟同步时间
*/1 * * * * ntpdate ntp1.aliyun.com
```


#### 克隆

选中虚拟机以后，选择右键clone。注意需要修改新的系统的主机名，网络地址，host文件。


### 2 大数据搭建
#### Hadoop 集群

<!--#### Unable to load native-hadoop library


-->


!!! problem "unable to load native library"

    Centos6遇到这个问题，一般是缺少GLIBC_2.14。可以用命令`ldd $HADOOP_HOME/lib/native/libhadoop.so.1.0.0`验证。
    
    ```bash
    wget  http://ftp.gnu.org/gnu/glibc/glibc-2.17.tar.gz
    tar -xvf glibc-2.17.tar.gz
    cd glibc-2.17
    mkdir build
    cd build 
    ../configure --prefix=/usr --disable-profile --enable-add-ons \
            --with-headers=/usr/include --with-binutils=/usr/bin
    make -j 8
    make  install
    strings /lib64/libc.so.6 | grep GLIBC
    ```


#### spark集群




### 3 Centos升级



