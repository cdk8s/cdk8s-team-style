# Metabase 安装和使用


#### Docker 运行

```
docker run -d -p 9393:9393 --name metabase metabase/metabase

docker logs -f metabase
```


#### 重置密码

```
如果是 docker 则 jar 文件在 /app 目录下
java -jar metabase.jar reset-password email@example.com

执行命令后会启动程序，然后在几秒后会生成一个随机密码
```
