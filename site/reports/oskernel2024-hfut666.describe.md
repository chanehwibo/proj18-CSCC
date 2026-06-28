# OSKernel2024-HFUT666 项目描述报告

## 基本信息

- 仓库 ID：`oskernel2024-hfut666`
- 风格：independent
- 架构：riscv64
- 样本来源等级：比赛作品样本（获奖等级未核验）
- 文件数：124
- 代码/文本行数：15306
- 主要语言：rust 8127 LOC, markdown 6579 LOC, build 419 LOC, asm 156 LOC, json 18 LOC

## 总览

OSKernel2024-HFUT666 是一个 independent 风格的小型操作系统相关仓库，主要语言统计为 rust: 8127 LOC, markdown: 6579 LOC, build: 419 LOC, asm: 156 LOC。仓库包含 124 个已扫描文件、约 15306 行可分析文本，当前抽取到 569 个符号定义。

## 摘要评分

- 综合成熟度：A 级：机制完整、证据充分（100/100）
- 已确认 OS 维度：7/7；高置信维度：7/7
- 构建入口：已确认；证据健康度：100.0% 覆盖率；无效证据引用：0
- 评分口径：该分数由本地静态分析、源码证据和 self-check 派生，不代表比赛官方评分，也不调用 LLM。

| 评分项 | 得分 | 依据 |
| --- | --- | --- |
| OS 机制覆盖 | 80/80 | 调度、内存、系统调用、文件系统、同步、中断、驱动等维度的确认情况 |
| 构建入口 | 10/10 | 是否识别到 Makefile、Cargo.toml、CMakeLists.txt 等构建入口 |
| 证据健康度 | 10/10 | 关键结论证据覆盖率与无效证据引用数 |

| OS 维度 | 状态 | 置信度 | 证据数 |
| --- | --- | --- | --- |
| 调度与任务管理 | 已确认 | high | 6 |
| 内存管理 | 已确认 | high | 6 |
| 系统调用 | 已确认 | high | 11 |
| 文件系统 | 已确认 | high | 6 |
| 同步机制 | 已确认 | high | 6 |
| 中断与异常 | 已确认 | high | 6 |
| 设备驱动 | 已确认 | high | 6 |

## 构建系统

- 仓库包含构建入口：build.rs, Cargo.toml, Makefile, common/Cargo.toml, ros-fs/Cargo.toml。（置信度：high）
  证据：
  - `build.rs:L1-L3`：构建入口
    代码片段：`fn main() { println!("cargo:rerun-if-changed=src/linker.ld"); println!("cargo:rustc-link-arg=-Tsrc/linker.ld");`
  - `Cargo.toml:L1-L3`：构建入口
    代码片段：`# 项目名称、版本、编译器版本、构建脚本所在地址 [package] name = "ros666"`
  - `Makefile:L1-L3`：构建入口
    代码片段：`#  Rust 内核构建目标二进制文件名 KERNEL_BINARY_NAME := $(shell cargo metadata --no-deps --format-version 1 | jq -r ' \ . as $$root | \`
  - `common/Cargo.toml:L1-L3`：构建入口
    代码片段：`[package] name = "common" version = "0.1.0"`
  - `ros-fs/Cargo.toml:L1-L3`：构建入口
    代码片段：`[package] name = "ros-fs" version = "0.1.0"`

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）
  - 相关符号包括：fn init, struct PidHandler, struct PidAllocator, fn new, fn alloc。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/task/mod.rs` | L7-L11 | 关键词命中 |
| `src/task/manager.rs` | L9-L13 | 关键词命中 |
| `src/task/processor.rs` | L8-L12 | 关键词命中 |
| `src/task/mod.rs` | L37-L41 | fn init |
| `src/task/pid.rs` | L18-L22 | struct PidHandler |
| `src/task/pid.rs` | L23-L27 | struct PidAllocator |

