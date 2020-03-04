
# API 请求风格

## 目的

- 建立起前后端开发人员之间的沟通术语、方式以提高协作效率

-------------------------------------------------------------------

## URL 规范

- 原则：先 Mock，后联调
- 示例：<http://www.abcd.com/multiapi/API_CODE>

#### API_CODE 的组成


- API_CODE
    - 类别码（1位英文字母）+ 数字编号（3位数字，建议累加，代表接口数量）+ 操作码（1位英文字母）+ 具体业务（因为单词）
    - `c101p_product`
        - `c`101p_product 是类别码，共享项目中约定 c 代表专家栏目功能
        - c`101`p_product 代表专家栏目下的第 1 个接口
        - c101`p`_product 代表 page 查询分页
        - c101p_`product` 代表操作的业务是商品业务
    - `c102c_order`
        - `c`102c_order 是类别码，共享项目中约定 c 代表专家栏目功能
        - c`102`c_order 代表专家栏目下的第 2 个接口
        - c102`c`_order 代表 create 创建数据
        - c102c_`order` 代表操作的业务是订单业务
- 要求
    - 全部小写组成
    - 复词用下划线分割
    - 操作码
        - P 获取分页（page）
        - L 获取全体（list）
        - T 获取树（tree）
        - V 详情（view）
        - C 创建（create）
        - D 删除（delete）
        - E 更新（edit）


-------------------------------------------------------------------

## 响应 JSON 规范

### 响应格式解释

- 判断接口是否响应成功：isSuccess = true 就是成功
- 响应失败的场景是根据 code 值来区分，code = 200 等同于 isSuccess = true 响应成功。但是失败有很多 code 值
    - 1 系统繁忙，请稍候重试
    - 200 成功
    - 100001 非法访问
    - 100002 参数不能为空
    - 100003 参数格式错误
    - 100004 重复请求
    - 100005 请求数据错误
    - 100006 请求数据不一致
    - 100007 数据不存在
    - 100008 数据已存在
    - 100009 数据异常
    - 100010 调用内部服务接口异常
    - 100011 调用第三方接口异常
    - 999999 系统异常

### 响应失败（"isSuccess": false）

#### 未登录

