# Prometheus 安装和使用

## 环境

- CentOS 7 64位
- 禁用防火墙、selinux、swap

## Prometheus 基本介绍

- 不错的发展史说明：<https://caicloud.io/blog/5a5db4203255f5063f2bd462>
- 特别说明：一般这类环境要尽可能保证所有服务器时间一致
- Prometheus 本地存储不适合存长久数据，一般存储一个月就够了。要永久存储需要配置远端存储，远端存储可以用 OpenTSDB
- Prometheus 也不适合做日志存储，日志存储还是推荐 ELK 方案

## Prometheus 安装（Docker）

- 官网：<https://prometheus.io/>
- Docker 官方镜像：<https://hub.docker.com/r/prom/prometheus/>
- 这里以 Spring Boot Metrics 为收集信息
- 创建配置文件：`vim /data/docker/prometheus/config/prometheus.yml`
- 在 scrape_configs 位置下增加我们自己应用的路径信息

```
# my global config
global:
  scrape_interval:     15s # 拉取监控服务信息周期
  evaluation_interval: 15s # 读取配置规则周期时间
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  - job_name: 'springboot'
    metrics_path: '/tkey-actuator/actuator/prometheus'
    static_configs:
    - targets: ['192.168.2.225:19091']
    # 如果是暴露在外网的 nginx，可以通过配置 nginx 的 basic_auth 来支持认证
    basic_auth:
      username: admin
      password: 123456
```

- 启动

```
docker run -d --name prometheus -p 9090:9090 \
-v /data/docker/prometheus/config/prometheus.yml:/etc/prometheus/prometheus.yml \
prom/prometheus
```

----------------------------------------------------------------------------------------------

## 配置

- Prometheus 默认数据是存储到本地磁盘，存储周期 15d。如果需要长期存储需要设置远程存储
- 官网 exporter 列表：<https://prometheus.io/docs/instrumenting/exporters/>
- 官网 exporter 暴露的端口列表：<https://github.com/prometheus/prometheus/wiki/Default-port-allocations>


### CentOS7 服务器

- 当前最新版本：node_exporter 0.18.1（201907）

```
mkdir -p /usr/local/prometheus/node_exporter

cd /usr/local/prometheus/node_exporter

wget https://github.com/prometheus/node_exporter/releases/download/v0.18.1/node_exporter-0.18.1.linux-amd64.tar.gz

tar -zxvf node_exporter-0.18.1.linux-amd64.tar.gz

```


```
创建Systemd服务
vim /etc/systemd/system/node_exporter.service



[Unit]
Description=node_exporter
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/prometheus/node_exporter/node_exporter-0.18.1.linux-amd64/node_exporter
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

- 关于 ExecStart 参数，可以再附带一些启动监控的参数，官网介绍：<https://github.com/prometheus/node_exporter/blob/master/README.md#enabled-by-default>
    - 格式：`ExecStart=/usr/local/prometheus/node_exporter/node_exporter-0.18.1.linux-amd64/node_exporter --collectors.enabled meminfo,hwmon,entropy`


```
启动 Node exporter
systemctl start node_exporter

systemctl daemon-reload

systemctl status node_exporter

```


```
修改prometheus.yml，加入下面的监控目标：

vim  /data/docker/prometheus/config/prometheus.yml

scrape_configs:
  - job_name: 'centos7'
    static_configs:
    - targets: ['192.168.1.3:9100']
      labels:
        instance: centos7_node1

```

- 重启 prometheus：`docker restart prometheus`
- Grafana 有现成的 dashboard：
    - <https://grafana.com/dashboards/405>
    - <https://grafana.com/dashboards/8919>

----------------------------------------------------------------------------------------------


### Nginx 指标

- 这里使用 Nginx VTS exporter：<https://github.com/hnlq715/nginx-vts-exporter>

- 安装 nginx 模块：

```
git clone --depth=1 https://github.com/vozlt/nginx-module-vts.git


编译 nginx 的时候加上：
./configure --prefix=/usr/local/nginx --with-http_ssl_module --add-module=/opt/nginx-module-vts

make（已经安装过了，就不要再 make install）
```


```
也有人做好了 docker 镜像：
https://hub.docker.com/r/xcgd/nginx-vts

docker run --name nginx-vts -p 80:80 -v /data/docker/nginx/conf/nginx.conf:/etc/nginx/nginx.conf:ro -d xcgd/nginx-vts
```


```
修改Nginx配置


http {
    vhost_traffic_status_zone;
    vhost_traffic_status_filter_by_host on;

    ...

    server {

        ...

        location /status {
            vhost_traffic_status_display;
            vhost_traffic_status_display_format html;
        }
    }
}


验证nginx-module-vts模块：http://192.168.1.3/status，会展示：
Nginx Vhost Traffic Status 统计表

