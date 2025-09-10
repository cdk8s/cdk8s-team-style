

# macOS 终端方案 iTerm2 + Zsh + vim + Homebrew


## 总结

- iTerm2 比 Mac 默认的 Terminal 终端好用，配合 Zsh 确实更加得体
- **牢记：** 装了 zsh 之后，修改终端配置就变成了：`vim ~/.zshrc`，而不是：`vim ~/.bashrc`，所以以后看到别人的文章中需要：`vim ~/.bashrc`，那你自己要变通思想过来。
- 同时更新修改后的配置文件也从：`source ~/.bashrc`，变成了：`source ~/.zshrc`，当然还有其他取取巧方式，这里不谈。

## 先安装 VSCode

- 下载地址：<https://code.visualstudio.com/Download>
- 安装 code 命令行到 path

### Homebrew 是什么

- 术语定义
    - Homebrew 官网：<http://brew.sh/index_zh-cn.html>
    - 维基百科定义：<https://weiji.ga/zh-hans/Homebrew>
    - 我的理解：类似 Ubuntu 的 apt-get，CentOS 的 yum。
- 同类常见技术
    - `Fink`
    - `MacPorts`
- 同类技术比较：
    - [Homebrew 和 Fink、MacPort 相比有什么优势？](http://www.zhihu.com/question/19862108)

### 安装

- 先安装 Xcode command line tools：
    - 打开终端，输入：`xcode-select --install `，如果提示已经安装过了那就不用管了。
- **国内源安装推荐文：**
    - 推荐中科大：<https://gitee.com/cunkai/HomebrewCN>
    - 安装完后退出整个软件，然后重新打开再通过 brew 安装其他软件
- 打开终端，复制该命令：`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    - 根据提示，按回车键
    - 根据提示，输入当前用户的密码
    - 终端中提示正在下载和安装 Homebrew，这个时间根据你网速的快慢来决定时间，反正我是很慢，真的很慢，还出现了下载速度 0kb 的状况，然后重新运行了一次就成功。
    - 如果实在下载不了可以这样做：
```
cd /opt && curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install >> brew_install

编辑该安装脚本，
把 
BREW_REPO = "https://github.com/Homebrew/brew".freeze 
替换成：
BREW_REPO = "https://mirrors.ustc.edu.cn/brew.git".freeze

然后执行安装脚本：/usr/bin/ruby /opt/brew_install，中间可能会有这个错误：Error: Failure while executing: git clone https://github.com/Homebrew/homebrew-core 

解决办法：
git clone git://mirrors.ustc.edu.cn/homebrew-core.git/ /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core --depth=1

换源：
cd "$(brew --repo)"
git remote set-url origin https://mirrors.ustc.edu.cn/brew.git


cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git

brew update

安装测试：brew install proxychains-ng
```

- 测试
    - 打开终端，复制该命令：`brew doctor`
        - 如果输出：`Your system is ready to brew.`，则表示安装成功。
- 卸载
    - 先查看你安装过的包列表：`brew list`
    - 打开终端，复制该命令：`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"`
    - 删除目录：`sudo rm -rf /usr/local/Homebrew`
- Homebrew 基本使用
    - 安装指定软件包：`brew install 软件包名称`，安装过程的讲解可以看这篇文章：<https://www.zybuluo.com/phper/note/87055>
    - 卸载指定软件包：`brew uninstall 软件包名称`
    - 更新指定软件包：`brew upgrade 软件包名称`
    - 搜索是否存在对应的软件包：`brew search 软件包名称`
    - 查看对应软件包的信息：`brew info 软件包名称`
    - 清理旧版本的包缓存时：`brew cleanup`
    - 查看你安装过的包列表：`brew list`
    - 更新 Homebrew 在服务器端上的包目录：`brew update`
    - 查看那些已安装的程序需要更新：`brew outdated`
- 使用国内源
    - 中科大
        - <https://lug.ustc.edu.cn/wiki/mirrors/help/brew.git>
        - <https://lug.ustc.edu.cn/wiki/mirrors/help/homebrew-bottles>
    - 清华
        - <https://mirror.tuna.tsinghua.edu.cn/help/homebrew/>
        - <https://mirror.tuna.tsinghua.edu.cn/help/homebrew-bottles/>

- 常用安装软件

```
日常工具：
brew install git zsh vim htop btop wrk telnet curl wget btop cmake

Swift开发相关：
brew install swiftlint swiftgen xcodegen swiftformat


如果安装过程报：git fatal: unsafe repository xxx is owned by someone else 这个错误，解决办法：git config --global --add safe.directory "*"

```

- 官网软件列表（按下载倒序排名）：<https://formulae.brew.sh/api/analytics/install-on-request/90d.json >


-------------------------------------------------------------------


### 安装 Zsh + oh-my-Zsh

- Zsh 官网：<https://www.zsh.org/>
- oh-my-Zsh 官网：<http://ohmyz.sh/>
- 先说下：Zsh 和 oh-my-Zsh 的关系
	- Zsh 是 Shell 中的一种，什么 Shell 你可以再搜索下，简单粗暴讲就是一个：命令解释器，你输入什么命令，它就执行什么，这个东西再 Unix 世界还有其他几个。
	- 由于 Zsh 配置门槛有点高，或者说需要专门花时间去了解 Zsh 才能配置好一个好用的 Zsh，也因为这样，用户也就相对少了。
	- 直到有一天 oh-my-Zsh 的作者诞生，他想要整理出一个配置框架出来，让大家直接使用他的这个公认最好的 Zsh 配置，省去繁琐的配置过程。所以，oh-my-Zsh 就诞生了，它只是会了让你减少 Zsh 的配置，然后又可以好好享受 Zsh 这个 Shell。
- Mac 和一般 Linux 默认的 shell 是 bash，一般人都觉得不好用，我作为一般人，也喜欢 Zsh，所以这里就用 Zsh。
- 为了简化配置 Zsh 过程，我们这里选择 oh-my-Zsh 这个配置库，这是目前大家公认好用的配置。
- 打开终端，先安装 git（已经安装的跳过该步骤），输入命令：`brew install git`
- 打开终端，安装 wget 工具，输入命令：`brew install wget`
- 打开终端，安装 Zsh：`brew install Zsh`
- 打开终端，安装 oh-my-Zsh：`sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`
    - 备用: `sh -c "$(wget https://gitee.com/cdk8s_org/oh-my-zsh/raw/master/tools/install.sh -O -)"`
    - 下载完后，会提示你输入当前登录系统的用户密码，输入完成之后就会从 bash 切换到 Zsh，如果你没有输入密码直接跳过了，可以运行该命令进行手动切换：`chsh -s /bin/Zsh gitnavi(你当前系统用户名)`
    - 切换完成之后，关掉终端，重新打开终端即可
- 如果你需要修改 oh-my-Zsh 的主题，和安装 Zsh 插件，具体可以看我过去整理的这篇文章：[Zsh 入门](https://github.com/judasn/Linux-Tutorial/blob/master/Zsh.md)
- 配置权限：

```
chmod 755 /usr/local/share/zsh
chmod 755 /usr/local/share/zsh/site-functions

```


### Zsh 软件特色

- 不区分大小写智能提示。我是不喜欢大小写区分的那种人，所以用了 zsh 之后，经常按 Tab 进行提示。
- 此外按下 tab 键显示出所有待选项后，再按一次 tab 键，即进入选择模式，进入选择模式后，按 tab 切向下一个选项，按 shift + tab 键切向上一个选项，ctrl+f/b/n/p 可以向前后左右切换。
- kill + 空格键 + Tab键，列出运行的进程，要啥哪个进程不需要再知道 PID 了，当然了 zsh，提供了让你知道 PID 的方法：
	- 比如输入：kill vim，再按下 tab，会变成：kill 5643
- `ls **/*`，分层级地列出当前目录下所有文件及目录，并递归目录
- `ls *.png` 查找当前目录下所有 png 文件
- `ls **/*.png` 递归查找
- zsh 的目录跳转很智能，你无需输入 cd 就可直接输入路径即可。比如：`..` 表示后退一级目录，`../../` 表示后退两级，依次类推。
- 在命令窗口中输入：`d`，将列出当前 session 访问过的所有目录，再按提示的数字即可进入相应目录。
- 给 man 命令增加结果高亮显示：
	- 编辑配置文件：`vim ~/.zshrc`，增加下面内容：

``` bash
# man context highlight
export LESS_TERMCAP_mb=$'\E[01;31m'       # begin blinking
export LESS_TERMCAP_md=$'\E[01;38;5;74m'  # begin bold
export LESS_TERMCAP_me=$'\E[0m'           # end mode
export LESS_TERMCAP_se=$'\E[0m'           # end standout-mode
export LESS_TERMCAP_so=$'\E[38;5;246m'    # begin standout-mode - info box
export LESS_TERMCAP_ue=$'\E[0m'           # end underline
export LESS_TERMCAP_us=$'\E[04;38;5;146m' # begin underline
```

- 刷新配置文件：`source ~/.zshrc`，重新查看 man 的命令就可以有高亮了。
- 常用插件：
    - `git clone --depth=1 https://gitee.com/cdk8s_org/zsh-autosuggestions.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions`
    - `git clone --depth=1 https://gitee.com/cdk8s_org/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting`
    - `vim ~/.zshrc`，在 plugins 修改配置文件为：`plugins=(git zsh-autosuggestions zsh-syntax-highlighting)`
- 最喜欢的主题：`af-magic` 和 `ys`
    - 修改配置文件为：`ZSH_THEME="af-magic"`
- 注意
    - 因为安装 zsh，终端的配置都变了，这时候可能最好重新安装 homebrew 会好一点，或者直接改它源
- 额外增加两个配置
```
ZSH_DISABLE_COMPFIX="true"
DISABLE_AUTO_UPDATE="true"
```



### 关于搭配上 tmux

- 这个我觉得不是人人都需要的东西，如果经常用终端，或是运维人员可以考虑学这个东西，我的资料也是网上找的，你们可以自己找一下。

## vim 知识

- 安装：`brew install vim`
- 下载配置：`curl https://gitee.com/cdk8s_org/vim-for-server/raw/master/vimrc > ~/.vimrc`

-------------------------------------------------------------------

## Proxychains4 为终端做代理

- 保证你本地有一个 socks5 到代理工具，不然下面的方法你无法使用。我这里的工具是：Shadowsocks
- 安装 Proxychains4，输入命令：`brew install proxychains-ng`
- 修改配置文件：`vim /usr/local/etc/proxychains.conf`
    - 在配置文件中找到：`[ProxyList]`（也就是第 111 行的地方），在其下面一行新增一条：`socks5  127.0.0.1 1080 # my vps`
- 测试：`proxychains4 curl www.google.com`，如果你能正常下载到 Google 页面，则表示成功了。以后只要在命令前面加个：proxychains4，即可。
- 修改终端配置，让命令更加简洁：
    - 如果你是 zsh 终端，配置修改：`vim ~/.zshrc`，添加一行：`alias proxy='proxychains4'`
    - 如果你是 bash 终端，配置修改：`vim ~/.bashrc`，添加一行：`alias proxy='proxychains4'`
    - 修改之后，以后要用 proxychains4 执行穿墙命令的话，那就可以这样写：`proxy curl www.google.com`


## 资料整理

- 来自 Google 过程中的资料（真心感谢这些作者）：
	- [Mac 终端命令大全](http://www.jianshu.com/p/3291de46f3ff)
    - <http://wiki.jikexueyuan.com/project/mac-dev-setup/iterm.html>
    - <http://wulfric.me/2015/08/iterm2/>
    - <http://yanghui.name/blog/2015/07/19/make-all-command-through-proxy/>
    - <https://segmentfault.com/a/1190000003001555>
    - <http://www.wklken.me/posts/2015/08/06/linux-tmux.html>
    - <http://www.dreamxu.com/mac-terminal/>
    - <http://zhaozhiming.github.io/blog/2015/11/22/save-and-restore-your-tmux/>
    - <http://cenalulu.github.io/linux/tmux/>
    - <http://blog.csdn.net/gatieme/article/details/49301037>
    - <http://blog.jobbole.com/87278/>
    - <http://wulfric.me/2015/08/zsh/>
    - <http://hujiandong.com/2016/09/11/iterm2/>
    - <http://www.jianshu.com/p/68ef9d2e1653>
    - <http://swiftcafe.io/2015/07/25/iterm/>


