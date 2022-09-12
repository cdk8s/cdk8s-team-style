
# Redis 安装和使用

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap

## Redis 基本介绍

- 官网：<https://redis.io/>
- 官网下载：<https://redis.io/download>
- Client 列表：<https://redis.io/clients>


## 如果你用 Spring Data Redis 依赖请注意

- 请先看官网最新支持到哪个版本的依赖：<https://docs.spring.io/spring-data/data-redis/docs/current/reference/html/#new-features>
	- 查看锚点为：`New in Spring Data Redis` 的内容
-  目前 Spring Data Redis 采用 lettuce
    - lettuce 官网对应 Redis 版本说明：<https://github.com/lettuce-io/lettuce-core/wiki/Lettuce-Versions>


## 如果你用 RedisDesktopManager 客户端请注意

- 请查看介绍中支持哪个版本：<https://github.com/uglide/RedisDesktopManager>

-------------------------------------------------------------------

## Redis 6.2.X 安装（Docker）

- 官网：<https://hub.docker.com/_/redis/>
- 创建一个宿主机目录用来存放 redis 配置文件、数据：`mkdir -p ~/docker/redis/conf ~/docker/redis/db`
- 赋权：`chmod -R 777 ~/docker/redis`
- 自己编写一个配置文件 `vim ~/docker/redis/conf/redis.conf`，内容如下：

- Redis 默认的配置文件内容：

``` ini
# 支持外网方式
bind 0.0.0.0
requirepass 123456
protected-mode no

# 不支持外网方式
bind 127.0.0.1
requirepass 123456
protected-mode yes

# 其他配置
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
pidfile /data/redis_6379.pid
loglevel notice
logfile ""
databases 16
always-show-logo no
set-proc-title yes
proc-title-template "{title} {listen-addr} {server-mode}"
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
rdb-del-sync-files no
dir /data
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-diskless-load disabled
repl-disable-tcp-nodelay no
replica-priority 100
acllog-max-len 128
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
lazyfree-lazy-user-del no
lazyfree-lazy-user-flush no
oom-score-adj no
oom-score-adj-values 0 200 800
disable-thp yes
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
stream-node-max-bytes 4096
stream-node-max-entries 100
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
dynamic-hz yes
aof-rewrite-incremental-fsync yes
rdb-save-incremental-fsync yes
jemalloc-bg-thread yes

```

- 启动镜像：

```
docker run -d -it -p 6379:6379 \
    -v ~/docker/redis/conf/redis.conf:/etc/redis/redis.conf \
    -v ~/docker/redis/db:/data \
    --restart always \
    --name cloud-redis redis:6.2 \
    redis-server /etc/redis/redis.conf
```
- 查看镜像运行情况：`docker ps`
- 进入镜像中 redis shell 交互界面：`docker exec -it cloud-redis redis-cli -h 127.0.0.1 -p 6379 -a adgredis123456`
- 重新启动服务：`docker restart cloud-redis`

-------------------------------------------------------------------

## Redis 3.X 安装（Docker）

- 官网：<https://hub.docker.com/_/redis/>
- 创建一个宿主机目录用来存放 redis 配置文件、数据：`mkdir -p ~/docker/redis/conf ~/docker/redis/db`
- 赋权：`chmod -R 777 ~/docker/redis`
- 自己编写一个配置文件 `vim ~/docker/redis/conf/redis.conf`，内容如下：

- Redis 默认的配置文件内容：

``` ini
# 安全相关配置（选填）
bind 127.0.0.1
requirepass adgredis123456
protected-mode yes

# 免密配置（选填）
bind 0.0.0.0
# 当为 no 的时候支持外网访问
protected-mode no

# 其他：
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
supervised no
pidfile /data/redis_6379.pid
loglevel notice
logfile ""
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
slave-priority 100
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
```

- 启动镜像：

```
docker run -d -it -p 6379:6379 \
    -v ~/docker/redis/conf/redis.conf:/etc/redis/redis.conf \
    -v ~/docker/redis/db:/data \
    --restart always \
    --name cloud-redis redis:3 \
    redis-server /etc/redis/redis.conf
```
- 查看镜像运行情况：`docker ps`
- 进入镜像中 redis shell 交互界面：`docker exec -it cloud-redis redis-cli -h 127.0.0.1 -p 6379 -a adgredis123456`
- 重新启动服务：`docker restart cloud-redis`

