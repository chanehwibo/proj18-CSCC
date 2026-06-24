# KernelSage 新手傻瓜式操作手册与演示步骤

本文档面向第一次接触本项目的同学和演示录屏操作者。照着本文档逐步执行，可以完成 KernelSage 的全流程功能演示、报告查看、LLM 可选增强、审计验证和回归测试。

文档目标不是解释所有源码细节，而是让操作者知道：

- 每一步输入什么命令。
- 命令跑对时屏幕上应该出现什么现象。
- 生成的文件在哪个路径下。
- 打开文件后应该重点展示哪里。
- 录屏时旁边可以配什么红色说明文字，证明项目功能成功。

## 0. 演示总览

建议使用 PowerShell 作为演示终端。所有命令默认在项目根目录执行：

```text
C:\Users\CanhuiBao\Desktop\2026操作系统大赛\proj18-os-agent-compare
```

推荐演示样本使用 `xv6-public`，原因是它是经典小型 OS，结构清晰，报告稳定，适合新手录制演示视频。

完整演示会覆盖 9 类能力：

| 顺序 | 功能 | 展示目的 |
| --- | --- | --- |
| 1 | 环境检查 | 确认 Python、Git、项目路径和样本目录正常 |
| 2 | `manifest-audit` | 证明样本库来源、repo_id、获奖来源和本地 HEAD 可自检 |
| 3 | `demo --html` | 一条命令生成画像、描述报告、对比报告和 HTML 报告 |
| 4 | 描述报告 | 展示七维 OS 机制画像和源码行号证据 |
| 5 | 对比报告 | 展示历史样本选择、相似点、差异点和人工复核边界 |
| 6 | HTML 证据报告 | 用浏览器展示更适合答辩的可视化证据视图 |
| 7 | `query-evidence` | 演示现场提问时如何检索调度器、页表、系统调用证据 |
| 8 | LLM dry-run、真实调用和审计 | 展示可控 LLM 增强、prompt 文件、API 调用和越界审计 |
| 9 | unittest 和 compileall | 证明项目不是只能跑样例，而是有自动化回归测试 |

## 1. 演示前准备

### 1.1 打开 PowerShell

操作：

1. 按 `Win` 键。
2. 输入 `PowerShell`。
3. 打开 Windows PowerShell。

如果录屏，请先把 PowerShell 窗口放大，字体调大到观众能看清。

建议旁边红字说明：

```text
所有功能都通过本地 CLI 命令演示，不依赖前端服务。
```

### 1.2 进入官方项目目录

命令：

```powershell
cd "C:\Users\CanhuiBao\Desktop\2026操作系统大赛\proj18-os-agent-compare"
```

检查当前位置：

```powershell
Get-Location
```

正确现象：

```text
Path
----
C:\Users\CanhuiBao\Desktop\2026操作系统大赛\proj18-os-agent-compare
```

如果路径不是上面这个项目目录，后续命令可能找不到 `scripts\kernelsage.py`。

建议旁边红字说明：

```text
当前进入的是官方 GitLab 仓库对应的项目目录，不操作旧仓库。
```

### 1.3 设置终端编码和 Python 模块路径

