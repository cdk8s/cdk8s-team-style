
# macOS 下 Golang 开发环境


### 下载地址

- Go 语言官网下载地址（需要代理）: <https://golang.org/dl/>
- Go 语言国内镜像站: <https://golang.google.cn/dl/>
- 下载 pkg 安装包，下一步下一步


### 配置环境

- 先查看安装之后默认的环境变量：`go env`

```
GO111MODULE=""
GOARCH="amd64"
GOBIN=""
GOCACHE="/Users/meek/Library/Caches/go-build"
GOENV="/Users/meek/Library/Application Support/go/env"
GOEXE=""
GOFLAGS=""
GOHOSTARCH="amd64"
GOHOSTOS="darwin"
GOINSECURE=""
GOMODCACHE="/Users/meek/go/pkg/mod"
GONOPROXY=""
GONOSUMDB=""
GOOS="darwin"
GOPATH="/Users/meek/go"
GOPRIVATE=""
GOPROXY="https://proxy.golang.org,direct"
GOROOT="/usr/local/go"
GOSUMDB="sum.golang.org"
GOTMPDIR=""
GOTOOLDIR="/usr/local/go/pkg/tool/darwin_amd64"
GCCGO="gccgo"
AR="ar"
CC="clang"
CXX="clang++"
CGO_ENABLED="1"
GOMOD=""
CGO_CFLAGS="-g -O2"
CGO_CPPFLAGS=""
CGO_CXXFLAGS="-g -O2"
CGO_FFLAGS="-g -O2"
CGO_LDFLAGS="-g -O2"
PKG_CONFIG="pkg-config"
GOGCCFLAGS="-fPIC -m64 -pthread -fno-caret-diagnostics -Qunused-arguments -fmessage-length=0 -fdebug-prefix-map=/var/folders/8y/380zy631543177_h1tnpjw580000gn/T/go-build128579891=/tmp/go-build -gno-record-gcc-switches -fno-common"
```

- 我们现在需要调整几个环境变量：`vim ~/.zshrc`
- 目录 /Volumes/two/code-space/go-code 是我自己创建的代码空间

```
# golang
export GOROOT="/usr/local/go"
export GOPATH="/Volumes/two/code-space/go-code"
export GOBIN=$GOPATH/bin
export GO111MODULE=on
export GOPROXY=http://mirrors.aliyun.com/goproxy/,direct
export PATH=$PATH:$GOPATH:$GOBIN:$GOROOT/bin
```

- 目录解释
    - GOROOT 值为GoLang安装目录，一般默认都是 /usr/local/go，可以从 go env 里面看到
    - GOPATH 值为GoLang项目目录。即自己的开发目录，注意：GOPATH不允许与GOBIN一致
    - GOBIN 值为GoLang编译软件使用目录。需要将该环境变量加入PATH环境变量，GOBIN目录一般为GOPATH/bin
    - GO111MODULE 值为on。GoLang模块化加载形式。即vendor目录使用，项目独立开发环境，适用于团队开发。
    - GOPROXY 值为GoLang 模块化形式 加载包时候使用的反向代理地址。必须要配合GO111MODULE一起使用。建议使用阿里云镜像地址https://mirrors.aliyun.com/goproxy/
- GO基本命令
    - run 启动。命令后接启动目录（自动在该目录寻找main包的main函数）或者文件（必须是main包并且有main函数）
    - build 编译文件。命令后接编译目录（自动在该目录寻找main包的main函数）或者文件（必须是main包并且有main函数）。指定编译目录和编译名称，例如：go build -o ./build/foo ./main.go。
    - test 测试模式启动。会扫描目录中的文件名后缀为 test.go的文件，进行测试。
    - env 读取当前环境及常量配置。
    - mod tidy 检查vendor目录包。移除未使用或者失效的包，并且按照配置更新包。
    - mod vendor 将包挪到当前目录下的vendor目录