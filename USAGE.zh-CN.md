# 中文使用说明

## 什么时候调用

显式说 使用 lvsea-kepuvideo，或明确要求从一个主题/文章开始制作中文科普知识视频，并且需要配音、SRT、分镜、HyperFrames 预览和 MP4。为了避免与通用 lvsea-video 重叠，本 Skill 不负责已有视频剪辑、手绘/拼贴风、产品发布、数字人和只加字幕任务。

## 最小输入

至少提供：主题、文章/网页/文件中的一种，以及目标时长。最好同时给出受众、平台/画幅、声音偏好、视觉风格和必须保留的事实。只有主题时，Skill 会先做公开研究和事实底稿；不会根据标题、搜索摘要或印象补齐专业结论。

## 默认行为

- 语言：中文；
- 画幅：9:16，1080×1920，30fps；
- 核心内容：一条视频优先解释一个核心问题；300 秒等长视频仍按章节组织，不能把多个无关主题堆在一起；
- 配音：默认 edge-tts，先生成三个 80–120 字试听样本；
- 字幕：以完整配音生成的 voice.srt 为唯一时间轴来源；
- 画面：HyperFrames HTML/CSS/SVG/动画，避免只显示字幕或无意义快切；
- 去 AI 味：最终编辑阶段调用 $lvsea-writing，不使用 humanizer-zh，不以规避检测为目标；
- 决策：声音选择、分镜确认、关键事实和权限问题由用户决定；问题复杂时保留 $grilling。

## 推荐调用

~~~text
使用 lvsea-kepuvideo 制作一个 300 秒关于膨润土的知识视频。
受众：非专业但在制造业工作的管理者。
画幅：9:16。要求：先查证膨润土的基本性质、主要工业用途和使用边界；
先给我看 article.md 和 script.md，口播稿用 lvsea-writing 最后处理，声音先生成 3 个试听，选定后再生成 voice.mp3、voice.srt、storyboard.md，
HyperFrames 先开预览，等我确认后再渲染 final.mp4。
~~~

## 中途的停点

1. article.md：确认主题范围、事实和来源；
2. script.md：确认能否自然念出、时长密度和术语；
3. audio/sample-*.mp3：选择声音；
4. storyboard.md：确认镜头职责、屏幕文字和素材；
5. HyperFrames Studio Preview：检查关键帧、字幕安全区和动画节奏；
6. final-check.md：确认媒体规格、音画、黑帧、溢出和最后一帧。

如果只是重新读取文件、运行检查或按已确认范围修复，可以自动继续；如果会改变主题、受众、核心判断、授权、费用或最终输出格式，进入 $grilling 并等待回答。

## 项目结构

~~~text
brief.md
article.md
evidence.md
script.md
writing-review.md
assets/
audio/sample-1.mp3
audio/sample-2.mp3
audio/sample-3.mp3
audio/voice.mp3
audio/voice.srt
storyboard.md
hyperframes/
output/final.mp4
reports/preflight.json
reports/final-check.md
~~~

## 四个常用场景

### 制造业知识

~~~text
使用 lvsea-kepuvideo 做一个 180 秒关于膨润土在铸造/钻井/环保中的知识视频，
先确认每个用途的事实边界和适用条件，不要把单个企业做法写成行业通用结论。
~~~

### 研究型科普

~~~text
使用 lvsea-kepuvideo 把这篇论文摘要转成 120 秒科普视频，
区分论文直接结论、我的推断和仍需核实的数字，最后再用 lvsea-writing 做口播终稿。
~~~

### 长时长分章

~~~text
使用 lvsea-kepuvideo 制作 600 秒关于安全生产双重预防机制的知识视频，
按“概念—现场例子—流程—常见误区—检查清单”分章，但整条视频保持一个主问题，
每章都使用 voice.srt 的真实时间轴，不要按固定每两秒切镜头。
~~~

### 局部返工

~~~text
使用 lvsea-kepuvideo 检查预览的 00:42–00:58：画面信息太空，
只把这里改成一个对比图和一条时间线；不要改 voice.mp3、voice.srt、字幕内容、总时长和其他镜头。
~~~

## 注意事项

- 目标秒数是规划约束，最终时长以实际配音和渲染文件为准；若超出，应先改稿或调整停顿，不用极端加速掩盖。
- lvsea-writing 只清理真实存在的模板腔、意义膨胀、翻译腔和不适合朗读的句式；不会擅自改变事实、物理/工艺含义、数字和必要术语。
- 原文图片、字体、声音、音乐和人物素材必须记录来源和授权；没有授权时改用抽象图解或本地生成的非事实性装饰。
- 付费 TTS、云端上传、声音克隆和社交平台发布不在默认流程内，必须单独确认。

