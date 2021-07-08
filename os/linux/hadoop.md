# Hadoop 安装和配置


## Hadoop 说明

- Hadoop 官网：<https://hadoop.apache.org/>
- Hadoop 官网下载：<https://hadoop.apache.org/releases.html>
- 下载 Hadoop：<https://archive.apache.org/dist/hadoop/common/hadoop-3.1.3/>
- 官网安装说明：<https://hadoop.apache.org/docs/r3.1.3/hadoop-project-dist/hadoop-common/ClusterSetup.html>
- 核心配置文件：<https://hadoop.apache.org/docs/r3.1.3/>

## 基础环境


- 最小配置
    - header1：4C8G
    - worker1：2C8G
    - worker2：2C8G
- 内网 ip：
	- header1：192.168.31.137
	- worker1：192.168.31.237
	- worker2：192.168.31.88
- 操作系统：CentOS 7.9
	- root 用户
- Hadoop:3.1.3

```
整体规划：副本数 3 个
header1 NameNode、DataNode、NodeManager、jobhistory
worker1 DataNode、NodeManager、Yarn ResourceManager
worker2 DataNode、NodeManager、second NameNode

Namenode,SecondaryNameNode,ResourceManager 这三个服务都是比较吃内存的所以不放在一台服务器上。
Namenode,SecondaryNameNode 是一个主备的关系最好不放在同一台机器上。
```



## 集群环境设置

- 分别给三台机子设置 hostname

```
hostnamectl set-hostname header1
hostnamectl set-hostname worker1
hostnamectl set-hostname worker2
```

- 对 header1 设置免密

```
因为我们在 header1 机器启动start-hdfs.sh 脚本需要配置 header1 到其余机器的ssh免密登录。
在 worker1 机器启动start-yarn.sh 脚本需要配置 worker1 到其余机器的ssh免密登录。


我们先在 header1
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa && cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
测试：ssh localhost
测试：ssh 192.168.31.137

同步到其他两台：
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@192.168.31.237
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@192.168.31.88

测试下是否可以免登陆：
ssh -p 22 root@192.168.31.237
ssh -p 22 root@192.168.31.88




我们在 worker1
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa && cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
测试：ssh localhost
测试：ssh 192.168.31.88

同步到其他两台：
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@192.168.31.137
ssh-copy-id -i /root/.ssh/id_rsa.pub -p 22 root@192.168.31.237

测试下是否可以免登陆：
ssh -p 22 root@192.168.31.137
ssh -p 22 root@192.168.31.237
```

- 设置 ansible 配置


```
在 header1 安装 ansible
yum install -y epel-release
yum install -y ansible

在 header1 使用 ansible
vim /etc/ansible/hosts

[hadoops]
192.168.31.137 ansible_ssh_port=22
192.168.31.88 ansible_ssh_port=22
192.168.31.237 ansible_ssh_port=22


测试：
ansible all -a 'ps'

在三台机子上都执行：
yum install -y lrzsz

在三台机子上都执行：
mkdir -p /opt/playbook /opt/software

在三台机子上：
cd /opt/software
将 hadoop-3.1.3.tar.gz、jdk-8u261-linux-x64.tar.gz 上传到 /opt/software

在 header1 上
cd /opt/playbook
把以下三个脚本上传上去，并执行：

ansible-playbook /opt/playbook/1-install-basic-no-docker-playbook.yml
ansible-playbook /opt/playbook/2-jdk8-playbook.yml
```


## Hadoop 安装

```
hadoop-env.sh	配置Hadoop运行所需的环境变量
yarn-env.sh	   配置Yarn运行所需的环境变量
core-site.xml	Hadoop核心全局配置文件，可在其他配置文件中引用该文件
hdfs-site.xml	HDFS配置文件，继承core-site.xml配置文件
mapred-site.xml	MapReduce配置文件，继承core-site.xml配置文件
yarn-site.xml	Yarn配置文件，继承core-site.xml配置文件
```

执行安装脚本：
ansible-playbook /opt/playbook/10-hadoop-playbook.yml



## header1 机子运行

```
首次使用需要先格式化  HDFS
hdfs namenode -format
必须出现有“successfully formatted”信息才表示格式化成功，然后就可以正式启动集群了；否则，就需要查看指令是否正确，或者之前Hadoop集群的安装和配置是否正确。
```

- 输出结果：

