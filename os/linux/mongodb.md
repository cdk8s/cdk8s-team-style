## MongoDB 安装和配置


## 基础概念

- MongoDB 元素概念
	- databases: 数据库;
	- collections:表；（collections组成了databases）
	- documents:行；（documents组成了collections）
- MongoDB 没有新建数据库的命令，只要进行 insert 或其它操作，MongoDB 就会自动帮你建立数据库和 collection。当查询一个不存在的 collection 时也不会出错，MongoDB 会认为那是一个空的 collection。
- 一个对象被插入到数据库中时，如果它没有 ID，会自动生成一个 "_id" 字段，为 12 字节(24位)16进制数。
- 当然如果插入文档不带 _id，则系统会帮你自动创建一个，如果自己指定了就用自己指定的。
- **核心：**
    - 使用 mongo 在插入数据的时候，每次插入的字段都可以各不相同，这对于那些表结构无法确定的业务来讲很有帮助

## 如果你用 Spring Data MongoDB 依赖请注意

- 请先看官网最新支持到哪个版本的依赖：<https://docs.spring.io/spring-data/mongodb/docs/current/reference/html/#new-features>
	- 查看锚点为：`What’s new in Spring Data MongoDB` 的内容，比如：What’s new in Spring Data MongoDB 1.10，出现这样一句话：`Compatible with MongoDB Server 3.4 and the MongoDB Java Driver 3.4`
- 目前 201712 支持 MongoDB 3.4

## 如果你用 Robomongo GUI 客户端请注意

- 请查看介绍中支持哪个版本：<https://robomongo.org/download>
- 目前 201712 支持 MongoDB 3.4

## 阿里云 MongoDB 版本支持

- 阿里云支持版本：
    - 目前（202006）主要分为下面几个主版本
    - 3.4
    - 4.0
    - 4.2
    - <https://www.aliyun.com/product/mongodb>
    - <https://help.aliyun.com/document_detail/61906.html>
- 主要架构分为：
    - 副本集：<https://help.aliyun.com/document_detail/54254.html>
    - 分片集群（基于多个副本集，费用更高，更易于扩展）：<https://help.aliyun.com/document_detail/54255.html>

-------------------------------------------------------------------

## Docker 下安装 MongoDB

- 官网 Docker 镜像：<https://hub.docker.com/_/mongo/>
    - 目前（202005）主要分为下面几个主版本
    - 3.6
    - 4.0
    - 4.2
- 先创建一个宿主机以后用来存放数据的目录：`mkdir -p /data/docker/mongo/db`
- 赋权：`chmod 777 -R /data/docker/mongo/db`
- 运行镜像 3.4（带有一个 admin 库的超级管理员。admin 库是权限数据库，专门负责超管，不能用于做业务库）：

```
docker run --name cloud-mongo \
-p 27017:27017 \
-v /data/docker/mongo/db:/data/db \
-e MONGO_INITDB_ROOT_USERNAME=mongo-admin \
-e MONGO_INITDB_ROOT_PASSWORD=123456 \
-d mongo:3.4 \
--auth
```

- 导出：`docker exec -it cloud-mongo mongoexport -h 127.0.0.1 -u 用户名 -p 密码 -d 库名 -c 集合名 -o /data/db/mongodb.json --type json`
- 导入：`docker exec -it cloud-mongo mongoimport -h 127.0.0.1 -u 用户名 -p 密码 -d 库名 -c 集合名 --file /data/db/mongodb.json --type json`
- 进入容器中 mongo shell 交互界面：`docker exec -it cloud-mongo mongo`，或者用 GUI 工具使用 mongo-admin 账号连上
- 接着创建一个普通数据库和用户：

```
use my_test_db

db.createUser(
    {
        user: "mytestuser",
        pwd: "123456",
        roles: [ 
            { role: "dbAdmin", db: "my_test_db" },
            { role: "readWrite", db: "my_test_db" }
        ]
    }
)

使用 db.auth() 可以对数据库中的用户进行验证，如果验证成功则返回 1，否则返回 0
db.auth("mytestuser","123456")
```

- 重新用 GUI 工具使用 mytestuser 账号连上就可以看到测试库了

-------------------------------------------------------------------


## 其他常用命令：

