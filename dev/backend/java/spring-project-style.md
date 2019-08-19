
# Spring 项目风格

## 提交代码之前要做的

- 做代码检查，看是否有哪里不小心多敲了一些字符
- 提交勾选：`Optimize imports`
- 检查 TODO 是否还有未完成功能

## 必须使用 Lombok


## 必须 mapstruct

## YAML 优先 properties


## POJO 规范

- 必须使用 Lombok
- 不允许使用基础类型：int、long、boolean 等
- 不允许 isXXXX 开头，可以改为：boolIsDelete 或是根据数据库模型的：deleteEnum
- 前端参数必须有 Hibernate Validator 注解
- 包命名
- pojo
    - entity（数据库映射）
    - vo（页面结果）
    - dto（接口响应）
    - param（接口请求）
    - bo（service 业务处理）
        - mq
        - cache
        - event
        - 等


## 设计模式重要性

## 无状态

- 保证可伸缩性


## 配置表、开关表的重要性

- 尽可能满足需求多变的场景
- 开关多样化可以尽可能避免回滚和多次发布

## 了解 io / cpu 优先级

- io 优先
- cpu 优先
- 数据库读优先
- 数据库写优先
- 更新与新增操作频率比
    - 更新的复杂度高于新增

## 了解监控数据

## 单元测试

## 压力测试

## JProfiler / VisualVM


## CPU 耗时 / 火焰图

## OOM

## Maven

- 阿里云国内镜像
- release 和 snapshot 的版本要区分好
    - 在开发阶段可以用 snapshot，发到生产必须是 release
    - 每迭代一个版本结束，对应的 pom 版本号都要跟着调整，不允许遗漏，并发到私服

## 配置表思维


## 重构时机

- 不允许在开发新功能、改 Bug 阶段进行重构

