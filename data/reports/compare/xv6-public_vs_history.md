# xv6-public 比较报告

- 对比历史仓库：os-tutorial, xv6-riscv
- 生成时间：2026-06-24T04:10:42.974448+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- os-tutorial（来源：架构参考样本）：score=8.08；同属 teaching-monolithic 风格; 架构重合度 1.00; 语言构成相似度 0.48; OS 维度重合度 0.29; 代码规模接近度 0.99
- xv6-riscv（来源：教学基线）：score=6.79；语言构成相似度 0.97; OS 维度重合度 1.00; 代码规模接近度 0.84

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 os-tutorial 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
  - `15-video-ports/kernel/kernel.c:L18-L22`：关键词命中
    代码片段：`/* Now you can examine both variables using gdb, since we still * don't know how to print strings on screen. Run 'make debug' and * on the gdb console: * breakpoint kernel.c:21...`
- 与 os-tutorial 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `mp.h:L50-L54`：关键词命中
    代码片段：`#define MPBUS     0x01  // One per bus #define MPIOAPIC  0x02  // One per I/O APIC #define MPIOINTR  0x03  // One per bus interrupt source #define MPLINTR   0x04  // One per sys...`
  - `20-interrupts-timer/kernel/kernel.c:L1-L3`：关键词命中
    代码片段：`#include "../cpu/isr.h" #include "../cpu/timer.h" #include "../drivers/keyboard.h"`
  - `20-interrupts-timer/drivers/keyboard.c:L1-L5`：关键词命中
    代码片段：`#include "keyboard.h" #include "ports.h" #include "../cpu/isr.h" #include "screen.h"`
- 与 xv6-riscv 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 与 xv6-riscv 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 xv6-riscv 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `mp.h:L50-L54`：关键词命中
    代码片段：`#define MPBUS     0x01  // One per bus #define MPIOAPIC  0x02  // One per I/O APIC #define MPIOINTR  0x03  // One per bus interrupt source #define MPLINTR   0x04  // One per sys...`
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
- 与 xv6-riscv 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `kalloc.c:L1-L4`：关键词命中
    代码片段：`// Physical memory allocator, intended to allocate // memory for user processes, kernel stacks, page table pages, // and pipe buffers. Allocates 4096-byte pages.`
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
- 与 xv6-riscv 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
- 与 xv6-riscv 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `bio.c:L22-L26`：关键词命中
    代码片段：`#include "defs.h" #include "param.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/vm.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "defs.h" #include "spinlock.h" #include "proc.h" #include "fs.h"`
- 与 xv6-riscv 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 与 xv6-riscv 在“文件系统”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：dinode, major, short, struct, type。（置信度：high）
  证据：
  - `fs.h:L27-L31`：struct dinode
    代码片段：`// On-disk inode structure struct dinode { short type;           // File type short major;          // Major device number (T_DEV only)`
  - `kernel/fs.h:L29-L33`：struct dinode
    代码片段：`// On-disk inode structure struct dinode { short type;              // File type short major;             // Major device number (T_DEVICE only)`
- 与 xv6-riscv 在“文件系统”维度发现片段级代码相似度 0.84 （token=0.75, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：size, struct, superblock, uint。（置信度：high）
  证据：
  - `fs.h:L12-L16`：struct superblock
    代码片段：`// mkfs computes the super block and builds an initial file system. The // super block describes the disk layout: struct superblock { uint size;         // Size of file system i...`
  - `kernel/fs.h:L11-L15`：struct superblock
    代码片段：`// mkfs computes the super block and builds an initial file system. The // super block describes the disk layout: struct superblock { uint magic;      // Must be FSMAGIC uint si...`
- 与 xv6-riscv 在“内存管理”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：next, run, struct。（置信度：high）
  证据：
  - `kalloc.c:L14-L18`：struct run
    代码片段：`// defined by the kernel linker script in kernel.ld struct run { struct run *next; };`
  - `kernel/kalloc.c:L15-L19`：struct run
    代码片段：`// defined by kernel.ld. struct run { struct run *next; };`
