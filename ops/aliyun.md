
# 阿里云常用服务

## 只有上云才能撑住规模化后的发展

- 初期技术选型上尽可能寻找云支持的
- 在公司规模小，自建服务基本都做不到 99.999% 高可用
- 在公司规模发展变迅速时，如果云技术和已有技术契合，迁移成本会低很多很多
- 目前暂定只选择：[阿里云服务](https://www.aliyun.com/minisite/goods?userCode=v2zozyxz)
- 这里罗列了阿里云常用的一些：[产品](https://github.com/cdk8s/cdk8s-team-style/blob/master/ops/aliyun.md)

-------------------------------------------------------------------

## 常用配置地址

- ECS服务器管理：<https://ecs.console.aliyun.com/#/server/region/所属地区>
- 安全组管理：<https://ecs.console.aliyun.com/#/securityGroup/region/所属地区>
- RAM 访问控制：<https://ram.console.aliyun.com/overview>
- SSL证书：<https://yundun.console.aliyun.com/?spm=5176.2020520154.products-recent.dcas.e96d1e43wIAa00&p=cas>
- 域名管理：<https://dc.console.aliyun.com>
- DNS 解析：<https://dns.console.aliyun.com/#/dns/domainList>
- OSS bucket：<https://oss.console.aliyun.com/bucket>
- 短信服务：<https://dysms.console.aliyun.com>


-------------------------------------------------------------------


## 对象存储 OSS

- 能用 OSS 的就不要用 NAS
- 基本上现在常见的图片、音视频等文件格式都可以存储到 OSS
- 对象存储 OSS <https://www.aliyun.com/product/oss>
- [阿里云 OSS 实用工具](https://promotion.aliyun.com/ntms/ossedu6.html)
- [图片处理](https://help.aliyun.com/document_detail/44686.html)
- [文档预览](https://help.aliyun.com/document_detail/99373.html)
- [图片识别](https://help.aliyun.com/document_detail/99383.html)
- [视频点播](https://help.aliyun.com/product/29932.html)
- [视频直播](https://help.aliyun.com/document_detail/29951.html)
- [短视频](https://promotion.aliyun.com/ntms/act/shortvideo.html)

## 人工只能

- [爬虫风险管理](https://www.aliyun.com/product/antibot)
- [视觉智能开放平台](https://vision.aliyun.com/)
- [NLP自学习平台](https://ai.aliyun.com/nlp/nlpautoml)
- [录音文件识别](https://ai.aliyun.com/nls/filetrans)
- [实时语音识别](https://ai.aliyun.com/nls/trans)
- [深度学习框架支持和](https://help.aliyun.com/document_detail/148437.html)
- [视频内容分析](https://promotion.aliyun.com/ntms/act/video-content-create.html)
- [人脸人体](https://vision.aliyun.com/facebody)
- [文字识别](https://help.aliyun.com/document_detail/146692.html)

## 容器服务 ACK

- <https://www.aliyun.com/product/kubernetes>

## 云服务器 ECS

- <https://www.aliyun.com/product/ecs>

## 数据管理（Web 数据库管理终端）

- <https://www.aliyun.com/product/dms>

## 云数据库RDS MySQL 版

- <https://www.aliyun.com/product/rds/mysql>

## 云数据库RDS PostgreSQL 版

- <https://www.aliyun.com/product/rds/postgresql>

## 分布式关系型数据库服务 DRDS

- <https://www.aliyun.com/product/drds>

## 云数据库 POLARDB（比 DRDS 优先）

- <https://www.aliyun.com/product/polardb>

## 时序时空数据库 TSDB

- <https://www.aliyun.com/product/hitsdb>

## 时序数据库 InfluxDB

- <https://www.aliyun.com/product/hitsdb_influxdb_pre>

## 时序数据库 Prometheus

- <https://www.aliyun.com/product/hitsdb_prometheus_pre>

## 云数据库 HBase 版

- <https://cn.aliyun.com/product/hbase>

## 云数据库 ClickHouse

- <https://www.aliyun.com/product/clickhouse>

## 阿里云 · Elasticsearch

- <https://data.aliyun.com/product/elasticsearch>

## 数据管理 DMS

- <https://www.aliyun.com/product/dms>

## 云数据库 HBase 版

- <https://cn.aliyun.com/product/hbase>

## 图数据库 GDB

- <https://www.aliyun.com/product/gdb>
- 核心
    - 支持 TinkerPop Gremlin 查询语言
- 场景：
    - 构建复杂的社交网络系统
    - 构建个人信用信息系统，欺诈检测场景
    - 构建多维度电商场景，进行个性化推荐
    - 构建数据高度连接的复杂知识图谱
    - 构建网络IT拓扑图
- 集成
    - dataworks：基于dataworks，GDB支持从MySQL、ODPS、OTS等导入数据。提供了丰富的配置规则，支持表数据到图点、边数据的多种映射，包括导入自定义的常量字段等

## 云数据库 Redis 版

- <https://www.aliyun.com/product/kvstore>

## 安全加速 SCDN

- <https://www.aliyun.com/product/scdn>

## CDN

- <https://www.aliyun.com/product/cdn>

## 全站加速 DCDN

- <https://www.aliyun.com/product/dcdn>

## 负载均衡 SLB

- <https://www.aliyun.com/product/slb>


## 日志服务 LOG

- 支持 Kafka 写入
- 支持 Java log4j2、logback 写入
    - <https://developer.aliyun.com/article/409045>

- <https://www.aliyun.com/product/sls>

## 数加 · 数据集成

- <https://www.aliyun.com/product/cdp>

## API网关

- <https://www.aliyun.com/product/apigateway>

## Quick BI（倾向于离线数据报表）

- <https://data.aliyun.com/product/bi>

## DataV数据可视化（倾向于实时数据报表）

- <https://data.aliyun.com/visual/datav>

## DDoS高防IP

- <https://www.aliyun.com/product/ddos>

## 云监控

- <https://www.aliyun.com/product/jiankong>

## 堡垒机

- <https://www.aliyun.com/product/bastionhost>

## 爬虫风险管理

- <https://www.aliyun.com/product/antibot>

## 实时计算 Flink

- <https://data.aliyun.com/product/sc>

## 开放搜索

- <https://www.aliyun.com/product/opensearch>

## 消息队列 RocketMQ

- <https://www.aliyun.com/product/rocketmq>

## 消息队列 AMQP(RabbitMQ)

- <https://www.aliyun.com/product/amqp>

## 微消息队列 MQTT

- <https://www.aliyun.com/product/mq4iot>

## 消息队列 Kafka

- <https://www.aliyun.com/product/kafka>

## 消息服务 MNS

- <https://www.aliyun.com/product/mns>

## 数据传输服务 DTS

- <https://www.aliyun.com/product/dts>

## 容器服务-Kubernetes 解决方案

- <https://www.aliyun.com/solution/kubernetes>

## 企业级分布式应用服务 EDAS

- <https://cn.aliyun.com/product/edas>

## 云效联合EDAS解决方案：DevOps闭环整体架构

- <https://www.aliyun.com/solution/middleware/yunxiaoedas>

## 物联网平台

- <https://www.aliyun.com/product/iot>

## 物联网设备接入

- <https://www.aliyun.com/product/iot-deviceconnect>

## 物联网设备管理

- <https://www.aliyun.com/product/iot-devicemanagement>

## 物联网数据分析

- <https://www.aliyun.com/product/iot-dataanalytics>

## 数据库备份DBS

- <https://www.aliyun.com/product/dbs>

## 云效

- <https://www.aliyun.com/product/yunxiao>

## 移动研发平台

- <https://www.aliyun.com/solution/emas/index>

## Cloud Toolkit 

- <https://www.aliyun.com/product/cloudtoolkit>

## Web应用托管服务

- <https://www.aliyun.com/product/webx>

## Dragonwell JDK

- <https://www.aliyun.com/product/dragonwell>

## 云效-代码托管

- <https://promotion.aliyun.com/ntms/act/code.html>

## 云效-Maven公共仓库

- <https://m.aliyun.com/markets/aliyun/ali-repo>

## 容器镜像服务 ACR

- <https://www.aliyun.com/product/acr>

## 云效-制品仓库

- <https://m.aliyun.com/markets/aliyun/repo-manage>

## CodePipeline

- <https://www.aliyun.com/product/codepipeline>

## Node.js 性能平台

- <https://www.aliyun.com/product/nodejs>

## Node.js 模块仓库

- <https://help.aliyun.com/document_detail/67306.html>

## 性能测试 PTS
- <https://www.aliyun.com/product/pts>

## 移动测试

- <https://www.aliyun.com/product/mqc>

## 云效-测试平台

- <https://www.aliyun.com/product/yunxiao-testing>

## 应用实时监控服务 ARMS

- <https://www.aliyun.com/product/arms>

## 链路追踪

- <https://www.aliyun.com/product/xtrace>

## DevOps 解决方案

- <https://develop.aliyun.com/devops>


