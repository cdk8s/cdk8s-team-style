# Elasticsearch 知识

## Docker 单节点部署

- 官网：<https://hub.docker.com/_/elasticsearch>
- 官网列表：<https://www.docker.elastic.co/>
- 阿里云支持版本：<https://data.aliyun.com/product/elasticsearch>
    - 阿里云有一个 `插件配置` 功能，常用的 Elasticsearch 插件都带了，勾选下即可安装。也支持上传安装。
- 注意：docker 版本下 client.transport.sniff = true 是无效的。


#### 7.9.3（Windows zip 安装）

```
下载地址：
https://www.elastic.co/guide/en/elasticsearch/reference/7.9/install-elasticsearch.html

在 config/elasticsearch.yml 添加一条配置：
xpack.ml.enabled: false

然后启动：
.\bin\elasticsearch.bat

```

#### 7.9.3（Docker 带 ik 分词）

- 先测试下镜像下载网络情况，一般会很慢：`docker pull docker.elastic.co/elasticsearch/elasticsearch:7.9.3`
    - 如果实在下载不下来就用：`docker pull elasticsearch:7.9.3`
- `mkdir -p ~/docker/elasticsearch-7.9.3/data`
- `vim ~/docker/elasticsearch-7.9.3/elasticsearch-7.9.3-docker.yml`，内容如下
- 下载 ik 分词（版本必须和 Elasticsearch 版本对应，包括小版本号）：<https://github.com/medcl/elasticsearch-analysis-ik/tags>
- 下载 pinyin 分词（版本必须和 Elasticsearch 版本对应，包括小版本号）：<https://github.com/medcl/elasticsearch-analysis-pinyin/tags>
  - 百度云下载（提取码: 5t5m）：<https://pan.baidu.com/s/1CONDXhTZ7Khn3Lohh9clog>
- 把 ik 解压到如下目录：`/Users/meek/docker/elasticsearch-7.9.3/elasticsearch-analysis-ik-7.9.3`
- 把 pinyin 解压到如下目录：`/Users/meek/docker/elasticsearch-7.9.3/elasticsearch-analysis-pinyin-7.9.3`

```
version: '3'
services:
  elasticsearch1:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.9.3
    container_name: elasticsearch-7.9.3
    restart: always
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx1512m"
      - "cluster.name=elasticsearch"
      - "discovery.type=single-node"
      - "network.host=0.0.0.0"
      - "http.host=0.0.0.0"
      - "xpack.security.enabled=true"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - 9200:9200
      - 9300:9300
    volumes:
      - /Users/meek/docker/elasticsearch-7.9.3/data:/usr/share/elasticsearch/data
      - /Users/meek/docker/elasticsearch-7.9.3/elasticsearch-analysis-ik-7.9.3:/usr/share/elasticsearch/plugins/elasticsearch-analysis-ik-7.9.3
      - /Users/meek/docker/elasticsearch-7.9.3/elasticsearch-analysis-pinyin-7.9.3:/usr/share/elasticsearch/plugins/elasticsearch-analysis-pinyin-7.9.3
```

- 启动：`docker-compose -f ~/docker/elasticsearch-7.9.3/elasticsearch-7.9.3-docker.yml -p elasticsearch_7.9.3 up -d`
- 设置密码：

```
进入 docker 中的 elasticsearch中，设置密码：
docker exec -it elasticsearch-7.9.3 /bin/bash
/usr/share/elasticsearch/bin/elasticsearch-setup-passwords interactive
根据终端提示，会让你依次设置用户：elastic、apm_system、kibana_system、logstash_system、beats_system、remote_monitoring_user 的密码，所以整个过程比较多。

测试：
不输入密码，理论上会报错
curl http://127.0.0.1:9200
输入正确密码，返回集群信息：
curl -u "elastic:123456" http://127.0.0.1:9200


修改密码：
格式：curl -u elastic -H "Content-Type: application/json" -X POST "http://127.0.0.1:9200/_xpack/security/user/用户名/_password" --data '{"password":"新密码"}'
示例：curl -u elastic -H "Content-Type: application/json" -X POST "http://127.0.0.1:9200/_xpack/security/user/elastic/_password" --data '{"password":"1234567"}'
回车后会让你输入旧密码，输入正确后，会自动修改密码。

测试是否成功：
curl -u "elastic:1234567" http://127.0.0.1:9200

查看 license：
curl -u "elastic:123456" http://127.0.0.1:9200/_license

关于 license 官网说明：https://www.elastic.co/cn/subscriptions
JDBC 直连客户端开源是不能使用的。

所以我们需要先改为 30 天试用版：
发起一个 POST 请求：
curl --location --request POST -u "elastic:123456" 'http://127.0.0.1:9200/_license/start_trial?acknowledge=true&pretty' \
--header 'Content-Type: application/json' \
--data-raw '{
  "acknowledged" : true,
  "trial_was_started" : true,
  "type" : "trial"
}'

这样 DBeaver 才可以直连 Elasticsearch
```

- Elasticsearch Head 插件地址：<https://chrome.google.com/webstore/detail/ffmkiejjmecolpfloofpjologoblkegm>
- Elasticsearch Elasticvue 插件地址：<https://microsoftedge.microsoft.com/addons/detail/elasticvue/geifniocjfnfilcbeloeidajlfmhdlgo>
- 打开 Head 插件，选择 `复合查询` 测试：


```
http://localhost:9200/
_analyze?pretty   POST


{"analyzer":"ik_smart","text":"安徽省长江流域"}

{"analyzer":"pinyin","text":"安徽省长江流域"}
```

- ik_max_word 和 ik_smart 什么区别?

```
ik_max_word: 会将文本做最细粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,中华人民,中华,华人,人民共和国,人民,人,民,共和国,共和,和,国国,国歌”，会穷尽各种可能的组合，适合 Term Query；
ik_smart: 会做最粗粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”，适合 Phrase 查询。
```




#### 5.6.x

- `vim ~/elasticsearch-5.6.8-docker.yml`
- 启动：`docker-compose -f ~/elasticsearch-5.6.8-docker.yml -p elasticsearch_5.6.8 up -d`

```
version: '3'
services:
  elasticsearch1:
    image: docker.elastic.co/elasticsearch/elasticsearch:5.6.8
    container_name: elasticsearch-5.6.8
    restart: always
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "cluster.name=elasticsearch"
      - "network.host=0.0.0.0"
      - "http.host=0.0.0.0"
      - "xpack.security.enabled=false"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - 9200:9200
      - 9300:9300
    volumes:
      - ~/docker/elasticsearch/data:/usr/share/elasticsearch/data

```

#### 6.4.3（带 ik 分词）



