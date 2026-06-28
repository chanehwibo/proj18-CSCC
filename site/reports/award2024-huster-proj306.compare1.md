# HUSTer proj306 Rust OS for framekernel architecture 比较报告

- 对比历史仓库：2022 代码掐架队
- 生成时间：2026-06-28T12:51:00.682985+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2022 代码掐架队（来源：赛事历史作品）：画像相似度 score=6.66；语言构成相似度 0.94; OS 维度重合度 1.00; 代码规模接近度 0.79

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2022 代码掐架队 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/comps/virtio/src/lib.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! The virtio of Asterinas. #![no_std] #![deny(unsafe_code)]`
  - `asterinas/kernel/aster-nix/src/console.rs:L3-L7`：关键词命中
    代码片段：`//! 'print' and 'println' macros //! //! FIXME: It will print to all 'virtio-console' devices, which is not a good choice. //!`
  - `codes/os/src/console.rs:L13-L17`：关键词命中
    代码片段：`} static CONSOLE: Mutex<ConsoleInner> = Mutex::new(ConsoleInner {}); impl Write for Stdout {`
  - `codes/os/src/drivers/mod.rs:L1-L4`：关键词命中
    代码片段：`mod block; pub mod serial; pub use block::BLOCK_DEVICE;`
- 与 2022 代码掐架队 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/fs/device.rs:L5-L9`：关键词命中
    代码片段：`fs::{ fs_resolver::{FsPath, FsResolver}, path::Dentry, utils::{InodeMode, InodeType}, },`
  - `asterinas/kernel/aster-nix/src/fs/rootfs.rs:L56-L60`：关键词命中
    代码片段：`match metadata.file_type() { FileType::File => { let dentry = parent.new_fs_child(name, InodeType::File, mode)?; entry.read_all(dentry.inode().writer(0))?; }`
  - `codes/os/src/fs/mod.rs:L1-L5`：关键词命中
    代码片段：`mod pipe; pub mod stdio; mod inode; mod mount; pub mod finfo;`
  - `codes/os/src/fs/finfo.rs:L63-L67`：关键词命中
    代码片段：`} pub fn new(name:&str, inode:usize, offset:isize, reclen: u16, d_type: u8)->Self{ let mut dirent = Self{ d_ino:inode,`
- 与 2022 代码掐架队 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `asterinas/ostd/src/trap/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Handles trap across kernel and user space. mod handler;`
  - `codes/os/src/trap/mod.rs:L7-L11`：关键词命中
    代码片段：`use crate::syscall::{syscall, test}; use crate::task::*; use crate::timer::set_next_trigger; use riscv::register::{ mtvec::TrapMode,`
  - `codes/os/src/sbi.rs:L29-L33`：关键词命中
    代码片段：`} pub fn set_timer(timer: usize) { sbi_call(SBI_SET_TIMER, timer, 0, 0); }`
- 与 2022 代码掐架队 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/mm/io.rs:L241-L245`：关键词命中
    代码片段：`/// When the operating range is in kernel space, the memory within that range /// is guaranteed to be valid. /// When the operating range is in user space, it is ensured that th...`
  - `asterinas/ostd/src/mm/mod.rs:L11-L15`：关键词命中
    代码片段：`pub(crate) mod dma; pub mod frame; pub(crate) mod heap_allocator; mod io; pub(crate) mod kspace;`
  - `codes/os/src/mm/mod.rs:L1-L3`：关键词命中
    代码片段：`mod heap_allocator; mod address; mod frame_allocator;`
  - `codes/os/src/mm/memory_set.rs:L1-L3`：关键词命中
    代码片段：`use super::{PageTable, PageTableEntry, PTEFlags}; use super::{VirtPageNum, VirtAddr, PhysPageNum, PhysAddr}; use super::{FrameTracker, frame_alloc, frame_add_ref, enquire_refcou...`
- 与 2022 代码掐架队 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/mod.rs:L5-L9`：关键词命中
    代码片段：`mod priority; mod processor; mod scheduler; #[allow(clippy::module_inception)] mod task;`
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
  - `codes/os/src/task/mod.rs:L6-L10`：关键词命中
    代码片段：`mod info; mod switch; mod task; mod resource; pub use resource::RLimit;`
  - `codes/os/src/task/info.rs:L87-L91`：关键词命中
    代码片段：`pub const RUSAGE_SELF:isize = 0; /* The calling process.  */ pub const RUSAGE_CHILDREN:isize = -1; /* All of its terminated child processes.  */ pub const RUSAGE_THREAD:isize =...`
- 与 2022 代码掐架队 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/mod.rs:L4-L8`：关键词命中
    代码片段：`mod atomic_bits; mod mutex; // TODO: refactor this rcu implementation // Comment out this module since it raises lint error`
  - `asterinas/ostd/src/sync/spin.rs:L8-L12`：关键词命中
    代码片段：`fmt, ops::{Deref, DerefMut}, sync::atomic::{AtomicBool, Ordering}, };`
  - `codes/os/src/main.rs:L79-L83`：关键词命中
    代码片段：`lazy_static! { static ref CORE2_FLAG: Arc<Mutex<Core2flag>> = Arc::new(Mutex::new(Core2flag { is_in: false })); }`
  - `codes/os/src/console.rs:L1-L5`：关键词命中
    代码片段：`use crate::sbi::console_putchar; use core::fmt::{self, Write}; use spin::Mutex; struct Stdout;`
- 与 2022 代码掐架队 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/syscall/brk.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 use crate::{prelude::*, syscall::SyscallReturn}; /// expand the user heap to new heap end, returns the new heap end if expansion succeeds.`
  - `asterinas/kernel/aster-nix/src/syscall/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Read the Cpu context content then dispatch syscall to corrsponding handler //! The each sub module contains functions that handle real sy...`
  - `codes/os/src/syscall/fs.rs:L961-L965`：关键词命中
    代码片段：`} // This syscall is not complete at all, only /read proc/self/exe pub fn sys_readlinkat(dirfd: isize, pathname: *const u8, buf: *mut u8, bufsiz: usize) -> isize { if dirfd == A...`
  - `codes/os/src/syscall/mod.rs:L86-L90`：关键词命中
    代码片段：`// println!("test: run sys_getppid 1000000 times, start {:?}",start); for _ in 0..1000000{ syscall(SYSCALL_GETPPID,[0,0,0,0,0,0]); // unsafe{ //     asm!(`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 函数/符号名重合：与 2022 代码掐架队 在“内存管理”维度发现 4 个同名定义：new, is_empty, handle_alloc_error, add_to_heap。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `asterinas/ostd/src/user.rs:L27-L27`：fn new
    代码片段：`pub fn new(vm_space: Arc<VmSpace>, init_ctx: UserContext) -> Self {`
  - `codes/user/vendor/buddy_system_allocator/src/frame.rs:L39-L39`：fn new
    代码片段：`pub fn new() -> Self {`
  - `asterinas/ostd/src/boot/memory_region.rs:L75-L75`：fn is_empty
    代码片段：`pub fn is_empty(&self) -> bool {`
  - `codes/user/vendor/buddy_system_allocator/src/linked_list.rs:L28-L28`：fn is_empty
    代码片段：`pub fn is_empty(&self) -> bool {`
- 函数/符号名重合：与 2022 代码掐架队 在“同步机制”维度发现 4 个同名定义：fmt, lock, try_lock, unlock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `asterinas/ostd/src/sync/atomic_bits.rs:L280-L280`：fn fmt
    代码片段：`fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {`
  - `codes/user/vendor/spin/src/mutex.rs:L231-L231`：fn fmt
    代码片段：`fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {`
  - `asterinas/ostd/src/sync/mutex.rs:L35-L35`：fn lock
    代码片段：`pub fn lock(&self) -> MutexGuard<T> {`
  - `codes/user/vendor/spin/src/mutex.rs:L172-L172`：fn lock
    代码片段：`pub fn lock(&self) -> MutexGuard<T> {`
- 结构体/类型重合：与 2022 代码掐架队 在“同步机制”维度发现 3 个同名定义：LockedHeapWithRescue, Mutex, RwLock。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `asterinas/ostd/src/mm/heap_allocator.rs:L40-L40`：struct LockedHeapWithRescue
    代码片段：`struct LockedHeapWithRescue<const ORDER: usize> {`
  - `codes/user/vendor/buddy_system_allocator/src/lib.rs:L282-L282`：struct LockedHeapWithRescue
    代码片段：`pub struct LockedHeapWithRescue {`
  - `asterinas/ostd/src/sync/mutex.rs:L14-L14`：struct Mutex
    代码片段：`pub struct Mutex<T: ?Sized> {`
  - `codes/user/vendor/spin/src/mutex.rs:L86-L86`：struct Mutex
    代码片段：`pub struct Mutex<T: ?Sized> {`
- 结构体/类型重合：与 2022 代码掐架队 在“内存管理”维度发现 1 个同名定义：LockedHeapWithRescue。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `asterinas/ostd/src/mm/heap_allocator.rs:L40-L40`：struct LockedHeapWithRescue
    代码片段：`struct LockedHeapWithRescue<const ORDER: usize> {`
  - `codes/user/vendor/buddy_system_allocator/src/lib.rs:L282-L282`：struct LockedHeapWithRescue
    代码片段：`pub struct LockedHeapWithRescue {`
- 文件路径重合：与 2022 代码掐架队 在“设备驱动”维度出现同名文件源码路径 `asterinas/kernel/aster-nix/src/console.rs` / `codes/os/src/console.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/console.rs:L3-L7`：关键词命中
    代码片段：`//! 'print' and 'println' macros //! //! FIXME: It will print to all 'virtio-console' devices, which is not a good choice. //!`
  - `codes/os/src/console.rs:L13-L17`：关键词命中
    代码片段：`} static CONSOLE: Mutex<ConsoleInner> = Mutex::new(ConsoleInner {}); impl Write for Stdout {`

## 相似点

- 与 2022 代码掐架队 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/comps/virtio/src/lib.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! The virtio of Asterinas. #![no_std] #![deny(unsafe_code)]`
  - `asterinas/kernel/aster-nix/src/console.rs:L3-L7`：关键词命中
    代码片段：`//! 'print' and 'println' macros //! //! FIXME: It will print to all 'virtio-console' devices, which is not a good choice. //!`
- 与 2022 代码掐架队 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/fs/device.rs:L5-L9`：关键词命中
    代码片段：`fs::{ fs_resolver::{FsPath, FsResolver}, path::Dentry, utils::{InodeMode, InodeType}, },`
  - `asterinas/kernel/aster-nix/src/fs/rootfs.rs:L56-L60`：关键词命中
    代码片段：`match metadata.file_type() { FileType::File => { let dentry = parent.new_fs_child(name, InodeType::File, mode)?; entry.read_all(dentry.inode().writer(0))?; }`
- 与 2022 代码掐架队 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `asterinas/ostd/src/trap/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Handles trap across kernel and user space. mod handler;`
- 与 2022 代码掐架队 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/mm/io.rs:L241-L245`：关键词命中
    代码片段：`/// When the operating range is in kernel space, the memory within that range /// is guaranteed to be valid. /// When the operating range is in user space, it is ensured that th...`
  - `asterinas/ostd/src/mm/mod.rs:L11-L15`：关键词命中
    代码片段：`pub(crate) mod dma; pub mod frame; pub(crate) mod heap_allocator; mod io; pub(crate) mod kspace;`
- 与 2022 代码掐架队 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/task/mod.rs:L5-L9`：关键词命中
    代码片段：`mod priority; mod processor; mod scheduler; #[allow(clippy::module_inception)] mod task;`
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
- 与 2022 代码掐架队 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/ostd/src/sync/mod.rs:L4-L8`：关键词命中
    代码片段：`mod atomic_bits; mod mutex; // TODO: refactor this rcu implementation // Comment out this module since it raises lint error`
  - `asterinas/ostd/src/sync/spin.rs:L8-L12`：关键词命中
    代码片段：`fmt, ops::{Deref, DerefMut}, sync::atomic::{AtomicBool, Ordering}, };`
- 与 2022 代码掐架队 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `asterinas/kernel/aster-nix/src/syscall/brk.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 use crate::{prelude::*, syscall::SyscallReturn}; /// expand the user heap to new heap end, returns the new heap end if expansion succeeds.`
  - `asterinas/kernel/aster-nix/src/syscall/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Read the Cpu context content then dispatch syscall to corrsponding handler //! The each sub module contains functions that handle real sy...`
- 与 2022 代码掐架队 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2022 代码掐架队 的语言构成不同：待测作品为 {'json': 381, 'markdown': 3324, 'yaml': 49, 'build': 2417, 'toml': 215, 'make': 66, 'c': 7549, 'asm': 1515, 'rust': 112841}，历史样本为 {'json': 62, 'build': 2072, 'markdown': 7242, 'asm': 658, 'text': 1942, 'rust': 152844, 'c': 2166, 'toml': 15, 'yaml': 79}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：19
- 含证据关键结论数：19（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
