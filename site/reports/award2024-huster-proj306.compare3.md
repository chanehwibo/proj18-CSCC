# HUSTer proj306 Rust OS for framekernel architecture 比较报告

- 对比历史仓库：zCore
- 生成时间：2026-06-28T12:08:03.819910+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- zCore（来源：教学基线）：画像相似度 score=7.42；架构重合度 0.50; 语言构成相似度 0.94; OS 维度重合度 1.00; 代码规模接近度 0.54

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 zCore 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/comps/virtio/src/lib.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! The virtio of Asterinas. #![no_std] #![deny(unsafe_code)]`
  - `asterinas/kernel/aster-nix/src/console.rs:L3-L7`：关键词命中
    代码片段：`//! 'print' and 'println' macros //! //! FIXME: It will print to all 'virtio-console' devices, which is not a good choice. //!`
  - `drivers/src/lib.rs:L1-L3`：关键词命中
    代码片段：`//! Device drivers of zCore. #![cfg_attr(not(feature = "mock"), no_std)]`
  - `drivers/src/io/mod.rs:L17-L21`：关键词命中
    代码片段：`// 用于处理外设地址空间访问的接口。 /// An interface for dealing with device address space access. pub trait Io { // 可访问的对象的类型。`
- 与 zCore 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/fs/device.rs:L5-L9`：关键词命中
    代码片段：`fs::{ fs_resolver::{FsPath, FsResolver}, path::Dentry, utils::{InodeMode, InodeType}, },`
  - `asterinas/kernel/aster-nix/src/fs/rootfs.rs:L56-L60`：关键词命中
    代码片段：`match metadata.file_type() { FileType::File => { let dentry = parent.new_fs_child(name, InodeType::File, mode)?; entry.read_all(dentry.inode().writer(0))?; }`
  - `zCore/src/fs.rs:L2-L6`：关键词命中
    代码片段：`if #[cfg(feature = "linux")] { use alloc::sync::Arc; use rcore_fs::vfs::FileSystem; #[cfg(feature = "libos")]`
  - `linux-object/src/fs/mod.rs:L31-L35`：关键词命中
    代码片段：`use kernel_hal::drivers; use rcore_fs::vfs::{FileSystem, FileType, INode, Result}; use rcore_fs_devfs::{ special::{NullINode, ZeroINode},`
- 与 zCore 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `asterinas/ostd/src/trap/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Handles trap across kernel and user space. mod handler;`
  - `drivers/src/irq/mod.rs:L1-L3`：关键词命中
    代码片段：`//! External interrupt request and handle. cfg_if::cfg_if! {`
  - `drivers/src/scheme/irq.rs:L22-L26`：关键词命中
    代码片段：`pub trait IrqScheme: Scheme { /// Is a valid IRQ number. fn is_valid_irq(&self, irq_num: usize) -> bool;`
- 与 zCore 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/mm/io.rs:L241-L245`：关键词命中
    代码片段：`/// When the operating range is in kernel space, the memory within that range /// is guaranteed to be valid. /// When the operating range is in user space, it is ensured that th...`
  - `asterinas/ostd/src/mm/mod.rs:L11-L15`：关键词命中
    代码片段：`pub(crate) mod dma; pub mod frame; pub(crate) mod heap_allocator; mod io; pub(crate) mod kspace;`
  - `zCore/src/memory.rs:L79-L83`：关键词命中
    代码片段：`} pub fn frame_alloc(frame_count: usize, align_log2: usize) -> Option<PhysAddr> { let (ptr, size) = HEAP .0`
  - `zCore/src/memory_x86_64.rs:L11-L15`：关键词命中
    代码片段：`/// Global physical frame allocator static FRAME_ALLOCATOR: Mutex<FrameAlloc> = Mutex::new(FrameAlloc::DEFAULT); #[inline]`
- 与 zCore 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/mod.rs:L5-L9`：关键词命中
    代码片段：`mod priority; mod processor; mod scheduler; #[allow(clippy::module_inception)] mod task;`
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
  - `linux-syscall/src/task.rs:L9-L13`：关键词命中
    代码片段：`use kernel_hal::context::UserContextField; use linux_object::thread::{CurrentThreadExt, RobustList, ThreadExt}; use linux_object::time::TimeSpec; use linux_object::{fs::INodeExt...`
  - `zircon-syscall/src/task.rs:L1-L4`：关键词命中
    代码片段：`use core::convert::TryFrom; use {super::*, zircon_object::task::*}; impl Syscall<'_> {`
- 与 zCore 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/mod.rs:L4-L8`：关键词命中
    代码片段：`mod atomic_bits; mod mutex; // TODO: refactor this rcu implementation // Comment out this module since it raises lint error`
  - `asterinas/ostd/src/sync/spin.rs:L8-L12`：关键词命中
    代码片段：`fmt, ops::{Deref, DerefMut}, sync::atomic::{AtomicBool, Ordering}, };`
  - `linux-object/src/sync/mod.rs:L3-L7`：关键词命中
    代码片段：`pub use self::event_bus::*; pub use self::semaphore::*; mod event_bus;`
  - `linux-object/src/sync/event_bus.rs:L10-L14`：关键词命中
    代码片段：`task::{Context, Poll}, }; use lock::Mutex; bitflags! {`
- 与 zCore 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/syscall/brk.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 use crate::{prelude::*, syscall::SyscallReturn}; /// expand the user heap to new heap end, returns the new heap end if expansion succeeds.`
  - `asterinas/kernel/aster-nix/src/syscall/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Read the Cpu context content then dispatch syscall to corrsponding handler //! The each sub module contains functions that handle real sy...`
  - `linux-syscall/src/task.rs:L30-L34`：关键词命中
    代码片段：`/// - ['nanosleep'](Self::sys_nanosleep) /// - ['set_tid_address'](Self::sys_set_tid_address) impl Syscall<'_> { /// 'fork' creates a new process by duplicating the calling proc...`
  - `zircon-syscall/src/task.rs:L2-L6`：关键词命中
    代码片段：`use {super::*, zircon_object::task::*}; impl Syscall<'_> { /// Create a new process. ///`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 函数/符号名重合：与 zCore 在“内存管理”维度发现 4 个同名定义：from, handle_page_fault, map, unmap。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `asterinas/ostd/src/error.rs:L27-L27`：fn from
    代码片段：`fn from(_err: PageTableError) -> Error {`
  - `zircon-object/src/hypervisor/mod.rs:L17-L17`：fn from
    代码片段：`fn from(e: RvmError) -> Self {`
  - `asterinas/ostd/src/mm/vm_space.rs:L104-L104`：fn handle_page_fault
    代码片段：`pub(crate) fn handle_page_fault(`
  - `zircon-object/src/hypervisor/guest.rs:L120-L120`：fn handle_page_fault
    代码片段：`fn handle_page_fault(&self, gpaddr: GuestPhysAddr) -> RvmResult {`
- 与 zCore 在“同步机制”维度发现片段级代码相似度 0.64 （token=0.55, structure=0.80）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：fn, impl, new, pub, self。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/spin.rs:L22-L26`：impl SpinLock<T>
    代码片段：`} impl<T> SpinLock<T> { /// Creates a new spin lock. pub const fn new(val: T) -> Self {`
  - `linux-object/src/sync/event_bus.rs:L53-L57`：fn new
    代码片段：`impl EventBus { /// create an event bus pub fn new() -> Arc<Mutex<Self>> { Arc::new(Mutex::new(Self::default())) }`
- 文件路径重合：与 zCore 在“文件系统”维度出现同名文件源码路径 `asterinas/kernel/aster-nix/src/fs/ext2/fs.rs` / `zCore/src/fs.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/fs/ext2/fs.rs:L6-L10`：关键词命中
    代码片段：`block_group::{BlockGroup, RawGroupDescriptor}, block_ptr::Ext2Bid, inode::{FilePerm, FileType, Inode, InodeDesc, RawInode}, prelude::*, super_block::{RawSuperBlock, SuperBlock,...`
  - `zCore/src/fs.rs:L2-L6`：关键词命中
    代码片段：`if #[cfg(feature = "linux")] { use alloc::sync::Arc; use rcore_fs::vfs::FileSystem; #[cfg(feature = "libos")]`
- 文件路径重合：与 zCore 在“中断与异常”维度出现同名文件源码路径 `asterinas/ostd/src/trap/irq.rs` / `drivers/src/scheme/irq.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `drivers/src/scheme/irq.rs:L22-L26`：关键词命中
    代码片段：`pub trait IrqScheme: Scheme { /// Is a valid IRQ number. fn is_valid_irq(&self, irq_num: usize) -> bool;`
- 文件路径重合：与 zCore 在“调度与任务管理”维度出现同名文件源码路径 `asterinas/ostd/src/task/task.rs` / `linux-syscall/src/task.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
  - `linux-syscall/src/task.rs:L9-L13`：关键词命中
    代码片段：`use kernel_hal::context::UserContextField; use linux_object::thread::{CurrentThreadExt, RobustList, ThreadExt}; use linux_object::time::TimeSpec; use linux_object::{fs::INodeExt...`
- 文件路径重合：与 zCore 在“调度与任务管理”维度出现同名文件源码路径 `asterinas/ostd/src/task/task.rs` / `zircon-syscall/src/task.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
  - `zircon-syscall/src/task.rs:L1-L4`：关键词命中
    代码片段：`use core::convert::TryFrom; use {super::*, zircon_object::task::*}; impl Syscall<'_> {`

## 相似点

- 与 zCore 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/comps/virtio/src/lib.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! The virtio of Asterinas. #![no_std] #![deny(unsafe_code)]`
  - `asterinas/kernel/aster-nix/src/console.rs:L3-L7`：关键词命中
    代码片段：`//! 'print' and 'println' macros //! //! FIXME: It will print to all 'virtio-console' devices, which is not a good choice. //!`
- 与 zCore 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/fs/device.rs:L5-L9`：关键词命中
    代码片段：`fs::{ fs_resolver::{FsPath, FsResolver}, path::Dentry, utils::{InodeMode, InodeType}, },`
  - `asterinas/kernel/aster-nix/src/fs/rootfs.rs:L56-L60`：关键词命中
    代码片段：`match metadata.file_type() { FileType::File => { let dentry = parent.new_fs_child(name, InodeType::File, mode)?; entry.read_all(dentry.inode().writer(0))?; }`
- 与 zCore 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `asterinas/ostd/src/trap/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Handles trap across kernel and user space. mod handler;`
- 与 zCore 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/mm/io.rs:L241-L245`：关键词命中
    代码片段：`/// When the operating range is in kernel space, the memory within that range /// is guaranteed to be valid. /// When the operating range is in user space, it is ensured that th...`
  - `asterinas/ostd/src/mm/mod.rs:L11-L15`：关键词命中
    代码片段：`pub(crate) mod dma; pub mod frame; pub(crate) mod heap_allocator; mod io; pub(crate) mod kspace;`
- 与 zCore 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/mod.rs:L5-L9`：关键词命中
    代码片段：`mod priority; mod processor; mod scheduler; #[allow(clippy::module_inception)] mod task;`
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
- 与 zCore 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/mod.rs:L4-L8`：关键词命中
    代码片段：`mod atomic_bits; mod mutex; // TODO: refactor this rcu implementation // Comment out this module since it raises lint error`
  - `asterinas/ostd/src/sync/spin.rs:L8-L12`：关键词命中
    代码片段：`fmt, ops::{Deref, DerefMut}, sync::atomic::{AtomicBool, Ordering}, };`
- 与 zCore 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/syscall/brk.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 use crate::{prelude::*, syscall::SyscallReturn}; /// expand the user heap to new heap end, returns the new heap end if expansion succeeds.`
  - `asterinas/kernel/aster-nix/src/syscall/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Read the Cpu context content then dispatch syscall to corrsponding handler //! The each sub module contains functions that handle real sy...`
- 与 zCore 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 zCore 的语言构成不同：新项目为 {'json': 381, 'markdown': 3324, 'yaml': 49, 'build': 2417, 'toml': 215, 'make': 66, 'c': 7549, 'asm': 1515, 'rust': 112841}，历史项目为 {'json': 91, 'build': 1519, 'markdown': 1927, 'toml': 60, 'rust': 50074, 'c': 694, 'asm': 109}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：20
- 含证据关键结论数：20（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