-------------------------------------------------------------------

## Redis 5.0.X 安装（Docker）

- 配置文件，有几个参数有做调整

```
# 安全相关配置（选填）
bind 127.0.0.1
requirepass adgredis123456
protected-mode yes

# 免密配置（选填）
bind 0.0.0.0
protected-mode no

port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
supervised no
pidfile /data/redis_6379.pid
loglevel notice
logfile ""
databases 16
always-show-logo yes
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
replica-priority 100
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
stream-node-max-bytes 4096
stream-node-max-entries 100
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
dynamic-hz yes
aof-rewrite-incremental-fsync yes
rdb-save-incremental-fsync yes
```

- 启动镜像：

```
docker run -d -it -p 6379:6379 \
    -v ~/docker/redis/conf/redis.conf:/etc/redis/redis.conf \
    -v ~/docker/redis/db:/data \
    --restart always \
    --name cloud-redis redis:5 \
    redis-server /etc/redis/redis.conf
```



-------------------------------------------------------------------

## Redis 离线安装（3、4、5 版本使用，6 未测试）

- 官网下载：<http://download.redis.io/releases/>

```
wget http://download.redis.io/releases/redis-3.2.9.tar.gz

tar -zxvf redis-3.2.9.tar.gz

cd redis-3.2.9
make
make PREFIX=/usr/local/redis install


# 创建目录用于存储redis配置文件
mkdir -p /usr/local/redis/config

# 复制配置文件到/usr/local/redis/config
cp /root/redis-3.2.9/redis.conf /usr/local/redis/config/


# 修改配置文件
vi /usr/local/redis/config/redis.conf

把
daemonize no 
改为
daemonize yes 

把
# requirepass foobared
改为
requirepass adgredis123456


# 创建redis.service文件
vim /etc/systemd/system/redis.service

# 添加如下内容：
[Unit]
Description=Redis
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/redis/bin/redis-server /usr/local/redis/config/redis.conf
ExecStop=/usr/local/redis/bin/redis-server -s stop
PrivateTmp=true
User=root
Group=root

[Install]
WantedBy=multi-user.target



启动redis：systemctl start redis
关闭redis：systemctl stop redis
设置开机自启：systemctl enable redis
关闭开机自启：systemctl disable redis
查看运行状态：systemctl status redis
访问客户端：/usr/local/redis/bin/redis-cli -h 127.0.0.1 -p 6379 -a adgredis123456

```



-------------------------------------------------------------------

## RedisCluster 集群（Docker 方式）

#### Redis 容器准备

- 目标：3 主 3 从（一般都是推荐奇数个 master）
- 最小集群数推荐是：3
- 测试机的最低配置推荐是：2C4G
- 拉取镜像：`docker pull registry.cn-shenzhen.aliyuncs.com/youmeek/redis-to-cluster:3.2.3`
- 重新打个 tag（旧名字太长了）：`docker tag registry.cn-shenzhen.aliyuncs.com/youmeek/redis-to-cluster:3.2.3 redis-to-cluster:3.2.3`
- 创建网段：`docker network create --subnet=172.19.0.0/16 net-redis-to-cluster`
- 宿主机创建配置文件：`mkdir -p ~/docker/redis-to-cluster/config && vim ~/docker/redis-to-cluster/config/redis.conf`

```
bind 0.0.0.0
protected-mode no
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize yes
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
logfile ""
databases 16
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir ./
slave-serve-stale-data yes
slave-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
slave-priority 100
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
lua-time-limit 5000
cluster-enabled yes
cluster-config-file nodes-6379.conf
cluster-node-timeout 15000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit slave 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
aof-rewrite-incremental-fsync yes
```

