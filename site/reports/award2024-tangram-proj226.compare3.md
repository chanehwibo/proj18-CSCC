# Tangram proj226 kernel components frameworks 比较报告

- 对比历史仓库：zCore
- 生成时间：2026-06-26T12:46:18.728984+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- zCore（来源：教学基线）：画像相似度 score=6.57；架构重合度 1.00; 语言构成相似度 0.29; OS 维度重合度 0.86; 代码规模接近度 0.55

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 zCore 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/raspi4/chainloader/src/driver.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! Driver support. use crate::synchronization::{interface::Mutex, NullLock};`
  - `tools/raspi4/chainloader/src/console.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! System console. mod null_console;`
  - `drivers/src/lib.rs:L1-L3`：关键词命中
    代码片段：`//! Device drivers of zCore. #![cfg_attr(not(feature = "mock"), no_std)]`
  - `drivers/src/io/mod.rs:L17-L21`：关键词命中
    代码片段：`// 用于处理外设地址空间访问的接口。 /// An interface for dealing with device address space access. pub trait Io { // 可访问的对象的类型。`
- 与 zCore 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
  - `zCore/src/fs.rs:L2-L6`：关键词命中
    代码片段：`if #[cfg(feature = "linux")] { use alloc::sync::Arc; use rcore_fs::vfs::FileSystem; #[cfg(feature = "libos")]`
  - `linux-object/src/fs/mod.rs:L31-L35`：关键词命中
    代码片段：`use kernel_hal::drivers; use rcore_fs::vfs::{FileSystem, FileType, INode, Result}; use rcore_fs_devfs::{ special::{NullINode, ZeroINode},`
