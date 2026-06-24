# xv6-riscv 比较报告

- 对比历史仓库：OSKernel2024-NQOS, OSKernel2024-aabcb, OSKernel2024-ouye
- 生成时间：2026-06-19T08:41:01.134561+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- OSKernel2024-NQOS（来源：比赛作品样本（获奖等级未核验））：score=11.55；同属 independent 风格; 架构重合度 1.00; 语言构成相似度 0.88; OS 维度重合度 1.00; 代码规模接近度 0.79
- OSKernel2024-aabcb（来源：比赛作品样本（获奖等级未核验））：score=11.55；同属 independent 风格; 架构重合度 1.00; 语言构成相似度 0.93; OS 维度重合度 1.00; 代码规模接近度 0.68
- OSKernel2024-ouye（来源：比赛作品样本（获奖等级未核验））：score=9.91；同属 independent 风格; 架构重合度 1.00; 语言构成相似度 0.34; OS 维度重合度 1.00; 代码规模接近度 0.24

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 OSKernel2024-NQOS 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 与 OSKernel2024-NQOS 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 OSKernel2024-NQOS 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from trampoline.S //`
- 与 OSKernel2024-NQOS 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
  - `kernel/vm.c:L8-L12`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char*)PGROUNDUP((uint64)pa_start); for(; p + PGSIZE <= (char*)pa_end; p += PGSIZE) kfree(p); }`
- 与 OSKernel2024-NQOS 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L23-L27`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;          // The process running on this cpu, or null. struct context context;     // swtch() here to enter scheduler(). int nof...`
- 与 OSKernel2024-NQOS 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/vm.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "defs.h" #include "spinlock.h" #include "proc.h" #include "fs.h"`
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/bio.c:L17-L21`：关键词命中
    代码片段：`#include "types.h" #include "param.h" #include "spinlock.h" #include "sleeplock.h" #include "riscv.h"`
- 与 OSKernel2024-NQOS 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
  - `kernel/trap.c:L74-L78`：关键词命中
    代码片段：`exit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
- 与 OSKernel2024-aabcb 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
- 与 OSKernel2024-aabcb 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
- 与 OSKernel2024-aabcb 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
- 与 OSKernel2024-aabcb 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
  - `kernel/mem/kvm.c:L12-L16`：关键词命中
    代码片段：`// 根据pagetable,找到va对应的pte // 若设置alloc=true 则在PTE无效时尝试申请一个物理页 // 成功返回PTE, 失败返回NULL`
  - `kernel/mem/uvm.c:L12-L16`：关键词命中
    代码片段：`uint64 va, pa, page; int flags; pte_t* pte; for(va = begin; va < end; va += PGSIZE)`
- 与 OSKernel2024-aabcb 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h" #include "lib/lock.h"`
  - `kernel/proc/exec.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "proc/elf.h" #include "mem/vmem.h"`
- 与 OSKernel2024-aabcb 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/vm.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "defs.h" #include "spinlock.h" #include "proc.h" #include "fs.h"`
  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/sleeplock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
- 与 OSKernel2024-aabcb 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfile.c:L6-L10`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "syscall/syscall.h" #include "syscall/sysfunc.h"`
- 与 OSKernel2024-ouye 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
  - `LAB4 内存管理/ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `LAB4 内存管理/kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
- 与 OSKernel2024-ouye 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `LAB4 内存管理/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `LAB4 内存管理/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 OSKernel2024-ouye 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `LAB5 内核线程/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
- 与 OSKernel2024-ouye 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
  - `LAB4 内存管理/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `LAB5 内核线程/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
- 与 OSKernel2024-ouye 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
  - `LAB4 内存管理/proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `LAB4 内存管理/proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
- 与 OSKernel2024-ouye 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/vm.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "defs.h" #include "spinlock.h" #include "proc.h" #include "fs.h"`
  - `LAB4 内存管理/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `LAB5 内核线程/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
- 与 OSKernel2024-ouye 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
  - `LAB4 内存管理/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `LAB5 内核线程/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 与 OSKernel2024-NQOS 在“文件系统”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：addr, f, file, fileread, int, n, r, struct。（置信度：high）
  证据：
  - `kernel/file.c:L105-L109`：关键词命中
    代码片段：`// addr is a user virtual address. int fileread(struct file *f, uint64 addr, int n) { int r = 0;`
  - `kernel/file.c:L105-L109`：关键词命中
    代码片段：`// addr is a user virtual address. int fileread(struct file *f, uint64 addr, int n) { int r = 0;`
