

# macOS 终端方案 iTerm2 + Zsh + vim + Homebrew


## 总结

- iTerm2 比 Mac 默认的 Terminal 终端好用，配合 Zsh 确实更加得体
- **牢记：** 装了 zsh 之后，修改终端配置就变成了：`vim ~/.zshrc`，而不是：`vim ~/.bash_profile`，所以以后看到别人的文章中需要：`vim ~/.bash_profile`，那你自己要变通思想过来。
- 同时更新修改后的配置文件也从：`source ~/.bash_profile`，变成了：`source ~/.zshrc`，当然还有其他取取巧方式，这里不谈。



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
- 国内源安装推荐文：<https://zhuanlan.zhihu.com/p/111014448>
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
    - 打开终端，复制该命令：`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"`
    - 删除目录：`sudo rm -rf /usr/local/Homebrew`
- Homebrew 基本使用
    - 安装指定软件包：`brew install 软件包名称`，安装过程的讲解可以看这篇文章：<https://www.zybuluo.com/phper/note/87055>
    - 卸载指定软件包：`brew uninstall 软件包名称`
    - 更新指定软件包：`brew upgrade 软件包名称`
    - 搜索是否存在对应的软件包：`brew search 软件包名称`
    - 查看对应软件包的信息：`brew info 软件包名称`
    - 更新 Homebrew 在服务器端上的包目录：`brew update`
    - 清理旧版本的包缓存时：`brew cleanup`
    - 查看你安装过的包列表：`brew list`
    - 更新 Homebrew 在服务器端上的包目录：`brew update`
    - 查看那些已安装的程序需要更新：`brew outdated`
- 使用国内源
    - 默认的源实在速度有够慢的
    - 中科大
        - <https://lug.ustc.edu.cn/wiki/mirrors/help/brew.git>
        - <https://lug.ustc.edu.cn/wiki/mirrors/help/homebrew-bottles>
    - 清华
        - <https://mirror.tuna.tsinghua.edu.cn/help/homebrew/>
        - <https://mirror.tuna.tsinghua.edu.cn/help/homebrew-bottles/>



-------------------------------------------------------------------


## iTerm2 知识

### iTerm2 是什么

- iTerm2 官网：<http://iterm2.com/>
- wiki 介绍：<https://en.wikipedia.org/wiki/ITerm2>

### 安装 iTerm2

- 在安装之前先说下前提，你的 Mac 必须装有：Homebrew，等下 zsh 要用到。
- 下载 iTerm 2
    - 当前时间（2016-10-31）最新版为：3.0.10
    - 下载地址，官网：<https://iterm2.com/>
- 安装 iTerm 2
    - 官网下载下来是一个 zip 压缩包，解压出来有一个 `.app` 文件，双击运行即可安装，或是拖到应用程序里面。
- 更改配色方案
    - 目前大家喜欢设置的配色方案为 solarized，iTerm2 默认是有带的，如果没有则访问：<https://github.com/altercation/solarized>
        - 在项目中找到 solarized/iterm2-colors-solarized 目录，下面有两个文件：Solarized Dark.itermcolors 和 Solarized Light.itermcolors，双击这两个文件就可以把配置文件导入到 iTerm 里了。
    - 更改后的配色最终效果如下图：已经截图了。同时还要再切换到 Text 标签，把 `Draw bold text in bold font` 的勾去掉。
    - <a href= "http://img.youmeek.com/2016/Mac-iTerm2-1.jpg" class="foobox"><img src="http://img.youmeek.com/2016/Mac-iTerm2-1.jpg" alt="iTerm2介绍"></a>


### iTerm2 软件特色

- 智能选中
    - 在 iTerm2 中，连续双击选中，连续三击选中整行，连续四击智能选中（智能规则可配置），可以识别网址，引号引起的字符串，邮箱地址等。
	- 在 iTerm2 中，选中即复制。即任何选中状态的字符串都被放到了系统剪切板中。
- Hotkey Window (快速调出窗口)
	- 这个非常好用，默认是没有设置，需要自己设置下。
	- 实际使用时我们经常会遇到这种场景：有时候只是执行几行命令，然后就不再使用它。可是我们还是必须要打开终端，使用完成后关闭它。但是用 iTerm2 这个功能只要按快捷键，出来虚化的终端，输入命令，然后再把光标放在其他地方自动就消息了。
	- 设置和效果如下图：
	    - <a href= "http://img.youmeek.com/2016/Mac-iTerm2-2.jpg" class="foobox"><img src="http://img.youmeek.com/2016/Mac-iTerm2-2.jpg" alt="iTerm2介绍"></a>
	    - <a href= "http://img.youmeek.com/2016/Mac-iTerm2-3.jpg" class="foobox"><img src="http://img.youmeek.com/2016/Mac-iTerm2-3.jpg" alt="iTerm2介绍"></a>
