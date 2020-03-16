
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
	--name mysql \
	--restart always \
	-p 3306:3306 \
	-e MYSQL_ROOT_PASSWORD=123456 \
	-e MYSQL_DATABASE=youmeek_nav \
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
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION

# 避免在 dump 命令中加上密码后提示：Using a password on the command line interface can be insecure
[mysqldump]
user=root
password=123456
```

- 赋权（避免挂载的时候，一些程序需要容器中的用户的特定权限使用）：`chmod -R 777 /data/docker/mysql/datadir /data/docker/mysql/log`
- 赋权：`chown -R 0:0 /data/docker/mysql/conf`
	- 配置文件的赋权比较特殊，如果是给 777 权限会报：[Warning] World-writable config file '/etc/mysql/conf.d/mysql-1.cnf' is ignored，所以这里要特殊对待。容器内是用 root 的 uid，所以这里与之相匹配赋权即可。
	- 我是进入容器 bash 内，输入：`whoami && id`，看到默认用户的 uid 是 0，所以这里才 chown 0
- 启动

```
docker run -p 3306:3306 \
    --name cloud-mysql \
    --restart always \
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
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```

- 或者：`SET GLOBAL sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';`
- 设置完成后记得关闭会话，重新连接

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

-------------------------------------------------------------------

## Percona TPCC-MySQL 测试工具

- 可以较好地模拟真实测试结果数据
- 官网主页：<https://github.com/Percona-Lab/tpcc-mysql>

```
TPC-C 是专门针对联机交易处理系统（OLTP系统）的规范，一般情况下我们也把这类系统称为业务处理系统。
TPC-C是TPC(Transaction Processing Performance Council)组织发布的一个测试规范，用于模拟测试复杂的在线事务处理系统。其测试结果包括每分钟事务数(tpmC)，以及每事务的成本(Price/tpmC)。
在进行大压力下MySQL的一些行为时经常使用。
```

#### 安装

- 先确定本机安装过 MySQL
- 并且安装过：`yum install mysql-devel`

```
git clone https://github.com/Percona-Lab/tpcc-mysql
cd tpcc-mysql/src
make

如果make没报错，就会在tpcc-mysql 根目录文件夹下生成tpcc二进制命令行工具tpcc_load、tpcc_start

如果要同时支持 PgSQL 可以考虑：https://github.com/Percona-Lab/sysbench-tpcc
```

#### 测试的几个表介绍

```
tpcc-mysql的业务逻辑及其相关的几个表作用如下：
New-Order：新订单，主要对应 new_orders 表
Payment：支付，主要对应 orders、history 表
Order-Status：订单状态，主要对应 orders、order_line 表
Delivery：发货，主要对应 order_line 表
Stock-Level：库存，主要对应 stock 表

其他相关表：
客户：主要对应customer表
地区：主要对应district表
商品：主要对应item表
仓库：主要对应warehouse表
```

#### 准备

- 测试阿里云 ECS 与 RDS 是否相通：
- 记得在 RDS 添加账号和给账号配置权限，包括：配置权限、数据权限（默认添加账号后都是没有开启的，还要自己手动开启）
- 还要添加内网 ECS 到 RDS 的白名单 IP 里面
- 或者在 RDS 上开启外网访问设置，但是也设置 IP 白名单（访问 ip.cn 查看自己的外网 IP 地址，比如：120.85.112.97）
- RDS 的内网地址和外网地址不一样，要认真看。

```
ping rm-wz9v0vej02ys79jbj.mysql.rds.aliyuncs.com

mysql -h rm-wz9v0vej02ys79jbj.mysql.rds.aliyuncs.com -P 3306 -u myaccount -p

输入密码：Aa123456
```



```
创库，名字为：TPCC：
CREATE DATABASE TPCC DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;


导入项目中的出初始化数据脚本：
创建表：create_table.sql
/usr/bin/mysql -h rm-wz9v0vej02ys79jbj.mysql.rds.aliyuncs.com -u myaccount -p tpcc < /root/tpcc-mysql/create_table.sql

创建索引和外键：add_fkey_idx.sql
/usr/bin/mysql -h rm-wz9v0vej02ys79jbj.mysql.rds.aliyuncs.com -u myaccount -p tpcc < /root/tpcc-mysql/add_fkey_idx.sql
```


