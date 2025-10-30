
## docker 部署

mkdir -p ~/docker/activemq-5.15.6/activemq-data
mkdir -p ~/docker/activemq-5.15.6/activemq-log
vim ~/docker/activemq-5.15.6/activemq-5.15.6-docker.yml

```
version: '3.8'

services:
  activemq:
    image: rmohr/activemq:5.15.6
    container_name: my-activemq
    restart: always
    ports:
      # OpenWire 协议端口 (Java 客户端使用)
      - "61616:61616"
      
      # STOMP 协议端口 (Python stomp.py 使用) - 重要！
      - "61613:61613"
      
      # MQTT 协议端口 (物联网设备使用)
      - "1883:1883"
      
      # AMQP 协议端口 (RabbitMQ 兼容)
      - "5672:5672"
      
      # WebSocket 端口
      - "61614:61614"
      
      # Web 管理控制台端口
      - "8161:8161"
      
    volumes:
      # 持久化消息数据到宿主机
      - ./activemq-data:/opt/activemq/data
      
      # 持久化日志到宿主机
      - ./activemq-log:/opt/activemq/log
      
      # 可选：自定义配置文件（如果需要高级配置）
      # - ./activemq-conf/activemq.xml:/opt/activemq/conf/activemq.xml
      
    environment:
      # 设置管理员用户名和密码
      ACTIVEMQ_ADMIN_LOGIN: admin
      ACTIVEMQ_ADMIN_PASSWORD: admin
      
      # JVM 内存设置（根据实际情况调整）
      ACTIVEMQ_OPTS_MEMORY: "-Xms512M -Xmx2G"
      
    healthcheck:
      # 健康检查：检查 Web 管理界面是否可访问
      test: ["CMD-SHELL", "curl -f http://localhost:8161/admin/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
      
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

- 启动：`docker-compose -f ~/docker/activemq-5.15.6/activemq-5.15.6-docker.yml -p activemq-5_15_6 up -d`

## 验证

在浏览器中访问 http://localhost:8161/admin