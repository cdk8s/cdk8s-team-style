#!/bin/sh

echo "=================set hostname and timezone================="
hostnamectl set-hostname header1
timedatectl set-timezone Asia/Shanghai
timedatectl set-ntp true

echo "=================Disable SELinux at next reboot================="
setenforce 0 && sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

echo "disable firewalld"
systemctl stop firewalld && systemctl disable firewalld && echo "vm.swappiness = 0" >> /etc/sysctl.conf && swapoff -a && sysctl -w vm.swappiness=0

echo "=================install-base-tool================="
cd /opt/software
unzip centos7.9-base-tool.zip
cd centos7.9-base-tool/
yum localinstall -y *.rpm

echo "=================install-vim================="
cd /opt/software
unzip centos7.9-vim.zip
cd centos7.9-vim/
yum localinstall -y *.rpm

echo "=================install-ansible================="
cd /opt/software
unzip centos7.9-ansible.zip
cd centos7.9-ansible/
yum localinstall -y *.rpm

echo "=================set ssh-keygen================="
ssh-keygen -t rsa -b 2048 -N '' -f ~/.ssh/id_rsa
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
