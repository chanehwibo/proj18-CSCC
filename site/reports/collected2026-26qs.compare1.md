# 2026 T2026105749910169 比较报告

- 对比历史仓库：2022 啊队队队
- 生成时间：2026-07-01T20:55:18.548119+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2022 啊队队队（来源：赛事历史作品）：画像相似度 score=9.43；同属 ucore-variant 风格; 语言构成相似度 0.98; OS 维度重合度 1.00; 代码规模接近度 0.48

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2022 啊队队队 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `src/virtio/blk.rs:L2-L6`：关键词命中
    代码片段：`pub const SECTOR_SIZE: usize = 512; pub const VIRTIO_BLK_T_IN: u32 = 0; pub const VIRTIO_BLK_S_OK: u8 = 0; pub const VIRTIO_BLK_S_IOERR: u8 = 1;`
  - `kernel/src/console.rs:L8-L12`：关键词命中
    代码片段：`macro_rules! print { ($fmt: literal $(, $($arg: tt)+)?) => { $crate::console::print(format_args!($fmt $(, $($arg)+)?)); } }`
  - `kernel/src/device/mod.rs:L9-L13`：关键词命中
    代码片段：`use fatfs::LossyOemCpConverter; use fatfs::NullTimeProvider; use virtio_drivers::VirtIOBlk; use virtio_drivers::VirtIOHeader; use crate::sync::mutex::Mutex;`
- 与 2022 啊队队队 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
  - `fatfs/src/fs.rs:L22-L26`：关键词命中
    代码片段：`use crate::time::{DefaultTimeProvider, TimeProvider}; // FAT implementation based on: //   http://wiki.osdev.org/FAT //   https://www.win.tue.nl/~aeb/linux/fs/fat/fat-1.html`
  - `kernel/src/fs/file.rs:L11-L15`：关键词命中
    代码片段：`use crate::memory::page_table::{PageMappingManager, PTEFlags}; use super::filetree::INode; #[allow(unused)]`
- 与 2022 啊队队队 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L1413-L1417`：关键词命中
    代码片段：`signals: SignalState, /// ITIMER_REAL: absolute monotonic deadline of the next SIGALRM (0 = /// disarmed) and the repeat interval (0 = one-shot). The budget-timer tick /// raise...`
  - `src/vm.rs:L240-L244`：关键词命中
    代码片段：`/// The hardware activation token: RV = the satp value; LA = the root PA. fn root_token(&self) -> usize; /// Install the kernel identity mapping (RAM + MMIO, U=0) so the trap ha...`
  - `kernel/src/interrupt/mod.rs:L1-L3`：关键词命中
    代码片段：`pub mod timer; use core::arch::global_asm;`
  - `kernel/src/main.rs:L13-L17`：关键词命中
    代码片段：`mod console; mod device; pub mod interrupt; mod memory; mod fs;`
- 与 2022 啊队队队 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/memory.rs:L112-L116`：关键词命中
    代码片段：`// mapping (mmap(MAP_SHARED|MAP_ANONYMOUS) BEFORE the fork), which the parent reaps // for "Summary: passed N". Back it with zero-filled SharedFile frames — the same // fork-sha...`
  - `src/syscall/mod.rs:L203-L207`：关键词命中
    代码片段：`/// LTP getegid01/geteuid01 scan /proc/self/status for the Uid:/Gid: lines. const PROC_SELF_STATUS: &[u8] = b"Name:\tltp\nState:\tR (running)\nTgid:\t1\nPid:\t1\nPPid:\t0\nUid:\...`
  - `kernel/src/memory/mod.rs:L4-L8`：关键词命中
    代码片段：`pub mod page; pub mod addr; pub mod page_table; pub mod mem_map; pub mod mem_set;`
  - `kernel/src/memory/heap.rs:L3-L7`：关键词命中
    代码片段：`// 堆大小 const HEAP_SIZE: usize = 0x0008_0000; // 堆空间`
