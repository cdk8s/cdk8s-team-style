
# Docker 安装和使用

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap

## Docker 基本介绍

- 官网：<https://www.docker.com/>


## Docker 安装

- 主要有两个版本，我们选择 CE 版本
    - Docker Enterprise Edition (Docker EE)
    - Docker Community Edition (Docker CE)
- 官网总的安装手册：<https://docs.docker.com/install/>
- 官网 CentOS 安装手册，这里我进行了抽取：<https://docs.docker.com/install/linux/docker-ce/centos/>
    - 不推荐 RPM 安装，除非没有网络

```
卸载旧版本（非必须）
sudo yum remove \
    docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-engine

安装依赖包
sudo yum install -y \
    yum-utils \
    device-mapper-persistent-data \
    lvm2

添加源（可能网络会很慢，有时候会报：Timeout，所以要多试几次）
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
 
更新本地包信息
sudo yum makecache fast

安装最新版本（部分地区速度可能会有点慢）
sudo yum install -y docker-ce docker-ce-cli containerd.io

查看有哪些版本可以安装（特殊场景）
yum list docker-ce --showduplicates | sort -r

安装指定版本（特殊场景）
sudo yum install docker-ce-18.09.1 docker-ce-cli-18.09.1 containerd.io

启动服务
sudo systemctl start docker

运行 demo 容器（部分地区速度可能会有点慢）
sudo docker run hello-world

停止服务
sudo systemctl stop docker
```
-------------------------------------------------------------------

## 镜像加速（阿里云）
 
- 目前国内常用的如下：
    - 阿里云：<https://dev.aliyun.com/search.html>
    - USTC：<https://lug.ustc.edu.cn/wiki/mirrors/help/docker>
    - daocloud：<http://get.daocloud.io/>
    - 网易：<https://c.163.com>
    - 时速云：<https://hub.tenxcloud.com/>
    - 灵雀云：<https://hub.alauda.cn/>
- 推荐优先阿里云，然后是 USTC
- 我下面的讲解也是基于阿里云加速
- 阿里云的服务需要注册账号
	- 新创建命名空间：<https://cr.console.aliyun.com/cn-hangzhou/instance/namespaces>
    - 设置访问凭证（推荐用固定凭证）：<https://cr.console.aliyun.com/cn-hangzhou/instance/credentials>
	- 镜像仓库列表：<https://cr.console.aliyun.com/cn-hangzhou/instances/repositories>
	    - 你提交的 image 都会在这里出现
	    - 如果你的命名空间此时此刻是私有的，则你 push 的 image 也是私有的。当你的命名空间改为公开也不会影响已经 push 过的 image 属性，只能重新再来 push 一次。
    - 注册后请访问：<https://cr.console.aliyun.com/#/accelerator>，你会看到专属的加速地址，比如我是：`https://ldhc17y9.mirror.aliyuncs.com`，所以下面文章你看到该地址都表示是这个专属地址，请记得自己更换自己的。
    - 以及教你如何使用 Docker 加速器。如果你已经安装了最新版的 Docker 你就不需要用它的脚本进行安装了。
- 最新版本的 Docker 是新增配置文件：`vim /etc/docker/daemon.json`，增加如下内容：
 
``` bash
{
  "registry-mirrors": ["https://ldhc17y9.mirror.aliyuncs.com"]
}
```
 
- `sudo systemctl daemon-reload`
- `sudo systemctl restart docker`
- 在以后的生活中如果要经常使用阿里云做为自己仓库，那你还需要做：
    - 在 `namespace管理` 中创建属于你自己的 namespace：<https://cr.console.aliyun.com/#/namespace/index>
    - 创建镜像仓库：<https://cr.console.aliyun.com/#/imageList>
        - 创建好仓库后，点击：`管理` 进入查看仓库的更多详细信息，这里面有很多有用的信息，包括一个详细的操作指南，**这份指南等下会用到。**
        - 比如我自己创建一个 redis-to-cluster 仓库，地址是阿里云给我们的：`registry.cn-shenzhen.aliyuncs.com/youmeek/redis-to-cluster`
        - 那我登录这个镜像地址的方式：

```
docker login registry.cn-shenzhen.aliyuncs.com
会让我输入
Username：阿里云邮箱
password：上文提到的--Registry登录密码
```

- 然后在我的仓库管理地址有教我如何推送和拉取镜像：<https://cr.console.aliyun.com/#/dockerImage/cn-shenzhen/youmeek/redis-to-cluster/detail>
- 拉取：`docker pull registry.cn-shenzhen.aliyuncs.com/youmeek/redis-to-cluster:[镜像版本号]`
- 推送：