- `vim ~/docker_data/elasticsearch-6.4.3-docker.yml`
- `mkdir -p ~/docker_data/elasticsearch-6.4.3/data`
- 启动：`docker-compose -f ~/docker_data/elasticsearch-6.4.3-docker.yml -p elasticsearch_6.4.3 up -d`
- 如果官网镜像比较慢可以换成阿里云：`registry.cn-hangzhou.aliyuncs.com/elasticsearch/elasticsearch:6.4.3`
- 下载 ik 分词（版本必须和 Elasticsearch 版本对应，包括小版本号）：<https://github.com/medcl/elasticsearch-analysis-ik>

```
version: '3'
services:
  elasticsearch1:
    image: docker.elastic.co/elasticsearch/elasticsearch:6.4.3
    container_name: elasticsearch-6.4.3
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "cluster.name=elasticsearch"
      - "discovery.type=single-node"
      - "network.host=0.0.0.0"
      - "http.host=0.0.0.0"
      - "xpack.security.enabled=false"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - 9200:9200
      - 9300:9300
    volumes:
      - ~/docker_data/elasticsearch-6.4.3/data:/usr/share/elasticsearch/data
      - ~/docker_data/ik-6.4.3:/usr/share/elasticsearch/plugins/ik
```

- Elasticsearch Head 插件地址：<https://chrome.google.com/webstore/detail/ffmkiejjmecolpfloofpjologoblkegm>
- 测试：


```
http://localhost:9200/
_analyze?pretty   POST


{"analyzer":"ik_smart","text":"安徽省长江流域"}
```

- ik_max_word 和 ik_smart 什么区别?

```
ik_max_word: 会将文本做最细粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,中华人民,中华,华人,人民共和国,人民,人,民,共和国,共和,和,国国,国歌”，会穷尽各种可能的组合，适合 Term Query；
ik_smart: 会做最粗粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”，适合 Phrase 查询。
```



#### 6.7.x（带 ik 分词）

- `vim ~/elasticsearch-6.7.2-docker.yml`
- `mkdir -p ~/docker/elasticsearch-6.7.2/data`
- 启动：`docker-compose -f ~/elasticsearch-6.7.2-docker.yml -p elasticsearch_6.7.2 up -d`
- 如果官网镜像比较慢可以换成阿里云：`registry.cn-hangzhou.aliyuncs.com/elasticsearch/elasticsearch:6.7.2`
- 下载 ik 分词（版本必须和 Elasticsearch 版本对应，包括小版本号）：<https://github.com/medcl/elasticsearch-analysis-ik>

```
version: '3'
services:
  elasticsearch1:
    image: docker.elastic.co/elasticsearch/elasticsearch:6.7.2
    container_name: elasticsearch-6.7.2
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "cluster.name=elasticsearch"
      - "discovery.type=single-node"
      - "network.host=0.0.0.0"
      - "http.host=0.0.0.0"
      - "xpack.security.enabled=false"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - 9200:9200
      - 9300:9300
    volumes:
      - ~/docker/elasticsearch-6.7.2/data:/usr/share/elasticsearch/data
      - ~/docker/ik:/usr/share/elasticsearch/plugins/ik
```

- Elasticsearch Head 插件地址：<https://chrome.google.com/webstore/detail/ffmkiejjmecolpfloofpjologoblkegm>
- 测试：


```
http://localhost:9200/
_analyze?pretty   POST


{"analyzer":"ik_smart","text":"安徽省长江流域"}
```

- ik_max_word 和 ik_smart 什么区别?

```
ik_max_word: 会将文本做最细粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,中华人民,中华,华人,人民共和国,人民,人,民,共和国,共和,和,国国,国歌”，会穷尽各种可能的组合，适合 Term Query；
ik_smart: 会做最粗粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”，适合 Phrase 查询。
```




#### 7.6.2（带 ik 分词）

- 先测试下镜像下载网络情况，一般会很慢：`docker pull docker.elastic.co/elasticsearch/elasticsearch:7.6.2`
    - 如果实在下载不下来就用：`docker pull elasticsearch:7.6.2`
- `vim ~/elasticsearch-7.6.2-docker.yml`，内容如下
- `mkdir -p ~/docker_data/elasticsearch-7.6.2/data`
- 启动：`docker-compose -f ~/elasticsearch-7.6.2-docker.yml -p elasticsearch_7.6.2 up -d`
- 下载 ik 分词（版本必须和 Elasticsearch 版本对应，包括小版本号）：<https://github.com/medcl/elasticsearch-analysis-ik>

```
version: '3'
services:
  elasticsearch1:
    image: elasticsearch:7.6.2
    container_name: elasticsearch-7.6.2
    environment:
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - "cluster.name=elasticsearch"
      - "discovery.type=single-node"
      - "network.host=0.0.0.0"
      - "http.host=0.0.0.0"
      - "xpack.security.enabled=false"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - 9200:9200
      - 9300:9300
    volumes:
      - ~/docker_data/elasticsearch-7.6.2/data:/usr/share/elasticsearch/data
      - ~/docker_data/ik-7.6.2:/usr/share/elasticsearch/plugins/ik
```

- Elasticsearch Head 插件地址：<https://chrome.google.com/webstore/detail/ffmkiejjmecolpfloofpjologoblkegm>
- 测试：


```
http://localhost:9200/
_analyze?pretty   POST


{"analyzer":"ik_smart","text":"安徽省长江流域"}
```

- ik_max_word 和 ik_smart 什么区别?

```
ik_max_word: 会将文本做最细粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,中华人民,中华,华人,人民共和国,人民,人,民,共和国,共和,和,国国,国歌”，会穷尽各种可能的组合，适合 Term Query；
ik_smart: 会做最粗粒度的拆分，比如会将“中华人民共和国国歌”拆分为“中华人民共和国,国歌”，适合 Phrase 查询。
```


-------------------------------------------------------------------

## 查看 Elasticsearch 健康状态

```
查看集群分布
curl -X GET 'http://192.168.0.18:9200/_cat/nodes?v'
ip           heap.percent ram.percent cpu load_1m load_5m load_15m node.role master name
192.168.0.19           37          98   0    0.05    0.06     0.05 mdi       -      elasticsearch-2
192.168.0.18           25          97   0    0.00    0.01     0.05 mdi       *      elasticsearch-1
192.168.0.20           22          96   0    0.00    0.01     0.05 mdi       -      elasticsearch-3

查看集群健康状态
curl -X GET 'http://192.168.0.18:9200/_cluster/health?pretty'
{
  "cluster_name" : "sacf",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 3,
  "number_of_data_nodes" : 3,
  "active_primary_shards" : 120,
  "active_shards" : 240,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}

查看索引清单健康状态
curl -X GET 'http://192.168.0.18:9200/_cluster/health?pretty&level=indices'

查看索引的分片的状态和位置（更加详细）
curl -X GET 'http://192.168.0.18:9200/_cluster/health?pretty&level=shards'
```