- 与 2022 啊队队队 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L197-L201`：关键词命中
    代码片段：`const PROC_MEMINFO: &[u8] = b"MemTotal:       262144 kB\nMemFree:        131072 kB\nMemAvailable:   131072 kB\nBuffers:          4096 kB\nCached:          32768 kB\n"; const PRO...`
  - `src/syscall/file.rs:L884-L888`：关键词命中
    代码片段：`fn device_id_for_path(path: &[u8]) -> u64 { if path == b"/proc" || path.starts_with(b"/proc/") { 2 } else {`
  - `kernel/src/task/mod.rs:L14-L18`：关键词命中
    代码片段：`use crate::memory::page::alloc_more; use crate::runtime_err::RuntimeError; use crate::task::process::Process; use crate::task::task_scheduler::start_tasks; use crate::memory::pa...`
  - `kernel/src/task/task.rs:L4-L8`：关键词命中
    代码片段：`use crate::memory::addr::UserAddr; use crate::interrupt::Context; use crate::task::task_scheduler::kill_task; use super::process::Process;`
- 与 2022 啊队队队 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L601-L605`：关键词命中
    代码片段：`// ---- SysV semaphores (semget / semop / semctl) ---- // A small global semaphore-set registry, sibling to the SysV-shm one above. Sets live // in kernel memory keyed by a 1-ba...`
  - `src/syscall/storage.rs:L195-L199`：关键词命中
    代码片段：`#[cfg(test)] static RUNTIME_STORAGE_POOL: std::sync::Mutex<RuntimeStoragePool> = std::sync::Mutex::new(RuntimeStoragePool::new());`
  - `kernel/src/sync/mod.rs:L1-L1`：关键词命中
    代码片段：`pub mod mutex;`
  - `kernel/src/sync/mutex.rs:L1-L3`：关键词命中
    代码片段：`use core::sync::atomic::{AtomicBool, Ordering}; use core::cell::UnsafeCell; use core::marker::Sync;`
- 与 2022 啊队队队 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/io.rs:L2-L6`：关键词命中
    代码片段：`//! and vectored ('readv'/'writev'/'preadv'/'pwritev' + v2) variants. //! //! Extracted handler domain (descendant of 'syscall'); reaches SyscallContext //! internals and shared...`
  - `src/syscall/mod.rs:L1379-L1383`：关键词命中
    代码片段：`pub ppid: usize, pub state: ProcessState, // The fields below stay private to the 'syscall' module. Handler domains // split into child modules (e.g. 'syscall::memory') are desc...`
  - `kernel/src/sbi.rs:L19-L23`：关键词命中
    代码片段：`let mut ret; unsafe { asm!("ecall", in("a7") which, inlateout("a0") arg0 as i32 => ret,`
  - `device/src/sbi.rs:L19-L23`：关键词命中
    代码片段：`let mut ret; unsafe { asm!("ecall", in("a7") which, inlateout("a0") arg0 as i32 => ret,`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 与 2022 啊队队队 在“文件系统”维度发现片段级代码相似度 0.81 （token=0.70, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：clone, copy, debug, derive, enum, eq, partialeq, pub。（置信度：high）
  证据：
  - `src/fs/ext4.rs:L25-L29`：enum Ext4Error
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq)] pub enum Ext4Error { Block(BlockError), AddressOverflow,`
  - `fatfs/src/fs.rs:L30-L34`：enum FatType
    代码片段：`/// 'FatType' values are based on the size of File Allocation Table entry. #[derive(Copy, Clone, Eq, PartialEq, Debug)] pub enum FatType { /// 12 bits per FAT entry Fat12,`
- 函数/符号名重合：与 2022 啊队队队 在“设备驱动”维度发现 4 个同名定义：write_str, new, read_block, write。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/console.rs:L13-L13`：fn write_str
    代码片段：`fn write_str(&mut self, s: &str) -> fmt::Result {`
  - `kernel/src/console.rs:L127-L127`：fn write_str
    代码片段：`fn write_str(&mut self, s: &str) -> Result {`
  - `src/fs/ext4.rs:L212-L212`：fn new
    代码片段：`pub fn new() -> Self {`
  - `kernel/src/device/sdcard.rs:L164-L164`：fn new
    代码片段：`pub fn new(`
- 与 2022 啊队队队 在“设备驱动”维度发现片段级代码相似度 0.74 （token=0.73, structure=0.77）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：arg, console, crate, format_args, macro_rules, print, tt。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `kernel/src/console.rs:L8-L12`：关键词命中
    代码片段：`macro_rules! print { ($fmt: literal $(, $($arg: tt)+)?) => { $crate::console::print(format_args!($fmt $(, $($arg)+)?)); } }`
- 函数/符号名重合：与 2022 啊队队队 在“文件系统”维度发现 4 个同名定义：is_empty, new, open, read_block。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/ext4.rs:L136-L136`：fn is_empty
    代码片段：`pub fn is_empty(&self) -> bool {`
  - `kernel/src/fs/filetree.rs:L190-L190`：fn is_empty
    代码片段：`pub fn is_empty(&self) -> bool {`
  - `src/fs/ext4.rs:L212-L212`：fn new
    代码片段：`pub fn new() -> Self {`
  - `kernel/src/fs/file.rs:L92-L92`：fn new
    代码片段：`pub fn new(inode: Rc<INode>) -> Result<Rc<Self>, RuntimeError>{`
- 与 2022 啊队队队 在“文件系统”维度发现片段级代码相似度 0.63 （token=0.50, structure=0.88）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：clone, copy, debug, derive, eq, partialeq, pub。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `fatfs/src/fs.rs:L30-L34`：enum FatType
    代码片段：`/// 'FatType' values are based on the size of File Allocation Table entry. #[derive(Copy, Clone, Eq, PartialEq, Debug)] pub enum FatType { /// 12 bits per FAT entry Fat12,`
- 函数/符号名重合：与 2022 啊队队队 在“调度与任务管理”维度发现 1 个同名定义：new。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/cyclictest.rs:L73-L73`：fn new
    代码片段：`fn new() -> Self {`
  - `kernel/src/task/fd_table.rs:L24-L24`：fn new
    代码片段：`pub fn new(file: Rc<dyn FileOP>) -> Self {`
- 函数/符号名重合：与 2022 啊队队队 在“同步机制”维度发现 1 个同名定义：read_block。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L773-L773`：fn read_block
    代码片段：`fn read_block(&mut self, block: u64, out: &mut [u8]) -> Result<(), Ext4Error> {`
  - `kernel/src/device/block.rs:L8-L8`：fn read_block
    代码片段：`fn read_block(&mut self, sector_offset: usize, buf: &mut [u8]) {`
- 结构体/类型重合：与 2022 啊队队队 在“设备驱动”维度发现 1 个同名定义：BlockDevice。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/block.rs:L123-L123`：trait BlockDevice
    代码片段：`pub trait BlockDevice {`
  - `kernel/src/device/mod.rs:L42-L42`：trait BlockDevice
    代码片段：`pub trait BlockDevice {`
- 结构体/类型重合：与 2022 啊队队队 在“文件系统”维度发现 2 个同名定义：FileType, Inode。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L165-L165`：enum FileType
    代码片段：`pub enum FileType {`
  - `kernel/src/fs/file.rs:L40-L40`：enum FileType
    代码片段：`pub enum FileType {`
  - `src/fs/ext4.rs:L374-L374`：struct Inode
    代码片段：`pub struct Inode {`
  - `kernel/src/fs/filetree.rs:L32-L32`：struct INode
    代码片段：`pub struct INode(pub RefCell<INodeInner>);`
- 结构体/类型重合：与 2022 啊队队队 在“同步机制”维度发现 1 个同名定义：BlockDevice。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/block.rs:L123-L123`：trait BlockDevice
    代码片段：`pub trait BlockDevice {`
  - `kernel/src/device/mod.rs:L42-L42`：trait BlockDevice
    代码片段：`pub trait BlockDevice {`
- 文件路径重合：与 2022 啊队队队 在“设备驱动”维度出现同名文件源码路径 `src/console.rs` / `kernel/src/console.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `kernel/src/console.rs:L8-L12`：关键词命中
    代码片段：`macro_rules! print { ($fmt: literal $(, $($arg: tt)+)?) => { $crate::console::print(format_args!($fmt $(, $($arg)+)?)); } }`
- 文件路径重合：与 2022 啊队队队 在“文件系统”维度出现同名文件源码路径 `src/syscall/file.rs` / `kernel/src/fs/file.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
  - `kernel/src/fs/file.rs:L11-L15`：关键词命中
    代码片段：`use crate::memory::page_table::{PageMappingManager, PTEFlags}; use super::filetree::INode; #[allow(unused)]`

## 相似点

- 与 2022 啊队队队 同属 ucore-variant 风格。（置信度：medium）
- 与 2022 啊队队队 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `src/virtio/blk.rs:L2-L6`：关键词命中
    代码片段：`pub const SECTOR_SIZE: usize = 512; pub const VIRTIO_BLK_T_IN: u32 = 0; pub const VIRTIO_BLK_S_OK: u8 = 0; pub const VIRTIO_BLK_S_IOERR: u8 = 1;`
- 与 2022 啊队队队 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
- 与 2022 啊队队队 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L1413-L1417`：关键词命中
    代码片段：`signals: SignalState, /// ITIMER_REAL: absolute monotonic deadline of the next SIGALRM (0 = /// disarmed) and the repeat interval (0 = one-shot). The budget-timer tick /// raise...`
  - `src/vm.rs:L240-L244`：关键词命中
    代码片段：`/// The hardware activation token: RV = the satp value; LA = the root PA. fn root_token(&self) -> usize; /// Install the kernel identity mapping (RAM + MMIO, U=0) so the trap ha...`
- 与 2022 啊队队队 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/memory.rs:L112-L116`：关键词命中
    代码片段：`// mapping (mmap(MAP_SHARED|MAP_ANONYMOUS) BEFORE the fork), which the parent reaps // for "Summary: passed N". Back it with zero-filled SharedFile frames — the same // fork-sha...`
  - `src/syscall/mod.rs:L203-L207`：关键词命中
    代码片段：`/// LTP getegid01/geteuid01 scan /proc/self/status for the Uid:/Gid: lines. const PROC_SELF_STATUS: &[u8] = b"Name:\tltp\nState:\tR (running)\nTgid:\t1\nPid:\t1\nPPid:\t0\nUid:\...`
- 与 2022 啊队队队 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L197-L201`：关键词命中
    代码片段：`const PROC_MEMINFO: &[u8] = b"MemTotal:       262144 kB\nMemFree:        131072 kB\nMemAvailable:   131072 kB\nBuffers:          4096 kB\nCached:          32768 kB\n"; const PRO...`
  - `src/syscall/file.rs:L884-L888`：关键词命中
    代码片段：`fn device_id_for_path(path: &[u8]) -> u64 { if path == b"/proc" || path.starts_with(b"/proc/") { 2 } else {`
- 与 2022 啊队队队 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L601-L605`：关键词命中
    代码片段：`// ---- SysV semaphores (semget / semop / semctl) ---- // A small global semaphore-set registry, sibling to the SysV-shm one above. Sets live // in kernel memory keyed by a 1-ba...`
  - `src/syscall/storage.rs:L195-L199`：关键词命中
    代码片段：`#[cfg(test)] static RUNTIME_STORAGE_POOL: std::sync::Mutex<RuntimeStoragePool> = std::sync::Mutex::new(RuntimeStoragePool::new());`
- 与 2022 啊队队队 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/io.rs:L2-L6`：关键词命中
    代码片段：`//! and vectored ('readv'/'writev'/'preadv'/'pwritev' + v2) variants. //! //! Extracted handler domain (descendant of 'syscall'); reaches SyscallContext //! internals and shared...`
  - `src/syscall/mod.rs:L1379-L1383`：关键词命中
    代码片段：`pub ppid: usize, pub state: ProcessState, // The fields below stay private to the 'syscall' module. Handler domains // split into child modules (e.g. 'syscall::memory') are desc...`
- 与 2022 啊队队队 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2022 啊队队队 的语言构成不同：待测作品为 {'build': 267, 'markdown': 2266, 'asm': 662, 'toml': 12, 'rust': 42750}，历史样本为 {'yaml': 19, 'json': 20, 'build': 91, 'markdown': 995, 'text': 19, 'toml': 2, 'rust': 13878, 'asm': 227}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：26
- 含证据关键结论数：26（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