```
docker login

docker tag [ImageId] registry.cn-shenzhen.aliyuncs.com/youmeek/redis-to-cluster:[镜像版本号]

docker push registry.cn-shenzhen.aliyuncs.com/youmeek/redis-to-cluster:[镜像版本号]
```

-------------------------------------------------------------------

## Docker 基本命令
 
- 官网文档：<https://docs.docker.com/engine/reference/run/>
 
#### 版本信息
 
- `docker version`，查看docker版本
- `docker info`，显示docker系统的信息

#### 镜像仓库
 
- `docker pull`：从仓库下载镜像到本地
    - `docker pull centos:latest`：获取 CentOS 默认版本镜像
    - `docker pull centos:7.3.1611`：获取 CentOS 7 镜像，下载大小 70M 左右，下面的操作基于此镜像
    - `docker pull centos:6.8`：获取 CentOS 6 镜像
    - `docker pull registry.cn-hangzhou.aliyuncs.com/chainone/centos7-jdk8`：获取别人做好的阿里云镜像
- `docker push`：将一个镜像 push 到 registry 仓库中
	- `docker push myapache:v1`
- `docker search`：从 registry 仓库搜索镜像
	- `docker search -s 3 centos`，参数 `-s 数字`：表示筛选出收藏数（stars值）大于等于 3 的镜像
- `docker login`：登录到一个镜像仓库。默认登录的是官网的仓库：<https://hub.docker.com>
    - 登录阿里云仓库格式：`sudo docker login --username=阿里云邮箱`
	    - 比如我是这个：`docker login --username=23333212@qq.com registry.cn-shenzhen.aliyuncs.com`，你完整的登录地址你需要访问：<https://cr.console.aliyun.com/#/imageList>，在你自己创建的仓库中去查看那份详细操作指南上的地址
        - 密码就是你首次访问：<https://cr.console.aliyun.com/#/accelerator>，弹窗出来让你设置的那个密码，如果忘记了重新设置下即可，重设地址：<https://cr.console.aliyun.com/#/imageList>，右上角有一个：修改docker登录密码。

#### 本地镜像管理

- `docker stats`：查看当前启动的容器各自占用的系统资源
	- `bin docker stats --no-stream kafkadocker_kafka_1 kafkadocker_zookeeper_1`：查看指定容器的占用资源情况
	- 更加高级的监控方式有一个软件叫做：ctop（推荐使用）：<https://github.com/bcicen/ctop>
	
```
CONTAINER ID        NAME                      CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
4532a9ee27b8        cloud-cadvisor            1.49%               53.28MiB / 3.702GiB   1.41%               13.5MB / 646MB      265MB / 0B          19
3895d5d50a5e        kafkadocker_kafka_1       1.45%               1.24GiB / 3.702GiB    33.51%              145MB / 186MB       499MB / 724MB       128
1d1a6a7c48d8        kafkadocker_zookeeper_1   0.11%               70.85MiB / 3.702GiB   1.87%               55.8MB / 33.7MB     209MB / 1.22MB      23
```

- `docker images`：显示本地所有的镜像列表
	- 关注 REPOSITORY(名称)，TAG(标签)，IMAGE ID(镜像ID)三列
- `docker images centos`：查看具体镜像情况
- `docker rmi`：删除镜像，一般删除镜像前要先删除容器，不然如果镜像有被容器调用会报错
    - `docker rmi 容器ID`：删除具体某一个镜像
    - `docker rmi 仓库:Tag`：删除具体某一个镜像
    - `docker rmi $(docker images -q)`，删除所有镜像
    - `docker rmi -f $(docker images -q)`，强制删除所有镜像
    - `docker rmi $(docker images | grep "vmware" | awk '{print $3}')`，批量删除带有 vmware 名称的镜像
- `docker tag`：为镜像打上标签
	- `docker tag -f ubuntu:14.04 ubuntu:latest`，-f 意思是强制覆盖
	- 同一个IMAGE ID可能会有多个TAG（可能还在不同的仓库），首先你要根据这些 image names 来删除标签，当删除最后一个tag的时候就会自动删除镜像；
	- `docker rmi 仓库:Tag`，取消标签（如果是镜像的最后一个标签，则会删除这个镜像）
- `docker build`：使用 Dockerfile 创建镜像（推荐）
	- `docker build . --rm -t runoob/ubuntu:v1`，参数 `-t`，表示：-tag，打标签
	- 多次 docker build 过程中是有依赖一个缓存的过程的，一般 build 过程都有好几个 step，Docker 非常聪明，会自己判断那些没有被修改过程的 step 采用缓存。如果想要避免使用缓存，可以使用这样命令 **--no-cache**：`docker build --no-cache . --rm -t runoob/ubuntu:v1`
