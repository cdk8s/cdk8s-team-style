 
 
# kubernetes 介绍

- 当前时间 2020-10
- 我使用的版本：
    - CentOS 7.8
    - Kubernetes 1.17.9

## 优点

- 容灾，有任何 node 节点宕机，pod 容器 stop 都可以自动帮我们拉起一个新的 pod 容器来提供服务。所以我们只要保证应用无状态即可。
- 轻松扩容
- 


## 组件

- 官网文档：<https://kubernetes.io/zh/docs/concepts/overview/components/>
- kubectl 部署和管理应用程序。使用 kubectl，你可以检查集群资源；创建、删除和更新组件；查看你的新集群；并启动实例应用程序。
- Master
    - etcd
    - kube-apiserver：API 服务器是 Kubernetes 控制面的组件， 该组件公开了 Kubernetes API。 API 服务器是 Kubernetes 控制面的前端
    - kube-scheduler
    - kube-controller-manager
    - cloud-controller-manager
- Node
    - Kubelet：一个在集群中每个节点上运行的代理。它保证容器都运行在 Pod 中。
    - kube-proxy
    - Container Runtime（docker、 containerd、CRI-O）
- 插件（Addons）
    - DNS
    - Web 界面（仪表盘）
    - 容器资源监控
    - 集群层面日志


## Pod

- 官网文档：<https://kubernetes.io/zh/docs/concepts/workloads/pods/>
- Pod 是可以在 Kubernetes 中创建和管理的、最小的可部署的计算单元。
- Pod 是一组（一个或多个） 容器；这些容器共享存储、网络、以及怎样运行这些容器的声明。这些容器是相对紧密的耦合在一起的。在非云环境中，在相同的物理机或虚拟机上运行的应用类似于在同一逻辑主机上运行的云应用。
- 通常你不需要直接创建 Pod，甚至单实例 Pod。 相反，你会使用诸如 Deployment 或 Job 这类工作负载资源 来创建 Pod。如果 Pod 需要跟踪状态， 可以考虑 StatefulSet 资源。

## Controllers

- 官网文档：<https://kubernetes.io/zh/docs/concepts/workloads/controllers/>
- 创建、管理多个 Pod
- 常见 Controller 有
    - ReplicaSet
        - 用来替换 ReplicationController
        - ReplicaSet 的目的是维护一组在任何时候都处于运行状态的 Pod 副本的稳定集合。 因此，它通常用来保证给定数量的、完全相同的 Pod 的可用性。
    - ReplicationController
    - Deployments
        - 一个 Deployment 控制器为 Pods 和 ReplicaSets 提供声明式的更新能力。
    - StatefulSets
        - StatefulSet 是用来管理有状态应用的工作负载 API 对象。
    - DaemonSet
        - DaemonSet 确保全部（或者某些）节点上运行一个 Pod 的副本。 当有节点加入集群时， 也会为他们新增一个 Pod 。 当有节点从集群移除时，这些 Pod 也会被回收。删除 DaemonSet 将会删除它创建的所有 Pod。

## Service

- 官网文档：<https://kubernetes.io/zh/docs/concepts/services-networking/>
- 多个 Pod 的组合。比如 3 台 Node 上各有一个商品模块的 Pod，那这三个 Pod 就可以组成一个 Service 对外暴露使用，内部进行负载均衡
- 将运行在一组 Pods 上的应用程序公开为网络服务的抽象方法。
- 为一组 Pod 提供相同的 DNS 名， 并且可以在它们之间进行负载均衡

## Ingress

- 官网文档：<https://kubernetes.io/zh/docs/concepts/services-networking/ingress/>
- Ingress 是对集群中服务的外部访问进行管理的 API 对象，典型的访问方式是 HTTP。
- Ingress 可以提供负载均衡、SSL 终结和基于名称的虚拟托管。
- 用的最多的是 ingress-nginx，会 nginx 会更好理解它

## Label 标签，用于对象资源的查询、筛选

- 官网文档：<>

## Namespace 命名空间，逻辑隔离

- 官网文档：<>


## 命令

- kubectl 官网命令：<https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands>

```
查看帮助命令
kubectl --help
kubectl get --help

查看所有类型、所有类型其下的东西，其中 -o wide 以纯文本方式显示更多详细信息，一般还用 -o yaml。
kubectl get all -o wide

查看k8s的所有node节点，确保都是 Ready
kubectl get node

获取所有命名空间列表以及其下的 pod 列表
kubectl get pod --all-namespaces -o wide
kubectl get pods --all-namespaces

获取指定命名空间的 pod 列表
kubectl get pod -n kube-system

查看 StorageClass 列表
kubectl get sc -o wide

查看 controllers 列表
kubectl get rc,svc -o wide

查看 service 列表
kubectl get pod,svc -o wide
kubectl get svc -o wide

输出 node 详细信息
kubectl describe node <node-name>

显示 Pod 的详细信息, 特别是查看 pod 无法创建的时候的日志
kubectl describe pod <pod-name> -n <namespaces-name>

查看pod的yaml文件
kubectl get pod <pod-name> -n <namespaces-name> -o yaml

查看pod的日志
kubectl logs <pod-name> -n <namespaces-name>
kubectl logs -f <pod-name> -n <namespaces-name>

根据 yaml 创建资源, apply 可以重复执行，create 不行
kubectl create -f pod.yaml
kubectl apply -f pod.yaml

基于 pod.yaml 定义的名称删除 pod
kubectl delete -f pod.yaml

删除所有包含某个 label 的pod 和 service
kubectl delete pod,svc -l name=<label-name>

查看 endpoint 列表
kubectl get endpoints


通过bash获得 pod 中某个容器的TTY，相当于登录容器
kubectl exec -it <pod-name> -n <namespaces-name> bash

编辑pod的yaml文件
kubectl get deployment -n <namespaces-name>
kubectl edit depolyment <pod-name> -n <namespaces-name> -o yaml

```

## YAML 组成

- apiVersion：版本
- Kind：操作类型有
    - Namespace
    - Pod
    - Service
    - Deployment
    - DaemonSet
    - Ingress
    - ConfigMap
    - ServiceAccount
    - Role
    - RoleBinding
    - ClusterRole
    - ClusterRoleBinding
- Metadata：元数据
- Spec：规格信息
























