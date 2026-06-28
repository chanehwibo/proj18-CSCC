# OSKernel2024-ouye 项目描述报告

## 基本信息

- 仓库 ID：`oskernel2024-ouye`
- 风格：independent
- 架构：riscv64
- 样本来源等级：比赛作品样本（获奖等级未核验）
- 文件数：861
- 代码/文本行数：294212
- 主要语言：asm 193770 LOC, c 89788 LOC, markdown 8006 LOC, build 2630 LOC, json 18 LOC

## 总览

OSKernel2024-ouye 是一个 independent 风格的小型操作系统相关仓库，主要语言统计为 asm: 193770 LOC, c: 89788 LOC, markdown: 8006 LOC, build: 2630 LOC。仓库包含 861 个已扫描文件、约 294212 行可分析文本，当前抽取到 4737 个符号定义。

## 摘要评分

- 综合成熟度：A 级：机制完整、证据充分（100/100）
- 已确认 OS 维度：7/7；高置信维度：7/7
- 构建入口：已确认；证据健康度：100.0% 覆盖率；无效证据引用：0
- 评分口径：该分数由本地静态分析、源码证据和 self-check 派生，不代表比赛官方评分，也不调用 LLM。

| 评分项 | 得分 | 依据 |
| --- | --- | --- |
| OS 机制覆盖 | 80/80 | 调度、内存、系统调用、文件系统、同步、中断、驱动等维度的确认情况 |
| 构建入口 | 10/10 | 是否识别到 Makefile、Cargo.toml、CMakeLists.txt 等构建入口 |
| 证据健康度 | 10/10 | 关键结论证据覆盖率与无效证据引用数 |

| OS 维度 | 状态 | 置信度 | 证据数 |
| --- | --- | --- | --- |
| 调度与任务管理 | 已确认 | high | 6 |
| 内存管理 | 已确认 | high | 6 |
| 系统调用 | 已确认 | high | 11 |
| 文件系统 | 已确认 | high | 6 |
| 同步机制 | 已确认 | high | 6 |
| 中断与异常 | 已确认 | high | 6 |
| 设备驱动 | 已确认 | high | 6 |

## 构建系统

- 仓库包含构建入口：LAB1 优先级调度/Makefile, LAB2 信号量机制/Makefile, LAB4 内存管理/Makefile, LAB5 内核线程/Makefile, LAB6 用户终端实验/Makefile。（置信度：high）
  证据：
  - `LAB1 优先级调度/Makefile:L1-L3`：构建入口
    代码片段：`OBJS = \ bio.o\ console.o\`
  - `LAB2 信号量机制/Makefile:L1-L3`：构建入口
    代码片段：`OBJS = \ bio.o\ console.o\`
  - `LAB4 内存管理/Makefile:L1-L3`：构建入口
    代码片段：`OBJS = \ bio.o\ console.o\`
  - `LAB5 内核线程/Makefile:L1-L3`：构建入口
    代码片段：`OBJS = \ bio.o\ console.o\`
  - `LAB6 用户终端实验/Makefile:L1-L3`：构建入口
    代码片段：`OBJS = \ bio.o\ console.o\`

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）
  - 相关符号包括：fn wakeup1p, struct cpu, struct context, enum procstate, struct vma。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `LAB4 内存管理/proc.c` | L5-L9 | 关键词命中 |
| `LAB4 内存管理/proc.h` | L2-L6 | 关键词命中 |
| `LAB5 内核线程/proc.c` | L5-L9 | 关键词命中 |
| `LAB4 内存管理/proc.c` | L665-L669 | fn wakeup1p |
| `LAB4 内存管理/proc.h` | L1-L4 | struct cpu |
| `LAB4 内存管理/proc.h` | L25-L29 | struct context |

### 关键代码片段

  - `LAB4 内存管理/proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `LAB4 内存管理/proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
  - `LAB5 内核线程/proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `LAB4 内存管理/proc.c:L665-L669`：fn wakeup1p
    代码片段：`} void wakeup1p(void *chan) { acquire(&ptable.lock); struct proc *p;`

### 相关符号

`fn wakeup1p` at `LAB4 内存管理/proc.c:L665`、`struct cpu` at `LAB4 内存管理/proc.h:L1`、`struct context` at `LAB4 内存管理/proc.h:L25`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）
  - 相关符号包括：struct run, struct run, struct run, struct run, struct run。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `LAB4 内存管理/vm.c` | L9-L13 | 关键词命中 |
