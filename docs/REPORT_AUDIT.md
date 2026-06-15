# KernelSage 报告人工抽查记录

- 日期：2026-06-11
- 目的：代替人工初审，检查自动生成报告中的证据是否支撑结论，重点关注 RTOS、微内核、unikernel、比赛样本这类容易被关键词误判的仓库。
- 范围：`freertos-kernel`、`sel4`、`includeos`、`oskernel2024-aabcb` 描述报告，以及 `oskernel2024-aabcb_vs_history` 对比报告。

## 抽查口径

| 检查项 | 判断标准 |
| --- | --- |
| 证据支撑 | 关键结论必须能回溯到源码文件、行号或符号定义 |
| 维度误判 | 重点检查系统调用、文件系统、设备驱动、同步、中断等容易被关键词带偏的维度 |
| 符号噪声 | 相关符号不能主要来自 include guard、硬件寄存器宏、注释关键词或测试目录 |
| 相似线索边界 | 代码级相似线索只能作为人工复核入口，不能写成抄袭或已确认重复 |
| 样本边界 | 未核验获奖等级的比赛样本不能称为特奖、一等奖或优秀获奖案例 |

## 已发现并修正的问题

### 1. IncludeOS C++ 覆盖不足

旧逻辑主要识别 Rust/C/Asm，未充分纳入 `.cpp`、`.hpp` 等 C++ 文件，导致 IncludeOS 的文件系统、驱动和内存证据不可靠。

已修正：

- `collector.py` 支持 `.cc/.cpp/.cxx/.hh/.hpp/.hxx`。
- `parser.py` 将 `cpp` 纳入符号抽取，并识别 C++ `class`。
- `analyzer.py` 将 `cpp` 纳入关键词证据检索。
- 缓存 schema 提升到 `1.8`，避免复用旧画像。

复查结果：`includeos` 现在识别 `cpp 118006 LOC`，并能引用 `src/fs/fat.cpp`、`src/fs/mbr.cpp`、`src/drivers/ide.cpp`、`src/drivers/e1000.cpp` 等真实源码证据。

### 2. 宏注释和路径子串导致误判

旧逻辑会把宏定义注释里的 `Lock/thread/device` 等词当成机制命中，也会把 `profile.cpp` 中的 `file` 子串误判为文件系统路径。

已修正：

- 宏符号只用宏名参与直接关键词匹配，不再让注释文字触发机制结论。
- 路径 hint 改为按路径 token 匹配，避免 `profile` 命中 `file`。
- `syscall` 符号 hint 移除过泛的 `sys`，避免 `system_log`、`boot_sys` 等路径误入。
- 低优先级目录中的符号，如 `test/`、`docs/`、`examples/`，不再支撑机制符号列表。
- 中断维度的符号匹配不再使用过泛的 `exception`，减少 `CookieException` 这类类名噪声。

### 3. 系统调用 stub 被过度解读

IncludeOS 存在 syscall 入口、兼容层和 stub，但源码片段包含 `ENOSYS`、`not implemented`、`stubtrace` 等标记。旧报告容易被理解成完整 syscall 实现。

已修正：

- `analyzer.py` 增加 syscall stub 标记识别。
- 若证据中出现 stub/未实现标记，系统调用维度降为 `medium`。
- 报告明确写成“系统调用入口或兼容层线索”，而不是“完整系统调用实现”。

复查结果：`includeos` 的系统调用维度现在为 `medium`，并说明应按接口线索解读。

## 样本抽查结论

### FreeRTOS

结论基本可信，但必须保守表达。

- 调度、内存、同步、中断维度有明确 RTOS 源码证据。
- 文件系统未确认是合理结果。
- 设备驱动未确认是更稳妥的结果，避免把 FreeRTOS 的 errno 或平台适配宏误解为通用驱动框架。
- 系统调用维度为 `medium`，应理解为 MPU/port layer、trap 或 syscall-like 平台适配线索，不等同于 Unix-like syscall。

### seL4

结论基本可信。