```
[root@header1 hadoop-3.1.3]# hdfs namenode -format
18/12/17 17:47:17 INFO namenode.NameNode: STARTUP_MSG:
/************************************************************
STARTUP_MSG: Starting NameNode
STARTUP_MSG:   host = localhost/127.0.0.1
STARTUP_MSG:   args = [-format]
STARTUP_MSG:   version = 3.1.3
STARTUP_MSG:   classpath = /usr/local/hadoop-3.1.3/etc/hadoop:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/apacheds-kerberos-codec-2.0.0-M15.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-io-2.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/activation-1.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/netty-3.6.2.Final.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jackson-mapper-asl-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/slf4j-api-1.7.5.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/junit-4.11.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/curator-recipes-2.6.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jasper-compiler-5.5.23.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jets3t-0.9.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-lang-2.6.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-digester-1.8.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jackson-core-asl-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/apacheds-i18n-2.0.0-M15.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/guava-11.0.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/gson-2.2.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jackson-jaxrs-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jettison-1.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jetty-6.1.26.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/api-util-1.0.0-M20.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/log4j-1.2.17.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-beanutils-core-1.8.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-httpclient-3.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-el-1.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/paranamer-2.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/slf4j-log4j12-1.7.5.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-collections-3.2.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jersey-server-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-net-3.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/hadoop-auth-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jasper-runtime-5.5.23.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jaxb-impl-2.2.3-1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/hamcrest-core-1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/stax-api-1.0-2.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-beanutils-1.7.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/protobuf-java-2.5.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/curator-framework-2.6.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/xz-1.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jsr305-1.3.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jsp-api-2.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-compress-1.4.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/asm-3.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jsch-0.1.42.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-configuration-1.6.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-cli-1.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jackson-xc-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-logging-1.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/htrace-core-3.0.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jetty-util-6.1.26.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-math3-3.1.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/mockito-all-1.8.5.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jersey-json-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/zookeeper-3.4.6.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/httpclient-4.2.5.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/servlet-api-2.5.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/xmlenc-0.52.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/httpcore-4.2.5.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/api-asn1-api-1.0.0-M20.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/java-xmlbuilder-0.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/avro-1.7.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jaxb-api-2.2.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/commons-codec-1.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/jersey-core-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/snappy-java-1.0.4.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/curator-client-2.6.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/lib/hadoop-annotations-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/hadoop-common-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/hadoop-common-3.1.3-tests.jar:/usr/local/hadoop-3.1.3/share/hadoop/common/hadoop-nfs-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/commons-io-2.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/netty-3.6.2.Final.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jackson-mapper-asl-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/commons-lang-2.6.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/commons-daemon-1.0.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jackson-core-asl-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/guava-11.0.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jetty-6.1.26.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/log4j-1.2.17.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/commons-el-1.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/xercesImpl-2.9.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jersey-server-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jasper-runtime-5.5.23.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/protobuf-java-2.5.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jsr305-1.3.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/xml-apis-1.3.04.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jsp-api-2.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/asm-3.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/commons-cli-1.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/commons-logging-1.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/htrace-core-3.0.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jetty-util-6.1.26.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/servlet-api-2.5.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/xmlenc-0.52.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/commons-codec-1.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/lib/jersey-core-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/hadoop-hdfs-3.1.3-tests.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/hadoop-hdfs-nfs-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/hdfs/hadoop-hdfs-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/commons-io-2.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/activation-1.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/aopalliance-1.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/netty-3.6.2.Final.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jackson-mapper-asl-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/commons-lang-2.6.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jackson-core-asl-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/guice-3.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/guava-11.0.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jackson-jaxrs-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jettison-1.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jetty-6.1.26.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/log4j-1.2.17.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/commons-httpclient-3.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/commons-collections-3.2.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jersey-server-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jaxb-impl-2.2.3-1.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/stax-api-1.0-2.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/protobuf-java-2.5.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/xz-1.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jsr305-1.3.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jersey-client-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/guice-servlet-3.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/commons-compress-1.4.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/asm-3.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/commons-cli-1.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jersey-guice-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jackson-xc-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/commons-logging-1.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jetty-util-6.1.26.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/leveldbjni-all-1.8.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jersey-json-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/javax.inject-1.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/zookeeper-3.4.6.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/servlet-api-2.5.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jaxb-api-2.2.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jline-0.9.94.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/commons-codec-1.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/lib/jersey-core-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-server-web-proxy-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-api-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-server-common-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-registry-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-server-nodemanager-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-client-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-common-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-applications-unmanaged-am-launcher-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-server-tests-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-server-resourcemanager-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-server-applicationhistoryservice-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/yarn/hadoop-yarn-applications-distributedshell-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/commons-io-2.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/aopalliance-1.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/netty-3.6.2.Final.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/jackson-mapper-asl-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/junit-4.11.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/jackson-core-asl-1.9.13.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/guice-3.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/log4j-1.2.17.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/paranamer-2.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/jersey-server-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/hamcrest-core-1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/protobuf-java-2.5.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/xz-1.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/guice-servlet-3.0.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/commons-compress-1.4.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/asm-3.2.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/jersey-guice-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/leveldbjni-all-1.8.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/javax.inject-1.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/avro-1.7.4.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/jersey-core-1.9.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/snappy-java-1.0.4.1.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/lib/hadoop-annotations-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-client-app-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-client-common-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-client-shuffle-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-client-core-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-client-hs-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-client-hs-plugins-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.3.jar:/usr/local/hadoop-3.1.3/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.1.3-tests.jar:/usr/local/hadoop-3.1.3/contrib/capacity-scheduler/*.jar
STARTUP_MSG:   build = https://github.com/apache/hadoop.git -r e8c9fe0b4c252caf2ebf1464220599650f119997; compiled by 'sjlee' on 2016-10-02T23:43Z
STARTUP_MSG:   java = 1.8.0_191
************************************************************/
18/12/17 17:47:17 INFO namenode.NameNode: registered UNIX signal handlers for [TERM, HUP, INT]
18/12/17 17:47:17 INFO namenode.NameNode: createNameNode [-format]
Formatting using clusterid: CID-beba43b4-0881-48b4-8eda-5c3bca046398
18/12/17 17:47:17 INFO namenode.FSNamesystem: No KeyProvider found.
18/12/17 17:47:17 INFO namenode.FSNamesystem: fsLock is fair:true
18/12/17 17:47:17 INFO blockmanagement.DatanodeManager: dfs.block.invalidate.limit=1000
18/12/17 17:47:17 INFO blockmanagement.DatanodeManager: dfs.namenode.datanode.registration.ip-hostname-check=true
18/12/17 17:47:17 INFO blockmanagement.BlockManager: dfs.namenode.startup.delay.block.deletion.sec is set to 000:00:00:00.000
18/12/17 17:47:17 INFO blockmanagement.BlockManager: The block deletion will start around 2018 Dec 17 17:47:17
18/12/17 17:47:17 INFO util.GSet: Computing capacity for map BlocksMap
18/12/17 17:47:17 INFO util.GSet: VM type       = 64-bit
18/12/17 17:47:17 INFO util.GSet: 2.0% max memory 889 MB = 17.8 MB
18/12/17 17:47:17 INFO util.GSet: capacity      = 2^21 = 2097152 entries
18/12/17 17:47:17 INFO blockmanagement.BlockManager: dfs.block.access.token.enable=false
18/12/17 17:47:17 INFO blockmanagement.BlockManager: defaultReplication         = 2
18/12/17 17:47:17 INFO blockmanagement.BlockManager: maxReplication             = 512
18/12/17 17:47:17 INFO blockmanagement.BlockManager: minReplication             = 1
18/12/17 17:47:17 INFO blockmanagement.BlockManager: maxReplicationStreams      = 2
18/12/17 17:47:17 INFO blockmanagement.BlockManager: replicationRecheckInterval = 3000
18/12/17 17:47:17 INFO blockmanagement.BlockManager: encryptDataTransfer        = false
18/12/17 17:47:17 INFO blockmanagement.BlockManager: maxNumBlocksToLog          = 1000
18/12/17 17:47:17 INFO namenode.FSNamesystem: fsOwner             = root (auth:SIMPLE)
18/12/17 17:47:17 INFO namenode.FSNamesystem: supergroup          = supergroup
18/12/17 17:47:17 INFO namenode.FSNamesystem: isPermissionEnabled = false
18/12/17 17:47:17 INFO namenode.FSNamesystem: HA Enabled: false
18/12/17 17:47:17 INFO namenode.FSNamesystem: Append Enabled: true
18/12/17 17:47:17 INFO util.GSet: Computing capacity for map INodeMap
18/12/17 17:47:17 INFO util.GSet: VM type       = 64-bit
18/12/17 17:47:17 INFO util.GSet: 1.0% max memory 889 MB = 8.9 MB
18/12/17 17:47:17 INFO util.GSet: capacity      = 2^20 = 1048576 entries
18/12/17 17:47:17 INFO namenode.NameNode: Caching file names occuring more than 10 times
18/12/17 17:47:17 INFO util.GSet: Computing capacity for map cachedBlocks
18/12/17 17:47:17 INFO util.GSet: VM type       = 64-bit
18/12/17 17:47:17 INFO util.GSet: 0.25% max memory 889 MB = 2.2 MB
18/12/17 17:47:17 INFO util.GSet: capacity      = 2^18 = 262144 entries
18/12/17 17:47:17 INFO namenode.FSNamesystem: dfs.namenode.safemode.threshold-pct = 0.9990000128746033
18/12/17 17:47:17 INFO namenode.FSNamesystem: dfs.namenode.safemode.min.datanodes = 0
18/12/17 17:47:17 INFO namenode.FSNamesystem: dfs.namenode.safemode.extension     = 30000
18/12/17 17:47:17 INFO namenode.FSNamesystem: Retry cache on namenode is enabled
18/12/17 17:47:17 INFO namenode.FSNamesystem: Retry cache will use 0.03 of total heap and retry cache entry expiry time is 600000 millis
18/12/17 17:47:17 INFO util.GSet: Computing capacity for map NameNodeRetryCache
18/12/17 17:47:17 INFO util.GSet: VM type       = 64-bit
18/12/17 17:47:17 INFO util.GSet: 0.029999999329447746% max memory 889 MB = 273.1 KB
18/12/17 17:47:17 INFO util.GSet: capacity      = 2^15 = 32768 entries
18/12/17 17:47:17 INFO namenode.NNConf: ACLs enabled? false
18/12/17 17:47:17 INFO namenode.NNConf: XAttrs enabled? true
18/12/17 17:47:17 INFO namenode.NNConf: Maximum size of an xattr: 16384
18/12/17 17:47:17 INFO namenode.FSImage: Allocated new BlockPoolId: BP-233285725-127.0.0.1-1545040037972
18/12/17 17:47:18 INFO common.Storage: Storage directory /data/hadoop/hdfs/name has been successfully formatted.
18/12/17 17:47:18 INFO namenode.FSImageFormatProtobuf: Saving image file /data/hadoop/hdfs/name/current/fsimage.ckpt_0000000000000000000 using no compression
18/12/17 17:47:18 INFO namenode.FSImageFormatProtobuf: Image file /data/hadoop/hdfs/name/current/fsimage.ckpt_0000000000000000000 of size 321 bytes saved in 0 seconds.
18/12/17 17:47:18 INFO namenode.NNStorageRetentionManager: Going to retain 1 images with txid >= 0
18/12/17 17:47:18 INFO util.ExitUtil: Exiting with status 0
18/12/17 17:47:18 INFO namenode.NameNode: SHUTDOWN_MSG:
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at localhost/127.0.0.1
************************************************************/

```

