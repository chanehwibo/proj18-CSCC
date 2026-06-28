# OSKernel2024-aabcb 比较报告

- 对比历史仓库：2025 达达乐队
- 生成时间：2026-06-28T12:36:03.955866+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2025 达达乐队（来源：赛事历史作品）：画像相似度 score=6.65；语言构成相似度 0.97; OS 维度重合度 1.00; 代码规模接近度 0.72

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2025 达达乐队 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
  - `kernel/dev/uart.c:L1-L4`：关键词命中
    代码片段：`/* * uart.c - 16550a UART 驱动（轮询 + 中断回显） * * 提供：`
  - `kernel/dev/virtio.c:L1-L4`：关键词命中
    代码片段：`/* * virtio.c - QEMU virtio-blk（虚拟磁盘）驱动 * * QEMU 侧常见配置：-device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0`
- 与 2025 达达乐队 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
  - `kernel/fs/fs.c:L4-L8`：关键词命中
    代码片段：`* 当前版本的 fs_init() 做了两件事： *   1) 初始化 buf cache，并从磁盘读取超级块到内存副本 sb； *   2) 运行一段 inode 读写自测逻辑（便于实验阶段验证 inode/data 分配链路）。 * * 注意：自测结束后会进入 while(1) 死循环。`
  - `kernel/fs/dir.c:L7-L11`：关键词命中
    代码片段：`* * 锁语义： *   - 目录项的查找/增删/遍历都要求调用者持有父目录 inode 的睡眠锁（pip->slk）。 *   - path_* 系列会按需对中间目录 inode 加锁、查找目录项、再移动到下一段。 */`
- 与 2025 达达乐队 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
  - `kernel/dev/plic.c:L1-L4`：关键词命中
    代码片段：`/* * plic.c - PLIC（Platform-level interrupt controller） * * 负责外部中断（external interrupt）的分发：`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
- 与 2025 达达乐队 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/mem/kvm.c:L12-L16`：关键词命中
    代码片段：`// 根据pagetable,找到va对应的pte // 若设置alloc=true 则在PTE无效时尝试申请一个物理页 // 成功返回PTE, 失败返回NULL`
  - `kernel/mem/uvm.c:L12-L16`：关键词命中
    代码片段：`uint64 va, pa, page; int flags; pte_t* pte; for(va = begin; va < end; va += PGSIZE)`
  - `kernel/fs/elf.c:L7-L11`：关键词命中
    代码片段：`*       1) 按页分配物理页并映射到用户页表 *       2) 从 elf_data 拷贝文件内容（filesz），其余 memsz 区域保持为 0（BSS） *   - 输出入口地址 e_entry 与 heap_top（最高段末尾按页对齐） */`
  - `kernel/fs/file.c:L433-L437`：关键词命中
    代码片段：`uint32 done = 0; while (done < to_read) { uint32 page_idx = (pos + done) / PGSIZE; uint32 page_off = (pos + done) % PGSIZE; if (page_idx >= RAMFS_MAX_PAGES || rf->pages[page_idx...`
- 与 2025 达达乐队 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h" #include "lib/lock.h"`
  - `kernel/proc/exec.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "proc/elf.h" #include "mem/vmem.h"`
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h"`
  - `kernel/proc/proc.c:L4-L8`：关键词命中
    代码片段：`#include "dev/uart.h" #include "mem/vmem.h" #include "proc/cpu.h" #include "proc/initcode.h" #include "trap/trap.h"`
- 与 2025 达达乐队 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/sleeplock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/spinlock.c:L1-L4`：关键词命中
    代码片段：`/* * spinlock.c - 自旋锁与可嵌套的关/开中断 * * 这份实现的核心思路：`
  - `kernel/lib/sleeplock.c:L13-L17`：关键词命中
    代码片段：`*/ #include "lib/lock.h" #include "proc/proc.h" #include "proc/cpu.h"`
