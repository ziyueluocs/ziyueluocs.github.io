# 学术主页设计预览

为 Ziyue Luo 的学术主页提供十个可交互的本地方案，供确定视觉方向。A 至 C 是第一轮方案，D 至 J 是第二轮新增的七个方向。工作分支为 `codex/academic-homepage-concepts`。

## 打开预览

在仓库根目录运行：

```sh
python3 design-preview/build.py
python3 -m http.server 4173 --bind 127.0.0.1
```

目前已选定 [方案 A · 经典书页](http://127.0.0.1:4173/design-preview/a.html)。其他方向仍可在 [十个方案对比](http://127.0.0.1:4173/design-preview/) 中查看。桌面页面顶部可直接切换 A 至 J，手机使用带完整名称的下拉菜单。

方案 A 的照片采用轻微圆角，桌面为 8px，手机为 6px。Contact 位于身份信息之后、About 之前；暂时使用个人邮箱，显示为普通文字 `luozywh [at] outlook.com`，待用户提供武大邮箱后替换；没有直接发邮件的链接。About 位于个人信息与照片区域下方，与 Research 使用相同的正文宽度。

## 十个方向

| 方案 | 视觉判断 | 内容组织 | 交互 |
| --- | --- | --- | --- |
| A · 经典书页 | 纸白背景、Georgia 衬线姓名、深蓝链接，强调安静的阅读感 | 居中单栏，简介与照片并排，论文按年份排列 | 原生章节跳转、完整作者展开、轻微链接反馈 |
| B · 侧栏档案 | 细浅蓝线条与独立个人栏，强调稳定的信息结构 | 左侧身份与导航，右侧简介、研究和论文；手机改为纵向 | 空间足够时侧栏常驻，较矮窗口与手机使用普通文档流 |
| C · 清浅蓝调 | 很浅的蓝色横向页眉、系统无衬线字体，强调现代感与克制 | 姓名与研究领域先出现，正文用左侧章节标签组织 | 原生链接与锚点，保留浅色和深色主题 |
| D · 大学公报 | 对称衬线刊头、双细线、纸刊式层次 | 简介与研究双栏并排，论文恢复通栏，照片嵌在研究栏 | 手机将双栏顺序展开 |
| E · 极简名片 | 小字号无衬线姓名、小圆形照片、很少装饰 | 窄阅读列，紧凑简介与连续书目 | 导航与论文链接保持直接、轻量 |
| F · 书信手稿 | 暖白纸面、蓝色页边、通篇衬线文字 | 独立信纸式阅读区，姓名采用克制的斜体 | 原生锚点，作者名单可展开 |
| G · 瑞士网格 | 清晰的对齐线、不对称布局、无衬线姓名 | 01 至 04 章节编号配合侧边标签，论文在右侧展开 | 手机保留章节编号并改为单栏 |
| H · 研究索引 | 细线目录与紧凑文字，强调信息密度 | 论文先出现，右侧放个人简介；宽屏将出版信息放独立列 | 窄屏出版信息回到题名下方，简介仍可通过导航访问 |
| I · 论文年鉴 | 衬线年份与浅蓝时间线 | 简介采用左右布局，之后按年份顺序浏览全部论文 | 年份锚点和原生章节跳转 |
| J · 居中人物 | 圆形照片、姓名、个人链接居中，气质温和 | 人物介绍在上方，正文仍左对齐，章节标题居中 | 简单导航、完整作者展开、主题切换 |

多数方案按个人身份与简介、研究方向、全部论文、联系方式排列；H 将论文放在首位，作为结构上的另一个选择。没有添加新闻、项目、奖项或论文精选等未经确认的内容。避免装饰性入场动画、滚动劫持和大幅视觉效果，尊重减少动态效果的系统偏好。

配色是为网页自行调配的近似色，不是 Apple 的官方色值：浅蓝 `#C5D8E8`、淡蓝背景 `#EDF4F9`、深蓝链接 `#355F7F`、正文 `#26343F`。浅蓝用于表面与细线，深蓝承担可读文本。

## 内容来源与维护

- 个人简介和联系信息来自 `_pages/about.md`；文字有轻微精简与语法修正。
- 十版都由 `_pages/publications.md` 生成全部 17 篇论文，保留原作者顺序、题名、出版信息和已有 PDF 链接。30 人作者列表可展开查看。
- 照片直接引用 `assets/img/portrait.jpg`；简历直接引用 `assets/pdf/CV.pdf`。
- Google Scholar、ORCID 和 LinkedIn 来自 `_config.yml`。
- `_data/cv.yml` 是模板示例内容，未使用。
- 根据用户确认，现职更新为武汉大学教授，之前在 OSU 先做博士后、后任 research scientist，与 Ness B. Shroff 和 Jia (Kevin) Liu 合作。学院英文使用武汉大学[官方学院目录](https://en.whu.edu.cn/About/Schools___Departments.htm)中的 School of Cyber Science and Engineering。
- 办公室采用 [Qian Wang 主页](http://nisplab.whu.edu.cn/People.htm)的写法，将房间替换为用户提供的 C509：Room C509, School of Cyber Science and Engineering；下一行是 Wuhan University, Wuhan, China。
- 本科经历按用户指定的 `advised by` 写法补入 Zongpeng Li，名字链接到其[清华大学中文主页](https://www.insc.tsinghua.edu.cn/info/1157/4007.htm)。
- 2026 年论文原有的 “to appear” 状态沿用，未核实论文状态变化。

`build.py` 是生成源，`styles.css` 是原有共享样式，`more-styles.css` 实现 D 至 J 及十方案对比控件，`preview.js` 负责主题偏好、缩略图自适应和手机方案切换。HTML 文件已生成，可直接由普通静态服务器提供。核心学术页面在禁用 JavaScript 时仍可阅读、跳转和展开作者列表，手机方案导航也会退回原生链接。

这十版保留为本地设计记录，不包含在公开发布内容中。选定的方案 A 已迁移到正式模板 `_templates/home.html`，使用 `_data/profile.json` 和 `_pages/publications.md` 维护内容，由 `scripts/build_site.py` 生成站点。正式构建移除了预览控件，并保留 `/publications/`、`/cv/` 兼容入口。后续主页更新以仓库根目录 README 为准。

## 设计参考

查阅日期：2026-09-09。

1. [Jon Barron](https://jonbarron.info/)：简介与肖像并排，窄幅阅读列，蓝色文字链接和连续的研究条目。借鉴信息优先级，不照搬其具体内容和样式。
2. [Deepak Pathak](https://www.cs.cmu.edu/~dpathak/)：联系信息、个人介绍与论文记录组织明确。这里保持原站已有的内容范围。
3. [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines)：采用语义化链接和标题、可见键盘焦点、明确图片尺寸、准确锚点、响应式布局和必要的对比度。Vercel 的品牌风格并非通用学术主页模板。
4. [Vercel Web Design Guidelines Agent Skill](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md)：作为界面审查方法的参考，未安装其命令或额外技能。
5. [Teaching agents product design at Vercel](https://vercel.com/blog/teaching-agents-product-design-at-vercel)：以读者目的来约束设计，并检查最终渲染效果。此处读者的主要目的为了解研究、查找论文和获得联系方式。
6. [Apple iPhone Air](https://www.apple.com/iphone-air/)：Sky Blue 的低饱和浅蓝是配色灵感。学术主页不采用产品营销页的大幅展示与动画。
