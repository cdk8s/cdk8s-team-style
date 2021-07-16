

## 安装 Zabbix 服务端 + agent2 客户端

```
环境：CentOS 7.9
关闭了防火墙、SELinux
**注意：必须把 zabbix server 安装在有 MySQL 的服务器上，不然无法启动，因为它需要用到 MySQL 客户端**
**注意：必须把 zabbix server 安装在有 MySQL 的服务器上，不然无法启动，因为它需要用到 MySQL 客户端**
**注意：必须把 zabbix server 安装在有 MySQL 的服务器上，不然无法启动，因为它需要用到 MySQL 客户端**
**注意：必须把 zabbix server 安装在有 MySQL 的服务器上，不然无法启动，因为它需要用到 MySQL 客户端**
**注意：必须把 zabbix server 安装在有 MySQL 的服务器上，不然无法启动，因为它需要用到 MySQL 客户端**


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
yum install -y zabbix-server-mysql zabbix-agent2 zabbix-get

安装前端（网络不稳定，需要多次尝试）
yum install -y centos-release-scl
yum install -y zabbix-web-mysql-scl zabbix-nginx-conf-scl


创建数据库、用户、授权关系
echo "CREATE DATABASE IF NOT EXISTS zabbix DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;" | mysql -u root --password='Upupmo123456'
echo "CREATE USER 'zabbix'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'Upupmo123456';" | mysql -u root --password='Upupmo123456'
echo "ALTER USER 'zabbix'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'Upupmo123456' PASSWORD EXPIRE NEVER;" | mysql -u root --password='Upupmo123456'
echo "GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'%' WITH GRANT OPTION;" | mysql -u root --password='Upupmo123456'
echo "FLUSH PRIVILEGES;" | mysql -u root --password='Upupmo123456'


解压初始化数据脚本：
zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz > /opt/create.sql

导入数据：
mysql -u root --password='Upupmo123456' zabbix < /opt/create.sql


修改配置文件，把 MySQL 连接密码保存进去
vim /etc/zabbix/zabbix_server.conf
找到 124 行：
DBPassword=我的MySQL密码


修改 nginx 配置，放开 80 端口和 server_name
vim /etc/opt/rh/rh-nginx116/nginx/conf.d/zabbix.conf
listen 80;
server_name 192.168.31.137;


修改 php 配置，把 nginx 账号授权加进去，以及修改时区
vim /etc/opt/rh/rh-php72/php-fpm.d/zabbix.conf
把 isten.acl_users = apache 改为 isten.acl_users = apache,nginx
把 ; php_value[date.timezone] = Europe/Riga 改为 php_value[date.timezone] = Asia/Shanghai（前面的冒号表示注释，也要跟着去掉）


加入自启动（Server 预计占用内存在 200M 左右）：
systemctl restart zabbix-server zabbix-agent2 rh-nginx116-nginx rh-php72-php-fpm
systemctl enable zabbix-server zabbix-agent2 rh-nginx116-nginx rh-php72-php-fpm

查看下 server 启动日志：
tail -100f /var/log/zabbix/zabbix_server.log


浏览器访问：http://192.168.31.137
这时候会出现配置的引导页面
在 Check of pre-requisites 页面确保右侧的所有都是绿色的 OK 提示
在 Configure DB connection 就根据你的情况配置好连接信息即可，建议 Database host 配置填写的是局域网 ip，而不是 localhost
在 Zabbix server details 配置你的 Zabbix 服务的域名、端口（默认 10051 不用改）

默认管理员账号密码：
Admin
zabbix

在这个页面可以修改显示语言：http://worker1/zabbix.php?action=userprofile.edit
```

## 其他机子安装最新的 agent2 客户端

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
修改 80 行，把 Server=127.0.0.1 改为 Server=192.168.31.137
修改 120 行，把 ServerActive=127.0.0.1 改为 ServerActive=192.168.31.137
修改 131 行，把 Hostname=Zabbix server 改为 Hostname=worker1（填写你当前客户端机子的 hostname）

重启服务：systemctl restart zabbix-agent2
启动后，查看占用端口：netstat -lntup
可以看到客户端会占用 10050 端口
通过 top 查看占用内存差不多 50MB 左右

加入自启动：
systemctl enable zabbix-agent2


现在转到浏览器，访问：http://192.168.31.137/hosts.php
选择右上角：创建主机
主机名称随便填，方便阅读即可
群组可以自定义输入，也可以选择，为了后续对一整个群组机子就操作使用的
Interfaces 填写你客户端机子的 ip 地址和端口即可，客户端端口默认是 10050
其他用默认值即可
然后切换 tab 到 `模板`
在 Link new templates 我们输入 linux 进行模糊搜索，然后在下拉结果中，选择：Template OS Linux by Zabbix agent，然后添加

添加完成后，重新访问：http://192.168.31.137/hosts.php
不断刷新，等打开1分钟，`可用性` 一列中 ZBX 字母是绿色高亮即表示已经连上客户端成功
```

-------------------------------------------------------------------


## 监控自定义监控项

- 客户端配置

```
修改配置文件：
vim /etc/zabbix/zabbix_agent2.conf
找到 291 行格式说明：UserParameter=<key>,<shell command>
假设我们要查看当前 SSH 登录用户数
UserParameter=login.ssh.user.num,w | awk 'NR==1{print $4}'