- 与 2025 达达乐队 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfile.c:L6-L10`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "syscall/syscall.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfunc.c:L3-L7`：关键词命中
    代码片段：`* * 目标与定位： *   - 为 oscomp / riscv-syscalls-testing 等测试提供“够用”的 Linux 风格 syscall 语义。 *   - 这是一个兼容层而非完整的 Linux：很多 syscall 仅实现最小子集，或直接返回固定值。 *`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 与 2025 达达乐队 在“同步机制”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：char, int, locked, name, spinlock, struct, typedef。（置信度：high）
  证据：
  - `include/lib/lock.h:L4-L8`：关键词命中
    代码片段：`#include "common.h" typedef struct spinlock { int locked; char* name;`
  - `include/lib/lock.h:L16-L20`：struct spinlock
    代码片段：`#include "common.h" typedef struct spinlock { int locked;   // 0/1：是否持有 char* name;   // 调试用名称`
- 与 2025 达达乐队 在“设备驱动”维度发现片段级代码相似度 0.72 （token=0.71, structure=0.73）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：blk, bus, device, drive, mmio, qemu, virtio, x0。（置信度：medium）
  证据：
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
  - `kernel/dev/virtio.c:L1-L4`：关键词命中
    代码片段：`/* * virtio.c - QEMU virtio-blk（虚拟磁盘）驱动 * * QEMU 侧常见配置：-device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0`
- 与 2025 达达乐队 在“设备驱动”维度发现片段级代码相似度 0.59 （token=0.53, structure=0.70）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：buf, return, virtio_disk_rw。（置信度：medium）
  证据：
  - `kernel/fs/buf.c:L133-L137`：关键词命中
    代码片段：`// 从磁盘读取对应块的数据 virtio_disk_rw(&b->buf, 0); return &b->buf;`
  - `kernel/fs/buf.c:L143-L147`：关键词命中
    代码片段：`sleeplock_acquire(&bn->buf.slk); // 从磁盘读取 virtio_disk_rw(&bn->buf, false); return &bn->buf; }`
- 与 2025 达达乐队 在“文件系统”维度发现片段级代码相似度 0.65 （token=0.69, structure=0.57）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：buf, buf_node, buf_t, next, struct, typedef。（置信度：medium）
  证据：
  - `kernel/fs/buf.c:L9-L13`：struct buf_node
    代码片段：`// 将buf包装成双向循环链表的node typedef struct buf_node { buf_t buf; struct buf_node* next;`
  - `kernel/fs/buf.c:L29-L33`：struct buf_node
    代码片段：`* 说明：buf_t 是第一个成员，因此 (buf_node_t*)buf_t 指针转换是合法的。 */ typedef struct buf_node { buf_t buf; struct buf_node* next;`
- 函数/符号名重合：与 2025 达达乐队 在“中断与异常”维度发现 4 个同名定义：trampoline, user_vector, user_return, kernel_vector。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/trap/trampoline.S:L9-L9`：fn trampoline
    代码片段：`trampoline:`
  - `kernel/trap/trampoline.S:L23-L23`：fn trampoline
    代码片段：`trampoline:`
  - `kernel/trap/trampoline.S:L14-L14`：fn user_vector
    代码片段：`user_vector:`
  - `kernel/trap/trampoline.S:L28-L28`：fn user_vector
    代码片段：`user_vector:`
- 函数/符号名重合：与 2025 达达乐队 在“系统调用”维度发现 4 个同名定义：trampoline, user_vector, user_return, kernel_vector。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/trap/trampoline.S:L9-L9`：fn trampoline
    代码片段：`trampoline:`
  - `kernel/trap/trampoline.S:L23-L23`：fn trampoline
    代码片段：`trampoline:`
  - `kernel/trap/trampoline.S:L14-L14`：fn user_vector
    代码片段：`user_vector:`
  - `kernel/trap/trampoline.S:L28-L28`：fn user_vector
    代码片段：`user_vector:`