#### 测试

- 数据库：阿里云 RDS-MySQL-5.7-2C4G
- 测试机：阿里云 ECS-4C4G-CentOS7.6
- 根据测试，不同的 ECS 测试机，不同的 RDS 测试结果有时候差距挺大的，这个很蛋疼。

- 需要注意的是 tpcc 默认会读取 /var/lib/mysql/mysql.sock 这个 socket 文件。因此，如果你的socket文件不在相应路径的话，可以做个软连接，或者通过TCP/IP的方式连接测试服务器
- 准备数据：

```
cd /opt/tpcc-mysql
./tpcc_load -h rm-wz9v0vej02ys79jbj.mysql.rds.aliyuncs.com -P 3306 -d TPCC -u myaccount -p Aa123456 -w 80
-w 80 表示创建 80 个仓库数据
这个过程花费时间还是挺长的，建议测试机是高性能计算型。2CPU 差不多要 8h，你自己估量下。
我这边 RDS 监控中，曲线上每秒 insert 差不多在 2W 差不多，如果你没有这个数，速度可能就很慢了。
我这边差不多用了 2.5h 完成数据准备。


插入过程 RDS-2C4G 的监控情况：
CPU利用率 24%
内存 30% ~ 40% （随着数据增加而增大）
连接数：1%
IOPS：9%
已使用存储空间：5.5G ~ 10G

要模拟出够真实的数据，仓库不要太少，一般要大于 100，
下面是基于 80 个库的最终数据：

select count(*) from customer;
    2400000
select count(*) from district;
    800    
select count(*) from history;
    2400000
select count(*) from item;
    100000
select count(*) from new_orders;
    720000
select count(*) from order_line;
    23996450
select count(*) from orders;
    2400000
select count(*) from stock;
    8000000
select count(*) from warehouse;
    80
```

- 开始测试：

```

./tpcc_start -h rm-wz9v0vej02ys79jbj.mysql.rds.aliyuncs.com -P 3306 -d TPCC -u myaccount -p Aa123456 -w 80 -c 200 -r 300 -l 1800 -f /opt/mysql_tpcc_100_20190325

-w 100 表示 100 个仓库数据
-c 200 表示并发 200 个线程
-r 300 表示预热 300 秒
-l 1800 表示持续压测 1800 秒
```


#### 报表


```
<TpmC>
188.000 TpmC
TpmC结果值(每分钟事务数，该值是第一次统计结果中的新订单事务数除以总耗时分钟数，例如本例中是：372/2=186)
tpmC值在国内外被广泛用于衡量计算机系统的事务处理能力
```

- RDS-2C4G-80个仓库结果：
- CPU：100%，内存：34%，连接数：17%，IOPS：62%，磁盘空间：20G


```
1780, trx: 979, 95%: 1849.535, 99%: 2402.613, max_rt: 3401.947, 986|3248.772, 98|698.821, 103|4202.110, 101|4547.416
1790, trx: 1021, 95%: 1898.903, 99%: 2700.936, max_rt: 3848.142, 999|3150.117, 100|500.740, 102|3600.104, 100|5551.834
1800, trx: 989, 95%: 1899.472, 99%: 2847.899, max_rt: 4455.064, 989|3049.921, 101|699.144, 97|3599.021, 102|5151.141

STOPPING THREADS........................................................................................................................................................................................................

<Raw Results>
  [0] sc:2 lt:174378  rt:0  fl:0 avg_rt: 1192.8 (5)
  [1] sc:253 lt:173935  rt:0  fl:0 avg_rt: 542.7 (5)
  [2] sc:4726 lt:12712  rt:0  fl:0 avg_rt: 144.7 (5)
  [3] sc:0 lt:17435  rt:0  fl:0 avg_rt: 3029.8 (80)
  [4] sc:0 lt:17435  rt:0  fl:0 avg_rt: 3550.7 (20)
 in 1800 sec.

<Raw Results2(sum ver.)>
  [0] sc:2  lt:174378  rt:0  fl:0
  [1] sc:254  lt:174096  rt:0  fl:0
  [2] sc:4726  lt:12712  rt:0  fl:0
  [3] sc:0  lt:17437  rt:0  fl:0
  [4] sc:0  lt:17435  rt:0  fl:0

<Constraint Check> (all must be [OK])
 [transaction percentage]
        Payment: 43.45% (>=43.0%) [OK]
   Order-Status: 4.35% (>= 4.0%) [OK]
       Delivery: 4.35% (>= 4.0%) [OK]
    Stock-Level: 4.35% (>= 4.0%) [OK]
 [response time (at least 90% passed)]
      New-Order: 0.00%  [NG] *
        Payment: 0.15%  [NG] *
   Order-Status: 27.10%  [NG] *
       Delivery: 0.00%  [NG] *
    Stock-Level: 0.00%  [NG] *

<TpmC>
                 5812.667 TpmC
```

