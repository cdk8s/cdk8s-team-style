
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



如何运行 appimage 软件（不需要安装）
appimage 本身就已经是一个无需安装的软件，所以想把它从你的机器上移除，只需要把 appimage 删除就行了
chmod +x software.AppImage
./software.AppImage

安装视频播放器：
sudo apt install -y vlc



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