- 赋权：`chmod -R 777 ~/docker/redis-to-cluster/`
- 运行 6 个节点：
	- `docker run -it -d --name redis-to-cluster-1 -p 5001:6379 -v ~/docker/redis-to-cluster/config/redis.conf:/usr/redis/redis.conf --net=net-redis-to-cluster --ip 172.19.0.2 redis-to-cluster:3.2.3 bash`
	- `docker run -it -d --name redis-to-cluster-2 -p 5002:6379 -v ~/docker/redis-to-cluster/config/redis.conf:/usr/redis/redis.conf --net=net-redis-to-cluster --ip 172.19.0.3 redis-to-cluster:3.2.3 bash`
	- `docker run -it -d --name redis-to-cluster-3 -p 5003:6379 -v ~/docker/redis-to-cluster/config/redis.conf:/usr/redis/redis.conf --net=net-redis-to-cluster --ip 172.19.0.4 redis-to-cluster:3.2.3 bash`
	- `docker run -it -d --name redis-to-cluster-4 -p 5004:6379 -v ~/docker/redis-to-cluster/config/redis.conf:/usr/redis/redis.conf --net=net-redis-to-cluster --ip 172.19.0.5 redis-to-cluster:3.2.3 bash`
	- `docker run -it -d --name redis-to-cluster-5 -p 5005:6379 -v ~/docker/redis-to-cluster/config/redis.conf:/usr/redis/redis.conf --net=net-redis-to-cluster --ip 172.19.0.6 redis-to-cluster:3.2.3 bash`
	- `docker run -it -d --name redis-to-cluster-6 -p 5006:6379 -v ~/docker/redis-to-cluster/config/redis.conf:/usr/redis/redis.conf --net=net-redis-to-cluster --ip 172.19.0.7 redis-to-cluster:3.2.3 bash`
- 配置 redis-to-cluster-1 节点：`docker exec -it redis-to-cluster-1 bash`
	- 启动容器的 redis：`/usr/redis/src/redis-server /usr/redis/redis.conf`
- 其他 5 个节点一样进行启动。

#### 创建 Cluster 集群（通过 redis-trib.rb）

- 配置 redis-to-cluster-1 节点（或者选择其他任意一个节点）：`docker exec -it redis-to-cluster-1 bash`
- `mkdir -p /usr/redis/cluster`
- `cp /usr/redis/src/redis-trib.rb /usr/redis/cluster/`
- `cd /usr/redis/cluster/`
- 创建 Cluster 集群（会有交互）（镜像中已经安装了 ruby 了）：`./redis-trib.rb create --replicas 1 172.19.0.2:6379 172.19.0.3:6379 172.19.0.4:6379 172.19.0.5:6379 172.19.0.6:6379 172.19.0.7:6379`
	- `--replicas 1` 表示为每个主节点创建一个从节点
	- 如果正常的话，会出现下面内容：

```
>>> Creating cluster
>>> Performing hash slots allocation on 6 nodes...
Using 3 masters:
172.19.0.2:6379
172.19.0.3:6379
172.19.0.4:6379
Adding replica 172.19.0.5:6379 to 172.19.0.2:6379
Adding replica 172.19.0.6:6379 to 172.19.0.3:6379
Adding replica 172.19.0.7:6379 to 172.19.0.4:6379
M: 9c1c64b18bfc2a0586be2089f13c330787c1f67b 172.19.0.2:6379
   slots:0-5460 (5461 slots) master
M: 35a633853329c9ff25bb93a7ce9192699c2ab6a8 172.19.0.3:6379
   slots:5461-10922 (5462 slots) master
M: 8ea2bfeeeda939abb43e96a95a990bcc55c10389 172.19.0.4:6379
   slots:10923-16383 (5461 slots) master
S: 9cb00acba065120ea96834f4352c72bb50aa37ac 172.19.0.5:6379
   replicates 9c1c64b18bfc2a0586be2089f13c330787c1f67b
S: 8e2a4bb11e97adf28427091a621dbbed66c61001 172.19.0.6:6379
   replicates 35a633853329c9ff25bb93a7ce9192699c2ab6a8
S: 5d0fe968559af3035d8d64ab598f2841e5f3a059 172.19.0.7:6379
   replicates 8ea2bfeeeda939abb43e96a95a990bcc55c10389
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join......
>>> Performing Cluster Check (using node 172.19.0.2:6379)
M: 9c1c64b18bfc2a0586be2089f13c330787c1f67b 172.19.0.2:6379
   slots:0-5460 (5461 slots) master
M: 35a633853329c9ff25bb93a7ce9192699c2ab6a8 172.19.0.3:6379
   slots:5461-10922 (5462 slots) master
M: 8ea2bfeeeda939abb43e96a95a990bcc55c10389 172.19.0.4:6379
   slots:10923-16383 (5461 slots) master
M: 9cb00acba065120ea96834f4352c72bb50aa37ac 172.19.0.5:6379
   slots: (0 slots) master
   replicates 9c1c64b18bfc2a0586be2089f13c330787c1f67b
M: 8e2a4bb11e97adf28427091a621dbbed66c61001 172.19.0.6:6379
   slots: (0 slots) master
   replicates 35a633853329c9ff25bb93a7ce9192699c2ab6a8
M: 5d0fe968559af3035d8d64ab598f2841e5f3a059 172.19.0.7:6379
   slots: (0 slots) master
   replicates 8ea2bfeeeda939abb43e96a95a990bcc55c10389
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```

