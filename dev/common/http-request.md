
# HTTP 请求风格

## 目的

- 建立起前后端开发人员之间的沟通术语、方式以提高协作效率
- 命名规则：驼峰（Camel-Case）

-------------------------------------------------------------------

## URL 规范

- 原则：先 Mock，后联调
- 示例：<http://www.abcd.com/multiapi/API_CODE>

#### CODE_API 的组成

- CODE_API
    - 具体业务 + 类别码（1位英文字母）+ 数字编号（3位数字，项目启动会在控制台按正序打印已有编号）+ 操作码（1位英文字母）
    - 目的：方便内部团队任何层次的人交流，大家遇到问题只要说编号即可。
    - 例如：
        - `product_101p`
        - `order_102c`
- 要求
    - 复词用驼峰命名
    - 操作码
        - P 获取分页（page）
        - L 获取全体（list）
        - T 获取树（tree）
        - V 详情（view）
        - C 创建（create）
        - D 删除（delete）
        - E 更新（edit）


-------------------------------------------------------------------

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

#### 单个对象查询

- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/view>
- 请求参数：

```
{
  "id": "11111111111111111111"
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

- 特殊场景可以考虑 GET 带复杂查询：
    - get + query string 可加入浏览器收藏夹
    - get + query string 对搜索引擎更友好

-------------------------------------------------------------------

## 响应约定

### 注意

- 采用标准的 Http 状态码，但是前段判断逻辑最好还是以 `"isSuccess": true` 为判断标准
    - 如果 HTTP 状态码返回是非 200，则一定是后台发生错误，这个错误可能是系统错误，也可能是业务层面不满足条件，但是这种就是肯定错误请求，前端阻塞弹出错误即可
    - 如果 HTTP 状态码返回是 200，接下来要判断 `"isSuccess": true` 是 true 才是表示后台已经正确处理业务了，如果是 false 则后台肯定存在业务错误，需要前台阻塞弹出提示 message 中的信息
- 响应业务失败的场景是根据 code 值来区分：
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
    - 200001 未认证
    - 200011 未绑定微信账号
    - 999999 系统异常

|HTTP 状态码|Spring|含义|
|---|---|---|
|200|请求成功|`HttpStatus.OK`|
|301|永久重定向|`HttpStatus.MOVED_PERMANENTLY`|
|307|临时重定向。以前的 302 在 HttpStatus 中被 `@Deprecated`|`HttpStatus.TEMPORARY_REDIRECT`|
|400|错误的请求、请求无效|`HttpStatus.BAD_REQUEST`|
|401|未认证|`HttpStatus.UNAUTHORIZED`|
|403|被拒绝、禁止访问|`HttpStatus.FORBIDDEN`|
|404|无法找到|`HttpStatus.NOT_FOUND`|
|500|服务器内部错误|`HttpStatus.INTERNAL_SERVER_ERROR`|


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

#### 所有权限树结构

```
{
  "data":
  [
    {
      "id": "482113491504779264",
      "permissionCode": "NestleMsNavi",
      "permissionName": "导航管理",
      "uri": "",
      "type": 2,
      "status": 1,
      "rank": 100,
      "parentId": null,
      "parentIds": null,
      "remark": "",
      "extendField": null,
      "isParent": true,
      "children": [
        {
          "id": "482113491504779265",
          "permissionCode": "NestleMsNaviUrl",
          "permissionName": "链接管理",
          "uri": "/NavUrl",
          "type": 2,
          "status": 1,
          "rank": 127,
          "parentId": "482113491504779264",
          "parentIds": "482113491504779264",
          "remark": "",
          "extendField": null,
          "isParent": true,
          "children": [
            {
              "id": "482113491504779266",
              "permissionCode": "NestleMsNaviUrlAdd",
              "permissionName": "添加",
              "uri": "/NavUrl/Add",
              "type": 2,
              "status": 1,
              "rank": 127,
              "parentId": "482113491504779265",
              "parentIds": "482113491504779264,482113491504779265",
              "remark": "",
              "extendField": null,
              "isParent": false,
              "children": null
            }
          ]
        }
      ]
    },
    {
      "id": "482116699655503872",
      "permissionCode": "NestleMsUpms",
      "permissionName": "权限管理",
      "uri": null,
      "type": 2,
      "status": 1,
      "rank": 127,
      "parentId": null,
      "parentIds": null,
      "remark": "",
      "extendField": null,
      "isParent": true,
      "children": [
        {
          "id": "482116699655503873",
          "permissionCode": "NestleMsUpmsUser",
          "permissionName": "账号管理",
          "uri": "/User",
          "type": 2,
          "status": 1,
          "rank": 1,
          "parentId": "482116699655503872",
          "parentIds": "482116699655503872",
          "remark": "",
          "extendField": null,
          "isParent": true,
          "children": [
            {
              "id": "482116699655503874",
              "permissionCode": "NestleMsUpmsUserAdd",
              "permissionName": "创建账号",
              "uri": "/User/Add",
              "type": 2,
              "status": 1,
              "rank": 1,
              "parentId": "482116699655503873",
              "parentIds": "482116699655503872,482116699655503873",
              "remark": "",
              "extendField": null,
              "isParent": false,
              "children": null
            }
          ]
        },
        {
          "id": "482116699655503878",
          "permissionCode": "NestleMsUpmsRole",
          "permissionName": "角色管理",
          "uri": "/Role",
          "type": 2,
          "status": 1,
          "rank": 2,
          "parentId": "482116699655503872",
          "parentIds": "482116699655503872",
          "remark": "",
          "extendField": null,
          "isParent": true,
          "children": [
            {
              "id": "482116699655503879",
              "permissionCode": "NestleMsUpmsRoleAdd",
              "permissionName": "创建角色",
              "uri": "/Role/Add",
              "type": 2,
              "status": 1,
              "rank": 1,
              "parentId": "482116699655503878",
              "parentIds": "482116699655503872,482116699655503878",
              "remark": "",
              "extendField": null,
              "isParent": false,
              "children": null
            }
          ]
        }
      ]
    }
  ],
  "isSuccess": true,
  "msg": "查询成功",
  "timestamp": 1536768054052,
  "code": 200
}
```


#### 编辑角色，回显勾选值（用平级的方式返回给前端）


```
{
  "data": {
    "id": "522959379599785984",
    "roleName": "标准用户",
    "remark": "",
    "storeId": null,
    "isSecured": null,
    "modifyDate": 1542340646421,
    "permissions": [
      {
        "id": "482113491504779264",
        "permissionCode": "NestleMsNavi",
        "permissionName": "导航管理",
        "uri": null,
        "type": 2,
        "status": 1,
        "rank": 100,
        "parentId": null,
        "parentIds": null,
        "remark": "",
        "extendField": null,
        "isParent": true
      },
      {
        "id": "482113491504779265",
        "permissionCode": "NestleMsNaviUrl",
        "permissionName": "链接管理",
        "uri": "/NavUrl",
        "type": 2,
        "status": 1,
        "rank": 127,
        "parentId": "482113491504779264",
        "parentIds": "482113491504779264",
        "remark": "",
        "extendField": null,
        "isParent": true
      },
      {
        "id": "482116699655503882",
        "permissionCode": "NestleMsUpmsRoleObject",
        "permissionName": "查看角色",
        "uri": "/Role/Object",
        "type": 2,
        "status": 1,
        "rank": 4,
        "parentId": "482113699655503878",
        "parentIds": "482113699655503872,482113699655503878",
        "remark": "",
        "extendField": null,
        "isParent": false
      }
    ]
  },
  "isSuccess": true,
  "msg": "查询成功",
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

### 请求头内容场景

- 如果是上传文件：`Content-Type: multipart/form-data`
- 如果普通请求：`Content-Type: application/json`

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

#### 单个对象查询

- 请求方式：`POST`
- URL：<https://github.com/cdk8s/store/sysUser/view>
- 请求参数：

```
{
  "id": "11111111111111111111"
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












