---
name: lvsea-kepuvideo
description: 为 Codex 提供中文科普知识视频的可复用 Skill：从主题、文章、网页或脚本建立事实底稿和内容简报，调用 lvsea-writing 做口播化与最后去 AI 味，用 Edge TTS 试听并生成配音与 SRT，依据真实时间轴设计 HyperFrames 分镜，经过预览、局部修订、媒体检查和最终渲染后交付 MP4、字幕、音频与可编辑工程。用户说“使用 lvsea-kepuvideo”、制作 X 秒科普视频、知识讲解视频、主题转视频或文章转科普视频时使用；遇到事实、权限、时长、声音或风格的关键歧义时保留 $grilling 设计树提问。不要用于一次性只写脚本或提示词、手绘/拼贴风、已有口播素材剪辑、产品发布、数字人、或只做字幕的小改。
---

# Lvsea 科普视频

## 目标

把一个中文科普主题或事实材料，推进成一条可核对、可继续编辑、以真实配音时间轴为时钟的知识视频。默认使用 HyperFrames 制作 9:16 竖屏信息动画；默认先做预览，人工确认后再渲染正式 MP4。

这不是“输入主题就盲目生成成片”的黑盒。文章、口播、配音、字幕、分镜、预览和渲染分阶段保存；任何阶段的缺口都停在对应门，不用漂亮的动画掩盖事实错误。

## 触发与边界

**触发词与调用方式**：用户明确说“使用 lvsea-kepuvideo”，或要求从中文主题、文章、网页或脚本制作带配音、SRT、分镜、HyperFrames 预览和 MP4 的科普知识视频时，按本流程执行。

### 应触发

- 用户明确点名 'lvsea-kepuvideo'，并提供主题、文章、网页、脚本或素材。
- 用户要求“制作 X 秒中文科普/知识讲解视频”，并希望从主题或文章走到配音、字幕、分镜和 MP4。
- 用户要求使用 HyperFrames 做知识视频，并需要 'lvsea-writing' 处理口播稿和 AI 模板腔。

### 不应触发

- 只写一份一次性口播稿、视频提示词或分镜清单，不制作视频工程。
- 手绘讲解、半调纸拼贴、产品发布、网站演示、数字人/头像、已有口播素材剪辑或只加字幕。
- 只修一个字幕词、只转码、只做音频清理或只检查一个现有 MP4。

这些邻近任务分别交给已有的通用视频、手绘、拼贴或媒体处理能力；不要为了命中关键词而强行加载本 Skill。

## 输入契约

从用户请求中归一化并写入项目 'brief.md'：

- 主题或来源：URL、文章、文件、脚本、数据或已有素材；
- 目标时长：用户给出的秒数；缺省时采用短知识视频并先确认；
- 目标受众和观看场景：普通公众、学生、制造业现场、管理者等；
- 核心问题：这一条视频只解决什么问题；长视频也按章节围绕一个主问题推进；
- 画幅和平台：默认 9:16、1080×1920、30fps；用户指定优先；
- 语言、声线、字幕方式、视觉方向、CTA 和素材/版权状态；
- 必须保留、不能出现、仍需核实的内容。

缺少小而安全的参数时使用默认值并记录假设。缺少主题、来源、关键事实、受众，或需要公开上传/付费调用却没有授权时，不猜测，进入 'grilling' 决策门。

## 推荐工作流

详细阶段合同见 [references/workflow.md](references/workflow.md)。每一步都保留中间产物，默认按以下顺序执行：

1. **建项目与预检**：创建独立项目目录和 'article.md'、'script.md'、'storyboard.md'、'assets/'、'audio/'、'hyperframes/'、'output/'、'reports/'；检查 Node.js、FFmpeg/ffprobe、HyperFrames 和 'lvsea-writing' 是否可调用。
2. **事实底稿**：读取用户材料；需要时做公开来源研究，保存来源和证据边界。只有主题时先生成 'article.md'，根据时长估算篇幅，再以事实核查为门。
3. **口播稿**：把 'article.md' 改成能直接朗读的 'script.md'。围绕一个核心问题，按目标时长控制密度，保留数字、名称、单位、条件和不确定性。
4. **最后去 AI 味**：这里不再调用原文中的 'humanizer-zh'。调用 '$lvsea-writing' 的视频口播/改稿路径，先保事实和结构，再做成组模式清理、朗读检查、最多两轮定点修订，并把结果写入 'writing-review.md'。具体替换规则见 [references/writing-adapter.md](references/writing-adapter.md)。
5. **试听选声**：默认用 'edge-tts'。从 'script.md' 前 80–120 字生成 3 个同语速试听文件，报告 voice 名称和路径，停下来让用户选择；用户已有授权音频或已指定声线时可跳过试听。
6. **生成配音与时间轴**：用选定声音生成 'audio/voice.mp3' 和 'audio/voice.srt'，用 'ffprobe' 检查实际时长、编码和采样率；SRT 必须覆盖整段音频，后续分镜只能服从这条真实时间轴。
7. **分镜设计**：基于 'script.md' 和 'audio/voice.srt' 生成 'storyboard.md'。每镜头写开始/结束时间、对应口播、画面职责、屏幕文字、动画方式和素材；优先 SVG/HTML/数字/曲线/时间线/对比图，避免只滚字幕和无意义快切。完成后先给用户检查。
8. **HyperFrames 预览**：读取已安装的 HyperFrames 入口及按需的 core、animation、creative、media、CLI 规则；运行 'lint'、'validate'、'inspect'，启动 Studio Preview，不先导出 MP4。
9. **局部修订与正式渲染**：用户指出时间段和问题后，只改指定镜头，保持配音、字幕、其他镜头和总时长不变；完整预览确认后再渲染 'output/final.mp4'，用 'ffprobe' 和视觉抽帧完成最终验收。