### 关键代码片段

  - `src/task/mod.rs:L7-L11`：关键词命中
    代码片段：`use lazy_static::lazy_static; use manager::TaskManager; use task::ProcessControlBlock; use crate::{fs::inode::open_file, utils::safety::SyncRefCell};`
  - `src/task/manager.rs:L9-L13`：关键词命中
    代码片段：`use lazy_static::lazy_static; use crate::task::context::TaskCtx; use crate::task::task::{ProcessControlBlock, ProcessStatus}; use crate::utils::safety::SyncRefCell;`
  - `src/task/processor.rs:L8-L12`：关键词命中
    代码片段：`use lazy_static::lazy_static; use crate::task::context::TaskCtx; use crate::task::task::ProcessControlBlock; use crate::trap::context::TrapCtx;`
  - `src/task/mod.rs:L37-L41`：fn init
    代码片段：`/// /// 初始化任务管理器，并将 INIT_PROC 放入任务管理器的就绪队列中 pub fn init() { TaskManager::put_task(INIT_PROC.clone()); }`

### 相关符号

`fn init` at `src/task/mod.rs:L37`、`struct PidHandler` at `src/task/pid.rs:L18`、`struct PidAllocator` at `src/task/pid.rs:L23`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）
  - 相关符号包括：fn init, struct PhysicalAddress, struct VirtualAddress, struct PhysicalPageNumber, struct VirtualPageNumber。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/mm/mod.rs` | L2-L6 | 关键词命中 |
| `src/mm/init.rs` | L3-L7 | 关键词命中 |
| `src/mm/address.rs` | L2-L6 | 关键词命中 |
| `src/mm/init.rs` | L13-L17 | fn init |
| `src/mm/address.rs` | L23-L27 | struct PhysicalAddress |
| `src/mm/address.rs` | L27-L31 | struct VirtualAddress |

### 关键代码片段

  - `src/mm/mod.rs:L2-L6`：关键词命中
    代码片段：`pub mod address; pub mod frame_allocator; pub mod heap_allocator; pub mod init;`
  - `src/mm/init.rs:L3-L7`：关键词命中
    代码片段：`use crate::trace; use super::{KERNEL_SPACE, frame_allocator, heap_allocator}; /// 记录内核堆是否已初始化`
  - `src/mm/address.rs:L2-L6`：关键词命中
    代码片段：`use core::ops::Add; use super::page_table::PageTableEntry; /// 页内偏移位数`
  - `src/mm/init.rs:L13-L17`：fn init
    代码片段：`// 初始化内核内存管理 pub fn init() { trace!("[Kernel] Init heap allocator"); heap_allocator::init_heap();`

### 相关符号