-------------------------------------------------------------------


## Elasticsearch 6.5.x 安装（适配与 5.5.x，6.6.x）

#### 环境

- CentOS 7.x
- 至少需要 2G 内存
- root 用户
- JDK 版本：1.8（最低要求），主推：JDK 1.8.0_121 以上
- 关闭 firewall
    - `systemctl stop firewalld.service` #停止firewall
    - `systemctl disable firewalld.service` #禁止firewall开机启动

#### 先配置部分系统变量

- 更多系统层面的配置可以看官网：<https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html>
- 配置系统最大打开文件描述符数：`vim /etc/sysctl.conf`

```
fs.file-max=65535
vm.max_map_count=262144
```

- 配置进程最大打开文件描述符：`vim /etc/security/limits.conf`

```
elasticsearch soft memlock unlimited
elasticsearch hard memlock unlimited
* soft nofile 262144
* hard nofile 262144
```

#### 开始安装

- 检查：`rpm -qa | grep elastic`
- 卸载：`rpm -e --nodeps elasticsearch`
- 官网 RPM 安装流程（重要，以下资料都是对官网的总结）：<https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html>
- 导入 KEY：`rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch`
- 新建文件：`vim /etc/yum.repos.d/elasticsearch.repo`
- 内容如下（6.x）：

```
[elasticsearch-6.x]
name=Elasticsearch repository for 6.x packages
baseurl=https://artifacts.elastic.co/packages/6.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

- 内容如下（5.x）：

```
[elasticsearch-5.x]
name=Elasticsearch repository for 5.x packages
baseurl=https://artifacts.elastic.co/packages/5.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

- 开始安装：`yum install -y elasticsearch`，预计文件有 108M 左右，国内网络安装可能会很慢，慢慢等
    - 安装完后会多了一个：elasticsearch 用户和组
- 设置 java 软链接：`ln -s /usr/local/jdk1.8.0_181/jre/bin/java /usr/local/sbin/java`
- 启动和停止软件（默认是不启动的）：
    - 启动：`systemctl start elasticsearch.service`
    - 状态：`systemctl status elasticsearch.service`
    - 停止：`systemctl stop elasticsearch.service`
    - 重新启动：`systemctl restart elasticsearch.service`
- 安装完成后，增加系统自启动：
    - `/bin/systemctl daemon-reload`
    - `/bin/systemctl enable elasticsearch.service`
- 检查：`curl -X GET "localhost:9200/"`

#### RPM 安装后的一些配置位置说明

- 更多说明可以看官网：<https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#rpm-configuring>
- 更加详细的配置可以看：<https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html>
- 默认系统生成了一个 elasticsearch 用户，下面的目录权限属于该用户
- Elasticsearch 安装后位置：`/usr/share/elasticsearch`
- Elasticsearch 的软件环境、堆栈的设置：`/etc/sysconfig/elasticsearch`
- Elasticsearch 的集群设置：`/etc/elasticsearch/elasticsearch.yml`
- Log 位置：`/var/log/elasticsearch/`
- 索引数据位置：`/var/lib/elasticsearch`
- 插件位置：`/usr/share/elasticsearch/plugins`
- 脚本文件位置：`/etc/elasticsearch/scripts`

#### 配置

- 编辑配置文件：`vim /etc/elasticsearch/elasticsearch.yml`
- 默认只能 localhost 访问，修改成支持外网访问

```
打开这个注释：#cluster.name: my-application
集群名称最好是自己给定，不然有些 client 端会连不上，或者要求填写

打开这个注释：#network.host: 192.168.0.1
改为：network.host: 0.0.0.0
```

#### 安装 X-Pack（6.5.x 默认带了 x-pack）

- `cd /usr/share/elasticsearch && bin/elasticsearch-plugin install x-pack`

#### GUI 客户端工具

- 优先推荐：<https://www.elastic-kaizen.com/download.html>
- <https://github.com/ElasticHQ/elasticsearch-HQ>


#### 安装 Chrome 扩展的 Head

- 下载地址：<https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm/>

#### 其他细节

- 如果就单个节点测试，新建索引的时候副本数记得填 0。

#### 创建索引并设置 mapping

- 官网类型说明：<https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html>

```
curl -XPUT 'http://127.0.0.1:9200/grafanadb' -H 'Content-Type: application/json' -d'
{
  "settings": {
    "refresh_interval": "5s",
    "number_of_shards": 5,
    "number_of_replicas": 0
  },
  "mappings": {
    "radar": {
      "properties": {
        "request_num": {
          "type": "long"
        },
        "post_date": {
          "type": "date",
          "format": "yyyy-MM-dd HH:mm:ss||epoch_millis"
        }
      }
    }
  }
}
'
```


#### 批量增加 / 删除测试数据

- 官网文档：<https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html>
- 批量增加，cURL 格式：

```
curl -X POST "http://127.0.0.1:9200/_bulk" -H 'Content-Type: application/json' -d'
{ "index" : { "_index" : "grafanadb", "_type" : "radar", "_id" : "100001" } }
{ "post_date" : "2018-12-01 10:00:00", "request_num" :  1 }
{ "index" : { "_index" : "grafanadb", "_type" : "radar", "_id" : "100002" } }
{ "post_date" : "2018-12-01 10:00:05", "request_num" :  2 }
{ "index" : { "_index" : "grafanadb", "_type" : "radar", "_id" : "100003" } }
{ "post_date" : "2018-12-01 10:00:10", "request_num" :  3 }
{ "index" : { "_index" : "grafanadb", "_type" : "radar", "_id" : "100004" } }
{ "post_date" : "2018-12-01 10:00:15", "request_num" :  4 }
{ "index" : { "_index" : "grafanadb", "_type" : "radar", "_id" : "100005" } }
{ "post_date" : "2018-12-01 10:00:20", "request_num" :  5 }
'
```

- 批量删除，cURL 格式：

```
curl -X POST "http://127.0.0.1:9200/_bulk" -H 'Content-Type: application/json' -d'
{ "delete": { "_index": "grafanadb", "_type": "radar", "_id": "100001" } }
{ "delete": { "_index": "grafanadb", "_type": "radar", "_id": "100002" } }
'
```

- 清空索引所有数据，分成5个切片去执行删除，cURL 格式：

```
curl -X POST "http://127.0.0.1:9200/索引名称/类型名称/_delete_by_query?refresh&slices=5&pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match_all": {}
  }
}
'
```




-------------------------------------------------------------------------------------------------------------------

## Elasticsearch 7.9.3 安装（CentOS 7.9）

```
官网安装说明：
https://www.elastic.co/guide/en/elasticsearch/reference/7.9/rpm.html

rpm包安装说明：
https://www.elastic.co/guide/en/elasticsearch/reference/7.9/rpm.html#install-rpm

已经做成了 Ansible Playbook，请查看 sculptor-boot-backend 项目下的 doc 目录 1-software-include-elasticsearch-playbook.yml
```



