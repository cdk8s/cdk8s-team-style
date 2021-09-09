

## 基础环境

- 官网文档：<https://cloud.tencent.com/document/product/436/10976>

```
确保 python 升级到最新的 3.x，也确保 pip 升级到最新版本，具体可以参考我的 centos.md

安装：
pip install coscmd

ln -s /usr/local/python3/bin/coscmd /usr/bin/coscmd


配置环境
coscmd config -a <secret_id> -s <secret_key> -b <bucketName> -r <region> [-m <max_thread>] [-p <parts_size>]
其中复杂参数有：
max_thread 可选参数，多线程上传时的最大线程数（默认为 5），有效值：1~10
parts_size 可选参数，分块上传的单块大小（单位为 MB，默认为 1MB），有效值：1~10

完整例子（相关密钥信息上腾讯云后台去看下）：
coscmd config -a AChT4ThiXAbpBDEFGhT4ThiXAbp -s WE54wreefvds3462refgwewe -b bucket-name -r ap-chengdu

然后会生成一个配置文件：~/.cos.conf
这里会记录下我们刚刚配置的密钥和桶信息

删除根目录下的 aa.txt 文件（需要交互确认）
coscmd delete aa.txt

删除根目录下的 aa.txt 文件（不需要交互确认）
echo y | coscmd delete aa.txt

删除根目录下的 client/ 目录
echo y | coscmd delete -r client/

上传本地文件到 cos 目录
coscmd upload /opt/aa.txt /

上传本地文件夹 client 到 cos 根目录下的 client 目录，两个名字是对应
coscmd upload -r /opt/client client

上传本地文件夹 client 到 cos 根目录下的 client 目录的下面，所以要注意加不加斜杠的区别
coscmd upload -r /opt/client client/



```

-------------------------------------------------------------------


## COS Migration 工具

- 官网：<https://cloud.tencent.com/document/product/436/15392>

```
需要 JDK8 环境
Linux 环境需要 IFUNC 支持，确保环境 binutils 版本大于 2.20，查看方式：ld --version

下载：
cd /opt/jar
git clone --depth=1 https://github.com/tencentyun/cos_migrate_tool_v5.git

修改：./conf/config.ini

重点修改：
secretId=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
secretKey=yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
bucketName=mybucket-1251668577
cosPath=/client
localPath=/opt/jar/sculptor-boot-frontend-nuxt-pc/.nuxt/dist/client
entireFileMd5Attached=on

运行：sh start_migrate.sh

```



