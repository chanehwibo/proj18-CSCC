# OSKernel2024-HFUT666 比较报告

- 对比历史仓库：2025 只编译了一次
- 生成时间：2026-06-28T12:14:44.820388+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2025 只编译了一次（来源：赛事历史作品）：画像相似度 score=6.40；语言构成相似度 0.80; OS 维度重合度 1.00; 代码规模接近度 0.79

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2025 只编译了一次 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/drivers/mod.rs:L4-L8`：关键词命中
    代码片段：`//! //! 目前支持: //! - qemu virtio block 设备。 //! - 引入了 K210 SD 卡驱动, 未经测试。 pub mod block;`
  - `src/drivers/block/mod.rs:L7-L11`：关键词命中
    代码片段：`pub mod sdcard; pub mod virtio_block; #[cfg(feature = "qemu")]`
  - `os/src/console.rs:L74-L78`：关键词命中
    代码片段：`macro_rules! print { ($fmt: literal $(, $($arg: tt)+)?) => { $crate::console::print(format_args!($fmt $(, $($arg)+)?)) } }`
  - `os/src/drivers/mod.rs:L1-L4`：关键词命中
    代码片段：`mod block; pub mod serial; pub use block::block_dev::BlockDevice;`
- 与 2025 只编译了一次 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L1-L5`：关键词命中
    代码片段：`use crate::mm::page_table::UserBuffer; pub mod inode; pub mod stdio;`
  - `src/fs/inode.rs:L1-L3`：关键词命中
    代码片段：`//! 操作系统 Inode (文件) 结构 //! //! 一个文件在操作系统中对应一个 Inode 结构，用于管理文件的读写操作`
  - `os/src/fs/mod.rs:L2-L6`：关键词命中
    代码片段：`mod fat32; mod file; pub(crate) mod inode; mod pipe; mod stdio;`
  - `os/src/fs/file.rs:L1-L3`：关键词命中
    代码片段：`use crate::fs::inode::{FatType, OSInode}; use crate::mm::UserBuffer; use alloc::string::String;`
- 与 2025 只编译了一次 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/trap/init.rs:L7-L11`：关键词命中
    代码片段：`use super::handler::trap_from_kernel; global_asm!(include_str!("trap.asm")); /// 初始化陷入`
  - `src/trap/handler.rs:L5-L9`：关键词命中
    代码片段：`use common::syscall::Syscall; use riscv::{ interrupt::{Exception, supervisor::Interrupt}, register::{ scause, stval,`
  - `os/src/timer.rs:L72-L76`：关键词命中
    代码片段：`let current_ms = get_time_ms(); TIMERS.exclusive_session(|timers| { while let Some(timer) = timers.peek() { if timer.expire_ms <= current_ms { wakeup_task(Arc::clone(&timer.task));`
  - `os/src/hal/arch/riscv/trap/mod.rs:L1-L3`：关键词命中
    代码片段：`//! 陷阱（Trap）处理模块。 //! //! 本模块负责处理所有 CPU 异常（Exceptions）和中断（Interrupts）。`
- 与 2025 只编译了一次 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mm/mod.rs:L2-L6`：关键词命中
    代码片段：`pub mod address; pub mod frame_allocator; pub mod heap_allocator; pub mod init;`
  - `src/mm/init.rs:L3-L7`：关键词命中
    代码片段：`use crate::trace; use super::{KERNEL_SPACE, frame_allocator, heap_allocator}; /// 记录内核堆是否已初始化`
  - `os/src/mm/mod.rs:L1-L4`：关键词命中
    代码片段：`pub mod address; mod frame_allocator; mod heap_allocator; mod memory_set;`
  - `os/src/mm/address.rs:L1-L3`：关键词命中
    代码片段：`//! 虚拟/物理地址与页号模块（SV39） //! //! # Overview`