- `docker history`：显示生成一个镜像的历史命令，可以看出这个镜像的构建过程，包括：每一层镜像的 ID、指令
- `docker save`：将一个镜像保存为一个 tar 包，带 layers 和 tag 信息（导出一个镜像）
    - `docker save 镜像ID -o /opt/test.tar`
- `docker load`：从一个 tar 包创建一个镜像（导入一个镜像）
    - `docker load -i /opt/test.tar`


#### 容器生命周期管理
 
- `docker run`，运行镜像
    - `docker run -v /java_logs/:/opt/ -d -p 8080:80 --name=myDockerNameIsGitNavi --hostname=myDockerNameIsGitNavi -i -t 镜像ID /bin/bash`
        - `-i -t` 分别表示保证容器中的 STDIN 开启，并分配一个伪 tty 终端进行交互，这两个是合着用。
        - `--name` 是给容器起了一个名字（如果没有主动给名字，docker 会自动给你生成一个）容器的名称规则：大小写字母、数字、下划线、圆点、中横线，用正则表达式来表达就是：[a-zA-Z0-9_*-]
        - `-d` 容器运行在后台。
        - `-p 8080:80` 表示端口映射，将宿主机的8080端口转发到容器内的80端口。（如果是 -P 参数，则表示随机映射应该端口，一般用在测试的时候）
        - `-v /java_logs/:/opt/` 表示目录挂载，/java_logs/ 是宿主机的目录，/opt/ 是容器目录
    - `docker run --rm --name=myDockerNameIsGitNavi --hostname=myDockerNameIsGitNavi -i -t centos /bin/bash`，--rm，表示退出即删除容器，一般用在做实验测试的时候
    - `docker run --restart=always -i -t centos /bin/bash`，--restart=always 表示停止后会自动重启
    - `docker run --restart=on-failure:5 -i -t centos /bin/bash`，--restart=on-failure:5 表示停止后会自动重启，最多重启 5 次
- `docker exec`：对守护式的容器里面执行命令，方便对正在运行的容器进行维护、监控、管理
    - `docker exec -i -t 容器ID /bin/bash`，进入正在运行的 docker 容器，并启动终端交互
    - `docker exec -d 容器ID touch /opt/test.txt`，已守护式的方式进入 docker 容器，并创建一个文件
- `docker stop 容器ID`，停止容器
    - `docker stop $(docker ps -a -q)`，停止所有容器
    - `docker stop $(docker ps -a -q) ; docker rm $(docker ps -a -q)`，停止所有容器，并删除所有容器
    - `docker kill $(docker ps -q) ; docker rm $(docker ps -a -q)`，停止所有容器，并删除所有容器
- `docker start 容器ID`，重新启动已经停止的容器（重新启动，docker run 参数还是保留之前的）
- `docker restart 容器ID`，重启容器
- `docker rm`，删除容器
    - `docker rm 容器ID`，删除指定容器（该容器必须是停止的）
    - `docker rm -f 容器ID`，删除指定容器（该容器如果正在运行可以这样删除）
    - `docker rm $(docker ps -a -q)`，删除所有容器
    - `docker rm -f $(docker ps -a -q)`，强制删除所有容器
	- `docker ps -a | grep 'weeks ago' | awk '{print $1}' | xargs docker rm` 删除老的(一周前创建)容器
	- `docker kill $(docker ps -q) ; docker rm $(docker ps -a -q) ; docker rmi $(docker images -q -a)` 停止所有容器，删除所有容器，删除所有镜像
- `docker commit`，把容器打成镜像
	- `docker commit 容器ID gitnavi/docker-nodejs-test:0.1`
		- gitnavi 是你注册的 https://store.docker.com/ 的名字，如果你没有的话，那需要先注册
		- docker-nodejs-test 是你为该镜像起的名字
		- 0.1 是镜像的版本号，默认是 latest 版本
    - `docker commit -m="这是一个描述信息" --author="GitNavi" 容器ID gitnavi/docker-nodejs-test:0.1`
	    - 在提交镜像时指定更多的数据（包括标签）来详细描述所做的修改
- `docker diff 容器ID`：显示容器文件系统的前后变化
- `--link` 同一个宿主机下的不同容器的连接：
	- `docker run -it 镜像ID --link redis-name:myredis /bin/bash`
		- `redis-name` 是容器名称
		- `myredis` 是容器别名，其他容器连接它可以用这个别名来写入到自己的配置文件中
