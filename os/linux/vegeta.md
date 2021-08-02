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
echo "GET http://127.0.0.1:233"| vegeta attack -rate=500 -duration=10s | tee results.bin | vegeta report


rate 每秒钟请求次数
connections 每个地址最大连接数
duration 持续时间
tee results.bin 保存测试报告并用 veteta report 显示报告内容，
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
```


## 分布式测试

```
这篇文章不错：<https://blog.csdn.net/minxihou/article/details/99353832>

值得提一下的就是如果是分布式压测最后统计结果生成报告的话，应该是将每台压力机的houminxi.bin拷贝到同一台机器的相同路径下。
使用vegeta report houminxi.bin houminxi-1.bin | less（记得拷贝过来将结果文件houminxi.bin重命名，以免覆盖其他机器拷贝过来结果文件。
vegeta report 后面每个文件以空格的形式分开，使用less命令是万一压测请求出错。这样不至于你合成结果就是一堆错误糊脸。
单台压力机中使用tee命令保存的二进制结果文件和你生成报告的文件不要重名，要不就被覆盖了。或者当你想使用分布式压测的时候不使用vegeta report命令，为了防止文件冲突。
```
