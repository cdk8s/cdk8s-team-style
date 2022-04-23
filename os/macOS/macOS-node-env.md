
# macOS 下 Node.js 开发环境

## Node 安装

- **Homebrew 方式（推荐，因为避免权限问题）**：`brew install node`
    - 如果你不想要最新版本的 node 可以先查询已有哪些版本：`brew search node`
    - 目前稳定版本是 14，要安装 14 可以这样做：

```
brew install node@14

根据安装后的提示配置环境变量：
export PATH="/usr/local/opt/node@14/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/node@14/lib"
export CPPFLAGS="-I/usr/local/opt/node@14/include"

brew link --overwrite --force node@14
```


- 其他方式：官网安装包下载：<https://nodejs.org/zh-cn/>
    - mac 不推荐用 pkg 包安装，很容易在项目中遇到各种权限问题

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

## nrm 切换源

```
安装：npm install -g nrm
列表源：nrm ls
使用源：nrm use taobao

安装 pnpm：
npm install -g pnpm@next-7
```

-------------------------------------------------------------------


## Yarn 安装

- 官网说明：<https://yarnpkg.com/lang/zh-hans/docs/install/#mac-stable>
- 先查询已有哪些版本：`brew search yarn`
- **Homebrew 方式（推荐）**：`brew install yarn`
- 升级：`brew upgrade yarn`
- 查看版本：`yarn --version`

-------------------------------------------------------------------

## 其他问题

- npm 安装很容易出现权限相关的问题，遇到了可以类似这样：`sudo npm install --unsafe-perm=true --allow-root --global gulp`

