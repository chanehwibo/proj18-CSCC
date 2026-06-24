# OSKernel2024-HFUT666 比较报告

- 对比历史仓库：OSKernel2024-NQOS, xv6-riscv, OSKernel2024-aabcb, ArceOS
- 生成时间：2026-06-08T02:40:53.030443+00:00

## 历史样本选择

- OSKernel2024-NQOS：score=10.23；同属 independent 风格; 架构重合度 1.00; 语言构成相似度 0.13; OS 维度重合度 1.00; 代码规模接近度 0.96
- xv6-riscv：score=9.87；同属 independent 风格; 架构重合度 1.00; 语言构成相似度 0.03; OS 维度重合度 1.00; 代码规模接近度 0.82
- OSKernel2024-aabcb：score=9.73；同属 independent 风格; 架构重合度 1.00; 语言构成相似度 0.07; OS 维度重合度 1.00; 代码规模接近度 0.59
- ArceOS：score=9.43；同属 independent 风格; 架构重合度 0.33; 语言构成相似度 0.61; OS 维度重合度 1.00; 代码规模接近度 0.55

## 相似点

- 与 OSKernel2024-NQOS 同属 independent 风格。（置信度：medium）
- 与 OSKernel2024-NQOS 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/mod.rs:L4-L8`：关键词命中
  - `kernel/uart.c:L1-L4`：关键词命中
- 与 OSKernel2024-NQOS 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L1-L5`：关键词命中
  - `kernel/fs.c:L1-L3`：关键词命中
- 与 OSKernel2024-NQOS 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/trap/init.rs:L3-L7`：关键词命中
  - `kernel/plic.c:L6-L10`：关键词命中
- 与 OSKernel2024-NQOS 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mm/mod.rs:L2-L6`：关键词命中
  - `kernel/vm.c:L10-L14`：关键词命中
- 与 OSKernel2024-NQOS 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/task/mod.rs:L6-L10`：关键词命中
  - `kernel/proc.c:L4-L8`：关键词命中
- 与 OSKernel2024-NQOS 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/block/mod.rs:L1-L5`：关键词命中
  - `kernel/spinlock.c:L1-L3`：关键词命中
- 与 OSKernel2024-NQOS 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
  - `kernel/trap.c:L12-L16`：关键词命中
- 与 OSKernel2024-NQOS 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）
- 与 xv6-riscv 同属 independent 风格。（置信度：medium）
- 与 xv6-riscv 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/mod.rs:L4-L8`：关键词命中
  - `kernel/uart.c:L1-L4`：关键词命中
- 与 xv6-riscv 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L1-L5`：关键词命中
  - `kernel/fs.c:L1-L3`：关键词命中
- 与 xv6-riscv 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/trap/init.rs:L3-L7`：关键词命中
  - `kernel/plic.c:L6-L10`：关键词命中
- 与 xv6-riscv 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mm/mod.rs:L2-L6`：关键词命中
  - `kernel/vm.c:L12-L16`：关键词命中
- 与 xv6-riscv 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/task/mod.rs:L6-L10`：关键词命中
  - `kernel/proc.c:L4-L8`：关键词命中
- 与 xv6-riscv 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/block/mod.rs:L1-L5`：关键词命中
  - `kernel/spinlock.c:L1-L3`：关键词命中
- 与 xv6-riscv 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
  - `kernel/trap.c:L12-L16`：关键词命中
- 与 xv6-riscv 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）
- 与 OSKernel2024-aabcb 同属 independent 风格。（置信度：medium）
- 与 OSKernel2024-aabcb 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/mod.rs:L4-L8`：关键词命中
  - `kernel/dev/uart.c:L1-L3`：关键词命中
- 与 OSKernel2024-aabcb 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L1-L5`：关键词命中
  - `kernel/fs/fs.c:L1-L3`：关键词命中
- 与 OSKernel2024-aabcb 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/trap/init.rs:L3-L7`：关键词命中
  - `kernel/dev/plic.c:L1-L3`：关键词命中
- 与 OSKernel2024-aabcb 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mm/mod.rs:L2-L6`：关键词命中
  - `kernel/mem/kvm.c:L12-L16`：关键词命中
- 与 OSKernel2024-aabcb 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/task/mod.rs:L6-L10`：关键词命中
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
- 与 OSKernel2024-aabcb 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/block/mod.rs:L1-L5`：关键词命中
  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
- 与 OSKernel2024-aabcb 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
  - `kernel/trap/trap.S:L1-L3`：关键词命中
- 与 OSKernel2024-aabcb 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）
- 与 ArceOS 同属 independent 风格。（置信度：medium）
- 与 ArceOS 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/mod.rs:L4-L8`：关键词命中
  - `modules/axdriver/src/lib.rs:L1-L3`：关键词命中
- 与 ArceOS 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L1-L5`：关键词命中
  - `modules/axfs/src/dev.rs:L1-L5`：关键词命中
- 与 ArceOS 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/trap/init.rs:L3-L7`：关键词命中
  - `modules/axhal/src/irq.rs:L1-L3`：关键词命中
- 与 ArceOS 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mm/mod.rs:L2-L6`：关键词命中
  - `modules/axmm/src/lib.rs:L92-L96`：关键词命中
- 与 ArceOS 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/task/mod.rs:L6-L10`：关键词命中
  - `modules/axmm/src/lib.rs:L74-L78`：关键词命中
- 与 ArceOS 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/block/mod.rs:L1-L5`：关键词命中
  - `modules/axfs/src/dev.rs:L1-L5`：关键词命中
- 与 ArceOS 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
  - `modules/axhal/src/irq.rs:L1-L5`：关键词命中
- 与 ArceOS 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 OSKernel2024-NQOS 的语言构成不同：新项目为 {'json': 18, 'build': 419, 'markdown': 6579, 'toml': 7, 'asm': 156, 'rust': 8127}，历史项目为 {'json': 18, 'markdown': 1725, 'build': 197, 'c': 13428, 'asm': 519}。（置信度：medium）
- 与 xv6-riscv 的语言构成不同：新项目为 {'json': 18, 'build': 419, 'markdown': 6579, 'toml': 7, 'asm': 156, 'rust': 8127}，历史项目为 {'json': 18, 'build': 199, 'c': 11718, 'asm': 276}。（置信度：medium）
- 与 OSKernel2024-aabcb 的语言构成不同：新项目为 {'json': 18, 'build': 419, 'markdown': 6579, 'toml': 7, 'asm': 156, 'rust': 8127}，历史项目为 {'json': 18, 'make': 26, 'build': 256, 'markdown': 227, 'c': 6835, 'asm': 308}。（置信度：medium）
- 与 ArceOS 的语言构成不同：新项目为 {'json': 18, 'build': 419, 'markdown': 6579, 'toml': 7, 'asm': 156, 'rust': 8127}，历史项目为 {'json': 20, 'build': 1933, 'markdown': 1596, 'toml': 138, 'c': 10256, 'rust': 20231, 'make': 679, 'asm': 189, 'text': 6}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：28
- 含证据关键结论数：28（100.0%）
- 无效证据引用数：0
- 未确认结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