- 容器与宿主机之间文件的拷贝
    - `docker cp /www/runoob 96f7f14e99ab:/www/` 将主机 /www/runoob 目录拷贝到容器 96f7f14e99ab 的 /www 目录下
    - `docker cp /www/runoob 96f7f14e99ab:/www` 将主机 /www/runoob 目录拷贝到容器 96f7f14e99ab 中，目录重命名为 www。
    - `docker cp  96f7f14e99ab:/www /tmp/` 将容器96f7f14e99ab的/www目录拷贝到主机的/tmp目录中。


#### docker 网络模式

- 查看也有网络：`docker network ls`
- 创建网络：`docker network create --subnet=172.19.0.0/16 net-redis-to-cluster`
- 已有容器连接到某个网络（一个容器可以同时连上多个网络）：`docker network connect net-redis-to-cluster my-redis-container`
- 如果是内网提供服务的，可以直接创建一个网络，其服务使用该网络。然后另外一个需要调用该服务的，并且是对外网提供服务的可以使用 host 模式
- `--network XXXXXX` 常见几种模式
	- bridge 默认模式，在 docker0 的网桥上创建新网络栈，确保独立的网络环境，实现网络隔离：`docker run -it 镜像ID --network=bridge /bin/bash`
	- none 不适用网卡，不会有 IP，无法联网：`docker run -it 镜像ID --network=none /bin/bash`
	- host 使用宿主机网络 IP、端口联网（在容器里面输入：ip a，看到的结果和在宿主机看到的一样）：`docker run -it 镜像ID --network=host /bin/bash`
	- 自定义-使用自己命名的网络栈，但是需要手动配置网卡、IP 信息：`docker run -it 镜像ID --network=自定义名称 /bin/bash`

#### 容器管理操作
 
- `docker ps`：列出当前所有 **正在运行** 的容器
    - `docker ps -a`：列出所有的容器（包含历史，即运行过的容器）
    - `docker ps -l`：列出最近一次启动的container
    - `docker ps -q`：列出最近一次运行的container ID
    - `docker ps -a -l`：列出最后一次运行的容器
    - `docker ps -n x`：显示最后 x 个容器，不管是正在运行或是已经停止的
- `docker top 容器ID`：显示容器的进程信息
- `docker events`：得到 docker 服务器的实时的事件
- `docker logs -f 容器ID`：查看容器日志（如果一些容器不断重启，或是自动停止，可以这样看下）
    - `docker logs 容器ID`，获取守护式容器的日志
    - `docker logs -f 容器ID`，不断监控容器日志，类似 tail -f
    - `docker logs -ft 容器ID`，在 -f 的基础上又增加 -t 表示为每条日志加上时间戳，方便调试
    - `docker logs --tail 10 容器ID`，获取日志最后 10 行
    - `docker logs --tail 0 -f 容器ID`，跟踪某个容器的最新日志而不必读取日志文件
    - `docker logs -f -t --since="2018-05-26" --tail=200 容器ID` 根据某个时间读取日志
    - `docker logs -f -t --since="2018-05-26T11:13:40" --tail=200 容器ID` 根据某个时间读取日志
    - `docker logs -f -t --since="2018-05-25T11:13:40" --until "2018-05-26T11:13:40" --tail=200 容器ID` 根据某个时间读取日志
    - `docker logs --since 10m 容器ID` 查看最近 10 分钟的日志
        - `-f` : 表示查看实时日志 
        - `-t` : 显示时间戳
        - `-since` : 显示某个开始时间的所有日志
        - `-tail=200` : 查看最后的 200 条日志
- `docker wait`，阻塞到一个容器，直到容器停止运行
- `docker export`，将容器整个文件系统导出为一个tar包，不带layers、tag等信息
- `docker port`，显示容器的端口映射
- `docker inspect 容器ID`：查看容器的全面信息，用 JSON 格式输出
- `docker inspect network名称`：查看 network 信息，用 JSON 格式输出，包含使用该网络的容器有哪些
- `docker container update --restart=always 容器ID`：调整容器为永远启动
- `docker system df`：类似于 Linux 上的 df 命令，用于查看 Docker 的磁盘使用情况
	- Images 镜像
	- Containers 容器
	- Local Volumes 数据卷

```
TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE
Images              6                   6                   1.049GB             0B (0%)
Containers          7                   4                   10.25kB             0B (0%)
Local Volumes       13                  5                   38.49GB             1.365MB (0%)
Build Cache                                                 0B                  0B
```

```
获取容器中的 IP：docker inspect -f {{.NetworkSettings.IPAddress}} 容器ID
获取容器中的 IP：docker inspect -f {{.Volumes}} 容器ID
查看容器的挂载情况：docker inspect 容器ID | grep Mounts -A 10
```

