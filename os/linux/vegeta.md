# Vegeta 安装和配置

## 环境

- CentOS 7 64位
- macOS 10.15.7
- macOS、CentOS 系统记得放开限制：

```
ulimit -n 10024
ulimit -u 5568
```

## Vegeta 基本介绍

- Vegeta 官网：<https://github.com/tsenart/vegeta>

## 安装

- 官网下载：<https://github.com/tsenart/vegeta/releases>
- Golang 开发，支持全平台，只是部分版本里面可能会没有 Windows 编译的版本而已
- macOS 支持 brew：`brew install vegeta`
- 其他平台解压后配置好环境变量直接使用


## GET 测试


```
echo "GET http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest"| vegeta -cpus=6 attack -rate=10000 -duration=30s | tee results.bin | vegeta report

cpus 使用 cpu 数量
rate 每秒钟请求次数
connections 每个地址最大连接数
duration 持续时间
tee results.bin 保存测试报告并用 veteta report 显示报告内容，


压测结果：
Requests      [total, rate, throughput]         300000, 10000.04, 3473.08
Duration      [total, attack, wait]             59.997s, 30s, 29.997s
Latencies     [min, mean, 50, 90, 95, 99, max]  9.074µs, 1.053s, 5.922ms, 22.79ms, 1.674s, 30s, 30.005s
Bytes In      [total, mean]                     20212181, 67.37
Bytes Out     [total, mean]                     0, 0.00
Success       [ratio]                           69.46%
Status Codes  [code:count]                      0:91627  200:208373
Error Set:
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": read tcp 127.0.0.1:51773->127.0.0.1:9091: read: connection reset by peer
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": dial tcp 0.0.0.0:0->127.0.0.1:9091: connect: connection reset by peer
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": read tcp 127.0.0.1:51785->127.0.0.1:9091: read: connection reset by peer
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": write tcp 127.0.0.1:51781->127.0.0.1:9091: write: broken pipe
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": readLoopPeekFailLocked: read tcp 127.0.0.1:51811->127.0.0.1:9091: read: connection reset by peer
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": read tcp 127.0.0.1:51782->127.0.0.1:9091: read: connection reset by peer
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": read tcp 127.0.0.1:51847->127.0.0.1:9091: read: connection reset by peer
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": write tcp 127.0.0.1:51810->127.0.0.1:9091: write: broken pipe
Get "http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest": dial tcp 0.0.0.0:0->127.0.0.1:9091: socket: too many open files

Duration：持续时间（攻击是加+等待时间），attack 攻击时间，wait 等待时间
Latencies：延迟
mean：单个请求的平均值
Bytes In 请求的大小（字节）
Bytes Out：字节输出
Status Codes：返回状态码与请求数，0 的状态码表示客户端临时结束
Success：请求成功率
Error Set 错误集

-------------------------------------------------------------------

这是 wrk 测试结果，可以用来做参考对比：（目前测试 wrk 会更强一些，但是不跨平台）
Running 30s test @ http://127.0.0.1:9091/sculptor-boot-backend/api/open/sysCommon/prometheusTest
  6 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     9.88ms    6.55ms 138.47ms   83.95%
    Req/Sec     1.73k   168.62     2.22k    69.44%
  Latency Distribution
     50%    7.76ms
     75%   12.31ms
     90%   17.75ms
     99%   33.98ms
  309718 requests in 30.01s, 210.96MB read
Requests/sec:  10320.17
Transfer/sec:      7.03MB



```


## POST 测试（兼容其他所有请求类型）

```
post 测试，需要创建一个文本：vim postTestFile.txt，内容如下：

# 这是注释格式
POST http://goku:9090/things
# 这是请求头
X-Account-ID: 99
@/opt/requestBodyJson.json


vegeta attack -targets=postTestFile.txt -rate=60 -duration=10s > results.bin

```

## 查看报表

```
查看方式有：
vegeta report results.bin
vegeta report -type='hist[0,100ms,200ms,300ms,500ms,1000ms,3000ms]' results.bin
vegeta report -type=json results.bin
vegeta report -type=json results.bin > /opt/jsonOutput.json
vegeta report -type=hdrplot results.bin

生成报表图：
vegeta plot --title ThisIsTitle results.bin > plot.html

别人做的统计表，可以参考：
https://img-blog.csdnimg.cn/20190813003520979.png
```




## 分布式测试

```
这篇文章不错：<https://blog.csdn.net/minxihou/article/details/99353832>

如果状态为“0”的请求分布比较多的时候，代表着这些请求没有在压力机发出整个测试就结束了。这里需要考虑有两点：
是否是被测端过饱和了导致更多的请求无法被接收到。
是否压力机太少了导致压力机产生了额定的请求速率但是没有发送出去。
这里不需要考虑测试的执行时间问题。因为压测端的请求速率是恒定的，如果说有status codes等于“0”的情况，你随着增加测试时间status codes等于“0”的个数只会越来越多。
博主使用的4核8GB内存的虚拟机来进行的压测。在这种规格的虚机下使用vegeta去压测一个静态页面时，rate指定超过3W会使虚机本身成为压力瓶颈。


值得提一下的就是如果是分布式压测最后统计结果生成报告的话，应该是将每台压力机的houminxi.bin拷贝到同一台机器的相同路径下。
使用vegeta report houminxi.bin houminxi-1.bin | less（记得拷贝过来将结果文件houminxi.bin重命名，以免覆盖其他机器拷贝过来结果文件。
vegeta report 后面每个文件以空格的形式分开，使用less命令是万一压测请求出错。这样不至于你合成结果就是一堆错误糊脸。
单台压力机中使用tee命令保存的二进制结果文件和你生成报告的文件不要重名，要不就被覆盖了。或者当你想使用分布式压测的时候不使用vegeta report命令，为了防止文件冲突。
```
