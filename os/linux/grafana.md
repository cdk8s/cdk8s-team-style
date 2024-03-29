# Grafana 安装和使用

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap

## Grafana 基本介绍

- 官网：<https://grafana.com/>

## 对于版本选择

- [支持的 Elasticsearch 版本](http://docs.grafana.org/features/datasources/elasticsearch/#elasticsearch-version)

## 升级 Grafana

```
以防万一，手工备份 grafana dashboard 配置

手工备份配置数据库、配置文件：
cp /etc/grafana/grafana.ini /opt
cp /var/lib/grafana/grafana.db /opt

停止旧服务：
sudo systemctl stop grafana-server

下载最新 rpm 包：
https://grafana.com/grafana/download?platform=linux

wget https://dl.grafana.com/enterprise/release/grafana-enterprise-9.0.0-1.x86_64.rpm
sudo yum install grafana-enterprise-9.0.0-1.x86_64.rpm
```


## Grafana 安装（Docker）

- 官网：<https://hub.docker.com/r/grafana/grafana/>

```
mkdir -p /data/docker/grafana/data
chmod -R 777 /data/docker/grafana/data

docker run -d --name grafana -p 3000:3000 -v /data/docker/grafana/data:/var/lib/grafana grafana/grafana

docker exec -it grafana /bin/bash

容器中默认的配置文件位置：/etc/grafana/grafana.ini
复制出配置文件到宿主机：docker cp grafana:/etc/grafana/grafana.ini /Users/gitnavi/
```

- <http://127.0.0.1:3000>
- 默认管理账号；admin，密码：admin，第一次登录后需要修改密码，也可以通过配置文件修改

```
[security]
admin_user = admin
admin_password = admin
```
----------------------------------------------------------------------------------------------

## Grafana 安装

- CentOS 7.4
- rpm 文件包大小 53M
- 所需内存：300M 左右
- 官网下载：<https://grafana.com/grafana/download?platform=linux>
- 官网指导：<http://docs.grafana.org/installation/rpm/>

```
sudo yum install -y initscripts fontconfig urw-fonts
wget https://dl.grafana.com/oss/release/grafana-5.4.0-1.x86_64.rpm 
sudo yum localinstall -y grafana-5.4.0-1.x86_64.rpm 
```


- 启动 Grafana 服务（默认是不启动的）

```
sudo systemctl start grafana-server
sudo systemctl status grafana-server
```

- 将 Grafana 服务设置为开机启动：`sudo systemctl enable grafana-server`
- 开放端口：`firewall-cmd --add-port=3000/tcp --permanent`
- 重新加载防火墙配置：`firewall-cmd --reload`
- 访问：<http://192.168.0.105:3000>
- 默认管理账号；admin，密码：admin，登录后需要修改密码

----------------------------------------------------------------------------------------------

## 配置

- 官网指导：<http://docs.grafana.org/installation/configuration/>
- 安装包默认安装后的一些路径
	- 二进制文件：`/usr/sbin/grafana-server`
	- init.d 脚本：`/etc/init.d/grafana-server`
	- 配置文件：`/etc/grafana/grafana.ini`
	- 日志文件：`/var/log/grafana/grafana.log`
	- 插件目录是：`/var/lib/grafana/plugins`
	- 默认配置的 sqlite3 数据库：`/var/lib/grafana/grafana.db`
- 最重要的配置文件：`vim /etc/grafana/grafana.ini`
	- 可以修改用户名和密码
	- 端口
	- 数据路径
	- 数据库配置
	- 第三方认证
	- Session 有效期
- 添加数据源：<http://192.168.0.105:3000/datasources/new>
- 添加组织：<http://192.168.0.105:3000/admin/orgs>
- 添加用户：<http://192.168.0.105:3000/org/users>
- 添加插件：<http://192.168.0.105:3000/plugins>
- 个性化设置：<http://192.168.0.105:3000/org>
- 软件变量：<http://192.168.0.105:3000/admin/settings>

## 官网 dashboard

- dashboar仓库地址：<https://grafana.com/dashboards>
- 本地可以通过输入 dashboard id 导入别人模板
- 打开：<http://192.168.0.105:3000/dashboard/import>
    - 输入对应的 id，点击 Load 即可

----------------------------------------------------------------------------------------------

## 配置域名

```
假设我们最终要访问的域名是：www.abc.com/grafana20211111

打开配置文件：
vim /etc/grafana/grafana.ini

修改如下配置：
domain = www.abc.com
root_url = %(protocol)s://%(domain)s:%(http_port)s/grafana20211111/
serve_from_sub_path = true

重启服务：systemctl start grafana-server

nginx 修改：
location /grafana20211111 {
    proxy_pass http://127.0.0.1:3000;
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

```

----------------------------------------------------------------------------------------------

## 数据源

#### Elasticsearch

- 使用：
- <https://cloud.tencent.com/info/68052367407c3bf21cc10c0263027f3f.html>
- <http://docs.grafana.org/features/datasources/elasticsearch/#using-elasticsearch-in-grafana>



----------------------------------------------------------------------------------------------


## 其他资料

- <https://blog.csdn.net/BianChengNinHao/article/details/80985302>
-

