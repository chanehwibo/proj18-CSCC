# OSKernel2024-NQOS 比较报告

- 对比历史仓库：2025 松蓝
- 生成时间：2026-06-29T13:39:39.625674+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2025 松蓝（来源：赛事历史作品）：画像相似度 score=6.75；语言构成相似度 0.88; OS 维度重合度 1.00; 代码规模接近度 0.98

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2025 松蓝 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART #include "memlayout.h" #include "dev/uart.h"`
  - `kernel/dev/console.c:L1-L4`：关键词命中
    代码片段：`#include <stdarg.h> #include "dev/console.h" #include "dev/uart.h" #include "mem/vmem.h"`
- 与 2025 松蓝 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `kernel/fs/vfs.c:L1-L3`：关键词命中
    代码片段：`#include "fs/vfs.h" #include "lock/lock.h" #include "lib/str.h"`
  - `kernel/fs/fat32/fat32_dir.c:L4-L8`：关键词命中
    代码片段：`#include "fs/base_stat.h" #include "fs/fat32.h" #include "fs/vfs.h" #include "proc/cpu.h" #include "lib/str.h"`
- 与 2025 松蓝 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from trampoline.S //`
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "riscv.h"`
  - `kernel/dev/timer.c:L2-L6`：关键词命中
    代码片段：`#include "sbi.h" #include "riscv.h" #include "dev/timer.h" #include "lib/print.h"`
- 与 2025 松蓝 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/vm.c:L8-L12`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char*)PGROUNDUP((uint64)pa_start); for(; p + PGSIZE <= (char*)pa_end; p += PGSIZE) kfree(p); }`
  - `kernel/mem/kvm.c:L16-L20`：关键词命中
    代码片段：`// 申请L2内核页表空间 kernel_pagetable = (pgtbl_t)pmem_alloc_pages(1, true); // printf("kernel pagetable = %p\n",kernel_pagetable); assert(kernel_pagetable != NULL, "kvm.c->kvm_init: 1\...`
  - `kernel/mem/uvm.c:L11-L15`：关键词命中
    代码片段：`#include "common.h" // 用户态虚拟内存管理：静态vm_region池 + SV39页表 + COW/mmap 支持 #define N_VM_REGION 128`
- 与 2025 松蓝 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L23-L27`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;          // The process running on this cpu, or null. struct context context;     // swtch() here to enter scheduler(). int nof...`
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "lock/lock.h" #include "riscv.h"`
  - `kernel/proc/exec.c:L1-L5`：关键词命中
    代码片段：`//exec.c #include "proc/elf.h" #include "proc/cpu.h" #include "mem/vmem.h"`
- 与 2025 松蓝 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/bio.c:L17-L21`：关键词命中
    代码片段：`#include "types.h" #include "param.h" #include "spinlock.h" #include "sleeplock.h" #include "riscv.h"`
  - `kernel/lock/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lock/lock.h" #include "proc/cpu.h" #include "lib/print.h"`
  - `kernel/lock/sleeplock.c:L1-L4`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "lock/lock.h" void sleeplock_init(sleeplock_t* lock, char* name)`
- 与 2025 松蓝 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/trap.c:L74-L78`：关键词命中
    代码片段：`exit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
  - `kernel/syscall/syscall.c:L2-L6`：关键词命中
    代码片段：`#include "proc/cpu.h"          // myproc #include "mem/vmem.h"          // uvm_copy #include "syscall/sysnum.h" #include "syscall/sysfile.h" #include "syscall/sysproc.h"`
  - `kernel/syscall/sysfile.c:L1-L3`：关键词命中
    代码片段：`#include "syscall/sysfile.h" #include "fs/vfs.h" #include "syscall/syscall.h"`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 宏名重合：与 2025 松蓝 在“设备驱动”维度发现 4 个同名定义：BACKSPACE, INPUT_BUF_SIZE, CONSOLE, RHR。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/console.c:L25-L25`：macro BACKSPACE
    代码片段：`#define BACKSPACE 0x100`
  - `kernel/dev/console.c:L9-L9`：macro BACKSPACE
    代码片段：`#define BACKSPACE 0x100`
  - `kernel/console.c:L48-L48`：macro INPUT_BUF_SIZE
    代码片段：`#define INPUT_BUF_SIZE 128`
  - `include/dev/console.h:L6-L6`：macro INPUT_BUF_SIZE
    代码片段：`#define INPUT_BUF_SIZE 128`
- 宏名重合：与 2025 松蓝 在“文件系统”维度发现 4 个同名定义：NOFILE, NFILE, NINODE, SYS_fstat。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/param.h:L4-L4`：macro NOFILE
    代码片段：`#define NOFILE       16  // open files per process`
  - `include/common.h:L44-L44`：macro NOFILE
    代码片段：`#define NOFILE 128                 // 单个进程同时打开的最大文件数量`
  - `kernel/param.h:L5-L5`：macro NFILE
    代码片段：`#define NFILE       100  // open files per system`
  - `include/common.h:L43-L43`：macro NFILE
    代码片段：`#define NFILE  256                // 整个系统同时打开的最大文件数量`
