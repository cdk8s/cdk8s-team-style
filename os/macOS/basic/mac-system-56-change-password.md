

- 默认安装 mac 不能输入 2 位数密码，所以安装完后我们需要修改


```
先输入 pwpolicy -clearaccountpolicies 进行清除账号的规则

再输入 passwd 进行更换密码 (macOS 12 系统新命令为：security set-keychain-password)

根据提示输入旧密码
根据提示输入新密码
根据提示输入确认新密码
```