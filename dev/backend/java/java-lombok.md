
# Lombok 介绍

- 官网：<https://projectlombok.org/features/all>

## 依赖

- 项目 Maven 引入依赖
- Maven 仓库地址：<https://search.maven.org/search?q=g:org.projectlombok%20AND%20a:lombok&core=gav>

```
<dependency>
	<groupId>org.projectlombok</groupId>
	<artifactId>lombok</artifactId>
	<version>1.18.8</version>
	<scope>provided</scope>
</dependency>
```

## IntelliJ IDEA 支持

- IntelliJ IDEA 安装插件，在插件库中搜索：`Lombok Plugin`
- IntelliJ IDEA 配置路径：`Settings | Build, Execution, Deployment | Compiler | Annotation Processors`
    - 勾选：`Enable annotation processing`


## POJO 必须有的注解

```
@Getter
@Setter
@ToString
```

## 日志注解

- 必须使用 `@Slf4j`


## 其他材料

- <https://projectlombok.org/features/all>
- <http://blog.didispace.com/java-lombok-1/>
- <http://blog.csdn.net/sunsfan/article/details/53542374>
- <http://codepub.cn/2015/07/30/Lombok-development-guidelines/>





