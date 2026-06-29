# OSKernel2024-HFUT666 比较报告

- 对比历史仓库：2022 啊队队队
- 生成时间：2026-06-29T14:10:07.362110+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2022 啊队队队（来源：赛事历史作品）：画像相似度 score=6.22；语言构成相似度 0.61; OS 维度重合度 1.00; 代码规模接近度 1.00

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2022 啊队队队 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/drivers/mod.rs:L4-L8`：关键词命中
    代码片段：`//! //! 目前支持: //! - qemu virtio block 设备。 //! - 引入了 K210 SD 卡驱动, 未经测试。 pub mod block;`
  - `src/drivers/block/mod.rs:L7-L11`：关键词命中
    代码片段：`pub mod sdcard; pub mod virtio_block; #[cfg(feature = "qemu")]`
  - `kernel/src/console.rs:L8-L12`：关键词命中
    代码片段：`macro_rules! print { ($fmt: literal $(, $($arg: tt)+)?) => { $crate::console::print(format_args!($fmt $(, $($arg)+)?)); } }`
  - `kernel/src/device/mod.rs:L9-L13`：关键词命中
    代码片段：`use fatfs::LossyOemCpConverter; use fatfs::NullTimeProvider; use virtio_drivers::VirtIOBlk; use virtio_drivers::VirtIOHeader; use crate::sync::mutex::Mutex;`
- 与 2022 啊队队队 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L1-L5`：关键词命中
    代码片段：`use crate::mm::page_table::UserBuffer; pub mod inode; pub mod stdio;`
  - `src/fs/inode.rs:L1-L3`：关键词命中
    代码片段：`//! 操作系统 Inode (文件) 结构 //! //! 一个文件在操作系统中对应一个 Inode 结构，用于管理文件的读写操作`
  - `fatfs/src/fs.rs:L22-L26`：关键词命中
    代码片段：`use crate::time::{DefaultTimeProvider, TimeProvider}; // FAT implementation based on: //   http://wiki.osdev.org/FAT //   https://www.win.tue.nl/~aeb/linux/fs/fat/fat-1.html`
  - `kernel/src/fs/file.rs:L11-L15`：关键词命中
    代码片段：`use crate::memory::page_table::{PageMappingManager, PTEFlags}; use super::filetree::INode; #[allow(unused)]`
- 与 2022 啊队队队 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/trap/init.rs:L7-L11`：关键词命中
    代码片段：`use super::handler::trap_from_kernel; global_asm!(include_str!("trap.asm")); /// 初始化陷入`
  - `src/trap/handler.rs:L5-L9`：关键词命中
    代码片段：`use common::syscall::Syscall; use riscv::{ interrupt::{Exception, supervisor::Interrupt}, register::{ scause, stval,`
  - `kernel/src/interrupt/mod.rs:L1-L3`：关键词命中
    代码片段：`pub mod timer; use core::arch::global_asm;`
  - `kernel/src/main.rs:L13-L17`：关键词命中
    代码片段：`mod console; mod device; pub mod interrupt; mod memory; mod fs;`
- 与 2022 啊队队队 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mm/mod.rs:L2-L6`：关键词命中
    代码片段：`pub mod address; pub mod frame_allocator; pub mod heap_allocator; pub mod init;`
  - `src/mm/init.rs:L3-L7`：关键词命中
    代码片段：`use crate::trace; use super::{KERNEL_SPACE, frame_allocator, heap_allocator}; /// 记录内核堆是否已初始化`
  - `kernel/src/memory/mod.rs:L4-L8`：关键词命中
    代码片段：`pub mod page; pub mod addr; pub mod page_table; pub mod mem_map; pub mod mem_set;`
  - `kernel/src/memory/heap.rs:L3-L7`：关键词命中
    代码片段：`// 堆大小 const HEAP_SIZE: usize = 0x0008_0000; // 堆空间`
