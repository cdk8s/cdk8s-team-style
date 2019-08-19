
# Mock 调试


## 目的

- 建立约定式的交流语言，协助团队提效
- 命名规则：驼峰（Camel-Case）

-------------------------------------------------------------------


### Mock 阶段

- Mock.js 文档：<http://mockjs.com/examples.html>
- 时间戳转换：<https://tool.lu/timestamp/>

#### Mock Page

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
  "code": 0
}
```


#### Mock 单个对象

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
  "code": 0
}
```










