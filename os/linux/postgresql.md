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

-------------------------------------------------------------------


## pgbench 做基准测试

- PostgerSQL 自带基准测试工具：pgbench
- 它可以自定义脚本文件进行测试，但是我们这里不复杂说，只讲内置的脚本进行测试
- CentOS 7 独立安装：`yum install -y postgresql-contrib`
- 查看版本：`pgbench -V`

#### 初始化数据库

- 初始化测试数据：`pgbench -i -s 2 -F 100 -h 127.0.0.1 -p 5432 -U myUserName -d myDBName`
    - `-i` 是初始化的意思
    - `-s 2` 表示初始化 2 个商户的数据。默认 1 个商户是 10W 个账号（pgbench_accounts），10 个出纳（pgbench_tellers），我们这里设置 2 就要对应的生成翻倍数据
    - `-F` 创建表时数据库的填充因子，取值 10 ~ 100，值越小 UPDATE 性能会有一定提升。

```
NOTICE:  table "pgbench_branches" does not exist, skipping
NOTICE:  table "pgbench_tellers" does not exist, skipping
NOTICE:  table "pgbench_accounts" does not exist, skipping
NOTICE:  table "pgbench_history" does not exist, skipping
creating tables...
10000 tuples done.
20000 tuples done.
30000 tuples done.
40000 tuples done.
50000 tuples done.
60000 tuples done.
70000 tuples done.
80000 tuples done.
90000 tuples done.
100000 tuples done.
set primary key...
vacuum...done.
```

#### 测试命令

- 测试语句参数说明

```
-c 并发客户端数 
-j 工作线程数
-M 提交查询到服务器使用的协议：simple|extended|prepared
-n 运行测试时不执行清理
-T 60 执行总时间，单位秒
-r 输出每个SQL的平均每语句延迟
```

- 只读测试，通过 `-S` 参数控制

```
nohup pgbench -c 5 -j 5 -M prepared -n -S -T 60 -h 127.0.0.1 -p 5432 -U myUserName -d myDBName > /opt/pgbenchtest-readonly.out 2>&1 &
```

- 更新、查询、插入测试

```
nohup pgbench -c 5 -j 5 -M prepared -n -T 60 -h 127.0.0.1 -p 5432 -U myUserName -d myDBName > /opt/pgbenchtest-all.out 2>&1 &
```

- 不执行更新测试，通过 `-N` 参数控制

```
nohup pgbench -c 5 -j 5 -M prepared -n -N -T 60 -h 127.0.0.1 -p 5432 -U myUserName -d myDBName > /opt/pgbenchtest-noupdate.out 2>&1 &
```



#### 测试报告

```
pghost: 127.0.0.1 pgport: 5432 nclients: 5 duration: 10 dbName: myDBName
transaction type: TPC-B (sort of)
scaling factor: 2
query mode: prepared
number of clients: 5
number of threads: 5
duration: 60 s
number of transactions actually processed: 7237
tps = 723.210820 (including connections establishing)
tps = 723.959626 (excluding connections establishing)
```

- 参数解释：
- number of clients 是测试时指定的客户端数量
- number of threads 是测试时指定的每个客户端的线程数
- number of transactions actually processed 是测试结束时实际完成的事务数和计划完成的事务数，
- tps = 723.210820 (including connections establishing)
    - 包含建立网络连接开销的 TPS 值
- tps = 723.959626 (excluding connections establishing)
    - 不包含建立网络连接开销的 TPS 值


## 资料

- <https://codeday.me/bug/20180726/203876.html>
