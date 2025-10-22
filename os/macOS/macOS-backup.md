
# macOS 在线重装

- 该文件已废弃，已腾讯文档记录为主

### 先备份

- 记录已安装软件列表
- 记录 Edge 浏览器安装的扩展
- 备份桌面文件/文件夹
- 备份 MySQL、Mongo、Elasticsearch 数据库数据，以及连接信息
  - dbeaver: `/Users/meek/Library/DBeaverData/workspace6/General/.dbeaver`
- **备份本地数据库表数据**
- 百度云盘下载到一半的文件
- 输入法自定义词库
- 备份浏览器书签
- 导出 SSH 配置（包括密钥是 pem 文件）
- 备份 Chrome 扩展列表
    - 包括 Proxy SwitchyOmega 配置
- 备份用户目录下的 .ssh 信息
- 视频剪辑素材
- 解压的绿色软件
- 代码目录
- 备份 Jump Desktop 连接信息
- QQ 和微信等聊天工具的记录
- 备份 zshrc
- 备份 Switch Host 配置
- 备份 IntelliJ IDEA 等 IDE 配置: `/Users/meek/Library/Application Support/JetBrains`
- 备份 .m2 下的 maven 配置和完整本地仓库
- 备份 docker 数据映射目录
- 备份 Bob 翻译配置
- 备份 Surge 配置

### 安装

- 官网文档：<https://support.apple.com/zh-cn/HT204904>
- 我旧 macbook 是 10.13 版本，现在要升级到 10.15，现在已经找不到 10.15 原 dmg 了，所以只能先 App Store 下载 Catalina 安装。
- 但是这种安装会保留我旧软件，所以我只能先升级，然后选择：关机 > Command (⌘)-R 进入 "macOS 实用工具界面"，主要有功能："重新安装 macOS、磁盘工具"
- 我先进入 "磁盘工具" 中删除我原有的系统卷宗（我原本就分了 2 个卷宗），然后重新创建一个 APFS 类型的新卷宗（不要选择 APFS 区分大小写，目前有些 Adobe 坑爹软件不支持），重新回到 "macOS 实用工具界面"，选择 "重新安装 macOS"
- 很早以前的离线 U 盘安装现在没了，最新的系统已经很难再找到官网的纯 dmg 镜像了