# OSKernel2024‑aabcb 项目描述报告

## 1. 基本信息

- **仓库名称**：OSKernel2024‑aabcb
- **开发语言**：C（6835 LOC）、汇编（308 LOC）、构建脚本（256 LOC）、Markdown（227 LOC）
- **目标架构**：riscv64
- **代码规模**：约 7670 行可分析文本，82 个文件，识别 338 个符号
- **来源层级**：比赛作品样本（competition_sample，非获奖案例）
- **构建系统**：基于 Makefile，入口文件包括 `Makefile`、`kernel/Makefile`、`mkfs/Makefile`、`user/Makefile`、`kernel/boot/Makefile`（见 `Makefile:L1-L3`、`kernel/Makefile:L1-L3`、`mkfs/Makefile:L1-L3`、`user/Makefile:L1-L3`、`kernel/boot/Makefile:L1-L3`）

## 2. 操作系统各维度描述

### 2.1 调度与任务管理

- **实现概要**：项目具备任务/线程管理与调度相关实现（`kernel/proc/cpu.c:L1-L3`、`kernel/proc/exec.c:L1-L3`、`kernel/proc/proc.c:L4-L8`）。
- **关键符号**：
  - `proc_alloc`：分配进程控制块，设置 trapframe 及页表物理内存（`kernel/proc/proc.c:L66-L70`）。
  - `proc_free`：释放进程所占资源，调用者须持有进程锁（`kernel/proc/proc.c:L113-L117`）。
  - `proc_init`：进程模块初始化函数（`kernel/proc/proc.c:L146-L150`）。
  - 另有 `proc_fork`、`proc_make_first` 等符号（未展开证据）。
- **调度策略**：未确认。

### 2.2 内存管理

- **实现概要**：包含页表、物理页、虚拟内存与堆分配等内存管理实现（`kernel/mem/kvm.c:L12-L16`、`kernel/mem/uvm.c:L12-L16`、`kernel/mem/pmem.c:L24-L28`）。
- **关键符号与功能**：
  - `vm_getpte`：根据页表与虚拟地址获取或创建页表项（`kernel/mem/kvm.c:L17-L21`）。
  - `uvm_copy_pgtbl`：拷贝用户态页表（不含 trapframe 与 trampoline），区间为 `USER_BASE` 至 `heap_top`（`kernel/mem/uvm.c:L105-L109`）。
  - `uvm_heap_ungrow`：缩减用户堆空间（`kernel/mem/uvm.c:L318-L322`）。
  - 宏 `PGSIZE` 定义为 4096（`kernel/mem/pmem.c:L24-L28`），`KERN_PAGES` 设置为 1024。
- **页面替换/分配算法**：未确认。

### 2.3 系统调用

- **实现概要**：存在系统调用入口与分发逻辑，相关文件包括 `kernel/syscall/syscall.c:L3-L7`、`kernel/syscall/sysfile.c:L6-L10`、`kernel/syscall/sysproc.c:L6-L10`。静态识别到 26 个系统调用相关符号。
- **关键符号**：
  - `sys_brk`：调整进程堆顶（`kernel/syscall/sysproc.c:L19-L23`）。
  - `sys_mmap`：内存映射（`kernel/syscall/sysproc.c:L46-L50`）。
  - `sys_munmap`：取消内存映射（`kernel/syscall/sysproc.c:L75-L79`）。
  - `sys_fork`：调用 `proc_fork` 创建子进程（`kernel/syscall/sysproc.c:L88-L92`）。
  - `sys_wait`：等待子进程退出（`kernel/syscall/sysproc.c:L93-L97`）。
- **异常入口**：`kernel_vector`（`kernel/trap/trap.S:L6-L10`）承担内核异常/系统调用入口角色。
- **调用规约与编号机制**：未确认。

### 2.4 文件系统

- **实现概要**：提供文件系统基本框架，涉及 inode、目录项、缓冲区管理等（`kernel/fs/fs.c:L2-L6`、`kernel/fs/dir.c:L1-L5`、`kernel/fs/file.c:L3-L7`）。
- **关键符号**：
  - `buf_node`：将缓冲区块包装为双向循环链表节点（`kernel/fs/buf.c:L9-L13`）。
  - `inode_init`：初始化 inode 缓存及全局自旋锁（`kernel/fs/inode.c:L16-L20`）。
  - `struct buf`：磁盘缓冲区，内部包含睡眠锁与数据存储（`include/fs/buf.h:L4-L8`）。
  - 另有 `struct dirent`、`struct file` 等符号（未展开证据）。
- **文件系统类型及布局**：未确认。

### 2.5 同步机制

- **实现概要**：基于自旋锁与睡眠锁提供同步原语（`kernel/lib/spinlock.c:L1-L3`、`kernel/lib/sleeplock.c:L1-L3`、`include/lib/lock.h:L4-L8`）。
- **关键符号**：
  - `struct spinlock`（`include/lib/lock.h:L4-L8`）。
  - `struct sleeplock`（`include/lib/lock.h:L10-L14`）。
- **具体锁算法**：未确认。

### 2.6 中断与异常

- **实现概要**：具备 trap 处理、平台级中断控制器及定时器逻辑（`kernel/dev/plic.c:L1-L3`、`kernel/dev/timer.c:L1-L5`、`kernel/trap/trap.S:L44-L48`）。
- **关键符号**：
  - `timer_init`：初始化时钟（`kernel/dev/timer.c:L18-L22`）。
  - `kernel_vector`：内核态 trap 入口（`kernel/trap/trap.S:L6-L10`）。
  - `timer_vector`：定时器专用 trap 入口（`kernel/trap/trap.S:L91-L95`）。
  - 另有 `trampoline`、`user_vector` 等符号（未展开证据）。
- **中断优先级、异常分类等详细处理逻辑**：未确认。

### 2.7 设备驱动

- **实现概要**：包含 UART 串口、virtio 磁盘及块设备驱动（`kernel/dev/uart.c:L1-L3`、`kernel/dev/virtio.c:L1-L5`、`kernel/fs/buf.c:L133-L137`）。
- **关键符号**：
  - `uart_puts`：串口输出字符串（`kernel/dev/uart.c:L71-L75`）。
  - Virtio MMIO 控制寄存器宏（`include/dev/virtio.h:L14-L18` 至 `include/dev/virtio.h:L15-L19`）：`VIRTIO_MMIO_MAGIC_VALUE`、`VIRTIO_MMIO_VERSION`、`VIRTIO_MMIO_DEVICE_ID`、`VIRTIO_MMIO_VENDOR_ID`。
- **驱动初始化流程、中断处理细节**：未确认。

## 3. 核验摘要

- 自动核验中提取的 16 项关键发现均有证据支持，覆盖率 100%，无无效证据。
- 未确认关键结论数（`self_check.unconfirmed`）：0。
- 仍需人工确认的信息（基于报告内标注）：调度策略、页面替换/分配算法、系统调用编号机制与调用规约、文件系统类型与布局、具体锁实现算法、中断处理详细逻辑、驱动初始化与中断处理细节等，均超出当前 evidence 范围，需结合完整源码或设计文档进一步分析。