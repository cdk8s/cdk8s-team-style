# SonarQube 安装和使用

## 官网资料

- 官网：<https://www.sonarqube.org/>
- 官网下载：<https://www.sonarqube.org/downloads/>
- 官网文档：<https://docs.sonarqube.org/latest/setup/install-server/>
- 官网插件库：<https://docs.sonarqube.org/display/PLUG/Plugin+Library>
- 环境要求说明：<https://docs.sonarqube.org/latest/requirements/requirements/>
    - 7.9 版本是 JDK 11
    - 7.8 版本是 JDK 8
- Github 主页（主要是用 Java 开发）：<https://github.com/SonarSource/sonarqube>
- 当前（2019-10）最新 LTS 是：7.9.1（206 MB）
- 主要支持的语言项目有：

```
C/C++
JavaScript
C#
Java
COBOL
TypeScript
PL/SQL
PL/I
PHP
ABAP
T-SQL
VB.NET
VB6
Python
RPG
Flex
Objective-C
Swift
Web（HTML and JSF/JSP）
XML
```


## Docker 的 SonarQube 安装和基本配置

- 官网安装说明：<https://docs.sonarqube.org/latest/setup/get-started-2-minutes/>

#### 简单 docker 方式

- 官网说明：<https://hub.docker.com/_/sonarqube/>
- 由于使用了 Elasticsearch，所以要确保：

```
sysctl -w vm.max_map_count=262144
sysctl -w fs.file-max=65536
ulimit -n 65536
ulimit -u 4096
```

- 没有数据库方式：`docker run -d --name sonarqube -p 9000:9000 sonarqube`
- 常挂载 + 数据库：
- 特别说明：7.9 版本不再支持 MySQL 了，所以我们这里就用官网推荐的 pgsql 了。如果要用 MySQL 推荐用 7.7 版本。

```
mkdir -p /data/docker/pgsql/data

chmod -R 777 /data/docker/pgsql

docker run \
	-d \
	--name pgsql \
	-p 5432:5432 \
	-e POSTGRES_USER=cdk8s_user \
	-e POSTGRES_PASSWORD=cdk8s123456 \
	-v /data/docker/pgsql/data:/var/lib/postgresql/data \
	postgres:11

CREATE DATABASE sonar;
```

```
mkdir -p /data/docker/sonarqube/conf /data/docker/sonarqube/data /data/docker/sonarqube/extension /data/docker/sonarqube/bundled-plugins

chmod -R 777 /data/docker/sonarqube

docker run -d --name sonarqube \
    -p 9000:9000 \
    -e sonar.jdbc.username=cdk8s_user \
    -e sonar.jdbc.password=cdk8s123456 \
    -e sonar.jdbc.url="jdbc:postgresql://172.16.0.91:5432/sonar?currentSchema=public" \
    -v /data/docker/sonarqube/conf:/opt/sonarqube/conf \
    -v /data/docker/sonarqube/data:/opt/sonarqube/data \
    -v /data/docker/sonarqube/extension:/opt/sonarqube/extensions \
    -v /data/docker/sonarqube/bundled-plugins:/opt/sonarqube/lib/bundled-plugins \
    sonarqube:7.9-community

docker run -d --name sonarqube \
    -p 9000:9000 \
    -e sonar.jdbc.username=cdk8s_user \
    -e sonar.jdbc.password=cdk8s123456 \
    -e sonar.jdbc.url="jdbc:postgresql://172.16.0.91:5432/sonar?currentSchema=public" \
    -v /data/docker/sonarqube/conf:/opt/sonarqube/conf \
    -v /data/docker/sonarqube/data:/opt/sonarqube/data \
    -v /data/docker/sonarqube/extension:/opt/sonarqube/extensions \
    -v /data/docker/sonarqube/bundled-plugins:/opt/sonarqube/lib/bundled-plugins \
    sonarqube:7.8-community
```

- 在浏览器里打开：<http://127.0.0.1:9000/>
- 管理员用户名、密码都是：`admin`

## SonarQube 插件

- Chinese Pack
    - 点击页头的：Administrator > Marketplace > 搜索：Chinese Pack > Install（过程会比较久，如果服务器网络不好，还会出现无法安装，需要多次重新来过）
    - 如果无法在线安装，可以到官网自行构建：<https://github.com/SonarQubeCommunity/sonar-l10n-zh.git>
    - 安装成功后，重启 SonarQube 服务，再次访问即可看到中文界面
- PMC
    - 搜索 PMC，安装该插件会先安装：sonar-java-plugin-5.13.1.18282.jar，整个过程由于网络原因，所以非常慢，大家可以注意观察：/data/docker/sonarqube/extension/downloads 目录变化，只有文件后缀从 .tmp 变成 .jar 才算完成
    - sonar-java-plugin-5.13.1.18282.jar
    - sonar-pmd-plugin-3.2.1.jar

## IntelliJ IDEA 与 Sonar 集成

- 登陆 SonarQube：点击右上角用户头像 > 我的账号 > 安全 > 令牌 > 输入一个自定义的 Token 名称，然后点击生成 > 复制 Token 值
- IntelliJ IDEA 搜索插件 SonarLint（48MB）
    - 或者官网下载离线安装：<https://plugins.jetbrains.com/plugin/7973-sonarlint/>
- 插件安装完后，打开 IntelliJ IDEA 设置：Preferences | Other Settings | SonarLint General Settings
    - 点击加号按钮，输入我们的 SonarQube URL 和 Token 值

## 集成 P3C

- 参考：<https://blog.csdn.net/zuozewei/article/details/90232808>
- SonarQube 7.8 及其以下支持
- 登录 SonarQube 打开 `质量配置` ，点击右上方的 `创建` 按钮，假设命名为：p3c。
- 打开 `代码规则` 配置页面，刚新建的 profile 是没有激活任何规则的，需要手动激活。我们需要为刚创建的 p3c profile 激活 p3c 规则，点击 `更多激活规则`
- 跳转到激活页面，在右侧过滤器中搜索 `p3c`，点击 `批量修改` > 点击：`活动`
- 返回 `质量配置`，我们可以设置 p3c profile 为默认。
- 可惜 IntelliJ IDEA 的 SonarLint 无法识别到这些规则，还是只能拿到 SonarQube 默认的 Java 规则


## Jenkins 与 Sonar 集成

- 分析器有很多种，原生的就是：Sonar Scanner 下载（42MB）：<https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/>
- 但是我们项目现在基本都是 Maven 和 Gradle，所以我这里使用 Maven Plugin
    - 官网说明：<https://docs.sonarqube.org/latest/analysis/scan/sonarscanner-for-maven/>
- 首先，我们需要配置 Maven 的 setting.xml文件，增加 sonarQube 配置。

```
<settings>
    <pluginGroups>
        <pluginGroup>org.sonarsource.scanner.maven</pluginGroup>
    </pluginGroups>
    <profiles>
        <profile>
            <id>sonar</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <properties>
                <sonar.host.url>
                  http://127.0.0.1:9000
                </sonar.host.url>
            </properties>
        </profile>
     </profiles>
</settings>
```

- 然后对项目执行命令：`mvn clean install sonar:sonar`


## SonarQube API


- <https://docs.sonarqube.org/latest/extend/web-api/>
- <https://docs.sonarqube.org/display/SONARQUBE43/Web+Service+API>























