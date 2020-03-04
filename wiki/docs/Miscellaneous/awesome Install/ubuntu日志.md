---
title: ubuntu日志 
date: 2017-12-30
tags: [Linux]
---

以ubuntu 16.06为例。

#### 配置源

备份源文件

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```

修改源列表，将/etc/apt/sources.list 内容替换为：

<small>
    
    # deb cdrom:[Ubuntu 16.04 LTS _Xenial Xerus_ - Release amd64 (20160420.1)]/ xenial main restricted
    deb-src http://archive.ubuntu.com/ubuntu xenial main restricted #Added by software-properties
    deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted multiverse universe #Added by software-properties
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted multiverse universe #Added by software-properties
    deb http://mirrors.aliyun.com/ubuntu/ xenial universe
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
    deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
    deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse #Added by software-properties
    deb http://archive.canonical.com/ubuntu xenial partner
    deb-src http://archive.canonical.com/ubuntu xenial partner
    deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted
    deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted multiverse universe #Added by software-properties
    deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
    deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse
</small>