- iTerm2 常用快捷键
	- 这篇文章配了很多图，如果你想更加具体地了解可以看这篇文章，我不想截图了：<http://swiftcafe.io/2015/07/25/iterm/>

|快捷键|介绍|
|:---------|:---------|
|输入的命令开头字符 + Command + ;|根据输入的前缀历史记录自动补全|
|Command + ;|根据历史记录自动补全|
|Command + [ 或 command + ]|切换屏幕|
|Command + enter|进入全屏模式，再按一次返回|
|Command + 鼠标单击|可以打开文件，文件夹和链接（iTerm2 是可以对显示的内容进行点击的哦）|
|Command + n|新建新的 Window 窗口|
|Command + t|新建标签页|
|Command + w|关闭当前标签或是窗口|
|Command + d|竖直分屏|
|Command + r|清屏|
|Command + /|按完之后，整个屏幕变成白茫茫的，而光标位置是一个小圆圈清除显示出来|
|Command + 方向键|切换标签页|
|Command + 数字|切换到指定数字标签页|
|Command + f|查找，所查找的内容会被自动复制 ,输入查找的部分字符，找到匹配的值按 tab，即可复制，带有补全功能|
|Command + option + e|全屏并排展示所有已经打开的标签页，带有可以搜索。|
|Command + Option + b|历史回放，类似视频录像的东西，有记录你最近时间内的操作。有一个类似播放器的进度条可以拖动查看你做了什么。存放内容设置（Preferences -> Genernal -> Instant Replay）。|
|Command + Option + 数字|切换 Window 窗口|
|Command + shift + d |水平分屏|
|Command + shift + h|查看剪贴板历史，在光标位置下方会出现一列你输入过的历史记录|
|Command + Shift + m|可以保存当前位置，之后可以按Command + Shift + j跳回这个位置。|
|Command + shift + alt + w|关闭所有窗口|
|Control + u|清空当前行，无论光标在什么位置|
|Control + a|移动到行首|
|Control + e|移动到行尾|
|Control + f|向前移动，相当于方向键右|
|Control + b|向后移动，相当于方向键左|
|Control + p|上一条命令，相当于方向键上|
|Control + n|下一条命令，相当于方向键下|
|Control + r|搜索历史命令|
|Control + y|召回最近用命令删除的文字|
|Control + h|删除光标之前的字符|
|Control + d|删除光标所在位置的字符|
|Control + w|删除光标之前的单词|
|Control + k|删除从光标到行尾的内容|
|Control + c|结束当前状态，另起一行|
|Control + t|交换光标和之前的字符|


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
- 打开终端，安装 oh-my-Zsh：`sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-Zsh/master/tools/install.sh -O -)"`
    - 下载完后，会提示你输入当前登录系统的用户密码，输入完成之后就会从 bash 切换到 Zsh，如果你没有输入密码直接跳过了，可以运行该命令进行手动切换：`chsh -s /bin/Zsh gitnavi(你当前系统用户名)`
    - 切换完成之后，关掉终端，重新打开终端即可
- 如果你需要修改 oh-my-Zsh 的主题，和安装 Zsh 插件，具体可以看我过去整理的这篇文章：[Zsh 入门](https://github.com/judasn/Linux-Tutorial/blob/master/Zsh.md)

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
    - `git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions`
    - `git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting`
    - `vim ~/.zshrc`，在 plugins 里面换行，分别添加：zsh-autosuggestions，zsh-syntax-highlighting
- 最喜欢的主题：`ys`

### 关于搭配上 tmux

- 这个我觉得不是人人都需要的东西，如果经常用终端，或是运维人员可以考虑学这个东西，我的资料也是网上找的，你们可以自己找一下。

## vim 知识

- 安装：`brew install vim`
- 下载配置：`curl https://raw.githubusercontent.com/wklken/vim-for-server/master/vimrc > ~/.vimrc`

-------------------------------------------------------------------

## Proxychains4 为终端做代理

- 保证你本地有一个 socks5 到代理工具，不然下面的方法你无法使用。我这里的工具是：Shadowsocks
- 安装 Proxychains4，输入命令：`brew install proxychains-ng`
- 修改配置文件：`vim /usr/local/etc/proxychains.conf`
    - 在配置文件中找到：`[ProxyList]`（也就是第 111 行的地方），在其下面一行新增一条：`socks5  127.0.0.1 1080 # my vps`
- 测试：`proxychains4 curl www.google.com`，如果你能正常下载到 Google 页面，则表示成功了。以后只要在命令前面加个：proxychains4，即可。
- 修改终端配置，让命令更加简洁：
    - 如果你是 zsh 终端，配置修改：`vim ~/.zshrc`，添加一行：`alias proxy='proxychains4'`
    - 如果你是 bash 终端，配置修改：`vim ~/.bash_profile`，添加一行：`alias proxy='proxychains4'`
    - 修改之后，以后要用 proxychains4 执行穿墙命令的话，那就可以这样写：`proxy wget google.com`


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


