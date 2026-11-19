# 仓库维护

- 上游 Skills 只读。禁止修改 Matt Pocock 在 `mattpocock/skills` 中发布的阶段及依赖指引，包括本机已安装的版本和离线包内的副本。项目需要调整流程时，在本项目的 `matt-mainflow` 编排规则中适配。
- 离线打包：用户说「打包」时，在仓库根目录运行 `python3 packaging/build.py`。已有固定版本的上游归档时可加 `--upstream-archive <归档路径>`。构建成功后对脚本输出的文件运行 `unzip -tq`，把完整路径作为可点击链接发给用户，并提示另存 ZIP。产物只存放在本地 `dist/`，禁止将 ZIP 提交、推送或上传到 GitHub，包括 Release 附件。
