# Sentry 安装和使用

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap
- 需要部署的组件很多，至少需要：4C8G，推荐 16G 内存不然真实环境是不够的

## Sentry 基本介绍

- 官网：<https://sentry.io/welcome/>
- 官网：<https://github.com/getsentry/sentry>


## Sentry 安装（Docker）

- 当前时间：2020-09-28 最新版本为：Sentry 20.10.0
- 官网专门提供了一个项目：
    - <https://github.com/getsentry/onpremise>
    - <https://develop.sentry.dev/self-hosted/>


```
git clone --depth=1 https://github.com/getsentry/onpremise.git

cd onpremise

确保有 docker、docker-compose 环境，
并且 docker 是启动状态
并且 docker 镜像源是国内地址，不然下载镜像就更慢了

开始安装，下载镜像比较多，所以过程挺长的，预计要 20 分钟左右，总下载镜像大小为 3.16GB
本身带了 redis，nginx，pgsql 等
安装过程的日志存储在：sentry_install_log-当前系统时间.txt
>> 终端安装过程会提示你创建用户
安装命令：./install.sh

启动：docker-compose up -d

如果安装过程你没有创建用户，可以再通过下面命令行创建账号
docker-compose run --rm web createuser

默认暴露的端口是9000
```

- 可以看到启动了很多容器：

```
CONTAINER ID        IMAGE                                  COMMAND                  CREATED             STATUS              PORTS                          NAMES
cc93db8157eb        nginx:1.16                             "nginx -g 'daemon of…"   14 minutes ago      Up 14 minutes       0.0.0.0:9000->80/tcp           sentry_onpremise_nginx_1
1481b568ae11        sentry-onpremise-local                 "/bin/sh -c 'exec /d…"   14 minutes ago      Up 14 minutes       9000/tcp                       sentry_onpremise_web_1
9a45312fa213        sentry-cleanup-onpremise-local         "/entrypoint.sh '0 0…"   14 minutes ago      Up 14 minutes       9000/tcp                       sentry_onpremise_sentry-cleanup_1
861b51d54597        sentry-onpremise-local                 "/bin/sh -c 'exec /d…"   14 minutes ago      Up 14 minutes       9000/tcp                       sentry_onpremise_worker_1
62c23270140f        sentry-onpremise-local                 "/bin/sh -c 'exec /d…"   14 minutes ago      Up 14 minutes       9000/tcp                       sentry_onpremise_post-process-forwarder_1
8d6cc0458275        sentry-onpremise-local                 "/bin/sh -c 'exec /d…"   14 minutes ago      Up 14 minutes       9000/tcp                       sentry_onpremise_ingest-consumer_1
0ac1ab32b857        sentry-onpremise-local                 "/bin/sh -c 'exec /d…"   14 minutes ago      Up 14 minutes       9000/tcp                       sentry_onpremise_cron_1
df75ae013afb        getsentry/relay:latest                 "/bin/bash /docker-e…"   14 minutes ago      Up 14 minutes       3000/tcp                       sentry_onpremise_relay_1
364f55072e3e        snuba-cleanup-onpremise-local          "/entrypoint.sh '*/5…"   14 minutes ago      Up 14 minutes       1218/tcp                       sentry_onpremise_snuba-cleanup_1
82a493c3ed36        symbolicator-cleanup-onpremise-local   "/entrypoint.sh '55 …"   14 minutes ago      Up 14 minutes       3021/tcp                       sentry_onpremise_symbolicator-cleanup_1
6c2e8329c40a        getsentry/snuba:latest                 "./docker_entrypoint…"   22 minutes ago      Up 14 minutes       1218/tcp                       sentry_onpremise_snuba-transactions-consumer_1
3b3546024d97        getsentry/snuba:latest                 "./docker_entrypoint…"   22 minutes ago      Up 14 minutes       1218/tcp                       sentry_onpremise_snuba-api_1
d4d0e234596b        getsentry/snuba:latest                 "./docker_entrypoint…"   22 minutes ago      Up 14 minutes       1218/tcp                       sentry_onpremise_snuba-outcomes-consumer_1
28c491c9f795        getsentry/snuba:latest                 "./docker_entrypoint…"   22 minutes ago      Up 14 minutes       1218/tcp                       sentry_onpremise_snuba-consumer_1
44489a8c4cec        getsentry/snuba:latest                 "./docker_entrypoint…"   22 minutes ago      Up 14 minutes       1218/tcp                       sentry_onpremise_snuba-sessions-consumer_1
be2375a4b101        getsentry/snuba:latest                 "./docker_entrypoint…"   22 minutes ago      Up 14 minutes       1218/tcp                       sentry_onpremise_snuba-replacer_1
a622a5aa5406        postgres:9.6                           "docker-entrypoint.s…"   22 minutes ago      Up 14 minutes       5432/tcp                       sentry_onpremise_postgres_1
69731926f42c        getsentry/symbolicator:latest          "/bin/bash /docker-e…"   22 minutes ago      Up 14 minutes       3021/tcp                       sentry_onpremise_symbolicator_1
88fdbf5612b6        memcached:1.5-alpine                   "docker-entrypoint.s…"   22 minutes ago      Up 14 minutes       11211/tcp                      sentry_onpremise_memcached_1
bf3f54887a16        tianon/exim4                           "docker-entrypoint.s…"   22 minutes ago      Up 14 minutes       25/tcp                         sentry_onpremise_smtp_1
8d4cf08cf6e4        confluentinc/cp-kafka:5.5.0            "/etc/confluent/dock…"   23 minutes ago      Up 14 minutes       9092/tcp                       sentry_onpremise_kafka_1
0f85b4915b06        redis:5.0-alpine                       "docker-entrypoint.s…"   23 minutes ago      Up 14 minutes       6379/tcp                       sentry_onpremise_redis_1
f628295620b7        yandex/clickhouse-server:20.3.9.70     "/entrypoint.sh"         23 minutes ago      Up 14 minutes       8123/tcp, 9000/tcp, 9009/tcp   sentry_onpremise_clickhouse_1
a7fcebcc4663        confluentinc/cp-zookeeper:5.5.0        "/etc/confluent/dock…"   23 minutes ago      Up 14 minutes       2181/tcp, 2888/tcp, 3888/tcp   sentry_onpremise_zookeeper_1
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


