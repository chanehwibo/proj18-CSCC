# Golden 对比报告：OSKernel2024-aabcb vs history

- 审核日期：2026-06-13
- 输入仓库：`data/samples/oskernel2024-aabcb`
- 自动报告：`data/reports/compare/oskernel2024-aabcb_vs_history.md`
- 审核方式：Codex 按人工审核口径核对历史样本选择、相似证据和边界表述
- 人工审核结论：通过，但必须保守解释代码级相似线索

## 自动报告基线

自动对比报告选择的 Top 3 历史样本为：

| 排名 | 历史样本 | 选择理由摘要 | 人工审核 |
| --- | --- | --- | --- |
| 1 | `xv6-riscv` | 同属 independent 风格，RISC-V 架构重合，语言和 OS 维度相似 | 合理 |
| 2 | `oskernel2024-nqos` | 同属比赛作品样本，风格、架构和 OS 维度接近 | 合理，但获奖等级未核验 |
| 3 | `oskernel2024-ouye` | 同属比赛作品样本，架构和维度重合 | 合理，但仓库内包含实验材料和派生代码，解释要更保守 |

报告 self-check 结果为关键结论 63 条、含证据关键结论 63 条、无效证据引用 0 条、未确认关键结论 0 条。

## 强线索人工校准

| 线索类型 | 新项目证据 | 历史样本证据 | 审核结论 | 校准口径 |
| --- | --- | --- | --- | --- |
| 内存布局宏 | `include/common.h:L30` 定义 `PGSIZE`；`include/memlayout.h:L43-L49` 定义 `TRAMPOLINE`、`TRAPFRAME`、`KSTACK` | `xv6-riscv/kernel/riscv.h:L352` 定义 `PGSIZE`；`xv6-riscv/kernel/memlayout.h:L44-L59` 定义 `TRAMPOLINE`、`KSTACK`、`TRAPFRAME` | 强复核线索 | 命名、常量和用户态 trampoline 布局高度接近，足以提示人工复核设计来源 |
| 进程和上下文结构 | `include/proc/cpu.h:L7` 定义 `cpu`；`include/proc/proc.h:L17` 定义 `context`；`include/proc/proc.h:L100` 定义 `proc` | `xv6-riscv/kernel/proc.h:L2-L24` 定义 `context/cpu`；`xv6-riscv/kernel/proc.h:L82-L100` 定义 `proc` | 强复核线索 | 结构命名和进程模型接近，应进入人工对比，但仍不能直接判定复制 |
| 上下文切换符号 | `kernel/proc/swtch.S:L3-L7` 声明并定义 `swtch` | `xv6-riscv/kernel/swtch.S:L3-L9` 声明并定义 `swtch` | 中高复核线索 | RISC-V 小内核常见 `swtch` 命名，但与进程结构组合后有复核价值 |
| 系统调用入口 | `user/syscall_num.h:L8` 定义 `SYS_fork`；`kernel/syscall/syscall.c:L14` 将 `SYS_fork` 绑定到 `sys_fork` | `xv6-riscv/kernel/syscall.h` 和 `xv6-riscv/kernel/syscall.c` 包含同类编号和分发表 | 中高复核线索 | 系统调用编号不必相同，但编号表加分发表说明路线相近 |

## 弱线索和降级规则

| 线索类型 | 证据 | 人工处理 |
| --- | --- | --- |
| UART 寄存器宏 | `kernel/dev/uart.c:L11-L15` 与 `xv6-riscv/kernel/uart.c:L24-L28` 都出现 `RHR`、`THR`、`IER`、`IER_TX_ENABLE` | 只能作为弱到中等线索。16550 UART 寄存器命名来自硬件约定，不能单独证明代码来源 |
| PLIC 常量 | `include/memlayout.h:L23-L24` 与 `xv6-riscv/kernel/memlayout.h:L30-L31` 都出现 `PLIC_PRIORITY`、`PLIC_PENDING` | 只能作为弱线索。PLIC 地址布局是 RISC-V 平台通用知识 |
| 同名路径 | `kernel/dev/uart.c`、`include/dev/virtio.h`、`kernel/fs/fs.c`、`kernel/proc/proc.c` 与 `xv6-riscv` 有同名或近似路径 | 只能提示人工定位文件，不能作为代码重复裁定 |
| 比赛样本相互接近 | `oskernel2024-nqos`、`oskernel2024-ouye` 与 aabcb 有多维重合 | 需要强调来源未核验，且比赛样本可能共享教学基线或实验路线 |

## 边界审查

自动报告中“功能重合与疑似重复证据”章节已明确说明不直接判定代码抄袭，代码级相似线索检测章节也写明结果不是抄袭裁定。该边界表达合格，golden 样例必须继续保留。

需要在答辩中强调：

- `oskernel2024-aabcb` 当前是公开比赛作品样本，不是已核验获奖样本；
- `oskernel2024-nqos` 和 `oskernel2024-ouye` 的获奖等级未核验，不能作为获奖背书；
- 与 `xv6-riscv` 的相似更多说明技术路线和实现骨架接近，是否构成代码复用必须结合完整文件、提交历史和比赛规则人工判断；
- “可能创新点”在当前参考库范围内未确认是合理输出，不能为了展示效果强行编造。

## Golden 期望输出

一份合格的 `oskernel2024-aabcb` 对比报告应满足：

- 历史样本选择理由同时包含风格、架构、语言、OS 维度和规模接近度；
- 功能重合章节覆盖七个 OS 维度，但明确这是功能层面的可复核重合；
- 代码级相似线索分为宏名、结构体/类型、函数/符号、路径和片段，不混为一个结论；
- 对 UART、PLIC、virtio 这类硬件通用线索降级解释；
- 全文不得出现“已确认抄袭”“代码重复成立”“获奖优秀样本证明”等越界表述。

## 不合格输出示例

以下表述不应出现在 golden 级对比报告中：

- “aabcb 与 xv6-riscv 有同名宏，因此可以确认抄袭。”
- “`RHR`、`THR` 等 UART 宏相同，说明核心代码重复。”
- “OSKernel2024-NQOS 和 OSKernel2024-ouye 是已核验获奖项目。”
- “当前参考库未发现差异，所以没有创新点。”

## 结论

`oskernel2024-aabcb_vs_history` 可以作为 KernelSage 的对比 golden 样例。它的价值在于同时包含强复核线索和必须降级解释的通用线索，适合校准系统是否能把“相似”写成证据入口，而不是越权裁定。
