# Harbor 安装和配置

## 环境说明

- CentOS 7.4
- 准备一个域名 harbor.cdk8s.com
- 准备 https 证书（nginx 类型）

## 官方文档

- 安装指导：<https://goharbor.io/docs/2.0.0/install-config/>
	- 从中我们可以知道需要：[Docker、Docker Compose 环境](./docker.md)
- 硬件最低要求：2C + 4GB（推荐 4C8GB）
	- 官网有推荐配置说明：[hardware](https://goharbor.io/docs/2.0.0/install-config/installation-prereqs/)
- 下载：<https://github.com/goharbor/harbor/releases>
	- 当前（2020-11）最新版本：**v2.0.3**
	- 当前（2020-11）最新版本：**v2.1.1**
	- 分 offline 和 online 版本，推荐使用 offline



## 安装

- 下载（524MB）：`cd /usr/local && wget https://github.com/goharbor/harbor/releases/download/v2.0.3/harbor-offline-installer-v2.1.1.tgz`
- 上传域名证书到：/opt/certs
    - 4707840_harbor.cdk8s.com.key
    - 4707840_harbor.cdk8s.com.pem
- 解压：`tar xvf harbor-offline-installer-v2.1.1.tgz`
- 复制配置文件：`cp /usr/local/harbor/harbor.yml.tmpl /usr/local/harbor/harbor.yml`：
- 修改配置文件：`vim /usr/local/harbor/harbor.yml`：


```

# 改为自己的域名
hostname: harbor.cdk8s.com


# 修改 https 证书
http:
  port: 80
https:
  port: 443
  certificate: /opt/certs/4707840_harbor.cdk8s.com.pem
  private_key: /opt/certs/4707840_harbor.cdk8s.com.key


# 启动Harbor后，管理员UI登录的密码，默认是 Harbor12345，用户名默认是：admin
harbor_admin_password: Harbor123456
```

- 开始安装：`sh /usr/local/harbor/install.sh`，控制台输出如下（预计需要 2 ~ 5 分钟）：

```
[Step 0]: checking if docker is installed ...
Note: docker version: 19.03.13
[Step 1]: checking docker-compose is installed ...
Note: docker-compose version: 1.27.4

[Step 1]: loading Harbor images ...
52ef9064d2e4: Loading layer [==================================================>]  135.9MB/135.9MB
4a6862dbadda: Loading layer [==================================================>]  23.25MB/23.25MB
.......
Creating network "harbor_harbor" with the default driver
Creating harbor-log ... done
Creating registry      ... done
Creating redis         ... done
Creating registryctl   ... done
Creating harbor-db     ... done
Creating harbor-portal ... done
Creating harbor-core   ... done
Creating harbor-jobservice ... done
Creating nginx             ... done
✔ ----Harbor has been installed and started successfully.----
```

- 测试安装结果

```
在本地的客户端测试是否可以登录
docker login -u admin -p Harbor123456 harbor.cdk8s.com
Login Succeeded


访问浏览器：harbor.cdk8s.com
输入账号密码
访问：<https://harbor.cdk8s.com/harbor/projects>，创建一个项目，比如：`sacf`，等下需要用到。
给本地的一个 maven 镜像打 tag，然后 push 上去

docker pull maven:3.3-jdk-8
docker tag maven:3.3-jdk-8 harbor.cdk8s.com/sacf/harbor-maven:3.3-jdk-8
docker push harbor.cdk8s.com/sacf/harbor-maven:3.3-jdk-8


如果需要重启 Harbor 服务，需要进入其安装目录，执行如下命令：
cd /usr/local/harbor
docker-compse down -v
docker-compse up -d
```


#### 如果你用 IP 地址配置 harbor 或者没有用 https 域名，你需要如下操作：

- docker 客户端默认是使用 https 访问 docker registry，我们默认在安装 Harbor 的时候配置文件用的时候 http，所以其他 docker 客户端需要修改
	- `vim /lib/systemd/system/docker.service`
	- 修改默认值为：`ExecStart=/usr/bin/dockerd`
	- 改为：`ExecStart=/usr/bin/dockerd --insecure-registry harbor.gitnavi.com`
	- `systemctl daemon-reload`
    - `systemctl reload docker`
    - `systemctl restart docker`


----------------------------------------------------------------------------

## harbor.yml 安装后的默认值

```
# Configuration file of Harbor

# The IP address or hostname to access admin UI and registry service.
# DO NOT use localhost or 127.0.0.1, because Harbor needs to be accessed by external clients.
hostname: reg.mydomain.com

# http related config
http:
  # port for http, default is 80. If https enabled, this port will redirect to https port
  port: 80

# https related config
https:
  # https port for harbor, default is 443
  port: 443
  # The path of cert and key files for nginx
  certificate: /your/certificate/path
  private_key: /your/private/key/path

# # Uncomment following will enable tls communication between all harbor components
# internal_tls:
#   # set enabled to true means internal tls is enabled
#   enabled: true
#   # put your cert and key files on dir
#   dir: /etc/harbor/tls/internal

# Uncomment external_url if you want to enable external proxy
# And when it enabled the hostname will no longer used
# external_url: https://reg.mydomain.com:8433

# The initial password of Harbor admin
# It only works in first time to install harbor
# Remember Change the admin password from UI after launching Harbor.
harbor_admin_password: Harbor12345

# Harbor DB configuration
database:
  # The password for the root user of Harbor DB. Change this before any production use.
  password: root123
  # The maximum number of connections in the idle connection pool. If it <=0, no idle connections are retained.
  max_idle_conns: 50
  # The maximum number of open connections to the database. If it <= 0, then there is no limit on the number of open connections.
  # Note: the default number of connections is 1024 for postgres of harbor.
  max_open_conns: 1000

# The default data volume
data_volume: /data

# Harbor Storage settings by default is using /data dir on local filesystem
# Uncomment storage_service setting If you want to using external storage
# storage_service:
#   # ca_bundle is the path to the custom root ca certificate, which will be injected into the truststore
#   # of registry's and chart repository's containers.  This is usually needed when the user hosts a internal storage with self signed certificate.
#   ca_bundle:

#   # storage backend, default is filesystem, options include filesystem, azure, gcs, s3, swift and oss
#   # for more info about this configuration please refer https://docs.docker.com/registry/configuration/
#   filesystem:
#     maxthreads: 100
#   # set disable to true when you want to disable registry redirect
#   redirect:
#     disabled: false

# Clair configuration
clair:
  # The interval of clair updaters, the unit is hour, set to 0 to disable the updaters.
  updaters_interval: 12

# Trivy configuration
#
# Trivy DB contains vulnerability information from NVD, Red Hat, and many other upstream vulnerability databases.
# It is downloaded by Trivy from the GitHub release page https://github.com/aquasecurity/trivy-db/releases and cached
# in the local file system. In addition, the database contains the update timestamp so Trivy can detect whether it
# should download a newer version from the Internet or use the cached one. Currently, the database is updated every
# 12 hours and published as a new release to GitHub.
trivy:
  # ignoreUnfixed The flag to display only fixed vulnerabilities
  ignore_unfixed: false
  # skipUpdate The flag to enable or disable Trivy DB downloads from GitHub
  #
  # You might want to enable this flag in test or CI/CD environments to avoid GitHub rate limiting issues.
  # If the flag is enabled you have to download the `trivy-offline.tar.gz` archive manually, extract `trivy.db` and
  # `metadata.json` files and mount them in the `/home/scanner/.cache/trivy/db` path.
  skip_update: false
  #
  # insecure The flag to skip verifying registry certificate
  insecure: false
  # github_token The GitHub access token to download Trivy DB
  #
  # Anonymous downloads from GitHub are subject to the limit of 60 requests per hour. Normally such rate limit is enough
  # for production operations. If, for any reason, it's not enough, you could increase the rate limit to 5000
  # requests per hour by specifying the GitHub access token. For more details on GitHub rate limiting please consult
  # https://developer.github.com/v3/#rate-limiting
  #
  # You can create a GitHub token by following the instructions in
  # https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
  #
  # github_token: xxx

jobservice:
  # Maximum number of job workers in job service
  max_job_workers: 10

notification:
  # Maximum retry count for webhook job
  webhook_job_max_retry: 10

chart:
  # Change the value of absolute_url to enabled can enable absolute url in chart
  absolute_url: disabled

# Log configurations
log:
  # options are debug, info, warning, error, fatal
  level: info
  # configs for logs in local storage
  local:
    # Log files are rotated log_rotate_count times before being removed. If count is 0, old versions are removed rather than rotated.
    rotate_count: 50
    # Log files are rotated only if they grow bigger than log_rotate_size bytes. If size is followed by k, the size is assumed to be in kilobytes.
    # If the M is used, the size is in megabytes, and if G is used, the size is in gigabytes. So size 100, size 100k, size 100M and size 100G
    # are all valid.
    rotate_size: 200M
    # The directory on your host that store log
    location: /var/log/harbor

  # Uncomment following lines to enable external syslog endpoint.
  # external_endpoint:
  #   # protocol used to transmit log to external endpoint, options is tcp or udp
  #   protocol: tcp
  #   # The host of external endpoint
  #   host: localhost
  #   # Port of external endpoint
  #   port: 5140

#This attribute is for migrator to detect the version of the .cfg file, DO NOT MODIFY!
_version: 2.0.0

# Uncomment external_database if using external database.
# external_database:
#   harbor:
#     host: harbor_db_host
#     port: harbor_db_port
#     db_name: harbor_db_name
#     username: harbor_db_username
#     password: harbor_db_password
#     ssl_mode: disable
#     max_idle_conns: 2
#     max_open_conns: 0
#   clair:
#     host: clair_db_host
#     port: clair_db_port
#     db_name: clair_db_name
#     username: clair_db_username
#     password: clair_db_password
#     ssl_mode: disable
#   notary_signer:
#     host: notary_signer_db_host
#     port: notary_signer_db_port
#     db_name: notary_signer_db_name
#     username: notary_signer_db_username
#     password: notary_signer_db_password
#     ssl_mode: disable
#   notary_server:
#     host: notary_server_db_host
#     port: notary_server_db_port
#     db_name: notary_server_db_name
#     username: notary_server_db_username
#     password: notary_server_db_password
#     ssl_mode: disable

# Uncomment external_redis if using external Redis server
# external_redis:
#   # support redis, redis+sentinel
#   # host for redis: <host_redis>:<port_redis>
#   # host for redis+sentinel:
#   #  <host_sentinel1>:<port_sentinel1>,<host_sentinel2>:<port_sentinel2>,<host_sentinel3>:<port_sentinel3>
#   host: redis:6379
#   password:
#   # sentinel_master_set must be set to support redis+sentinel
#   #sentinel_master_set:
#   # db_index 0 is for core, it's unchangeable
#   registry_db_index: 1
#   jobservice_db_index: 2
#   chartmuseum_db_index: 3
#   clair_db_index: 4
#   trivy_db_index: 5
#   idle_timeout_seconds: 30

# Uncomment uaa for trusting the certificate of uaa instance that is hosted via self-signed cert.
# uaa:
#   ca_file: /path/to/ca

# Global proxy
# Config http proxy for components, e.g. http://my.proxy.com:3128
# Components doesn't need to connect to each others via http proxy.
# Remove component from `components` array if want disable proxy
# for it. If you want use proxy for replication, MUST enable proxy
# for core and jobservice, and set `http_proxy` and `https_proxy`.
# Add domain to the `no_proxy` field, when you want disable proxy
# for some special registry.
proxy:
  http_proxy:
  https_proxy:
  no_proxy:
  components:
    - core
    - jobservice
    - clair
    - trivy
```


## 资料

- <https://www.ilanni.com/?p=13492>
- <https://blog.csdn.net/aixiaoyang168/article/details/73549898>
