
# EasyMock 安装和使用

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap

## EasyMock 基本介绍

- 官网：<https://github.com/easy-mock>

## 安装

- 官网安装说明：<https://github.com/easy-mock/easy-mock-docker>
- 设置环境

```
mkdir -p /data/docker/easymock/mongodb /data/docker/easymock/redis /data/docker/easymock/logs

chmod 777 /data/docker/easymock/logs

vim docker-compose.yml
```

- docker-compose.yml 内容

```
version: '3'

services:
  mongodb:
    image: mongo:3.4.1
    volumes:
      - '/data/docker/easymock/mongodb:/data/db'
    networks:
      - easy-mock
    restart: always

  redis:
    image: redis:4.0.6
    command: redis-server --appendonly yes
    volumes:
      - '/data/docker/easymock/redis:/data'
    networks:
      - easy-mock
    restart: always

  web:
    image: easymock/easymock:1.6.0
    command: /bin/bash -c "npm start"
    ports:
      - 7300:7300
    volumes:
      - '/data/docker/easymock/logs:/home/easy-mock/easy-mock/logs'
    networks:
      - easy-mock
    restart: always

networks:
  easy-mock:
```

- 运行：`docker-compose up -d`
- 访问地址：<http://119.23.241.211:7300>
- 直接输入用户名密码，没有会自动注册，目前没有看到有超级管理员的概念










