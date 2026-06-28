# HUSTer proj306 Rust OS for framekernel architecture 项目描述报告

## 基本信息

- 仓库 ID：`award2024-huster-proj306`
- 风格：framekernel
- 架构：x86_64
- 样本来源等级：已核验获奖案例（一等奖，来源：os-funtion-winners.md）
- 文件数：1130
- 代码/文本行数：128357
- 主要语言：rust 112841 LOC, c 7549 LOC, markdown 3324 LOC, build 2417 LOC, asm 1515 LOC

## 总览

HUSTer proj306 Rust OS for framekernel architecture 是一个 framekernel 风格的小型操作系统相关仓库，主要语言统计为 rust: 112841 LOC, c: 7549 LOC, markdown: 3324 LOC, build: 2417 LOC。仓库包含 1130 个已扫描文件、约 128357 行可分析文本，当前抽取到 9541 个符号定义。

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

- 仓库包含构建入口：asterinas/Cargo.toml, asterinas/Makefile, asterinas/kernel/Cargo.toml, asterinas/osdk/Cargo.toml, asterinas/ostd/Cargo.toml。（置信度：high）
  证据：
  - `asterinas/Cargo.toml:L1-L3`：构建入口
    代码片段：`[workspace] resolver = "2" members = [`
  - `asterinas/Makefile:L1-L3`：构建入口
    代码片段：`# SPDX-License-Identifier: MPL-2.0 # Global options.`
  - `asterinas/kernel/Cargo.toml:L1-L3`：构建入口
    代码片段：`[package] name = "asterinas" version = "0.4.0"`
  - `asterinas/osdk/Cargo.toml:L1-L3`：构建入口
    代码片段：`[package] name = "cargo-osdk" version = "0.6.2"`
  - `asterinas/ostd/Cargo.toml:L1-L3`：构建入口
    代码片段：`[package] name = "ostd" version = "0.6.2"`

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）
  - 相关符号包括：trait TaskContextApi, fn set_instruction_pointer, fn instruction_pointer, fn set_stack_pointer, fn stack_pointer。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `asterinas/ostd/src/task/mod.rs` | L5-L9 | 关键词命中 |
| `asterinas/ostd/src/task/task.rs` | L13-L17 | 关键词命中 |
| `asterinas/ostd/src/task/priority.rs` | L3-L7 | 关键词命中 |
| `asterinas/ostd/src/task/task.rs` | L28-L32 | trait TaskContextApi |
| `asterinas/ostd/src/task/task.rs` | L30-L34 | fn set_instruction_pointer |
| `asterinas/ostd/src/task/task.rs` | L33-L37 | fn instruction_pointer |

### 关键代码片段

  - `asterinas/ostd/src/task/mod.rs:L5-L9`：关键词命中
    代码片段：`mod priority; mod processor; mod scheduler; #[allow(clippy::module_inception)] mod task;`
  - `asterinas/ostd/src/task/task.rs:L13-L17`：关键词命中
    代码片段：`add_task, priority::Priority, processor::{current_task, schedule}, }; pub(crate) use crate::arch::task::{context_switch, TaskContext};`
  - `asterinas/ostd/src/task/priority.rs:L3-L7`：关键词命中
    代码片段：`pub const REAL_TIME_TASK_PRIORITY: u16 = 100; /// The priority of a task. /// /// Similar to Linux, a larger value represents a lower priority,`
  - `asterinas/ostd/src/task/task.rs:L28-L32`：trait TaskContextApi
    代码片段：`/// Trait for manipulating the task context. pub trait TaskContextApi { /// Sets instruction pointer fn set_instruction_pointer(&mut self, ip: usize);`

### 相关符号

`trait TaskContextApi` at `asterinas/ostd/src/task/task.rs:L28`、`fn set_instruction_pointer` at `asterinas/ostd/src/task/task.rs:L30`、`fn instruction_pointer` at `asterinas/ostd/src/task/task.rs:L33`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）
  - 相关符号包括：trait VmIo, fn read_bytes, fn read_val, fn read_slice, fn write_bytes。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `asterinas/ostd/src/mm/io.rs` | L241-L245 | 关键词命中 |