- 升级：RDS-4C8G-80个仓库结果
- CPU：100%，内存：55%，连接数：10%，IOPS：20%，磁盘空间：25G

```
1780, trx: 2303, 95%: 796.121, 99%: 1099.640, max_rt: 1596.883, 2293|2249.288, 232|256.393, 230|1694.050, 235|2550.775
1790, trx: 2336, 95%: 798.030, 99%: 1093.403, max_rt: 1547.840, 2338|2803.739, 234|305.185, 232|1799.869, 228|2453.748
1800, trx: 2305, 95%: 801.381, 99%: 1048.528, max_rt: 1297.465, 2306|1798.565, 229|304.329, 227|1649.609, 233|2549.599

STOPPING THREADS........................................................................................................................................................................................................

<Raw Results>
  [0] sc:7 lt:406567  rt:0  fl:0 avg_rt: 493.7 (5)
  [1] sc:10485 lt:395860  rt:0  fl:0 avg_rt: 240.1 (5)
  [2] sc:24615 lt:16045  rt:0  fl:0 avg_rt: 49.4 (5)
  [3] sc:0 lt:40651  rt:0  fl:0 avg_rt: 1273.6 (80)
  [4] sc:0 lt:40656  rt:0  fl:0 avg_rt: 1665.3 (20)
 in 1800 sec.

<Raw Results2(sum ver.)>
  [0] sc:7  lt:406569  rt:0  fl:0
  [1] sc:10487  lt:396098  rt:0  fl:0
  [2] sc:24615  lt:16045  rt:0  fl:0
  [3] sc:0  lt:40655  rt:0  fl:0
  [4] sc:0  lt:40659  rt:0  fl:0

<Constraint Check> (all must be [OK])
 [transaction percentage]
        Payment: 43.46% (>=43.0%) [OK]
   Order-Status: 4.35% (>= 4.0%) [OK]
       Delivery: 4.35% (>= 4.0%) [OK]
    Stock-Level: 4.35% (>= 4.0%) [OK]
 [response time (at least 90% passed)]
      New-Order: 0.00%  [NG] *
        Payment: 2.58%  [NG] *
   Order-Status: 60.54%  [NG] *
       Delivery: 0.00%  [NG] *
    Stock-Level: 0.00%  [NG] *

<TpmC>
                 13552.467 TpmC
```


- 升级：RDS-8C16G-80个仓库结果
- CPU：100%，内存：35%，连接数：5%，IOPS：18%，磁盘空间：30G

