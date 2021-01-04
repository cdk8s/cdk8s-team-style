
# Flutter 学习过程

- 官网
- 是什么
- 为什么（编年史、版本发布历史）
- 怎么做
- 开发环境搭建
- Hello World
- 包管理
- 常用库、组件
- **核心困难：Android 开发很多依赖包都需要特殊网络才可以下载，这个需要自己准备工具，不然很难跑起来。**

## 官网资料

- Flutter 官网文档：<https://flutter.dev/>
- Flutter 官网安装文档：<https://flutter.dev/docs/get-started/install/macos>

## 视频资料

- Dart 基础
    - <https://www.bilibili.com/video/BV1uz4118767>
    - <https://www.imooc.com/learn/1035>
    - <https://space.bilibili.com/404904528/channel/detail?cid=111585>
- Flutter 基础
    - <https://space.bilibili.com/404904528/channel/detail?cid=123470> 
    - <https://www.bilibili.com/video/BV1pi4y1G7kb> 
    - <https://www.bilibili.com/video/BV1dK4y1f7oF?p=1>
    - <https://www.bilibili.com/video/BV1dK4y1f7oF?p=4>
- Flutter 实战
    - <https://space.bilibili.com/404904528/channel/detail?cid=106755>
    - <https://www.bilibili.com/video/BV1ZK4y1s759>

## macOS 下的环境搭建

- xcode、Command Line Tools for Xcode 下载地址：<https://developer.apple.com/download/more/>
- 苹果官网下载 xip 压缩格式文件，双击解压（文件大，很占用 CPU 请等待），解压出来的 Xcode.app 拖动到 Application 中即可
- 安装 Xcode 命令行工具：

```
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
```

- 还需要安装：`brew install cocoapods`
- Flutter 国内特殊下载 SDK 下载地址：<https://flutter.cn/docs/development/tools/sdk/releases>
- Flutter SDK 是一个 zip 包，解压下，假设我解压路径是：/Users/gitnavi/software/flutter_sdk/flutter
- 然后我配置环境变量

```
vim ~/.zshrc

export PATH=$PATH:/Users/gitnavi/software/flutter_sdk/flutter/bin

source ~/.zshrc

dart --version
pub --version
flutter --version
会显示 flutter 版本，dart 版本，第一次使用会很慢展示出来
这里要注意 dart 版本

flutter doctor
会提示你需要用到个版本 xcode，要安装什么插件等等
```

- Flutter 国内特殊镜像源说明：<https://flutter.cn/community/china>

```
vim ~/.zshrc

export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn

source ~/.zshrc
```

## 配置 Dart SDK

- 虽然 Dart SDK 已经在捆绑在 Flutter 里了，可以不需要单独安装 Dart，但是这里还是推荐安装下，方便 IDE 对 Dark 语法更好的支持。
- 官网地址：<https://github.com/dart-lang/sdk/releases>
- 国内别人提供的地址：<https://www.dartcn.com/tools/sdk/archive/>

```
# dart sdk
DART_HOME=/Users/youmeek/software/dart/2.8.4/dart-sdk
PATH=$PATH:$DART_HOME/bin
export DART_HOME
export PATH
```


## 配置 Android Studio

- 下载 Android Studio：<https://developer.android.google.cn/studio?hl=zh-cn>
- 打开 Android Studio 安装 SDK、AVD（模拟器）
- 打开 Android Studio 的 SDK 设置：先取消勾选：Hide Obsolete Packages，然后选择 SDK Tools 》Android SDK Tools (Obsolete)
- 设置 Android 变量，这里已经假设了你前面安装 Android Studio 已经安装好了 SDK，也安装了模拟器。并且 Android Studioo 也告诉了你 SDK 的安装路径了

```
vim ~/.zshrc

export ANDROID_HOME="/Users/gitnavi/Library/Android/sdk"
export NDK_ROOT="/Users/gitnavi/Library/Android/sdk/ndk-bundle"
export PATH=${PATH}:${ANDROID_HOME}/emulator
export PATH=${PATH}:${ANDROID_HOME}/tools
export PATH=${PATH}:${ANDROID_HOME}/platform-tools

source ~/.zshrc
```

- Android Studio 安装必备插件
    - Dart
    - Flutter


## Hello World

- 假设你已经在 Android Studio 上安装好了 Flutter 插件之后
- 重启 Android Studio 之后可以直接通过向导方式创建 Flutter 项目。


## 常用库、组件

- 官网库：<https://pub.dev>
- 国内包搜索站：<https://pub.flutter-io.cn/>

## 常用命令

```
flutter packages get

flutter run
flutter -v run
flutter run -d devices_id
flutter run -d all

flutter emulators
flutter emulator --launch apple_ios_simulator

flutter build apk
flutter build apk --release --target-platform android-arm64
```