
# macOS 下 Java + Docker 开发环境

## Git

- 官网下载：<http://git-scm.com/download/mac>
- 安装过程和 Windows 没啥区别，都是下一步下一步。
- IntelliJ IDEA 对 Git 的支持很好，也不需要额外配置什么，IntelliJ IDEA 的 Git 操作都很便捷强烈使用 IntelliJ IDEA 作为 Git 的 GUI 操作工具。
- **Homebrew 方式（推荐）**：`brew install git`

## JDK

- 官网下载 JDK7：<http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html>
- 官网下载 JDK8：<http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html>
- Java 开发环境理论上一般都是这个优先安装的。
- 安装过程和 Windows 没啥区别，都是下一步下一步，只是比 Windows 简单，连安装路径都不需要改而已，所以这里不截图了。
- 我这边不管是 Windows、Mac、Linux，只要开发环境，JAVA_HOME 我都是 JDK8，同时还装有 JDK6、JDK7，在使用 IntelliJ IDEA 的时候，我可以同时使用三个版本的 JDK。
- JDK 的环境变量是要添加的，我这边可以贴一下。
- 在本系列前面的章节中我已经说明了，我这边是 Zsh 环境，所以我需要编辑这个配置文件：`vim ~/.zshrc`
- 如果你是 bash，你需要编辑的是这个：`vim ~/.bash_profile`
- 修改后之后刷新配置文件我是：`source ~/.zshrc`

``` bash
# JDK 1.8
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_112.jdk/Contents/Home
JRE_HOME=$JAVA_HOME/jre
PATH=$PATH:$JAVA_HOME/bin
CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
export JAVA_HOME
export JRE_HOME
export PATH
export CLASSPATH
```

- 卸载 JDK

``` bash
sudo rm -rf /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin

sudo rm -rf /Library/PreferencePanes/JavaControlPanel.prefPane

sudo rm -rf /Library/Java/JavaVirtualMachines/jdk1.8.0_112.jdk
```

## IntelliJ IDEA