| `LAB5 内核线程/vm.c` | L9-L13 | 关键词命中 |
| `LAB1 优先级调度/vm.c` | L9-L13 | 关键词命中 |
| `LAB4 内存管理/kalloc.c` | L14-L18 | struct run |
| `LAB5 内核线程/kalloc.c` | L14-L18 | struct run |
| `LAB1 优先级调度/kalloc.c` | L14-L18 | struct run |

### 关键代码片段

  - `LAB4 内存管理/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `LAB5 内核线程/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `LAB1 优先级调度/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `LAB4 内存管理/kalloc.c:L14-L18`：struct run
    代码片段：`// defined by the kernel linker script in kernel.ld struct run { struct run *next; };`

### 相关符号

`struct run` at `LAB4 内存管理/kalloc.c:L14`、`struct run` at `LAB5 内核线程/kalloc.c:L14`、`struct run` at `LAB1 优先级调度/kalloc.c:L14`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含系统调用入口、编号或分发逻辑。（置信度：high）
  - 相关符号包括：macro SYS_fork, macro SYS_exit, macro SYS_wait, macro SYS_pipe, macro SYS_read。（置信度：medium）
  - 静态识别到 21 个系统调用相关符号。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `LAB4 内存管理/syscall.c` | L6-L10 | 关键词命中 |
| `LAB5 内核线程/syscall.c` | L6-L10 | 关键词命中 |
| `LAB1 优先级调度/syscall.c` | L6-L10 | 关键词命中 |
| `LAB4 内存管理/syscall.h` | L1-L4 | macro SYS_fork |
| `LAB4 内存管理/syscall.h` | L1-L5 | macro SYS_exit |
| `LAB4 内存管理/syscall.h` | L2-L6 | macro SYS_wait |

### 关键代码片段

  - `LAB4 内存管理/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `LAB5 内核线程/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `LAB1 优先级调度/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `LAB4 内存管理/syscall.h:L1-L4`：macro SYS_fork
    代码片段：`// System call numbers #define SYS_fork    1 #define SYS_exit    2 #define SYS_wait    3`

### 相关符号

`macro SYS_fork` at `LAB4 内存管理/syscall.h:L1`、`macro SYS_exit` at `LAB4 内存管理/syscall.h:L1`、`macro SYS_wait` at `LAB4 内存管理/syscall.h:L2`、`macro T_SYSCALL` at `LAB4 内存管理/traps.h:L25`、`macro T_SYSCALL` at `LAB5 内核线程/traps.h:L25`、`macro T_SYSCALL` at `LAB1 优先级调度/traps.h:L25`、`macro T_SYSCALL` at `LAB2 信号量机制/traps.h:L25`、`fn sys_clone` at `LAB5 内核线程/sysproc.c:L189`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 文件系统

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含文件系统、VFS、inode、目录项或文件读写相关实现。（置信度：high）
  - 相关符号包括：struct superblock, struct dinode, struct dirent, struct superblock, struct dinode。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `LAB4 内存管理/fs.c` | L2-L6 | 关键词命中 |
| `LAB4 内存管理/fs.h` | L7-L11 | 关键词命中 |
| `LAB5 内核线程/fs.c` | L2-L6 | 关键词命中 |
| `LAB4 内存管理/fs.h` | L12-L16 | struct superblock |
| `LAB4 内存管理/fs.h` | L27-L31 | struct dinode |
| `LAB4 内存管理/fs.h` | L51-L55 | struct dirent |

### 关键代码片段

  - `LAB4 内存管理/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `LAB4 内存管理/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `LAB5 内核线程/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `LAB4 内存管理/fs.h:L12-L16`：struct superblock
    代码片段：`// mkfs computes the super block and builds an initial file system. The // super block describes the disk layout: struct superblock { uint size;         // Size of file system i...`

### 相关符号

`struct superblock` at `LAB4 内存管理/fs.h:L12`、`struct dinode` at `LAB4 内存管理/fs.h:L27`、`struct dirent` at `LAB4 内存管理/fs.h:L51`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）
  - 相关符号包括：fn main, fn main, fn main, fn main, struct spinlock。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `LAB4 内存管理/fs.c` | L16-L20 | 关键词命中 |