-------------------------------------------------------------------------------------------------------------------


## Elasticsearch 5.2.0 安装

- 官网下载地址：<https://www.elastic.co/cn/downloads/elasticsearch>
- Elasticsearch 5.2.0 版本下载地址（32M）：<https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.2.0.zip>


### 环境

- 机子 IP：192.168.1.127
- CentOS 7.3
- JDK 版本：1.8（最低要求），主推：JDK 1.8.0_121 以上
- Elasticsearch 版本：5.2.0
- 关闭 firewall
    - `systemctl stop firewalld.service` #停止firewall
    - `systemctl disable firewalld.service` #禁止firewall开机启动


### zip 解压安装

- 官网总的安装文档：<https://www.elastic.co/guide/en/elasticsearch/reference/5.x/zip-targz.html>
- 我的解压目录：`/usr/program`，解压包名：`elasticsearch-5.2.0.zip`
- 解压：`cd /usr/program ; unzip elasticsearch-5.2.0.zip`
- 删除掉压缩包：`rm -rf elasticsearch-5.2.0.zip`
- 添加组和用户
    - 该版本不能使用 root 用户进行使用
    - `useradd elasticsearch -p 123456`，添加一个名为 elasticsearch 的用户，还有一个同名的组
- 添加数据目录：`mkdir -p /opt/elasticsearch/data /opt/elasticsearch/log`
- 赋权限：
    - `chown -R elasticsearch:elasticsearch /usr/program/elasticsearch-5.2.0 /opt/elasticsearch`
- 编辑配置文件：`vim /usr/program/elasticsearch-5.2.0/config/elasticsearch.yml`，打开下面注释，并修改

``` nginx
cluster.name: youmeek-cluster
node.name: youmeek-node-1
path.data: /opt/elasticsearch/data
path.logs: /opt/elasticsearch/log
bootstrap.memory_lock: true
network.host: 0.0.0.0 # 也可以是本机 IP
http.port: 9200
discovery.zen.ping.unicast.hosts: ["192.168.1.127"]  #如果有多个机子集群，这里就写上这些机子的 IP，格式：["192.168.1.127","192.168.1.126"]
```

- 重点说明：Elasticsearch 的集群环境，主要就是上面这段配置文件内容的差别。如果有其他机子：node.name、discovery.zen.ping.unicast.hosts 需要改下。集群中所有机子的配置文件中 discovery.zen.ping.unicast.hosts 都要有所有机子的 IP 地址。
- 修改这个配置文件，不然无法锁内存：`vim /etc/security/limits.conf`
- 在文件最尾部增加下面内容：

``` nginx
# allow user 'elasticsearch' mlockall
elasticsearch soft memlock unlimited
elasticsearch hard memlock unlimited
* soft nofile 262144
* hard nofile 262144
```

- 修改：`vim /etc/sysctl.conf`，添加下面配置

``` ini
vm.max_map_count=262144
```

- 重启机子：`reboot`。
- 切换用户：`su elasticsearch`
- 控制台运行（启动比较慢）：`cd /usr/program/elasticsearch-5.2.0 ; ./bin/elasticsearch`
- 后台运行：`cd /usr/program/elasticsearch-5.2.0 ; ./bin/elasticsearch -d -p 自定义pid值`
- 在本机终端输入该命令：`curl -X GET 'http://192.168.1.127:9200'`，（也可以用浏览器访问：<http://192.168.1.127:9200/>）如果能得到如下结果，则表示启动成功：

``` json
{
  "name" : "youmeek-node-1",
  "cluster_name" : "youmeek-cluster",
  "cluster_uuid" : "c8RxQdOHQJq-Tg8rrPi_UA",
  "version" : {
    "number" : "5.2.0",
    "build_hash" : "24e05b9",
    "build_date" : "2017-01-24T19:52:35.800Z",
    "build_snapshot" : false,
    "lucene_version" : "6.4.0"
  },
  "tagline" : "You Know, for Search"
}
```

-------------------------------------------------------------------

## 安装 Kibana 5.2.0（7.9.3）

- 官网下载地址：<https://www.elastic.co/cn/downloads/kibana>
- macOS：<https://artifacts.elastic.co/downloads/kibana/kibana-7.9.3-darwin-x86_64.tar.gz>
- Kibana 5.2.0 版本下载地址（36M）：<https://artifacts.elastic.co/downloads/kibana/kibana-5.2.0-linux-x86_64.tar.gz>
- Kibana 5.2.0 官网文档：<https://www.elastic.co/guide/en/kibana/5.2/index.html>
- Kibana 5.2.0 官网安装文档：<https://www.elastic.co/guide/en/kibana/5.2/targz.html>

### tar.gz 解压安装

- 安装目录：/usr/program
- 解压：`cd /usr/program ; tar zxvf kibana-5.2.0-linux-x86_64.tar.gz`
- 删除压缩包：`rm -rf kibana-5.2.0-linux-x86_64.tar.gz`
- 修改解压后的目录名称：`mv kibana-5.2.0-linux-x86_64 kibana-5.2.0`
- 修改配置：`vim /usr/program/kibana-5.2.0/config/kibana.yml`，默认配置都是注释的，我们这里打开这些注释：

``` nginx
server.port: 5601
server.host: "0.0.0.0" # 请将这里改为 0.0.0.0 或是当前本机 IP，不然可能会访问不了
erver.name: "youmeek-kibana"
elasticsearch.url: "http://192.168.1.127:9200"
elasticsearch.username: "elasticsearch"
elasticsearch.password: "123456"
```

- 运行：`cd /usr/program/kibana-5.2.0 ; ./bin/kibana`
- 浏览器访问：<http://192.168.1.127:5601>，可以看到 Kibana `Configure an index pattern` 界面
- 访问 Dev Tools 工具，后面写 DSL 语句会常使用该功能：<http://192.168.1.127:5601/app/kibana#/dev_tools/console?_g=()>

-------------------------------------------------------------------


## Beats

### Beats 资料

- Beats 官网：<https://www.elastic.co/cn/products/beats>
- Beats 简单介绍：日志数据搜集器。一般安装在需要收集日志的服务器上，然后把收集的数据发送到 Elasticsearch 或是先发送到 logstash 清洗整理（解析过滤）后再发送到 Elasticsearch。
    - logstash 也有收集日志的功能，只是它相对 Beats 更加消耗 CPU 和内存，所以一般使用 Beats 收集日志。