- 检查版本：`mongod --version`
- 启动：`service mongod start`
- 停止：`service mongod stop`
- 重启：`service mongod restart`
- 添加自启动：`chkconfig mongod on`
- 进入客户端：`mongo`，如果有授权用户格式为：`mongo 127.0.0.1:27017/admin -u 用户名 -p 用户密码`
- 卸载命令：`yum erase $(rpm -qa | grep mongodb-org)`
	- 删除数据库：`rm -r /var/lib/mongo`
    - 删除 log：`rm -r /var/log/mongodb`

## 添加授权用户

- 先进入 mongo 客户端 ：`mongo`
- 输入：`use admin`，然后输入：

``` bash
db.createUser(
   {
     user: "gitnavi",
     pwd: "123456",
     roles: [ { "role" : "dbAdmin", "db" : "youmeek_nav" } ]
   }
)
```

- 修改密码：`db.changeUserPassword(用户名, 密码)`
- 删除用户：` db.removeUser(用户名)`
- 内置角色：
	- read：允许用户读取指定数据库
	- readWrite：允许用户读写指定数据库
	- dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile
	- userAdmin：允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户
	- clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
	- readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限
	- readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限
	- userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
	- dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。
	- root：只在admin数据库中可用。超级账号，超级权限

## MongoDB 配置

- 编辑配置文件：`vim /etc/mongod.conf`，注意：编辑完记得重启 MongoDB 服务
- 默认的数据库目录：`/var/lib/mongo`
- 默认的日志目录：`/var/log/mongodb`
- 默认的配置文件内容：

``` ini
bindIp:127.0.0.1 #注释此行，表示除了本机也可以登陆

# 补充这个，表示必须使用带用户名密码的才能请求 mongodb，比如访问 admin 数据库：mongo 192.168.1.121:27017/admin -u 用户名 -p 用户密码
security:
  authorization: enabled
```

## 命名规范

- 数据库名：区分大小写，推荐全部小写，复词用下划线分开，eg：`my_test_db`
- 集合名：不能使用系统预留的 `system.` 做为前缀


## 常用 CURD 命令

#### 集合操作

```
插入
db.createCollection("my_collection")

删除
db.my_collection.drop()
```

#### 插入 1 条数据（如果集合不存在则自动创建）

```
db.my_collection.insert(
	{
		"book_name": "这是书名2",
		"book_price": 33.32,
		"book_author": "这是作者名2",
		"book_time": "2020-06-25 00:58:05",
		"group": {
			"price": 2682,
			"customer_num": 2
		}
	}
)

成功插入返回结果格式：WriteResult({ "nInserted" : 1, "writeConcernError" : [ ] })
```

#### 插入多条数据

- 其实 `db.my_collection.insert` 也是可以插入多条，但是还是推荐 insertMany

```
db.my_collection.insertMany(
    [
        {
            "book_name": "这是书名3",
            "book_price": 33.33,
            "book_author": "这是作者名3",
            "book_time": "2020-06-25 00:58:05",
            "group": {
                "price": 2683,
                "customer_num": 3
            }
        },
        {
            "book_name": "这是书名4",
            "book_price": 33.34,
            "book_author": "这是作者名4",
            "book_time": "2020-06-25 00:58:05",
            "group": {
                "price": 2684,
                "customer_num": 4
            }
        }
    ]
)

成功插入返回结果格式：
(Array) 2 Elements

```

-------------------------------------------------------------------

#### 更新文档（覆盖修改）

- 修改书名为 `这是书名2` 的数据为新数据结构，旧的数据结构被完整替换

```
db.my_collection.update(
    {
    "book_name": "这是书名2"
    },
    {
        "book_name": "这是书名22222",
        "book_price": 22222.2,
        "book_author": "这是作者名22222"
    }
)

成功更新后返回格式：
WriteResult({
	"nMatched" : 1,
	"nUpserted" : 0,
	"nModified" : 1,
	"writeConcernError" : [ ]
})
```


#### 更新文档（局部修改，只修改第一条）

- 默认只修改第一条匹配的数据，即使查询条件能匹配到多个数据也是修改第一条
- 使用符号：`$set:`

```
db.my_collection.update(
    {
    "book_name": "这是书名22222"
    },
    {
        $set:
        {
            "book_name": "这是书名33333",
            "book_author": "这是作者名33333"
        }
    }
)

成功更新后返回格式：
WriteResult({
	"nMatched" : 1,
	"nUpserted" : 0,
	"nModified" : 1,
	"writeConcernError" : [ ]
})
```

#### 更新文档（局部修改，修改全部匹配到数据）

- 使用符号：`multi: true`