- 下面为一个 docker inspect 后的结果示例：

```json
[
    {
        "Id": "e1dff77b99d9c8489e0a0ce68a19ec5ffe18cc5d8b8ec17086f7f7bea29aa09b",
        "Created": "2018-01-18T03:47:16.138180181Z",
        "Path": "docker-entrypoint.sh",
        "Args": [
            "--auth"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 19952,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2018-01-18T03:47:16.348568927Z",
            "FinishedAt": "0001-01-01T00:00:00Z"
        },
        "Image": "sha256:42aa46cfbd7a0d1101311defac39872b447b32295b40f9c99104ede5d02e9677",
        "ResolvConfPath": "/var/lib/docker/containers/e1dff77b99d9c8489e0a0ce68a19ec5ffe18cc5d8b8ec17086f7f7bea29aa09b/resolv.conf",
        "HostnamePath": "/var/lib/docker/containers/e1dff77b99d9c8489e0a0ce68a19ec5ffe18cc5d8b8ec17086f7f7bea29aa09b/hostname",
        "HostsPath": "/var/lib/docker/containers/e1dff77b99d9c8489e0a0ce68a19ec5ffe18cc5d8b8ec17086f7f7bea29aa09b/hosts",
        "LogPath": "/var/lib/docker/containers/e1dff77b99d9c8489e0a0ce68a19ec5ffe18cc5d8b8ec17086f7f7bea29aa09b/e1dff77b99d9c8489e0a0ce68a19ec5ffe18cc5d8b8ec17086f7f7bea29aa09b-json.log",
        "Name": "/cas-mongo",
        "RestartCount": 0,
        "Driver": "overlay",
        "Platform": "linux",
        "MountLabel": "",
        "ProcessLabel": "",
        "AppArmorProfile": "",
        "ExecIDs": null,
        "HostConfig": {
            "Binds": [
                "/data/mongo/db:/data/db"
            ],
            "ContainerIDFile": "",
            "LogConfig": {
                "Type": "json-file",
                "Config": {}
            },
            "NetworkMode": "default",
            "PortBindings": {
                "27017/tcp": [
                    {
                        "HostIp": "",
                        "HostPort": "27017"
                    }
                ]
            },
            "RestartPolicy": {
                "Name": "always",
                "MaximumRetryCount": 0
            },
            "AutoRemove": false,
            "VolumeDriver": "",
            "VolumesFrom": null,
            "CapAdd": null,
            "CapDrop": null,
            "Dns": [],
            "DnsOptions": [],
            "DnsSearch": [],
            "ExtraHosts": null,
            "GroupAdd": null,
            "IpcMode": "shareable",
            "Cgroup": "",
            "Links": null,
            "OomScoreAdj": 0,
            "PidMode": "",
            "Privileged": false,
            "PublishAllPorts": false,
            "ReadonlyRootfs": false,
            "SecurityOpt": null,
            "UTSMode": "",
            "UsernsMode": "",
            "ShmSize": 67108864,
            "Runtime": "runc",
            "ConsoleSize": [
                0,
                0
            ],
            "Isolation": "",
            "CpuShares": 0,
            "Memory": 0,
            "NanoCpus": 0,
            "CgroupParent": "",
            "BlkioWeight": 0,
            "BlkioWeightDevice": [],
            "BlkioDeviceReadBps": null,
            "BlkioDeviceWriteBps": null,
            "BlkioDeviceReadIOps": null,
            "BlkioDeviceWriteIOps": null,
            "CpuPeriod": 0,
            "CpuQuota": 0,
            "CpuRealtimePeriod": 0,
            "CpuRealtimeRuntime": 0,
            "CpusetCpus": "",
            "CpusetMems": "",
            "Devices": [],
            "DeviceCgroupRules": null,
            "DiskQuota": 0,
            "KernelMemory": 0,
            "MemoryReservation": 0,
            "MemorySwap": 0,
            "MemorySwappiness": null,
            "OomKillDisable": false,
            "PidsLimit": 0,
            "Ulimits": null,
            "CpuCount": 0,
            "CpuPercent": 0,
            "IOMaximumIOps": 0,
            "IOMaximumBandwidth": 0
        },
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay/0ab08b1f9c8f5f70cdcac2b01d9ee31de9e5a4955003567573635e8837931249/root",
                "MergedDir": "/var/lib/docker/overlay/4d6bb0d57f3f1b1dcf98c70b4bee4abf8dc110c7efa685ee5d84fe6f58c07b63/merged",
                "UpperDir": "/var/lib/docker/overlay/4d6bb0d57f3f1b1dcf98c70b4bee4abf8dc110c7efa685ee5d84fe6f58c07b63/upper",
                "WorkDir": "/var/lib/docker/overlay/4d6bb0d57f3f1b1dcf98c70b4bee4abf8dc110c7efa685ee5d84fe6f58c07b63/work"
            },
            "Name": "overlay"
        },
        "Mounts": [
            {
                "Type": "volume",
                "Name": "6cd9721ff6a2768cd20e4a0678b176fa81a5de1c7d21fe6212b50c6854196db2",
                "Source": "/var/lib/docker/volumes/6cd9721ff6a2768cd20e4a0678b176fa81a5de1c7d21fe6212b50c6854196db2/_data",
                "Destination": "/data/configdb",
                "Driver": "local",
                "Mode": "",
                "RW": true,
                "Propagation": ""
            },
            {
                "Type": "bind",
                "Source": "/data/mongo/db",
                "Destination": "/data/db",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            }
        ],
        "Config": {
            "Hostname": "e1dff77b99d9",
            "Domainname": "",
            "User": "",
            "AttachStdin": false,
            "AttachStdout": false,
            "AttachStderr": false,
            "ExposedPorts": {
                "27017/tcp": {}
            },
            "Tty": false,
            "OpenStdin": false,
            "StdinOnce": false,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "GOSU_VERSION=1.7",
                "GPG_KEYS=0C49F3730359A14518585931BC711F9BA15703C6",
                "MONGO_PACKAGE=mongodb-org",
                "MONGO_REPO=repo.mongodb.org",
                "MONGO_MAJOR=3.4",
                "MONGO_VERSION=3.4.10"
            ],
            "Cmd": [
                "--auth"
            ],
            "Image": "mongo:3.4",
            "Volumes": {
                "/data/configdb": {},
                "/data/db": {}
            },
            "WorkingDir": "",
            "Entrypoint": [
                "docker-entrypoint.sh"
            ],
            "OnBuild": null,
            "Labels": {}
        },
        "NetworkSettings": {
            "Bridge": "",
            "SandboxID": "7eabf418238f4d9f5fd5163fd4d173bbaea7764687a5cf40a9757d42b90ab2f9",
            "HairpinMode": false,
            "Link                                                            LocalIPv6Address": "",
            "LinkLocalIPv6PrefixLen": 0,
            "Ports": {
                "27017/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "27017"
                    }
                ]
            },
            "SandboxKey": "/var/run/docker/netns/7eabf418238f",
            "SecondaryIPAddresses": null,
            "SecondaryIPv6Addresses": null,
            "EndpointID": "11c8d10a4be63b4ed710add6c440adf9d090b71918d4aaa837c46258e5425b80",
            "Gateway": "172.17.0.1",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "172.17.0.2",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "MacAddress": "02:42:ac:11:00:02",
            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": null,
                    "NetworkID": "ada97659acda146fc57e15a099e430a6e97de87f6d043b91d4c3582f6ab52d47",
                    "EndpointID": "11c8d10a4be63b4ed710add6c440adf9d090b71918d4aaa837c46258e5425b80",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:11:00:02",
                    "DriverOpts": null
                }
            }
        }
    }
]
```

