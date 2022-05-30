
# 【从开公司到开发全平台产品】2.黑、白苹果软硬件及系统安装-UPUPMO


- 本文视频版已发到 Bilibili：<https://www.bilibili.com/video/BV1qt4y1p7rF/>
- 大家好，我是 UPUPMO.com 的作者 Meek，欢迎观看 《从开公司到开发全平台产品》系列。
- 希望通过该系列可以帮助新手快速了解全栈软件产品的一些思路、应用。
- 如果你心中有创意，也想独立开发产品，可以在视频或文章的最后，查看联系信息加我好友。
- 本期我们讲解第二章：《黑、白苹果软硬件及系统安装》
- 我们将会从以下5个小节进行探讨：

```
1. 白苹果硬件推荐
2. 黑苹果硬件推荐
3. 黑苹果详细安装流程（macOS Monterey）
4. macOS 新手入门指南
5. macOS 软件大全推荐
```

-------------------------------------------------------------------


## 1. 白苹果硬件推荐

![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/m1-cpu.png)


- M1 CPU 首发在 2020-11，距离今天 2022-05 已经过去快 2 年。目前现状是只有少数工业化级软件不支持 M1，或者说支持的不完善。但是对于大多数用户、开发者来讲，基本可以说没啥影响了，可以大胆买。（Macbook Air 登场视频）
- 我主推2个产品

#### 1.1 第一个产品


![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/macbook-pro.png)

- MacBook Pro，它是我认为对于工作者来说最佳性价比的苹果设备。特别是对于那些不时需要出门在外办公、写代码、写文案、做设计、做音乐、做视频的人来讲，是最佳的移动办公设备。它的触控板真的是非常好用。（背景macbook pro登场视频）

#### 1.2 第二个产品


![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/mac-studio.png)

- Mac Studio，它是最适合于固定办公场景的用户。
- 但是由于 Mac Studio 价格还是有点高，我们可以用黑苹果来代替。
- 如果有足够的经济实力，还是推荐购买。

-------------------------------------------------------------------


## 2. 黑苹果硬件推荐


![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/opencore-index.png)

- 当前最有名的黑苹果引导是 OpenCore，它的官网文档写得非常的好，不推荐大家使用第三方封装的镜像、EFI，而是我们自己根据官网的教程来定制。
- OpenCore 官网有指导我们怎么选择硬件，接下来我将进行解读：
- <https://dortania.github.io/OpenCore-Install-Guide/macos-limits.html#cpu-support>

![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/opencore-cpu.png)

- 对于 CPU 的选择，如官网说明，CPU 目前（2022-05）是支持到 Intel 11 代架构，但是 11 代的核显是无法驱动的，所以稳妥起见还是推荐 10 代为最佳。主要因为苹果有采用 Intel 十代的 iMac，该适配的都适配到位了。
- 虽然官网没有专门提核显问题，这里我还是推荐 CPU 最好是有核显的，也就是排除带 F 后缀的 CPU 型号，比如：i7-10700F，这可以帮助我们在处理视频工作的时候有核显加速。虽然 W3275 这类服务器 CPU 性能更强，但是大多数人都是综合类生活场景需求。
- 当然，不排除等等党胜利，不排除过一段时间 12 代的 kf 成为新成熟方案，但是至少在当下，想要以稳定作为生产力输出的话还是用官网推荐的 CPU 最好。
- 假设我们这里选择了：i9-10900K，盒装已经不卖了，大家只能淘宝买散片

![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/opencore-gpu.png)

- 对于 GPU 的选择，能支持到最新系统的 GPU 目前（2022-05）只有 AMD 的才能免驱，主推 Navi 20 架构的 RX 6000 系列，更加具体的说是：Navi 23、Navi 21 两个系。
- 目前已知支持的有：RX6600XT/RX6800/RX6800XT/RX6900XT（需要特别注意的是：RX6700 暂时不支持免驱，不建议购买）
- 当然，很多人都想跳过这代 `矿卡`，你等，你赢。
- 假设我们这里选择了：RX6600XT

![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/opencore-motherboard.png)

- 对于主板、硬盘的选择，官网没太多限制，但是主板京东目前（2022-05）还在卖的一手 Z490 不多了，
- 假设我们这里选择了：华擎（ASRock）Z490 Steel Legend钢铁传奇主板
- 硬盘选择：西数SN770

![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/opencore-wifi.png)