- 目前常见的 Beats 类型：
    - Filebeat（搜集文件数据）；
    - Packetbeat（搜集网络流量数据）；
    - Metricbeat（搜集系统、进程和文件系统级别的 CPU 和内存使用情况等数据）；
    - Winlogbeat（搜集 Windows 事件日志数据）。
    - Heartbeat（主动探测服务是否可用）。

## 安装 X-Pack 或是其他插件

- X-Pack 是官网提供的管理增强工具，但是全部功能收费，有一个月使用，有部分功能免费。其他免费的插件。
    - licence 的用法可以看这篇文章：
        - <http://blog.csdn.net/abcd_d_/article/details/53178798>
        - <http://blog.csdn.net/AbnerSunYH/article/details/53436212>
        - 破解：<http://www.lofter.com/lpost/33be15_d4fd028>
    - 免费插件：
    - head - 节点数据查看管理：<https://github.com/mobz/elasticsearch-head>
    - kopf - 集群管理：<https://github.com/lmenezes/elasticsearch-kopf>
- 官网说明：<https://www.elastic.co/guide/en/x-pack/5.2/installing-xpack.html>
- 安装（过程比较慢）：`/usr/share/elasticsearch/bin/elasticsearch-plugin install x-pack`
- 如果线上安装速度太慢，那就离线安装：
    - 下载，我放在 /opt 目录下（119M）：`wget https://artifacts.elastic.co/downloads/packs/x-pack/x-pack-5.2.2.zip`
    - 安装：`/usr/share/elasticsearch/bin/elasticsearch-plugin install file:///opt/x-pack-5.2.2.zip`
- 卸载：`/usr/share/elasticsearch/bin/elasticsearch-plugin remove x-pack`
- 安装后重启服务，重启后访问你会发现需要用户和密码，我们可以关掉这个，在 elasticsearch.yml 中添加：`xpack.security.enabled: false`
- 其他 5.2 资料：
    - <https://blog.yourtion.com/install-x-pack-for-elasticsearch-and-kibana.html>
    - <https://www.ko178.cn/?p=353>
    - <https://my.oschina.net/HeAlvin/blog/828639>
    - <http://www.jianshu.com/p/004765d2238b>
    - <http://www.cnblogs.com/delgyd/p/elk.html>
    - <http://www.itdadao.com/articles/c15a1135185p0.html>
    - <http://www.busyboy.cn/?p=920>
    - <http://nosmoking.blog.51cto.com/3263888/1897989>
    - <http://www.freebuf.com/sectool/139687.html>

-------------------------------------------------------------------------------------------------------------------


## 2.4.X

### 安装 elasticsearch 集群

### 下载

- 下载在我个人习惯的子自己创建的目录下：/usr/program/elk
- elasticsearch 2.4.1（26 M）：`wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-2.4.1.tar.gz`
- logstash 2.4.0（80 M）：`wget https://download.elastic.co/logstash/logstash/logstash-2.4.1.tar.gz`
- kibana 4.6.1（32 M）：`wget https://download.elastic.co/kibana/kibana/kibana-4.6.1-linux-x86_64.tar.gz`

### tar 解压安装

- **确保系统安装有 JDK**
- 官网文档：<https://www.elastic.co/guide/en/elasticsearch/reference/5.2/zip-targz.html>
- 添加日志存放目录、数据存放目录：`mkdir -p /opt/elasticsearch/data /opt/elasticsearch/log`
- 添加组和用户
    - 该版本不能使用 root 用户进行使用
    - `useradd elasticsearch -p 123456`，添加一个名为 elasticsearch 的用户，还有一个同名的组
- 解压下载的文件
    - `cd /usr/program/elk`
    - `tar zxvf elasticsearch-2.4.1.tar.gz`
- 赋权限：
    - `chown -R elasticsearch:elasticsearch /usr/program/elk /opt/elasticsearch`
- 我 tar 安装后一些路径说明：
    - home：`/usr/program/elk/elasticsearch-2.4.1`
    - bin：`/usr/program/elk/elasticsearch-2.4.1/bin`
    - 配置文件：`/usr/program/elk/elasticsearch-2.4.1/config/elasticsearch.yml`
    - plugins：`/usr/program/elk/elasticsearch-2.4.1/plugins`
    - script：`/usr/program/elk/elasticsearch-2.4.1/scripts`
    - data：`/opt/elasticsearch/data`
    - log：`/opt/elasticsearch/log/集群名称.log`
- 编辑配置文件：`vim /usr/program/elk/elasticsearch-2.4.1/config/elasticsearch.yml`，打开下面注释，并修改

``` nginx
cluster.name: gitnavi-cluster
node.name: gitnavi-node-1
path.data: /opt/elasticsearch/data
path.logs: /opt/elasticsearch/log
bootstrap.memory_lock: true
network.host: 0.0.0.0 # 也可以是本机 IP
http.port: 9200
discovery.zen.ping.multicast.enabled: false
discovery.zen.ping.unicast.hosts: ["192.168.1.127", "192.168.1.126"]  #这个为两台机子的 IP 地址
```

- 修改这个配置文件，不然无法锁内存：`vim /etc/security/limits.conf`
- 在文件最尾部增加下面内容：

``` nginx
# allow user 'elasticsearch' mlockall
elasticsearch soft memlock unlimited
elasticsearch hard memlock unlimited
* soft nofile 262144
* hard nofile 262144
```

- 关闭 firewall
    - `systemctl stop firewalld.service` #停止firewall
    - `systemctl disable firewalld.service` #禁止firewall开机启动

- 切换到 elasticsearch 用户下：`su elasticsearch`
- 带控制台的启动（比较慢）：`/usr/program/elk/elasticsearch-2.4.1/bin/elasticsearch`
    - 控制台会输出类似这样的信息：

```
[2017-03-13 18:42:51,170][INFO ][node                     ] [gitnavi-node-1] version[2.4.1], pid[21156], build[c67dc32/2016-09-27T18:57:55Z]
[2017-03-13 18:42:51,177][INFO ][node                     ] [gitnavi-node-1] initializing ...
[2017-03-13 18:42:51,821][INFO ][plugins                  ] [gitnavi-node-1] modules [reindex, lang-expression, lang-groovy], plugins [head, kopf], sites [head, kopf]
[2017-03-13 18:42:51,852][INFO ][env                      ] [gitnavi-node-1] using [1] data paths, mounts [[/ (rootfs)]], net usable_space [12.4gb], net total_space [17.4gb], spins? [unknown], types [rootfs]
[2017-03-13 18:42:51,852][INFO ][env                      ] [gitnavi-node-1] heap size [1015.6mb], compressed ordinary object pointers [true]
[2017-03-13 18:42:54,094][INFO ][node                     ] [gitnavi-node-1] initialized
[2017-03-13 18:42:54,094][INFO ][node                     ] [gitnavi-node-1] starting ...
[2017-03-13 18:42:54,175][INFO ][transport                ] [gitnavi-node-1] publish_address {192.168.1.127:9300}, bound_addresses {[::]:9300}
[2017-03-13 18:42:54,178][INFO ][discovery                ] [gitnavi-node-1] gitnavi-cluster/-XywT60EScO-9lgzjfnsgg
[2017-03-13 18:42:57,344][INFO ][cluster.service          ] [gitnavi-node-1] new_master {gitnavi-node-1}{-XywT60EScO-9lgzjfnsgg}{192.168.1.127}{192.168.1.127:9300}, reason: zen-disco-join(elected_as_master, [0] joins received)
[2017-03-13 18:42:57,410][INFO ][gateway                  ] [gitnavi-node-1] recovered [0] indices into cluster_state
[2017-03-13 18:42:57,414][INFO ][http                     ] [gitnavi-node-1] publish_address {192.168.1.127:9200}, bound_addresses {[::]:9200}
[2017-03-13 18:42:57,414][INFO ][node                     ] [gitnavi-node-1] started
```