## Docker 容器产生的 log 位置

- Docker 运行一段时间，如果你的容器有大量的输出信息，则这个 log 文件会非常大，所以要考虑清理。
- log 位置：`/var/lib/docker/containers/容器ID值/容器ID值-json.log`
- 可以考虑在停到容器的时候备份这个文件到其他位置，然后：`echo > 容器ID值-json.log`
- 当然，官网也提供了自动化的方案：<https://docs.docker.com/config/containers/logging/json-file/>
	- 修改 Docker 是配置文件：`vim /etc/docker/daemon.json`，（如果没有这个文件，自己新增）增加如下内容：
 
``` bash
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "5"
  }
}
```

- 如果你已经有该文件文件莱使用国内源，那修改方案应该是这样的：
 
``` bash
{
	"registry-mirrors": ["https://ldhc17y9.mirror.aliyuncs.com"],
	"log-driver": "json-file",
	"log-opts": {
		"max-size": "10m",
	    "max-file": "5"
	}
}
```

## 删除 Docker 镜像中为 none 的镜像

- Dockerfile 代码更新频繁，自然 docker build 构建同名镜像也频繁的很，产生了众多名为 none 的无用镜像

```
docker rmi $(docker images -f "dangling=true" -q)
```

## Docker daemon.json 可配置参数

- 查看文档：<https://docs.docker.com/engine/reference/commandline/dockerd/>

## Docker remote api 远程操作配置（保证在内网环境）

