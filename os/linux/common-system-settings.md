
## 基础操作

```
查看 Linux 內核、Debian 系统版本
cat /proc/version
Linux version 5.18.0-kali5-amd64 (devel@kali.org) (gcc-11 (Debian 11.3.0-3) 11.3.0, GNU ld (GNU Binutils for Debian) 2.38) #1 SMP PREEMPT_DYNAMIC Debian 5.18.5-1kali6 (2022-07-07)

强制使用简单密码：
终端输入：
openssl passwd -6 -salt $(< /dev/urandom tr -dc '[:alnum:]' | head -c 32)
输入新密码，比如：aa
得到：
$6$utqcYT2jklngQCW6$2FtCAFKwn1uq6z.VLRiI9KOmVujNJFyh8gnn3Uhzg5ZoJrat/4.nxZySYow20HegwC3muCduq1ov0RYtjPJQx0

修改配置：sudo vim /etc/shadow
把这一行注释：#meek:$y$j9T$7q2qN9sc7QZV.X2QV4XRm0$ZapMUSZuF3W..Z5h99EbL.E8vCXWV.3GGwNemJK.zsA:19301:0:99999:7:::
改为这个新密码：meek:$6$utqcYT2jklngQCW6$2FtCAFKwn1uq6z.VLRiI9KOmVujNJFyh8gnn3Uhzg5ZoJrat/4.nxZySYow20HegwC3muCduq1ov0RYtjPJQx0:19301:0:99999:7:::


安装的时候是没有让你设置 root 密码的，所以先设置 root 密码
sudo passwd root


开启远程 SSH：
vim /etc/ssh/sshd_config
该值改为：PasswordAuthentication yes
保存

service ssh start  重启
service ssh status  状态是否正常运行
update-rc.d ssh enable 添加开机启动

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