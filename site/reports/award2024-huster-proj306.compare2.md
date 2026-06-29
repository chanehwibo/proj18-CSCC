# HUSTer proj306 Rust OS for framekernel architecture 比较报告

- 对比历史仓库：ArceOS
- 生成时间：2026-06-29T13:39:44.361098+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- ArceOS（来源：教学基线）：画像相似度 score=6.48；架构重合度 0.33; 语言构成相似度 0.69; OS 维度重合度 1.00; 代码规模接近度 0.44

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 ArceOS 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/comps/virtio/src/lib.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! The virtio of Asterinas. #![no_std] #![deny(unsafe_code)]`
  - `asterinas/kernel/aster-nix/src/console.rs:L3-L7`：关键词命中
    代码片段：`//! 'print' and 'println' macros //! //! FIXME: It will print to all 'virtio-console' devices, which is not a good choice. //!`
  - `modules/axdriver/src/virtio.rs:L19-L23`：关键词命中
    代码片段：`} /// A trait for VirtIO device meta information. pub trait VirtIoDevMeta { const DEVICE_TYPE: DeviceType;`
  - `modules/axdriver/src/drivers.rs:L6-L10`：关键词命中
    代码片段：`use axdriver_base::DeviceType; #[cfg(feature = "virtio")] use crate::virtio::{self, VirtIoDevMeta};`
