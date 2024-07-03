
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

## RedisCluster 集群

#### Redis 容器准备

- 目标：3 主 3 从，最小集群主机是 3 节点 6 个实例（一般都是推荐奇数个 master）
- 测试机的最低配置推荐是：2C4G


-------------------------------------------------------------------

## Redis 常用命令

- 命令是不区分大小写的，但是这里为了方便和后面的 key value 进行区分所以我全部写大写，你也可以用小写。
    - 但是需要注意的是：key 是完全区分大小写的，比如 key=codeBlog 和 key=codeblog 是两个键值
- 官网命令列表：<http://redis.io/commands>
- `redis-cli -h 127.0.0.1 -p 6379`，如果有密码，进入 client 后需要输入：`auth 123456`
- `redis-cli -h 127.0.0.1 -p 6379 -a 123456  monitor`，监控当前 redis 执行的命令，可以观察程序通过框架真正执行的命令
- `SET key value`，设值。eg：`SET myblog www.uptmr.com`
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
blocked_clients : 正在等待阻塞命令（BLPOP、BRPOP、BRPOPLPUSH）的客户端的数量（常用）


used_memory_human :Redis此时分配的内存总量(byte)，包含redis进程内部的开销和数据占用的内存，也包括了客户端的查询缓冲区，随着缓冲区内存使用的增长，used_memory的值也会变大（常用，常用）
    如果发现 used_memory 比 maxmemory 大得多，就证明客户端查询缓冲区出现了异常
    如果 used_memory – slave_output_buffer_size – mem_aof_buffer 的值是否超过了 maxmemory，就会发生 OOM 异常
used_memory_rss_human：向操作系统申请的内存大小（即常驻内存）这个值和 top 、 ps 等命令的输出一致，一般比 used_memory_human 值大。（常用，常用）
used_memory_peak_human : Redis 的内存消耗峰值（常用，常用）
used_memory_peak_perc：used_memory_peak / used_memory 的百分比，峰值内存占用的内存百分比（常用）
used_memory_lua : Lua 引擎所使用的内存大小（以字节为单位）（常用）
used_memory_dataset：数据占用的内存大小(used_memory - used_memory_overhead)（常用）
used_memory_dataset_perc：数据占用的内存大小百分比，数据占用的内存大小百分比,(used_memory_dataset / (used_memory - used_memory_startup))*100%（常用）
used_memory_overhead: Redis维护数据集的内部机制所需的内存开销,包括所有客户端输出缓冲区、查询缓冲区、AOF重写缓冲区和主从复制的backlog
maxmemory_human：最大内存限制，设置为 0 表示不限制，如果没有开启 AOF，可以设置为 0，如果开启了 AOF 可以设置为机子内存的 45% 大小（常用，常用）
maxmemory_policy: 内存管理策略（常用，常用）
mem_fragmentation_ratio : 碎片率(used_memory_rss / used_memory),正常(1,1.6),大于比例说明内存碎片严重，需要进行内存整理（常用，常用）
expired_keys : 过期的的键数量（常用）
mem_aof_buffer: AOF使用内存
evicted_keys : 因为最大内存容量限制而被驱逐（evict）的键数量（常用，常用）
total_connections_received: 服务器已接受过的连接总数（常用）
total_commands_processed: 服务器已处理的命令总数（常用）

请注意：
maxmemory_human 定义了的最大大小(即 used_memory_dataset 的上限)，而 used_memory_rss_human 是从操作系统的角度分配给 Redis 的实际内存。 
used_memory_rss_human 包括数据、服务器的所有开销(例如数据结构、缓冲区等)，并且可能是碎片化的。
这意味着当您的 used_memory_dataset 达到 maxmemory_human 时，used_memory_rss_human 可能会明显大于 maxmemory_human


used_cpu_user：redis进程指令在用户态所消耗的cpu时间，该值为累计值（秒）
used_cpu_sys:redis进程指令在核心态所消耗的cpu时间，该值为累计值（秒）
used_cpu_sys_children:redis后台进程指令在用户态所消耗的cpu时间，该值为累计值（秒）
used_cpu_sys_children：redis后台进程指令在核心态所消耗的cpu时间，该值为累计值（秒）
对于Redis的开发者（社区贡献者），可以通过这个信息来看到Redis运行情况，即启动一段时间或者执行某个命令一段时间之后分别耗费在内核或者用户态的时间。
user_cpu_sys 和user_cpu_sys_children的区别比较明显，一个是Redis主进程消耗，一个是后台进程消耗（后台包括RDB文件的消耗，master，slave同步产生的消耗等等）


模拟压测：
bin/redis-benchmark -q -d 1024000 -n 10000 -r 2500 -t set
往Redis中导入大量的数据，之后你再用INFO MEMORY命令查看内存信息，会发现used_memory_human的值增大，甚至比maxmemory大（前提你的maxmemory不是设置为0）。之后再继续往Redis里写数据，发生OOM问题，Redis进程被杀死（可以在redis-server进程日志中看到输出“killed”）。

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


