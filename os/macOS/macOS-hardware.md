

## 如何识别硬件有效信息

- 机子背面刻有序列号
- 与系统中：关于本机 》 序列号，两个序列号是一致的
- 访问官网查询序列号情况：<https://checkcoverage.apple.com/>

## 常见硬件指标


- 查看硬盘读写数据量、通电时长

```
使用软件：Drive Scope 或者 SMART Utility（备用）
软件中有详细数据
```

- 如果是笔记本还可以查看电池循环次数

```
关于本机 > 更多信息... > 系统报告...
在：效能信息 > 循环计数 中可以看到次数
```

- 硬盘读写速度

```
使用软件：Disk Speed Test，
M1 Pro 的 macbook pro 500GB 数据是：写3000，读4400
M2 MAX 的 Mac studio 1TB 数据是：写6000，读5000
```


- 查看 CPU、GPU 分数

```
使用软件：Geekbench Pro

M1 Pro 的 macbook pro 500GB 数据是：
cpu单核 1862，多核 8989
gpu 的 opencl 模式下，分数 36775


M2 MAX 的 Mac studio 1TB 数据是：
cpu单核 2715，多核 14914
gpu 的 opencl 模式下，分数 76404
```



