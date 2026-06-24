# IncludeOS 项目描述报告

## 基本信息

- 仓库 ID：`includeos`
- 风格：unikernel
- 架构：x86_64
- 样本来源等级：架构参考样本
- 文件数：1170
- 代码/文本行数：128146
- 主要语言：cpp 118006 LOC, build 3554 LOC, asm 2874 LOC, c 2076 LOC, markdown 823 LOC

## 总览

IncludeOS 是一个 unikernel 风格的小型操作系统相关仓库，主要语言统计为 cpp: 118006 LOC, build: 3554 LOC, asm: 2874 LOC, c: 2076 LOC。仓库包含 1170 个已扫描文件、约 128146 行可分析文本，当前抽取到 2518 个符号定义。

## 摘要评分

- 综合成熟度：A 级：机制完整、证据充分（96/100）
- 已确认 OS 维度：7/7；高置信维度：6/7
- 构建入口：已确认；证据健康度：100.0% 覆盖率；无效证据引用：0
- 评分口径：该分数由本地静态分析、源码证据和 self-check 派生，不代表比赛官方评分，也不调用 LLM。

| 评分项 | 得分 | 依据 |
| --- | --- | --- |
| OS 机制覆盖 | 76/80 | 调度、内存、系统调用、文件系统、同步、中断、驱动等维度的确认情况 |
| 构建入口 | 10/10 | 是否识别到 Makefile、Cargo.toml、CMakeLists.txt 等构建入口 |
| 证据健康度 | 10/10 | 关键结论证据覆盖率与无效证据引用数 |

| OS 维度 | 状态 | 置信度 | 证据数 |
| --- | --- | --- | --- |
| 调度与任务管理 | 已确认 | high | 5 |
| 内存管理 | 已确认 | high | 6 |
| 系统调用 | 已确认 | medium | 11 |
| 文件系统 | 已确认 | high | 6 |
| 同步机制 | 已确认 | high | 6 |
| 中断与异常 | 已确认 | high | 4 |
| 设备驱动 | 已确认 | high | 6 |

## 构建系统

- 仓库包含构建入口：CMakeLists.txt, example/CMakeLists.txt, src/CMakeLists.txt, test/CMakeLists.txt, userspace/CMakeLists.txt。（置信度：high）
  证据：
  - `CMakeLists.txt:L1-L3`：构建入口
    代码片段：`cmake_minimum_required(VERSION 3.31.6) #we are only creating libraries for ELF`
  - `example/CMakeLists.txt:L1-L3`：构建入口
    代码片段：`cmake_minimum_required(VERSION 3.31.6) set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)`
  - `src/CMakeLists.txt:L1-L3`：构建入口
    代码片段：`# # CMake script for the OS library #`
  - `test/CMakeLists.txt:L1-L3`：构建入口
    代码片段：`cmake_minimum_required(VERSION 3.31.6) # #  builds unit tests`
  - `userspace/CMakeLists.txt:L1-L3`：构建入口
    代码片段：`include_directories(../api) include_directories(../mod) include_directories(../mod/GSL)`

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）
  - 相关符号包括：fn syscall_SYS_sched_yield, fn pthread_join。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `api/kernel/fiber.hpp` | L155-L159 | 关键词命中 |
| `src/kernel/fiber.cpp` | L76-L80 | 关键词命中 |
| `api/kernel/timers.hpp` | L41-L45 | 关键词命中 |
| `src/musl/sched_yield.cpp` | L7-L11 | fn syscall_SYS_sched_yield |
| `src/posix/pthread.cpp` | L39-L43 | fn pthread_join |

