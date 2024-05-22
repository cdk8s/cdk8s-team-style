# YApi 安装和配置


## 部署的环境

- 系统：`CentOS 7.4`
- 硬件要求：`1 GB RAM minimum`
- ip：`http://192.168.1.121`
- docker version：`17.12.1-ce, build 7390fc6`
- docker-compose version：`1.18.0, build 8dd22a9`

> 建议部署成 http 站点，因 chrome 浏览器安全限制，部署成 https 会导致测试功能在请求 http 站点时文件上传功能异常。--[来源](https://yapi.ymfe.org/devops.html)

## Docker 快速部署-方案1

- 推荐 <https://github.com/fjc0k/docker-YApi>

```
git clone --depth=1 https://github.com/fjc0k/docker-YApi.git

修改 docker-compose.yml
YAPI_ADMIN_ACCOUNT 为你的管理员邮箱
YAPI_ADMIN_PASSWORD 为你的管理员密码
YAPI_CLOSE_REGISTER 改为 false（不需要开放给别人注册再设置为 true）

启动服务
docker-compose up -d

给服务器开放 40001 端口
访问地址：http://106.51.106.10:40001/
```

## 数据导入、导出

```
导出：
我这里的 mongo 容器名是 yapi-mongo

备份数据到指定容器目录：
docker exec yapi-mongo mongodump -d yapi -o /my-yapi/

进入到容器中打包备份文件
docker exec -it yapi-mongo /bin/bash
cd /my-yapi
tar -cvf yapi-20240425.tar /my-yapi/yapi

退出容器，将备份文件移动到宿主机
docker cp yapi-mongo:/my-yapi/yapi-20240425.tar /opt

-------------------------------------------------------------------
导入：
docker cp /opt/yapi-20240425.tar  yapi-mongo:/data/

进入到容器中解压文件
docker exec -it yapi-mongo /bin/bash
cd /data
tar -xvf yapi-20240425.tar

退出容器终端，还原数据
docker exec yapi-mongo mongorestore -d yapi --drop --dir /data/my-yapi/yapi


```

## Windows、macOS 的 mongodb 特殊性

```
在 Windows、macOS 系统下 docker mongo 无法完成启动，会报错：Operation not permitted Actual exception type: std::system_error
需要在 docker-compose.yml 增加一个：privileged: true
并且因为它暴露端口是用 expose 参数，这种只是一种声明，不是真正的端口映射，所以如果是本地开发需要连接 mongo 需要额外增加一个 ports 参数。
两个配置都修改之后的效果如下：

  yapi-mongo:
    image: mongo:latest
    container_name: yapi-mongo
    volumes:
      - ./data/db:/data/db
    expose:
      - 27017
    ports:
      - 27017:27017
    restart: unless-stopped
    privileged: true
```


## YApi 介绍

- 官网：<https://yapi.ymfe.org/index.html>
- Github：<https://github.com/YMFE/yapi>
- 官网在线演示：<http://yapi.demo.qunar.com/>
- 使用手册：<https://yapi.ymfe.org/usage.html>
