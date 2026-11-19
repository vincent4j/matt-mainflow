<h1 align="center">Matt Pocock 开发工作流</h1>

<p align="center">Matt Pocock Mainflow</p>

<p align="center">
  <strong>将 Matt Pocock 的六步开发工作流 The Main Flow（30 万+ GitHub Stars）串成一个入口，帮你和 Agent 在写代码前谈清需求、拆成可验收的工单，写完后按约定审查代码。</strong>
</p>

<p align="center">
  <a href="https://www.aihero.dev/skills">查看 Matt Pocock 的 Skills 和 The Main Flow</a>
</p>

<p align="center">
  <a href="#why">The Main Flow 解决什么问题</a> ·
  <a href="#workflow">Matt Pocock 开发工作流 怎么用</a> ·
  <a href="#quickstart">快速上手</a> ·
  <a href="#project-files">项目文件</a>
</p>

---

<a id="why"></a>

## 💡 The Main Flow 解决什么问题？

把一个粗略的功能想法交给 Agent，它可能很快就写出代码，但需求边界和验收条件往往还没谈清。Matt Pocock 的 **The Main Flow** 给出了从想法到交付的路线。先把关键决定写成规格，再拆成可以独立验收的工单。实现后，用同一份规格检查代码有没有做对，最后复盘哪里可以改进。 [The Main Flow 原文](https://www.aihero.dev/skills)

**需求讨论 → 写规格 → 拆工单 → 实现 → 代码审查 → 复盘**

`grill-with-docs` → `to-spec` → `to-tickets` → `implement` → `code-review` → `retro`

[![AI Hero 页面截图，展示 The Main Flow 的六个 Skills](assets/the-main-flow.png)](https://www.aihero.dev/skills)

<a id="workflow"></a>

## 🎯 Matt Pocock 开发工作流 让这套流程更容易用

**Matt Pocock 开发工作流 把 Matt Pocock 的六个 Skills 串成一个入口。** 把任务和手头已有的规格或工单交给它，它会选好从哪一步开始、提示接下来做什么，并记录进度。换个会话也能接着做。

| 你手头的任务 | Matt Pocock 开发工作流 怎么推进 |
|---|---|
| 登录跳转有个小问题，复现和验收都清楚 | 直接修复、验证，再检查改动是否符合验收。 |
| 想做一个功能，行为和边界还没说清 | 先和你确认关键决定，再写成规格供确认。一次能做完时，直接进入实现。 |
| 项目要分几次做，或者要交给另一个会话接手 | 把规格拆成可独立验收的工单，经你确认后按依赖推进。 |
| 手上已经有规格或工单 | 核对现有文件与当前任务，从最早还有工作的阶段接入。 |

代码审查同时看项目规范和已确认的需求。有返工、漏检或交接问题时，可以复盘哪一步值得改进。完整的路线选择见 [Skill 说明](SKILL.md#选择路线)。

---

<a id="quickstart"></a>

## 🚀 快速上手

### 安装

把下面这句话发给你的 Agent。

```text
请从 https://github.com/vincent4j/matt-mainflow 安装 matt-mainflow 到你的 Skills 目录，并按仓库 SKILL.md 中的阶段依赖表安装所需的 Matt Pocock Skills。
```

安装后打开新会话，在技能列表中确认能找到这个 Skill。

### 开始一个任务

在开发项目中选择 **Matt Pocock 开发工作流**（英文菜单中显示为 **Matt Pocock Mainflow**）并描述任务。支持斜杠菜单的 Agent 可以这样输入。

```text
/matt-mainflow 登录成功后应返回登录前访问的页面。先和我确认验收条件，再开始修改。
```

| 你想做什么 | 直接告诉 Agent |
|---|---|
| 看看做到哪了 | 查看进度 |
| 推进刚展示的待确认步骤 | 确认继续 |
| 改一条已经讨论过的需求 | 返回写规格，我想修改验收条件 |
| 留到下次处理 | 暂停。下次在同一个项目里调用 Matt Pocock 开发工作流，说「继续」。 |
| 验收和审查完成，准备结束 | 收尾 |

首次需要项目配置时，Agent 会展示拟写入的内容，经你确认后再 [启用项目](SKILL.md#项目启用)。

---

<a id="project-files"></a>

## 📁 项目里会新增什么？

| 文件或目录 | 用来做什么 |
|---|---|
| `.scratch/matt-mainflow/<任务名>/state.md` | 记录当前阶段、已确认的范围和下一步，供新会话续接。 |
| `.scratch/<任务名>/issues/` | 需要拆分时，存放确认后的工单，每张一个 Markdown 文件。 |

书面规格沿用项目的本地约定。收尾后，正式成果已提交且你确认过清单时，可以回复「清理本任务」移除对应的临时文件。

[场景验收清单](references/validation.md)