重启服务：systemctl restart zabbix-agent2

然后切换到服务端输入测试命令（这里测试的服务端本机的客户端）：
zabbix_get -s 127.0.0.1 -p 10050 -k "login.ssh.user.num"
```

- 网页端配置

```
打开：http://192.168.31.137/hosts.php
选择对应主机的 `监控项`
选择右上角 `创建监控项`
键值填写我们上面创造的：login.ssh.user.num
新的应用集，可以理解为监控项组
点击 `测试` 我们就可以拿到对应的值
```

-------------------------------------------------------------------

## 触发器

```
网页端打开：http://192.168.31.137/hosts.php
选择对应主机的 `触发器`
选择右上角 `创建触发器`
表达式一栏点击 `添加`
    - 监控项选择我们刚刚创建的 SSH 登录数量监控
    - `功能` 表示可以取最后(最近)值、平均值、总数、最近相差值
    - `最后一个 X 计数` 默认是 1，表示当出现一次这样的问题就开始触发报警。如果填写 5，就是连续出现 5 次这样的情况我才触发 
    - `间隔` 填写多久触发一次
    - `结果` 我们选择大于号，数值填写 3
事件成功迭代：选择 `表达式`
    - 如果你认为 ssh 必须是 1 才能算恢复正常，不需要报警，则可以继续添加一个 `恢复表达式`
    - 填写恢复表达式跟上面逻辑是一样的只是现在 结果 要填写 等于 1
点击添加保存


当你有多个 ssh 连接后，你可以访问：http://192.168.31.137/zabbix.php?action=problem.view
可以看到有问题数据
```

-------------------------------------------------------------------

## 配置企业微信收到报警信息


- 企业微信后台设置

```
访问企业微信后台：https://work.weixin.qq.com/wework_admin/frame
访问通讯录：https://work.weixin.qq.com/wework_admin/frame#contacts
创建一个 `监控部门`，然后导入需要接收消息的用户
选择其中一个认定为核心人员，获取他的账号名，比如我是：ZhangZhaoHuang

访问我的企业：https://work.weixin.qq.com/wework_admin/frame#profile
查看最底部：企业 ID 的值（也叫做 CorpID），稍后要用到：wwdd7f11cb112cc2c3

访问应用管理：https://work.weixin.qq.com/wework_admin/frame#apps
点击 创建应用
应用名称填写：运维告警
可见范围选择：刚刚创建的 监控部门
创建完，记录
AgentId：1000018
Secret：R61V-w8x0q0ZRSNIhX__JU4C8-2s7Mdtd9dynzRNOcw
```

- Zabbix 服务端设置

```
vim /etc/zabbix/zabbix_server.conf
找到 523 行，确保脚本路径是没有被注释的：AlertScriptsPath=/usr/lib/zabbix/alertscripts


cd /usr/lib/zabbix/alertscripts/
wget https://raw.githubusercontent.com/OneOaaS/weixin-alert/master/weixin_linux_amd64
mv weixin_linux_amd64 wechat
chmod 755 wechat 
chown zabbix:zabbix wechat


测试脚本：
/usr/lib/zabbix/alertscripts/wechat --corpid=wwdd7f11cb112cc2c3 --corpsecret=R61V-w8x0q0ZRSNIhX__JU4C8-2s7Mdtd9dynzRNOcw --msg="您好，告警测试" --user=ZhangZhaoHuang --agentid=1000018
返回：
{"errcode":0,"errmsg":"ok","invaliduser":""}
```


- Zabbix 网页端设置

```
打开 `报警媒介类型`：http://192.168.31.137/zabbix.php?action=mediatype.list
点击右上角：创建媒体类型
类型选择：脚本
脚本名称就是：/usr/lib/zabbix/alertscripts 目录下的 wechat
脚本参数：
    - 填写 `--corpid=wwdd7f11cb112cc2c3`
    - 填写 `--corpsecret=R61V-w8x0q0ZRSNIhX__JU4C8-2s7Mdtd9dynzRNOcw`
    - 填写 `--agentid=1000018`
    - 填写 `--user={ALERT.SENDTO}`
    - 填写 `--msg={ALERT.MESSAGE}`
添加完成后，右边有一个测试按钮，可以试一下是否可以发送成功


打开用户管理：http://192.168.31.137/zabbix.php?action=user.list
选择管理员 Admin
点击页头 tab，选择 `报警媒介`，添加
    - 类型选择：我们刚加的企业微信媒介
    - 收件人填写：ZhangZhaoHuang


设置告警动作：http://192.168.31.137/actionconf.php
先把左上角的下拉选择变成：`Trigger actions`
然后点击右上角 `创建动作`
    条件选择 `触发器`，选择 `等于`，触发器输入框输入我们自己创建的触发器名称，让它模糊提示
