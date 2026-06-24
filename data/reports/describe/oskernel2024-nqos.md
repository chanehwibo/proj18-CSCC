# OSKernel2024-NQOS 项目描述报告

## 基本信息

- 仓库 ID：`oskernel2024-nqos`
- 风格：independent
- 架构：riscv64
- 样本来源等级：比赛作品样本（获奖等级未核验）
- 文件数：90
- 代码/文本行数：15887
- 主要语言：c 13428 LOC, markdown 1725 LOC, asm 519 LOC, build 197 LOC, json 18 LOC

## 总览

OSKernel2024-NQOS 是一个 independent 风格的小型操作系统相关仓库，主要语言统计为 c: 13428 LOC, markdown: 1725 LOC, asm: 519 LOC, build: 197 LOC。仓库包含 90 个已扫描文件、约 15887 行可分析文本，当前抽取到 555 个符号定义。

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
| 系统调用 | 已确认 | high | 6 |
| 文件系统 | 已确认 | high | 6 |
| 同步机制 | 已确认 | high | 6 |
| 中断与异常 | 已确认 | high | 6 |
| 设备驱动 | 已确认 | high | 6 |

## 构建系统

- 仓库包含构建入口：Makefile。（置信度：high）
  证据：
  - `Makefile:L1-L3`：构建入口
    代码片段：`K=kernel U=user`

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）
  - 相关符号包括：class cpu, class proc, class spinlock, class trapframe, fn clone。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/proc.c` | L4-L8 | 关键词命中 |
| `kernel/proc.h` | L23-L27 | 关键词命中 |
| `kernel/sysproc.c` | L5-L9 | 关键词命中 |
| `kernel/proc.c` | L7-L11 | class cpu |
| `kernel/proc.c` | L9-L13 | class proc |
| `kernel/proc.c` | L14-L18 | class spinlock |

### 关键代码片段

  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L23-L27`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;          // The process running on this cpu, or null. struct context context;     // swtch() here to enter scheduler(). int nof...`
  - `kernel/sysproc.c:L5-L9`：关键词命中
    代码片段：`#include "memlayout.h" #include "spinlock.h" #include "proc.h" uint64`
  - `kernel/proc.c:L7-L11`：class cpu
    代码片段：`#include "defs.h" struct cpu cpus[NCPU]; struct proc proc[NPROC];`

### 相关符号

`class cpu` at `kernel/proc.c:L7`、`class proc` at `kernel/proc.c:L9`、`class spinlock` at `kernel/proc.c:L14`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）
  - 相关符号包括：struct run, class run, class spinlock, macro MAKE_SATP, macro PGSIZE。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/vm.c` | L8-L12 | 关键词命中 |
| `kernel/kalloc.c` | L36-L40 | 关键词命中 |
| `kernel/defs.h` | L62-L66 | 关键词命中 |
| `kernel/kalloc.c` | L15-L19 | struct run |
| `kernel/kalloc.c` | L16-L20 | class run |
| `kernel/kalloc.c` | L20-L24 | class spinlock |

### 关键代码片段

  - `kernel/vm.c:L8-L12`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char*)PGROUNDUP((uint64)pa_start); for(; p + PGSIZE <= (char*)pa_end; p += PGSIZE) kfree(p); }`
  - `kernel/defs.h:L62-L66`：关键词命中
    代码片段：`void            ramdiskrw(struct buf*); // kalloc.c void*           kalloc(void); void            kfree(void *);`
  - `kernel/kalloc.c:L15-L19`：struct run
    代码片段：`// defined by kernel.ld. struct run { struct run *next; };`

### 相关符号

`struct run` at `kernel/kalloc.c:L15`、`class run` at `kernel/kalloc.c:L16`、`class spinlock` at `kernel/kalloc.c:L20`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含系统调用入口、编号或分发逻辑。（置信度：high）
  - 相关符号包括：class proc, macro SYS_fork, macro SYS_exit, macro SYS_wait, macro SYS_pipe。（置信度：medium）
  - 静态识别到 1 个系统调用相关符号。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/trap.c` | L74-L78 | 关键词命中 |
| `kernel/syscall.c` | L5-L9 | 关键词命中 |
| `kernel/syscall.c` | L12-L16 | class proc |
| `kernel/syscall.h` | L1-L4 | macro SYS_fork |
| `kernel/syscall.h` | L1-L5 | macro SYS_exit |
| `user/signaltest.c` | L205-L209 | fn testsignal_syscall |

### 关键代码片段

  - `kernel/trap.c:L74-L78`：关键词命中
    代码片段：`exit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
  - `kernel/syscall.c:L12-L16`：class proc
    代码片段：`fetchaddr(uint64 addr, uint64 *ip) { struct proc *p = myproc(); if(addr >= p->sz || addr+sizeof(uint64) > p->sz) // both tests needed, in case of overflow return -1;`
  - `kernel/syscall.h:L1-L4`：macro SYS_fork
    代码片段：`// System call numbers #define SYS_fork    1 #define SYS_exit    2 #define SYS_wait    3`

### 相关符号