- 宏名重合：与 2025 松蓝 在“中断与异常”维度发现 4 个同名定义：PLIC_PRIORITY, PLIC_PENDING, PLIC_SENABLE, PLIC_SPRIORITY。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/memlayout.h:L30-L30`：macro PLIC_PRIORITY
    代码片段：`#define PLIC_PRIORITY (PLIC + 0x0)`
  - `include/memlayout.h:L7-L7`：macro PLIC_PRIORITY
    代码片段：`#define PLIC_PRIORITY(id) (PLIC_BASE + (id) * 4)`
  - `kernel/memlayout.h:L31-L31`：macro PLIC_PENDING
    代码片段：`#define PLIC_PENDING (PLIC + 0x1000)`
  - `include/memlayout.h:L8-L8`：macro PLIC_PENDING
    代码片段：`#define PLIC_PENDING (PLIC_BASE + 0x1000)`
- 宏名重合：与 2025 松蓝 在“内存管理”维度发现 4 个同名定义：TRAPFRAME, SATP_SV39, MAKE_SATP, PTE_V。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/memlayout.h:L59-L59`：macro TRAPFRAME
    代码片段：`#define TRAPFRAME (TRAMPOLINE - PGSIZE)`
  - `include/memlayout.h:L45-L45`：macro TRAPFRAME
    代码片段：`#define TRAPFRAME (TRAMPOLINE - 4096)`
  - `kernel/riscv.h:L225-L225`：macro SATP_SV39
    代码片段：`#define SATP_SV39 (8L << 60)`
  - `include/mem/vmem.h:L39-L39`：macro SATP_SV39
    代码片段：`#define SATP_SV39 (8L << 60)  // MODE = SV39`
- 宏名重合：与 2025 松蓝 在“调度与任务管理”维度发现 3 个同名定义：NPROC, SIGSTOP, SYS_sched_yield。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC        64  // maximum number of processes`
  - `include/common.h:L26-L26`：macro NPROC
    代码片段：`#define NPROC 64                  // 进程最大数量`
  - `kernel/signal.h:L16-L16`：macro SIGSTOP
    代码片段：`#define SIGSTOP      19    // Stop    Stop process`
  - `include/signal/signal.h:L25-L25`：macro SIGSTOP
    代码片段：`#define SIGSTOP    19   // Stop process unblockable`
- 宏名重合：与 2025 松蓝 在“系统调用”维度发现 4 个同名定义：TRAPFRAME, SYS_exit, SYS_read, SYS_fstat。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/memlayout.h:L59-L59`：macro TRAPFRAME
    代码片段：`#define TRAPFRAME (TRAMPOLINE - PGSIZE)`
  - `include/memlayout.h:L45-L45`：macro TRAPFRAME
    代码片段：`#define TRAPFRAME (TRAMPOLINE - 4096)`
  - `kernel/syscall.h:L3-L3`：macro SYS_exit
    代码片段：`#define SYS_exit    2`
  - `user/include/syscall_num.h:L27-L27`：macro SYS_exit
    代码片段：`#define SYS_exit        93`
