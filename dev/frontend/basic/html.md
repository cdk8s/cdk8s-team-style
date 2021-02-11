
## HTML 基础

- 主推网站：
    - <https://www.w3school.com.cn/h.asp>
    - <https://www.runoob.com/html/html-tutorial.html>
    - <https://www.w3cschool.cn/html/>
    - <https://www.w3schools.com/html/default.asp>
    - <https://whatwg-cn.github.io/html/>
    - <>
    - <>

#### 常见元素

- 按默认样式分（HTML4）
    - block level elements (块级元素)
        - block 元素通常被现实为独立的一块，会单独换一行。块状元素可以相互嵌套，并且可以包裹内联元素。我们常用块状元素包裹大块的内容，比如段落。
        - 常见的块级元素有 div, p, form, table, pre, h1~h6, dl, ol, ul 等。
    - inline elements (内联元素)
        - inline 元素则前后不会产生换行，一系列inline元素都在一行中一个接着一个显示，直到该行排满。
        - 常见的内联元素有 span, a, strong, em, label, input, select, textarea, img, br 等。
    - inline-block
        - 简单来说就是将对象呈现为inline对象，但是对象的内容作为block对象呈现。之后的内联对象会被排列在同一行内。比如我们可以给一个link（a元素）inline-block属性值，使其既具有block的宽度高度特性又具有inline的同行特性
    - 一般来说，可以通过 display:inline 和 display:block、display:inline-block 的设置，改变元素的布局级别。
- 按内容分（HTML5）
    - [kinds-of-content](https://html.spec.whatwg.org/#kinds-of-content)
        - 鼠标移到圈内会展示对应的列表下有哪些标签

-------------------------------------------------------------------

#### 元素嵌套

- block 元素里面可以包含 inline 元素
- block 元素不一定能包含 block 元素
- inline 元素一般不能包含 block 元素
    - 特殊的比如：a 包含 div 是可以（HTML5是合法的）


-------------------------------------------------------------------


#### 常见元素

- 元素（Elements）由于 start tag + content + end tag 组成
- [HTML 标签简写及全称](https://www.runoob.com/html/html-tag-name.html)
- [HTML5/HTML 4.01/XHTML 元素和有效的 DTD](https://www.w3school.com.cn/tags/html_ref_dtd.asp)
- [HTML 参考手册（按字母排序）](https://www.w3school.com.cn/tags/index.asp)
- [HTML 参考手册（按功能排序）](https://www.w3school.com.cn/tags/html_ref_byfunc.asp)


-------------------------------------------------------------------



-------------------------------------------------------------------

#### 元素默认样式和定制化

- HTML 标签很多都是自带样式的，有的喜欢高度定制化，就需要去掉默认样式自己再写
- [CSS Tools: Reset CSS 常见标签的去掉样式值](https://meyerweb.com/eric/tools/css/reset/)
- [DavidWells/reset.css](https://gist.github.com/DavidWells/18e73022e723037a50d6)
- [yahoo yui3 CSS Reset](https://clarle.github.io/yui3/yui/docs/cssreset/)
- `npm install reset-css`

-------------------------------------------------------------------

#### 响应式

- meta Viewport
    - [响应式 Web 设计 - Viewport](https://www.runoob.com/css/css-rwd-viewport.html)
    - [HTML 常用头部标签（meta）](https://www.runoob.com/w3cnote/html-meta-intro.html)
    - [常用meta整理](https://www.runoob.com/w3cnote/meta.html)
    - [Viewport 模板](https://www.runoob.com/w3cnote/viewport-template.html)
    - []()
    - []()
    - []()
    - []()