命令：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONPATH='src'
```

正确现象：

- 命令执行后通常没有输出。
- 没有红色报错就是成功。

说明：

- `$env:PYTHONPATH='src'` 是必须的，它让 Python 能找到 `src\os_agent` 包。
- 每次新开 PowerShell 窗口，都要重新执行这一组命令。

如果忘记设置，可能出现：

```text
ModuleNotFoundError: No module named 'os_agent'
```

建议旁边红字说明：

```text
PYTHONPATH 指向 src 后，CLI 可以加载本项目的智能体模块。
```

### 1.4 检查 Python 和 Git

命令：

```powershell
python --version
git --version
```

正确现象：

```text
Python 3.11.x
git version 2.x.x.windows.x
```

版本号不必完全一致，但建议：

- Python 为 3.11 或更高。
- Git 能正常输出版本。

如果 `git --version` 提示找不到命令，说明 Git 没有加入 PATH，需要先修复 PATH 后再拉取样本。已拉取好的样本可以先完成本地演示。

### 1.5 检查样本目录

命令：

```powershell
Get-ChildItem data\samples | Select-Object Name
```

正确现象：

应该能看到多行样本目录，例如：

```text
Name
----
arceos
freertos-kernel
os-tutorial
oskernel2024-aabcb
xv6-public
xv6-riscv
...
```

至少需要看到：

- `xv6-public`
- `os-tutorial`
- `xv6-riscv`
- `manifest.json`

如果 `data\samples\xv6-public` 不存在，先执行样本拉取。

拉取全部样本：

```powershell
python scripts\fetch_repos.py
```

只拉取本手册演示需要的核心样本：

```powershell
python scripts\fetch_repos.py --only xv6-public --only os-tutorial --only xv6-riscv
```

正确现象：

- 屏幕会出现 git clone 或 skip 已存在仓库的信息。
- 结束后 `data\samples` 下出现对应目录。

注意：

- 首次拉取需要网络。
- 样本源码属于本地数据，默认被 `.gitignore` 忽略，不提交仓库。

建议旁边红字说明：

```text
历史样本库是本地数据源，后续所有对比都基于这些可复核源码。
```

## 2. 功能一：样本库可信度自检

### 2.1 运行 manifest-audit

命令：

```powershell
python scripts\kernelsage.py manifest-audit
```

当前正确输出示例：

```text
Manifest audit summary
- manifest: C:\Users\CanhuiBao\Desktop\2026操作系统大赛\proj18-os-agent-compare\data\samples\manifest.json
- samples_dir: C:\Users\CanhuiBao\Desktop\2026操作系统大赛\proj18-os-agent-compare\data\samples
- repos: 21
- errors: 0
- warnings: 0
- issues: none
```

关键成功标志：

- `repos: 21`
- `errors: 0`
- `warnings: 0`
- `issues: none`

如果样本没全部拉取，`repos` 仍可能是 21，但 warnings 可能提示本地目录缺失。正式录屏前建议确保为 `0 error、0 warning`。

建议红框框选：

- `repos: 21`
- `errors: 0`
- `warnings: 0`
- `issues: none`

建议旁边红字说明：

```text
样本库可信度自检通过：21 个样本的 ID、来源记录、本地目录和 HEAD 信息可核验。
```

### 2.2 JSON 模式，适合说明可接入 CI

命令：

```powershell
python scripts\kernelsage.py manifest-audit --json
```

正确现象：

- 输出 JSON。
- JSON 中应包含 `"errors": []` 或 error 数量为 0。
- JSON 中应包含样本数量和 issue 列表。

建议旁边红字说明：

```text
同一套自检可以输出 JSON，便于后续接入自动化检查。
```

## 3. 功能二：指定输入仓库并跑完整主流程

这一节对应比赛场景里的主流程：给系统一个待检测 OS 仓库路径，系统先生成该仓库画像，再和历史样本库做查重式对比。

### 3.1 输入仓库是什么

KernelSage 的输入仓库就是命令里的第一个路径。例如下面命令中的 `data\samples\xv6-public` 就是本次被分析、被比对的输入仓库：

```powershell
python scripts\kernelsage.py demo data\samples\xv6-public --repo-id xv6-public --limit 2 --jobs 4 --html
```

输入仓库可以来自三种位置：

- 已经拉取到 `data\samples\` 的公开样本，适合稳定录屏演示。
- 现场临时克隆到 `data\inputs\new-input` 的新仓库，适合展示“给一个新仓库作为输入”；`data\inputs\` 是本地临时目录，不提交。
- 任意本地 OS 仓库路径，例如 `D:\repos\student-os`。

历史比对库来自 `data\samples\manifest.json` 和本地 `data\samples\` 目录。输入仓库不需要提交到本项目仓库；提交的是样本清单、拉取脚本和最终生成的报告。若输入仓库本身也位于 `data\samples\`，系统会跳过它自身，只和其他历史样本比对。

### 3.2 用比赛作品样本作为输入仓库

下面这组命令更像评委关心的查重场景：把 `oskernel2024-aabcb` 当作待检测输入仓库，和历史样本库做对比。

先根据 `data\samples\manifest.json` 拉取这个公开比赛仓库：

```powershell
python scripts\fetch_repos.py --only oskernel2024-aabcb
```

该命令会从下面的公开地址浅克隆到 `data\samples\oskernel2024-aabcb`：

```text
https://gitlab.eduxiji.net/T202410269994328/project2608132-273971.git
```

再对本地输入仓库进行画像和历史比对：

```powershell
python scripts\kernelsage.py describe data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --html
python scripts\kernelsage.py compare data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --history data\samples --limit 3 --jobs 4 --html
```

成功后重点查看：

```powershell
notepad data\reports\describe\oskernel2024-aabcb.md
notepad data\reports\compare\oskernel2024-aabcb_vs_history.md
start data\reports\html\oskernel2024-aabcb.describe.html
start data\reports\html\oskernel2024-aabcb_vs_history.html
```

如果现场要换成一个全新的输入仓库，可以先克隆到 `data\inputs\new-input`，再运行同样的 `describe` 和 `compare`：

```powershell
git clone <仓库地址> data\inputs\new-input
python scripts\kernelsage.py describe data\inputs\new-input --repo-id new-input --html
python scripts\kernelsage.py compare data\inputs\new-input --repo-id new-input --history data\samples --limit 3 --jobs 4 --html
```

建议旁边红字说明：

```text
系统输入的是一个待检测 OS 仓库路径，历史样本库只作为对比基线；第三方源码不随项目提交，评委可根据 manifest 复现拉取。
```

### 3.3 运行离线规则版 demo

`demo` 是最适合录屏的核心命令。它会自动完成：

- 构建或读取 `KernelProfile` 画像。
- 生成 Markdown 描述报告。
- 选择最相近的历史样本。
- 生成 Markdown 对比报告。
- 生成 HTML 证据报告。

命令：

```powershell
python scripts\kernelsage.py demo data\samples\xv6-public --repo-id xv6-public --limit 2 --jobs 4 --html
```

当前正确输出示例：

```text
demo repo: data\samples\xv6-public
profile cache hit: xv6-public -> ...\data\profiles\xv6-public.json
html report written: ...\data\reports\html\xv6-public.describe.html
profile written: ...\data\profiles\xv6-public.json
report written: ...\data\reports\describe\xv6-public.md
profile cache hit: xv6-public -> ...\data\profiles\xv6-public.json
html report written: ...\data\reports\html\xv6-public_vs_history.html
selected history repositories:
- os-tutorial: score=8.08; 同属 teaching-monolithic 风格; 架构重合度 1.00; 语言构成相似度 0.48
- xv6-riscv: score=6.79; 语言构成相似度 0.97; OS 维度重合度 1.00; 代码规模接近度 0.84
profile cache summary: hits=20 rebuilt=0 history_total=20
compare report written: ...\data\reports\compare\xv6-public_vs_history.md
demo outputs:
- profile: ...\data\profiles\xv6-public.json
- describe report: ...\data\reports\describe\xv6-public.md
- compare report: ...\data\reports\compare\xv6-public_vs_history.md
```

正确现象：

- 出现 `profile written` 或 `profile cache hit`，二者都代表画像阶段成功。
- 出现 `report written`，代表描述报告生成成功。
- 出现 `selected history repositories`，代表系统自动选出了历史对比对象。
- 出现 `compare report written`，代表对比报告生成成功。
- 出现 `html report written`，代表 HTML 报告生成成功。

说明：

- 第一次运行可能显示 `profile cache rebuilt`，不是错误。
- 后续运行可能显示 `profile cache hit`，表示命中画像缓存，速度更快。
- `--jobs 4` 表示并行构建历史样本画像，样本变多时比串行更快。

建议红框框选：

- `selected history repositories`
- `os-tutorial`
- `xv6-riscv`
- `compare report written`
- `html report written`

建议旁边红字说明：

```text
一条 demo 命令完成画像、描述、历史对比和 HTML 证据报告生成，主流程闭环成功。
```

### 3.4 本步骤生成的文件

命令执行成功后，重点展示以下路径：

| 文件 | 用途 | 是否提交仓库 |
| --- | --- | --- |
| `data\profiles\xv6-public.json` | 结构化 OS 画像 | 否 |
| `data\reports\describe\xv6-public.md` | 单仓库描述报告 | 是，最终演示报告已提交 |
| `data\reports\compare\xv6-public_vs_history.md` | 历史样本对比报告 | 是，最终演示报告已提交 |
| `data\reports\html\xv6-public.describe.html` | 描述报告 HTML 证据视图 | 是，最终演示报告已提交 |
| `data\reports\html\xv6-public_vs_history.html` | 对比报告 HTML 证据视图 | 是，最终演示报告已提交 |

检查文件是否存在：

```powershell
Test-Path data\profiles\xv6-public.json
Test-Path data\reports\describe\xv6-public.md
Test-Path data\reports\compare\xv6-public_vs_history.md
Test-Path data\reports\html\xv6-public.describe.html
Test-Path data\reports\html\xv6-public_vs_history.html
```

正确现象：

```text
True
True
True
True
True
```

建议旁边红字说明：

```text
五个核心产物全部生成：profile 是本地缓存，最终 Markdown/HTML 演示报告已随仓库提交，便于评委直接查看。
```

## 4. 功能三：查看单仓库描述报告

### 4.1 在终端快速查看 Markdown

命令：

```powershell
Get-Content -Encoding UTF8 data\reports\describe\xv6-public.md | Select-Object -First 120
```

正确现象：

你应该能看到 `xv6-public` 的描述报告内容，通常包含：

- 项目概览。
- 调度、内存、系统调用、文件系统、同步、中断、驱动等 OS 维度。
- 源码文件路径和行号。
- 核验摘要或 self-check 结果。

建议红框框选：

- 报告标题。
- 某个机制下面的源码路径，例如 `proc.c:L...`、`vm.c:L...`、`syscall.c:L...`。
- 报告末尾的核验摘要。

建议旁边红字说明：

```text
描述报告不是泛泛总结，每个关键机制都绑定源码路径和行号，评审可以回到源码复核。
```

### 4.2 用记事本打开 Markdown 文件

命令：

```powershell
notepad data\reports\describe\xv6-public.md
```

正确现象：

- 记事本打开 `xv6-public.md`。
- 文档内容是中文 Markdown 报告。
- 能看到分章节结构和证据列表。

录屏展示建议：

1. 先展示报告标题。
2. 滚动到 OS 机制维度部分。
3. 停在带源码行号的证据列表。
4. 最后滚动到核验摘要。

建议旁边红字说明：

```text
系统先做静态分析形成 KernelProfile，再生成面向人类阅读的 OS 描述报告。
```

## 5. 功能四：查看历史样本对比报告

### 5.1 在终端快速查看对比报告

命令：

```powershell
Get-Content -Encoding UTF8 data\reports\compare\xv6-public_vs_history.md | Select-Object -First 160
```

正确现象：

报告中应该包含以下信息：

- 新仓库 `xv6-public`。
- 被选中的历史仓库，通常包括 `os-tutorial` 和 `xv6-riscv`。
- 选择理由，例如同属教学单体内核、架构重合、语言构成相似、OS 维度重合。
- 相似点、差异点、可能创新点或未确认创新点。
- 需要人工复核的线索。
- 代码级相似线索不是抄袭裁定的边界说明。

建议红框框选：

- `历史样本选择` 或相似对象列表。
- `os-tutorial`、`xv6-riscv`。
- `相似线索不是抄袭裁定` 相关文字。
- 核验摘要。

建议旁边红字说明：

```text
系统会先解释为什么选这些历史样本，再输出相似点和差异点，不直接做抄袭裁定。
```

### 5.2 用记事本打开对比报告

命令：

```powershell
notepad data\reports\compare\xv6-public_vs_history.md
```

正确现象：

- 记事本打开对比报告。
- 能看到历史样本选择和对比结论。
- 能看到源码证据或代码级复核线索。

录屏展示建议：

1. 先展示比较对象选择。
2. 展示相似点和差异点。
3. 展示待人工复核项。
4. 强调系统只给复核线索，不代替评审裁决。

建议旁边红字说明：

```text
对比报告把相似性、差异性和人工复核边界分开写，降低误判风险。
```

## 6. 功能五：查看 HTML 证据报告

HTML 报告适合演示视频和答辩，因为浏览器展示比纯 Markdown 更直观。

### 6.1 打开描述 HTML

命令：

```powershell
start data\reports\html\xv6-public.describe.html
```

正确现象：

- 默认浏览器打开一个本地 HTML 文件。
- 页面展示描述报告相关的结构化信息。
- 能看到证据文件、行号、自检状态等内容。

建议红框框选：

- 页面标题。
- 证据文件列表。
- 行号。
- self-check 或核验状态。

建议旁边红字说明：

```text
HTML 报告把 Markdown 中的证据链变成可展示视图，更适合答辩现场讲解。
```

### 6.2 打开对比 HTML

命令：

```powershell
start data\reports\html\xv6-public_vs_history.html
```

正确现象：

- 浏览器打开对比 HTML。
- 能看到历史样本、相似度分数、证据文件、核验状态等内容。

建议红框框选：

- 相似度分数或历史样本列表。
- 证据路径和行号。
- self-check 状态。

建议旁边红字说明：

```text
对比 HTML 能直观看到相似度和证据来源，便于评审快速定位关键差异。
```

说明：

- HTML 是静态本地文件，不需要启动 Web 服务。
- 即使 Markdown 使用 `--use-llm` 增强，HTML 仍由结构化 profile/compare 数据渲染，主要用于证据展示。

## 7. 功能六：现场证据检索 query-evidence

这个功能适合答辩现场被问到某个 OS 概念时使用。例如评委问：“你们能不能找出调度器、页表、系统调用相关源码？”

### 7.1 搜索调度器、页表、系统调用

命令：

```powershell
python scripts\kernelsage.py query-evidence "调度器/页表/系统调用" --limit 5
```

当前正确输出示例：

```text
Evidence query: 调度器/页表/系统调用
- repos scanned: 21
- source files scanned: 1639
- hits: 5

