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

## 阶段 12：18 个代表性样本库扩展

- 日期：2026-06-08
- 目标：在不大规模拉取仓库的前提下，将参考库扩展到 18 个代表性样本，增强对未知 OS 仓库的比较全面性。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 样本清单 | `data/samples/manifest.json` 从 10 个样本扩展到 18 个样本 |
| 技术路线覆盖 | 新增 x86、x86_64、ARM、RTOS、微内核、嵌入式内核、unikernel、C++ 等代表样本 |
| 仓库采集 | 成功浅克隆 `xv6-public`、`os-tutorial`、`littlekernel`、`freertos-kernel`、`tock`、`sel4`、`includeos`、`redox-kernel` |
| 报告生成 | 生成 `xv6-public`、`freertos-kernel`、`sel4`、`includeos` 的描述报告 |
| 对比验证 | 生成 `xv6-public` 的 Top 5 对比报告，验证同架构/同风格样本能进入优先比较结果 |
| 评审材料 | 更新 `README.md` 和 `docs/STAGE_REVIEW.md`，说明 18 个样本的覆盖范围和边界 |

### 已验证命令

```powershell
python scripts\fetch_repos.py --only xv6-public --only os-tutorial --only littlekernel --only freertos-kernel --only tock --only sel4 --only includeos --only redox-kernel
python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public
python scripts\kernelsage.py describe data\samples\freertos-kernel --repo-id freertos-kernel
python scripts\kernelsage.py describe data\samples\sel4 --repo-id sel4
python scripts\kernelsage.py describe data\samples\includeos --repo-id includeos
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 5
```

### 当前产出

| 类型 | 路径 |
| --- | --- |
| 描述报告 | `data/reports/describe/xv6-public.md` |
| 描述报告 | `data/reports/describe/freertos-kernel.md` |
| 描述报告 | `data/reports/describe/sel4.md` |
| 描述报告 | `data/reports/describe/includeos.md` |
| 对比报告 | `data/reports/compare/xv6-public_vs_history.md` |

说明：上述报告继续作为本地运行生成物保留，供人工查看，不提交到仓库。

### 观察结果

- `xv6-public` 的 Top 5 对比对象为 `os-tutorial`、`sel4`、`xv6-riscv`、`littlekernel`、`oskernel2024-aabcb`。
- 新增样本后，x86/C 输入仓库能够优先匹配同架构、同风格项目，说明参考库代表性优于 10 样本版本。
- 首次对 18 个样本做全候选比较时出现过 120 秒超时，后续在缓存/已生成画像存在时可正常完成；这提示下一阶段应加入画像缓存复用或预计算流程。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 优化比较流程的画像缓存复用，避免每次 compare 重新分析全部历史样本 |
| P1 | 对新增样本报告做人工抽查，校正 RTOS、微内核、unikernel 的关键词和维度判断 |
| P1 | 继续补充明确来源的优秀获奖案例仓库 |

## 阶段 13：README 首页视觉与信息结构优化

- 日期：2026-06-08
- 目标：优化仓库首页呈现方式，让评委和导师能快速看到项目状态、核心能力、参考库覆盖、运行命令和安全边界。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| README 首页 | 重写 README 顶部结构，增加状态徽章、项目卡片和当前状态矩阵 |
| 能力展示 | 将原来的长段文字整理为核心能力表，突出扫描、画像、比较、LLM 和 self-check |
| 参考库说明 | 将 18 个样本按教学基线、比赛作品、架构补充、RTOS/微内核/unikernel 分层展示 |
| 运行入口 | 整理快速开始、输出文件、LLM 配置和测试命令，方便直接复现 |
| 边界说明 | 明确创新性判断不强行断言，覆盖不足时降低置信度并提示人工复核 |
| 仓库目录 | 更新目录树，保留关键源码、脚本、文档和测试文件入口 |

### 说明