- 与 zCore 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/c/pow.c:L601-L605`：关键词命中
    代码片段：`if (y == 0.0) y = asdouble(sbits & 0x8000000000000000); /* The underflow exception needs to be signaled explicitly.  */ fp_force_eval(fp_barrier(0x1p-1022) * 0x1p-1022); }`
  - `tools/axlibc/c/time.c:L109-L113`：关键词命中
    代码片段：`} struct tm *gmtime(const time_t *timer) { static struct tm tm;`
  - `drivers/src/irq/mod.rs:L1-L3`：关键词命中
    代码片段：`//! External interrupt request and handle. cfg_if::cfg_if! {`
  - `drivers/src/scheme/irq.rs:L22-L26`：关键词命中
    代码片段：`pub trait IrqScheme: Scheme { /// Is a valid IRQ number. fn is_valid_irq(&self, irq_num: usize) -> bool;`
- 与 zCore 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `apps/task/tls/src/main.rs:L9-L13`：关键词命中
    代码片段：`use core::ptr::addr_of; use std::{thread, vec::Vec}; #[thread_local]`
  - `apps/task/sleep/src/main.rs:L7-L11`：关键词命中
    代码片段：`use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
  - `linux-syscall/src/task.rs:L9-L13`：关键词命中
    代码片段：`use kernel_hal::context::UserContextField; use linux_object::thread::{CurrentThreadExt, RobustList, ThreadExt}; use linux_object::time::TimeSpec; use linux_object::{fs::INodeExt...`
  - `zircon-syscall/src/task.rs:L1-L4`：关键词命中
    代码片段：`use core::convert::TryFrom; use {super::*, zircon_object::task::*}; impl Syscall<'_> {`
- 与 zCore 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/src/rand.rs:L3-L7`：关键词命中
    代码片段：`use core::{ ffi::{c_int, c_long, c_uint}, sync::atomic::{AtomicU64, Ordering::SeqCst}, };`
  - `apps/task/sleep/src/main.rs:L6-L10`：关键词命中
    代码片段：`extern crate axstd as std; use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
  - `linux-object/src/sync/mod.rs:L3-L7`：关键词命中
    代码片段：`pub use self::event_bus::*; pub use self::semaphore::*; mod event_bus;`
  - `linux-object/src/sync/event_bus.rs:L10-L14`：关键词命中
    代码片段：`task::{Context, Poll}, }; use lock::Mutex; bitflags! {`
- 与 zCore 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `tools/axlibc/include/signal.h:L102-L106`：macro si_syscall
    代码片段：`#define si_int       si_value.sival_int #define si_call_addr __si_fields.__sigsys.si_call_addr #define si_syscall   __si_fields.__sigsys.si_syscall #define si_arch      __si_fie...`
  - `linux-syscall/src/task.rs:L30-L34`：关键词命中
    代码片段：`/// - ['nanosleep'](Self::sys_nanosleep) /// - ['set_tid_address'](Self::sys_set_tid_address) impl Syscall<'_> { /// 'fork' creates a new process by duplicating the calling proc...`
  - `zircon-syscall/src/task.rs:L2-L6`：关键词命中
    代码片段：`use {super::*, zircon_object::task::*}; impl Syscall<'_> { /// Create a new process. ///`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 未发现达到阈值的路径、符号、结构体/宏或片段级代码相似线索；当前仅保留功能维度重合证据。

## 相似点

- 与 zCore 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/raspi4/chainloader/src/driver.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! Driver support. use crate::synchronization::{interface::Mutex, NullLock};`
  - `tools/raspi4/chainloader/src/console.rs:L3-L7`：关键词命中
    代码片段：`// Copyright (c) 2018-2023 Andre Richter <andre.o.richter@gmail.com> //! System console. mod null_console;`
- 与 zCore 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/include/sys/stat.h:L7-L11`：关键词命中
    代码片段：`struct stat { dev_t st_dev;             /* ID of device containing file*/ ino_t st_ino;             /* inode number*/ mode_t st_mode;           /* protection*/ nlink_t st_nlink;...`
  - `zCore/src/fs.rs:L2-L6`：关键词命中
    代码片段：`if #[cfg(feature = "linux")] { use alloc::sync::Arc; use rcore_fs::vfs::FileSystem; #[cfg(feature = "libos")]`
- 与 zCore 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/c/pow.c:L601-L605`：关键词命中
    代码片段：`if (y == 0.0) y = asdouble(sbits & 0x8000000000000000); /* The underflow exception needs to be signaled explicitly.  */ fp_force_eval(fp_barrier(0x1p-1022) * 0x1p-1022); }`
  - `tools/axlibc/c/time.c:L109-L113`：关键词命中
    代码片段：`} struct tm *gmtime(const time_t *timer) { static struct tm tm;`
- 与 zCore 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `apps/task/tls/src/main.rs:L9-L13`：关键词命中
    代码片段：`use core::ptr::addr_of; use std::{thread, vec::Vec}; #[thread_local]`
  - `apps/task/sleep/src/main.rs:L7-L11`：关键词命中
    代码片段：`use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
- 与 zCore 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/src/rand.rs:L3-L7`：关键词命中
    代码片段：`use core::{ ffi::{c_int, c_long, c_uint}, sync::atomic::{AtomicU64, Ordering::SeqCst}, };`
  - `apps/task/sleep/src/main.rs:L6-L10`：关键词命中
    代码片段：`extern crate axstd as std; use std::sync::atomic::{AtomicUsize, Ordering}; use std::thread; use std::time::{Duration, Instant};`
- 与 zCore 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `tools/axlibc/include/signal.h:L102-L106`：macro si_syscall
    代码片段：`#define si_int       si_value.sival_int #define si_call_addr __si_fields.__sigsys.si_call_addr #define si_syscall   __si_fields.__sigsys.si_syscall #define si_arch      __si_fie...`
  - `linux-syscall/src/task.rs:L30-L34`：关键词命中
    代码片段：`/// - ['nanosleep'](Self::sys_nanosleep) /// - ['set_tid_address'](Self::sys_set_tid_address) impl Syscall<'_> { /// 'fork' creates a new process by duplicating the calling proc...`
- 与 zCore 在 driver, filesystem, interrupt, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 zCore 的语言构成不同：新项目为 {'json': 33, 'build': 974, 'markdown': 5808, 'toml': 376, 'c': 10873, 'make': 596, 'rust': 5140, 'asm': 125, 'text': 53}，历史项目为 {'json': 91, 'build': 1519, 'markdown': 1927, 'toml': 60, 'rust': 50074, 'c': 694, 'asm': 109}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：12
- 含证据关键结论数：12（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
