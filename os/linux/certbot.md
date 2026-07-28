
```

已经使用了 Certbot 进行管理证书(必须先配置好域名解析)
sudo apt install certbot python3-certbot-nginx


生成证书
sudo certbot --nginx -d lgai-translate-app.uptmr.net
sudo certbot --nginx -d lgai-translate-page.uptmr.net

生成过程会提示:
Certificate is saved at: /etc/letsencrypt/live/lgai-translate-app.uptmr.net/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/lgai-translate-app.uptmr.net/privkey.pem
Certificate is saved at: /etc/letsencrypt/live/lgai-translate-page.uptmr.net/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/lgai-translate-page.uptmr.net/privkey.pem
Successfully deployed certificate for lgai-translate-app.uptmr.net to /etc/nginx/sites-enabled/default


cd /etc/nginx/conf.d 新增一个配置

sudo systemctl reload nginx


-------------------------------------------------------------------

如果是 openresty 方案


sudo mkdir -p /var/www/certbot/.well-known/acme-challenge
sudo chmod 755 /var/www/certbot
sudo chmod 755 /var/www/certbot/.well-known
sudo chmod 755 /var/www/certbot/.well-known/acme-challenge

vim /usr/local/openresty/nginx/conf.d/frp.conf

server {
    listen 80;
    listen [::]:80;

    server_name xxxx.aaaaaa.com;

    # Certbot HTTP-01 验证
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type text/plain;
        try_files $uri =404;
    }

    # 其他请求跳转 HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

sudo /usr/local/openresty/nginx/sbin/nginx -s reload


验证:
echo 'acme-ok' | sudo tee /var/www/certbot/.well-known/acme-challenge/test

curl -i http://xxxx.aaaaaa.com/.well-known/acme-challenge/test

没问题后删除:
sudo rm -f /var/www/certbot/.well-known/acme-challenge/test

sudo certbot certonly \
  --webroot \
  --webroot-path /var/www/certbot \
  --domain xxxx.aaaaaa.com \
  --email gitnavi@qq.com \
  --agree-tos \
  --non-interactive


会提示: 
Certificate is saved at: /etc/letsencrypt/live/xxxx.aaaaaa.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/xxxx.aaaaaa.com/privkey.pem


然后就可以配置 https 了:

server {
    listen 80;
    listen [::]:80;

    server_name frp.uptmr.net;

    # 必须长期保留，续期还要使用
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type text/plain;
        try_files $uri =404;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;

    server_name frp.uptmr.net;

    ssl_certificate
        /etc/letsencrypt/live/frp.uptmr.net/fullchain.pem;

    ssl_certificate_key
        /etc/letsencrypt/live/frp.uptmr.net/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:18080;

        proxy_http_version 1.1;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}

=================================

查看已安装的证书
sudo certbot certificates


强制立即续期证书
sudo certbot renew --force-renewal


删除证书
sudo certbot delete --cert-name your_domain.com


为新增域名添加证书
sudo certbot --nginx -d new.domain.com
```

