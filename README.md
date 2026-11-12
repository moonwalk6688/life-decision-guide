# life-decision-guide

基于《高性价比人生指南》的 Codex Skill。面对生活、工作与创业中的选择，它先查书中完整条目及备注，再区分适用条件、成本、收益口径和证据等级。

## 安装

在 PowerShell 中运行：

```powershell
New-Item -ItemType Directory -Path "$HOME\.codex\skills" -Force | Out-Null
git clone https://github.com/moonwalk6688/life-decision-guide.git "$HOME\.codex\skills\life-decision-guide"
```

重新打开 Codex 后，提问时可以点名 `$life-decision-guide`，例如：

> 用 $life-decision-guide 帮我分析要不要辞职创业，分别列出时间、现金和退出成本。

## 内容与边界

- `SKILL.md`：检索、核验与回答流程。
- `references/`：章节路由、读数方法和跨章节决策模式。
- `scripts/find_entry.py`：按章节和条号提取完整条目。
- `sources/book/`、`sources/docs/`：原项目的正文快照、长文与核实记录。

本地来源对应原项目提交 `e2605d3`，不是实时同步。医疗、法律、金融、政策和产品信息可能变化；实际办理或作高风险决定前，应核对最新官方及所在地信息。

## 出处与许可

原书及原始资料来自 [eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter)，正文依原项目的 [CC BY 4.0](sources/LICENSE) 许可转载；保留原项目版权、出处与许可说明。本仓库对原项目 Skill 的工作流程做了改编，改动和来源见 [ATTRIBUTION.md](ATTRIBUTION.md)。原项目代码许可见 [MIT](sources/LICENSE-CODE)。

本仓库由个人独立维护，与原项目作者没有官方隶属关系。发现书中内容与现行规定冲突时，以更新的一手来源为准。