- 连接集群测试：
	- 进入随便一个节点：`docker exec -it redis-to-cluster-1 bash`
	- `/usr/redis/src/redis-cli -c`
	- 查看集群情况：`cluster nodes`
	- 写入数据：`set myKey myValue`，如果成功会返回：`Redirected to slot [16281] located at 172.19.0.4:6379`，可以推断它是 redis-to-cluster-3 容器
	- 暂定掉 redis-to-cluster-3 容器：`docker pause redis-to-cluster-3`
	- 重新连接：`/usr/redis/src/redis-cli -c`
	- 查看集群情况：`cluster nodes`
	- 获取值：`get myKey`
	- 重新启动 redis-to-cluster-3：`docker unpause redis-to-cluster-3`
	- 查看集群情况：`cluster nodes`
- Spring Boot 项目 Docker 容器访问 RedisCluster
	- application.yml 配置的 IP 地址：172.19.0.2 等
	- docker 容器启动增加 `--net=host` 使用宿主机网络

-------------------------------------------------------------------

## Redis 常用命令

- 命令是不区分大小写的，但是这里为了方便和后面的 key value 进行区分所以我全部写大写，你也可以用小写。
    - 但是需要注意的是：key 是完全区分大小写的，比如 key=codeBlog 和 key=codeblog 是两个键值
- 官网命令列表：<http://redis.io/commands>
- `redis-cli -h 127.0.0.1 -p 6379`，如果有密码，进入 client 后需要输入：`auth 123456`
- `SET key value`，设值。eg：`SET myblog www.upupmo.com`
- `redis-server -v`，查看服务器版本
- `info keyspace`，查看各个库的 key 使用情况
- `GET key`，取值
- `SELECT 0`，切换数据库
- `INCR key`，递增数字
- `DECR key`，递减数字
- `KEYS *`，查看当前数据库下所有的 key
- `APPEND key value`，给尾部追加内容，如果要追加的 key 不存在，则相当于 SET key value
- `STRLEN key`，返回键值的长度，如果键不存在则返回 0
- `MSET key1 value1 key2 value2`，同时设置多值
- `MGET key1 value1 key2 value2`，同时取多值
- `EXPIRE key 27`，设置指定键的生存时间，27 的单位是秒
- `TTL key`，查看键的剩余生存时间
    - 返回 -2，表示不存在，过了生存时间后被删除
    - 返回 -1，表示没有生存时间，永久存储
    - 返回正整数，表示还剩下对应的生存时间
- `PERSIST key`，清除生成时间，重新变成永久存储（重新设置 key 的值也可以起到清除生存时间的效果）
- `FLUSHDB`，清空当前数据库所有键值
- `FLUSHALL`，清空所有数据库的所有键值


## Redis Info

- 客户端下命令行：`info`
	- 参考：<http://redisdoc.com/server/info.html>

