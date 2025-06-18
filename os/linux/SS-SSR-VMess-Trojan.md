
## 安装(只支持 socket5)

sudo apt install shadowsocks-libev

## 配置

vim ~/shadowsocks.json

```
注意: 标注有服务商的代表这个是服务商的连接信息，而不是节点的信息。
节点这里只要有 ip 或域名即可

{
    "server": "你的节点IP或域名",
    "server_port": 24991(服务商),
    "local_port": 1080,
    "password": "VPadM132134m(服务商)",
    "timeout": 300,
    "method": "chacha20-ietf-poly1305(服务商)",
    "mode": "tcp_and_udp",
    "plugin": "",
    "obfs": "plain"
}
```

## 启动

ss-local -c ~/shadowsocks.json
nohup ss-local -c ~/shadowsocks.json > ~/ss-local.log 2>&1 &

## 测试

没代理前:
curl https://ipinfo.io

代理后:
curl --socks5 127.0.0.1:1080 https://ipinfo.io


## 转换为 http 代理

sudo apt install -y privoxy
sudo cp /etc/privoxy/config /etc/privoxy/config.backup.20250617

sudo vim /etc/privoxy/config
```
最后一行添加:
forward-socks5t / 127.0.0.1:1080 .
```

sudo systemctl restart privoxy
sudo systemctl start privoxy
sudo systemctl status privoxy

没代理前，访问失败
curl https://www.google.com

代理后:
curl --proxy http://127.0.0.1:8118 https://ipinfo.io

-------------------------------------------------------------------

vim ~/.bashrc
全局设置环境变量(方案一):
export http_proxy=http://127.0.0.1:8118
export https_proxy=http://127.0.0.1:8118
export ftp_proxy=http://127.0.0.1:8118
unset all_proxy

全局设置环境变量(方案二):
注意:(socks5h:// 表示域名解析也通过代理，而 socks5:// 则是本地解析域名。)
unset http_proxy
unset https_proxy
unset ftp_proxy
export all_proxy=socks5h://127.0.0.1:1080

以上方案你只能选一个实验，哪个有效用哪个。

使用完代理之后，要注释掉这些配置，并 source ~/.bashrc，并且还要重新连上一个新会话的终端这样才可以被重置
