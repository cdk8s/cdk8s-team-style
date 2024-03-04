
# CDK8S 研发风格


## 作者新方向，感谢支持

- [开发全平台产品（文字版）](https://github.com/cdk8s/cdk8s-team-style/blob/master/full-stack/README.md)
- [UPGPT - 简洁 AI 助手](https://upgpt.uptmr.com/)

## 只有上云才能撑住规模化后的发展

- 初期技术选型上尽可能寻找云支持的
- 在公司规模小，自建服务基本都做不到 99.999% 高可用
- 在公司规模发展变迅速时，如果云技术和已有技术契合，迁移成本会低很多很多
- 目前暂定只选择：[阿里云服务](https://www.aliyun.com/minisite/goods?userCode=v2zozyxz)
- 这里罗列了阿里云常用的一些：[产品](https://github.com/cdk8s/cdk8s-team-style/blob/master/ops/aliyun.md)

## 别人的人生（Life）

> They say we die twice. Once when the breath leaves our body, and once when the last person we know says our name. -- Stand Up Guys

- 人生短暂，你不应该浪费时间在意他人眼光
- 每个人活着都应有属于自己的意义，衷心地希望你能找到.Orz.
- [《人生七年》(第 1 ~ 9 部)](https://movie.douban.com/tag/#/?sort=T&tags=%E4%BA%BA%E7%94%9F%E4%B8%83%E5%B9%B4)
- [《穷富翁大作战》(第 2 部)](https://movie.douban.com/subject/25926859/)

## 线上仓库

- <https://github.com/cdk8s/cdk8s-team-style>
- <https://gitee.com/cdk8s/cdk8s-team-style>

## 声明（Notice）

- **本系列没有终点，时间仓促，有部分还未完成，有部分会随着我们认知的变化而变化**
- 该专题主要表达我们团队的：`管理理念和研发执行力`，更多的是引起每个人关注思考
- 很多事情，我们不知道什么是对的，但是错的也许已经遇到过，能避则避
- 有部分内容适合中型公司，小型公司不建议参考
- 后续发布的专题都会基于此风格下
- **最后：** 不打嘴炮，没有银弹，请 `持怀疑态度` 看待本专题任何内容

## 介绍（Introduce）

- **该专题的作用很明确：寻找志同道合的人，引发自身的思考**
- 我们重沟通
- 我们对细节和结果都很看重
    - 我们不想：`手术很成功，病人却死了`，也有人说：`没有过程的结果是垃圾，没有结果的过程是放屁`
    - 细节可以提炼出 **可复用** 的方法论
    - 结果可以验证方法论是否有效
- 我们追求：`度量驱动 + 数据驱动` 下的 `可复用模式`
- 我们并不迂腐，不是想去定规矩而定规矩，也没有强迫症、绝对完美主义
- 我们只是在追寻律动，一种能平衡生活和工作的节奏感（或者叫做生活与工作的最佳实践）
    - 我们认为这种节奏感在规则下面更容易找到，也更容易做到 DevOps
    - 可能会在这个过程失去部分想象力，但是我相信很多人还没到谈想象力（创新）的地步

## 认为（Preference）


- 只有 macOS 系统是最适合 **国内** 开发者
- 只有 JetBrains 的 IDE 是最适合开发者
- 只有 Google 能摆渡
- 只有上云才能撑住规模化后的企业发展，符合当今以及未来的企业发展模式
    - 初期技术选型上，尽可能寻找已经有云支持的技术类型
    - 在公司规模小，自建服务基本都做不到 99.999% 高可用
    - 在公司规模变大后，有云的支持，迁移、扩容成本会低很多很多
- 以上是肯定句，不接受反驳，不引战，只接受建议
    - 我们知道国内有大量 Eclipse、Visual Studio Code 的粉丝，也有大量的 Windows 和 Linux 粉丝，我们尊重别人的选择
    - 我对 VSC 也是喜欢的，只是目前它更适合于个人。在推广整个团队规范和开发体验上，IDE 有更好的优势。
- 以下是我们的早期作品，我们只是想表达：我们和大家的经验都是类似的，我们没有做盲目的否定他人信仰这件事
    - 大学和工作初期使用的是 NetBeans + Eclipse + MyEclipse，后面工作几年全部都是 IntelliJ IDEA
    - 我们在 Windows + macOS + Ubuntu 下的软件列表：[UPUPMO](https://upupmo.com)
    - 我们对 macOS 的理解：[点击我](https://github.com/cdk8s/cdk8s-team-style/blob/master/os/macOS/README.md)
    - 我们对 Linux 的理解：[点击我](https://github.com/cdk8s/cdk8s-team-style/blob/master/os/linux/README.md)
    - 我们对 IntelliJ IDEA 的理解：[点击我](https://github.com/judasn/IntelliJ-IDEA-Tutorial)

## 坚信（Believe）

- 坚信
    - 标准先行、标准先行、标准先行
    - 工作和生活是可以平衡
    - 团队信息传达要准确
    - 团队目标一致，优先级一致
    - 每个人懂得换位思考，学会聆听
    - 每个人的信用积累容易，损害简单
    - 努力给自己找标签、贴标签，固化自己又改变自己
    - 不害怕风险，勇敢分享
    - 我们的风格能帮我们能找到一起好好玩的人
- 它能
    - 降低新人学习成本
    - 降低维护成本，增强可重构可行性
    - 研发提效，降低沟通成本
    - 方便自动代码生成器生成代码
    - 对外宣传团队理念的表达方式


## 硬件（Hardware）

- 硬件是所有软件的基础，是团队合作的基础，我们很不希望大家开发的时候总是在抱怨这个卡、那个慢
- 我们推荐还没有经济实力情况下使用黑苹果，有经济实力后购买原生苹果产品
- 相关硬件配置推荐：[点击我](https://github.com/cdk8s/cdk8s-team-style/blob/master/other/hardware.md)


## 细分（Category）

### 管理（PM）

- [工作方式](https://github.com/cdk8s/cdk8s-team-style/blob/master/pm/working.md)
- [人才体系](https://github.com/cdk8s/cdk8s-team-style/blob/master/pm/team-system.md)
- [激励](https://github.com/cdk8s/cdk8s-team-style/blob/master/pm/team-manage.md)
- [团队组建](https://github.com/cdk8s/cdk8s-team-style/blob/master/pm/team-build.md)
- [无尽的会议](https://github.com/cdk8s/cdk8s-team-style/blob/master/pm/meeting.md)
- [面试 / 考核](https://github.com/cdk8s/cdk8s-team-style/blob/master/pm/interview.md)

### 产品（Product）

- [软件需求](https://github.com/cdk8s/cdk8s-team-style/blob/master/product/requirement.md)
- 原型
- 问卷设计
- 数据思维

### 设计（Design）

- [UI 风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/design/ui-style.md)
- 交互思维
- 产品思维


### 开发共识（Consensus）

- [EditConfig 风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/common/editconfig-style.md)
- [Git 风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/common/git-style.md)
- [Git 多账号体系](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/common/git-multi-account.md)
- [HTTP 请求风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/common/http-request.md)
- [Mock 调试](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/common/mock.md)
- [UML 建模](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/common/uml-style.md)

### 后端（Backend）

- [数据库风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/db-style.md)
- [MySQL 转 PostgreSQL 经验](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/postgresql.md)
- [中间件](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/component-style.md)
- [Spring 项目风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/java/spring-project-style.md)
- [Java 命名风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/java/java-names.md)
- [程序日志输出风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/java/java-log-style.md)
- [Lombok](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/java/java-lombok.md)
- [Swagger](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/java/java-swagger.md)
- [Hibernate Validator 请求参数校验](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/java/hibernate-validator-style.md)
- [MapStruct - Java bean 映射工具](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/backend/java/java-mapstruct.md)

### 前端（Frontend）

- [前端开发风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/frontend/frontend-style.md)
- [命名风格](https://github.com/cdk8s/cdk8s-team-style/blob/master/dev/frontend/frontend-names.md)


### 测试（Test）

- [测试思维](https://github.com/cdk8s/cdk8s-team-style/blob/master/test/test-style.md)


### 运维（Operations）

- [监控思维](https://github.com/cdk8s/cdk8s-team-style/blob/master/ops/monitor.md)
- [阿里云](https://github.com/cdk8s/cdk8s-team-style/blob/master/ops/aliyun.md)
- [华为云](https://github.com/cdk8s/cdk8s-team-style/blob/master/ops/huaweicloud.md)
- [腾讯云](https://github.com/cdk8s/cdk8s-team-style/blob/master/ops/tencent-cloud.md)
- [安全思维](https://github.com/cdk8s/cdk8s-team-style/blob/master/ops/safe.md)

### 营销（Marketing）

- [微信公众号运营](https://github.com/cdk8s/cdk8s-team-style/blob/master/marketing/weixin.md)
- [SEO 思维](https://github.com/cdk8s/cdk8s-team-style/blob/master/marketing/seo.md)


### 数据（Data）

- 数据采集
- 数据建模
- 数据分析
- 运营监控
- 可视化
- 用户画像
- 智能推荐
- 产品实验
- 数据之外

### 操作系统（OS）

- [macOS 系统](https://github.com/cdk8s/cdk8s-team-style/blob/master/os/macOS/README.md)
- [CentOS 系统](https://github.com/cdk8s/cdk8s-team-style/blob/master/os/linux/README.md)

### 其他（Other）

- [写作意识](https://github.com/cdk8s/cdk8s-team-style/blob/master/other/read-write.md)
- [IDE 思维](https://github.com/cdk8s/cdk8s-team-style/blob/master/other/ide-style.md)


## 生活用品指南

- [购物指南-程序员-系列](https://github.com/cdk8s/cdk8s-team-style/blob/master/life/1111/)

## 学习逻辑

- 要解决什么问题
- 基础技术点、核心技术点是什么（也用于面试）
- 项目实战


## 联系（Contact）

- 邮箱：`cdk8s#qq.com`
- 微信公众号

![公众号](https://cdn.uptmr.com/upupmo-article/old-gitnavi/cdk8s_qr_300px.png)


## 忧伤

![功归一篑](https://cdn.uptmr.com/upupmo-article/old-gitnavi/build-railway.png)


