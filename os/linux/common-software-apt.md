
# 支持 Debian、Ubuntu、Kali Linux


```
安装先关:
Kali Linux 安装，使用完全软件镜像，安装过程选择安装所有软件，使用 DOS 界面安装，因为在 2022.3 版本上，遇到用图形化安装中间总是半途黑屏，没办法安装完所有软件
建议首次接触，使用中文作为系统语言。

Ubuntu 安装过程不推荐勾选网络下载相关包，不推荐做安装过程升级软件，时间长，又不好用。


Debain 的 Xfce 的顶部一栏叫做：面板
```




## conda 和 pip 区别

```

尽量使用conda的环境隔离功能，为不同的任务创建不同的环境
一般原则，在新环境中，如果装多个packages，既用到conda，又用到pip，那就先conda 的都装好，再pip
conda有严格的检查机制，可以保证你下载的依赖版本一定可以工作，pip不行。
pip的一个好处是可以安装时既检查conda安装过package的也检查pip安装过的package。不过，它只负责要什么装什么，不负责能不能把装的一堆packages打通
有一些package 作者只会发布pip而没有发布conda版的


官网介绍：https://www.anaconda.com/blog/understanding-conda-and-pip
pip是用来安装python包的，安装的是python wheel或者源代码的包。从源码安装的时候需要有编译器的支持，pip也不会去支持python语言之外的依赖项。
conda是用来安装conda package，虽然大部分conda包是python的，但它支持了不少非python语言写的依赖项，比如mkl cuda这种c c++写的包。然后，conda安装的都是编译好的二进制包，不需要你自己编译。所以，pip有时候系统环境没有某个编译器可能会失败，conda不会。这导致了conda装东西的体积一般比较大，尤其是mkl这种，动不动几百兆甚至一G多。
然后，conda功能其实比pip更多。pip几乎就是个安装包的软件，conda是个环境管理的工具。conda自己可以用来创建环境，pip不能，需要依赖virtualenv之类的。意味着你能用conda安装python解释器，pip不行。这一点我觉得是conda很有优势的地方，用conda env可以很轻松地管理很多个版本的python，pip不行。
conda和pip对于环境依赖的处理不同，总体来讲，conda比pip更加严格，conda会检查当前环境下所有包之间的依赖关系，pip可能对之前安装的包就不管了。这样做的话，conda基本上安上了就能保证工作，pip有时候可能装上了也不work。不过我个人感觉这个影响不大，毕竟主流包的支持都挺不错的，很少遇到broken的情况。这个区别也导致了安装的时候conda算依赖项的时间比pip多很多，而且重新安装的包也会更多（会选择更新旧包的版本）。
最后，pip的包跟conda不完全重叠，有些包只能通过其中一个装。
```

## 常用软件

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

新安装的 vscode deb 包默认已经可以在终端中直接使用 code 命令了，功能也更加齐全
卸载默认的 code-oss，下载最新的
查看已安装情况：apt list | grep code-oss
卸载： sudo apt remove --purge code-oss


安装截图软件：
sudo apt-get install shutter

安装 edge 浏览器，登录微软账号，可以同步浏览器配置

如何运行 appimage 软件（不需要安装）
appimage 本身就已经是一个无需安装的软件，所以想把它从你的机器上移除，只需要把 appimage 删除就行了
chmod +x software.AppImage
./software.AppImage

安装视频播放器：
sudo apt install -y vlc

- 安装剪切板
- 命令：`sudo apt-get install parcellite`
- 修改快捷键：`右键软件 | 首选项 | Hotkeys | 历史记录按键组合`


安装 Peek（Gif 录制）
- 自己构建 deb 包安装
sudo apt install cmake valac libgtk-3-dev libkeybinder-3.0-dev libxml2-utils gettext txt2man
git clone https://github.com/phw/peek.git --depth=1
mkdir peek/build
cd peek/build
cmake -DCMAKE_INSTALL_PREFIX=/usr -DGSETTINGS_COMPILE=OFF ..
make package

sudo dpkg -i peek-*-Linux.deb

