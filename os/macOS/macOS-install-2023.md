
# 黑苹果详细安装教程-基于OpenCore官网指导-UPUPMO（macOS Monterey）

## 特别声明

```
如果你是 12、13 代酷睿需要仿冒 10 代酷睿
可以在 OpenCore 的 config.plist → Kernel → Emulate 添加以下内容即可：

Cpuid1Data：55060A00 00000000 00000000 00000000
Cpuid1Mask：FFFFFFFF 00000000 00000000 00000000
```


## 文章大纲

```
01. 必备知识
02. 作者当前硬件说明
03. 主板 BIOS 版本升级
04. 确定声卡、网卡信息
05. 配置 EFI 驱动
06. 配置 ACPI（SSDTs）
07. 配置 config.plist
08. 制作启动盘（苹果官网恢复镜像）
09. 配置主板 BIOS
10. 开始安装 macOS
11. 验证、调试、优化
12. 安装后的系统优化
13. 特别注意事项说明
```

-------------------------------------------------------------------

## 1. 必备知识

- 查看本篇需要有台式机组装知识储备、Windows 安装知识储备、主板 BIOS 配置知识储备、macOS 基础知识，比如如何安装软件，修改系统偏好设置等。
- 关于 macOS 基础系列我已经整理好了，不会可以先学习下：
- <https://github.com/cdk8s/cdk8s-team-style/blob/master/os/macOS/macOS-basic.md>
- 如果你无法具备以上基础知识，出错概念极大，不要灰心，多试几次，多搜索，直到你基础知识都学到位，理论上必然可以安装好。基础不过关，总是会充满困苦的。
- 本篇是基于台式机方案，但是过程详解了 OpenCore 官网指导，所以同道理也可以用到一些笔记本上，但是毕竟是有些区别，笔记本用户要有心里准备受挫。

```
1. 本篇文章的前篇是《从开公司到开发全平台产品-2.黑、白苹果软硬件及系统安装》，可全网搜索先进行查看。
2. OpenCore 的核心包都在 GitHub，不排除你所在地区网络需要自备穿越工具才能下载。
3. 准备好 2 块固态硬盘，一块已经安装好 Windows 系统，一块干净的准备安装 macOS。
4. 准备好一个 FAT32 格式 U盘（16 GB或以上）
5. 本篇只是详细文字版，不再出视频教程，想看视频推荐本文尾部推荐的 UP 主，但是先建议先看我的文字版，因为我比他们还详细，更加注意小细节，本文是对着 OpenCore 官网来的。
6. 本篇很详细，内容很长，新手建议从头看到尾，不推荐边看边操作。先让自己有一个系统性地了解，让来详细研究每一步是最好的学习办法。
```

- 本文首发在 Github：<https://github.com/cdk8s/cdk8s-team-style/blob/master/os/macOS/macOS-install.md>
- 后续全网其他平台不会更新，想要关注更新可以访问 Github 进行查看

-------------------------------------------------------------------

## 2. 作者当前硬件说明

```
已经试过以下设备：
CPU：Intel i9-10900k、Intel i7-8700k、Intel i7-8700
主板：技嘉 Z490M、技嘉 Z370M、技嘉 B360M
显卡：AMD RX 6600XT、AMD RX 5600XT（免驱支持最高到 macOS12）、AMD RX 560
硬盘：推荐尽可能是西部数码 Black 系列，支持 TRIM 比较好
本文对 Intel 8代、10代验证有效，其他版本未测试，但是理论上 Intel 10 代以前都是有效。
```

-------------------------------------------------------------------

## 3. 主板 BIOS 版本升级（非必须）

- 声明：更新 BIOS 有风险，请自行评估，计算机基础不过关的不推荐升级。
- 因为有的主板出厂是是有多个版本的，所以到主板官网下驱动的时候有的人会看到 xxx-rev1.0，xxx-rev2.0 这样的区分选项。
- 这时候你需要打开机箱，在主板边角位置找到写有版本号的信息，一般情况主板是没有那么多版本的。
- 如下图，是作者的主板版本信息：

