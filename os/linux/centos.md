# CentOS 常用设置

## 镜像源

- 下载对应版本repo文件, 放入 /etc/yum.repos.d/ (操作前请做好相应备份)
- <http://mirrors.163.com/.help/centos.html>
- <https://developer.aliyun.com/mirror/centos>
- `yum install -y epel-release`

## 升级 Python

- 下载最新版本：<https://www.python.org/downloads/>
    - 当前 2021-02 最新版本为：3.9.2，点击进去选择：Gzipped source tarball 进行下载
- 编译安装

```
安装基础依赖工具
yum group install -y 'Development Tools'

yum install zlib-devel bzip2-devel openssl-devel ncurese-devel readline-devel sqlite-devel

wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz

tar zxvf Python-3.9.2.tgz
cd Python-3.9.2
./configure  --prefix=/usr/local/python3
make && make install
```

- 更换系统默认的Python版本

```
查看当前 python 版本：
python -V 得到 2.7.5

mv /usr/bin/python /usr/bin/python2.7.5

ln -s /usr/local/python3/bin/python3.9 /usr/bin/python

ln -s /usr/local/python3/bin/pip3 /usr/bin/pip

验证：
python -V
pip -V
```

- 修改 yum 设置

```
因 yum 的功能依赖于 Python2.x，我们现在改了默认 python 的版本会造成 yum 无法使用，所以要调整下：
vim /usr/bin/yum

把第一行原本为：
#!/usr/bin/python
改为
#!/usr/bin/python2.7.5

```



## 安装常用工具

```
yum install -y epel-release
yum install -y zip unzip lrzsz git wget htop deltarpm zsh vim

wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O - | sh
chsh -s /bin/zsh root
curl https://raw.githubusercontent.com/wklken/vim-for-server/master/vimrc > ~/.vimrc
```

## 查看版本号/主机名

- `cat /etc/redhat-release`
- `cat /etc/hostname`

## 配置网络

- 查看系统下有哪些网卡：`ls /etc/sysconfig/network-scripts/`，新版本不叫 eth0 这类格式了，比如我当前这个叫做：ifcfg-ens33（你的肯定跟我不一样，但是格式类似）
- 先备份：`cp /etc/sysconfig/network-scripts/ifcfg-ens33 /etc/sysconfig/network-scripts/ifcfg-ens33.bak`
- 编辑该文件：`vim /etc/sysconfig/network-scripts/ifcfg-ens33`，改为如下信息：（IP 段自己改为自己的网络情况）

``` ini
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
IPADDR=192.168.0.127
NETMASK=255.255.255.0
GATEWAY=192.168.0.1
DNS1=8.8.8.8
DNS1=114.114.114.114
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens33
UUID=b9f01b7d-4ebf-4d3a-a4ec-ae203425bb11
DEVICE=ens33
ONBOOT=yes
```

- 修改后，重启网络服务：`systemctl restart network.service`

## systemctl 的用法

- `systemctl is-enabled iptables.service` #查询服务是否开机启动
- `systemctl enable iptables.service` #开机运行服务
- `systemctl disable iptables.service` #取消开机运行
- `systemctl start iptables.service` #启动服务
- `systemctl stop iptables.service` #停止服务
- `systemctl restart iptables.service` #重启服务
- `systemctl reload iptables.service` #重新加载服务配置文件
- `systemctl status iptables.service` #查询服务运行状态
- `systemctl --failed` #显示启动失败的服务
- `systemctl list-units --type=service` #查看所有服务
- `systemctl is-enabled httpd` #查看httpd服务是否开机启动
- 对于启动脚本的存放位置，也不再是 `/etc/init.d/`（这个目录也是存在的），而是 `/usr/lib/systemd/system/`

### 开放端口

- 一般设置软件端口有一个原则：
	- 0 ~ 1024 系统保留，一般不要用到
	- 1024 ~ 65535（2^16） 可以随意用
- 添加单个端口：`firewall-cmd --zone=public --add-port=8883/tcp --permanent`
- 添加范围端口：`firewall-cmd --zone=public --add-port=8883-8885/tcp --permanent`
- 删除端口：`firewall-cmd --zone=public --remove-port=8883/tcp --permanent`
- 重启防火墙：`firewall-cmd --reload`
	- 命令解释：
	- `--zone` #作用域
	- `--add-port=80/tcp` #添加端口，格式为：端口/通讯协议
	- `--permanent` #永久生效，没有此参数重启后失效
- 列出所有端口列表：`firewall-cmd --list-all`


## 关禁用防火墙、selinux、swap

```
systemctl stop firewalld.service
systemctl disable firewalld.service
systemctl disable iptables.service

iptables -P FORWARD ACCEPT

setenforce 0 && sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

echo "vm.swappiness = 0" >> /etc/sysctl.conf
swapoff -a && sysctl -w vm.swappiness=0
```



## 设置时区

```
timedatectl set-timezone Asia/Shanghai
timedatectl status
```


## 资料

- <http://blog.topspeedsnail.com/archives/3017>
- <http://chenbaocheng.com/2015/07/15/Centos-7-%E5%AE%89%E8%A3%85%E9%85%8D%E7%BD%AEiptables/>
- <http://cuidehua.blog.51cto.com/5449828/1858374>
- <http://putty.biz/760>