| `asterinas/ostd/src/mm/mod.rs` | L11-L15 | 关键词命中 |
| `asterinas/ostd/src/mm/kspace.rs` | L53-L57 | 关键词命中 |
| `asterinas/ostd/src/mm/io.rs` | L30-L34 | trait VmIo |
| `asterinas/ostd/src/mm/io.rs` | L38-L42 | fn read_bytes |
| `asterinas/ostd/src/mm/io.rs` | L41-L45 | fn read_val |

### 关键代码片段

  - `asterinas/ostd/src/mm/io.rs:L241-L245`：关键词命中
    代码片段：`/// When the operating range is in kernel space, the memory within that range /// is guaranteed to be valid. /// When the operating range is in user space, it is ensured that th...`
  - `asterinas/ostd/src/mm/mod.rs:L11-L15`：关键词命中
    代码片段：`pub(crate) mod dma; pub mod frame; pub(crate) mod heap_allocator; mod io; pub(crate) mod kspace;`
  - `asterinas/ostd/src/mm/kspace.rs:L53-L57`：关键词命中
    代码片段：`}, page_prop::{CachePolicy, PageFlags, PageProperty, PrivilegedPageFlags}, page_table::{boot_pt::BootPageTable, KernelMode, PageTable}, MemoryRegionType, Paddr, PagingConstsTrai...`
  - `asterinas/ostd/src/mm/io.rs:L30-L34`：trait VmIo
    代码片段：`/// ['Segment']: crate::mm::Segment /// ['Frame']: crate::mm::Frame pub trait VmIo: Send + Sync { /// Reads a specified number of bytes at a specified offset into a given buffer...`

### 相关符号

`trait VmIo` at `asterinas/ostd/src/mm/io.rs:L30`、`fn read_bytes` at `asterinas/ostd/src/mm/io.rs:L38`、`fn read_val` at `asterinas/ostd/src/mm/io.rs:L41`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含系统调用入口、编号或分发逻辑。（置信度：high）
  - 相关符号包括：struct IrqLine, fn alloc_specific, fn alloc, fn new, fn num。（置信度：medium）
  - 静态识别到 188 个系统调用相关符号。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `asterinas/kernel/aster-nix/src/syscall/brk.rs` | L1-L5 | 关键词命中 |
| `asterinas/kernel/aster-nix/src/syscall/mod.rs` | L1-L5 | 关键词命中 |
| `asterinas/kernel/aster-nix/src/syscall/exit.rs` | L4-L8 | 关键词命中 |
| `asterinas/ostd/src/trap/irq.rs` | L26-L30 | struct IrqLine |
| `asterinas/ostd/src/trap/irq.rs` | L35-L39 | fn alloc_specific |
| `asterinas/ostd/src/trap/irq.rs` | L46-L50 | fn alloc |

### 关键代码片段

  - `asterinas/kernel/aster-nix/src/syscall/brk.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 use crate::{prelude::*, syscall::SyscallReturn}; /// expand the user heap to new heap end, returns the new heap end if expansion succeeds.`
  - `asterinas/kernel/aster-nix/src/syscall/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Read the Cpu context content then dispatch syscall to corrsponding handler //! The each sub module contains functions that handle real sy...`
  - `asterinas/kernel/aster-nix/src/syscall/exit.rs:L4-L8`：关键词命中
    代码片段：`prelude::*, process::{posix_thread::do_exit, TermStatus}, syscall::SyscallReturn, };`
  - `asterinas/ostd/src/trap/irq.rs:L26-L30`：struct IrqLine
    代码片段：`#[derive(Debug)] #[must_use] pub struct IrqLine { irq_num: u8, #[allow(clippy::redundant_allocation)]`

### 相关符号

`struct IrqLine` at `asterinas/ostd/src/trap/irq.rs:L26`、`fn alloc_specific` at `asterinas/ostd/src/trap/irq.rs:L35`、`fn alloc` at `asterinas/ostd/src/trap/irq.rs:L46`、`fn sys_brk` at `asterinas/kernel/aster-nix/src/syscall/brk.rs:L4`、`fn sys_dup` at `asterinas/kernel/aster-nix/src/syscall/dup.rs:L8`、`fn sys_dup2` at `asterinas/kernel/aster-nix/src/syscall/dup.rs:L18`、`fn sys_dup3` at `asterinas/kernel/aster-nix/src/syscall/dup.rs:L31`、`fn syscall_dispatch` at `asterinas/kernel/aster-nix/src/syscall/mod.rs:L182`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 文件系统

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含文件系统、VFS、inode、目录项或文件读写相关实现。（置信度：high）
  - 相关符号包括：fn start_block_device, fn lazy_init, struct PipeReader, fn new, fn poll。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `asterinas/kernel/aster-nix/src/fs/device.rs` | L5-L9 | 关键词命中 |
