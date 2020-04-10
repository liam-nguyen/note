---
title: Hue
toc: false
date: 2017-10-30
hidden: true
---     

下载[4.6版本](https://gethue.com/hue-4-6-and-its-improvements-are-out/)后，使用`make apps`命令生成安装包。Hue的配置集中在`$HUE_HOME/desktop/conf/hue.ini`文件，最后用`build/env/bin/supervisor`启动hue。

如果是Centos6的话，还需要安装Python2.7。

```bash
# 安装python2.7
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar -xvf Python-2.7.10.tgz
cd Python-2.7.10
./configure --prefix=/usr/local/python2
make 
make install 
cp -r usr/local/python2/python2.7 /usr/include
# 安装pip
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
ln -s /usr/local/python2.7/bin/pip /usr/bin/pip
# 安装基本包
pip install future
pip install cryptography
```


##### hdfs


修改core-site.xml，添加hadoop, hue代理用户