```



## GPU 监控

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


先使用：`nvidia-smi -l 1` 命令查看GPU使用率、显存使用
    - 显示的表格第一格是风扇转速、温度、能耗瓦数信息，Perf：性能状态，从P0到P12，P0表示最大性能，P12表示状态最小性能（即 GPU 未工作时为P0，达到最大工作限度时为P12）
    - 第二格是显存占用，第三格是GPU使用率

如果GPU使用率为0优先检查代码是否调用了GPU进行计算。如果GPU使用率已经为90%+，则可以考虑换多卡并行或更高算力的GPU。
nvidia-smi是Nvidia显卡命令行管理套件，基于NVML库，旨在管理和监控Nvidia GPU设备。
这里推荐一个好用的小工具：gpustat,直接pip install gpustat即可安装，gpustat基于nvidia-smi，可以提供更美观简洁的展示，结合watch命令，可以动态实时监控GPU的使用情况。
watch --color -n1 gpustat -cpu 

使用nvidia-smi命令检查GPU的使用情况，如果发现程序已经关闭了但是还有显存占用，说明有残留进程占用了显存，可以进行 kill：
ps -ef | grep mySoftwareName | awk '{print $2}' | xargs kill -9


如果GPU占用率为0说明代码可能没有使用GPU，需检查代码。
如果GPU占用率忽高忽低、占用率峰值在50%以下，那么可能是数据预处理跟不上GPU的处理速度，你可以排查：
假设您的实例核心数为5，如果CPU占用率接近500%（即5个核心都正在高负载使用）那么可能是CPU数量不够，CPU出现了瓶颈，此时您可以迁移实例到更高CPU数量的主机上去或者升配。如果CPU占用率远没有达到500%的，
说明您的代码没有把CPU的算力压榨出来，一般可以通过修改Torch Dataloader中的worker_num提高CPU负载，经验值num_worker = 略小于核心数量，最好测试不同worker num值对性能的影响。


可以通过这个性能优化文档上的 python 脚本进行调试：https://www.autodl.com/docs/perf/


如果上述步骤都没有解决问题，那么请调试代码，找到耗时的代码行做进一步分析。通常代码级别有几种常见的对性能有影响的写法，请自查：
每次迭代中做一些与计算无关的操作。比如保存测试图片等等，解决办法是拉长保存测试图片的周期，避免每次迭代都做额外耗时的操作
频繁保存模型，导致保存模型占用了训练过程一定比例的时间
PyTorch的官方性能优化指南：https://pytorch.org/tutorials/recipes/recipes/tuning_guide.html
TensorFlow的官方性能优化指南：https://www.tensorflow.org/guide/function
```

## 使用 GPU 计算


```
查看显卡信息：lspci | grep -i vga
显示当前GPU：hashcat -I
测试性能：hashcat -b

不采用 GPU 解密：multiforcer -h MD5 -f ~/my_test/md5_test.txt -u charsetfile --threads 512 --blocks 512 -m 500
采用 GPU 解密：multiforcer -h MD5 -f ~/my_test/md5_test.txt -u charsetfile --nocpu
如果报错：Multiforcer：error while loading shared libraries: libcudart.so.4: cannot open shared object file: No such file or directory

查看下本机 libcudart.so.4 文件的位置：locate  libcudart.so.4
切换到 root 用户，然后执行：echo '/usr/lib64/' >> /etc/ld.so.conf
让链接生效：ldconfig


```

## AMD 显卡驱动相关

```


AMD rx560 驱动下载：
https://www.amd.com/zh-hans/support/graphics/radeon-500-series/radeon-rx-500-series/radeon-rx-560
但是只支持 ubuntu 下载，又因为 ubuntu 也是基于 debian 的，所以可以在 ubuntu 上输入：cat /proc/version，查看其基于哪个 debian，再和自己的 kali linux 对比 debian 就可以确定可以安装哪个了
Debian 11 对应的 ubuntu 20、21
Debian 12 对应的 ubuntu 22

AMD rx5600xt 驱动下载：
https://www.amd.com/zh-hans/support/graphics/amd-radeon-5600-series/amd-radeon-rx-5600-series/amd-radeon-rx-5600-xt

下载下来的是 deb 文件，文件很小，
安装：sudo apt install ./amdgpu-install_22.20.50200-1_all.deb
安装完后会在在该路径有具体安装脚本：
/usr/bin/amdgpu-install

AMD 官网驱动安装说明：
https://amdgpu-install.readthedocs.io/en/latest/index.html

目前官网脚本是不支持 kali linux 安装的，需要修改脚本，在 288 行 function os_release() 方法中的 294 行改为 ubuntu|linuxmint|debian|kali
默认全部安装的是否已经带了，只支持 ubuntu 安装

查看帮助文档：amdgpu-install -h
可以看到目前 --opencl 只支持 legacy、rocr 参数了
开始安装：amdgpu-install -y --opencl=rocr,legacy


```

## 软件图标设置