## HDFS 启动

- 切换到 header1 机器

```
- 启动：start-dfs.sh，根据提示一路 yes
这个命令效果：
主节点会启动任务：NameNode 和 SecondaryNameNode
从节点会启动任务：DataNode


主节点查看：jps，可以看到：
21922 Jps
21603 NameNode
21787 SecondaryNameNode


从节点查看：jps 可以看到：
19728 DataNode
19819 Jps

如果要停止，命令：stop-dfs.sh

动MapReduce JobHistory Server，并在指定服务器上以mapred运行：
mapred --daemon start historyserver

```


- 查看运行更多情况：`hdfs dfsadmin -report`

```
Configured Capacity: 0 (0 B)
Present Capacity: 0 (0 B)
DFS Remaining: 0 (0 B)
DFS Used: 0 (0 B)
DFS Used%: NaN%
Under replicated blocks: 0
Blocks with corrupt replicas: 0
Missing blocks: 0
```

- 如果需要停止：`stop-dfs.sh`
- 查看 log：`cd $HADOOP_HOME/logs`

```
其他平时常用命令：
hdfs --daemon start namenode
hdfs --daemon start datanode
yarn --daemon start resourcemanager
yarn --daemon start nodemsnager
```


## YARN 运行

```
切换到 worker1 机器
start-yarn.sh
然后 jps 你会看到一个：ResourceManager 

从节点你会看到：NodeManager

停止：stop-yarn.sh

使用以下命令打印正在运行的节点的报告：
yarn node -list

使用以下命令获取正在运行的应用程序的列表：
yarn application -list


#停止历史服务
mapred --daemon stop historyserver
```

