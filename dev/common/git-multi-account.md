
# Git多账号体系


## 目的

- 规范不同体系下的账号名称统一，使得不同的项目提交记录信息一致
- 提高提交代码效率

-------------------------------------------------------------------


## 注意说明

- 必须采用 SSH Clone，目前市场上常见仓库都支持 SSH Clone

## 步骤

#### 假设场景

- 我一共有 4 个账号：
    - 在 Github 有 2 个账号，邮箱和账号名分别是：
        - github_1_email@qq.com，github_1_name
        - github_2_email@qq.com，github_2_name
    - 在 Gitee 有 2 个账号，邮箱和账号名分别是：
        - gitee_1_email@qq.com，gitee_1_name
        - gitee_2_email@qq.com，gitee_2_name

#### 生成不同账号的密钥、公钥

- 下面以 macOS 环境为例，Windows 只是生成文件的存放目录不一样而已
- 先切换目录：`cd ~/.ssh`

```
ssh-keygen -t rsa -C "github_1_email@qq.com"
提示你输入名称的时候 Enter file in which to save the key，输入：github_1_rsa
其他不输入，直接回车
```

```
ssh-keygen -t rsa -C "github_2_email@qq.com"
提示你输入名称的时候 Enter file in which to save the key，输入：github_2_rsa
其他不输入，直接回车
```

```
ssh-keygen -t rsa -C "gitee_1_email@qq.com"
提示你输入名称的时候 Enter file in which to save the key，输入：gitee_1_rsa
其他不输入，直接回车
```

```
ssh-keygen -t rsa -C "gitee_2_email@qq.com"
提示你输入名称的时候 Enter file in which to save the key，输入：gitee_2_rsa
其他不输入，直接回车
```

- 这时候你可以在你的 ~/.ssh 目录下看到这几个的 rsa 和 rsa.pub 文件


#### 配置 ssh config 文件


- 创建文件：`vim ~/.ssh/config`，内容如下：

```
host github_1_host
    Hostname github.com
    User github_1_name
    IdentityFile ~/.ssh/github_1_rsa

host github_2_host
    Hostname github.com
    User github_2_name
    IdentityFile ~/.ssh/github_2_rsa

host gitee_1_host
    Hostname gitee.com
    User gitee_1_name
    IdentityFile ~/.ssh/gitee_1_rsa

host gitee_2_host
    Hostname gitee.com
    User gitee_2_name
    IdentityFile ~/.ssh/gitee_2_rsa

```


- 将密钥添加到 ssh-agent 的缓存中：

```
先进入 ssh-agent 交互界面：ssh-agent bash

分别添加：
ssh-add ~/.ssh/github_1_rsa
ssh-add ~/.ssh/github_2_rsa
ssh-add ~/.ssh/gitee_1_rsa
ssh-add ~/.ssh/gitee_2_rsa
```


#### 访问 Github 添加公钥

- 读取下面 2 个 Github 公钥内容，然后把内容复制到 Github 配置
- Github 公钥配置地址：<https://github.com/settings/keys>

```
more ~/.ssh/github_1_rsa.pub
more ~/.ssh/github_2_rsa.pub
```


#### 访问 Gitee 添加公钥

- 读取下面 2 个 Gitee 公钥内容，然后把内容复制到 Gitee 配置
- Gitee 公钥配置地址：<https://gitee.com/profile/sshkeys>

```
more ~/.ssh/gitee_1_rsa.pub
more ~/.ssh/gitee_2_rsa.pub
```



## SSH Clone 项目操作


#### Clone github_1 的项目过程

```
git clone git@github_1_host:github_1_name/tkey-demo.git
```

#### Clone github_2 的项目过程

```
git clone git@github_2_host:github_2_name/tkey-demo.git
```

#### Clone gitee_1 的项目过程

```
git clone git@gitee_1_host:gitee_1_name/tkey-demo.git
```

#### Clone gitee_2 的项目过程

```
git clone git@gitee_2_host:gitee_2_name/tkey-demo.git
```


## 修改 github_1 的项目用户信息（其他类似）

- 第一种，命令方式：

```
git config user.name "github_1_name"
git config user.email "github_1_email@qq.com"
```

- 第二种，修改 /tkey-demo/.git/config 文件：

```
[user]
    name = github_1_name
    email = github_1_email@qq.com
```
