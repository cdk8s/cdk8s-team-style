


## 离线数仓

- 每天处理前一天数据，也就是一批一批处理数据，也叫做批处理
- 前端用户行为埋点数据采集
- 后端埋点采集
- MySQL 业务数据采集
- ETL
- 即时查询（补充对于那些没有被 spark 预先设计好调度统计的查询场景）
- 数据可视化（BI可视化：Metabase、Superset）
- 集群监控
- 元数据管理（也就是记录他们是如何一步一步递进的：ods > dwd > dws > dwt > ads ）
- 质量监控（监控计算出来结果的质量）

## 测试环境

- 最小配置
- header1：4C8G
- worker1：2C4G
- worker2：2C4G

## Hadoop、Yarn 架构

```
NameNode and ResourceManager 主节点
DataNode and NodeManager 工作节点


YARN (Yet Another Resource Negotiator)。YARN的核心思想是将资源管理和Job的调度/监控进行分离

YARN的核心组件可以分为两大部分：

全局组件

Resource Manager（RM）: 作为全局统一的资源管理、调度、分配。Resource Manager由Scheduler（调度器：本质上是一种策略）和Applicatio Manager（应用程序管理器，ASM：负责管理Client用户提交的应用）组成。Scheduler根据节点的容量、队列情况，为Application分配资源；Application Manager接受用户提交的请求，在节点中启动Application Master，并监控Application Master的状态、进行必要的重启。
Node Manager（NM）: 在每一个节点上都有一个Node Manager作为代理监控节点的资源使用情况（cpu, memory, disk, network）并向Resource Manager上报节点状态。
Per-applicaiton组件

Application Master（AM）: 负责数据处理job的执行调度。Application Master与Resource Manager进行沟通，获取资源进行计算。得到资源后，与节点上的Node Manager进行沟通，在分配的Container汇总执行任务，并监控任务执行的情况。（每当 Client 提交一个 Application 时候，就会新建一个 ApplicationMaster 。由这个 ApplicationMaster 去与 ResourceManager 申请容器资源，获得资源后会将要运行的程序发送到容器上启动，然后进行分布式计算。）
Container: 资源的一种抽象方式，它封装了某个节点上的多维度资源，如内存、CPU、磁盘、网络等，当Application Master向Resource Manager申请资源时，Resource Manager为Application Master返回的资源便是Container。
```

## hadoop 相关配置文件的参数解释

- <https://hadoop.apache.org/docs/r3.1.3/>
- 打开官网看左侧菜单的最底部，有一个 Configuration，其中包含如下文件的配置说明：

```
core-default.xml
hdfs-default.xml
hdfs-rbf-default.xml
mapred-default.xml
yarn-default.xml
Deprecated Properties

```


## hdfs 多目录存储

```
HDFS的DataNode节点保存数据的路径由dfs.datanode.data.dir参数决定，其默认值为file://${hadoop.tmp.dir}/dfs/data，若服务器有多个磁盘，必须对该参数进行修改。如服务器磁盘如上图所示，则该参数应修改为如下的值。
所以参数 ${hadoop.tmp.dir} 侧面上也可以说明决定了 namenode、datanode 的存储路径
<property>
    <name>dfs.datanode.data.dir</name>
<value>file:///hd2/dfs/data2,file:///hd3/dfs/data3,file:///hd4/dfs/data4</value>
</property>
其中：/hd2，/hd3，/hd4 开头都是挂载的其他磁盘路径地址
注意：而且这个配置不能同步到所有服务器，因为每个节点的多目录配置可以不一致。单独配置即可。
```

## 集群数据均衡

```
1）不同节点间数据均衡（数据是发生真实转移，要保证内网网络顺畅，没有调度任务运行的空闲时间）
开启数据均衡命令：
start-balancer.sh -threshold 10
对于参数10，代表的是集群中各个节点的磁盘空间利用率相差不超过10%，比如一个节点硬盘用了50%，另外一个节点用了70%，就是相差20%，超过了10%就会进行调整
中途停止数据均衡命令，下次可以继续执行上次命令
stop-balancer.sh
2）磁盘间数据均衡，支持跨节点（hadoop3之后新特性）
（1）生成均衡计划（只有一块磁盘，就不会生成计划）
hdfs diskbalancer -plan hadoop103（节点服务器的hostname）
（2）执行均衡计划
hdfs diskbalancer -execute hadoop103.plan.json
（3）查看当前均衡任务的执行情况
hdfs diskbalancer -query hadoop103
（4）取消均衡任务
hdfs diskbalancer -cancel hadoop103.plan.json
```



 
-------------------------------------------------------------------