1. [33.5] oskernel2024-hfut666 (competition_sample) src/mm/memory_set.rs:L6-L10
   matched: frame_allocator, frame_alloc, memory, alloc, frame, page, sv39, mm
   snippet: ...
2. [32.5] oskernel2024-aabcb (competition_sample) kernel/proc/proc.c:L200-L204
   matched: pagetable, mappages, pgsize, frame, page, proc, pte_, trap, pte, vm
   snippet: ...
```

正确现象：

- `repos scanned` 显示扫描了多少样本仓库。
- `source files scanned` 显示扫描了多少源码文件。
- `hits` 大于 0。
- 每条结果都有 repo、来源等级、文件路径、行号、匹配词和代码片段。

建议红框框选：

- `repos scanned: 21`
- `source files scanned: 1639`
- `hits: 5`
- 某条结果的 `repo_id`、源码路径和 `L行号-L行号`。

建议旁边红字说明：

```text
query-evidence 可以把中文 OS 概念映射到真实源码位置，支持现场可解释检索。
```

### 7.2 只查某一个仓库

命令：

```powershell
python scripts\kernelsage.py query-evidence "系统调用" --repo-id xv6-public --limit 3
```

正确现象：

- 只返回 `xv6-public` 相关结果。
- 结果中应该能看到 syscall 相关源码文件或函数。

建议旁边红字说明：

```text
可以限定 repo_id，直接回答某个样本项目中证据在哪里。
```

### 7.3 JSON 输出

命令：

```powershell
python scripts\kernelsage.py query-evidence "系统调用" --repo-id xv6-public --limit 3 --json
```

正确现象：

- 输出机器可读 JSON。
- 其中包含命中的仓库、文件、行号、分数和片段。

建议旁边红字说明：

```text
检索结果支持 JSON，后续可以接入 Web 展示或自动评测流程。
```

## 8. 功能七：LLM dry-run，生成提问稿但不调用 API

dry-run 的意思是“试跑”。在本项目里，`--llm-dry-run` 只生成要发给 LLM 的 prompt 文件，不真正请求 API，所以：

- 不消耗 API 额度。
- 不需要网络。
- 可以人工检查 prompt 是否包含正确证据。
- 适合答辩时说明 LLM 是受控使用的。

### 8.1 生成 compare prompt

命令：

```powershell
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 2 --jobs 4 --llm-dry-run
```

当前正确输出示例：

```text
profile cache hit: xv6-public -> ...\data\profiles\xv6-public.json
LLM dry-run prompt written to ...\data\reports\prompts\xv6-public.compare.prompt.md
selected history repositories:
- os-tutorial: score=8.08; 同属 teaching-monolithic 风格; 架构重合度 1.00; 语言构成相似度 0.48
- xv6-riscv: score=6.79; 语言构成相似度 0.97; OS 维度重合度 1.00; 代码规模接近度 0.84
profile cache summary: hits=20 rebuilt=0 history_total=20
compare report written: ...\data\reports\compare\xv6-public_vs_history.md
```

关键成功标志：

```text
LLM dry-run prompt written to ...\data\reports\prompts\xv6-public.compare.prompt.md
```

建议红框框选：

- `LLM dry-run prompt written`
- `data\reports\prompts\xv6-public.compare.prompt.md`

建议旁边红字说明：

```text
dry-run 只生成 LLM 提问稿，不调用 API，便于审计 prompt 和控制成本。
```

### 8.2 打开 prompt 文件

命令：

```powershell
notepad data\reports\prompts\xv6-public.compare.prompt.md
```

正确现象：

打开的 prompt 文件中应该包含：

- 任务要求。
- 新仓库画像。
- 历史样本选择结果。
- 源码证据片段。
- 要求模型不能编造文件名、函数名、行号。
- 要求模型保留人工复核边界。

建议红框框选：

- prompt 中的 evidence 或源码片段。
- 禁止编造证据的约束。
- 人工复核边界要求。

建议旁边红字说明：

```text
LLM 的输入不是整仓库裸读，而是经过静态分析整理出的证据包和约束说明。
```

## 9. 功能八：真实 LLM 调用和本地审计

这一节是可选演示。只有在本地 `.env` 已经配置 DeepSeek API key，并且允许消耗 API 额度时执行。

重要安全要求：

- 不要打开 `.env`。
- 不要展示 API key。
- 不要把 `.env`、`data\llm_cache`、`data\reports\prompts`、`data\reports\tmp`、`data\profiles`、`data\samples`、`data\inputs` 提交到仓库；`data\reports\describe`、`data\reports\compare`、`data\reports\html` 中的最终演示报告可以提交。

### 9.1 检查当前 LLM 模型名

命令：

```powershell
python -c "from os_agent.llm import load_settings; s=load_settings(); print(s.model)"
```

正确现象：

```text
deepseek-v4-pro
```

建议旁边红字说明：

```text
当前默认使用 deepseek-v4-pro，模型配置来自本地环境，不展示密钥。
```

### 9.2 先生成审计用 prompt 文件

`audit-llm-report` 命令需要读取 prompt 文件。真实 `--use-llm` 调用会在内存中审计 prompt，但不会自动把 prompt 文件保存到磁盘；只有 `--llm-dry-run` 会写出 `data\reports\prompts\*.prompt.md`。

因此，如果要在演示中单独运行 `audit-llm-report`，请先执行下面两条 dry-run 命令。

命令：

```powershell
python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public --llm-dry-run
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 2 --jobs 4 --llm-dry-run
```

正确现象：

```text
LLM dry-run prompt written to ...\data\reports\prompts\xv6-public.describe.prompt.md
LLM dry-run prompt written to ...\data\reports\prompts\xv6-public.compare.prompt.md
```

说明：

- 这一步只保存 prompt，不调用 API。
- dry-run 会临时写出规则版 Markdown 报告。
- 下一步真实 `--use-llm` 会重新生成 Markdown 报告，所以建议先 dry-run，再真实调用，再审计。

建议旁边红字说明：

```text
先保存审计用 prompt 文件，后续可以逐条核对 LLM 报告是否越过证据边界。
```

### 9.3 记录调用前 cache 数量

命令：

```powershell
(Get-ChildItem data\llm_cache -Filter *.json -ErrorAction SilentlyContinue | Measure-Object).Count
```

正确现象：

- 输出一个数字，例如 `8`。
- 这个数字表示当前本地 LLM 缓存文件数量。

说明：

- 如果目录不存在，输出可能是 `0`。
- cache 是本地生成物，不提交仓库。

### 9.4 发起真实 LLM demo

为了尽量避免命中旧缓存，可以临时设置一个新的 temperature。数值可以改成之前没用过的小数，例如 `0.239`、`0.241`。

命令：

```powershell
$env:LLM_TEMPERATURE='0.241'
python scripts\kernelsage.py demo data\samples\xv6-public --repo-id xv6-public --limit 2 --jobs 4 --use-llm --html
```

正确现象：

- 命令能完整结束。
- 出现 `report written`、`compare report written`、`html report written`。
- 如果 API 正常，Markdown 报告由 LLM 增强生成。
- 如果 API 异常，系统会 fallback 到规则版报告，这也是可靠性设计的一部分。

如果录制“真实 API 成功调用”，建议同时看 cache 数量是否增加。

调用后检查：

```powershell
(Get-ChildItem data\llm_cache -Filter *.json -ErrorAction SilentlyContinue | Measure-Object).Count
```

正确现象：

- 如果没有命中缓存且 API 调用成功，数字通常会比调用前增加。
- 如果数字没有增加，可能是命中了缓存，或本次调用 fallback 到规则版。

建议红框框选：

- `--use-llm`
- `report written`
- `compare report written`
- cache 数量变化。

建议旁边红字说明：

```text
LLM 是可选增强：成功时提升报告表达，失败时自动回退规则版，不影响主流程交付。
```

### 9.5 审计 LLM 描述报告

这里的 prompt 文件来自 9.2 的 dry-run，报告文件来自 9.4 的真实 `--use-llm` 运行。

命令：

```powershell
python scripts\kernelsage.py audit-llm-report --report-type profile --prompt data\reports\prompts\xv6-public.describe.prompt.md --report data\reports\describe\xv6-public.md
```

正确输出示例：

```json
{
  "ok": true,
  "allowed_evidence_count": 38,
  "cited_reference_count": 47,
  "issues": []
}
```

关键成功标志：

```text
"ok": true
```

建议旁边红字说明：

```text
LLM 描述报告通过本地审计，未发现越界引用证据。
```

### 9.6 审计 LLM 对比报告

这里的 prompt 文件来自 9.2 的 dry-run，报告文件来自 9.4 的真实 `--use-llm` 运行。

命令：

```powershell
python scripts\kernelsage.py audit-llm-report --report-type compare --prompt data\reports\prompts\xv6-public.compare.prompt.md --report data\reports\compare\xv6-public_vs_history.md
```

正确现象：

- JSON 中 `"ok": true`。
- `issues` 可能为空，也可能出现 severity 为 `warning` 的提示。
- 只要 `"ok": true`，说明没有触发阻断级问题。

示例：

```json
{
  "ok": true,
  "allowed_evidence_count": 129,
  "cited_reference_count": 129,
  "issues": []
}
```

建议红框框选：

- `"ok": true`
- `allowed_evidence_count`
- `cited_reference_count`

建议旁边红字说明：

```text
LLM 输出必须经过证据审计，不能凭空新增不存在的文件、行号或抄袭裁定。
```

## 10. 功能九：完整自动化测试

测试是证明项目稳定性的最后一步。录屏可以放在最后 20 到 30 秒。

### 10.1 运行 unittest

命令：

```powershell
python -m unittest discover -s tests
```

当前正确输出尾部：

```text
----------------------------------------------------------------------
Ran 92 tests in 0.715s

