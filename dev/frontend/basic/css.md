
## 基础


-------------------------------------------------------------------

#### 元素默认样式和定制化

- HTML 标签很多都是自带样式的，有的喜欢高度定制化，就需要去掉默认样式自己再写
- [CSS Tools: Reset CSS 常见标签的去掉样式值](https://meyerweb.com/eric/tools/css/reset/)
- [DavidWells/reset.css](https://gist.github.com/DavidWells/18e73022e723037a50d6)
- [yahoo yui3 CSS Reset](https://clarle.github.io/yui3/yui/docs/cssreset/)
- `npm install reset-css`

-------------------------------------------------------------------

#### 选择器

- !important 修饰的样式优先级最高
- id 选择器

- 类选择器
- 属性选择器
- 伪类选择器

- 元素选择器
- 伪元素选择器

- 层级选择器
- 组选择器
- 否定选择器

#### 布局常用样式属性

- width
- height
- background
- border
- padding
- margin
- float

#### 非常用样式属性

- 字体
    - color
    - font-size
    - font-family：字体名称用双引号包裹，如果是字体族是不能用双引号包裹，直接写就行
        - 字体族
            - serif 衬线字体
            - sans-serif 非衬线字体
            - monospace 等宽字体
    - font-weight：粗体
    - font-style：itatic 可以设置斜体
    - text-decoration：下划线
    - text-align
    - text-indent
    - cursor 手型指针
- 行高：
    - line-height
- 背景：
    - 背景颜色
        - 十进制
        - RGB（可以设置透明度）
        - HSL（可以设置饱和度、透明度）
    - 渐变色背景（可以玩出很多花样）：linear-gradient
    - 多背景叠加：background(可以依次用空格隔开写多个背景)
    - 背景图片和属性（雪碧图本质就是 background-position 来调整小图标显示位置，通过 background-size 来调整图标大小）
        - background-repeat: no-repeat;
        - background-position: center top;
        - background-position: 20px 30px;
        - background-size:100px 50px;
    - base64 和性能优化
    - 多分辨率适配
- 边框
    - 线型
    - 大小
    - 颜色
    - 背景图 border-image
    - 边框衔接（可以实现三角形、扇形）：border-bottom、border-top、border-left、border-right
- 滚动
    - 滚动条
    - overflow: visible
    - overflow: hidden
    - overflow: scroll
    - overflow: auto
- 文字折行（文字换行）：比如换行的时候是否把整个单词拆分换行，还是保留单词换行
    - 三种不同方式
    - overflow-wrap（也叫做 word-wrap）
    - word-break
    - white-space
- 粗体
- 斜线
- 下划线



#### CSS 元素溢出

- 当子标签的尺寸超过父标签的尺寸时
- overflow
    - visible
    - hidden
    - auto

#### CSS 显示特性

- display
    - none
    - inline
    - block


#### 盒子模型

- 影响盒子大小
    - width
    - height
    - padding
    - border
- 不影响盒子大小
    - margin

#### 动画






















