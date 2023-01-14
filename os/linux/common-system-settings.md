
## 基础操作

```
查看 Linux 內核、Debian 系统版本
cat /proc/version
Linux version 5.18.0-kali5-amd64 (devel@kali.org) (gcc-11 (Debian 11.3.0-3) 11.3.0, GNU ld (GNU Binutils for Debian) 2.38) #1 SMP PREEMPT_DYNAMIC Debian 5.18.5-1kali6 (2022-07-07)

强制使用简单密码：
终端输入：
openssl passwd -6 -salt $(< /dev/urandom tr -dc '[:alnum:]' | head -c 32)
输入新密码，比如：aa
得到：
$6$utqcYT2jklngQCW6$2FtCAFKwn1uq6z.VLRiI9KOmVujNJFyh8gnn3Uhzg5ZoJrat/4.nxZySYow20HegwC3muCduq1ov0RYtjPJQx0

修改配置：sudo vim /etc/shadow
把这一行注释：#meek:$y$j9T$7q2qN9sc7QZV.X2QV4XRm0$ZapMUSZuF3W..Z5h99EbL.E8vCXWV.3GGwNemJK.zsA:19301:0:99999:7:::
改为这个新密码：meek:$6$utqcYT2jklngQCW6$2FtCAFKwn1uq6z.VLRiI9KOmVujNJFyh8gnn3Uhzg5ZoJrat/4.nxZySYow20HegwC3muCduq1ov0RYtjPJQx0:19301:0:99999:7:::


安装的时候是没有让你设置 root 密码的，所以先设置 root 密码
sudo passwd root


开启远程 SSH：
vim /etc/ssh/sshd_config
该值改为：PasswordAuthentication yes
保存

service ssh start  重启
service ssh status  状态是否正常运行
update-rc.d ssh enable 添加开机启动

```

