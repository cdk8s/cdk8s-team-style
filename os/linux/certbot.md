
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