- 与 xv6-riscv 在“调度与任务管理”维度发现片段级代码相似度 0.74 （token=0.60, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：context, cpu, struct。（置信度：medium）
  证据：
  - `proc.h:L1-L4`：struct cpu
    代码片段：`// Per-CPU state struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler`
  - `kernel/proc.h:L20-L24`：struct cpu
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler().`
- 与 xv6-riscv 在“调度与任务管理”维度发现片段级代码相似度 0.68 （token=0.50, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：context, cpu, struct。（置信度：medium）
  证据：
  - `proc.h:L1-L4`：struct cpu
    代码片段：`// Per-CPU state struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
- 宏名重合：与 xv6-riscv 在“设备驱动”维度发现 4 个同名定义：BACKSPACE, CONSOLE, NDEV, ROOTDEV。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `console.c:L127-L127`：macro BACKSPACE
    代码片段：`#define BACKSPACE 0x100`
  - `kernel/console.c:L25-L25`：macro BACKSPACE
    代码片段：`#define BACKSPACE 0x100       // erase the last output character`
  - `file.h:L37-L37`：macro CONSOLE
    代码片段：`#define CONSOLE 1`
  - `kernel/file.h:L40-L40`：macro CONSOLE
    代码片段：`#define CONSOLE 1`
- 宏名重合：与 xv6-riscv 在“文件系统”维度发现 4 个同名定义：NELEM, CONSOLE, min, ROOTINO。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `defs.h:L190-L190`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x)/sizeof((x)[0]))`
  - `kernel/defs.h:L185-L185`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x) / sizeof((x)[0]))`
  - `file.h:L37-L37`：macro CONSOLE
    代码片段：`#define CONSOLE 1`
  - `kernel/file.h:L40-L40`：macro CONSOLE
    代码片段：`#define CONSOLE 1`
- 宏名重合：与 xv6-riscv 在“内存管理”维度发现 4 个同名定义：PGSIZE, PGROUNDUP, PGROUNDDOWN, PTE_W。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `mmu.h:L85-L85`：macro PGSIZE
    代码片段：`#define PGSIZE          4096    // bytes mapped by a page`
  - `kernel/riscv.h:L352-L352`：macro PGSIZE
    代码片段：`#define PGSIZE  4096 // bytes per page`
  - `mmu.h:L90-L90`：macro PGROUNDUP
    代码片段：`#define PGROUNDUP(sz)  (((sz)+PGSIZE-1) & ~(PGSIZE-1))`
  - `kernel/riscv.h:L355-L355`：macro PGROUNDUP
    代码片段：`#define PGROUNDUP(sz)  (((sz) + PGSIZE - 1) & ~(PGSIZE - 1))`
- 宏名重合：与 xv6-riscv 在“调度与任务管理”维度发现 3 个同名定义：min, NPROC, NOFILE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `kernel/fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC        64  // maximum number of processes`
  - `kernel/param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC       64                // maximum number of processes`
- 宏名重合：与 xv6-riscv 在“同步机制”维度发现 4 个同名定义：min, BSIZE, IBLOCK, BBLOCK。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `kernel/fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `fs.h:L6-L6`：macro BSIZE
    代码片段：`#define BSIZE 512  // block size`
  - `kernel/fs.h:L5-L5`：macro BSIZE
    代码片段：`#define BSIZE   1024 // block size`
- 宏名重合：与 xv6-riscv 在“系统调用”维度发现 4 个同名定义：NFILE, ROOTDEV, FSSIZE, SYS_fork。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `param.h:L5-L5`：macro NFILE
    代码片段：`#define NFILE       100  // open files per system`
  - `kernel/param.h:L4-L4`：macro NFILE
    代码片段：`#define NFILE       100               // open files per system`
  - `param.h:L8-L8`：macro ROOTDEV
    代码片段：`#define ROOTDEV       1  // device number of file system root disk`
  - `kernel/param.h:L7-L7`：macro ROOTDEV
    代码片段：`#define ROOTDEV     1                 // device number of file system root disk`
