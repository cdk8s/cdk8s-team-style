
# 前端开发风格

## 前提

- 以 [WebStorm](https://www.jetbrains.com/webstorm) 为标准开发 IDE，不允许使用其他
- ESLint 规范

```
{
  "extends": [
    "eslint-config-umi",
    "eslint-config-react-app",
    "eslint-config-prettier"
  ]
}
```

-------------------------------------------------------------------

## 项目命名

- 必须是以中划线分割：heh-admin

## HTML 细节

```
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>这是标题</title>
    <meta name="description" content="不超过150个字符">
    <meta name="keywords" content="代码,文档,图片,视频">

    <!-- 为移动设备添加 viewport -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="shortcut icon" href="/favicon.ico">
</head>
</html>
```

- 引入资源尽可能放在 CDN，不要指定资源所带的具体协议 ( http:,https: ) 

```
<script src="//cdn.com/jquery.min.js"></script>
```

- 需要图片占位的一律使用：<http://temp.im/>

-------------------------------------------------------------------

## 后台管理

### React 篇

#### 以 ant-design-pro 为标准

- 官网：<https://github.com/ant-design/ant-design-pro/>
- 组件和页面的文件夹 + 文件：必须是大写开头，其他都已小写开头

#### 命名

- canXXXXX：判断是否可执行某个动作
- hasXXXXX：判断是否含有某个值
- isXXXXX：判断是否为某个值
- getXXXXX：获取某个值
- setXXXXX：设置某个值
- onXXXX: 触发事件函数


-------------------------------------------------------------------


## 前端提交代码之前要做的

- 做修改后代码的 Compare 检查，看是否有哪里不小心多敲了一些字符
- 用 WebStorm 右键 src 做：`Inspect Code`
- 用 WebStorm 的 Typescript 窗口的 `Compile All`
- 勾选 `Check TODO`
- 勾选 `Run Git Hooks`
    - 相关 git hooks 位于每个 git 项目下的隐藏文件夹 .git/hooks 文件夹里


-------------------------------------------------------------------

## Ajax 请求规范

- [前后端请求与响应规范.md]()

-------------------------------------------------------------------

## 参考资料

- Airbnb JavaScript 代码规范
- <https://juejin.im/entry/5b2211afe51d4558ba1a4e52>
- <https://www.w3cschool.cn/webdevelopment/uqokbozt.html>
- <https://guide.aotu.io/docs/>
- <http://www.edllogistics.com/Upload/File/2017-04-07/1437290728/%E4%BC%BD%E7%84%B6%E5%89%8D%E7%AB%AF%E6%8A%80%E6%9C%AF%E8%A7%84%E8%8C%83.pdf>
- <https://www.yuque.com/ucf-web/book/rdewg0>