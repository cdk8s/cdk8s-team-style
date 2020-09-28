# Sentry 安装和使用

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap
- 需要部署的组件很多，至少需要：4C8G

## Sentry 基本介绍

- 官网：<https://sentry.io/welcome/>
- 官网：<https://github.com/getsentry/sentry>


## Sentry 安装（Docker）

- 官网专门提供了一个项目：<https://github.com/getsentry/onpremise>


```
git clone --depth=1 https://github.com/getsentry/onpremise.git

cd onpremise

开始安装，下载镜像比较多，所以过程挺长的
本身带了 redis，nginx，pgsql 等
安装过程会提示你创建用户
./install.sh

安装过程的日志存储在：sentry_install_log-当前系统时间.txt

docker-compose up -d

如果安装过程你没有创建用户，可以再通过下面命令行创建账号
docker-compose run --rm web createuser

默认暴露的端口是9000

```

- <http://127.0.0.1:9000>
- 可以设置中文：<http://127.0.0.1:9000/settings/account/details/>
- 如果你自己调整配置文件，需要更新，操作步骤：

```
重新构建镜像
docker-compose build

同步数据
docker-compose run --rm web upgrade

重新启动容器
docker-compose up -d
```

## 定时删除旧数据

- 避免存储数据太多，磁盘越来越大
- 写个 shell 脚本，然后定时执行该脚本

```
#!/usr/bin/env bash
docker exec -i sentry_onpremise_worker_1 sentry cleanup --days 30 && docker exec -i -u postgres sentry_onpremise_postgres_1 vacuumdb -U postgres -d postgres -v -f --analyze
```


