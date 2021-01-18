# RocketMQ 安装和配置

- 基于 JDK8
- **核心：Broker 软件非常耗内存，至少要 16G 内存的机子才合适，所以不适合小企业**
- 阿里云是以 Topic 占用和 API 调用为计算费用
- 官网帮助文档：<https://rocketmq.apache.org/docs/quick-start/>
- 中文官网帮助文档：<https://github.com/apache/rocketmq/tree/master/docs/cn>
- 阿里云帮助文档：<https://help.aliyun.com/document_detail/29532.html>
- 官网扩展：<https://github.com/apache/rocketmq-externals>
- 4.3.x 版本之后支持分布式事务

## 核心概念

- 更多名词解释：<https://help.aliyun.com/document_detail/29533.html>
- Topic：消息主题，一级消息类型，生产者向其发送消息。
- 生产者：也称为消息发布者，负责生产并发送消息至Topic。
- 消费者：也称为消息订阅者，负责从Topic接收并消费消息。
- 消息：生产者向Topic发送并最终传送给消费者的数据和（可选）属性的组合。
- 消息属性：生产者可以为消息定义的属性，包含Message Key和Tag。
- Group：一类生产者或消费者，这类生产者或消费者通常生产或消费同一类消息，且消息发布或订阅的逻辑一致。
- 优势（有些是阿里云才支持）
    - 支持集群、负载均衡、水平扩展
    - 多协议接入、方便的Web控制台、资源报表、监控报警
    - 支持：普通消息、事务消息、定时和延时消息、顺序消息、消息轨迹（默认没有开启）
    - 支持：消息重试、消息过滤（类似 RabbitMQ 的 routingKey 功能）、至少投递一次（消费幂等）、消息可查询
    - 支持：集群消费、广播消费、批量消息
- nameServer
- broker（用于消息存储和生产消息转发）


## Docker 安装 RocketMQ（不推荐）

- 官网不推荐 Docker 部署
- 有个 docker-compose 部署：<https://github.com/apache/rocketmq-docker>
- 但是目前大家都是用其他人封装的：
    - <https://www.cnblogs.com/qa-freeroad/p/13693060.html>
    - <https://my.oschina.net/u/4030990/blog/3232512>

## 解压安装方式

- 官网下载：<https://rocketmq.apache.org/dowloading/releases/>
    - 当前最新版本为：4.8.0（20210118）
    - 选择：Binary: rocketmq-all-4.8.0-bin-release.zip
- 启动 nameServer

```
如果机子内存不够需要调整下
runserver.sh
JAVA_OPT="${JAVA_OPT} -server -Xms4g -Xmx4g -Xmn2g -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=320m"


nohup sh /Users/meek/software/rocketmq-all-4.8.0-bin-release/bin/mqnamesrv &

tail -f /Users/meek/software/rocketmq-all-4.8.0-bin-release/logs/rocketmqlogs/namesrv.log

最后关闭：
sh /Users/meek/software/rocketmq-all-4.8.0-bin-release/bin/mqshutdown namesrv
```

- 启动 broker

```
如果机子内存不够需要调整下
runbroker.sh
JAVA_OPT="${JAVA_OPT} -server -Xms8g -Xmx8g -Xmn4g"

nohup sh /Users/meek/software/rocketmq-all-4.8.0-bin-release/bin/mqbroker -n localhost:9876 &
tail -f /Users/meek/software/rocketmq-all-4.8.0-bin-release/logs/rocketmqlogs/broker.log 

先关闭：
sh /Users/meek/software/rocketmq-all-4.8.0-bin-release/bin/mqshutdown broker
```

- 安装控制台（基于 Spring Boot 开发）
- 可以重点参考这篇文章：<https://www.cnblogs.com/qa-freeroad/p/13690509.html>

```
git clone --depth=1 https://github.com/apache/rocketmq-externals.git

用 IntelliJ IDEA 打开 rocketmq-console 方便修改配置

如果需要修改配置文件：
/src/main/resources/application.properties
默认端口是：8080
修改 rocketmq.config.namesrvAddr=localhost:9876（如果有多个节点可以用英文逗号隔开）

pom.xml 修改为最新版本
<rocketmq.version>你的RocketMQ版本</rocketmq.version>

mvn clean package -Dmaven.test.skip=true

java -jar target/rocketmq-console-*.jar

访问：http://localhost:8080
```

- console 界面介绍，左上角可以切换中文
    - 运维：主要是设置nameserver和配置 VIPChannel
        - VIPChannel 针对的是topic的优先级，相当于在消息处理的时候，有些topic可以走 VIPChannel，可以优先被处理
    - 驾驶舱：控制台的dashboard，可以分别按broker和主题来查看消息的数量和趋势。
    - **集群：** 整个RocketMq的集群情况，包括分片，编号，地址，版本，消息生产和消息消费的TPS等，这个在做性能测试的时候可以作为数据指标。
    - **主题：** 即topic，可以新增/更新topic；也看查看topic的信息，如状态，路由，消费者管理和发送消息等。
    - **消费者：** 可以在当前broker中查看/新建消费者group，包括消费者信息和消费进度
    - **生产者：** 可以在当前broker中查看生产组下的生产者group，包生产者信息和生产者状态
    - **消息：** 可以按照topc，messageID，messageKey分别查询具体的消息
    - 用户中心：切换语言和登陆相关（登陆需要在console的配置中打开对应配置，默认不需要登陆）
    - 其中最常用的是集群，主题，消费者和消息这四部分。 


## 资料

- <>