### 关键代码片段

  - `api/kernel/fiber.hpp:L155-L159`：关键词命中
    代码片段：`void start(); /** Yield into the parent fiber. */ static void yield();`
  - `src/kernel/fiber.cpp:L76-L80`：关键词命中
    代码片段：`__fiber_jumpstart(stack_loc_, this, &(parent_stack_)); // Returns here after first yield / final return if (PER_CPU(main_) == this)`
  - `api/kernel/timers.hpp:L41-L45`：关键词命中
    代码片段：`static id_t periodic(duration_t period, handler_t); static id_t periodic(duration_t when, duration_t period, handler_t); // un-schedule timer, and free it static void stop(id_t);`
  - `src/musl/sched_yield.cpp:L7-L11`：fn syscall_SYS_sched_yield
    代码片段：`extern "C" long syscall_SYS_sched_yield() { return stubtrace(sys_sched_yield, "sched_yield"); }`

### 相关符号

`fn syscall_SYS_sched_yield` at `src/musl/sched_yield.cpp:L7`、`fn pthread_join` at `src/posix/pthread.cpp:L39`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）
  - 相关符号包括：class Memory_exception, fn active_page_size, class Pmr_pool, class Pmr_resource, fn on_non_full。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/kernel/heap.cpp` | L29-L33 | 关键词命中 |
| `api/kernel/memory.hpp` | L137-L141 | 关键词命中 |
| `src/drivers/heap_debugging.cpp` | L29-L33 | 关键词命中 |
| `api/kernel/memory.hpp` | L108-L112 | class Memory_exception |
| `api/kernel/memory.hpp` | L326-L330 | fn active_page_size |
| `api/mem/alloc/pmr.hpp` | L33-L37 | class Pmr_pool |

### 关键代码片段

  - `src/kernel/heap.cpp:L29-L33`：关键词命中
    代码片段：`size_t kernel::heap_usage() noexcept { return brk_bytes_used() + mmap_bytes_used();`
  - `api/kernel/memory.hpp:L137-L141`：关键词命中
    代码片段：`* The range must be a subset of a range mapped by a previous call to map. * The page sizes will be adjusted to match len as closely as possible, * creating new page tables as ne...`
  - `src/drivers/heap_debugging.cpp:L29-L33`：关键词命中
    代码片段：`extern void print_backtrace(); extern void* heap_begin; extern void* heap_end; static void safe_print_symbol(int N, void* addr);`
  - `api/kernel/memory.hpp:L108-L112`：class Memory_exception
    代码片段：`/** Exception class possibly used by various ::mem functions. **/ class Memory_exception : public std::runtime_error { using runtime_error::runtime_error; };`

### 相关符号

`class Memory_exception` at `api/kernel/memory.hpp:L108`、`fn active_page_size` at `api/kernel/memory.hpp:L326`、`class Pmr_pool` at `api/mem/alloc/pmr.hpp:L33`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：medium）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含系统调用入口或兼容层线索，但源码片段显示部分调用仍是 stub/未实现，应按接口线索而非完整系统调用实现解读。（置信度：medium）
  - 相关符号包括：fn syscall_n, macro syscall, macro SYS_lchown, macro SYS_getuid, macro SYS_getgid。（置信度：medium）
  - 静态识别到 100 个系统调用相关符号。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/musl/syscall_n.cpp` | L1-L5 | 关键词命中 |
| `deps/musl/patches/syscall.h` | L4-L8 | 关键词命中 |
| `src/arch/x86_64/syscall_entry.cpp` | L22-L26 | 关键词命中 |
| `src/musl/syscall_n.cpp` | L7-L11 | fn syscall_n |
| `deps/musl/patches/syscall.h` | L36-L40 | macro syscall |
| `deps/musl/patches/syscall.h` | L69-L73 | macro SYS_lchown |

### 关键代码片段

  - `src/musl/syscall_n.cpp:L1-L5`：关键词命中
    代码片段：`#include "stub.hpp" long syscall(long /*number*/) { return -ENOSYS;`
  - `deps/musl/patches/syscall.h:L4-L8`：关键词命中
    代码片段：`#include <features.h> #include <errno.h> #include <sys/syscall.h> #include "includeos_syscalls.h"`
  - `src/arch/x86_64/syscall_entry.cpp:L22-L26`：关键词命中
    代码片段：`uint64_t a4, uint64_t a5) { kprintf("<syscall entry> no %lu (a1=%#lx a2=%#lx a3=%#lx a4=%#lx a5=%#lx) \n", n, a1, a2, a3, a4, a5); os::panic("Syscalls are not implemented in Inc...`
  - `src/musl/syscall_n.cpp:L7-L11`：fn syscall_n
    代码片段：`extern "C" long syscall_n(long i) { return stubtrace(syscall, "syscall", i); }`

### 相关符号

`fn syscall_n` at `src/musl/syscall_n.cpp:L7`、`macro syscall` at `deps/musl/patches/syscall.h:L36`、`macro SYS_lchown` at `deps/musl/patches/syscall.h:L69`、`fn syscall_n` at `src/musl/syscall_n.cpp:L7`、`macro _INTERNAL_SYSCALL_H` at `deps/musl/patches/syscall.h:L1`、`macro __SYSCALL_LL_E` at `deps/musl/patches/syscall.h:L8`、`macro __SYSCALL_LL_O` at `deps/musl/patches/syscall.h:L11`、`macro SYSCALL_RLIM_INFINITY` at `deps/musl/patches/syscall.h:L15`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 文件系统

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含文件系统、VFS、inode、目录项或文件读写相关实现。（置信度：high）
  - 相关符号包括：class Path, struct MBR, struct partition, struct BPB, struct mbr。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/fs/fat.cpp` | L16-L20 | 关键词命中 |
| `src/fs/mbr.cpp` | L10-L14 | 关键词命中 |
| `src/fs/disk.cpp` | L18-L22 | 关键词命中 |
| `api/fs/fat.hpp` | L30-L34 | class Path |
| `api/fs/mbr.hpp` | L25-L29 | struct MBR |
| `api/fs/mbr.hpp` | L28-L32 | struct partition |

### 关键代码片段

  - `src/fs/fat.cpp:L16-L20`：关键词命中
    代码片段：`// limitations under the License. #include <fs/fat.hpp> #include <fs/fat_internal.hpp>`
  - `src/fs/mbr.cpp:L10-L14`：关键词命中
    代码片段：`return "Empty"; case 0x01: return "DOS 12-bit FAT"; case 0x02: return "XENIX root";`
  - `src/fs/disk.cpp:L18-L22`：关键词命中
    代码片段：`#include <fs/disk.hpp> #include <fs/mbr.hpp> #include <fs/fat.hpp> #include <cassert> #include <info>`
  - `api/fs/fat.hpp:L30-L34`：class Path
    代码片段：`namespace fs { class Path; struct FAT : public File_system`

### 相关符号

`class Path` at `api/fs/fat.hpp:L30`、`struct MBR` at `api/fs/mbr.hpp:L25`、`struct partition` at `api/fs/mbr.hpp:L28`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）
  - 相关符号包括：fn sys_sync, fn sys_syncfs, fn syscall_SYS_sync, fn syscall_SYS_syncfs。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `api/kernel/rng.hpp` | L26-L30 | 关键词命中 |
| `api/kernel/fiber.hpp` | L25-L29 | 关键词命中 |
| `src/fs/fat_async.cpp` | L47-L51 | 关键词命中 |
| `src/musl/sync.cpp` | L1-L5 | fn sys_sync |
| `src/musl/sync.cpp` | L5-L9 | fn sys_syncfs |
| `src/musl/sync.cpp` | L10-L14 | fn syscall_SYS_sync |

### 关键代码片段

  - `api/kernel/rng.hpp:L26-L30`：关键词命中
    代码片段：`#include <smp_utils> #ifdef INCLUDEOS_SMP_ENABLE #include <mutex> #endif`
  - `api/kernel/fiber.hpp:L25-L29`：关键词命中
    代码片段：`#ifdef INCLUDEOS_SMP_ENABLE #include <atomic> #endif`
  - `src/fs/fat_async.cpp:L47-L51`：关键词命中
    代码片段：`{ FS_PRINT("int_ls: sec=%u\n", sector); auto next = weak_next.lock(); device.read( sector,`
  - `src/musl/sync.cpp:L1-L5`：fn sys_sync
    代码片段：`#include "stub.hpp" static long sys_sync() { return 0; }`

### 相关符号

`fn sys_sync` at `src/musl/sync.cpp:L1`、`fn sys_syncfs` at `src/musl/sync.cpp:L5`、`fn syscall_SYS_sync` at `src/musl/sync.cpp:L10`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 中断与异常

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `interrupt` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含 trap、中断、异常或定时器处理逻辑。（置信度：high）
  - 相关符号包括：class Timer。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/drivers/ide.cpp` | L152-L156 | 关键词命中 |
| `api/kernel/cpuid.hpp` | L69-L73 | 关键词命中 |
| `api/kernel/fiber.hpp` | L33-L37 | 关键词命中 |
| `api/util/timer.hpp` | L28-L32 | class Timer |

### 关键代码片段

  - `src/drivers/ide.cpp:L152-L156`：关键词命中
    代码片段：`this->pci_iobase = pcidev.iobase(); /** IRQ initialization */ Events::get().subscribe(IDE_IRQN, {&IDE::irq_handler}); __arch_enable_legacy_irq(IDE_IRQN);`
  - `api/kernel/cpuid.hpp:L69-L73`：关键词命中
    代码片段：`MSR,               // Model Specific Registers PAE,               // Physical Address Extension MCE,               // Machine-Check Exception CX8,               // CMPXCHG8 Inst...`
  - `api/kernel/fiber.hpp:L33-L37`：关键词命中
    代码片段：`extern "C" void fiber_jumpstarter(Fiber* f); /** Exception: General error for fibers */ class Err_bad_fiber : public std::runtime_error { using runtime_error::runtime_error;`
  - `api/util/timer.hpp:L28-L32`：class Timer
    代码片段：`* */ class Timer { public: using id_t        = Timers::id_t;`

### 相关符号

`class Timer` at `api/util/timer.hpp:L28`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。（置信度：high）
  - 相关符号包括：fn current, fn autoreg, class PCI_Device, class IDE, class e1000。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/drivers/ide.cpp` | L17-L21 | 关键词命中 |
| `src/drivers/ide.hpp` | L31-L35 | 关键词命中 |
| `src/drivers/e1000.cpp` | L151-L155 | 关键词命中 |
| `src/drivers/ide.cpp` | L114-L118 | fn current |
| `src/drivers/ide.cpp` | L430-L434 | fn autoreg |
| `src/drivers/ide.hpp` | L28-L32 | class PCI_Device |

### 关键代码片段

  - `src/drivers/ide.cpp:L17-L21`：关键词命中
    代码片段：`/** *  Intel IDE Controller datasheet at : *  ftp://download.intel.com/design/intarch/datashts/29055002.pdf */`
  - `src/drivers/ide.hpp:L31-L35`：关键词命中
    代码片段：`} /** IDE device driver  */ class IDE : public hw::Writable_Block_device { public:`
  - `src/drivers/e1000.cpp:L151-L155`：关键词命中
    代码片段：`this->retrieve_hw_addr(); // SW reset device write_cmd(REG_CTRL, (1 << 26)); while (read_cmd(REG_CTRL) & (1 << 26)) {`
  - `src/drivers/ide.cpp:L114-L118`：fn current
    代码片段：`~workq_item() {} uint8_t* current() { return &buffer->at(position * IDE::SECTOR_SIZE); }`

### 相关符号

`fn current` at `src/drivers/ide.cpp:L114`、`fn autoreg` at `src/drivers/ide.cpp:L430`、`class PCI_Device` at `src/drivers/ide.hpp:L28`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 附录：核验摘要

- 关键结论数：16
- 含证据关键结论数：16（100.0%）
- 无效证据引用数：0
- 未确认结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