- 文件系统未确认是合理结果，符合微内核边界。
- 系统调用、同步、中断、驱动等维度有内核源码证据。
- 仍有少量宏型符号较弱，例如硬件 `STRIDE` 常量，不应在答辩中夸大为调度算法证据。

### IncludeOS

C++ 覆盖修正后可信度明显提高。

- 文件系统和驱动证据已落到 `src/fs/*`、`src/drivers/*`。
- 系统调用维度已降级为兼容层或 stub 线索。
- 该样本适合作为 C++/unikernel 覆盖能力展示，但不适合作为“完整 syscall 实现”展示。

### oskernel2024-aabcb

描述报告整体可信。

- 调度、内存、系统调用、文件系统、同步、中断、驱动七个维度均有源码路径和符号证据。
- 对比报告选择 `xv6-riscv`、`OSKernel2024-NQOS`、`OSKernel2024-ouye` 作为最相似样本，选择理由包含风格、架构、语言构成、OS 维度和规模接近度。
- 对比报告明确写明“不直接判定代码抄袭”，代码级相似线索只作为人工复核入口。

## Golden 校准样例

为回应“缺少人工标注黄金报告”的评审意见，本轮固定了 2 份 golden 样例：

| Golden 文件 | 对应自动报告 | 校准重点 |
| --- | --- | --- |
| `docs/golden/xv6-public.describe.golden.md` | `data/reports/describe/xv6-public.md` | 校准七维 OS 机制结论是否被强源码证据支撑 |
| `docs/golden/oskernel2024-aabcb.compare.golden.md` | `data/reports/compare/oskernel2024-aabcb_vs_history.md` | 校准历史样本选择、代码级相似线索分级和“不裁定抄袭”边界 |

审核结论：

- `xv6-public` 描述报告通过 golden 校准。自动报告 self-check 为 16/16，但 golden 不直接依赖覆盖率，而是补充核对 `scheduler()`、`walkpgdir/mappages()`、`syscall()`、inode、spinlock、trap 和 IDE/KBD 中断等强证据。
- `oskernel2024-aabcb` 对比报告通过 golden 校准。`PGSIZE/TRAMPOLINE/TRAPFRAME/KSTACK`、`proc/context/cpu`、`swtch` 等属于强复核线索；UART、PLIC、virtio 路径等硬件通用线索被降级为弱到中等线索。
- 两份 golden 均明确说明：相似线索不是抄袭裁定，self-check 不是官方评分，未核验比赛样本不能硬标获奖等级。

## 剩余风险

| 风险 | 当前处理 | 后续优化方向 |
| --- | --- | --- |
| 关键词仍非语义理解 | 已增加证据行号、符号过滤和人工复核提示 | V2 引入 AST/调用图或更细粒度规则 |
| 少量宏符号仍偏弱 | 过滤注释、路径噪声和低优先级目录 | 为 driver/interrupt/memory 建立维度专用白名单 |
| 高证据覆盖不等于高质量 | 已固定 1 份描述 golden 和 1 份对比 golden，说明人工校准口径 | 后续规则变化后同步复核 golden |
| 历史样本库仍有限 | 报告保留来源等级和覆盖边界，已根据官方提供的 `os-funtion-winners.md` 补入 3 个 2024 功能赛道一等奖样本 | 继续抽查新增获奖样本报告，避免获奖样本引入新的误判 |

## 本轮验证

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
$env:PYTHONPATH='src'; python -m compileall src scripts\kernelsage.py tests
python scripts\kernelsage.py describe data\samples\freertos-kernel --repo-id freertos-kernel --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\includeos --repo-id includeos --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\sel4 --repo-id sel4 --rebuild-profile-cache
python scripts\kernelsage.py describe data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --rebuild-profile-cache
python scripts\kernelsage.py compare data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --limit 3
```

当前验证结果：64 个 unittest 全部通过，`compileall` 通过；本地已重新生成四份描述报告和一份对比报告，生成物保留在 ignored 的 `data/reports/` 目录供人工查看。Golden 校准材料见 `docs/GOLDEN_CASES.md` 和 `docs/golden/`。
