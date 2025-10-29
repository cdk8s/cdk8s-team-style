
## docker 部署

mkdir -p ~/docker/activemq-5.15.6/activemq-data
mkdir -p ~/docker/activemq-5.15.6/activemq-log
vim ~/docker/activemq-5.15.6/activemq-5.15.6-docker.yml

```
version: '3.8'

services:
  activemq:
    image: rmohr/activemq:5.15.6
    container_name: my-activemq-compose
    restart: always
    ports:
      # JMS 端口
      - "61616:61616"
      # Web 控制台端口
      - "8161:8161"
    volumes:
      # 持久化消息数据到宿主机
      - ./activemq-data:/data/activemq
      # 持久化日志到宿主机 (可选)
      - ./activemq-log:/var/log/activemq
    environment:
      # 设置管理员用户名和密码 (推荐)
      - ACTIVEMQ_ADMIN_LOGIN=admin
      - ACTIVEMQ_ADMIN_PASSWORD=admin
```

- 启动：`docker-compose -f ~/docker/activemq-5.15.6/activemq-5.15.6-docker.yml -p activemq-5_15_6 up -d`

## 验证

在浏览器中访问 http://localhost:8161/admin