| `asterinas/kernel/aster-nix/src/fs/rootfs.rs` | L56-L60 | 关键词命中 |
| `asterinas/kernel/aster-nix/src/fs/ext2/fs.rs` | L6-L10 | 关键词命中 |
| `asterinas/kernel/aster-nix/src/fs/mod.rs` | L29-L33 | fn start_block_device |
| `asterinas/kernel/aster-nix/src/fs/mod.rs` | L46-L50 | fn lazy_init |
| `asterinas/kernel/aster-nix/src/fs/pipe.rs` | L19-L23 | struct PipeReader |

### 关键代码片段

  - `asterinas/kernel/aster-nix/src/fs/device.rs:L5-L9`：关键词命中
    代码片段：`fs::{ fs_resolver::{FsPath, FsResolver}, path::Dentry, utils::{InodeMode, InodeType}, },`
  - `asterinas/kernel/aster-nix/src/fs/rootfs.rs:L56-L60`：关键词命中
    代码片段：`match metadata.file_type() { FileType::File => { let dentry = parent.new_fs_child(name, InodeType::File, mode)?; entry.read_all(dentry.inode().writer(0))?; }`
  - `asterinas/kernel/aster-nix/src/fs/ext2/fs.rs:L6-L10`：关键词命中
    代码片段：`block_group::{BlockGroup, RawGroupDescriptor}, block_ptr::Ext2Bid, inode::{FilePerm, FileType, Inode, InodeDesc, RawInode}, prelude::*, super_block::{RawSuperBlock, SuperBlock,...`
  - `asterinas/kernel/aster-nix/src/fs/mod.rs:L29-L33`：fn start_block_device
    代码片段：`}; fn start_block_device(device_name: &str) -> Result<Arc<dyn BlockDevice>> { if let Some(device) = aster_block::get_device(device_name) { let cloned_device = device.clone();`

### 相关符号

`fn start_block_device` at `asterinas/kernel/aster-nix/src/fs/mod.rs:L29`、`fn lazy_init` at `asterinas/kernel/aster-nix/src/fs/mod.rs:L46`、`struct PipeReader` at `asterinas/kernel/aster-nix/src/fs/pipe.rs:L19`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）
  - 相关符号包括：struct SpinLock, impl SpinLock<T>, fn lock_irq_disabled, fn try_lock_irq_disabled, fn lock。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `asterinas/ostd/src/sync/mod.rs` | L4-L8 | 关键词命中 |
| `asterinas/ostd/src/sync/spin.rs` | L8-L12 | 关键词命中 |
| `asterinas/ostd/src/sync/wait.rs` | L2-L6 | 关键词命中 |
| `asterinas/ostd/src/sync/spin.rs` | L17-L21 | struct SpinLock |
| `asterinas/ostd/src/sync/spin.rs` | L22-L26 | impl SpinLock<T> |
| `asterinas/ostd/src/sync/spin.rs` | L38-L42 | fn lock_irq_disabled |

### 关键代码片段

  - `asterinas/ostd/src/sync/mod.rs:L4-L8`：关键词命中
    代码片段：`mod atomic_bits; mod mutex; // TODO: refactor this rcu implementation // Comment out this module since it raises lint error`
  - `asterinas/ostd/src/sync/spin.rs:L8-L12`：关键词命中
    代码片段：`fmt, ops::{Deref, DerefMut}, sync::atomic::{AtomicBool, Ordering}, };`
  - `asterinas/ostd/src/sync/wait.rs:L2-L6`：关键词命中
    代码片段：`use alloc::{collections::VecDeque, sync::Arc}; use core::sync::atomic::{AtomicBool, AtomicU32, Ordering}; use super::SpinLock;`
  - `asterinas/ostd/src/sync/spin.rs:L17-L21`：struct SpinLock
    代码片段：`/// A spin lock. pub struct SpinLock<T: ?Sized> { lock: AtomicBool, val: UnsafeCell<T>,`

### 相关符号