- 本轮只调整 README 文档呈现，不改变代码逻辑。
- 公开检索中未能严谨确认“排名靠前项目仓库链接”，因此 README 未写入未证实的获奖背书；只参考公开 OS 赛项目常见的信息组织方式。

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
```

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 优化比较流程的画像缓存复用，避免 18 样本首次 compare 成本过高 |
| P1 | 对新增样本报告做人工抽查，校正 RTOS、微内核、unikernel 的关键词和维度判断 |
| P1 | 整理答辩讲稿和截图材料 |

## 阶段 14：托管仓库目标收敛

- 日期：2026-06-08
- 目标：将后续开发推送目标收敛到官网自动生成的新 GitLab 仓库，避免继续向临时仓库或 GitHub 推送。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 默认远程 | 将 `origin` 调整为官网自动生成仓库 `https://gitlab.eduxiji.net/T2026100659911488/project3136859-389327` |
| 临时仓库 | 将旧 `proj18_tjnu/proj18` remote 改名为 `proj18_temp`，仅保留 fetch，禁用 push |
| GitHub | 保留 `github` fetch 信息，禁用 push，后续不再推送 GitHub |
| 推送规则 | 后续默认只执行 `git push origin main`，目标为官网自动生成的新仓库 |

### 当前远程约定

| remote | 用途 |
| --- | --- |
| `origin` | 正式提交目标，官网自动生成仓库 |
| `proj18_temp` | 旧临时仓库，只作历史参考，不推送 |
| `github` | 旧 GitHub 镜像，不推送 |

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | 在 GitLab 网页端将正式项目显示名称改为 `proj18-tjnu-一定要以人类的身份赢啊` |
| P0 | 在 GitLab 网页端将旧临时项目显示名称改为 `2026-proj18临时版` |
| P0 | 优化比较流程的画像缓存复用，避免 18 样本首次 compare 成本过高 |

## 阶段 15：KernelProfile 画像缓存复用

- 日期：2026-06-08
- 目标：解决 18 个参考样本下 `compare` 重复扫描、解析和画像全部历史仓库导致的性能问题。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 模型恢复 | 为 `KernelProfile`、`Finding`、`Evidence`、`RepoMeta`、`SymbolDef` 增加 JSON 反序列化能力 |
| 缓存模块 | 新增 `src/os_agent/profile_cache.py`，统一管理画像缓存读取、写入和失效判断 |
| 缓存指纹 | 使用仓库路径、HEAD、文件数量、总大小、最新修改时间判断缓存是否仍有效 |
| CLI 接入 | `profile`、`describe`、`describe-all`、`demo`、`compare` 默认启用缓存 |
| 手动控制 | 新增 `--rebuild-profile-cache` 和 `--no-profile-cache` 参数 |
| 对比输出 | `compare` 输出历史样本缓存命中和重建数量，方便观察性能收益 |
| 测试 | 新增缓存命中、源码变化失效、强制重建和 CLI 参数测试 |
| 文档 | README 和阶段评审文档补充缓存机制、推荐命令和 token 成本边界 |

### 成本边界说明

- 画像缓存只缓存本地静态分析结果，不调用 DeepSeek，不增加 API token。
- 默认规则版报告不产生 LLM 费用。
- 只有显式使用 `--use-llm` 时才会请求在线模型并消耗 token。
- 更详细的报告如果意味着更长 prompt、更多 evidence 或更多历史样本进入 LLM，上线调用时才会增加 token；本阶段缓存优化不会增加该成本。

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 5
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 5
```

### 观察结果

- 第一轮 `compare` 重建 17 个历史样本画像，用时约 75 秒，输出 `hits=0 rebuilt=17 history_total=17`。
- 第二轮相同命令命中 17 个历史样本画像，用时约 3.4 秒，输出 `hits=17 rebuilt=0 history_total=17`。
- 对比结论保持一致，说明缓存只改变性能，不改变样本选择逻辑。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 对新增样本报告做人工抽查，校正 RTOS、微内核、unikernel 的关键词和维度判断 |
| P1 | 整理答辩讲稿和截图材料 |
| P2 | 若样本继续扩到 30+，再考虑 BM25/向量召回减少进入 LLM 的历史样本数量 |

## 阶段 16：对比报告重合证据增强

- 日期：2026-06-09
- 目标：修正对比报告“只说可能相似、不充分展示代码证据”的问题，让功能重合和疑似重复线索可追溯、可复核。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 比较模型 | `CompareResult` 新增 `overlap_points` 字段，专门记录功能重合和疑似重复线索 |
| 比较逻辑 | `CompareAgent` 在共享 OS 维度上生成双方证据，包含新仓库和历史仓库的源码 evidence |
| 报告模板 | `Reporter` 新增“功能重合与疑似重复证据”小节 |
| 代码论证 | 证据渲染从只显示 `path:Lx-Ly`，增强为同时显示短代码片段 |
| 边界声明 | 报告明确说明“不直接判定代码抄袭”，只标注需要人工复核的功能重合线索 |
| Self-check | compare 核验纳入 `overlap_points`，证据覆盖统计同步更新 |
| LLM Prompt | LLM 比较 prompt 纳入 `overlap_points`，要求模型不得直接把相似表述为抄袭 |
| 测试 | 新增 reporter 测试，覆盖重合证据小节和代码片段输出；更新 LLM prompt 测试 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python -m compileall src scripts\kernelsage.py
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 5
```

