
# TKey 环境

- CentOS 7.5 x64

## 修改 SSH 端口

- 配置文件介绍（记得先备份）：`sudo vim /etc/ssh/sshd_config`
- 打开这一行注释：Port 22
	- 自定义端口选择建议在万位的端口，如：10000-65535之间，假设这里我改为 52221
- CentOS 7：添加端口：`firewall-cmd --zone=public --add-port=52221/tcp --permanent`
	- 重启防火墙：`firewall-cmd --reload`
- CentOS 7 命令：`systemctl restart sshd.service`


## 安装 ansible

- CentOS：`sudo yum install -y ansible`
	- 查看版本：`ansible --version`
- 编辑配置文件：`vim /etc/ansible/hosts`，在文件尾部添加：

```
[local]
172.16.16.4 ansible_ssh_port=52221
```

- 让远程所有主机都执行 `ps` 命令，输出如下

```
ansible all -a 'ps'
```



## 基础设置

- 禁用
    - firewalld
    - selinux
    - swap
- 安装
    - zip unzip lrzsz git wget htop deltarpm 
    - zsh vim
    - docker docker-compose

- 创建脚本文件：`vim /opt/install-basic-playbook.yml`

```
- hosts: all
  remote_user: root
  tasks:
    - name: Disable SELinux at next reboot
      selinux:
        state: disabled
        
    - name: disable firewalld
      command: "{{ item }}"
      with_items:
         - systemctl stop firewalld
         - systemctl disable firewalld
         - echo "vm.swappiness = 0" >> /etc/sysctl.conf
         - swapoff -a
         - sysctl -w vm.swappiness=0
         
    - name: install-epel
      command: "{{ item }}"
      with_items:
         - yum install -y epel-release
         
    - name: install-basic
      command: "{{ item }}"
      with_items:
         - yum install -y zip unzip lrzsz git wget htop deltarpm
         
    - name: install-zsh
      shell: "{{ item }}"
      with_items:
         - yum install -y zsh
         - wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O - | sh
         - chsh -s /bin/zsh root
         
    - name: install-vim
      shell: "{{ item }}"
      with_items:
         - yum install -y vim
         - curl https://raw.githubusercontent.com/wklken/vim-for-server/master/vimrc > ~/.vimrc
         
    - name: install-docker
      shell: "{{ item }}"
      with_items:
         - yum install -y yum-utils device-mapper-persistent-data lvm2
         - yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
         - yum makecache fast
         - yum install -y docker-ce docker-ce-cli containerd.io
         - systemctl start docker.service
         - docker run hello-world
         
    - name: install-docker-compose
      shell: "{{ item }}"
      with_items:
         - curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-Linux-x86_64" -o /usr/local/bin/docker-compose
         - chmod +x /usr/local/bin/docker-compose
         - docker-compose --version
         - systemctl restart docker.service
         - systemctl enable docker.service
```

- 执行：`ansible-playbook /opt/install-basic-playbook.yml`


## 离线安装 jdk

- 下载 jdk 到 /opt 目录下
- 创建脚本文件：`vim /opt/jdk8-playbook.yml`

```
- hosts: all
  remote_user: root
  vars:
    java_install_folder: /usr/local
    file_name: jdk-8u212-linux-x64.tar.gz
  tasks:
    - name: copy jdk
      copy: src=/opt/{{ file_name }} dest={{ java_install_folder }}
      
    - name: tar jdk
      shell: chdir={{ java_install_folder }} tar zxf {{ file_name }}
      
    - name: set JAVA_HOME
      blockinfile: 
        path: /root/.zshrc
        marker: "#{mark} JDK ENV"
        block: |
          JAVA_HOME={{ java_install_folder }}/jdk1.8.0_212
          JRE_HOME=$JAVA_HOME/jre
          PATH=$PATH:$JAVA_HOME/bin
          CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
          export JAVA_HOME
          export JRE_HOME
          export PATH
          export CLASSPATH
    
    - name: source zshrc
      shell: source /root/.zshrc
         
    - name: Clean file
      file:
        state: absent
        path: "{{ java_install_folder }}/{{ file_name }}" 
```


- 执行命令：`ansible-playbook /opt/jdk8-playbook.yml`



## 安装 maven


- 下载 maven 到 /opt 目录下：`wget http://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.zip`
- 创建脚本文件：`vim /opt/maven-playbook.yml`

```
- hosts: all
  remote_user: root
  vars:
    maven_install_folder: /usr/local
    file_name: apache-maven-3.6.1-bin.zip
  tasks:
    - name: copy maven
      copy: src=/opt/{{ file_name }} dest={{ maven_install_folder }}
      
    - name: unzip maven
      shell: chdir={{ maven_install_folder }} unzip {{ file_name }}
      
    - name: set MAVEN_HOME
      blockinfile: 
        path: /root/.zshrc
        marker: "#{mark} MAVEN ENV"
        block: |
            MAVEN_HOME=/usr/local/apache-maven-3.6.1
            M3_HOME=/usr/local/apache-maven-3.6.1
            PATH=$PATH:$M3_HOME/bin
            MAVEN_OPTS="-Xms256m -Xmx356m"
            export M3_HOME
            export MAVEN_HOME
            export PATH
            export MAVEN_OPTS
    
    - name: source zshrc
      shell: source /root/.zshrc
         
    - name: Clean file
      file:
        state: absent
        path: "{{ maven_install_folder }}/{{ file_name }}" 
```


- 执行命令：`ansible-playbook /opt/maven-playbook.yml`


## 安装 node

- 创建脚本文件：`vim /opt/node-playbook.yml`

```
- hosts: all
  remote_user: root
  tasks:
    - name: uninstall-node
      shell: yum remove -y nodejs npm

    - name: curl
      shell: "curl --silent --location https://rpm.nodesource.com/setup_10.x | sudo bash -"
      
    - name: install-node
      command: "{{ item }}"
      with_items:
         - yum -y install nodejs
```


- 执行命令：`ansible-playbook /opt/node-playbook.yml`




