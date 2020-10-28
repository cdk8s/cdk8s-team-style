

# 集群安装

## 阿里云购买 ECS、EIP、NAT、SLB

- 核心：必须保证 ECS、EIP、NAT、SLB 都在同一个地区（不用具体到可用区级别），可能有些地区有 ECS 但是其他比如 SLB 没有，所以一定要都看下购买页面的地区选择选项 
- 购买 6 台 ECS 4C8G 服务器，都不需要有公网 IP
- EIP 需要 2 个，一个是绑定 SLB，一个绑定 NAT 网关的 DNAT（如果你还需要外网可以访问这些 ECS，那还需要一个 EIP 来绑定 NAT 网关的 SNAT，一个 EIP 只能绑定一个 ECS 所有端口，或者指定一台 ECS 的一个端口）
- 通过阿里云NAT网关产品实现无公网ECS通过有EIP的服务器代理访问公网
- 关于 NAT 网关支持 SNAT 和 DNAT介绍
    - SNAT 可以为VPC内无公网IP的ECS实例提供访问互联网的代理服务。
    - DNAT 可以将NAT网关上的公网IP映射给ECS实例使用，使ECS实例能够提供互联网服务
    - NAT 可以绑定多台 ECS，也可以直接绑定交换机。如果服务器都在一个交换机，直接绑定交换机最方便。
    - 一个 NAT 网关可以绑定 20 个 EIP

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

- 购买 SLB 用于对外暴露外网访问
- 访问实例管理：<https://slbnew.console.aliyun.com/slb/cn-beijing/slbs>
    - 可以看到我们的公网 IP 为：`47.112.248.107`，这个后面要用到
- 点击 `添加后端服务器` 按钮，选择我们的 k8s 所有 master 节点，如果有 3 个 master 就勾选 3 个
- 点击 `监听配置向导` 按钮
    - 我们要监听 TCP 6443 端口（api-server），下一步，选择 `默认服务器组`，各个 master 节点的端口上配置 6443，权重 100。最后提交配置。
    - 我们要监听 TCP 30880 端口（对外的 web 管理界面），下一步，选择 `默认服务器组`，各个 master 节点的端口上配置 30880，权重 100。最后提交配置。
- 选择一台 master1 节点，创建配置文件并执行

````
先安装一些简单工具：
yum install -y zip unzip lrzsz git epel-release wget htop deltarpm

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

- 如果安装中间会自动帮我们安装 docker，但是安装后默认的源是 Docker 国外的会很慢
- 所以我们可以考虑自己安装 Docker，改源。当前时间 2020-10 KubeSphere 3.0.0 用的是 `Docker version 19.03.13, build 4484c46d9d`

```
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

sudo systemctl daemon-reload
sudo systemctl restart docker
```

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
- 推荐 GlusterFS

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