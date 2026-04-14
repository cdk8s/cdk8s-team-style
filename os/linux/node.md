# Node 安装和配置

## nvm 官网

- <https://github.com/nvm-sh/nvm>

## 开启代理
vim ~/.bashrc

export https_proxy=socks5h://127.0.0.1:1080
export http_proxy=socks5h://127.0.0.1:1080
export all_proxy=socks5h://127.0.0.1:1080

## 安装

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

```
# 不能访问github的话， 可以用下面这条
curl -o- https://gitee.com/RubyMetric/nvm-cn/raw/main/install.sh | bash
 
# 然后执行下面的两条命令即可
chmod +x ~/.nvm/nvm.sh
source ~/.bashrc
```

因为会自动加上一些环境变量，所以还需要:
source ~/.bashrc

nvm install v20

npm install -g nrm
nrm use taobao
npm install -g yarn
npm install -g pnpm


## nvm 指定项目使用版本

```
# 2. 创建 .nvmrc 文件并写入 16
echo "16" > .nvmrc

# 每次进目录都要手动敲一次 nvm use
nvm use
```


-------------------------------------------------------------------

## Node 官方版安装

- 官网：<https://nodejs.org>
- 官网下载：<https://nodejs.org/zh-cn/download/>
- 历史版本下载：<https://nodejs.org/zh-cn/download/releases/>
- 此时（20171212） Maven 最新版本为：**8.9.3 (includes npm 5.5.1)**
- 官网安装教程：<https://nodejs.org/en/download/package-manager/>
- 官网 CentOS 系统下的安装教程：<https://nodejs.org/en/download/package-manager/#enterprise-linux-and-fedora>
- 官网文档复制过来就是：

```
如果你是要安装 node 8 系列，下载这个 yum 源
curl --silent --location https://rpm.nodesource.com/setup_8.x | sudo bash -

如果你是要安装 node 9 系列，下载这个 yum 源
curl --silent --location https://rpm.nodesource.com/setup_9.x | sudo bash -

如果你是要安装 node 10 系列，下载这个 yum 源
curl --silent --location https://rpm.nodesource.com/setup_10.x | sudo bash -

如果你是要安装 node 11 系列，下载这个 yum 源
curl --silent --location https://rpm.nodesource.com/setup_11.x | sudo bash -

如果你是要安装 node 12 系列，下载这个 yum 源
curl --silent --location https://rpm.nodesource.com/setup_12.x | sudo bash -

然后通过 yum 开始安装（软件大小：51M 左右）
sudo yum -y install nodejs
```

- 验证：`node -v`
- 注意:因为网络原因，最好先把脚本下载到本地，再用代理进行安装


## 卸载

```
sudo yum -y remove nodejs npm

sudo rm -f /usr/local/bin/node
sudo rm -f /usr/local/bin/npm
sudo rm -f /usr/local/bin/npx

# 清理 npm 全局安装目录（CentOS 7 默认通常在这两个位置之一）
sudo rm -rf /usr/lib/node_modules
sudo rm -rf /usr/local/lib/node_modules

# 清理 npm 缓存目录
sudo rm -rf /root/.npm

sudo yum clean all

node -v
npm -v

```

## nrm 快速切换 NPM 源

- 安装：`npm install -g nrm`
- 列表源：`nrm ls`
- 使用源：`nrm use taobao`
- 更多使用方法：<https://segmentfault.com/a/1190000000473869>

## 安装 yarn

- 安装：`npm install -g yarn`
- 验证：`yarn -v`

## 其他常用库

```
npm install -g serve
```

