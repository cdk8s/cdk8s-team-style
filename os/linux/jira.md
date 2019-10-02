# Jira 安装和配置


## Jira 介绍

- 官网：<https://www.atlassian.com/software/jira>
- 官网下载：<https://www.atlassian.com/software/jira/download>
- 官网帮助中心：<https://confluence.atlassian.com/alldoc/>

## Jira 版本

- 2019-10：8.4.1
- 2019-04：7.13.3

#### 数据库配置


- 创建本地数据存储 + 配置文件目录：`mkdir -p /data/docker/mysql/datadir /data/docker/mysql/conf /data/docker/mysql/log`
- 在宿主机上创建一个配置文件：`vim /data/docker/mysql/conf/mysql-1.cnf`，内容如下：

```
# 该编码设置是我自己配置的
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

- 赋权：`chmod -R 777 /data/docker/mysql/datadir /data/docker/mysql/log`
- 赋权：`chown -R 0:0 /data/docker/mysql/conf`


```
docker run \
	--name mysql-jira \
	-p 3306:3306 \
	-v /data/docker/mysql/datadir:/var/lib/mysql \
    -v /data/docker/mysql/log:/var/log/mysql \
    -v /data/docker/mysql/conf:/etc/mysql/conf.d \
	-e MYSQL_ROOT_PASSWORD=cdk8s123456 \
	-e MYSQL_DATABASE=jira_db \
	-e MYSQL_USER=jira_user \
	-e MYSQL_PASSWORD=cdk8s123456 \
	-d \
	mysql:5.7
```

- 连上容器：`docker exec -it mysql-jira /bin/bash`
	- 连上 MySQL：`mysql -u root -p`
- 设置编码：**必须做这一步，不然配置过程会报错，JIRA 的 DB 要求是 utf8mb4**

```
SET NAMES 'utf8mb4';
alter database jira_db character set utf8mb4;
```


#### 安装

- 下载：<https://www.atlassian.com/software/jira/download>
    - 选择：tar.gz 类型下载
- 解压：`tar zxvf atlassian-jira-software-8.4.1.tar.gz`
- 创建 home 目录：`mkdir /usr/local/atlassian-jira-software-8.4.1-standalone/data`
- 配置 home 变量：

```
编辑：vim ~/.zshrc

在文件尾部添加：

JIRA_HOME=/usr/local/atlassian-jira-software-8.4.1-standalone/data
export JIRA_HOME


刷新配置：source ~/.zshrc
```

- 设置 MySQL 连接：
- 把 mysql-connector-java-5.1.47.jar 放在目录 `/usr/local/atlassian-jira-software-8.4.1-standalone/atlassian-jira/WEB-INF/lib`


#### License 过程

- 参考自己的为知笔记


#### 运行

- 启动：`sh /usr/local/atlassian-jira-software-8.4.1-standalone/bin/start-jira.sh`
- 停止：`sh /usr/local/atlassian-jira-software-8.4.1-standalone/bin/stop-jira.sh`
    - `ps -ef | grep java`
- 查看 log：`tail -300f /usr/local/atlassian-jira-software-8.4.1-standalone/logs/catalina.out`
- 访问：<http://服务器ip:8080>
    - 注意防火墙配置
- 如果需要更换端口号可以修改：`/usr/local/atlassian-jira-software-8.4.1-standalone/conf/server.xml` 文件中的内容。


#### 中文化

- 从 7.x 版本默认已经有中文支持，不需要再汉化了
- 在安装后首次进入的时候就可以配置，选择中文了
        

#### 首次配置

- 参考文章：<https://blog.csdn.net/yelllowcong/article/details/79624970>
- 因为步骤一样，所以我就不再截图了。

    
