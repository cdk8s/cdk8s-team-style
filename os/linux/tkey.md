
# TKey 环境

- CentOS 7.5 x64

## 修改 SSH 端口

- 配置文件介绍（记得先备份）：`sudo vim /etc/ssh/sshd_config`
- 打开这一行注释：Port 22
	- 自定义端口选择建议在万位的端口，如：10000-65535之间，假设这里我改为 52221
- CentOS 7：添加端口：`firewall-cmd --zone=public --add-port=52221/tcp --permanent`
	- 重启防火墙：`firewall-cmd --reload`
- CentOS 7 命令：`systemctl restart sshd.service`


## 安装 ansible

- CentOS：`sudo yum install -y ansible`
	- 查看版本：`ansible --version`
- 编辑配置文件：`vim /etc/ansible/hosts`，在文件尾部添加：

```
[local]
172.16.16.4 ansible_ssh_port=52221
```

- 让远程所有主机都执行 `ps` 命令，输出如下

```
ansible all -a 'ps'
```



## 基础设置

- 禁用
    - firewalld
    - selinux
    - swap
- 安装
    - zip unzip lrzsz git wget htop deltarpm 
    - zsh vim
    - docker docker-compose

- 创建脚本文件：`vim /opt/install-basic-playbook.yml`

```
- hosts: all
  remote_user: root
  tasks:
    - name: Disable SELinux at next reboot
      selinux:
        state: disabled
        
    - name: disable firewalld
      command: "{{ item }}"
      with_items:
         - systemctl stop firewalld
         - systemctl disable firewalld
         - echo "vm.swappiness = 0" >> /etc/sysctl.conf
         - swapoff -a
         - sysctl -w vm.swappiness=0
         
    - name: install-epel
      command: "{{ item }}"
      with_items:
         - yum install -y epel-release
         
    - name: install-basic
      command: "{{ item }}"
      with_items:
         - yum install -y zip unzip lrzsz git wget htop deltarpm
         
    - name: install-zsh
      shell: "{{ item }}"
      with_items:
         - yum install -y zsh
         - wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O - | sh
         - chsh -s /bin/zsh root
         
    - name: install-vim
      shell: "{{ item }}"
      with_items:
         - yum install -y vim
         - curl https://raw.githubusercontent.com/wklken/vim-for-server/master/vimrc > ~/.vimrc
         
    - name: install-docker
      shell: "{{ item }}"
      with_items:
         - yum install -y yum-utils device-mapper-persistent-data lvm2
         - yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
         - yum makecache fast
         - yum install -y docker-ce docker-ce-cli containerd.io
         - systemctl start docker.service
         - docker run hello-world
         
    - name: install-docker-compose
      shell: "{{ item }}"
      with_items:
         - curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-Linux-x86_64" -o /usr/local/bin/docker-compose
         - chmod +x /usr/local/bin/docker-compose
         - docker-compose --version
         - systemctl restart docker.service
         - systemctl enable docker.service
```

- 执行：`ansible-playbook /opt/install-basic-playbook.yml`


## 离线安装 jdk

- 下载 jdk 到 /opt 目录下
- 创建脚本文件：`vim /opt/jdk8-playbook.yml`

```
- hosts: all
  remote_user: root
  vars:
    java_install_folder: /usr/local
    file_name: jdk-8u212-linux-x64.tar.gz
  tasks:
    - name: copy jdk
      copy: src=/opt/{{ file_name }} dest={{ java_install_folder }}
      
    - name: tar jdk
      shell: chdir={{ java_install_folder }} tar zxf {{ file_name }}
      
    - name: set JAVA_HOME
      blockinfile: 
        path: /root/.zshrc
        marker: "#{mark} JDK ENV"
        block: |
          JAVA_HOME={{ java_install_folder }}/jdk1.8.0_212
          JRE_HOME=$JAVA_HOME/jre
          PATH=$PATH:$JAVA_HOME/bin
          CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
          export JAVA_HOME
          export JRE_HOME
          export PATH
          export CLASSPATH
    
    - name: source zshrc
      shell: source /root/.zshrc
         
    - name: Clean file
      file:
        state: absent
        path: "{{ java_install_folder }}/{{ file_name }}" 
```


- 执行命令：`ansible-playbook /opt/jdk8-playbook.yml`



## 安装 maven


- 下载 maven 到 /opt 目录下：`wget http://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.zip`
- 创建脚本文件：`vim /opt/maven-playbook.yml`

```
- hosts: all
  remote_user: root
  vars:
    maven_install_folder: /usr/local
    file_name: apache-maven-3.6.1-bin.zip
  tasks:
    - name: copy maven
      copy: src=/opt/{{ file_name }} dest={{ maven_install_folder }}
      
    - name: unzip maven
      shell: chdir={{ maven_install_folder }} unzip {{ file_name }}
      
    - name: set MAVEN_HOME
      blockinfile: 
        path: /root/.zshrc
        marker: "#{mark} MAVEN ENV"
        block: |
            MAVEN_HOME=/usr/local/apache-maven-3.6.1
            M3_HOME=/usr/local/apache-maven-3.6.1
            PATH=$PATH:$M3_HOME/bin
            MAVEN_OPTS="-Xms256m -Xmx356m"
            export M3_HOME
            export MAVEN_HOME
            export PATH
            export MAVEN_OPTS
    
    - name: source zshrc
      shell: source /root/.zshrc
         
    - name: Clean file
      file:
        state: absent
        path: "{{ maven_install_folder }}/{{ file_name }}" 
```


- 执行命令：`ansible-playbook /opt/maven-playbook.yml`


## 安装 node

- 创建脚本文件：`vim /opt/node-playbook.yml`

