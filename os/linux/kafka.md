# Kafka 安装和配置


## 对于版本

- 由于 Kafka 经常会被连接到各个地方去，所以对于 Kafka 的版本，一般不能用太新的，要看你用在什么地方。
- [Flink 的要求](https://ci.apache.org/projects/flink/flink-docs-release-1.6/dev/connectors/kafka.html)
- [Spark 的要求](https://spark.apache.org/docs/latest/streaming-kafka-integration.html)
- [Spring 的要求](http://projects.spring.io/spring-kafka/)
- 注意：Topic 的命名采用驼峰命名，不要带点、下划线，有些场景会出问题，虽然用这类方式命名不会报错

## 消息系统的好处

- 解耦（各个业务系统各自为政，有各自新需求，各自系统自行修改，只通过消息来通信）
- 大系统层面的扩展性（不用改旧业务系统代码，增加新系统，接收新消息）
- 异步通信（一个消息，多个业务系统来消费。某些场景可以堆积到一定程度再去消费）
- 缓冲（解耦某些需要长时间处理业务）


## Kafka 介绍

> A distributed streaming platform

- 官网：<https://kafka.apache.org/>
- Github：<https://github.com/apache/kafka>
    - 主要是由 Java 和 Scala 开发
- 官网下载：<https://kafka.apache.org/downloads>
- 当前最新稳定版本（201803）：**1.0.1**
- 官网 quickstart：<https://kafka.apache.org/quickstart>
- 运行的机子不要小于 2G 内存
- Kafka 流行的主要原因：
    - 支持常见的发布订阅功能
    - 分布式
    - 高吞吐量（听说：普通单机也支持每秒 100000 条消息的传输）
    - 磁盘数据持久化，消费者 down 后，重新 up 的时候可以继续接收前面未接收到的消息
    - 支持流数据处理，常见于大数据
- 核心概念：
    - Producer：生产者（业务系统），负责发布消息到 broker
    - Consumer：消费者（业务系统），向 broker 读取消息的客户端
    - Broker：可以理解为：存放消息的管道（kafka 软件节点本身）
    - Topic：可以理解为：消息主题、消息标签、消息通道、消息队列（物理上不同 Topic 的消息分开存储，根据 Partition 参数决定一个 Topic 的消息保存于一个或多个 broker 上。作为使用者，不用关心 Topic 实际物理存储地方。）
    - Partition：是物理上的概念，每个 Topic 包含一个或多个 Partition。一般有几个 Broker，填写分区最好是等于大于节点值。分区目的主要是数据分片，解决水平扩展、高吞吐量。当 Producer 生产消息的时候，消息会被算法计算后分配到对应的分区，Consumer 读取的时候算法也会帮我们找到消息所在分区，这是内部实现的，应用层面不用管。
    - Replication-factor：副本。假设有 3 个 Broker 的情况下，当副本为 3 的时候每个 Partition 会在每个 Broker 都会存有一份，目的主要是容错。
        - 其中有一个 Leader。
        - 如果你只有一个 Broker，但是创建 Topic 的时候指定 Replication-factor 为 3，则会报错
    - **（重要）** Consumer Group：每个 Consumer 属于一个特定的 Consumer Group（可为每个 Consumer 指定 group name，若不指定 group name 则属于默认的 group）一般一个业务系统集群指定同一个 group id，然后一个业务系统集群只能一个节点来消费同一个消息。
        - Consumer Group 信息存储在 zookeeper 中，需要通过 zookeeper 的客户端来查看和设置
        - 如果某 Consumer Group 中 consumer 数量少于 partition 数量，则至少有一个 consumer 会消费多个 partition 的数据
        - 如果 consumer 的数量与 partition 数量相同，则正好一个 consumer 消费一个 partition 的数据
        - 如果 consumer 的数量多于 partition 的数量时，会有部分 consumer 无法消费该 topic 下任何一条消息。所以，如果想要让消费者加快消费，可以在 Spring Boot 注解上指定要消费的分区，这样可以让多个消费者分别消费相同 topic 下不同分区的数据
        - 如果想重复消费，可以创建不同的消费者组，订阅相同的 topic。当新的消费组运行起来后，topic 中的所有历史数据都会从头开始消费一遍
        - 具体实验可以看这篇文章：[Kafka深度解析](http://www.jasongj.com/2015/01/02/Kafka%E6%B7%B1%E5%BA%A6%E8%A7%A3%E6%9E%90/)
    - Record：消息数据本身，由一个 key、value、timestamp 组成
- 业界常用的 docker 镜像：
    - [wurstmeister/kafka-docker（不断更新，优先）](https://github.com/wurstmeister/kafka-docker/)
    - Spring 项目选用依赖包的时候，对于版本之间的关系可以看这里：<http://projects.spring.io/spring-kafka/>
        - 目前（201803）
        - spring boot 2.0 以上基础框架版本，kafka 版本 1.0.x，推荐使用：spring-kafka 2.1.4.RELEASE
        - spring boot 2.0 以下基础框架版本，kafka 版本 0.11.0.x, 1.0.x，推荐使用：spring-kafka 1.3.3.RELEASE
- 官网 quickstart 指导：<https://kafka.apache.org/quickstart>
- 常用命令：
    - wurstmeister/kafka-docker 容器中 kafka home：`cd /opt/kafka`
    - 假设我的 zookeeper 地址：`10.135.157.34:2181`，如果你有多个节点用逗号隔开
    - 列出所有 topic：`bin/kafka-topics.sh --list --zookeeper 10.135.157.34:2181`
    - 创建 topic：`bin/kafka-topics.sh --create --topic kafka-test-topic-1 --partitions 3 --replication-factor 1 --zookeeper 10.135.157.34:2181`
        - 创建名为 kafka-test-topic-1 的 topic，3个分区分别存放数据，数据备份总共 2 份
    - 查看特定 topic 的详情：`bin/kafka-topics.sh --describe --topic kafka-test-topic-1 --zookeeper 10.135.157.34:2181`
    - 删除 topic：`bin/kafka-topics.sh --delete --topic kafka-test-topic-1 --zookeeper 10.135.157.34:2181`
      - 默认使用 kafka-topics --delete 命令删除topic时并没有真正的删除，而是把topic标记为：“marked for deletion”，导致重新创建相同名称的Topic时报错“already exists”。
      - 默认情况下Kafka是禁用了删除Topic的操作，所以在执行Topic删除的时候只是将删除的Topic标记为“marked for deletion”状态。可以通过修改Kafka服务的配置参数启用。
      - 如果要真正删除topic，需要同时考虑删除 zookpeer 中的数据
    - 更多命令可以看：<http://orchome.com/454>
- 假设 topic 详情的返回信息如下：
    - `PartitionCount:6`：分区为 6 个
    - `ReplicationFactor:3`：副本为 3 个
    - `Partition: 0 Leader: 3`：Partition 下标为 0 的主节点是 broker.id=3
        - 当 Leader down 掉之后，其他节点会选举中一个新 Leader
    - `Replicas: 3,1,2`：在 `Partition: 0` 下共有 3 个副本，broker.id 分别为 3,1,2
    - `Isr: 3,1,2`：在 `Partition: 0` 下目前存活的 broker.id 分别为 3,1,2

```
Topic:kafka-all    PartitionCount:6    ReplicationFactor:3    Configs:
    Topic: kafka-all    Partition: 0    Leader: 3    Replicas: 3,1,2    Isr: 3,1,2
    Topic: kafka-all    Partition: 1    Leader: 1    Replicas: 1,2,3    Isr: 1,2,3
    Topic: kafka-all    Partition: 2    Leader: 2    Replicas: 2,3,1    Isr: 2,3,1
    Topic: kafka-all    Partition: 3    Leader: 3    Replicas: 3,2,1    Isr: 3,2,1
    Topic: kafka-all    Partition: 4    Leader: 1    Replicas: 1,3,2    Isr: 1,3,2
    Topic: kafka-all    Partition: 5    Leader: 2    Replicas: 2,1,3    Isr: 2,1,3
```


----------------------------------------------------------------------------------------------


## Docker 单个实例部署（2.8.1）

- 注意 Spring Boot 的要求：<https://spring.io/projects/spring-kafka>
- 作者 [github](https://github.com/wurstmeister/kafka-docker) 看下 tag 目录，切换不同 tag，然后看下 Dockerfile 里面的 kafka 版本号
- 作者 [docker hub](https://hub.docker.com/r/wurstmeister/kafka/tags) 看下 tag 有 kafka 版本号
- 这里的 kafka 对外网暴露端口是 9094，内网端口是 9092

```
我宿主机 ip 为：192.168.31.109
先创建目录：mkdir -p ~/docker/kafka ~/docker/zookeeper/data
vim ~/docker/docker-compose-kafka.yml

version: '3.2'
services:
  zookeeper:
    image: wurstmeister/zookeeper
    container_name: zookeeper
    restart: always
    volumes:
      - /Users/meek/docker/zookeeper/data:/data
    ports:
      - 2181:2181

  kafka_node1:
    image: wurstmeister/kafka:2.13-2.8.1
    container_name: kafka_node1
    restart: always
    ports:
      - 9092:9092
      - 9999:9999
    environment:
      HOSTNAME_COMMAND: "docker info | grep ^Name: | cut -d' ' -f 2"
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.31.109:9092
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_ADVERTISED_PORT: 9094
      KAFKA_PORT: 9092
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      KAFKA_LOG_RETENTION_HOURS: 168
      JMX_PORT: 9999
      KAFKA_JMX_OPTS: "-Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=192.168.31.109 -Dcom.sun.management.jmxremote.rmi.port=9999"
    volumes:
      - /Users/meek/docker/kafka:/kafka
      - /etc/localtime:/etc/localtime
    depends_on:
      - zookeeper

```

- 启动：`docker-compose -p zookeeper_kafka -f ~/docker/docker-compose-kafka.yml up -d`
- 停止：`docker-compose -p zookeeper_kafka -f ~/docker/docker-compose-kafka.yml stop`
- 访问：<http://127.0.0.1:9000>
- 测试：
    - 进入 kafka 容器：`docker exec -it kafka_node1 /bin/bash`
    - 验证 jmx 是否开启成功：打开 jconsole，输入：`192.168.31.109:9999` 没有账号密码，直接连接
    - 根据官网 Dockerfile 说明，kafka home 应该是：`cd /opt/kafka`
    - 创建 topic 命令：`bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic my-topic-test`
    - 查看 topic 命令：`bin/kafka-topics.sh --list --zookeeper zookeeper:2181`
    - 删除 topic：`bin/kafka-topics.sh --delete --topic my-topic-test --zookeeper zookeeper:2181`
    - 给 topic 发送消息命令：`bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my-topic-test`，然后在出现交互输入框的时候输入你要发送的内容
    - 再开一个终端，进入 kafka 容器，接受消息：`bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic-test --from-beginning`
        - 其中 `--from-beginning` 参数表示在启动该客户端的时候接受前面 kafka 的所有记录。不加这个参数，则旧数据不会收到，生产者新生产的消息才会接收到。
    - 此时发送的终端输入一个内容回车，接受消息的终端就可以收到。


----------------------------------------------------------------------------------------------

## Kafka 常用命令

```
创建 Topic
参数 --topic 指定 Topic 名，--partitions 指定分区数，--replication-factor 指定备份数：
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
如果 kafka 目录在 zk 中的子目录，则需要也配置上：
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181/kafka --replication-factor 1 --partitions 1 --topic test

列出所有 Topic
/usr/local/kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181 

查看具体 Topic
/usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic test 

查看 topic 指定分区 offset 的最大值或最小值（time 为 -1 时表示最大值，为 -2 时表示最小值）
/usr/local/kafka/bin/kafka-run-class.sh kafka.tools.GetOffsetShell --topic test --time -1 --broker-list 127.0.0.1:9092 --partitions 0 


删除 Topic
/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --topic test --delete 


生产消息
/usr/local/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test 

查看消费者 Group 列表
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list

查看指定 Group 详情
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --describe

消费消息，从头开始
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
消费消息，从尾部开始取数据，必需要指定分区：
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --offset latest --partition 0
消费消息，从尾部开始取数据，取指定个数
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --offset latest --partition 0 --max-messages 10

指定 Group 进行消费
/usr/local/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test -group test_group --from-beginning

删除 Group 中 Topic
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --topic test --delete

删除 Group
/usr/local/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --delete


平衡 leader
/usr/local/kafka/bin/kafka-preferred-replica-election.sh --bootstrap-server localhost:9092

自带压测工具
/usr/local/kafka/bin/kafka-producer-perf-test.sh --topic test --num-records 100 --record-size 1 --throughput 100 --producer-props bootstrap.servers=localhost:9092 

```


----------------------------------------------------------------------------------------------



## Docker 多机多实例部署（外网无法访问）

- 三台机子：
    - 内网 ip：`172.24.165.129`，外网 ip：`47.91.22.116`
    - 内网 ip：`172.24.165.130`，外网 ip：`47.91.22.124`
    - 内网 ip：`172.24.165.131`，外网 ip：`47.74.6.138`
- 修改三台机子 hostname：
    - 节点 1：`hostnamectl --static set-hostname youmeekhost1`
    - 节点 2：`hostnamectl --static set-hostname youmeekhost2`
    - 节点 3：`hostnamectl --static set-hostname youmeekhost3`
- 三台机子的 hosts 都修改为如下内容：`vim /etc/hosts`

```
172.24.165.129 youmeekhost1
172.24.165.130 youmeekhost2
172.24.165.131 youmeekhost3
```

- 开发机设置 hosts：

```
47.91.22.116 youmeekhost1
47.91.22.124 youmeekhost2
47.74.6.138 youmeekhost3
```


#### Zookeeper 集群

- 节点 1：

```
docker run -d --name=zookeeper1 --net=host --restart=always \
-v /data/docker/zookeeper/data:/data \
-v /data/docker/zookeeper/log:/datalog \
-v /etc/hosts:/etc/hosts \
-e ZOO_MY_ID=1 \
-e "ZOO_SERVERS=server.1=youmeekhost1:2888:3888 server.2=youmeekhost2:2888:3888 server.3=youmeekhost3:2888:3888" \
zookeeper:latest
```


- 节点 2：

```
docker run -d --name=zookeeper2 --net=host --restart=always \
-v /data/docker/zookeeper/data:/data \
-v /data/docker/zookeeper/log:/datalog \
-v /etc/hosts:/etc/hosts \
-e ZOO_MY_ID=2 \
-e "ZOO_SERVERS=server.1=youmeekhost1:2888:3888 server.2=youmeekhost2:2888:3888 server.3=youmeekhost3:2888:3888" \
zookeeper:latest
```


- 节点 3：

```
docker run -d --name=zookeeper3 --net=host --restart=always \
-v /data/docker/zookeeper/data:/data \
-v /data/docker/zookeeper/log:/datalog \
-v /etc/hosts:/etc/hosts \
-e ZOO_MY_ID=3 \
-e "ZOO_SERVERS=server.1=youmeekhost1:2888:3888 server.2=youmeekhost2:2888:3888 server.3=youmeekhost3:2888:3888" \
zookeeper:latest
```



#### 先安装 nc 再来校验 zookeeper 集群情况

- 环境：CentOS 7.4
- 官网下载：<https://nmap.org/download.html>，找到 rpm 包
- 当前时间（201803）最新版本下载：`wget https://nmap.org/dist/ncat-7.60-1.x86_64.rpm`
- 安装并 ln：`sudo rpm -i ncat-7.60-1.x86_64.rpm && ln -s /usr/bin/ncat /usr/bin/nc`
- 检验：`nc --version`

#### zookeeper 集群测试

- 节点 1 执行命令：`echo stat | nc youmeekhost1 2181`，能得到如下信息：

```
Zookeeper version: 3.4.11-37e277162d567b55a07d1755f0b31c32e93c01a0, built on 11/01/2017 18:06 GMT
Clients:
 /172.31.154.16:35336[0](queued=0,recved=1,sent=0)

Latency min/avg/max: 0/0/0
Received: 1
Sent: 0
Connections: 1
Outstanding: 0
Zxid: 0x0
Mode: follower
Node count: 4
```

- 节点 2 执行命令：`echo stat | nc youmeekhost2 2181`，能得到如下信息：

```
Zookeeper version: 3.4.11-37e277162d567b55a07d1755f0b31c32e93c01a0, built on 11/01/2017 18:06 GMT
Clients:
 /172.31.154.17:55236[0](queued=0,recved=1,sent=0)

Latency min/avg/max: 0/0/0
Received: 1
Sent: 0
Connections: 1
Outstanding: 0
Zxid: 0x100000000
Mode: leader
Node count: 4
```

- 节点 3 执行命令：`echo stat | nc youmeekhost3 2181`，能得到如下信息：

```
Zookeeper version: 3.4.11-37e277162d567b55a07d1755f0b31c32e93c01a0, built on 11/01/2017 18:06 GMT
Clients:
 /172.31.65.88:41840[0](queued=0,recved=1,sent=0)

Latency min/avg/max: 0/0/0
Received: 1
Sent: 0
Connections: 1
Outstanding: 0
Zxid: 0x100000000
Mode: follower
Node count: 4
```

##### Kafka 集群

- 节点 1 执行：

```
docker run -d --net=host --name=kafka1 \
--restart=always \
--env KAFKA_BROKER_ID=1 \
--env KAFKA_ZOOKEEPER_CONNECT=youmeekhost1:2181,youmeekhost2:2181,youmeekhost3:2181 \
--env KAFKA_LOG_DIRS=/data/docker/kafka/logs \
--env HOSTNAME_COMMAND="docker info | grep ^Name: | cut -d' ' -f 2" \
--env KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT \
--env KAFKA_ADVERTISED_PROTOCOL_NAME=OUTSIDE \
--env KAFKA_ADVERTISED_PORT=9094 \
--env KAFKA_PROTOCOL_NAME=INSIDE \
--env KAFKA_PORT=9092 \
--env KAFKA_AUTO_CREATE_TOPICS_ENABLE=true \
--env KAFKA_LOG_RETENTION_HOURS=168 \
--env KAFKA_HEAP_OPTS="-Xmx1G -Xms1G" \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /etc/localtime:/etc/localtime \
-v /data/docker/kafka/logs:/data/docker/kafka/logs \
-v /etc/hosts:/etc/hosts \
wurstmeister/kafka:latest
```

- 节点 2 执行：

```
docker run -d --net=host --name=kafka2 \
--restart=always \
--env KAFKA_BROKER_ID=2 \
--env KAFKA_ZOOKEEPER_CONNECT=youmeekhost1:2181,youmeekhost2:2181,youmeekhost3:2181 \
--env KAFKA_LOG_DIRS=/data/docker/kafka/logs \
--env HOSTNAME_COMMAND="docker info | grep ^Name: | cut -d' ' -f 2" \
--env KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT \
--env KAFKA_ADVERTISED_PROTOCOL_NAME=OUTSIDE \
--env KAFKA_ADVERTISED_PORT=9094 \
--env KAFKA_PROTOCOL_NAME=INSIDE \
--env KAFKA_PORT=9092 \
--env KAFKA_AUTO_CREATE_TOPICS_ENABLE=true \
--env KAFKA_LOG_RETENTION_HOURS=168 \
--env KAFKA_HEAP_OPTS="-Xmx1G -Xms1G" \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /etc/localtime:/etc/localtime \
-v /data/docker/kafka/logs:/data/docker/kafka/logs \
-v /etc/hosts:/etc/hosts \
wurstmeister/kafka:latest
```

- 节点 3 执行：

```
docker run -d --net=host --name=kafka3 \
--restart=always \
--env KAFKA_BROKER_ID=3 \
--env KAFKA_ZOOKEEPER_CONNECT=youmeekhost1:2181,youmeekhost2:2181,youmeekhost3:2181 \
--env KAFKA_LOG_DIRS=/data/docker/kafka/logs \
--env HOSTNAME_COMMAND="docker info | grep ^Name: | cut -d' ' -f 2" \
--env KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT \
--env KAFKA_ADVERTISED_PROTOCOL_NAME=OUTSIDE \
--env KAFKA_ADVERTISED_PORT=9094 \
--env KAFKA_PROTOCOL_NAME=INSIDE \
--env KAFKA_PORT=9092 \
--env KAFKA_AUTO_CREATE_TOPICS_ENABLE=true \
--env KAFKA_LOG_RETENTION_HOURS=168 \
--env KAFKA_HEAP_OPTS="-Xmx1G -Xms1G" \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /etc/localtime:/etc/localtime \
-v /data/docker/kafka/logs:/data/docker/kafka/logs \
-v /etc/hosts:/etc/hosts \
wurstmeister/kafka:latest
```

#### Kafka 集群测试

- 在 kafka1 上测试：
    - 进入 kafka1 容器：`docker exec -it kafka1 /bin/bash`
    - 根据官网 Dockerfile 说明，kafka home 应该是：`cd /opt/kafka`
    - 创建 topic 命令：`bin/kafka-topics.sh --create --zookeeper youmeekhost1:2181,youmeekhost2:2181,youmeekhost3:2181 --replication-factor 3 --partitions 3 --topic my-topic-test`
    - 查看 topic 命令：`bin/kafka-topics.sh --list --zookeeper youmeekhost1:2181,youmeekhost2:2181,youmeekhost3:2181`
    - 给 topic 发送消息命令：`bin/kafka-console-producer.sh --broker-list youmeekhost1:9092 --topic my-topic-test`，然后在出现交互输入框的时候输入你要发送的内容
- 在 kafka2 上测试：
    - 进入 kafka2 容器：`docker exec -it kafka2 /bin/bash`
    - 接受消息：`cd /opt/kafka && bin/kafka-console-consumer.sh --bootstrap-server youmeekhost2:9092 --topic my-topic-test --from-beginning`
- 在 kafka3 上测试：
    - 进入 kafka3 容器：`docker exec -it kafka3 /bin/bash`
    - 接受消息：`cd /opt/kafka && bin/kafka-console-consumer.sh --bootstrap-server youmeekhost3:9092 --topic my-topic-test --from-beginning`
- 如果 kafka1 输入的消息，kafka2 和 kafka3 能收到，则表示已经成功。


#### Kafka 认证配置

- 可以参考：[Kafka的SASL/PLAIN认证配置说明](http://www.2bowl.info/kafka%e7%9a%84saslplain%e8%ae%a4%e8%af%81%e9%85%8d%e7%bd%ae%e8%af%b4%e6%98%8e/)



-------------------------------------------------------------------

## GUI 工具


#### EFAK（以前叫做 Kafka Eagle）

- 官网：<https://github.com/smartloli/EFAK>
- Kafka 集群较小的情况下，用单节点部署即可，如果集群较大，可以考虑分布式部署。具体可以参考：[Kafka Eagle分布式模式](https://www.cnblogs.com/smartloli/p/15732794.html)

```
Linux、macos：

配置好 JAVA_HOME

配置 kafka JMX 可以监听消费者情况
在 kafka 启动脚本 kafka-server-start.sh 增加一句：
export JMX_PORT="9999"


下载地址：https://github.com/smartloli/kafka-eagle-bin/tags
解压 tar -zxvf kafka-eagle-bin-2.1.0.tar.gz

配置 KE_HOME：
export KE_HOME=/Users/meek/my-software/efak-web-2.1.0
export PATH=$PATH:$KE_HOME/bin



修改配置文件给单机使用，使用 MySQL 存储：

DROP DATABASE IF EXISTS `ke`;
CREATE DATABASE IF NOT EXISTS `ke` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;
USE `ke`;

vim /Users/meek/my-software/efak-web-2.1.0/conf/system-config.properties

# efak 支持一个软件管理多个 kafka 集群，有多个可以这样写：efak.zk.cluster.alias=cluster1,cluster2,cluster3，后面的集群配置依次 cluster1 内容进行补充
efak.zk.cluster.alias=cluster1
# 多个 zk 可以这样写：
# cluster1.zk.list=192.168.31.109:2181,192.168.31.108:2181,192.168.31.107:2181
cluster1.zk.list=192.168.31.109:2181
cluster1.zk.acl.enable=false
cluster1.zk.acl.schema=digest
cluster1.zk.acl.username=test
cluster1.zk.acl.password=test123
cluster1.efak.broker.size=20
kafka.zk.limit.size=16
efak.webui.port=8048
efak.distributed.enable=false
efak.cluster.mode.status=master
efak.worknode.master.host=localhost
efak.worknode.port=8085

# kafka 默认没有开启 jmx，记得开启，可以不需要账号密码，只要开放好 9999 端口即可
cluster1.efak.jmx.acl=false
cluster1.efak.jmx.user=keadmin
cluster1.efak.jmx.password=keadmin123
cluster1.efak.jmx.ssl=false
cluster1.efak.jmx.truststore.location=/data/ssl/certificates/kafka.truststore
cluster1.efak.jmx.truststore.password=ke123456

cluster1.efak.offset.storage=kafka
cluster1.efak.jmx.uri=service:jmx:rmi:///jndi/rmi://%s/jmxrmi
efak.metrics.charts=true
efak.metrics.retain=15
efak.sql.topic.records.max=5000
efak.sql.topic.preview.records.max=10
efak.topic.token=keadmin
cluster1.efak.sasl.enable=false
cluster1.efak.sasl.protocol=SASL_PLAINTEXT
cluster1.efak.sasl.mechanism=SCRAM-SHA-256
cluster1.efak.sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="kafka" password="kafka-eagle";
cluster1.efak.sasl.client.id=
cluster1.efak.blacklist.topics=
cluster1.efak.sasl.cgroup.enable=false
cluster1.efak.sasl.cgroup.topics=

# 修改自己的 MySQL 连接
efak.driver=com.mysql.cj.jdbc.Driver
efak.url=jdbc:mysql://127.0.0.1:3306/ke?useUnicode=true&characterEncoding=UTF-8&zeroDateTimeBehavior=convertToNull
efak.username=root
efak.password=123456



启动：
cd ${KE_HOME}/bin
chmod +x ke.sh 
ke.sh start
ke.sh stop


访问：http://127.0.0.1:8048
admin
123456
默认密码可以进入 UI 后，点击右上角：Reset 进行修改。也可以通过 MySQL 直接修改。

重点关注：
http://127.0.0.1:8048/topic/list 可以看到有哪些 topic，以及对应有哪些消费组，具体到某个 topi 详情页的 LogSize 字段表示有多少条数据，消费组下 Lag（滞后，未消费的意思）值是多少
http://127.0.0.1:8048/consumers 可以看到有哪些消费者节点，叫什么组名，消费哪些 topic，当前消费到 Offset 的值是什么


KSQL 格式：
有多个分区支持在多个分区中查询，
可以查询出所有不管是已消费、未消费的所有消息
支持模糊查询，
一次最多查询5000条记录，要查询全量只能通过 kafka 原始命令行，建议通过 offset 字段分批查也行。
select * from `my-topic-test` where `partition` in (0) and msg like '%链接%' limit 10
select * from `my-topic-test` where `partition` in (0,1,2) and msg like '%链接%' limit 10
select * from `my-topic-test` where `partition` in (0) and `offset` in (1000) limit 10
select * from `my-topic-test` where `partition` in (0) and `offset` > 4000 limit 10
select * from `my-topic-test` where `partition` in (0) and `offset` > 4000 and `date` > '2022-06-25 00:51:28' limit 10
select * from `my-topic-test` where `partition` in (0) and `timespan` > 1656089490855 limit 10
select * from `my-topic-test` where `partition` in (0) and `timespan` > 1656089490855 and `timespan` < 1656089499579 limit 10
```



#### LogiKM

- 官网：<https://github.com/didi/LogiKM>

#### kafkaUI-lite 管理 Kafka

- 项目地址：<https://gitee.com/freakchicken/kafka-ui-lite>
- 它的 docker 是无效的，所以建议直接用 tar 运行


#### Kafka 单纯监控 KafkaOffsetMonitor（不推荐）

- Github 官网：<https://github.com/quantifind/KafkaOffsetMonitor>
    - README 带了下载地址和运行命令
    - 只是已经很久不更新了

#### 部署 kafka-manager（不推荐）

- Github 官网：<https://github.com/yahoo/kafka-manager>
    - 注意官网说明的版本支持
- 节点 1（没成功）：`docker run -d --name=kafka-manager1 --restart=always -p 9000:9000 -e ZK_HOSTS="youmeekhost1:2181,youmeekhost2:2181,youmeekhost3:2181" sheepkiller/kafka-manager:latest`
- 源码类安装可以看：[Kafka监控工具—Kafka Manager](http://www.2bowl.info/kafka%e7%9b%91%e6%8e%a7%e5%b7%a5%e5%85%b7-kafka-manager/)
- Kafka manager 是一款管理 + 监控的工具，比较重




-------------------------------------------------------------------

```
请下载kafka-ui-lite.tar.gz包并解压

# 终端启动
sh bin/kafkaUI.sh start
# 守护启动
sh bin/kafkaUI.sh -d start
# 关闭后台启动的进程
sh bin/kafkaUI.sh stop

启动后访问：http://127.0.0.1:8889/

```


----------------------------------------------------------------------------------------------


```
- hosts: header1
  remote_user: root
  tasks:
    - debug:
        msg:
          - "启动命令：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-server-start.sh -daemon /usr/local/kafka_2.11-2.4.1/config/server.properties"
          - "停止命令：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-server-stop.sh"
          - "查看所有topic：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-topics.sh --zookeeper header1:2181,worker1:2181,worker2:2181/kafka --list"
          - "查看指定topic：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-topics.sh --zookeeper header1:2181,worker1:2181,worker2:2181/kafka --describe --topic myTopicName"
          - "创建指定topic，topic 命名不能有下划线、点：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-topics.sh --zookeeper header1:2181,worker1:2181,worker2:2181/kafka --create --replication-factor 3 --partitions 2 --topic myTopicName"
          - "删除指定topic：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-topics.sh --zookeeper header1:2181,worker1:2181,worker2:2181/kafka --delete --topic myTopicName"
          - "发送消息：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-console-producer.sh --broker-list header1:9092,worker1:9092,worker2:9092 --topic myTopicName"
          - "接收消息，只接收当前的：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-console-consumer.sh --bootstrap-server header1:9092,worker1:9092,worker2:9092 --topic myTopicName"
          - "接收消息，包括前面的消息：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-console-consumer.sh --bootstrap-server header1:9092,worker1:9092,worker2:9092 --from-beginning --topic myTopicName"
          - "修改分区数：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-topics.sh --zookeeper header1:2181,worker1:2181,worker2:2181/kafka --alter --topic myTopicName --partitions 6"
    - debug:
        msg:
          - "查看当前消费者列表：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-consumer-groups.sh --bootstrap-server header1:9092,worker1:9092,worker2:9092 --list"
          - "根据消费者名查看当前消费情况：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-consumer-groups.sh --bootstrap-server header1:9092,worker1:9092,worker2:9092 --describe --group 前面的查询出的消费者"
    - debug:
        msg:
          - "生产者压力测试：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-producer-perf-test.sh  --topic myTopicName --record-size 100 --num-records 100000 --throughput -1 --producer-props bootstrap.servers=header1:9092,worker1:9092,worker2:9092"
          - "参数：record-size是一条信息有多大，单位是字节"
          - "参数：num-records是总共发送多少条信息。"
          - "参数：throughput 是每秒多少条信息，设成-1，表示不限流，可测出生产者最大吞吐量"
          - "测试结果：100000 records sent, 92764.378479 records/sec (8.85 MB/sec), 161.54 ms avg latency, 688.00 ms max latency, 15 ms 50th, 626 ms 95th, 678 ms 99th, 687 ms 99.9th"
          - "测试结果表示：一共写入10w条消息，吞吐量为 8.85 MB/sec，每次写入的平均延迟为 161.54 ms 毫秒，最大的延迟为 688.00 毫秒"
    - debug:
        msg:
          - "消费者压力测试：sh /usr/local/kafka_2.11-2.4.1/bin/kafka-consumer-perf-test.sh --broker-list header1:9092,worker1:9092,worker2:9092 --topic myTopicName --fetch-size 10000 --messages 100000 --threads 1"
          - "参数：fetch-size 指定每次fetch的数据的大小"
          - "参数：messages 总共要消费的消息个数"
          - "测试结果：2021-07-10 01:37:13:088, 2021-07-10 01:37:13:601, 9.5436, 18.6036, 100075, 195077.9727, 1625852233293, -1625852232780, -0.0000, -0.0001"
          - "测试结果表示：开始测试时间，测试结束数据，共消费数据 9.5436MB，吞吐量 18.6036MB/s，共消费 100075 条，平均每秒消费 195077.9727 条"
    - debug:
        msg: "kafka 监控工具：https://www.kafka-eagle.org/index.html"
```

- Spring Boot 依赖：

```xml
<dependency>
	<groupId>org.springframework.kafka</groupId>
	<artifactId>spring-kafka</artifactId>
	<version>1.3.3.RELEASE</version>
</dependency>

<dependency>
	<groupId>org.apache.kafka</groupId>
	<artifactId>kafka-clients</artifactId>
	<version>1.0.1</version>
</dependency>

<dependency>
	<groupId>org.apache.kafka</groupId>
	<artifactId>kafka-streams</artifactId>
	<version>1.0.1</version>
</dependency>
```

- 项目配置文件：bootstrap-servers 地址：`instance-3v0pbt5d:9092`（这里端口是 9092 别弄错了）

----------------------------------------------------------------------------------------------


----------------------------------------------------------------------------------------------


## 其他资料

- [管理Kafka的Consumer-Group信息](http://lsr1991.github.io/2016/01/03/kafka-consumer-group-management/)
- [Kafka--Consumer消费者](http://blog.xiaoxiaomo.com/2016/05/14/Kafka-Consumer%E6%B6%88%E8%B4%B9%E8%80%85/)
- <http://www.ituring.com.cn/article/499268>
- <http://orchome.com/kafka/index>
- <https://www.jianshu.com/p/263164fdcac7>
- <https://www.cnblogs.com/wangxiaoqiangs/p/7831990.html>
- <http://www.bijishequ.com/detail/536308>
- <http://lanxinglan.cn/2017/10/18/%E5%9C%A8Docker%E7%8E%AF%E5%A2%83%E4%B8%8B%E9%83%A8%E7%BD%B2Kafka/>
- <https://www.cnblogs.com/ding2016/p/8282907.html>
- <http://blog.csdn.net/fuyuwei2015/article/details/73379055>
- <https://segmentfault.com/a/1190000012990954>
- <http://www.54tianzhisheng.cn/2018/01/04/Kafka/>
- <https://renwole.com/archives/442>
- <http://www.bijishequ.com/detail/542646?p=85>
- <http://blog.csdn.net/zhbr_f1/article/details/73732299>
- <http://wangzs.leanote.com/post/kafka-manager%E5%AE%89%E8%A3%85>
- <https://cloud.tencent.com/developer/article/1013313>
- <http://blog.csdn.net/boling_cavalry/article/details/78309050>
- <https://www.jianshu.com/p/d77149efa59f>
- <http://www.bijishequ.com/detail/536308>
- <http://blog.51cto.com/13323775/2063420>
- <http://lanxinglan.cn/2017/10/18/%E5%9C%A8Docker%E7%8E%AF%E5%A2%83%E4%B8%8B%E9%83%A8%E7%BD%B2Kafka/>
- <http://www.cnblogs.com/huxi2b/p/7929690.html>
- <http://blog.csdn.net/HG_Harvey/article/details/79198496>
- <http://blog.csdn.net/vtopqx/article/details/78638996>
- <http://www.weduoo.com/archives/2047>
- <https://blog.52itstyle.com/archives/2358/>

