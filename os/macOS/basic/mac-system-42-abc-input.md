
![2016-11-20_10-46-59.jpg](https://cdn.uptmr.com/upupmo-article/mac/basic/mac-system-42-abc-input.png)


```
Mac Studio 长按电源进入恢复模式，关闭 SIP 机制，终端输入：csrutil disable
然后重启电脑，进入电脑后找到 ~/Library/Preferences/com.apple.HIToolbox.plist 文件
用 xcode 打开该文件，找到 Root > AppleEnabledInputSources > Item0 > KeyboardLayout Name = ABC 这个项，删除该 Item0
保存配置文件
右键点击 com.apple.HIToolbox.plist 文件 > 显示简介 > 勾选已锁定，不要让它改回来
重启电脑。
进入恢复模式，打开系统完整性保护（SIP），终端输入：csrutil enable
```

- 换种方式就是推荐用 [自动切换输入法](https://www.uptmr.com/subject?cpid=111111111111111211)