- 宏名重合：与 2025 达达乐队 在“设备驱动”维度发现 4 个同名定义：UART_BASE, UART_IRQ, VIRTIO_BASE, VIRTIO_IRQ。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/memlayout.h:L14-L14`：macro UART_BASE
    代码片段：`#define UART_BASE  0x10000000ul`
  - `include/memlayout.h:L9-L9`：macro UART_BASE
    代码片段：`#define UART_BASE  0x10000000ul`
  - `include/memlayout.h:L15-L15`：macro UART_IRQ
    代码片段：`#define UART_IRQ   10`
  - `include/memlayout.h:L10-L10`：macro UART_IRQ
    代码片段：`#define UART_IRQ   10`
- 宏名重合：与 2025 达达乐队 在“文件系统”维度发现 4 个同名定义：FS_MAGIC, FT_UNUSED, FT_DIR, FT_FILE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `mkfs/mkfs.c:L10-L10`：macro FS_MAGIC
    代码片段：`#define FS_MAGIC 0x12345678`
  - `mkfs/mkfs.c:L10-L10`：macro FS_MAGIC
    代码片段：`#define FS_MAGIC 0x12345678`
  - `mkfs/mkfs.c:L43-L43`：macro FT_UNUSED
    代码片段：`#define FT_UNUSED 0`
  - `mkfs/mkfs.c:L44-L44`：macro FT_UNUSED
    代码片段：`#define FT_UNUSED 0`
- 宏名重合：与 2025 达达乐队 在“中断与异常”维度发现 4 个同名定义：UART_IRQ, VIRTIO_IRQ, PLIC_BASE, PLIC_PRIORITY。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/memlayout.h:L15-L15`：macro UART_IRQ
    代码片段：`#define UART_IRQ   10`
  - `include/memlayout.h:L10-L10`：macro UART_IRQ
    代码片段：`#define UART_IRQ   10`
  - `include/memlayout.h:L19-L19`：macro VIRTIO_IRQ
    代码片段：`#define VIRTIO_IRQ   1`
  - `include/memlayout.h:L51-L51`：macro VIRTIO_IRQ
    代码片段：`#define VIRTIO_IRQ 1`
- 宏名重合：与 2025 达达乐队 在“内存管理”维度发现 4 个同名定义：__COMMON_H__, NULL, NCPU, PGSIZE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/common.h:L3-L3`：macro __COMMON_H__
    代码片段：`#define __COMMON_H__`
  - `include/common.h:L3-L3`：macro __COMMON_H__
    代码片段：`#define __COMMON_H__`
  - `include/common.h:L20-L20`：macro NULL
    代码片段：`#define NULL ((void*)0)`
  - `include/common.h:L20-L20`：macro NULL
    代码片段：`#define NULL ((void*)0)`
- 宏名重合：与 2025 达达乐队 在“调度与任务管理”维度发现 4 个同名定义：NPROC, __CPU_H__, __PROC_H__, FILE_PER_PROC。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/common.h:L28-L28`：macro NPROC
    代码片段：`#define NPROC 64             // 最大进程数量`
  - `include/proc/proc.h:L22-L22`：macro NPROC
    代码片段：`#define NPROC 64`
  - `include/proc/cpu.h:L2-L2`：macro __CPU_H__
    代码片段：`#define __CPU_H__`
  - `include/proc/cpu.h:L2-L2`：macro __CPU_H__
    代码片段：`#define __CPU_H__`
- 宏名重合：与 2025 达达乐队 在“同步机制”维度发现 4 个同名定义：BLOCK_SIZE, N_DATA_BLOCK, N_INODE_BLOCK, N_BLOCK。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/common.h:L32-L32`：macro BLOCK_SIZE
    代码片段：`#define BLOCK_SIZE 1024      // 磁盘的block大小`
  - `include/common.h:L32-L32`：macro BLOCK_SIZE
    代码片段：`#define BLOCK_SIZE 1024`
  - `mkfs/mkfs.c:L50-L50`：macro N_DATA_BLOCK
    代码片段：`#define N_DATA_BLOCK     8192 // 1个block的bitmap管理的极限`
  - `mkfs/mkfs.c:L51-L51`：macro N_DATA_BLOCK
    代码片段：`#define N_DATA_BLOCK     8192 // 1个block的bitmap管理的极限`
