

# MySQL 转 PostgreSQL 经验

## 声明

- 本文思路从一开始就定位为基于云数据库来部署，不考虑生产环境自己搭建、维护、备份
- 本文只为：sculptor-boot-generator 代码生成器体系服务 [Github](https://github.com/cdk8s/sculptor-boot-generator) [Gitee](https://gitee.com/cdk8s/sculptor-boot-generator)
- 感谢群里老鐡童鞋审稿!

#### PostgreSQL 资料打包

- 关注公众号：`cd-k8s`，聊天窗口输入：`postgresql`
- 可以得到 1 套视频、9 本 PDF 资料

#### 总结

- MySQL 的用户群体性好于 PostgreSQL，特别是国内，更加容易上手。但是 PostgreSQL 从体验上最大优势就是插件以及带来的各种可能。
- 两者的基准压力测试工具不同，很难说测试数据对比是公平的，如果是通过 Java 代码测试同配置的 CURD，非极限情况下，两者使用感受上差距不大。
- PostgreSQL 在做统计分析上可以借助各种函数、语法进行支持，所以在数据分析上有优势
- 借用知乎上的一句总结 PostgreSQL 我觉得很合适：**PostgreSQL 是一专多长的全栈数据库：在可观的规模内，都能做到一招鲜吃遍天**
    - 所以，作为中小企业我觉得完全可以依赖 PostgreSQL，特别是求活阶段的企业

## 本文大纲

- PostgreSQL 官网资料介绍
- PostgreSQL 和 MySQL 语法差异点
- PostgreSQL 在阿里云的情况
- PostgreSQL 的 Docker 本地部署
- PostgreSQL 基准测试
- PostgreSQL 特有索引介绍
- PostgreSQL json 和 jsonb 类型
- PostgreSQL 执行过程分析
- PostgreSQL 中文分词、全文检索、自定义中文词库
- PostgreSQL 日常维护
- PostgreSQL 插件推荐
- PostgreSQL 衍生生态介绍

-------------------------------------------------------------------

## PostgreSQL 官网资料介绍

- 官网：<https://www.postgresql.org/>
- 官网下载：<https://www.postgresql.org/download/>
- 官网文档：<https://www.postgresql.org/docs/>
    - 中文文档 10：<http://www.postgres.cn/docs/10/>
    - 中文文档 11（未完全）：<http://www.postgres.cn/docs/11/index.html>
- 版本历史：<https://www.postgresql.org/support/versioning/>
- Why use PostgreSQL：<https://www.postgresql.org/about/>
- pgAdmin：<https://www.pgadmin.org/>


## GUI Tool

- 我不推荐官方的 pgAdmin，只是因为有更好的产品替换：Navicat Premium
- Navicat Premium 支持跨平台，支持各类关系型、非关系型数据库，支持各类云平台
- 界面体验比 DBeaver 更加友好，支持模型与 SQL 转换
- 支持各种场景的导入导出
- 官网介绍：<https://www.navicat.com.cn/products/navicat-premium>
- 但是，pgAdmin 也有一些优点，比如有 Dashboard、Statistics 可以直观查看服务器的一些统计信息。

-------------------------------------------------------------------

## PostgreSQL 和 MySQL 语法差异点

#### PostgreSQL 与 MySQL 常用共同数据类型

- 如果考虑同时兼容多个数据库，最好在设计之初就考虑差异点
- 数值类型
    - smallint
    - integer
    - bigint
    - double
    - decimal
- 字符类型
    - char(100)
    - varchar(100)
    - text
- 日期/时间类型（我个人喜欢存储时间戳，所以用 bigint）
    - timestamp
    - date
    - time
- JSON 类型（PostgreSQL 推荐使用 jsonb，因为它支持 GIN 索引）
    - json

#### PostgreSQL 与 MySQL 语法共同点

- 插入数据

```sql
INSERT INTO sys_demo(id, demo_name, demo_num, demo_type_enum, ranking, description, state_enum, delete_enum, create_date, create_user_id, update_date, update_user_id, delete_date, delete_user_id)
VALUES (111111111111111101, '演示次数01', '101', 1, 100, '演示描述01', 1, 1, 1574663780828, 111111111111111111, 1574663780828, 111111111111111111, NULL, NULL);
```

- 插入外键

```sql
alter table sys_login_log add constraint FK_ID1 foreign key (user_id) REFERENCES sys_user (id);
```

- 插入索引

```sql
CREATE INDEX rel_permission_role_index_most ON rel_permission_role (role_id, permission_id);

CREATE UNIQUE INDEX unique_username ON sys_user (username);
```


#### PostgreSQL 与 MySQL 语法异同点

- 符号上
    - PostgreSQL 不支持有 ` 号包裹表名、字段名等情况
- 命名上
    - 创建索引的时候，MySQL 只要同表中索引名称唯一即可，PostgreSQL 必须整个库唯一
- 创表：在 `sculptor-boot-generator` 项目上，有一个策略类：`GeneratorPostgreSQL.java` 在通过 MySQL 生成的时候可以直接生成 PostgreSQL 的创表语句，但是只针对我们自己的约定的字段类型
- MySQL 创表

```sql
DROP TABLE IF EXISTS sys_user;

CREATE TABLE sys_user
(
    id                   bigint      NOT NULL COMMENT '主键ID',
    username             varchar(50) NOT NULL COMMENT '用户账号:oneParam',
    real_name            varchar(50) NULL COMMENT '真实姓名',
    user_password        varchar(50) NOT NULL COMMENT '登录密码',
    password_salt        varchar(10) NOT NULL COMMENT '密码盐:放于密码后面',
    user_email           varchar(50) NULL COMMENT '邮箱地址:oneParam',
    telephone            varchar(20) NULL COMMENT '固话',
    mobile_phone         varchar(20) NULL COMMENT '手机号:oneParam',
    gender_enum          tinyint     NOT NULL DEFAULT '1' COMMENT '性别:[1=保密=PRIVACY, 2=男性=MALE, 3=女性=FEMALE, 4=中性=NEUTRAL]max=4',
    register_type_enum   tinyint     NOT NULL DEFAULT '1' COMMENT '注册方式:[1=系统预置=SYSTEM_INIT, 2=后台管理系统新增=MANAGEMENT_ADD, 3=主动注册=REGISTER, 4=被邀请注册=INVITE]max=4',
    register_origin_enum tinyint     NOT NULL DEFAULT '1' COMMENT '注册来源:[1=WEB方式=WEB, 2=安卓APP=ANDROID, 3=苹果APP=IOS, 4=H5=H5, 5=微信小程序=WECHAT_MINI_PROGRAM, 6=微信公众号=WECHAT_OFFICIAL_ACCOUNT]max=6',
    state_enum           tinyint     NOT NULL DEFAULT '1' COMMENT '启用状态:[1=启用=ENABLE, 2=禁用=DISABLE]max=2',
    delete_enum          tinyint     NOT NULL DEFAULT '1' COMMENT '删除状态:[1=未删除=NOT_DELETED, 2=已删除=DELETED]max=2',
    create_date          bigint      NOT NULL COMMENT '创建时间',
    create_user_id       bigint      NOT NULL COMMENT '创建人',
    update_date          bigint      NOT NULL COMMENT '更新时间',
    update_user_id       bigint      NOT NULL COMMENT '更新人',
    delete_date          bigint      NULL COMMENT '删除时间',
    delete_user_id       bigint      NULL COMMENT '删除人',
    PRIMARY KEY (id)
) COMMENT ='用户表';
```

- PostgreSQL 创表

```sql
DROP TABLE IF EXISTS sys_user;

CREATE TABLE sys_user
(
    id                   bigint      NOT NULL,
    username             varchar(50) NOT NULL,
    real_name            varchar(50) NULL,
    user_password        varchar(50) NOT NULL,
    password_salt        varchar(10) NOT NULL,
    user_email           varchar(50) NULL,
    telephone            varchar(20) NULL,
    mobile_phone         varchar(20) NULL,
    gender_enum          smallint    NOT NULL,
    register_type_enum   smallint    NOT NULL,
    register_origin_enum smallint    NOT NULL,
    state_enum           smallint    NOT NULL,
    delete_enum          smallint    NOT NULL,
    create_date          bigint      NOT NULL,
    create_user_id       bigint      NOT NULL,
    update_date          bigint      NOT NULL,
    update_user_id       bigint      NOT NULL,
    delete_date          bigint      NULL,
    delete_user_id       bigint      NULL,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

COMMENT ON TABLE sys_user IS '用户表';
COMMENT ON COLUMN sys_user.id IS '主键ID';
COMMENT ON COLUMN sys_user.username IS '用户账号';
COMMENT ON COLUMN sys_user.real_name IS '真实姓名';
省略其他
```

#### PostgreSQL 与 MySQL 事务差

- PostgreSQL 除了常规的 DML 的 ROLLBACK 之外，还支持 DDL 的 ROLLBACK
- 常规脚本操作，稳妥一点的流程基本是：`BEGIN > COMMIT / ROLLBACK`
- PostgreSQL 额外支持 DDL 操作，比如 CREATE TABLE，TRUNCATE 等的 ROLLBACK
- 测试：

```
select count(*) from sys_user;
假设返回有 9 条数据

BEGIN;

TRUNCATE sys_user;

select count(*) from sys_user;
返回有 0 条数据

ROLLBACK;

select count(*) from sys_user;
还是返回有 9 条数据
```

#### PostgreSQL 与 MySQL 在 Java 使用

- 没有太大区别，ORM 框架都帮你解决了（假设使用的都是共有的类型）
- PostgreSQL 配置信息

```
spring:
  datasource:
    driver-class-name: org.postgresql.Driver
    url: jdbc:postgresql://postgresql.cdk8s.com:5432/cdk8s_sculptor_boot?useSSL=false
    username: root
    password: 123456
```

- MySQL 配置信息

```
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://mysql.cdk8s.com:3306/cdk8s_sculptor_boot?useSSL=false
    username: root
    password: 123456
```



## PostgreSQL 在阿里云的情况

- 阿里云 PostgreSQL 官网：<https://www.aliyun.com/product/rds/postgresql>
- 阿里云 PostgreSQL 帮助文档：<https://help.aliyun.com/document_detail/96715.html>
- 阿里云 PostgreSQL 各版本对比：<https://help.aliyun.com/document_detail/145467.html>
- PostgreSQL进阶之路：RDS PG+HDB PG应用和案例集-云栖社区-阿里云：<https://yq.aliyun.com/topic/118>
- 查看阿里云 PostgreSQL 的版本插件支持：<https://www.alibabacloud.com/help/zh/doc-detail/142340.htm>
    - 也可以连上数据库，然后输入：`SELECT * FROM pg_available_extensions order by name`
- 2019-12 查询到的阿里云 PostgreSQL 12 支持的插件列表（目前 12 不支持高可用版本）
- 补充：因为我的工单反馈后就阿里官方补充了文档，但是还是缺部分信息，我自己购买后做了测试，这里有完整的数据

|name|default_version|comment|
|:----------|:-------------:|------|
|adminpack|2.0|administrative functions for PostgreSQL|
|amcheck|1.2|functions for verifying relation integrity|
|autoinc|1.0|functions for autoincrementing fields|
|bloom|1.0|bloom access method - signature file based index|
|btree_gin|1.3|support for indexing common datatypes in GIN|
|btree_gist|1.5|support for indexing common datatypes in GiST|
|citext|1.6|data type for case-insensitive character strings|
|cube|1.4|data type for multidimensional cubes|
|dblink|1.2|connect to other PostgreSQL databases from within a database|
|dict_int|1.0|text search dictionary template for integers|
|dict_xsyn|1.0|text search dictionary template for extended synonym processing|
|earthdistance|1.1|calculate great-circle distances on the surface of the Earth|
|file_fdw|1.0|foreign-data wrapper for flat file access|
|fuzzystrmatch|1.1|determine similarities and distance between strings|
|hstore|1.6|data type for storing sets of (key, value) pairs|
|hstore_plperl|1.0|transform between hstore and plperl|
|hstore_plperlu|1.0|transform between hstore and plperlu|
|hstore_plpython2u|1.0|transform between hstore and plpython2u|
|hstore_plpython3u|1.0|transform between hstore and plpython3u|
|hstore_plpythonu|1.0|transform between hstore and plpythonu|
|insert_username|1.0|functions for tracking who changed a table|
|intagg|1.1|integer aggregator and enumerator (obsolete)|
|intarray|1.2|functions, operators, and index support for 1-D arrays of integers|
|isn|1.2|data types for international product numbering standards|
|jsonb_plperl|1.0|transform between jsonb and plperl|
|jsonb_plperlu|1.0|transform between jsonb and plperlu|
|jsonb_plpython2u|1.0|transform between jsonb and plpython2u|
|jsonb_plpython3u|1.0|transform between jsonb and plpython3u|
|jsonb_plpythonu|1.0|transform between jsonb and plpythonu|
|lo|1.1|Large Object maintenance|
|ltree|1.1|data type for hierarchical tree-like structures|
|ltree_plpython2u|1.0|transform between ltree and plpython2u|
|ltree_plpython3u|1.0|transform between ltree and plpython3u|
|ltree_plpythonu|1.0|transform between ltree and plpythonu|
|moddatetime|1.0|functions for tracking last modification time|
|pageinspect|1.7|inspect the contents of database pages at a low level|
|pg_buffercache|1.3|examine the shared buffer cache|
|pg_freespacemap|1.2|examine the free space map (FSM)|
|pg_prewarm|1.2|prewarm relation data|
|pg_stat_statements|1.7|track execution statistics of all SQL statements executed|
|pg_trgm|1.4|text similarity measurement and index searching based on trigrams|
|pg_visibility|1.2|examine the visibility map (VM) and page-level visibility info|
|pgcrypto|1.3|cryptographic functions|
|pgrowlocks|1.2|show row-level locking information|
|pgstattuple|1.5|show tuple-level statistics|
|plperl|1.0|PL/Perl procedural language|
|plperlu|1.0|PL/PerlU untrusted procedural language|
|plpgsql|1.0|PL/pgSQL procedural language|
|plpython2u|1.0|PL/Python2U untrusted procedural language|
|plpythonu|1.0|PL/PythonU untrusted procedural language|
|pltcl|1.0|PL/Tcl procedural language|
|pltclu|1.0|PL/TclU untrusted procedural language|
|postgres_fdw|1.0|foreign-data wrapper for remote PostgreSQL servers|
|refint|1.0|functions for implementing referential integrity (obsolete)|
|seg|1.3|data type for representing line segments or floating-point intervals|
|sslinfo|1.2|information about SSL certificates|
|tablefunc|1.0|functions that manipulate whole tables, including crosstab|
|tcn|1.0|Triggered change notifications|
|tsm_system_rows|1.0|TABLESAMPLE method which accepts number of rows as a limit|
|tsm_system_time|1.0|TABLESAMPLE method which accepts time in milliseconds as a limit|
|unaccent|1.1|text search dictionary that removes accents|
|uuid-ossp|1.1|generate universally unique identifiers (UUIDs)|
|xml2|1.1|XPath querying and XSLT|

- 2019-12 查询到的阿里云 PostgreSQL 11 支持的插件列表（目前 11 支持高可用版本）

|name|default_version|comment|
|:----------|:-------------:|------|
|address_standardizer|2.5.1|Used to parse an address into constituent elements. Generally used to support geocoding address normalization step.|
|address_standardizer_data_us|2.5.1|Address Standardizer US dataset example|
|adminpack|2.0|administrative functions for PostgreSQL|
|amcheck|1.1|functions for verifying relation integrity|
|autoinc|1.0|functions for autoincrementing fields|
|bloom|1.0|bloom access method - signature file based index|
|btree_gin|1.3|support for indexing common datatypes in GIN|
|btree_gist|1.5|support for indexing common datatypes in GiST|
|citext|1.5|data type for case-insensitive character strings|
|cube|1.4|data type for multidimensional cubes|
|dblink|1.2|connect to other PostgreSQL databases from within a database|
|dict_int|1.0|text search dictionary template for integers|
|dict_xsyn|1.0|text search dictionary template for extended synonym processing|
|earthdistance|1.1|calculate great-circle distances on the surface of the Earth|
|file_fdw|1.0|foreign-data wrapper for flat file access|
|fuzzystrmatch|1.1|determine similarities and distance between strings|
|ganos_address_standardizer|2.4|Used to parse an address into constituent elements. Generally used to support geocoding address normalization step.|
|ganos_address_standardizer_data_us|2.4|Address Standardizer US dataset example|
|ganos_geometry|2.4|Ganos geometry extension for PostgreSQL|
|ganos_geometry_sfcgal|2.4|Ganos geometry SFCGAL functions extension for PostgreSQL|
|ganos_geometry_topology|2.4|Ganos geometry topology spatial types and functions extension for PostgreSQL|
|ganos_networking|2.4|Ganos networking extension for PostgreSQL|
|ganos_pointcloud|2.4|Ganos pointcloud extension For PostgreSQL|
|ganos_pointcloud_geometry|2.4|Ganos_pointcloud LIDAR data and ganos_geometry data for PostgreSQL|
|ganos_raster|2.4|Ganos raster extension for PostgreSQL|
|ganos_spatialref|2.4|Ganos spatial reference extension for PostgreSQL|
|ganos_tiger_geocoder|2.4|Ganos tiger geocoder and reverse geocoder|
|ganos_trajectory|2.4|Ganos trajectory extension for PostgreSQL|
|hstore|1.5|data type for storing sets of (key, value) pairs|
|hstore_plperl|1.0|transform between hstore and plperl|
|hstore_plperlu|1.0|transform between hstore and plperlu|
|hstore_plpython2u|1.0|transform between hstore and plpython2u|
|hstore_plpython3u|1.0|transform between hstore and plpython3u|
|hstore_plpythonu|1.0|transform between hstore and plpythonu|
|insert_username|1.0|functions for tracking who changed a table|
|intagg|1.1|integer aggregator and enumerator (obsolete)|
|intarray|1.2|functions, operators, and index support for 1-D arrays of integers|
|isn|1.2|data types for international product numbering standards|
|jsonb_plperl|1.0|transform between jsonb and plperl|
|jsonb_plperlu|1.0|transform between jsonb and plperlu|
|jsonb_plpython2u|1.0|transform between jsonb and plpython2u|
|jsonb_plpython3u|1.0|transform between jsonb and plpython3u|
|jsonb_plpythonu|1.0|transform between jsonb and plpythonu|
|lo|1.1|Large Object maintenance|
|log_fdw|1.0|foreign-data wrapper for csvlog|
|ltree|1.1|data type for hierarchical tree-like structures|
|ltree_plpython2u|1.0|transform between ltree and plpython2u|
|ltree_plpython3u|1.0|transform between ltree and plpython3u|
|ltree_plpythonu|1.0|transform between ltree and plpythonu|
|moddatetime|1.0|functions for tracking last modification time|
|ogr_fdw|1.0|foreign-data wrapper for GIS data access|
|orafce|3.8|Functions and operators that emulate a subset of functions and packages from the Oracle RDBMS|
|pageinspect|1.7|inspect the contents of database pages at a low level|
|pase|0.0.1|ant ai similarity search|
|pg_buffercache|1.3|examine the shared buffer cache|
|pg_concurrency_control|1.0|pg_concurrency_control|
|pg_cron|1.1|Job scheduler for PostgreSQL|
|pg_freespacemap|1.2|examine the free space map (FSM)|
|pg_pathman|1.5|Partitioning tool for PostgreSQL|
|pg_prewarm|1.2|prewarm relation data|
|pg_stat_statements|1.6|track execution statistics of all SQL statements executed|
|pg_trgm|1.4|text similarity measurement and index searching based on trigrams|
|pg_visibility|1.2|examine the visibility map (VM) and page-level visibility info|
|pgcrypto|1.3|cryptographic functions|
|pgrouting|2.6.2|pgRouting Extension|
|pgrowlocks|1.2|show row-level locking information|
|pgstattuple|1.5|show tuple-level statistics|
|plperl|1.0|PL/Perl procedural language|
|plperlu|1.0|PL/PerlU untrusted procedural language|
|plpgsql|1.0|1.0|PL/pgSQL procedural language|
|plpython2u|1.0|PL/Python2U untrusted procedural language|
|plpythonu|1.0|PL/PythonU untrusted procedural language|
|pltcl|1.0|PL/Tcl procedural language|
|pltclu|1.0|PL/TclU untrusted procedural language|
|postgis|2.5.1|PostGIS geometry, geography, and raster spatial types and functions|
|postgis_sfcgal|2.5.1|PostGIS SFCGAL functions|
|postgis_tiger_geocoder|2.5.1|PostGIS tiger geocoder and reverse geocoder|
|postgis_topology|2.5.1|PostGIS topology spatial types and functions|
|postgres_fdw|1.0|foreign-data wrapper for remote PostgreSQL servers|
|refint|1.0|functions for implementing referential integrity (obsolete)|
|rum|1.3|RUM index access method|
|seg|1.3|data type for representing line segments or floating-point intervals|
|sslinfo|1.2|information about SSL certificates|
|tablefunc|1.0|functions that manipulate whole tables, including crosstab|
|tcn|1.0|Triggered change notifications|
|timescaledb|1.3.0|Enables scalable inserts and complex queries for time-series data|
|timetravel|1.0|functions for implementing time travel|
|tsm_system_rows|1.0|TABLESAMPLE method which accepts number of rows as a limit|
|tsm_system_time|1.0|TABLESAMPLE method which accepts time in milliseconds as a limit|
|unaccent|1.1|text search dictionary that removes accents|
|uuid-ossp|1.1|generate universally unique identifiers (UUIDs)|
|varbitx|1.0|varbit functions pack|
|xml2|1.1|XPath querying and XSLT|
|zhparser|1.0|a parser for full-text search of Chinese|


![阿里云记录](http://img.gitnavi.com/markdown/aliyun-postgresql-1.png)

![阿里云记录](http://img.gitnavi.com/markdown/aliyun-postgresql-2.png)


## PostgreSQL 11 带 zhparser 插件的 Docker 部署（非官方）

- <https://hub.docker.com/r/davidlauhn/postgres-11-with-zhparser>
- 字典文件在容器：`/usr/share/postgresql/11/tsearch_data`
- 配置文件在容器：`/var/lib/postgresql/data/postgresql.conf`

```
mkdir -p /Users/youmeek/docker_data/pgsql11/data /Users/youmeek/docker_data/pgsql11/conf

sudo chmod -R 777 /Users/youmeek/docker_data/pgsql11

先启动一个简单容器拿配置文件：
docker run -d --name pgsql11 davidlauhn/postgres-11-with-zhparser

复制配置文件出来，后面我就不说这个目录了，改为 /etc 目录下
docker cp pgsql11:/var/lib/postgresql/data/postgresql.conf /Users/youmeek/docker_data/pgsql11/conf

停止旧容器
docker stop pgsql11 && docker rm pgsql11

再次赋权
sudo chmod -R 777 /Users/youmeek/docker_data/pgsql11

启动新容器
docker run \
	-d \
	--name pgsql11 \
	-e POSTGRES_PASSWORD=123456 \
	-v /Users/youmeek/docker_data/pgsql11/conf/postgresql.conf:/etc/postgresql/postgresql.conf \
	-v /Users/youmeek/docker_data/pgsql11/data:/var/lib/postgresql/data \
	-p 5432:5432 \
	davidlauhn/postgres-11-with-zhparser \
	-c 'config_file=/etc/postgresql/postgresql.conf'


默认库名：postgres
用户名：postgres
```

#### 连接配置

- 这个文件是专门配置登录认证信息：`/var/lib/postgresql/data/pg_hba.conf`
- 默认 ip4 下只能是 127.0.0.1 才能登陆，我这里还补上了一个：192.168.0.101，大家可以自己扩展，一行一个配置
- METHOD 列是配置密码连接加密方式，照抄即可
- 修改完记得重启服务
- 还有一个特殊的地方：
    - `/etc/postgresql/postgresql.conf` 里面有一个参数默认是：`listen_addresses = '*'`
    - 但是不排除有些版本是 localhost，那就需要改为星号，不然会连不上
    - 建议把连接改为大点：`max_connections = 1000`


```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
host    all             all             192.168.0.101/32        trust
# IPv6 local connections:
host    all             all             ::1/128                 trust
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            trust
host    replication     all             ::1/128                 trust

host all all all md5
```

## PostgreSQL 的数据库和模式说明（schema）

- 这里把 schema 翻译成模式，我记得好像是阿里云还是哪里看到的，暂且就这样叫吧。
- PostgreSQL 相对 MySQL 表特殊的地方在于其数据库下面还有一个东西叫做：`schema 模式`，默认每个库下都有一个 `public` 模式
- PostgreSQL 支持多模式，但是不推荐使用其他。因为 `public` 是默认模式，所以在写查询 SQL 的时候可以省掉这个，这样方便以后系统做数据库迁移


## 常用管理 SQL

```
查看版本
select version();

查看软件配置
select * from pg_config;

查看设置参数
select * from pg_settings;

更多目录参数：
https://www.postgresql.org/docs/11/catalogs.html
http://postgres.cn/docs/10/catalogs.html

创建用户
CREATE USER root WITH PASSWORD '123456';

创建库，并且赋权给 root
CREATE DATABASE cdk8s_sculptor_boot OWNER root;

将 newDbName 数据库的所有权限都赋予 root：
GRANT ALL PRIVILEGES ON DATABASE newDbName TO root;

导出数据：docker exec -it 容器ID pg_dump -h localhost -U postgres 数据库名 > /data/backup.sql
```

-------------------------------------------------------------------


## pgbench 基准测试

- PostgerSQL 自带基准测试工具：pgbench
- 它可以自定义脚本文件进行测试，但是我们这里不复杂说，只讲内置的脚本进行测试
- CentOS 7 独立安装：`yum install -y postgresql-contrib`
- 查看版本：`pgbench -V`

#### 初始化数据库

- 初始化测试数据：`pgbench -i -s 2 -F 100 -h 127.0.0.1 -p 5432 -U myUserName -d myDBName`
    - `-i` 是初始化的意思
    - `-s 2` 表示初始化 2 个商户的数据。默认 1 个商户是 10W 个账号（pgbench_accounts），10 个出纳（pgbench_tellers），我们这里设置 2 就要对应的生成翻倍数据
    - `-F` 创建表时数据库的填充因子，取值 10 ~ 100，值越小 UPDATE 性能会有一定提升。

```
NOTICE:  table "pgbench_branches" does not exist, skipping
NOTICE:  table "pgbench_tellers" does not exist, skipping
NOTICE:  table "pgbench_accounts" does not exist, skipping
NOTICE:  table "pgbench_history" does not exist, skipping
creating tables...
10000 tuples done.
20000 tuples done.
30000 tuples done.
40000 tuples done.
50000 tuples done.
60000 tuples done.
70000 tuples done.
80000 tuples done.
90000 tuples done.
100000 tuples done.
set primary key...
vacuum...done.
```

#### 测试命令

- 测试语句参数说明

```
-c 并发客户端数 
-j 工作线程数
-M 提交查询到服务器使用的协议：simple|extended|prepared
-n 运行测试时不执行清理
-T 60 执行总时间，单位秒
-r 输出每个SQL的平均每语句延迟
```

- 只读测试，通过 `-S` 参数控制

```
nohup pgbench -c 5 -j 5 -M prepared -n -S -T 60 -h 127.0.0.1 -p 5432 -U myUserName -d myDBName > /opt/pgbenchtest-readonly.out 2>&1 &
```

- 更新、查询、插入测试

```
nohup pgbench -c 5 -j 5 -M prepared -n -T 60 -h 127.0.0.1 -p 5432 -U myUserName -d myDBName > /opt/pgbenchtest-all.out 2>&1 &
```

- 不执行更新测试，通过 `-N` 参数控制

```
nohup pgbench -c 5 -j 5 -M prepared -n -N -T 60 -h 127.0.0.1 -p 5432 -U myUserName -d myDBName > /opt/pgbenchtest-noupdate.out 2>&1 &
```



#### 测试报告

```
pghost: 127.0.0.1 pgport: 5432 nclients: 5 duration: 10 dbName: myDBName
transaction type: TPC-B (sort of)
scaling factor: 2
query mode: prepared
number of clients: 5
number of threads: 5
duration: 60 s
number of transactions actually processed: 7237
tps = 723.210820 (including connections establishing)
tps = 723.959626 (excluding connections establishing)
```

- 参数解释：
- number of clients 是测试时指定的客户端数量
- number of threads 是测试时指定的每个客户端的线程数
- number of transactions actually processed 是测试结束时实际完成的事务数和计划完成的事务数，
- tps = 723.210820 (including connections establishing)
    - 包含建立网络连接开销的 TPS 值
- tps = 723.959626 (excluding connections establishing)
    - 不包含建立网络连接开销的 TPS 值

-------------------------------------------------------------------

## PostgreSQL 特有索引介绍

- 索引类型：B-tree，Hash，GiST，SP-GiST，GIN
- 一般普通表我们用 B-tree
- 全文检索的用 GIN，又分为两种：
    - tsvector：表示一个被优化的，可以基于搜索的文档
    - tsquery：表示一个文本查询，支持布尔操作 & | !
    - 两者搭配使用：`select * from tableName where to_tsvector('zhparser', fieldName) @@ to_tsquery('搜索内容1|其他内容2');`
    - GIN 索引支持操作符：`@>`，`?`，`?&`，`?|`

-------------------------------------------------------------------

## PostgreSQL json 和 jsonb 类型

- PostgreSQL 的 JSON 存储有两种字段类型：json、jsonb，两者的区别主要是对软件本身而言，一般是说：json 写入快，读取慢，jsonb 写入慢，读取快。因为 jsonb 是二进制存储，json 是文本存储。
- jsonb 支持 GIN 索引类型，所以实际使用过程我们推荐 jsonb
- 假设有一段 JSON：

```
{
  "id": 11111111111111,
  "username": "admin"
}
```

- 给字段创建 GIN 索引：`CREATE INDEX idx_name ON tableName USING GIN(fieldName);`
- 查询操作：

```
select * from tableName where jsonFieldName @> '{"username":"admin"}'
```

-------------------------------------------------------------------

## PostgreSQL 执行过程分析

```
explain (analyze,verbose,costs,buffers,timing)
select * from sys_user where to_tsvector('zhparser', real_name) @@ to_tsquery('李四|admin');
```

- 输出内容格式如下：

```
Seq Scan on public.sys_user  (cost=0.00..66.38 rows=1 width=692) (actual time=0.837..1.622 rows=10 loops=1)
  Output: id, username, real_name, user_password, password_salt, user_email, telephone, mobile_phone, ...省略... delete_date, delete_user_id
  Filter: (to_tsvector('zhparser'::regconfig, (sys_user.real_name)::text) @@ to_tsquery('李四|admin'::text))
  Rows Removed by Filter: 82
  Buffers: shared hit=3
Planning Time: 1.640 ms
Execution Time: 1.863 ms
```

- 上面信息有一个内容叫做：扫描节点，常见的有：
    - Seq Scan，全表顺序扫描
    - Index Scan，基于索引扫描，但不只是返回索引列的值
    - IndexOnly Scan，基于索引扫描，并且只返回索引列的值，简称为覆盖索引
    - BitmapIndex Scan，利用Bitmap 结构扫描
    - BitmapHeap Scan，把BitmapIndex Scan 返回的Bitmap 结构转换为元组结构
    - Tid Scan，用于扫描一个元组TID 数组
    - Subquery Scan，扫描一个子查询
    - Function Scan，处理含有函数的扫描
    - TableFunc Scan，处理tablefunc 相关的扫描
    - Values Scan，用于扫描Values 链表的扫描
    - Cte Scan，用于扫描WITH 字句的结果集
    - NamedTuplestore Scan，用于某些命名的结果集的扫描
    - WorkTable Scan，用于扫描Recursive Union 的中间数据
    - Foreign Scan，用于外键扫描
    - Custom Scan，用于用户自定义的扫描
- 代价估计信息：(cost=0.00..66.38 rows=1 width=692)
- 真实执行信息：(actual time=0.837..1.622 rows=10 loops=1)
    - actual time 执行时间
        - 点点符号之前是节点实际的启动时间，即找到符合该节点条件的第一个结果实际需要的时间
        - 后面是总执行时间
        - 单位都是 ms
    - rows 是实际返回的行数值，不是 MySQL 的扫描行数
    - loops 指的是该节点实际的重启次数。如果一个计划节点在运行过程中，它的相关参数值（如绑定变量）发生了变化，就需要重新运行这个计划节点。
- 除了以上 3 个核心，更多参数说明可以参看：<http://mysql.taobao.org/monthly/2018/11/06/>

-------------------------------------------------------------------

## PostgreSQL 中文分词、全文检索、自定义中文词库

- PostgreSQL 全文索引的实现要靠 gin 索引(通用倒排索引)。默认内置了英文、西班牙文等分词，但是没有中文。
- 我们需要借助插件：[zhparser](https://github.com/amutu/zhparser)
- 阿里云帮助文档：<https://help.aliyun.com/knowledge_detail/44451.html>

#### 测试分词效果

```
数据库级别（不是软件用例级别）
CREATE EXTENSION zhparser;

我把配置叫做：zhparser，后面的都是采用这个，大家也可以自己改为自己喜欢的名字
CREATE TEXT SEARCH CONFIGURATION zhparser (PARSER = zhparser);

修改一个全文检索配置的定义
映射了名词(n)，动词(v)，形容词(a)，成语(i),叹词(e)和习用语(l)6种。词典使用的是内置的simple词典，即仅做小写转换。
这篇文章介绍写得很好：https://cloud.tencent.com/developer/article/1430039
ALTER TEXT SEARCH CONFIGURATION zhparser ADD MAPPING FOR n,v,a,i,e,l WITH simple;

select ts_debug('zhparser', '白垩纪是地球上海陆分布和生物界急剧变化、火山活动频繁的时代');

SELECT * from ts_parse('zhparser', 'hello world! 2010年保障房建设在全国范围内获全面启动，从中央到地方纷纷加大 了保障房的建设和投入力度 。2011年，保障房进入了更大规模的建设阶段。住房城乡建设部党组书记、部长姜伟新去年底在全国住房城乡建设工作会议上表示，要继续推进保障性安居工程建设。');

SELECT to_tsvector('zhparser','“今年保障房新开工数量虽然有所下调，但实际的年度在建规模以及竣工规模会超以往年份，相对应的对资金的需求也会创历>史纪录。”陈国强说。在他看来，与2011年相比，2012年的保障房建设在资金配套上的压力将更为严峻。');

SELECT to_tsquery('zhparser', '保障房资金压力');
SELECT plainto_tsquery('zhparser', '保障房资金压力');
```

#### 扩展词库-方法1

- 自定义词典的优先级高于自带的词典
- 限制 zhparser 版本为 2.1 或以上

```
先查看没有扩展之前的效果：保障 房 资金 压力
SELECT * FROM ts_parse('zhparser', '保障房资金压力');
 
现在把 资金压力 插入到自定义表中
insert into zhparser.zhprs_custom_word values('资金压力');

同步数据
select sync_zhprs_custom_word();

断开当前连接，重新建立连接，再查询：资金压力 就为一个词了
SELECT * FROM ts_parse('zhparser', '保障房资金压力');


-------------------------------------------------------------------

特别说明，阿里云的 zhparser 虽然显示是 1.0 版本，但是通过工单沟通后了解到他们改造了这个插件，所以版本没用。
他们的自定义词库是这样用的：https://help.aliyun.com/knowledge_detail/44451.html
表名和函数都进行了重命名：

insert into pg_ts_custom_word values ('保障房资');

select zhprs_sync_dict_xdb();

SELECT to_tsquery('zhparser', '保障房资金压力');
```

#### 扩展词库-方法2

```
自定义词典的文件必须放在 /usr/share/postgresql/11/tsearch_data 目录中

zhparser根据文件扩展名确定词典的格式类型
.txt扩展名表示词典是文本格式
.xdb扩展名表示这个词典是xdb格式
多个文件使用逗号分隔,词典的分词优先级由低到高,
如：zhparser.extra_dicts = 'dict_extra.txt,mydict.xdb'

该参数添加到：postgresql.conf 里面
```

- dict_extra.txt 内容格式

```
; dict_extra.txt
我是新增词     2.0
再试一个       1.0       1.0    @
; 以下词为删除项
这是删除           1.0      1.0    !
```

```
测试：
SELECT * FROM ts_parse('zhparser', '我是新增词，你可以再试一个');
结果：
114	我
118	是
118	新增
110	词
117	，
114	你
118	可以
100	再
118	试
109	一个


复制词典到容器：docker cp /Users/youmeek/dict_extra.txt pgsql11:/usr/share/postgresql/11/tsearch_data

重启容器：docker restart pgsql11

重新连接测试：
SELECT * FROM ts_parse('zhparser', '我是新增词，你可以再试一个');
结果：
120	我是新增词
117	，
114	你
118	可以
120	再试一个
```


#### 独立全文检索字段

- 如果需要用到大量的全文检索，建议有额外的字段专门来存储对应字段的分词内容

```
create index idx_name on tableName using gin(to_tsvector('zhparser', fieldName));
select * from tableName where to_tsvector('zhparser', fieldName) @@ '搜索内容';
select * from tableName where to_tsvector('zhparser', fieldName) @@ '搜索内容11 & 搜索内容22';
select * from tableName where to_tsvector('zhparser', fieldName) @@ '搜索内容11 | 搜索内容22';
select * from tableName where to_tsvector('zhparser', fieldName) @@ to_tsquery('搜索内容1|其他内容2');


添加一个分词字段，gin 索引必须是 tsvector 类型
ALTER TABLE table ADD COLUMN tsv_columnName tsvector;

将字段的分词向量更新到新字段中
UPDATE table SET tsv_columnName = to_tsvector('zhparser', coalesce(fieldName,''));

在新字段上创建索引
CREATE INDEX idx_gin_zhcn ON table USING GIN(tsv_columnName);

创建一个更新分词触发器
create trigger trigger_name before insert or update 
on table for each row execute procedure tsvector_update_trigger(tsv_columnName, 'zhparser', fieldname);


```

-------------------------------------------------------------------

## PostgreSQL 日常维护

#### 开启 pg_stat_statements 模块

- 该模块可用于收集数据库中的 SQL 运行信息，例如：SQL 的总执行时间、调用次数等，常用语监控 SQL 性能

```
修改配置文件：/etc/postgresql/postgresql.conf
把原来默认值是：shared_preload_libraries = ''，改为
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.max= 5000 
pg_stat_statements.track= all 
pg_stat_statements.track_utility = on
pg_stat_statements.save = on


重启软件

用 postgres 超级用户登录：
create extension pg_stat_statements;

这时候会生成：
1 个 pg_stat_statements 视图
2 个函数：pg_stat_statements，pg_stat_statements_reset()

统计调用次数最多
select * from pg_stat_statements order by calls desc limit 10

统计平均用时最多
select * from pg_stat_statements order by mean_time desc limit 10

清空统计数据
select pg_stat_statements_reset();
```

- 核心字段，查询的时候可以根据下面字段来做排序，筛选出对应的一些 SQL 记录

```
calls：调用次数
query：执行 sql 内容
total_time：执行的总时间，单位 ms
min_time：执行的最小时间，单位 ms
max_time：执行的最大时间，单位 ms
mean_time：执行的平均时间，单位 ms
rows：影响的数据行树
shared_blks_hit：SQL 命中的共享内存数据块数量
shared_blks_read：SQL 读取的共享内存数据块数量
shared_blks_written：SQL 写入的共享内存数据块数量
shared_blks_dirtied：SQL 产生的共享内存数据脏块数量
```

- 如果是本地部署，需要通过 WEB UI 界面查看以上信息，可以借助它：pg_web_stats
- pg_web_stats：<https://github.com/kirs/pg_web_stats>

#### 日志检查

- 设置日志输出格式为 csvlog
- 每天存一份，一份最大 100M
- 修改 postgresql.conf 文件，添加如下内容（默认配置参数是没有打开注释的）
- 重启服务器，在 data 目录下可以看到一个新目录：pg_log

```
log_destination = 'csvlog'              # Valid values are combinations of
logging_collector = on                  # Enable capturing of stderr and csvlog
log_directory = 'pg_log'                # directory where log files are written,
log_filename = 'postgresql-%d_%H%M%S.log'       # log file name pattern,
log_file_mode = 0600                    # creation mode for log files,
log_truncate_on_rotation = on           # If on, an existing log file with the
log_rotation_age = 1d                   # Automatic rotation of logfiles will
log_rotation_size = 100MB               # Automatic rotation of logfiles will
```

- csv 可以用 excel 直接打开
- 如果数据很多，可以看下列头有哪些，然后创建一个表，把 csv 数据导入到表中，然后进行 sql 筛选
- log 中如果有 error code 可以在这里找到对应说明：<https://www.postgresql.org/docs/11/errcodes-appendix.html>

#### 连接数检查

- 查看当前连接数的具体信息

```
SELECT * from  pg_stat_activity;
```

#### 容量检查

- 通过如下 SQL 可以看出当前库的存储大小
- 如果定期查询，可以归纳出业务发展情况变化，是否有突发性增长，大表等等
- `pg_size_pretty` 表示用人类可读的单位显示出来

```
select datname,pg_size_pretty(pg_database_size(oid)) from pg_database;
```

- 查出所有表按大小排序并分离 data 与 index 存储大小

```
SELECT
    table_name,
    pg_size_pretty(table_size) AS table_size,
    pg_size_pretty(indexes_size) AS indexes_size,
    pg_size_pretty(total_size) AS total_size
FROM (
    SELECT
        table_name,
        pg_table_size(table_name) AS table_size,
        pg_indexes_size(table_name) AS indexes_size,
        pg_total_relation_size(table_name) AS total_size
    FROM (
        SELECT ('"' || table_schema || '"."' || table_name || '"') AS table_name
        FROM information_schema.tables
    ) AS all_tables
    ORDER BY total_size DESC
) AS pretty_sizes
where table_name like '"public"."%'
```

#### 查看提交与回滚数量

- 如果回滚次数 / 提交次数过大，就说明程序肯定哪里有问题，造成经常回滚

```
select datname,xact_commit,xact_rollback from pg_stat_database;
```

#### 定期 vacuum

- 新版本的 PostgreSQL 中有自动 vacuum 策略，但是如果是大批量的数据IO可能会导致自动执行很慢，需要配合手动执行以及自己的脚本来清理数据库
- 打开配置文件，找到自动策略开启的配置：`autovacuum = on`
- 手动执行，需要用最高权限的 postgres 用户，建议夜间业务低峰时处理

```
vacuumdb -d dbName -f -z -v
```

- 查询临界值、年龄可以参考这篇：<https://blog.csdn.net/u011598529/article/details/49276029>


-------------------------------------------------------------------

## PostgreSQL 插件推荐

#### PostGIS 插件

- 支持空间对象、空间索引、空间操作函数和空间操作符
- 常见业务场景：
    - 圈地：以当前或者指定中心点，找出周边 1 公里范围内的商家或人
    - 围栏：检测指定点落在哪个地理围栏中，比如共享单车是否停在禁停区，无人机是否在禁飞区
- 如果需要用到空间数据的话，这个插件就是最好的支持
- 目前阿里云的 PostgreSQL 11 支持，最新的 12 还没有该插件
- 推荐空间数据类型统一使用 Geometry 类型
- PostgreSQL 也内置了几个几何类型，但是跟 PostGIS 的不是同机制，推荐使用以 ST 开头的对象（ST = Spatial Type）

#### pg_pathman

- 官网：<https://github.com/postgrespro/pg_pathman>
- 看德哥文章说比内置分区性能来的好，我没试过，大家可以自己试试。阿里云的 PostgreSQL 11 已经内置该插件


#### pgRouting 插件

- 基于 PostgreSQL 和 PostGIS 提供了地理位置引路系统
- 核心功能：
    - 所有最短路径组合（Johnson 算法）
    - 所有最短路径组合（Floyd-Warshall 算法）
    - 最短 A* 路径
    - 双向 Dijkstra 最短路径
    - 双向 A* 最短路径
    - Dijkstra 最短路径
    - 行车距离
    - K-最短路径，多候选路径
    - K-Dijkstra，一对多最短路径
    - 旅行销售人员（Traveling Sales Person）
    - TRSP（Turn Restriction Shortest Path）


#### TimescaleDB 插件

- 作为时序数据
- 支持时序数据的自动分片、高效写入、检索、准实时聚合等
- 阿里云：<https://help.aliyun.com/document_detail/118899.html>


#### PASE 插件

- 向量检索，基于 IVFFlat 或 HNSW 算法
- 阿里云：<https://help.aliyun.com/document_detail/147837.html>

#### 其他插件

- 比如直接读写数据源 FDW(Foreign data wrappers)，比如 Redis、Hadoop、MySQL 等，但是我不是很喜欢这样做，所以这里不推荐
- [使用 dblink、postgres_fdw 插件进行跨库操作](https://help.aliyun.com/document_detail/142422.html)
- [使用 mysql_fdw 插件读写 MySQL 数据](https://help.aliyun.com/document_detail/143613.html)


-------------------------------------------------------------------


## PostgreSQL 衍生生态介绍

- Amazon Aurora 的 PostgreSQL 兼容版本：<https://aws.amazon.com/cn/rds/aurora/>
- 实时数据仓库、大规模并行处理、BI、AI
    - GreenPlum：<https://greenplum.org/>
    - 阿里云版本：<https://www.aliyun.com/product/gpdb>
    - Amazon Redshift：<https://aws.amazon.com/cn/redshift/>
- NewSQL（外部接口是 PostgreSQL）
    - CockroachDB：<https://github.com/cockroachdb/cockroach>
    - YugabyteDB：<https://www.yugabyte.com/yugabytedb/>
- 大规模并行处理
    - Postgres-XL：<https://www.postgres-xl.org/>
- 高可用方案
    - stolon 云原生高可用：<https://github.com/sorintlab/stolon>
    - patroni 传统高可用：<https://github.com/zalando/patroni>

-------------------------------------------------------------------

## 官网之外参考资料

- <https://www.cnblogs.com/zhenbianshu/p/7795247.html>
- <https://cloud.tencent.com/developer/article/1430039>
- <http://57km.cc/post/postgresql%20full%20index%20for%20chinese.html>
- <http://mysql.taobao.org/monthly/2018/11/06/>
- <https://blog.windrunner.me/postgres/>
- <https://www.zhihu.com/question/20010554>
- <https://blog.csdn.net/u011598529/article/details/49276029>











