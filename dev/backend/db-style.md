
# 数据库风格

### 限制

- 所有 Text，Blob 等大字段的数据，都必须存储到另外的独立表中，然后有业务 ID 关联业务主表


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
DROP TABLE IF EXISTS `oauth_client`;

CREATE TABLE `oauth_client`
(
    `id`             bigint       NOT NULL COMMENT '主键ID',
    `client_name`    varchar(35)  NOT NULL COMMENT '账号名称',
    `client_id`      varchar(35)  NOT NULL COMMENT '账号ID',
    `client_secret`  varchar(35)  NOT NULL COMMENT '账号密钥',
    `client_url`     varchar(200) NOT NULL DEFAULT '' COMMENT '账号匹配的网站，支持正则符号',
    `client_desc`    varchar(50)  NULL COMMENT '账号描述',
    `logo_url`       varchar(200) NULL COMMENT 'logo 的链接地址',
    `ranking`        tinyint      NOT NULL DEFAULT '100' COMMENT '排序，默认值100，值越小越靠前(rank 是关键字不允许用)',
    `remark`         varchar(255) NULL COMMENT '备注',
    `state_enum`     tinyint      NOT NULL DEFAULT '1' COMMENT '是否启动, 1正常，2禁用',
    `delete_enum`    tinyint      NOT NULL DEFAULT '1' COMMENT '是否删除, 1正常，2删除',
    `create_date`    bigint       NOT NULL COMMENT '创建时间',
    `create_user_id` bigint       NOT NULL COMMENT '创建人',
    `update_date`    bigint       NOT NULL COMMENT '更新时间',
    `update_user_id` bigint       NOT NULL COMMENT '更新人',
    `delete_date`    bigint       NULL COMMENT '删除时间',
    `delete_user_id` bigint       NULL COMMENT '删除人',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='客户端信息表';
```

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

 