- 结构体/类型重合：与 2025 达达乐队 在“文件系统”维度发现 4 个同名定义：super_block, inode_disk, dirent, buf_node。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `mkfs/mkfs.c:L12-L12`：struct super_block
    代码片段：`typedef struct super_block {`
  - `mkfs/mkfs.c:L13-L13`：struct super_block
    代码片段：`typedef struct super_block {`
  - `mkfs/mkfs.c:L27-L27`：struct inode_disk
    代码片段：`typedef struct inode_disk {`
  - `mkfs/mkfs.c:L28-L28`：struct inode_disk
    代码片段：`typedef struct inode_disk {`
- 结构体/类型重合：与 2025 达达乐队 在“内存管理”维度发现 4 个同名定义：mmap_region_node, page_node, alloc_region, mmap_region。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `kernel/mem/mmap.c:L10-L10`：struct mmap_region_node
    代码片段：`typedef struct mmap_region_node {`
  - `kernel/mem/mmap.c:L21-L21`：struct mmap_region_node
    代码片段：`typedef struct mmap_region_node {`
  - `kernel/mem/pmem.c:L9-L9`：struct page_node
    代码片段：`typedef struct page_node {`
  - `kernel/mem/pmem.c:L29-L29`：struct page_node
    代码片段：`typedef struct page_node {`
