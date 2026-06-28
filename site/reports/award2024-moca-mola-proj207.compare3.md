# Moca-Mola proj207 new-os 比较报告

- 对比历史仓库：2025 啊对的对的,嗷不对不对
- 生成时间：2026-06-28T12:08:06.441584+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2025 啊对的对的,嗷不对不对（来源：赛事历史作品）：画像相似度 score=5.97；语言构成相似度 0.95; OS 维度重合度 0.86; 代码规模接近度 0.64

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2025 啊对的对的,嗷不对不对 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/drivers/device/sd.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/spi.hpp" namespace Driver::Device { using HAL::STM32F4xx::SPI_t;`
  - `src/drivers/device/led.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/gpio.hpp" namespace Driver::Device { using HAL::STM32F4xx::GPIO_t;`
  - `kernel/mem/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/driver/bio.c:L23-L27`：关键词命中
    代码片段：`#include "fs/vfs/fs.h" #include "fs/buf.h" #include "dev/virtio.h" struct {`
- 与 2025 啊对的对的,嗷不对不对 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/user/fatfs/ff.h:L1-L4`：关键词命中
    代码片段：`/*---------------------------------------------------------------------------/ /  FatFs - FAT file system module include R0.11a    (C)ChaN, 2015 /-------------------------------...`
  - `src/user/fatfs/ff.cpp:L1-L4`：关键词命中
    代码片段：`/*----------------------------------------------------------------------------/ /  FatFs - FAT file system module  R0.11a                (C)ChaN, 2015        / /----------------...`
  - `kernel/fs/vfs/fs.c:L1-L3`：关键词命中
    代码片段：`#include "fs/vfs/fs.h" #include <defs.h>`
  - `kernel/fs/vfs/ops.c:L1-L3`：关键词命中
    代码片段：`#include "fs/vfs/ops.h" #include <fs/fcntl.h>`
- 与 2025 啊对的对的,嗷不对不对 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L34-L38`：关键词命中
    代码片段：`down() { // Assert if irq disabled MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard;`
  - `src/mos/kernel/task.hpp:L101-L105`：关键词命中
    代码片段：`terminate(TcbPtr_t tcb = current()) { MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard; if (tcb == nullptr || tcb->is_status(TERMINATED))`
  - `kernel/sys/plic.c:L4-L8`：关键词命中
    代码片段：`#include "platform.h" #include "defs.h" #include "proc/plic.h" //`
  - `kernel/trap/riscv/trap.c:L8-L12`：关键词命中
    代码片段：`#include "mem/mem.h" #include "sbi.h" #include "proc/plic.h" #include "dev/virtio.h"`
- 与 2025 啊对的对的,嗷不对不对 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `vendor/Driver/inc/stm32f4xx_qspi.h:L386-L390`：关键词命中
    代码片段：`#define QSPI_PMM_AND                 ((uint32_t)0x00000000) #define QSPI_PMM_OR                  ((uint32_t)QUADSPI_CR_PMM) #define IS_QSPI_PMM(PMM)      (((PMM) == QSPI_PMM_AND...`
  - `vendor/Driver/src/stm32f4xx_qspi.c:L353-L357`：关键词命中
    代码片段：`/* OR Match Mode */ { /* Set the PMM bit */ QUADSPI->CR |= QUADSPI_CR_PMM; }`
  - `kernel/mem/vm.c:L8-L12`：关键词命中
    代码片段：`#include "defs.h" #include "fs/vfs/fs.h" #include "mem/kalloc.h" #include "lib/string.h" #include "dev/virtio.h"`
  - `kernel/mem/kalloc.c:L9-L13`：关键词命中
    代码片段：`#include "platform.h" #include "defs.h" #include "mem/kalloc.h" #include <mem/slab.h>`
- 与 2025 啊对的对的,嗷不对不对 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/task.hpp:L7-L11`：关键词命中
    代码片段：`#include "alloc.hpp" namespace MOS::Kernel::Task { using namespace Global;`
  - `src/mos/kernel/ipc.hpp:L3-L7`：关键词命中
    代码片段：`#include "data_type/queue.hpp" #include "task.hpp" namespace MOS::Kernel::IPC`
  - `kernel/proc/exec.c:L4-L8`：关键词命中
    代码片段：`#include "platform.h" #include "lock/spinlock.h" #include "proc/proc.h" #include "defs.h" #include "lib/elf.h"`
  - `kernel/proc/pipe.c:L4-L8`：关键词命中
    代码片段：`#include "param.h" #include "lock/spinlock.h" #include "proc/proc.h" #include "lock/sleeplock.h" #include "fs/fcntl.h"`
