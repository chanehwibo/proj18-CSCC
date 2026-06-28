# Moca-Mola proj207 new-os 比较报告

- 对比历史仓库：Little Kernel
- 生成时间：2026-06-28T12:59:33.998495+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- Little Kernel（来源：架构参考样本）：画像相似度 score=6.27；架构重合度 0.33; 语言构成相似度 0.93; OS 维度重合度 0.86; 代码规模接近度 0.32

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 Little Kernel 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/drivers/device/sd.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/spi.hpp" namespace Driver::Device { using HAL::STM32F4xx::SPI_t;`
  - `src/drivers/device/led.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/gpio.hpp" namespace Driver::Device { using HAL::STM32F4xx::GPIO_t;`
  - `external/platform/nrfx/drivers/nrfx_common.h:L231-L235`：关键词命中
    代码片段：`typedef void (* nrfx_irq_handler_t)(void); /** @brief Driver state. */ typedef enum {`
  - `external/platform/nrfx/drivers/nrfx_errors.h:L46-L50`：关键词命中
    代码片段：`#define NRFX_ERROR_BASE_NUM         0x0BAD0000 /** @brief Base number of driver error codes. */ #define NRFX_ERROR_DRIVERS_BASE_NUM (NRFX_ERROR_BASE_NUM + 0x10000)`
- 与 Little Kernel 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/user/fatfs/ff.h:L1-L4`：关键词命中
    代码片段：`/*---------------------------------------------------------------------------/ /  FatFs - FAT file system module include R0.11a    (C)ChaN, 2015 /-------------------------------...`
  - `src/user/fatfs/ff.cpp:L1-L4`：关键词命中
    代码片段：`/*----------------------------------------------------------------------------/ /  FatFs - FAT file system module  R0.11a                (C)ChaN, 2015        / /----------------...`
  - `lib/fs/ext2/io.c:L76-L80`：关键词命中
    代码片段：`// This function returns a pointer to the cache block that corresponds to the indirect block pointer. static int ext2_get_indirect_block_pointer_cache_block(ext2_t *ext2, struct...`
  - `lib/fs/fat/dir.h:L18-L22`：关键词命中
    代码片段：`struct fat_dir_cookie; // Convert UTF-8 to UCS-2 for FAT LFN handling. // Returns NO_ERROR on success, ERR_INVALID_ARGS for malformed/unrepresentable UTF-8, // and ERR_TOO_BIG i...`
- 与 Little Kernel 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L34-L38`：关键词命中
    代码片段：`down() { // Assert if irq disabled MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard;`
  - `src/mos/kernel/task.hpp:L101-L105`：关键词命中
    代码片段：`terminate(TcbPtr_t tcb = current()) { MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard; if (tcb == nullptr || tcb->is_status(TERMINATED))`
  - `kernel/timer.c:L9-L13`：关键词命中
    代码片段：`/** * @file * @brief  Kernel timer subsystem * @defgroup timer Timers *`
  - `kernel/include/kernel/timer.h:L11-L15`：关键词命中
    代码片段：`#include <stdint.h> // This file defines the timer API for the LK kernel. // Timers are used to schedule callbacks to occur at a specific time in the future.`
- 与 Little Kernel 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `vendor/Driver/inc/stm32f4xx_qspi.h:L386-L390`：关键词命中
    代码片段：`#define QSPI_PMM_AND                 ((uint32_t)0x00000000) #define QSPI_PMM_OR                  ((uint32_t)QUADSPI_CR_PMM) #define IS_QSPI_PMM(PMM)      (((PMM) == QSPI_PMM_AND...`
  - `vendor/Driver/src/stm32f4xx_qspi.c:L353-L357`：关键词命中
    代码片段：`/* OR Match Mode */ { /* Set the PMM bit */ QUADSPI->CR |= QUADSPI_CR_PMM; }`
  - `kernel/vm/vm.c:L57-L61`：关键词命中
    代码片段：`LTRACE_ENTRY; /* allow the vmm a shot at initializing some of its data structures */ vmm_init_preheap();`
  - `kernel/vm/pmm.c:L500-L504`：关键词命中
    代码片段：`STATIC_COMMAND_START #if LK_DEBUGLEVEL > 0 STATIC_COMMAND("pmm", "physical memory manager", &cmd_pmm) #endif STATIC_COMMAND_END(pmm);`