![图片1](https://openfilecdn.upupmo.com/upupmo-article/mac/macos-install/motherboard-version.png)

- 确定好主板版本后，到主板官网下载最新 BIOS：
- 技嘉官网：<https://www.gigabyte.cn/Support/Motherboard>
- 技嘉官网更新 BIOS 说明：<https://www.gigabyte.cn/WebPage/-2/HowToReflashBIOS.html>
- 华硕官网：<https://www.asus.com.cn/support/Download-Center/>
- 华硕官网更新 BIOS 说明：<https://www.asus.com.cn/support/FAQ/1008859#A2>
- 作者的技嘉 Z490M BIOS 下载地址，有一个版本可以更新：
- <https://www.gigabyte.cn/Motherboard/Z490M-GAMING-X-rev-10/support#support-dl-BIOS>
- 这里我们再简单介绍下技嘉主板的更新方法：
- 准备一个 U盘，格式必须是 FAT32，把下载到 BIOS 更新包先解压到本地电脑后，再复制到 U盘根目录。
- 接着重启电脑按 DEL 进入 BIOS 设置，再根据我主板界面提示的 Q-FLASH 快捷键进入 Q-FLASH 模式（这是技嘉主板的叫法，其他品牌不这么叫）。如下图步骤更新：

![图片1](https://openfilecdn.upupmo.com/upupmo-article/mac/macos-install/bios-update-1.png)
![图片2](https://openfilecdn.upupmo.com/upupmo-article/mac/macos-install/bios-update-2.png)
![图片3](https://openfilecdn.upupmo.com/upupmo-article/mac/macos-install/bios-update-3.png)

-------------------------------------------------------------------

## 4. 确定声卡、网卡信息


- 现在，我们已经假设你有一个固态硬盘已经安装好 Windows 系统。
- 这时候你先进入 Windows 系统下安装 `Aida64`，通过该软件查看自己的硬件配置信息。
- 重点关注声卡、网卡。比如我的信息：
```
我的声卡是：Realtek ALC S1220A
我的网卡是：Intel(R) Ethernet Connection (11) I219-V
```
- 以上两个信息先记录下来，等下都会用到。

-------------------------------------------------------------------

## 5. 配置 EFI 驱动（配置基础的 OpenCore Files）


- 官网教程写得非常好，即使你英文不好也要先翻译快速过下
  - <https://dortania.github.io/OpenCore-Install-Guide/installer-guide/>
  - 官网是先格式化优盘，然后下载镜像，然后在优盘中修改 EFI 文件，我觉得不对。应该是现在本地硬盘上修改 EFI 再放入优盘。所以我顺序调换了一下。
- 准备 Python3 环境
  - 下载地址：<https://www.python.org/downloads/>
  - 安装的时候记得勾选添加系统变量到 path：Add Python to environment variables
- 准备 ProperTree 工具
  - 下载 ProperTree 编辑器软件（官网要求不要使用 OpenCore Configurator）
  - 下载地址：<https://github.com/corpnewt/ProperTree>
  - 下载解压，双击打开 ProperTree.bat
- 准备 Rufus 工具
  - 下载地址：<https://rufus.ie/zh/>
  - 准备 8GB 以上优盘，使用 Rufus 格式化为 FAT32 格式，其设置如下
      - 引导类型选择：非可引导
      - 分区类型：GPT
      - 目标系统类型：BIOS 或 UEFI
      - 文件系统：Large FAT32
      - 簇大小：32K

#### 5.1 下载 OpenCore 并保留基础驱动

- 官网文档：<https://dortania.github.io/OpenCore-Install-Guide/installer-guide/opencore-efi.html>
- 下载地址：<https://github.com/acidanthera/OpenCorePkg/releases>
- 在 Windows 系统下，先下载：OpenCore
  - 当前时间 2022-04 最新版为 0.7.9，后续有其他版本也是一样流程不用担心
  - 当前时间 2023-09 最新版为 0.9.5，后续有其他版本也是一样流程不用担心（经过测试 0.9.4 有问题，0.9.5 测试成功）
- 解压 OpenCore 得到目录 /OpenCore-0.9.4-RELEASE
- 先把 /OpenCore-0.9.4-RELEASE/IA32 删除掉，这个是给 32 位的机子准备的
- 进入 /OpenCore-0.9.4-RELEASE/X64 文件夹，把里面的 EFI 文件夹复制电脑桌面，假设我们暂定给它命名为：NEW_EFI，方便区分。
- 接着把 /OpenCore-0.9.4-RELEASE/Docs 下的 Sample.plist 文件复制到 NEW_EFI/OC 的目录下，并改名为 config.plist
- 接着把 /NEW_EFI/OC/Drivers 下的所有默认文件删除掉，只留下 OpenRuntime.efi、ResetNvramEntry.efi、OpenCanopy.efi（OpenCanopy 是用于 GUI 展示，非必须，但是先建议按我的来）
  - ResetNvramEntry.efi 是用于在系统启动菜单中添加一个 Reset NVRAM 按钮
  - Reset NVRAM 的作用是：它存储了音量、时间、键盘和鼠标偏好、显示屏分辨率、启动磁盘选择、时区，以及最近的内核崩溃信息等信息，有时候可以解决一些乱七八糟问题
- 接着把 /NEW_EFI/OC/Tools 下的所有默认文件删除掉
- 以上这些 EFI 为什么不要官网文档有解释：<https://dortania.github.io/OpenCore-Install-Guide/installer-guide/opencore-efi.html>
- 以及下面要讲的更多配置，官网也有解释：<https://dortania.github.io/OpenCore-Install-Guide/ktext.html#firmware-drivers>

#### 5.2 HfsPlus 固件驱动

- 下载最新的 HfsPlus.efi（必须，用于对 HFS 文件系统支持）
- 下载地址：<https://github.com/acidanthera/OcBinaryData/blob/master/Drivers>
- 放到 /NEW_EFI/OC/Drivers 目录下


#### 5.3 Lilu 驱动

- 对于 Kexts 类型的驱动，官网提供了专门的下载站，优先考虑从这里瞎子啊：<https://dortania.github.io/builds/?viewall=true>
- 下载最新的 Lilu（必须，基础库）
- 下载地址：<https://github.com/acidanthera/Lilu/releases>
- 解压后把 Kexts 目录下的 Lilu.kext 文件复制到 /NEW_EFI/OC/Kexts 目录下

#### 5.4 VirtualSMC 驱动

- 下载最新的 VirtualSMC（必须，用于模拟苹果的 SMC）
- 下载地址：<https://github.com/acidanthera/VirtualSMC/releases>
- 解压后把 Kexts 目录下的
- 必须（AMD 显卡用户）
    - VirtualSMC.kext
    - SMCProcessor.kext 用于监控 CPU 温度
    - SMCSuperIO.kext 用于监控散热器速度
    - SMCRadeonGPU.kext 用于监控 AMD GPU 温度（通过 iStat Meuns 看到显卡温度了）
    - RadeonSensor.kext 用于 AMD GPU 传感器
- 非必须
    - SMCLightSensor.kext 用于环境光检测（台式机不需要）
    - SMCBatteryManager.kext 用于读取电池信息（台式机不需要）
- 文件复制到 /NEW_EFI/OC/Kexts 目录下
- 因为 从 Radeon VII 开始，Apple 停止直接查看显卡温度的功能，我们需要加载额外的 RadeonSensor 来显示温度。
- RadeonSensor 就是目前最流行的项目：<https://github.com/aluveitie/RadeonSensor>
- 下载最新的 Release 版本（点击 Downloads 按钮）：<https://github.com/aluveitie/RadeonSensor/tags>



#### 5.5 显卡驱动

- 下载最新的 WhateverGreen（必须，显卡支持）
- 下载地址：<https://github.com/acidanthera/WhateverGreen/releases>
- 解压后把 Kexts 目录下的 WhateverGreen.kext 文件复制到 /NEW_EFI/OC/Kexts 目录下


#### 5.6 声卡驱动

- 下载最新的 AppleALC
- 下载地址：<https://github.com/acidanthera/AppleALC/releases>
- 解压后把 Kexts 目录下的 AppleALC.kext 文件复制到 /NEW_EFI/OC/Kexts 目录下


#### 5.7 非苹果品牌的 SSD 硬盘驱动

- 固态硬盘不推荐海力士，镁光，Intel 牌子。
- 下载最新的 NVMeFix
- 下载地址：<https://github.com/acidanthera/NVMeFix/releases>
- 解压后把 Kexts 目录下的 NVMeFix.kext 文件复制到 /NEW_EFI/OC/Kexts 目录下

#### 5.8 网卡驱动

- 网卡场景比较多，具体规则看官网：
- <https://dortania.github.io/OpenCore-Install-Guide/ktext.html#ethernet>
- 技嘉 Z370M 对应的是：`Intel(R) Ethernet Connection (2) I219-V`
- 技嘉 B360M 对应的是：`Intel(R) Ethernet Connection (2) I219-V`
- 技嘉 Z490M 对应的是：`Intel(R) Ethernet Connection (2) I219-V`
- 根据官网规则，作者的 3 块主板应该选择 IntelMausi
- 下载最新的：IntelMausi
- 下载地址：<https://github.com/acidanthera/IntelMausi/releases>
- 解压后把 Kexts 目录下的 IntelMausi.kext 文件复制到 /NEW_EFI/OC/Kexts 目录下

#### 5.9 PS2 驱动（非必须）
- 如果你用的是 PS2 接口的鼠标、键盘则需要 VoodooPS2
- 下载地址：<https://github.com/acidanthera/VoodooPS2/releases>
- 解压后把 Kexts 目录下的 VoodooPS2Controller.kext 文件复制到 /NEW_EFI/OC/Kexts 目录下

#### 5.10 无线网卡 + 蓝牙推荐（非必须）

- 如果你台式机要使用无线网卡+蓝牙建议淘宝买：
- BCM94360CD + PCIEx1 转接卡（四天线）
- BCM94360CS2 + PCIEx1 转接卡（两天线）
- 还需要 AirportBrcmFixup：
- 下载地址：<https://github.com/acidanthera/AirportBrcmFixup/releases>
- 还需要 BrcmPatchRAM：
- 下载地址：<https://github.com/acidanthera/BrcmPatchRAM/releases>
- 解压后把 Kexts 复制到 /NEW_EFI/OC/Kexts 目录下。
- 虽然它们可以免驱，但是下面即将介绍的 USB 定制记得也看看这个设备对应的值，因为蓝牙设备是用 USB2.0 的线连接的，所以也需要 USB 定制

#### 5.11 USB 驱动定制（必须，很繁琐，需要认真看多次）

- 2023-09 更新，现在官网有新的工具和适配方法：<https://dortania.github.io/OpenCore-Install-Guide/ktext.html#usb>
- 步骤：
```
从 https://github.com/USBToolBox/tool/releases 下载名字为 Windows.exe 文章
运行后会出现一个命令行交互界面，选择：Discover Ports，然后不要关掉终端，
找个 USB 优盘，插入到各个接口中，插入后 5 秒不要动，等命令行中显示它识别到你插入的优盘，你再拔出来换下一个，直到所有端口识别到。
如果是 typec 接口，正反面交换插入让它识别。

全部识别到后，输入 B 回车返回主菜单，接着选择：Select Ports and Build Kext
然后根据提示输入 K 回车即可导出 UTBMap.kext，一般会保存到 exe 软件同级目录下

接着再下载这里 https://github.com/USBToolBox/kext 下载 USBToolBox.kext，把这两个都放在 kext 目录下

配置的时候：在 Kernel 分类下的 XhciPortLimit 设置 False（下面也有再次强调，看不懂这句话配置可以直接跳过）
```


- 2022-05 编写的旧手动配置方法
```
- 先确定自己属于哪个 SMBOIS 平台，大家可以学习我以下方式来确认自己属于哪个值。
- 我的 i7-8700k，属于 coffee-lake 架构：
- 打开网站：<https://dortania.github.io/OpenCore-Install-Guide/config.plist/coffee-lake.html#platforminfo>
- 查看官网得到的 SMBOIS 结果是：iMac19,1
- 我的 i9-10900k，属于 Comet Lake 架构：
- 打开网站：<https://dortania.github.io/OpenCore-Install-Guide/config.plist/comet-lake.html#platforminfo>
- 查看官网得到的 SMBOIS 结果是：iMac20,2
- 接着下载我文章底部提供的这个配置文件：`台式机&笔记本USB万能驱动.zip` 先解压到本地。
- 接着用双击打开 ProperTree.bat，选择 `File 》 Open 》 刚解压目录\台式机USB万能驱动\USBMap.kext\Contents\info.plist`
- 在 ProperTree 的 IOKitPersonalities 节点下面，找到属于我们的 SMBOIS 的值。
- 比如我的  i7-8700k 是：iMac19,1-XHC，然后其他的都删除掉。
- 接在在 Windows 系统搜索栏中输入：`设备管理器`，打开设备管理器。
- 这时候电脑上已经插着鼠标、键盘先不要动，应该还有几个 usb 接口是空着的，我们等下要一个一个试这些 usb 口。
- 接着在 设备管理器 中找到：通用串行总线控制器，这时候我们选择主板后面从上往下第一个 USB3.0 口插入一个 U盘(该 U盘必须是 USB3.0 的)。
- 这时候你再观察：通用串行总线控制器，下面会多了一个：USB 大容量存储设备，
- 对它右键：属性 》 详细信息，在 `属性` 下拉中选择：位置路径，我们可以看到类似这样的格式数据:
- `ACPI(_SB_)#ACPI(PCI0)#ACPI(XHC_)#ACPI(RHUB)#ACPI(SS05)`
- 取最后一个关键字：SS05，然后我们要拿笔记下来这个 USB 口叫做 SS05 名字
- 接着我们拔掉 U盘，再换一个 USB3.0 口，按照以上方法（一定不要插 USB2.0 的口），记下来它叫啥名字，最后我的主板得到的数据如下，所有 USB3.0 的口从上往下、从左往右布局上看：

第1排左第1个 = SS03
第1排左第2个 = SS04
第2排左第1个 = SS01
第3排左第1个 = SS05
第3排左第2个 = SS06
机箱前面板 USB3.0 口 = SS07


- 接着我们用 USB2.0 的 U盘（没有 USB 2.0 的 U盘可以用 USB 接口的鼠标等设备），接着依次插入 USB3.0、USB2.0 所有的口，最终得到结果是：

第1排左第1个 = HS03
第1排左第2个 = HS04
第2排左第1个 = HS01
第3排左第1个 = HS05
第3排左第2个 = HS06
机箱前面板 USB3.0 口 = HS07
机箱前面板 USB2.0 口 = HS10
统计数据看起来好像只是把 SS 改为了 HS，大家还是以自己的为准。


- 接着我们回到 ProperTree 软件，
- 在 `IOKitPersonalities 》 iMac19,1-XHC 》 IOProviderMergeProperties 》ports` 节点下面
- 保留我们上面统计到的数值的节点
- 有插 USB 供电的蓝牙设备的也要统计下自己的值是什么，然后保留下来别删除，然后在其 UsbConnector 属性值还要改为：255。默认的值是 3
- 接着可以保存编辑的文件了。
- 接着将 USBMap.kext 放在 /NEW_EFI/OC/KEXT 文件夹下
```

#### 5.12 其他特殊主板要求

- 根据官网说明：<https://dortania.github.io/OpenCore-Install-Guide/ktext.html#usb>
- **部分主板还需要这个：XHCI-unsupported，包括我的 B360M**
- 下载地址：<https://github.com/RehabMan/OS-X-USB-Inject-All>
- 解压后放在，放在 /NEW_EFI/OC/KEXT 文件夹下

-------------------------------------------------------------------

## 6. 配置 ACPI（SSDTs）

- 首先要根据自己的 CPU 核心架构类型，选择不同的 SSDTs
- 官网文档：<https://dortania.github.io/OpenCore-Install-Guide/ktext.html#desktop>
- SSDT 下载地址：<https://github.com/dortania/Getting-Started-With-ACPI/tree/master/extra-files/compiled>
    - 下载这个仓库文件，解压后把以下这些 aml 文件复制到 /NEW_EFI/OC/ACPI 目录下

- 我的是 i9-10900k，属于 Comet Lake 架构，根据官网的表格（从左往右看过去），我需要用到：
```
SSDT-PLUG（cpu 电源管理修正）
SSDT-EC-USBX（usb 修正）
SSDT-AWAC（时钟修正）
SSDT-RHUB（官网详情页说：华硕 z490 必须加，Gigabyte and AsRock 不需要）
```

- 根据官网文档，另外一台：i7-8700k 是 Coffee Lake 架构需要
```
SSDT-PLUG
SSDT-EC-USBX
SSDT-AWAC
SSDT-PMC（官网详情页说 Z370 的主板不需要，所以刚好省略）
```


-------------------------------------------------------------------

## 7. 配置文件 config.plist

- 我的 i9-10900k 是 comet lake 架构，对应的官网配置文档地址：
- <https://dortania.github.io/OpenCore-Install-Guide/config.plist/comet-lake.html>
- 我的 i7-8700k 是 Coffee Lake 架构，对应的官网配置文档地址：
- <https://dortania.github.io/OpenCore-Install-Guide/config.plist/coffee-lake.html>
- **注意注意注意：请根据你的 CPU 架构，选择你自己的官网说明，里面有很多图片指导，接下来要用到，一定要选择自己架构的链接，不要直接照搬我的地址**
- 需要特别说明的：官网图片显示的是早期版本内容，所以 Boolean 类型的值是 YES/NO， 现在版本都是 TRUE/FALSE。以下步骤比较麻烦，大家要耐心根据官网文档一个一个值对过去。
- 打开 ProperTree 软件，
- 选择 `File 》Open 》/NEW_EFI/OC/config.plist 文件`
- 打开后，接着：
- 选择 `File 》OC Clean Snapshot 》/NEW_EFI/OC 文件夹`，它会自动识别里面内容
- 如果软件弹窗提示：`Disable the following kexts with Duplicate CFBundleIdentifiers?` 请按 Yes


#### 7.1 在 ACPI 分类

![配置方法](https://openfilecdn.upupmo.com/upupmo-article/mac/macos-install/opencore-config.png)

- 根据官网文档里图片红框说明操作，三个都是 True


#### 7.2 在 Booter 分类

- 根据官网文档里图片红框说明操作（从这里开始就不再贴图了，注意看文字）
- Quirks 节点上有多个要配置，注意看说明
    - 其中因为我的 B360M 主板支持配置 Resizable BAR Support，所以 ResizeAppleGpuBars 值要设置为 0

#### 7.3 在 DeviceProperties 分类

- 跟文档图片红框中相比，默认的值是缺失的 PciRoot(0x0)/Pci(0x2,0x0) 整个条目的，其下面有3个值都要自己添加上去，自己需要添加，要根据图片注意类型等细节
- AAPL,ig-platform-id 的值根据文档描述：
- 如果你是没有独立显卡的，只有核显那值要为：07009B3E 或者 00009B3E，两个只能试着来，默认用第一个值。
- 如果你是有独立显卡，独立显卡用于驱动显示器，核显用于加速，则需要填写第三个值 0300913E。
- 关于音频配置，我的主板如下：
```
技嘉 Z370M 是：Realtek ALC892
技嘉 B360M 是：Realtek ALC892
技嘉 Z490M 是：Realtek ALCS1220A
```
- layout-id 音频布局值需要参考这个文档：（官网详情说目前他们其实没用这个值，而是借用 NVRAM 分类下的 alcid = 1 的数值来起作用，所以这个可以暂时先用默认值）
- <https://github.com/acidanthera/AppleALC/wiki/Supported-codecs>
- 我的 ALC892 对应的布局有：
```
layout 1, 2, 3, 4, 5, 7, 12, 15, 16, 17, 18, 20, 22, 23, 28, 31, 32, 90, 92, 97, 99, 100
```
- 如果后续这个参数有用了，那我们需要这样换算：如果这里我们选择 7 这个 ID 进行测试，将 7 转化成 16 进制格式为 07，后面为了满足格式要求添加 6 个 0，则为
- 07000000，将这个值替换默认的 01000000（如果你的 layout 中有 1 则可以考虑不替换，采用默认值）；
- 如果我们测试 ID 为 27，27 的 16 进制为 1b，补上 6 个 0 则为 1b000000
- 如果你是 Comet Lake 架构，并且主板网卡是 intel I225-V，你还需要额外 device-id
- 我的主板都不是，所以不需要


#### 7.4 在 Kernel 分类下

- **首先：需要在 Add 中，要把 Lilu.kext 放在第一个节点，VirtualSMC.kext 放在第二个节点，因为后面的驱动是依赖 Lilu 这个基础包的**
- 在 Quirks 节点上，因为我们在主板上禁用 CFG-Lock，所以 AppleXcpmCfgLock 设置为 False。如果你的主板 BIOS 没有这个选项，那 AppleXcpmCfgLock 要设置为 true。
- 因为我们要开启主板的 VT-D，所以 DisableIoMapper 设置为 true，稍后 BIOS 中就不需要禁用 VT-D 了
- XhciPortLimit：解除15个端口限制，确认USB端口完美定制的可以为false，或者要安装的系统大于macOS11.3。有USB定制的为false

#### 7.5 在 Misc 分类下

- 根据图片说明操作即可，如果有些红框的值你配置是没有的，就自己添加
- Vault 的值是字符串值 Optional，需要自己输入
- 有一个比较特别的设置：<https://dortania.github.io/OpenCore-Install-Guide/config.plist/security.html#misc>
  - 推荐 `Misc -> Security -> SecureBootModel` 设置为 `Default`
- 默认 OpenCore 的引导界面只有终端英文交互，不是很直观，所以我们需要给它加上 GUI
- 指导：<https://dortania.github.io/OpenCore-Post-Install/cosmetic/gui.html>
- 下载 Resources 目录：<https://github.com/acidanthera/OcBinaryData>
- 把解压后的 Resources 目录覆盖 /NEW_EFI/OC/Resources  目录，
- 然后还有几个 config 参数需要改，根据文档继续修改
```
Misc -> Boot -> PickerMode: External
Misc -> Boot -> PickerAttributes: 17
Misc -> Boot -> PickerVariant 建议为 Acidanthera\Syrah 表示使用默认主题
```

#### 7.6 在 NVRAM 分类下

- boot-args 是关键参数，
- 其中 `keepsyms=1 debug=0x100` 的意思是：禁用 macOS 的 watchdog
- alcid=1 是真正起作用的音频布局，这个 1 就是上面文档中你对应声卡支持的序列，安装完要一个一个试，默认先填写 1 吧
- 各声卡布局列表可以查看：
- 官网地址：<https://github.com/acidanthera/applealc/wiki/supported-codecs>
- 注意，如果你是 AMD RX 5000、RX 6000 系列显卡（RX 6700XT 是特例，它无法驱动，不推荐购买），
- 比如我的 6600XT，则还需要加一个参数：`agdpmod=pikera` 原因是很多人都出现引导结束后，键盘灯是亮的，但是显示器没有信号的问题。
- 除了官网图片红色框的两个参数之外，还要注意
- prev-lang:kbd 改为 String 类型，值是：en-US:0
- csr-active-config: 00000000，表示不关闭 SIP，采用默认值即可
- 官网还提示：对于 Comet Lake 架构并且网卡是 Intel I225-V 或者是十代 CPU 对应的技嘉主板，
- 还需要在 boot-args 加个：dk.e1000=0 参数

#### 7.7 在 PlatformInfo 分类上的参数修改

- 根据官网文章，我的 i9-10900k 对应的平台是 `iMac20,2` 、 i7-8700k 是 `iMac19,1`
- 这里需要借助 GenSMBIOS（计算苹果序列号，用于登录 App Store）
- 下载：GenSMBIOS
- 官网下载：<https://github.com/corpnewt/GenSMBIOS>
- 双击打开 GenSMBIOS.bat，根据终端提示选择：Generate SMBIOS
- 然后此时终端会自动下载一些依赖，速度比较慢，不排除还下载不成功，如果不成功就得用穿越工具。
- 如果选择 Generate SMBIOS 成功后，等它进入一个输入交互界面后，输入：`iMac20,2`
- 这时候会生成一些序列号，都记到记事本上，然后拷贝到 ProperTree 对应的输入框上，它们键值格式对应关系是：

```
Type:         iMac19,1
Serial:       C02Y10MCDV1Q
Board Serial: C028535034NLNV98C
SmUUID:       86D9DE3C-378B-3B4C-B404-07C036A962C9
Apple ROM:    24F09438728A

Type 的值填写在配置文件上的： SystemProductName
Serial  的值填写在配置文件上的： SystemSerialNumber
Board Serial 的值填写在配置文件上的： MLB
SmUUID 的值填写在配置文件上的： SystemUUID
Apple ROM 的值填写在配置文件上的： ROM
```

#### 7.8 在 UEFI 分类下

- 根据图片说明操作即可
- 最好拖动 HfsPlus.efi 节点在第一个，OpenRuntime.efi 排第二个


#### 最后

- 最后，保存配置文件的修改：File > Save
- 到了这一步，算是所有配置文件调整好了



-------------------------------------------------------------------



## 8. 制作启动盘（苹果官网恢复镜像）

- 官网说明：<https://dortania.github.io/OpenCore-Install-Guide/installer-guide/windows-install.html#downloading-macos>
- 进入一开始下载的 OpenCore 目录下：/OpenCore-0.9.4-RELEASE/Utilities/macrecovery/
- 在 cmd 中 cd 到这个目录下，然后根据系统需求，执行如下命令（**注意注意注意：这几个值可能会变，请按上面官网地址查看最新文档**）
- 这个命令表示会下载苹果恢复系统基础镜像

```
# High Sierra (10.13)
python3 ./macrecovery.py -b Mac-7BA5B2D9E42DDD94 -m 00000000000J80300 download
python3 ./macrecovery.py -b Mac-BE088AF8C5EB4FA2 -m 00000000000J80300 download

# Mojave (10.14)
python3 ./macrecovery.py -b Mac-7BA5B2DFE22DDD8C -m 00000000000KXPG00 download

# Catalina (10.15)
python3 ./macrecovery.py -b Mac-00BE6ED71E35EB86 -m 00000000000000000 download

# Big Sur (11)
python3 ./macrecovery.py -b Mac-42FD25EABCABB274 -m 00000000000000000 download

# Monterey (12)
python3 ./macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000000000 download

# Latest version
# ie. Ventura (13)
python3 ./macrecovery.py -b Mac-4B682C642B45593E -m 00000000000000000 download
```

- **注意**：如果你的电脑只有一个 Python3 那执行命令应该是：python ./macrecovery.py xxxxxxxxx
- 输入完命令后，打开 Windows 任务管理器，切换到以太网选项，如果看到网络飙升就表示这时候已经开始下载镜像了。
- 下载好会在 \OpenCore-0.9.4-RELEASE\Utilities\macrecovery 目录下看到新增两个文件：BaseSystem.chunklist、BaseSystem.dmg（614MB）（有的是 RecoveryImage 开头文件）
- 使用 FAT32 格式的优盘，在U盘根目录创建一个目录：`com.apple.recovery.boot`，进入该目录，把下载好的 BaseSystem.dmg、BaseSystem.chunklist 放进来
- **注意注意注意：接着把我们上面做好的 NEW_EFI 目录也放到U盘根目录，改名为 EFI**
- **此时优盘根目录应该就只有两个目录：EFI、com.apple.recovery.boot**


-------------------------------------------------------------------

## 9. 配置主板 BIOS

- 官网说明：<https://dortania.github.io/OpenCore-Install-Guide/config.plist/comet-lake.html#intel-BIOS-settings>
- 因为各个主板的一些叫法可能不一样，下面是以我技嘉主板为例，大家各自的主板还需要自己研究下，理论上大多数叫法应该是一样的。

#### 9.1 以下都要禁用（Disable）

```
Fast Boot（在 boot 栏，有的也叫做 BIOS 栏）
    B360 主板：BIOS
Secure Boot Enable（在 boot 栏，或者 Favorites 栏）
    B360 主板：BIOS > Secure Boot
Secure Boot Mode 》custom
    B360 主板：BIOS > Secure Boot
Security Device Support（在 settings 》Miscellaneous 》Trusted Computing 栏，我要求的）
    B360 主板：Peripherals > Trusted Computing
Serial/COM Port（在 settings 》IO Ports 》Super IO 栏，有的在 Peripherals 栏）
    B360 主板：Peripherals > Super IO Configuration
Parallel Port（在 settings 栏，有的没这个）
    B360 主板：没有这个
VT-d（在 Tweaker 》Advanced CPU）
    我们前面 DisableIoMapper 设置了true，所以这个可以不禁用
    B360 主板：Chipset
CSM Support（在 boot 栏或者BIOS，或者 Favorites 栏）
    B360 主板：BIOS
Thunderbolt（雷电接口，比较新的机子有）
Platform Power Management（在 settings 栏）
    B360 主板：Power
Intel SGX(SW Guard Extensions)（在 settings 》Miscellaneous 栏）
    B360 主板：Peripherals
Intel Platform Trust(PPT、PTT)（在 settings 》Miscellaneous 栏）
    B360 主板：Peripherals
CFG Lock （在 boot 栏，有的主板没有这个选项，这个跟文章上部分配置中的 AppleXcpmCfgLock 参数有关，具体看上面说明）
    B360 主板：BIOS
Peripherals > Network Stack Configuration > Network Stack
Chipset > Wake on LAN Enable
```

#### 9.2 以下都要开启（Enable）

```
VT-x（在 Chipset 栏，有的叫做 intel Virtualization Technology，有的没有）
    B360 主板：没有这个
Extreme Memory Profile（有的叫做 X.M.P，设置为 enable 或者 profile1，表示对内存不锁频）
    B360 主板：M.I.T 》Advanced Frequency Settings
Intel Turbo Boost Technology（在 tweaker 栏，有的叫做M.I.T）
    B360 主板：M.I.T 》Advanced Frequency Settings 》Advanced CPU Core Settings 》Hyper-Threading Technology
Hyper-Threading（在 M.I.T 》Advanced Frequency Settings 》Advanced CPU Core Settings 》Hyper-Threading Technology。有的主板是 Tweaker 》Advance CPU Settings）
    B360 主板：M.I.T 》Advanced Frequency Settings 》Advanced CPU Core Settings 》Hyper-Threading Technology
Above 4G decoding（在 settings 》IO Ports 栏，注意对于 2020 之后的一些主板，当你开启 Above 4G decoding 之后，Resizable BAR Support 应该设置为 Disabled，比如 z490 系列的主板）
    B360 主板：Chipset
Execute Disable Bit（大多数主板没有这个）
EHCI/XHCI Hand-off（在 settings 栏，USB 选项里面）
    B360 主板：Peripherals > USB Configuration
OS type 设置为 Windows 8.1/10 UEFI Mode（在 boot 栏，有的不叫做这个，如果有一些 win10，win7 可以选择的话那就直接选择 win10 也算.如果是有 WINDOWS 8.1/10 WHQL 就直接选这个带 WHQL 的）
    B360 主板：BIOS
Internal Graphics（在 settings 》IO Ports 栏，有的在 Chipset，这个是核显要启动，配置完要保存重启电脑后下面的选项才可以看到 DVMT Total Memory Size、DVMT Pre-Allocated）
    B360 主板：Chipset
DVMT Pre-Allocated(iGPU Memory) 设置为 256M（在 settings 栏，有的没有，原因看下面那段文字）
    B360 主板：Chipset
SATA Controllerl（在 boot 栏，或者 Favorites 栏）
    B360 主板：Peripherals > SATA And RST Configuration
SATA Mode: AHCI（在 settings 栏）
    B360 主板：Peripherals > SATA And RST Configuration
Security Option 设置为 System（在 Boot 栏）
    B360 主板：BIOS
USB Mass Storege Driver Support（有的主板没有）
    B360 主板：Peripherals > USB Configuration
Legacy USB Support（有的主板没有）
    B360 主板：Peripherals > USB Configuration
选择独立显卡 PCIe 1 Slot
    B360 主板：Peripherals > Initial Display Output > PCIe 1 Slot（有独立显卡的时候）


其中在 BIOS 中加载核显最为复杂，步骤较多，在这里进行强调。
如果你是 F 后缀的 CPU 本身不带核显就不用看这一段了。
iGPU（有的叫做 Integrated Graphics） 必须是:Enabled
部分主板此项可能名为 GFX 或 Integrated Graphics 等
部分主板在开启本项保存退出 BIOS 重启再进入 BIOS 后，才会显示下面选项。我的主板就是这样的，是在 Chipset 一栏中显示.
Multiple Monitor 》Enabled，这个我没有，如果你有也设置为 Enabled)
此项主要开启核显多屏幕连接功能，但在部分机型上，没独显仅用核显时需要开启此项才能正常驱动核显。
Primary Display IGFX/IGD/PEG/PCIE 》Auto。这个我没有，如果你有设置为 Auto。
如果同时存在独显和核显，使用 Auto，如果仅用核显选择 IGFX/IGD，仅用独显选择 PCIE/PEG
DVMT Total Memory Size 》MAX，我的叫做 DVMT Total Gfx Mem。
DVMT Pre-Allocated 》建议值：64M/96M/128M/256M
```

-------------------------------------------------------------------

## 10. 开始安装 macOS

- 先确保你的台式机连接了有线网络，并且当前家里的网络是可用的状态。
- 先把 Windows 的固态硬盘先拔掉，只留下那个空的固态硬盘等下安装苹果。这个空盘不需要先分区，不需要格式化，就是单纯空的。
- 这样可以方便后续安装的时候避免选错，也可以避免在安装过程重启的时候就进入 Windows 系统，只有好处没有坏处。
- 插入刚刚准备好的 U盘，在 BIOS 中选择用 U盘启动，稍后会进入一个安装选择界面，
- 不用动它，选默认即可，过几秒后会自动进入终端跑代码输出日志而已，这时候有些代码可能会稍微停个5~10秒是很正常的。
- 但是如果你是看到跑代码界面一直停留，说明应该是你的 EFI 哪里配置出问题了（一般整个跑代码需要 1~3 分钟）
- 如果跑代码完成后会进入苹果安装界面，这时候界面是英文的，你可以点击左上角：`File 》 choose language 》更改为中文`，
- 接着选择：“磁盘工具”，刚进去可能要等个10秒左右才会出现你的硬盘名字，
- 这时候对你的空盘硬盘进行分区，选择对应硬盘，选择：“抹掉”， 名称取个英文的磁盘名字比如 mymac，格式选择 APFS，方案选择 CUID分区图。
- 分区完成后，关掉窗口，会重新回到系统安装选择界面，点击 “重新安装 macOS”，请一定要确保家里网络是通的。
- 根据提示同意协议，选择安装到刚刚那个 mymac 分区，开始安装。
- 整个安装过程前面 10 分钟左右都是在远程下载苹果最新系统镜像，这时候家里的宽带路由器应该是跑满的，
- 如果你们家里宽带比较差，那这个下载时间可能会很久。
- 这个安装过程中间会重启多次，有 3~4 次左右，一共安装时间差不多在 30 ~ 60 分钟不等，
- 期间都是自动选择对应的启动项，我们不需要管任何事情，只要好好看着就行。
- 中间不排除你的显示器进入休眠关闭，此时不是关机，可以动动鼠标看看。这期间一定不要把 U盘拔掉。
- 如果安装完成后，系统是会自动根据引导进入 macOS 登录界面的。
- 此时我们还是不能拔掉 U盘，当前系统还是通过 U盘引导才能启动到系统的。
- **再次强调，这时候 U盘 还不能拔，文章下面有一段：《最后：把 U盘 EFI 拷贝到 macOS 系统盘》，经过这个步骤之后才可以拔掉 U盘。**

-------------------------------------------------------------------

## 11. 验证、调试、优化

- 假设你这时候已经可以进入 macOS 了。

#### 11.1 调试音频值

- 下载：OpenCore Configurator（链接看文章最底部）
- 下载与你当前 OpenCore 核心相同的版本。
- 打开U盘目录 /EFI/OC/ 目录，右键选择 config.plist 文件，选择打开方式：使用OpenCore Configurator 打开
- 选择左侧：NVRAM-随机访问存储器设置，结果可能有多个选项，每个都点一下，直到看到最右侧键值对中有 boot-args 参数，
- 该参数原来的值应该是：`-v keepsyms=1 debug=0x100 alcid=1`
- 这里的 `alcid=1` 就是音频布局，
- 根据官网文档：<https://github.com/acidanthera/applealc/wiki/supported-codecs>
- 我主板的音频设备是：Realtek ALC892，与之对应的布局有：
```
layout 1, 2, 3, 4, 5, 7, 12, 15, 16, 17, 18, 20, 22, 23, 28, 31, 32, 90, 92, 97, 99, 100
```
- 一开始我用了 1 进行测试，如果不行就得一个一个值改，然后重启电脑进行测试。
- 这一步很麻烦，没有快捷方法，只能你慢慢试，理论上根据官网布局值一般是够用的。


#### 11.2 验证黑苹果完整性

- 验证双系统可以正常切换（如果不用 Windows 系统的，最好拔掉 Windows 硬盘，这是最优解）
- 确定 Apple ID 可以登录（登录的该 Apple ID 最好是以前登录过真实的苹果设备的，比如 iPhone、MacBook 的，这样更加安全）
- 连接多个显示器，显示是否正常
- 验证有线网络连接
- 验证声音播放
- 确保所有USB 2.0/3.0 和 3.1 接口
- 如果有无线网卡、蓝牙也要检测下
- 验证自动睡眠、手动睡眠（建议少用睡眠，台式机不像笔记本）
- 验证关机/重启
- 安装 iStat Menus，查看系统资源监控，如CPU、内存、硬盘负载/温度可以展示
- 安装 CPU-S，测试变频
- 安装 VideoProc Converter，验证核显加速
- 安装 Hackintool，查看以下信息：
    - 在系统下面是否有显示：IGPU、GFX0 信息，如果没有 IGPU 则表示你核显没识别到。
    - VDA 解码器是否是：完全支持，是的话才可以硬解
    - 查看 GFX0 显卡是否支持 硬件加速(QE/CI)，正常值是 Yes
    - 查看 GFX0 显卡是否支持 Metal，正常值是 Yes


#### 11.3 最后：把 U盘 EFI 拷贝到 macOS 系统盘

- 因为我们前面调试的都是 U盘下的 EFI 所有 造成 U盘不可以拔， 到了这一步表示你已经优化完成了，可以做最后的迁移了。
- 我们需要把 U盘中的 EFI 目录复制到 mac 固态硬盘的 ESP 分区根目录下。
- 这时候我们可以打开 OpenCore Configuretor（如果没安装需要自己去下载安装），
- 点击头部工具栏选择：`工具 》 挂载 EFI`
- 在弹出界面中，下面的 “EFI 分区” 区域中，选择你 macOS 安装的所在盘，点击右侧的：挂载分区
- 挂载后分区后，点击 “打开分区”，然后把U盘下整个 EFI 目录拷贝到该分区根目录下。
- 这表示以后就从硬盘上的 EFI 引导，我们现在可以拔掉U盘重启试一下。


-------------------------------------------------------------------

## 12. 安装后的系统优化


#### 12.1 设置双系统引导

- 双系统下 OpenCore 会自动识别 Windows 分区，所以不需要做过多的修改。只需要把 macOS 所在磁盘改为第一引导顺序即可。
- 然后在 macOS 下：`系统偏好设置 》 启动磁盘 》选择 mac 盘，然后锁住`
- 像我已经不用 Windows 的情况下，其实也可以把安装前的 Windows 的盘格式化掉，作为 macOS 的数据盘使用


#### 12.2 设置双系统引导选项读秒时间

- 打开U盘目录 /EFI/OC/ 目录，右键选择 config.plist 文件，选择打开方式：使用 OpenCore Configurator 打开。
- 选择左侧：`Misc其他设置 》Boot 》Timeout`，建议 Timeout 改为3-5，如果觉得太慢了也可以改为 1，不建议改为 0。
- 选择左侧：`Misc其他设置 》Security 》AllowSetDefault` 的值设置为true


#### 12.3 关闭开机跑代码窗口

- 打开 U盘目录 /EFI/OC/，右键 config.plist 文件，选择打开方式：使用OpenCore Configurator.app打开
- 选择左侧：`NVRAM-随机访问存储器设置`，右侧会有多个选项，每个都点一下，直到看到右侧键值对中有 boot-args
- 原来的值是：`-v keepsyms=1 debug=0x100 alcid=1`
- 这时候要去掉 `-v` 这个值，该值表示启动时候终端显示执行代码过程，有故障的时候好分析



#### 12.4 关闭启动日志生成

- 打开 U盘目录 /EFI/OC/，右键 config.plist 文件，选择打开方式：使用OpenCore Configurator.app打开
- 选择左侧：`Misc其他设置 》debug` 选项下的 target 数值改为 3（原来是67）
- 然后保存 config.plist 重启电脑试试



#### 12.5 系统优化

- 关闭聚焦：`sudo mdutil -a -i off`
- 系统偏好设置 》节能 》设置永久
- 系统偏好设置 》软件更新 》高级 》关闭自动更新
- 系统偏好设置 》辅助功能 》显示 》指针 》指针大小
- 系统偏好设置 》程序坞与菜单栏 》设置程序坞放大效果、取消时间显示、取消 Wi-Fi 显示、取消聚焦显示
- 系统偏好设置 》显示器 》夜览模式
- 系统偏好设置 》调度中心 》触发角
- 通过终端命令修改用户密码
- 先输入：`pwpolicy -clearaccountpolicies` 进行清除密码长度限制规则
- 再输入：`passwd` 进行更换密码 ( macOS 12 系统命令为：`security set-keychain-password`)
- 设置网络 DNS，具体参考：
- <https://github.com/cdk8s/cdk8s-team-style/blob/master/os/macOS/macOS-basic.md>
- 然后清除 DNS 缓存：`sudo killall -HUP mDNSResponder`


#### 12.7 显卡超过 60 度后还是没有开启转速

- 一般现在的显卡到是 60 度就会自动开启转速，但是有时候还是会出现没有开启转速的情况，这时候我们可以通过修改显卡的配置文件来解决这个问题。
- 可以通过玩大型游戏（比如：海岛大亨）来升温触发显卡转速，看下是否达到 60 度后自动开启转速
- 可以参考这个视频：<https://www.bilibili.com/video/BV1WT411A72F>

#### 12.8 开启 HiDPI

- 参考文章：<https://apple.sqlsec.com/6-%E5%AE%9E%E7%94%A8%E5%A7%BF%E5%8A%BF/6-5/>
- 一般是 4k 分辨率开启后选择 2k 这样才会有好的效果

```
执行这个脚本：https://github.com/xzhih/one-key-hidpi
国外源
sh -c "$(curl -fsSL https://raw.githubusercontent.com/xzhih/one-key-hidpi/master/hidpi.sh)"

国内源
sh -c "$(curl -fsSL https://html.sqlsec.com/hidpi.sh)"

脚本引导的时候选择：(1)开启HIDPI 即可
开启后，在显示器设置中，分辨率选择的时候右边有一个小的文字：(HiDPI)

```

-------------------------------------------------------------------

## 13. 特别注意事项说明

#### 13.1 系统升级

- 如果你打算以 macOS 为生产力，那建议养成好习惯，最好设置默认引导系统是 macOS，
- 并且关闭 Windows 系统的自动更新，避免一些可能出现的升级意外。
- 如果不用 Windows 那就更好了，直接拔掉 Windows 硬盘。

#### 13.2 分享 EFI 注意事项

- 如果你打算分享你的 EFI 文件到网络上，那我建议你分享之前记得把自己 SMBIOS 值修改下，
- 避免别人直接使用，避免一台电脑同时在线多个 Apple ID 造成账号异常。

#### 13.3 BIOS 注意事项

- 如果你安装完黑苹果之后，又换了一些硬件，比如新增其他硬盘，不排除此时的主板的 BIOS 设置会被重置，
- 这时候你再接回原来好的 mac 盘是会出现启动不了，这时候就要再去检查一些原来那些 BIOS 修改的是否还在。
- 如果你主板有保存 BIOS 配置功能，记得保存一份，方便后续直接还原。

#### 13.4 安全

- 不推荐在 Windows 上安装可见 macOS 磁盘的软件（比如 Paragon HFS），可以避免误删除到系统文件。
- 如果你经常和我一样安装杂七杂八的不安全软件，最好不要关闭 SIP。


-------------------------------------------------------------------

## 特别链接集合

- [国光的黑苹果](https://github.com/sqlsec/Hackintosh)
- Windows 系统中准备的软件
    - 台式机&笔记本USB万能驱动.zip
    - Aida64
    - DiskGenius
- macOS 系统中准备的软件
    - OpenCore Configurator
    - iStat Menus
    - CPU-S
    - VideoProc Converter
    - Hackintool
- UP 主
    - 大头菜Cass
    - 司波图
    - ereel
    - 吾乃阿风同学
    - 黛码小哥哥
    - QZFoureyes
- 教程
    - 完美双系统系列教程第9集，升级OC引导

- 以上非 Github 链接都已整理在这里（用电脑浏览器打开）：<https://www.upupmo.com/s/5f6fdb1a9a9d4f0e8cb80817dcd00309>


