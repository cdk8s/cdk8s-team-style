
# 常见证书类型

```
x509的证书编码格式有两种
1.PEM(Privacy-enhanced Electronic Mail) 是明文格式的 以 -----BEGIN CERTIFICATE-----开头，已-----END CERTIFICATE-----结尾，中间是经过base64编码的内容,apache需要的证书就是这类编码的证书 查看这类证书的信息的命令为 ：openssl x509 -noout -text -in server.pem
其实PEM就是把DER的内容进行了一次base64编码
2.DER 是二进制格式的证书 查看这类证书的信息的命令为 ：openssl x509 -noout -text -inform der -in server.der

扩展名：
.key 私钥
.crt 即 certificate的缩写，即证书，可以是DER（二进制）编码的，也可以是PEM（ ASCII (Base64) ）编码的 ，在类unix系统中比较常见，与 .DER 格式相同，不保存私钥。可以直接用在 nginx
.csr 是 Certificate Signing Request的缩写，即证书签名请求，这不是证书，可以简单理解成公钥，一般是生成请求以后发送给CA，然后CA会给你签名并发回证书
.key 一般公钥或者密钥都会用这种扩展名，可以是DER编码的或者是PEM编码的 查看DER编码的（公钥或者密钥）的文件的命令为 openssl rsa -inform DER -noout -text -in xxx.key 查看PEM编码的（公钥或者密钥）的文件的命令为 openssl rsa -inform PEM -noout -text -in xxx.key
.cer 证书 常见于Windows系统 编码类型同样可以是DER或者PEM的，windows 下有工具可以转换crt到cer。是证书的公钥，一般都是二进制文件，不保存私钥。
.der 证书，文件是二进制格式，只保存证书，不保存私钥。
.pfx 证书, 二进制格式，同时包含证书和私钥，一般有密码保护。全称 Predecessor of PKCS#12, 是微软支持的私钥格式，二进制格式，同时包含证书和私钥，一般有密码保护。一般用于 Windows IIS 服务器。
.p12 证书，二进制格式，也叫做 PKCS12，同时包含证书和私钥，一般有密码保护。
.jks，二进制格式，同时包含证书和私钥，一般有密码保护。全称 Java KeyStore ，是 Java 的 keytools 证书工具支持的证书私钥格式。jks 包含了公钥和私钥，可以通过 keytool 工具来将公钥和私钥导出。因为包含了私钥，所以 jks 文件通常通过一个密码来加以保护。一般用于 Java 或者 Tomcat 服务器。
.pem，一般是文本格式，可保存证书，可保存私钥。全称是 Privacy Enhanced Mail，格式一般为文本格式，以 -----BEGIN 开头，以 -----END 结尾，中间内容是 BASE64 编码，可保存公钥，也可以保存私钥。有时候会将 pem 格式的私钥改后缀为 .key 以示区别。这种格式的证书常用于 Apache 和 Nginx 服务器，所以我们在配置 Nginx SSL 的时候就会发现这种格式的证书文件。

```

-------------------------------------------------------------------

# mkcert 方案（推荐）

- 支持各个平台
- 官网文档：<https://github.com/FiloSottile/mkcert>

## 生成根证书

- 下载软件: <https://github.com/FiloSottile/mkcert/releases/latest>

```
macOS 选择 darwin-amd64 后缀文件
mv mkcert-v1.4.3-darwin-amd64 mkcert
chmod +x mkcert
mv mkcert /usr/local/bin
查看版本：mkcert -version
当前 2021-06 最新版：1.4.3

将 mkcert 的 CA 根认证机构安装到服务器上
mkcert -install

查看根的 CA 证书位置：mkcert -CAROOT
显示我 macOS 目录如下：/Users/meek/Library/Application Support/mkcert
查看目录下文件：cd /Users/meek/Library/Application\ Support/mkcert && ll 
可以看到就2个文件：
rootCA-key.pem（这个文件不可以分享出去，最核心）
rootCA.pem（这个后续客户端都会用到）

-------------------------------------------------------------------

CentOS 选择 linux-amd64 后缀文件
先安装依赖：yum install nss-tools
mv mkcert-v1.4.3-linux-amd64 mkcert
chmod +x mkcert
mv mkcert /usr/local/bin
其他步骤如 macOS 一样

-------------------------------------------------------------------
Ubuntu
先安装依赖：apt install libnss3-tools
其他跟上面一样
其他步骤如 macOS 一样
```


