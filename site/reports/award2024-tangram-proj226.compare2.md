# Tangram proj226 kernel components frameworks 比较报告

- 对比历史仓库：2024 你起吧
- 生成时间：2026-06-28T07:36:36.789063+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2024 你起吧（来源：赛事历史作品）：画像相似度 score=5.66；语言构成相似度 0.71; OS 维度重合度 0.86; 代码规模接近度 0.81

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2024 你起吧 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/raspi4/chainloader/src/driver.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! Driver support. use crate::synchronization::{interface::Mutex, NullLock};`
  - `tools/raspi4/chainloader/src/console.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! System console. mod null_console;`
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/virtio.h:L4-L8`：关键词命中
    代码片段：`// // virtio device definitions. // for both the mmio interface, and virtio descriptors. // only tested with qemu.`
- 与 2024 你起吧 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
  - `src/fs.rs:L78-L82`：关键词命中
    代码片段：`unsafe { let fs = EXT4FS.assume_init_ref(); // println!("rs::readi: i: {} off: {}", (*ip).inode_num, off); let len = fs.read_at((*ip).inode_num, off as _, &mut v).unwrap(); eith...`
  - `kernel/fs.c:L2-L6`：关键词命中
    代码片段：`//   + Blocks: allocator for raw disk blocks. //   + Log: crash recovery for multi-step updates. //   + Files: inode allocator, reading, writing, metadata. //   + Directories: i...`
