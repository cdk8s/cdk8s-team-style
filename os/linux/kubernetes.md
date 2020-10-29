 
 
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


## Pod（最小单元）

## Service

- 多个 Pod 的组合。比如 3 台 Node 上各有一个商品模块的 Pod，那这三个 Pod 就可以组成一个 Service 对外暴露使用，内部进行负载均衡

## Controllers

## Deployment

## Label 标签，用于对象资源的查询、筛选

## Namespace 命名空间，逻辑隔离

## YAML 组成

- apiVersion
- Kind
- Metadata
- Spec

## 命令


```
查看帮助命令
kubectl --help
kubectl get --help

查看所有类型、所有类型其下的东西
kubectl get all -o wide

查看k8s的所有node节点，确保都是 Ready
kubectl get node

获取所有命名空间列表以及其下的 pod 列表，其中 -o wide 显示展示更多详细信息
kubectl get pods  -o wide
kubectl get pod --all-namespaces -o wide
kubectl get pods --all-namespaces

获取指定命名空间的 pod 列表
kubectl get pod -n kube-system

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