## 签发证书（生成指定域名证书）

```
接下来有几种签发证书（生成域名证书）方式：
mkcert example.org（注意，这里没有双引号）
生成单域名证书和key,  "example.org.pem" and "example.org-key.pem"

mkcert example.com myapp.dev localhost 127.0.0.1 ::1（注意，这里没有双引号）
生成多域名/ip证书和key,"example.com+4.pem" and "example.com+4-key.pem".

mkcert "*.example.it"
生成泛域名证书,"_wildcard.example.it.pem" and "_wildcard.example.it-key.pem".

因为我这边局域网，有 hosts 映射，所以我这里选择指定域名+ip方式生成：mkcert mytestabcdef.com localhost 192.168.31.207 127.0.0.1 ::1
可以得到两个如下文件：
mytestabcdef.com+4-key.pem
mytestabcdef.com+4.pem
```


## 给 web 服务部署证书

```
这里给 nginx 做证书配置

server {
    # listen            80;
    listen 443 ssl;
    
    ssl_certificate     /usr/share/nginx/html/mytestabcdef.com+4.pem;
    ssl_certificate_key /usr/share/nginx/html/mytestabcdef.com+4-key.pem;
    
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;
    
    
    server_name       192.168.31.207 mytestabcdef.com;

    location / {
      root            /usr/share/nginx/html;
      index           index.html index.htm;
    }
}
```


## 如果是局域网内服务

```
因为 ip 地址不好记，建议大家可以修改 hosts 或者自行搭建 dns 服务器
```

## 各种客户端信任证书方法（重要一步）

```
- Windows 系统
将 rootCA.pem 复制到 windows 上，并将其后缀改为 .crt，双击 rootCA.crt，根据提示安装证书
设置完后重启浏览器（这一步不能少）

- macOS 系统
将 rootCA.pem 复制到 macOS 上，并将其后缀改为 .crt，双击 rootCA.crt，根据提示安装证书
打开 macOS 自带的系统应用 `钥匙串访问`
点击软件左侧的 `系统`，在右侧证书列表中可以找到一个类似这样命名的证书文件：mkcert meek@meekdeiMac-Pro.local
双击这个证书，在弹出框中点击 `信任` 下拉，在使用此证书时，下拉选择 `始终信任`
设置完后重启浏览器（这一步不能少）

- CentOS 系统
安装证书导入工具：yum install -y ca-certificates
cp rootCA.pem /etc/pki/ca-trust/source/anchors/
update-ca-trust

- Ubuntu 系统
安装证书导入工具：apt-get install ca-certificates
mkdir  /usr/share/ca-certificates/selfCA
cp rootCA.pem /usr/share/ca-certificates/selfCA/
echo "selfCA/rootCA.pem" >> /etc/ca-certificates.conf
update-ca-certificates

- Android 系统
把 rootCA.cer 放在 nginx 根目录下，然后手机浏览器访问该文件，比如：https://192.168.31.207/rootCA.cer，浏览器会自动把该 cer 下载下来
我这边以 MIUI 12.5 系统为例，打开：设置 > 密码与安全 > 系统安全 > 加密与凭据 > 安装证书 > CA 证书，对下载证书进行安装
设置完后重启浏览器（这一步不能少）

- iOS 系统
把 rootCA.cer 放在 nginx 根目录下，然后手机浏览器访问该文件，比如：https://192.168.31.207/rootCA.cer，浏览器会自动把该 cer 下载下来
我这边以 iOS 14.6 系统为例，打开：设置 > 通用 > 描述文件，对下载证书进行安装，安装按钮在右上角
接着在：设置 > 通用 > 关于本机 > 证书信任设置，把我们的证书开关打开
设置完后重启浏览器（这一步不能少）

如果不想从系统层面信任，也可以自从电脑浏览器上信任（推荐还是系统层级信任）
firefox导入证书
选项 > 隐私与安全 > 查看证书 > 证书颁发机构
点击对话框中的'导入证书' 选择rootCA.cer,导入完成后
选中刚才导入的证书（mkcert开头的那个）-编辑信任设置，勾选：
此证书可以标识网站
此证书可以标识电子邮件用户
设置完后重启浏览器（这一步不能少）

chrome 导入证书
设置--隐私设置和安全性--管理证书--导入--选择rootCA.cer
设置完后重启浏览器（这一步不能少）
```

