# PostgreSQL 安装和配置


## 官网

- 官网：<https://www.postgresql.org/>
    - 201906 最新版本
    - 12 beta
    - 11 release
- 官网 Docker hub：<https://hub.docker.com/_/postgres>


## Docker 安装 PostgreSQL（带挂载）

```
mkdir -p /data/docker/pgsql/data

chmod -R 777 /data/docker/pgsql

docker run \
	-d \
	--name pgsql \
	-p 5432:5432 \
	-e POSTGRES_USER=cdk8s_user \
	-e POSTGRES_PASSWORD=cdk8s123456 \
	-v /data/docker/pgsql/data:/var/lib/postgresql/data \
	postgres:11
```

- 连上容器：`docker exec -it pgsql /bin/bash`
	- 连上 PostgreSQL：`psql -h 127.0.0.1 -p 5432 -U cdk8s_user`


```
CREATE DATABASE sonar;
```

## PostgreSQL 10 带 zhparser（非官方）

- <https://hub.docker.com/r/chenxinaz/zhparser>
- 字典文件在容器：`/usr/share/postgresql/10/tsearch_data`
- 配置文件在容器：`/var/lib/postgresql/data/postgresql.conf`

```
mkdir -p /data/docker/pgsql/data

chmod -R 777 /data/docker/pgsql

docker run \
	-d \
	-p 5432:5432 \
	-v /data/docker/pgsql/data:/var/lib/postgresql/data \
	chenxinaz/zhparser
```

## PostgreSQL 11 带 zhparser（非官方）

- <https://hub.docker.com/r/davidlauhn/postgres-11-with-zhparser>
- 字典文件在容器（在 macOS 下没映射成功，不知道为什么）：`/usr/share/postgresql/11/tsearch_data`
- 配置文件在容器：`/var/lib/postgresql/data/postgresql.conf`

```
mkdir -p /data/docker/pgsql/data

chmod -R 777 /data/docker/pgsql

docker run \
	-d \
	-p 5432:5432 \
	-v /data/docker/pgsql/data:/var/lib/postgresql/data \
	davidlauhn/postgres-11-with-zhparser
```



## 资料

- <https://codeday.me/bug/20180726/203876.html>
