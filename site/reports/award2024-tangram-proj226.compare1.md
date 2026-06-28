# Tangram proj226 kernel components frameworks 比较报告

- 对比历史仓库：ArceOS
- 生成时间：2026-06-28T12:59:34.546879+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- ArceOS（来源：教学基线）：画像相似度 score=6.73；架构重合度 0.67; 语言构成相似度 0.62; OS 维度重合度 0.86; 代码规模接近度 0.72

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 ArceOS 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/raspi4/chainloader/src/driver.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! Driver support. use crate::synchronization::{interface::Mutex, NullLock};`
  - `tools/raspi4/chainloader/src/console.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! System console. mod null_console;`
  - `modules/axdriver/src/virtio.rs:L19-L23`：关键词命中
    代码片段：`} /// A trait for VirtIO device meta information. pub trait VirtIoDevMeta { const DEVICE_TYPE: DeviceType;`
  - `modules/axdriver/src/drivers.rs:L6-L10`：关键词命中
    代码片段：`use axdriver_base::DeviceType; #[cfg(feature = "virtio")] use crate::virtio::{self, VirtIoDevMeta};`
- 与 ArceOS 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
  - `modules/axfs/src/fs/fatfs.rs:L32-L36`：关键词命中
    代码片段：`fatfs::format_volume(&mut disk, opts).expect("failed to format volume"); let inner = fatfs::FileSystem::new(disk, fatfs::FsOptions::new()) .expect("failed to initialize FAT file...`
  - `modules/axfs/src/lib.rs:L5-L9`：关键词命中
    代码片段：`//! # Cargo Features //! //! - 'fatfs': Use [FAT] as the main filesystem and mount it on '/'. This feature //!   is **enabled** by default. //! - 'devfs': Mount ['axfs_devfs::De...`
