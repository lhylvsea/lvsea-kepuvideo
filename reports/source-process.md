# Source Process Record

## Source

- X post: https://x.com/yyn1748762/status/2105835330406654424
- Linked X article: https://x.com/i/article/2105651241519038464
- Article title: 不会剪视频，也能用 Codex 从 0 做出一条完整成片，我把完整复刻流程写出来了
- Source reviewed: 2026-10-03
- Retrieval note: the direct X page returned 403 in the web reader; the public article payload was cross-checked through the public X oEmbed endpoint and the FXTwitter status payload. Only the article's visible workflow and prompts were used; no private account data or media was copied.

## Extracted workflow

1. Create an isolated project with article, script, storyboard, assets, audio, HyperFrames and output folders.
2. Turn a topic into a fact-checked article and stop for review.
3. Convert the article into a readable Chinese voiceover, keeping one core question.
4. When script.md still feels templated, run a final humanizer pass and read it aloud.
5. Preview three Chinese TTS voices from the first 80–120 characters before full narration.
6. Generate the complete voice track and SRT timing together.
7. Build storyboard.md from the real SRT timing, not estimated scene durations.
8. Use HyperFrames for HTML/CSS/SVG motion and start a preview before rendering.
9. Patch only the reported time range, then re-check.
10. Watch the whole preview, run final checks, render H.264/AAC MP4 and inspect with ffprobe.

## Adaptation for this package

- humanizer-zh was not treated as an installable dependency. Its role is implemented by an explicit $lvsea-writing final-edit contract.
- The fixed relativity example was generalized to any Chinese knowledge topic and to arbitrary target durations, including long-form chaptered videos.
- grilling is retained as a conditional design-tree gate for decisions that cannot be safely inferred.
- The process adds evidence, rights, dependency, SRT, safety-area and release boundaries that were not part of the source article's short tutorial.

