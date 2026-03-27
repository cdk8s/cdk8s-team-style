## Clickhouse 安装和配置


## 基础

- 列式数据库
- 官网：<https://clickhouse.com>


``
场景：
不适合 join，单表查询性能很好
更新是以批次方式更新（>1000条），而不是单条
添加进入后不怎么修改
要查询的结果字段不会很多，适合一个数据有很多很多属性字段，也叫大宽表
``


## Docker 安装

- 官网：<https://hub.docker.com/r/clickhouse/clickhouse-server/>
- 2021-12 当前最新版本为：21.9

```
mkdir -p ~/docker/clickhouse/data  ~/docker/clickhouse/log ~/docker/clickhouse/config

先运行一个基础版本，复制出默认的配置文件：
docker run -d --name clickhouse-server clickhouse/clickhouse-server
docker cp clickhouse-server:/etc/clickhouse-server/config.xml ~/docker/clickhouse/config/config.xml
docker cp clickhouse-server:/etc/clickhouse-server/users.xml ~/docker/clickhouse/config/users.xml
删除 docker stop clickhouse-server && docker rm clickhouse-server

默认只能给 127.0.0.1，修改配置文件：/etc/clickhouse-server/config.xml
打开 181 的注释：<listen_host>0.0.0.0</listen_host>

如果需要设置密码，还需要映射出这个配置文件并添加上密码设置：（默认用户名是 default）
/etc/clickhouse-server/user.xml
在 68 行的密码标签上填上密码：<password>123456</password>

创建一个带映射的容器：
docker run -d --name clickhouse \
-p 8123:8123 -p 9009:9009 -p 9090:9000 \
--restart=always --ulimit nofile=262144:262144 \
-v ~/docker/clickhouse/data:/var/lib/clickhouse \
-v ~/docker/clickhouse/log:/var/log/clickhouse-server \
-v ~/docker/clickhouse/config/config.xml:/etc/clickhouse-server/config.xml \
-v ~/docker/clickhouse/config/users.xml:/etc/clickhouse-server/users.xml \
clickhouse/clickhouse-server


使用 DataGrip 连接
host：127.0.0.1
port：8123
User: default
passwor: 123456
```
