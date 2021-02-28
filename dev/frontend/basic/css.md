
## 基础


-------------------------------------------------------------------

#### 常量

- 一般浏览器默认的字体大小为 16px
- 如果字体大小是16px，那么1em=16px。

#### 盒子模型

- 影响盒子大小
    - width
    - height
    - padding
    - border
- 不影响盒子大小
    - margin
- display
    - display: block;
    - display: inline;
    - display: inline-block;
- position
    - position: static;
    - position: relative; 相对
    - position: absolute; 绝对，但是是相对于最近的父级的 absolute 或 relative，如果父级都不是这个定位，就相对 body
    - position: fixed; 绝对，
    - z-index 折叠顺序，只有 relative、absolute、fixed 有效
- float 浮动元素（国内很常用，因为兼容低端浏览器好），它的浮动块对其他元素不会影响，但是对里面的文字有影响，不会漂浮在文字上。
- flexbox 真正意义上新时代的布局
- 响应式
    - 设计考虑：哪些可以隐藏、折行、自适应空间
    - rem / viewport / @media（media queries）

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
    - max-width
    - min-width
- height
    - max-height
    - min-height
- background
- border
    - border: 20px solid; 一般除了写大小，还要写上是直线、虚线才有作用。边框默认的颜色是跟里面的元素颜色一样，一般也要设置颜色
    - border-width
    - border-color
    - border-style
    - border-top
    - border-bottom
    - border-left
    - border-right
- padding
- margin
- float

#### 非常用样式属性

- 字体
    - color
        - 十六进制
        - RGB（可以设置透明度）
        - RGBA（可以设置透明度）
        - HSL（可以设置饱和度、透明度）
    - font-size
    - font-family：字体名称用双引号包裹，如果是字体族是不能用双引号包裹，直接写就行
        - 字体族
            - serif 衬线字体
            - sans-serif 非衬线字体
            - monospace 等宽字体
            - cursive
            - fantasy
    - font-weight：粗体
        - 由于受大部分字体限制，几百的数值显示出来的粗体差异不大
        - normal 等同于 400，bold 等同于 700 的值
    - font-style：
        - normal 正常
        - italic 斜体
        - oblique 倾斜（和 italic 看起来差别不大）
    - text-align 设置元素内文本的水平对齐方式（只对块元素有效）
        - left
        - right
        - center
        - justify 两端对齐
    - vertical-align 设置元素内容的垂直方式（只对行元素有效，比较少用）
        - 单行文字水平、垂直居中：
            - line-height: 400px;（一般是父元素容器的 height 是多少值，这个就多少值）
            - text-align: center; 
        - 多行文字水平、垂直居中：
            - vertical-align: middle;
            - display: table-cell;（父元素容器要设置 display: table;）
            - text-align: center; 
    - text-decoration：下划线
        - underline 下换线
        - overline 上划线
        - line-through 贯穿性
        - blink 
        - none
    - text-indent 将段落的第一行缩进多少单位，推荐使用 em 作为单位。
    - cursor 手型指针
- 行高：
    - line-height（行与行之间的距离）
    - line-height 不能用 px 为单位，不然要搭配 font-size 一起使用。推荐使用 em（最常用） 或者 100% 作为单位。
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
- 单词之间的间距：word-spacing
- 字母之间的间距：letter-spacing
- 文本的大小写：text-transform
    - capitalize 首字母大写
    - uppercase 全部大写
    - lowercase 全部小写
    - none
- 背景：
    - 背景颜色：background-color
        - transparent 透明，没有颜色
        - 十六进制
        - RGB（可以设置透明度）
        - RGBA（可以设置透明度）
        - HSL（可以设置饱和度、透明度）
    - 渐变色背景（可以玩出很多花样）：linear-gradient
    - 多背景叠加：background(可以依次用空格隔开写多个背景)
    - 背景图片（background-image）和属性（雪碧图本质就是 background-position 来调整小图标显示位置，通过 background-size 来调整图标大小）
        - background-repeat: no-repeat; 不重复
        - background-repeat: repeat; 重复
        - background-repeat: repeat-x; 水平重复
        - background-repeat: repeat-y; 垂直重复
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


#### CSS 元素溢出

- 当子标签的尺寸超过父标签的尺寸时
- overflow
    - visible
    - hidden
    - auto

#### CSS 显示特性

- display
    - none
    - inline：元素显示为内联元素（行内元素），元素前后没有换行符
        - 此样式下：width、height 属性无效
        - 此样式下：margin-top、margin-bottom、padding-top、padding-bottom 属性无效
        - 此样式下：margin-left、margin-right、padding-left、padding-right 属性有效
    - block：元素显示为块级元素，元素前后有换行符
        - 此样式下：width、height、margin、padding 属性有效
    - inline-block：行内块元素。元素呈现为 inline，但是具有 block 特性
        - 主要是我们想让一个块元素一直水平排序，并且超过了换行继续显示
- float 浮动元素
    - 默认块元素是换行显示的，但是可以通过添加 float 属性，实现水平行显示效果
    - float: left
    - float: right
    - float: none
    - float: inherit 继承浮动
    - 
    - 
    - 
    - 


#### 动画






