## 工具路由

- **写作与去 AI 味**：'$lvsea-writing'；不以规避检测为目标，不使用固定口头禅、错别字或虚构经历。
- **关键歧义与风险决策**：'$grilling'；按它的设计树格式一次提出当前 frontier 的全部问题，给推荐答案，等待用户回答后再推进。事实查找由代理完成，选择和授权由用户决定。
- **画面与渲染**：'$hyperframes' 作为视频制作入口；按需读取 'hyperframes-core'、'hyperframes-animation'、'hyperframes-creative'、'hyperframes-media'、'hyperframes-cli'。没有可用入口或运行环境时，明确缺口，不偷偷换成另一套引擎。
- **音频与媒体检查**：'edge-tts'、'ffmpeg'、'ffprobe'。付费云 TTS、声音克隆、云端上传和未授权素材不作为默认路径。
- **插图**：只在简单图解无法表达时使用用户授权或本地生成素材；记录素材来源、用途和授权状态，不下载来源不明的图片填空。

## 必须停下的门

- 来源打不开、事实冲突、医学/安全/政策等高风险事实无法核对；
- 主题、受众或核心问题会改变稿子方向；
- 需要用户选择声音、视觉风格、公开上传、付费 provider 或声音/素材授权；
- 'article.md'、'script.md'、'voice.srt' 或 'storyboard.md' 未通过当前阶段检查；
- HyperFrames 的 lint/validate/inspect 或最终媒体检查失败。

预览确认、声音选择和用户要求的关键决策不能由默认值替代。普通文件整理、重新运行检查和按已确认范围修复可以连续完成。

## 输出契约

项目至少包含：

~~~text
<project>/
├── brief.md
├── article.md
├── evidence.md
├── script.md
├── writing-review.md
├── assets/
├── audio/
│   ├── sample-1.mp3
│   ├── sample-2.mp3
│   ├── sample-3.mp3
│   ├── voice.mp3
│   └── voice.srt
├── storyboard.md
├── hyperframes/
├── output/
│   └── final.mp4
└── reports/
    ├── preflight.json
    └── final-check.md
~~~

实际交付只报告已经存在并验证的文件；没有 provider 实跑、视觉抽帧或人工预览确认时，标为 'missing evidence'，不称为“已完成成片”。

## 安全边界

- 只读取用户授权的网页、文件和媒体；网页标题或搜索摘要不能替代正文。
- 原始材料、私有脚本、Cookie、Token、声音授权证明和个人信息不写入 Skill 仓库或公开报告。
- 'lvsea-writing' 的“去 AI 味”是事实保真的最后编辑层，不是检测器规避器；不得编造经历、数字、引用、案例或产品能力。
- 默认不上传素材、不调用收费 provider、不克隆真人声音、不发布到社交平台；这些动作必须在任务中明确授权并记录。
- 目标仓库只发布抽象规则、验证脚本和匿名示例，不发布本次项目的文章、音频、视频、截图或临时绝对路径。

## 中文调用示例

- '使用 lvsea-kepuvideo 制作一个 60 秒关于相对论的中文知识视频，9:16，先生成文章和口播稿，声音让我试听选择。'
- '使用 lvsea-kepuvideo 制作一个 300 秒关于膨润土的科普视频，面向制造业管理者，先查证关键事实，再按真实配音时间轴做 HyperFrames 分镜。'
- '使用 lvsea-kepuvideo 把这篇文章做成 90 秒知识视频，保留来源和数字，先让我审脚本和分镜，不要直接渲染。'
- '使用 lvsea-kepuvideo 修改预览中 00:12–00:18 的镜头，只改画面，不改配音、字幕和其他镜头。'

## 维护与验证

包维护时运行：

~~~powershell
python scripts/validate_skill.py .
python scripts/verify_project.py --help
python scripts/verify_video_output.py --help
python <lvsea-zao-skill>/scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
python <lvsea-zao-skill>/scripts/export_skill_ir.py . --output reports/skill-ir.json
python <lvsea-zao-skill>/scripts/context_sizer.py . --output reports/context-budget.json
~~~

本地入口发现还要通过 'Test-SkillInstall.ps1'；公开发布另需分支、秘密扫描、远程版本、Release 和隔离安装证据。静态包验证不能替代实际 HyperFrames provider 运行和人工视频审看。