`struct SpinLock` at `asterinas/ostd/src/sync/spin.rs:L17`、`impl SpinLock<T>` at `asterinas/ostd/src/sync/spin.rs:L22`、`fn lock_irq_disabled` at `asterinas/ostd/src/sync/spin.rs:L38`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 中断与异常

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `interrupt` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含 trap、中断、异常或定时器处理逻辑。（置信度：high）
  - 相关符号包括：struct IrqLine, fn alloc_specific, fn alloc, fn new, fn num。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `asterinas/ostd/src/trap/irq.rs` | L8-L12 | 关键词命中 |
| `asterinas/ostd/src/trap/mod.rs` | L1-L5 | 关键词命中 |
| `asterinas/ostd/src/trap/handler.rs` | L5-L9 | 关键词命中 |
| `asterinas/ostd/src/trap/irq.rs` | L26-L30 | struct IrqLine |
| `asterinas/ostd/src/trap/irq.rs` | L35-L39 | fn alloc_specific |
| `asterinas/ostd/src/trap/irq.rs` | L46-L50 | fn alloc |

### 关键代码片段

  - `asterinas/ostd/src/trap/irq.rs:L8-L12`：关键词命中
    代码片段：`use crate::{ arch::irq::{self, IrqCallbackHandle, IRQ_ALLOCATOR}, prelude::*, task::{disable_preempt, DisablePreemptGuard},`
  - `asterinas/ostd/src/trap/mod.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! Handles trap across kernel and user space. mod handler;`
  - `asterinas/ostd/src/trap/handler.rs:L5-L9`：关键词命中
    代码片段：`use trapframe::TrapFrame; use crate::{arch::irq::IRQ_LIST, cpu_local}; pub(crate) fn call_irq_callback_functions(trap_frame: &TrapFrame, irq_number: usize) {`
  - `asterinas/ostd/src/trap/irq.rs:L26-L30`：struct IrqLine
    代码片段：`#[derive(Debug)] #[must_use] pub struct IrqLine { irq_num: u8, #[allow(clippy::redundant_allocation)]`

### 相关符号

`struct IrqLine` at `asterinas/ostd/src/trap/irq.rs:L26`、`fn alloc_specific` at `asterinas/ostd/src/trap/irq.rs:L35`、`fn alloc` at `asterinas/ostd/src/trap/irq.rs:L46`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。（置信度：high）
  - 相关符号包括：fn virtio_component_init, fn pop_device_transport, fn negotiate_features, struct Feature, struct VirtioConsolesPrinter。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `asterinas/kernel/comps/virtio/src/lib.rs` | L1-L5 | 关键词命中 |
| `asterinas/kernel/aster-nix/src/console.rs` | L3-L7 | 关键词命中 |
| `asterinas/kernel/comps/console/src/lib.rs` | L1-L5 | 关键词命中 |
| `asterinas/kernel/comps/virtio/src/lib.rs` | L34-L38 | fn virtio_component_init |
| `asterinas/kernel/comps/virtio/src/lib.rs` | L77-L81 | fn pop_device_transport |
| `asterinas/kernel/comps/virtio/src/lib.rs` | L87-L91 | fn negotiate_features |

### 关键代码片段

  - `asterinas/kernel/comps/virtio/src/lib.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! The virtio of Asterinas. #![no_std] #![deny(unsafe_code)]`
  - `asterinas/kernel/aster-nix/src/console.rs:L3-L7`：关键词命中
    代码片段：`//! 'print' and 'println' macros //! //! FIXME: It will print to all 'virtio-console' devices, which is not a good choice. //!`
  - `asterinas/kernel/comps/console/src/lib.rs:L1-L5`：关键词命中
    代码片段：`// SPDX-License-Identifier: MPL-2.0 //! The console device of Asterinas. #![no_std] #![deny(unsafe_code)]`
  - `asterinas/kernel/comps/virtio/src/lib.rs:L34-L38`：fn virtio_component_init
    代码片段：`#[init_component] fn virtio_component_init() -> Result<(), ComponentInitError> { // Find all devices and register them to the corresponding crate transport::init();`

### 相关符号

`fn virtio_component_init` at `asterinas/kernel/comps/virtio/src/lib.rs:L34`、`fn pop_device_transport` at `asterinas/kernel/comps/virtio/src/lib.rs:L77`、`fn negotiate_features` at `asterinas/kernel/comps/virtio/src/lib.rs:L87`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 附录：核验摘要

- 关键结论数：16
- 含证据关键结论数：16（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