- 与 2025 只编译了一次 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/task/mod.rs:L7-L11`：关键词命中
    代码片段：`use lazy_static::lazy_static; use manager::TaskManager; use task::ProcessControlBlock; use crate::{fs::inode::open_file, utils::safety::SyncRefCell};`
  - `src/task/manager.rs:L9-L13`：关键词命中
    代码片段：`use lazy_static::lazy_static; use crate::task::context::TaskCtx; use crate::task::task::{ProcessControlBlock, ProcessStatus}; use crate::utils::safety::SyncRefCell;`
  - `os/src/task/mod.rs:L13-L17`：关键词命中
    代码片段：`//! - 所有对 PCB/TCB 内部的可变访问通过 'UPIntrFreeCell' 或 'UPIntrRefMut' 独占访问，避免数据竞争 //! - 用户资源（ustack、trap_cx、tid）在主线程退出前被正确释放，防止内存泄漏 //! - 'schedule' 必须提供有效 'TaskContext' 指针，否则会导致上下文切换错误...`
  - `os/src/task/task.rs:L44-L48`：关键词命中
    代码片段：`use crate::mm::{MapPermission, PhysPageNum, VirtAddr}; use crate::sync::{UPIntrFreeCell, UPIntrRefMut}; use crate::task::context::TaskContext; use crate::task::process::ProcessC...`