```
- hosts: all
  remote_user: root
  tasks:
    - name: uninstall-node
      shell: yum remove -y nodejs npm

    - name: curl
      shell: "curl --silent --location https://rpm.nodesource.com/setup_10.x | sudo bash -"
      
    - name: install-node
      command: "{{ item }}"
      with_items:
         - yum -y install nodejs
```


- 执行命令：`ansible-playbook /opt/node-playbook.yml`

## 安装 Jenkins

- 创建脚本文件：`vim /opt/jenkins-playbook.yml`

```
- hosts: all
  remote_user: root
  tasks:
    - name: wget
      shell: wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo

    - name: rpm import
      shell: rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key

    - name: install
      shell: yum install -y jenkins
```

- 执行命令：`ansible-playbook /opt/jenkins-playbook.yml`
- 在安装完默认推荐的插件后还需要额外安装：
    - `Maven Integration`

-------------------------------------------------------------------

## 安装 Redis 5.x（Docker）

```
mkdir -p /data/docker/redis/conf /data/docker/redis/db
chmod -R 777 /data/docker/redis
```

```
创建配置文件：
vim /data/docker/redis/conf/redis.conf



bind 0.0.0.0
requirepass 123456
protected-mode yes

port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
supervised no
pidfile /data/redis_6379.pid
loglevel notice
logfile ""
databases 16
always-show-logo yes
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-disable-tcp-nodelay no
replica-priority 100
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
appendonly no
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
stream-node-max-bytes 4096
stream-node-max-entries 100
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
dynamic-hz yes
aof-rewrite-incremental-fsync yes
rdb-save-incremental-fsync yes
```

- 启动镜像：

```
docker run \
    --name cdk8s-redis \
    --restart always \
    -d -it -p 6379:6379 \
    -v /data/docker/redis/conf/redis.conf:/etc/redis/redis.conf \
    -v /data/docker/redis/db:/data \
    redis:5 \
    redis-server /etc/redis/redis.conf
```

-------------------------------------------------------------------

## 安装 MySQL（Docker）

```
mkdir -p /data/docker/mysql/datadir /data/docker/mysql/conf /data/docker/mysql/log
```

```
创建配置文件：
vim /data/docker/mysql/conf/mysql-1.cnf


[mysql]
default-character-set = utf8mb4

# 下面内容是 docker mysql 默认的 start
[mysqld]
pid-file = /var/run/mysqld/mysqld.pid
socket = /var/run/mysqld/mysqld.sock
datadir = /var/lib/mysql
#log-error = /var/log/mysql/error.log
# By default we only accept connections from localhost
#bind-address = 127.0.0.1
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
# 上面内容是 docker mysql 默认的 end

# 下面开始的内容就是我自己配置的
log-error=/var/log/mysql/error.log
default-storage-engine = InnoDB
collation-server = utf8mb4_unicode_520_ci
init_connect = 'SET NAMES utf8mb4'
character-set-server = utf8mb4
lower_case_table_names = 1
max_allowed_packet = 50M
```

```
chmod -R 777 /data/docker/mysql/datadir /data/docker/mysql/log
chown -R 0:0 /data/docker/mysql/conf
```


```
docker run \
	--name cdk8s-mysql \
	--restart always \
	-d \
	-p 3306:3306 \
	-v /data/docker/mysql/datadir:/var/lib/mysql \
	-v /data/docker/mysql/log:/var/log/mysql \
	-v /data/docker/mysql/conf:/etc/mysql/conf.d \
	-e MYSQL_ROOT_PASSWORD=123456 \
	mysql:5.7
```

## 安装 Prometheus（Docker）

```

创建配置文件：
mkdir -p /data/docker/prometheus/conf && vim /data/docker/prometheus/conf/prometheus.yml
chmod -R 777 /data/docker/prometheus

# my global config
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"


scrape_configs:
  - job_name: 'cdk8s-sso'
    metrics_path: '/tkey-actuator/actuator/prometheus'
    static_configs:
    - targets: ['172.16.16.4:19091']
```


- 启动

```
docker run \
    -d \
    --name cdk8s-prometheus \
    --restart always \
    -p 9090:9090 \
    -v /data/docker/prometheus/conf/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```


## 安装 Grafana（Docker）


```
mkdir -p /data/docker/grafana/data
chmod -R 777 /data/docker/grafana/data

docker run \
    -d \
    --name cdk8s-grafana \
    --restart always \
    -p 3000:3000 \
    -v /data/docker/grafana/data:/var/lib/grafana \
    grafana/grafana
```

- <http://127.0.0.1:3000>
- 默认管理账号；admin，密码：admin，第一次登录后需要修改密码


## 安装 Nginx（Docker）

```
mkdir -p /data/docker/nginx/logs /data/docker/nginx/conf
chmod -R 777 /data/docker/nginx
```

```
创建配置文件：
vim /data/docker/nginx/conf/nginx.conf




worker_processes      1;

events {
  worker_connections  1024;
}

http {
  include             mime.types;
  default_type        application/octet-stream;

  sendfile on;

  keepalive_timeout   65;

  server {
    listen            80;
    server_name       localhost 127.0.0.1 191.112.221.203;

    location / {
      root            /usr/share/nginx/html;
      index           index.html index.htm;
    }
  }
}
```


- 运行容器：

```
docker run \
    -d \
    --name cdk8s-nginx \
    --restart always \
    -p 80:80 \
    -v /data/docker/nginx/logs:/var/log/nginx \
    -v /data/docker/nginx/conf/nginx.conf:/etc/nginx/nginx.conf:ro \
    nginx:1.17
```
- 重新启动服务：`docker restart cdk8s-nginx`








