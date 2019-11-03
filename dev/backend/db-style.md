
# 数据库风格

### 理念

- 整型比字符串好（因为字符串和校对规则/排序规则使字符比整型更复杂）

### 线上更新脚本规则（必须中的必须）

- DDL（数据定义语言）和 DML（数据操纵语言）必须分开成两个文件
- DDL 是指：CREATE TABLE/VIEW/INDEX
- DML 是指：INSERT/UPDATE/DELETE DATA

### 名词说明

- 关联查询 = 连接查询
- 复合索引 = 联合索引

### 创建数据库

- 库名：最多 32 个字符

```
DROP DATABASE IF EXISTS `oauth_sso`;
CREATE DATABASE IF NOT EXISTS `oauth_sso` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;
USE `oauth_sso`;
```

### 创建数据表原则（CREATE TABLE）

- 不能用关键字和保留字，其列表：[官网说明](https://dev.mysql.com/doc/refman/5.7/en/keywords.html)
- 推荐表名前缀含义
    - sys_（System）
    - dic_（Dictionary）
    - rel_（Relationship）
    - biz_（Business）
- 表名：最多 32 个字符
- 单表最大容量预估在 1000W ~ 5000W
- 浮点数用：decimal 类型。金额类型必须是 decimal 或者 bigint（程序需要额外处理倍数问题）
- 枚举对象在表字段中的设计
    - 枚举用 tinyint 并且从 1 开始，原因：[Mybatis 中 Integer 值为 0 时，很麻烦](https://blog.csdn.net/zcl_love_wx/article/details/78799719)
    - 所有枚举全部以 `_enum` 结尾
    - 如果是代表是与否的布尔枚举场景，命名必须是：`bool_` 开头，`_enum` 结尾，不用担心命名过长。这样是为了解决 java isXXX 开头带来的 set、get 命名的问题
- 尽可能设置字段为 NOT NULL，特别是该字段要设置索引的。有默认值是空字符串都比 NULL 好，但是要考虑应用程序上的逻辑，空字符和 NULL 判断完全不一样。
- 只有 varchar(N) 才需要指定位数，其他的一律不允许出现位数，比如 `不允许出现 int(4) 这种`
- varchar(N) N 表示字符数，不是字节数。N 尽可能在 255 以内，尽可能是 10 的倍数。
- 增加冗余字段
	- 设计数据表时应尽量遵循范式理论的规约，尽可能的减少冗余字段，让数据库设计看起来精致、优雅。但是，合理的加入冗余字段可以提高查询速度。
- 增加查询结果视图表（也可以考虑存放于 Elasticsearch）
	- 对于需要经常联合查询的表，可以建立中间表以提高查询效率。
	- 通过建立中间表，将需要通过联合查询的数据插入到中间表中，然后将原来的联合查询改为对中间表的查询。
- 所有 Text，Blob 等大字段的数据，都必须存储到另外的独立表中，然后有业务 ID 关联业务主表，避免表过大
- 将字段很多的表分解成多个表
	- 对于字段较多的表，如果有些字段的使用频率很低，可以将这些字段分离出来形成新表，然后有业务 ID 关联业务主表
	- 可以避免查询缓存频繁失效（要考虑这样的设计会不会反而需要经常关联查询，这样是得不偿失）
- 设计索引
    - 一张表索引数量控制小于等于 5 个
    - 一个索引的字段控制在小于等于 5 个（复合索引）
- 复合索引遵守：最左匹配原则 == 越常用的字段越放左边
- 复合索引说明：

```
假如有三个字段的索引：(client_id,client_url,state_enum) 则最终产生如下索引搭配：
client_id 索引
client_id + client_url 索引
client_id + client_url + state_enum 索引
如果你 where 条件是：client_id and state_enum 则不会匹配到。
```

- 创表常用示例

```sql
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

- 在注释上有几个规则会决定代码生成器：
    - `密码盐:放于密码后面`
        - 英文冒号左边的 `密码盐` 会对外展示，`放于密码后面` 是用于团队解释
    - `启用状态:[1=启用=ENABLE, 2=禁用=DISABLE]max=2`
        - 英文冒号左边的 `启用状态` 会对外展示
        - `[1=启用=ENABLE, 2=禁用=DISABLE]` 会生成 StateEnum.java 类中的 name，code，description 相关
        - `max=2` 代表 API 请求校验的传入值的最大值限制

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

### 删除数据表索引

```
DROP INDEX index_client_id ON `my_db`.`my_table`;
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

-------------------------------------------------------------------

## MySQL 写 Query SQL 原则

- 考虑是否变更几率少，如果是就上缓存
- 少用 `select *`
- 少用 `子查询，多用连接(join)`，因为子查询会产生临时表，没有索引，而优化器对连接有优化。但是子查询可读性比较高，如果数据不多也可以用。
- 多用 `limit`
- 多表关联建议控制在 4 个表以内
- inner join 优于 left join
- 用 exists 替代 in，用 not exists 替代 not in
- 尽量避免在 where 子句中对字段进行 null 值判断，否则将导致引擎放弃使用索引而进行全表扫描
- group by 和 order by 事项
    - group by 和 order by 的列尽可能是一张表里的，最好设计的时候就尽可能冗余
    - group by 的时候尽可能也有 order by，如果没啥列需要排序可以 order by null
    - 多表关联下 order by 的列最好是在连接顺序的第一张表
    - group by 和 distinct 字段尽可能使用索引
    - order by 字段尽可能使用索引
- 索引事项
    - 避免在索引列上使用计算函数
    - 避免在索引列上使用 is null 和 is not null
    - 避免模糊查询百分号在左边出现：`like %abc`
    - 避免数据类型出现隐式转化（如 varchar 不加单引号的话可能会自动转换为 int 型）
    - 使用 or 要保证前、后字段都是有索引的
    - 关联查询的关联字段（on 字段）尽可能有索引
	- 复合索引：最左侧匹配原则
- 把一个复杂查询拆分成多个简单查询（**经常用**）
    - 比如三张表关联查询，可以改为先查询主表得到一个 idList，然后把这个 idList 作为 EXISTS 条件去分别查询其他两张表，然后在应用层面组装这三个 List 结果集
    - 如果有缓存，这样效率还会更加快速，还可以减少锁的竞争，


-------------------------------------------------------------------

## MySQL 写 INSERT/UPDATE/DELETE SQL 原则


- 切分执行
    - 比如一下子要删除大量表中的数据，耗时要非常久，这时候会暂满整个事务日志，阻塞很多小查询的资源。这时候可以写个程序，改为每次删除 1 万条数据，每隔 5 分钟执行一次。
- 插入数据时，影响插入速度的主要是索引、唯一性校验、一次插入的数据条数等，开发环境情况下的考虑：
	- 开发场景中，如果需要初始化数据，导入数据等一些操作，而且是开发人员进行处理的，可以考虑在插入数据之前，先禁用整张表的索引，
		- 禁用索引使用 SQL：`ALTER TABLE table_name DISABLE KEYS;`
		- 当导入完数据之后，重新让MySQL创建索引，并开启索引：`ALTER TABLE table_name ENABLE KEYS;`
	- 如果表中有字段是有唯一性约束的，可以先禁用，然后在开启：
		- 禁用唯一性检查的语句：`SET UNIQUE_CHECKS = 0;`
		- 开启唯一性检查的语句：`SET UNIQUE_CHECKS = 1;`
	- 禁用外键检查（建议还是少量用外键，而是采用代码逻辑来处理）
		- 插入数据之前执行禁止对外键的检查，数据插入完成后再恢复，可以提供插入速度。
		- 禁用：`SET foreign_key_checks = 0;`
		- 开启：`SET foreign_key_checks = 1;`
	- 使用批量插入数据
	- 禁止自动提交
		- 插入数据之前执行禁止事务的自动提交，数据插入完成后再恢复，可以提供插入速度。
		- 禁用：`SET autocommit = 0;`
		- 开启：`SET autocommit = 1;`

-------------------------------------------------------------------

## MySQL 参数使用


#### 服务状态查询

- 查看当前数据库的状态，常用的有：
	- 查看当前 MySQL 版本：`show variables like '%version%';`
	- 查看系统状态：`show status;`
	- 查看刚刚执行 SQL 是否有警告信息：`show warnings;`
	- 查看刚刚执行 SQL 是否有错误信息：`show errors;`
	- 查看当前连接数量：`show status like 'max_used_connections';`
- 查看当前 MySQL 中已经记录了多少条慢查询，前提是配置文件中开启慢查询记录了.
    - `show status like '%slow_queries%';`
- 查询当前 MySQL 中查询、更新、删除执行多少条了，可以通过这个来判断系统是侧重于读还是侧重于写，如果是写要考虑使用读写分离。
    - `show status like '%Com_select%';`
    - `show status like '%Com_update%';`
    - `show status like '%Com_delete%';`
- 显示 MySQL 服务启动运行了多少时间，如果MySQL服务重启，该时间重新计算，单位秒
    - `show status like 'uptime';`
- 其他：

```
显示线程相关变量：
show variables like '%thread%';

显示查询缓存相关
show variables like '%query_cache%';

显示查询缓存状态相关
show status like '%Qcache%';

更多参数：
show variables like '%log%';
show variables like '%log_error%';
show variables like '%slow_query_log%';
show variables like '%general_log%';
show global variables;
show session variables;
```

- show variables 优先显示会话级变量的值，如果这个值不存在，则显示全局级变量的值，当然你也可以加上 GLOBAL 或 SESSION 关键字区别;
- global 是整个 MySQL 程序层面的参数，重启 MySQL 依旧存在
- session 是会话级别，如果有修改，则在当前的连接中是有效的，重启 MySQL 后，或者断开连接后就失效。
- 查看慢日志的参数

```
show variables like '%slow_query_log%';

打开：
set global slow_query_log='ON';

关闭：
set global slow_query_log='OFF';
```


- 查看通用日志的参数

```
show variables like '%general_log%';

打开：
set global general_log='ON';

关闭：
set global general_log='OFF';
```

- 现在我们就可以监控 MySQL 看有什么 sql 语句在执行：`tail -300f /usr/local/mysql/data/youmeekdeiMac.log`
- 查看好要关闭可以设置：

```
set global general_log='OFF';
```


### 死锁故障排除


```
show engine innodb status;
```


### 并发问题排除

```
show processlist;

如果要统计，可以把结果输出到一个文件，然后再：grep State: processlist.txt | sort | uniq -c | sort -rn

结束某个请求：
kill 122; 
```

```
查看哪些请求被锁住了：
先选择：information_schema 数据库
SELECT * FROM information_schema.innodb_locks;
SELECT * FROM information_schema.innodb_lock_waits;
SELECT * FROM information_schema.innodb_trx;
```

-------------------------------------------------------------------

## EXPLAIN 分析

- 使用 EXPLAIN 进行 SQL 语句分析：`EXPLAIN SELECT * FROM sys_user;`
- 得到的结果有下面几列：
	- **id**，该列表示当前结果序号，无特殊意义，不重要
	- **select_type**，表示 SELECT 语句的类型，有下面几种
		- SIMPLE，表示简单查询，其中不包括连接查询和子查询
		- PRIMARY，表示主查询，或者是最外面的查询语句。比如你使用一个子查询语句，比如这条 SQL：`EXPLAIN SELECT * FROM (SELECT sys_user_id FROM sys_user WHERE sys_user_id = 1) AS temp_table;`
			- 这条 SQL 有两个结果，其中有一个结果的类型就是 PRIMARY
		- UNION，使用 UNION 的 SQL 是这个类型
		- DERIVED，在 SQL 中 From 后面子查询
		- SUBQUERY，子查询
		- 还有其他一些
	- **table**，表名或者是子查询的一个结果集
	- **type**，表示表的链接类型，分别有（以下的连接类型的顺序是从最佳类型到最差类型）**（这个属性重要）**：
		- 性能好：
			- system，表仅有一行，这是 const 类型的特列，平时不会出现，这个也可以忽略不计。
			- const，数据表最多只有一个匹配行，因为只匹配一行数据，所以很快，常用于 PRIMARY KEY 或者 UNIQUE 索引的查询，可理解为 const 是最优化的。
			- eq_ref，mysql 手册是这样说的:"对于每个来自于前面的表的行组合，从该表中读取一行。这可能是最好的联接类型，除了 const 类型。它用在一个索引的所有部分被联接使用并且索引是 UNIQUE(唯一键) 也不是 PRIMARY KEY(主键)"。eq_ref 可以用于使用 = 比较带索引的列。
			- ref，查询条件索引既不是 UNIQUE(唯一键) 也不是 PRIMARY KEY(主键) 的情况。ref 可用于 = 或 < 或 > 操作符的带索引的列。
			- ref_or_null，该联接类型如同 ref，但是添加了 MySQL 可以专门搜索包含 NULL 值的行。在解决子查询中经常使用该联接类型的优化。
		- 性能较差：
			- index_merge，该联接类型表示使用了索引合并优化方法。在这种情况下，key 列包含了使用的索引的清单，key_len 包含了使用的索引的最长的关键元素。
			- unique_subquery，该类型替换了下面形式的IN子查询的ref: `value IN (SELECT primary_key FROM single_table WHERE some_expr)`。unique_subquery 是一个索引查找函数,可以完全替换子查询,效率更高。
			- index_subquery，该联接类型类似于 unique_subquery。可以替换 IN 子查询, 但只适合下列形式的子查询中的非唯一索引: `value IN (SELECT key_column FROM single_table WHERE some_expr)`
			- range，只检索给定范围的行, 使用一个索引来选择行。
			- index，该联接类型与 ALL 相同, 除了只有索引树被扫描。这通常比 ALL 快, 因为索引文件通常比数据文件小。
		- 性能最差：
			- ALL，对于每个来自于先前的表的行组合, 进行完整的表扫描。（性能最差）
	- **possible_keys**，指出 MySQL 能使用哪个索引在该表中找到行。如果该列为 NULL，说明没有使用索引，可以对该列创建索引来提供性能。**（这个属性重要）**
	- **key**，显示 MySQL 实际决定使用的键 (索引)。如果没有选择索引, 键是 NULL。**（这个属性重要）**
	- **key**_len，显示 MySQL 决定使用的键长度。如果键是 NULL, 则长度为 NULL。注意：key_len 是确定了 MySQL 将实际使用的索引长度。
	- **ref**，显示使用哪个列或常数与 key 一起从表中选择行。
	- **rows**，显示 MySQL 认为它执行查询时必须检查的行数。**（这个属性重要）**
	- **Extra**，该列包含 MySQL 解决查询的详细信息：
		- **Using filesort: 没有利用索引实现排序，效率低。**
		- **Using temporary: 为了解决查询, MySQL 需要创建一个临时表来容纳结果，效率低。**
	    - NULL：使用了索引，在存储引擎层直接返回结果
		- Distinct: MySQL 发现第 1 个匹配行后, 停止为当前的行组合搜索更多的行。
		- Not exists: MySQL 能够对查询进行 LEFT JOIN 优化, 发现 1 个匹配 LEFT JOIN 标准的行后, 不再为前面的的行组合在该表内检查更多的行。
		- range checked for each record (index map: #): MySQL 没有发现好的可以使用的索引, 但发现如果来自前面的表的列值已知, 可能部分索引可以使用。
		- Using index: 从只使用索引树中的信息而不需要进一步搜索读取实际的行来检索表中的列信息。
		- Using where: WHERE 子句用于限制哪一个行匹配下一个表或发送到客户。

-------------------------------------------------------------------


## 系统内置库

#### information_schema 库

- information_schema 提供了访问数据库元数据的方式。
- 它保存了 mysql 服务器所有数据库的信息。比如数据库的库名、数据库的表、数据库表的数据类型，索引，外键、存储过程、视图，函数，事件，触发器等结构信息。
    - character_sets：存储数据库相关字符集信息（memory存储引擎）
    - collations：字符集对应的排序规则
    - collation_character_set_applicability：字符集和连线校对的对应关系
    - schema_privileges：提供了数据库的相关权限
    - table_privileges: 提供的是表权限相关信息
    - column_privileges ：表授权的用户的权限
    - user_privileges:提供的是用户表权限相关信息
    - **columns：存储所有表的所有字段信息**
    - innodb_sys_columns ：innodb的元数据
    - engines ：引擎类型，是否支持这个引擎，描述，是否支持事物，是否支持分布式事务，是否能够支持事物的回滚点
    - events ：记录mysql中的事件，类似于定时作业
    - files ：这张表提供了有关在mysql的表空间中的数据存储的文件的信息，文件存储的位置
    - parameters ：参数表存储了一些存储过程和方法的参数，以及存储过程的返回值信息
    - plugins ：mysql的插件信息，是否是活动状态等信息
    - routines：关于存储过程和方法function的一些信息
    - schemata：这个表提供了实例下有多少个数据库，而且还有数据库默认的字符集
    - triggers :触发器的信息
    - views :视图的信息
    - referential_constraints：这个表提供的外键相关的信息
    - table_constraints ：这个表提供的是 相关的约束信息
    - innodb_sys_foreign_cols ：innodb关于外键的元数据信息
    - key_column_usage ：数据库中所有有约束的列
    - global_status：系统状态
    - global_variables：系统变量
    - session_status：session状态
    - session_variables：session变量
    - partitions ：mysql分区表相关的信息
    - processlist：当前线程列表
    - innodb_cmp_per_index，innodb_cmp_per_index_reset：关于压缩innodb信息表的时候的相关信息
    - innodb_cmpmem ，innodb_cmpmem_reset：innodb的压缩页的buffer pool信息
    - innodb_buffer_pool_stats ：表提供有关innodb 的buffer pool相关信息
    - innodb_buffer_page_lru，innodb_buffer_page :维护了innodb lru list的相关信息
    - innodb_buffer_page ：buffer里面缓冲的页数据
    - innodb_sys_datafiles ：这张表就是记录的表的文件存储的位置和表空间的一个对应关系
    - innodb_temp_table_info ：所有的innodb的所有用户使用到的信息
    - innodb_metrics ：提供innodb的各种的性能指数
    - innodb_sys_virtual :表存储的是innodb表的虚拟列的信息
    - innodb_cmp，innodb_cmp_reset：存储的是关于压缩innodb信息表的时候的相关信息
    - **tables：数据库中表的信息**
    - tablespaces：活跃表空间
    - innodb_sys_tables：表格的格式和存储特性，包括行格式，压缩页面大小位级别的信息
    - **statistics：关于表的索引信息**
    - **innodb_sys_indexes：innodb表的索引的相关信息**
    - **innodb_sys_tablestats：mysql数据库的统计信息**
    - innodb_sys_fields ：innodb的表索引字段信息，以及字段的排名
    - innodb_ft_config :这张表存的是全文索引的信息
    - innodb_ft_default_stopword：stopword 的信息
    - innodb_ft_index_cache ：这张表存放的是插入前的记录信息，也是为了避免dml时候昂贵的索引重组
    - optimizer_trace ：提供的是优化跟踪功能产生的信息
    - profiling：服务器执行语句的工作情况
    - innodb_ft_being_deleted：nnodb_ft_deleted的一个快照
    - **innodb_locks: innodb现在获取的锁**
    - **innodb_lock_waits：系统锁等待相关信息，包含了阻塞的一行或者多行的记录，而且还有锁请求和被阻塞改请求的锁信息等**
    - **innodb_trx：包含了所有正在执行的的事物相关信息，而且包含了事物是否被阻塞或者请求锁**


#### performance_schema 库

- performance_schema 用于监视 MySQL 服务器，收集数据库服务器性能参数，它是内存表，不使用磁盘存储，在 datadir 的 performance_schema 目录下，只有.frm 表结构文件，没有数据文件。
- 表内容在服务器启动时重新填充，并在服务器关闭时丢弃。
- 可用于监控服务器在一个较低级别的运行过程中的资源消耗、资源等待等情况。
    - setup_actors：配置用户纬度的监控，默认监控所有用户
    - setup_consumers：配置events的消费者类型，即收集的events写入到哪些统计表中
    - setup_instruments：配置具体的instrument
    - setup_objects：配置监控对象，默认对mysql、performance_schema和information_schema中的表都不监控，而其它所有表都监控。
    - setup_timers：配置每种类型指令的统计时间单位
    - cond_instances：系统中使用的条件变量的对象
    - file_instances：系统中打开了文件的对象，包括ibdata文件，redo文件，binlog文件，用户的表文件等
    - **mutex_instances：系统中使用互斥量对象的所有记录**
    - **rwlock_instances： 系统中使用读写锁对象的所有记录**
    - socket_instances：活跃会话对象实例
    - **events_waits_current：记录了当前线程等待的事件**
    - **events_waits_history：记录了每个线程最近等待的10个事件**
    - events_waits_history_long：记录了最近所有线程产生的10000个事件
    - **events_stages_current：记录了当前线程所处的执行阶段**
    - **events_stages_history：记录了当前线程所处的执行阶段10条历史记录**
    - events_stages_history_long：记录了当前线程所处的执行阶段10000条历史记录
    - events_statements_current：最顶层的请求，SQL语句或是COMMAND
    - users：记录用户连接数信息
    - hosts：记录了主机连接数信息
    - accounts：记录了用户主机连接数信息
    - events_waits_summary_global_by_event_name：按等待事件类型聚合
    - events_waits_summary_by_instance：按等待事件对象聚合
    - events_waits_summary_by_thread_by_event_name：按每个线程和事件来统计
    - events_stages_summary_global_by_event_name：按事件阶段类型聚合
    - events_stages_summary_by_thread_by_event_name：按每个线程和事件来阶段统计
    - events_statements_summary_by_digest：按照事件的语句进行聚合
    - events_statements_summary_global_by_event_name：按照事件的语句进行聚合
    - events_statements_summary_by_thread_by_event_name：按照线程和事件的语句进行聚合
    - file_summary_by_instance：按事件类型统计（物理IO维度）
    - file_summary_by_event_name：具体文件统计（物理IO维度）
    - table_io_waits_summary_by_table：根据wait/io/table/sql/handler，聚合每个表的I/O操作（逻辑IO纬度）
    - **table_io_waits_summary_by_index_usage：按索引维度统计**
    - **table_lock_waits_summary_by_table：聚合了表锁等待事件**
    - socket_summary_by_instance：socket聚合统计表
    - performance_timers：系统支持的统计时间单位
    - threads：监视服务端的当前运行的线程

#### 其他两个内置库

sys：库中所有的数据源来自performance_schema，目标是降低performance_schema的复杂度。
mysql：mysql的核心数据库，主要负责存储数据库的用户、权限设置、关键字等mysql自身需要使用的控制和管理信息。


-------------------------------------------------------------------

## MySQL 常用类型说明


#### 整数类型

- TINYINT，SMALLINT，MEDIUMINT，INT，BIGINT
- 存储空间分别是：8，16，24，32，64 位存储空间
- 存储的值范围分别是：-2的n-1次方 ~ 2的n-1次方再减去1。n 是存储空间的位数值
- UNSIGNED 表示不允许负值，大致可以使正数的上限提高一倍。比如TINYINT存储范围是-128 ~ 127，而UNSIGNED TINYINT存储的范围却是0 – 255

```
int(10) 与 int(11) 后的括号中的字符表示显示宽度（display size），推荐不写显示宽度
整数列的显示宽度与 mysql 需要用多少个字符来显示该列数值，与该整数需要的存储空间的大小都没有关系
int 类型的字段能存储的数据上限还是 2147483647(有符号型) 和 4294967295(无符号型)
所以括号数字对该字段所表示的取值范围并没影响，这个补位的数字只有当你设置该字段为 zerofill 的时候才会体现差别
```

#### 实数类型(小数类型)

- 推荐 DECIMAL，但是开销相对较大
- 还有一种方法开销比较小，用 BIGINT。比如：3.25，那存在数据库就是：3.25 X 100 = 325，取出的时候再除去 100 得到 3.25。


#### 字符串类型

- CHAR(5) 不可变长度字符串类型，如果确定了该列的数据格式都是固定一个位数，可以使用，性能更高。
- VARCHAR(5) 可变长度字符串类型，存储常规字符串，一般建议最大字符数控制在：21844 以内。
- BLOB 存储二进制，二进制一般我们都会直接落盘，很少会直接存储在 MySQL
- TEXT 存储大文本字符串，一般我们常见的都是存储纯文本内容
- BLOB 没有排序规则或字符集而 TEXT 有


#### 时间类型

- TIMESTAMP 根据时区展示，比如 mysql 连接的时候带有时区参数，则查询出来的结果都是以该时区表示，4 字节存储空间，范围：1970 年 ~ 2038 年，精确到秒，默认是 NOT NULL，性能较高
- DATETIME 与时区无关，8 字节存储空间，范围：1001 年 ~ 9999 年，精确到秒
- 如果需要到毫秒，可以使用 BIGINT 存储时间戳


#### 不要使用的类型

- ENUM，SET，BIT

