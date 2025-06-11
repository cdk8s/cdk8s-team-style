
## APT 类系统（Debian、Ubuntu、Kali Linux、Raspberry）


#### 常用

```
sudo apt install -y git vim htop wrk telnet curl wget zsh

```

#### Zsh 配置

```
- 常用插件：
    - `git clone --depth=1 https://gitee.com/cdk8s_org/zsh-autosuggestions.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions`
    - `git clone --depth=1 https://gitee.com/cdk8s_org/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting`
    - `vim ~/.zshrc`，在 plugins 修改配置文件为：`plugins=(git zsh-autosuggestions zsh-syntax-highlighting)`
- 最喜欢的主题：`af-magic` 和 `ys`
    - 修改配置文件为：`ZSH_THEME="af-magic"`

- 额外增加两个配置
ZSH_DISABLE_COMPFIX="true"
DISABLE_AUTO_UPDATE="true"

```

#### 中文输入法

```
安装搜狗
官网安装方法：https://shurufa.sogou.com/linux/guide
sudo apt update
sudo apt-get install fcitx
安装输入法依赖
sudo apt install libqt5qml5 libqt5quick5 libqt5quickwidgets5 qml-module-qtquick2 libgsettings-qt1
sudo dpkg -i ./sogoupinyin_4.0.1.2800_x86_64.deb
如果安装过程中提示缺少相关依赖，则执行如下命令解决：
sudo apt -f install
设置fcitx开机自启动
在终端执行sudo cp /usr/share/applications/fcitx.desktop /etc/xdg/autostart/
卸载系统ibus输入法框架
在终端执行 sudo apt purge ibus
后重启电脑，按 Ctrl + 空格切换输入法
记得在搜狗中去掉不要的快捷键，比如 ctrl + shift + f 切换简繁体
理论上重启电脑后是不需要做任何配置的，如果发现还没出现，可以这样操作：
打开：左上角开始面板》设置》设置管理器 》Fcitx配置》必须列表中有搜狗输入法
搜狗自定义短语位置，一共有2个地方，但是改了不会同步到软件中，重启后也无效，暂时没有办法
/home/meek/.config/sogoupinyin/dict/PCPYDict/phrase/PhraseEdit.txt
/home/meek/.config/sogoupinyin/dict/PCWBDict

```

#### VSCode

```
官网说明：https://code.visualstudio.com/docs/setup/linux

sudo apt-get install wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
arm架构：sudo sh -c 'echo "deb [arch=arm64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
x64架构：sudo sh -c 'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg

sudo apt install apt-transport-https
sudo apt update
sudo apt install code


```


#### 截图软件

```

安装截图软件：
sudo apt-get install shutter

```

#### Edge 浏览器

```
安装 edge 浏览器，登录微软账号，可以同步浏览器配置
```

#### 剪切板

```
CopyQ：https://github.com/hluk/CopyQ/releases
```


#### 系统监控


```
显示 CPU、GPU 温度
先安装它：sudo apt install lm-sensors hddtemp
实时运行：watch sensors
能看到硬盘、CPU、GPU、电源、内存、瓦数等信息

传感器检测
sh -c "yes|sensors-detect"


推荐的 GUI 上的查看温度信息软件：
sudo apt-get install psensor
然后这个在右上角面板中增加：传感器插件，显示CPU、GPU 温度


也可以用这个：
sudo apt install hardinfo
命令打开；hardinfo

```


-------------------------------------------------------------------

## YUM 类系统（CentOS、Fedora、openSUSE）



#### VSCode

```
官网说明：https://code.visualstudio.com/docs/setup/linux

sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'

dnf check-update
sudo dnf install code

yum check-update
sudo yum install code
```

