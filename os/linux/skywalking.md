# SkyWalking 安装和配置


## OpenAPM 相关

- 目前市场工具一览：<https://openapm.io/landscape>
- 目前最活跃的标准：[OpenTracing](https://opentracing.io/)
- 现在比较活跃的应该是：
    - [Jaeger](https://www.jaegertracing.io/)
    - [SkyWalking](https://skywalking.apache.org/)


## 官网资料

- 当前时间：2019-05，最新版本：6.1
- 当前时间：2020-11，最新版本：8.2
- 官网：<https://skywalking.apache.org/>
- 官网 Github：<https://github.com/apache/skywalking>
- 官网文档：<https://github.com/apache/skywalking/blob/master/docs/README.md>
- 官网下载：<http://skywalking.apache.org/downloads/>
    - 2020-11：现在有 Binary Distribution for ElasticSearch 7 版本，不需要自己编译
    - 该网页显示：官网目前推荐的是通过源码构建出包，docker 镜像推荐
    - 源码构建方法：<https://github.com/apache/skywalking/blob/master/docs/en/guides/How-to-build.md>
- 这里简单抽取下核心内容：
- 至少需要 jdk8 + maven3
- 需要 Elasticsearch
    - Elasticsearch 和 SkyWalking 的所在服务器的时间必须一致
    - 看了下源码依赖的 Elasticsearch 依赖包，目前支持 5.x 和 6.x


## Docker 版本使用

```
docker run --name skywalking-oap-server -d \
--restart=always \
-e TZ=Asia/Shanghai \
-p 12800:12800 \
-p 11800:11800 \
-e SW_STORAGE=elasticsearch7 \
-e SW_STORAGE_ES_CLUSTER_NODES=192.168.31.88:9200 \
apache/skywalking-oap-server:8.2.0-es7

docker run --name skywalking-ui -d \
-e TZ=Asia/Shanghai \
-p 8180:8080 \
-e SW_OAP_ADDRESS=192.168.31.88:12800 \
apache/skywalking-ui:8.2.0
```



## 编译后版本使用（mac 下无法正常运行，不知道为什么）

- 解压目录的结构

```
webapp: UI 前端（web 监控页面）的 jar 包和配置文件；
oap-libs: 后台应用的 jar 包，以及它的依赖 jar 包，里边有一个 server-starter-*.jar 就是启动程序；
config: 启动后台应用程序的配置文件，是使用的各种配置
bin: 各种启动脚本，一般使用脚本 startup.* 来启动 web 页面 和对应的 后台应用；
    oapService.*: 默认使用的后台程序的启动脚本；（使用的是默认模式启动，还支持其他模式，各模式区别见 启动模式）
    oapServiceInit.*: 使用 init 模式启动；在此模式下，OAP服务器启动以执行初始化工作，然后退出
    oapServiceNoInit.*: 使用 no init模式启动；在此模式下，OAP服务器不进行初始化。
    webappService.*: UI 前端的启动脚本；
    startup.*: 组合脚本，同时启动 oapService.*:、webappService.* 脚本；
agent:
    skywalking-agent.jar: 代理服务 jar 包
    config: 代理服务启动时使用的配置文件
    plugins: 包含多个插件，代理服务启动时会加载改目录下的所有插件（实际是各种 jar 包）
    optional-plugins: 可选插件，当需要支持某种功能时，比如 SpringCloud Gateway，则需要把对应的 jar 包拷贝到 plugins 目录下；

```

- 如果报 java.lang.OutOfMemoryError: GC overhead limit exceeded，可以调大 JVM

```
修改 bin 目录下的所有 shell 脚本
JAVA_OPTS=" -Xms556M -Xmx1512M"
```

- 修改webapp/webapp.yml端口(UI配置)

```
# web 应用的启动端口，默认是 8080，我这里改为 8180
server:
  port: 8180

collector:
  path: /graphql
  ribbon:
    ReadTimeout: 10000
    # SkyWalking 服务的 restful 端口，默认是 12800。如果有多个用英文逗号隔开
    listOfServers: 127.0.0.1:12800
```

- 修改conf/application.yml中 104 行的 storage

```
storage:
  # 默认是 H2，我们这里改为 elasticsearch7
  selector: ${SW_STORAGE:elasticsearch7}
  elasticsearch7:
    # 索引名
    nameSpace: ${SW_NAMESPACE:"skywalking-log"}
    # es 集群地址
    clusterNodes: ${SW_STORAGE_ES_CLUSTER_NODES:127.0.0.1:9200}
    protocol: ${SW_STORAGE_ES_HTTP_PROTOCOL:"http"}
    trustStorePath: ${SW_STORAGE_ES_SSL_JKS_PATH:""}
    trustStorePass: ${SW_STORAGE_ES_SSL_JKS_PASS:""}
    dayStep: ${SW_STORAGE_DAY_STEP:1} # Represent the number of days in the one minute/hour/day index.
    indexShardsNumber: ${SW_STORAGE_ES_INDEX_SHARDS_NUMBER:1} # Shard number of new indexes
    indexReplicasNumber: ${SW_STORAGE_ES_INDEX_REPLICAS_NUMBER:1} # Replicas number of new indexes
    # Super data set has been defined in the codes, such as trace segments.The following 3 config would be improve es performance when storage super size data in es.
    superDatasetDayStep: ${SW_SUPERDATASET_STORAGE_DAY_STEP:-1} # Represent the number of days in the super size dataset record index, the default value is the same as dayStep when the value is less than 0
    superDatasetIndexShardsFactor: ${SW_STORAGE_ES_SUPER_DATASET_INDEX_SHARDS_FACTOR:5} #  This factor provides more shards for the super data set, shards number = indexShardsNumber * superDatasetIndexShardsFactor. Also, this factor effects Zipkin and Jaeger traces.
    superDatasetIndexReplicasNumber: ${SW_STORAGE_ES_SUPER_DATASET_INDEX_REPLICAS_NUMBER:0} # Represent the replicas number in the super size dataset record index, the default value is 0.
    user: ${SW_ES_USER:""}
    password: ${SW_ES_PASSWORD:""}
    secretsManagementFile: ${SW_ES_SECRETS_MANAGEMENT_FILE:""} # Secrets management file in the properties format includes the username, password, which are managed by 3rd party tool.
    bulkActions: ${SW_STORAGE_ES_BULK_ACTIONS:1000} # Execute the async bulk record data every ${SW_STORAGE_ES_BULK_ACTIONS} requests
    syncBulkActions: ${SW_STORAGE_ES_SYNC_BULK_ACTIONS:50000} # Execute the sync bulk metrics data every ${SW_STORAGE_ES_SYNC_BULK_ACTIONS} requests
    flushInterval: ${SW_STORAGE_ES_FLUSH_INTERVAL:10} # flush the bulk every 10 seconds whatever the number of requests
    concurrentRequests: ${SW_STORAGE_ES_CONCURRENT_REQUESTS:2} # the number of concurrent requests
    resultWindowMaxSize: ${SW_STORAGE_ES_QUERY_MAX_WINDOW_SIZE:10000}
    metadataQueryMaxSize: ${SW_STORAGE_ES_QUERY_MAX_SIZE:5000}
    segmentQueryMaxSize: ${SW_STORAGE_ES_QUERY_SEGMENT_SIZE:200}
    profileTaskQueryMaxSize: ${SW_STORAGE_ES_QUERY_PROFILE_TASK_SIZE:200}
    advanced: ${SW_STORAGE_ES_ADVANCED:""}
```

- 如果你要使用 MySQL 进行存储的话

```
创建 skywalking 数据库
因为 oap-libs 目录下缺少 mysql 的驱动程序，所以还需要下载 mysql-connector-java-*.jar 放到 oap-libs 目录下，这里我使用的版本是 5.1.46。
一般该 jar 包在本地的 maven 仓库都有，直接拷贝过去即可，一般在目录 ~/.m2/repository/mysql/mysql-connector-java/5.1.46 下。
```

- 启动 `sh /Volumes/mydata/software/apache-skywalking-apm-bin-es7/bin/startup.sh`
- 会打印这样两句话：
```
SkyWalking OAP started successfully!
SkyWalking Web Application started successfully!
```

- 查看 oap server 日志：`tail -333f /Volumes/mydata/software/apache-skywalking-apm-bin-es7/logs/webapp.log`
- 查看 webapp 日志：`tail -333f /Volumes/mydata/software/apache-skywalking-apm-bin-es7/logs/webapp.log`
- 浏览器访问 http://127.0.0.1:8180
 - 分别配置启动参数（vm arguments）如下（有多少个服务需要跟踪，就配置多少个）
 
```
## 11800 是 skywalking 默认的 grpc 端口
-javaagent:/Volumes/mydata/software/apache-skywalking-apm-bin-es7/agent/skywalking-agent.jar 
-Dskywalking.agent.service_name=sculptor-boot-backend 
-Dskywalking.collector.backend_service=127.0.0.1:11800
```

- 默认不兼容 Spring Cloud Gateway 的链路，需要额外处理

```
skywalking-agent.jar 在启动时会加载 plugins 下的所有插件，但不会加载 optional-plugins 下的，其实看目录名就知道了，可选插件 就是可有可没有，需要等需要的时候再加到 plugins 下即可
我们看到， optional-plugins 下就有跟 SpringCloud Gateway 相关的插件，那就它了，把它丢到 plugins 目录下
我们还注意到另一个插件 apm-spring-webflux-5.x-plugin-6.6.0.jar，把它也丢到 plugins 目录下
```

- 自定义忽略追踪部分请求

```
注意到，optional-plugins 中有这样的插件 apm-trace-ignore-plugin-6.6.0.jar，把它丢到 plugins 目录下先。
加上插件只是让 Skywalking 拥有忽略某些请求的能力，但还需要我们指定哪些需要忽略。下载 配置文件，然后把它丢到 /agent/config/ 目录下，增加过滤规则。里边的内容如下：
如果你用 eureka、consul 的话，已经配置了规则 
https://github.com/apache/skywalking/blob/master/apm-sniffer/optional-plugins/trace-ignore-plugin/apm-trace-ignore-plugin.config
```

-------------------------------------------------------------------

## 支持收集的组件列表

- 国内常用的组件目前看来都支持了
- <https://github.com/apache/skywalking/blob/master/docs/en/setup/service-agent/java-agent/Supported-list.md>


## Java Agent（探针）


#### IntelliJ IDEA 项目调试

- 前面构建服务的时候记得构建出 jar 包出来，这里要用到
- 自己的 Spring Boot 项目
- 引包：

```
<!--SkyWalking start-->
<!-- https://mvnrepository.com/artifact/org.apache.skywalking/apm-toolkit-trace -->
<dependency>
    <groupId>org.apache.skywalking</groupId>
    <artifactId>apm-toolkit-trace</artifactId>
    <version>6.1.0</version>
</dependency>
<!--SkyWalking end-->
```

- 常用注解：


```
@Trace
@ApiOperation(tags = {"用户系统管理->用户管理->用户列表"}, value = "查询所有用户列表", notes = "查询所有用户列表")
@RequestMapping(value = "/list", method = RequestMethod.GET)
@ResponseBody
public List<SysUser> list() {
    List<SysUser> sysUserList = sysUserService.findAll();
    ActiveSpan.tag("一共有数据：", sysUserList.size() + "条");
    log.info("当前 traceId={}", TraceContext.traceId());
    return sysUserList;
}

```

- 更多注解的使用：<https://github.com/apache/skywalking/blob/master/docs/en/setup/service-agent/java-agent/Application-toolkit-trace.md>

- 你的 demo 项目在 IntelliJ IDEA 启动的时候加上 VM 参数上设置：

```
-javaagent:/你自己的路径/skywalking-agent.jar -Dskywalking.agent.application_code=my_app_001 -Dskywalking.collector.backend_service=localhost:11800
```

- 默认 11800 是 gRPC 的接收接口
- 你自己构建出来的 jar 路径一般是：`/skywalking/apm-sniffer/apm-agent/target/skywalking-agent.jar`
- 然后请求你带有 Trace 的 Controller，然后去 UI 界面看统计情况

#### jar 包方式

- 你的 Spring Boot jar 包 run 之前加上 VM 参数：

```
java -javaagent:/你自己的路径/skywalking-agent.jar -Dskywalking.collector.backend_service=localhost:11800 -Dskywalking.agent.application_code=my_app_002 -jar my-project-1.0-SNAPSHOT.jar
```


#### Docker 方式

- Dockerfile

```
FROM openjdk:8-jre-alpine

LABEL maintainer="tanjian20150101@gmail.com"

ENV SW_AGENT_NAMESPACE=java-agent-demo \
	SW_AGENT_COLLECTOR_BACKEND_SERVICES=localhost:11800

COPY skywalking-agent /apache-skywalking-apm-bin/agent

COPY target/sky-demo-1.0-SNAPSHOT.jar /demo.jar

ENTRYPOINT java -javaagent:/apache-skywalking-apm-bin/agent/skywalking-agent.jar -jar /demo.jar
```

- 构建镜像：

```
docker build -t hello-demo .
docker run -p 10101:10101 -e SW_AGENT_NAMESPACE=hello-world-demo-005 -e SW_AGENT_COLLECTOR_BACKEND_SERVICES=127.10.0.2:11800 hello-demo
```



## 构建 jar 部署在服务器

- 如果想直接打包出 jar 部署与服务器，只需要这样：<https://github.com/apache/skywalking/blob/master/docs/en/guides/How-to-build.md#build-from-github>

```
cd skywalking/

git submodule init

git submodule update

mvn clean package -DskipTests
```

## 告警配置

- <https://skywalking.apache.org/zh/blog/2019-01-03-monitor-microservice.html>


- /config/agent.config

```

# 当前的应用编码，最终会显示在webui上。
# 建议一个应用的多个实例，使用有相同的application_code。请使用英文
agent.application_code=Your_ApplicationName

# 每三秒采样的Trace数量
# 默认为负数，代表在保证不超过内存Buffer区的前提下，采集所有的Trace
# agent.sample_n_per_3_secs=-1

# 设置需要忽略的请求地址
# 默认配置如下
# agent.ignore_suffix=.jpg,.jpeg,.js,.css,.png,.bmp,.gif,.ico,.mp3,.mp4,.html,.svg

# 探针调试开关，如果设置为true，探针会将所有操作字节码的类输出到/debugging目录下
# skywalking团队可能在调试，需要此文件
# agent.is_open_debugging_class = true

# 对应Collector的config/application.yml配置文件中 agent_server/jetty/port 配置内容
# 例如：
# 单节点配置：SERVERS="127.0.0.1:8080" 
# 集群配置：SERVERS="10.2.45.126:8080,10.2.45.127:7600" 
collector.servers=127.0.0.1:10800

# 日志文件名称前缀
logging.file_name=skywalking-agent.log

# 日志文件最大大小
# 如果超过此大小，则会生成新文件。
# 默认为300M
logging.max_file_size=314572800

# 日志级别，默认为DEBUG。
logging.level=DEBUG
```


## 资料

- <https://skywalking.apache.org/zh/blog/2018-12-21-SkyWalking-source-code-read.html>
- <https://github.com/JaredTan95/skywalking-tutorials>
- <https://www.bilibili.com/video/av40796154?from=search&seid=8779011383117018227>
- <https://skywalking.apache.org/zh/blog/2019-01-03-monitor-microservice.html>
- <https://www.jianshu.com/p/f3fffc2c0cd4>
- <>
- <>
- <>






