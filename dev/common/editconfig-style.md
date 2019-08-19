
# 文件 / 代码格式

- 必须采用 editorconfig
- IntelliJ IDEA / WebStorm 自带支持
- 文件本身编码：使用不带 BOM 的 UTF-8 编码（WebStorm 默认就是）

## EditorConfig

- 官网：<https://editorconfig.org/>

## 标准内容

- [.editorconfig](https://github.com/cdk8s/cdk8s-team-style/blob/master/.editorconfig)

```
# http://editorconfig.org
root = true

[*]
indent_style = space
indent_size = 4
charset = utf-8
end_of_line = lf
trim_trailing_whitespace = true
insert_final_newline = true
max_line_length = 300

[*.{groovy,java,kt,kts}]
indent_style = tab
continuation_indent_size = 8

[*.{xml,xsd}]
indent_style = tab

[Makefile]
indent_style = tab

[*.py]
indent_size = 4

[*.js]
indent_size = 4

[*.ts]
indent_size = 4

[*.html]
indent_size = 4

[*.{less,css}]
indent_size = 2

[*.json]
indent_size = 2

[*.{tsx,jsx}]
indent_size = 2

[*.yml]
indent_size = 2

[*.sql]
indent_size = 2

[*.md]
insert_final_newline = false
trim_trailing_whitespace = false
```

