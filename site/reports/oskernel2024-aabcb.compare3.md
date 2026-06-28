# OSKernel2024-aabcb 比较报告

- 对比历史仓库：xv6-public
- 生成时间：2026-06-28T07:45:00.158690+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- xv6-public（来源：架构参考样本）：画像相似度 score=6.70；语言构成相似度 0.96; OS 维度重合度 1.00; 代码规模接近度 0.79

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 xv6-public 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
  - `ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
- 与 xv6-public 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
  - `fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 xv6-public 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
  - `trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `mp.h:L50-L54`：关键词命中
    代码片段：`#define MPBUS     0x01  // One per bus #define MPIOAPIC  0x02  // One per I/O APIC #define MPIOINTR  0x03  // One per bus interrupt source #define MPLINTR   0x04  // One per sys...`
- 与 xv6-public 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/mem/kvm.c:L12-L16`：关键词命中
    代码片段：`// 根据pagetable,找到va对应的pte // 若设置alloc=true 则在PTE无效时尝试申请一个物理页 // 成功返回PTE, 失败返回NULL`
  - `kernel/mem/uvm.c:L12-L16`：关键词命中
    代码片段：`uint64 va, pa, page; int flags; pte_t* pte; for(va = begin; va < end; va += PGSIZE)`
  - `vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `kalloc.c:L1-L4`：关键词命中
    代码片段：`// Physical memory allocator, intended to allocate // memory for user processes, kernel stacks, page table pages, // and pipe buffers. Allocates 4096-byte pages.`
- 与 xv6-public 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h" #include "lib/lock.h"`
  - `kernel/proc/exec.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "proc/elf.h" #include "mem/vmem.h"`
  - `proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
- 与 xv6-public 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/sleeplock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `bio.c:L22-L26`：关键词命中
    代码片段：`#include "defs.h" #include "param.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
- 与 xv6-public 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfile.c:L6-L10`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "syscall/syscall.h" #include "syscall/sysfunc.h"`
  - `syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 宏名重合：与 xv6-public 在“内存管理”维度发现 4 个同名定义：PGSIZE, PGROUNDUP, PTE_W, PTE_U。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/common.h:L30-L30`：macro PGSIZE
    代码片段：`#define PGSIZE 4096          // 物理页大小`
  - `mmu.h:L85-L85`：macro PGSIZE
    代码片段：`#define PGSIZE          4096    // bytes mapped by a page`
  - `kernel/mem/pmem.c:L27-L27`：macro PGROUNDUP
    代码片段：`#define PGROUNDUP(x) (((x) + PGSIZE - 1) & ~(PGSIZE - 1))`
  - `mmu.h:L90-L90`：macro PGROUNDUP
    代码片段：`#define PGROUNDUP(sz)  (((sz)+PGSIZE-1) & ~(PGSIZE-1))`
- 宏名重合：与 xv6-public 在“系统调用”维度发现 4 个同名定义：SYS_fork, SYS_wait, SYS_exit, SYS_sleep。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `user/syscall_num.h:L8-L8`：macro SYS_fork
    代码片段：`#define SYS_fork         4`
  - `syscall.h:L2-L2`：macro SYS_fork
    代码片段：`#define SYS_fork    1`
  - `user/syscall_num.h:L9-L9`：macro SYS_wait
    代码片段：`#define SYS_wait         5`
  - `syscall.h:L4-L4`：macro SYS_wait
    代码片段：`#define SYS_wait    3`
- 结构体/类型重合：与 xv6-public 在“文件系统”维度发现 3 个同名定义：dirent, file, inode。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `mkfs/mkfs.c:L37-L37`：struct dirent
    代码片段：`typedef struct dirent {`
  - `fs.h:L53-L53`：struct dirent
    代码片段：`struct dirent {`
  - `include/fs/file.h:L22-L22`：struct file
    代码片段：`typedef struct file {`
  - `file.h:L1-L1`：struct file
    代码片段：`struct file {`
- 函数/符号名重合：与 xv6-public 在“调度与任务管理”维度发现 1 个同名定义：swtch。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/proc/swtch.S:L7-L7`：fn swtch
    代码片段：`swtch:`
  - `swtch.S:L10-L10`：fn swtch
    代码片段：`swtch:`
- 结构体/类型重合：与 xv6-public 在“调度与任务管理”维度发现 3 个同名定义：cpu, context, proc。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/proc/cpu.h:L7-L7`：struct cpu
    代码片段：`typedef struct cpu {`
  - `proc.h:L2-L2`：struct cpu
    代码片段：`struct cpu {`
  - `include/proc/proc.h:L17-L17`：struct context
    代码片段：`typedef struct context {`
  - `proc.h:L27-L27`：struct context
    代码片段：`struct context {`
