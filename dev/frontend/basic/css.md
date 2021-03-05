
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


## flex 布局

- 配图资料：
    - 通过游戏练习：<http://flexboxfroggy.com/#zh-cn>
    - <https://juejin.cn/post/6844903474774147086>
    - <https://www.zhangxinxu.com/wordpress/2018/10/display-flex-css3-css/>
    - <https://juejin.cn/post/6897121569945223176>
    - <>
- 整体知识点
    - 在Flex布局中，flex子元素的设置float，clear以及vertical-align属性都是没有用的。
    - 有 main axis（主轴）、cross axis（交叉轴）的概念，并且这个很重要，是核心、基础
    - 当主轴是水平布局的时候，交叉轴就是垂直布局
    - 当主轴是垂直布局的时候，交叉轴就是水平布局
    - 所以，主轴不是说就一定是水平布局的，这是核心点
- 思路：
    - 主轴方向 flex-direction
    - 主轴对齐方式 justify-content
    - 有没有换行的需求 flex-wrap
    - 交叉轴方向 align-items（单行） 或 align-content（换行）
- 游戏第 24 题答案：<http://flexboxfroggy.com/#zh-cn>

```
flex-direction: column-reverse;
justify-content: center;
flex-wrap: wrap-reverse;
align-content: space-between;
```

-------------------------------------------------------------------


- 父容器
- 给 div 这类块状元素元素设置 display:flex 或者给 span 这类内联元素设置 display:inline-flex

```
flex-direction 决定主轴的方向，是水平布局，还是垂直布局
flex-direction: row（水平，常用） | row-reverse | column（垂直，常用） | column-reverse;

flex-wrap 用来控制主轴子项整体单行显示还是换行显示。默认不换行，会平分所有的子元素的宽度，所以如果子元素有设置宽度也是没用的。
flex-wrap: nowrap（常用） | wrap（常用）| wrap-reverse（反向换行）;

flex-flow：flex-direction 和 flex-wrap 的简写形式
flex-flow：row wrap;

justify-content 决定在主轴上的对齐方式
justify-content: flex-start（默认，常用） | flex-end | center（常用） | space-between（常用） | space-around | space-evenly（常用）;
flex-start（默认值）：左对齐
flex-end：右对齐
center： 居中
space-between：两端对齐，项目之间的间隔都相等。
space-evenly: 每个 item 的间距相等。（相比 space-around 看起来会更加自然，所以比较会常用）
space-around：每个项目两侧的间隔相等。所以，项目之间的间隔比项目与边框的间隔大一倍

align-items 用于控制交叉轴方向（当是单行的时候）
align-items: stretch | flex-start | flex-end | center | baseline;
flex-start：交叉轴的起点对齐。
flex-end：交叉轴的终点对齐。
center：交叉轴的中点对齐。
baseline: 项目的第一行文字的基线对齐。
stretch（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度。

align-content 用于控制交叉轴方向（当有换行的时候）
align-content: stretch | flex-start | flex-end | center | space-between | space-around | space-evenly;
flex-start：与交叉轴的起点对齐。
flex-end：与交叉轴的终点对齐。
center：与交叉轴的中点对齐。
space-between：与交叉轴两端对齐，轴线之间的间隔平均分布。
space-around：每根轴线两侧的间隔都相等。所以，轴线之间的间隔比轴线与边框的间隔大一倍。
stretch（默认值）：轴线占满整个交叉轴。


```
-------------------------------------------------------------------


- 子元素（子项）

```
前置知识：
指定某个具体元素可以用 id 选择器，还可以用伪类加上下标的方式，下标从1开始：.mySpan:nth-child(2)，还可以用表达式，常见的伪类还有：
tr:nth-child(2n+1)
表示HTML表格中的奇数行。
tr:nth-child(odd)
表示HTML表格中的奇数行。
tr:nth-child(2n)
表示HTML表格中的偶数行。
tr:nth-child(even)
表示HTML表格中的偶数行。
span:nth-child(0n+1)
表示子元素中第一个且为span的元素，与:first-child 选择器作用相同。
span:nth-child(1)
表示父元素中子元素为第一的并且名字为span的标签被选中
span:nth-child(-n+3)
匹配前三个子元素中的span元素。


flex-grow 规定在空间允许的情况下，子元素如何按照比例分配可用剩余空间。如果所有的子元素的属性都设定为1，则父元素中的剩余空间会等分给所有子元素。如果其中某个子元素的flex-grow设定为2，则在分配剩余空间时该子元素将获得其他元素二倍的空间（至少会尽力获得）
默认值为0，意味着即使有剩余空间，各子元素也不会放大。

flex-shrink 如果空间不足就缩小，flex-shrink默认值为1， 当所有子元素都为默认值时，则空间不足时子元素会同比例缩小。如果其中某个子元素的flex-shrink值为0，则空间不足时该子元素并不会缩小。如果其中某个子元素的flex-shrink值为2时，则空间不足时该子元素会以二倍速度缩小。

flex-basis 设置基准大小，当主轴为 x 是，flex-basis 设置的大小为宽度，并且会覆盖 width 值，当主轴为 y 是，flex-basis 设置的大小为高度，并且会覆盖 hegiht 值

flex：flex-grow, flex-shrink, flex-basis的缩写

align-self 控制单独某一个flex子项的垂直对齐方式。默认值为auto，表示继承父元素的align-items属性，如果没有父元素，则等同于stretch
align-self: auto | flex-start | flex-end | center | baseline | stretch;
auto: 默认值，表示继承父元素的 align-items 属性
flex-start：交叉轴的起点对齐。
flex-end：交叉轴的终点对齐。
center：交叉轴的中点对齐。
baseline: 项目的第一行文字的基线对齐。
stretch（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度。

order 设置order改变某一个flex子项的排序位置，数值越小越靠前，默认值为0

```

-------------------------------------------------------------------

- 水平、垂直居中

```
.parent {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

-------------------------------------------------------------------

- 两列布局：左边固定，右边自适应

```
.parent {
  display: flex;
  justify-content: center;
}

.left {
  width: 100px;
}

.right {
  flex-grow: 1;
}

```

- 两列布局：左边不固定，右边自适应

```
.parent {
  display: flex;
}
.right {
  flex-grow: 1;
}
```


- 三列布局：左边固定，中间自适应，右边固定

```
.parent {
  display: flex;
}
.left {
  width: 100px;
}
.middle {
  flex-grow: 1;
}
.right {
  width: 100px;
}
```

- 九宫格布局

```
.parent {
  display: flex;
  flex-wrap: wrap;
}

.child {
  width: calc(calc(100% / 3) - 10px);
  margin: 5px;
  height: 100px;
  background-color: #fda085;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}
```



-------------------------------------------------------------------


- 不同宽度的时候采用不同的样式

```
/* 大屏 */
.navigation {
  display: flex;
  flex-flow: row wrap;
  /* 这里设置对齐主轴方向的末端 */
  justify-content: flex-end;
}

/* 中屏 */
@media all and (max-width: 800px) {
  .navigation {
    /* 当在中屏上，设置居中，并设置剩余空间环绕在子元素左右 */
    justify-content: space-around;
  }
}

/* 小屏 */
@media all and (max-width: 500px) {
  .navigation {
    /* 在小屏上，我们不在使用行作为主轴，而以列为主轴 */
    flex-direction: column;
  }
}
```

