- 函数/符号名重合：与 2025 达达乐队 在“调度与任务管理”维度发现 1 个同名定义：swtch。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/proc/swtch.S:L7-L7`：fn swtch
    代码片段：`swtch:`
  - `kernel/proc/switch.S:L14-L14`：fn swtch
    代码片段：`swtch:`
- 结构体/类型重合：与 2025 达达乐队 在“调度与任务管理”维度发现 4 个同名定义：cpu, context, trapframe, proc_state。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `include/proc/cpu.h:L7-L7`：struct cpu
    代码片段：`typedef struct cpu {`
  - `include/proc/cpu.h:L15-L15`：struct cpu
    代码片段：`typedef struct cpu {`
  - `include/proc/proc.h:L17-L17`：struct context
    代码片段：`typedef struct context {`
  - `include/proc/proc.h:L32-L32`：struct context
    代码片段：`typedef struct context {`
- 结构体/类型重合：与 2025 达达乐队 在“同步机制”维度发现 3 个同名定义：super_block, spinlock, sleeplock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `mkfs/mkfs.c:L12-L12`：struct super_block
    代码片段：`typedef struct super_block {`
  - `mkfs/mkfs.c:L13-L13`：struct super_block
    代码片段：`typedef struct super_block {`
  - `include/lib/lock.h:L6-L6`：struct spinlock
    代码片段：`typedef struct spinlock {`
  - `include/lib/lock.h:L18-L18`：struct spinlock
    代码片段：`typedef struct spinlock {`
- 文件路径重合：与 2025 达达乐队 在“设备驱动”维度出现同路径源码路径 `kernel/dev/uart.c` / `kernel/dev/uart.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/uart.c:L1-L4`：关键词命中
    代码片段：`/* * uart.c - 16550a UART 驱动（轮询 + 中断回显） * * 提供：`
- 文件路径重合：与 2025 达达乐队 在“设备驱动”维度出现同路径源码路径 `kernel/dev/virtio.c` / `kernel/dev/virtio.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
  - `kernel/dev/virtio.c:L1-L4`：关键词命中
    代码片段：`/* * virtio.c - QEMU virtio-blk（虚拟磁盘）驱动 * * QEMU 侧常见配置：-device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0`
- 结构体/类型重合：与 2025 达达乐队 在“设备驱动”维度发现 1 个同名定义：buf_node。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `kernel/fs/buf.c:L11-L11`：struct buf_node
    代码片段：`typedef struct buf_node {`
  - `kernel/fs/buf.c:L31-L31`：struct buf_node
    代码片段：`typedef struct buf_node {`
- 文件路径重合：与 2025 达达乐队 在“文件系统”维度出现同路径源码路径 `kernel/fs/fs.c` / `kernel/fs/fs.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/fs.c:L4-L8`：关键词命中
    代码片段：`* 当前版本的 fs_init() 做了两件事： *   1) 初始化 buf cache，并从磁盘读取超级块到内存副本 sb； *   2) 运行一段 inode 读写自测逻辑（便于实验阶段验证 inode/data 分配链路）。 * * 注意：自测结束后会进入 while(1) 死循环。`
- 文件路径重合：与 2025 达达乐队 在“文件系统”维度出现同路径源码路径 `kernel/fs/dir.c` / `kernel/fs/dir.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
  - `kernel/fs/dir.c:L7-L11`：关键词命中
    代码片段：`* * 锁语义： *   - 目录项的查找/增删/遍历都要求调用者持有父目录 inode 的睡眠锁（pip->slk）。 *   - path_* 系列会按需对中间目录 inode 加锁、查找目录项、再移动到下一段。 */`
- 文件路径重合：与 2025 达达乐队 在“中断与异常”维度出现同路径源码路径 `kernel/dev/plic.c` / `kernel/dev/plic.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/plic.c:L1-L4`：关键词命中
    代码片段：`/* * plic.c - PLIC（Platform-level interrupt controller） * * 负责外部中断（external interrupt）的分发：`
- 文件路径重合：与 2025 达达乐队 在“中断与异常”维度出现同路径源码路径 `kernel/dev/timer.c` / `kernel/dev/timer.c`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：high）
  证据：
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
- 结构体/类型重合：与 2025 达达乐队 在“中断与异常”维度发现 2 个同名定义：timer, trapframe。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `include/dev/timer.h:L7-L7`：struct timer
    代码片段：`typedef struct timer {`
  - `include/dev/timer.h:L16-L16`：struct timer
    代码片段：`typedef struct timer {`
  - `include/proc/proc.h:L37-L37`：struct trapframe
    代码片段：`typedef struct trapframe {`
  - `include/proc/proc.h:L52-L52`：struct trapframe
    代码片段：`typedef struct trapframe {`

## 相似点

- 与 2025 达达乐队 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
- 与 2025 达达乐队 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
- 与 2025 达达乐队 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
- 与 2025 达达乐队 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/mem/kvm.c:L12-L16`：关键词命中
    代码片段：`// 根据pagetable,找到va对应的pte // 若设置alloc=true 则在PTE无效时尝试申请一个物理页 // 成功返回PTE, 失败返回NULL`
  - `kernel/mem/uvm.c:L12-L16`：关键词命中
    代码片段：`uint64 va, pa, page; int flags; pte_t* pte; for(va = begin; va < end; va += PGSIZE)`
- 与 2025 达达乐队 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h" #include "lib/lock.h"`
  - `kernel/proc/exec.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "proc/elf.h" #include "mem/vmem.h"`
- 与 2025 达达乐队 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/sleeplock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
- 与 2025 达达乐队 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfile.c:L6-L10`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "syscall/syscall.h" #include "syscall/sysfunc.h"`
- 与 2025 达达乐队 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2025 达达乐队 的语言构成不同：待测作品为 {'json': 18, 'make': 26, 'build': 256, 'markdown': 227, 'c': 6835, 'asm': 308}，历史样本为 {'json': 20, 'make': 26, 'build': 287, 'markdown': 170, 'c': 10506, 'asm': 356}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：39
- 含证据关键结论数：39（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