- 与 2024 你起吧 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/c/pow.c:L601-L605`：关键词命中
    代码片段：`if (y == 0.0) y = asdouble(sbits & 0x8000000000000000); /* The underflow exception needs to be signaled explicitly.  */ fp_force_eval(fp_barrier(0x1p-1022) * 0x1p-1022); }`
  - `tools/axlibc/c/time.c:L109-L113`：关键词命中
    代码片段：`} struct tm *gmtime(const time_t *timer) { static struct tm tm;`
  - `kernel/plic.c:L6-L10`：关键词命中
    代码片段：`// // the riscv Platform Level Interrupt Controller (PLIC). //`
  - `kernel/trap.c:L32-L36`：关键词命中
    代码片段：`// // handle an interrupt, exception, or system call from user space. // called from trampoline.S //`
- 与 2024 你起吧 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `apps/task/tls/src/main.rs:L9-L13`：关键词命中
    代码片段：`use core::ptr::addr_of; use std::{thread, vec::Vec}; #[thread_local]`
  - `apps/task/sleep/src/main.rs:L7-L11`：关键词命中
    代码片段：`use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
  - `src/task.rs:L9-L13`：关键词命中
    代码片段：`use core::ptr::null_mut; pub type Task = proc_; impl Drop for Task {`
  - `kernel/proc.c:L4-L8`：关键词命中
    代码片段：`#include "riscv.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h" #include "file.h"`
- 与 2024 你起吧 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/src/rand.rs:L3-L7`：关键词命中
    代码片段：`use core::{ ffi::{c_int, c_long, c_uint}, sync::atomic::{AtomicU64, Ordering::SeqCst}, };`
  - `apps/task/sleep/src/main.rs:L6-L10`：关键词命中
    代码片段：`extern crate axstd as std; use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
  - `kernel/fs.c:L15-L19`：关键词命中
    代码片段：`#include "param.h" #include "stat.h" #include "spinlock.h" #include "proc.h" #include "sleeplock.h"`
  - `src/task.rs:L1-L4`：关键词命中
    代码片段：`use crate::bindings::{allocpid, proc_, procstate_USED, NPROC}; use crate::ffi_import::SpinLock; use crate::pagetable::PageTable; use crate::pool::{Pool, PoolRef};`
- 与 2024 你起吧 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/include/signal.h:L102-L106`：macro si_syscall
    代码片段：`#define si_int       si_value.sival_int #define si_call_addr __si_fields.__sigsys.si_call_addr #define si_syscall   __si_fields.__sigsys.si_syscall #define si_arch      __si_fie...`
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`exit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
  - `kernel/syscall.c:L5-L9`：关键词命中
    代码片段：`#include "spinlock.h" #include "proc.h" #include "syscall.h" #include "defs.h" #include "errno.h"`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 宏名重合：与 2024 你起吧 在“设备驱动”维度发现 4 个同名定义：ENXIO, ENOTBLK, EBUSY, EXDEV。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/errno.h:L9-L9`：macro ENXIO
    代码片段：`#define ENXIO           6      /* No such device or address */`
  - `kernel/errno.h:L9-L9`：macro ENXIO
    代码片段：`#define	ENXIO		 6	/* No such device or address */`
  - `tools/axlibc/include/errno.h:L18-L18`：macro ENOTBLK
    代码片段：`#define ENOTBLK         15     /* Block device required */`
  - `kernel/errno.h:L18-L18`：macro ENOTBLK
    代码片段：`#define	ENOTBLK		15	/* Block device required */`
- 宏名重合：与 2024 你起吧 在“文件系统”维度发现 4 个同名定义：ENOENT, EBADF, EEXIST, ENFILE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/errno.h:L5-L5`：macro ENOENT
    代码片段：`#define ENOENT          2      /* No such file or directory */`
  - `kernel/errno.h:L5-L5`：macro ENOENT
    代码片段：`#define	ENOENT		 2	/* No such file or directory */`
  - `tools/axlibc/include/errno.h:L12-L12`：macro EBADF
    代码片段：`#define EBADF           9      /* Bad file number */`
  - `kernel/errno.h:L12-L12`：macro EBADF
    代码片段：`#define	EBADF		 9	/* Bad file number */`
- 宏名重合：与 2024 你起吧 在“中断与异常”维度发现 3 个同名定义：EINTR, ETIME, ERESTART。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/errno.h:L7-L7`：macro EINTR
    代码片段：`#define EINTR           4      /* Interrupted system call */`
  - `kernel/errno.h:L7-L7`：macro EINTR
    代码片段：`#define	EINTR		 4	/* Interrupted system call */`
  - `tools/axlibc/include/errno.h:L65-L65`：macro ETIME
    代码片段：`#define ETIME           62  /* Timer expired */`
  - `kernel/errno.h:L78-L78`：macro ETIME
    代码片段：`#define	ETIME		62	/* Timer expired */`
- 宏名重合：与 2024 你起吧 在“同步机制”维度发现 4 个同名定义：ENOTBLK, EDEADLK, ENOLCK, EWOULDBLOCK。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/errno.h:L18-L18`：macro ENOTBLK
    代码片段：`#define ENOTBLK         15     /* Block device required */`
  - `kernel/errno.h:L18-L18`：macro ENOTBLK
    代码片段：`#define	ENOTBLK		15	/* Block device required */`
  - `tools/axlibc/include/errno.h:L38-L38`：macro EDEADLK
    代码片段：`#define EDEADLK         35     /* Resource deadlock would occur */`
  - `kernel/errno.h:L40-L40`：macro EDEADLK
    代码片段：`#define	EDEADLK		35	/* Resource deadlock would occur */`
- 宏名重合：与 2024 你起吧 在“系统调用”维度发现 4 个同名定义：EINTR, EROFS, ENOSYS, ERESTART。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/errno.h:L7-L7`：macro EINTR
    代码片段：`#define EINTR           4      /* Interrupted system call */`
  - `kernel/errno.h:L7-L7`：macro EINTR
    代码片段：`#define	EINTR		 4	/* Interrupted system call */`
  - `tools/axlibc/include/errno.h:L33-L33`：macro EROFS
    代码片段：`#define EROFS           30     /* Read-only file system */`
  - `kernel/errno.h:L33-L33`：macro EROFS
    代码片段：`#define	EROFS		30	/* Read-only file system */`
- 宏名重合：与 2024 你起吧 在“调度与任务管理”维度发现 2 个同名定义：ESRCH, ECHILD。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `tools/axlibc/include/errno.h:L6-L6`：macro ESRCH
    代码片段：`#define ESRCH           3      /* No such process */`
  - `kernel/errno.h:L6-L6`：macro ESRCH
    代码片段：`#define	ESRCH		 3	/* No such process */`
  - `tools/axlibc/include/errno.h:L13-L13`：macro ECHILD
    代码片段：`#define ECHILD          10     /* No child processes */`
  - `kernel/errno.h:L13-L13`：macro ECHILD
    代码片段：`#define	ECHILD		10	/* No child processes */`

## 相似点

- 与 2024 你起吧 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/raspi4/chainloader/src/driver.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! Driver support. use crate::synchronization::{interface::Mutex, NullLock};`
  - `tools/raspi4/chainloader/src/console.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! System console. mod null_console;`
- 与 2024 你起吧 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
  - `src/fs.rs:L78-L82`：关键词命中
    代码片段：`unsafe { let fs = EXT4FS.assume_init_ref(); // println!("rs::readi: i: {} off: {}", (*ip).inode_num, off); let len = fs.read_at((*ip).inode_num, off as _, &mut v).unwrap(); eith...`
- 与 2024 你起吧 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/c/pow.c:L601-L605`：关键词命中
    代码片段：`if (y == 0.0) y = asdouble(sbits & 0x8000000000000000); /* The underflow exception needs to be signaled explicitly.  */ fp_force_eval(fp_barrier(0x1p-1022) * 0x1p-1022); }`
  - `tools/axlibc/c/time.c:L109-L113`：关键词命中
    代码片段：`} struct tm *gmtime(const time_t *timer) { static struct tm tm;`
- 与 2024 你起吧 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `apps/task/tls/src/main.rs:L9-L13`：关键词命中
    代码片段：`use core::ptr::addr_of; use std::{thread, vec::Vec}; #[thread_local]`
  - `apps/task/sleep/src/main.rs:L7-L11`：关键词命中
    代码片段：`use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
- 与 2024 你起吧 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/src/rand.rs:L3-L7`：关键词命中
    代码片段：`use core::{ ffi::{c_int, c_long, c_uint}, sync::atomic::{AtomicU64, Ordering::SeqCst}, };`
  - `apps/task/sleep/src/main.rs:L6-L10`：关键词命中
    代码片段：`extern crate axstd as std; use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
- 与 2024 你起吧 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/include/signal.h:L102-L106`：macro si_syscall
    代码片段：`#define si_int       si_value.sival_int #define si_call_addr __si_fields.__sigsys.si_call_addr #define si_syscall   __si_fields.__sigsys.si_syscall #define si_arch      __si_fie...`
  - `kernel/trap.c:L58-L62`：关键词命中
    代码片段：`exit(-1); // sepc points to the ecall instruction, // but we want to return to the next instruction. p->trapframe->epc += 4;`
- 与 2024 你起吧 在 driver, filesystem, interrupt, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2024 你起吧 的语言构成不同：新项目为 {'json': 33, 'build': 974, 'markdown': 5808, 'toml': 376, 'c': 10873, 'make': 596, 'rust': 5140, 'asm': 125, 'text': 53}，历史项目为 {'json': 32, 'build': 284, 'markdown': 486, 'c': 8469, 'asm': 315, 'rust': 9355, 'toml': 4}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：18
- 含证据关键结论数：18（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
