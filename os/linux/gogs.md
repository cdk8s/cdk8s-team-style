# Gogs 安装和配置

## 环境说明

- CentOS 7.9


## 官方文档

- 官网文档：<https://gogs.io/>
- 官网安装文档：<https://gogs.io/docs/installation>
- 官网下载：<https://github.com/gogs/gogs/releases>


## 二进制安装（直接使用 SQLite3）

```
假设我文件放在 /opt 目录下

wget https://github.com/gogs/gogs/releases/download/v0.12.3/gogs_0.12.3_linux_amd64.tar.gz

tar zxvf gogs_0.12.3_linux_amd64.tar.gz


配置
创建自定义配置文件目录：
mkdir -p /opt/gogs/repositories /opt/gogs/datadb /opt/gogs/logs

控制条启动：
/opt/gogs/gogs web

Gogs 默认会在端口 3000 启动 HTTP 服务，但是 3000 端口跟 grafana 冲突，如果启动，请先停用 grafana 等配置好之后再启动
访问 http://192.168.31.137:3000/install 以进行初始配置，在配置文件里面可以设置新端口号
如果数据量不大，数据库类型可以 SQLite3
数据库文件路径，建议放在大的磁盘下：/opt/gogs/datadb/gogs.db
仓库根目录，建议放在大的磁盘下：/opt/gogs/repositories
运行系统用户：root
管理员用户名：不能用内置的 admin 名字


======================================================

设置开机启动，官网集成了脚本：
有 systemd、supervisor 等
https://github.com/gogs/gogs/tree/main/scripts

vim /etc/systemd/system/gogs.service

[Unit]
Description=Gogs
After=network.target
[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/gogs
ExecStart=/opt/gogs/gogs web
Restart=always
ProtectSystem=full
PrivateDevices=yes
PrivateTmp=yes
NoNewPrivileges=true
[Install]
WantedBy=multi-user.target


systemctl daemon-reload
systemctl enable gogs.service
systemctl start gogs.service
systemctl status gogs.service
```