- 与 ArceOS 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/fs/device.rs:L5-L9`：关键词命中
    代码片段：`fs::{ fs_resolver::{FsPath, FsResolver}, path::Dentry, utils::{InodeMode, InodeType}, },`
  - `asterinas/kernel/aster-nix/src/fs/rootfs.rs:L56-L60`：关键词命中
    代码片段：`match metadata.file_type() { FileType::File => { let dentry = parent.new_fs_child(name, InodeType::File, mode)?; entry.read_all(dentry.inode().writer(0))?; }`
  - `modules/axfs/src/fs/fatfs.rs:L32-L36`：关键词命中
    代码片段：`fatfs::format_volume(&mut disk, opts).expect("failed to format volume"); let inner = fatfs::FileSystem::new(disk, fatfs::FsOptions::new()) .expect("failed to initialize FAT file...`
  - `modules/axfs/src/lib.rs:L5-L9`：关键词命中
    代码片段：`//! # Cargo Features //! //! - 'fatfs': Use [FAT] as the main filesystem and mount it on '/'. This feature //!   is **enabled** by default. //! - 'devfs': Mount ['axfs_devfs::De...`
- 与 ArceOS 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `asterinas/ostd/src/trap/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Handles trap across kernel and user space. mod handler;`
  - `modules/axhal/src/irq.rs:L1-L3`：关键词命中
    代码片段：`//! Interrupt management. use axcpu::trap::{IRQ, register_trap_handler};`
  - `modules/axhal/src/lib.rs:L20-L24`：关键词命中
    代码片段：`//! - 'fp-simd': Enable floating-point and SIMD support. //! - 'paging': Enable page table manipulation. //! - 'irq': Enable interrupt handling support. //! - 'tls': Enable kern...`
- 与 ArceOS 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/mm/io.rs:L241-L245`：关键词命中
    代码片段：`/// When the operating range is in kernel space, the memory within that range /// is guaranteed to be valid. /// When the operating range is in user space, it is ensured that th...`
  - `asterinas/ostd/src/mm/mod.rs:L11-L15`：关键词命中
    代码片段：`pub(crate) mod dma; pub mod frame; pub(crate) mod heap_allocator; mod io; pub(crate) mod kspace;`
  - `modules/axmm/src/backend/alloc.rs:L1-L5`：关键词命中
    代码片段：`use axalloc::global_allocator; use axhal::mem::{phys_to_virt, virt_to_phys}; use axhal::paging::{MappingFlags, PageSize, PageTable}; use memory_addr::{PAGE_SIZE_4K, PageIter4K,...`
  - `modules/axmm/src/lib.rs:L78-L82`：关键词命中
    代码片段：`let mut aspace = AddrSpace::new_empty(base, size)?; if !cfg!(target_arch = "aarch64") && !cfg!(target_arch = "loongarch64") { // ARMv8 (aarch64) and LoongArch64 use separate pag...`
- 与 ArceOS 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/mod.rs:L5-L9`：关键词命中
    代码片段：`mod priority; mod processor; mod scheduler; #[allow(clippy::module_inception)] mod task;`
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
  - `modules/axfs/src/root.rs:L174-L178`：关键词命中
    代码片段：`#[cfg(feature = "procfs")] root_dir // should not fail .mount("/proc", mounts::procfs().unwrap()) .expect("fail to mount procfs at /proc");`
  - `modules/axhal/src/lib.rs:L21-L25`：关键词命中
    代码片段：`//! - 'paging': Enable page table manipulation. //! - 'irq': Enable interrupt handling support. //! - 'tls': Enable kernel space thread-local storage support. //! - 'rtc': Enabl...`
- 与 ArceOS 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/mod.rs:L4-L8`：关键词命中
    代码片段：`mod atomic_bits; mod mutex; // TODO: refactor this rcu implementation // Comment out this module since it raises lint error`
  - `asterinas/ostd/src/sync/spin.rs:L8-L12`：关键词命中
    代码片段：`fmt, ops::{Deref, DerefMut}, sync::atomic::{AtomicBool, Ordering}, };`
  - `modules/axfs/src/root.rs:L7-L11`：关键词命中
    代码片段：`use axfs_vfs::{VfsNodeAttr, VfsNodeOps, VfsNodeRef, VfsNodeType, VfsOps, VfsResult}; use axns::{ResArc, def_resource}; use axsync::Mutex; use lazyinit::LazyInit;`
  - `modules/axhal/src/lib.rs:L113-L117`：关键词命中
    代码片段：`pub use axplat::init::{init_early_secondary, init_later_secondary}; #[cfg(feature = "smp")] use core::sync::atomic::{AtomicUsize, Ordering}; /// Initializes CPU-local data struc...`
- 与 ArceOS 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/syscall/brk.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 use crate::{prelude::*, syscall::SyscallReturn}; /// expand the user heap to new heap end, returns the new heap end if expansion succeeds.`
  - `asterinas/kernel/aster-nix/src/syscall/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Read the Cpu context content then dispatch syscall to corrsponding handler //! The each sub module contains functions that handle real sy...`
  - `api/arceos_posix_api/src/imp/fs.rs:L107-L111`：fn sys_open
    代码片段：`/// Return its index in the file table ('fd'). Return 'EMFILE' if it already /// has the maximum number of files open. pub fn sys_open(filename: *const c_char, flags: c_int, mod...`
  - `api/arceos_posix_api/src/imp/fs.rs:L120-L124`：fn sys_lseek
    代码片段：`/// /// Return its position after seek. pub fn sys_lseek(fd: c_int, offset: ctypes::off_t, whence: c_int) -> ctypes::off_t { debug!("sys_lseek <= {} {} {}", fd, offset, whence);...`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 函数/符号名重合：与 ArceOS 在“同步机制”维度发现 3 个同名定义：lock, try_lock, unlock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `asterinas/ostd/src/sync/mutex.rs:L35-L35`：fn lock
    代码片段：`pub fn lock(&self) -> MutexGuard<T> {`
  - `ulib/axstd/src/io/stdio.rs:L51-L51`：fn lock
    代码片段：`pub fn lock(&self) -> StdinLock<'static> {`
  - `asterinas/ostd/src/sync/mutex.rs:L50-L50`：fn try_lock
    代码片段：`pub fn try_lock(&self) -> Option<MutexGuard<T>> {`
  - `ulib/axstd/src/sync/mutex.rs:L64-L64`：fn try_lock
    代码片段：`fn try_lock(&self) -> bool {`
- 与 ArceOS 在“同步机制”维度发现片段级代码相似度 0.69 （token=0.53, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：atomic, core, ordering, sync, use。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/wait.rs:L2-L6`：关键词命中
    代码片段：`use alloc::{collections::VecDeque, sync::Arc}; use core::sync::atomic::{AtomicBool, AtomicU32, Ordering}; use super::SpinLock;`
  - `modules/axsync/src/mutex.rs:L1-L3`：关键词命中
    代码片段：`//! A naïve sleeping mutex. use core::sync::atomic::{AtomicU64, Ordering};`
- 与 ArceOS 在“同步机制”维度发现片段级代码相似度 0.68 （token=0.50, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：atomic, ordering, sync。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/spin.rs:L8-L12`：关键词命中
    代码片段：`fmt, ops::{Deref, DerefMut}, sync::atomic::{AtomicBool, Ordering}, };`
  - `modules/axsync/src/mutex.rs:L1-L3`：关键词命中
    代码片段：`//! A naïve sleeping mutex. use core::sync::atomic::{AtomicU64, Ordering};`
- 文件路径重合：与 ArceOS 在“中断与异常”维度出现同名文件源码路径 `asterinas/ostd/src/trap/irq.rs` / `modules/axhal/src/irq.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `modules/axhal/src/irq.rs:L1-L3`：关键词命中
    代码片段：`//! Interrupt management. use axcpu::trap::{IRQ, register_trap_handler};`
- 文件路径重合：与 ArceOS 在“调度与任务管理”维度出现同名文件源码路径 `asterinas/ostd/src/task/task.rs` / `api/arceos_api/src/imp/task.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
  - `api/arceos_api/src/imp/task.rs:L1-L3`：fn ax_sleep_until
    代码片段：`pub fn ax_sleep_until(deadline: crate::time::AxTimeValue) { #[cfg(feature = "multitask")] axtask::sleep_until(deadline);`

## 相似点

- 与 ArceOS 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/comps/virtio/src/lib.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! The virtio of Asterinas. #![no_std] #![deny(unsafe_code)]`
  - `asterinas/kernel/aster-nix/src/console.rs:L3-L7`：关键词命中
    代码片段：`//! 'print' and 'println' macros //! //! FIXME: It will print to all 'virtio-console' devices, which is not a good choice. //!`
- 与 ArceOS 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/fs/device.rs:L5-L9`：关键词命中
    代码片段：`fs::{ fs_resolver::{FsPath, FsResolver}, path::Dentry, utils::{InodeMode, InodeType}, },`
  - `asterinas/kernel/aster-nix/src/fs/rootfs.rs:L56-L60`：关键词命中
    代码片段：`match metadata.file_type() { FileType::File => { let dentry = parent.new_fs_child(name, InodeType::File, mode)?; entry.read_all(dentry.inode().writer(0))?; }`
- 与 ArceOS 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `asterinas/ostd/src/trap/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Handles trap across kernel and user space. mod handler;`
- 与 ArceOS 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/mm/io.rs:L241-L245`：关键词命中
    代码片段：`/// When the operating range is in kernel space, the memory within that range /// is guaranteed to be valid. /// When the operating range is in user space, it is ensured that th...`
  - `asterinas/ostd/src/mm/mod.rs:L11-L15`：关键词命中
    代码片段：`pub(crate) mod dma; pub mod frame; pub(crate) mod heap_allocator; mod io; pub(crate) mod kspace;`
- 与 ArceOS 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/mod.rs:L5-L9`：关键词命中
    代码片段：`mod priority; mod processor; mod scheduler; #[allow(clippy::module_inception)] mod task;`
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
- 与 ArceOS 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/mod.rs:L4-L8`：关键词命中
    代码片段：`mod atomic_bits; mod mutex; // TODO: refactor this rcu implementation // Comment out this module since it raises lint error`
  - `asterinas/ostd/src/sync/spin.rs:L8-L12`：关键词命中
    代码片段：`fmt, ops::{Deref, DerefMut}, sync::atomic::{AtomicBool, Ordering}, };`
- 与 ArceOS 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/syscall/brk.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 use crate::{prelude::*, syscall::SyscallReturn}; /// expand the user heap to new heap end, returns the new heap end if expansion succeeds.`
  - `asterinas/kernel/aster-nix/src/syscall/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Read the Cpu context content then dispatch syscall to corrsponding handler //! The each sub module contains functions that handle real sy...`
- 与 ArceOS 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 ArceOS 的语言构成不同：待测作品为 {'json': 381, 'markdown': 3324, 'yaml': 49, 'build': 2417, 'toml': 215, 'make': 66, 'c': 7549, 'asm': 1515, 'rust': 112841}，历史样本为 {'json': 20, 'build': 1933, 'markdown': 1596, 'toml': 138, 'c': 10256, 'rust': 20231, 'make': 679, 'asm': 189, 'text': 6}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：19
- 含证据关键结论数：19（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