- 与 2025 啊对的对的,嗷不对不对 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L88-L92`：关键词命中
    代码片段：`MOS_ASSERT( owner != Task::current(), "Non-recursive lock" ); owner = Task::current();`
  - `src/mos/kernel/data_type/tcb.hpp:L155-L159`：关键词命中
    代码片段：`} MOS_INLINE inline void // Used in Mutex store_pri(Prior_t new_pri) volatile {`
  - `kernel/proc/semaphore.c:L1-L4`：关键词命中
    代码片段：`#include "lock/semaphore.h" #include "defs.h"`
  - `kernel/mem/uart.c:L7-L11`：关键词命中
    代码片段：`#include "mem/memlayout.h" #include "platform.h" #include "lock/spinlock.h" #include "proc/proc.h" #include "defs.h"`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 未发现达到阈值的路径、符号、结构体/宏或片段级代码相似线索；当前仅保留功能维度重合证据。

## 相似点

- 与 2025 啊对的对的,嗷不对不对 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/device/sd.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/spi.hpp" namespace Driver::Device { using HAL::STM32F4xx::SPI_t;`
  - `src/drivers/device/led.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/gpio.hpp" namespace Driver::Device { using HAL::STM32F4xx::GPIO_t;`
- 与 2025 啊对的对的,嗷不对不对 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/user/fatfs/ff.h:L1-L4`：关键词命中
    代码片段：`/*---------------------------------------------------------------------------/ /  FatFs - FAT file system module include R0.11a    (C)ChaN, 2015 /-------------------------------...`
  - `src/user/fatfs/ff.cpp:L1-L4`：关键词命中
    代码片段：`/*----------------------------------------------------------------------------/ /  FatFs - FAT file system module  R0.11a                (C)ChaN, 2015        / /----------------...`
- 与 2025 啊对的对的,嗷不对不对 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L34-L38`：关键词命中
    代码片段：`down() { // Assert if irq disabled MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard;`
  - `src/mos/kernel/task.hpp:L101-L105`：关键词命中
    代码片段：`terminate(TcbPtr_t tcb = current()) { MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard; if (tcb == nullptr || tcb->is_status(TERMINATED))`
- 与 2025 啊对的对的,嗷不对不对 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `vendor/Driver/inc/stm32f4xx_qspi.h:L386-L390`：关键词命中
    代码片段：`#define QSPI_PMM_AND                 ((uint32_t)0x00000000) #define QSPI_PMM_OR                  ((uint32_t)QUADSPI_CR_PMM) #define IS_QSPI_PMM(PMM)      (((PMM) == QSPI_PMM_AND...`
  - `vendor/Driver/src/stm32f4xx_qspi.c:L353-L357`：关键词命中
    代码片段：`/* OR Match Mode */ { /* Set the PMM bit */ QUADSPI->CR |= QUADSPI_CR_PMM; }`
- 与 2025 啊对的对的,嗷不对不对 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/task.hpp:L7-L11`：关键词命中
    代码片段：`#include "alloc.hpp" namespace MOS::Kernel::Task { using namespace Global;`
  - `src/mos/kernel/ipc.hpp:L3-L7`：关键词命中
    代码片段：`#include "data_type/queue.hpp" #include "task.hpp" namespace MOS::Kernel::IPC`
- 与 2025 啊对的对的,嗷不对不对 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L88-L92`：关键词命中
    代码片段：`MOS_ASSERT( owner != Task::current(), "Non-recursive lock" ); owner = Task::current();`
  - `src/mos/kernel/data_type/tcb.hpp:L155-L159`：关键词命中
    代码片段：`} MOS_INLINE inline void // Used in Mutex store_pri(Prior_t new_pri) volatile {`
- 与 2025 啊对的对的,嗷不对不对 在 driver, filesystem, interrupt, memory, scheduler, sync 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2025 啊对的对的,嗷不对不对 的语言构成不同：新项目为 {'json': 18, 'markdown': 2336, 'cpp': 12727, 'c': 165504, 'asm': 995}，历史项目为 {'json': 20, 'build': 479, 'markdown': 1008, 'c': 280934, 'asm': 1166, 'text': 9, 'cpp': 36728}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：12
- 含证据关键结论数：12（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