- 与 Little Kernel 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/task.hpp:L7-L11`：关键词命中
    代码片段：`#include "alloc.hpp" namespace MOS::Kernel::Task { using namespace Global;`
  - `src/mos/kernel/ipc.hpp:L3-L7`：关键词命中
    代码片段：`#include "data_type/queue.hpp" #include "task.hpp" namespace MOS::Kernel::IPC`
  - `kernel/thread.c:L13-L17`：关键词命中
    代码片段：`* This file is the core kernel threading interface. * * @defgroup thread Threads * @{ */`
  - `kernel/include/kernel/thread.h:L9-L13`：关键词命中
    代码片段：`#include <arch/defines.h> #include <arch/ops.h> #include <arch/thread.h> #include <arch/arch_ops.h> #include <kernel/spinlock.h>`
- 与 Little Kernel 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L88-L92`：关键词命中
    代码片段：`MOS_ASSERT( owner != Task::current(), "Non-recursive lock" ); owner = Task::current();`
  - `src/mos/kernel/data_type/tcb.hpp:L155-L159`：关键词命中
    代码片段：`} MOS_INLINE inline void // Used in Mutex store_pri(Prior_t new_pri) volatile {`
  - `kernel/mutex.c:L10-L14`：关键词命中
    代码片段：`/** * @file * @brief  Mutex functions * * @defgroup mutex Mutex`
  - `kernel/semaphore.c:L1-L3`：关键词命中
    代码片段：`/* semaphore.c * * Copyright 2012 Christopher Anderson <chris@nullcode.org>`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 未发现达到阈值的路径、符号、结构体/宏或片段级代码相似线索；当前仅保留功能维度重合证据。

## 相似点

- 与 Little Kernel 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/device/sd.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/spi.hpp" namespace Driver::Device { using HAL::STM32F4xx::SPI_t;`
  - `src/drivers/device/led.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/gpio.hpp" namespace Driver::Device { using HAL::STM32F4xx::GPIO_t;`
- 与 Little Kernel 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/user/fatfs/ff.h:L1-L4`：关键词命中
    代码片段：`/*---------------------------------------------------------------------------/ /  FatFs - FAT file system module include R0.11a    (C)ChaN, 2015 /-------------------------------...`
  - `src/user/fatfs/ff.cpp:L1-L4`：关键词命中
    代码片段：`/*----------------------------------------------------------------------------/ /  FatFs - FAT file system module  R0.11a                (C)ChaN, 2015        / /----------------...`
- 与 Little Kernel 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L34-L38`：关键词命中
    代码片段：`down() { // Assert if irq disabled MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard;`
  - `src/mos/kernel/task.hpp:L101-L105`：关键词命中
    代码片段：`terminate(TcbPtr_t tcb = current()) { MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard; if (tcb == nullptr || tcb->is_status(TERMINATED))`
- 与 Little Kernel 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `vendor/Driver/inc/stm32f4xx_qspi.h:L386-L390`：关键词命中
    代码片段：`#define QSPI_PMM_AND                 ((uint32_t)0x00000000) #define QSPI_PMM_OR                  ((uint32_t)QUADSPI_CR_PMM) #define IS_QSPI_PMM(PMM)      (((PMM) == QSPI_PMM_AND...`
  - `vendor/Driver/src/stm32f4xx_qspi.c:L353-L357`：关键词命中
    代码片段：`/* OR Match Mode */ { /* Set the PMM bit */ QUADSPI->CR |= QUADSPI_CR_PMM; }`
- 与 Little Kernel 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/task.hpp:L7-L11`：关键词命中
    代码片段：`#include "alloc.hpp" namespace MOS::Kernel::Task { using namespace Global;`
  - `src/mos/kernel/ipc.hpp:L3-L7`：关键词命中
    代码片段：`#include "data_type/queue.hpp" #include "task.hpp" namespace MOS::Kernel::IPC`
- 与 Little Kernel 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L88-L92`：关键词命中
    代码片段：`MOS_ASSERT( owner != Task::current(), "Non-recursive lock" ); owner = Task::current();`
  - `src/mos/kernel/data_type/tcb.hpp:L155-L159`：关键词命中
    代码片段：`} MOS_INLINE inline void // Used in Mutex store_pri(Prior_t new_pri) volatile {`
- 与 Little Kernel 在 driver, filesystem, interrupt, memory, scheduler, sync 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 Little Kernel 的语言构成不同：待测作品为 {'json': 18, 'markdown': 2336, 'cpp': 12727, 'c': 165504, 'asm': 995}，历史样本为 {'json': 413, 'markdown': 3057, 'make': 6936, 'yaml': 161, 'c': 1521345, 'text': 752, 'build': 642, 'toml': 4, 'rust': 1047, 'asm': 42640, 'cpp': 20341}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：12
- 含证据关键结论数：12（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