切换 tab 到 `操作`
`操作` 选择添加，在弹出框中
    - 选择 Admin 管理员
    - `仅发送` 选择我们添加的企业微信媒介
    - 勾选 `Custom message`，填写如下信息

主题：
服务故障: <font color="warning">{EVENT.NAME}</font>

消息内容：
服务故障: <font color="warning">{EVENT.NAME}</font>
告警主机: **{HOST.NAME}**
主机地址: **{HOST.IP}**
监控项目: {ITEM.NAME}
当前取值: {ITEM.LASTVALUE}
告警等级: {TRIGGER.SEVERITY}
告警时间: {EVENT.DATE}-{EVENT.TIME}
事件ID: {EVENT.ID}



`恢复操作` 选择添加，在弹出框中
    - 选择 Admin 管理员
    - `仅发送` 选择我们添加的企业微信媒介
    - 勾选 `Custom message`，填写如下信息

主题：
故障恢复: <font color="info">{EVENT.NAME}</font>

消息内容：
故障恢复: <font color="info">{EVENT.NAME}</font>
主机名称: **{HOST.NAME}**
主机地址: **{HOST.IP}**
告警名称: {EVENT.NAME}
持续时长: {EVENT.DURATION}
恢复时间: {EVENT.RECOVERY.DATE}-{EVENT.RECOVERY.TIME} 
当前状态: {TRIGGER.STATUS}
当前取值: {ITEM.LASTVALUE}
事件ID: {EVENT.ID}


现在可以模拟异常情况了
```


-------------------------------------------------------------------

## 其他工具介绍

```
yum install -y zabbix-get

通过命令行获取客户端的主机名
zabbix_get -s 127.0.0.1 -p 10050 -I 127.0.0.1 -k "system.hostname"

通过命令行获取客户端的 cpu 情况
zabbix_get -s 127.0.0.1 -p 10050 -k "system.cpu.load[all,avg1]"
```

-------------------------------------------------------------------

## MySQL 监控

```
下载 percona 提供的插件：https://www.percona.com/downloads/percona-monitoring-plugins/
版本：Percona Monitoring Plugins 1.1.8
选择：percona-zabbix-templates-1.1.8-1.noarch.rpm 下载

-------------------------------------------------------------------

客户端操作（这台机子有 MySQL、PHP7.x 服务）：
安装版本较新的 php 7.4
yum install -y epel-release
yum install -y http://rpms.remirepo.net/enterprise/remi-release-7.rpm
yum install -y yum-utils
yum-config-manager --enable remi-php74
yum install -y php php-cli php-fpm php-mysqlnd php-zip php-devel php-gd php-mcrypt php-mbstring php-curl php-xml php-pear php-bcmath php-json php-redis
php -v

下载监控插件：
wget https://downloads.percona.com/downloads/percona-monitoring-plugins/percona-monitoring-plugins-1.1.8/binary/redhat/7/x86_64/percona-zabbix-templates-1.1.8-1.noarch.rpm
yum localinstall -y percona-zabbix-templates-1.1.8-1.noarch.rpm
安装过程有提示：
Scripts are installed to /var/lib/zabbix/percona/scripts
Templates are installed to /var/lib/zabbix/percona/templates

拷贝自定义的变量：
cp /var/lib/zabbix/percona/templates/userparameter_percona_mysql.conf /etc/zabbix/zabbix_agent2.d
重启服务：systemctl restart zabbix-agent2

修改 PHP 的 MySQL 连接信息：
vim /var/lib/zabbix/percona/scripts/ss_get_mysql_stats.php
把 30、31 行的连接信息进行修改：
mysql_user = 'zabbix';
mysql_pass = 'Upupmo123456';

通过 shell 测试查看 pool size：/var/lib/zabbix/percona/scripts/get_mysql_stats_wrapper.sh gq
通过 agent 查看：zabbix_agent2 -t MySQL.Questions
可以拿到数值就表示配置都正常了。

服务端测试操作：
zabbix_get -s 127.0.0.1 -p 10050 -k "MySQL.Questions"

-------------------------------------------------------------------
都拿到值后，我们开始接下来操作：
下载模板文件：https://pan.baidu.com/s/1iIK1eFISRK0x2ggUA01sIQ  密码: 7rar
官网自带的那个模板文件不支持 zabbix 3及以上版本

网页端：
打开：http://192.168.31.137/templates.php
点击右上角 `导入`
选择我们模板文件，点击 `导入`

访问：http://192.168.31.137/hosts.php
选择我们的对应主机，切换 tab 到 `模板`
    Link new templates 输入 percona 模糊搜索出我们的模板
    现在可以看到我们主机的监控项变多


打开客户端机子：
修改一个临时文件的权限：（MySQL 的端口必须是 3306，不然文件名会不一样，php 脚本也需要对应修改，所以还是建议使用 3306 端口）
chown -R zabbix.zabbix /tmp/localhost-mysql_cacti_stats.txt

访问：http://192.168.31.137/zabbix.php?action=latest.view
默认是 5 分钟抓取一次数据，5 分钟后就可以看到对应的数据了
```




