```
db.my_collection.update(
    {
    "book_name": "这是书名22222"
    },
    {
        $set:
        {
            "book_name": "这是书名33333",
            "book_author": "这是作者名33333"
        }
    },
    {
        multi: true
    }
)
```

-------------------------------------------------------------------

#### 删除所有文档

```
db.my_collection.remove({})
```


#### 删除查询条件文档

```
db.my_collection.remove(
    {
        "book_name": "这是书名22222"
    }
)
```

-------------------------------------------------------------------

#### 查询集合所有数据

```
db.my_collection.find()
```

#### 统计总数（count）

```
db.my_collection.count()
```

#### 分页查询

- 查询统计数量

```
db.my_collection.count(
    {
        "book_name": "这是书名3"
    }
)
```

- 查询具体列表值（带排序）
    - `1` 升序
    - `-1` 降序

```
db.my_collection.find(
    {
        "book_name": "这是书名3"
    }
)
.sort(
    {
        "book_price":1
    }
)
.skip(0)
.limit(10)
```

#### 单个条件查询（根属性）

```
db.my_collection.find(
    {
        "book_name": "这是书名3"
    }
)
```

#### 单个条件查询，先只显示指定字段（投影查询）

- 1 是要显示，0 是不显示
- 指定了某几个字段是 1 后，其他则默认都是 0 表示不显示。但是 _id 默认是显示的，不想显示可以设置为 0

```
db.my_collection.find(
    {
        "book_name": "这是书名3"
    },
    {
        "book_name": 1,
        "_id": 0
    }
)
```

#### 单个条件查询（嵌套属性）

```
db.my_collection.find(
    {
        "group.customer_num": 2
    }
)
```

#### in 查询

```
db.my_collection.find(
    {
        "book_name": {
            $in: [
                "这是书名3",
                "这是书名4"
            ]
        }
    }
)
```

#### not in 查询

```
db.my_collection.find(
    {
        "book_name": {
            $nin: [
                "这是书名3",
                "这是书名4"
            ]
        }
    }
)
```

#### 多条件查询（and）

```
db.my_collection.find(
    {
        $and:[
            {
                "book_name": "这是书名3"
            },
            {
                "book_author": "这是作者名3"
            }
        ]
    }
)
```

#### 多条件查询（or）

```
db.my_collection.find(
    {
        $or:[
            {
                "book_name": "这是书名3"
            },
            {
                "book_author": "这是作者名3"
            }
        ]
    }
)
```

-------------------------------------------------------------------

#### 查看所有索引字段

```
db.my_collection.getIndexes()
```


#### 创建单个索引

- `1` 升序
- `-1` 降序

```
db.my_collection.createIndex(
    {
        "book_name": 1
    }
)

插入后返回格式：
{
    "createdCollectionAutomatically": false,
    "numIndexesBefore": NumberInt("1"),
    "numIndexesAfter": NumberInt("2"),
    "ok": 1
}


```


#### 创建复合索引

```
db.my_collection.createIndex(
    {
        "book_price": 1,
        "book_auther": 1,
    }
)
```

#### 删除索引

- 索引名称可以通过：`db.my_collection.getIndexes()` 获得，就是字段 `name` 的值

```
db.my_collection.dropIndex("索引名称")
```


-------------------------------------------------------------------

#### 执行计划使用

- 推荐 navicat 在执行按钮的最右侧有一个树一样的按钮就是专门做解析的，可以不用这个 explain 语法来，效果更佳好

```
db.my_collection.find(
    {
        $or:[
            {
                "book_name": "这是书名3"
            },
            {
                "book_author": "这是作者名3"
            }
        ]
    }
).explain()
```

-------------------------------------------------------------------

## 常用查询命令

