# 2026 T2026105749910169 比较报告

- 对比历史仓库：2022 Maturin
- 生成时间：2026-07-01T20:55:18.582593+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2022 Maturin（来源：赛事历史作品）：画像相似度 score=9.37；同属 ucore-variant 风格; 语言构成相似度 0.75; OS 维度重合度 1.00; 代码规模接近度 0.87

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2022 Maturin 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `src/virtio/blk.rs:L2-L6`：关键词命中
    代码片段：`pub const SECTOR_SIZE: usize = 512; pub const VIRTIO_BLK_T_IN: u32 = 0; pub const VIRTIO_BLK_S_OK: u8 = 0; pub const VIRTIO_BLK_S_IOERR: u8 = 1;`
  - `kernel/src/console.rs:L21-L25`：关键词命中
    代码片段：`#[macro_export] macro_rules! info { () => ($crate::console::info(core::format_args!("\n"));); ($($arg:tt)*) => { $crate::console::info(core::format_args!($($arg)*));`
  - `kernel/src/drivers/block/mod.rs:L2-L6`：关键词命中
    代码片段：`use alloc::sync::Arc; mod virtio_block; mod block_device; pub use virtio_block::VirtIOBlock;`
- 与 2022 Maturin 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
  - `rust-fatfs/src/fs.rs:L21-L25`：关键词命中
    代码片段：`use crate::time::{DefaultTimeProvider, TimeProvider}; // FAT implementation based on: //   http://wiki.osdev.org/FAT //   https://www.win.tue.nl/~aeb/linux/fs/fat/fat-1.html`
  - `kernel/src/file/mod.rs:L9-L13`：关键词命中
    代码片段：`mod socket; mod stdio; mod vfs; use crate::timer::TimeSpec;`
- 与 2022 Maturin 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L1413-L1417`：关键词命中
    代码片段：`signals: SignalState, /// ITIMER_REAL: absolute monotonic deadline of the next SIGALRM (0 = /// disarmed) and the repeat interval (0 = one-shot). The budget-timer tick /// raise...`
  - `src/vm.rs:L240-L244`：关键词命中
    代码片段：`/// The hardware activation token: RV = the satp value; LA = the root PA. fn root_token(&self) -> usize; /// Install the kernel identity mapping (RAM + MMIO, U=0) so the trap ha...`
  - `kernel/src/trap/mod.rs:L1-L5`：关键词命中
    代码片段：`//! 中断异常处理 //! //! 所有中断和异常的入口在 trap.S 中的 __alltraps，它会在保存上下文信息后跳转到本文件中的 trap_handler 函数 //! //! 在这个模块中，程序的执行流不一定正常。主要有三种可能：`
  - `kernel/src/trap/trap.S:L14-L18`：关键词命中
    代码片段：`bgtz sp, __user_trap_start # here is prework before kernel trap entry # in "__real_trap_entry", tp will be replaced by 34*8(sp), where we assumed is saved by __restore before. #...`
- 与 2022 Maturin 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/memory.rs:L112-L116`：关键词命中
    代码片段：`// mapping (mmap(MAP_SHARED|MAP_ANONYMOUS) BEFORE the fork), which the parent reaps // for "Summary: passed N". Back it with zero-filled SharedFile frames — the same // fork-sha...`
  - `src/syscall/mod.rs:L203-L207`：关键词命中
    代码片段：`/// LTP getegid01/geteuid01 scan /proc/self/status for the Uid:/Gid: lines. const PROC_SELF_STATUS: &[u8] = b"Name:\tltp\nState:\tR (running)\nTgid:\t1\nPid:\t1\nPPid:\t0\nUid:\...`
  - `kernel/src/memory/mod.rs:L4-L8`：关键词命中
    代码片段：`mod allocator; mod areas; mod page_table; mod user; mod vmm;`
  - `kernel/src/memory/vmm.rs:L4-L8`：关键词命中
    代码片段：`addr_to_page_id, align_down, align_up, cross_page, get_phys_memory_regions, page_count, page_id_to_addr, virt_to_phys, DiffSet, CutSet, PTEFlags, PageTable, PmAreaLazy, VirtAddr...`
