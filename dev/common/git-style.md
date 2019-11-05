
# Git 风格

- **基于 IntelliJ IDEA / WebStorm**
- 只有当 IDE 完成不了的功能才可以使用命令行

## Git 仓库项目名

- 复词使用中划线隔开，例如：`tkey-demo`

## 版本号

- 采用：[Semantic Versioning（简称 SemVer）](https://semver.org/)
- 总格式：v1.1.0 = 主版本号.小版本.修订号
- 主版本号：不考虑向下兼容，开发新特性
- 小版本：考虑向下兼容，开发新特性
- 修订号：考虑向下兼容，修复bug

## 场景修饰

- 里程碑（milestone）：v1.1.0.M1
- 预览版（release candidate）：v1.1.0.RC1
- 正式版（release）：v1.1.0.RELEASE

## Git 命名

- Branch
    - master
    - release
    - test
    - dev
    - feature-add-user
    - hotfix-1.1.2-20190809-3
    - dev-1.1.2
    - test-1.1.2
    - release-1.1.2
- Tags
    - v1.1.0.M1
    - v1.1.0.RC1
    - v1.1.0.RELEASE
- commit 前缀规范：采用 Angular 的规范：<https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit>

```
build: Changes that affect the build system or external dependencies (example scopes: maven, gradle, gulp, broccoli, npm)
ci: Changes to our CI configuration files and scripts (example scopes: Circle, BrowserStack, SauceLabs)
docs: Documentation only changes
feat: A new feature
fix: A bug fix
perf: A code change that improves performance
refactor: A code change that neither fixes a bug nor adds a feature
style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
test: Adding missing tests or correcting existing tests
```

- 每改一个独立功能 commit 一次，别写了一堆功能再一次 commit，到时候做提交的代码检查会死人
- 比如：

```
docs: 更新 Git 规范
feat: 新增简化模式
```

## Gitflow 工作流

- [点击查看](https://github.com/judasn/IntelliJ-IDEA-Tutorial/blob/master/vcs-introduce.md#git-flow-%E7%9A%84%E4%BB%8B%E7%BB%8D)
