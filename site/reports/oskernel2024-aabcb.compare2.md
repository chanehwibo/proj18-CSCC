# OSKernel2024-aabcb 比较报告

- 对比历史仓库：xv6-riscv
- 生成时间：2026-06-28T12:14:43.945650+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- xv6-riscv（来源：教学基线）：画像相似度 score=11.55；同属 independent 风格; 架构重合度 1.00; 语言构成相似度 0.93; OS 维度重合度 1.00; 代码规模接近度 0.68

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 xv6-riscv 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 与 xv6-riscv 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 xv6-riscv 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
- 与 xv6-riscv 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/mem/kvm.c:L12-L16`：关键词命中
    代码片段：`// 根据pagetable,找到va对应的pte // 若设置alloc=true 则在PTE无效时尝试申请一个物理页 // 成功返回PTE, 失败返回NULL`
  - `kernel/mem/uvm.c:L12-L16`：关键词命中
    代码片段：`uint64 va, pa, page; int flags; pte_t* pte; for(va = begin; va < end; va += PGSIZE)`
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
- 与 xv6-riscv 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h" #include "lib/lock.h"`
  - `kernel/proc/exec.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "proc/elf.h" #include "mem/vmem.h"`
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
- 与 xv6-riscv 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/sleeplock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/vm.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "defs.h" #include "spinlock.h" #include "proc.h" #include "fs.h"`
- 与 xv6-riscv 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfile.c:L6-L10`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "syscall/syscall.h" #include "syscall/sysfunc.h"`
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 宏名重合：与 xv6-riscv 在“设备驱动”维度发现 4 个同名定义：RHR, THR, IER, IER_TX_ENABLE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/dev/uart.c:L11-L11`：macro RHR
    代码片段：`#define RHR 0                 // receive holding register (for input bytes)`
  - `kernel/uart.c:L24-L24`：macro RHR
    代码片段：`#define RHR             0        // receive holding register (for input bytes)`
  - `kernel/dev/uart.c:L12-L12`：macro THR
    代码片段：`#define THR 0                 // transmit holding register (for output bytes)`
  - `kernel/uart.c:L25-L25`：macro THR
    代码片段：`#define THR             0        // transmit holding register (for output bytes)`
- 宏名重合：与 xv6-riscv 在“中断与异常”维度发现 4 个同名定义：PLIC_PRIORITY, PLIC_PENDING, PLIC_SENABLE, PLIC_SPRIORITY。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/memlayout.h:L23-L23`：macro PLIC_PRIORITY
    代码片段：`#define PLIC_PRIORITY(id) (PLIC_BASE + (id) * 4)`
  - `kernel/memlayout.h:L30-L30`：macro PLIC_PRIORITY
    代码片段：`#define PLIC_PRIORITY        (PLIC + 0x0)`
  - `include/memlayout.h:L24-L24`：macro PLIC_PENDING
    代码片段：`#define PLIC_PENDING (PLIC_BASE + 0x1000)`
  - `kernel/memlayout.h:L31-L31`：macro PLIC_PENDING
    代码片段：`#define PLIC_PENDING         (PLIC + 0x1000)`
- 宏名重合：与 xv6-riscv 在“内存管理”维度发现 4 个同名定义：PGSIZE, TRAMPOLINE, TRAPFRAME, KSTACK。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/common.h:L30-L30`：macro PGSIZE
    代码片段：`#define PGSIZE 4096          // 物理页大小`
  - `kernel/riscv.h:L352-L352`：macro PGSIZE
    代码片段：`#define PGSIZE  4096 // bytes per page`
  - `include/memlayout.h:L43-L43`：macro TRAMPOLINE
    代码片段：`#define TRAMPOLINE (VA_MAX - PGSIZE)`
  - `kernel/memlayout.h:L44-L44`：macro TRAMPOLINE
    代码片段：`#define TRAMPOLINE (MAXVA - PGSIZE)`
- 宏名重合：与 xv6-riscv 在“系统调用”维度发现 4 个同名定义：TRAPFRAME, SYS_fork, SYS_wait, SYS_exit。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/memlayout.h:L46-L46`：macro TRAPFRAME
    代码片段：`#define TRAPFRAME (TRAMPOLINE - PGSIZE)`
  - `kernel/memlayout.h:L59-L59`：macro TRAPFRAME
    代码片段：`#define TRAPFRAME (TRAMPOLINE - PGSIZE)`
  - `user/syscall_num.h:L8-L8`：macro SYS_fork
    代码片段：`#define SYS_fork         4`
  - `kernel/syscall.h:L2-L2`：macro SYS_fork
    代码片段：`#define SYS_fork   1`
- 结构体/类型重合：与 xv6-riscv 在“文件系统”维度发现 3 个同名定义：dirent, file, inode。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `mkfs/mkfs.c:L37-L37`：struct dirent
    代码片段：`typedef struct dirent {`
  - `kernel/fs.h:L57-L57`：struct dirent
    代码片段：`struct dirent {`
  - `include/fs/file.h:L22-L22`：struct file
    代码片段：`typedef struct file {`
  - `kernel/file.h:L1-L1`：struct file
    代码片段：`struct file {`
- 函数/符号名重合：与 xv6-riscv 在“调度与任务管理”维度发现 1 个同名定义：swtch。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/proc/swtch.S:L7-L7`：fn swtch
    代码片段：`swtch:`
  - `kernel/swtch.S:L9-L9`：fn swtch
    代码片段：`swtch:`
- 结构体/类型重合：与 xv6-riscv 在“调度与任务管理”维度发现 4 个同名定义：cpu, context, trapframe, proc。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/proc/cpu.h:L7-L7`：struct cpu
    代码片段：`typedef struct cpu {`
  - `kernel/proc.h:L22-L22`：struct cpu
    代码片段：`struct cpu {`
  - `include/proc/proc.h:L17-L17`：struct context
    代码片段：`typedef struct context {`
  - `kernel/proc.h:L2-L2`：struct context
    代码片段：`struct context {`
