```
先下载 nvm-windows(nvm-setup.exe)：
官网：https://github.com/coreybutler/nvm-windows/releases
百度云：https://pan.baidu.com/s/1BNaHh8a5DlAtg7qtsIB4UQ?pwd=7mv2


如果 setup 无法安装可以下载绿色版本: nvm-noinstall.zip
解压后，配置环境变量:

NVM_HOME：变量值应为 nvm 的安装目录（例如 C:\my-software\nvm-noinstall）。
NVM_SYMLINK：变量值应为 Node.js 的符号链接目录（通常为 C:\Program Files\nodejs）。
找到 Path 变量，确保里面包含了 %NVM_HOME% 和 %NVM_SYMLINK%。

如果是绿色版需要在解压后的根目录创建一个: settings.txt
配置:
root: C:\my-software\nvm-noinstall
path: C:\Program Files\nodejs
arch: 64
proxy: none
node_mirror: https://npmmirror.com/mirrors/node/
npm_mirror: https://npmmirror.com/mirrors/npm/

通过命令设置镜像:
nvm node_mirror https://npmmirror.com/mirrors/node/
nvm npm_mirror https://npmmirror.com/mirrors/npm/


检查镜像速度：
curl.exe -I https://npmmirror.com/mirrors/node/index.json

nvm install v18.20.4
nvm use v18.20.4
nvm alias default v18.20.4
```