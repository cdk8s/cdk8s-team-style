
# 监控

- 很多时候数据不一定可靠，直觉也未必不可相信
- 样本量的可靠性
- 评估方法
- 数据分析
- 对于程序异常的认真劲要高于任何事，所以在收集异常这件事上，决不能放低警惕
- 什么都可以不会，程序员不会打 log 要死一百遍

## 开关

- 有些监控是特殊场景下使用的，需要开关来开启，开启后需要收集大量细腻度的信息
- Apollo

## 程序埋点

- 调用次数、耗时
- 执行次数、耗时
- 一般埋点出入口
    - 外部请求
    - 请求外部
    - 缓存请求
    - 存储请求
    - MQ 处理
    - Job 处理
    - 搜索处理


## 业务埋点

- 不推荐埋点在客户端，理论上客户端提交的所有数据都会提交到后端，并且调整收集策略，后端会更加方便，除非没办法的数据
- 埋点的数据来自报表要展示什么，没必要什么东西都进行收集
- 收集要素
    - 时间
        - 时间戳
    - 地点
        - IP 地址
        - GPS 坐标
    - 人物
        - 已登录用户：用户ID
        - 未登录用户：访问 IP + 设备 ID
    - 做了什么（做不同的事情，上传的数据不一样）
        - 登录 / 注册
        - 搜索
        - 查看
        - 加入购物车
        - 下单
        - 支付
        - 退货
        - 咨询
        - 投诉
        - 使用时长
    - 怎么做
        - 使用设备
        - 使用操作系统
        - 系统语言
        - 使用浏览器类型
        - 使用 APP 版本
        - 请求 Referer
        - 来源渠道
        - 来源入口
        - 移动设备信息
            - 屏幕分辨率
            - 屏幕颜色
            - 是否 WIFI
            - 网络运营商
- 常用指标
    - 转化率
    - 留存
    - 销量
    - 客单价
- 一般在 Controller 层进行埋点
- 综合埋点也可以用 AOP、Filter 等


## Prometheus

- Prometheus Client API

```
import io.prometheus.client.Gauge;
import io.prometheus.client.Histogram;
import io.prometheus.client.Counter;
import io.prometheus.client.Summary;
import io.prometheus.client.CollectorRegistry;
import io.prometheus.client.exporter.PushGateway;
import io.prometheus.client.exporter.MetricsServlet;
```



## 慢 SQL 收集、分析

- 看输出到哪个存储系统中合适
- 要能区分出 GET、POST 请求的地址和请求参数

## 慢接口收集、分析

## 中间件监控

## Spring Boot Actuator（应用度量）

## Prometheus + Grafana（容器 + 应用度量）

## SkyWalking（应用程序监控）

## Flink（用户画像）

## Metabase（简易 BI）

## Superset（正常 BI）

## ELK（日志监控）

## 数据分析

## Sentry（前端监控）


## 爬虫分析

## 恶意用户分析

## 恶意攻击

## Dashboard



