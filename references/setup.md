# 项目启用

需要启用项目时，从 `matt-mainflow` 入口进入。将 `setup-matt-pocock-skills` 作为只读参考，沿用检查、展示草案、确认后写入的顺序。项目工单按[工单存放](../SKILL.md#工单存放)配置，直接展示以下改动：

- 在项目根目录的 `.gitignore` 中确保有 `/.scratch/`，已有相同规则时复用。验收用 `git check-ignore --no-index -v -- .scratch/` 核对，已跟踪的文件另行报告。
- 在根目录 `AGENTS.md` 的 `## Agent skills` 内写入或原位更新 `### 本地工单`，直接写明「工单保存在 `.scratch/<task-slug>/issues/`，每张一个编号 Markdown 文件，依赖通过工单编号引用。续接已有工单时沿用其路径。」该段是工单配置，不创建 `docs/agents/issue-tracker.md`。领域文档和可选的本地分诊标签仍按上游指引配置。
