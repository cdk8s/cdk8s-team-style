
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


## 准备

```
确保都是 Ready
kubectl get nodes

确保都是 Running
kubectl get pods --all-namespaces
```