### 观察结果

- 新生成的 `data/reports/compare/xv6-public_vs_history.md` 已包含“功能重合与疑似重复证据”小节。
- 每条重合线索会展示双方源码路径、行号和短代码片段。
- 报告仍保持谨慎边界：只说明功能维度和实现线索重合，不自动判定代码级重复或抄袭。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 人工抽查新版报告，继续修正关键词误命中和弱证据 |
| P1 | 为疑似重复线索增加更细的证据类型，例如函数名重合、文件路径重合、结构体/宏重合 |
| P1 | 整理一份人工审阅后的高质量样例报告用于答辩 |

## 阶段 17：描述报告维度审阅细化

- 日期：2026-06-09
- 目标：让描述报告不再只是维度命中清单，而是更接近导师可读的代码审阅报告。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 报告结构 | 每个 OS 维度改为“结论、分析口径、设计判断、证据表、关键代码片段、相关符号、复核建议” |
| 证据展示 | 对每个维度汇总文件、行号、说明，并展示短代码片段 |
| 未确认维度 | 对未确认维度输出明确说明和补查建议 |
| 符号线索 | 从符号抽取 evidence 中汇总相关函数、结构体等实现线索 |
| 测试 | 增加描述报告测试，确认输出证据表、代码片段和复核建议 |
| 文档 | README 和阶段评审材料同步说明描述报告增强 |

### 成本边界说明