- 结构体/类型重合：与 xv6-riscv 在“文件系统”维度发现 4 个同名定义：file, inode, devsw, superblock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `file.h:L1-L1`：struct file
    代码片段：`struct file {`
  - `kernel/file.h:L1-L1`：struct file
    代码片段：`struct file {`
  - `file.h:L13-L13`：struct inode
    代码片段：`struct inode {`
  - `kernel/file.h:L17-L17`：struct inode
    代码片段：`struct inode {`
- 函数/符号名重合：与 xv6-riscv 在“调度与任务管理”维度发现 1 个同名定义：swtch。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `swtch.S:L10-L10`：fn swtch
    代码片段：`swtch:`
  - `kernel/swtch.S:L9-L9`：fn swtch
    代码片段：`swtch:`
- 结构体/类型重合：与 xv6-riscv 在“调度与任务管理”维度发现 4 个同名定义：cpu, context, procstate, proc。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `proc.h:L2-L2`：struct cpu
    代码片段：`struct cpu {`
  - `kernel/proc.h:L22-L22`：struct cpu
    代码片段：`struct cpu {`
  - `proc.h:L27-L27`：struct context
    代码片段：`struct context {`
  - `kernel/proc.h:L2-L2`：struct context
    代码片段：`struct context {`
- 结构体/类型重合：与 xv6-riscv 在“同步机制”维度发现 3 个同名定义：superblock, sleeplock, spinlock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `fs.h:L14-L14`：struct superblock
    代码片段：`struct superblock {`
  - `kernel/fs.h:L13-L13`：struct superblock
    代码片段：`struct superblock {`
  - `sleeplock.h:L2-L2`：struct sleeplock
    代码片段：`struct sleeplock {`
  - `kernel/sleeplock.h:L2-L2`：struct sleeplock
    代码片段：`struct sleeplock {`
- 结构体/类型重合：与 xv6-riscv 在“中断与异常”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `x86.h:L150-L150`：struct trapframe
    代码片段：`struct trapframe {`
  - `kernel/proc.h:L40-L40`：struct trapframe
    代码片段：`struct trapframe {`