| `LAB5 内核线程/fs.c` | L16-L20 | 关键词命中 |
| `LAB1 优先级调度/fs.c` | L16-L20 | 关键词命中 |
| `LAB4 内存管理/sh_rw_lock.c` | L3-L7 | fn main |
| `LAB5 内核线程/sh_rw_lock.c` | L3-L7 | fn main |
| `LAB2 信号量机制/sh_rw_lock.c` | L3-L7 | fn main |

### 关键代码片段

  - `LAB4 内存管理/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `LAB5 内核线程/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `LAB1 优先级调度/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `LAB4 内存管理/sh_rw_lock.c:L3-L7`：fn main
    代码片段：`#include "user.h" int main(){ sh_var_write(0);		//给内核全局变量赋初值 int id=sem_create(1);	//创建信号量，参数为1表示该资源数量为1，同一时刻只能有一个进程互斥访问`

### 相关符号

`fn main` at `LAB4 内存管理/sh_rw_lock.c:L3`、`fn main` at `LAB5 内核线程/sh_rw_lock.c:L3`、`fn main` at `LAB2 信号量机制/sh_rw_lock.c:L3`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 中断与异常

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `interrupt` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含 trap、中断、异常或定时器处理逻辑。（置信度：high）
  - 相关符号包括：macro TIMER, macro TIMER, macro TIMER, macro TIMER, macro TIMER。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `LAB4 内存管理/trap.c` | L9-L13 | 关键词命中 |
| `LAB5 内核线程/trap.c` | L9-L13 | 关键词命中 |
| `LAB1 优先级调度/trap.c` | L9-L13 | 关键词命中 |
| `LAB4 内存管理/lapic.c` | L30-L34 | macro TIMER |
| `LAB5 内核线程/lapic.c` | L30-L34 | macro TIMER |
| `LAB1 优先级调度/lapic.c` | L30-L34 | macro TIMER |

### 关键代码片段

  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `LAB5 内核线程/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `LAB1 优先级调度/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `LAB4 内存管理/lapic.c:L30-L34`：macro TIMER
    代码片段：`#define FIXED      0x00000000 #define ICRHI   (0x0310/4)   // Interrupt Command [63:32] #define TIMER   (0x0320/4)   // Local Vector Table 0 (TIMER) #define X1         0x0000000...`

### 相关符号

`macro TIMER` at `LAB4 内存管理/lapic.c:L30`、`macro TIMER` at `LAB5 内核线程/lapic.c:L30`、`macro TIMER` at `LAB1 优先级调度/lapic.c:L30`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。（置信度：high）
  - 相关符号包括：macro IOAPIC, struct ioapic, macro IOAPIC, struct ioapic, macro IOAPIC。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `LAB4 内存管理/ide.c` | L1-L3 | 关键词命中 |
| `LAB4 内存管理/kbd.c` | L2-L6 | 关键词命中 |
| `LAB4 内存管理/kbd.h` | L1-L5 | 关键词命中 |
| `LAB4 内存管理/ioapic.c` | L7-L11 | macro IOAPIC |
| `LAB4 内存管理/ioapic.c` | L26-L30 | struct ioapic |
| `LAB5 内核线程/ioapic.c` | L7-L11 | macro IOAPIC |

### 关键代码片段

  - `LAB4 内存管理/ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `LAB4 内存管理/kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
  - `LAB4 内存管理/kbd.h:L1-L5`：关键词命中
    代码片段：`// PC keyboard interface constants #define KBSTATP         0x64    // kbd controller status port(I) #define KBS_DIB         0x01    // kbd data in buffer #define KBDATAP...`
  - `LAB4 内存管理/ioapic.c:L7-L11`：macro IOAPIC
    代码片段：`#include "traps.h" #define IOAPIC  0xFEC00000   // Default physical address of IO APIC #define REG_ID     0x00  // Register index: ID`

### 相关符号

`macro IOAPIC` at `LAB4 内存管理/ioapic.c:L7`、`struct ioapic` at `LAB4 内存管理/ioapic.c:L26`、`macro IOAPIC` at `LAB5 内核线程/ioapic.c:L7`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 附录：核验摘要

- 关键结论数：16
- 含证据关键结论数：16（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
