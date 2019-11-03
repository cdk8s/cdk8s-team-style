
# 数据库风格

### 限制

- 所有 Text，Blob 等大字段的数据，都必须存储到另外的独立表中，然后有业务 ID 关联业务主表

### 线上更新脚本规则（必须中的必须）

- DDL（数据定义语言）和 DML（数据操纵语言）必须分开成两个文件
- DDL 是指：CREATE TABLE/VIEW/INDEX
- DML 是指：INSERT/UPDATE/DELETE DATA

### 创建数据库

- 库名：最多 32 个字符

```
DROP DATABASE IF EXISTS `oauth_sso`;
CREATE DATABASE IF NOT EXISTS `oauth_sso` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;
USE `oauth_sso`;
```


### 创建数据表

- 表名：最多 32 个字符
- 只有 varchar 才需要指定位数，其他的一律不允许出现数字
- 在做判断的时候会当做空字符处理：[相关文章](https://blog.csdn.net/zcl_love_wx/article/details/78799719)
- 关键字和保留字列表：<https://dev.mysql.com/doc/refman/5.7/en/keywords.html>

```
DROP TABLE IF EXISTS `sys_user`;

CREATE TABLE `sys_user`
(
    `id`                   bigint      NOT NULL COMMENT '主键ID',
    `username`             varchar(50) NOT NULL COMMENT '用户账号',
    `user_password`        varchar(50) NOT NULL COMMENT '登录密码',
    `password_salt`        varchar(10) NOT NULL COMMENT '密码盐:放于密码后面',
    `user_email`           varchar(50) NULL COMMENT '邮箱地址',
    `telephone`            varchar(20) NULL COMMENT '固话',
    `mobile_phone`         varchar(20) NULL COMMENT '手机号',
    `gender_enum`          tinyint     NOT NULL DEFAULT '1' COMMENT '性别:[1=保密=PRIVACY, 2=男性=MALE, 3=女性=FEMALE, 4=中性=NEUTRAL]max=4',
    `register_type_enum`   tinyint     NOT NULL DEFAULT '1' COMMENT '注册方式:[1=系统预置=SYSTEM_INIT, 2=后台管理系统新增=MANAGEMENT_ADD, 3=主动注册=REGISTER, 4=被邀请注册=INVITE]max=4',
    `register_origin_enum` tinyint     NOT NULL DEFAULT '1' COMMENT '注册来源:[1=WEB方式=WEB, 2=安卓APP=ANDROID, 3=苹果APP=IOS, 4=H5=H5, 5=微信小程序=WECHAT_MINI_PROGRAM, 6=微信公众号=WECHAT_OFFICIAL_ACCOUNT]max=6',
    `state_enum`           tinyint     NOT NULL DEFAULT '1' COMMENT '启用状态:[1=启用=ENABLE, 2=禁用=DISABLE]max=2',
    `delete_enum`          tinyint     NOT NULL DEFAULT '1' COMMENT '删除状态:[1=未删除=NOT_DELETED, 2=已删除=DELETED]max=2',
    `create_date`          bigint      NOT NULL COMMENT '创建时间',
    `create_user_id`       bigint      NOT NULL COMMENT '创建人',
    `update_date`          bigint      NOT NULL COMMENT '更新时间',
    `update_user_id`       bigint      NOT NULL COMMENT '更新人',
    `delete_date`          bigint      NULL COMMENT '删除时间',
    `delete_user_id`       bigint      NULL COMMENT '删除人',
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_username` (`username`) USING BTREE COMMENT '登录用户名唯一'
) COMMENT ='用户表';
```

- 以上有几个规则会决定代码生成器：
    - `密码盐:放于密码后面`
        - 英文冒号左边的 `密码盐` 会对外展示，`放于密码后面` 是用于团队说明
    - `启用状态:[1=启用=ENABLE, 2=禁用=DISABLE]max=2`
        - 英文冒号左边的 `启用状态` 会对外展示
        - `[1=启用=ENABLE, 2=禁用=DISABLE]` 会生成 StateEnum.java 类中的 name，code，description 相关
        - `max=2` 代表 API 请求校验的传入值的最大值限制


### 大型项目表前缀

- sys_（System）
- dic_（Dictionary）
- rel_（Relationship）
- biz_（Business）


### enum 属性的创建

- 所有枚举全部以 _enum 结尾，不管是不是布尔。
- boolean 类型比如 delete_enum 的 1 表示是，也就是删除，2 表示未删除。
- 其他比如 state_enum。下标也是从 1 开始，不允许从 0 开始。


### 表追加新字段

```
ALTER TABLE `my_db`.`my_table` ADD COLUMN `contract_no_` VARCHAR(32) NULL COMMENT '合同编号' AFTER `id`;
```

### 表删除字段

```
ALTER TABLE `my_db`.`my_table` DROP COLUMN charge_user_id;
```

### 修改字段长度

```
ALTER TABLE `my_db`.`my_table` MODIFY COLUMN my_create_date varchar(100);
```

### 修改字段可以为空

```
ALTER TABLE `my_db`.`my_table` MODIFY COLUMN data_value varchar(1024) null;
```


### 创建数据表索引

```
ALTER TABLE `my_db`.`my_table` ADD INDEX index_client_id (client_id); 
ALTER TABLE `my_db`.`my_table` ADD INDEX index_client_id_url (client_id,client_url); 
```

#### JDBC 连接：mysql-connector-java 8.x

- `com.mysql.cj.jdbc.Driver`

```
jdbc:mysql://127.0.0.1:3306/tkey-demo?useSSL=false&autoReconnect=true&allowMultiQueries=true&rewriteBatchedStatements=true&serverTimezone=Asia/Shanghai&useUnicode=true&characterEncoding=UTF-8&character_set_client=utf8mb4&character_set_connection=utf8mb4&character_set_database=utf8mb4&character_set_results=utf8mb4&character_set_server=utf8mb4&character_set_system=utf8&character_set_filesystem=binary&collation_connection=utf8mb4_unicode_520_ci&collation_database=utf8mb4_unicode_520_ci&collation_server=utf8mb4_unicode_520_ci
```


#### JDBC 连接：mysql-connector-java 5.x

- `com.mysql.jdbc.Driver`

```
jdbc:mysql://127.0.0.1:3306/tkey-demo?useSSL=false&autoReconnect=true&allowMultiQueries=true&rewriteBatchedStatements=true&serverTimezone=UTC&useUnicode=true&characterEncoding=UTF-8&character_set_client=utf8mb4&character_set_connection=utf8mb4&character_set_database=utf8mb4&character_set_results=utf8mb4&character_set_server=utf8mb4&character_set_system=utf8&character_set_filesystem=binary&collation_connection=utf8mb4_unicode_520_ci&collation_database=utf8mb4_unicode_520_ci&collation_server=utf8mb4_unicode_520_ci
```

 -------------------------------------------------------------------
 
### 单体系统更新可以使用 liquibase 方案
 
 - 只对开发/测试环境有效，生产环境需要 DBA 手工执行和检查
- 示例 `/db/changelog/ddb.changelog-master.sql` 文件

```
--liquibase formatted sql
--changeset youmeek:1
CREATE TABLE `sys_user` (
  `id` varchar(36) NOT NULL COMMENT '主键ID',
  `username` varchar(32) NOT NULL COMMENT '用户账号',
  PRIMARY KEY (`id`)
)COMMENT='用户表';