OK
```

实际耗时可能不同，但必须看到：

- `Ran 92 tests`
- `OK`

如果中间出现少量测试命令打印，例如 `profile written`、`compare report written`、`LLM failed or audit rejected output, falling back...`，这是测试用例在验证 CLI 和 fallback 行为，不是失败。

建议红框框选：

- `Ran 92 tests`
- `OK`

建议旁边红字说明：

```text
92 个 unittest 覆盖 CLI、报告、LLM 审计、缓存、fetch、安全边界、HTML 和检索能力。
```

### 10.2 运行语法编译检查

命令：

```powershell
python -m compileall -q src scripts\kernelsage.py scripts\fetch_repos.py tests
```

正确现象：

- 没有任何输出。
- 没有红色报错。
- 回到命令提示符。

说明：

- `compileall -q` 安静模式下无输出就是成功。
- 如果有语法错误，会显示具体 Python 文件和行号。

建议旁边红字说明：

```text
compileall 无输出表示源码、脚本和测试文件语法检查通过。
```

## 11. 录制 5 分钟功能演示视频建议脚本

这里的视频只演示作品功能，不包含 PPT 汇报和口头答辩。

### 11.1 时间分配

| 时间 | 画面 | 操作 | 旁边说明文字 |
| --- | --- | --- | --- |
| 0:00-0:25 | README 或赛题页面 | 展示项目名和定位 | `面向小型 OS 仓库的智能分析比对系统` |
| 0:25-0:45 | PowerShell | 进入项目目录，设置 `PYTHONPATH` | `本地 CLI 演示，不依赖前端服务` |
| 0:45-1:10 | PowerShell | 运行 `manifest-audit` | `21 个样本 0 error 0 warning，样本库可自检` |
| 1:10-1:50 | PowerShell | 指定输入仓库并运行 `demo --html` | `输入仓库完成画像、描述、对比和 HTML 报告` |
| 1:50-2:25 | 记事本 | 打开描述报告 | `七维 OS 机制画像，关键结论带源码路径和行号` |
| 2:25-3:00 | 记事本 | 打开对比报告 | `自动选择历史样本，输出相似、差异和人工复核线索` |
| 3:00-3:35 | 浏览器 | 打开两个 HTML 报告 | `证据、行号、自检状态和相似度分数可视化` |
| 3:35-4:05 | PowerShell | 运行 `query-evidence` | `输入中文 OS 概念，返回真实源码位置` |
| 4:05-4:35 | PowerShell/记事本 | 运行 `--llm-dry-run` 并打开 prompt | `只生成提问稿，不调用 API，LLM 输入可审计` |
| 4:35-4:50 | PowerShell | 可选展示真实 LLM 审计结果 | `LLM 输出通过证据边界审计` |
| 4:50-5:00 | PowerShell | 展示 unittest 尾部 | `92 个 unittest 通过，工程质量闭环` |

### 11.2 推荐录屏命令顺序

录屏时建议按下面顺序复制执行。

```powershell
cd "C:\Users\CanhuiBao\Desktop\2026操作系统大赛\proj18-os-agent-compare"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONPATH='src'
```

```powershell
python scripts\kernelsage.py manifest-audit
```

```powershell
python scripts\kernelsage.py demo data\samples\xv6-public --repo-id xv6-public --limit 2 --jobs 4 --html
```

```powershell
notepad data\reports\describe\xv6-public.md
```

```powershell
notepad data\reports\compare\xv6-public_vs_history.md
```

```powershell
start data\reports\html\xv6-public.describe.html
start data\reports\html\xv6-public_vs_history.html
```

```powershell
python scripts\kernelsage.py query-evidence "调度器/页表/系统调用" --limit 5
```

```powershell
python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 2 --jobs 4 --llm-dry-run
notepad data\reports\prompts\xv6-public.compare.prompt.md
```

如果需要在视频中展示真实 LLM 调用和审计，把下面这组命令插入 dry-run 后面。注意不要打开 `.env`。

```powershell
python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public --llm-dry-run
$env:LLM_TEMPERATURE='0.241'
python scripts\kernelsage.py demo data\samples\xv6-public --repo-id xv6-public --limit 2 --jobs 4 --use-llm --html
python scripts\kernelsage.py audit-llm-report --report-type profile --prompt data\reports\prompts\xv6-public.describe.prompt.md --report data\reports\describe\xv6-public.md
python scripts\kernelsage.py audit-llm-report --report-type compare --prompt data\reports\prompts\xv6-public.compare.prompt.md --report data\reports\compare\xv6-public_vs_history.md
```

```powershell
python -m unittest discover -s tests
python -m compileall -q src scripts\kernelsage.py scripts\fetch_repos.py tests
```

如果 5 分钟时间不够，`audit-llm-report` 和 `compileall` 可以只展示命令和成功结果，不展开解释。

## 12. 生成文件展示清单

演示结束后，可以打开这些文件证明功能完整。

| 展示文件 | 打开命令 | 应该展示的内容 | 成功说明文字 |
| --- | --- | --- | --- |
| `data\profiles\xv6-public.json` | `notepad data\profiles\xv6-public.json` | 结构化画像 JSON | `源码被转成可复用的 KernelProfile` |
| `data\reports\describe\xv6-public.md` | `notepad data\reports\describe\xv6-public.md` | 七维 OS 描述、证据行号、核验摘要 | `描述报告可人工复核` |
| `data\reports\compare\xv6-public_vs_history.md` | `notepad data\reports\compare\xv6-public_vs_history.md` | 历史样本选择、相似点、差异点、复核边界 | `对比报告不直接裁定抄袭，只给证据线索` |
| `data\reports\html\xv6-public.describe.html` | `start data\reports\html\xv6-public.describe.html` | 描述报告 HTML 证据视图 | `HTML 更适合答辩展示` |
| `data\reports\html\xv6-public_vs_history.html` | `start data\reports\html\xv6-public_vs_history.html` | 对比 HTML、相似度、证据、自检 | `相似度和证据来源可视化` |
| `data\reports\prompts\xv6-public.compare.prompt.md` | `notepad data\reports\prompts\xv6-public.compare.prompt.md` | LLM prompt 和证据约束 | `LLM 输入可审计，不是黑箱调用` |

其中 `data\reports\describe`、`data\reports\compare` 和 `data\reports\html` 的最终演示报告已提交到仓库，便于评委直接查看；`data\profiles`、`data\reports\prompts`、`data\llm_cache` 和样本源码仍是本地运行数据。

## 13. 常见问题排查

### 13.1 报错：找不到 `os_agent`

现象：

```text
ModuleNotFoundError: No module named 'os_agent'
```

原因：

没有设置 `PYTHONPATH`。

修复命令：

```powershell
$env:PYTHONPATH='src'
```

然后重新执行刚才失败的命令。

### 13.2 中文输出乱码

现象：

- PowerShell 中中文显示成乱码。
- Markdown 打开后中文不正常。

修复命令：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING='utf-8'
```

