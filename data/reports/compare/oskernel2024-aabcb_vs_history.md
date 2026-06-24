# 项目比较报告

## 比较对象选择

本次比较选取了三个历史仓库与待审项目 `OSKernel2024-aabcb` 进行对比，选择依据如下：

- **xv6-riscv**（来源：教学基线）
  评分 11.55；同属 independent 风格；架构重合度 1.00；语言构成相似度 0.93；OS 维度重合度 1.00；代码规模接近度 0.68。

- **OSKernel2024-NQOS**（来源：比赛作品样本，获奖等级未核验）
  评分 11.42；同属 independent 风格；架构重合度 1.00；语言构成相似度 0.92；OS 维度重合度 1.00；代码规模接近度 0.58。

- **OSKernel2024-ouye**（来源：比赛作品样本，获奖等级未核验）
  评分 9.98；同属 independent 风格；架构重合度 1.00；语言构成相似度 0.38；OS 维度重合度 1.00；代码规模接近度 0.22。

## 功能重合与疑似重复证据

以下功能维度均在新项目与各历史仓库之间发现可追溯源码的重合现象，**这些重合仅表示功能实现线索相似，需人工复核方可判断是否构成实质性重复，并非代码抄袭的直接裁定**。

### 与 xv6-riscv（教学基线）的重合维度

- **设备驱动**
  `kernel/dev/uart.c:L1-L3` / `kernel/uart.c:L1-L4`，`kernel/dev/virtio.c:L1-L5` / `kernel/virtio.h:L1-L4`。

- **文件系统**
  `kernel/fs/fs.c:L2-L6`、`kernel/fs/dir.c:L1-L5` / `kernel/fs.c:L2-L6`、`kernel/fs.h:L6-L10`。

- **中断与异常**
  `kernel/dev/plic.c:L1-L3`、`kernel/dev/timer.c:L1-L5` / `kernel/plic.c:L6-L10`、`kernel/trap.c:L31-L35`。

- **内存管理**
  `kernel/mem/kvm.c:L12-L16`、`kernel/mem/uvm.c:L12-L16` / `kernel/vm.c:L10-L14`、`kernel/kalloc.c:L36-L40`。

- **调度与任务管理**
  `kernel/proc/cpu.c:L1-L3`、`kernel/proc/exec.c:L1-L3` / `kernel/proc.c:L4-L8`、`kernel/proc.h:L21-L25`。

- **同步机制**
  `kernel/lib/spinlock.c:L1-L3`、`kernel/lib/sleeplock.c:L1-L3` / `kernel/fs.c:L15-L19`、`kernel/vm.c:L5-L9`。

- **系统调用**
  `kernel/syscall/syscall.c:L3-L7`、`kernel/syscall/sysfile.c:L6-L10` / `kernel/trap.c:L58-L62`、`kernel/syscall.c:L5-L9`。

### 与 OSKernel2024-NQOS（比赛作品样本）的重合维度

- **设备驱动**：`kernel/dev/uart.c:L1-L3` / `kernel/uart.c:L1-L4`，`kernel/dev/virtio.c:L1-L5` / `kernel/virtio.h:L1-L4`。
- **文件系统**：`kernel/fs/fs.c:L2-L6`、`kernel/fs/dir.c:L1-L5` / `kernel/fs.c:L2-L6`、`kernel/fs.h:L7-L11`。
- **中断与异常**：`kernel/dev/plic.c:L1-L3` / `kernel/plic.c:L6-L10`，`kernel/dev/timer.c:L1-L5` / `kernel/trap.c:L31-L35`。
- **内存管理**：`kernel/mem/kvm.c:L12-L16` / `kernel/vm.c:L8-L12`，`kernel/mem/uvm.c:L12-L16` / `kernel/kalloc.c:L36-L40`。
- **调度与任务管理**：`kernel/proc/cpu.c:L1-L3` / `kernel/proc.c:L4-L8`，`kernel/proc/exec.c:L1-L3` / `kernel/proc.h:L23-L27`。
- **同步机制**：`kernel/lib/spinlock.c:L1-L3`、`kernel/lib/sleeplock.c:L1-L3` / `kernel/fs.c:L15-L19`、`kernel/bio.c:L17-L21`。
- **系统调用**：`kernel/syscall/syscall.c:L3-L7` / `kernel/trap.c:L74-L78`，`kernel/syscall/sysfile.c:L6-L10` / `kernel/syscall.c:L5-L9`。

