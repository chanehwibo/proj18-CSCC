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

### 追加记录：失败回退与比较报告 dry-run

- 日期：2026-06-04
- 背景：本地 `.env` 已配置 DeepSeek API Key，但真实请求返回 `402 Insufficient Balance`，说明账户余额不足。

| 模块 | 完成内容 |
| --- | --- |
| 安全修正 | 发现 `.env.example` 曾被写入真实 Key，已转移到本地 `.env` 并恢复 `.env.example` 占位符 |
| 失败回退 | `describe --use-llm` 在 LLM API 失败时自动回退到规则版报告，不中断输出 |
| 比较 LLM | 新增比较报告 LLM prompt 生成逻辑 |
| CLI | `compare` 新增 `--use-llm` 与 `--llm-dry-run` 参数 |
| 文档 | README 补充 API 失败回退和比较报告 dry-run 用法 |

已验证命令：

```powershell
python scripts\kernelsage.py describe data\samples\rcore-tutorial-v3-ch9 --repo-id rcore-tutorial-v3-ch9 --use-llm
python scripts\kernelsage.py compare data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2 --llm-dry-run
python -m compileall src scripts\kernelsage.py
```

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 充值或更换可用模型后，试跑一次真实 `--use-llm` |
| P0 | 增加 LLM self-check prompt，核验证据支撑 |
| P1 | 优化 prompt 长度，降低 token 成本 |

## 阶段 3：端到端 Demo 与轻量 Self-check

- 日期：2026-06-05
- 目标：修复 MVP 命令链路中的稳定性问题，补齐答辩可用的一键演示命令，并让报告具备明确的证据核验摘要。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| CLI 稳定性 | 修复 `describe-all` 在新增 LLM 参数后缺少 `use_llm`/`llm_dry_run` 字段导致的运行错误 |
| Demo 命令 | 新增 `demo` 子命令，一次生成结构化画像、描述报告和比较报告 |
| Self-check | 新增 `src/os_agent/selfcheck.py`，核验证据文件与行号是否存在 |
| 报告输出 | 描述报告和比较报告末尾新增轻量核验摘要 |
| 统计口径 | 明确证据率只统计需要源码证据支撑的设计判断，语言构成、风格标签和汇总性描述不计入证据率 |
| 文档 | 更新 README，补充 `demo` 命令、self-check 说明和当前状态 |

### 已验证命令

```powershell
python -m compileall src scripts\kernelsage.py
python scripts\kernelsage.py describe-all
python scripts\kernelsage.py demo data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2
```

### 当前产出

| 类型 | 路径 |
| --- | --- |
| Demo 画像 | `data/profiles/rcore-tutorial-v3.json` |
| Demo 描述报告 | `data/reports/describe/rcore-tutorial-v3.md` |
| Demo 比较报告 | `data/reports/compare/rcore-tutorial-v3_vs_history.md` |

说明：上述报告与画像仍属于生成物，继续被 `.gitignore` 忽略，不作为源码提交。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 把 self-check 结果接入 LLM prompt，让模型生成报告前看到证据核验口径 |
| P0 | 优化比较报告的历史样本选择，避免只按目录顺序取样 |
| P1 | 继续改进维度关键词和文件优先级，减少文档文件对“代码实现”判断的干扰 |

## 阶段 4：仓库整理与 README 更新

- 日期：2026-06-05
- 目标：清理本地运行生成物，明确仓库保留边界，并把 README 更新为当前可用的开源项目首页。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 本地清理 | 删除 `__pycache__`、`data/profiles/`、`data/reports/`、`data/llm_cache/` 和抓取报告等运行生成物 |
| 保留边界 | 保留 `.env` 本地配置和 `data/samples/` 本地样本仓库；二者均不提交 |
| README | 重写 README，补充目标、当前能力、架构、快速运行、LLM 配置、证据核验口径、仓库目录和研发计划 |
| 安全说明 | README 明确 `.env` 禁止提交，默认命令不调用 LLM API |

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 优化比较报告的历史样本选择策略 |
| P0 | 在可用 LLM API 下试跑真实描述报告 |
| P1 | 增加最小测试用例，覆盖 demo/self-check/CLI 参数 |

## 阶段 5：历史样本选择策略优化

- 日期：2026-06-06
- 目标：避免比较流程按目录顺序截取历史仓库，改为根据结构化画像选择更合适的对比样本。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 样本选择 | 新增 `src/os_agent/selector.py`，按风格、架构、语言构成、OS 维度和代码规模对历史样本打分 |
| CLI | `compare` 构建全部候选画像后再排序选取 Top N，不再按目录顺序提前截断 |
| 报告 | 比较报告新增“历史样本选择”小节，展示分数和选择理由 |
| LLM | 比较报告 LLM prompt 增加 `selection_notes`，保留样本选择依据 |
| 测试 | 新增 `tests/test_selector.py`，验证选择器不会受输入顺序影响 |
| 文档 | README 更新历史样本选择策略和研发计划状态 |

### 已验证命令

