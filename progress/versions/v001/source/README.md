# v001 可编辑制作工程

本工程使用 HTML/SVG、手工单线字形及本地 Z003 字体。`scene.js` 根据时间直接计算画面，`timeline.json` 保存共用节拍参数；不依赖网络素材、随机状态或浏览器实际播放速度。

## 文件

- `index.html`：画布和本地字体入口，交由渲染脚本内嵌依赖后载入。
- `lettering.js`：从旧对话中恢复并修正的单线字形数据。
- `scene.js`：帽形、针、裂剑、真实连接锚点、书写与退场、两帧红闪及冲击后果。
- `timeline.json`：五句的演出窗口、音源裁切范围和输出参数。时间来自原字幕定位与波形检查，尚未逐词听审。
- `render.py`：用系统 Chromium/Playwright 渲染设计稿或逐帧编码静音视频。
- `finish.py`：提取原声、双遍响度处理、合成最终 MP4。
- `audio_review.py`：生成波形及动作标记；不进行语音识别或逐词对齐。
- `validate.py`：检查实际视频全部帧、两帧红闪、触边、音视频参数和响度，生成实际视频关键帧与总览。
- `requirements.txt`、`toolchain.json`：Python 依赖和已验证工具版本。
- `design-pass-*`：不同阶段的静态设计检查图，不是从成片提取的交付关键帧。
- `motion-draft.mp4`、`motion-review/`：存在布局问题的低清运动稿及检查结果。
- `layout-draft.mp4`、`layout-draft-source/`：早段剑柄触边的高清布局稿及其源码快照。
- `design-notes.md`：问题与修正过程。

最终交付应使用 `progress/versions/v001/video.mp4`；对应已冻结的源码在 `progress/versions/v001/source/`。中间稿用于复盘，不代表最终效果。

## 复现方式

从仓库根目录运行（输出路径需不存在）：

```sh
python3 progress/project/v001/render.py --stills --output progress/project/v001/new-design-stills
python3 progress/project/v001/render.py --output progress/project/v001/new-silent.mp4
python3 progress/project/v001/finish.py --silent progress/project/v001/new-silent.mp4 --output-dir progress/project/v001/new-export
python3 progress/project/v001/validate.py --video progress/project/v001/new-export/video.mp4 --output progress/project/v001/new-export/validation
```

渲染需要系统 FFmpeg、Chromium，以及 `requirements.txt` 中的包。当前云环境中浏览器启动需要已获准的进程权限；普通沙箱会在 Chromium 本地套接字操作处失败。沿用工具的正常审批流程，不通过关闭网络/TLS 检查处理。

新生成文件需登记到 `progress/catalog.json`。修改工程后重新生成完整版本和实际视频关键帧，并保留旧版源码及输出。