--changeset youmeek:2
insert  into `sys_user`(`id`,`username`,`user_password`,`email`,`delete_enum`,`create_date`,`lock_version`)
values ('374933329427959808','admin','e10adc3949ba59abbe56e057f20f883e','judas.n@qq.com','0','1514736123456',3);
insert  into `sys_user`(`id`,`username`,`user_password`,`email`,`delete_enum`,`create_date`,`lock_version`)
values ('374933329427959809','judasn','e10adc3949ba59abbe56e057f20f883e','363379444@qq.com','0','1514736123456',2);
```

- 脚本说明


```
sql 文件必须以这个开头
--liquibase formatted sql


每个版本的 SQL 前面要加上：
--changeset youmeek:1.1
加上这个注释之后，该注释下面的所有 sql 都会在启动的时候被判断，如果发现这个版本未执行就会被执行。
可以有换行，并且支持分号隔开的多个语句。

原理是 liquibase 会在我们数据库上增加一个表，专门记录执行过的版本号
```

- 依赖包

```
<!--liquibase 数据库表结构变更管理-->
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>
```


- 配置文件：

```
spring:
  liquibase:
    enabled: true
    change-log: 'classpath:/db/changelog/db.changelog-master.sql'
    # 每次都先删除后执行
    drop-first: false
```

 