### 与 OSKernel2024-ouye（比赛作品样本）的重合维度

- **设备驱动**：`kernel/dev/uart.c:L1-L3` / `LAB4 内存管理/ide.c:L1-L3`、`LAB4 内存管理/kbd.c:L2-L6`。
- **文件系统**：`kernel/fs/fs.c:L2-L6`、`kernel/fs/dir.c:L1-L5` / `LAB4 内存管理/fs.c:L2-L6`、`LAB4 内存管理/fs.h:L7-L11`。
- **中断与异常**：`kernel/dev/plic.c:L1-L3` / `LAB4 内存管理/trap.c:L9-L13`（含 `LAB5 内核线程` 目录对应文件）。
- **内存管理**：`kernel/mem/kvm.c:L12-L16` / `LAB4 内存管理/vm.c:L9-L13`（含 `LAB5 内核线程` 目录）。
- **调度与任务管理**：`kernel/proc/cpu.c:L1-L3` / `LAB4 内存管理/proc.c:L5-L9`、`LAB4 内存管理/proc.h:L2-L6`。
- **同步机制**：`kernel/lib/spinlock.c:L1-L3`、`kernel/lib/sleeplock.c:L1-L3` / `LAB4 内存管理/fs.c:L16-L20`（含 `LAB5 内核线程` 目录）。
- **系统调用**：`kernel/syscall/syscall.c:L3-L7` / `LAB4 内存管理/syscall.c:L6-L10`（含 `LAB5 内核线程` 目录）。

## 代码级相似线索检测

以下线索基于符号名、结构体/类型、宏定义与文件路径的自动匹配结果，**所有线索均属命名或局部结构重合，不能直接作为抄袭裁定依据，必须由人工复核确定相似程度**。

### 与 xv6-riscv 的相似线索

- **宏名重合（设备驱动）**：`RHR`（`kernel/dev/uart.c:L11` / `kernel/uart.c:L24`）、`THR`、`IER`、`IER_TX_ENABLE`。
- **宏名重合（中断与异常）**：`PLIC_PRIORITY`（`include/memlayout.h:L23` / `kernel/memlayout.h:L30`）、`PLIC_PENDING`、`PLIC_SENABLE`、`PLIC_SPRIORITY`。
- **宏名重合（内存管理）**：`PGSIZE`（`include/common.h:L30` / `kernel/riscv.h:L352`）、`TRAMPOLINE`、`TRAPFRAME`、`KSTACK`。
- **宏名重合（系统调用）**：`TRAPFRAME`（`include/memlayout.h:L46` / `kernel/memlayout.h:L59`）、`SYS_fork`（`user/syscall_num.h:L8` / `kernel/syscall.h:L2`）、`SYS_wait`、`SYS_exit`。
- **结构体/类型重合（文件系统）**：`dirent`（`mkfs/mkfs.c:L37` / `kernel/fs.h:L57`）、`file`（`include/fs/file.h:L22` / `kernel/file.h:L1`）、`inode`。
- **函数/符号名重合（调度与任务管理）**：`swtch`（`kernel/proc/swtch.S:L7` / `kernel/swtch.S:L9`）。
- **结构体/类型重合（调度与任务管理）**：`cpu`（`include/proc/cpu.h:L7` / `kernel/proc.h:L22`）、`context`（`include/proc/proc.h:L17` / `kernel/proc.h:L2`）、`trapframe`、`proc`。
- **文件路径重合**：`kernel/dev/uart.c` / `kernel/uart.c`，`include/dev/virtio.h` / `kernel/virtio.h`，`kernel/fs/fs.c` / `kernel/fs.c`，`kernel/fs/file.c` / `kernel/file.c`，`kernel/dev/plic.c` / `kernel/plic.c`，`kernel/proc/proc.c` / `kernel/proc.c`。

### 与 OSKernel2024-NQOS 的相似线索

