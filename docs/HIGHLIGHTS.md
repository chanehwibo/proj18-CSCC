# KernelSage 特色与亮点

本文档记录 KernelSage 当前已经落地的工程亮点、处理方案和答辩表述，便于和外层答辩材料 `特色与亮点.md` 保持一致。

## 总体定位

KernelSage 是面向小型操作系统仓库的源码证据驱动分析比对智能体。系统不直接替代评审裁决，而是把 OS 机制画像、源码证据、历史样本比较和风险边界整理成可复核报告。

核心原则：

- 证据优先：结论尽量绑定源码文件、行号、片段和符号。
- OS 语义优先：围绕调度、内存、系统调用、文件系统、中断、驱动、同步七维机制建模。
- 边界清晰：相似性线索只作为人工复核入口，不直接写成抄袭裁定。
- LLM 受控：LLM 只做可选文本增强，失败或审计不通过时回退规则报告。
- 本地可演示：核心命令不依赖网络，适合答辩现场运行。

## 亮点一：源码证据链优先

### 特色

报告不仅输出“实现了哪些 OS 机制”，还输出对应源码路径、行号、代码片段和相关符号。

### 处理方案

- 仓库扫描提取源码、目录、README/docs、构建入口和语言分布。
- Rust/C/C++/Assembly 轻量符号解析，抽取函数、结构体、宏、impl 和汇编符号。
- `KernelProfile` 保存七维机制画像及证据。
- `selfcheck` 校验证据文件和行号，避免报告脱离源码。

### 答辩表述

我们不是先写结论再找依据，而是先建立源码证据链，再生成报告。评审可以从每个判断回到源码复核。

## 亮点二：七维 OS 机制画像

### 特色

系统按 OS 领域机制分析项目，而不是只统计代码量、语言和目录。

### 处理方案

- 七维画像：调度、内存管理、系统调用、文件系统、中断、驱动、同步。
- 每个维度结合关键词、路径 hint、符号和片段判断。
- 对 syscall stub、兼容层入口、测试目录符号、宏注释误命中等边界做降噪。

### 答辩表述

项目评价口径贴近操作系统赛题本身，关注机制实现和证据，而不是泛化仓库指标。

## 亮点三：分层历史样本库

### 特色

参考库当前包含 21 个代表性样本，覆盖教学基线、真实系统路线、往届比赛作品和已核验获奖案例。

### 处理方案

- 通过 manifest 管理 `repo_id`、URL、来源等级、奖项和来源链接。
- 样本选择时结合语言、架构、项目风格、OS 机制画像和规模。
- 已核验获奖案例必须同时记录奖项和官方来源。

### 答辩表述

我们不追求无边界堆样本数量，而是用代表性样本覆盖主要技术路线，并在报告中说明比较范围。

## 亮点四：manifest-audit 样本库可信度自检

### 特色

`manifest-audit` 可以现场检查样本库可信度，回答“样本 ID 是否安全、获奖来源是否记录、本地样本是否完整”等问题。

### 处理方案

- 检查 `repo_id` 安全，避免路径穿越。
- 检查 URL、奖项等级、官方来源、本地目录和 HEAD 记录。
- 支持 `--json` 与 `--strict`，便于演示或接入 CI。

### 演示命令

```powershell
$env:PYTHONPATH='src'
python scripts\kernelsage.py manifest-audit
python scripts\kernelsage.py manifest-audit --json
```

## 亮点五：HTML 证据报告

### 特色

Markdown 报告之外可生成静态 HTML，集中展示结论、证据文件、行号、自检状态和相似度分数。

### 处理方案

- `describe`、`compare`、`describe-all`、`demo` 支持 `--html`。
- HTML 报告复用 self-check，不绕过证据校验。
- 即使 Markdown 使用 `--use-llm` 增强，HTML 仍由结构化 profile/compare 数据渲染，是证据展示视图，不直接复刻 LLM 文本。
- 默认输出到 `data/reports/html/`，作为本地生成物不提交仓库。

### 演示命令

```powershell
$env:PYTHONPATH='src'
python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public --html
python scripts\kernelsage.py compare data\samples\xv6-riscv --history data\samples --repo-id xv6-riscv --limit 3 --html
```

## 亮点六：query-evidence 可解释源码检索

### 特色

