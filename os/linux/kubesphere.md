
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

-------------------------------------------------------------------

## 高可用集群开始安装

```
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
systemctl stop firewalld && systemctl disable firewalld
echo "vm.swappiness = 0" >> /etc/sysctl.conf
swapoff -a && sysctl -w vm.swappiness=0

所有服务器都要先安装一些简单工具：
yum install -y zip unzip lrzsz git epel-release wget htop deltarpm

所有服务器都要更换CentOS YUM源为阿里云yum源
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum clean all && yum makecache
yum update -y

所有服务器都要进行时间同步，并确认时间同步成功
timedatectl
timedatectl set-ntp true

开始在所选安装机器上设置免密登录，我这里选择了 master1
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa

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

- 安装中间会自动帮我们安装 docker，但是安装后默认的源是 Docker 国外的会很慢
- 所以我们可以考虑自己安装 Docker，改源。当前时间 2020-10 KubeSphere 3.0.0 用的是 `Docker version 19.03.13, build 4484c46d9d`

```
yum install -y yum-utils \
    device-mapper-persistent-data \
    lvm2

yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 如果以上添加仓库速度慢可以用阿里云源地址
# http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

yum install -y containerd.io docker-ce-19.03.13 docker-ce-cli-19.03.13

systemctl start docker
systemctl enable docker

修改镜像源配置
vim /etc/docker/daemon.json