- 与 OSKernel2024-NQOS 在“文件系统”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：magic, size, struct, superblock, uint。（置信度：high）
  证据：
  - `kernel/fs.h:L11-L15`：struct superblock
    代码片段：`// mkfs computes the super block and builds an initial file system. The // super block describes the disk layout: struct superblock { uint magic;      // Must be FSMAGIC uint si...`
  - `kernel/fs.h:L12-L16`：struct superblock
    代码片段：`// mkfs computes the super block and builds an initial file system. The // super block describes the disk layout: struct superblock { uint magic;        // Must be FSMAGIC uint...`
- 与 OSKernel2024-NQOS 在“内存管理”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：char, for, kfree, p, pa_end, pa_start, pgroundup, pgsize。（置信度：high）
  证据：
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char*)PGROUNDUP((uint64)pa_start); for(; p + PGSIZE <= (char*)pa_end; p += PGSIZE) kfree(p); }`
- 与 OSKernel2024-NQOS 在“内存管理”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：next, run, struct。（置信度：high）
  证据：
  - `kernel/kalloc.c:L15-L19`：struct run
    代码片段：`// defined by kernel.ld. struct run { struct run *next; };`
  - `kernel/kalloc.c:L15-L19`：struct run
    代码片段：`// defined by kernel.ld. struct run { struct run *next; };`
- 与 OSKernel2024-NQOS 在“调度与任务管理”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：context, cpu, int, noff, proc, struct。（置信度：high）
  证据：
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
  - `kernel/proc.h:L23-L27`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;          // The process running on this cpu, or null. struct context context;     // swtch() here to enter scheduler(). int nof...`
- 与 OSKernel2024-NQOS 在“调度与任务管理”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：context, ra, sp, struct, uint64。（置信度：high）
  证据：
  - `kernel/proc.h:L1-L4`：struct context
    代码片段：`// Saved registers for kernel context switches. struct context { uint64 ra; uint64 sp;`
  - `kernel/proc.h:L2-L6`：struct context
    代码片段：`#define SIGINT 2 // Saved registers for kernel context switches. struct context { uint64 ra; uint64 sp;`
- 宏名重合：与 OSKernel2024-NQOS 在“设备驱动”维度发现 4 个同名定义：BACKSPACE, INPUT_BUF_SIZE, CONSOLE, UART0。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/console.c:L25-L25`：macro BACKSPACE
    代码片段：`#define BACKSPACE 0x100       // erase the last output character`
  - `kernel/console.c:L25-L25`：macro BACKSPACE
    代码片段：`#define BACKSPACE 0x100`
  - `kernel/console.c:L51-L51`：macro INPUT_BUF_SIZE
    代码片段：`#define INPUT_BUF_SIZE 128`
  - `kernel/console.c:L48-L48`：macro INPUT_BUF_SIZE
    代码片段：`#define INPUT_BUF_SIZE 128`
- 宏名重合：与 OSKernel2024-NQOS 在“文件系统”维度发现 4 个同名定义：NELEM, major, minor, mkdev。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/defs.h:L185-L185`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x) / sizeof((x)[0]))`
  - `kernel/defs.h:L212-L212`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x)/sizeof((x)[0]))`
  - `kernel/file.h:L12-L12`：macro major
    代码片段：`#define major(dev)  ((dev) >> 16 & 0xFFFF)`
  - `kernel/file.h:L12-L12`：macro major
    代码片段：`#define major(dev)  ((dev) >> 16 & 0xFFFF)`
- 宏名重合：与 OSKernel2024-NQOS 在“中断与异常”维度发现 4 个同名定义：UART0, UART0_IRQ, VIRTIO0, VIRTIO0_IRQ。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/memlayout.h:L21-L21`：macro UART0
    代码片段：`#define UART0     0x10000000L`
  - `kernel/memlayout.h:L21-L21`：macro UART0
    代码片段：`#define UART0 0x10000000L`
  - `kernel/memlayout.h:L22-L22`：macro UART0_IRQ
    代码片段：`#define UART0_IRQ 10`
  - `kernel/memlayout.h:L22-L22`：macro UART0_IRQ
    代码片段：`#define UART0_IRQ 10`
- 宏名重合：与 OSKernel2024-NQOS 在“内存管理”维度发现 4 个同名定义：NELEM, TRAMPOLINE, KSTACK, TRAPFRAME。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/defs.h:L185-L185`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x) / sizeof((x)[0]))`
  - `kernel/defs.h:L212-L212`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x)/sizeof((x)[0]))`
  - `kernel/memlayout.h:L44-L44`：macro TRAMPOLINE
    代码片段：`#define TRAMPOLINE (MAXVA - PGSIZE)`
  - `kernel/memlayout.h:L44-L44`：macro TRAMPOLINE
    代码片段：`#define TRAMPOLINE (MAXVA - PGSIZE)`