如果记事本仍乱码，可以用 VS Code 打开 Markdown，并选择 UTF-8 编码。

### 13.3 `data\samples\xv6-public` 不存在

现象：

```text
FileNotFoundError
```

或命令提示样本路径不存在。

修复命令：

```powershell
python scripts\fetch_repos.py --only xv6-public --only os-tutorial --only xv6-riscv
```

如果要完整样本库：

```powershell
python scripts\fetch_repos.py
```

### 13.4 manifest-audit 有 warning

可能原因：

- 某些样本目录未拉取。
- 本地 `.kernelsage_meta.json` 缺少 HEAD 信息。
- manifest 中新增样本但还未采集。

处理方式：

1. 先确认 `data\samples` 下样本目录是否完整。
2. 重新执行 `python scripts\fetch_repos.py`。
3. 再执行 `python scripts\kernelsage.py manifest-audit`。

正式演示建议达到：

```text
errors: 0
warnings: 0
issues: none
```

### 13.5 LLM 调用失败

可能原因：

- `.env` 中没有 API key。
- 网络不可用。
- 中转站 API 临时异常。
- 模型返回格式异常。

正确理解：

- 这不影响规则版主流程。
- 系统会 fallback 到规则版报告。
- 默认演示可以只使用 `--llm-dry-run`，不消耗 API。

