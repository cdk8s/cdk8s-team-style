
# Java 命名风格

## 目的

- 建立约定式的交流语言，协助团队提效
- 命名规则：驼峰（Camel-Case）

-------------------------------------------------------------------

### 项目命名

- 以中划线分开，比如：tkey-sso

### Maven

- <groupId>com.cdk8s.tkey</groupId>
    - 组织域名 + 业务系统大范围名称
- <artifactId>tkey-sso-server</artifactId>
    - 业务系统小范围名称


### Spring Boot 启动类命名

- Application.java


### Controller 方法名

- method
    - `RequestMethod.POST`
    - `RequestMethod.GET`
- RequestMapping
    - `page`
    - `list`
    - `listByUserName`
    - `detail`
    - `detailByUserName`
    - `create`
    - `update`
    - `delete`
    - `batchCreate`
    - `batchUpdate`
    - `batchUpdate`
    
### Service 方法名

- 查询都用 `find` 开头
    - 查询所有 `findAllList`
    - 获取分页对象（传参是对象）：`findPage`
    - 获取单个对象：`findOneById`、`findOneByUserName`
    - 获取单个对象（传参是对象）：`findOneByParam`
    - 获取列表对象：`findListByUserName`、`findListByIdList`
    - 获取列表对象（传参是对象）：`findListByParam`
- 单个更新操作：`update`
- 单个删除操作：`delete`
- 单个增加操作：`create`
- 多个操作（传参是对象）：`batch开头`
- 返回值是判断用户名是否存在：`existUserLoginName`
- 返回值是检查手机号是否合规：`checkUserLoginName`
- 获得用户总数：`getUserCountNum`
- 调度更新会员等级：`jobByUpdateUserLevel`
- MQ 消息发送：`sendByUpdateProduct`
- MQ 监听消息：`listenByUpdateProduct`
- 私有方法是代表获得某个内容：`get开头`



### Mapper 方法名

- `select`
    - 查询列表：`selectByUsername` 
    - 查询列表：`selectByUsernameAndStateEnum` 
    - 查询前 3 个对象列表：`selectFirst3ByUserName` 
    - 查询单个对象：`selectFirstByUserName` 
    - 查询最大值：`selectMaxIdByUserName` 
- `update`
    - `updateUserNameById`
    - `updateUserNameByIdAndDeleteEnum`
    - `updateClientNameByIdIn`
- `count`
    - `countByUserName`
    - `countDistinctUserNameById`
- `insert`
- `delete`
- `exist`

### POJO

- 不允许以 is 开头，比如：isDelete
- dto：API 响应参数
- entity：数据库映射对象（不能有 Entity 后缀）
- param：请求参数
- bo：用于 service 层的参数 business object
- vo：响应页面参数 view object（非前后端分离场景）

### 事务注解

- 启动类加上注解

```
@EnableTransactionManagement 
```

- 在 mysql 查询的方法上加注解

```
@Transactional(readOnly = true)
public UserDTO findByUsername(String username) {

}
```

- 在 mysql 相关增删改的方法上加注解

```
@Transactional
public UserDTO updateByUsername(String username) {

}
```


### Java 注释

- [必须采用 IntelliJ IDEA / WebStorm 的代码模板功能](https://github.com/judasn/IntelliJ-IDEA-Tutorial/blob/master/file-templates-introduce.md)

```
//=====================================业务处理 start=====================================

//=====================================业务处理  end=====================================


//=====================================私有方法 start=====================================

//=====================================私有方法  end=====================================
```

### 方法注释

- 方法注释不是必须带有参数，比如：
- 需要带参数的场景是：该参数在约定字典中不存在，是不常见单词，则必须注释
- 方法有何功能也是根据是否有出现约定字典之外的不常见单词

```
/**
 * 检查 tgc 是否有效
 */
public String checkCookieTgc(String userAgent, String requestIp, String tgcCookieValue) {

}
```


### YAML

- 自定义变量的前缀必须是：`custom.variable`
- 复词用中划线：

```
custom:
  variable:
    login-interceptor-check-enable: false
```

- 自定义常用属性变量

```
custom:
  properties:
    tkey-api:
      root-url: "http://www.cdk8s.com"
      user-name: cdk8s
      shop-id: 123456
      max-file-size: 100MB
      connection-timeout: 100s
      properties-enum: ONE
      order-id-list: 11,22,33
      user-address-array: aa,bb,cc
      product-id-list: 
        - 123456
        - 1234567
        - 12345678
      string-map:
        aa: bb
        cc: dd
```

- 自定义 starer

```
custom:
  starter:
    httpclient:
      connect-time-out: 3000
```


### 参考资料

- [Google API 设计指南](https://cloud.google.com/apis/design/)

