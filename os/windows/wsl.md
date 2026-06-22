


```
以管理员身份打开 PowerShell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

重启电脑

理论上速度会很慢:
wsl --install -d Ubuntu

理论上速度会很慢:
wsl --install -d Ubuntu --web-download



打开 https://github.com/microsoft/WSL/releases ，下载最新版 wsl.x.x.x.0.x64.msi（ARM 设备选 arm64），双击安装

wsl --version
wsl --set-default-version 2

从清华镜像下载 Ubuntu WSL 镜像
https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/jammy/ （找 *-wsl-amd64.wsl


wsl --install --from-file "D:\Downloads\ubuntu-22.04.2-wsl-amd64.wsl" --name Ubuntu-22.04 --location "D:\WSL\Ubuntu2204"


wsl -d Ubuntu-22.04
wsl --list --verbose

sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
vim /etc/apt/sources.list

deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse



```