- 守护进程方式启动：`/usr/program/elk/elasticsearch-2.4.1/bin/elasticsearch -d`
- 守护进程方式停止：`ps -ef|grep elasticsearc`，只能通过 kill pid 来结束
- 访问：`http://192.168.1.127:9200/`，可以看到如下内容：

``` json
{
  "name" : "gitnavi-node-1",
  "cluster_name" : "gitnavi-cluster",
  "cluster_uuid" : "0b66dYpnTd-hh7x4Phfm1A",
  "version" : {
    "number" : "2.4.1",
    "build_hash" : "c67dc32e24162035d18d6fe1e952c4cbcbe79d16",
    "build_timestamp" : "2016-09-27T18:57:55Z",
    "build_snapshot" : false,
    "lucene_version" : "5.5.2"
  },
  "tagline" : "You Know, for Search"
}
```

- 插件（插件的迭代很容易跟不上官网的版本，所以请牢记关注插件官网的说明）
    - head，节点数据查看管理：<https://github.com/mobz/elasticsearch-head>
    - kopf，集群管理：<https://github.com/lmenezes/elasticsearch-kopf>
    - Bigdesk，监控查看CPU内存索引数据搜索情况http连接数：<https://github.com/hlstudio/bigdesk>
- 安装（过程比较慢）
    - head：`/usr/program/elk/elasticsearch-2.4.1/bin/plugin install mobz/elasticsearch-head`
        - 安装完的访问地址：`http://192.168.1.127:9200/_plugin/head`
    - kopf：`/usr/program/elk/elasticsearch-2.4.1/bin/plugin install lmenezes/elasticsearch-kopf`
        - 安装完的访问地址：`http://192.168.1.127:9200/_plugin/kopf`
    - Bigdesk：`/usr/program/elk/elasticsearch-2.4.1/bin/plugin install hlstudio/bigdesk`
        - 安装完的访问地址：`http://192.168.1.127:9200/_plugin/bigdesk`
    - 卸载：`/usr/share/elasticsearch/bin/elasticsearch-plugin remove 插件名称`
- IK 分词插件的安装（**重点：所有节点都需要安装此插件**）
    - IK 分词官网：<https://github.com/medcl/elasticsearch-analysis-ik>
    - 官网首页已经有一个表格说明 ES 版本和 IK 插件的版本对应，我们可以看到：ES 2.4.1 对应 IK 分词 1.10.1，下载地址：<https://github.com/medcl/elasticsearch-analysis-ik/releases/tag/v1.10.1>
    - 进入 ES 插件目录：`cd /usr/program/elk/elasticsearch-2.4.1/plugins`
    - 创建 ik 目录：`mkdir ik`
    - 把下载的 elasticsearch-analysis-ik-1.10.1.zip 上传到刚新建的 ik 目录下
    - 解压：`unzip elasticsearch-analysis-ik-1.10.1.zip`
    - 删除压缩包：`rm -rf elasticsearch-analysis-ik-1.10.1.zip`
    - 编辑 ES 配置文件：`vim /usr/program/elk/elasticsearch-2.4.1/config/elasticsearch.yml`
        - 在文件底部添加如下内容：

``` ini
index.analysis.analyzer.default.tokenizer : "ik_max_word"
index.analysis.analyzer.default.type: "ik"
```

- 重启 ES ： /usr/program/elk/elasticsearch-2.4.1/bin/elasticsearch
- 验证 ik 插件，浏览器访问：<http://192.168.1.127:9200/_analyze?analyzer=ik&pretty=true&text=这是一个针对程序员优化的导航GitNavi.com>，能得到如下结果就表示成功：

``` json
[
  {
    "token": "这是",
    "start_offset": 0,
    "end_offset": 2,
    "type": "CN_WORD",
    "position": 0
  },
  {
    "token": "一个",
    "start_offset": 2,
    "end_offset": 4,
    "type": "CN_WORD",
    "position": 1
  },
  {
    "token": "一",
    "start_offset": 2,
    "end_offset": 3,
    "type": "TYPE_CNUM",
    "position": 2
  },
  {
    "token": "个",
    "start_offset": 3,
    "end_offset": 4,
    "type": "COUNT",
    "position": 3
  },
  {
    "token": "针对",
    "start_offset": 4,
    "end_offset": 6,
    "type": "CN_WORD",
    "position": 4
  },
  {
    "token": "程序员",
    "start_offset": 6,
    "end_offset": 9,
    "type": "CN_WORD",
    "position": 5
  },
  {
    "token": "程序",
    "start_offset": 6,
    "end_offset": 8,
    "type": "CN_WORD",
    "position": 6
  },
  {
    "token": "序",
    "start_offset": 7,
    "end_offset": 8,
    "type": "CN_WORD",
    "position": 7
  },
  {
    "token": "员",
    "start_offset": 8,
    "end_offset": 9,
    "type": "CN_CHAR",
    "position": 8
  },
  {
    "token": "优化",
    "start_offset": 9,
    "end_offset": 11,
    "type": "CN_WORD",
    "position": 9
  },
  {
    "token": "导航",
    "start_offset": 12,
    "end_offset": 14,
    "type": "CN_WORD",
    "position": 10
  },
  {
    "token": "航",
    "start_offset": 13,
    "end_offset": 14,
    "type": "CN_WORD",
    "position": 11
  },
  {
    "token": "gitnavi.com",
    "start_offset": 14,
    "end_offset": 25,
    "type": "LETTER",
    "position": 12
  },
  {
    "token": "gitnavi",
    "start_offset": 14,
    "end_offset": 21,
    "type": "ENGLISH",
    "position": 13
  },
  {
    "token": "com",
    "start_offset": 22,
    "end_offset": 25,
    "type": "ENGLISH",
    "position": 14
  }
]
```

