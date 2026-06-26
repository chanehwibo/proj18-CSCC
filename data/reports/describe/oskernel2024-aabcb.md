# OSKernel2024-aabcb 项目描述报告

## 基本信息

- 仓库 ID：`oskernel2024-aabcb`
- 风格：independent
- 架构：riscv64
- 样本来源等级：比赛作品样本（获奖等级未核验）
- 文件数：82
- 代码/文本行数：7670
- 主要语言：c 6835 LOC, asm 308 LOC, build 256 LOC, markdown 227 LOC, make 26 LOC

## 总览

OSKernel2024-aabcb 是一个 independent 风格的小型操作系统相关仓库，主要语言统计为 c: 6835 LOC, asm: 308 LOC, build: 256 LOC, markdown: 227 LOC。仓库包含 82 个已扫描文件、约 7670 行可分析文本，当前抽取到 338 个符号定义。

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
| 同步机制 | 已确认 | high | 5 |
| 中断与异常 | 已确认 | high | 6 |
| 设备驱动 | 已确认 | high | 6 |

## 构建系统

- 仓库包含构建入口：Makefile, kernel/Makefile, mkfs/Makefile, user/Makefile, kernel/boot/Makefile。（置信度：high）
  证据：
  - `Makefile:L1-L3`：构建入口
    代码片段：`include common.mk KERN = kernel`
  - `kernel/Makefile:L1-L3`：构建入口
    代码片段：`include ../common.mk MOUDLES = $(shell ls -d */)`
  - `mkfs/Makefile:L1-L3`：构建入口
    代码片段：`.PHONY: clean build: mkfs.c`
  - `user/Makefile:L1-L3`：构建入口
    代码片段：`include ../common.mk init: initcode.c`
  - `kernel/boot/Makefile:L1-L3`：构建入口
    代码片段：`# 头文件 INLCUDES := ../../include`

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）
  - 相关符号包括：fn proc_alloc, fn proc_free, fn proc_init, fn proc_make_first, fn proc_fork。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/proc/cpu.c` | L1-L3 | 关键词命中 |
| `kernel/proc/exec.c` | L1-L3 | 关键词命中 |
| `kernel/proc/proc.c` | L4-L8 | 关键词命中 |
| `kernel/proc/proc.c` | L66-L70 | fn proc_alloc |
| `kernel/proc/proc.c` | L113-L117 | fn proc_free |
| `kernel/proc/proc.c` | L146-L150 | fn proc_init |

### 关键代码片段

  - `kernel/proc/cpu.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "riscv.h" #include "lib/lock.h"`
  - `kernel/proc/exec.c:L1-L3`：关键词命中
    代码片段：`#include "proc/cpu.h" #include "proc/elf.h" #include "mem/vmem.h"`
  - `kernel/proc/proc.c:L4-L8`：关键词命中
    代码片段：`#include "mem/vmem.h" #include "mem/mmap.h" #include "proc/cpu.h" #include "proc/initcode.h" #include "memlayout.h"`
  - `kernel/proc/proc.c:L66-L70`：fn proc_alloc
    代码片段：`// 设置pid + 设置上下文中的ra和sp // 申请tf和pgtbl使用的物理页 proc_t* proc_alloc() { proc_t *p;`

### 相关符号

`fn proc_alloc` at `kernel/proc/proc.c:L66`、`fn proc_free` at `kernel/proc/proc.c:L113`、`fn proc_init` at `kernel/proc/proc.c:L146`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）
  - 相关符号包括：fn vm_getpte, fn uvm_copy_pgtbl, fn uvm_heap_ungrow, macro PGSIZE, macro PGSIZE。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/mem/kvm.c` | L12-L16 | 关键词命中 |
| `kernel/mem/uvm.c` | L12-L16 | 关键词命中 |
| `kernel/mem/pmem.c` | L24-L28 | 关键词命中 |
| `kernel/mem/kvm.c` | L17-L21 | fn vm_getpte |
| `kernel/mem/uvm.c` | L105-L109 | fn uvm_copy_pgtbl |
| `kernel/mem/uvm.c` | L318-L322 | fn uvm_heap_ungrow |

### 关键代码片段

  - `kernel/mem/kvm.c:L12-L16`：关键词命中
    代码片段：`// 根据pagetable,找到va对应的pte // 若设置alloc=true 则在PTE无效时尝试申请一个物理页 // 成功返回PTE, 失败返回NULL`
  - `kernel/mem/uvm.c:L12-L16`：关键词命中
    代码片段：`uint64 va, pa, page; int flags; pte_t* pte; for(va = begin; va < end; va += PGSIZE)`
  - `kernel/mem/pmem.c:L24-L28`：关键词命中
    代码片段：`#define KERN_PAGES 1024 // 内核可分配空间占1024个pages #define PGSIZE 4096  // 页面大小 #define PGROUNDUP(x) (((x) + PGSIZE - 1) & ~(PGSIZE - 1))`
  - `kernel/mem/kvm.c:L17-L21`：fn vm_getpte
    代码片段：`// 提示：使用 VA_TO_VPN PTE_TO_PA PA_TO_PTE // 定义用于获取或创建一个页表项 (PTE) 的函数 pte_t* vm_getpte(pgtbl_t pgtbl, uint64 va, bool alloc) { if (va >= VA_MAX)  // 检查虚拟地址是否超出最大允许范围`