不要做的事：

```text
不要在录屏中打开 .env。
不要展示 API key。
不要把 .env 提交到仓库。
```

### 13.6 unittest 中出现 fallback 字样

现象：

测试过程中看到：

```text
LLM failed or audit rejected output, falling back to rule-based report
```

这是正常现象。

原因：

测试用例故意构造了越界 LLM 输出，用来验证系统能拒绝不合格报告并回退规则版。

真正的成功标志是最后：

```text
Ran 92 tests
OK
```

## 14. 安全和提交边界

以下内容是本地数据或密钥，不能提交；最终演示报告目录除外：

| 路径 | 原因 |
| --- | --- |
| `.env` | 包含本地 API key |
| `data\samples\` | 本地拉取的样本源码 |
| `data\inputs\` | 现场临时克隆的输入仓库 |
| `data\reports\prompts\` | LLM dry-run prompt，可能包含长证据包 |
| `data\reports\tmp\` | 临时审计文件 |
| `data\profiles\` | 本地画像缓存 |
| `data\llm_cache\` | LLM 响应缓存 |
| `__pycache__\` | Python 运行缓存 |

检查工作区：

```powershell
git status --short --ignored
```

正确现象：

- 如果没有修改源码和文档，普通 tracked 区域应为空。
- 可能看到 `!! .env`、`!! data/profiles/`、`!! data/llm_cache/`、`!! data/samples/...`、`!! data/inputs/`、`!! data/reports/prompts/` 或 `!! data/reports/tmp/`，这表示它们被忽略，不会提交；最终演示报告目录 `data/reports/describe`、`data/reports/compare`、`data/reports/html` 已纳入仓库。

建议旁边红字说明：

```text
本地密钥、样本源码、LLM 缓存和 prompt/tmp 产物保持 ignored；最终演示报告随仓库提交，便于评委查看。
```

## 15. 最终成功判定清单

正式录屏或验收前，按下面清单逐项确认。

| 检查项 | 成功标准 |
| --- | --- |
| 进入项目目录 | `Get-Location` 指向 `proj18-os-agent-compare` |
| 编码和模块路径 | 已执行 `$env:PYTHONPATH='src'` |
| 样本库 | `data\samples\xv6-public` 存在 |
| manifest-audit | `repos: 21`、`errors: 0`、`warnings: 0`、`issues: none` |
| demo 主流程 | 出现 `report written`、`compare report written`、`html report written` |
| 描述报告 | `data\reports\describe\xv6-public.md` 存在，包含 OS 机制和证据 |
| 对比报告 | `data\reports\compare\xv6-public_vs_history.md` 存在，包含历史样本选择 |
| HTML 报告 | 两个 HTML 文件能用浏览器打开 |
| query-evidence | `hits` 大于 0，结果包含源码路径和行号 |
| dry-run | 生成 `data\reports\prompts\xv6-public.compare.prompt.md` |
| LLM 审计 | `audit-llm-report` 输出 `"ok": true` |
| unittest | `Ran 92 tests` 且 `OK` |
| compileall | 无输出、无报错 |
| 安全边界 | 不展示 `.env`；提交最终演示报告，但不提交样本源码、临时输入仓库、profile、prompt 和 LLM 缓存 |

全部满足后，可以说明：

```text
KernelSage 已完成从样本库可信度自检、OS 画像、描述报告、历史对比、HTML 证据展示、可解释检索、LLM 受控增强到自动化测试的全流程功能演示。
```
