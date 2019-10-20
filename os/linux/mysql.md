
# MySQL 安装和使用

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap

## MySQL 基本介绍

- 官网：<https://dev.mysql.com/>
- 官网 8 下载：<https://dev.mysql.com/downloads/mysql/>
- 官网 5.5 下载：<http://dev.mysql.com/downloads/mysql/5.5.html#downloads>
- 官网 5.6 下载：<http://dev.mysql.com/downloads/mysql/5.6.html#downloads>
- 官网 5.7 下载：<http://dev.mysql.com/downloads/mysql/5.7.html#downloads>
- 官网帮助中心：<http://dev.mysql.com/doc/refman/5.6/en/source-installation.html>


## Docker 安装 MySQL 5.7（不带挂载）

```
docker run \
	--name mysql-jira \
	--restart always \
	-p 3306:3306 \
	-e MYSQL_ROOT_PASSWORD=adg_123456 \
	-e MYSQL_DATABASE=jira_db \
	-e MYSQL_USER=jira_user \
	-e MYSQL_PASSWORD=jira_123456 \
	-d \
	mysql:5.7
```

- 连上容器：`docker exec -it mysql-jira /bin/bash`
	- 连上 MySQL：`mysql -u root -p`
- 设置编码：

```
SET NAMES 'utf8mb4';
alter database jira_db character set utf8mb4;
```

## Docker 安装 MySQL 5.7（带挂载）

- 创建本地数据存储 + 配置文件目录：`mkdir -p /data/docker/mysql/datadir /data/docker/mysql/conf /data/docker/mysql/log`
- 在宿主机上创建一个配置文件：`vim /data/docker/mysql/conf/mysql-1.cnf`，内容如下：

```
# 该编码设置是我自己配置的
[mysql]
default-character-set = utf8mb4

# 下面内容是 docker mysql 默认的 start
[mysqld]
pid-file = /var/run/mysqld/mysqld.pid
socket = /var/run/mysqld/mysqld.sock
datadir = /var/lib/mysql
#log-error = /var/log/mysql/error.log
# By default we only accept connections from localhost
#bind-address = 127.0.0.1
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
# 上面内容是 docker mysql 默认的 end

# 下面开始的内容就是我自己配置的
log-error=/var/log/mysql/error.log
default-storage-engine = InnoDB
collation-server = utf8mb4_unicode_520_ci
init_connect = 'SET NAMES utf8mb4'
character-set-server = utf8mb4
lower_case_table_names = 1
max_allowed_packet = 50M
```

- 赋权（避免挂载的时候，一些程序需要容器中的用户的特定权限使用）：`chmod -R 777 /data/docker/mysql/datadir /data/docker/mysql/log`
- 赋权：`chown -R 0:0 /data/docker/mysql/conf`
	- 配置文件的赋权比较特殊，如果是给 777 权限会报：[Warning] World-writable config file '/etc/mysql/conf.d/mysql-1.cnf' is ignored，所以这里要特殊对待。容器内是用 root 的 uid，所以这里与之相匹配赋权即可。
	- 我是进入容器 bash 内，输入：`whoami && id`，看到默认用户的 uid 是 0，所以这里才 chown 0
- 启动

```
docker run -p 3306:3306 \
    --name cloud-mysql \
    -v /data/docker/mysql/datadir:/var/lib/mysql \
    -v /data/docker/mysql/log:/var/log/mysql \
    -v /data/docker/mysql/conf:/etc/mysql/conf.d \
    -e MYSQL_ROOT_PASSWORD=123456 \
    -d mysql:5.7
```

- 连上容器：`docker exec -it cloud-mysql /bin/bash`
	- 连上 MySQL：`mysql -u root -p`
	- 创建表：`CREATE DATABASE wormhole DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;`
- 关于容器的 MySQL 配置，官网是这样说的：<https://hub.docker.com/_/mysql/>

>> The MySQL startup configuration is specified in the file /etc/mysql/my.cnf, and that file in turn includes any files found in the /etc/mysql/conf.d directory that end with .cnf.Settings in files in this directory will augment and/or override settings in /etc/mysql/my.cnf. If you want to use a customized MySQL configuration,you can create your alternative configuration file in a directory on the host machine and then mount that directory location as /etc/mysql/conf.d inside the mysql container.

- 容器中的 my.cnf 内容如下：

```
# Copyright (c) 2016, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/
```

- docker 的 MySQL 备份和还原：
	- 备份：`docker exec cloud-mysql /usr/bin/mysqldump -u root --password=123456 DATABASE_Name > /opt/backup.sql`
	- 还原：`docker exec -i cloud-mysql /usr/bin/mysql -u root --password=123456 DATABASE_Name < /opt/backup.sql`

-------------------------------------------------------------------


## MySQL 配置

- 官网配置参数解释：<http://dev.mysql.com/doc/refman/5.6/en/mysqld-option-tables.html>
- 找一下当前系统中有多少个 my.cnf 文件：`find / -name "my.cnf"`，我查到的结果：

``` nginx
/etc/my.cnf
/usr/local/mysql/my.cnf
/usr/local/mysql/mysql-test/suite/ndb/my.cnf
/usr/local/mysql/mysql-test/suite/ndb_big/my.cnf
.............
/usr/local/mysql/mysql-test/suite/ndb_rpl/my.cnf
```


