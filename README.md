# lvsea-kepuvideo

中文科普主题到 HyperFrames 成片的分阶段 Agent Skill：先把事实和口播稿做稳，再用 lvsea-writing 完成最后的自然化编辑，试听 edge-tts 声音，生成真实 SRT 时间轴，按时间轴做 HyperFrames 分镜，预览确认后才渲染 MP4。

它是一个窄入口流程，不是通用剪辑器，也不是 AI 检测规避器。它与 lvsea-video 的区别是：本 Skill 专注从主题/文章开始的知识讲解；与 handdrawn-knowledge-video、gbro-collage-info 的区别是：默认使用 HyperFrames 的 HTML/SVG 信息动画，不固定手绘或拼贴风格；与 presenter/avatar 工作流的区别是：默认无数字人和付费云 provider。

## 安装

从 GitHub 安装：

~~~powershell
npx skills add https://github.com/lhylvsea/lvsea-kepuvideo --skill lvsea-kepuvideo -g -y
~~~

确认安装目录中直接存在 SKILL.md，然后显式调用：

~~~text
使用 lvsea-kepuvideo 制作一个 60 秒关于相对论的中文知识视频，先让我选择声音，预览通过后再渲染。
~~~

## 前置条件

- [ ] Node.js 22+、npm/npx 可用；
- [ ] FFmpeg 与 ffprobe 可用；
- [ ] HyperFrames 入口和所需 domain skills 已安装或本地可调用；
- [ ] lvsea-writing 已可调用；
- [ ] 如使用 edge-tts，Python 包和网络访问可用；
- [ ] 文章、图片、音频、字体和声音均有相应使用权；
- [ ] 不把 Token、Cookie、私有材料或原始项目媒体提交到仓库。

## 你可以这样说

- “使用 lvsea-kepuvideo 制作一个 300 秒关于膨润土的科普视频，面向制造业管理者，先查证事实，再做口播、试听、SRT 和 HyperFrames 分镜。”
- “使用 lvsea-kepuvideo 把这篇文章做成 90 秒 9:16 知识视频，先给我看文章和 script.md，不要直接渲染。”
- “使用 lvsea-kepuvideo 生成三个普通话试听音频，我选完声音再生成完整配音和字幕。”
- “使用 lvsea-kepuvideo 修改预览 00:12–00:18 的画面，只改该镜头，保持音频、字幕和其他镜头不变。”

## 工作流与产物

默认项目目录包含：

~~~text
brief.md -> article.md -> script.md -> writing-review.md
                                  ↓
                    audio/voice.mp3 + voice.srt
                                  ↓
                         storyboard.md
                                  ↓
             hyperframes/ -> preview -> output/final.mp4
~~~

关键停点是：事实底稿、script.md、试听选声、storyboard.md、HyperFrames 预览和最终 QA。遇到关键歧义时调用 $grilling，一次问清当前设计树 frontier 后等待回答；不为普通路径细节制造问卷。

原流程中的 humanizer-zh 已替换为 $lvsea-writing：它先保持事实和专业含义，再做口播化、成组 AI 模式复查、朗读检查和最多两轮定点修订。细则见 references/writing-adapter.md。

## 验证

包维护时运行：

~~~powershell
python scripts/validate_skill.py .
python <lvsea-zao-skill>/scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
python <lvsea-zao-skill>/scripts/export_skill_ir.py . --output reports/skill-ir.json
python <lvsea-zao-skill>/scripts/context_sizer.py . --output reports/context-budget.json
~~~

视频项目阶段验证：

~~~powershell
python scripts/verify_project.py --project <project> --stage script
python scripts/verify_project.py --project <project> --stage audio
python scripts/verify_project.py --project <project> --stage storyboard
python scripts/verify_video_output.py --input <project>\output\final.mp4 --audio <project>\audio\voice.mp3 --expected-width 1080 --expected-height 1920
~~~

入口发现还需通过维护者的 Test-SkillInstall.ps1。静态包门禁、ffprobe 和 HyperFrames 检查不能代替实际 provider 输出质量或人工审看；没有这些证据时报告 missing evidence。

## Troubleshooting

| 问题 | 处理 |
|---|---|
| 来源打不开 | 记录失败原因，要求用户提供正文/文件；不要按标题补写。 |
| edge-tts 不可用 | 报告缺口；只有用户明确选择其他已授权 TTS 才切换。 |
| 声音太长或太快 | 先调整 script 内容和停顿，再以实际 voice.srt 重建分镜；不要硬切句尾。 |
| HyperFrames 校验失败 | 保留失败日志，修复根因后重新 lint/validate/inspect，不跳过检查。 |
| 某镜头不好 | 用时间范围、现象和目标描述局部修改；保持其他镜头和时间轴不变。 |
| 字幕越界/末行孤字 | 按语义手动断行并重新渲染所有相关版本，同步更新 SRT。 |

## 重要边界

本 Skill 不承诺固定时长一定一次生成成功，不自动上传素材、不自动调用付费 API、不克隆真人声音、不自动发布到平台。主题涉及制造安全、健康、政策、金融或真实人物时，事实来源、授权和人工终审优先于画面完成度。

## 来源与许可证

工作流依据 [X 原文流程](https://x.com/yyn1748762/status/2105835330406654424) 整理，并参考 [HyperFrames](https://github.com/heygen-com/hyperframes)、[lvsea-writing](https://github.com/lhylvsea/lvsea-writing)、[lvsea-video](https://github.com/lhylvsea/lvsea-video) 及相邻视频 Skill 的结构；取舍见 reports/。没有复制相邻仓库的完整文件或私有素材。

MIT License，见 [LICENSE](LICENSE)。

