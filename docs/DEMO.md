# KernelSage 演示流程

本文档用于固定答辩和阶段检查时的演示流程。演示目标是让评审直观看到：系统可以输入一个小型 OS 仓库，自动生成结构化画像、描述报告、比较报告，并给出证据核验摘要。

## 演示目标

演示围绕三个问题展开：

1. 系统是否能理解一个小型操作系统仓库的基本结构。
2. 系统是否能围绕操作系统机制生成可核验描述。
3. 系统是否能选择合适历史样本并生成比较报告。

## 演示准备

在项目根目录执行：

```powershell
cd C:\Users\CanhuiBao\Desktop\2026操作系统大赛\proj18-os-agent-compare
```

确认样本仓库已存在：

```powershell
Get-ChildItem data\samples
```

如果缺少样本仓库，先拉取：

```powershell
python scripts\fetch_repos.py
```

## 推荐演示命令

### 1. 端到端演示

```powershell
python scripts\kernelsage.py demo data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2
```

预期输出：

- `data/profiles/rcore-tutorial-v3.json`
- `data/reports/describe/rcore-tutorial-v3.md`
- `data/reports/compare/rcore-tutorial-v3_vs_history.md`

命令行会显示被选中的历史仓库及分数，例如：

```text
selected history repositories:
- zCore: score=...
- xv6-riscv: score=...
```

讲解重点：

- 系统没有按目录顺序取样，而是按画像相似度选择历史仓库。
- 选择依据包括 OS 风格、架构、语言构成、OS 维度重合度和代码规模。
- Markdown 文档不会被当作 OS 机制实现证据，避免文档型仓库误入比较结果。
- 生成物都在 `data/reports/` 和 `data/profiles/` 下，默认不提交仓库。

### 2. 查看描述报告

```powershell
Get-Content -Encoding UTF8 data\reports\describe\rcore-tutorial-v3.md | Select-Object -First 80
```

讲解重点：

- 报告按调度、内存、系统调用、文件系统、同步、中断、驱动 7 个 OS 维度组织。
- 每个关键判断都带源码路径和行号。
- 报告末尾有 self-check 摘要，说明关键结论证据覆盖率和无效证据引用数。

### 3. 查看比较报告

```powershell
Get-Content -Encoding UTF8 data\reports\compare\rcore-tutorial-v3_vs_history.md | Select-Object -First 120
```

讲解重点：

- 报告顶部展示“历史样本选择”，解释为什么选择这些历史仓库。
- 相似点、差异点和可能创新点都保留证据引用。
- 系统不会直接把相似性判定为抄袭，而是输出需要人工复核的依据。

### 4. LLM dry-run 演示

```powershell
python scripts\kernelsage.py describe data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --llm-dry-run
```

讲解重点：

- dry-run 只生成 prompt，不调用 API，不产生费用。
- prompt 中包含 KernelProfile、证据片段和 self-check 摘要。
- prompt 明确要求模型不能编造文件名、函数名、行号或未确认算法细节。

### 5. 真实 LLM 调用

只有在 `.env` 已配置可用 API Key，并确认允许消耗 API 额度时执行：

```powershell
python scripts\kernelsage.py describe data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --use-llm
```

讲解重点：

- 默认命令不会调用 LLM。
- `--use-llm` 才会请求在线模型。
- 请求失败时会自动回退到规则版报告。
- LLM 响应会缓存到 `data/llm_cache/`。

## 答辩讲解顺序

建议讲解顺序：

1. 赛题不是写 OS，而是写分析 OS 仓库的智能体系统。
2. 本项目先建立结构化画像，避免直接让 LLM 读全仓库导致幻觉。
3. 静态分析负责提取事实和证据，LLM 只负责把事实组织成更自然的报告。
4. 比较前先做历史样本选择，避免随机或目录顺序导致比较对象不合理。
5. 每份报告都带证据链和 self-check，便于人工复核。

## 当前可展示亮点

- OS 专用 7 维度画像，而不是通用代码摘要。
- 比较样本按画像相似度选择。
- 关键结论带源码路径和行号。
- 可用 HTML 证据报告展示结论、行号、自检状态和相似度分数。
- 可用 `query-evidence` 直接检索“调度器/页表/系统调用”等源码证据。
- 可用 `manifest-audit` 自检样本库可信度。
- LLM 调用有 dry-run、缓存、失败回退和证据约束。
- 工具可用一条 `demo` 命令完成端到端演示。

## 当前边界

- V1 仍以静态规则和关键词证据为主，不做完整调用图。
- LLM 输出需要继续人工审阅，不能作为最终判定。
- 当前历史样本规模较小，后续可扩展到更多比赛仓库。
- HTML 报告和 query-evidence 是本地展示/检索入口，不改变底层分析结论，也不替代人工复核。

## 演示后清理

如果需要保持工作区干净，可以删除运行生成物：

```powershell
Remove-Item data\profiles,data\reports,data\llm_cache -Recurse -Force -ErrorAction SilentlyContinue
```

`.env` 和 `data/samples/` 是本地数据，已被 `.gitignore` 忽略，不会被提交。
