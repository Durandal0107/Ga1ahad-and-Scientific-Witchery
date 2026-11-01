# 项目资料与接续入口

用户要求：任何对制作和修改视频可能有价值的文件，都保存在 `progress/` 并做好标注。这里保存成果、原料、可编辑工程、讨论及有复用价值的中间结果。

## 下次从这里开始

1. 阅读 [requirements.md](requirements.md)，了解当前目标、最新反馈与待讨论方案。
2. 查阅 [catalog.json](catalog.json)，按用途、状态及关联版本定位实际文件、调用方式和依赖；`missing` 列出尚未取得的资料。
3. 从仓库根目录运行 `python3 progress/tools/catalog.py --check`，检查文件齐全且内容与清单一致。
4. 查看版本索引；有实际工程后，按对应版本说明的工作目录、依赖及命令继续制作。

## 保存位置

| 位置 | 内容与状态 |
| --- | --- |
| [requirements.md](requirements.md) | 固定的效果要求、反馈和修改记录。 |
| [catalog.json](catalog.json) | 每个文件的用途、来源、状态、关联版本、调用方式、依赖、大小及 SHA-256；清单本身不自计算哈希。 |
| [context/old.md](context/old.md) | 历史对话、制作代码与修改过程。仅移除了 6 个附件 URL 的临时查询参数，行号保持不变；根目录原文保留。附件链接本身不等于文件已保存。 |
| [references/line-art.md](references/line-art.md) | 当前采用的细线动画风格要求。 |
| [references/prompts.md](references/prompts.md) | 早期 10 秒模板；其固定时长不直接适用于当前任务。 |
| [assets/source/Mili_Ga1ahad_and_Scientific_Witchery.mp4](assets/source/Mili_Ga1ahad_and_Scientific_Witchery.mp4) | 原始音乐视频，与根目录源文件逐字节一致。 |
| `assets/fonts/` | 旧工程使用过的三种字体及 [许可](assets/fonts/LICENSE.txt)，从当前环境取得；未证明与旧环境二进制一致。 |
| [project/v001/README.md](project/v001/README.md) | 新编写的可编辑工程、脚本、时间轴、依赖、设计稿、运动稿及修正记录；不是取回的旧独立工程。 |
| [assets/audio/five-lines-17.6-29.3.wav](assets/audio/five-lines-17.6-29.3.wav) | 从原始视频 17.600–29.300 秒新提取的无损原声片段，供后期处理使用。 |
| [planning/legacy-upload-001-revision-plan.md](planning/legacy-upload-001-revision-plan.md) | 针对用户上传上一版短片的修改方向、画面定位和建议分镜。 |
| `versions/` | 最新重做 [v001](versions/v001/README.md) 及 17 张实际成片关键帧；保留用户提供的 [上一版评审片](versions/legacy-upload-001/README.md)。 |
| [validation/onboarding/README.md](validation/onboarding/README.md) | 已有工具验证样片、参数、当前版本信息和验证记录，不是 MV 设计版本。 |
| [tools/catalog.py](tools/catalog.py) | 更新和检查清单，仅使用 Python 标准库。 |
| [templates/version-README.md](templates/version-README.md) | 版本说明模板，包含修改、复现、验证及待办。 |

参考视频、截图、声音片段、图形素材等在取得或生成后，也要保存实际文件并登记；不能只留下临时链接或另一个环境的路径。

## 每轮更新流程

