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
YAPI_CLOSE_REGISTER 改为 false

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
docker cp /opt/yapi-20240425.tar  容器名:/data/

进入到容器中解压文件
docker exec -it 容器名 /bin/bash
cd /data
tar -zxvf yapi-20240425.tar

还原数据
docker exec 容器名 mongorestore -d yapi --drop --dir /data/yapi

重启服务：
docker-compose up -d

```


## YApi 介绍

- 官网：<https://yapi.ymfe.org/index.html>
- Github：<https://github.com/YMFE/yapi>
- 官网在线演示：<http://yapi.demo.qunar.com/>
- 使用手册：<https://yapi.ymfe.org/usage.html>
