
## 前提

- 关闭防火墙等限制

## Linux 最小安装

- 当前版本（202010）：5.2.2
- 官网说明：<https://www.rainbond.com/docs/quick-start/quick-install/>

```
如果你是局域网的机子或者本地电脑虚拟机，则先确定你的局域网 IP 比如：192.168.31.123
如果你是阿里云 ECS 这类云虚拟机，则确认你的公网 IP 比如：81.71.118.156
确认以上 IP 等下要用到
同时确保服务器 SSH 端口为 22，这个也是必须的
确保服务器的防火墙是关闭的，云服务器的安全组是开放所有端口的

ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa
ssh-copy-id 刚刚让你确认的IP地址

验证是否可以免密登录：ssh -p 22 root@刚刚让你确认的IP地址

export EIP=刚刚让你确认的IP地址

开始执行安装，整个过程会用阿里云的 docker 镜像源，所以速度相对还是很快，但是也得十来分钟
wget https://rainbond-pkg.oss-cn-shanghai.aliyuncs.com/offline/5.2/easzup && chmod +x easzup && ./easzup -D

开始启动，启动也需要几分钟
./easzup -S && docker exec -it kubeasz easzctl start-aio


执行完成后，出现以下提示：
[INFO] save context: aio
[INFO] save aio roles' configration
[INFO] save aio ansible hosts
[INFO] save aio kubeconfig
[INFO] save aio kube-proxy.kubeconfig
[INFO] save aio certs
[INFO] Action successed : start-aio
[INFO] Visit http://刚刚让你确认的IP地址:30008 to view the installation progress

根据提示访问对应地址http://刚刚让你确认的IP地址:30008，查看 Rainbond 平台安装进度
这时候界面上还会显示要下载一些安装包，它们自己操作，我们不需要管
界面上都安装完成后会提示你访问：访问地址 http://刚刚让你确认的IP地址:7070
```

## 企业视图下的管理

- 官网 5.2.x 版本的快速上手视频演示，讲得很好（密码:3lvp）：<https://pan.baidu.com/s/1crqwKU2HIj81xk1_JOzo2g>
- 点击左上角的伸缩按钮，可以看到有分为：`企业视图`、`团队视图`
- 首次使用 `团队视图` 下面肯定是没有任何内容的，所以我们需要先创建团队。
- 在 `企业视图 > 总览 > 创建团队`，填写团队名称，选择企业已有集群
- 创建好之后需要刷新下浏览器，然后点击左上角的伸缩按钮，可以看到：`团队视图` 有我们刚刚创建的团队，点击这个团队名字

## 团队视图下的管理

- 在 `团队视图` 下面可以创建各种项目
- 点击左侧 `新增` 可以有几种安装应用方式，我们一般场景应该是 `基于源码创建组件`，填写自己的仓库地址、分支即可
- 我们也可以选择官网 Demo，内置了好几种语言的 Demo 项目，并且还提供了 gitee 的源码地址，这个很贴心
- 拉取好之后，点击 `创建`，则会进入应用的视图下，这时候看构建组件的日志，可以看到 maven 编译包的日志信息


## 应用视图下的管理

- 在 `应用 > 默认应用 > 组件列表` 假设我们创建了一个服务组件下的 Java Maven 项目
- 在应用的页头 `构建源` 中可以配置 Maven 相关参数，构建命令等
- 在应用的页头 `伸缩` 中可以配置手动伸缩容器个数，或根据内存、CPU使用情况进行自动伸缩
- 在应用的页头 `其他设置` 中可以配置健康检查
- 在应用的右上角有 `Web终端` 可以进入 Docker 容器中，查看 Docker 文件
- 在 `应用 > 默认应用 > 网关` 我们可以创建外网访问的策略。官网这样解释 `访问策略是指从集群外访问组件的方式，包括使用HTTP域名访问或IP+Port(TCP/UDP)访问，这里仅管理当前应用下的所有组件的访问策略`


## 准备

```
确保都是 Ready
kubectl get nodes

确保都是 Running
kubectl get pods --all-namespaces
```

## 快速安装 Kubernetes

- <https://www.rainbond.com/docs/user-operations/install/kubernetes-install/#kubernetes%E7%9A%84%E9%AB%98%E5%8F%AF%E7%94%A8%E5%AE%89%E8%A3%85>

## 基于 K8s 高可用安装 Rainbond

- <https://www.rainbond.com/docs/install/install-from-k8s/high-availability/>




