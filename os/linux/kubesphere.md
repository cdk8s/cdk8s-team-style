
# Kubernetes 高可用集群部署方案

- 由于需要高可用，所以至少 3 台 Master 节点和 3 台 Worker 节点，需要保证是 Master 和 Worker 节点数都是奇数的，以防止 leader 选举时出现脑裂状况。
- 我们这里假设使用多台阿里 ECS 实例快速部署一套高可用的生产环境，要满足 Kubernetes 集群服务需要做到高可用，需要保证 kube-apiserver 的 HA，我们暂时选择阿里云负载均衡（SLB）
- 由于 Kubernetes 集群中各个节点需要互相频繁通信，所以为了避免出现一些特别的问题，我们需要保证部署节点和各个节点之间要做到：
    - SSH 可以访问所有节点
    - 所有节点时间同步
    - 关闭 SELinux
    - 关闭局域网防火墙

![部署架构](https://s1.ax1x.com/2020/10/29/B8OwtA.png)

|主机|角色|
|---|---|
|eip|DNAT|
|eip|SLB|
|master1|master1, etcd|
|master2|master2, etcd|
|master3|master3, etcd|
|node1|node|
|node2|node|
|node3|node|

## 购买 ECS、EIP、NAT、SLB 注意细节

- 核心：必须保证 ECS、EIP、NAT、SLB 都在同一个地区（不用具体到可用区级别），可能有些地区有 ECS 但是其他比如 SLB 没有，所以一定要都看下购买页面的地区选择选项 
- 购买 6 台 ECS 服务器，都不需要有公网 IP
- EIP 需要 2 个，一个是绑定 SLB，一个绑定 NAT 网关的 DNAT（如果你还需要外网可以访问这些 ECS，那还需要一个 EIP 来绑定 NAT 网关的 SNAT，一个 EIP 只能绑定一个 ECS 所有端口，或者指定一台 ECS 的一个端口）
- 通过阿里云NAT网关产品实现无公网ECS通过有EIP的服务器代理访问公网
- 关于 EIP 介绍
    - 独立的公网IP资源，可以与阿里云专有网络VPC类型的ECS、NAT网关、ENI网卡、私网负载均衡SLB绑定，并可以动态解绑，实现公网IP与ECS、NAT网关、ENI网卡、SLB的解耦，满足灵活管理的要求。
- 关于 SLB 介绍
    - 负载均衡服务，通过流量分发来提升应用系统的服务能力，通过消除单点故障来提升应用系统的可用性。负载均衡具有即开即用，超大容量，稳定可靠，弹性伸缩，按需付费等特点，支持基于4层(TCP/UDP)负载均衡和基于7层(HTTP/HTTPS)反向代理。
- 关于 NAT 网关支持 SNAT 和 DNAT 介绍
    - SNAT 可以为VPC内无公网IP的 ECS 实例提供访问互联网的代理服务。
    - DNAT 可以将NAT网关上的公网IP映射给ECS实例使用，使ECS实例能够提供互联网服务
    - NAT 可以绑定多台 ECS，也可以直接绑定交换机。如果服务器都在一个交换机，直接绑定交换机最方便。
    - 一个 NAT 网关可以绑定 20 个 EIP

## Kubesphere 介绍

- Kubesphere 可以简单理解为是 Kubernetes 的官网外的一种 Dashboard
- Kubesphere 官网：<https://kubesphere.com.cn/>
- 通过 KubeSphere 可以快速管理 Kubernetes 集群、部署应用、服务发现、CI/CD 流水线、集群扩容、微服务治理、日志查询和监控告警
- KubeSphere 平台内置的多租户设计，让不同的团队能够在一个平台中不同的企业空间下，更安全地从云端到边缘部署云原生应用。开发者通过界面点击即可快速部署项目，平台内置丰富的云原生可观察性与 DevOps 工具集帮助运维人员定位问题和快速交付。
- 内置常用的自动化部署环境，为应用（Java/NodeJs/Python/Go）部署提供定制化的容器运行环境
- 基于 Jenkins 为引擎打造的 CI/CD，内置 Source-to-Image 和 Binary-to-Image 自动化打包部署工具
- 对底层 Kubernetes 中的多种类型的资源提供可视化的展示与监控数据，以向导式 UI 实现工作负载管理、镜像管理、服务与应用路由管理 (服务发现)、密钥配置管理等，并提供弹性伸缩 (HPA) 和容器健康检查支持

## Rainbond 介绍

- Rainbond 是以企业云原生应用开发、架构、运维、共享、交付为核心的 Kubernetes 平台
- Rainbond 官网：<https://www.rainbond.com>
- 基于 Kubernetes，但用户无需学习和编辑复杂的yaml文件，开发者仅需要以最简单的方式构建和维护应用模型，所有Kubernetes资源由Rainbond编排创建和维护
- 面向应用的DevOps开发流水线，提供从源码或简单镜像持续构建云原生应用的能力
- 节点自动安装、扩容、监控、容错。平台支持高可用、多数据中心管理、多租户管理。

## Rancher

- Rancher 为采用容器的团队提供了完整的软件堆栈，解决了跨任何基础设施架构管理多个 Kubernetes 集群的运维和安全挑战，同时为DevOps团队提供了用于运行容器化工作负载的集成工具。
- Rancher 官网：<https://rancher.com/>
- Rancher 可以集中管理部署在任何基础设施上的 Kubernetes 集群，还可以实行统一的集中式身份验证和访问控制
- Rancher 的流水线提供了简单的 CI / CD 体验。使用它可以自动拉取代码，运行构建或脚本，发布 Docker 镜像或应用商店应用以及部署更新的软件。

## kubernetes / dashboard

- kubernetes 官网出品的 dashboard
- Github 官网：<https://github.com/kubernetes/dashboard>
- Kubernetes 仪表板是用于 Kubernetes 集群的基于 web 的通用UI。它允许用户管理集群中运行的应用程序并对它们进行故障排除，以及管理集群本身。功能相对简单。

-------------------------------------------------------------------

## KubeSphere 3.0.0 在阿里云、腾讯云、物理机单机 All-in-one 经验总结

- **核心：** 在腾讯云上默认有一个坑，就是 hostname 是大写，会造成安装失败，所以请按照我的来
- 当前（202010）KubeSphere 最新版本号：3.0.0
- 官网说明：<https://kubesphere.io/zh/docs/quick-start/all-in-one-on-linux/>

#### 我的服务器硬件信息说明

```
8核 16GB 5Mbps 50GB
公网IP：81.61.121.155
私有IP：172.16.0.5
安全组是开放所有端口
```

#### 我的服务器软件信息说明

```
系统：CentOS 7.8

关闭 SELinux
setenforce 0 && sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

禁用防火墙
systemctl stop firewalld && systemctl disable firewalld && echo "vm.swappiness = 0" >> /etc/sysctl.conf && swapoff -a && sysctl -w vm.swappiness=0

安装一些简单工具：
yum install -y zip unzip lrzsz git epel-release wget htop deltarpm

服务器更换 CentOS YUM 源为阿里云
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum clean all && yum makecache
yum update -y

时间同步
timedatectl && timedatectl set-ntp true

设置 hostname，这个最好设置一下，并且设置全部小写字母和数字，一定要小写字母
hostnamectl set-hostname master

开始在所选安装机器上设置免密登录，我这里选择了 master1
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa

这里都是内网地址
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@172.16.0.5

测试下是否可以免登陆：
ssh -p 22 root@172.16.0.5
```

#### 安装 Docker

- 虽然 kubekey 安装中间会自动帮我们安装 docker，但是安装后默认的源是 Docker 国外的会很慢
- 所以我们可以考虑自己安装 Docker 并且修改源。当前时间 2020-10 KubeSphere 3.0.0 用的是 `Docker version 19.03.13, build 4484c46d9d`
- 开始安装 Docker

```
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y containerd.io docker-ce-19.03.13 docker-ce-cli-19.03.13

systemctl start docker
systemctl enable docker

修改镜像源配置
vim /etc/docker/daemon.json

{
  "registry-mirrors": [
    "https://ldhc17y9.mirror.aliyuncs.com",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}

systemctl daemon-reload
systemctl restart docker
```

## 安装 Kubernetes + KubeSphere

```
wget -c https://kubesphere.io/download/kubekey-v1.0.0-linux-amd64.tar.gz -O - | tar -xz
chmod +x kk

开始安装，终端会出现一个当前环境已有环境检查，比如 docker 已安装等
./kk create cluster --with-kubernetes v1.17.9 --with-kubesphere v3.0.0

如果安装过程出现错误中断了：Failed to init kubernetes cluster: interrupted by error
那就重新再执行下上面的脚本，重新来一次

当控制台出现这一行字，表示 kubesphere 开始进入守护进程方式安装后续部分了
INFO[12:51:25 CST] Installation is complete.
Please check the result using the command:
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f

这时候你可以看到你服务器已经下载了这些镜像：
[root@master1 ~]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
kubesphere/ks-installer              v3.0.0              893b46ffa208        6 weeks ago         692MB
kubesphere/kube-proxy                v1.17.9             ddc09a4c2193        3 months ago        117MB
kubesphere/kube-controller-manager   v1.17.9             c7f1dde319ee        3 months ago        161MB
kubesphere/kube-apiserver            v1.17.9             7417868987f3        3 months ago        171MB
kubesphere/kube-scheduler            v1.17.9             f7b1228fa995        3 months ago        94.4MB
calico/node                          v3.15.1             1470783b1474        3 months ago        262MB
calico/pod2daemon-flexvol            v3.15.1             a696ebcb2ac7        3 months ago        112MB
calico/cni                           v3.15.1             2858353c1d25        3 months ago        217MB
calico/kube-controllers              v3.15.1             8ed9dbffe350        3 months ago        53.1MB
kubesphere/provisioner-localpv       1.10.0              6b5529f464f7        5 months ago        68.4MB
kubesphere/node-disk-operator        0.5.0               8741fafb7b21        5 months ago        167MB
kubesphere/node-disk-manager         0.5.0               dbbed43bcbdb        5 months ago        168MB
kubesphere/k8s-dns-node-cache        1.15.12             5340ba194ec9        6 months ago        107MB
coredns/coredns                      1.6.9               faac9e62c0d6        7 months ago        43.2MB
kubesphere/etcd                      v3.3.12             28c771d7cfbf        21 months ago       40.6MB
kubesphere/pause                     3.1                 da86e6ba6ca1        2 years ago         742kB

我们可以根据命令来查看守护进程安装进度：
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f

当我们看到这个就表示守护进程安装成功了
#####################################################
###              Welcome to KubeSphere!           ###
#####################################################

Console: http://172.16.0.5:30880
Account: admin
Password: P@88w0rd

NOTES：
  1. After logging into the console, please check the
     monitoring status of service components in
     the "Cluster Management". If any service is not
     ready, please wait patiently until all components
     are ready.
  2. Please modify the default password after login.

#####################################################
https://kubesphere.io             2020-10-30 17:18:00
#####################################################


这时候我们再来看看下载了哪些镜像：
[root@master1 ~]# docker images
REPOSITORY                                    TAG                 IMAGE ID            CREATED             SIZE
kubesphere/ks-installer                       v3.0.0              893b46ffa208        6 weeks ago         692MB
kubesphere/ks-controller-manager              v3.0.0              85bd13080839        2 months ago        82MB
kubesphere/ks-apiserver                       v3.0.0              d9fac59cfb8c        2 months ago        120MB
kubesphere/ks-console                         v3.0.0              d5987e1f99ac        2 months ago        95.5MB
prom/prometheus                               v2.20.1             b205ccdd28d3        2 months ago        145MB
kubesphere/notification-manager               v0.1.0              331a0e6ece23        3 months ago        47.5MB
kubesphere/notification-manager-operator      v0.1.0              c441b79e9606        3 months ago        44.4MB
kubesphere/kube-proxy                         v1.17.9             ddc09a4c2193        3 months ago        117MB
kubesphere/kube-apiserver                     v1.17.9             7417868987f3        3 months ago        171MB
kubesphere/kube-controller-manager            v1.17.9             c7f1dde319ee        3 months ago        161MB
kubesphere/kube-scheduler                     v1.17.9             f7b1228fa995        3 months ago        94.4MB
calico/node                                   v3.15.1             1470783b1474        3 months ago        262MB
calico/pod2daemon-flexvol                     v3.15.1             a696ebcb2ac7        3 months ago        112MB
calico/cni                                    v3.15.1             2858353c1d25        3 months ago        217MB
calico/kube-controllers                       v3.15.1             8ed9dbffe350        3 months ago        53.1MB
kubesphere/prometheus-config-reloader         v0.38.3             8011d6eb5bac        4 months ago        10.1MB
kubesphere/prometheus-operator                v0.38.3             a703e647b26f        4 months ago        38.6MB
prom/alertmanager                             v0.21.0             c876f5897d7b        4 months ago        55.5MB
kubesphere/kube-state-metrics                 v1.9.6              092e8ed1e0b3        5 months ago        32.8MB
kubesphere/provisioner-localpv                1.10.0              6b5529f464f7        5 months ago        68.4MB
kubesphere/node-disk-operator                 0.5.0               8741fafb7b21        5 months ago        167MB
kubesphere/node-disk-manager                  0.5.0               dbbed43bcbdb        5 months ago        168MB
kubesphere/linux-utils                        1.10.0              28c1cd0be1ea        5 months ago        11MB
osixia/openldap                               1.3.0               faac9bb59f83        5 months ago        260MB
kubesphere/metrics-server                     v0.3.7              07c9e703ca2c        6 months ago        55.4MB
kubesphere/k8s-dns-node-cache                 1.15.12             5340ba194ec9        6 months ago        107MB
coredns/coredns                               1.6.9               faac9e62c0d6        7 months ago        43.2MB
csiplugin/snapshot-controller                 v2.0.1              525889021849        9 months ago        41.4MB
kubesphere/node-exporter                      ks-v0.18.1          cfb0175954de        11 months ago       23.7MB
kubesphere/kubectl                            v1.0.0              7f81664a09d0        12 months ago       82.1MB
redis                                         5.0.5-alpine        ed7d2ff5a623        14 months ago       29.3MB
jimmidyson/configmap-reload                   v0.3.0              7ec24a279487        14 months ago       9.7MB
kubesphere/etcd                               v3.3.12             28c771d7cfbf        21 months ago       40.6MB
kubesphere/kube-rbac-proxy                    v0.4.1              70eeaa7791f2        21 months ago       41.3MB
kubesphere/pause                              3.1                 da86e6ba6ca1        2 years ago         742kB
mirrorgooglecontainers/defaultbackend-amd64   1.4                 846921f0fe0e        3 years ago         4.84MB


等个 5 分钟再来看看有哪些 pod：
[root@master ~]# kubectl get pods -A
NAMESPACE                      NAME                                               READY   STATUS    RESTARTS   AGE
kube-system                    calico-kube-controllers-59d85c5c84-qbwqb           1/1     Running   0          12m
kube-system                    calico-node-zn84s                                  1/1     Running   0          12m
kube-system                    coredns-74d59cc5c6-plx4c                           1/1     Running   0          12m
kube-system                    coredns-74d59cc5c6-zct54                           1/1     Running   0          12m
kube-system                    kube-apiserver-master                              1/1     Running   0          12m
kube-system                    kube-controller-manager-master                     1/1     Running   0          12m
kube-system                    kube-proxy-9672d                                   1/1     Running   0          12m
kube-system                    kube-scheduler-master                              1/1     Running   0          12m
kube-system                    metrics-server-5ddd98b7f9-dbc2n                    1/1     Running   0          11m
kube-system                    nodelocaldns-6w4rr                                 1/1     Running   0          12m
kube-system                    openebs-localpv-provisioner-84956ddb89-jkdns       1/1     Running   0          12m
kube-system                    openebs-ndm-fcrlq                                  1/1     Running   0          12m
kube-system                    openebs-ndm-operator-6896cbf7b8-sz2pv              1/1     Running   1          12m
kube-system                    snapshot-controller-0                              1/1     Running   0          9m46s
kubesphere-controls-system     default-http-backend-5d464dd566-cns9c              1/1     Running   0          9m24s
kubesphere-controls-system     kubectl-admin-6c9bd5b454-54xhj                     1/1     Running   0          6m22s
kubesphere-monitoring-system   alertmanager-main-0                                2/2     Running   0          7m35s
kubesphere-monitoring-system   kube-state-metrics-5c466fc7b6-z8w2c                3/3     Running   0          8m30s
kubesphere-monitoring-system   node-exporter-jvgws                                2/2     Running   0          8m31s
kubesphere-monitoring-system   notification-manager-deployment-7ff95b7544-zzk6p   1/1     Running   0          4m12s
kubesphere-monitoring-system   notification-manager-operator-5cbb58b756-pnpwr     2/2     Running   0          8m17s
kubesphere-monitoring-system   prometheus-k8s-0                                   3/3     Running   1          7m25s
kubesphere-monitoring-system   prometheus-operator-78c5cdbc8f-hjg7p               2/2     Running   0          8m31s
kubesphere-system              ks-apiserver-566f7d5c96-rnk96                      1/1     Running   0          7m57s
kubesphere-system              ks-console-fb4c655cf-nkq5q                         1/1     Running   0          9m12s
kubesphere-system              ks-controller-manager-64459d95bb-p9jz7             1/1     Running   0          7m57s
kubesphere-system              ks-installer-85854b8c8-cmppw                       1/1     Running   0          12m
kubesphere-system              openldap-0                                         1/1     Running   0          9m35s
kubesphere-system              redis-6fd6c6d6f9-96rs2                             1/1     Running   0          9m40s
```

- 访问管理界面：<http://81.61.121.155:30880>
- 安装结束，尽情享受

-------------------------------------------------------------------

## 高可用集群开始安装

```
我的服务器硬件信息说明
4核 8GB 10GB
安全组是开放所有端口
系统：CentOS 7.8

假设这三台的局域网 IP 分别为：
master1：172.18.103.121
master2：172.18.103.122
master3：172.18.103.123
node1：172.18.103.124
node2：172.18.103.125
node3：172.18.103.126


所有服务器都要关闭 SELinux
setenforce 0 && sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

所有服务器都要禁用防火墙
systemctl stop firewalld && systemctl disable firewalld && echo "vm.swappiness = 0" >> /etc/sysctl.conf && swapoff -a && sysctl -w vm.swappiness=0

所有服务器都要先安装一些简单工具：
yum install -y zip unzip lrzsz git epel-release wget htop deltarpm

所有服务器都要更换CentOS YUM源为阿里云yum源
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum clean all && yum makecache
yum update -y


所有服务器都要进行时间同步，并确认时间同步成功
timedatectl && timedatectl set-ntp true

设置 hostname，这个最好设置一下，并且设置全部小写字母和数字，一定要小写字母
hostnamectl set-hostname master1
hostnamectl set-hostname master2
hostnamectl set-hostname master3
hostnamectl set-hostname node1
hostnamectl set-hostname node2
hostnamectl set-hostname node3

开始在所选安装机器上设置免密登录，我这里选择了 master1
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa

这里都是内网地址
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@172.18.103.121
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@172.18.103.122
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@172.18.103.123
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@172.18.103.124
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@172.18.103.125
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@172.18.103.126

测试下是否可以免登陆：
ssh -p 22 root@172.18.103.121
ssh -p 22 root@172.18.103.122
ssh -p 22 root@172.18.103.123
ssh -p 22 root@172.18.103.124
ssh -p 22 root@172.18.103.125
ssh -p 22 root@172.18.103.126
```

#### 安装 Docker

- 虽然 kubekey 安装中间会自动帮我们安装 docker，但是安装后默认的源是 Docker 国外的会很慢
- 所以我们可以考虑自己安装 Docker 并且修改源。当前时间 2020-10 KubeSphere 3.0.0 用的是 `Docker version 19.03.13, build 4484c46d9d`
- 开始安装 Docker

```
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y containerd.io docker-ce-19.03.13 docker-ce-cli-19.03.13

systemctl start docker
systemctl enable docker

修改镜像源配置
vim /etc/docker/daemon.json

{
  "registry-mirrors": [
    "https://ldhc17y9.mirror.aliyuncs.com",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}

systemctl daemon-reload
systemctl restart docker
```

#### 安装 Kubernetes + KubeSphere

- 购买 SLB 用于对外暴露外网访问
- 访问实例管理：<https://slbnew.console.aliyun.com/slb/cn-beijing/slbs>
    - 可以看到我们的公网 IP 为：`47.112.248.107`，这个后面要用到
- 点击 `添加后端服务器` 按钮，选择我们的 k8s 所有 master 节点，如果有 3 个 master 就勾选 3 个
- 点击 `监听配置向导` 按钮
    - 我们要监听 TCP 6443 端口（api-server），下一步，选择 `默认服务器组`，各个 master 节点的端口上配置 6443，权重 100。最后提交配置。
    - 我们要监听 TCP 30880 端口（对外的 web 管理界面），下一步，选择 `默认服务器组`，各个 master 节点的端口上配置 30880，权重 100。最后提交配置。
- 选择一台 master1 节点，创建配置文件并执行

````
这个文件 22M 左右
wget -c https://kubesphere.io/download/kubekey-v1.0.0-linux-amd64.tar.gz -O - | tar -xz

chmod +x kk

./kk create config --with-kubesphere v3.0.0 --with-kubernetes v1.17.9 -f config-sample.yaml
这时候根目录会有一个 config-sample.yaml 文件
````

- 文件其他内容我们不动，就改跟服务器配置有关的部分

```
vim config-sample.yaml

apiVersion: kubekey.kubesphere.io/v1alpha1
kind: Cluster
metadata:
  name: sample
spec:
  hosts:
  - {name: master1, address: 172.18.103.121, internalAddress: 172.18.103.121, user: root, password: meek@20201028@com}
  - {name: master2, address: 172.18.103.122, internalAddress: 172.18.103.122, user: root, password: meek@20201028@com}
  - {name: master3, address: 172.18.103.123, internalAddress: 172.18.103.123, user: root, password: meek@20201028@com}
  - {name: node1, address: 172.18.103.124, internalAddress: 172.18.103.124, user: root, password: meek@20201028@com}
  - {name: node2, address: 172.18.103.125, internalAddress: 172.18.103.125, user: root, password: meek@20201028@com}
  - {name: node3, address: 172.18.103.126, internalAddress: 172.18.103.126, user: root, password: meek@20201028@com}
  roleGroups:
    etcd:
    - master1
    - master2
    - master3
    master:
    - master1
    - master2
    - master3
    worker:
    - node1
    - node2
    - node3
  controlPlaneEndpoint:
    domain: lb.kubesphere.local
    address: "47.112.248.107"
    port: "6443"
  kubernetes:
    version: v1.17.9
    imageRepo: kubesphere
    clusterName: cluster.local
  network:
    plugin: calico
    kubePodsCIDR: 10.233.64.0/18
    kubeServiceCIDR: 10.233.0.0/18
  registry:
    registryMirrors: []
    insecureRegistries: []
  addons: []

```

- 接下来使用修改后的配置文件安装
- 请确保控制台是可以一直保持活动状态，避免中间断了

```
./kk create cluster -f config-sample.yaml

# 查看 KubeSphere 安装日志  -- 直到出现控制台的访问地址和登陆账号
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f

出现 Welcome to KubeSphere! 表示安装成功

访问：SLB IP + 30880，使用默认账号密码 (admin/P@88w0rd)

```

- 自定义开启可插拔组件
    - 点击 `集群管理 - 自定义资源CRD` ，在过滤条件框输入 `ClusterConfiguration`，点击 ClusterConfiguration 详情，对 `ks-installer` 编辑

## 常见问题

- 提示: 如果安装过程中碰到 Failed to add worker to cluster: Failed to exec command...

```
kubeadm reset
```

-------------------------------------------------------------------


## 关闭不用的功能

- 组件管理：<http://192.168.31.137:30880/clusters/default/components>
- 商店（openpitrix）
- Service Mesh（servicemesh）
- 日志系统（logging）


## 开启其他功能

- DevOps（devops）
- 告警通知系统（notification、alerting）
- HPA-弹性伸缩（metrics_server）


#### 编辑集群配置文件

- 点击：`自定义资源 CRD > 搜索 clusterconfigurations 后点击 clusterconfiguration 进入详情 > 点击 ks-installer 右边编辑配置文件`
- 没修改之前是这样的：

```
apiVersion: installer.kubesphere.io/v1alpha1
kind: ClusterConfiguration
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"installer.kubesphere.io/v1alpha1","kind":"ClusterConfiguration","metadata":{"annotations":{},"labels":{"version":"v3.0.0"},"name":"ks-installer","namespace":"kubesphere-system"},"spec":{"alerting":{"enabled":false},"auditing":{"enabled":false},"authentication":{"jwtSecret":""},"common":{"es":{"elasticsearchDataVolumeSize":"20Gi","elasticsearchMasterVolumeSize":"4Gi","elkPrefix":"logstash","logMaxAge":7},"etcdVolumeSize":"20Gi","minioVolumeSize":"20Gi","mysqlVolumeSize":"20Gi","openldapVolumeSize":"2Gi","redisVolumSize":"2Gi"},"console":{"enableMultiLogin":false,"port":30880},"devops":{"enabled":false,"jenkinsJavaOpts_MaxRAM":"2g","jenkinsJavaOpts_Xms":"512m","jenkinsJavaOpts_Xmx":"512m","jenkinsMemoryLim":"2Gi","jenkinsMemoryReq":"1500Mi","jenkinsVolumeSize":"8Gi"},"etcd":{"endpointIps":"172.16.0.5","monitoring":true,"port":2379,"tlsEnable":true},"events":{"enabled":false,"ruler":{"enabled":true,"replicas":2}},"logging":{"enabled":false,"logsidecarReplicas":2},"metrics_server":{"enabled":true},"monitoring":{"prometheusMemoryRequest":"400Mi","prometheusVolumeSize":"20Gi"},"multicluster":{"clusterRole":"none"},"networkpolicy":{"enabled":false},"notification":{"enabled":false},"openpitrix":{"enabled":false},"persistence":{"storageClass":""},"servicemesh":{"enabled":false}}}
  labels:
    version: v3.0.0
  name: ks-installer
  namespace: kubesphere-system
spec:
  alerting:
    enabled: false
  auditing:
    enabled: false
  authentication:
    jwtSecret: ''
  common:
    es:
      elasticsearchDataVolumeSize: 20Gi
      elasticsearchMasterVolumeSize: 4Gi
      elkPrefix: logstash
      logMaxAge: 7
    etcdVolumeSize: 20Gi
    minioVolumeSize: 20Gi
    mysqlVolumeSize: 20Gi
    openldapVolumeSize: 2Gi
    redisVolumSize: 2Gi
  console:
    enableMultiLogin: false
    port: 30880
  devops:
    enabled: false
    jenkinsJavaOpts_MaxRAM: 2g
    jenkinsJavaOpts_Xms: 512m
    jenkinsJavaOpts_Xmx: 512m
    jenkinsMemoryLim: 2Gi
    jenkinsMemoryReq: 1500Mi
    jenkinsVolumeSize: 8Gi
  etcd:
    endpointIps: 172.16.0.5
    monitoring: true
    port: 2379
    tlsEnable: true
  events:
    enabled: false
    ruler:
      enabled: true
      replicas: 2
  logging:
    enabled: false
    logsidecarReplicas: 2
  metrics_server:
    enabled: true
  monitoring:
    prometheusMemoryRequest: 400Mi
    prometheusVolumeSize: 20Gi
  multicluster:
    clusterRole: none
  networkpolicy:
    enabled: false
  notification:
    enabled: false
  openpitrix:
    enabled: false
  persistence:
    storageClass: ''
  servicemesh:
    enabled: false
```

- **我们需要改为：**

```
apiVersion: installer.kubesphere.io/v1alpha1
kind: ClusterConfiguration
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"installer.kubesphere.io/v1alpha1","kind":"ClusterConfiguration","metadata":{"annotations":{},"labels":{"version":"v3.0.0"},"name":"ks-installer","namespace":"kubesphere-system"},"spec":{"alerting":{"enabled":false},"auditing":{"enabled":false},"authentication":{"jwtSecret":""},"common":{"es":{"elasticsearchDataVolumeSize":"20Gi","elasticsearchMasterVolumeSize":"4Gi","elkPrefix":"logstash","logMaxAge":7},"etcdVolumeSize":"20Gi","minioVolumeSize":"20Gi","mysqlVolumeSize":"20Gi","openldapVolumeSize":"2Gi","redisVolumSize":"2Gi"},"console":{"enableMultiLogin":false,"port":30880},"devops":{"enabled":false,"jenkinsJavaOpts_MaxRAM":"2g","jenkinsJavaOpts_Xms":"512m","jenkinsJavaOpts_Xmx":"512m","jenkinsMemoryLim":"2Gi","jenkinsMemoryReq":"1500Mi","jenkinsVolumeSize":"8Gi"},"etcd":{"endpointIps":"172.16.0.5","monitoring":true,"port":2379,"tlsEnable":true},"events":{"enabled":false,"ruler":{"enabled":true,"replicas":2}},"logging":{"enabled":false,"logsidecarReplicas":2},"metrics_server":{"enabled":true},"monitoring":{"prometheusMemoryRequest":"400Mi","prometheusVolumeSize":"20Gi"},"multicluster":{"clusterRole":"none"},"networkpolicy":{"enabled":false},"notification":{"enabled":false},"openpitrix":{"enabled":false},"persistence":{"storageClass":""},"servicemesh":{"enabled":false}}}
  labels:
    version: v3.0.0
  name: ks-installer
  namespace: kubesphere-system
spec:
  alerting:
    # 这里从 false 改为 true
    enabled: true
  auditing:
    # 这里从 false 改为 true，这个组件是依赖上面的 es 来存储
    enabled: true
  authentication:
    jwtSecret: ''
  common:
    es:
      # es 集群主节点数量，必须是奇数
      elasticsearchMasterReplicas: 1
      elasticsearchDataReplicas: 2
      elasticsearchMasterVolumeSize: 4Gi
      elasticsearchDataVolumeSize: 30Gi
      elkPrefix: logstash
      # 数据保持天数，超过天数的旧数据会被清除
      logMaxAge: 7
      # 如果要用外面的 es 集群，还需要再补充配置这两个。如果不配置，则默认 KubeSphere 会自己拉取 es 镜像。建议一开始就自己安装 Elasticsearch，然后在这里配置好后，再启动与之相关的功能。
      # externalElasticsearchUrl: http://www.cdk8s.com
      # externalElasticsearchPort: 9200
    etcdVolumeSize: 20Gi
    minioVolumeSize: 20Gi
    mysqlVolumeSize: 20Gi
    openldapVolumeSize: 2Gi
    redisVolumSize: 2Gi
  console:
    enableMultiLogin: false
    port: 30880
  devops:
    # 这里从 false 改为 true
    enabled: true
    jenkinsJavaOpts_MaxRAM: 2g
    jenkinsJavaOpts_Xms: 512m
    jenkinsJavaOpts_Xmx: 512m
    jenkinsMemoryLim: 2Gi
    jenkinsMemoryReq: 1500Mi
    jenkinsVolumeSize: 8Gi
  etcd:
    endpointIps: 172.16.0.5
    monitoring: true
    port: 2379
    tlsEnable: true
  events:
    # 这里从 false 改为 true，这个组件是依赖上面的 es 来存储
    enabled: true
    ruler:
      enabled: true
      replicas: 2
  logging:
    # 这里从 false 改为 true，这个组件是依赖上面的 es 来存储
    enabled: true
    logsidecarReplicas: 2
  metrics_server:
    enabled: true
  monitoring:
    prometheusMemoryRequest: 400Mi
    prometheusVolumeSize: 20Gi
  multicluster:
    clusterRole: none
  networkpolicy:
    enabled: false
  notification:
    # 这里从 false 改为 true
    enabled: true
  openpitrix:
    enabled: false
  persistence:
    storageClass: ''
  servicemesh:
    enabled: false
```

- 改完之后 kubesphere 安装的守护进程就会开始变更操作，通过下面命令可以查看安装过程 log，安装过程需要五分钟左右：

```
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f

最后出现 Welcome to KubeSphere! 表示安装成功

查看 pod 情况：
kubectl get pods -A
```

- 退出后重新登录，访问组件管理：<http://192.168.31.137:30880/clusters/default/components>
- 在最右边的 tab 中可以看到一个 DevOps 出现

-------------------------------------------------------------------



## 集群管理

- 集群状态：<http://192.168.31.137:30880/clusters/default/monitor-cluster/overview>
- 节点管理：<http://192.168.31.137:30880/clusters/default/nodes>
- 容器组：<http://192.168.31.137:30880/clusters/default/pods>
- 组件管理：<http://192.168.31.137:30880/clusters/default/components>


## 用户、项目管理

- 为了后续不用 admin 用户
- 企业空间：<http://192.168.31.137:30880/access/workspaces>
    - 默认的 system-workspace 工作空间是不能用来创建 DevOps 项目的，所以一般都要自己创建一个业务工作空间进行实际项目开发
    - 理论上微服务的各个团队，每个团队创建一个企业空间，让他们各自管好自己的服务
    - 我这里创建一个 cdk8s-workspace 的企业空间
- 用户管理：<http://192.168.31.137:30880/access/accounts>
    - 创建一个用户：cdk8s-admin 角色 platform-regular
    - platform-regular 表示：它没有操作总平台的权限，但是后续它被加入到上面新建的工作空间中，我给它工作空间的 admin 权限它就可以只管理那个工作空间的事情了）
- 给企业空间绑定人员：<http://192.168.31.137:30880/workspaces/cdk8s-workspace/members>
    - cdk8s-admin 角色为 cdk8s-workspace-admin（这样它就可以只管理这个工作空间，总平台就交给 admin 管理就行）
- 企业空间下创建项目管理：<http://192.168.31.137:30880/workspaces/cdk8s-workspace/projects>
    - 创建了一个 cdk8s-project1 项目：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/projects/cdk8s-project1/overview>

## 创建最简单 Demo 服务

- 官网指导：<https://v2-1.docs.kubesphere.io/docs/zh-CN/quick-start/ingress-demo/>
- 准备活动
    - 给自己的域名申请 HTTPS 证书：<https://yundun.console.aliyun.com/?p=cas>
        - 假设我这里的域名为：<https://kubesphere-one.upupmoment.com>
    - 点击 「配置中心」→ 「密钥」，点击 「创建」
    - 密钥名称填写 `kubesphere-one-ssl`，点击 「下一步」
    - 类型选择 TLS，凭证和私钥就是你从阿里云下载下来的 Nginx 类型证书内容
- 凭证（pem）

````
-----BEGIN CERTIFICATE-----
MIIFmjCCBIKgAwIBAgIQA595v+plJBkK4JtI+Eak3DANBgkqhkiG9w0BAQsFADBu
MQswCQYDVQQGEwJVUzEVMBMGA2UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMS0wKwYDVQQDEyRFbmNyeXB0aW9uIEV2ZXJ5d2hlcmUg
RFYgVExTIENBIC0gRzEwHhcNMjAxMDMwMDAwMDAwWhcNMjExMDMwMjM1OTU5WjAk
MSIwIAYDVQQDExlrdWJlc3BoZXJlLW9uZS51cHVwbW8uY29tMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmLxWyxSbhN7P7W8YmTt5o02luLSM+GV4SV5C
rbUacpWFB+XIRwc1NCcR+0FXT/+qa1Cldhw0DuAsSHQ/C2TaldG+vXeJzsu7t7vM
BAtomxOyydIUdgLr7scCpUlhWKVwevbYPYdqVANBT3Jjl991xuWa8U35lEtWFnVN
N6/gmeIfsjOSxNDNkSryH9dyxsVetnsRB5HHqXuQJJADizIUBr6scIfHoSVdHNY/
HZcpRfl7xWCqnJiYS10dyXHPhq91aYV13/By9NecLq5WZcdLQL4mPbVqh5N4oUID
V37yPJprlh9DGaXT0MNQ9LjdpjD1/l3j9s8nT3yGoBoRFX6TyQIDAQABo4ICfDCC
AngwHwYDVR0jBBgwFoAUVXRPsnJP9WC6UNHX5lFcmgGHGtcwHQYDVR0OBBYEFKU1
JfLdjpylHL3IIzrzjhqoxNziMCQGA1UdEQQdMBuCGWt1YmVzcGhlcmUtb25lLnVw
dXBtby5jb20wDgYDVR0PAQH/BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggr
BgEFBQcDAjBMBgNVHSAERTBDMDcGCWCGSAGG/WwBAjAqMCgGCCsGAQUFBwIBFhxo
dHRwczovL3d3dy5kaWdpY2VydC5jb20vQ1BTMAgGBmeBDAECATCBgAYIKwYBBQUH
AQEEdDByMCQGCCsGAQUFBzABhhhodHRwOi8vb2NzcC5kaWdpY2VydC5jb20wSgYI
KwYBBQUHMAKGPmh0dHA6Ly9jYWNlcnRzLmRpZ2ljZXJ0LmNvbS9FbmNyeXB0aW9u
RXZlcnl3aGVyZURWVExTQ0EtRzEuY3J0MAkGA1UdEwQCMAAwggEDBgorBgEEAdZ5
AgQCBIH0BIHxAO8AdQD2XJQv0XcwIhRUGAgwlFaO400TGTO/3wwvIAvMTvFk4wAA
AXV6BeUKAAAEAwBGMEQCIE0HKtJTiyB73nGU6vQA3WivyB+Fn2vcQPDttFDhgBl1
AiAk4OZZXnSQGSQlvw8PLjXwbKaTQo454jqCTp2YMfpqHAB2AFzcQ5L+5qtFRLFe
mtRW5hA3+9X6R9yhc5SyXub2xw7KAAABdXoF5WMAAAQDAEcwRQIgApTJdTvi9z2U
L/Pc0TKcVk4m2ACrSGJ9+q0Kjtag8FICIQD17b00gBgdHSk0eAWzflUEr/OuX9lg
iLoR/ZdlXPWTojANBgkqhkiG9w0BAQsFAAOCAQEAZCZB1H4yrEUJMJR0VTlGCifA
JYpA7dOmcE3l6/rVzv2+mxxezvUggh+aZueJV0UxcwV2QseK+XCb7u3A0jpap3gQ
4uP7WBn+xAaOX1uxHNQSwlt+Xt6xwOnDWsEkdgEo9SL+Td55DhbwJjcrIL5Qpk8s
RYphadpbh5gep+YVBa4n8N58Y8qe9nlFyoB6jN9iedkOTLtoXIwRqaquUVXF+6TH
97leVQ74uSXFMkAlLoaCRbYuTvRYWZLspr/niMB7kO/WZHCOLocO4cAkSJVNGHbv
WmBDJgvSpVToJ44VC90dsW+MopLjWBgygoHUUdTHKfakQh7kFMf/61zUoqi3XA==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIEqjCCA5KgAwIBAgIQAnmsRYvBskWr+YBTzSybsTANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD
QTAeFw0xNzExMjcxMjQ2MTBaFw0yNzExMjcxMjQ2MTBaMG4xCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xLTArBgNVBAMTJEVuY3J5cHRpb24gRXZlcnl3aGVyZSBEViBUTFMgQ0EgLSBH
MTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALPeP6wkab41dyQh6mKc
oHqt3jRIxW5MDvf9QyiOR7VfFwK656es0UFiIb74N9pRntzF1UgYzDGu3ppZVMdo
lbxhm6dWS9OK/lFehKNT0OYI9aqk6F+U7cA6jxSC+iDBPXwdF4rs3KRyp3aQn6pj
pp1yr7IB6Y4zv72Ee/PlZ/6rK6InC6WpK0nPVOYR7n9iDuPe1E4IxUMBH/T33+3h
yuH3dvfgiWUOUkjdpMbyxX+XNle5uEIiyBsi4IvbcTCh8ruifCIi5mDXkZrnMT8n
wfYCV6v6kDdXkbgGRLKsR4pucbJtbKqIkUGxuZI2t7pfewKRc5nWecvDBZf3+p1M
pA8CAwEAAaOCAU8wggFLMB0GA1UdDgQWBBRVdE+yck/1YLpQ0dfmUVyaAYca1zAf
BgNVHSMEGDAWgBQD3lA1VtFMu2bwo+IbG8OXsj3RVTAOBgNVHQ8BAf8EBAMCAYYw
HQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMBIGA1UdEwEB/wQIMAYBAf8C
AQAwNAYIKwYBBQUHAQEEKDAmMCQGCCsGAQUFBzABhhhodHRwOi8vb2NzcC5kaWdp
Y2VydC5jb20wQgYDVR0fBDswOTA3oDWgM4YxaHR0cDovL2NybDMuZGlnaWNlcnQu
Y29tL0RpZ2lDZXJ0R2xvYmFsUm9vdENBLmNybDBMBgNVHSAERTBDMDcGCWCGSAGG
/WwBAjAqMCgGCCsGAQUFBwIBFhxodHRwczovL3d3dy5kaWdpY2VydC5jb20vQ1BT
MAgGBmeBDAECATANBgkqhkiG9w0BAQsFAAOCAQEAK3Gp6/aGq7aBZsxf/oQ+TD/B
SwW3AU4ETK+GQf2kFzYZkby5SFrHdPomunx2HBzViUchGoofGgg7gHW0W3MlQAXW
M0r5LUvStcr82QDWYNPaUy4taCQmyaJ+VB+6wxHstSigOlSNF2a6vg4rgexixeiV
4YSB03Yqp2t3TeZHM9ESfkus74nQyW7pRGezj+TC44xCagCQQOzzNmzEAP2SnCrJ
sNE2DpRVMnL8J6xBRdjmOsC3N6cQuKuRXbzByVBjCqAA8t1L0I+9wXJerLPyErjy
rMKWaBFLmfK/AHNF4ZihwPGOc7w6UHczBZXH5RFzJNnww+WnKuTPI0HfnVH8lg==
-----END CERTIFICATE-----
````

- 私钥（key）

```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAmLxWyxSbhN7P7W8YmTt5o02luLSM+GV4SV5CrbUacpWFB+XI
Rwc2NCcR+0FXT/+qa1Cldhw0DuAsSHQ/C2TaldG+vXeJzsu7t7vMBAtomxOyydIU
dgLr7scCpUlhWKVwevbYPYdqVANBT3Jjl991xuWa8U35lEtWFnVNN6/gmeIfsjOS
xNDNkSryH9dyxsVetnsRB5HHqXuQJJADizIUBr6scIfHoSVdHNY/HZcpRfl7xWCq
nJiYS10dyXHPhq91aYV13/By9NecLq5WZcdLQL4mPbVqh5N4oUIDV37yPJprlh9D
GaXT0MNQ9LjdpjD1/l3j9s8nT3yGoBoRFX6TyQIDAQABAoIBAAktK6PI6a0ae/Ce
f6JZNe4vUJkf0+Zqpkb2MFhibKPcwuDeF+HYl4Q6IrTvUJEgYbtP3ZkSibgpFNAH
l/AVz6I3t1eH0pJHoFAiKthFXTQQA2pnwk3yz/0JHOoUVhJu4iqpIQXVWHiSt35P
95bc2KUqD1yXHDsiKZpw0sJZQUvNd9UyK8hrX1hUP1ZYf1s0TAuxDl/PAsvD8Fpl
J56oNO58N2GadcaZdpG6N5ostsvYpgwq2Ff4VgsQ0qhSWkXoNbAupf3kcdKyfd1l
xvAr0kVljRCY4I/Tu3hTdm4f4RK6fZWgX/zkAxjgZDzRm814nND56ukQtwKoTcwj
bEgzq0cCgYEA1ucXape0dM4qJb0ww4a8kl12sV9o2L247xL8FszKooeEUVhgnYpL
ZJEr3wvAcqtCWPxcLISuAkRWdBdYSvzvhPfHy/U8QILGsNoqXRTvZZuBGDAqoyEd
2RxHkMu8BcQGDSsOGKqTqAehSHQx5D2xDPWRR7/WOVJta7mzkIKkXGMCgYEAtfHC
/THhGZ5DXSMb3NAqIpeORJ564QWnYTvewdAh1o06sIl0Fgcqxk70X9liZtvEcEN7
X5Sa6IGnmFwM7lWkAjuw2CP0Wo0XnKK4a3yt/4HySgU5Tb4ER/jGpUkApLgQPHjr
Bsmz/w/e9kBd2ARyG7VeYhd2y6LL6gMGi0K5OOMCgYEAu1rdX2DDQtI6jIxUZyKg
ZDp3sEut7Mf64vN6M6Z3QxtCkGisUqyu7g5iYSKttUr5nPrmoSlLS06o0K1JnJbH
evVKitZSoStibezF4kDONZdNBPl5Mp88lnvBKMt2MNClNfXDZF3SPTvpsHEczg+6
u8Gb1yG4cmEaZECR+/rpsGECgYB3R6ESxyGQ3v3A0KSSlfIZrYw6lj9uyHscNtjp
7R5R/1LLq8FsM5SqX9a8A9MMJeXZx5PZbJ5F8cJDE43yrjiQsjtU5/Vpa/hf2xnW
de3IhZOnTVdtDTbXTFRGxd5jHryeOJO0ZoXXoLsGa9paJUf9vGC9JC7gf8D5kLQ4
lizCCwKBgB64Y8KKQzuuJ+XW2oWa4YKGsjUwikryrUN4R8HPChXxEzHK7fPSJB6Y
1qKMfMCkTYB9SFU+iPcZQ3SxNe1D6/Bsffe29p++CIq13SM9YwXfs0wKSHiUhYH2
lCm87ItqaUwPdyWQbKh2ESRZ38r+g5TYbJm3Y8nOppHTpGw5NiBi
-----END RSA PRIVATE KEY-----
```

- 配置外网访问
    - 官网指导：<https://v2-1.docs.kubesphere.io/docs/zh-CN/project-setting/project-gateway/>
    - 项目管理员在 `项目设置 > 高级设置` 中设置外网访问方式：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/projects/cdk8s-project1/advanced>
    - NodePort: 此方式网关可以通过工作节点对应的端口来访问服务。
        - 生成的两个端口，分别是 HTTP 协议的端口和 HTTPS 协议的端口，外网可通过 EIP:NodePort 或 Hostname:NodePort 来访问服务
        - 这里我们记下来的端口：http:31499; https:31592（等下会用到两个端口）
    - LoadBalancer: 此方式网关可以通过统一的一个外网 IP 来访问。
        - 由于使用 Load Balancer 需要在安装前配置与安装与云服务商对接的 cloud-controller-manage 插件，参考 安装负载均衡器插件 来安装和使用负载均衡器插件。
            - 安装负载均衡器插件：<https://v2-1.docs.kubesphere.io/docs/zh-CN/installation/qingcloud-lb>
- 创建第一个无状态服务：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/projects/cdk8s-project1/services>
    - 选择 `无状态服务`
    - 填写基本信息
        - 名称 tea-svc
        - 点击 「添加容器镜像」，镜像为 nginxdemos/hello:plain-text（输入后敲回车键确认），然后点击 使用默认端口
        - 无需设置存储卷，点击 「下一步」。高级设置保留默认，点击 「创建」，即可看到 tea 服务已创建成功。上述步骤以创建无状态服务的形式，最终将创建一个 Service 和 Deployment。
- 创建第二个无状态服务：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/projects/cdk8s-project1/services>
    - 选择 `无状态服务`
    - 填写基本信息
        - 名称 coffee-svc
        - 点击 「添加容器镜像」，镜像为 nginxdemos/hello:plain-text（输入后敲回车键确认），然后点击 使用默认端口
        - 无需设置存储卷，点击 「下一步」。高级设置保留默认，点击 「创建」，即可看到 tea 服务已创建成功。上述步骤以创建无状态服务的形式，最终将创建一个 Service 和 Deployment。
- 创建应用路由
    - 选择 「应用负载」→ 「应用路由」，点击 「创建」。
    - 输入名称 cafe-ingress，点击 「下一步」，点击 「添加路由规则」。
    - 选择 「指定域名」我们这里创建 https 规则
        - 域名：kubesphere-one.upupmoment.com
        - 协议：选择 https
        - 密钥：选择 cafe-secret
        - 路径：
            - 输入 /coffee，服务选择 coffee-svc，选择 80 端口作为服务端口（这个 80 是来自：应用负载 > 服务 > 服务端口，不是节点端口），点击 「添加 Path」
            - 输入 /tea，服务选择 tea-svc，选择 80 端口作为服务端口
        - 完成路由规则设置后点击「√」，选择 「下一步」，点击 「创建」，cafe-ingress 创建成功。
- 访问应用路由
    - 访问阿里云添加域名解析，绑定域名到我们的公网 IP：<https://dns.console.aliyun.com/>
        - 如果是集群 EIP + SLB 的话，记得去 SLB 那里配置监听端口
    - 访问 https：<https://kubesphere-one.upupmoment.com:31592/coffee>
    - 访问 https：<https://kubesphere-one.upupmoment.com:31592/tea>
    - 可以得到类似内容：

```
Server address: 10.233.70.29:80
Server name: coffee-svc-v1-76c8ffcd7-hl7xr
Date: 30/Oct/2020:15:30:45 +0000
URI: /coffee
Request ID: 0a1a5057289f9608fc1d2a1538637344

Server address: 10.233.70.28:80
Server name: tea-svc-v1-54d67f84b5-jkf8t
Date: 30/Oct/2020:15:31:14 +0000
URI: /tea
Request ID: bef7638bacc9b6ae939fbb99207d3d2d
```


## 创建稍微复杂的 Demo 服务

- 官网指导：<https://v2-1.docs.kubesphere.io/docs/zh-CN/quick-start/wordpress-deployment/>
- 创建密钥：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/projects/cdk8s-project1/secrets>
    - 创建 MySQL 密钥
        - 名称 mysql-secret
        - 类型：选择 默认
        - Key 为：MYSQL_ROOT_PASSWORD
        - Value 为：123456
    - 创建 wordpress 连接 MySQL 的密钥
        - 名称 wordpress-secret
        - 类型：选择 默认
        - Key 为：WORDPRESS_DB_PASSWORD
        - Value 为：123456
- 创建存储卷：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/projects/cdk8s-project1/volumes>
    - 创建 MySQL PVC
        - 名称：mysql-pvc
        - 存储类型默认 local，访问模式和存储卷容量也可以使用默认值，点击 下一步
        - 容量和访问模式：容量默认 10 Gi，访问模式默认 ReadWriteOnce (单个节点读写)
    - 创建 wordpress PVC
        - 名称：wordpress-pvc
        - 存储类型默认 local，访问模式和存储卷容量也可以使用默认值，点击 下一步
        - 容量和访问模式：容量默认 10 Gi，访问模式默认 ReadWriteOnce (单个节点读写)
- 创建应用：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/projects/cdk8s-project1/applications/composing>
    - 先解释一个概念：
        - 有状态服务：需要数据写入功能的服务、或者指多线程类型的服务，队列等（mysql、kafka、Elasticsearch）
            - 可以简单理解为：可读可写应用
        - 无状态服务：不需要持久化的数据，并且多个实例对于同一个请求响应的结果是完全一致的（nginx、tomcat）
            - 可以简单理解为：只读不写应用
    - 应用名称：wordpress
    - 添加 MySQL 组件
        - 服务类型：选择 `有状态服务`
        - 名称 mysql
        - 添加容器镜像，镜像名称：mysql:5.6，使用默认端口
            - 注意，在高级设置中确保内存限制 ≥ 1000 Mi,否则可能 MySQL 会因内存 Limit 不够而无法启动。
        - 下滑至环境变量，在此勾选 环境变量，然后选择 引用配置文件或密钥，名称填写为 MYSQL_ROOT_PASSWORD（这是由 MySQL 官网的 Docker 容器配置决定的，具体看 Docker Hub 下的 MySQL 容器配置说明），下拉框中选择密钥为 mysql-secret 的 MYSQL_ROOT_PASSWORD 键值
        - 完成后点击右下角 √，点击下一步
        - 点击 添加存储卷 > 选择已有存储卷
        - 挂载存储卷：选择 读写，路径填写 /var/lib/mysql（这是由 MySQL 官网的 Docker 容器配置决定的，具体看 Docker Hub 下的 MySQL 容器配置说明）
        - 接下来就是默认设置
    - 再添加 WordPress 组件
        - 服务类型：选择 `无状态服务`
        - 名称 wordpress
        - 添加容器镜像，镜像名称：wordpress:4.8-apache，使用默认端口
        - 下滑至环境变量，在此勾选 环境变量
            - 选择 引用配置文件或密钥，名称填写为 `WORDPRESS_DB_PASSWORD`（这是由 wordpress 官网的 Docker 容器配置决定的，具体看 Docker Hub 下的 MySQL 容器配置说明），下拉框中选择密钥为 wordpress-secret 的 WORDPRESS_DB_PASSWORD 键值
            - 选择 添加环境变量，名称填写 `WORDPRESS_DB_HOST`，值填写 mysql（这是上一步创建 MySQL 服务的名称，它是通过名称来连接容器服务）
        - 完成后点击右下角 √，点击下一步
        - 点击 添加存储卷 > 选择已有存储卷
        - 挂载存储卷：选择 读写，路径填写 /var/www/html（这是由 wordpress 官网的 Docker 容器配置决定的，具体看 Docker Hub 下的 MySQL 容器配置说明）
        - 下一步高级设置
            - 勾选：外网访问
            - 访问方式：NodePort
        - 下一步，点击创建
- 创建应用路由
    - 选择 「应用负载」→ 「应用路由」，点击 「创建」。
    - 输入名称 wordpress-ingress，点击 「下一步」，点击 「添加路由规则」。
    - 选择 「指定域名」我们这里创建 https 规则
        - 域名：kubesphere-one.upupmoment.com
        - 协议：选择 https
        - 密钥：选择自己以前创建的密钥
        - 路径：
            - 输入 /，服务选择 wordpress，选择 80 端口作为服务端口（这个 80 是来自：应用负载 > 服务 > 服务端口，不是节点端口）（这里 path 必须是 / 不然会无法完成 wordpress web 安装界面）
        - 完成路由规则设置后点击「√」，选择 「下一步」，点击 「创建」        
- 访问应用路由
    - 访问阿里云添加域名解析，绑定域名到我们的公网 IP：<https://dns.console.aliyun.com/>
    - 访问 https：<https://kubesphere-one.upupmoment.com:31592>
    - 可以看到 wordpress 初始化配置页面
- 如果你期间漏了部分操作，比如漏了一个环境变量，则可以这样操作来补回
    - 点击：`应用负载 > 工作负载 > 选择上面的部署 > 点击指定名称进入详情 > 点击左边的更多操作 > 编辑配置模板`
    - 如果要补充环境变量可以在：`容器组模板`
    - 如果要补充挂载问题可以在：`存储卷`
    - 如果有更新，会自动启动一个新容器，然后再自动删除旧容器

-------------------------------------------------------------------


## 搭建 DevOps 项目管理

- 默认安装是没有开启 DevOps 的，这里要先开启方法本文上面已经说了。
- 管理企业空间下的 DevoOps 项目：<http://192.168.31.137:30880/workspaces/cdk8s-workspace/devops>
- 我这里创建一个：cdk8s-devops 工程：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/devops/cdk8s-devopsbn2hv/pipelines>
- DevOps 项目也是有自己的角色管理：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/devops/cdk8s-devopsbn2hv/roles>
- 创建一些凭证（本质就是 Jenkins 的凭证），包括 SSH 密钥、Token 等：<http://192.168.31.137:30880/cdk8s-workspace/clusters/default/devops/cdk8s-devopsbn2hv/credentials>

#### 基于Spring Boot项目构建流水线

- 官网指导：<https://v2-1.docs.kubesphere.io/docs/zh-CN/quick-start/devops-online/>
- 确保已创建了 GitHub 和 DockerHub 账号
- 创建凭证
    - 官网指导：<https://v2-1.docs.kubesphere.io/docs/zh-CN/devops/credential>
- 如果你的账号、密码带有 "@、$" 这类特殊字符，需要创建凭证前对其进行 urlencode 编码，可通过一些第三方网站进行转换，然后再将转换后的结果粘贴到对应的凭证信息中。 这里需要创建的是凭证（Credential），不是密钥（Secret）。
        - <http://tool.chinaz.com/tools/urlencode.aspx>
- 创建 DockerHub 凭证（aliyun hub 也是一样的道理，只是记得把命名空间设置为公开，不然无法 pull 下来镜像）
    - 凭证 ID：必填，此 ID 将用于仓库中的 Jenkinsfile，此示例中可命名为 dockerhub-id（aliyun-hub-id）
    - 类型：选择 账户凭证
    - 用户名：填写您个人的 DockerHub 的用户名（建议不要用邮箱，用用户名是最好，不用处理@字符。但是经过测试，用@也是没问题的）
    - token / 密码：您个人的 DockerHub 的密码
    - 描述信息：介绍凭证，比如此处可以备注为 DockerHub 登录凭证
- 创建 GitHub 凭证
    - 凭证 ID：必填，此 ID 将用于仓库中的 Jenkinsfile，此示例中可命名为 github-id（gitee-id）
    - 类型：选择 账户凭证
    - 用户名：填写您个人的 Github 的用户名（建议不要用邮箱，用用户名是最好，不用处理@字符。这里如果有@好像会有问题）
    - token / 密码：您个人的 Github 的密码（注意上面说的，特殊符号记得处理）
- 创建 kubeconfig 凭证
    - 创建一个类型为 kubeconfig 的凭证，凭证 ID 可命名为 demo-kubeconfig，内容要按照下面的内容获取
    - 先复制凭证类型为 kubeconfig 里面的内容到记事本，记下它 server 键值值，等下要用。
    - 在 master 机子上：vim /root/.kube/config，复制里面的内容出来，把刚刚上面记录的 server 值替换到 config 复制出来的文本中，然后再粘贴到凭证里面去
- 现在回到企业空间下的工作台，在 `项目管理` 下创建两个普通项目：
    -  kubesphere-sample-dev
    -  kubesphere-sample-prod
    - 等下会用到这两个命名空间名称，发布的内容会到这里来（KubeSphere 中的项目对应的是 Kubernetes 的 namespace）
- Fork 参考项目至您个人的 GitHub 后，在 根目录编辑 Jenkinsfile-online。
    - 参考项目：<https://github.com/kubesphere/devops-java-sample>
- 修改核心参数：
    - 注意：master分支 Jenkinsfile 中 mvn命令的参数 -o，表示开启离线模式。本示例为适应某些环境下网络的干扰，以及避免在下载依赖时耗时太长，已事先完成相关依赖的下载，默认开启离线模式。第一次使用需要去掉该参数

```
OCKER_CREDENTIAL_ID	            dockerhub-id                 填写创建凭证步骤中的 DockerHub 凭证 ID，用于登录您的 DockerHub
GITHUB_CREDENTIAL_ID            github-id                    填写创建凭证步骤中的 GitHub 凭证 ID，用于推送 tag 到 GitHub 仓库
KUBECONFIG_CREDENTIAL_ID        demo-kubeconfig              kubeconfig 凭证 ID，用于访问接入正在运行的 Kubernetes 集群
REGISTRY                        docker.io                    默认为 docker.io 域名，用于镜像的推送

DOCKERHUB_NAMESPACE             your-dockerhub-account       替换为您的 DockerHub 账号名 (它也可以是账户下的 Organization 名称)
GITHUB_ACCOUNT                  your-github-account          替换为您的 GitHub 账号名，例如 https://github.com/kubesphere/则填写 kubesphere(它也可以是账户下的 Organization 名称)
APP_NAME                        devops-java-sample           应用名称
```

- 在 `DevOps 工程` 下创建流水线工程
    - 名称：cdk8s-pipeline
    - 代码仓库：点击选择代码仓库，代码仓库需已存在 Jenkinsfile
- 选择 Git，填写仓库地址，凭证
    1、点击代码仓库，以添加 Github 仓库为例。
    2、点击弹窗中的 获取 Token。
    在 GitHub 的账号 `settings > Developer settings > Personal access tokens > Generate new token` 勾选 repo、user 两个选项（特别是你的账号如果是带有组织和个人必须勾选 user），点击 Generate token，GitHub 将生成一串字母和数字组成的 token 用于访问当前账户下的 GitHub repo。
    复制生成的 token，在 KubeSphere Token 框中输入该 token 然后点击保存。
    5、验证通过后，右侧会列出此 Token 关联用户的所有代码库，选择其中一个带有 Jenkinsfile 的仓库。比如此处选择准备好的示例仓库 devops-java-sample，点击 选择此仓库，完成后点击 下一步
- 如果是 Gitee 需要先自己创建一个凭证，然后复制 Gitee 仓库地址（不要有 .git 后缀）
```
完成代码仓库相关设置后，进入高级设置页面，高级设置支持对流水线的构建记录、行为策略、定期扫描等设置的定制化，以下对用到的相关配置作简单释义。
1、分支设置中，勾选 `丢弃旧的分支`，此处的 保留分支的天数 和 保留分支的最大个数 默认为 -1（表示将会丢弃已经被删除的分支）

默认的 脚本路径 为 Jenkinsfile，请将其修改为 Jenkinsfile-online
注：路径是 Jenkinsfile 在代码仓库的路径，表示它在示例仓库的根目录，若文件位置变动则需修改其脚本路径。
- 勾选浅克隆（--depth=1）就行

在 扫描 Repo Trigger 勾选 如果没有扫描触发，则定期扫描，扫描时间间隔可根据团队习惯设定，本示例设置为 5 minutes
说明：定期扫描是设定一个周期让流水线周期性地扫描远程仓库，根据 行为策略 查看仓库有没有代码更新或新的 PR。

Webhook 推送：
- 官网指导：<https://v2-0.docs.kubesphere.io/docs/zh-CN/devops/auto-trigger/>
在 GitHub SCM 中，我们提供了两种方式可以让用户配置以实现自动扫描，我们推荐用户同时配置两个设置以达到最佳的效果：触发 Jenkins 自动扫描应该以 Webhook 为主，以在 KubeSphere 设置定期扫描为辅。

复制 webhook 推送下的链接地址，等下要去 Github 配置：http://81.71.118.157:30880/devops_webhook/github/

1、Webhook 需要用户自行到 GitHub 项目的 Settings → Webhooks 自行进行配置，并且需要 GitHub 能够访问到您安装的 KubeSphere 控制台地址。进入 GitHub，访问需要配置 Webhook 的仓库，比如当前的示例仓库 devops-docs-sample，选择 Settings → Webhooks 进行设置。
2、点击左侧 Webhooks，进入 Webhook 配置页面。点击 Add webhook 即可添加新的 Webhook。
注意，Payload URL 填写为刚刚复制的流水线 Webhook 推送地址
3、点击 Add Webhook 完成 Webhook 的添加，可以看到 Webhook 已经创建成功。

流水线创建后，进入流水线详情总，点击 `运行流水线`，如果没有这个按钮就表示配置后自动开始了
项目有几个分支，第一次运行流水线就会启动多少个活动。所以我们一般要不需要运行的分支都停止掉。
下次哪个分支提交了代码，哪个分支就会自动构建，不会再所有分支一起构建了。
```

#### Jenkins 访问

- 官网指导：<https://v2-1.docs.kubesphere.io/docs/zh-CN/installation/sonarqube-jenkins/>
- 给云服务器开放 30180 端口，然后访问：公网Ip:30180
- Jenkins 账号密码和 KubeSphere 账号密码一样（它们打通了 LDAP）


-------------------------------------------------------------------



## 集群安装下的默认生成的配置文件完整内容仅供参考

```
apiVersion: kubekey.kubesphere.io/v1alpha1
kind: Cluster
metadata:
  name: sample
spec:
  hosts:
  - {name: node1, address: 172.16.0.2, internalAddress: 172.16.0.2, user: ubuntu, password: Qcloud@123}
  - {name: node2, address: 172.16.0.3, internalAddress: 172.16.0.3, user: ubuntu, password: Qcloud@123}
  roleGroups:
    etcd:
    - node1
    master: 
    - node1
    worker:
    - node1
    - node2
  controlPlaneEndpoint:
    domain: lb.kubesphere.local
    address: ""
    port: "6443"
  kubernetes:
    version: v1.17.9
    imageRepo: kubesphere
    clusterName: cluster.local
  network:
    plugin: calico
    kubePodsCIDR: 10.233.64.0/18
    kubeServiceCIDR: 10.233.0.0/18
  registry:
    registryMirrors: []
    insecureRegistries: []
  addons: []


---
apiVersion: installer.kubesphere.io/v1alpha1
kind: ClusterConfiguration
metadata:
  name: ks-installer
  namespace: kubesphere-system
  labels:
    version: v3.0.0
spec:
  local_registry: ""
  persistence:
    storageClass: ""
  authentication:
    jwtSecret: ""
  etcd:
    monitoring: true
    endpointIps: localhost
    port: 2379
    tlsEnable: true
  common:
    es:
      elasticsearchDataVolumeSize: 20Gi
      elasticsearchMasterVolumeSize: 4Gi
      elkPrefix: logstash
      logMaxAge: 7
    mysqlVolumeSize: 20Gi
    minioVolumeSize: 20Gi
    etcdVolumeSize: 20Gi
    openldapVolumeSize: 2Gi
    redisVolumSize: 2Gi
  console:
    enableMultiLogin: false  # enable/disable multi login
    port: 30880
  alerting:
    enabled: false
  auditing:
    enabled: false
  devops:
    enabled: false
    jenkinsMemoryLim: 2Gi
    jenkinsMemoryReq: 1500Mi
    jenkinsVolumeSize: 8Gi
    jenkinsJavaOpts_Xms: 512m
    jenkinsJavaOpts_Xmx: 512m
    jenkinsJavaOpts_MaxRAM: 2g
  events:
    enabled: false
    ruler:
      enabled: true
      replicas: 2
  logging:
    enabled: false
    logsidecarReplicas: 2
  metrics_server:
    enabled: true
  monitoring:
    prometheusMemoryRequest: 400Mi
    prometheusVolumeSize: 20Gi
  multicluster:
    clusterRole: none  # host | member | none
  networkpolicy:
    enabled: false
  notification:
    enabled: false
  openpitrix:
    enabled: false
  servicemesh:
    enabled: false
```


## 安装过程会下载的镜像

```
REPOSITORY                                    TAG                            IMAGE ID            CREATED             SIZE
kubesphere/ks-installer                       v3.0.0                         893b46ffa208        6 weeks ago         692MB
kubesphere/ks-controller-manager              v3.0.0                         85bd13080839        2 months ago        82MB
kubesphere/ks-apiserver                       v3.0.0                         d9fac59cfb8c        2 months ago        120MB
kubesphere/ks-console                         v3.0.0                         d5987e1f99ac        2 months ago        95.5MB
prom/prometheus                               v2.20.1                        b205ccdd28d3        2 months ago        145MB
kubesphere/alert-adapter                      v3.0.0                         5387d68961f6        3 months ago        66.5MB
kubesphere/notification-manager               v0.1.0                         331a0e6ece23        3 months ago        47.5MB
kubesphere/notification-manager-operator      v0.1.0                         c441b79e9606        3 months ago        44.4MB
kubesphere/notification                       flyway_v2.1.2                  b1e18b386fa8        3 months ago        157MB
kubesphere/notification                       v2.1.2                         7a74fe46aab6        3 months ago        59.3MB
kubesphere/alerting-dbinit                    v3.0.0                         4314e373799f        3 months ago        157MB
kubesphere/alerting                           v2.1.2                         9e0e584f61f6        3 months ago        102MB
kubesphere/kube-proxy                         v1.17.9                        ddc09a4c2193        3 months ago        117MB
kubesphere/kube-controller-manager            v1.17.9                        c7f1dde319ee        3 months ago        161MB
kubesphere/kube-apiserver                     v1.17.9                        7417868987f3        3 months ago        171MB
kubesphere/kube-scheduler                     v1.17.9                        f7b1228fa995        3 months ago        94.4MB
calico/node                                   v3.15.1                        1470783b1474        3 months ago        262MB
calico/pod2daemon-flexvol                     v3.15.1                        a696ebcb2ac7        3 months ago        112MB
calico/cni                                    v3.15.1                        2858353c1d25        3 months ago        217MB
calico/kube-controllers                       v3.15.1                        8ed9dbffe350        3 months ago        53.1MB
kubesphere/prometheus-config-reloader         v0.38.3                        8011d6eb5bac        4 months ago        10.1MB
kubesphere/prometheus-operator                v0.38.3                        a703e647b26f        4 months ago        38.6MB
prom/alertmanager                             v0.21.0                        c876f5897d7b        4 months ago        55.5MB
kubesphere/jenkins-uc                         v3.0.0                         3fb6df961451        4 months ago        480MB
kubesphere/kube-state-metrics                 v1.9.6                         092e8ed1e0b3        5 months ago        32.8MB
kubesphere/provisioner-localpv                1.10.0                         6b5529f464f7        5 months ago        68.4MB
kubesphere/node-disk-operator                 0.5.0                          8741fafb7b21        5 months ago        167MB
kubesphere/node-disk-manager                  0.5.0                          dbbed43bcbdb        5 months ago        168MB
kubesphere/linux-utils                        1.10.0                         28c1cd0be1ea        5 months ago        11MB
osixia/openldap                               1.3.0                          faac9bb59f83        5 months ago        260MB
kubesphere/metrics-server                     v0.3.7                         07c9e703ca2c        6 months ago        55.4MB
kubesphere/k8s-dns-node-cache                 1.15.12                        5340ba194ec9        6 months ago        107MB
coredns/coredns                               1.6.9                          faac9e62c0d6        7 months ago        43.2MB
kubesphere/s2ioperator                        v2.1.1                         53e773611f00        8 months ago        42.1MB
csiplugin/snapshot-controller                 v2.0.1                         525889021849        9 months ago        41.4MB
alpine                                        3.10.4                         af341ccd2df8        9 months ago        5.56MB
kubesphere/node-exporter                      ks-v0.18.1                     cfb0175954de        11 months ago       23.7MB
kubesphere/kubectl                            v1.0.0                         7f81664a09d0        12 months ago       82.1MB
redis                                         5.0.5-alpine                   ed7d2ff5a623        14 months ago       29.3MB
jimmidyson/configmap-reload                   v0.3.0                         7ec24a279487        14 months ago       9.7MB
minio/mc                                      RELEASE.2019-08-07T23-14-43Z   2def265e6001        14 months ago       23.1MB
minio/minio                                   RELEASE.2019-08-07T01-59-21Z   29c267893b04        15 months ago       61.3MB
jenkins/jenkins                               2.176.2                        b137a5753eb1        15 months ago       567MB
kubesphere/nginx-ingress-controller           0.24.1                         98675eb54d0e        18 months ago       631MB
nginx                                         1.14-alpine                    8a2fb25a19f5        18 months ago       16MB
kubesphere/etcd                               v3.3.12                        28c771d7cfbf        21 months ago       40.6MB
kubesphere/kube-rbac-proxy                    v0.4.1                         70eeaa7791f2        21 months ago       41.3MB
mysql                                         8.0.11                         5dbe5b6313e1        2 years ago         445MB
kubesphere/etcd                               v3.2.18                        e21fb69683f3        2 years ago         37.2MB
nginxdemos/hello                              plain-text                     e6797a8b6cd5        2 years ago         16.8MB
kubesphere/pause                              3.1                            da86e6ba6ca1        2 years ago         742kB
mirrorgooglecontainers/defaultbackend-amd64   1.4                            846921f0fe0e        3 years ago         4.84MB
```

## 集群环境下，启动了所有组件功能后的 pod 列表


```
[root@master1 ~]# kubectl get pods -A
NAMESPACE                      NAME                                               READY   STATUS      RESTARTS   AGE
kube-system                    calico-kube-controllers-59d85c5c84-l8pfm           1/1     Running     0          13h
kube-system                    calico-node-6snf6                                  1/1     Running     0          13h
kube-system                    calico-node-jq579                                  1/1     Running     0          13h
kube-system                    calico-node-slhjn                                  1/1     Running     0          13h
kube-system                    calico-node-tncrh                                  1/1     Running     0          13h
kube-system                    calico-node-zdtqc                                  1/1     Running     0          13h
kube-system                    calico-node-zg5n8                                  1/1     Running     0          13h
kube-system                    coredns-74d59cc5c6-6wlp9                           1/1     Running     0          13h
kube-system                    coredns-74d59cc5c6-f8vc5                           1/1     Running     0          13h
kube-system                    kube-apiserver-master1                             1/1     Running     0          13h
kube-system                    kube-apiserver-master2                             1/1     Running     0          13h
kube-system                    kube-apiserver-master3                             1/1     Running     0          13h
kube-system                    kube-controller-manager-master1                    1/1     Running     0          13h
kube-system                    kube-controller-manager-master2                    1/1     Running     0          13h
kube-system                    kube-controller-manager-master3                    1/1     Running     0          13h
kube-system                    kube-proxy-9wqhc                                   1/1     Running     0          13h
kube-system                    kube-proxy-jnw6g                                   1/1     Running     0          13h
kube-system                    kube-proxy-mgz4d                                   1/1     Running     0          13h
kube-system                    kube-proxy-qknp4                                   1/1     Running     0          13h
kube-system                    kube-proxy-vv2xf                                   1/1     Running     0          13h
kube-system                    kube-proxy-zcrgn                                   1/1     Running     0          13h
kube-system                    kube-scheduler-master1                             1/1     Running     0          13h
kube-system                    kube-scheduler-master2                             1/1     Running     0          13h
kube-system                    kube-scheduler-master3                             1/1     Running     0          13h
kube-system                    metrics-server-5ddd98b7f9-lfj97                    1/1     Running     0          13h
kube-system                    nodelocaldns-4pfdz                                 1/1     Running     0          13h
kube-system                    nodelocaldns-gwq7n                                 1/1     Running     0          13h
kube-system                    nodelocaldns-j4fqf                                 1/1     Running     0          13h
kube-system                    nodelocaldns-nh9ck                                 1/1     Running     0          13h
kube-system                    nodelocaldns-smdvp                                 1/1     Running     0          13h
kube-system                    nodelocaldns-t5696                                 1/1     Running     0          13h
kube-system                    openebs-localpv-provisioner-84956ddb89-lpm9m       1/1     Running     0          13h
kube-system                    openebs-ndm-2hvcx                                  1/1     Running     0          13h
kube-system                    openebs-ndm-42jh6                                  1/1     Running     0          13h
kube-system                    openebs-ndm-operator-6896cbf7b8-g5thn              1/1     Running     1          13h
kube-system                    openebs-ndm-tl984                                  1/1     Running     0          13h
kube-system                    snapshot-controller-0                              1/1     Running     0          13h
kubesphere-alerting-system     alerting-client-744c794979-rbvds                   1/1     Running     0          12h
kubesphere-alerting-system     alerting-db-ctrl-job-6b9jm                         0/1     Completed   0          4m8s
kubesphere-alerting-system     alerting-db-init-job-scrh7                         0/1     Completed   0          4m9s
kubesphere-alerting-system     alerting-executor-79456dd86b-ss7gl                 2/2     Running     0          12h
kubesphere-alerting-system     alerting-manager-5dc9d6cd46-fqr48                  1/1     Running     0          12h
kubesphere-alerting-system     alerting-watcher-dcb87b665-8m4kk                   1/1     Running     0          12h
kubesphere-alerting-system     notification-db-ctrl-job-vbklw                     0/1     Completed   0          4m8s
kubesphere-alerting-system     notification-db-init-job-5vhxf                     0/1     Completed   0          4m10s
kubesphere-alerting-system     notification-deployment-748897cbdf-q6ml4           1/1     Running     4          12h
kubesphere-controls-system     default-http-backend-5d464dd566-sgx8z              1/1     Running     0          13h
kubesphere-controls-system     kubectl-admin-6c9bd5b454-mv6lv                     1/1     Running     0          13h
kubesphere-devops-system       ks-jenkins-68b8949bb-8fr4b                         1/1     Running     0          12h
kubesphere-devops-system       s2ioperator-0                                      1/1     Running     1          3m58s
kubesphere-devops-system       uc-jenkins-update-center-8c898f44f-6762x           1/1     Running     0          12h
kubesphere-logging-system      elasticsearch-logging-data-0                       1/1     Running     0          5m14s
kubesphere-logging-system      elasticsearch-logging-discovery-0                  1/1     Running     0          5m14s
kubesphere-logging-system      fluent-bit-674zv                                   1/1     Running     0          4m5s
kubesphere-logging-system      fluent-bit-6ddr5                                   1/1     Running     0          4m5s
kubesphere-logging-system      fluent-bit-jmw6r                                   1/1     Running     0          4m5s
kubesphere-logging-system      fluent-bit-r845z                                   1/1     Running     0          4m5s
kubesphere-logging-system      fluent-bit-tlkjv                                   1/1     Running     0          4m5s
kubesphere-logging-system      fluent-bit-vxbp7                                   1/1     Running     0          4m5s
kubesphere-logging-system      fluentbit-operator-5bf7687b88-5xqp2                1/1     Running     0          5m5s
kubesphere-logging-system      ks-events-exporter-5cb959c74b-x7rwb                2/2     Running     0          3m34s
kubesphere-logging-system      ks-events-operator-7d46fcccc9-pmvcs                1/1     Running     0          3m59s
kubesphere-logging-system      ks-events-ruler-97f756879-bmzdc                    2/2     Running     0          3m34s
kubesphere-logging-system      ks-events-ruler-97f756879-cnjxv                    2/2     Running     0          3m34s
kubesphere-logging-system      kube-auditing-operator-7574bd6f96-jrd6s            1/1     Running     0          4m4s
kubesphere-logging-system      kube-auditing-webhook-deploy-6dfb46bb6c-4kvc2      1/1     Running     0          3m46s
kubesphere-logging-system      kube-auditing-webhook-deploy-6dfb46bb6c-q7cm5      1/1     Running     0          3m46s
kubesphere-logging-system      logsidecar-injector-deploy-667c6c9579-lcvjb        2/2     Running     0          4m3s
kubesphere-logging-system      logsidecar-injector-deploy-667c6c9579-sjwcf        2/2     Running     0          4m3s
kubesphere-monitoring-system   alertmanager-main-0                                2/2     Running     0          13h
kubesphere-monitoring-system   alertmanager-main-1                                2/2     Running     0          13h
kubesphere-monitoring-system   alertmanager-main-2                                2/2     Running     0          13h
kubesphere-monitoring-system   kube-state-metrics-5c466fc7b6-jlwcz                3/3     Running     0          13h
kubesphere-monitoring-system   node-exporter-gfn74                                2/2     Running     0          13h
kubesphere-monitoring-system   node-exporter-ghbjz                                2/2     Running     0          13h
kubesphere-monitoring-system   node-exporter-jpbk4                                2/2     Running     0          13h
kubesphere-monitoring-system   node-exporter-ldkz6                                2/2     Running     0          13h
kubesphere-monitoring-system   node-exporter-skqqw                                2/2     Running     0          13h
kubesphere-monitoring-system   node-exporter-wtf6q                                2/2     Running     0          13h
kubesphere-monitoring-system   notification-manager-deployment-7ff95b7544-9gktx   1/1     Running     0          13h
kubesphere-monitoring-system   notification-manager-deployment-7ff95b7544-k2sbr   1/1     Running     0          13h
kubesphere-monitoring-system   notification-manager-operator-5cbb58b756-wpwfb     2/2     Running     0          13h
kubesphere-monitoring-system   prometheus-k8s-0                                   3/3     Running     1          13h
kubesphere-monitoring-system   prometheus-k8s-1                                   3/3     Running     1          13h
kubesphere-monitoring-system   prometheus-operator-78c5cdbc8f-c7cpf               2/2     Running     0          13h
kubesphere-system              etcd-85c98fb695-zmtsq                              1/1     Running     0          12h
kubesphere-system              ks-apiserver-65b8d48c77-bbzkg                      1/1     Running     0          2m36s
kubesphere-system              ks-apiserver-65b8d48c77-vsnqw                      1/1     Running     0          2m33s
kubesphere-system              ks-apiserver-65b8d48c77-xrps7                      1/1     Running     0          2m34s
kubesphere-system              ks-console-9bc9c5df8-2sxf9                         1/1     Running     0          13h
kubesphere-system              ks-console-9bc9c5df8-l76kd                         1/1     Running     0          13h
kubesphere-system              ks-console-9bc9c5df8-vknbj                         1/1     Running     0          13h
kubesphere-system              ks-controller-manager-6f7b5f6d6-9hmlb              1/1     Running     0          2m34s
kubesphere-system              ks-controller-manager-6f7b5f6d6-d872w              1/1     Running     0          2m28s
kubesphere-system              ks-controller-manager-6f7b5f6d6-v5rfj              1/1     Running     0          2m36s
kubesphere-system              ks-installer-85854b8c8-9d9nk                       1/1     Running     0          13h
kubesphere-system              minio-764b67f6fb-566bh                             1/1     Running     0          12h
kubesphere-system              mysql-67cd66d5d-5n76k                              1/1     Running     0          12h
kubesphere-system              openldap-0                                         1/1     Running     0          13h
kubesphere-system              openldap-1                                         1/1     Running     0          13h
kubesphere-system              redis-ha-haproxy-ffb8d889d-htrkv                   1/1     Running     0          13h
kubesphere-system              redis-ha-haproxy-ffb8d889d-jsx6m                   1/1     Running     0          13h
kubesphere-system              redis-ha-haproxy-ffb8d889d-swdnm                   1/1     Running     0          13h
kubesphere-system              redis-ha-server-0                                  2/2     Running     0          13h
kubesphere-system              redis-ha-server-1                                  2/2     Running     0          13h
kubesphere-system              redis-ha-server-2                                  2/2     Running     0          13h
```

## 集群环境下，启动了所有组件功能后的 master image 列表

```
[root@master1 ~]# docker images
REPOSITORY                           TAG                 IMAGE ID            CREATED             SIZE
kubesphere/ks-controller-manager     v3.0.0              85bd13080839        2 months ago        82MB
kubesphere/ks-apiserver              v3.0.0              d9fac59cfb8c        2 months ago        120MB
kubesphere/ks-console                v3.0.0              d5987e1f99ac        2 months ago        95.5MB
kubesphere/fluent-bit                v1.4.6              e46b2f18c44a        2 months ago        71.8MB
kubesphere/kube-proxy                v1.17.9             ddc09a4c2193        3 months ago        117MB
kubesphere/kube-controller-manager   v1.17.9             c7f1dde319ee        3 months ago        161MB
kubesphere/kube-apiserver            v1.17.9             7417868987f3        3 months ago        171MB
kubesphere/kube-scheduler            v1.17.9             f7b1228fa995        3 months ago        94.4MB
calico/node                          v3.15.1             1470783b1474        3 months ago        262MB
calico/pod2daemon-flexvol            v3.15.1             a696ebcb2ac7        3 months ago        112MB
calico/cni                           v3.15.1             2858353c1d25        3 months ago        217MB
calico/kube-controllers              v3.15.1             8ed9dbffe350        3 months ago        53.1MB
kubesphere/linux-utils               1.10.0              28c1cd0be1ea        5 months ago        11MB
osixia/openldap                      1.3.0               faac9bb59f83        5 months ago        260MB
kubesphere/k8s-dns-node-cache        1.15.12             5340ba194ec9        6 months ago        107MB
coredns/coredns                      1.6.9               faac9e62c0d6        7 months ago        43.2MB
kubesphere/node-exporter             ks-v0.18.1          cfb0175954de        11 months ago       23.7MB
redis                                5.0.5-alpine        ed7d2ff5a623        14 months ago       29.3MB
haproxy                              2.0.4               9009db9c8961        14 months ago       91.1MB
kubesphere/etcd                      v3.3.12             28c771d7cfbf        21 months ago       40.6MB
kubesphere/kube-rbac-proxy           v0.4.1              70eeaa7791f2        21 months ago       41.3MB
kubesphere/pause                     3.1                 da86e6ba6ca1        2 years ago         742kB
```

## 集群环境下，启动了所有组件功能后的 node image 列表

````
[root@node1 ~]# docker images
REPOSITORY                                 TAG                            IMAGE ID            CREATED             SIZE
docker                                     19.03                          6972c414f322        10 days ago         217MB
kubesphere/ks-controller-manager           v3.0.0                         85bd13080839        2 months ago        82MB
kubesphere/ks-apiserver                    v3.0.0                         d9fac59cfb8c        2 months ago        120MB
kubesphere/fluentbit-operator              v0.2.0                         6b6b86b48aa3        2 months ago        44MB
kubesphere/kube-events-ruler               v0.1.0                         7006904470db        2 months ago        108MB
kubesphere/kube-auditing-webhook           v0.1.0                         035825cb64ce        2 months ago        117MB
kubesphere/fluent-bit                      v1.4.6                         e46b2f18c44a        2 months ago        71.8MB
prom/prometheus                            v2.20.1                        b205ccdd28d3        2 months ago        145MB
kubesphere/notification-manager-operator   v0.1.0                         c441b79e9606        3 months ago        44.4MB
kubesphere/notification                    flyway_v2.1.2                  b1e18b386fa8        3 months ago        157MB
kubesphere/notification                    v2.1.2                         7a74fe46aab6        3 months ago        59.3MB
kubesphere/alerting                        v2.1.2                         9e0e584f61f6        3 months ago        102MB
kubesphere/log-sidecar-injector            1.1                            bd5f40b9ebbf        3 months ago        51.6MB
kubesphere/kube-proxy                      v1.17.9                        ddc09a4c2193        3 months ago        117MB
calico/node                                v3.15.1                        1470783b1474        3 months ago        262MB
calico/pod2daemon-flexvol                  v3.15.1                        a696ebcb2ac7        3 months ago        112MB
calico/cni                                 v3.15.1                        2858353c1d25        3 months ago        217MB
calico/kube-controllers                    v3.15.1                        8ed9dbffe350        3 months ago        53.1MB
kubesphere/prometheus-config-reloader      v0.38.3                        8011d6eb5bac        4 months ago        10.1MB
prom/alertmanager                          v0.21.0                        c876f5897d7b        4 months ago        55.5MB
kubesphere/provisioner-localpv             1.10.0                         6b5529f464f7        5 months ago        68.4MB
kubesphere/node-disk-manager               0.5.0                          dbbed43bcbdb        5 months ago        168MB
kubesphere/linux-utils                     1.10.0                         28c1cd0be1ea        5 months ago        11MB
kubesphere/metrics-server                  v0.3.7                         07c9e703ca2c        6 months ago        55.4MB
kubesphere/k8s-dns-node-cache              1.15.12                        5340ba194ec9        6 months ago        107MB
coredns/coredns                            1.6.9                          faac9e62c0d6        7 months ago        43.2MB
alpine                                     3.10.4                         af341ccd2df8        9 months ago        5.56MB
kubesphere/node-exporter                   ks-v0.18.1                     cfb0175954de        11 months ago       23.7MB
kubesphere/kubectl                         v1.0.0                         7f81664a09d0        12 months ago       82.1MB
kubesphere/elasticsearch-oss               6.7.0-1                        1b7edda08f75        13 months ago       702MB
jimmidyson/configmap-reload                v0.3.0                         7ec24a279487        14 months ago       9.7MB
minio/mc                                   RELEASE.2019-08-07T23-14-43Z   2def265e6001        15 months ago       23.1MB
kubesphere/kube-rbac-proxy                 v0.4.1                         70eeaa7791f2        21 months ago       41.3MB
mysql                                      8.0.11                         5dbe5b6313e1        2 years ago         445MB
kubesphere/pause                           3.1                            da86e6ba6ca1        2 years ago         742kB
````



-------------------------------------------------------------------

## 持久化存储配置说明

- <https://v2-1.docs.kubesphere.io/docs/zh-CN/installation/storage-configuration/>
- 推荐 
    - Ceph RBD(块存储)：<https://v2-1.docs.kubesphere.io/docs/zh-CN/appendix/ceph-ks-install/>
    - GlusterFS：<https://v2-1.docs.kubesphere.io/docs/zh-CN/appendix/glusterfs-ks-install/>

## 重启服务器后注意事项

- <https://kubesphere.com.cn/forum/d/1661-k8s-kubesphere>

```
K8s 和 KubeSphere 都不存在重启一说，只有 Docker 可以重启。通常情况 K8s 和 Docker 在服务器重启后可以自愈，KubeSphere 也会自动恢复运行。

sudo systemctl daemon-reload
sudo systemctl restart docker
```

## KubeSphere v3.0.0 对接 SonarQube

- <https://kubesphere.com.cn/forum/d/2044-kubesphere-v3-0-0-sonarqube>

## 集成第三方服务（集群外数据库）


## API 接口

- 查看token

```
curl -X POST \
  http://IP:30880/kapis/iam.kubesphere.io/v1alpha2/login \
  -H 'Content-Type: application/json' \
  -d '{
  "username":"admin",
  "password":"密码"
}'

```


## 网络问题

- 如果想对外用域名进行访问，需要添加：应用路由，不然只能用公网 IP + NodePort
- 添加应用路由的时候，应用可以是有开 NodePort 也可以没开


## 使用外部的 MySQL 等服务

- 这里的核心是 Service 和 Endpoint 要同名
- 然后其他应用就可以用这个名字进行访问了

```
kind: Service
apiVersion: v1
metadata:
  name: mysql-external
  namespace: sacf-project
  annotations:
    kubesphere.io/creator: sacf-admin
spec:
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306
---
apiVersion: v1
kind: Endpoints
metadata:
  name: mysql-external
  namespace: sacf-project
  annotations:
    kubesphere.io/creator: sacf-admin
subsets:
  - addresses:
      - ip: 10.23.1.32
    ports:
      - port: 3306
```

- 然后应用配置：`kubectl apply -f mysql-service-endpoint.yaml`
- 如果要删除：

```
kubectl delete services mysql-external -n sacf-project
kubectl delete endpoints mysql-external -n sacf-project
```


## 使用外部 Harbor

```
harbor 的 https 证书不是自建的，是阿里云免费一年的证书

假设后面用到的所有凭证、密钥我们都叫做 harbor-id

在你创建的项目空间中：配置中心 > 密钥，必须创建一个 harbor-id 的镜像类型密钥，并且必须是点击验证后是告诉你验证通过的。这是必须的。

在你的 DevOps 工程中的：工程管理 > 凭证，必须创建一个 harbor-id，这样你 pipeline 过程 push 镜像才能 push 成功，这是必须的。
```

- 项目 Deployment yaml 需要配置，这是我的发布的 yaml，其中最重要的改动是最下面我有一个中文注释

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: kubesphere
    component: ks-sample-dev
    tier: backend
  name: ks-sample-dev
  namespace: kubesphere-sample-dev
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  selector:
    matchLabels:
      app: kubesphere
      component: ks-sample-dev
      tier: backend
  template:
    metadata:
      labels:
        app: kubesphere
        component: ks-sample-dev
        tier: backend
    spec:
      containers:
        - env:
            - name: CACHE_IGNORE
              value: js|html
            - name: CACHE_PUBLIC_EXPIRATION
              value: 3d
          image: $REGISTRY/$DOCKERHUB_NAMESPACE/$APP_NAME:SNAPSHOT-$BRANCH_NAME-$BUILD_NUMBER
          readinessProbe:
            httpGet:
              path: /
              port: 8080
            timeoutSeconds: 10
            failureThreshold: 30
            periodSeconds: 5
          imagePullPolicy: Always
          name: ks-sample
          ports:
            - containerPort: 8080
              protocol: TCP
          resources:
            limits:
              cpu: 300m
              memory: 600Mi
            requests:
              cpu: 100m
              memory: 100Mi
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      # 如果用私有仓库，这里需要配置上你私有仓库配置的凭证名
      imagePullSecrets:
        - name: harbor-id
      restartPolicy: Always
      terminationGracePeriodSeconds: 30
```

## 如果要部署 Istio 应用

- 需要先安装微服务治理的功能组件：<https://v2-1.docs.kubesphere.io/docs/zh-CN/installation/install-servicemesh/>
- 安装过程挺长的，差不多要 5~10 分钟。安装后，admin 重新登录界面，在 Components 下面就有一个 Istio 组件了。 
- 项目要开启服务治理还需要：`项目设置 > 高级设置 > 外网访问 > NodePort > 开启应用治理`
- 添加示例应用：`应用负载 > 应用 > 部署示例应用 > 应用治理必须是开启的`