-------------------------------------------------------------------

# OpenSSL 方案

## 创建根证书

```
1.生成根证书密钥
cd /etc/pki/CA/
openssl genrsa -out ./private/ca.key 2048

2.生成根证书请求
openssl req -new -in ./private/ca.key -out ca.csr

3.生成根证书
openssl x509 -req -in ca.csr -signkey ./private/ca.key -extensions v3_ca -out ca.crt

```


## 创建中间证书

- 创建中间CA的好处是即使中间CA的私钥泄露，造成的影响也是可控的，我们只需要使用root CA撤销对应中间CA的证书即可

```
#准备环境
mkdir /etc/pki/CA/intermediate
cd /etc/pki/CA/intermediate
mkdir certs crl newcerts private
chmod 700 private
touch index.txt
echo 1000 > serial

#生成密钥
cd /etc/pki/CA
openssl genrsa -aes256 -out intermediate/private/ca.key 2048
#新建请求
openssl req -config intermediate_CA.cnf -sha256 -new -key intermediate/private/ca.key -out intermediate/certs/ca.csr
#签发中间CA证书
openssl ca -config root_CA.cnf -extensions v3_ca -notext -md sha256 -in intermediate/certs/ca.csr -out intermediate/certs/ca.cert
```

## 利用根证书或者中间证书签发客户端证书的步骤如下：

```
mkdir -p /root/ca
1.新建证书密钥（key）
openssl genrsa -out /root/ca/server.key 2048

2.新建证书请求（csr）
注意要和刚才ca证书申请的，信息一致
openssl req -new -in /root/ca/server.key -out /root/ca/server.csr

3.CA签发证书（crt）
openssl x509 -req -in /root/ca/server.csr -CA /etc/pki/CA/ca.crt -CAkey /etc/pki/CA/private/ca.key -CAcreateserial -out /root/ca/server.crt

4.证书有效性验证（crt）
openssl verify -CAfile /etc/pki/CA/ca.crt /root/ca/server.crt

5.不同客户端证书格式转换
# crt,pem 格式证书可用于linux/nginx/node.js 格式客户端
# p12(pkcs12)格式证书用于 tomcat/java/android 客户端
# crt/cer + key 转 pkcs12/pfx/p12 ，需要连同私钥一起导入，需要设置密码
openssl pkcs12 -export -in /root/ca/server.crt -inkey  /root/ca/server.key -out /opt/cert.p12 -name "alias"

JKS 与 p12互转
keytool -importkeystore -srckeystore cert.p12 -srcstoretype PKCS12 -deststoretype JKS -destkeystore cert.jks
keytool -importkeystore -srckeystore cert.jks -srcstoretype JKS -deststoretype PKCS12 -destkeystore cert.p12

```

## 吊销证书

```
#获取要吊销的证书的serial
openssl x509 -in /root/ca/server.crt -noout -serial -subject

#对比serial与subject 信息是否与index.txt中的信息一致
#如果一致，则可以吊销证书
openssl ca -revoke /etc/pki/CA/newcerts/SERIAL.pem

#如果是第一次吊销证书，需要指定吊销的证书编号
echo 01 >/etc/pki/CA/crlnumber

#更新吊销证书列表
openssl ca -gencrl -out /etc/pki/CA/crl.pem

#完成后，可查看吊销的证书列表
openssl crl -in /etc/pki/CA/crl.pem -noout -text
```


## 资料：

- <https://www.jianshu.com/p/7cb5c2cffaaa>
- <https://www.cnblogs.com/zhaobowen/p/13321578.html>
