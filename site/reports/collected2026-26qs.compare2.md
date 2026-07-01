# 2026 T2026105749910169 比较报告

- 对比历史仓库：2025 Chronix
- 生成时间：2026-07-01T20:55:18.384206+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2025 Chronix（来源：赛事历史作品）：画像相似度 score=9.95；同属 ucore-variant 风格; 语言构成相似度 0.99; OS 维度重合度 1.00; 代码规模接近度 0.98

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2025 Chronix 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `src/virtio/blk.rs:L2-L6`：关键词命中
    代码片段：`pub const SECTOR_SIZE: usize = 512; pub const VIRTIO_BLK_T_IN: u32 = 0; pub const VIRTIO_BLK_S_OK: u8 = 0; pub const VIRTIO_BLK_S_IOERR: u8 = 1;`
  - `os/src/drivers/mod.rs:L2-L5`：关键词命中
    代码片段：`pub mod dma; pub mod net; pub mod serial; pub use block::BLOCK_DEVICE;`
  - `os/src/drivers/net/mod.rs:L1-L4`：关键词命中
    代码片段：`#[allow(unused)] pub mod virtio_net; pub mod loopback; use core::{mem, ptr::NonNull};`
- 与 2025 Chronix 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
  - `os/src/fs/fs.rs:L4-L8`：关键词命中
    代码片段：`use alloc::sync::{Arc, Weak}; use crate::{fs::{tmpfs::{dentry::TmpDentry, inode::{InodeContent, TmpInode, TmpSysInode}}, vfs::{dentry::{global_find_dentry, global_update_dentry,...`
  - `os/src/fs/mod.rs:L1-L5`：关键词命中
    代码片段：`//! file system module: offer the file system interface //! define the file trait //! impl File for OSInode in 'inode.rs' //! impl Stdin and Stdout in 'stdio.rs' #![allow(missin...`
- 与 2025 Chronix 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L1413-L1417`：关键词命中
    代码片段：`signals: SignalState, /// ITIMER_REAL: absolute monotonic deadline of the next SIGALRM (0 = /// disarmed) and the repeat interval (0 = one-shot). The budget-timer tick /// raise...`
  - `src/vm.rs:L240-L244`：关键词命中
    代码片段：`/// The hardware activation token: RV = the satp value; LA = the root PA. fn root_token(&self) -> usize; /// Install the kernel identity mapping (RAM + MMIO, U=0) so the trap ha...`
  - `os/src/trap/mod.rs:L1-L3`：关键词命中
    代码片段：`//! Trap handling functionality //! //! For rCore, we have a single trap entry point, namely '__alltraps'. At`
  - `os/src/timer/ffi.rs:L1-L4`：关键词命中
    代码片段：`use alloc::collections::btree_map::Values; use crate::timer::get_current_time_ns; use super::{get_current_time_ms, NSEC_PER_SEC};`
- 与 2025 Chronix 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/memory.rs:L112-L116`：关键词命中
    代码片段：`// mapping (mmap(MAP_SHARED|MAP_ANONYMOUS) BEFORE the fork), which the parent reaps // for "Summary: passed N". Back it with zero-filled SharedFile frames — the same // fork-sha...`
  - `src/syscall/mod.rs:L203-L207`：关键词命中
    代码片段：`/// LTP getegid01/geteuid01 scan /proc/self/status for the Uid:/Gid: lines. const PROC_SELF_STATUS: &[u8] = b"Name:\tltp\nState:\tR (running)\nTgid:\t1\nPid:\t1\nPPid:\t0\nUid:\...`
  - `os/src/mm/mod.rs:L1-L5`：关键词命中
    代码片段：`//! Memory management implementation //! //! SV39 page-based virtual-memory architecture for RV64 systems, and //! everything about memory management, like frame allocator, page...`
  - `os/src/mm/user.rs:L2-L6`：关键词命中
    代码片段：`use alloc::sync::Arc; use hal::{addr::{VirtAddr, VirtAddrHal}, constant::{Constant, ConstantsHal}, pagetable::MapPerm, println}; use crate::{mm::vm::UserVmPagesLocker, processor...`