- 与 2022 Maturin 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L197-L201`：关键词命中
    代码片段：`const PROC_MEMINFO: &[u8] = b"MemTotal:       262144 kB\nMemFree:        131072 kB\nMemAvailable:   131072 kB\nBuffers:          4096 kB\nCached:          32768 kB\n"; const PRO...`
  - `src/syscall/file.rs:L884-L888`：关键词命中
    代码片段：`fn device_id_for_path(path: &[u8]) -> u64 { if path == b"/proc" || path.starts_with(b"/proc/") { 2 } else {`
  - `kernel/src/task/mod.rs:L9-L13`：关键词命中
    代码片段：`mod cpu_local; mod kernel_stack; mod scheduler; mod switch; mod task;`
  - `kernel/src/task/task.rs:L25-L29`：关键词命中
    代码片段：`/// /// 目前来说，TCB外层可能是调度器或者 CpuLocal： /// 1. 如果它在调度器里，则 Scheduler 内部不会修改它，且从 Scheduler 里取出或者放入 TCB 是由调度器外部的 Mutex 保护的； /// 2. 如果它在 CpuLocal 里，则同时只会有一个核可以访问它，也不会冲突。 pub struct Tas...`
- 与 2022 Maturin 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L601-L605`：关键词命中
    代码片段：`// ---- SysV semaphores (semget / semop / semctl) ---- // A small global semaphore-set registry, sibling to the SysV-shm one above. Sets live // in kernel memory keyed by a 1-ba...`
  - `src/syscall/storage.rs:L195-L199`：关键词命中
    代码片段：`#[cfg(test)] static RUNTIME_STORAGE_POOL: std::sync::Mutex<RuntimeStoragePool> = std::sync::Mutex::new(RuntimeStoragePool::new());`
  - `rust-fatfs/src/fs.rs:L8-L12`：关键词命中
    代码片段：`use core::marker::PhantomData; use core::u32; use lock::Mutex; use crate::boot_sector::{format_boot_sector, BiosParameterBlock, BootSector};`
  - `kernel/src/console.rs:L36-L40`：关键词命中
    代码片段：`} /// 打印格式字串，使用与 print 不同的 Mutex 锁 #[macro_export] macro_rules! eprint {`
- 与 2022 Maturin 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall/io.rs:L2-L6`：关键词命中
    代码片段：`//! and vectored ('readv'/'writev'/'preadv'/'pwritev' + v2) variants. //! //! Extracted handler domain (descendant of 'syscall'); reaches SyscallContext //! internals and shared...`
  - `src/syscall/mod.rs:L1379-L1383`：关键词命中
    代码片段：`pub ppid: usize, pub state: ProcessState, // The fields below stay private to the 'syscall' module. Handler domains // split into child modules (e.g. 'syscall::memory') are desc...`
  - `kernel/src/syscall/fs.rs:L1-L5`：关键词命中
    代码片段：`//! 与读写、文件相关的系统调用 //! //! 注意获取 current_task 的时候都使用了 unwrap()，这意味着默认只有用户程序才会调用 syscall 模块进行操作。 //! 如果内核态异常中断需要处理， trap 只能利用其他模块，如 MemorySet::handle_kernel_page_fault 等`
  - `kernel/src/syscall/mod.rs:L43-L47`：关键词命中
    代码片段：`/// 处理系统调用 pub fn syscall(syscall_id: usize, args: [usize; 6]) -> isize { let syscall_id = if let Ok(id) = SyscallNo::try_from(syscall_id) { id`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 与 2022 Maturin 在“文件系统”维度发现片段级代码相似度 0.81 （token=0.70, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：clone, copy, debug, derive, enum, eq, partialeq, pub。（置信度：high）
  证据：
  - `src/fs/ext4.rs:L25-L29`：enum Ext4Error
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq)] pub enum Ext4Error { Block(BlockError), AddressOverflow,`
  - `rust-fatfs/src/fs.rs:L29-L33`：enum FatType
    代码片段：`/// 'FatType' values are based on the size of File Allocation Table entry. #[derive(Copy, Clone, Eq, PartialEq, Debug)] pub enum FatType { /// 12 bits per FAT entry Fat12,`
- 与 2022 Maturin 在“设备驱动”维度发现片段级代码相似度 0.68 （token=0.62, structure=0.77）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：arg, console, crate, format_args, macro_rules, tt。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `kernel/src/console.rs:L21-L25`：关键词命中
    代码片段：`#[macro_export] macro_rules! info { () => ($crate::console::info(core::format_args!("\n"));); ($($arg:tt)*) => { $crate::console::info(core::format_args!($($arg)*));`
- 函数/符号名重合：与 2022 Maturin 在“文件系统”维度发现 4 个同名定义：clear, len, is_empty, default。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/ext4.rs:L109-L109`：fn clear
    代码片段：`pub fn clear(&mut self) {`
  - `rust-fatfs/src/dir.rs:L764-L764`：fn clear
    代码片段：`fn clear(&mut self) {`
  - `src/fs/ext4.rs:L132-L132`：fn len
    代码片段：`pub fn len(&self) -> usize {`
  - `rust-fatfs/src/dir.rs:L768-L768`：fn len
    代码片段：`pub(crate) fn len(&self) -> usize {`
- 与 2022 Maturin 在“文件系统”维度发现片段级代码相似度 0.63 （token=0.50, structure=0.88）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：clone, copy, debug, derive, eq, partialeq, pub。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `rust-fatfs/src/fs.rs:L29-L33`：enum FatType
    代码片段：`/// 'FatType' values are based on the size of File Allocation Table entry. #[derive(Copy, Clone, Eq, PartialEq, Debug)] pub enum FatType { /// 12 bits per FAT entry Fat12,`
- 文件路径重合：与 2022 Maturin 在“设备驱动”维度出现同名文件源码路径 `src/console.rs` / `kernel/src/console.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `kernel/src/console.rs:L21-L25`：关键词命中
    代码片段：`#[macro_export] macro_rules! info { () => ($crate::console::info(core::format_args!("\n"));); ($($arg:tt)*) => { $crate::console::info(core::format_args!($($arg)*));`

## 相似点

- 与 2022 Maturin 同属 ucore-variant 风格。（置信度：medium）
- 与 2022 Maturin 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `src/virtio/blk.rs:L2-L6`：关键词命中
    代码片段：`pub const SECTOR_SIZE: usize = 512; pub const VIRTIO_BLK_T_IN: u32 = 0; pub const VIRTIO_BLK_S_OK: u8 = 0; pub const VIRTIO_BLK_S_IOERR: u8 = 1;`
- 与 2022 Maturin 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
- 与 2022 Maturin 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L1413-L1417`：关键词命中
    代码片段：`signals: SignalState, /// ITIMER_REAL: absolute monotonic deadline of the next SIGALRM (0 = /// disarmed) and the repeat interval (0 = one-shot). The budget-timer tick /// raise...`
  - `src/vm.rs:L240-L244`：关键词命中
    代码片段：`/// The hardware activation token: RV = the satp value; LA = the root PA. fn root_token(&self) -> usize; /// Install the kernel identity mapping (RAM + MMIO, U=0) so the trap ha...`
- 与 2022 Maturin 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/memory.rs:L112-L116`：关键词命中
    代码片段：`// mapping (mmap(MAP_SHARED|MAP_ANONYMOUS) BEFORE the fork), which the parent reaps // for "Summary: passed N". Back it with zero-filled SharedFile frames — the same // fork-sha...`
  - `src/syscall/mod.rs:L203-L207`：关键词命中
    代码片段：`/// LTP getegid01/geteuid01 scan /proc/self/status for the Uid:/Gid: lines. const PROC_SELF_STATUS: &[u8] = b"Name:\tltp\nState:\tR (running)\nTgid:\t1\nPid:\t1\nPPid:\t0\nUid:\...`
- 与 2022 Maturin 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L197-L201`：关键词命中
    代码片段：`const PROC_MEMINFO: &[u8] = b"MemTotal:       262144 kB\nMemFree:        131072 kB\nMemAvailable:   131072 kB\nBuffers:          4096 kB\nCached:          32768 kB\n"; const PRO...`
  - `src/syscall/file.rs:L884-L888`：关键词命中
    代码片段：`fn device_id_for_path(path: &[u8]) -> u64 { if path == b"/proc" || path.starts_with(b"/proc/") { 2 } else {`
- 与 2022 Maturin 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/mod.rs:L601-L605`：关键词命中
    代码片段：`// ---- SysV semaphores (semget / semop / semctl) ---- // A small global semaphore-set registry, sibling to the SysV-shm one above. Sets live // in kernel memory keyed by a 1-ba...`
  - `src/syscall/storage.rs:L195-L199`：关键词命中
    代码片段：`#[cfg(test)] static RUNTIME_STORAGE_POOL: std::sync::Mutex<RuntimeStoragePool> = std::sync::Mutex::new(RuntimeStoragePool::new());`
- 与 2022 Maturin 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall/io.rs:L2-L6`：关键词命中
    代码片段：`//! and vectored ('readv'/'writev'/'preadv'/'pwritev' + v2) variants. //! //! Extracted handler domain (descendant of 'syscall'); reaches SyscallContext //! internals and shared...`
  - `src/syscall/mod.rs:L1379-L1383`：关键词命中
    代码片段：`pub ppid: usize, pub state: ProcessState, // The fields below stay private to the 'syscall' module. Handler domains // split into child modules (e.g. 'syscall::memory') are desc...`
- 与 2022 Maturin 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2022 Maturin 的语言构成不同：待测作品为 {'build': 267, 'markdown': 2266, 'asm': 662, 'toml': 12, 'rust': 42750}，历史样本为 {'json': 30, 'build': 508, 'markdown': 1713, 'toml': 9, 'yaml': 18, 'text': 394, 'rust': 27639, 'c': 9309, 'make': 29, 'asm': 177}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：19
- 含证据关键结论数：19（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
