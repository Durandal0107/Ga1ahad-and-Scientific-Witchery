# 媒体工具验证资料

用途：保留当前云环境已经完成的媒体工具验证，便于判断后续失败来自素材、编码还是制作工程。这里的 1 秒样片不是新制作的 MV，不列入视频版本。

## 文件说明

- [smoke.mp4](smoke.mp4)：从原视频开头转码的 1 秒样片；H.264 640×360、24 fps，AAC 双声道 48 kHz。
- [smoke-media.json](smoke-media.json)：本次归档后重新执行 ffprobe 的实际输出。
- [source-media.json](source-media.json)：已归档原始视频的 ffprobe 参数，约 219.208333 秒，1080×608、24 fps，AAC 双声道 44.1 kHz。
- [verification.json](verification.json)：本次对归档样片完整解码的命令、退出码和错误输出。
- [toolchain.json](toolchain.json)：当前工具/包的版本探测。不是旧工程锁文件，也不能代替 Chromium/Playwright 的实际渲染检查。

原始视频在本对话的环境初始化阶段已完整解码通过；本轮以与根目录源文件的 SHA-256 一致性验证归档副本，未重复全片解码。未对 MV 进行新的声画同步或响度验证。

## 样片复现

从仓库根目录执行以下命令，先为输出选择一个尚不存在的归档路径：

```sh
ffmpeg -nostdin -v error -xerror -i progress/assets/source/Mili_Ga1ahad_and_Scientific_Witchery.mp4 -t 1 -vf scale=640:-2 -c:v libx264 -threads 2 -pix_fmt yuv420p -c:a aac -ar 48000 -ac 2 progress/validation/onboarding/smoke-new.mp4
```

生成后应登记新文件及其验证结果。不要覆盖原有样片或用户资料。工具版本变更后的新编码不保证与旧样片逐字节一致。

## 字体来源

`../../assets/fonts/` 保存 Nimbus Roman Regular/Italic、Z003 Medium Italic，以及 Debian `fonts-urw-base35` 的许可文件。包版本见 `toolchain.json`。它们来自当前环境，尚未确认与旧对话所在环境的文件完全一致；使用时仍需检查排版。