- 宏名重合：与 xv6-public 在“文件系统”维度发现 1 个同名定义：SYS_fstat。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/syscall/sysnum.h:L19-L19`：macro SYS_fstat
    代码片段：`#define SYS_fstat        14`
  - `syscall.h:L9-L9`：macro SYS_fstat
    代码片段：`#define SYS_fstat   8`
- 宏名重合：与 xv6-public 在“调度与任务管理”维度发现 1 个同名定义：NPROC。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/common.h:L28-L28`：macro NPROC
    代码片段：`#define NPROC 64             // 最大进程数量`
  - `param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC        64  // maximum number of processes`
- 结构体/类型重合：与 xv6-public 在“中断与异常”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/proc/proc.h:L37-L37`：struct trapframe
    代码片段：`typedef struct trapframe {`
  - `x86.h:L150-L150`：struct trapframe
    代码片段：`struct trapframe {`
- 结构体/类型重合：与 xv6-public 在“内存管理”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/proc/proc.h:L37-L37`：struct trapframe
    代码片段：`typedef struct trapframe {`
  - `x86.h:L150-L150`：struct trapframe
    代码片段：`struct trapframe {`
- 结构体/类型重合：与 xv6-public 在“同步机制”维度发现 2 个同名定义：spinlock, sleeplock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/lib/lock.h:L6-L6`：struct spinlock
    代码片段：`typedef struct spinlock {`
  - `spinlock.h:L2-L2`：struct spinlock
    代码片段：`struct spinlock {`
  - `include/lib/lock.h:L12-L12`：struct sleeplock
    代码片段：`typedef struct sleeplock {`
  - `sleeplock.h:L2-L2`：struct sleeplock
    代码片段：`struct sleeplock {`
- 结构体/类型重合：与 xv6-public 在“系统调用”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/proc/proc.h:L37-L37`：struct trapframe
    代码片段：`typedef struct trapframe {`
  - `x86.h:L150-L150`：struct trapframe
    代码片段：`struct trapframe {`
- 文件路径重合：与 xv6-public 在“文件系统”维度出现同名文件源码路径 `kernel/fs/fs.c` / `fs.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
- 文件路径重合：与 xv6-public 在“文件系统”维度出现同名文件源码路径 `kernel/fs/file.c` / `file.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/fs/file.c:L3-L7`：关键词命中
    代码片段：`#include "fs/dir.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/file.h" #include "mem/vmem.h"`
  - `file.c:L95-L99`：关键词命中
    代码片段：`// Read from file f. int fileread(struct file *f, char *addr, int n) { int r;`
- 文件路径重合：与 xv6-public 在“调度与任务管理”维度出现同名文件源码路径 `kernel/proc/proc.c` / `proc.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/proc/proc.c:L4-L8`：关键词命中
    代码片段：`#include "mem/vmem.h" #include "mem/mmap.h" #include "proc/cpu.h" #include "proc/initcode.h" #include "memlayout.h"`
  - `proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
- 文件路径重合：与 xv6-public 在“系统调用”维度出现同名文件源码路径 `kernel/syscall/syscall.c` / `syscall.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`

## 相似点

- 与 xv6-public 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
- 与 xv6-public 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
- 与 xv6-public 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
- 与 xv6-public 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/mem/kvm.c:L12-L16`：关键词命中
    代码片段：`// 根据pagetable,找到va对应的pte // 若设置alloc=true 则在PTE无效时尝试申请一个物理页 // 成功返回PTE, 失败返回NULL`
  - `kernel/mem/uvm.c:L12-L16`：关键词命中
    代码片段：`uint64 va, pa, page; int flags; pte_t* pte; for(va = begin; va < end; va += PGSIZE)`
- 与 xv6-public 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h" #include "lib/lock.h"`
  - `kernel/proc/exec.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "proc/elf.h" #include "mem/vmem.h"`
- 与 xv6-public 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/sleeplock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
- 与 xv6-public 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfile.c:L6-L10`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "syscall/syscall.h" #include "syscall/sysfunc.h"`
- 与 xv6-public 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 xv6-public 的语言构成不同：新项目为 {'json': 18, 'make': 26, 'build': 256, 'markdown': 227, 'c': 6835, 'asm': 308}，历史项目为 {'json': 18, 'c': 9405, 'asm': 373, 'build': 286}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：29
- 含证据关键结论数：29（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