- Elasticsearch 5.x 版本之后，就不需要再修改这个配置文件了 `/usr/program/elk/elasticsearch-2.4.1/config/elasticsearch.yml`，直接解压 zip 后，直接可以启动使用。可以访问这个进行测试：<http://192.168.1.127:9200/_analyze?analyzer=ik_max_word&pretty=true&text=这是一个针对程序员优化的导航GitNavi.com>
- 其他一些配置文件：
    - main.dic，内置中文词库文件是，差不多有 27W 条记录。
    - stopword.dic，英文停用词，一般不会被分词，不会存放在倒排索引中。
    - quantifier.dic，用来存放一些量词。
    - suffix.dic，用来存放后缀词。
    - surname.dic，姓氏。
- 自定义分词词库：
    - 修改配置文件：IKAnalyzer.cfg.xml
    - 在 ext_dict 标签中指定我们自己新增的 dic 文件（给的 demo 路径是 custom 目录下）。
    - 修改完重启下 Elasticsearch 集群
- 自定义停用词库：
    - 修改配置文件：IKAnalyzer.cfg.xml
    - 在 ext_stopwords 标签中指定我们自己新增的 dic 文件（给的 demo 路径是 custom 目录下）。
    - 修改完重启下 Elasticsearch 集群


### 构建 elasticsearch 集群

- 另外一台机子也同样这样安装，但是有几个地方有差别：
    - 特别注意：集群的关键点是配置文件中的：cluster.name，这个一样就表示在一个集群中
    - 配置文件：`/usr/program/elk/elasticsearch-2.4.1/config/elasticsearch.yml`
        - node 名称改为不一样的，比如我这边改为 2：node.name: gitnavi-node-2
    - 插件不用安装，有一台机子安装即可
    - 先启动装有 head 的机子，然后再启动另外一台，这样好辨别


-------------------------------------------------------------------

## 常用 Elasticsearch 命令（查询系统类）

```
- 查询集群健康状况：GET /_cat/health?v
```

-------------------------------------------------------------------


## 常用 Elasticsearch 命令（查询索引类）

```
- 查询集群中有哪些索引：GET /_cat/indices?v
- 查询所有索引配置信息：GET /_all/_settings
- 查询索引配置信息：GET /es-api-sculptor-boot-backend_def-url/_settings
- 查询多个索引配置信息：GET /product_index,es-api-sculptor-boot-backend_def-url/_settings
```


-------------------------------------------------------------------

## 常用 Elasticsearch 命令（操作索引类）

```
- 简单的索引操作：
- 删除指定索引：DELETE /product_index
- 删除指定多个索引：DELETE /product_index,order_index
- 删除匹配符索引：DELETE /product_*
- 删除所有索引：DELETE /_all

新增索引：
PUT /order_index
{
  "settings": {
    "index": {
      "number_of_shards": 5,
      "number_of_replicas": 1
    }
  }
}


修改索引副本：
PUT /order_index/_settings
{
	"number_of_replicas": 2
}


新增索引并设置mapping
PUT /product_index
{
  "settings": {
    "refresh_interval": "5s",
    "number_of_shards": 5,
    "number_of_replicas": 1
  },
  "mappings": {
    "product": {
      "properties": {
        "id": {
          "type": "text",
          "index": "not_analyzed"
        },
        "product_name": {
          "type": "text",
          "store": "no",
          "term_vector": "with_positions_offsets",
          "analyzer": "ik_max_word",
          "search_analyzer": "ik_max_word",
          "boost": 5,
          "fields": {
            "keyword": {
                "type": "keyword",
                "ignore_above": 256
            }
          }
        },
        "product_desc": {
          "type": "text",
          "index": "not_analyzed"
        },
        "price": {
          "type": "double",
          "index": "not_analyzed"
        },
        "created_date_time": {
          "type": "date",
          "index": "not_analyzed",
          "format": "basic_date_time"
        },
        "last_modified_date_time": {
          "type": "date",
          "index": "not_analyzed",
          "format": "basic_date_time"
        },
        "version": {
          "type": "long",
          "index": "no"
        }
      }
    }
  }
}





```


-------------------------------------------------------------------

## 常用 Elasticsearch 命令（操作数据类）

```

插入一条数据：如果没有 Index 会自动提前在创建
PUT /product_index/_doc/1
{
    "product_name" : "PHILIPS toothbrush HX6730/02",
    "product_desc" :  "【3?9 元，前 1000 名赠刷头，6 月 1 日 0 点火爆开抢，618 开门红巅峰 48 小时，抢先加入购物车】飞利浦畅销款，万千好评！深入净齿，智能美白！",
    "price" :  399.00
}



更新整个 Document（需要带上所有属性，注意细节，这里改了 product_name）：
这种方式的本质是：软删除。把旧版本标记为 deleted，实际还没物理删除，该条数据的 _version 元数据其实会再 +1 的。如果你再 PUT 下还是这个 ID 数据进去，_version 还是会继续 +1。当 Elasticsearch 数据越来越多，会物理删除这些标记的数据。

PUT /product_index/_doc/3
{
    "product_name" : "星空太空 iphone7 plus 蓝紫色 6s 繁星 7plus 宇宙 se 原创保护苹果 5 包手机壳",
    "product_desc" :  "一说到星空，就有太多美好的记忆，美丽的浩瀚宇宙，有太多说不清的神秘之处，星空太美丽，太绚烂！",
    "price" :  36.00
}

- 更新 Document 其中一个 field：（这种叫做：partial update，整个流程本质跟全量更新差不多，都是先把旧的标记为 deleted，新的数据创建。只是查询这个过程是在 Elasticsearch 内部，效率更高。）
POST /product_index/_doc/3/_update
{
  "doc": {
    "product_name": "星空太空 iphone7 蓝紫色 6s 繁星 iphone7 plus 宇宙 se 原创保护苹果 5 包手机壳"
  }
}


通过 ID 删除：DELETE /product_index/_doc/3，本质：标记为 deleted，等数据越来越大的情况 Elasticsearch 才去物理删除。

批量插入：
POST /product_index/_bulk
{ "index" : { "_id" : "100001" } }
{ "post_date" : "2018-12-01 10:00:00", "request_num" :  1 }
{ "index" : { "_id" : "100002" } }
{ "post_date" : "2018-12-01 10:00:05", "request_num" :  2 }

- 批量删除
POST /product_index/_bulk
{ "delete": { "_id": "100001" } }
{ "delete": { "_id": "100002" } }
```

-------------------------------------------------------------------

## 常用 Elasticsearch 命令（查询数据类）

