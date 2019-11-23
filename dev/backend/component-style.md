
# 中间件

- 理论上：不管项目大小、团队大小，永恒不变的总会有：MQ、Job、Cache。只是有些是线程级别使用，有些是中间件级别使用。

## Redis

- 复词用下划线：`PLATFORM:SYS_ROLE:1`
- 不能有特殊符号，包含空格、换行、单双引号以及其他转义字符
- key 命名：`业务名:表名:id`，比如：`PLATFORM:SYS_ROLE:1`
- key 固定部分全部大写，动态部分随意。
- 更多：
    - [阿里云Redis开发规范](https://yq.aliyun.com/articles/531067)
    - [Redis开发规范](https://blog.csdn.net/mysqldba23/article/details/69390344)

## RabbitMQ 规范

- vhost组件
    - 规则：`业务系统名_vhost`
    - 实例：`platform_vhost`
- Exchange
    - tx = topic exchange
    - fx = fanout exchange
    - dx = direct exchange
    - 规则：`业务系统名.模块名.tx或者fx、dx`
    - 实例：`platform.sys_user.tx`    
- Queue
    - 规则：`消费者:业务系统名.模块名.tx或者fx、dx.事件名`
    - 实例：`integral:platform.sys_user.tx.created`
- Routing Key
    - 规则：`业务系统名.模块名.tx或者fx、dx.事件名`
    - 实例：`platform.sys_user.tx.created`

## Elasticsearch 规范


## Kafka 规范

## Flink 规范


## WebSocket 规范

## Elasticsearch 规范

## 分布式调度

## 短信服务
## 邮件服务
## 验证码服务
## 图片存储服务
## 文件存储服务


## 故障复盘






