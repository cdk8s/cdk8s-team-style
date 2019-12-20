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

## PostgreSQL 11 带 zhparser（非官方）

- <https://hub.docker.com/r/davidlauhn/postgres-11-with-zhparser>
- 如果要使用 10 版本，可以看，配置方法都一样：<https://hub.docker.com/r/chenxinaz/zhparser>
- 字典文件在容器（在 macOS 下没映射成功，不知道为什么）：`/usr/share/postgresql/11/tsearch_data`
- 配置文件在容器：`/var/lib/postgresql/data/postgresql.conf`

```
mkdir -p /Users/youmeek/docker_data/pgsql11/data /Users/youmeek/docker_data/pgsql11/conf

sudo chmod -R 777 /Users/youmeek/docker_data/pgsql11

先启动一个简单容器拿配置文件：
docker run -d --name pgsql11 davidlauhn/postgres-11-with-zhparser

复制配置文件
docker cp pgsql11:/var/lib/postgresql/data/postgresql.conf /Users/youmeek/docker_data/pgsql11


docker run \
	-d \
	--name pgsql11 \
	-e POSTGRES_PASSWORD=123456 \
	-v /Users/youmeek/docker_data/pgsql11/conf/postgresql.conf:/etc/postgresql/postgresql.conf \
	-v /Users/youmeek/docker_data/pgsql11/data:/var/lib/postgresql/data \
	-p 5432:5432 \
	davidlauhn/postgres-11-with-zhparser \
	-c 'config_file=/etc/postgresql/postgresql.conf'

```



## 资料

- <https://codeday.me/bug/20180726/203876.html>
