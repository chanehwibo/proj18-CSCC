# KernelSage 研发历程记录

本文档用于记录项目每个阶段的研发进展、完成任务、验证情况和后续计划。后续新增功能、修复问题或调整方案时，在本文档基础上继续追加或修改。

## 阶段 1：MVP 仓库分析闭环

- 日期：2026-05-29
- 目标：先形成可运行的最小闭环，完成“仓库采集 → 结构化画像 → 描述报告 → 比较报告”的基础链路。
- 提交：`b1d6a6a Build MVP repository analysis pipeline`

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 项目计划 | 将 `docs/PLAN.md` 调整为 MVP 优先的 V1/V2 分层计划 |
| 样本清单 | 新增 `data/samples/manifest.json`，收录 6 个历史样本仓库 |
| 仓库采集 | 新增 `scripts/fetch_repos.py`，支持按 manifest 克隆历史仓库 |
| 数据模型 | 新增 `src/os_agent/models.py`，定义 RepoSnapshot、KernelProfile、Evidence、Finding 等结构 |
| 仓库扫描 | 实现 `collector.py`，支持文件扫描、语言统计、README/docs 读取和基础元信息整理 |
| 符号抽取 | 实现 `parser.py`，对 Rust/C/Asm 做轻量符号定义抽取 |
| 维度分析 | 实现 `analyzer.py`，围绕调度、内存、系统调用、文件系统、同步、中断、驱动 7 个维度抽取证据 |
| 报告生成 | 实现 `reporter.py`，输出 Markdown 描述报告和比较报告 |
| 比较流程 | 实现 `agent.py`，支持新仓库与历史样本的基础多维度比较 |
| CLI | 新增 `src/os_agent/cli.py` 和 `scripts/kernelsage.py`，提供 profile、describe、describe-all、compare 命令 |
| 文档 | 更新 `README.md`，加入 MVP 路线和快速运行命令 |
| Git 管理 | 更新 `.gitignore`，避免提交样本仓库本体、profiles 和 reports 生成物 |

### 已验证命令

```powershell
python scripts\kernelsage.py describe data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3
python scripts\kernelsage.py describe-all
python scripts\kernelsage.py compare data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2
python -m compileall src scripts\kernelsage.py
```

### 当前产出

| 类型 | 路径 |
| --- | --- |
| 结构化画像 | `data/profiles/*.json` |
| 描述报告 | `data/reports/describe/*.md` |
| 比较报告 | `data/reports/compare/rcore-tutorial-v3_vs_history.md` |

说明：上述 `data/profiles/` 和 `data/reports/` 属于生成物，已被 `.gitignore` 忽略，不作为源码提交。

### 当前能力边界

- 当前版本不依赖第三方 Python 包，可以直接用 Python 3.11 运行。
- 当前描述报告基于规则、关键词和证据片段生成，尚未接入 LLM 润色。
- 当前比较报告已经具备双方证据引用，但比较逻辑仍偏规则化，后续需要接入 LLM 生成更自然、更细致的比较文本。
- 当前符号抽取为轻量实现，不做跨文件调用图和完整 AST 语义分析。

### 下一阶段计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 接入 LLM 客户端，用证据约束生成更自然的描述报告 |
| P0 | 接入 LLM 比较流程，生成相似点、差异点和可能创新点 |
| P0 | 增加轻量 self-check，核验证据是否存在、关键结论是否有支撑 |
| P1 | 改进维度分析关键词和文件优先级，降低用户态代码和 README 干扰 |
| P1 | 增加 1 个端到端 demo 示例和固定演示命令 |
| P2 | 视样本规模决定是否加入 BM25 检索 |

## 阶段 2：LLM 客户端安全接入

- 日期：2026-05-29
- 目标：建立 DeepSeek/OpenAI 兼容 LLM 调用基础设施，同时避免开发调试阶段误扣费或泄露 API Key。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 环境模板 | 新增 `.env.example`，提供 DeepSeek API 配置模板 |
| 安全策略 | 确认 `.env` 被 `.gitignore` 忽略，真实 API Key 不进入仓库 |
| 缓存策略 | 新增 `data/llm_cache/` 忽略规则，LLM 响应按 prompt hash 缓存 |
| LLM 客户端 | 新增 `src/os_agent/llm.py`，使用标准库接入 OpenAI-compatible chat completions API |
| Dry-run | 新增 `--llm-dry-run`，只生成 prompt 文件，不调用 API |
| 显式调用 | 新增 `--use-llm`，只有显式传参才调用 LLM API |
| 文档 | 更新 `README.md`，说明 DeepSeek 配置、dry-run、缓存和安全约定 |

### 已验证命令

```powershell
python scripts\kernelsage.py describe data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --llm-dry-run
python -m compileall src scripts\kernelsage.py
```

### 当前能力边界

- 当前只完成描述报告的 LLM 接入，比较报告的 LLM 接入尚未完成。
- 当前没有在仓库中写入真实 API Key。
- 当前 dry-run 已可生成 `data/reports/prompts/*.prompt.md`，用于人工检查 prompt 后再决定是否调用 API。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 使用新 API Key 本地配置 `.env` 后，试跑一次 `--use-llm` |
| P0 | 将 LLM 接入比较报告生成流程 |
| P0 | 增加 LLM self-check prompt，核验证据支撑 |
| P1 | 优化 prompt 长度，降低 token 成本 |