- `show dbs`，查看已有数据库
- `use 数据库名`，进入指定数据库，如果这个数据库不存在了也是可以进入的，进入之后 insert 一条语句就会自动创建了。
- `db`，显示当前用的数据库
- `show collections`，列出当前数据库的collections(当前数据库下的表)
- `show tables`，查看数据库中的集
- `exit`，退出
- `show users`，查看当前库下的用户
- `db.system.users.find().pretty()`，查看所有用户
- `db.dropAllUsers()`，删除所有用户
- `db.dropDatebase()`，删除当前这个数据库
- `db.createCollection("my_collection")`，创建集合
- `db.集名称.find()`，查看集中的所有数据，等同于：select * from 表名称
- `db.集名称.findOne()`，查看集中的一条数据，等同于：select * from 表名称 limit 0,1
- `db.集名称.find().limit(10)`，查看集中的一条数据
- `db.集名称.find().sort({name:1})`，查询列表，根据字段name排序 #1正序 -1倒序
- `db.集名称.find().sort({x:1}).skip(5).limit(10)`，查询列表，根据字段name排序，等同于 select from foo order by x asc limit 5, 10
- `db.集名称.find({x:10})`，查询列表，等同于 select from foo where x = 10
- `db.集名称.find({x: {$lt:10}})`，select from foo where x < 10
- `db.集名称.find({}, {y:true})`，select y from foo
- `db.集名称.find({"address.city":"gz"})`，搜索嵌套文档address中city值为gz的记录
- `db.集名称.find({likes:"math"})`，搜索数组
- `db.集名称.find({name:"lichuang"})`，根据索引或字段查找数据
- `db.集名称.insert({"a":1,"b":2})`，插入一个测试数据
- `db.集名称.update({name:"张三"},{$set:{name:"李四"}})`，更新数据，等同于：UPDATE 表名 SET name='李四' WHERE name = '张三'
- `db.集名称.update({name:"张三"},{$set:{name:"李四"},{upsert:true},{multi:true}})`，更新数据，等同于：UPDATE 表名 SET name='李四' WHERE name = '张三'。其中特殊的是 upsert 为 true 的时候，表示如果没有这条数据，则创建一条。multi 表示，所有满足条件的都进行更新，不然默认只找到的第一条更新。
- `db.集名称.remove({name:"lichuang"})`，删除数据，等同于：DELETE FROM 表名 WHERE name='lichuang'
- `db.集名称.drop()`，删除这个集合
- `db.集名称.getIndexes()`，查看集合索引
- `db.集名称.dropIndex("name_1")`，删除索引
- `db.集名称.ensureIndex({title:1})`，创建索引
- `db.集名称.ensureIndex({titile:1},{name:"indexname"})`，创建索引，第二个属性设置索引名称
- `db.集名称.ensureIndex({titile:1},{unique:true/false})`，创建唯一索引，第二个属性设置为true说明该字段中值不能重复，false可以重复
- `db.集名称.ensureIndex({name:1,age:1})`，复合索引
- `db.集名称.ensureIndex({"address.city":1})`，在嵌套文档的字段上建索引
- `db.集名称.insert({"article","text"})`，全文索引，指定为text类型,每个数据集合中只允许创建一个全文索引
- `db.adminCommand( {setParameter:1, textSearchEnabled:true})`，开启全文本索引功能
- 一些符号说明：

``` ini
$gt ->greater then 大于
$lt ->less then 小于
$gte ->greater then and equal 大于等于
$lte ->less than and equal 小于等于
$ne ->not equal 不等于
```

- 其他材料：
	- <https://segmentfault.com/a/1190000007550421>
	- <https://segmentfault.com/a/1190000005095959>
	- <http://blog.csdn.net/endlu/article/details/51098518>
	- <http://www.cnblogs.com/shaosks/p/5666764.html>
	- <http://www.cookqq.com/blog/51277786-c26c-4f94-9be2-428f3633d9e5>
	- <http://www.thinksaas.cn/topics/0/513/513705.html>
	- <https://www.fedte.cc/p/511.html>

## 导入 / 导出 / 备份 /还原

- 数据的导出、导入
	- 导出：`mongoexport -h 127.0.0.1 -u 用户名 -p 密码 -d 库名 -c 集合名 -o /opt/mongodb.json --type json`
	- 导入：`mongoimport -h 127.0.0.1 -u 用户名 -p 密码 -d 库名 -c 集合名 --file /opt/mongodb.json --type json`


## Java 包

- spring-data-mongodb：<http://projects.spring.io/spring-data-mongodb/>
- mongo-java-driver：<https://github.com/mongodb/mongo-java-driver>


## GUI 管理工具

- Robomongo：<https://robomongo.org/>
- Navicat 也支持

## 基准测试

- <https://github.com/brianfrankcooper/YCSB/tree/master/mongodb#4-run-ycsb>

## 随机生成测试数据

- <https://github.com/feliixx/mgodatagen>


## 资料

- <http://www.cnblogs.com/zhoujinyi/p/4610050.html>
- <http://lvtraveler.github.io/2016/05/22/%E3%80%90MongoDB%E3%80%91MongoDB%E5%85%A5%E9%97%A8%EF%BC%88%E4%B8%80%EF%BC%89%E5%9F%BA%E6%9C%AC%E6%93%8D%E4%BD%9C-%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4/>