- 宏名重合：与 OSKernel2024-NQOS 在“调度与任务管理”维度发现 3 个同名定义：min, NPROC, NOFILE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `kernel/fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `kernel/param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC       64                // maximum number of processes`
  - `kernel/param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC        64  // maximum number of processes`
- 宏名重合：与 OSKernel2024-NQOS 在“同步机制”维度发现 4 个同名定义：min, BSIZE, IBLOCK, BBLOCK。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `kernel/fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `kernel/fs.h:L5-L5`：macro BSIZE
    代码片段：`#define BSIZE   1024 // block size`
  - `kernel/fs.h:L6-L6`：macro BSIZE
    代码片段：`#define BSIZE 1024  // block size`
- 结构体/类型重合：与 OSKernel2024-NQOS 在“设备驱动”维度发现 4 个同名定义：virtq_desc, virtq_avail, virtq_used_elem, virtq_used。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/virtio.h:L55-L55`：struct virtq_desc
    代码片段：`struct virtq_desc {`
  - `kernel/virtio.h:L53-L53`：struct virtq_desc
    代码片段：`struct virtq_desc {`
  - `kernel/virtio.h:L65-L65`：struct virtq_avail
    代码片段：`struct virtq_avail {`
  - `kernel/virtio.h:L63-L63`：struct virtq_avail
    代码片段：`struct virtq_avail {`
- 结构体/类型重合：与 OSKernel2024-NQOS 在“文件系统”维度发现 4 个同名定义：file, inode, devsw, superblock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/file.h:L1-L1`：struct file
    代码片段：`struct file {`
  - `kernel/file.h:L1-L1`：struct file
    代码片段：`struct file {`
  - `kernel/file.h:L17-L17`：struct inode
    代码片段：`struct inode {`
  - `kernel/file.h:L17-L17`：struct inode
    代码片段：`struct inode {`
- 函数/符号名重合：与 OSKernel2024-NQOS 在“调度与任务管理”维度发现 1 个同名定义：swtch。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/swtch.S:L9-L9`：fn swtch
    代码片段：`swtch:`
  - `kernel/swtch.S:L9-L9`：fn swtch
    代码片段：`swtch:`
- 结构体/类型重合：与 OSKernel2024-NQOS 在“调度与任务管理”维度发现 4 个同名定义：context, cpu, trapframe, procstate。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/proc.h:L2-L2`：struct context
    代码片段：`struct context {`
  - `kernel/proc.h:L4-L4`：struct context
    代码片段：`struct context {`
  - `kernel/proc.h:L22-L22`：struct cpu
    代码片段：`struct cpu {`
  - `kernel/proc.h:L24-L24`：struct cpu
    代码片段：`struct cpu {`
- 结构体/类型重合：与 OSKernel2024-NQOS 在“同步机制”维度发现 3 个同名定义：superblock, sleeplock, spinlock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/fs.h:L13-L13`：struct superblock
    代码片段：`struct superblock {`
  - `kernel/fs.h:L14-L14`：struct superblock
    代码片段：`struct superblock {`
  - `kernel/sleeplock.h:L2-L2`：struct sleeplock
    代码片段：`struct sleeplock {`
  - `kernel/sleeplock.h:L2-L2`：struct sleeplock
    代码片段：`struct sleeplock {`
- 结构体/类型重合：与 OSKernel2024-aabcb 在“文件系统”维度发现 3 个同名定义：file, inode, dirent。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/file.h:L1-L1`：struct file
    代码片段：`struct file {`
  - `include/fs/file.h:L22-L22`：struct file
    代码片段：`typedef struct file {`
  - `kernel/file.h:L17-L17`：struct inode
    代码片段：`struct inode {`
  - `include/fs/inode.h:L32-L32`：struct inode
    代码片段：`typedef struct inode {`
- 函数/符号名重合：与 OSKernel2024-aabcb 在“调度与任务管理”维度发现 1 个同名定义：swtch。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/swtch.S:L9-L9`：fn swtch
    代码片段：`swtch:`
  - `kernel/proc/swtch.S:L7-L7`：fn swtch
    代码片段：`swtch:`
- 结构体/类型重合：与 OSKernel2024-aabcb 在“调度与任务管理”维度发现 4 个同名定义：context, cpu, trapframe, proc。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/proc.h:L2-L2`：struct context
    代码片段：`struct context {`
  - `include/proc/proc.h:L17-L17`：struct context
    代码片段：`typedef struct context {`
  - `kernel/proc.h:L22-L22`：struct cpu
    代码片段：`struct cpu {`
  - `include/proc/cpu.h:L7-L7`：struct cpu
    代码片段：`typedef struct cpu {`
- 函数/符号名重合：与 OSKernel2024-ouye 在“调度与任务管理”维度发现 1 个同名定义：swtch。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/swtch.S:L9-L9`：fn swtch
    代码片段：`swtch:`
  - `LAB1 优先级调度/swtch.S:L10-L10`：fn swtch
    代码片段：`swtch:`
- 文件路径重合：与 OSKernel2024-NQOS 在“设备驱动”维度出现同路径源码路径 `kernel/uart.c` / `kernel/uart.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
- 文件路径重合：与 OSKernel2024-NQOS 在“设备驱动”维度出现同路径源码路径 `kernel/virtio.h` / `kernel/virtio.h`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 文件路径重合：与 OSKernel2024-NQOS 在“文件系统”维度出现同路径源码路径 `kernel/fs.c` / `kernel/fs.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
- 文件路径重合：与 OSKernel2024-NQOS 在“文件系统”维度出现同路径源码路径 `kernel/fs.h` / `kernel/fs.h`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `kernel/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 文件路径重合：与 OSKernel2024-NQOS 在“中断与异常”维度出现同路径源码路径 `kernel/plic.c` / `kernel/plic.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
- 文件路径重合：与 OSKernel2024-NQOS 在“中断与异常”维度出现同路径源码路径 `kernel/trap.c` / `kernel/trap.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from trampoline.S //`

## 相似点

- 与 OSKernel2024-NQOS 同属 independent 风格。（置信度：medium）
- 与 OSKernel2024-NQOS 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 与 OSKernel2024-NQOS 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 OSKernel2024-NQOS 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
- 与 OSKernel2024-NQOS 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
- 与 OSKernel2024-NQOS 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
- 与 OSKernel2024-NQOS 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/vm.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "defs.h" #include "spinlock.h" #include "proc.h" #include "fs.h"`
- 与 OSKernel2024-NQOS 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
- 与 OSKernel2024-NQOS 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）
- 与 OSKernel2024-aabcb 同属 independent 风格。（置信度：medium）
- 与 OSKernel2024-aabcb 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 与 OSKernel2024-aabcb 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 OSKernel2024-aabcb 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
- 与 OSKernel2024-aabcb 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
- 与 OSKernel2024-aabcb 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
- 与 OSKernel2024-aabcb 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/vm.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "defs.h" #include "spinlock.h" #include "proc.h" #include "fs.h"`
- 与 OSKernel2024-aabcb 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
- 与 OSKernel2024-aabcb 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）
- 与 OSKernel2024-ouye 同属 independent 风格。（置信度：medium）
- 与 OSKernel2024-ouye 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver for 16550a UART. //`
  - `kernel/virtio.h:L1-L4`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 与 OSKernel2024-ouye 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `kernel/fs.h:L6-L10`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 OSKernel2024-ouye 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L31-L35`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from, and returns to, trampoline.S // return value is user satp for trampoline.S to switch to.`
- 与 OSKernel2024-ouye 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/vm.c:L10-L14`：关键词命中
    代码片段：`/* * the kernel's page table. */ pagetable_t kernel_pagetable;`
  - `kernel/kalloc.c:L36-L40`：关键词命中
    代码片段：`char *p; p = (char *)PGROUNDUP((uint64)pa_start); for (; p + PGSIZE <= (char *)pa_end; p += PGSIZE) kfree(p); }`
- 与 OSKernel2024-ouye 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
  - `kernel/proc.h:L21-L25`：关键词命中
    代码片段：`// Per-CPU state. struct cpu { struct proc *proc;      // The process running on this cpu, or null. struct context context; // swtch() here to enter scheduler(). int noff;...`
- 与 OSKernel2024-ouye 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `kernel/vm.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "defs.h" #include "spinlock.h" #include "proc.h" #include "fs.h"`
- 与 OSKernel2024-ouye 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`kexit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
- 与 OSKernel2024-ouye 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 OSKernel2024-NQOS 的语言构成不同：新项目为 {'json': 18, 'build': 199, 'c': 11718, 'asm': 276}，历史项目为 {'json': 18, 'markdown': 1725, 'build': 197, 'c': 13428, 'asm': 519}。（置信度：medium）
- 与 OSKernel2024-aabcb 的语言构成不同：新项目为 {'json': 18, 'build': 199, 'c': 11718, 'asm': 276}，历史项目为 {'json': 18, 'make': 26, 'build': 256, 'markdown': 227, 'c': 6835, 'asm': 308}。（置信度：medium）
- 与 OSKernel2024-ouye 的语言构成不同：新项目为 {'json': 18, 'build': 199, 'c': 11718, 'asm': 276}，历史项目为 {'json': 18, 'markdown': 8006, 'c': 89788, 'asm': 193770, 'build': 2630}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：69
- 含证据关键结论数：69（100.0%）
- 无效证据引用数：0
- 未确认结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
