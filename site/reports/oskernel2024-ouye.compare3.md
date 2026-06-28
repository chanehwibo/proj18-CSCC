# OSKernel2024-ouye 比较报告

- 对比历史仓库：2025 啊对的对的,嗷不对不对
- 生成时间：2026-06-28T07:19:23.249209+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2025 啊对的对的,嗷不对不对（来源：赛事历史作品）：画像相似度 score=5.55；语言构成相似度 0.31; OS 维度重合度 1.00; 代码规模接近度 0.92

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2025 啊对的对的,嗷不对不对 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `LAB4 内存管理/kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
  - `kernel/mem/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/driver/bio.c:L23-L27`：关键词命中
    代码片段：`#include "fs/vfs/fs.h" #include "fs/buf.h" #include "dev/virtio.h" struct {`
- 与 2025 啊对的对的,嗷不对不对 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `LAB4 内存管理/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `kernel/fs/vfs/fs.c:L1-L3`：关键词命中
    代码片段：`#include "fs/vfs/fs.h" #include <defs.h>`
  - `kernel/fs/vfs/ops.c:L1-L3`：关键词命中
    代码片段：`#include "fs/vfs/ops.h" #include <fs/fcntl.h>`
- 与 2025 啊对的对的,嗷不对不对 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `LAB5 内核线程/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `kernel/sys/plic.c:L4-L8`：关键词命中
    代码片段：`#include "platform.h" #include "defs.h" #include "proc/plic.h" //`
  - `kernel/trap/riscv/trap.c:L8-L12`：关键词命中
    代码片段：`#include "mem/mem.h" #include "sbi.h" #include "proc/plic.h" #include "dev/virtio.h"`
- 与 2025 啊对的对的,嗷不对不对 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `LAB5 内核线程/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `kernel/mem/vm.c:L8-L12`：关键词命中
    代码片段：`#include "defs.h" #include "fs/vfs/fs.h" #include "mem/kalloc.h" #include "lib/string.h" #include "dev/virtio.h"`
  - `kernel/mem/kalloc.c:L9-L13`：关键词命中
    代码片段：`#include "platform.h" #include "defs.h" #include "mem/kalloc.h" #include <mem/slab.h>`
- 与 2025 啊对的对的,嗷不对不对 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `LAB4 内存管理/proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
  - `kernel/proc/exec.c:L4-L8`：关键词命中
    代码片段：`#include "platform.h" #include "lock/spinlock.h" #include "proc/proc.h" #include "defs.h" #include "lib/elf.h"`
  - `kernel/proc/pipe.c:L4-L8`：关键词命中
    代码片段：`#include "param.h" #include "lock/spinlock.h" #include "proc/proc.h" #include "lock/sleeplock.h" #include "fs/fcntl.h"`
- 与 2025 啊对的对的,嗷不对不对 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `LAB5 内核线程/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `kernel/proc/semaphore.c:L1-L4`：关键词命中
    代码片段：`#include "lock/semaphore.h" #include "defs.h"`
  - `kernel/mem/uart.c:L7-L11`：关键词命中
    代码片段：`#include "mem/memlayout.h" #include "platform.h" #include "lock/spinlock.h" #include "proc/proc.h" #include "defs.h"`
- 与 2025 啊对的对的,嗷不对不对 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `LAB5 内核线程/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `kernel/sys/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "lock/spinlock.h" #include "proc/proc.h" #include "sys/syscall.h" #include "defs.h" #include "lib/string.h"`
  - `kernel/trap/riscv/trap.c:L127-L131`：关键词命中
    代码片段：`exit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 宏名重合：与 2025 啊对的对的,嗷不对不对 在“文件系统”维度发现 4 个同名定义：NELEM, NOFILE, NFILE, NINODE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/defs.h:L194-L194`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x)/sizeof((x)[0]))`
  - `include/defs.h:L143-L143`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x)/sizeof((x)[0]))`
  - `LAB1 优先级调度/param.h:L4-L4`：macro NOFILE
    代码片段：`#define NOFILE       16  // open files per process`
  - `include/param.h:L5-L5`：macro NOFILE
    代码片段：`#define NOFILE      128  // open files per process`
- 宏名重合：与 2025 啊对的对的,嗷不对不对 在“内存管理”维度发现 4 个同名定义：PGSIZE, PGROUNDUP, PGROUNDDOWN, PTE_P。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/mmu.h:L85-L85`：macro PGSIZE
    代码片段：`#define PGSIZE          4096    // bytes mapped by a page`
  - `include/platform.h:L357-L357`：macro PGSIZE
    代码片段：`#define PGSIZE 4096 // bytes per page`
  - `LAB1 优先级调度/mmu.h:L90-L90`：macro PGROUNDUP
    代码片段：`#define PGROUNDUP(sz)  (((sz)+PGSIZE-1) & ~(PGSIZE-1))`
  - `include/platform.h:L360-L360`：macro PGROUNDUP
    代码片段：`#define PGROUNDUP(sz)  (((sz)+PGSIZE-1) & ~(PGSIZE-1))`
- 宏名重合：与 2025 啊对的对的,嗷不对不对 在“同步机制”维度发现 4 个同名定义：MAXOPBLOCKS, LOGSIZE, NBUF, FSSIZE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/param.h:L10-L10`：macro MAXOPBLOCKS
    代码片段：`#define MAXOPBLOCKS  10  // max # of blocks any FS op writes`
  - `include/param.h:L12-L12`：macro MAXOPBLOCKS
    代码片段：`#define MAXOPBLOCKS  20  // max # of blocks any FS op writes`
  - `LAB1 优先级调度/param.h:L11-L11`：macro LOGSIZE
    代码片段：`#define LOGSIZE      (MAXOPBLOCKS*3)  // max data blocks in on-disk log`
  - `include/param.h:L13-L13`：macro LOGSIZE
    代码片段：`#define LOGSIZE      (MAXOPBLOCKS*3)  // max data blocks in on-disk log`