`class proc` at `kernel/syscall.c:L12`、`macro SYS_fork` at `kernel/syscall.h:L1`、`macro SYS_exit` at `kernel/syscall.h:L1`、`fn testsignal_syscall` at `user/signaltest.c:L205`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 文件系统

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含文件系统、VFS、inode、目录项或文件读写相关实现。（置信度：high）
  - 相关符号包括：class superblock, class inode, struct superblock, class inode, class superblock。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/fs.c` | L2-L6 | 关键词命中 |
| `kernel/fs.h` | L7-L11 | 关键词命中 |
| `kernel/defs.h` | L2-L6 | 关键词命中 |
| `kernel/fs.c` | L25-L29 | class superblock |
| `kernel/fs.c` | L176-L180 | class inode |
| `kernel/fs.h` | L12-L16 | struct superblock |

### 关键代码片段

  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `kernel/defs.h:L2-L6`：关键词命中
    代码片段：`struct context; struct file; struct inode; struct pipe; struct proc;`
  - `kernel/fs.c:L25-L29`：class superblock
    代码片段：`// there should be one superblock per disk device, but we run with // only one device struct superblock sb; // Read the super block.`

### 相关符号

`class superblock` at `kernel/fs.c:L25`、`class inode` at `kernel/fs.c:L176`、`struct superblock` at `kernel/fs.h:L12`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）
  - 相关符号包括：class cpu, struct spinlock, class cpu, class spinlock, class spinlock。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/spinlock.c` | L4-L8 | 关键词命中 |
| `kernel/spinlock.h` | L1-L3 | 关键词命中 |
| `kernel/sleeplock.c` | L6-L10 | 关键词命中 |
| `kernel/spinlock.c` | L100-L104 | class cpu |
| `kernel/spinlock.h` | L1-L4 | struct spinlock |
| `kernel/spinlock.h` | L5-L9 | class cpu |

### 关键代码片段

  - `kernel/spinlock.c:L4-L8`：关键词命中
    代码片段：`#include "param.h" #include "memlayout.h" #include "spinlock.h" #include "riscv.h" #include "proc.h"`
  - `kernel/spinlock.h:L1-L3`：关键词命中
    代码片段：`// Mutual exclusion lock. struct spinlock { uint locked;       // Is the lock held?`
  - `kernel/sleeplock.c:L6-L10`：关键词命中
    代码片段：`#include "param.h" #include "memlayout.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/spinlock.c:L100-L104`：class cpu
    代码片段：`pop_off(void) { struct cpu *c = mycpu(); if(intr_get()) panic("pop_off - interruptible");`

### 相关符号

`class cpu` at `kernel/spinlock.c:L100`、`struct spinlock` at `kernel/spinlock.h:L1`、`class cpu` at `kernel/spinlock.h:L5`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 中断与异常

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `interrupt` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含 trap、中断、异常或定时器处理逻辑。（置信度：high）
  - 相关符号包括：class spinlock, class proc, macro IER, macro ISR, macro MSTATUS_MIE。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/plic.c` | L6-L10 | 关键词命中 |
| `kernel/trap.c` | L31-L35 | 关键词命中 |
| `kernel/vm.c` | L31-L35 | 关键词命中 |
| `kernel/trap.c` | L7-L11 | class spinlock |
| `kernel/trap.c` | L46-L50 | class proc |
| `kernel/uart.c` | L22-L26 | macro IER |

### 关键代码片段

  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from trampoline.S //`
  - `kernel/vm.c:L31-L35`：关键词命中
    代码片段：`kvmmap(kpgtbl, VIRTIO0, VIRTIO0, PGSIZE, PTE_R | PTE_W); // PLIC kvmmap(kpgtbl, PLIC, PLIC, 0x4000000, PTE_R | PTE_W);`
  - `kernel/trap.c:L7-L11`：class spinlock
    代码片段：`#include "defs.h" struct spinlock tickslock; uint ticks;`

### 相关符号

`class spinlock` at `kernel/trap.c:L7`、`class proc` at `kernel/trap.c:L46`、`macro IER` at `kernel/uart.c:L22`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。（置信度：high）
  - 相关符号包括：macro Reg, macro RHR, macro THR, macro IER, macro IER_RX_ENABLE。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/uart.c` | L1-L4 | 关键词命中 |
| `kernel/virtio.h` | L1-L4 | 关键词命中 |
| `kernel/console.c` | L1-L4 | 关键词命中 |
| `kernel/uart.c` | L14-L18 | macro Reg |
| `kernel/uart.c` | L20-L24 | macro RHR |
| `kernel/uart.c` | L21-L25 | macro THR |

### 关键代码片段

  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
  - `kernel/console.c:L1-L4`：关键词命中
    代码片段：`// // Console input and output, to the uart. // Reads are line at a time. // Implements special input characters:`
  - `kernel/uart.c:L14-L18`：macro Reg
    代码片段：`// at address UART0. this macro returns the // address of one of the registers. #define Reg(reg) ((volatile unsigned char *)(UART0 + (reg))) // the UART control registers.`

### 相关符号

`macro Reg` at `kernel/uart.c:L14`、`macro RHR` at `kernel/uart.c:L20`、`macro THR` at `kernel/uart.c:L21`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 附录：核验摘要

- 关键结论数：16
- 含证据关键结论数：16（100.0%）
- 无效证据引用数：0
- 未确认结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