```

```
如果不想统计流量的server，可以禁用vhost_traffic_status，配置示例：
server {
    ...
    vhost_traffic_status off;
    ...
}
```


- 安装 nginx-vts-exporter

```
官网版本：https://github.com/hnlq715/nginx-vts-exporter/releases

wget https://github.com/hnlq715/nginx-vts-exporter/releases/download/v0.10.3/nginx-vts-exporter-0.10.3.linux-amd64.tar.gz

tar zxvf nginx-vts-exporter-0.10.3.linux-amd64.tar.gz

chmod +x /usr/local/nginx-vts-exporter-0.10.3.linux-amd64/nginx-vts-exporter
```

```
创建Systemd服务
vim /etc/systemd/system/nginx_vts_exporter.service


[Unit]
Description=nginx_exporter
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/nginx-vts-exporter-0.10.3.linux-amd64/nginx-vts-exporter -nginx.scrape_uri=http://192.168.1.3/status/format/json
Restart=on-failure

[Install]
WantedBy=multi-user.target
```


```
启动nginx-vts-exporter
systemctl start nginx_vts_exporter.service
systemctl daemon-reload
systemctl status nginx_vts_exporter.service
```


```
修改 prometheus.yml，加入下面的监控目标：
vim  /data/docker/prometheus/config/prometheus.yml

scrape_configs:
  - job_name: 'nginx'
    static_configs:
    - targets: ['192.168.1.3:9913']
      labels:
        instance: nginx1


如果nginx 有加 basic auth，则需要这样：
scrape_configs:
  - job_name: "nginx"
    metrics_path: /status/format/prometheus
    basic_auth:
      username: youmeek
      password: '123456'
    static_configs:
    - targets: ['192.168.1.3:9913']
      labels:
        instance: 'nginx1'

```

- 重启 prometheus：`docker restart prometheus`
- Grafana 有现成的 dashboard：
    - <https://grafana.com/dashboards/2949>
    - <https://grafana.com/dashboards/2984>

#### Spring Boot 监控

#### Redis 监控

https://grafana.com/grafana/dashboards/11835
https://grafana.com/grafana/dashboards/11692

#### MySQL 监控

https://grafana.com/grafana/dashboards/7362

#### Nginx 监控

https://grafana.com/grafana/dashboards/7362



----------------------------------------------------------------------------------------------



### 微服务下的多服务收集

- <https://blog.csdn.net/zhuyu19911016520/article/details/88411371>



----------------------------------------------------------------------------------------------


### 告警

- <https://blog.csdn.net/zhuyu19911016520/article/details/88627004>
- <https://www.jianshu.com/p/e59cfd15612e>

- 告警配置

- 告警检测

- [Grafana+Prometheus系统监控之邮件报警功能](https://blog.52itstyle.vip/archives/2014/)
- [Grafana+Prometheus系统监控之钉钉报警功能](https://blog.52itstyle.vip/archives/2029/)
- [Grafana+Prometheus系统监控之webhook](https://blog.52itstyle.vip/archives/2068/)


## 远端存储方案

- <https://segmentfault.com/a/1190000015576540>


## PromQL

- 资料：<https://songjiayang.gitbooks.io/prometheus/content/promql/summary.html>
- 官网函数列表：<https://prometheus.io/docs/prometheus/latest/querying/functions/>
- 类 SQL 对比，方便理解：

```
查询当前所有数据
// PromQL
http_requests_total

// MySQL
SELECT * from http_requests_total WHERE created_at BETWEEN 1495435700 AND 1495435710;

-------------------------------------------------------------------

条件查询
// PromQL
http_requests_total{code="200", handler="query"}

// MySQL
SELECT * from http_requests_total WHERE code="200" AND handler="query" AND created_at BETWEEN 1495435700 AND 1495435710;

-------------------------------------------------------------------

模糊查询: code 为 2xx 的数据
// PromQL
http_requests_total{code~="2xx"}

// MySQL
SELECT * from http_requests_total WHERE code LIKE "%2%" AND created_at BETWEEN 1495435700 AND 1495435710;

-------------------------------------------------------------------

比较查询: value 大于 100 的数据
// PromQL
http_requests_total > 100

// MySQL
SELECT * from http_requests_total WHERE value > 100 AND created_at BETWEEN 1495435700 AND 1495435710;

-------------------------------------------------------------------

范围区间查询: 过去 5 分钟数据
// PromQL
http_requests_total[5m]

// MySQL
SELECT * from http_requests_total WHERE created_at BETWEEN 1495435410 AND 1495435710;

-------------------------------------------------------------------

count 查询: 统计当前记录总数
// PromQL
count(http_requests_total)

// MySQL
SELECT COUNT(*) from http_requests_total WHERE created_at BETWEEN 1495435700 AND 1495435710;

-------------------------------------------------------------------