- 官网下载：<http://www.jetbrains.com/idea/>
- 最优秀的 IDE，没有之一，我所有的生产力硬件设备都是为了支持它而购买的，所以内存一定要够大。
- 下面的 Maven、Tomcat 都是依赖于 IntelliJ IDEA 运行的，所以本质上我只要搞定 IntelliJ IDEA，其他的 Java 开发环境 IntelliJ IDEA 都会帮我们解决。
- 关于 IntelliJ IDEA Mac 下安装/配置等相关，请看我写的这个系列，里面有详细说明：[IntelliJ IDEA 简体中文专题教程](https://github.com/judasn/IntelliJ-IDEA-Tutorial)
- 在 IntelliJ IDEA 有几个特别的地方我单独拿出来讲讲吧：
	- 如果启动 Tomcat 的时候报：`Permission denied`，你则可以：打开终端，进入 Tomcat\bin 目录，然后执行：`chmod 777 *.sh`
	- 如果启动 Tomcat 之后，控制台乱码了，并且你确认你在 IntelliJ IDEA 的 Preferences 中设置的控制台字体是支持中文的，那你可以尝试下在 Tomcat VM 参数上加上：`-Dfile.encoding=UTF-8`
	- Git 的路径配置：`Preferences -- Version Control -- Git -- Path to Git executable` 的值是：`/usr/local/git/bin/git`
	- 如果你已经看过前面的：[一个Java程序员眼中的Mac OS（系列六：终端方案iTerm2 + Zsh）](http://code.youmeek.com/2016/11/29/2016/11/Mac-iTerm2/)，假设你也已经安装了 zsh
		- 那你的 IntelliJ IDEA 终端路径可以改成 zsh 的，配置方法在 `Preferences -- Tools -- Terminal -- Shell path` 的值改为是：`/bin/zsh`
- IntelliJ IDEA 在 Mac 下的配置文件保存路径
	- 下面内容中：`XXXXXX`，表示 IntelliJ IDEA 的版本号，IntelliJ IDEA 的配置目录是跟版本号有关系的。
	- `/Users/你的用户名/Library/Application Support/IntelliJIdeaXXXXXX`，用于保存安装的插件
	- `/Users/你的用户名/Library/Caches/IntelliJIdeaXXXXXX`，用于保存缓存、日志、以及本地的版本控制信息（local history 这个功能）
	- `/Users/你的用户名/Library/Preferences/IntelliJIdeaXXXXXX`，用于保存你的个人配置、授权文件，等价于 Windows 下的 `config` 目录
- IntelliJ IDEA 设置 JDK

<a href= "http://img.youmeek.com/2016/Mac-IDEA-JDK.jpg" class="foobox"><img src="http://img.youmeek.com/2016/Mac-IDEA-JDK.jpg" alt="IntelliJ IDEA JDK 设置"></a>


## Maven

- 官网下载：<http://maven.apache.org/download.cgi>
- Maven 是绿色版的，任何系统都适用。
- 安装方式和 Windows、Linux 没啥本质区别，都是把 zip 文件夹解压，然后新增几个系统变量，修改 Maven 配置文件参数。
- 如果你不懂 Maven 相关知识可以查看我过去写的这篇文章：[构建工具-Maven-相关知识-整理专题](http://code.youmeek.com/2016/03/09/2016/03/Maven/)
- 我是把 Maven 解压后，直接把 Windows 的 settings.xml 复制过来，修改下该文件本地仓库的路径，其他没啥可以改的了。
- 然后本地仓库的那些依赖包是直接从 Windows 下拷贝过来的，这个是任何系统下都兼容的，不需要额外处理。
- 最后再用 IntelliJ IDEA 对 Maven 的配置路径重新做了修改。
- 以上这些点都需要你对 Maven 和 IntelliJ IDEA 有了解，对于这两个东西我也在本文章都贴了相关的文章链接，我这里不多说了，学习总是需要花时间的。
- Maven 的环境变量是要添加的，我这边可以贴一下：

``` bash
MAVEN_HOME=/Users/youmeek/my_software/work_software/maven3.3.9
PATH=$PATH:$MAVEN_HOME/bin
export MAVEN_HOME
export PATH
```

- 验证：'mvn -v'

## Gradle

- 官网下载：<https://gradle.org/releases/>
- Gradle 和 Maven 思路是一模一样的，所以这里直接贴一下配置：

``` bash
 # Gradle
 GRADLE_HOME=/Users/youmeek/my_software/work_software/gradle4.2
 PATH=$PATH:$GRADLE_HOME/bin
 export GRADLE_HOME
 export PATH
```

- 验证：'gradle -v'

## Docker

- 通过 dmg 安装：<https://download.docker.com/mac/stable/Docker.dmg>
- 修改 register 的方式可以参看这篇文章：<http://www.runoob.com/docker/macos-docker-install.html>
- 如果经常会在 Docker 中启动很多中间件，建议调整下 CPU 和 Memory 大小：`Advanced | CPUs | Memory | Swap`
    - 如果你有用 Elasticsearch，基本都要调整该参数

## MySQL 5.7

- 官网下载 MySQL：<http://dev.mysql.com/downloads/mysql/>
- MySQL 5.7 版本：<https://dev.mysql.com/downloads/mysql/5.7.html#downloads>
- MySQL 官网提供的 Mac 系统的安装包，是下一步下一步安装类型的，没啥难度，大家自己试一下。
- **需要特别注意的是：安装结束后，会提示你它生成的一个随机密码，你要复制下，等下要用**
- 有几个点需要注意的是：
	- 如何修改 root 密码：
		- 打开：`系统偏好设置 -- 底部的 MySQL -- 点击：Stop MySQL Server`，根据提示输入你的 Mac 用户密码。
		- 连接：`sudo /usr/local/mysql/bin/mysql -h 127.0.0.1 -u root -P 3306 -p`，输入刚刚复制的密码
                - 修改密码：`set password = password('123456');`
	- MySQL 配置文件设置
		- 创建文件 `vim /etc/my.cnf`，参考内容如下
		- 重启 MySQL 服务即可
		- 这里给一个 demo 示例：

```
[mysql]
default-character-set = utf8mb4


[mysqld]
symbolic-links=0
log-error=/var/log/mysql/error.log
default-storage-engine = InnoDB
collation-server = utf8mb4_unicode_520_ci
init_connect = 'SET NAMES utf8mb4'
character-set-server = utf8mb4
lower_case_table_names = 1
max_allowed_packet = 50M
```