## 离线数据数仓

### 数仓分类

- 行为数仓
- 业务数仓

### 表分类

- 实体表：具体业务表
    - 每日全量同步
- 维度表：码表，枚举表，状态表，分类表，城市编号等
    - 每日全量同步
- 事务型事实表：一旦发生就不会改变，比如交易流水表、操作日志、出入库记录
    - 每日增量同步
- 周期型事实表：随着业务变化不断生成的数据，比如订单状态，请假审批状态，贷款申请流程
    - 每日新增及变化量

### 用户行为埋点数据（日志采集）

- <https://github.com/wenthomas/my-bigdata-study/tree/master/my-log-collector>
- 容量评估
    - 每天日活跃用户100万，每人一天平均100条：100万*100条 = 10000万条 = 1 亿条
    - 每条日志 1KB 左右.每天 1 亿条：100000000 / 1024 / 1024 = 约 100GB
    - 数仓ODS层采用LZO+parquet存储：100G 压缩为 10G 左右
    - 数仓DWD层采用LZO + parquet存储：10G 左右
    - 数仓DWS层轻度聚合存储（为了快速运算，不压缩）： 50G 左右
    - 数仓ADS层数据星很小：忽略不计
    - 保存3副本： 70G*3=210G
    - 半年内不矿容服务器来算： 210G*180天 = 约 37T
    - 预留20%〜30%Buf=37T/0.7=53T
- 埋点数据格式
    - 每隔一段时间批量发送
    - 来源（单个）：APP、PC、小程序
    - 公共字段（单个）
        - AppKey
        - 设备标识
        - 用户标识
        - 程序版本号
        - 操作系统
        - 操作系统版本
        - 系统语言
        - 渠道号
        - APP 系统版本
        - 国家
        - 省份
        - 城市
        - 地区
        - IP
        - 手机品牌
        - 手机具体型号
        - 屏幕宽高
        - 运行商名称
        - 网络模式
        - 经度
        - 纬度
        - 发送消息前的初始化时间
    - 业务字段（多个）
        - 操作事件生产时间
        - 操作事件类型编号
        - 操作事件内容（ key-value 多个。一般到这一层就结束，不要再多一层，不然解析比较麻烦）
            - 广告展示
            - 广告点击
            - 下拉刷新
            - 加载更多
            - 不感兴趣


### 业务数据 RDS（MySQL）

- 每天活跃用户100万，每天下单的用户10万，每人每天产生的业务数据 10条,每条日志 1KB 左右：10万*10条*1KB=1G左右
- 数仓四层存储：1G*3=3G
- 保存3副本： 3G*3=9G
- 半年内不护容服务器来算： 9G*180天=约1.6T
- 预留20%〜30%Buf=1.6T/0.7=2T


### 爬虫数据

### 流程

- DataStudio
    - 数据开发
        - 新建业务流程
        - 调度配置
- FunctionStudio
    - 自定义 UDTF


-------------------------------------------------------------------

## 实时数据数仓

### 用户行为埋点数据（日志采集）

