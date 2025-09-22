

## 安装 trojan (只支持 trojan 协议)

- 虽然几年没更新了，但是 2025-09 的时候还是可以用
- <https://github.com/trojan-gfw/trojan/releases>
- 下载 trojan-1.16.0-linux-amd64.tar.xz
- 解压，把 config.json 改为如下内容:

```

{
  "run_type": "client",
  "local_addr": "127.0.0.1",
  "local_port": 1080,
  "remote_addr": "cnsg.1xxxxxxcu(这是你代理的指定节点的URL或者IP)",
  "remote_port": 65300(这是你代理的指定节点的端口),
  "password": [
    "7a663xxxxxx81519(这是你代理的指定节点的密码)"
  ],
  "log_level": 1,
  "ssl": {
    "verify": false,
    "verify_hostname": false,
    "cert": "",
    "cipher": "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:AES128-SHA:AES256-SHA:DES-CBC3-SHA",
    "cipher_tls13": "TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384",
    "sni": "",
    "alpn": [
      "h2",
      "http/1.1"
    ],
    "reuse_session": true,
    "session_ticket": false,
    "curves": ""
  },
  "tcp": {
    "no_delay": true,
    "keep_alive": true,
    "reuse_port": false,
    "fast_open": false,
    "fast_open_qlen": 20
  }
}

```
- 启动 `./trojan -c config.json`
- 另起一个终端测试: `curl --socks5 127.0.0.1:1080 https://ipinfo.io`
- 如果要专为 http 协议，参考本文下面的 `## 转换为 http 代理`

-------------------------------------------------------------------

## 安装(只支持 socket5、SS 协议)

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

-------------------------------------------------------------------

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
