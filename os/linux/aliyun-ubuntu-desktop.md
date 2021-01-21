
# 给阿里云 Ubuntu 16.04 系统安装图形化桌面

- 有些场景比较特殊，比如需要一些特别的 VPN 工具，隧道等
- 官网参考：<https://help.aliyun.com/knowledge_detail/41227.html>


## 安装

```
通过 SSH 先连接上去安装软件：
apt-get update
sudo apt-get install -y x-window-system-core
sudo apt-get install -y gdm
sudo apt-get install -y ubuntu-desktop
sudo apt-get install -y gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal


vim /etc/pam.d/gdm-autologin
#注释 "auth requied pam_succeed_if.so user != root quiet success"

vim /etc/pam.d/gdm-password
#注释行 "auth requied pam_succeed_if.so user != root quiet success"

reboot

打开阿里云控制台 > 远程连接 > VNC 远程连接 > 第一次需要设置密码，假设我设置为 Meek12，设置后就可以连接上去了
```