- 宏名重合：与 xv6-riscv 在“文件系统”维度发现 1 个同名定义：SYS_fstat。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/syscall/sysnum.h:L19-L19`：macro SYS_fstat
    代码片段：`#define SYS_fstat        14`
  - `kernel/syscall.h:L9-L9`：macro SYS_fstat
    代码片段：`#define SYS_fstat  8`
- 宏名重合：与 xv6-riscv 在“调度与任务管理”维度发现 1 个同名定义：NPROC。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/common.h:L28-L28`：macro NPROC
    代码片段：`#define NPROC 64             // 最大进程数量`
  - `kernel/param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC       64                // maximum number of processes`
- 结构体/类型重合：与 xv6-riscv 在“中断与异常”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/proc/proc.h:L37-L37`：struct trapframe
    代码片段：`typedef struct trapframe {`
  - `kernel/proc.h:L40-L40`：struct trapframe
    代码片段：`struct trapframe {`
- 结构体/类型重合：与 xv6-riscv 在“内存管理”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/proc/proc.h:L37-L37`：struct trapframe
    代码片段：`typedef struct trapframe {`
  - `kernel/proc.h:L40-L40`：struct trapframe
    代码片段：`struct trapframe {`
- 结构体/类型重合：与 xv6-riscv 在“同步机制”维度发现 2 个同名定义：spinlock, sleeplock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/lib/lock.h:L6-L6`：struct spinlock
    代码片段：`typedef struct spinlock {`
  - `kernel/spinlock.h:L2-L2`：struct spinlock
    代码片段：`struct spinlock {`
  - `include/lib/lock.h:L12-L12`：struct sleeplock
    代码片段：`typedef struct sleeplock {`
  - `kernel/sleeplock.h:L2-L2`：struct sleeplock
    代码片段：`struct sleeplock {`
- 结构体/类型重合：与 xv6-riscv 在“系统调用”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/proc/proc.h:L37-L37`：struct trapframe
    代码片段：`typedef struct trapframe {`
  - `kernel/proc.h:L40-L40`：struct trapframe
    代码片段：`struct trapframe {`
- 文件路径重合：与 xv6-riscv 在“设备驱动”维度出现同名文件源码路径 `kernel/dev/uart.c` / `kernel/uart.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
- 文件路径重合：与 xv6-riscv 在“设备驱动”维度出现同名文件源码路径 `include/dev/virtio.h` / `kernel/virtio.h`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `include/dev/virtio.h:L14-L18`：macro VIRTIO_MMIO_MAGIC_VALUE
    代码片段：`// virtio mmio control registers, mapped starting at 0x10001000. // from qemu virtio_mmio.h #define VIRTIO_MMIO_MAGIC_VALUE 0x000 // 0x74726976 #define VIRTIO_MMIO_VERSION 0x004...`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 文件路径重合：与 xv6-riscv 在“文件系统”维度出现同名文件源码路径 `kernel/fs/fs.c` / `kernel/fs.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
- 文件路径重合：与 xv6-riscv 在“文件系统”维度出现同名文件源码路径 `kernel/fs/file.c` / `kernel/file.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/fs/file.c:L3-L7`：关键词命中
    代码片段：`#include "fs/dir.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/file.h" #include "mem/vmem.h"`
  - `kernel/file.c:L105-L109`：关键词命中
    代码片段：`// addr is a user virtual address. int fileread(struct file *f, uint64 addr, int n) { int r = 0;`
- 文件路径重合：与 xv6-riscv 在“中断与异常”维度出现同名文件源码路径 `kernel/dev/plic.c` / `kernel/plic.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
- 文件路径重合：与 xv6-riscv 在“调度与任务管理”维度出现同名文件源码路径 `kernel/proc/proc.c` / `kernel/proc.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/proc/proc.c:L4-L8`：关键词命中
    代码片段：`#include "mem/vmem.h" #include "mem/mmap.h" #include "proc/cpu.h" #include "proc/initcode.h" #include "memlayout.h"`
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`

## 相似点

- 与 xv6-riscv 同属 independent 风格。（置信度：medium）
- 与 xv6-riscv 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
- 与 xv6-riscv 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
- 与 xv6-riscv 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
- 与 xv6-riscv 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/mem/kvm.c:L12-L16`：关键词命中
    代码片段：`// 根据pagetable,找到va对应的pte // 若设置alloc=true 则在PTE无效时尝试申请一个物理页 // 成功返回PTE, 失败返回NULL`
  - `kernel/mem/uvm.c:L12-L16`：关键词命中
    代码片段：`uint64 va, pa, page; int flags; pte_t* pte; for(va = begin; va < end; va += PGSIZE)`
- 与 xv6-riscv 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h" #include "lib/lock.h"`
  - `kernel/proc/exec.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "proc/elf.h" #include "mem/vmem.h"`
- 与 xv6-riscv 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/sleeplock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
- 与 xv6-riscv 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfile.c:L6-L10`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "syscall/syscall.h" #include "syscall/sysfunc.h"`
- 与 xv6-riscv 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 xv6-riscv 的语言构成不同：新项目为 {'json': 18, 'make': 26, 'build': 256, 'markdown': 227, 'c': 6835, 'asm': 308}，历史项目为 {'json': 18, 'build': 199, 'c': 11718, 'asm': 276}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：33
- 含证据关键结论数：33（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
