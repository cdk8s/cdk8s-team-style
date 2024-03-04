
![2016-11-20_10-46-59.jpg](https://cdn.uptmr.com/upupmo-article/mac/basic/mac-system-38-change-launchpad.png)

- 推荐用 [macOS 小助手](https://www.upupmo.com/subject?cpid=111111111111111211)

-------------------------------------------------------------------

- 也可以用命令行：
- 图片合并的方式类似于 iPhone，只要拖动软件图标合在一起自动变成一个文件夹
- 调整 Launchpad 应用图标排列方式：
    - 打开终端
    - 输入命令：`defaults write com.apple.dock springboard-rows -int 8`
        - 6 表示显示行数是 6 个。
    - 输入命令：`defaults write com.apple.dock springboard-columns -int 12`
        - 8 表示显示列数为8个。
    - 重置：`defaults write com.apple.dock ResetLaunchPad -bool true`
    - 输入命令，重启 Dock：`killall Dock`

--------------------

- 恢复默认的排列方式：
    - 打开终端
    - 输入命令：`defaults write com.apple.dock springboard-rows Default`
    - 输入命令：`defaults write com.apple.dock springboard-columns Default`
    - 输入命令，重启 Dock：`killall Dock`

