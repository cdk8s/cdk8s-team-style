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
wrk -t4 -c20 -d10s --latency --timeout 10s http://www.qq.com

结果：
Running 10s test @ http://www.qq.com
  4 threads and 20 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     6.65ms    1.06ms  26.30ms   78.25%
    Req/Sec   755.01     51.42     0.86k    75.50%
  Latency Distribution
     50%    6.48ms
     75%    7.10ms
     90%    7.86ms
     99%    9.32ms
  30092 requests in 10.01s, 9.96MB read
Requests/sec:   3005.16
Transfer/sec:      0.99MB

默认是开启了长连接，如果要关闭可以设置请求头：Connection: Close
每个时间点的并发数大致等于连接数（connection），测试的时候一般是不断调整该参数。每个线程分配到连接数 = 连接数 除 线程数
其中，线程数，并不是设置的越大，推荐设置当前机器 CPU 虚拟核心数的数值或 2 倍之间
```

## 脚本使用

- 创建：vim /opt/post-wrk.lua

```
form 表单请求类型
wrk.method = "POST"  
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"
wrk.headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/90.0.4430.72"
wrk.body = "hms_user_id=222222&routing_key=ad.sys_user.add"  
```

```
json 请求类型
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json;charset=UTF-8"
wrk.headers["userId"] = "123"
wrk.headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/90.0.4430.72"
wrk.body = '{"userId": "10001","coinType": "GT","type": "2","amount": "5.1"}'
```

```
wrk -t4 -c20 -d10s --latency --timeout 10s --script=/opt/post-wrk.lua https://www.baidu.com
```