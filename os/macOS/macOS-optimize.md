
## 系统优化

- 关闭聚焦：`sudo mdutil -a -i off`
- 系统偏好设置 》节能 》设置永久
- 系统偏好设置 》软件更新 》高级 》关闭自动更新
- 系统偏好设置 》辅助功能 》显示 》指针 》指针大小
- 系统偏好设置 》程序坞与菜单栏 》设置程序坞放大效果、取消时间显示、取消 Wi-Fi 显示、取消聚焦显示
- 系统偏好设置 》显示器 》夜览模式
- 系统偏好设置 》调度中心 》触发角
- 系统偏好设置 》通用 》隔空投送与接力
  - 关闭：允许在这台Mac和iCloud设备之间使用“接力”，避免粘贴的传递（当前版本做得不聪明）
- 通过终端命令修改用户密码
- 先输入：`pwpolicy -clearaccountpolicies` 进行清除密码长度限制规则
- 再输入：`passwd` 进行更换密码 ( macOS 12 及最新系统命令为：`security set-keychain-password`)
- 设置网络 DNS，具体参考：
- <https://github.com/cdk8s/cdk8s-team-style/blob/master/os/macOS/macOS-DNS.md>
- 然后清除 DNS 缓存：`sudo killall -HUP mDNSResponder`

## 配置文件分享

- stash 配置
- SwitchHosts 配置
- Cursor 配置