- 与 2022 啊队队队 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/task/mod.rs:L7-L11`：关键词命中
    代码片段：`use lazy_static::lazy_static; use manager::TaskManager; use task::ProcessControlBlock; use crate::{fs::inode::open_file, utils::safety::SyncRefCell};`
  - `src/task/manager.rs:L9-L13`：关键词命中
    代码片段：`use lazy_static::lazy_static; use crate::task::context::TaskCtx; use crate::task::task::{ProcessControlBlock, ProcessStatus}; use crate::utils::safety::SyncRefCell;`
  - `kernel/src/task/mod.rs:L14-L18`：关键词命中
    代码片段：`use crate::memory::page::alloc_more; use crate::runtime_err::RuntimeError; use crate::task::process::Process; use crate::task::task_scheduler::start_tasks; use crate::memory::pa...`
  - `kernel/src/task/task.rs:L4-L8`：关键词命中
    代码片段：`use crate::memory::addr::UserAddr; use crate::interrupt::Context; use crate::task::task_scheduler::kill_task; use super::process::Process;`
- 与 2022 啊队队队 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/fs/inode.rs:L6-L10`：关键词命中
    代码片段：`use lazy_static::lazy_static; use ros_fs::{fs::FileSystemRootInode, layout::disk_inode::InodeType, virt_fs::MemInode}; use spin::Mutex; use crate::{drivers::block::BLOCK_DEVICE,...`
  - `ros-fs/src/fs.rs:L3-L7`：关键词命中
    代码片段：`//! 建立在物理磁盘块设备上的文件系统，提供了文件系统的底层基本操作，包括创建文件系统、打开文件系统、分配 inode、分配数据块等。 use alloc::sync::Arc; use spin::Mutex; use crate::{`
  - `kernel/src/sync/mod.rs:L1-L1`：关键词命中
    代码片段：`pub mod mutex;`
  - `kernel/src/sync/mutex.rs:L1-L3`：关键词命中
    代码片段：`use core::sync::atomic::{AtomicBool, Ordering}; use core::cell::UnsafeCell; use core::marker::Sync;`