```powershell
python -m compileall src scripts\kernelsage.py
python scripts\kernelsage.py demo data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2
python scripts\kernelsage.py compare data\samples\xv6-riscv --repo-id xv6-riscv --limit 3
```

### 观察结果

- `rcore-tutorial-v3` 的 Top 2 历史样本从目录顺序候选变为 `zCore`、`rcore-tutorial-v3-ch9`。
- `xv6-riscv` 的 Top 3 历史样本按画像相似度排序为 `arceos`、`rcore-tutorial-v3`、`rcore-tutorial-v3-ch9`。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 在可用 LLM API 下试跑真实描述报告 |
| P1 | 扩展最小测试用例，覆盖 CLI demo 与 self-check |

## 阶段 6：真实 LLM 试跑与最小测试补强

- 日期：2026-06-06
- 目标：按计划验证真实 LLM 调用链路，并补充最小测试用例，降低后续迭代回归风险。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| LLM 试跑 | 使用 `.env` 中的模型配置运行 `describe --use-llm`，成功生成真实 LLM 描述报告并写入缓存 |
| Prompt 收紧 | 强化 LLM system/user prompt，要求只引用输入 evidence 中已有的文件和行号，不扩写未确认算法细节 |
| Self-check 输入 | LLM 描述 prompt 增加 `self_check` 摘要，提示模型保留证据核验口径 |
| CLI 测试 | 新增 `tests/test_cli.py`，覆盖 `demo` 参数解析和 LLM dry-run 参数 |
| Selector 测试 | 新增 `tests/test_selector.py`，覆盖历史样本选择不受输入顺序影响 |
| Self-check 测试 | 新增 `tests/test_selfcheck.py`，覆盖有效证据、无效证据和未确认结论统计 |

### 已验证命令

```powershell
python scripts\kernelsage.py describe data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --use-llm
python -m compileall src scripts\kernelsage.py
$env:PYTHONPATH='src'; python -m unittest discover -s tests
```

### 观察结果

- 真实 LLM 调用成功，生成了 `data/reports/describe/rcore-tutorial-v3.md` 和一条 `data/llm_cache/` 缓存。
- 首次真实输出可读性较好，但存在根据上下文扩写实现细节的倾向，因此已收紧 prompt。
- LLM 相关生成物和缓存继续作为本地运行产物，不提交到仓库。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 重新用 dry-run 检查收紧后的 LLM prompt |
| P1 | 整理答辩演示材料和固定演示流程 |

## 阶段 7：答辩演示流程整理

- 日期：2026-06-06
- 目标：把当前 MVP 能力整理成固定演示流程，便于阶段检查、和导师沟通以及后续答辩准备。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 演示文档 | 新增 `docs/DEMO.md`，固定端到端演示命令、报告查看命令和讲解重点 |
| 答辩讲解 | 整理“赛题不是写 OS，而是分析 OS 仓库智能体”的讲解主线 |
| LLM 说明 | 在演示流程中区分 dry-run 和真实 API 调用，强调费用与安全边界 |
| README | 更新仓库目录、研发计划状态和演示文档入口 |

### 推荐演示命令

```powershell
python scripts\kernelsage.py demo data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2
```

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 改进关键词和文件优先级，减少文档或用户态代码干扰 |
| P1 | 增加 CLI demo 端到端轻量测试 |

## 阶段 8：证据优先级与文档干扰修正

- 日期：2026-06-06
- 目标：减少比较报告中 Markdown 文档、工具脚本和用户态路径对“内核机制实现”判断的干扰。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 路径优先级 | `KernelAnalyzer` 新增内核路径、支撑路径、低优先级路径分层评分 |
| 文档证据 | OS 维度关键词检索不再使用 Markdown 作为实现证据 |
| 样本选择 | 文档型样本不再仅凭 Markdown 命中获得 OS 维度确认 |
| 测试 | 新增 analyzer 路径优先级测试和 doc-only 仓库测试 |
| 文档 | 更新 README 和 DEMO，说明 Markdown 不作为 OS 实现证据 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python scripts\kernelsage.py demo data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2
python scripts\kernelsage.py compare data\samples\xv6-riscv --repo-id xv6-riscv --limit 3
```

### 观察结果

- `outline.md`、`xtask/`、`ulib/`、`apps/` 等路径不再出现在新生成的比较报告证据中。
- `rcore-tutorial-v3` 的 Top 2 历史样本变为 `zCore`、`xv6-riscv`，不再把文档型 `rcore-tutorial-v3-ch9` 作为主要比较对象。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 增加 CLI demo 端到端轻量测试 |
| P1 | 整理可提交的阶段性样例报告或报告截图 |

## 阶段 9：阶段性评审材料整理

- 日期：2026-06-08
- 目标：在不提交 `data/reports/` 运行生成物的前提下，整理一份可提交、可复现、便于导师和队友查看的阶段性评审材料。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| Demo 复现 | 重新运行 `demo`，生成最新描述报告和比较报告 |
| 测试验证 | 运行最小测试集，确认 CLI、selector、self-check、analyzer 测试通过 |
| 评审材料 | 新增 `docs/STAGE_REVIEW.md`，记录复现命令、报告摘要、历史样本选择结果、self-check 指标和人工复核结论 |
| README | 增加阶段性评审材料入口 |

### 已验证命令

```powershell
python scripts\kernelsage.py demo data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2
$env:PYTHONPATH='src'; python -m unittest discover -s tests
```

### 观察结果

- 描述报告关键结论证据覆盖率为 100.0%，无效证据引用数为 0。
- 比较报告关键结论证据覆盖率为 100.0%，无效证据引用数为 0。
- 当前 Top 2 历史样本为 `zCore` 和 `xv6-riscv`。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 让 LLM 在 evidence/self-check 约束下生成更自然的比较报告 |
| P1 | 增加 CLI demo 端到端测试 |

## 阶段 10：LLM 比较报告约束增强

- 日期：2026-06-08
- 目标：让 LLM 生成比较报告时保留历史样本选择依据、证据链和 self-check 统计，避免强行总结创新点。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| Compare Prompt | `_compare_prompt` 增加 `self_check` 摘要，要求输出比较对象选择、相似点、差异点、可能创新点、待人工复核项和核验摘要 |
| 创新点约束 | 当 `unique_points` 为空或只有“未确认”时，要求明确写“当前证据不足，未自动确认创新点”，禁止强行归纳 |
| 样本选择依据 | 要求 LLM 必须保留 `selection_notes` 中的历史样本选择依据 |
| 测试 | 新增 `tests/test_llm_prompt.py`，检查 compare prompt 包含 selection、self_check 和不强行生成创新点的约束 |
| 文档 | README 更新 LLM 约束说明和研发计划状态 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python scripts\kernelsage.py compare data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2 --llm-dry-run
python -m compileall src scripts\kernelsage.py
```

