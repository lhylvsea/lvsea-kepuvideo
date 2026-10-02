# QA、权限与证据边界

## 依赖预检

完整执行前只检查实际需要的依赖：

| 能力 | 检查 | 缺失处理 |
|---|---|---|
| Python | python --version | 无法运行脚本时报告，不改用隐藏环境 |
| Node/npm | node --version、npm --version | HyperFrames 无法启动则停在项目预检 |
| FFmpeg/ffprobe | ffmpeg -version、ffprobe -version | 不生成“已验证”的成片 |
| HyperFrames | npx hyperframes doctor 或项目已有 CLI | 只做前置产物，说明不能渲染 |
| edge-tts | python -m edge_tts 或 edge-tts --help | 等待用户授权替代 TTS |
| lvsea-writing | 直接入口或本地 Skill | 使用保守口播检查并标记缺少专家调用 |
| grilling | 本地入口 | 关键决策不能静默猜测，需在对话中收敛 |

依赖存在不等于可调用。至少要做一次最小命令探测或读取实际工具输出；“文件存在”“HTTP 200”“插件已安装”不能代替真实调用证据。

## 质量层级

按证据分层报告：

1. **静态包层**：frontmatter、manifest、接口、脚本、参考链接和触发评测。
2. **项目结构层**：brief/article/script/audio/storyboard/output 文件和 SRT 结构。
3. **媒体技术层**：ffprobe 解码、时长、分辨率、帧率、视频/音频编码和流存在。
4. **HyperFrames 运行层**：lint、validate、inspect、preview 和 render 的实际输出。
5. **视觉与音画层**：关键帧抽检、字幕溢出、黑帧、静音、节奏、可读性和听感。
6. **外部 provider/人工层**：付费服务、云端授权、真人声音、版权、作者确认和最终发布判断。

只通过上层不能推断下层。当前没有真实项目输出时，报告 static package only / missing evidence；没有人工审看时，不宣称“成片质量已验证”。

## 权限默认值

- 网页和公开资料：只读研究；把 URL、日期、来源归属和待核实项写入 evidence.md；
- 本地项目：只写用户指定的项目目录，不回写浏览器缓存或全局数据；
- TTS：默认本地 edge-tts；需要联网时说明，声音克隆必须有明确授权；
- 图片/音乐/字体：优先用户提供、已授权或本地生成；记录 license 和用途；
- 远程服务：不把密钥写入文件、命令行历史、报告或 Git；收费调用前显示 provider、预计时长和费用；
- GitHub：本 Skill 本身不自动发布成片，不把项目媒体提交到 Skill 仓库。

## 输出前检查

- 事实：数字、日期、名称、单位、专业含义和来源归属没有被口播改写破坏；
- 文本：script.md 能朗读，AI 模板残留已定点处理，没有虚假引用或助手式收尾；
- 音频：voice.mp3 可解码，时长与 SRT 覆盖关系正确，没有尾部截断；
- 画面：主要镜头有职责，安全区、文字和 SVG 通过检查；
- 工具：HyperFrames lint/validate/inspect 结果留痕；
- 交付：final.mp4、SRT、独立音频、封面、工程和 final-check 只报告实际存在者。

## 回滚边界

- 项目阶段失败时保留中间产物和日志，不删除用户内容；
- 局部镜头修订只在 Git/项目副本或明确文件范围内进行；
- Skill 发布使用功能分支和不可覆盖的 semver 版本；失败时停止，不删除远程仓库；
- 本地安装同步先备份旧副本或写入隔离目录；不要把工作副本直接当成已安装副本；
- 公开仓库只包含匿名规则和工具，不包含原文文章、MP3/MP4、截图、Cookie、Token 或绝对路径。