- 结构体/类型重合：与 2025 松蓝 在“设备驱动”维度发现 4 个同名定义：virtq_desc, virtq_avail, virtq_used_elem, virtq_used。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/virtio.h:L53-L53`：struct virtq_desc
    代码片段：`struct virtq_desc {`
  - `include/dev/virtio.h:L45-L45`：struct virtq_desc
    代码片段：`struct virtq_desc {`
  - `kernel/virtio.h:L63-L63`：struct virtq_avail
    代码片段：`struct virtq_avail {`
  - `include/dev/virtio.h:L55-L55`：struct virtq_avail
    代码片段：`struct virtq_avail {`
- 结构体/类型重合：与 2025 松蓝 在“调度与任务管理”维度发现 4 个同名定义：context, cpu, trapframe, procstate。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/proc.h:L4-L4`：struct context
    代码片段：`struct context {`
  - `include/proc/proc.h:L55-L55`：struct context
    代码片段：`typedef struct context {`
  - `kernel/proc.h:L24-L24`：struct cpu
    代码片段：`struct cpu {`
  - `include/proc/cpu.h:L6-L6`：struct cpu
    代码片段：`typedef struct cpu {`
- 结构体/类型重合：与 2025 松蓝 在“中断与异常”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/proc.h:L45-L45`：struct trapframe
    代码片段：`struct trapframe {`
  - `include/proc/proc.h:L15-L15`：struct trapframe
    代码片段：`typedef struct trapframe {`
- 结构体/类型重合：与 2025 松蓝 在“内存管理”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/proc.h:L45-L45`：struct trapframe
    代码片段：`struct trapframe {`
  - `include/proc/proc.h:L15-L15`：struct trapframe
    代码片段：`typedef struct trapframe {`
- 结构体/类型重合：与 2025 松蓝 在“同步机制”维度发现 2 个同名定义：sleeplock, spinlock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/sleeplock.h:L2-L2`：struct sleeplock
    代码片段：`struct sleeplock {`
  - `include/lock/lock.h:L12-L12`：struct sleeplock
    代码片段：`typedef struct sleeplock {`
  - `kernel/spinlock.h:L2-L2`：struct spinlock
    代码片段：`struct spinlock {`
  - `include/lock/lock.h:L6-L6`：struct spinlock
    代码片段：`typedef struct spinlock {`
- 结构体/类型重合：与 2025 松蓝 在“系统调用”维度发现 1 个同名定义：trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/proc.h:L45-L45`：struct trapframe
    代码片段：`struct trapframe {`
  - `include/proc/proc.h:L15-L15`：struct trapframe
    代码片段：`typedef struct trapframe {`
- 文件路径重合：与 2025 松蓝 在“设备驱动”维度出现同名文件源码路径 `kernel/uart.c` / `kernel/dev/uart.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART #include "memlayout.h" #include "dev/uart.h"`
- 文件路径重合：与 2025 松蓝 在“设备驱动”维度出现同名文件源码路径 `kernel/virtio.h` / `include/dev/virtio.h`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
  - `include/dev/virtio.h:L6-L10`：macro VIRTIO_MMIO_MAGIC_VALUE
    代码片段：`// virtio mmio control registers, mapped starting at 0x10001000. // from qemu virtio_mmio.h #define VIRTIO_MMIO_MAGIC_VALUE 0x000 // 0x74726976 #define VIRTIO_MMIO_VERSION 0x004...`
- 文件路径重合：与 2025 松蓝 在“中断与异常”维度出现同名文件源码路径 `kernel/plic.c` / `kernel/dev/plic.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "riscv.h"`
- 文件路径重合：与 2025 松蓝 在“中断与异常”维度出现同名文件源码路径 `kernel/uart.c` / `kernel/dev/uart.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/uart.c:L28-L32`：macro ISR
    代码片段：`#define FCR_FIFO_ENABLE (1<<0) #define FCR_FIFO_CLEAR (3<<1) // clear the content of the two FIFOs #define ISR 2                 // interrupt status register #define LCR 3...`
  - `kernel/dev/uart.c:L14-L18`：macro ISR
    代码片段：`#define FCR_FIFO_ENABLE (1<<0) #define FCR_FIFO_CLEAR  (3<<1) #define ISR  2      // interrupt status reg #define LCR  3      // line control reg #define LCR_EIGHT_BITS  (3<<0)...`
- 文件路径重合：与 2025 松蓝 在“调度与任务管理”维度出现同名文件源码路径 `kernel/proc.c` / `kernel/proc/proc.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc/proc.c:L2-L6`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "proc/cpu.h" #include "proc/initcode.h" #include "mem/pmem.h"`
- 文件路径重合：与 2025 松蓝 在“系统调用”维度出现同名文件源码路径 `kernel/syscall.c` / `kernel/syscall/syscall.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
  - `kernel/syscall/syscall.c:L2-L6`：关键词命中
    代码片段：`#include "proc/cpu.h"          // myproc #include "mem/vmem.h"          // uvm_copy #include "syscall/sysnum.h" #include "syscall/sysfile.h" #include "syscall/sysproc.h"`

## 相似点

- 与 2025 松蓝 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 与 2025 松蓝 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 2025 松蓝 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from trampoline.S //`
- 与 2025 松蓝 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/vm.c:L8-L12`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char*)PGROUNDUP((uint64)pa_start); for(; p + PGSIZE <= (char*)pa_end; p += PGSIZE) kfree(p); }`
- 与 2025 松蓝 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L23-L27`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;          // The process running on this cpu, or null. struct context context;     // swtch() here to enter scheduler(). int nof...`
- 与 2025 松蓝 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/bio.c:L17-L21`：关键词命中
    代码片段：`#include "types.h" #include "param.h" #include "spinlock.h" #include "sleeplock.h" #include "riscv.h"`
- 与 2025 松蓝 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/trap.c:L74-L78`：关键词命中
    代码片段：`exit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
- 与 2025 松蓝 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2025 松蓝 的语言构成不同：待测作品为 {'json': 18, 'markdown': 1725, 'build': 197, 'c': 13428, 'asm': 519}，历史样本为 {'json': 20, 'make': 30, 'build': 469, 'markdown': 39, 'c': 15277, 'asm': 340}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：32
- 含证据关键结论数：32（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