### 观察结果

- compare dry-run prompt 已包含 `selection_notes`、`self_check`、核验摘要要求和创新点不足时的显式处理规则。
- 本阶段没有真实调用 LLM API，不产生费用。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 增加 CLI demo 端到端测试 |
| P1 | 整理答辩材料初稿 |

## 阶段 11：公开比赛作品对比库扩展

- 日期：2026-06-08
- 目标：补充真实比赛作品样本，避免对比库只由教学基线组成，并保留本轮生成报告供人工审阅。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 样本清单 | `data/samples/manifest.json` 从 6 个样本扩展到 10 个样本，新增 4 个 2024 操作系统比赛公开仓库 |
| 样本分类 | 新增样本统一标记为 `contest-case`，与 `teaching-baseline` 教学基线区分 |
| 仓库采集 | 成功拉取 `oskernel2024-hfut666`、`oskernel2024-aabcb`、`oskernel2024-nqos`、`oskernel2024-ouye` |
| 报告生成 | 为 4 个新增样本生成描述报告，并生成 `oskernel2024-hfut666` 的 Top 4 历史对比报告 |
| 评审材料 | 更新 `docs/STAGE_REVIEW.md`，记录新增样本、复现命令、报告路径和对比观察 |
| README | 补充当前对比库范围，并同步实际测试文件列表 |

### 已验证命令

```powershell
python scripts\fetch_repos.py --only oskernel2024-hfut666 --only oskernel2024-aabcb --only oskernel2024-nqos --only oskernel2024-ouye
python scripts\kernelsage.py describe data\samples\oskernel2024-hfut666 --repo-id oskernel2024-hfut666
python scripts\kernelsage.py describe data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb
python scripts\kernelsage.py describe data\samples\oskernel2024-nqos --repo-id oskernel2024-nqos
python scripts\kernelsage.py describe data\samples\oskernel2024-ouye --repo-id oskernel2024-ouye
python scripts\kernelsage.py compare data\samples\oskernel2024-hfut666 --repo-id oskernel2024-hfut666 --limit 4
```

### 当前产出

| 类型 | 路径 |
| --- | --- |
| 描述报告 | `data/reports/describe/oskernel2024-hfut666.md` |
| 描述报告 | `data/reports/describe/oskernel2024-aabcb.md` |
| 描述报告 | `data/reports/describe/oskernel2024-nqos.md` |
| 描述报告 | `data/reports/describe/oskernel2024-ouye.md` |
| 对比报告 | `data/reports/compare/oskernel2024-hfut666_vs_history.md` |

说明：上述报告为运行生成物，按当前需求暂时保留在本地供查看，但仍不提交到仓库。

### 观察结果

- `oskernel2024-hfut666` 的 Top 4 对比对象为 `oskernel2024-nqos`、`xv6-riscv`、`oskernel2024-aabcb`、`arceos`。
- 新增比赛作品已经进入相似样本排序结果，对比库代表性优于仅使用教学基线的版本。
- 王杰优秀获奖案例的公开仓库 URL 本轮尚未明确定位，后续拿到地址后应优先补入。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 对新增比赛样本报告进行人工审阅，修正明显误判的关键词或路径优先级 |
| P1 | 增加 CLI demo 端到端测试 |
| P1 | 继续补充明确来源的优秀获奖案例仓库 |