```
1780, trx: 4502, 95%: 398.131, 99%: 501.634, max_rt: 772.128, 4473|740.073, 446|183.361, 448|1042.264, 442|1302.569
1790, trx: 4465, 95%: 398.489, 99%: 541.424, max_rt: 803.659, 4476|845.313, 448|152.917, 450|997.319, 454|1250.160
1800, trx: 4506, 95%: 397.774, 99%: 501.334, max_rt: 747.074, 4508|701.625, 453|108.619, 450|1052.293, 451|1107.277

STOPPING THREADS........................................................................................................................................................................................................

<Raw Results>
  [0] sc:20 lt:803738  rt:0  fl:0 avg_rt: 240.5 (5)
  [1] sc:13844 lt:789535  rt:0  fl:0 avg_rt: 128.5 (5)
  [2] sc:54560 lt:25817  rt:0  fl:0 avg_rt: 22.1 (5)
  [3] sc:0 lt:80372  rt:0  fl:0 avg_rt: 739.8 (80)
  [4] sc:0 lt:80378  rt:0  fl:0 avg_rt: 771.1 (20)
 in 1800 sec.

<Raw Results2(sum ver.)>
  [0] sc:20  lt:803747  rt:0  fl:0
  [1] sc:13845  lt:789916  rt:0  fl:0
  [2] sc:54561  lt:25817  rt:0  fl:0
  [3] sc:0  lt:80377  rt:0  fl:0
  [4] sc:0  lt:80381  rt:0  fl:0

<Constraint Check> (all must be [OK])
 [transaction percentage]
        Payment: 43.47% (>=43.0%) [OK]
   Order-Status: 4.35% (>= 4.0%) [OK]
       Delivery: 4.35% (>= 4.0%) [OK]
    Stock-Level: 4.35% (>= 4.0%) [OK]
 [response time (at least 90% passed)]
      New-Order: 0.00%  [NG] *
        Payment: 1.72%  [NG] *
   Order-Status: 67.88%  [NG] *
       Delivery: 0.00%  [NG] *
    Stock-Level: 0.00%  [NG] *

<TpmC>
                 26791.934 TpmC
```


- 升级：RDS-16C64G-80个仓库结果
- CPU：100%，内存：18%，连接数：2%，IOPS：10%，磁盘空间：40G

```
1780, trx: 8413, 95%: 203.560, 99%: 279.322, max_rt: 451.010, 8414|441.849, 841|92.900, 839|583.340, 843|644.276
1790, trx: 8269, 95%: 204.599, 99%: 282.602, max_rt: 444.075, 8262|412.414, 827|91.551, 831|665.421, 824|616.396
1800, trx: 8395, 95%: 202.285, 99%: 255.026, max_rt: 436.136, 8404|446.292, 839|87.081, 839|609.221, 842|697.509

STOPPING THREADS........................................................................................................................................................................................................

<Raw Results>
  [0] sc:37 lt:1532893  rt:0  fl:0 avg_rt: 124.8 (5)
  [1] sc:36091 lt:1496111  rt:0  fl:0 avg_rt: 68.5 (5)
  [2] sc:105738 lt:47555  rt:0  fl:0 avg_rt: 11.4 (5)
  [3] sc:0 lt:153285  rt:0  fl:0 avg_rt: 404.6 (80)
  [4] sc:0 lt:153293  rt:0  fl:0 avg_rt: 389.5 (20)
 in 1800 sec.

<Raw Results2(sum ver.)>
  [0] sc:37  lt:1532918  rt:0  fl:0
  [1] sc:36093  lt:1496868  rt:0  fl:0
  [2] sc:105739  lt:47556  rt:0  fl:0
  [3] sc:0  lt:153297  rt:0  fl:0
  [4] sc:0  lt:153298  rt:0  fl:0

<Constraint Check> (all must be [OK])
 [transaction percentage]
        Payment: 43.47% (>=43.0%) [OK]
   Order-Status: 4.35% (>= 4.0%) [OK]
       Delivery: 4.35% (>= 4.0%) [OK]
    Stock-Level: 4.35% (>= 4.0%) [OK]
 [response time (at least 90% passed)]
      New-Order: 0.00%  [NG] *
        Payment: 2.36%  [NG] *
   Order-Status: 68.98%  [NG] *
       Delivery: 0.00%  [NG] *
    Stock-Level: 0.00%  [NG] *

<TpmC>
                 51097.668 TpmC
```


- 几轮下来，最终数据量：

```
select count(*) from customer;
    2400000
select count(*) from district;
    800    
select count(*) from history;
    5779395
select count(*) from item;
    100000
select count(*) from new_orders;
    764970
select count(*) from order_line;
    57453708
select count(*) from orders;
    5745589
select count(*) from stock;
    8000000
select count(*) from warehouse;
    80
```


## 资料

- <http://www.cnblogs.com/xiongpq/p/3384681.html>
