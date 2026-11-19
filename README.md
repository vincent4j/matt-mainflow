# Matt Mainflow

一个入口，按 Matt Pocock 的主流程推进开发。输入 `/matt-mainflow` 并描述任务，Agent 会显示当前阶段和下一步，等你确认或选择后继续。

**需求讨论 → 写规格 → 拆工单 → 实现 → 代码审查 → 复盘**

## 使用

- 开始：`/matt-mainflow 我想修复登录后跳转错误`
- 查看：`查看进度`
- 推进：`确认继续`
- 调整：`返回写规格，我想修改验收条件`
- 暂停：`暂停`；以后在项目中再次调用入口即可续接。
- 收尾：6/6 复盘完成后回复 `收尾`，盘点临时文件，将长期有用的内容并入正式文档、代码或测试。正式成果提交后，确认清单并回复 `清理本任务`，删除该任务的全部临时产物。

每个任务的进度保存在实际开发项目的 `.scratch/matt-mainflow/<task-slug>/state.md`。工单存于开发项目的 `.scratch/<task-slug>/issues/`，每张一个编号 Markdown 文件。支持从已有规格或工单接入。

## 依赖与安装

项目首次启用时，从 `matt-mainflow` 入口按 [项目启用](SKILL.md#项目启用) 配置本地工单和 Git 忽略规则。

本 skill 复用 [mattpocock/skills](https://github.com/mattpocock/skills) 的阶段指引，不包含其副本。需要：`grill-with-docs`、`to-spec`、`to-tickets`、`implement`、`code-review`、`retro`，以及 `setup-matt-pocock-skills`、`grilling`、`domain-modeling`、`tdd`、`codebase-design`、`writing-for-agents`。不使用 `implement-spec`。

将本仓库放入宿主支持的 skills 搜索目录，或通过软链接接入，并安装上述依赖。入口根据宿主提供的路径定位各阶段指引。斜杠菜单和嵌套调用能力取决于宿主；不支持原生嵌套调用时，入口读取阶段文件作为操作指南。

阶段确认用于推进当前任务；提交、推送及外部发布沿用用户的实际授权。确认会绑定具体范围和产物版本，内容变化后重新确认。实现按已选批次连续推进，批次内包含工单审查和复验，第 5 阶段再核验整体审查覆盖。

## 验证范围

静态格式校验不证明宿主发现、跨会话续接或真实开发流程已经通过；这些需要在实际宿主和开发项目中验证。

维护和验收时使用[场景清单](references/validation.md)，记录实际结果与证据。
