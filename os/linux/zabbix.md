

## Zabbix 安装

```
环境：CentOS 7.9
关闭了防火墙、SELinux


官网下载：https://www.zabbix.com/download?zabbix=5.0&os_distribution=centos&os_version=7&db=mysql&ws=nginx
官网有一个引导式选择平台，展示不同的安装脚本，很有意思

添加源：（网络不稳定，需要多次尝试）
rpm -Uvh https://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-release-5.0-1.el7.noarch.rpm
yum clean all

编辑源文件：
vim /etc/yum.repos.d/zabbix.repo

找到第 11 行，把 [zabbix-frontend] 下的
enabled=0 改为 enabled=1

安装后端服务（网络不稳定，需要多次尝试）
yum install -y zabbix-server-mysql zabbix-agent

安装前端（网络不稳定，需要多次尝试）
yum install -y centos-release-scl
yum install -y zabbix-web-mysql-scl zabbix-nginx-conf-scl


创建数据库、用户、授权关系
echo "CREATE DATABASE IF NOT EXISTS zabbix DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;" | mysql -u root --password='Upupmo123456_#'
echo "CREATE USER 'zabbix'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'Upupmo123456_#';" | mysql -u root --password='Upupmo123456_#'
echo "ALTER USER 'zabbix'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'Upupmo123456_#' PASSWORD EXPIRE NEVER;" | mysql -u root --password='Upupmo123456_#'
echo "GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'%' WITH GRANT OPTION;" | mysql -u root --password='Upupmo123456_#'
echo "FLUSH PRIVILEGES;" | mysql -u root --password='Upupmo123456_#'


解压初始化数据脚本：
zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz > /opt/create.sql

导入数据：
mysql -u root --password='Upupmo123456_#' zabbix < /opt/create.sql


修改配置文件，把 MySQL 连接密码保存进去
vim /etc/zabbix/zabbix_server.conf
找到 124 行：
DBPassword=我的MySQL密码


修改 nginx 配置，放开 80 端口和 server_name
vim /etc/opt/rh/rh-nginx116/nginx/conf.d/zabbix.conf
listen 80;
server_name worker1;


修改 php 配置，把 nginx 账号授权加进去，以及修改时区
vim /etc/opt/rh/rh-php72/php-fpm.d/zabbix.conf
把 isten.acl_users = apache 改为 isten.acl_users = apache,nginx
把 ; php_value[date.timezone] = Europe/Riga 改为 php_value[date.timezone] = Asia/Shanghai（前面的冒号表示注释，也要跟着去掉）


加入自启动（Server 预计占用内存在 200M 左右）：
systemctl restart zabbix-server zabbix-agent rh-nginx116-nginx rh-php72-php-fpm
systemctl enable zabbix-server zabbix-agent rh-nginx116-nginx rh-php72-php-fpm

浏览器访问：http://worker1
这时候会出现配置的引导页面
在 Check of pre-requisites 页面确保右侧的所有都是绿色的 OK 提示
在 Configure DB connection 就根据你的情况配置好连接信息即可
在 Zabbix server details 配置你的 Zabbix 服务的域名、端口（默认 10051 不用改）

默认管理员账号密码：
Admin
zabbix

在这个页面可以修改显示语言：http://worker1/zabbix.php?action=userprofile.edit
```

## 安装最新的 agent2 客户端

```
agent2 官网介绍：https://www.zabbix.com/documentation/current/manual/concepts/agent2
总结起来就是：
用 Go 开发，更高的性能，跟少的资源

先安装源：（网络不稳定，需要多次尝试）
rpm -Uvh https://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-release-5.0-1.el7.noarch.rpm

安装软件：（网络不稳定，需要多次尝试）
yum install -y zabbix-agent2

修改配置文件：
vim /etc/zabbix/zabbix_agent2.conf（如果是第一代的 agent 配置文件是 vim /etc/zabbix/zabbix_agentd.conf）
修改 80 行，把 Server=127.0.0.1 改为 Server=192.168.31.88
修改 120 行，把 ServerActive=127.0.0.1 改为 ServerActive=192.168.31.88
修改 131 行，把 Hostname=Zabbix server 改为 Hostname=header1


重启服务：systemctl restart zabbix-agent2
启动后，查看占用端口：netstat -lntup
可以看到客户端会占用 10050 端口
通过 htop 查看占用内存差不多 50MB 左右

加入自启动：
systemctl enable zabbix-agent2


现在转到浏览器，访问：http://worker1/hosts.php
选择右上角：创建主机
主机名称随便填，方便阅读即可
群组可以自定义输入，也可以选择，为了后续对一整个群组机子就操作使用的
Interfaces 填写你客户端机子的 ip 地址和端口即可，客户端端口默认是 10050
其他用默认值即可
然后切换 tab 到 `模板`
在 Link new templates 我们输入 linux 进行模糊搜索，然后在下拉结果中，选择：Template OS Linux by Zabbix agent，然后添加

添加完成后，重新访问：http://worker1/hosts.php
不断刷新，等打开1分钟，`可用性` 一列中 ZBX 字母是绿色高亮即表示已经连上客户端成功
```




