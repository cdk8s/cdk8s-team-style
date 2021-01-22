# 运维脚本集合

## 设置免密登录

- 在 A 机器上输入命令：`ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa`
- 生成的密钥目录在：**/root/.ssh**
- 写入：`cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys`
- 测试：`ssh localhost`

## 安装 ansible

- CentOS：`sudo yum install -y ansible`
	- 查看版本：`ansible --version`
- 编辑配置文件：`vim /etc/ansible/hosts`，在文件尾部添加：
- 查看自己的内网 ip：`ifconfig`，假设是：172.16.16.4

```
[local]
172.18.182.155 ansible_ssh_port=22
```

- 让远程所有主机都执行 `ps` 命令，输出如下

```
ansible all -a 'ps'
```

## 先安装 lrzsz

```
yum install -y lrzsz
```

## 按数值顺序执行 playbook

```
mkdir -p /opt/playbook /opt/jar /data/docker/openresty/cert /opt/software
```

- **上传脚本到 /opt/playbook 目录**
- **上传 https 证书到 /data/docker/openresty/cert 目录下**
- **上传软件到 /opt/software/jdk-8u261-linux-x64.tar.gz、/opt/software/apache-maven-3.6.3-bin.zip**
- **配置 jenkins node 节点信息**

```
ansible-playbook /opt/playbook/1-install-basic-playbook.yml
ansible-playbook /opt/playbook/2-jdk8-playbook.yml
ansible-playbook /opt/playbook/3-maven-playbook.yml
ansible-playbook /opt/playbook/4-node-playbook.yml
ansible-playbook /opt/playbook/5-mysql8-playbook.yml
ansible-playbook /opt/playbook/6-redis-playbook.yml
ansible-playbook /opt/playbook/7-jenkins-playbook.yml
ansible-playbook /opt/playbook/8-openresty-playbook.yml
```


## 安装后的检测

```
docker --version && docker-compose --version && java -version && mvn -v && mysql --version && redis-server --version && node -v && npm -v && nginx -V
```