### 相关符号

`fn vm_getpte` at `kernel/mem/kvm.c:L17`、`fn uvm_copy_pgtbl` at `kernel/mem/uvm.c:L105`、`fn uvm_heap_ungrow` at `kernel/mem/uvm.c:L318`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含系统调用入口、编号或分发逻辑。（置信度：high）
  - 相关符号包括：fn kernel_vector, fn timer_vector, fn sys_brk, fn sys_mmap, fn sys_munmap。（置信度：medium）
  - 静态识别到 26 个系统调用相关符号。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/syscall/syscall.c` | L3-L7 | 关键词命中 |
| `kernel/syscall/sysfile.c` | L6-L10 | 关键词命中 |
| `kernel/syscall/sysproc.c` | L6-L10 | 关键词命中 |
| `kernel/trap/trap.S` | L6-L10 | fn kernel_vector |
| `kernel/trap/trap.S` | L91-L95 | fn timer_vector |
| `kernel/syscall/sysproc.c` | L19-L23 | fn sys_brk |

### 关键代码片段

  - `kernel/syscall/syscall.c:L3-L7`：关键词命中
    代码片段：`#include "mem/mmap.h" #include "mem/vmem.h" #include "syscall/syscall.h" #include "syscall/sysnum.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysfile.c:L6-L10`：关键词命中
    代码片段：`#include "lib/str.h" #include "lib/print.h" #include "syscall/syscall.h" #include "syscall/sysfunc.h"`
  - `kernel/syscall/sysproc.c:L6-L10`：关键词命中
    代码片段：`#include "lib/print.h" #include "dev/timer.h" #include "syscall/sysfunc.h" #include "syscall/syscall.h" #include "memlayout.h"`
  - `kernel/trap/trap.S:L6-L10`：fn kernel_vector
    代码片段：`.globl kernel_vector .align 4 kernel_vector: # 准备空间给32个通用寄存器`

### 相关符号

`fn kernel_vector` at `kernel/trap/trap.S:L6`、`fn timer_vector` at `kernel/trap/trap.S:L91`、`fn sys_brk` at `kernel/syscall/sysproc.c:L19`、`fn sys_brk` at `kernel/syscall/sysproc.c:L19`、`fn sys_mmap` at `kernel/syscall/sysproc.c:L46`、`fn sys_munmap` at `kernel/syscall/sysproc.c:L75`、`fn sys_fork` at `kernel/syscall/sysproc.c:L88`、`fn sys_wait` at `kernel/syscall/sysproc.c:L93`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 文件系统

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含文件系统、VFS、inode、目录项或文件读写相关实现。（置信度：high）
  - 相关符号包括：struct buf_node, fn inode_init, struct buf, struct dirent, struct file。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/fs/fs.c` | L2-L6 | 关键词命中 |
| `kernel/fs/dir.c` | L1-L5 | 关键词命中 |
| `kernel/fs/file.c` | L3-L7 | 关键词命中 |
| `kernel/fs/buf.c` | L9-L13 | struct buf_node |
| `kernel/fs/inode.c` | L16-L20 | fn inode_init |
| `include/fs/buf.h` | L4-L8 | struct buf |

### 关键代码片段

  - `kernel/fs/fs.c:L2-L6`：关键词命中
    代码片段：`#include "fs/buf.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/dir.h" #include "lib/str.h"`
  - `kernel/fs/dir.c:L1-L5`：关键词命中
    代码片段：`#include "fs/fs.h" #include "fs/buf.h" #include "fs/inode.h" #include "fs/dir.h" #include "fs/bitmap.h"`
  - `kernel/fs/file.c:L3-L7`：关键词命中
    代码片段：`#include "fs/dir.h" #include "fs/bitmap.h" #include "fs/inode.h" #include "fs/file.h" #include "mem/vmem.h"`
  - `kernel/fs/buf.c:L9-L13`：struct buf_node
    代码片段：`// 将buf包装成双向循环链表的node typedef struct buf_node { buf_t buf; struct buf_node* next;`

### 相关符号

