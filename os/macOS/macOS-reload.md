

# macOS 离线重装

### 备份

- 记录已安装软件列表
- 备份桌面文件/文件夹
- 备份 MySQL、Mongo、Elasticsearch 数据库数据，以及连接信息
- 百度云盘下载到一半的文件
- 输入法自定义词库
- 备份浏览器书签
- 导出 SSH 配置
- 备份 Chrome 扩展列表
    - 包括 Proxy SwitchyOmega 配置
- 备份用户目录下的 .ssh 信息
- QQ 和微信等聊天工具的记录
- 备份 zshrc

### 最新系统下载，制作 U 盘启动盘

- 当前时间（202009）最新正式版系统为：macOS Catalina 10.15（最新预览版是 macOS Big Sur）
- 找一台可以联网的苹果电脑，打开 Apple Store，搜索 Catalina，搜索结果第一个应该就是系统镜像，差不多 5GB 大小，然后点击下载。下载完成之后不要点安装，直接退出。
- 插入 U 盘到 macbook，打开 "应用程序 → 实用工具 → 磁盘工具"，将U盘「抹掉」(格式化) 成「Apple 文件系统 (APFS 区分大小写)：macOS 10.13 或后续版本使用的文件系统」格式、GUID 分区图
- 把 U 盘右键重命名为：thismyupan
- 打开终端，输入命令：

```
sudo /Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia --volume /Volumes/thismyupan
```

### 开始重装

- 有了启动盘后：按下电源键开机，当听到 "噹" 的一声时，按住 Option 键不放，直到出现启动菜单选项
- 这时选择安装U盘 (黄色图标) 并回车，就可以开始安装了，在过程中你可以通过"磁盘工具"对 Mac 的磁盘式化或者重新分区等操作。
- 选择：磁盘工具，建议格掉旧安装盘。然后我习惯会分卷宗。我一般有两个卷宗。
- 第一个是用来安装系统，第二个是存放代码文件。
- 选择：重新安装 macOS，继续，选择安装的卷宗。

