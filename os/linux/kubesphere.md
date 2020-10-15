
## 前提

- 关闭防火墙等限制

## Linux 最小安装

- 当前版本（202010）：3.0.0
- 官网说明：<https://kubesphere.io/zh/docs/quick-start/all-in-one-on-linux/>

```
下载脚本
wget -c https://kubesphere.io/download/kubekey-v1.0.0-linux-amd64.tar.gz -O - | tar -xz
chmod +x kk

开始安装
./kk create cluster --with-kubernetes v1.17.9 --with-kubesphere v3.0.0

中间会自动帮我们安装 docker，但是安装后默认的源是国外的会很慢，我们可以停掉安装先换源
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