{
  "log-opts": {
    "max-size": "5m",
    "max-file": "3"
  },
  "exec-opts": [
    "native.cgroupdriver=systemd"
  ],
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







## Linux 最小安装

- 当前版本（202010）：3.0.0
- 官网说明：<https://kubesphere.io/zh/docs/quick-start/all-in-one-on-linux/>

```
下载脚本
wget -c https://kubesphere.io/download/kubekey-v1.0.0-linux-amd64.tar.gz -O - | tar -xz
chmod +x kk

开始安装
./kk create cluster --with-kubernetes v1.17.9 --with-kubesphere v3.0.0

查看执行 log
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f

出现 Welcome to KubeSphere! 表示安装成功
```

## 管理

- 企业空间：<http://192.168.31.137:30880/access/workspaces>
    - 理论上微服务的各个团队，每个团队创建一个企业空间，让他们各自管好自己的服务
- 项目管理：<http://192.168.31.137:30880/clusters/default/projects>
- 集群状态：<http://192.168.31.137:30880/clusters/default/monitor-cluster/overview>
- 节点管理：<http://192.168.31.137:30880/clusters/default/nodes>
- 容器组：<http://192.168.31.137:30880/clusters/default/pods>
- 组件管理：<http://192.168.31.137:30880/clusters/default/components>


## 关闭不用的功能

- 商店（openpitrix）
- Service Mesh（servicemesh）
- 日志系统（logging）

## 开启其他功能

- DevOps（devops）
- 告警通知系统（notification、alerting）
- HPA-弹性伸缩（metrics_server）

## 准备

```
确保都是 Ready
kubectl get nodes

确保都是 Running
kubectl get pods --all-namespaces

输出 pod 详细信息
kubectl describe pod $pod_name
```

## 编辑集群配置文件

- 访问：<http://192.168.31.137:30880/clusters/default/customresources/clusterconfigurations.installer.kubesphere.io/resources>
- 点击三个点 > 编辑配置文件，默认如下

```
apiVersion: installer.kubesphere.io/v1alpha1
kind: ClusterConfiguration
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"installer.kubesphere.io/v1alpha1","kind":"ClusterConfiguration","metadata":{"annotations":{},"labels":{"version":"v3.0.0"},"name":"ks-installer","namespace":"kubesphere-system"},"spec":{"alerting":{"enabled":false},"auditing":{"enabled":false},"authentication":{"jwtSecret":""},"common":{"es":{"elasticsearchDataVolumeSize":"20Gi","elasticsearchMasterVolumeSize":"4Gi","elkPrefix":"logstash","logMaxAge":7},"etcdVolumeSize":"20Gi","minioVolumeSize":"20Gi","mysqlVolumeSize":"20Gi","openldapVolumeSize":"2Gi","redisVolumSize":"2Gi"},"console":{"enableMultiLogin":false,"port":30880},"devops":{"enabled":false,"jenkinsJavaOpts_MaxRAM":"2g","jenkinsJavaOpts_Xms":"512m","jenkinsJavaOpts_Xmx":"512m","jenkinsMemoryLim":"2Gi","jenkinsMemoryReq":"1500Mi","jenkinsVolumeSize":"8Gi"},"etcd":{"endpointIps":"192.168.31.137","monitoring":true,"port":2379,"tlsEnable":true},"events":{"enabled":false,"ruler":{"enabled":true,"replicas":2}},"logging":{"enabled":false,"logsidecarReplicas":2},"metrics_server":{"enabled":true},"monitoring":{"prometheusMemoryRequest":"400Mi","prometheusVolumeSize":"20Gi"},"multicluster":{"clusterRole":"none"},"networkpolicy":{"enabled":false},"notification":{"enabled":false},"openpitrix":{"enabled":false},"persistence":{"storageClass":""},"servicemesh":{"enabled":false}}}
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
    endpointIps: 192.168.31.137
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

- 我们需要改为：

```
apiVersion: installer.kubesphere.io/v1alpha1
kind: ClusterConfiguration
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: >
      {"apiVersion":"installer.kubesphere.io/v1alpha1","kind":"ClusterConfiguration","metadata":{"annotations":{},"labels":{"version":"v3.0.0"},"name":"ks-installer","namespace":"kubesphere-system"},"spec":{"alerting":{"enabled":false},"auditing":{"enabled":false},"authentication":{"jwtSecret":""},"common":{"es":{"elasticsearchDataVolumeSize":"20Gi","elasticsearchMasterVolumeSize":"4Gi","elkPrefix":"logstash","logMaxAge":7},"etcdVolumeSize":"20Gi","minioVolumeSize":"20Gi","mysqlVolumeSize":"20Gi","openldapVolumeSize":"2Gi","redisVolumSize":"2Gi"},"console":{"enableMultiLogin":false,"port":30880},"devops":{"enabled":false,"jenkinsJavaOpts_MaxRAM":"2g","jenkinsJavaOpts_Xms":"512m","jenkinsJavaOpts_Xmx":"512m","jenkinsMemoryLim":"2Gi","jenkinsMemoryReq":"1500Mi","jenkinsVolumeSize":"8Gi"},"etcd":{"endpointIps":"192.168.31.137","monitoring":true,"port":2379,"tlsEnable":true},"events":{"enabled":false,"ruler":{"enabled":true,"replicas":2}},"logging":{"enabled":false,"logsidecarReplicas":2},"metrics_server":{"enabled":true},"monitoring":{"prometheusMemoryRequest":"400Mi","prometheusVolumeSize":"20Gi"},"multicluster":{"clusterRole":"none"},"networkpolicy":{"enabled":false},"notification":{"enabled":false},"openpitrix":{"enabled":false},"persistence":{"storageClass":""},"servicemesh":{"enabled":false}}}
  labels:
    version: v3.0.0
  name: ks-installer
  namespace: kubesphere-system
spec:
  alerting:
    enabled: true
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
    enabled: true
    jenkinsJavaOpts_MaxRAM: 2g
    jenkinsJavaOpts_Xms: 512m
    jenkinsJavaOpts_Xmx: 512m
    jenkinsMemoryLim: 2Gi
    jenkinsMemoryReq: 1500Mi
    jenkinsVolumeSize: 8Gi
  etcd:
    endpointIps: 192.168.31.137
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
    enabled: true
  openpitrix:
    enabled: false
  persistence:
    storageClass: ''
  servicemesh:
    enabled: false
```

- 改完之后就会开始变更安装，可以查看安装过程 log，这个时间会比较久：

```
kubectl logs -n kubesphere-system $(kubectl get pod -n kubesphere-system -l app=ks-install -o jsonpath='{.items[0].metadata.name}') -f

出现 Welcome to KubeSphere! 表示安装成功
```

- 访问组件管理：<http://192.168.31.137:30880/clusters/default/components>
- 可以看到 DevOps 相关组件已经运行

## DevOps 项目管理

- 默认的 system-workspace 工作空间是不能用来创建 DevOps 项目的，所以一般都要自己创建一个业务工作空间进行实际项目开发
- 我这里创建一个：my-workspace 的项目空间：<http://192.168.31.137:30880/workspaces/my-workspace/overview/usage>
- 企业空间也有自己的角色管理：<http://192.168.31.137:30880/workspaces/my-workspace/roles>
- 管理 DevoOps 项目：<http://192.168.31.137:30880/workspaces/my-workspace/devops>
- 我这里创建一个：mydevops 项目：<http://192.168.31.137:30880/my-workspace/clusters/default/devops/mydevopspz7kv/pipelines>
- DevOps 项目也是有自己的角色管理：<http://192.168.31.137:30880/my-workspace/clusters/default/devops/mydevopspz7kv/roles>
- 创建一些凭证，包括 SSH 密钥、Token 等：<http://192.168.31.137:30880/my-workspace/clusters/default/devops/mydevopspz7kv/credentials>


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