1. 在 `requirements.md` 追加效果目标、本轮修改与未解决事项，更新生效要求并保留历史。
2. 保存素材、参考、工程、渲染及后期脚本、依赖、配置、字体与许可、时间轴、分镜和有复用价值的中间结果。失败尝试若有助于定位问题或避免返工，也需存档并标记。长任务在关键节点保存，不等最终导出。
3. 新成片放入新的 `versions/vNNN/`，同时保留对应源码、配置与复现方法；关键帧从该版视频提取并记录帧号/时间码。共享输入用 `progress/` 内相对路径引用，明确依赖。保留旧版本。
4. 按 [版本说明模板](templates/version-README.md) 记录输入、改动、调用步骤、实际验证及不足，更新版本索引。仅文档变更或未完成渲染时说明未生成新视频的原因。
5. 为每个新文件在 `catalog.json` 添加 `path`、`kind`、`purpose`、`source`、`status`、`related_versions`、`usage` 和 `depends_on`。路径相对 `progress/`，依赖须指向已登记的文件。缺失资料登记在 `missing`，不能列为已有。
6. 从仓库根目录运行 `python3 progress/tools/catalog.py --refresh` 更新大小与哈希，再运行 `python3 progress/tools/catalog.py --check`。工具会检查未登记文件、缺少注释、缺失文件和依赖。哈希检查不能代替视觉、音频和渲染检查。
7. 检查并提交到 GitHub，确认远端后报告保存完成；保护其他对话的修改，不强制推送。

可重建且无复用价值的缓存不必保存；有价值的中间结果、草稿和工程不能只留在 `/tmp`。根目录旧文件保留为来源，日常调用优先用此目录内的归档；新增上传及时归档，来源变化时记录新版本，避免悄悄覆盖历史。

## 视频版本索引

最新重做版本为 v001：12.8 秒、1080p、30 fps，含原声。原始音乐视频与工具验证样片不占用制作版本号。

| 版本 | 日期（北京时间） | 修改概要 | 视频 | 关键帧、工程与说明 | 状态 |
| --- | --- | --- | --- | --- | --- |
| v001 | 2026-11-01 | 帽形/针线与裂剑、连续牵引转场、歌词退场、两帧红闪后 kill 直接落位 | [新版视频](versions/v001/video.mp4) | [关键帧、源码与验证](versions/v001/README.md) | 已制作，待用户评审 |
| legacy-upload-001 | 2026-11-01 | 用户上传的旧版，附本轮分析 | [视频](versions/legacy-upload-001/video.mp4) | [关键帧与说明](versions/legacy-upload-001/README.md)；工程待恢复 | 已归档，待修改 |

## 历史版本（文件待恢复）

| 旧版名称 | 历史报告 | 最后反馈 | 当前文件状态 |
| --- | --- | --- | --- |
| `five-lines-mv` | 12.8 秒、1080p、30 fps，包含原声。 | 意象太小，文字力量、线条作用与人物情感表达不足。 | 视频、关键帧和独立工程未找到。 |
| `five-lines-mv-v2` | 12.8 秒、1080p、30 fps，重绘连笔字体及意象。 | 人物意象、冲击、转场、无意义线条及歌词退场仍需修改。 | 用户已提供与此描述吻合的旧版评审片，归档为 legacy-upload-001；原工程及旧关键帧仍未恢复。 |

历史报告不能代替本轮质检；恢复或重新渲染后再建立带实际文件的版本条目。完整要求、来源定位和恢复清单见 [requirements.md](requirements.md)。

## 接续状态

- 已归档原始音乐视频、两份风格资料、旧对话、当前可用字体和媒体工具验证资料。
- 当前范围是前五句歌词的确认短片，六项最新修改目标见 `requirements.md`。
- 用户随后要求“重做并上传”“继续完成动画”；本轮选择帽形/针/剑与两帧红闪方案实施，等待对成片的评价。历史建议中的镜头滞后未单独采用。
- 用户已提供上一版短片，视频与本轮抽取的关键帧已存档；[修改方向](planning/legacy-upload-001-revision-plan.md) 将六项反馈落实到五句的具体动作。
- 新工程与正式成片已完成，全部 384 帧解码通过，图像检测无空白或触边，红闪为 306/307 帧；声音为 −13.9 LUFS、−6.6 dBTP。时间点基于继承字幕和波形，未完成人工逐词听审。
- 旧独立工程、其他历史视频、原关键帧、参考 PV 和截图仍待恢复；新工程是重新制作，不代表旧文件已找回。
