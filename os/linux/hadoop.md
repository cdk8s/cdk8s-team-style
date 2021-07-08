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

执行完成后，端口所有终端窗口，重新连接


## header1 机子运行

```
首次使用需要先格式化  HDFS
hdfs namenode -format
必须出现有
common.Storage: Storage directory /home/data/hadoop/hdfs/tmpdir/dfs/name has been successfully formatted
的信息才表示格式化成功，然后就可以正式启动集群了；否则，就需要查看指令是否正确，或者之前Hadoop集群的安装和配置是否正确。
```

- 输出结果：

```
2021-07-08 10:31:47,359 INFO namenode.NameNode: registered UNIX signal handlers for [TERM, HUP, INT]
2021-07-08 10:31:47,409 INFO namenode.NameNode: createNameNode [-format]
Formatting using clusterid: CID-3c97fdc3-7d66-4834-b14d-fe707d27d29b
2021-07-08 10:31:47,691 INFO namenode.FSEditLog: Edit logging is async:true
2021-07-08 10:31:47,699 INFO namenode.FSNamesystem: KeyProvider: null
2021-07-08 10:31:47,700 INFO namenode.FSNamesystem: fsLock is fair: true
2021-07-08 10:31:47,700 INFO namenode.FSNamesystem: Detailed lock hold time metrics enabled: false
2021-07-08 10:31:47,703 INFO namenode.FSNamesystem: fsOwner             = root (auth:SIMPLE)
2021-07-08 10:31:47,703 INFO namenode.FSNamesystem: supergroup          = supergroup
2021-07-08 10:31:47,703 INFO namenode.FSNamesystem: isPermissionEnabled = true
2021-07-08 10:31:47,703 INFO namenode.FSNamesystem: HA Enabled: false
2021-07-08 10:31:47,730 INFO common.Util: dfs.datanode.fileio.profiling.sampling.percentage set to 0. Disabling file IO profiling
2021-07-08 10:31:47,737 INFO blockmanagement.DatanodeManager: dfs.block.invalidate.limit: configured=1000, counted=60, effected=1000
2021-07-08 10:31:47,737 INFO blockmanagement.DatanodeManager: dfs.namenode.datanode.registration.ip-hostname-check=true
2021-07-08 10:31:47,740 INFO blockmanagement.BlockManager: dfs.namenode.startup.delay.block.deletion.sec is set to 000:00:00:00.000
2021-07-08 10:31:47,740 INFO blockmanagement.BlockManager: The block deletion will start around 2021 七月 08 10:31:47
2021-07-08 10:31:47,741 INFO util.GSet: Computing capacity for map BlocksMap
2021-07-08 10:31:47,741 INFO util.GSet: VM type       = 64-bit
2021-07-08 10:31:47,742 INFO util.GSet: 2.0% max memory 6.9 GB = 141.7 MB
2021-07-08 10:31:47,742 INFO util.GSet: capacity      = 2^24 = 16777216 entries
2021-07-08 10:31:47,751 INFO blockmanagement.BlockManager: dfs.block.access.token.enable = false
2021-07-08 10:31:47,755 INFO Configuration.deprecation: No unit for dfs.namenode.safemode.extension(30000) assuming MILLISECONDS
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManagerSafeMode: dfs.namenode.safemode.threshold-pct = 0.9990000128746033
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManagerSafeMode: dfs.namenode.safemode.min.datanodes = 0
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManagerSafeMode: dfs.namenode.safemode.extension = 30000
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManager: defaultReplication         = 3
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManager: maxReplication             = 512
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManager: minReplication             = 1
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManager: maxReplicationStreams      = 2
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManager: redundancyRecheckInterval  = 3000ms
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManager: encryptDataTransfer        = false
2021-07-08 10:31:47,755 INFO blockmanagement.BlockManager: maxNumBlocksToLog          = 1000
2021-07-08 10:31:47,768 INFO namenode.FSDirectory: GLOBAL serial map: bits=24 maxEntries=16777215
2021-07-08 10:31:47,777 INFO util.GSet: Computing capacity for map INodeMap
2021-07-08 10:31:47,777 INFO util.GSet: VM type       = 64-bit
2021-07-08 10:31:47,778 INFO util.GSet: 1.0% max memory 6.9 GB = 70.9 MB
2021-07-08 10:31:47,778 INFO util.GSet: capacity      = 2^23 = 8388608 entries
2021-07-08 10:31:47,787 INFO namenode.FSDirectory: ACLs enabled? false
2021-07-08 10:31:47,787 INFO namenode.FSDirectory: POSIX ACL inheritance enabled? true
2021-07-08 10:31:47,787 INFO namenode.FSDirectory: XAttrs enabled? true
2021-07-08 10:31:47,787 INFO namenode.NameNode: Caching file names occurring more than 10 times
2021-07-08 10:31:47,791 INFO snapshot.SnapshotManager: Loaded config captureOpenFiles: false, skipCaptureAccessTimeOnlyChange: false, snapshotDiffAllowSnapRootDescendant: true, maxSnapshotLimit: 65536
2021-07-08 10:31:47,792 INFO snapshot.SnapshotManager: SkipList is disabled
2021-07-08 10:31:47,794 INFO util.GSet: Computing capacity for map cachedBlocks
2021-07-08 10:31:47,794 INFO util.GSet: VM type       = 64-bit
2021-07-08 10:31:47,795 INFO util.GSet: 0.25% max memory 6.9 GB = 17.7 MB
2021-07-08 10:31:47,795 INFO util.GSet: capacity      = 2^21 = 2097152 entries
2021-07-08 10:31:47,799 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.window.num.buckets = 10
2021-07-08 10:31:47,799 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.num.users = 10
2021-07-08 10:31:47,799 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.windows.minutes = 1,5,25
2021-07-08 10:31:47,801 INFO namenode.FSNamesystem: Retry cache on namenode is enabled
2021-07-08 10:31:47,801 INFO namenode.FSNamesystem: Retry cache will use 0.03 of total heap and retry cache entry expiry time is 600000 millis
2021-07-08 10:31:47,802 INFO util.GSet: Computing capacity for map NameNodeRetryCache
2021-07-08 10:31:47,802 INFO util.GSet: VM type       = 64-bit
2021-07-08 10:31:47,802 INFO util.GSet: 0.029999999329447746% max memory 6.9 GB = 2.1 MB
2021-07-08 10:31:47,802 INFO util.GSet: capacity      = 2^18 = 262144 entries
2021-07-08 10:31:47,815 INFO namenode.FSImage: Allocated new BlockPoolId: BP-592614855-192.168.31.137-1625711507811
2021-07-08 10:31:47,831 INFO common.Storage: Storage directory /home/data/hadoop/hdfs/tmpdir/dfs/name has been successfully formatted.
2021-07-08 10:31:47,844 INFO namenode.FSImageFormatProtobuf: Saving image file /home/data/hadoop/hdfs/tmpdir/dfs/name/current/fsimage.ckpt_0000000000000000000using no compression
2021-07-08 10:31:47,903 INFO namenode.FSImageFormatProtobuf: Image file /home/data/hadoop/hdfs/tmpdir/dfs/name/current/fsimage.ckpt_0000000000000000000 of size 391 bytes saved in 0 seconds .
2021-07-08 10:31:47,911 INFO namenode.NNStorageRetentionManager: Going to retain 1 images with txid >= 0
2021-07-08 10:31:47,914 INFO namenode.FSImage: FSImageSaver clean checkpoint: txid = 0 when meet shutdown.
2021-07-08 10:31:47,914 INFO namenode.NameNode: SHUTDOWN_MSG:
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at header1/192.168.31.137
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
