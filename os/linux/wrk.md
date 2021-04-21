# wrk 安装和配置


## wrk 介绍

- wrk 官网：<https://github.com/wg/wrk>

## 安装

- 官网说明：https://github.com/wg/wrk/wiki/Installing-Wrk-on-Linux
- CentOS 7

```
yum install https://extras.getpagespeed.com/release-el7-latest.rpm
yum install wrk
```

## 简单使用

```
查看版本
wrk -v

发起最简单请求
wrk -t5 -c5 -d30s http://www.baidu.com

Running 30s test @ http://www.baidu.com
5 threads and 5 connections

Thread Stats   Avg      Stdev     Max   +/- Stdev
Latency    44.59ms   17.41ms 331.91ms   95.66%
Req/Sec    23.11      5.77    30.00     57.04%

3439 requests in 30.03s, 50.47MB read
Socket errors: connect 0, read 10, write 0, timeout 0
Requests/sec:    114.52
Transfer/sec:      1.68MB

默认是开启了长连接，如果要关闭可以设置请求头：Connection: Close
每个时间点的并发数大致等于连接数（connection），每个线程分配到连接数 = 连接数 除 线程数
其中，线程数，并不是设置的越大，推荐设置当前机器 CPU 虚拟核心数的数值或 2 倍之间
```

## 脚本使用

- 创建：vim /opt/post-wrk.lua

```
wrk.method = "POST"  
wrk.body   = "hms_user_id=222222&routing_key=ad.sys_user.add"  
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"
```

```

wrk -t10 -c100 -d15s --script=/opt/post-wrk.lua --latency http://127.0.0.1:9090/websocket/api/send-by-user-id
```