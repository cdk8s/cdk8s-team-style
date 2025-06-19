
## 开启代理
vim ~/.bashrc

export https_proxy=socks5h://127.0.0.1:1080
export http_proxy=socks5h://127.0.0.1:1080
export all_proxy=socks5h://127.0.0.1:1080

## 安装

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

因为会自动加上一些环境变量，所以还需要:
source ~/.bashrc

nvm install v20

npm install -g nrm
nrm use taobao
npm install -g yarn
npm install -g pnpm