

## Zabbix 安装

```
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