- 后端埋点：Filebeat 采集 > Kafka > Logstash > DataHub > DataWorks > 实时计算 > DataHub > AnalyticDB > DataV
- 前端埋点：Nginx + Nginx-kafka-module > Kafka > Logstash > DataHub > DataWorks > 实时计算 > DataHub > AnalyticDB > DataV
- 参考资料：
    - [Filebeat+Kafka+Logstash+ElasticSearch+Kibana搭建完整版](https://www.cnblogs.com/jiashengmei/p/8857053.html)
    - [Logstash + DataHub + MaxCompute/StreamCompute 进行实时数据分析](https://blog.csdn.net/weixin_34059951/article/details/91664451)
    - []()
    - []()
    - []()
    - []()

### DataHub（数据总线）

- <https://www.aliyun.com/product/datahub>
- <https://datahub.console.aliyun.com/datahub>
- Logstash DataHub 插件（优先）：<https://help.aliyun.com/document_detail/47451.html>
- Flume DataHub 插件：<https://help.aliyun.com/document_detail/143572.html>

### 业务数据 RDS（MySQL）

- RDS > DTS > DataHub > DataWorks > 实时计算 > DataHub > AnalyticDB
- 添加本地电脑 IP 到白名单中
    - 本地 IP 可以写成 112.32.36.0/24 代表 1 ~ 255 都可以访问
- 申请外网地址
- 创建账号

### DTS（数据传输服务）

- <https://www.aliyun.com/product/dts>
- 数据同步
    - MySQL > DataHub
    - MySQL > MySQL
    - MySQL > Elasticsearch
    - MySQL > Kafka
    - MySQL > MaxCompute
    - MySQL > POLARDB
    - MySQL > AnalyticDB for MySQL
    - MySQL > AnalyticDB for PostgreSQL
- 数据迁移
- 数据订阅

### 实时数仓分层

- ods 原始数据层，保持数据原貌不做处理 datahub
    - 业务数仓
        - 商品信息表
        - 品牌信息表
        - 产品分类表
        - 用户信息表
        - 订单表
        - 订单明细表
        - 支付流水表
        - 省市表
        - 地区表（华中，华南等）
- dwd 数据明细层，数据清洗 datahub
    - 预处理
        - 空值去除/补充
        - 脏数据
    - 业务数仓
        - 订单表
        - 用户信息表
        - 订单明细表
        - 商品信息表
        - 地区省市表
- dws 服务数据层，轻度聚合、汇总 datahub
    - 业务数仓
        - 用户当日交易行为宽表
    - 行为数仓
        - 每日活跃表（趋势图-折线图）
        - 每周活跃表（趋势图-折线图）
        - 每月活跃表（趋势图-折线图）
        - 每日新增用户表（趋势图-折线图）
        - 每日留存用户表（趋势图-折线图）
- ads 统计报表层，最终报告输出值 AnalyticDB
    - 业务数仓
        - 年龄销售统计表（饼图，年龄段维度）
        - 地区销售统计表（色彩地图，地区维度）
        - 商品销售统计表（柱状图，商品名称维度）
    - 行为数仓
        - PV
        - UV
        - 跳出率
        - 平均访问时长
        - 新增客户总数
        - 渠道日活（饼图）
        - 每日新增设备数量表
        - 流失用户数量表
        - 沉默用户数量表
        - 留存用户数量表
        - 留存用户数比率表
        - 本周回流用户数量表
        - 最新七天内连续三天活跃用户数量表
        - 连续三周活跃用户数量表
- dim 维度表命名前缀
- df（day full） 每日全量导入命名前缀
- di（day increment） 每日增量导入命名前缀


### 实时计算（Flink）

- <https://data.aliyun.com/product/sc>
- 独享模式
    - 创建集群
        - 集群详情里面有一个 ENI 是集群的 IP 列表，要复制到 AnalyticDB 白名单中
    - 创建集群下项目

### DataWorks（数据工厂）

- <https://data.aliyun.com/product/ide>
- 创建工作空间，绑定实时计算（独享模式）
    - 绑定集群
    - 绑定集群下项目
- 进入数据开发
- DataStudio
- Stream Studio
    - 新建业务流程
        - 新建任务
- 任务模式
    - DAG 组件模式（拖拉拽模式）
    - SQL 模式（FlinkSQL/BLink）
        - [官网帮助文档](https://help.aliyun.com/document_detail/111864.html)
- 任务组件
    - 数据源表
        - [创建数据源表](https://help.aliyun.com/knowledge_list/62516.html)
        - DataHub
        - Kafka
    - 数据维表
        - [数据维表](https://help.aliyun.com/knowledge_list/62518.html)
        - RDS
    - 数据处理
        - UDTF
        - Select
        - Filter
        - Join
        - GroupBy
        - UnionAll
        - 固定列切分
        - 动态列切分
    - 数据结果表
        - [创建数据结果表](https://help.aliyun.com/knowledge_list/62517.html)
        - RDS
        - DataHub
        - AnalyticDB
        - Elasticsearch
- 执行计划

### AnalyticDB for MySQL

- <https://www.aliyun.com/product/ads>
- 数据安全中添加实时计算 IP、本地电脑 IP 到白名单中
    - 本地 IP 可以写成 112.32.36.0/24 代表 1 ~ 255 都可以访问
- 申请外网地址
- 创建账号
- 特点
    - 可处理百亿数据，无需分库分表
    - 实时化写入
    - 高并发查询（PB 级别）
    - ETL
- 维度表或者普通表：<https://help.aliyun.com/document_detail/128514.html>

### AnalyticDB for PostgreSQL

- <https://www.aliyun.com/product/gpdb>

### DataV

- AnalyticDB > DataV