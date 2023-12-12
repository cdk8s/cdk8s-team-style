# Jira 安装和配置


## Jira 介绍

- 官网：<https://www.atlassian.com/software/jira>
- 官网下载：<https://www.atlassian.com/software/jira/download>
- 官网帮助中心：<https://confluence.atlassian.com/alldoc/>

## Jira 版本

- 对于 licene 过程：
- 进过测试支持 8.4.x、8.13.27
- 8.20.x 不支持


#### 数据库配置


```
create database jira_db default character set utf8mb4 collate utf8mb4_bin;
CREATE USER 'jira_user'@'localhost' IDENTIFIED BY '123456';
GRANT ALL PRIVILEGES ON jira_db.* TO 'jira_user'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

```


#### 安装

- 下载：<https://www.atlassian.com/software/jira/download>
    - 选择：tar.gz 类型下载
- 解压：`tar zxvf atlassian-jira-software-8.13.27.tar.gz`
- 创建 home 目录：`mkdir /usr/local/atlassian-jira-software-8.13.27-standalone/data`
- 配置 home 变量：

```
编辑：vim ~/.zshrc

在文件尾部添加：

JIRA_HOME=/usr/local/atlassian-jira-software-8.13.27-standalone/data
export JIRA_HOME


刷新配置：source ~/.zshrc
```

- 设置 MySQL 连接（支持 MySQL5.7、MySQL 8）：
- 如果是 MySQL 5.7 那就把 mysql-connector-java-5.1.47.jar 放在目录 `/usr/local/atlassian-jira-software-8.13.27-standalone/atlassian-jira/WEB-INF/lib`
- 如果是 MySQL 8 那就把 mysql-connector-java-8.0.29.jar 放在目录 `/usr/local/atlassian-jira-software-8.13.27-standalone/atlassian-jira/WEB-INF/lib`


#### License 过程（相关文件在百度云盘）

```

vim /usr/local/atlassian-jira-software-8.13.27-standalone/bin/setenv.sh
增加：export JAVA_OPTS="-javaagent:/opt/jar/atlassian-agent.jar ${JAVA_OPTS}"

cd /usr/local/atlassian-jira-software-8.13.27-standalone/atlassian-jira/WEB-INF/lib/
mv atlassian-extras-3.2.jar atlassian-extras-3.2.jar.back
上传：atlassian-extras-3.2.jar 
```


#### 运行

- 启动：`sh /usr/local/atlassian-jira-software-8.13.27-standalone/bin/start-jira.sh`
- 停止：`sh /usr/local/atlassian-jira-software-8.13.27-standalone/bin/stop-jira.sh`
    - `ps -ef | grep java`
- 查看 log：`tail -300f /usr/local/atlassian-jira-software-8.13.27-standalone/logs/catalina.out`
- 访问：<http://服务器ip:8080>
    - 注意云服务器的防火墙配置
- 如果需要更换端口号可以修改：`vim /usr/local/atlassian-jira-software-8.13.27-standalone/conf/server.xml` 文件中的内容。

#### 首次访问配置

```
http://服务器ip:8080

右上角选择：中文
接着选择：我将设置它自己 > 其他数据库，填写：MySQL 信息
然后根据提示下一步可以得到一个：服务器 BNC6-0SLA-E3YZ-RC7B

根据服务器机器码生成注册码：
java -jar /opt/jar/atlassian-agent.jar -p jira -m git123@qq.com -n meek -o http://81.71.108.155:8080 -s BNC6-0SLA-E3YZ-RC7B

然后会生成一个注册码，填写这个注册码到网页，然后下一步，这个过程需要等待一段时间，
接着会出现：设置管理员账号
接着设置：设置电子邮件通知 > 以后再说
接着设置：中文，然后就可以使用了
```




#### 中文化

- 从 7.x 版本默认已经有中文支持，不需要再汉化了
- 在安装后首次进入的时候就可以配置，选择中文了
        

#### 首次配置

- 参考文章：<https://blog.csdn.net/yelllowcong/article/details/79624970>
- 因为步骤一样，所以我就不再截图了。

## 重置管理员密码

```
编辑文件：
/usr/local/atlassian-jira-software-8.13.27-standalone/bin/setenv.sh

找到这个参数，然后增加后面部分内容：
JVM_SUPPORT_RECOMMENDED_ARGS="-Datlassian.recovery.password='admin123456'"

重启 jira，然后用浏览器打开JIRA页面，登陆，
用户名：recovery_admin
密码：刚才设置的密码

这个recovery_admin是个临时的管理员，登录后修改 原来JIRA管理员的密码，或把一个新的用户授权成为JIRA管理员
然后把刚才那个-Datlassian.recovery.password启动参数删掉，再重启JIRA
```

    