- 与 2022 啊队队队 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
    代码片段：`use alloc::{sync::Arc, vec::Vec}; use common::syscall::{ OpenFlags, Syscall, SyscallArgs, SyscallRet, time::{TimeVal, TimeZone},`
  - `common/src/syscall.rs:L9-L13`：关键词命中
    代码片段：`/// https://gpages.juszkiewicz.com.pl/syscalls-table/syscalls.html #[derive(Debug, Copy, Clone, PartialEq, Eq)] pub enum Syscall { /// 打开文件 ///`
  - `kernel/src/sbi.rs:L19-L23`：关键词命中
    代码片段：`let mut ret; unsafe { asm!("ecall", in("a7") which, inlateout("a0") arg0 as i32 => ret,`
  - `device/src/sbi.rs:L19-L23`：关键词命中
    代码片段：`let mut ret; unsafe { asm!("ecall", in("a7") which, inlateout("a0") arg0 as i32 => ret,`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 函数/符号名重合：与 2022 啊队队队 在“设备驱动”维度发现 4 个同名定义：new, CS_HIGH, CS_LOW, HIGH_SPEED_ENABLE。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/drivers/block/sdcard.rs:L211-L211`：fn new
    代码片段：`pub fn new(`
  - `kernel/src/device/sdcard.rs:L164-L164`：fn new
    代码片段：`pub fn new(`
  - `src/drivers/block/sdcard.rs:L227-L227`：fn CS_HIGH
    代码片段：`fn CS_HIGH(&self) {`
  - `kernel/src/device/sdcard.rs:L180-L180`：fn CS_HIGH
    代码片段：`fn CS_HIGH(&self) {`
- 函数/符号名重合：与 2022 啊队队队 在“文件系统”维度发现 4 个同名定义：new, read, write, readable。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/inode.rs:L40-L40`：fn new
    代码片段：`pub fn new(readable: bool, writable: bool, inode: Arc<MemInode>) -> Self {`
  - `kernel/src/fs/file.rs:L92-L92`：fn new
    代码片段：`pub fn new(inode: Rc<INode>) -> Result<Rc<Self>, RuntimeError>{`
  - `src/fs/inode.rs:L68-L68`：fn read
    代码片段：`fn read(&self, mut buf: UserBuffer) -> usize {`
  - `kernel/src/fs/filetree.rs:L213-L213`：fn read
    代码片段：`pub fn read(&self) -> Result<Vec<u8>, RuntimeError>{`
- 函数/符号名重合：与 2022 啊队队队 在“内存管理”维度发现 4 个同名定义：from, add, page_offset, new。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/mm/address.rs:L94-L94`：fn from
    代码片段：`fn from(address: usize) -> Self {`
  - `kernel/src/memory/addr.rs:L27-L27`：fn from
    代码片段：`fn from(addr: usize) -> Self {`
  - `src/mm/address.rs:L196-L196`：fn add
    代码片段：`fn add(self, rhs: Self) -> Self {`
  - `kernel/src/memory/addr.rs:L178-L178`：fn add
    代码片段：`fn add(self, rhs: Self) -> Self::Output {`
- 函数/符号名重合：与 2022 啊队队队 在“同步机制”维度发现 4 个同名定义：read_block, write_block, lock, drop。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/drivers/block/sdcard.rs:L796-L796`：fn read_block
    代码片段：`fn read_block(&self, block_id: usize, buf: &mut [u8]) {`
  - `kernel/src/device/block.rs:L8-L8`：fn read_block
    代码片段：`fn read_block(&mut self, sector_offset: usize, buf: &mut [u8]) {`
  - `src/drivers/block/sdcard.rs:L802-L802`：fn write_block
    代码片段：`fn write_block(&self, block_id: usize, buf: &[u8]) {`
  - `kernel/src/device/block.rs:L12-L12`：fn write_block
    代码片段：`fn write_block(&mut self, sector_offset: usize, buf: &mut [u8]) {`
- 结构体/类型重合：与 2022 啊队队队 在“设备驱动”维度发现 4 个同名定义：SDCard, CMD, InitError, SDCardCSD。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/drivers/block/sdcard.rs:L69-L69`：struct SDCard
    代码片段：`pub struct SDCard<SPI> {`
  - `kernel/src/device/sdcard.rs:L22-L22`：struct SDCard
    代码片段：`pub struct SDCard<SPI> {`
  - `src/drivers/block/sdcard.rs:L97-L97`：enum CMD
    代码片段：`pub enum CMD {`
  - `kernel/src/device/sdcard.rs:L50-L50`：enum CMD
    代码片段：`pub enum CMD {`
- 结构体/类型重合：与 2022 啊队队队 在“文件系统”维度发现 3 个同名定义：File, Stdin, Stdout。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/mod.rs:L11-L11`：trait File
    代码片段：`pub trait File: Send + Sync {`
  - `kernel/src/fs/file.rs:L79-L79`：struct File
    代码片段：`pub struct File(pub RefCell<FileInner>);`
  - `src/fs/stdio.rs:L7-L7`：struct Stdin
    代码片段：`pub struct Stdin;`
  - `kernel/src/fs/stdio.rs:L4-L4`：struct StdIn
    代码片段：`pub struct StdIn;`
- 函数/符号名重合：与 2022 啊队队队 在“中断与异常”维度发现 2 个同名定义：get_time_us, set_next_timeout。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/timer.rs:L19-L19`：fn get_time_us
    代码片段：`pub fn get_time_us() -> usize {`
  - `kernel/src/interrupt/timer.rs:L78-L78`：fn get_time_us
    代码片段：`pub fn get_time_us() -> usize {`
  - `src/timer.rs:L24-L24`：fn set_next_timeout
    代码片段：`pub fn set_next_timeout(timeout_us: usize) {`
  - `kernel/src/interrupt/timer.rs:L123-L123`：fn set_next_timeout
    代码片段：`fn set_next_timeout() {`
- 函数/符号名重合：与 2022 啊队队队 在“调度与任务管理”维度发现 2 个同名定义：new, alloc。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/task/manager.rs:L35-L35`：fn new
    代码片段：`pub fn new() -> Self {`
  - `kernel/src/task/fd_table.rs:L24-L24`：fn new
    代码片段：`pub fn new(file: Rc<dyn FileOP>) -> Self {`
  - `src/task/pid.rs:L42-L42`：fn alloc
    代码片段：`fn alloc(&mut self) -> Option<PidHandler> {`
  - `kernel/src/task/fd_table.rs:L113-L113`：fn alloc
    代码片段：`pub fn alloc(&mut self) -> usize {`
- 结构体/类型重合：与 2022 啊队队队 在“内存管理”维度发现 2 个同名定义：PTEFlags, PageTableEntry。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/mm/page_table.rs:L138-L138`：struct PTEFlags
    代码片段：`pub struct PTEFlags: u8 {`
  - `kernel/src/memory/page_table.rs:L22-L22`：struct PTEFlags
    代码片段：`pub struct PTEFlags: u8 {`
  - `src/mm/page_table.rs:L168-L168`：struct PageTableEntry
    代码片段：`pub struct PageTableEntry {`
  - `kernel/src/memory/page_table.rs:L41-L41`：struct PageTableEntry
    代码片段：`pub struct PageTableEntry {`
- 结构体/类型重合：与 2022 啊队队队 在“同步机制”维度发现 2 个同名定义：VirtIOBlock, BlockDevice。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/drivers/block/virtio_block.rs:L38-L38`：struct VirtIOBlock
    代码片段：`pub struct VirtIOBlock(Mutex<VirtIOBlk<HalImpl, MmioTransport>>);`
  - `kernel/src/device/block.rs:L5-L5`：struct VirtIOBlock
    代码片段：`pub struct VirtIOBlock(pub VirtIOBlk<'static>);`
  - `ros-fs/src/block_dev.rs:L11-L11`：trait BlockDevice
    代码片段：`pub trait BlockDevice: Send + Sync + Any {`
  - `kernel/src/device/mod.rs:L42-L42`：trait BlockDevice
    代码片段：`pub trait BlockDevice {`
- 文件路径重合：与 2022 啊队队队 在“文件系统”维度出现同名文件源码路径 `ros-fs/src/fs.rs` / `fatfs/src/fs.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `ros-fs/src/fs.rs:L1-L5`：关键词命中
    代码片段：`//! 物理文件系统 //! //! 建立在物理磁盘块设备上的文件系统，提供了文件系统的底层基本操作，包括创建文件系统、打开文件系统、分配 inode、分配数据块等。 use alloc::sync::Arc; use spin::Mutex;`
  - `fatfs/src/fs.rs:L22-L26`：关键词命中
    代码片段：`use crate::time::{DefaultTimeProvider, TimeProvider}; // FAT implementation based on: //   http://wiki.osdev.org/FAT //   https://www.win.tue.nl/~aeb/linux/fs/fat/fat-1.html`

## 相似点

- 与 2022 啊队队队 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/mod.rs:L4-L8`：关键词命中
    代码片段：`//! //! 目前支持: //! - qemu virtio block 设备。 //! - 引入了 K210 SD 卡驱动, 未经测试。 pub mod block;`
  - `src/drivers/block/mod.rs:L7-L11`：关键词命中
    代码片段：`pub mod sdcard; pub mod virtio_block; #[cfg(feature = "qemu")]`
- 与 2022 啊队队队 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L1-L5`：关键词命中
    代码片段：`use crate::mm::page_table::UserBuffer; pub mod inode; pub mod stdio;`
  - `src/fs/inode.rs:L1-L3`：关键词命中
    代码片段：`//! 操作系统 Inode (文件) 结构 //! //! 一个文件在操作系统中对应一个 Inode 结构，用于管理文件的读写操作`
- 与 2022 啊队队队 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/trap/init.rs:L7-L11`：关键词命中
    代码片段：`use super::handler::trap_from_kernel; global_asm!(include_str!("trap.asm")); /// 初始化陷入`
  - `src/trap/handler.rs:L5-L9`：关键词命中
    代码片段：`use common::syscall::Syscall; use riscv::{ interrupt::{Exception, supervisor::Interrupt}, register::{ scause, stval,`
- 与 2022 啊队队队 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mm/mod.rs:L2-L6`：关键词命中
    代码片段：`pub mod address; pub mod frame_allocator; pub mod heap_allocator; pub mod init;`
  - `src/mm/init.rs:L3-L7`：关键词命中
    代码片段：`use crate::trace; use super::{KERNEL_SPACE, frame_allocator, heap_allocator}; /// 记录内核堆是否已初始化`
- 与 2022 啊队队队 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/task/mod.rs:L7-L11`：关键词命中
    代码片段：`use lazy_static::lazy_static; use manager::TaskManager; use task::ProcessControlBlock; use crate::{fs::inode::open_file, utils::safety::SyncRefCell};`
  - `src/task/manager.rs:L9-L13`：关键词命中
    代码片段：`use lazy_static::lazy_static; use crate::task::context::TaskCtx; use crate::task::task::{ProcessControlBlock, ProcessStatus}; use crate::utils::safety::SyncRefCell;`
- 与 2022 啊队队队 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/inode.rs:L6-L10`：关键词命中
    代码片段：`use lazy_static::lazy_static; use ros_fs::{fs::FileSystemRootInode, layout::disk_inode::InodeType, virt_fs::MemInode}; use spin::Mutex; use crate::{drivers::block::BLOCK_DEVICE,...`
  - `ros-fs/src/fs.rs:L3-L7`：关键词命中
    代码片段：`//! 建立在物理磁盘块设备上的文件系统，提供了文件系统的底层基本操作，包括创建文件系统、打开文件系统、分配 inode、分配数据块等。 use alloc::sync::Arc; use spin::Mutex; use crate::{`
- 与 2022 啊队队队 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
    代码片段：`use alloc::{sync::Arc, vec::Vec}; use common::syscall::{ OpenFlags, Syscall, SyscallArgs, SyscallRet, time::{TimeVal, TimeZone},`
  - `common/src/syscall.rs:L9-L13`：关键词命中
    代码片段：`/// https://gpages.juszkiewicz.com.pl/syscalls-table/syscalls.html #[derive(Debug, Copy, Clone, PartialEq, Eq)] pub enum Syscall { /// 打开文件 ///`
- 与 2022 啊队队队 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2022 啊队队队 的语言构成不同：待测作品为 {'json': 18, 'build': 419, 'markdown': 6579, 'toml': 7, 'asm': 156, 'rust': 8127}，历史样本为 {'yaml': 19, 'json': 20, 'build': 91, 'markdown': 995, 'text': 19, 'toml': 2, 'rust': 13878, 'asm': 227}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：25
- 含证据关键结论数：25（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