```
# Ubuntu 给 Dash 添加程序图标
 进入图标存放目录|：`cd /usr/share/applications`
- 创建文件并编辑：`sudo gedit pycharm.desktop`

[Desktop Entry]
Name=Pycharm
Name[zh_CN]=Pycharm
Comment=Pycharm3:The Python IDE
Exec=/pycharm-community-2017.1.1/bin/pycharm.sh
Icon=/pycharm-community-2017.1.1/bin/pycharm.png
Terminal=false
Type=Application
Categories=Application;
Encoding=UTF-8
StartupNotify=true

- 重点参数说明（注意：路径使用完整路径）
    - Name 为你想要显示在 Launcher 中的名称
    - Comment 为说明。
    - Exec 为程序执行位置
    - Icon 为图标所在路径
- 最后，打开 Dash，在顶部搜索框搜索 **pycharm**，此时你应该能搜到它，先单击试一下看能不能打开，如果可以打开，拖到该图标启动器上，下次就可以直接从启动器打开了


从 /usr/share/applications 目录一个已有的 desktop 文件到 /home/meek/desktop 目录下
修改为 idea.desktop，内容如下：
[Desktop Entry]
Version=2022.2.3
Type=Application
Name=IDEA
Comment=IntelliJ IDEA
Exec=/home/meek/my_software/idea-IU-222.4345.14/bin/idea.sh
Terminal=false
Icon=/home/meek/my_software/idea-IU-222.4345.14/bin/idea.png
Categories=Development;
Kali Linux 可以把这个文件拖动到顶部面板栏
Ubuntu 需要对文件图标右键 >> 选择:Allow Lauching。添加到左边栏：右键已经运行的软件 >> 添加到喜爱，即可

IntelliJ IDEA 破解：
修改配置 idea-IU-222.4345.14/bin/idea64.vmoptions

IntelliJ 系列软件也有直接穿件功能：工具 > 穿件桌面条目

```


## Kali Linux 桌面设置

```

对多显示器场景的额外设置
打开：左上角开始面板》设置》设置管理器 》显示
在这里可以设置多个显示器排列顺序、主显示器、分辨率、镜像等


设置桌面
打开：左上角开始面板》设置》设置管理器 》桌面
可以设置壁纸，不同显示器壁纸各自设置
在 “图标” 选项中勾选 “在主显示器上显示图标”



新安装的 deb 软件在：左上角开始面板》全部应用程序》找到刚刚安装软件》拖动新安装软件图标到任务栏上



在右上角显示网速：
右键右上角的面板 》面板》添加新项目》网络监视器
还有一个 “Clipman 剪切板管理器” 也很好用


主题
打开：左上角开始面板》设置》设置管理器 》外观
建议使用白色主题风格

黑色任务栏
打开：左上角开始面板》设置》设置管理器 》面板》外观》暗黑模式


鼠标光标变大，方便寻找
打开：左上角开始面板》设置》设置管理器 》鼠标和触摸板》主题》光标大小



```

## Java 环境配置

```
maven 安装配置，因为 kali linux 默认安装了 zsh，所以这里需要该它的配置：
vim ~/.zshrc
# Maven
MAVEN_HOME=/home/meek/my_software/apache-maven-3.8.6
M3_HOME=/home/meek/my_software/apache-maven-3.8.6
PATH=$PATH:$M3_HOME/bin
MAVEN_OPTS="-Xms556m -Xmx1056m"
export M3_HOME
export MAVEN_HOME
export PATH
export MAVEN_OPTS

- 刷新配置文件：source ~/.zshrc
- 测试是否安装成功：mvn -version



额外安装的一些软件
sudo apt install htop curl wget wrk telnet

安装 finalsshell
官网：http://www.hostbuf.com/t/1059.html
命令：
rm -f finalshell_install_linux.sh ;wget www.hostbuf.com/downloads/finalshell_install_linux.sh;chmod +x finalshell_install_linux.sh;./finalshell_install_linux.sh;


自带的 DBeaver 版本太老了，下载最新：
官网：https://dbeaver.io/download/ 
sudo apt remove --purge dbeaver
sudo apt install ./dbeaver-ce_22.2.3_amd64.deb 

还需要链接的时候，还需要对 “本地客户端” 进行选择，点击 “浏览”，添加 /usr/bin 目录
没做这一步可能会导致无法导入 sql 脚本



自带的 mysql 是 mariadb
先卸载：sudo apt remove --purge mariadb-*

下载：https://dev.mysql.com/downloads/mysql/
mysql-server_8.0.31-1debian11_amd64.deb-bundle.tar
解压后，名字含有 test 的包都可以删除掉，只留下：
libmysqlclient21_8.0.31-1debian11_amd64.deb
libmysqlclient-dev_8.0.31-1debian11_amd64.deb
mysql-client_8.0.31-1debian11_amd64.deb
mysql-common_8.0.31-1debian11_amd64.deb
mysql-community-client_8.0.31-1debian11_amd64.deb
mysql-community-client-core_8.0.31-1debian11_amd64.deb
mysql-community-client-plugins_8.0.31-1debian11_amd64.deb
mysql-community-server_8.0.31-1debian11_amd64.deb
mysql-community-server-core_8.0.31-1debian11_amd64.deb
mysql-community-server-debug_8.0.31-1debian11_amd64.deb
mysql-server_8.0.31-1debian11_amd64.deb

安装所有：
sudo apt install ./*.deb
然后会进入 DOS 交互式安装界面：
1. 让你输入 root 密码
2. 让你选择密码身份插件，为了方便兼容早期版本，我选择：
    Use Legacy Authentication Method

安装好后：
systemctl start mysql
systemctl enable mysql
```