```
查询所有：
GET /product_index/_search
{
  "query": {
    "match_all": {}
  }
}


查询第 4 页（4 x 10 = 40），每页 10 条：
GET /es-api-sculptor-boot-backend_def-url/_search
{
	"query": {
		"query_string": {
			"query": "*"
		}
	},
	"from": 40,
	"size": 10,
	"sort": []
}

- 查询商品名称包含 toothbrush 的商品，同时按照价格降序排序：
GET /product_index/_search
{
  "query": {
    "match": {
      "product_name": "toothbrush"
    }
  },
  "sort": [
    {
      "price": "desc"
    }
  ]
}



多搜索条件组合查询（最常用）
- bool 下包括：must（必须匹配，类似于数据库的 =），must_not（必须不匹配，类似于数据库的 !=），should（没有强制匹配，类似于数据库的 or），filter（过滤）
GET /product_index/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "product_name": "PHILIPS toothbrush"
          }
        }
      ],
      "should": [
        {
          "match": {
            "product_desc": "刷头"
          }
        }
      ],
      "must_not": [
        {
          "match": {
            "product_name": "HX6730"
          }
        }
      ],
      "filter": {
        "range": {
          "price": {
            "gte": 33.00
          }
        }
      }
    }
  }
}

GET /product_index/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "term": {
            "product_name": "飞利浦"
          }
        },
        {
          "bool": {
            "must": [
              {
                "term": {
                  "product_desc": "刷头"
                },
                "term": {
                  "price": 30
                }
              }
            ]
          }
        }
      ]
    }
  }
}



- 通过 ID 查询（默认返回所有元数据）：GET /product_index/_doc/3
- 通过 ID 查询（返回指定元数据）：GET /product_index/_doc/1?_source=product_name,product_desc
- 查询指定索引的所有数据：GET /product_index/_search
- 设置查询超时：GET /product_index/_doc/_search?timeout=5s
- 查询多个索引：GET /product_index,order_index/_search
- 查询多个索引、多个类型：GET /product_index,order_index/product,order/_search
- 查询所有索引、多个类型：GET /_all/product,order/_search
- 匹配符模糊查询多个索引：GET /product_*/_search
- 通过商品名搜索，并价格倒序：GET /product_index/_doc/_search?q=product_name:toothbrush&sort=price:desc
- 通过商品名搜索（商品名称不等于搜索词，这里用了减号），并价格倒序：GET /product_index/_doc/_search?q=-product_name:toothbrush&sort=price:desc


深度分页：scroll = 1m 表示用来缓存时间
GET /es-api-sculptor-boot-backend_def-url/_search?scroll=1m
{
  "query": {
    "match_all": {}
  },
  "sort": [],
  "size": 10
}
上面的查询结果会返回一个 scroll_id，下面的查询可以用 scroll_id 继续查询。其他条件不需要再加，scroll_id 已经有记录。因为只缓存 1m，必须在 1m 中查询，不然 scroll_id 会失效。：
GET /_search/scroll
{
    "scroll": "1m", 
    "scroll_id" : "FGluY2x1ZGVfY29udGV4dF91dWlkDXF1ZXJ5QW5kRmV0Y2gBFEEwN29sb0VCdGZ5aFJHQmU1ajlEAAAAAAAABCMWblJXUWVHQnhUYkMydjhISjNlTUg5Zw=="
}

- 指定查询结果字段（field）
GET /product_index/_search
{
  "query": {
    "match_all": {}
  },
  "_source": [
    "product_name",
    "price"
  ]
}


- 搜索商品名称包含 toothbrush，而且售价大于 400 元，小于 700 的商品
|符号标识|代表含义|
|---|---|
|gte|大于或等于|
|gt|大于|
|lte|小于或等于|
|lt|小于|

GET /product_index/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "product_name": "toothbrush"
        }
      },
      "filter": {
        "range": {
          "price": {
            "gt": 400,
            "lt": 700
          }
        }
      }
    }
  }
}


- match 查询的字段内容是进行分词处理的
- 索引中只要有任意一个匹配拆分后词就可以出现在结果中，只是匹配度越高的排越前面
- 比如查询：PHILIPS toothbrush，会被拆分成两个单词：PHILIPS 和 toothbrush。只要索引中 product_name 中只要含有任意对应单词，都会在搜索结果中，只是如果有数据同时含有这两个单词，则排序在前面。
GET /product_index/_search
{
  "query": {
    "match": {
      "product_name": "PHILIPS toothbrush"
    }
  }
}


- 索引中必须同时匹配拆分后词就可以出现在结果中
- 比如查询：PHILIPS toothbrush，会被拆分成两个单词：PHILIPS 和 toothbrush。索引中必须有同时有这两个单词的才会在结果中。
GET /product_index/_search
{
  "query": {
    "match_phrase": {
      "product_name": "PHILIPS toothbrush"
    }
  }
}


- term 用法（与 match 进行对比）（term 一般用在不分词字段上的，因为它是完全匹配查询，如果要查询的字段是分词字段就会被拆分成各种分词结果，和完全查询的内容就对应不上了。）：
- 所以自己设置 mapping 的时候有些不分词的时候就最好设置不分词。
- 其实 Elasticsearch 5.X 之后给 text 类型的分词字段，又默认新增了一个子字段 keyword，这个字段的类型就是 keyword，是不分词的，默认保留 256 个字符。假设 product_name 是分词字段，那有一个 product_name.keyword 是不分词的字段，也可以用这个子字段来做完全匹配查询。
GET /product_index/_search
{
  "query": {
    "term": {
      "product_name": "PHILIPS toothbrush"
    }
  }
}

terms 用法，类似于数据库的 in
GET /product_index/product/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "terms": {
          "product_name": [
            "toothbrush",
            "shell"
          ]
        }
      }
    }
  }
}



- multi_match 用法：
- 查询 product_name 和 product_desc 字段中，只要有：toothbrush 关键字的就查询出来。
GET /product_index/_search
{
  "query": {
    "multi_match": {
      "query": "toothbrush",
      "fields": [
        "product_name",
        "product_desc"
      ]
    }
  }
}


- multi_match 跨多个 field 查询，表示查询分词必须出现在相同字段中。
GET /product_index/product/_search
{
  "query": {
    "multi_match": {
      "query": "PHILIPS toothbrush",
      "type": "cross_fields",
      "operator": "and",
      "fields": [
        "product_name",
        "product_desc"
      ]
    }
  }
}



- range 用法，查询数值、时间区间：
GET /product_index/_search
{
  "query": {
    "range": {
      "price": {
        "gte": 30.00
      }
    }
  }
}







- Highlight Search 高亮搜索
- 给匹配拆分后的查询词增加高亮的 html 标签，比如这样的结果：`"<em>PHILIPS</em> <em>toothbrush</em> HX6730/02"`
GET /product_index/_search
{
  "query": {
    "match": {
      "product_name": "PHILIPS toothbrush"
    }
  },
  "highlight": {
    "fields": {
      "product_name": {}
    }
  }
}

```


## 资料

- <>
- <>