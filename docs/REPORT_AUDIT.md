# KernelSage 报告人工抽查记录

- 日期：2026-06-11
- 目的：代替人工初审，检查自动生成报告中的证据是否支撑结论，尤其关注 RTOS、微内核、unikernel 和比赛样本这类容易被关键词误判的仓库。
- 范围：`freertos-kernel`、`sel4`、`includeos`、`oskernel2024-aabcb` 描述报告，以及 `oskernel2024-aabcb_vs_history` 对比报告。

## 抽查口径

| 检查项 | 判断标准 |
| --- | --- |
| 证据支撑 | 报告中的关键结论必须能回溯到源码文件、行号或符号定义 |
| 维度误判 | 重点检查系统调用、文件系统、设备驱动等容易误命中的 OS 维度 |
| 相似线索边界 | 代码级相似线索只能作为人工复核入口，不能写成抄袭或已确认重复 |
| 样本边界 | 未核验获奖等级的比赛样本不能被称为特奖、一等奖或优秀获奖案例 |

## 发现并修正的问题

### 1. IncludeOS C++ 源码识别不足

抽查 `includeos` 时发现，旧扫描逻辑主要识别 Rust/C/Asm，未充分纳入 `.cpp`、`.hpp` 等 C++ 文件，导致 unikernel 样本的文件系统、驱动和内存相关证据不够可信。

已完成修正：

- `collector.py` 增加 `.cc`、`.cpp`、`.cxx`、`.hh`、`.hpp`、`.hxx` 的 C++ 语言识别。
- `parser.py` 将 `cpp` 纳入符号抽取范围，并识别 C++ `class` 定义。
- `analyzer.py` 将 `cpp` 纳入关键词证据检索范围。
- `profile_cache.py` 将缓存 schema 升级到 `1.7`，避免复用旧画像。

修正后 `includeos` 描述报告显示：`cpp 118006 LOC`、1170 个已扫描文件、约 128146 行可分析文本，并能引用 `src/fs/fat.cpp`、`src/fs/mbr.cpp`、`src/drivers/ide.cpp`、`src/drivers/e1000.cpp` 等真实源码证据。

### 2. 相关符号存在宏噪声

抽查 `freertos-kernel` 和 `sel4` 时发现，部分“相关符号包括”会因为文件路径命中而带出 include guard、版本宏或硬件寄存器宏。这类符号不一定错误，但如果无差别展示，会降低报告的可读性和说服力。

已完成修正：

- `_symbol_hits` 改为优先检查符号名和签名中的直接关键词命中。
- 只有 `fn`、`struct`、`class`、`enum`、`trait` 这类上下文符号允许通过路径命中进入结果。
- 宏只有在符号名或签名直接命中关键词时才保留，避免 `INC_TASK_H` 等路径型噪声进入调度维度。
- 新增回归测试，确认 `struct tskTaskControlBlock` 和 `schedule` 可保留，`INC_TASK_H` 不再作为相关调度符号输出。

## 样本抽查结论

### FreeRTOS

结论基本可信，但需要保守表述：

- 调度、内存、同步、中断维度有明确 RTOS 源码证据。
- 文件系统未确认是合理结果。
- 系统调用和设备驱动维度仍应理解为 RTOS port layer、硬件端口和平台适配线索，不宜等同于 Unix-like syscall 或完整通用驱动框架。
- 相关符号仍可能包含部分硬件寄存器宏，后续可进一步做维度专用过滤。

### seL4

结论基本可信：

- 文件系统未确认是合理结果，符合微内核仓库边界。
- 系统调用、调度、内存、同步、中断、驱动维度有较强内核证据。
- 报告中仍有一些宏型符号，但大多来自地址空间、页表、设备寄存器或平台硬件路径，属于可解释证据，不应夸大为高级功能实现。

### IncludeOS

C++ 修正后报告可信度明显提高：

- 文件系统和驱动证据已经落到 `src/fs/*` 与 `src/drivers/*`。
- 系统调用维度需要谨慎解释。报告中出现 `src/musl/syscall_n.cpp`、`src/arch/x86_64/syscall_entry.cpp` 等线索，表示 syscall 兼容层、入口或 stub 处理，并不等同于传统宏内核 syscall 完整实现。
- 该样本适合作为 C++/unikernel 覆盖能力的展示样例。

### oskernel2024-aabcb

描述报告整体可信：

- 调度、内存、系统调用、文件系统、同步、中断、驱动七个维度均有源码路径与符号证据。
- 对比报告能输出功能重合、代码级相似线索、宏名重合、类型重合、函数名重合和文件路径重合。
- 报告明确保留“不直接判定代码抄袭”的边界，这一点符合比赛答辩口径。

## 对比报告抽查结论

`oskernel2024-aabcb_vs_history.md` 的对比结果可作为人工复核入口：

- 与 `xv6-riscv`、`OSKernel2024-NQOS` 等样本的相似性选择理由清楚，包含风格、架构、语言构成、OS 维度和规模接近度。
- 功能重合章节能按 OS 维度列出双方 evidence。
- 代码级相似线索包含片段相似度、宏名重合、结构体/类型重合、函数/符号名重合和文件路径重合。
- 报告没有把相似线索写成抄袭裁定，仍要求结合完整文件和提交历史进行人工复核。

## 剩余风险

| 风险 | 当前处理 | 后续优化方向 |
| --- | --- | --- |
| 兼容层或 stub 被识别为完整机制 | 报告中保留人工复核建议 | 增加 syscall subtype，例如 `entry`、`wrapper`、`stub`、`full_dispatch` |
| 宏证据仍偏多 | 已过滤纯路径命中的无关宏 | 为 driver、interrupt、memory 建立更细的宏白名单和黑名单 |
| 高置信度不等于高成熟度 | 摘要评分依赖维度覆盖和 evidence，不代表官方评分 | 增加人工标注 golden report 作为校准样例 |
| 历史样本库仍有限 | 报告保留来源等级和覆盖边界 | 获取官方获奖链接后补充 verified_award 样本 |

## 本轮验证

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
$env:PYTHONPATH='src'; python -m compileall src scripts\kernelsage.py tests
python scripts\kernelsage.py describe data\samples\freertos-kernel --repo-id freertos-kernel --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\includeos --repo-id includeos --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\sel4 --repo-id sel4 --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --rebuild-profile-cache
```

当前测试结果：48 个 unittest 全部通过，`compileall` 通过。
