# OpenResty 安装和配置

## 部署的环境

- 系统：`CentOS 7.4`
- 硬件要求：`1 GB RAM minimum`
- ip：`http://192.168.1.121`
- docker version：`17.12.1-ce, build 7390fc6`

## CentOS 包安装

```
sudo yum install yum-utils
sudo yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo
sudo yum install -y openresty

默认安装在：
/usr/local/openresty
```

## 配置

```
新增环境变量：
vim ~/.zshrc

export PATH=${PATH}:/usr/local/openresty/bin
export PATH=${PATH}:/usr/local/openresty/nginx/sbin

source ~/.zshrc

创建配置文件：
nginx -c /usr/local/openresty/nginx/conf/nginx.conf

刷新配置文件：
nginx -s reload

mkdir /usr/local/openresty/nginx/conf.d

```

## 推荐的 nginx.conf 配置内容


```
worker_processes  1;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;


    sendfile        on;

    keepalive_timeout  65;

    gzip on;
    gzip_buffers 8 16k;
    gzip_min_length 512;
    gzip_disable "MSIE [1-6]\.(?!.*SV1)";
    gzip_http_version 1.1;
    gzip_types   text/plain text/css application/javascript application/x-javascript application/json application/xml;
    client_max_body_size 20m;

    limit_req_zone $binary_remote_addr zone=contentRateLimit:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=perIpLimit:10m;
    limit_conn_zone $server_name zone=perServerLimit:10m;

    include /usr/local/openresty/nginx/conf.d/*.conf;

}
```



## 限流配置

- 核心思路
    - 如果作为代理服务器，我们需要限制每个用户的请求速度和链接数量，但是，由于一个页面有多个子资源，如果毫无选择的都进行限制，那就会出现很多不必要的麻烦，如：一个页面有40个子资源，那么如果想让一个页面完整的显示，就需要将请求速度和连接数都调整到40，以此达到不阻塞用户正常请求，而这个限制，对服务器性能影响很大，几百用户就能把一台nginx的处理性能拉下来。
    - 所以我们需要制定哪些请求是需要进行限制的，如html页面；哪些是不需要限制的，如css、js、图片等，这样就需要通过配置对应的location进一步细化。
    - 我们不对css、js、gif、png，jpg等进行连接限制，而对除此之外的链接进行限制
    - 一般我们是请求频率限制 + 连接频率限制一起使用

```
worker_processes      1;

events {
  worker_connections  1024;
}

http {
  include             mime.types;
  default_type        application/octet-stream;

  sendfile on;

  keepalive_timeout   65;

  # 请求频率限制
  # $binary_remote_addr 针对的IP地址作为参照物
  # zone=contentRateLimit:10m  设置一个桶 桶的名字 contentRateLimit 并且分配10M容量。
  # rate=5r/s; 设置每秒钟处理多少个请求 5个请求每秒。
  limit_req_zone $binary_remote_addr zone=contentRateLimit:10m rate=5r/s;
  
  # 连接频率限制
  #存储个人请求Ip的连接限流容量
  limit_conn_zone $binary_remote_addr zone=perIpLimit:10m;
  #整个location对应请求的总的连接并发容量配置
  limit_conn_zone $server_name zone=perServerLimit:10m;

  server {
    listen            80;
    server_name       localhost 127.0.0.1 119.29.67.40;

    location / {
        ##表示每个IP的最大并发连接数为3
        limit_conn perIpLimit 3;

        #限制当前Location总的连接数，超过的请求会被拒绝。这里为了方便简单测试，所以设置为 5，一般这个可以设置我 100，1000 左右的值
        limit_conn perServerLimit 5;

        #burst=5，相当于设置一个大小为5的缓冲区，超过了访问频次的请求会先放到这个缓冲区中等待。
        #但是这个缓冲区大小只有5，超过缓冲区的请求会直接503
        #nodelay是无延迟的意思，表示请求超过频次时，可提供处理(burst + rate)个请求的能力
        #请求超过（burst + rate）的时候就会直接返回503，永远不存在请求需要等待的情况。
        #注意：不存在单独使用nodelay的情况。nodelay是和burst配合使用的
        limit_req zone=contentRateLimit burst=5 nodelay;

        root            /usr/local/openresty/nginx/html;
        index           index.html index.htm;
    }
  }
}
```

## 资料

- <https://my.oschina.net/u/4314104/blog/3584373>