- 保留 **/etc/my.cnf** 和 **/usr/local/mysql/mysql-test/** 目录下配置文件，其他删除掉。
- 我整理的一个单机版配置说明（MySQL 5.6，适用于 1G 内存的服务器）：
	- [my.cnf](MySQL-Settings/MySQL-5.6/1G-Memory-Machine/my-for-comprehensive.cnf)
- 其中我测试的结果，在不适用任何配置修改的情况下，1G 内存安装 MySQL 5.6 默认就会占用 400M 左右的内存，要降下来的核心配置要补上这几个参数：

```
performance_schema_max_table_instances=400
table_definition_cache=400
table_open_cache=256
```

## 修改 root 账号密码

- 启动 Mysql 服务器（CentOS 6）：`service mysql start`
- 启动 Mysql 服务器（CentOS 7）：`systemctl start mysql`
- 查看是否已经启动了：`ps aux | grep mysql`
- 默认安装情况下，root 的密码是空，所以为了方便我们可以设置一个密码，假设我设置为：123456
- 终端下执行：`mysql -uroot`
    - 现在进入了 mysql 命令行管理界面，输入：`SET PASSWORD = PASSWORD('123456');FLUSH PRIVILEGES;`
    - 现在进入了 mysql 命令行管理界面，输入：`UPDATE user SET authentication_string=PASSWORD('123456') where USER='root';FLUSH PRIVILEGES;`
- 修改密码后，终端下执行：`mysql -uroot -p`
    - 根据提示，输入密码进度 mysql 命令行状态。
- 如果你在其他机子上连接该数据库机子报：**Access denied for user 'root'@'localhost' (using password: YES)**
	- 解决办法：
	- 在终端中执行（CentOS 6）：`service mysql stop`
	- 在终端中执行（CentOS 7）：`systemctl stop mysql`
	- 在终端中执行（前面添加的 Linux 用户 mysql 必须有存在）：`/usr/local/mysql/bin/mysqld --skip-grant-tables --user=mysql`
		- 此时 MySQL 服务会一直处于监听状态，你需要另起一个终端窗口来执行接下来的操作
		- 在终端中执行：`mysql -u root mysql` 或者：`mysql -h 127.0.0.1 -u root -P 3306 -p`
		- 把密码改为：123456，进入 MySQL 命令后执行：`UPDATE user SET Password=PASSWORD('123456') where USER='root';FLUSH PRIVILEGES;`
		- 然后重启 MySQL 服务（CentOS 6）：`service mysql restart`
		- 然后重启 MySQL 服务（CentOS 7）：`systemctl restart mysql`

## 连接报错："Host '192.168.1.133' is not allowed to connect to this MySQL server"

- 不允许除了 localhost 之外去连接，解决办法，进入 MySQL 命令行，输入下面内容：
- 开发机设置允许任何机子访问：
	- `vim /etc/my.cnf` 中不能有：`bind-address = 127.0.0.1`
	- 配置：`GRANT ALL PRIVILEGES ON *.* TO '数据库用户名'@'%' IDENTIFIED BY '数据库用户名的密码' WITH GRANT OPTION;`
	- 更新配置：`flush privileges;`
- 生产机设置只运行本机访问：
	- `vim /etc/my.cnf` 中必须有：`bind-address = 127.0.0.1`
	- 配置：`GRANT ALL PRIVILEGES ON *.* TO '数据库用户名'@'127.0.0.1' IDENTIFIED BY '数据库用户名的密码' WITH GRANT OPTION;`
	- 更新配置：`flush privileges;`


## 修改密码报错：Your password does not satisfy the current policy requirements

- MySQL 5.7 安全性要求更高，需要这么做：

```
set global validate_password_policy=0; #密码强度设为最低等级
set global validate_password_length=6; #密码允许最小长度为6
set password = password('新密码');
FLUSH PRIVILEGES;
```

## MySQL 5.7 

- 报错内容：

```
Expression #1 of ORDER BY clause is not in GROUP BY clause and contains nonaggregated column 'youmeek.nm.id' 
which is not functionally dependent on columns in GROUP BY clause; 
this is incompatible with sql_mode=only_full_group_by
```

- 查下自己的模式：`select version(), @@sql_mode;`
- 解决办法，修改 my.cnf，增加这一行：

```
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION;
```


## 小内存机子，MySQL 频繁挂掉解决办法（1G + CentOS 7.4）

- 保存系统日志到本地进行查看：`cd  /var/log/ && sz messages`
- 其中可以看到这样的几句话（可以知道内存不够了）：

```
Jul  6 21:49:14 VM_123_201_centos kernel: Out of memory: Kill process 19452 (httpd) score 36 or sacrifice child
Jul  6 21:49:14 VM_123_201_centos kernel: Killed process 19452 (httpd) total-vm:516404kB, anon-rss:36088kB, file-rss:168kB, shmem-rss:12kB
```

- 对于 1G 的内存 MySQL（5.6.35），建议重点下面配置：

```
[mysqld]
table_definition_cache=400
table_open_cache=256
innodb_buffer_pool_size = 64M
max_connections = 100 
```

- 增加 swap（云服务基本都是没 swap 的）
- 分别执行下面 shell 命令：

```
dd if=/dev/zero of=/swapfile bs=1M count=1024
mkswap /swapfile
swapon /swapfile
```

- 修改配置文件：`vim /etc/fstab`
	- 添加这句在文件最后一行：`/swapfile swap swap defauluts 0 0`
- 重启机子：`reboot`

## SQL 优化

- 表设计
    - 考虑：查多还是写多
    - 预估数据量
    - 考虑：一对一、一对多、多对多
    - 是否该冗余字段
    - 是否加索引
    - 字段类型是否选择合理
- explain
    - 哪些场景不走索引进行全表扫描



## 资料

- <http://www.cnblogs.com/xiongpq/p/3384681.html>
