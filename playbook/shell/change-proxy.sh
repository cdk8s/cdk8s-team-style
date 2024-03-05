#!/bin/zsh

# 获取当前默认的 shell
current_shell=$(echo $SHELL)
if [[ "$current_shell" == "/bin/zsh" ]]; then
    echo "当前终端正在使用的是 zsh shell。"
else
    echo "当前终端并非使用 zsh shell，请切换到 zsh 后再执行该脚本。"
    exit 1
fi

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "当前系统是 macOS，可以执行该脚本"
else
    echo "当前脚本只支持 macOS 执行该脚本"
    exit 1
fi

# 设置需要添加的配置
config1='export https_proxy=http://127.0.0.1:7890;'
config2='export http_proxy=http://127.0.0.1:7890;'
config3='export all_proxy=socks5://127.0.0.1:7890;'

enable_proxy() {
    # 添加配置
    if ! grep -Fxq "$config1" ~/.zshrc || ! grep -Fxq "$config2" ~/.zshrc || ! grep -Fxq "$config3" ~/.zshrc
    then
        echo "" >> ~/.zshrc
        echo "$config1" >> ~/.zshrc
        echo "$config2" >> ~/.zshrc
        echo "$config3" >> ~/.zshrc
        echo "已添加需要的配置到 .zshrc 文件。"
    else
        echo "已存在需要的配置，无需添加。"
    fi
}

disable_proxy() {
    # 删除配置，需要转义斜杠
    sed -i '' "/${config1//\//\\/}/d" ~/.zshrc
    sed -i '' "/${config2//\//\\/}/d" ~/.zshrc
    sed -i '' "/${config3//\//\\/}/d" ~/.zshrc
    echo "已删除需要的配置从 .zshrc 文件。"
}

source_config() {
    # 删除配置
    echo "刷新 .zshrc 文件。"
    source ~/.zshrc
}


# 开启命令：./change-proxy.sh on
# 禁用命令：./change-proxy.sh off
if [[ $1 == "on" ]]; then
    enable_proxy
    source_config
elif [[ $1 == "off" ]]; then
    disable_proxy
    source_config
else
    echo "Usage: $0 [on|off]"
fi
