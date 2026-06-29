# OSKernel2024-ouye 比较报告

- 对比历史仓库：2024 RuaruaOs
- 生成时间：2026-06-29T13:39:41.699387+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2024 RuaruaOs（来源：赛事历史作品）：画像相似度 score=5.76；语言构成相似度 0.69; OS 维度重合度 1.00; 代码规模接近度 0.37

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2024 RuaruaOs 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `LAB4 内存管理/kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
  - `uart.c:L53-L57`：关键词命中
    代码片段：`uart_write_reg(IER, (1 << 0) | (1 << 1)); initlock(&uart_tx_lock, "uart"); return 0;`
  - `console.c:L1-L4`：关键词命中
    代码片段：`/* * This code segment implements a simple console interface for a RISC-V based operating system. * It provides functionalities for reading from and writing to the console, hand...`
- 与 2024 RuaruaOs 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `LAB4 内存管理/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `fs.c:L12-L16`：关键词命中
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b)) // there should be one superblock per disk device, but we run with // only one device`
  - `file.c:L100-L104`：关键词命中
    代码片段：`static num = 0; int fileread(struct file* f, uint64_t addr, int n){ int r = 0; //printf("fileread %d %d %d %p\n", f->type, f->readable, n, addr);`
- 与 2024 RuaruaOs 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `LAB5 内核线程/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `plic.c:L10-L14`：关键词命中
    代码片段：`void plicinit(void){ *(uint32_t*)(PLIC + Uart0_IRQ * 4) = 1; *(uint32_t*)(PLIC + VIRTIO0_IRQ*4) = 1; }`
  - `trap.c:L210-L214`：关键词命中
    代码片段：`//printf("holing: %d\n", holding(&myproc()->lock)); setkilled(myproc()); //panic("kernel trap"); if(!namecmp("iozone", myproc()->name)) { panic("kerneltrap");`
- 与 2024 RuaruaOs 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `LAB5 内核线程/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `vm.c:L19-L23`：关键词命中
    代码片段：`void kvmmap(pagetable_t kpgtbl, uint64_t va, uint64_t pa, uint64_t sz, int perm); pa_t walkaddr(pagetable_t pagetable, uint64_t va); pagetable_t kvmmake(void){`
  - `page.c:L18-L22`：关键词命中
    代码片段：`extern uint32_t BSS_START; extern uint32_t BSS_END; extern uint32_t HEAP_START; extern uint32_t HEAP_END; extern uint32_t HEAP_SIZE;`
- 与 2024 RuaruaOs 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `LAB4 内存管理/proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
  - `proc.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h" #include "shm.h"`
  - `thread.c:L5-L9`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "defs.h"`
- 与 2024 RuaruaOs 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `LAB5 内核线程/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `fs.c:L3-L7`：关键词命中
    代码片段：`#include "defs.h" #include "mystat.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `vm.c:L7-L11`：关键词命中
    代码片段：`#include "os.h" #include "riscv.h" #include "spinlock.h" #include "proc.h" #include "memlayout.h"`
- 与 2024 RuaruaOs 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `LAB4 内存管理/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `LAB5 内核线程/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h"`
  - `init/initcode.S:L11-L15`：关键词命中
    代码片段：`li a2, 0 li a7, 20 ecall li a0, 0`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 宏名重合：与 2024 RuaruaOs 在“设备驱动”维度发现 4 个同名定义：BACKSPACE, CONSOLE, NDEV, ROOTDEV。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/console.c:L127-L127`：macro BACKSPACE
    代码片段：`#define BACKSPACE 0x100`
  - `console.c:L24-L24`：macro BACKSPACE
    代码片段：`#define BACKSPACE 0x100`
  - `LAB1 优先级调度/file.h:L37-L37`：macro CONSOLE
    代码片段：`#define CONSOLE 1`
  - `include/file.h:L75-L75`：macro CONSOLE
    代码片段：`#define CONSOLE 1`
- 宏名重合：与 2024 RuaruaOs 在“文件系统”维度发现 4 个同名定义：NELEM, CONSOLE, min, ROOTINO。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/defs.h:L194-L194`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x)/sizeof((x)[0]))`
  - `include/defs.h:L219-L219`：macro NELEM
    代码片段：`#define NELEM(x) (sizeof(x)/sizeof((x)[0]))`
  - `LAB1 优先级调度/file.h:L37-L37`：macro CONSOLE
    代码片段：`#define CONSOLE 1`
  - `include/file.h:L75-L75`：macro CONSOLE
    代码片段：`#define CONSOLE 1`
- 宏名重合：与 2024 RuaruaOs 在“同步机制”维度发现 4 个同名定义：min, BSIZE, IBLOCK, BBLOCK。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/fs.c:L24-L24`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `fs.c:L13-L13`：macro min
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b))`
  - `LAB1 优先级调度/fs.h:L6-L6`：macro BSIZE
    代码片段：`#define BSIZE 512  // block size`
  - `include/fs.h:L6-L6`：macro BSIZE
    代码片段：`#define BSIZE 1024  // block size`
- 宏名重合：与 2024 RuaruaOs 在“系统调用”维度发现 3 个同名定义：NFILE, ROOTDEV, FSSIZE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/param.h:L5-L5`：macro NFILE
    代码片段：`#define NFILE       100  // open files per system`
  - `mkfs.c:L57-L57`：macro NFILE
    代码片段：`#define NFILE       100  // open files per system`
  - `LAB1 优先级调度/param.h:L8-L8`：macro ROOTDEV
    代码片段：`#define ROOTDEV       1  // device number of file system root disk`
  - `mkfs.c:L60-L60`：macro ROOTDEV
    代码片段：`#define ROOTDEV       1  // device number of file system root disk`
- 结构体/类型重合：与 2024 RuaruaOs 在“文件系统”维度发现 4 个同名定义：file, inode, devsw, superblock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `LAB1 优先级调度/file.h:L1-L1`：struct file
    代码片段：`struct file {`
  - `include/file.h:L18-L18`：struct file
    代码片段：`struct file {`
  - `LAB1 优先级调度/file.h:L13-L13`：struct inode
    代码片段：`struct inode {`
  - `include/file.h:L37-L37`：struct inode
    代码片段：`struct inode {`
- 函数/符号名重合：与 2024 RuaruaOs 在“调度与任务管理”维度发现 1 个同名定义：swtch。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `LAB1 优先级调度/swtch.S:L10-L10`：fn swtch
    代码片段：`swtch:`
  - `entry.S:L7-L7`：fn swtch
    代码片段：`swtch:`
- 宏名重合：与 2024 RuaruaOs 在“内存管理”维度发现 1 个同名定义：PTE_FLAGS。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `LAB1 优先级调度/mmu.h:L101-L101`：macro PTE_FLAGS
    代码片段：`#define PTE_FLAGS(pte)  ((uint)(pte) &  0xFFF)`
  - `vm.c:L155-L155`：macro PTE_FLAGS
    代码片段：`#define PTE_FLAGS(pte) ((pte) & 0x3FF)`
- 宏名重合：与 2024 RuaruaOs 在“调度与任务管理”维度发现 2 个同名定义：NPROC, NOFILE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `LAB1 优先级调度/param.h:L1-L1`：macro NPROC
    代码片段：`#define NPROC        64  // maximum number of processes`
  - `mkfs.c:L54-L54`：macro NPROC
    代码片段：`#define NPROC        64  // maximum number of processes`
  - `LAB1 优先级调度/param.h:L4-L4`：macro NOFILE
    代码片段：`#define NOFILE       16  // open files per process`
  - `mkfs.c:L56-L56`：macro NOFILE
    代码片段：`#define NOFILE       16  // open files per process`
- 结构体/类型重合：与 2024 RuaruaOs 在“内存管理”维度发现 1 个同名定义：run。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `LAB1 优先级调度/kalloc.c:L16-L16`：struct run
    代码片段：`struct run {`
  - `kalloc.c:L13-L13`：struct run
    代码片段：`struct run{`
- 结构体/类型重合：与 2024 RuaruaOs 在“同步机制”维度发现 1 个同名定义：superblock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `LAB1 优先级调度/fs.h:L14-L14`：struct superblock
    代码片段：`struct superblock {`
  - `mkfs.c:L20-L20`：struct superblock
    代码片段：`struct superblock {`
- 结构体/类型重合：与 2024 RuaruaOs 在“系统调用”维度发现 1 个同名定义：sysinfo。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `LAB1 优先级调度/sysinfo.h:L5-L5`：struct sysinfo
    代码片段：`struct sysinfo {`
  - `syscall.c:L327-L327`：struct sysinfo
    代码片段：`struct sysinfo {`
- 文件路径重合：与 2024 RuaruaOs 在“文件系统”维度出现同名文件源码路径 `LAB4 内存管理/fs.c` / `fs.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `fs.c:L12-L16`：关键词命中
    代码片段：`#define min(a, b) ((a) < (b) ? (a) : (b)) // there should be one superblock per disk device, but we run with // only one device`
- 文件路径重合：与 2024 RuaruaOs 在“文件系统”维度出现同名文件源码路径 `LAB4 内存管理/fs.h` / `include/fs.h`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
  - `include/fs.h:L36-L40`：关键词命中
    代码片段：`/* Fields for EXT4_DYNAMIC_REV superblocks only. */ /* 0 */	uint32_t first_inode;	 /* First non-reserved inode */ /* 0 */	uint16_t inode_size;	  /* Size of inode structure */ /*...`
- 文件路径重合：与 2024 RuaruaOs 在“中断与异常”维度出现同名文件源码路径 `LAB4 内存管理/trap.c` / `trap.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `trap.c:L210-L214`：关键词命中
    代码片段：`//printf("holing: %d\n", holding(&myproc()->lock)); setkilled(myproc()); //panic("kernel trap"); if(!namecmp("iozone", myproc()->name)) { panic("kerneltrap");`
- 文件路径重合：与 2024 RuaruaOs 在“中断与异常”维度出现同名文件源码路径 `LAB5 内核线程/trap.c` / `trap.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB5 内核线程/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `trap.c:L210-L214`：关键词命中
    代码片段：`//printf("holing: %d\n", holding(&myproc()->lock)); setkilled(myproc()); //panic("kernel trap"); if(!namecmp("iozone", myproc()->name)) { panic("kerneltrap");`
- 文件路径重合：与 2024 RuaruaOs 在“内存管理”维度出现同名文件源码路径 `LAB4 内存管理/vm.c` / `vm.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB4 内存管理/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `vm.c:L19-L23`：关键词命中
    代码片段：`void kvmmap(pagetable_t kpgtbl, uint64_t va, uint64_t pa, uint64_t sz, int perm); pa_t walkaddr(pagetable_t pagetable, uint64_t va); pagetable_t kvmmake(void){`
- 文件路径重合：与 2024 RuaruaOs 在“内存管理”维度出现同名文件源码路径 `LAB5 内核线程/vm.c` / `vm.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `LAB5 内核线程/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `vm.c:L19-L23`：关键词命中
    代码片段：`void kvmmap(pagetable_t kpgtbl, uint64_t va, uint64_t pa, uint64_t sz, int perm); pa_t walkaddr(pagetable_t pagetable, uint64_t va); pagetable_t kvmmake(void){`

## 相似点

- 与 2024 RuaruaOs 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/ide.c:L1-L3`：关键词命中
    代码片段：`// Simple PIO-based (non-DMA) IDE driver code. #include "types.h"`
  - `LAB4 内存管理/kbd.c:L2-L6`：关键词命中
    代码片段：`#include "x86.h" #include "defs.h" #include "kbd.h" int`
- 与 2024 RuaruaOs 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
  - `LAB4 内存管理/fs.h:L7-L11`：关键词命中
    代码片段：`// Disk layout: // [ boot block | super block | log | inode blocks | //                                          free bit map | data blocks] //`
- 与 2024 RuaruaOs 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
  - `LAB5 内核线程/trap.c:L9-L13`：关键词命中
    代码片段：`#include "spinlock.h" // Interrupt descriptor table (shared by all CPUs). struct gatedesc idt[256]; extern uint vectors[];  // in vectors.S: array of 256 entry pointers`
- 与 2024 RuaruaOs 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
  - `LAB5 内核线程/vm.c:L9-L13`：关键词命中
    代码片段：`extern char data[];  // defined by kernel.ld pde_t *kpgdir;  // for use in scheduler() // Set up CPU's kernel segment descriptors.`
- 与 2024 RuaruaOs 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/proc.c:L5-L9`：关键词命中
    代码片段：`#include "mmu.h" #include "x86.h" #include "proc.h" #include "spinlock.h"`
  - `LAB4 内存管理/proc.h:L2-L6`：关键词命中
    代码片段：`struct cpu { uchar apicid;                // Local APIC ID struct context *scheduler;   // swtch() here to enter scheduler struct taskstate ts;         // Used by x86 to find st...`
- 与 2024 RuaruaOs 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
  - `LAB5 内核线程/fs.c:L16-L20`：关键词命中
    代码片段：`#include "mmu.h" #include "proc.h" #include "spinlock.h" #include "sleeplock.h" #include "fs.h"`
- 与 2024 RuaruaOs 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `LAB4 内存管理/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
  - `LAB5 内核线程/syscall.c:L6-L10`：关键词命中
    代码片段：`#include "proc.h" #include "x86.h" #include "syscall.h" // User code makes a system call with INT T_SYSCALL.`
- 与 2024 RuaruaOs 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2024 RuaruaOs 的语言构成不同：待测作品为 {'json': 18, 'markdown': 8006, 'c': 89788, 'asm': 193770, 'build': 2630}，历史样本为 {'json': 20, 'c': 10966, 'text': 16804, 'asm': 25140, 'build': 368, 'markdown': 1365}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：31
- 含证据关键结论数：31（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