- **宏名重合（设备驱动）**：`RHR`（`kernel/dev/uart.c:L11` / `kernel/uart.c:L22`）、`THR`、`IER`、`IER_TX_ENABLE`。
- **宏名重合（中断与异常）**：`PLIC_PRIORITY`（`include/memlayout.h:L23` / `kernel/memlayout.h:L30`）、`PLIC_PENDING`、`PLIC_SENABLE`、`PLIC_SPRIORITY`。
- **结构体/类型重合（文件系统）**：`dirent`（`mkfs/mkfs.c:L37` / `kernel/fs.h:L56`）、`file`（`include/fs/file.h:L22` / `kernel/file.h:L1`）、`inode`。
- **函数/符号名重合（调度与任务管理）**：`swtch`（`kernel/proc/swtch.S:L7` / `kernel/swtch.S:L9`）。
- **结构体/类型重合（调度与任务管理）**：`cpu`（`include/proc/cpu.h:L7` / `kernel/proc.h:L24`）、`context`（`include/proc/proc.h:L17` / `kernel/proc.h:L4`）、`trapframe`、`proc`。

### 与 OSKernel2024-ouye 的相似线索

- **结构体/类型重合（文件系统）**：`dirent`（`mkfs/mkfs.c:L37` / `LAB1 优先级调度/fs.h:L53`）、`file`（`include/fs/file.h:L22` / `LAB1 优先级调度/file.h:L1`）、`inode`。
- **函数/符号名重合（调度与任务管理）**：`swtch`（`kernel/proc/swtch.S:L7` / `LAB1 优先级调度/swtch.S:L10`）。
- **结构体/类型重合（调度与任务管理）**：`cpu`（`include/proc/cpu.h:L7` / `LAB1 优先级调度/proc.h:L4`）、`context`（`include/proc/proc.h:L17` / `LAB1 优先级调度/proc.h:L29`）、`proc`。

## 相似点

- 新项目 `OSKernel2024-aabcb` 与三个历史仓库均属 **independent 风格**。
- 在 **设备驱动、文件系统、中断与异常、内存管理、调度与任务管理、同步机制、系统调用** 七个核心 OS 维度上，新项目与每个历史仓库均有可确认的源代码实现，可作为进一步人工复核的重点方向。

## 差异点

- **语言构成** 存在明显差异：
  - 与 xv6-riscv 对比：`OSKernel2024-aabcb` 的构成 `{'json': 18, 'make': 26, 'build': 256, 'markdown': 227, 'c': 6835, 'asm': 308}`，历史项目 `{'json': 18, 'build': 199, 'c': 11718, 'asm': 276}`。
  - 与 OSKernel2024-NQOS 对比：历史项目含更多 C 和汇编代码，且 Markdown 占比不同。
  - 与 OSKernel2024-ouye 对比：历史项目代码规模显著更大（C/汇编总量大幅超过新项目），且包含大量 build 文件。

## 可能创新点

**当前证据不足，未自动确认创新点。** 报告未发现 unique_points 中被核验的创新实现线索，因此暂无法总结新项目的创新特征。

## 待人工复核项

为了确认上述重合是否超出教学基线或比赛作品中的合理复用范围，建议人工重点复核以下内容：

1. **与 xv6-riscv（教学基线）** 的 7 个维度源代码相似性，特别是 UART、Virtio 驱动、文件系统布局、中断处理、内存分配与页表、进程切换、自旋锁/睡眠锁等实现细节的逐行比对。
2. **与 OSKernel2024-NQOS（比赛作品样本）** 的同名宏定义、结构体定义（如 `cpu`、`context`、`proc`）及文件路径重合情况，判断是否仅为教学框架继承。
3. **与 OSKernel2024-ouye（比赛作品样本）** 的实验目录线索（如 `LAB4 内存管理`、`LAB5 内核线程` 中出现 xv6 风格文件路径和证据片段），需要复核这些内容是教学实验残留、合理参考，还是与当前 RISC-V 项目存在实质实现关系。
4. 所有代码级相似线索（宏名、结构体/类型、函数/符号名、文件路径）需结合具体实现逻辑进行人工评估，确认是否存在非合规借鉴。

## 核验摘要

本报告基于自动检测的 **63 项关键发现**，全部均有对应证据，证据覆盖率 100%，未出现无效证据。**未确认关键结论数为 0**，所有功能重合及相似线索均已标注需待人工复核，尚未形成最终抄袭判决。报告中的证据率统计仅涉及关键设计判断，自动检测结果不替代人工评审。