## 端口情况

- 主节点当前运行的所有端口：`netstat -tpnl | grep java`
- 会用到端口（为了方便展示，整理下顺序）：

```
tcp        0      0 172.16.0.17:9000        0.0.0.0:*               LISTEN      22932/java >> NameNode
tcp        0      0 0.0.0.0:50070           0.0.0.0:*               LISTEN      22932/java >> NameNode
tcp        0      0 0.0.0.0:50090           0.0.0.0:*               LISTEN      23125/java >> SecondaryNameNode
tcp6       0      0 172.16.0.17:8030      :::*                    LISTEN      23462/java   >> ResourceManager
tcp6       0      0 172.16.0.17:8031      :::*                    LISTEN      23462/java   >> ResourceManager
tcp6       0      0 172.16.0.17:8032      :::*                    LISTEN      23462/java   >> ResourceManager
tcp6       0      0 172.16.0.17:8033      :::*                    LISTEN      23462/java   >> ResourceManager
tcp6       0      0 172.16.0.17:8088      :::*                    LISTEN      23462/java   >> ResourceManager
```

- 从节点当前运行的所有端口：`netstat -tpnl | grep java`
- 会用到端口（为了方便展示，整理下顺序）：

```
tcp        0      0 0.0.0.0:50010           0.0.0.0:*               LISTEN      14545/java >> DataNode
tcp        0      0 0.0.0.0:50020           0.0.0.0:*               LISTEN      14545/java >> DataNode
tcp        0      0 0.0.0.0:50075           0.0.0.0:*               LISTEN      14545/java >> DataNode
tcp6       0      0 :::8040                 :::*                    LISTEN      14698/java >> NodeManager
tcp6       0      0 :::8042                 :::*                    LISTEN      14698/java >> NodeManager
tcp6       0      0 :::13562                :::*                    LISTEN      14698/java >> NodeManager
tcp6       0      0 :::37481                :::*                    LISTEN      14698/java >> NodeManager
```