- 与 ArceOS 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/c/pow.c:L601-L605`：关键词命中
    代码片段：`if (y == 0.0) y = asdouble(sbits & 0x8000000000000000); /* The underflow exception needs to be signaled explicitly.  */ fp_force_eval(fp_barrier(0x1p-1022) * 0x1p-1022); }`
  - `tools/axlibc/c/time.c:L109-L113`：关键词命中
    代码片段：`} struct tm *gmtime(const time_t *timer) { static struct tm tm;`
  - `modules/axhal/src/irq.rs:L1-L3`：关键词命中
    代码片段：`//! Interrupt management. use axcpu::trap::{IRQ, register_trap_handler};`
  - `modules/axhal/src/lib.rs:L20-L24`：关键词命中
    代码片段：`//! - 'fp-simd': Enable floating-point and SIMD support. //! - 'paging': Enable page table manipulation. //! - 'irq': Enable interrupt handling support. //! - 'tls': Enable kern...`
- 与 ArceOS 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `apps/task/tls/src/main.rs:L9-L13`：关键词命中
    代码片段：`use core::ptr::addr_of; use std::{thread, vec::Vec}; #[thread_local]`
  - `apps/task/sleep/src/main.rs:L7-L11`：关键词命中
    代码片段：`use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
  - `modules/axfs/src/root.rs:L174-L178`：关键词命中
    代码片段：`#[cfg(feature = "procfs")] root_dir // should not fail .mount("/proc", mounts::procfs().unwrap()) .expect("fail to mount procfs at /proc");`
  - `modules/axhal/src/lib.rs:L21-L25`：关键词命中
    代码片段：`//! - 'paging': Enable page table manipulation. //! - 'irq': Enable interrupt handling support. //! - 'tls': Enable kernel space thread-local storage support. //! - 'rtc': Enabl...`
- 与 ArceOS 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/src/rand.rs:L3-L7`：关键词命中
    代码片段：`use core::{ ffi::{c_int, c_long, c_uint}, sync::atomic::{AtomicU64, Ordering::SeqCst}, };`
  - `apps/task/sleep/src/main.rs:L6-L10`：关键词命中
    代码片段：`extern crate axstd as std; use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
  - `modules/axfs/src/root.rs:L7-L11`：关键词命中
    代码片段：`use axfs_vfs::{VfsNodeAttr, VfsNodeOps, VfsNodeRef, VfsNodeType, VfsOps, VfsResult}; use axns::{ResArc, def_resource}; use axsync::Mutex; use lazyinit::LazyInit;`
  - `modules/axhal/src/lib.rs:L113-L117`：关键词命中
    代码片段：`pub use axplat::init::{init_early_secondary, init_later_secondary}; #[cfg(feature = "smp")] use core::sync::atomic::{AtomicUsize, Ordering}; /// Initializes CPU-local data struc...`
- 与 ArceOS 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/include/signal.h:L102-L106`：macro si_syscall
    代码片段：`#define si_int       si_value.sival_int #define si_call_addr __si_fields.__sigsys.si_call_addr #define si_syscall   __si_fields.__sigsys.si_syscall #define si_arch      __si_fie...`
  - `api/arceos_posix_api/src/imp/fs.rs:L107-L111`：fn sys_open
    代码片段：`/// Return its index in the file table ('fd'). Return 'EMFILE' if it already /// has the maximum number of files open. pub fn sys_open(filename: *const c_char, flags: c_int, mod...`
  - `api/arceos_posix_api/src/imp/fs.rs:L120-L124`：fn sys_lseek
    代码片段：`/// /// Return its position after seek. pub fn sys_lseek(fd: c_int, offset: ctypes::off_t, whence: c_int) -> ctypes::off_t { debug!("sys_lseek <= {} {} {}", fd, offset, whence);...`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 与 ArceOS 在“文件系统”维度发现片段级代码相似度 1.00 （token=1.00, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：dev_t, ino_t, mode_t, nlink_t, st_dev, st_ino, st_mode, st_nlink。（置信度：high）
  证据：
  - `tools/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
  - `ulib/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
- 与 ArceOS 在“同步机制”维度发现片段级代码相似度 0.80 （token=0.69, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：atomic, atomicu64, core, ordering, sync, use。（置信度：high）
  证据：
  - `tools/axlibc/src/rand.rs:L3-L7`：关键词命中
    代码片段：`use core::{ ffi::{c_int, c_long, c_uint}, sync::atomic::{AtomicU64, Ordering::SeqCst}, };`
  - `modules/axsync/src/mutex.rs:L1-L3`：关键词命中
    代码片段：`//! A naïve sleeping mutex. use core::sync::atomic::{AtomicU64, Ordering};`
- 与 ArceOS 在“同步机制”维度发现片段级代码相似度 0.68 （token=0.50, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：atomic, ordering, sync, use。（置信度：medium）
  证据：
  - `apps/task/yield/src/main.rs:L6-L10`：关键词命中
    代码片段：`extern crate axstd as std; use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread;`
  - `modules/axsync/src/mutex.rs:L1-L3`：关键词命中
    代码片段：`//! A naïve sleeping mutex. use core::sync::atomic::{AtomicU64, Ordering};`
- 宏名重合：与 ArceOS 在“设备驱动”维度发现 4 个同名定义：DT_BLK, ENXIO, ENOTBLK, EBUSY。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/dirent.h:L37-L37`：macro DT_BLK
    代码片段：`#define DT_BLK     6`
  - `ulib/axlibc/include/dirent.h:L37-L37`：macro DT_BLK
    代码片段：`#define DT_BLK     6`
  - `tools/axlibc/include/errno.h:L9-L9`：macro ENXIO
    代码片段：`#define ENXIO           6      /* No such device or address */`
  - `ulib/axlibc/include/errno.h:L9-L9`：macro ENXIO
    代码片段：`#define ENXIO           6      /* No such device or address */`
- 宏名重合：与 ArceOS 在“文件系统”维度发现 4 个同名定义：assert, ENOENT, EBADF, EEXIST。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/assert.h:L10-L10`：macro assert
    代码片段：`#define assert(x) ((void)((x) || (__assert_fail(#x, __FILE__, __LINE__, __func__), 0)))`
  - `ulib/axlibc/include/assert.h:L13-L13`：macro assert
    代码片段：`#define assert(x) ((void)((x) || (__assert_fail(#x, __FILE__, __LINE__, __func__), 0)))`
  - `tools/axlibc/include/errno.h:L5-L5`：macro ENOENT
    代码片段：`#define ENOENT          2      /* No such file or directory */`
  - `ulib/axlibc/include/errno.h:L5-L5`：macro ENOENT
    代码片段：`#define ENOENT          2      /* No such file or directory */`
- 宏名重合：与 ArceOS 在“调度与任务管理”维度发现 4 个同名定义：DEFAULT_STACK_SIZE, DEFAULT_GUARD_SIZE, ESRCH, ECHILD。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/c/pthread.c:L81-L81`：macro DEFAULT_STACK_SIZE
    代码片段：`#define DEFAULT_STACK_SIZE 131072`
  - `ulib/axlibc/c/pthread.c:L81-L81`：macro DEFAULT_STACK_SIZE
    代码片段：`#define DEFAULT_STACK_SIZE 131072`
  - `tools/axlibc/c/pthread.c:L82-L82`：macro DEFAULT_GUARD_SIZE
    代码片段：`#define DEFAULT_GUARD_SIZE 8192`
  - `ulib/axlibc/c/pthread.c:L82-L82`：macro DEFAULT_GUARD_SIZE
    代码片段：`#define DEFAULT_GUARD_SIZE 8192`
- 宏名重合：与 ArceOS 在“同步机制”维度发现 4 个同名定义：ENOTBLK, EDEADLK, ENOLCK, EWOULDBLOCK。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/errno.h:L18-L18`：macro ENOTBLK
    代码片段：`#define ENOTBLK         15     /* Block device required */`
  - `ulib/axlibc/include/errno.h:L18-L18`：macro ENOTBLK
    代码片段：`#define ENOTBLK         15     /* Block device required */`
  - `tools/axlibc/include/errno.h:L38-L38`：macro EDEADLK
    代码片段：`#define EDEADLK         35     /* Resource deadlock would occur */`
  - `ulib/axlibc/include/errno.h:L38-L38`：macro EDEADLK
    代码片段：`#define EDEADLK         35     /* Resource deadlock would occur */`
- 宏名重合：与 ArceOS 在“系统调用”维度发现 3 个同名定义：EINTR, EROFS, ENOSYS。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `tools/axlibc/include/errno.h:L7-L7`：macro EINTR
    代码片段：`#define EINTR           4      /* Interrupted system call */`
  - `ulib/axlibc/include/errno.h:L7-L7`：macro EINTR
    代码片段：`#define EINTR           4      /* Interrupted system call */`
  - `tools/axlibc/include/errno.h:L33-L33`：macro EROFS
    代码片段：`#define EROFS           30     /* Read-only file system */`
  - `ulib/axlibc/include/errno.h:L33-L33`：macro EROFS
    代码片段：`#define EROFS           30     /* Read-only file system */`
- 函数/符号名重合：与 ArceOS 在“同步机制”维度发现 1 个同名定义：lock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `tools/raspi4/chainloader/src/synchronization.rs:L29-L29`：fn lock
    代码片段：`fn lock<'a, R>(&'a self, f: impl FnOnce(&'a mut Self::Data) -> R) -> R;`
  - `ulib/axstd/src/io/stdio.rs:L51-L51`：fn lock
    代码片段：`pub fn lock(&self) -> StdinLock<'static> {`
- 宏名重合：与 ArceOS 在“中断与异常”维度发现 1 个同名定义：EINTR。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `tools/axlibc/include/errno.h:L7-L7`：macro EINTR
    代码片段：`#define EINTR           4      /* Interrupted system call */`
  - `ulib/axlibc/include/errno.h:L7-L7`：macro EINTR
    代码片段：`#define EINTR           4      /* Interrupted system call */`
- 文件路径重合：与 ArceOS 在“文件系统”维度出现同名文件源码路径 `tools/axlibc/include/sys/stat.h` / `ulib/axlibc/include/sys/stat.h`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `tools/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
  - `ulib/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`

## 相似点

- 与 ArceOS 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/raspi4/chainloader/src/driver.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! Driver support. use crate::synchronization::{interface::Mutex, NullLock};`
  - `tools/raspi4/chainloader/src/console.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! System console. mod null_console;`
- 与 ArceOS 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
  - `modules/axfs/src/fs/fatfs.rs:L32-L36`：关键词命中
    代码片段：`fatfs::format_volume(&mut disk, opts).expect("failed to format volume"); let inner = fatfs::FileSystem::new(disk, fatfs::FsOptions::new()) .expect("failed to initialize FAT file...`
- 与 ArceOS 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/c/pow.c:L601-L605`：关键词命中
    代码片段：`if (y == 0.0) y = asdouble(sbits & 0x8000000000000000); /* The underflow exception needs to be signaled explicitly.  */ fp_force_eval(fp_barrier(0x1p-1022) * 0x1p-1022); }`
  - `tools/axlibc/c/time.c:L109-L113`：关键词命中
    代码片段：`} struct tm *gmtime(const time_t *timer) { static struct tm tm;`
- 与 ArceOS 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `apps/task/tls/src/main.rs:L9-L13`：关键词命中
    代码片段：`use core::ptr::addr_of; use std::{thread, vec::Vec}; #[thread_local]`
  - `apps/task/sleep/src/main.rs:L7-L11`：关键词命中
    代码片段：`use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
- 与 ArceOS 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/src/rand.rs:L3-L7`：关键词命中
    代码片段：`use core::{ ffi::{c_int, c_long, c_uint}, sync::atomic::{AtomicU64, Ordering::SeqCst}, };`
  - `apps/task/sleep/src/main.rs:L6-L10`：关键词命中
    代码片段：`extern crate axstd as std; use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
- 与 ArceOS 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/include/signal.h:L102-L106`：macro si_syscall
    代码片段：`#define si_int       si_value.sival_int #define si_call_addr __si_fields.__sigsys.si_call_addr #define si_syscall   __si_fields.__sigsys.si_syscall #define si_arch      __si_fie...`
  - `api/arceos_posix_api/src/imp/fs.rs:L107-L111`：fn sys_open
    代码片段：`/// Return its index in the file table ('fd'). Return 'EMFILE' if it already /// has the maximum number of files open. pub fn sys_open(filename: *const c_char, flags: c_int, mod...`
- 与 ArceOS 在 driver, filesystem, interrupt, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 ArceOS 的语言构成不同：待测作品为 {'json': 33, 'build': 974, 'markdown': 5808, 'toml': 376, 'c': 10873, 'make': 596, 'rust': 5140, 'asm': 125, 'text': 53}，历史样本为 {'json': 20, 'build': 1933, 'markdown': 1596, 'toml': 138, 'c': 10256, 'rust': 20231, 'make': 679, 'asm': 189, 'text': 6}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：23
- 含证据关键结论数：23（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