`fn init` at `src/mm/init.rs:L13`、`struct PhysicalAddress` at `src/mm/address.rs:L23`、`struct VirtualAddress` at `src/mm/address.rs:L27`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含系统调用入口、编号或分发逻辑。（置信度：high）
  - 相关符号包括：fn syscall, fn sys_openat, fn sys_close, fn sys_read, fn sys_write。（置信度：medium）
  - 静态识别到 28 个系统调用相关符号。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/syscall.rs` | L3-L7 | 关键词命中 |
| `common/src/syscall.rs` | L9-L13 | 关键词命中 |
| `user-lib/src/syscall.rs` | L3-L7 | 关键词命中 |
| `src/syscall.rs` | L21-L25 | fn syscall |
| `src/syscall.rs` | L49-L53 | fn sys_openat |
| `src/syscall.rs` | L63-L67 | fn sys_close |

### 关键代码片段

  - `src/syscall.rs:L3-L7`：关键词命中
    代码片段：`use alloc::{sync::Arc, vec::Vec}; use common::syscall::{ OpenFlags, Syscall, SyscallArgs, SyscallRet, time::{TimeVal, TimeZone},`
  - `common/src/syscall.rs:L9-L13`：关键词命中
    代码片段：`/// https://gpages.juszkiewicz.com.pl/syscalls-table/syscalls.html #[derive(Debug, Copy, Clone, PartialEq, Eq)] pub enum Syscall { /// 打开文件 ///`
  - `user-lib/src/syscall.rs:L3-L7`：关键词命中
    代码片段：`use core::arch::asm; use common::syscall::{Syscall, SyscallArgs, SyscallRet}; pub use common::syscall::time::{TimeVal, TimeZone};`
  - `src/syscall.rs:L21-L25`：fn syscall
    代码片段：`}; pub fn syscall(call: Syscall, args: SyscallArgs) -> SyscallRet { match call { Syscall::OpenAt => sys_openat(args[0] as *const u8, args[1] as usize),`

### 相关符号

`fn syscall` at `src/syscall.rs:L21`、`fn sys_openat` at `src/syscall.rs:L49`、`fn sys_close` at `src/syscall.rs:L63`、`fn syscall` at `src/syscall.rs:L21`、`fn sys_openat` at `src/syscall.rs:L49`、`fn sys_close` at `src/syscall.rs:L63`、`fn sys_read` at `src/syscall.rs:L77`、`fn sys_write` at `src/syscall.rs:L99`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 文件系统

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含文件系统、VFS、inode、目录项或文件读写相关实现。（置信度：high）
  - 相关符号包括：trait File, fn read, fn write, fn readable, fn writable。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/fs/mod.rs` | L1-L5 | 关键词命中 |
| `src/fs/inode.rs` | L1-L3 | 关键词命中 |
| `ros-fs/src/fs.rs` | L1-L5 | 关键词命中 |
| `src/fs/mod.rs` | L9-L13 | trait File |
| `src/fs/mod.rs` | L17-L21 | fn read |
| `src/fs/mod.rs` | L25-L29 | fn write |

### 关键代码片段

  - `src/fs/mod.rs:L1-L5`：关键词命中
    代码片段：`use crate::mm::page_table::UserBuffer; pub mod inode; pub mod stdio;`
  - `src/fs/inode.rs:L1-L3`：关键词命中
    代码片段：`//! 操作系统 Inode (文件) 结构 //! //! 一个文件在操作系统中对应一个 Inode 结构，用于管理文件的读写操作`
  - `ros-fs/src/fs.rs:L1-L5`：关键词命中
    代码片段：`//! 物理文件系统 //! //! 建立在物理磁盘块设备上的文件系统，提供了文件系统的底层基本操作，包括创建文件系统、打开文件系统、分配 inode、分配数据块等。 use alloc::sync::Arc; use spin::Mutex;`
  - `src/fs/mod.rs:L9-L13`：trait File
    代码片段：`/// /// 一个文件可以被多个进程共享，因此需要实现 Send 和 Sync trait pub trait File: Send + Sync { /// 从文件中读取数据到用户空间 ///`

### 相关符号

`trait File` at `src/fs/mod.rs:L9`、`fn read` at `src/fs/mod.rs:L17`、`fn write` at `src/fs/mod.rs:L25`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）
  - 相关符号包括：fn open, impl FileSystemRootInode::for::Arc<Mutex<FileSystem>>, struct VirtIOBlock, fn get_cache, struct LockedHeap。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/fs/inode.rs` | L6-L10 | 关键词命中 |
| `ros-fs/src/fs.rs` | L3-L7 | 关键词命中 |
| `src/drivers/block/virtio_block.rs` | L14-L18 | 关键词命中 |
| `ros-fs/src/fs.rs` | L183-L187 | fn open |
| `ros-fs/src/fs.rs` | L216-L220 | impl FileSystemRootInode::for::Arc<Mutex<FileSystem>> |
| `src/drivers/block/virtio_block.rs` | L36-L40 | struct VirtIOBlock |

### 关键代码片段

  - `src/fs/inode.rs:L6-L10`：关键词命中
    代码片段：`use lazy_static::lazy_static; use ros_fs::{fs::FileSystemRootInode, layout::disk_inode::InodeType, virt_fs::MemInode}; use spin::Mutex; use crate::{drivers::block::BLOCK_DEVICE,...`
  - `ros-fs/src/fs.rs:L3-L7`：关键词命中
    代码片段：`//! 建立在物理磁盘块设备上的文件系统，提供了文件系统的底层基本操作，包括创建文件系统、打开文件系统、分配 inode、分配数据块等。 use alloc::sync::Arc; use spin::Mutex; use crate::{`
  - `src/drivers/block/virtio_block.rs:L14-L18`：关键词命中
    代码片段：`use lazy_static::lazy_static; use ros_fs::block_dev::BlockDevice; use spin::Mutex; use virtio_drivers::{ BufferDirection, Hal, PhysAddr,`
  - `ros-fs/src/fs.rs:L183-L187`：fn open
    代码片段：`/// /// 从块设备中打开一个已有的文件系统，读取超级块，inode 位图，数据块位图等信息 pub fn open(dev: Arc<dyn BlockDevice>) -> Arc<Mutex<Self>> { let cache = get_cache(0, dev.clone()).expect("get cache failed"); l...`

### 相关符号

`fn open` at `ros-fs/src/fs.rs:L183`、`impl FileSystemRootInode::for::Arc<Mutex<FileSystem>>` at `ros-fs/src/fs.rs:L216`、`struct VirtIOBlock` at `src/drivers/block/virtio_block.rs:L36`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 中断与异常

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `interrupt` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含 trap、中断、异常或定时器处理逻辑。（置信度：high）
  - 相关符号包括：fn init, fn enable_timer_interrupt, fn set_kernel_trap_entry, struct TrapCtx, fn set_sp。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/trap/init.rs` | L7-L11 | 关键词命中 |
| `src/trap/handler.rs` | L5-L9 | 关键词命中 |
| `src/syscall.rs` | L16-L20 | 关键词命中 |
| `src/trap/init.rs` | L10-L14 | fn init |
| `src/trap/init.rs` | L15-L19 | fn enable_timer_interrupt |
| `src/trap/init.rs` | L23-L27 | fn set_kernel_trap_entry |

### 关键代码片段

  - `src/trap/init.rs:L7-L11`：关键词命中
    代码片段：`use super::handler::trap_from_kernel; global_asm!(include_str!("trap.asm")); /// 初始化陷入`
  - `src/trap/handler.rs:L5-L9`：关键词命中
    代码片段：`use common::syscall::Syscall; use riscv::{ interrupt::{Exception, supervisor::Interrupt}, register::{ scause, stval,`
  - `src/syscall.rs:L16-L20`：关键词命中
    代码片段：`printkln, task::{self, manager::TaskManager, processor::Processor, task::ProcessStatus}, timer::get_time_us, trap::context::Riscv64RegAlias, warn,`
  - `src/trap/init.rs:L10-L14`：fn init
    代码片段：`/// 初始化陷入 pub fn init() { set_kernel_trap_entry(); }`

### 相关符号

`fn init` at `src/trap/init.rs:L10`、`fn enable_timer_interrupt` at `src/trap/init.rs:L15`、`fn set_kernel_trap_entry` at `src/trap/init.rs:L23`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。（置信度：high）
  - 相关符号包括：struct SDCard, enum CMD, enum InitError, struct SDCardCSD, struct SDCardCID。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/drivers/mod.rs` | L4-L8 | 关键词命中 |
| `src/drivers/block/mod.rs` | L7-L11 | 关键词命中 |
| `src/drivers/block/sdcard.rs` | L1-L3 | 关键词命中 |
| `src/drivers/block/sdcard.rs` | L67-L71 | struct SDCard |
| `src/drivers/block/sdcard.rs` | L95-L99 | enum CMD |
| `src/drivers/block/sdcard.rs` | L130-L134 | enum InitError |

### 关键代码片段

  - `src/drivers/mod.rs:L4-L8`：关键词命中
    代码片段：`//! //! 目前支持: //! - qemu virtio block 设备。 //! - 引入了 K210 SD 卡驱动, 未经测试。 pub mod block;`
  - `src/drivers/block/mod.rs:L7-L11`：关键词命中
    代码片段：`pub mod sdcard; pub mod virtio_block; #[cfg(feature = "qemu")]`
  - `src/drivers/block/sdcard.rs:L1-L3`：关键词命中
    代码片段：`//! ## SDCard Driver //! //! ## References:`
  - `src/drivers/block/sdcard.rs:L67-L71`：struct SDCard
    代码片段：`use lazy_static::*; pub struct SDCard<SPI> { spi: SPI, spi_cs: u32,`

### 相关符号

`struct SDCard` at `src/drivers/block/sdcard.rs:L67`、`enum CMD` at `src/drivers/block/sdcard.rs:L95`、`enum InitError` at `src/drivers/block/sdcard.rs:L130`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 附录：核验摘要

- 关键结论数：16
- 含证据关键结论数：16（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
