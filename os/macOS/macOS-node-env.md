
# macOS 下 Node.js 开发环境

## 多 Node 环境

- 先确保已经卸载了 brew 安装的 node、或者是 pkg 安装的 node

```
brew update
mkdir ~/.nvm
brew install nvm

.zshrc 增加如下2个配置
export NVM_DIR=~/.nvm
source $(brew --prefix nvm)/nvm.sh

刷新 .zshrc
source ~/.zshrc

查看有哪些版本：nvm ls-remote

nvm install v16.20.2
nvm install v18.19.1

nvm ls

nvm use v18.19.1

nvm uninstall v21.6.2
```



## Node 卸载

- Homebrew 卸载（也是挺麻烦的，重新安装各种东西要删除）：`brew uninstall node`
    - `sudo rm -rf /usr/local/Cellar/node*`
    - `sudo rm -rf /usr/local/share/systemtap`
    - `sudo rm -rf /usr/local/lib/dtrace/node*`
- 官网安装包卸载：
    - `sudo rm -rf /usr/local/{bin/{node,npm,node-debug,node-gyp},include/node*,lib/node_modules/npm,lib/node,share/man/*/node*}`
    - `sudo rm -rf ~/.npm*`
    - `sudo rm -rf ~/.node*`
    - `sudo rm -rf /usr/local/lib/node*`
    - `sudo rm -rf /usr/local/share/doc/node*`

-------------------------------------------------------------------



-------------------------------------------------------------------

## nrm 切换源

```
安装：npm install -g nrm
列表源：nrm ls
使用源：nrm use taobao
```

-------------------------------------------------------------------


## Yarn 安装

- 官网说明：<https://yarnpkg.com/lang/zh-hans/docs/install/#mac-stable>
- 安装：`npm install -g yarn`
- 查看版本：`yarn --version`

-------------------------------------------------------------------


## pnpm 安装

- 官网说明：<https://pnpm.io/installation>
- 安装：`npm install -g pnpm`
- 查看版本：`pnpm --version`

-------------------------------------------------------------------

## 其他问题

- npm 安装很容易出现权限相关的问题，遇到了可以类似这样：`sudo npm install --unsafe-perm=true --allow-root --global gulp`