- 与 2025 只编译了一次 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/fs/inode.rs:L6-L10`：关键词命中
    代码片段：`use lazy_static::lazy_static; use ros_fs::{fs::FileSystemRootInode, layout::disk_inode::InodeType, virt_fs::MemInode}; use spin::Mutex; use crate::{drivers::block::BLOCK_DEVICE,...`
  - `ros-fs/src/fs.rs:L3-L7`：关键词命中
    代码片段：`//! 建立在物理磁盘块设备上的文件系统，提供了文件系统的底层基本操作，包括创建文件系统、打开文件系统、分配 inode、分配数据块等。 use alloc::sync::Arc; use spin::Mutex; use crate::{`
  - `os/src/sync/mod.rs:L7-L11`：关键词命中
    代码片段：`//! //! 模块内部按功能拆分为多个子模块： //! - 'mutex'：互斥锁抽象及其具体实现（自旋 / 阻塞） //! - 'semaphore'：计数型信号量 //! - 'condvar'：条件变量`
  - `os/src/sync/mutex.rs:L1-L3`：关键词命中
    代码片段：`//! # 互斥锁（Mutex）同步原语模块 //! //! ## Overview`
- 与 2025 只编译了一次 在“系统调用”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
    代码片段：`use alloc::{sync::Arc, vec::Vec}; use common::syscall::{ OpenFlags, Syscall, SyscallArgs, SyscallRet, time::{TimeVal, TimeZone},`
  - `common/src/syscall.rs:L9-L13`：关键词命中
    代码片段：`/// https://gpages.juszkiewicz.com.pl/syscalls-table/syscalls.html #[derive(Debug, Copy, Clone, PartialEq, Eq)] pub enum Syscall { /// 打开文件 ///`
  - `os/src/syscall/mod.rs:L41-L45`：关键词命中
    代码片段：`pub use process::*; pub fn syscall(syscall_id: usize, args: [usize; 6]) -> isize { match syscall_id { //SYSCALL_OPEN => sys_openat(args[0] as *const u8, args[1] as u32),`
  - `os/src/hal/arch/riscv/sbi.rs:L5-L9`：关键词命中
    代码片段：`//! //! # Design //! - 所有 SBI 调用通过 'ecall' 指令触发陷入 S 模式执行。 //! - 'sbi_call' 函数是通用封装，将函数号和参数传递给 SBI。 //! - 上层函数（如 'set_timer'、'console_putchar'）直接调用 'sbi_call'，简化内核接口。`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 与 2025 只编译了一次 在“内存管理”维度发现片段级代码相似度 0.81 （token=0.71, structure=1.00）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：fn, heap_allocator, init, init_heap, pub。（置信度：high）
  证据：
  - `src/mm/init.rs:L13-L17`：fn init
    代码片段：`// 初始化内核内存管理 pub fn init() { trace!("[Kernel] Init heap allocator"); heap_allocator::init_heap();`
  - `os/src/mm/mod.rs:L7-L11`：fn init
    代码片段：`/// 初始化内存管理子系统 /// 包括堆内存分配器、物理页帧分配器和内核虚拟地址空间的建立与激活 pub fn init() { heap_allocator::init_heap(); frame_allocator::init_frame_allocator();`
- 函数/符号名重合：与 2025 只编译了一次 在“文件系统”维度发现 4 个同名定义：new, read_all, read, write。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/inode.rs:L40-L40`：fn new
    代码片段：`pub fn new(readable: bool, writable: bool, inode: Arc<MemInode>) -> Self {`
  - `os/src/fs/block_cache.rs:L68-L68`：fn new
    代码片段：`pub fn new() -> Self {`
  - `src/fs/inode.rs:L49-L49`：fn read_all
    代码片段：`pub fn read_all(&self) -> Vec<u8> {`
  - `os/src/fs/inode.rs:L90-L90`：fn read_all
    代码片段：`pub fn read_all(&self) -> Vec<u8> {`
- 与 2025 只编译了一次 在“文件系统”维度发现片段级代码相似度 0.69 （token=0.62, structure=0.80）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：bool, buf, fn, readable, self, userbuffer, usize, write。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L25-L29`：fn write
    代码片段：`/// ## 返回 /// 写入的字节数 fn write(&self, buf: UserBuffer) -> usize; /// 根据打开文件的模式判断是否可读 fn readable(&self) -> bool;`
  - `os/src/fs/file.rs:L8-L12`：fn writable
    代码片段：`pub trait File: Send + Sync { fn readable(&self) -> bool; fn writable(&self) -> bool; fn read(&self, buf: UserBuffer) -> usize; fn write(&self, buf: UserBuffer) -> usize;`
- 与 2025 只编译了一次 在“文件系统”维度发现片段级代码相似度 0.66 （token=0.58, structure=0.80）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：bool, buf, fn, readable, self, userbuffer, usize。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L25-L29`：fn write
    代码片段：`/// ## 返回 /// 写入的字节数 fn write(&self, buf: UserBuffer) -> usize; /// 根据打开文件的模式判断是否可读 fn readable(&self) -> bool;`
  - `os/src/fs/file.rs:L7-L11`：fn readable
    代码片段：`pub trait File: Send + Sync { fn readable(&self) -> bool; fn writable(&self) -> bool; fn read(&self, buf: UserBuffer) -> usize;`
- 函数/符号名重合：与 2025 只编译了一次 在“内存管理”维度发现 4 个同名定义：get_mut, get_ref, get_pte_array, get_bytes_array。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/mm/address.rs:L43-L43`：fn get_mut
    代码片段：`pub fn get_mut<T>(&self) -> &'static mut T {`
  - `os/src/mm/address.rs:L174-L174`：fn get_mut
    代码片段：`pub fn get_mut<T>(&self) -> &'static mut T {`
  - `src/mm/address.rs:L51-L51`：fn get_ref
    代码片段：`pub fn get_ref<T>(&self) -> &'static T {`
  - `os/src/mm/address.rs:L170-L170`：fn get_ref
    代码片段：`pub fn get_ref<T>(&self) -> &'static T {`
- 函数/符号名重合：与 2025 只编译了一次 在“同步机制”维度发现 4 个同名定义：new, read, sync, drop。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/inode.rs:L40-L40`：fn new
    代码片段：`pub fn new(readable: bool, writable: bool, inode: Arc<MemInode>) -> Self {`
  - `os/src/fs/block_cache.rs:L68-L68`：fn new
    代码片段：`pub fn new() -> Self {`
  - `src/fs/inode.rs:L68-L68`：fn read
    代码片段：`fn read(&self, mut buf: UserBuffer) -> usize {`
  - `os/src/fs/block_cache.rs:L193-L193`：fn read
    代码片段：`pub fn read<T, V>(&self, offset: usize, f: impl FnOnce(&T) -> V) -> V {`
- 函数/符号名重合：与 2025 只编译了一次 在“系统调用”维度发现 4 个同名定义：syscall, sys_close, sys_read, sys_write。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/syscall.rs:L23-L23`：fn syscall
    代码片段：`pub fn syscall(call: Syscall, args: SyscallArgs) -> SyscallRet {`
  - `user/src/syscall.rs:L27-L27`：fn syscall
    代码片段：`fn syscall(id: usize, args: [usize; 6]) -> isize {`
  - `src/syscall.rs:L65-L65`：fn sys_close
    代码片段：`pub fn sys_close(fd: usize) -> SyscallRet {`
  - `user/src/syscall.rs:L70-L70`：fn sys_close
    代码片段：`pub fn sys_close(fd: usize) -> isize {`
- 与 2025 只编译了一次 在“系统调用”维度发现片段级代码相似度 0.62 （token=0.50, structure=0.83）。这属于代码级相似线索，不等同于抄袭结论，需要人工结合完整文件和提交历史复核。 共同 token：const, current_user_token, fn, let, path, pub, u8。（置信度：medium）
  证据：
  - `src/syscall.rs:L49-L53`：fn sys_openat
    代码片段：`/// [Syscall::OpenAt] pub fn sys_openat(path: *const u8, flags: usize) -> SyscallRet { let current = Processor::get_current().unwrap(); let path = get_translated_string(Processo...`
  - `os/src/syscall/fs.rs:L41-L45`：fn sys_chdir
    代码片段：`// cwd_inode更新逻辑，如果能打不开文件就崩溃，初始化为根目录 pub fn sys_chdir(path: *const u8) -> isize { let token = current_user_token(); let path = translated_str(token, path);`
- 函数/符号名重合：与 2025 只编译了一次 在“设备驱动”维度发现 1 个同名定义：new。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/drivers/block/sdcard.rs:L211-L211`：fn new
    代码片段：`pub fn new(`
  - `os/src/fs/block_cache.rs:L140-L140`：fn new
    代码片段：`pub fn new(block_id: usize, block_device: Arc<dyn BlockDevice>) -> Self {`
- 结构体/类型重合：与 2025 只编译了一次 在“文件系统”维度发现 4 个同名定义：OSInode, File, Stdin, Stdout。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/inode.rs:L27-L27`：struct OSInode
    代码片段：`pub struct OSInode {`
  - `os/src/fs/inode.rs:L20-L20`：struct OSInode
    代码片段：`pub struct OSInode {`
  - `src/fs/mod.rs:L11-L11`：trait File
    代码片段：`pub trait File: Send + Sync {`
  - `os/src/fs/file.rs:L8-L8`：trait File
    代码片段：`pub trait File: Send + Sync {`
- 函数/符号名重合：与 2025 只编译了一次 在“中断与异常”维度发现 1 个同名定义：get_time_us。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：medium）
  证据：
  - `src/timer.rs:L19-L19`：fn get_time_us
    代码片段：`pub fn get_time_us() -> usize {`
  - `os/src/timer.rs:L28-L28`：fn get_time_us
    代码片段：`pub fn get_time_us() -> usize {`
- 结构体/类型重合：与 2025 只编译了一次 在“同步机制”维度发现 3 个同名定义：File, BlockCacheManager, BlockCache。该结果表示命名和局部结构存在可复核相似线索，不直接表示代码复制。（置信度：high）
  证据：
  - `src/fs/mod.rs:L11-L11`：trait File
    代码片段：`pub trait File: Send + Sync {`
  - `os/src/fs/file.rs:L8-L8`：trait File
    代码片段：`pub trait File: Send + Sync {`
  - `ros-fs/src/block_cache.rs:L18-L18`：struct BlockCacheManager
    代码片段：`pub struct BlockCacheManager {`
  - `os/src/fs/block_cache.rs:L235-L235`：struct BlockCacheManager
    代码片段：`pub struct BlockCacheManager {`
- 文件路径重合：与 2025 只编译了一次 在“内存管理”维度出现同名文件源码路径 `src/mm/address.rs` / `os/src/mm/address.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `src/mm/address.rs:L2-L6`：关键词命中
    代码片段：`use core::ops::Add; use super::page_table::PageTableEntry; /// 页内偏移位数`
  - `os/src/mm/address.rs:L1-L3`：关键词命中
    代码片段：`//! 虚拟/物理地址与页号模块（SV39） //! //! # Overview`
- 文件路径重合：与 2025 只编译了一次 在“系统调用”维度出现同名文件源码路径 `src/syscall.rs` / `user/src/syscall.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
    代码片段：`use alloc::{sync::Arc, vec::Vec}; use common::syscall::{ OpenFlags, Syscall, SyscallArgs, SyscallRet, time::{TimeVal, TimeZone},`
  - `user/src/syscall.rs:L25-L29`：关键词命中
    代码片段：`#[cfg(feature = "riscv")] fn syscall(id: usize, args: [usize; 6]) -> isize { let mut ret: isize; unsafe {`
- 文件路径重合：与 2025 只编译了一次 在“系统调用”维度出现同名文件源码路径 `common/src/syscall.rs` / `user/src/syscall.rs`。这说明实现位置或文件命名存在可复核相似线索，不等同于代码重复裁定。（置信度：medium）
  证据：
  - `common/src/syscall.rs:L9-L13`：关键词命中
    代码片段：`/// https://gpages.juszkiewicz.com.pl/syscalls-table/syscalls.html #[derive(Debug, Copy, Clone, PartialEq, Eq)] pub enum Syscall { /// 打开文件 ///`
  - `user/src/syscall.rs:L25-L29`：关键词命中
    代码片段：`#[cfg(feature = "riscv")] fn syscall(id: usize, args: [usize; 6]) -> isize { let mut ret: isize; unsafe {`

## 相似点

- 与 2025 只编译了一次 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/mod.rs:L4-L8`：关键词命中
    代码片段：`//! //! 目前支持: //! - qemu virtio block 设备。 //! - 引入了 K210 SD 卡驱动, 未经测试。 pub mod block;`
  - `src/drivers/block/mod.rs:L7-L11`：关键词命中
    代码片段：`pub mod sdcard; pub mod virtio_block; #[cfg(feature = "qemu")]`
- 与 2025 只编译了一次 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/mod.rs:L1-L5`：关键词命中
    代码片段：`use crate::mm::page_table::UserBuffer; pub mod inode; pub mod stdio;`
  - `src/fs/inode.rs:L1-L3`：关键词命中
    代码片段：`//! 操作系统 Inode (文件) 结构 //! //! 一个文件在操作系统中对应一个 Inode 结构，用于管理文件的读写操作`
- 与 2025 只编译了一次 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/trap/init.rs:L7-L11`：关键词命中
    代码片段：`use super::handler::trap_from_kernel; global_asm!(include_str!("trap.asm")); /// 初始化陷入`
  - `src/trap/handler.rs:L5-L9`：关键词命中
    代码片段：`use common::syscall::Syscall; use riscv::{ interrupt::{Exception, supervisor::Interrupt}, register::{ scause, stval,`
- 与 2025 只编译了一次 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mm/mod.rs:L2-L6`：关键词命中
    代码片段：`pub mod address; pub mod frame_allocator; pub mod heap_allocator; pub mod init;`
  - `src/mm/init.rs:L3-L7`：关键词命中
    代码片段：`use crate::trace; use super::{KERNEL_SPACE, frame_allocator, heap_allocator}; /// 记录内核堆是否已初始化`
- 与 2025 只编译了一次 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/task/mod.rs:L7-L11`：关键词命中
    代码片段：`use lazy_static::lazy_static; use manager::TaskManager; use task::ProcessControlBlock; use crate::{fs::inode::open_file, utils::safety::SyncRefCell};`
  - `src/task/manager.rs:L9-L13`：关键词命中
    代码片段：`use lazy_static::lazy_static; use crate::task::context::TaskCtx; use crate::task::task::{ProcessControlBlock, ProcessStatus}; use crate::utils::safety::SyncRefCell;`
- 与 2025 只编译了一次 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/fs/inode.rs:L6-L10`：关键词命中
    代码片段：`use lazy_static::lazy_static; use ros_fs::{fs::FileSystemRootInode, layout::disk_inode::InodeType, virt_fs::MemInode}; use spin::Mutex; use crate::{drivers::block::BLOCK_DEVICE,...`
  - `ros-fs/src/fs.rs:L3-L7`：关键词命中
    代码片段：`//! 建立在物理磁盘块设备上的文件系统，提供了文件系统的底层基本操作，包括创建文件系统、打开文件系统、分配 inode、分配数据块等。 use alloc::sync::Arc; use spin::Mutex; use crate::{`
- 与 2025 只编译了一次 在“系统调用”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/syscall.rs:L3-L7`：关键词命中
    代码片段：`use alloc::{sync::Arc, vec::Vec}; use common::syscall::{ OpenFlags, Syscall, SyscallArgs, SyscallRet, time::{TimeVal, TimeZone},`
  - `common/src/syscall.rs:L9-L13`：关键词命中
    代码片段：`/// https://gpages.juszkiewicz.com.pl/syscalls-table/syscalls.html #[derive(Debug, Copy, Clone, PartialEq, Eq)] pub enum Syscall { /// 打开文件 ///`
- 与 2025 只编译了一次 在 driver, filesystem, interrupt, memory, scheduler, sync, syscall 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2025 只编译了一次 的语言构成不同：新项目为 {'json': 18, 'build': 419, 'markdown': 6579, 'toml': 7, 'asm': 156, 'rust': 8127}，历史项目为 {'json': 20, 'build': 367, 'markdown': 4892, 'toml': 117, 'rust': 12330, 'text': 6, 'c': 1833, 'asm': 366, 'make': 116}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：29
- 含证据关键结论数：29（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