```
{
  "data": null,
  "isSuccess": false,
  "msg": "您还未登录，请先登录",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 登录失败

```
{
  "data": null,
  "isSuccess": false,
  "msg": "用户名或密码不正确",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 退出失败

```
{
  "data": null,
  "isSuccess": false,
  "msg": "退出失败",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 请求格式不正确

```
{
  "data": null,
  "isSuccess": false,
  "msg": "每页显示最小值 10，最大值 20",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 系统内部异常


```
{
  "data": null,
  "isSuccess": false,
  "msg": "服务器异常，请联系管理员",
  "timestamp": 1536768054052,
  "code": 200
}
```

-------------------------------------------------------------------

### 响应成功（"isSuccess": true）

#### 常量数据

```
{
  "data": {
    "deleteEnum": [
      {
        "label": "未删除",
        "value": "1"
      },
      {
        "label": "已删除",
        "value": "2"
      }
    ],
    "stateEnum": [
      {
        "label": "启用",
        "value": "1"
      },
      {
        "label": "禁用",
        "value": "2"
      }
    ]
  },
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```


#### 登录成功

```
{
  "data": {
    "token": "Cd534924C12561De4Eb948531A7Fdeb9"
  },
  "isSuccess": true,
  "msg": "登出成功",
  "timestamp": 1536768054052,
  "code": 200
}
```


#### 退出成功

```
{
  "data": null,
  "isSuccess": true,
  "msg": "退出成功",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 查询单个对象

```
{
  "data": {
    "id": "417454619141211111",
    "storeId": "417454619141214207",
    "roleName": "管理员1",
    "roleIntroduce": "管理员介绍1"
  },
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 查询列表

```
{
  "data": [
    {
      "id": "417454619141211111",
      "storeId": "417454619141214207",
      "roleName": "管理员1"
    },
    {
      "id": "417454619141211112",
      "storeId": "417454619141214207",
      "roleName": "管理员2"
    }
  ],
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 返回分页数据

```
{
  "data": {
    "list": [
      {
        "username": "admin",
        "email": "jun@qq.com"
      },
      {
        "username": "judasn",
        "email": "3644@qq.com"
      }
    ],
    "total": 2,
    "pageNum": 1,
    "pageSize": 10,
    "size": 2,
    "startRow": 1,
    "endRow": 2,
    "pages": 1,
    "prePage": 0,
    "nextPage": 0,
    "isFirstPage": true,
    "isLastPage": true,
    "hasPreviousPage": false,
    "hasNextPage": false,
    "navigatePages": 8,
    "navigatepageNums": [
      1
    ],
    "navigateFirstPage": 1,
    "navigateLastPage": 1,
    "firstPage": 1,
    "lastPage": 1
  },
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```


#### 添加数据成功

```
{
  "data": null,
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 修改数据成功

```
{
  "data": null,
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```

#### 删除数据成功

```
{
  "data": null,
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```


-------------------------------------------------------------------

#### Mock 资料

- Mock.js 文档：<http://mockjs.com/examples.html>
- 时间戳转换：<https://tool.lu/timestamp/>

#### Mock 返回 Page

```
{
  "data": {
    "list|2-4": [
        {
          "string": "@string(12)",
          "integer": "@integer(10, 30)",
          "float": "@float(60, 100, 2, 2)",
          "boolean": "@boolean",
          "timestamp_时间戳": "@natural(1510133532000,1564133532000)",
          "date": "@date(yyyy-MM-dd)",
          "datetime": "@datetime",
          "datetime2": "@datetime(yyyy-MM-dd HH:mm:ss)",
          "now": "@now",
          "url": "@url",
          "ip": "@ip",
          "upper": "@upper(@title)",
          "guid": "@guid",
          "id": "@id",
          "guid": "@guid",
          "image": "@image(200x200)",
          "title": "@title",
          "email": "@email",
          "region_地区": "@region",
          "province_省": "@province",
          "province_省": "@province()工商行政管理局",
          "city_市": "@city",
          "county_区": "@county",
          "cparagraph_中文段落": "@cparagraph",
          "csentence_中文句子": "@csentence",
          "ctitle_中文标题": "@ctitle(12)",
          "putReason": "提交虚假材料或者采取其_@ctitle(10)",
          "cname_中文名": "@cname",
          "range": "@range(2, 6)"
        }
    ],
    "total": 2,
    "pageNum": 1,
    "pageSize": 10,
    "size": 2,
    "startRow": 1,
    "endRow": 2,
    "pages": 1,
    "prePage": 0,
    "nextPage": 0,
    "isFirstPage": true,
    "isLastPage": true,
    "hasPreviousPage": false,
    "hasNextPage": false,
    "navigatePages": 8,
    "navigatepageNums": [
      1
    ],
    "navigateFirstPage": 1,
    "navigateLastPage": 1,
    "firstPage": 1,
    "lastPage": 1
  },
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```


#### Mock 返回单个对象

```
{
  "data": {
    "string": "@string(12)",
    "integer": "@integer(10, 30)",
    "float": "@float(60, 100, 2, 2)",
    "boolean": "@boolean",
    "timestamp_时间戳": "@natural(1510133532000,1564133532000)",
    "date": "@date(yyyy-MM-dd)",
    "datetime": "@datetime",
    "datetime2": "@datetime(yyyy-MM-dd HH:mm:ss)",
    "now": "@now",
    "url": "@url",
    "ip": "@ip",
    "upper": "@upper(@title)",
    "guid": "@guid",
    "id": "@id",
    "guid": "@guid",
    "image": "@image(200x200)",
    "title": "@title",
    "email": "@email",
    "region_地区": "@region",
    "province_省": "@province",
    "province_省": "@province()工商行政管理局",
    "city_市": "@city",
    "county_区": "@county",
    "cparagraph_中文段落": "@cparagraph",
    "csentence_中文句子": "@csentence",
    "ctitle_中文标题": "@ctitle(12)",
    "putReason": "提交虚假材料或者采取其_@ctitle(10)",
    "cname_中文名": "@cname",
    "range": "@range(2, 6)"
  },
  "isSuccess": true,
  "msg": "操作成功",
  "timestamp": 1536768054052,
  "code": 200
}
```

-------------------------------------------------------------------


## 请求 JSON 规范

### 共有请求头参数

- x-token
- app_code（app 代码）
- app_version（终端 app 版本）
- app_uhid（硬件信息）
- app_token（app token 字段）
- app_userid（用户id）

### POST 请求

#### 分页查看

- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/page>
- 请求参数：

```
{
  "pageNum": 1,
  "pageSize": 10,
  "userName": "aaaaaa"
}
```


#### 列表查看

- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/list>
- 请求参数：

```
{
  "userName": "aaaaaa",
  "gender":1
}
```


#### 单个对象新增

- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/create>
- 请求参数：

```
{
  "userName": "aaaaaa",
  "gender":1
}
```

#### 单个对象更新


- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/update>
- 请求参数：

```
{
  "id": 123456666,
  "userName": "aaaaaa",
  "gender":1
}
```

#### 批量新增对象

- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/batchCreate>
- 请求参数：

```
{
  "objectList": [
    {
      "userName": "aaaaaa",
      "gender": 1
    },
    {
      "userName": "bbbbbbb",
      "gender": 1
    }
  ]
}
```

#### 批量更新对象

- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/batchUpdate>
- 请求参数：

```
{
  "objectList": [
    {
      "id": 123456,
      "userName": "aaaaaa",
      "gender": 1
    },
    {
      "id": 123457,
      "userName": "bbbbbbb",
      "gender": 1
    }
  ]
}
```



#### 批量删除

- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/batchDelete>
- 请求参数：

```
{
  "idList": [
    123456,
    123457,
    123458
  ]
}
```


### GET 请求

- 通过 ID 查看单个对象（GET）：<https://github.com/cdk8s/store/sysUser/detail?id=123456>
- 通过 ID 删除单个对象（GET）：<https://github.com/cdk8s/store/sysUser/delete?id=123456>
- 通过 userName 查看单个对象（GET）：<https://github.com/cdk8s/store/sysUser/detailByUserName?userName=123456>
- 通过 userName 查看列表（GET）：<https://github.com/cdk8s/store/sysUser/listByUserName?userName=123456>
- 特殊场景可以考虑 GET 带复杂查询：
    - get + query string 对 cache 更友好
    - get + query string 可加入浏览器收藏夹
    - get + query string 对搜索引擎更友好