- 假设要被远程操作的服务器 IP：`192.168.1.22`
- 修改其配置文件：`vim /lib/systemd/system/docker.service`
- 修改默认值为：`ExecStart=/usr/bin/dockerd`
- 改为：`ExecStart=/usr/bin/dockerd -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2376`
	- 如果还需要连自己的 harbor 这类，完整配置：`ExecStart=/usr/bin/dockerd --insecure-registry harbor.youmeek.com -H unix:///var/run/docker.sock -H tcp://0.0.0.0:2376`
- `systemctl daemon-reload`
- `systemctl reload docker`
- `systemctl restart docker`
- 验证：
	- 在其他服务器上运行：`docker -H 192.168.1.22:2376 images `
	- 能拿到和它本身看到的一样的数据表示可以了


## Dockerfile 解释

- 该文件名就叫 Dockerfile，注意大小写，没有后缀，否则会报错。
- 主要由下面几个部分组成：
	- 基础镜像信息
	- 维护者/创建者信息
	- 镜像操作指令
	- 容器启动时执行执行
- 注释符号：`# 这是一段注释说明`
- 常用指令关键字：
	- `FROM`，基础镜像信息
	- `MAINTAINER`，维护者/创建者信息
	- `ADD`，添加文件。如果添加的文件是类似 tar.gz 压缩包，会自动解压。
		- 特别注意的是：ADD 文件到镜像的地址如果是目录，则需要最后保留斜杠，比如：`ADD test.tar.gz /opt/shell/`。不是斜杠结尾会认为是文件。
		- 添加文件格式：`ADD test.sh /opt/shell/test.sh`
		- 添加压缩包并解压格式：`ADD test.tar.gz /opt/shell/`，该压缩包会自动解压在 /opt/shell 目录下
	- `COPY`，类似 ADD，只是 COPY 只是复制文件，不会做类似解压压缩包这种行为。
		- `COPY /opt/conf/ /etc/` 把宿主机的 /opt/conf 下文件复制到镜像的 /etc 目录下。
	- `WORKDIR`，设置工作目录，可以理解为类似 cd 命令，表示现在在某个目录路径，然后下面的 CMD、ENTRYPOINT 操作都是基于此目录
	- `VOLUME`，目录挂载
	- `EXPOSE`，暴露端口
	- `USER`，指定该镜像以什么用户去运行，也可以用这个来指定：`docker run -u root`。不指定默认是 root
	- `ENV`，定义环境变量，该变量可以在后续的任何 RUN 指令中使用，使用方式：$HOME_DIR。在 docker run 的时候可以该方式来覆盖变量值 `docker run -e “HOME_DIR=/opt”`
	- `RUN`，执行命令并创建新的镜像层，RUN 经常用于安装软件包
	- `CMD`，执行命令，并且一个 Dockerfile 只能有一条 CMD，有多条的情况下最后一条有效。在一种场景下 CMD 命令无效：docker run 的时候也指定了相同命令，则 docker run 命令优先级最高
	- `ENTRYPOINT`，配置容器启动时运行的命令，不会被 docker run 指令覆盖，并且 docker run 的指令可以作为参数传递到 ENTRYPOINT 中。要覆盖 ENTRYPOINT 命令也是有办法的：docker run --entrypoint 方式。Dockerfile 同时有 CMD 和 ENTRYPOINT 的时候，CMD 的指令是作为参数传递给 ENTRYPOINT 使用。
		- 特别注意：RUN、CMD 和 ENTRYPOINT 这三个 Dockerfile 指令看上去很类似，很容易混淆。
		- 最佳实战：[来源](https://www.ibm.com/developerworks/community/blogs/132cfa78-44b0-4376-85d0-d3096cd30d3f/entry/RUN_vs_CMD_vs_ENTRYPOINT_%E6%AF%8F%E5%A4%A95%E5%88%86%E9%92%9F%E7%8E%A9%E8%BD%AC_Docker_%E5%AE%B9%E5%99%A8%E6%8A%80%E6%9C%AF_17?lang=en_us)
			- 使用 RUN 指令安装应用和软件包，构建镜像。
			- 如果 Docker 镜像的用途是运行应用程序或服务，比如运行一个 MySQL，应该优先使用 Exec 格式的 ENTRYPOINT 指令。CMD 可为 ENTRYPOINT 提供额外的默认参数，同时可利用 docker run 命令行替换默认参数。
			- 如果想为容器设置默认的启动命令，可使用 CMD 指令。用户可在 docker run 命令行中替换此默认命令。


## Dockerfile 部署 Spring Boot 应用

- jar 名称：skb-user-0.0.1-SNAPSHOT.jar
- 打算用的宿主机端口：9096
- Dockerfile 文件和 jar 文件存放在宿主机目录：/opt/zch
- Dockerfile 内容如下：

``` bash
FROM java:8-jre
MAINTAINER gitnavi <gitnavi@qq.com>

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD skb-user-0.0.1-SNAPSHOT.jar /usr/local/skb/user/

CMD ["java", "-Xmx500m", "-jar", "/usr/local/skb/user/skb-user-0.0.1-SNAPSHOT.jar", "--spring.profiles.active=test"]

EXPOSE 9096
```

- 开始构建：
	- `cd /opt/zch`
	- `docker build . --tag="skb/user:v1.0.1"`
		- 因为 build 过程中会有多层镜像 step 过程，所以如果 build 过程中失败，那解决办法的思路是找到 step 失败的上一层，成功的 step 中镜像 ID。然后 docker run 该镜像 ID，手工操作，看报什么错误，然后就比较清晰得了解错误情况了。
	- `docker run -d -p 9096:9096 -v /usr/local/logs/:/opt/ --name=skbUser --hostname=skbUser skb/user:v1.0.1`
	- 查看启动后容器列表：`docker ps`
	- jar 应用的日志是输出在容器的 /opt 目录下，因为我们上面用了挂载，所在在我们宿主机的 /usr/local/logs 目录下可以看到输出的日志
- 防火墙开放端口：
	- `firewall-cmd --zone=public --add-port=9096/tcp --permanent`
	- `firewall-cmd --reload`
- 解释：

```
# 是为了解决容器的时区和宿主机不一致问题
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
```

## Dockerfile 部署 Tomcat 应用

- 编写 Dockerfile

```
FROM tomcat:8.0.46-jre8
MAINTAINER GitNavi <gitnavi@qq.com>

ENV JAVA_OPTS="-Xms2g -Xmx2g -XX:MetaspaceSize=128M -XX:MaxMetaspaceSize=312M"
ENV CATALINA_HOME /usr/local/tomcat

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN rm -rf /usr/local/tomcat/webapps/*

ADD qiyeweixin.war /usr/local/tomcat/webapps/

EXPOSE 8080

CMD ["catalina.sh", "run"]
```

- 打包镜像：`docker build -t harbor.gitnavi.com/demo/qiyeweixin:1.2.2 ./`
- 运行：`docker run -d -p 8888:8080 --name=qiyeweixin --hostname=qiyeweixin -v /data/docker/logs/qiyeweixin:/data/logs/qiyeweixin harbor.gitnavi.com/demo/qiyeweixin:1.2.2`
- 带 JVM 参数运行：`docker run -d -p 8888:8080 -e JAVA_OPTS='-Xms7g -Xmx7g -XX:MetaspaceSize=128M -XX:MaxMetaspaceSize=512M' --name=qiyeweixin --hostname=qiyeweixin -v /data/docker/logs/qiyeweixin:/data/logs/qiyeweixin harbor.gitnavi.com/demo/qiyeweixin:1.2.2`
	- 虽然 Dockerfile 已经有 JVM 参数，并且也是有效的。但是如果 docker run 的时候又带了 JVM 参数，则会以 docker run 的参数为准
- 测试 JVM 是否有效方法，在代码里面书写，该值要接近 xmx 值：

```
long maxMemory = Runtime.getRuntime().maxMemory();
logger.warn("-------------maxMemory=" + ((double) maxMemory / (1024 * 1024)));
```

## Docker Compose

- Docker Compose 主要用于定义和运行多个 Docker 容器的工具，这样可以快速运行一套分布式系统
	- 容器之间是有依赖关系，比如我一个 Java web 系统依赖 DB 容器、Redis 容器，必须这些依赖容器先运行起来。
- 一个文件：docker-compose.yml
- 一个命令：`docker-compose up`
    - 指定文件：`docker-compose -f zookeeper.yml -p zk_test up -d`
- 官网安装说明：<https://docs.docker.com/compose/install/#install-compose>
- 安装方法：

```
sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

```

- 检查是否安装成功：`docker-compose --version`，输出：`docker-compose version 1.18.0, build 8dd22a9`
- 常用命令：
	- 运行：`docker-compose up -d`
	- 停止运行：`docker-compose down`
	- 查看容器：`docker-compose ps`
	- 删除停止的服务容器：`docker-compose rm`

## Docker Swarm

- Docker Swarm 是一个 Docker 集群管理工具


## Harbor 镜像私有仓库

- 官网：<http://vmware.github.io/harbor/>

## 资料

- 书籍：《第一本 Docker 书》









