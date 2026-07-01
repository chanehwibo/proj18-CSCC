# 2026 T2026105749910169 项目描述报告

## 基本信息

- 仓库 ID：`collected2026-26qs`
- 风格：ucore-variant
- 架构：未确认
- 样本来源等级：current_contest_case
- 文件数：74
- 代码/文本行数：45957
- 主要语言：rust 42750 LOC, markdown 2266 LOC, asm 662 LOC, build 267 LOC, toml 12 LOC

## 总览

2026 T2026105749910169 是一个 ucore-variant 风格的小型操作系统相关仓库，主要语言统计为 rust: 42750 LOC, markdown: 2266 LOC, asm: 662 LOC, build: 267 LOC。仓库包含 74 个已扫描文件、约 45957 行可分析文本，当前抽取到 2182 个符号定义。

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
| 调度与任务管理 | 已确认 | high | 4 |
| 内存管理 | 已确认 | high | 6 |
| 系统调用 | 已确认 | high | 11 |
| 文件系统 | 已确认 | high | 6 |
| 同步机制 | 已确认 | high | 3 |
| 中断与异常 | 已确认 | high | 3 |
| 设备驱动 | 已确认 | high | 6 |

## 构建系统

- 仓库包含构建入口：Cargo.toml, Makefile。（置信度：high）
  证据：
  - `Cargo.toml:L1-L3`：构建入口
    代码片段：`[package] name = "os_mod_kernel" version = "0.1.0"`
  - `Makefile:L1-L3`：构建入口
    代码片段：`SHELL := /bin/sh RUST_TOOLCHAIN ?= /root/.rustup/toolchains/nightly-2025-01-18-x86_64-unknown-linux-gnu`

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）
  - 相关符号包括：fn render_thread。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/syscall/mod.rs` | L197-L201 | 关键词命中 |
| `src/syscall/file.rs` | L884-L888 | 关键词命中 |
| `src/vm.rs` | L1735-L1739 | 关键词命中 |
| `src/cyclictest.rs` | L31-L35 | fn render_thread |

### 关键代码片段

  - `src/syscall/mod.rs:L197-L201`：关键词命中
    代码片段：`const PROC_MEMINFO: &[u8] = b"MemTotal:       262144 kB\nMemFree:        131072 kB\nMemAvailable:   131072 kB\nBuffers:          4096 kB\nCached:          32768 kB\n"; const PRO...`
  - `src/syscall/file.rs:L884-L888`：关键词命中
    代码片段：`fn device_id_for_path(path: &[u8]) -> u64 { if path == b"/proc" || path.starts_with(b"/proc/") { 2 } else {`
  - `src/vm.rs:L1735-L1739`：关键词命中
    代码片段：`} /// LoongArch adapter fork twin (the layer the future LA per-process scheduler calls). /// Byte-for-byte the RvSv39 fork_clone/free_frames, but over LaPt — LaPt::fork_cow ///...`
  - `src/cyclictest.rs:L31-L35`：fn render_thread
    代码片段：`} fn render_thread(thread: u32, max_latency: u32, sink: &mut impl OutputSink) { sink.write_str("T: "); write_u32(thread, sink);`

### 相关符号

`fn render_thread` at `src/cyclictest.rs:L31`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）
  - 相关符号包括：fn sys_brk, fn brk_return_value, fn sys_mmap, fn next_mmap_addr, fn sys_mprotect。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/syscall/memory.rs` | L112-L116 | 关键词命中 |
| `src/syscall/mod.rs` | L203-L207 | 关键词命中 |
| `src/vm.rs` | L1-L3 | 关键词命中 |
| `src/syscall/memory.rs` | L10-L14 | fn sys_brk |
| `src/syscall/memory.rs` | L34-L38 | fn brk_return_value |
| `src/syscall/memory.rs` | L43-L47 | fn sys_mmap |

### 关键代码片段

  - `src/syscall/memory.rs:L112-L116`：关键词命中
    代码片段：`// mapping (mmap(MAP_SHARED|MAP_ANONYMOUS) BEFORE the fork), which the parent reaps // for "Summary: passed N". Back it with zero-filled SharedFile frames — the same // fork-sha...`
  - `src/syscall/mod.rs:L203-L207`：关键词命中
    代码片段：`/// LTP getegid01/geteuid01 scan /proc/self/status for the Uid:/Gid: lines. const PROC_SELF_STATUS: &[u8] = b"Name:\tltp\nState:\tR (running)\nTgid:\t1\nPid:\t1\nPPid:\t0\nUid:\...`
  - `src/vm.rs:L1-L3`：关键词命中
    代码片段：`//! Real-VM rework — Phase 0 foundations (AddrSpace / demand paging / COW / ...). //! //! Compiled ONLY under 'cfg(any(feature = "addrspace", test))', so the graded`
  - `src/syscall/memory.rs:L10-L14`：fn sys_brk
    代码片段：`use super::*; pub(crate) fn sys_brk( ctx: &mut SyscallContext, memory: &impl UserMemoryAccess,`

### 相关符号

`fn sys_brk` at `src/syscall/memory.rs:L10`、`fn brk_return_value` at `src/syscall/memory.rs:L34`、`fn sys_mmap` at `src/syscall/memory.rs:L43`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含系统调用入口、编号或分发逻辑。（置信度：high）
  - 相关符号包括：fn sys_write, fn sys_read, fn sys_pread64, fn sys_pwrite64, fn sys_readv。（置信度：medium）
  - 静态识别到 110 个系统调用相关符号。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/syscall/io.rs` | L2-L6 | 关键词命中 |
| `src/syscall/mod.rs` | L1379-L1383 | 关键词命中 |
| `src/syscall/file.rs` | L1-L5 | 关键词命中 |
| `src/syscall/io.rs` | L8-L12 | fn sys_write |
| `src/syscall/io.rs` | L75-L79 | fn sys_read |
| `src/syscall/io.rs` | L129-L133 | fn sys_pread64 |

### 关键代码片段

  - `src/syscall/io.rs:L2-L6`：关键词命中
    代码片段：`//! and vectored ('readv'/'writev'/'preadv'/'pwritev' + v2) variants. //! //! Extracted handler domain (descendant of 'syscall'); reaches SyscallContext //! internals and shared...`
  - `src/syscall/mod.rs:L1379-L1383`：关键词命中
    代码片段：`pub ppid: usize, pub state: ProcessState, // The fields below stay private to the 'syscall' module. Handler domains // split into child modules (e.g. 'syscall::memory') are desc...`
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
  - `src/syscall/io.rs:L8-L12`：fn sys_write
    代码片段：`use super::*; pub(crate) fn sys_write( ctx: &mut SyscallContext, memory: &impl UserMemoryAccess,`

### 相关符号

`fn sys_write` at `src/syscall/io.rs:L8`、`fn sys_read` at `src/syscall/io.rs:L75`、`fn sys_pread64` at `src/syscall/io.rs:L129`、`fn sys_write` at `src/syscall/io.rs:L8`、`fn sys_read` at `src/syscall/io.rs:L75`、`fn sys_pread64` at `src/syscall/io.rs:L129`、`fn sys_pwrite64` at `src/syscall/io.rs:L156`、`fn sys_readv` at `src/syscall/io.rs:L187`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 文件系统

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含文件系统、VFS、inode、目录项或文件读写相关实现。（置信度：high）
  - 相关符号包括：enum Ext4Error, fn from, fn install_read_wall_clock, fn read_wall_deadline, struct ByteBuf。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/fs/ext4.rs` | L199-L203 | 关键词命中 |
| `src/syscall/file.rs` | L1-L5 | 关键词命中 |
| `src/syscall/mod.rs` | L1049-L1053 | 关键词命中 |
| `src/fs/ext4.rs` | L25-L29 | enum Ext4Error |
| `src/fs/ext4.rs` | L56-L60 | fn from |
| `src/fs/ext4.rs` | L76-L80 | fn install_read_wall_clock |

### 关键代码片段

  - `src/fs/ext4.rs:L199-L203`：关键词命中
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)] pub struct DirectoryEntry { pub inode: u32, pub file_type: FileType, pub name: FileName,`
  - `src/syscall/file.rs:L1-L5`：关键词命中
    代码片段：`//! File, directory, fd-table and stat syscalls. //! //! The VFS-facing syscall surface: fd ops (dup/fcntl/close/lseek/ftruncate), //! 'openat', path ops (chdir/mkdirat/unlinkat...`
  - `src/syscall/mod.rs:L1049-L1053`：关键词命中
    代码片段：`// ---- Extended attributes (setxattr / getxattr / listxattr / removexattr) ---- // A small global (path, name) -> value store. Keyed by the path + attribute-name STRINGS // (no...`
  - `src/fs/ext4.rs:L25-L29`：enum Ext4Error
    代码片段：`#[derive(Debug, Clone, Copy, PartialEq, Eq)] pub enum Ext4Error { Block(BlockError), AddressOverflow,`

### 相关符号

`enum Ext4Error` at `src/fs/ext4.rs:L25`、`fn from` at `src/fs/ext4.rs:L56`、`fn install_read_wall_clock` at `src/fs/ext4.rs:L76`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/syscall/mod.rs` | L601-L605 | 关键词命中 |
| `src/syscall/storage.rs` | L195-L199 | 关键词命中 |
| `src/main.rs` | L3148-L3152 | 关键词命中 |

### 关键代码片段

  - `src/syscall/mod.rs:L601-L605`：关键词命中
    代码片段：`// ---- SysV semaphores (semget / semop / semctl) ---- // A small global semaphore-set registry, sibling to the SysV-shm one above. Sets live // in kernel memory keyed by a 1-ba...`
  - `src/syscall/storage.rs:L195-L199`：关键词命中
    代码片段：`#[cfg(test)] static RUNTIME_STORAGE_POOL: std::sync::Mutex<RuntimeStoragePool> = std::sync::Mutex::new(RuntimeStoragePool::new());`
  - `src/main.rs:L3148-L3152`：关键词命中
    代码片段：`(*core::ptr::addr_of_mut!(PROCESS_RUNTIME)).reset_root(context); syscall::shm_reset(); // fresh process tree => no shm segments allocated yet syscall::sem_reset(); // fresh proc...`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 中断与异常

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `interrupt` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含 trap、中断、异常或定时器处理逻辑。（置信度：high）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/syscall/mod.rs` | L1413-L1417 | 关键词命中 |
| `src/vm.rs` | L240-L244 | 关键词命中 |
| `src/lib.rs` | L49-L53 | 关键词命中 |

### 关键代码片段

  - `src/syscall/mod.rs:L1413-L1417`：关键词命中
    代码片段：`signals: SignalState, /// ITIMER_REAL: absolute monotonic deadline of the next SIGALRM (0 = /// disarmed) and the repeat interval (0 = one-shot). The budget-timer tick /// raise...`
  - `src/vm.rs:L240-L244`：关键词命中
    代码片段：`/// The hardware activation token: RV = the satp value; LA = the root PA. fn root_token(&self) -> usize; /// Install the kernel identity mapping (RAM + MMIO, U=0) so the trap ha...`
  - `src/lib.rs:L49-L53`：关键词命中
    代码片段：`let save_t0 = asm .find("sd x5, 5 * 8(sp)") .expect("riscv trap vector must save x5/t0"); let read_sscratch = asm .find("csrr t0, sscratch")`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。（置信度：high）
  - 相关符号包括：fn open, fn read_superblock, fn read_at, struct Writer, fn write_byte。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/console.rs` | L28-L32 | 关键词命中 |
| `src/virtio/blk.rs` | L2-L6 | 关键词命中 |
| `src/virtio/mod.rs` | L1-L3 | 关键词命中 |
| `src/fs/ext4.rs` | L407-L411 | fn open |
| `src/fs/ext4.rs` | L784-L788 | fn read_superblock |
| `src/fs/ext4.rs` | L835-L839 | fn read_at |

### 关键代码片段

  - `src/console.rs:L28-L32`：关键词命中
    代码片段：`macro_rules! print { ($($arg:tt)*) => {{ $crate::console::_print(format_args!($($arg)*)); }}; }`
  - `src/virtio/blk.rs:L2-L6`：关键词命中
    代码片段：`pub const SECTOR_SIZE: usize = 512; pub const VIRTIO_BLK_T_IN: u32 = 0; pub const VIRTIO_BLK_S_OK: u8 = 0; pub const VIRTIO_BLK_S_IOERR: u8 = 1;`
  - `src/virtio/mod.rs:L1-L3`：关键词命中
    代码片段：`pub mod blk; pub mod mmio; pub mod pci;`
  - `src/fs/ext4.rs:L407-L411`：fn open
    代码片段：`impl<'a, D: BlockDevice> Ext4Reader<'a, D> { pub fn open(device: &'a mut D) -> Result<Self, Ext4Error> { let superblock = read_superblock(device)?; Ok(Self { device, superblock })`

### 相关符号

`fn open` at `src/fs/ext4.rs:L407`、`fn read_superblock` at `src/fs/ext4.rs:L784`、`fn read_at` at `src/fs/ext4.rs:L835`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 附录：核验摘要

- 关键结论数：14
- 含证据关键结论数：14（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