- 宏名重合：与 2025 啊对的对的,嗷不对不对 在“系统调用”维度发现 3 个同名定义：NFILE, ROOTDEV, FSSIZE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/param.h:L5-L5`：macro NFILE
    代码片段：`#define NFILE       100  // open files per system`
  - `include/param.h:L6-L6`：macro NFILE
    代码片段：`#define NFILE       100  // open files per system`
  - `LAB1 优先级调度/param.h:L8-L8`：macro ROOTDEV
    代码片段：`#define ROOTDEV       1  // device number of file system root disk`
  - `include/param.h:L9-L9`：macro ROOTDEV
    代码片段：`#define ROOTDEV       1  // device number of file system root disk`
- 宏名重合：与 2025 啊对的对的,嗷不对不对 在“设备驱动”维度发现 2 个同名定义：NDEV, ROOTDEV。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `LAB1 优先级调度/param.h:L7-L7`：macro NDEV
    代码片段：`#define NDEV         10  // maximum major device number`
  - `include/param.h:L8-L8`：macro NDEV
    代码片段：`#define NDEV         10  // maximum major device number`
  - `LAB1 优先级调度/param.h:L8-L8`：macro ROOTDEV
    代码片段：`#define ROOTDEV       1  // device number of file system root disk`
  - `include/param.h:L9-L9`：macro ROOTDEV
    代码片段：`#define ROOTDEV       1  // device number of file system root disk`
- 宏名重合：与 2025 啊对的对的,嗷不对不对 在“调度与任务管理”维度发现 2 个同名定义：NPROC, NOFILE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `LAB1 优先级调度/param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC        64  // maximum number of processes`
  - `include/param.h:L3-L3`：macro NPROC
    代码片段：`#define NPROC        64  // maximum number of processes`
  - `LAB1 优先级调度/param.h:L4-L4`：macro NOFILE
    代码片段：`#define NOFILE       16  // open files per process`
  - `include/param.h:L5-L5`：macro NOFILE
    代码片段：`#define NOFILE      128  // open files per process`
- 文件路径重合：与 2025 啊对的对的,嗷不对不对 在“文件系统”维度出现同名文件源码路径 `LAB4 内存管理/fs.c` / `kernel/fs/vfs/fs.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs/vfs/fs.c:L1-L3`：关键词命中
    代码片段：`#include "fs/vfs/fs.h" #include <defs.h>`
- 文件路径重合：与 2025 啊对的对的,嗷不对不对 在“文件系统”维度出现同名文件源码路径 `LAB5 内核线程/fs.c` / `kernel/fs/vfs/fs.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB5 内核线程/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs/vfs/fs.c:L1-L3`：关键词命中
    代码片段：`#include "fs/vfs/fs.h" #include <defs.h>`
- 文件路径重合：与 2025 啊对的对的,嗷不对不对 在“中断与异常”维度出现同名文件源码路径 `LAB4 内存管理/trap.c` / `kernel/trap/riscv/trap.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `kernel/trap/riscv/trap.c:L8-L12`：关键词命中
    代码片段：`#include "mem/mem.h" #include "sbi.h" #include "proc/plic.h" #include "dev/virtio.h"`
- 文件路径重合：与 2025 啊对的对的,嗷不对不对 在“中断与异常”维度出现同名文件源码路径 `LAB4 内存管理/trap.c` / `kernel/trap/loongarch/trap.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `kernel/trap/loongarch/trap.c:L46-L50`：fn pagefault_handler
    代码片段：`} int pagefault_handler(uint64 va, uint64 cause) { /* *TODO: 支持lazy allocation和cow`
- 文件路径重合：与 2025 啊对的对的,嗷不对不对 在“内存管理”维度出现同名文件源码路径 `LAB4 内存管理/vm.c` / `kernel/mem/vm.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB4 内存管理/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `kernel/mem/vm.c:L8-L12`：关键词命中
    代码片段：`#include "defs.h" #include "fs/vfs/fs.h" #include "mem/kalloc.h" #include "lib/string.h" #include "dev/virtio.h"`
- 文件路径重合：与 2025 啊对的对的,嗷不对不对 在“内存管理”维度出现同名文件源码路径 `LAB5 内核线程/vm.c` / `kernel/mem/vm.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB5 内核线程/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `kernel/mem/vm.c:L8-L12`：关键词命中
    代码片段：`#include "defs.h" #include "fs/vfs/fs.h" #include "mem/kalloc.h" #include "lib/string.h" #include "dev/virtio.h"`

## 相似点

- 与 2025 啊对的对的,嗷不对不对 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `LAB4 内存管理/kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
- 与 2025 啊对的对的,嗷不对不对 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `LAB4 内存管理/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 2025 啊对的对的,嗷不对不对 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `LAB5 内核线程/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
- 与 2025 啊对的对的,嗷不对不对 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `LAB5 内核线程/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
- 与 2025 啊对的对的,嗷不对不对 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `LAB4 内存管理/proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
- 与 2025 啊对的对的,嗷不对不对 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `LAB5 内核线程/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
- 与 2025 啊对的对的,嗷不对不对 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `LAB5 内核线程/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
- 与 2025 啊对的对的,嗷不对不对 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2025 啊对的对的,嗷不对不对 的语言构成不同：新项目为 {'json': 18, 'markdown': 8006, 'c': 89788, 'asm': 193770, 'build': 2630}，历史项目为 {'json': 20, 'build': 479, 'markdown': 1008, 'c': 280934, 'asm': 1166, 'text': 9, 'cpp': 36728}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：26
- 含证据关键结论数：26（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