```
server 部分记录了 Redis 服务器的信息，它包含以下域：

redis_version : Redis 服务器版本
redis_git_sha1 : Git SHA1
redis_git_dirty : Git dirty flag
os : Redis 服务器的宿主操作系统
arch_bits : 架构（32 或 64 位）
multiplexing_api : Redis 所使用的事件处理机制
gcc_version : 编译 Redis 时所使用的 GCC 版本
process_id : 服务器进程的 PID
run_id : Redis 服务器的随机标识符（用于 Sentinel 和集群）
tcp_port : TCP/IP 监听端口
uptime_in_seconds : 自 Redis 服务器启动以来，经过的秒数
uptime_in_days : 自 Redis 服务器启动以来，经过的天数
lru_clock : 以分钟为单位进行自增的时钟，用于 LRU 管理


connected_clients : 已连接客户端的数量（不包括通过从属服务器连接的客户端）（常用）
client_longest_output_list : 当前连接的客户端当中，最长的输出列表
client_longest_input_buf : 当前连接的客户端当中，最大输入缓存
blocked_clients : 正在等待阻塞命令（BLPOP、BRPOP、BRPOPLPUSH）的客户端的数量


used_memory : 由 Redis 分配器分配的内存总量，以字节（byte）为单位（常用）
used_memory_human : 以人类可读的格式返回 Redis 分配的内存总量（常用）
used_memory_rss : 从操作系统的角度，返回 Redis 已分配的内存总量（俗称常驻集大小）。这个值和 top 、 ps 等命令的输出一致。（常用）
used_memory_peak : Redis 的内存消耗峰值（以字节为单位）（常用）
used_memory_peak_human : 以人类可读的格式返回 Redis 的内存消耗最高峰值（常用）
used_memory_lua : Lua 引擎所使用的内存大小（以字节为单位）（常用）
mem_fragmentation_ratio : used_memory_rss 和 used_memory 之间的比率
mem_allocator : 在编译时指定的， Redis 所使用的内存分配器。可以是 libc 、 jemalloc 或者 tcmalloc 。
used_memory_rss_human：系统给redis分配的内存（即常驻内存）（常用）
used_memory_lua_human : 系统内存大小（常用）
expired_keys : 过期的的键数量（常用）
evicted_keys : 因为最大内存容量限制而被驱逐（evict）的键数量（常用）
used_cpu_sys_children : Redis 后台进程在 内核态 消耗的 CPU（常用）
used_cpu_user_children : Redis 后台进程在 用户态 消耗的 CPU（常用）

total_connections_received: 服务器已接受过的连接总数（常用）
total_commands_processed: 服务器已处理的命令总数（常用）
```


## Redis 基准压力测试

- 默认安装包下就自带
- 官网文档：<https://redis.io/topics/benchmarks>
- 运行：`redis-benchmark -q -n 100000`
	- `-q` 表示 quiet 安静执行，结束后直接输出结果即可
	- `-n 100000` 请求 10 万次

```
PING_INLINE: 62189.05 requests per second
PING_BULK: 68634.18 requests per second
SET: 58241.12 requests per second
GET: 65445.03 requests per second
INCR: 57703.40 requests per second
LPUSH: 61199.51 requests per second
RPUSH: 68119.89 requests per second
LPOP: 58309.04 requests per second
RPOP: 63775.51 requests per second
SADD: 58479.53 requests per second
HSET: 61500.61 requests per second
SPOP: 58241.12 requests per second
LPUSH (needed to benchmark LRANGE): 59523.81 requests per second
LRANGE_100 (first 100 elements): 60350.03 requests per second
LRANGE_300 (first 300 elements): 57636.89 requests per second
LRANGE_500 (first 450 elements): 63251.11 requests per second
LRANGE_600 (first 600 elements): 58479.53 requests per second
MSET (10 keys): 56401.58 requests per second
```

- 只测试特定类型：`redis-benchmark -t set,lpush -n 100000 -q`


## K8S YAML

```
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: sculptor-boot-redis
  namespace: sculptor-boot-backend-dev
spec:
  podManagementPolicy: Parallel
  serviceName: sculptor-boot-redis
  replicas: 1
  selector:
    matchLabels:
      app: sculptor-boot-redis
  template:
    metadata:
      labels:
        app: sculptor-boot-redis
    spec:
      containers:
        - name: sculptor-boot-redis
          image: redis:4
          lifecycle:
            postStart:
              exec:
                command: [ "/bin/sh", "-c", "redis-cli config set requirepass 123456" ]
          ports:
            - containerPort: 6379
          resources:
            limits:
              cpu: 1
              memory: 1Gi
            requests:
              cpu: 0.5
              memory: 500Mi
---
apiVersion: v1
kind: Service
metadata:
  namespace: sculptor-boot-backend-dev
  name: sculptor-boot-redis
  labels:
    app: sculptor-boot-redis
spec:
  ports:
    - port: 6379
      targetPort: 6379
  selector:
    app: sculptor-boot-redis
```

-------------------------------------------------------------------

## GUI 工具

- Another Redis Desktop Manager（开源、跨平台）：<https://github.com/qishibo/AnotherRedisDesktopManager>
- RDM（收费、跨平台）




## 资料

- <http://yanshisan.blog.51cto.com/7879234/1377992>
- <https://segmentfault.com/a/1190000002685224>
- <http://itbilu.com/linux/management/4kB2ninp.html>
- <http://keenwon.com/1335.html>