sum 查询: 统计当前数据总值
// PromQL
sum(http_requests_total)

// MySQL
SELECT SUM(value) from http_requests_total WHERE created_at BETWEEN 1495435700 AND 1495435710;

-------------------------------------------------------------------

avg 查询: 统计当前数据平均值
// PromQL
avg(http_requests_total)

// MySQL
SELECT AVG(value) from http_requests_total WHERE created_at BETWEEN 1495435700 AND 1495435710;

-------------------------------------------------------------------

top 查询: 查询最靠前的 3 个值
// PromQL
topk(3, http_requests_total)

// MySQL
SELECT * from http_requests_total WHERE created_at BETWEEN 1495435700 AND 1495435710 ORDER BY value DESC LIMIT 3;


-------------------------------------------------------------------

rate / irate 查询，过去 5 分钟平均每秒数值
// PromQL
rate(http_requests_total[5m])
irate(http_requests_total[5m])

// MySQL
SELECT code, handler, instance, job, method, SUM(value)/300 AS value from http_requests_total WHERE created_at BETWEEN 1495435700 AND 1495435710  GROUP BY code, handler, instance, job, method;

```

- 查询条件支持正则匹配，例如：

```
http_requests_total{code!="200"}  // 表示查询 code 不为 "200" 的数据
http_requests_total{code=～"2.."} // 表示查询 code 为 "2xx" 的数据
http_requests_total{code!～"2.."} // 表示查询 code 不为 "2xx" 的数据
```

- 逻辑运算符:

```
支持的逻辑运算符有 and，or，unless, 例如 http_requests_total == 5 or http_requests_total == 2 表示 http_requests_total 结果中等于 5 或者 2 的数据。
```

- 聚合运算符:

```
支持的聚合运算符有 sum，min，max，avg，stddev，stdvar，count，count_values，bottomk，topk，quantile，, 例如 max(http_requests_total) 表示 http_requests_total 结果中最大的数据。
注意，和四则运算类型，Prometheus 的运算符也有优先级，它们遵从（^）> (*, /, %) > (+, -) > (==, !=, <=, <, >=, >) > (and, unless) > (or) 的原则。
```

- 查看 http_requests_total 5分钟内，平均每秒数据

```
rate(http_requests_total[5m])
irate(http_requests_total[5m])

irate和rate都会用于计算某个指标在一定时间间隔内的变化速率。但是它们的计算方法有所不同：irate取的是在指定时间范围内的最近两个数据点来算速率，而rate会取指定时间范围内所有数据点，算出一组速率，然后取平均值作为结果。
所以官网文档说：irate适合快速变化的计数器（counter），而rate适合缓慢变化的计数器（counter）。
```



----------------------------------------------------------------------------------------------

## Nginx 反向代理

```
// 直接配置 server 域名的情况下
location / {
    auth_basic   "please input you user name and password";
    auth_basic_user_file    /opt/nginx-auth/passwd.db;

    proxy_pass http://127.0.0.1:9090;
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}


// 配置路径域名的情况下：
需要在 Prometheus 的启动参数加上：--web.external-url = myPrometheus
location /myPrometheus/ {
    rewrite ^/myPrometheus(.*)$ $1 break;

    auth_basic   "please input you user name and password";
    auth_basic_user_file    /opt/nginx-auth/passwd.db;

    proxy_pass http://127.0.0.1:9090;
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

```


----------------------------------------------------------------------------------------------

## API 接口

- 官网文档：<https://prometheus.io/docs/prometheus/latest/querying/api/>

```
GET /api/v1/query
POST /api/v1/query
URL query parameters:
    query=<string>: Prometheus expression query string.
    time=<rfc3339 | unix_timestamp>: Evaluation timestamp. Optional.
    timeout=<duration>: Evaluation timeout. Optional. Defaults to and is capped by the value of the -query.timeout flag.


GET /api/v1/query_range
POST /api/v1/query_range
    URL query parameters:
    query=<string>: Prometheus expression query string.
    start=<rfc3339 | unix_timestamp>: Start timestamp, inclusive.
    end=<rfc3339 | unix_timestamp>: End timestamp, inclusive.
    step=<duration | float>: Query resolution step width in duration format or float number of seconds.
    timeout=<duration>: Evaluation timeout. Optional. Defaults to and is capped by the value of the -query.timeout flag.


推荐使用 POST，请求头加：Content-Type: application/x-www-form-urlencoded
可以避免 GET 过大查询参数字符限制
```



----------------------------------------------------------------------------------------------


## 其他资料

- <https://www.aneasystone.com/archives/2018/11/prometheus-in-action.html>
    - 写得非常非常非常好
- <https://www.hi-linux.com/posts/27014.html>
- <https://www.linuxea.com/1915.html>
- <https://blog.csdn.net/palet/article/details/82763695>