- 与 2025 Chronix 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L197-L201`：关键词命中
    代码片段：`const PROC_MEMINFO: &[u8] = b"MemTotal:       262144 kB\nMemFree:        131072 kB\nMemAvailable:   131072 kB\nBuffers:          4096 kB\nCached:          32768 kB\n"; const PRO...`
  - `src/syscall/file.rs:L884-L888`：关键词命中
    代码片段：`fn device_id_for_path(path: &[u8]) -> u64 { if path == b"/proc" || path.starts_with(b"/proc/") { 2 } else {`
  - `os/src/task/fs.rs:L1-L3`：关键词命中
    代码片段：`//! file system support for Task use alloc::{sync::Arc, vec::Vec};`
  - `os/src/task/mod.rs:L1-L3`：关键词命中
    代码片段：`//! Task management implementation //! //! Everything about task management, like starting and switching tasks is`
- 与 2025 Chronix 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L601-L605`：关键词命中
    代码片段：`// ---- SysV semaphores (semget / semop / semctl) ---- // A small global semaphore-set registry, sibling to the SysV-shm one above. Sets live // in kernel memory keyed by a 1-ba...`
  - `src/syscall/storage.rs:L195-L199`：关键词命中
    代码片段：`#[cfg(test)] static RUNTIME_STORAGE_POOL: std::sync::Mutex<RuntimeStoragePool> = std::sync::Mutex::new(RuntimeStoragePool::new());`
  - `os/src/sync/up.rs:L2-L6`：关键词命中
    代码片段：`use core::cell::{UnsafeCell, RefMut,RefCell}; use core::sync::atomic::{AtomicBool, Ordering}; use core::ops::{Deref, DerefMut}; use log::info;`
  - `os/src/sync/mod.rs:L6-L10`：关键词命中
    代码片段：`extern crate alloc; /// safe cell type for uniprocessor systems pub mod mutex; pub mod lazy;`
- 与 2025 Chronix 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/io.rs:L2-L6`：关键词命中
    代码片段：`//! and vectored ('readv'/'writev'/'preadv'/'pwritev' + v2) variants. //! //! Extracted handler domain (descendant of 'syscall'); reaches SyscallContext //! internals and shared...`
  - `src/syscall/mod.rs:L1379-L1383`：关键词命中
    代码片段：`pub ppid: usize, pub state: ProcessState, // The fields below stay private to the 'syscall' module. Handler domains // split into child modules (e.g. 'syscall::memory') are desc...`
  - `os/src/syscall/fd.rs:L1-L5`：关键词命中
    代码片段：`use alloc::sync::Arc; use crate::{fs::{tmpfs::{dentry::TmpDentry, inode::{EmptyFile, TmpSysInode}}, vfs::inode::InodeMode, OpenFlags}, syscall::{SysError, SysResult, SyscallId},...`
  - `os/src/syscall/fs.rs:L17-L21`：关键词命中
    代码片段：`use crate::processor::processor::{current_processor,current_task,current_user_token}; /// syscall: write pub async fn sys_write(fd: usize, buf: usize, len: usize) -> SysResult {...`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 函数/符号名重合：与 2025 Chronix 在“设备驱动”维度发现 4 个同名定义：write_str, from, as_slice, fmt。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/console.rs:L13-L13`：fn write_str
    代码片段：`fn write_str(&mut self, s: &str) -> fmt::Result {`
  - `user/src/console.rs:L11-L11`：fn write_str
    代码片段：`fn write_str(&mut self, s: &str) -> fmt::Result {`
  - `src/fs/ext4.rs:L58-L58`：fn from
    代码片段：`fn from(value: BlockError) -> Self {`
  - `os/src/devices/pci.rs:L41-L41`：fn from
    代码片段：`fn from(value: u8) -> Self {`
- 函数/符号名重合：与 2025 Chronix 在“文件系统”维度发现 4 个同名定义：len, new, read_at, write。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/ext4.rs:L132-L132`：fn len
    代码片段：`pub fn len(&self) -> usize {`
  - `os/src/fs/utils.rs:L40-L40`：fn len
    代码片段：`fn len(&self) -> usize {`
  - `src/fs/ext4.rs:L212-L212`：fn new
    代码片段：`pub fn new() -> Self {`
  - `os/src/fs/pipe.rs:L28-L28`：fn new
    代码片段：`pub fn new(capacity: usize) -> Self {`
- 函数/符号名重合：与 2025 Chronix 在“同步机制”维度发现 3 个同名定义：block_size, read_block, read_at。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/ext4.rs:L427-L427`：fn block_size
    代码片段：`pub fn block_size(&self) -> usize {`
  - `os/src/devices/mod.rs:L151-L151`：fn block_size
    代码片段：`fn block_size(&self) -> usize;`
  - `src/fs/ext4.rs:L773-L773`：fn read_block
    代码片段：`fn read_block(&mut self, block: u64, out: &mut [u8]) -> Result<(), Ext4Error> {`
  - `os/src/devices/buffer_cache.rs:L79-L79`：fn read_block
    代码片段：`pub fn read_block(&self, block_id: usize, buf: &mut [u8]) {`
- 结构体/类型重合：与 2025 Chronix 在“设备驱动”维度发现 1 个同名定义：BlockDevice。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/block.rs:L123-L123`：trait BlockDevice
    代码片段：`pub trait BlockDevice {`
  - `os/src/devices/mod.rs:L146-L146`：trait BlockDevice
    代码片段：`pub trait BlockDevice: Send + Sync + Any {`
- 结构体/类型重合：与 2025 Chronix 在“同步机制”维度发现 1 个同名定义：BlockDevice。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/block.rs:L123-L123`：trait BlockDevice
    代码片段：`pub trait BlockDevice {`
  - `os/src/devices/mod.rs:L146-L146`：trait BlockDevice
    代码片段：`pub trait BlockDevice: Send + Sync + Any {`
- 文件路径重合：与 2025 Chronix 在“系统调用”维度出现同名文件源码路径 `src/syscall/io.rs` / `os/src/syscall/io.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `src/syscall/io.rs:L2-L6`：关键词命中
    代码片段：`//! and vectored ('readv'/'writev'/'preadv'/'pwritev' + v2) variants. //! //! Extracted handler domain (descendant of 'syscall'); reaches SyscallContext //! internals and shared...`
  - `os/src/syscall/io.rs:L1-L3`：关键词命中
    代码片段：`//! io related syscall use core::{cmp, future::Future, mem, num::NonZeroI64, pin::Pin, ptr::read, sync::atomic::AtomicUsize, task::{Context, Poll}, time::Duration, usize};`

## 相似点

- 与 2025 Chronix 同属 ucore-variant 风格。（置信度：medium）
- 与 2025 Chronix 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `src/virtio/blk.rs:L2-L6`：关键词命中
    代码片段：`pub const SECTOR_SIZE: usize = 512; pub const VIRTIO_BLK_T_IN: u32 = 0; pub const VIRTIO_BLK_S_OK: u8 = 0; pub const VIRTIO_BLK_S_IOERR: u8 = 1;`
- 与 2025 Chronix 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
- 与 2025 Chronix 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L1413-L1417`：关键词命中
    代码片段：`signals: SignalState, /// ITIMER_REAL: absolute monotonic deadline of the next SIGALRM (0 = /// disarmed) and the repeat interval (0 = one-shot). The budget-timer tick /// raise...`
  - `src/vm.rs:L240-L244`：关键词命中
    代码片段：`/// The hardware activation token: RV = the satp value; LA = the root PA. fn root_token(&self) -> usize; /// Install the kernel identity mapping (RAM + MMIO, U=0) so the trap ha...`
- 与 2025 Chronix 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/memory.rs:L112-L116`：关键词命中
    代码片段：`// mapping (mmap(MAP_SHARED|MAP_ANONYMOUS) BEFORE the fork), which the parent reaps // for "Summary: passed N". Back it with zero-filled SharedFile frames — the same // fork-sha...`
  - `src/syscall/mod.rs:L203-L207`：关键词命中
    代码片段：`/// LTP getegid01/geteuid01 scan /proc/self/status for the Uid:/Gid: lines. const PROC_SELF_STATUS: &[u8] = b"Name:\tltp\nState:\tR (running)\nTgid:\t1\nPid:\t1\nPPid:\t0\nUid:\...`
- 与 2025 Chronix 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L197-L201`：关键词命中
    代码片段：`const PROC_MEMINFO: &[u8] = b"MemTotal:       262144 kB\nMemFree:        131072 kB\nMemAvailable:   131072 kB\nBuffers:          4096 kB\nCached:          32768 kB\n"; const PRO...`
  - `src/syscall/file.rs:L884-L888`：关键词命中
    代码片段：`fn device_id_for_path(path: &[u8]) -> u64 { if path == b"/proc" || path.starts_with(b"/proc/") { 2 } else {`
- 与 2025 Chronix 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L601-L605`：关键词命中
    代码片段：`// ---- SysV semaphores (semget / semop / semctl) ---- // A small global semaphore-set registry, sibling to the SysV-shm one above. Sets live // in kernel memory keyed by a 1-ba...`
  - `src/syscall/storage.rs:L195-L199`：关键词命中
    代码片段：`#[cfg(test)] static RUNTIME_STORAGE_POOL: std::sync::Mutex<RuntimeStoragePool> = std::sync::Mutex::new(RuntimeStoragePool::new());`
- 与 2025 Chronix 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/io.rs:L2-L6`：关键词命中
    代码片段：`//! and vectored ('readv'/'writev'/'preadv'/'pwritev' + v2) variants. //! //! Extracted handler domain (descendant of 'syscall'); reaches SyscallContext //! internals and shared...`
  - `src/syscall/mod.rs:L1379-L1383`：关键词命中
    代码片段：`pub ppid: usize, pub state: ProcessState, // The fields below stay private to the 'syscall' module. Handler domains // split into child modules (e.g. 'syscall::memory') are desc...`
- 与 2025 Chronix 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2025 Chronix 的语言构成不同：待测作品为 {'build': 267, 'markdown': 2266, 'asm': 662, 'toml': 12, 'rust': 42750}，历史样本为 {'json': 20, 'build': 353, 'markdown': 2055, 'toml': 139, 'make': 405, 'rust': 43626, 'asm': 381}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：20
- 含证据关键结论数：20（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
