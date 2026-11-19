# 项目启用

首次推进项目任务前，检查是否已有适用的本地工单与规格约定，以及 `.scratch/` 是否已被 Git 忽略。已有配置满足要求时直接复用。发现缺项或用户要求启用时，读取 `setup-matt-pocock-skills` 指引，沿用检查、展示草案、确认后写入的顺序。

即使仓库配置了 GitHub remote，初始化也使用本地 Markdown 工单。按照[本地存放规则](../SKILL.md#规格与工单存放)展示下列需要新增或更新的内容。项目检查与验证均使用本地文件和 Git：

- 在项目根目录的 `.gitignore` 中确保有 `/.scratch/`，已有相同规则时复用。验收用 `git check-ignore --no-index -v -- .scratch/` 核对，已跟踪的文件另行报告。
- 在根目录 `AGENTS.md` 的 `## Agent skills` 内写入或原位更新 `### 本地工单`，直接写明「工单保存在 `.scratch/<task-slug>/issues/`，每张一个编号 Markdown 文件，依赖通过工单编号引用。续接已有工单时沿用其路径。」同时注明项目现有的本地规格约定，缺少约定时使用上述默认路径。该段是本地配置，不创建 `docs/agents/issue-tracker.md`。领域文档和可选的本地分诊标签仍按上游指引配置。