- 结构体/类型重合：与 xv6-riscv 在“内存管理”维度发现 2 个同名定义：run, trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kalloc.c:L16-L16`：struct run
    代码片段：`struct run {`
  - `kernel/kalloc.c:L17-L17`：struct run
    代码片段：`struct run {`
  - `x86.h:L150-L150`：struct trapframe
    代码片段：`struct trapframe {`
  - `kernel/proc.h:L40-L40`：struct trapframe
    代码片段：`struct trapframe {`
- 结构体/类型重合：与 xv6-riscv 在“系统调用”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `x86.h:L150-L150`：struct trapframe
    代码片段：`struct trapframe {`
  - `kernel/proc.h:L40-L40`：struct trapframe
    代码片段：`struct trapframe {`
- 文件路径重合：与 xv6-riscv 在“文件系统”维度出现同名文件源码路径 `fs.c` / `kernel/fs.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
- 文件路径重合：与 xv6-riscv 在“文件系统”维度出现同名文件源码路径 `fs.h` / `kernel/fs.h`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 文件路径重合：与 xv6-riscv 在“中断与异常”维度出现同名文件源码路径 `trap.c` / `kernel/trap.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
- 文件路径重合：与 xv6-riscv 在“中断与异常”维度出现同名文件源码路径 `vm.c` / `kernel/vm.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `vm.c:L21-L25`：关键词命中
    代码片段：`// Cannot share a CODE descriptor for both kernel and user // because it would have to have DPL_USR, but the CPU forbids // an interrupt from CPL=0 to DPL=3. c = &cpus[cpuid()];...`
  - `kernel/vm.c:L33-L37`：关键词命中
    代码片段：`kvmmap(kpgtbl, VIRTIO0, VIRTIO0, PGSIZE, PTE_R | PTE_W); // PLIC kvmmap(kpgtbl, PLIC, PLIC, 0x4000000, PTE_R | PTE_W);`
- 文件路径重合：与 xv6-riscv 在“内存管理”维度出现同名文件源码路径 `vm.c` / `kernel/vm.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
- 文件路径重合：与 xv6-riscv 在“内存管理”维度出现同名文件源码路径 `kalloc.c` / `kernel/kalloc.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kalloc.c:L1-L4`：关键词命中
    代码片段：`// Physical memory allocator, intended to allocate // memory for user processes, kernel stacks, page table pages, // and pipe buffers. Allocates 4096-byte pages.`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`

## 相似点

- 与 os-tutorial 同属 teaching-monolithic 风格。（置信度：medium）
- 与 os-tutorial 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
- 与 os-tutorial 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `mp.h:L50-L54`：关键词命中
    代码片段：`#define MPBUS     0x01  // One per bus #define MPIOAPIC  0x02  // One per I/O APIC #define MPIOINTR  0x03  // One per bus interrupt source #define MPLINTR   0x04  // One per sys...`
- 与 os-tutorial 在 driver, interrupt 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）
- 与 xv6-riscv 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
- 与 xv6-riscv 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 xv6-riscv 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `mp.h:L50-L54`：关键词命中
    代码片段：`#define MPBUS     0x01  // One per bus #define MPIOAPIC  0x02  // One per I/O APIC #define MPIOINTR  0x03  // One per bus interrupt source #define MPLINTR   0x04  // One per sys...`
- 与 xv6-riscv 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `kalloc.c:L1-L4`：关键词命中
    代码片段：`// Physical memory allocator, intended to allocate // memory for user processes, kernel stacks, page table pages, // and pipe buffers. Allocates 4096-byte pages.`
- 与 xv6-riscv 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
- 与 xv6-riscv 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `bio.c:L22-L26`：关键词命中
    代码片段：`#include "defs.h" #include "param.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
- 与 xv6-riscv 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
- 与 xv6-riscv 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 os-tutorial 的语言构成不同：新项目为 {'json': 18, 'c': 9405, 'asm': 373, 'build': 286}，历史项目为 {'json': 18, 'markdown': 1418, 'asm': 4100, 'c': 4193, 'build': 495}。（置信度：medium）
- 与 xv6-riscv 的语言构成不同：新项目为 {'json': 18, 'c': 9405, 'asm': 373, 'build': 286}，历史项目为 {'json': 18, 'build': 199, 'c': 11718, 'asm': 276}。（置信度：medium）

## 可能创新点

- 新项目在“文件系统”维度有可确认实现，而历史样本 os-tutorial 当前未确认该维度。（置信度：low）
  证据：
  - `fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 新项目在“内存管理”维度有可确认实现，而历史样本 os-tutorial 当前未确认该维度。（置信度：low）
  证据：
  - `vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `kalloc.c:L1-L4`：关键词命中
    代码片段：`// Physical memory allocator, intended to allocate // memory for user processes, kernel stacks, page table pages, // and pipe buffers. Allocates 4096-byte pages.`
- 新项目在“调度与任务管理”维度有可确认实现，而历史样本 os-tutorial 当前未确认该维度。（置信度：low）
  证据：
  - `proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
- 新项目在“同步机制”维度有可确认实现，而历史样本 os-tutorial 当前未确认该维度。（置信度：low）
  证据：
  - `fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `bio.c:L22-L26`：关键词命中
    代码片段：`#include "defs.h" #include "param.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
- 新项目在“系统调用”维度有可确认实现，而历史样本 os-tutorial 当前未确认该维度。（置信度：low）
  证据：
  - `syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`

## 附录：核验摘要

- 关键结论数：47
- 含证据关键结论数：47（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