`query-evidence` 输入“调度器/页表/系统调用”等概念后，返回相关样本、源码位置、行号、片段和匹配词。

### 处理方案

- `indexer.py` 构建本地源码索引，读取 Rust/C/C++/Assembly。
- `retriever.py` 做中文/英文概念扩展，映射到 OS 画像关键词。
- 按行命中、路径上下文和内核路径优先级排序。
- 支持 `--repo-id`、`--limit`、`--max-files-per-repo` 和 `--json`。

### 演示命令

```powershell
$env:PYTHONPATH='src'
python scripts\kernelsage.py query-evidence "调度器/页表/系统调用" --limit 5
python scripts\kernelsage.py query-evidence "系统调用" --repo-id xv6-public --limit 3 --json
```

### 边界

该命令是静态检索入口，不是完整语义证明；最终仍需要结合 describe/compare 报告和人工复核。

## 亮点七：LLM 受控增强和失败回退

### 特色

系统支持 DeepSeek/OpenAI-compatible API，但默认规则版不调用在线模型。LLM 输出必须受证据和审计约束。

### 处理方案

- `--use-llm` 显式启用模型。
- `--llm-dry-run` 只生成 prompt 文件，不调用 API。
- 默认模型配置为 `deepseek-v4-pro`。
- `audit-llm-report` 按 profile/compare 类型检查 LLM 是否引用不存在证据、越界确认创新点或写成裁定。
- API 异常、JSON 异常、字段缺失、审计失败都会 fallback 到规则版报告。
- `.env`、`data/llm_cache/` 等本地敏感数据不提交。

### 答辩表述

LLM 在这里不是裁判，而是受控的文本生成组件。结论来自源码证据和规则分析。

## 亮点八：相似性比较边界明确

### 特色

系统输出相似点、差异点、可能创新点和疑似重复线索，但不直接裁定抄袭。

### 处理方案

- 历史样本选择先输出选择理由。
- 相似度综合项目风格、架构、语言、机制画像和规模。
- 代码级相似只展示路径、符号、片段和分数。
- compare evidence 按新仓库和历史仓库 root 分别校验。

### 答辩表述

系统负责把可复核线索整理出来，最终判断仍由评审结合完整代码、提交历史和上下文完成。

## 亮点九：工程化质量闭环

### 特色

项目把审核发现的问题持续固化为规则和测试，而不是只修当前样例。

### 处理方案

- 当前 83 个 unittest 覆盖 CLI、报告、LLM 审计、fetch、self-check、HTML 和检索。
- `compileall` 检查语法完整性。
- 报告人工抽查结果进入 parser/analyzer/self-check 规则。
- `DEVELOPMENT_LOG.md` 记录阶段性设计、取舍和验证结果。

### 答辩表述

我们的质量保障不是靠一次性人工检查，而是通过可重复运行的测试和研发记录形成闭环。

## 亮点十：本地优先、可离线演示

### 特色

核心能力可以本地运行，不依赖在线模型和外部网络。

### 处理方案

- `profile`、`describe`、`compare`、`manifest-audit`、`query-evidence` 均可本地运行。
- LLM 是可选增强，不影响规则版主流程。
- 样本、报告、画像缓存和 LLM cache 作为本地生成物 ignored。
- HTML 报告是静态文件，无需前端服务。

## 推荐答辩演示顺序

1. 样本库可信度自检：`python scripts\kernelsage.py manifest-audit`
2. 单仓库描述报告：`python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public --html`
3. 历史样本对比：`python scripts\kernelsage.py compare data\samples\xv6-riscv --history data\samples --repo-id xv6-riscv --limit 3 --jobs 4 --html`
4. 现场源码检索：`python scripts\kernelsage.py query-evidence "调度器/页表/系统调用" --limit 5`
5. LLM 边界说明：`python scripts\kernelsage.py compare data\samples\xv6-riscv --history data\samples --repo-id xv6-riscv --llm-dry-run`

## 总结

KernelSage 的核心亮点不是“能生成一份报告”，而是把 OS 仓库分析拆成可追溯、可比较、可审计、可演示的工程链路。源码证据链保证结论可复核，七维机制画像保证赛题相关性，样本库和 manifest-audit 保证比较来源可信，HTML 和 query-evidence 提升答辩展示能力，LLM 审计与 fallback 则保证 AI 增强不会越过证据边界。