- 本阶段增强的是本地规则版 Markdown 报告，不调用 LLM。
- 默认 `describe` 不消耗 DeepSeek API token。
- 只有显式使用 `--use-llm` 时才会请求在线模型；若后续把更详细 evidence 放入 LLM prompt，才会增加 token。

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python -m compileall src scripts\kernelsage.py
python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public
```

### 观察结果

- 新生成的 `data/reports/describe/xv6-public.md` 已包含证据表、关键代码片段、相关符号和复核建议。
- 对系统调用、文件系统、同步、中断等维度，报告能直接展示源码路径和短代码片段。
- 未确认的内存管理维度会明确标注未确认，并给出补查建议。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 人工抽查新版描述报告，修正弱证据和误命中 |
| P1 | 为报告增加“摘要评分/成熟度等级”但保持证据约束 |
| P1 | 整理一份人工审阅后的高质量样例报告用于答辩 |

## 阶段 18：报告准确率人工抽查与误判修正
- 日期：2026-06-09
- 目标：由系统侧承担第一轮人工抽查，验证描述报告中的关键结论是否真正由源码证据支撑，优先修正误判、漏判和弱证据。

### 抽查样本

| 样本 | 选择原因 |
| --- | --- |
| `xv6-public` | 教学型宏内核，覆盖系统调用、文件系统、页表、驱动等经典机制 |
| `freertos-kernel` | RTOS 内核，容易暴露“系统调用/文件系统/驱动”误判 |
| `sel4` | 微内核，容易暴露文件系统、同步、驱动等维度边界问题 |

### 发现并修正的问题

| 问题类型 | 具体表现 | 修正方式 |
| --- | --- | --- |
| 内存管理漏判 | `xv6-public` 之前未稳定确认 `vm.c`、`kalloc.c` 中的页表和物理页分配实现 | 补充 `walkpgdir`、`mappages`、`kalloc`、`kfree`、`pte_`、`pde_` 等 OS 常见关键词 |
| 文件系统误判 | `fatal` 被 `fat` 命中，`reading/readied/smmu_read_reg32` 被 `readi` 命中 | 关键词匹配改为标识符边界匹配，避免普通英文子串误命中 |
| 系统调用误判 | FreeRTOS 的 `SYSCALL priority`、`SYS_CLK_IRQ`、RISC-V `portYIELD ecall` 被误认为系统调用接口 | 系统调用维度只接受 `syscall` 路径、明确 `sys_` 函数、`ecall` 入口或 `handle_syscall` 类强证据，排除 portable 层 yield/trap 术语 |
| 驱动误判 | 头文件示例注释中的 `Driver/UART/device` 被误判为驱动实现 | 驱动维度要求路径或片段包含具体驱动文件、设备路径或 `ideinit`、`uartinit`、`kbdgetc` 等实现级符号 |
| 同步弱证据 | `clock` 中的 `lock` 子串会污染同步维度证据 | 同步维度改为边界匹配并优先保留 `lock/sync/smp/mutex/semaphore/atomic` 路径或强符号 |
| C 符号伪抽取 | `else if (...) {` 可能被抽成 `fn if` | C 解析器跳过控制流语句，新增回归测试 |

### 已完成验证

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python -m compileall src scripts\kernelsage.py
python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\freertos-kernel --repo-id freertos-kernel --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\sel4 --repo-id sel4 --rebuild-profile-cache
```

### 抽查结论

- 单元测试增加到 20 个并全部通过。
- `xv6-public` 仍能确认调度、内存、系统调用、文件系统、同步、中断、驱动等机制，证据路径集中在 `proc.c`、`vm.c`、`syscall.c`、`fs.c`、`spinlock.c`、`trap.c`、`ide.c` 等真实源码文件。
- `freertos-kernel` 不再误确认系统调用、文件系统和设备驱动；仍确认调度、堆内存、同步和中断/定时器相关机制。
- `sel4` 不再误确认文件系统；仍确认调度、内存、系统调用、同步、中断和驱动相关机制。
- 重新生成的报告保留在 `data/reports/describe/` 下，供人工查看；这些生成物仍不提交仓库。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 继续抽查 compare 报告中的相似性/重复线索，检查是否存在弱证据或过度判断 |
| P1 | 为描述报告增加摘要评分/成熟度等级，但评分必须链接到已确认维度和证据 |
| P2 | 扩展一小组“反例测试仓库”，专门覆盖注释误命中、宏名误命中和路径误导 |

## 阶段 19：描述报告摘要评分与成熟度等级
- 日期：2026-06-10
- 目标：在描述报告中增加可解释的摘要评分，帮助导师和评审快速判断仓库整体成熟度，同时保证评分来自源码证据和 self-check，不引入 LLM 主观打分。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| Reporter | 在描述报告总览后新增“摘要评分”小节 |
| 评分规则 | 采用 100 分本地规则：OS 机制覆盖 80 分、构建入口 10 分、证据健康度 10 分 |
| 维度权重 | 调度、内存、系统调用、文件系统、同步、中断、驱动按重要性加权 |
| 成熟度等级 | 新增 A/B/C/D 四档解释，避免裸分数难以理解 |
| 证据绑定 | 报告列出已确认维度、高置信维度、证据数、证据覆盖率和无效证据数 |
| 成本边界 | 明确评分由本地静态分析派生，不调用 DeepSeek API，不增加 token 成本 |
| 文档 | 新增 `docs/REPORT_SCORE_SOLUTION.md` 记录问题与解决方案 |
| README | 更新核心能力表，补充摘要评分能力 |
| 测试 | 增加 reporter 测试，验证成熟度评分、评分项和维度表输出 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python -m compileall src scripts\kernelsage.py
python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\freertos-kernel --repo-id freertos-kernel --rebuild-profile-cache
```

### 观察结果

- 单元测试增加到 21 个并全部通过。
- `xv6-public` 描述报告输出 A 级，100/100；7 个 OS 维度全部确认，构建入口确认，证据覆盖率 100%。
- `freertos-kernel` 描述报告输出 B 级，70/100；调度、内存、同步、中断确认，系统调用、文件系统、设备驱动保持未确认。
- 评分会显式说明“不是比赛官方评分，也不调用 LLM”，避免黑盒评分和 token 成本误解。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 继续抽查 compare 报告中的相似性/重复线索，检查是否存在弱证据或过度判断 |
| P1 | 整理一份人工审阅后的高质量样例报告用于答辩 |
| P2 | 扩展一小组“反例测试仓库”，专门覆盖注释误命中、宏名误命中和路径误导 |

## 阶段 20：片段级代码相似度检测
- 日期：2026-06-10
- 目标：修正“代码级重复还只是功能重合线索，不是真正相似度检测”的问题，在 compare 报告中增加轻量、可解释的代码片段相似度检测。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 数据模型 | `CompareResult` 新增 `code_similarity_points`，与功能重合线索分开存储 |
| 相似度模块 | 新增 `similarity.py`，实现 evidence 片段 token/结构相似度检测 |
| 弱信号过滤 | 去除注释、字符串、include/define 等预处理行，过滤 include-only、comment-only 和极少共同 token 的弱线索 |
| CompareAgent | 在同一 OS 维度双方都有 evidence 时计算片段级相似度 |
| Reporter | 比较报告新增“代码片段相似度检测”小节 |
| Self-check | 将 `code_similarity_points` 纳入比较报告证据核验 |
| LLM Prompt | LLM 比较 prompt 新增 `code_similarity_points`，要求区分片段相似线索和抄袭裁定 |
| 文档 | 新增 `docs/CODE_SIMILARITY_SOLUTION.md` 记录问题、解决方案和答辩表述 |
| 测试 | 新增相似度检测测试，覆盖正例和弱信号过滤 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python -m compileall src scripts\kernelsage.py
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 5
```

### 观察结果

- 单元测试增加到 26 个并全部通过。
- `xv6-public_vs_history.md` 已新增“代码片段相似度检测”小节。
- 当前样例没有发现达到阈值的片段级代码相似线索，报告保守输出“未发现达到阈值”，避免把 include 或结构体前置声明误报为高相似。
- 报告仍明确说明片段级相似度不是抄袭裁定，需要人工结合完整文件和提交历史复核。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 整理一份人工审阅后的高质量样例报告用于答辩 |
| P1 | 继续抽查 compare 报告，调整相似度阈值和 evidence 选取策略 |
| P2 | 若需要更强代码重复检测，接入函数级归一化、MinHash 或 SimHash |

## 阶段 21：低成本代码级相似线索完善

- 日期：2026-06-10
- 目标：补齐“文件路径重合、函数名重合、结构体/宏重合、代码片段相似度”四类线索，让疑似重复判断更有依据，同时不增加 DeepSeek API 成本。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| Parser | C 解析新增 `#define` 宏定义抽取；收紧结构体识别，只把真实 `struct name {` 定义纳入符号表 |
| CompareAgent | 新增文件路径重合、函数/符号名重合、结构体/类型重合、宏名重合四类本地检测 |
| 片段相似度 | 保留 token/结构 Jaccard 片段相似度，继续过滤注释、include-only 和弱 token 信号 |
| 报告限量 | 代码级相似线索最多保留 30 条，每类最多 6 条，优先展示高价值代表项 |
| Reporter | 比较报告小节改为“代码级相似线索检测”，明确这些只是复核线索，不是抄袭裁定 |
| LLM Prompt | compare prompt 同步说明 code_similarity_points 可能包含路径、符号、结构体/宏和片段线索 |
| 缓存 | 画像缓存 schema 升级到 1.1，避免旧结构体误判缓存继续污染报告 |
| 文档 | 更新 README 与 `docs/CODE_SIMILARITY_SOLUTION.md` |
| 测试 | 新增 parser 和 compare 测试，覆盖结构体使用误判过滤、路径/函数/类型/宏重合输出 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python -m compileall src scripts\kernelsage.py
$env:PYTHONPATH='src'; python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 5 --rebuild-profile-cache
$env:PYTHONPATH='src'; python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 5
```

### 观察结果

- 单元测试增加到 29 个并全部通过。
- `xv6-public_vs_history.md` 已输出“代码级相似线索检测”小节，包含片段相似度、宏名重合、结构体/类型重合、函数/符号名重合和文件路径重合。
- C 结构体误判已修正，`struct proc *p` 这类使用不会再作为结构体定义进入符号重合统计。
- 本阶段全程未调用 LLM，不增加 DeepSeek API token 成本；后续只有显式 `--use-llm` 才会产生在线模型费用。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 人工抽查新 compare 报告中的前 30 条代码级线索，继续降低宏名或通用结构体带来的噪声 |
| P1 | 整理一份高质量样例报告，用于答辩展示系统如何区分功能重合、代码级线索和人工裁定 |
| P2 | 如时间允许，再考虑函数体归一化、MinHash/SimHash 或 AST 级相似度作为增强项 |

## 阶段 22：LLM 比较报告 dry-run 审查

- 日期：2026-06-11
- 目标：解决“LLM 版报告还需要正式试跑”的问题，先用 dry-run 检查 compare prompt 是否具备证据约束、成本控制和防幻觉边界。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| Dry-run | 对 `xv6-public` 执行 compare LLM dry-run，只生成 prompt，不调用 API |
| Prompt 审查 | 检查 prompt 是否包含 `selection_notes`、`overlap_points`、`code_similarity_points`、`self_check` |
| 防幻觉约束 | 确认 prompt 要求不得编造文件名、函数名、行号、算法名称或实现细节 |
| 抄袭边界 | 确认 prompt 要求功能重合和代码级线索只能作为人工复核依据，不能直接裁定抄袭 |
| 创新点边界 | 确认 prompt 要求证据不足时必须写“当前证据不足，未自动确认创新点” |
| 输出审查 | 新增 `audit-llm-report` 命令，本地检查 LLM 报告是否引用越界、缺关键章节或出现越权抄袭措辞 |
| 成本控制 | 本阶段只做 dry-run，不产生 DeepSeek API token 消耗 |
| 文档 | 更新外层 `痛点与解决方案.md`，补充 LLM 试跑三道闸门和答辩表述 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 3 --llm-dry-run
rg -n "不要编造|必须保留|不能直接裁定|当前证据不足|self_check|selection_notes|code_similarity_points|overlap_points" data\reports\prompts\xv6-public.compare.prompt.md
python scripts\kernelsage.py audit-llm-report --prompt data\reports\prompts\xv6-public.compare.prompt.md --report data\reports\compare\xv6-public_vs_history.md
```

### 观察结果

- dry-run prompt 已生成到 `data/reports/prompts/xv6-public.compare.prompt.md`。
- prompt 约 1769 行、约 6 万字符，真实调用时应控制 `--limit`，优先使用 `limit=2` 或 `limit=3`。
- prompt 已包含证据约束、样本选择依据、代码级相似线索、self-check 统计和创新点不足时的保守表达规则。
- 本地审查命令已跑通，对当前规则版 compare 报告输出 `ok=true`；提示缺少 LLM 建议章节属于 warning，不影响 evidence 边界检查。
- 真实 API 试跑尚未执行，需在确认 DeepSeek 余额/API 可用后只做一次小样本调用。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P0 | API 可用后执行一次 `--use-llm --limit 3` 真实比较报告试跑 |
| P0 | 使用 `audit-llm-report` 审查真实 LLM 输出，再人工核查是否存在语义弱化或过度总结 |
| P1 | 若 LLM 输出弱化证据，继续收紧 compare prompt 或增加输出后自检 |

## 阶段 23：参考样本来源分级与获奖案例边界

- 日期：2026-06-11
- 目标：解决“优秀获奖案例还没确认，不能硬标特奖/一等奖样本”的问题，建立可信来源机制，避免报告和 LLM 误用未核验标签。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 数据模型 | `RepoMeta` 新增 `source_tier`、`award_level`、`award_source_url` 字段 |
| Collector | 从 manifest/local meta 读取来源等级，并将旧 `category` 自动映射到新分级 |
| 来源分级 | `contest-case` 映射为 `competition_sample`，`teaching-baseline` 映射为 `teaching_baseline`，`architecture-baseline` 映射为 `architecture_reference` |
| Reporter | 描述报告显示样本来源等级；比较报告声明未核验比赛样本不作为特奖/一等奖背书 |
| Selector 输出 | `selection_notes` 增加历史样本来源等级，便于 LLM 和人工审查识别样本边界 |
| LLM Prompt | 明确禁止把未标注为 `verified_award` 的历史样本称为特奖、一等奖或优秀获奖案例 |
| 缓存 | 画像缓存 schema 升级到 1.2，避免旧画像缺少来源等级字段 |
| 文档 | 更新 README、`docs/STAGE_REVIEW.md` 和外层 `痛点与解决方案.md` |
| 测试 | 新增 collector 来源等级映射测试，更新 reporter 和 LLM prompt 测试 |

### 当前口径

- 当前 18 个参考样本中没有 `verified_award` 已核验获奖案例。
- 公开比赛仓库只能称为 `competition_sample` 比赛作品样本，不能称为特奖/一等奖案例。
- 后续只有拿到官方获奖页面和可靠仓库链接后，才加入 `verified_award` 样本池。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 若拿到官方获奖链接，补充 2-3 个 `verified_award` 样本，并记录 award source |
| P1 | 在答辩材料中强调“样本来源分级，宁缺毋滥”的可信边界 |
| P2 | 后续可为 manifest 增加来源校验脚本，检查 `verified_award` 是否同时填写 `award_level` 和 `award_source_url` |

## 阶段 24：精选样例展示材料

- 日期：2026-06-11
- 目标：补齐“缺少人工审阅后的高质量样例报告”的问题，固定一份可用于演示视频和答辩讲稿的展示材料。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 稳定性样例 | 选择 `xv6-public`，展示经典小型 OS 仓库的稳定识别和比较能力 |
| 比赛场景样例 | 选择 `oskernel2024-aabcb`，展示公开比赛作品样本的分析和比较能力 |
| 报告链路 | 重新生成两类样本的 describe/compare 报告，作为本地展示依据 |
| 展示文档 | 新增 `docs/SHOWCASE_CASE.md`，整理输入仓库、描述报告、对比报告、self-check 和人工点评 |
| README | 增加 `SHOWCASE_CASE.md` 链接，说明其可作为演示视频和答辩讲稿底稿 |
| 边界说明 | 展示文档明确说明样本来源等级、代码级线索不是抄袭裁定、创新性判断需保守解释 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'
python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 3
python scripts\kernelsage.py describe data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb
python scripts\kernelsage.py compare data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --limit 3
```

### 观察结果

- `xv6-public`：描述报告 A 级 100/100，描述 self-check 覆盖率 100%，对比报告覆盖率 100%，适合展示稳定性。
- `oskernel2024-aabcb`：描述报告 A 级 100/100，来源等级为 `competition_sample`，适合展示比赛场景。
- 两个样例均保留“未核验比赛样本不作为特奖/一等奖背书”的边界。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 根据 `docs/SHOWCASE_CASE.md` 录制 3-5 分钟演示视频 |
| P1 | 将展示文档中的人工点评压缩成答辩讲稿口播版 |
| P2 | 若后续接入 `verified_award` 样本，再补充一个获奖案例展示样例 |

## 阶段 25：端到端测试补强

- 日期：2026-06-11
- 目标：回应“测试覆盖还偏少”的问题，在不引入网络、真实 LLM API 或大样本库依赖的前提下，为 describe 和 compare 主流程补充轻量端到端回归测试。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| 测试 fixture | 在测试中动态构造最小 OS 仓库，包含调度、内存、系统调用、文件系统、同步、中断、驱动和 Makefile |
| describe E2E | 新增测试覆盖 `cmd_describe` 从仓库输入到 profile JSON 与 Markdown 描述报告产出 |
| compare E2E | 新增测试覆盖 `cmd_compare` 从新仓库、历史库选择到比较报告产出 |
| 回归断言 | 检查报告关键章节、源码路径、行号证据、历史样本选择和代码级相似线索章节 |
| 隔离性 | 测试使用临时目录和 monkey patch 的 `REPORTS_DIR`/`PROFILES_DIR`/`SAMPLES_DIR`，不污染真实样本库和本地报告 |
| README | 更新当前测试状态和仓库目录中的测试文件清单 |

### 已验证命令

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
$env:PYTHONPATH='src'; python -m compileall src scripts\kernelsage.py tests
```

### 观察结果

- 测试总数从 34 个增加到 36 个，全部通过。
- 新增测试不调用 DeepSeek API，不消耗 token。
- 端到端测试覆盖的是规则版主链路，能防止后续修改导致 describe/compare 报告无法生成、关键章节消失或历史样本选择失效。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 后续如引入真实 LLM 输出，可补一条 dry-run prompt 审计端到端测试 |
| P2 | 若出现新的误判类型，再增加小型反例 fixture 仓库 |

## 阶段 26：真实 LLM 比较报告试跑与审计修正

- 日期：2026-06-11
- 目标：对 `xv6-public` 和 `oskernel2024-aabcb` 各执行一次真实 DeepSeek compare 报告生成，并用本地 `audit-llm-report` 检查证据链和越权表述。

### 已完成任务

| 模块 | 完成内容 |
| --- | --- |
| Dry-run 基准 | 先为两份 compare 生成 prompt，作为审计 evidence 边界 |
| 真实 LLM 试跑 | 对 `xv6-public` 和 `oskernel2024-aabcb` 分别执行 `--use-llm --limit 3` |
| 输出审计 | 使用 `audit-llm-report` 检查 LLM 输出是否引用越界、缺关键章节或出现越权抄袭措辞 |
| 问题发现 | 首次审计发现 DeepSeek 将证据写成 `path:1-3`，未按 `path:L1-L3` 格式输出，导致审计器判定 missing citations |
| 输出归一化 | LLM 报告生成后自动把反引号内的 `path:1-3` 归一化为 `path:L1-L3`，不新增文件或行号 |
| 审计增强 | 审计器支持中文/空格路径，并支持同一文件相邻 evidence 合并覆盖，例如 L11 与 L12 合法覆盖 L11-L12 |
| Prompt 收紧 | compare/profile prompt 明确要求证据引用必须写成反引号代码格式 `path:Lx-Ly`，禁止 `path:10-14` |
| 测试 | 增加 LLM 引用归一化、中文路径审计、相邻 evidence 范围审计和 prompt 格式约束测试 |

### 已验证命令

```powershell
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 3 --llm-dry-run
python scripts\kernelsage.py compare data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --limit 3 --llm-dry-run
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 3 --use-llm
python scripts\kernelsage.py compare data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --limit 3 --use-llm
python scripts\kernelsage.py audit-llm-report --prompt data\reports\prompts\xv6-public.compare.prompt.md --report data\reports\compare\xv6-public_vs_history.md
python scripts\kernelsage.py audit-llm-report --prompt data\reports\prompts\oskernel2024-aabcb.compare.prompt.md --report data\reports\compare\oskernel2024-aabcb_vs_history.md
```

### 观察结果

- `xv6-public` LLM compare 审计通过：allowed evidence 166，cited references 125，issues 0。
- `oskernel2024-aabcb` LLM compare 审计通过：allowed evidence 192，cited references 109，issues 0。
- 两份报告均保留“代码级相似线索不是抄袭裁定”的边界，并保留“当前证据不足，未自动确认创新点”的保守表达。
- 完整测试增加到 39 个并全部通过。
- 本次真实调用消耗 DeepSeek API token；后续重复运行同 prompt 会优先使用本地 `data/llm_cache/` 缓存。

### 下一步计划

| 优先级 | 任务 |
| --- | --- |
| P1 | 人工抽查两份真实 LLM 报告，检查语义是否弱化证据或过度总结 |
| P1 | 将一份通过审计的 LLM compare 报告纳入演示材料，但明确其是“受约束润色”而不是裁判 |
| P2 | 后续如继续接入更多模型，复用同一套 dry-run + audit 闸门 |
