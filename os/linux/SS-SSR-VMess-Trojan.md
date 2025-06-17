
## 安装

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

curl https://ipinfo.io
curl --socks5 127.0.0.1:1080 https://ipinfo.io