- 无线网卡是非必须的，如果你想要无线网络相关功能，那官网也有推荐对应的型号：
- <https://dortania.github.io/Wireless-Buyers-Guide/unsupported.html>
- 你可以淘宝搜索以下无线网卡：
- BCM94360CD + PCIEx1 转接卡（四天线）
- BCM94360CS2 + PCIEx1 转接卡（两天线）
- 个人主推 BCM94360CD

![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/opencore-other.png)

- 其他硬件上就再没特别要求了。

#### 硬件总结

![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/macos-hardware.png)

- 综合前面介绍的，最后我们总结下硬件上整体的推荐方案：
- CPU 选用：i9-10900K
- GPU 选用：RX-6600XT
- 主板选用：Z490
- 硬盘：SN770
- 无线网卡：BCM94360CD
- 显示器，我个人推荐较便宜的：AOC Q2790PQ、AOC U27N3C，整体性价比较高。
- 加上其他台式机配件，如果是外接 4 个 2K、4K显示器，那预算需要 1.2w ~ 1.5w 左右。
- 再加一台 MacBook Air 16G （1w）或 MacBook Pro 16G 1.5w）用于外出写代码。则理想状态下的办公条件需要：2.5w ~ 3w 左右。大家也不用急于一时，慢慢积累。



-------------------------------------------------------------------


## 3. 黑苹果详细安装流程（macOS Monterey）


![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/macos-install-opencore.png)


- 由于该章节内容过多，有一万多个字，所以我独立出一个文章，具体大家可以访问如下地址：
- <https://github.com/cdk8s/cdk8s-team-style/blob/master/os/macOS/macOS-install.md>
- 也可以全网搜索：`UPUPMO 黑苹果安装`


-------------------------------------------------------------------


## 4. macOS 新手入门指南

![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/macos-basic.png)


- 一共六十多章节我已经全部整理好了，主要分为：必懂概念、系统功能点两部分。
- 如果你还有遇到什么新手问题是我没考虑到位的，可以微信联系我。
- 具体大家可以看如下地址：
- <https://github.com/cdk8s/cdk8s-team-style/blob/master/os/macOS/macOS-basic.md>

-------------------------------------------------------------------


## 5. macOS 软件大全推荐


![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/macos-game.png)


- 常用、优秀的软件我都已经整理好了，大家可以访问下面链接查看。
- 特别需要说明的，macOS 是可以打游戏的，我也整理了主流的几十款中大型游戏。但是它整体效果没有 Windows 强，游戏也没有 Windows 多而已。应付一般人是足够的。
- <https://www.upupmo.com/subject?cpid=111111111111111211>


![opencore-index](https://openfilecdn.upupmo.com/upupmo-article/mac/2-macos/macos-dev-software.png)


- 需要特别单独来说明的是：编程软件争论
- 目前行业主流现状如下（不接受反驳）：
- Java 普遍 IntelliJ IDEA，Go 普遍 Goland，Python 普遍 PyCharm，
- Php 普遍 PhpStorm，Android 普遍 Android Studio，C 普遍 Visual Studio
- JavaScript 普遍 VSCode。至于 Vim、记事本等小众流派不在讨论范围。
- 其他都没啥问题，就前端我有异议。
- 如果你平时就只是写代码，那 VSCode 搭配各种插件确实可以很好地完成任务。
- 但是像我这种每当学习一种新东西的时候会从 Github 下载几十个项目在同一个目录下进行配置分析、查询引用、快速检索、互相比对等操作的人来讲，VSCode 完全没法用。
- 个人认为在硬件足够的情况下，应该优先使用 WebStorm，它能做的事情比 VSCode 多的多。当然目前大家基本都会安装 VSCode，毕竟轻量，做个临时编辑器也比其他好用。
- 对于开发者来讲，从 Windows 转到 macOS 最初的痛苦莫过于快捷键，我已经帮 IntelliJ 系的 IDE 用户准备了材料，具体查看以下文章。
- <https://github.com/judasn/IntelliJ-IDEA-Tutorial/blob/master/keymap-win-mac.md>

-------------------------------------------------------------------


## 下期预告

- 下期我们将介绍《软件开发设计阶段的思考、实践》，分别从以下 5 个方面进行讲解：

```
1. 竞品分析
2. 原型设计
3. 架构设计
4. 基础数据准备（爬虫）
5. 项目管理准备
```

## 最后

- 如果你心中有创意，想自己开发产品，可以微信联系我们。
- 如果你觉得视频对你有帮助，欢迎点赞、收藏、转发。我们下期见。