-------------------------------------------------------------------

## 管理界面

- 查看 HDFS NameNode 管理界面（默认端口 9870）：<http://header1:9870>
- 访问 YARN ResourceManager 管理界面（默认端口 8088）：<http://header1:8088> 
- 访问 NodeManager-1 管理界面：<http://worker1:8042> 
- 访问 NodeManager-2 管理界面：<http://worker2:8042> 


-------------------------------------------------------------------

## 运行作业

- 在 header1 节点上操作
- 运行一个 Mapreduce 作业试试：
	- 计算 π：`hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.3.jar pi 1 1`
- 运行一个文件相关作业：
	- 由于运行 hadoop 时指定的输入文件只能是 HDFS 文件系统中的文件，所以我们必须将要进行 wordcount 的文件从本地文件系统拷贝到 HDFS 文件系统中。
	- 查看目前根目录结构：`hadoop fs -ls /`
		- 查看目前根目录结构，另外写法：`hadoop fs -ls hdfs://linux-05:9000/`
		- 或者列出目录以及下面的文件：`hadoop fs -ls -R /`
		- 更多命令可以看：[hadoop HDFS常用文件操作命令](https://segmentfault.com/a/1190000002672666)
	- 创建目录：`hadoop fs -mkdir -p /tmp/zch/wordcount_input_dir`
	- 上传文件：`hadoop fs -put /opt/input.txt /tmp/zch/wordcount_input_dir`
	- 查看上传的目录下是否有文件：`hadoop fs -ls /tmp/zch/wordcount_input_dir`
	- 向 yarn 提交作业，计算单词个数：`hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.1.3.jar wordcount /tmp/zch/wordcount_input_dir /tmp/zch/wordcount_output_dir`
	- 查看计算结果输出的目录：`hadoop fs -ls /tmp/zch/wordcount_output_dir`
	- 查看计算结果输出内容：`hadoop fs -cat /tmp/zch/wordcount_output_dir/part-r-00000`
- 查看正在运行的 Hadoop 任务：`yarn application -list`
- 关闭 Hadoop 任务进程：`yarn application -kill 你的ApplicationId`


-------------------------------------------------------------------

## 资料

- <https://www.wangfeng.live/2021/03/hadoop-3-3-0-fully-distributed-deployment-configuration/>
- <https://book.itheima.net/course/1269935677353533441/1269937996044476418/1269939156776165381>
