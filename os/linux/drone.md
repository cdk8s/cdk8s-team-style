# Drone 安装和配置（适合 k8s 的 CI/CD）

112

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap

## Drone 基本介绍

- 未完成
- Drone 官网：<https://www.drone.io/>
- Drone 官网 Github：<https://github.com/drone/drone>
- Drone 官网文档：<https://docs.drone.io/>

## 安装

```
安装服务端

docker run \
  --volume=/var/lib/drone:/data \
  --env=DRONE_AGENTS_ENABLED=true \
  --env=DRONE_GOGS_SERVER=https://gogs.company.com \
  --env=DRONE_RPC_SECRET={{DRONE_RPC_SECRET}} \
  --env=DRONE_SERVER_HOST={{DRONE_SERVER_HOST}} \
  --env=DRONE_SERVER_PROTO={{DRONE_SERVER_PROTO}} \
  --publish=80:80 \
  --publish=443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:2

安装客户端

curl -L https://github.com/drone-runners/drone-runner-exec/releases/latest/download/drone_runner_exec_linux_amd64.tar.gz | tar zx
$ sudo install -t /usr/local/bin drone-runner-exec

mkdir /var/log/drone-runner-exec


vim /etc/drone-runner-exec/config

DRONE_RPC_PROTO=https
DRONE_RPC_HOST=drone.company.com
DRONE_RPC_SECRET=super-duper-secret

DRONE_LOG_FILE=/var/log/drone-runner-exec/log.txt


drone-runner-exec service install
drone-runner-exec service start


cat /var/log/drone-runner-exec/log.txt
INFO[0000] starting the server
INFO[0000] successfully pinged the remote server

```

##  官网运行示例

- 官网主页：<https://docs.drone.io/pipeline/docker/examples/>


```
https://docs.drone.io/pipeline/docker/examples/languages/java/


kind: pipeline
name: home
type: docker
steps:
  - name: build
    image: maven:3-jdk-8
    commands:
      - mvn install -Dmaven.test.skip=true
    volumes:
      - name: mvn-config
        path: /root/.m2
      - name: mvn-repo
        path: /usr/local/java/apache-maven-3.6.1/repo
  - name: docker-build-push
    image: plugins/docker
    settings:
      registry: 192.168.8.13#私服地址
      repo: 192.168.8.13/library/tomcat8
      username: #私服用户名称
      password: #私服密码
      use_cache: true
      insecure: true
      tags:
        - test
volumes:
  - name: mvn-config
    host:
      path: /usr/local/java/apache-maven-3.6.1/conf
  - name: mvn-repo
    host:
      path: /usr/local/java/apache-maven-3.6.1/repo



```

