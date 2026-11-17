# Matt Mainflow

一个入口，按 Matt Pocock 的主流程推进开发。输入 `/matt-mainflow` 并描述任务，Agent 会显示当前阶段和下一步，等你确认或选择后继续。

**需求讨论 → 写规格 → 拆工单 → 实现 → 代码审查 → 复盘**

## 使用

- 开始：`/matt-mainflow 我想修复登录后跳转错误`
- 查看：`查看进度`
- 推进：`确认继续`
- 调整：`返回写规格，我想修改验收条件`
- 暂停：`暂停`；以后在项目中再次调用入口即可续接。

每个任务的进度保存在实际开发项目的 `.scratch/matt-mainflow/<task-slug>/state.md`。首次需要项目配置时，引导设置工单位置和文档布局；支持从已有规格或工单接入。

## 依赖与安装

本 skill 复用 [mattpocock/skills](https://github.com/mattpocock/skills) 的阶段指引，不包含其副本。需要：`grill-with-docs`、`to-spec`、`to-tickets`、`implement`、`code-review`、`retro`，以及 `setup-matt-pocock-skills`、`grilling`、`domain-modeling`、`tdd`、`codebase-design`、`writing-for-agents`。不使用 `implement-spec`。

本机通过 `/Users/vincent4j/.agents/skills/matt-mainflow` 软链接接入本仓库。其他环境把仓库接入宿主支持的 skills 搜索目录，并安装上述依赖。斜杠菜单和嵌套调用能力取决于宿主；不支持原生嵌套调用时，入口读取阶段文件作为操作指南。

阶段确认用于推进当前任务；提交、推送及外部发布沿用用户的实际授权。实现已产生的有效审查结果会复用，避免重复审查。

## 验证范围

静态格式校验不证明宿主发现、跨会话续接或真实开发流程已经通过；这些需要在实际宿主和开发项目中验证。