`struct buf_node` at `kernel/fs/buf.c:L9`、`fn inode_init` at `kernel/fs/inode.c:L16`、`struct buf` at `include/fs/buf.h:L4`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）
  - 相关符号包括：struct spinlock, struct sleeplock。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/lib/spinlock.c` | L1-L3 | 关键词命中 |
| `kernel/lib/sleeplock.c` | L1-L3 | 关键词命中 |
| `include/lib/lock.h` | L4-L8 | 关键词命中 |
| `include/lib/lock.h` | L4-L8 | struct spinlock |
| `include/lib/lock.h` | L10-L14 | struct sleeplock |

### 关键代码片段

  - `kernel/lib/spinlock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `kernel/lib/sleeplock.c:L1-L3`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "proc/cpu.h"`
  - `include/lib/lock.h:L4-L8`：关键词命中
    代码片段：`#include "common.h" typedef struct spinlock { int locked; char* name;`
  - `include/lib/lock.h:L4-L8`：struct spinlock
    代码片段：`#include "common.h" typedef struct spinlock { int locked; char* name;`

### 相关符号

`struct spinlock` at `include/lib/lock.h:L4`、`struct sleeplock` at `include/lib/lock.h:L10`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 中断与异常

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `interrupt` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含 trap、中断、异常或定时器处理逻辑。（置信度：high）
  - 相关符号包括：fn timer_init, fn kernel_vector, fn timer_vector, fn trampoline, fn user_vector。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/dev/plic.c` | L1-L3 | 关键词命中 |
| `kernel/dev/timer.c` | L1-L5 | 关键词命中 |
| `kernel/trap/trap.S` | L44-L48 | 关键词命中 |
| `kernel/dev/timer.c` | L18-L22 | fn timer_init |
| `kernel/trap/trap.S` | L6-L10 | fn kernel_vector |
| `kernel/trap/trap.S` | L91-L95 | fn timer_vector |

### 关键代码片段

  - `kernel/dev/plic.c:L1-L3`：关键词命中
    代码片段：`// Platform-level interrupt controller #include "memlayout.h"`
  - `kernel/dev/timer.c:L1-L5`：关键词命中
    代码片段：`#include "lib/lock.h" #include "lib/print.h" #include "dev/timer.h" #include "memlayout.h" #include "riscv.h"`
  - `kernel/trap/trap.S:L44-L48`：关键词命中
    代码片段：`sd t6, 240(sp) # trap的处理过程 call trap_kernel_handler`
  - `kernel/dev/timer.c:L18-L22`：fn timer_init
    代码片段：`// 时钟初始化 // called in start.c void timer_init() { int id = r_mhartid(); // 获取当前 CPU 的 ID`

### 相关符号

`fn timer_init` at `kernel/dev/timer.c:L18`、`fn kernel_vector` at `kernel/trap/trap.S:L6`、`fn timer_vector` at `kernel/trap/trap.S:L91`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。（置信度：high）
  - 相关符号包括：fn uart_puts, macro VIRTIO_MMIO_MAGIC_VALUE, macro VIRTIO_MMIO_VERSION, macro VIRTIO_MMIO_DEVICE_ID, macro VIRTIO_MMIO_VENDOR_ID。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `kernel/dev/uart.c` | L1-L3 | 关键词命中 |
| `kernel/dev/virtio.c` | L1-L5 | 关键词命中 |
| `kernel/fs/buf.c` | L133-L137 | 关键词命中 |
| `kernel/dev/uart.c` | L71-L75 | fn uart_puts |
| `include/dev/virtio.h` | L14-L18 | macro VIRTIO_MMIO_MAGIC_VALUE |
| `include/dev/virtio.h` | L15-L19 | macro VIRTIO_MMIO_VERSION |

### 关键代码片段

  - `kernel/dev/uart.c:L1-L3`：关键词命中
    代码片段：`// low-level driver routines for 16550a UART. #include "memlayout.h"`
  - `kernel/dev/virtio.c:L1-L5`：关键词命中
    代码片段：`/* QEMU提供的虚拟磁盘的驱动 QEMUOPTS = -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 这个文件最终提供三个重要函数: virtio_init() // 初始化函数`
  - `kernel/fs/buf.c:L133-L137`：关键词命中
    代码片段：`// 从磁盘读取对应块的数据 virtio_disk_rw(&b->buf, 0); return &b->buf;`
  - `kernel/dev/uart.c:L71-L75`：fn uart_puts
    代码片段：`} void uart_puts(const char *s) { while (*s != '\0') { uart_putc_sync(*s++);`

### 相关符号

`fn uart_puts` at `kernel/dev/uart.c:L71`、`macro VIRTIO_MMIO_MAGIC_VALUE` at `include/dev/virtio.h:L14`、`macro VIRTIO_MMIO_VERSION` at `include/dev/virtio.h:L15`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 附录：核验摘要

- 关键结论数：16
- 含证据关键结论数：16（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
