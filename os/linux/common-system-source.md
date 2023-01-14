
## CentOS 设置国内源


```
清华源官网：https://mirrors.tuna.tsinghua.edu.cn/help/centos/


建议先备份 /etc/yum.repos.d/ 内的文件。
然后编辑 /etc/yum.repos.d/ 中的相应文件，在 mirrorlist= 开头行前面加 # 注释掉；并将 baseurl= 开头行取消注释（如果被注释的话）。 对于 CentOS 7 ，请把该行内的域名（例如mirror.centos.org）替换为 mirrors.tuna.tsinghua.edu.cn。 对于 CentOS 8 ，请把 mirror.centos.org/$contentdir 替换为 mirrors.tuna.tsinghua.edu.cn/centos。
以上步骤可以被下方的命令一步完成

# 对于 CentOS 7
sudo sed -e 's|^mirrorlist=|#mirrorlist=|g' \
         -e 's|^#baseurl=http://mirror.centos.org|baseurl=https://mirrors.tuna.tsinghua.edu.cn|g' \
         -i.bak \
         /etc/yum.repos.d/CentOS-*.repo

# 对于 CentOS 8
sudo sed -e 's|^mirrorlist=|#mirrorlist=|g' \
         -e 's|^#baseurl=http://mirror.centos.org/$contentdir|baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos|g' \
         -i.bak \
         /etc/yum.repos.d/CentOS-*.repo

注意其中的*通配符，如果只需要替换一些文件中的源，请自行增删。
注意，如果需要启用其中一些 repo，需要将其中的 enabled=0 改为 enabled=1。
最后，更新软件包缓存

sudo yum makecache

```

--------------------------------------------------------------------------------------------------------------------------------------



## Kali Linux 设置国内源

```
先查看自己的系统的 codename：lsb_release -a
No LSB modules are available.
Distributor ID: Kali
Description:    Kali GNU/Linux Rolling
Release:        2022.3
Codename:       kali-rolling
我这边是 kali-rolling，则我下面的地址都是 kali-rolling 关键字

中科大：https://mirrors.ustc.edu.cn/help/kali.html
阿里：https://developer.aliyun.com/mirror/

vim /etc/apt/sources.list
先注释掉官方源

# 官方源
# deb http://http.kali.org/kali kali-rolling main non-free contrib
# deb-src http://http.kali.org/kali kali-rolling main non-free contrib

#中科大
deb http://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
deb-src http://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib

#阿里云
#deb http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
#deb-src http://mirrors.aliyun.com/kali kali-rolling main non-free contrib



备注：每次更新完软件源文件后，需要使用 sudo apt-get update 命令更新索引以生效。

```

--------------------------------------------------------------------------------------------------------------------------------------


## Raspberry Pi OS 设置国内源

```
备份源文件：
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp /etc/apt/sources.list.d/raspi.list /etc/apt/sources.list.d/raspi.list.bak

清华源官网：https://mirrors.tuna.tsinghua.edu.cn/help/raspbian/


# armv7l 用户（32位）：编辑 `/etc/apt/sources.list` 文件，删除原文件所有内容，用以下内容取代
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ bullseye main non-free contrib rpi
# deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ bullseye main non-free contrib rpi

# armv7l（32位） 用户如果需要开启 multi-arch 使用 arm64 软件源，需要在 `/etc/apt/sources.list` 中加上
deb [arch=arm64] http://mirrors.tuna.tsinghua.edu.cn/raspbian/multiarch/ bullseye main

# aarch64 用户（64位）：编辑 `/etc/apt/sources.list` 文件，用以下内容取代：
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free

# 对于两个架构，编辑 `/etc/apt/sources.list.d/raspi.list` 文件，删除原文件所有内容，用以下内容取代：
deb https://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ bullseye main


同步更新源sudo apt-get update
更新升级以安装软件包sudo apt-get upgrade



```

--------------------------------------------------------------------------------------------------------------------------------------


## Ubuntu 设置国内源

```
清华源官网：https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/



sudo sed -i "s@http://.*archive.ubuntu.com@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list
sudo sed -i "s@http://.*security.ubuntu.com@https://mirrors.tuna.tsinghua.edu.cn@g" /etc/apt/sources.list



```


--------------------------------------------------------------------------------------------------------------------------------------

## Debian 设置国内源

```
清华源官网：https://mirrors.tuna.tsinghua.edu.cn/help/debian/



Debian 的软件源配置文件是 /etc/apt/sources.list。将系统自带的该文件做个备份，将该文件替换为下面内容，即可使用 TUNA 的软件源镜像。
如果遇到无法拉取 https 源的情况，请先使用 http 源并安装：
$ sudo apt install apt-transport-https ca-certificates


# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free



```

