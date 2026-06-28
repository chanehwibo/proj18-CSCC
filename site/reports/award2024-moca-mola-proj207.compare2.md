# Moca-Mola proj207 new-os 比较报告

- 对比历史仓库：2023 AVX
- 生成时间：2026-06-28T07:36:36.093422+00:00
- 参考库边界：只有带官方来源的 `verified_award` 样本才会被视为获奖案例；未核验比赛样本不作为特奖/一等奖背书。

## 历史样本选择

- 2023 AVX（来源：赛事历史作品）：画像相似度 score=6.05；语言构成相似度 0.92; OS 维度重合度 0.86; 代码规模接近度 0.77

## 功能重合与疑似重复证据

本节只说明功能维度和实现线索的重合，不直接判定代码抄袭。是否构成代码级重复，需要结合完整代码、提交历史和人工复核进一步确认。

- 与 2023 AVX 在“设备驱动”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/drivers/device/sd.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/spi.hpp" namespace Driver::Device { using HAL::STM32F4xx::SPI_t;`
  - `src/drivers/device/led.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/gpio.hpp" namespace Driver::Device { using HAL::STM32F4xx::GPIO_t;`
  - `kernel/uart.c:L1-L4`：关键词命中
    代码片段：`// // low-level driver routines for 16550a UART. //`
  - `kernel/console.c:L1-L4`：关键词命中
    代码片段：`// // Console input and output, to the uart. // Reads are line at a time. // Implements special input characters:`
- 与 2023 AVX 在“文件系统”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/user/fatfs/ff.h:L1-L4`：关键词命中
    代码片段：`/*---------------------------------------------------------------------------/ /  FatFs - FAT file system module include R0.11a    (C)ChaN, 2015 /-------------------------------...`
  - `src/user/fatfs/ff.cpp:L1-L4`：关键词命中
    代码片段：`/*----------------------------------------------------------------------------/ /  FatFs - FAT file system module  R0.11a                (C)ChaN, 2015        / /----------------...`
  - `kernel/file.c:L206-L210`：关键词命中
    代码片段：`// Read from file f. // addr is a user virtual address. int fileread(struct file *f, uint64 addr, int n) { int r = 0;`
  - `kernel/include/file.h:L68-L72`：关键词命中
    代码片段：`struct file*    filedup(struct file*); void            fileinit(void); int             fileread(struct file*, uint64, int n); int             filestat(struct file*, uint64 addr)...`
- 与 2023 AVX 在“中断与异常”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L34-L38`：关键词命中
    代码片段：`down() { // Assert if irq disabled MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard;`
  - `src/mos/kernel/task.hpp:L101-L105`：关键词命中
    代码片段：`terminate(TcbPtr_t tcb = current()) { MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard; if (tcb == nullptr || tcb->is_status(TERMINATED))`
  - `kernel/plic.c:L1-L4`：关键词命中
    代码片段：`#include "include/plic.h" #include "include/memlayout.h" #include "include/param.h"`
  - `kernel/trap.c:L1-L3`：关键词命中
    代码片段：`#include "include/trap.h" #include "include/console.h" #include "include/disk.h"`
- 与 2023 AVX 在“内存管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `vendor/Driver/inc/stm32f4xx_qspi.h:L386-L390`：关键词命中
    代码片段：`#define QSPI_PMM_AND                 ((uint32_t)0x00000000) #define QSPI_PMM_OR                  ((uint32_t)QUADSPI_CR_PMM) #define IS_QSPI_PMM(PMM)      (((PMM) == QSPI_PMM_AND...`
  - `vendor/Driver/src/stm32f4xx_qspi.c:L353-L357`：关键词命中
    代码片段：`/* OR Match Mode */ { /* Set the PMM bit */ QUADSPI->CR |= QUADSPI_CR_PMM; }`
  - `kernel/vm.c:L1-L5`：关键词命中
    代码片段：`#include "include/vm.h" #include "include/elf.h" #include "include/kalloc.h" #include "include/memlayout.h" #include "include/param.h"`
  - `kernel/kalloc.c:L3-L7`：关键词命中
    代码片段：`// and pipe buffers. Allocates whole 4096-byte pages. #include "include/kalloc.h" #include "include/memlayout.h" #include "include/param.h"`
- 与 2023 AVX 在“调度与任务管理”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/task.hpp:L7-L11`：关键词命中
    代码片段：`#include "alloc.hpp" namespace MOS::Kernel::Task { using namespace Global;`
  - `src/mos/kernel/ipc.hpp:L3-L7`：关键词命中
    代码片段：`#include "data_type/queue.hpp" #include "task.hpp" namespace MOS::Kernel::IPC`
  - `kernel/proc.c:L1-L4`：关键词命中
    代码片段：`#include "include/proc.h" #include "include/fat32.h" #include "include/file.h"`
  - `kernel/thread.c:L1-L3`：关键词命中
    代码片段：`#include "include/thread.h" #include "include/kalloc.h" #include "include/memlayout.h"`
- 与 2023 AVX 在“同步机制”维度存在功能重合：双方均有可追溯源码证据，属于需要重点复核的相似实现线索。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L88-L92`：关键词命中
    代码片段：`MOS_ASSERT( owner != Task::current(), "Non-recursive lock" ); owner = Task::current();`
  - `src/mos/kernel/data_type/tcb.hpp:L155-L159`：关键词命中
    代码片段：`} MOS_INLINE inline void // Used in Mutex store_pri(Prior_t new_pri) volatile {`
  - `kernel/bio.c:L21-L25`：关键词命中
    代码片段：`#include "include/sdcard.h" #include "include/sleeplock.h" #include "include/spinlock.h" #include "include/types.h"`
  - `kernel/sem.c:L2-L6`：关键词命中
    代码片段：`#include "include/printf.h" #include "include/proc.h" #include "include/spinlock.h" #include "include/timer.h" #include "include/types.h"`

## 代码级相似线索检测

本节从文件路径、函数/符号名、结构体/宏名和 evidence 片段 token/结构相似度四个层面输出可复核线索，并优先保留高价值代表项。该结果比功能重合更接近代码级分析，但仍不是抄袭裁定。

- 未发现达到阈值的路径、符号、结构体/宏或片段级代码相似线索；当前仅保留功能维度重合证据。

## 相似点

- 与 2023 AVX 在“设备驱动”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/drivers/device/sd.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/spi.hpp" namespace Driver::Device { using HAL::STM32F4xx::SPI_t;`
  - `src/drivers/device/led.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/gpio.hpp" namespace Driver::Device { using HAL::STM32F4xx::GPIO_t;`
- 与 2023 AVX 在“文件系统”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/user/fatfs/ff.h:L1-L4`：关键词命中
    代码片段：`/*---------------------------------------------------------------------------/ /  FatFs - FAT file system module include R0.11a    (C)ChaN, 2015 /-------------------------------...`
  - `src/user/fatfs/ff.cpp:L1-L4`：关键词命中
    代码片段：`/*----------------------------------------------------------------------------/ /  FatFs - FAT file system module  R0.11a                (C)ChaN, 2015        / /----------------...`
- 与 2023 AVX 在“中断与异常”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L34-L38`：关键词命中
    代码片段：`down() { // Assert if irq disabled MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard;`
  - `src/mos/kernel/task.hpp:L101-L105`：关键词命中
    代码片段：`terminate(TcbPtr_t tcb = current()) { MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard; if (tcb == nullptr || tcb->is_status(TERMINATED))`
- 与 2023 AVX 在“内存管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `vendor/Driver/inc/stm32f4xx_qspi.h:L386-L390`：关键词命中
    代码片段：`#define QSPI_PMM_AND                 ((uint32_t)0x00000000) #define QSPI_PMM_OR                  ((uint32_t)QUADSPI_CR_PMM) #define IS_QSPI_PMM(PMM)      (((PMM) == QSPI_PMM_AND...`
  - `vendor/Driver/src/stm32f4xx_qspi.c:L353-L357`：关键词命中
    代码片段：`/* OR Match Mode */ { /* Set the PMM bit */ QUADSPI->CR |= QUADSPI_CR_PMM; }`
- 与 2023 AVX 在“调度与任务管理”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/task.hpp:L7-L11`：关键词命中
    代码片段：`#include "alloc.hpp" namespace MOS::Kernel::Task { using namespace Global;`
  - `src/mos/kernel/ipc.hpp:L3-L7`：关键词命中
    代码片段：`#include "data_type/queue.hpp" #include "task.hpp" namespace MOS::Kernel::IPC`
- 与 2023 AVX 在“同步机制”维度均有可确认实现。（置信度：medium）
  证据：
  - `src/mos/kernel/sync.hpp:L88-L92`：关键词命中
    代码片段：`MOS_ASSERT( owner != Task::current(), "Non-recursive lock" ); owner = Task::current();`
  - `src/mos/kernel/data_type/tcb.hpp:L155-L159`：关键词命中
    代码片段：`} MOS_INLINE inline void // Used in Mutex store_pri(Prior_t new_pri) volatile {`
- 与 2023 AVX 在 driver, filesystem, interrupt, memory, scheduler, sync 等维度均有可确认实现，可作为进一步人工复核重点。（置信度：medium）

## 差异点

- 与 2023 AVX 的语言构成不同：新项目为 {'json': 18, 'markdown': 2336, 'cpp': 12727, 'c': 165504, 'asm': 995}，历史项目为 {'json': 20, 'build': 353, 'markdown': 1027, 'asm': 1663, 'c': 132010, 'make': 90, 'text': 2}。（置信度：medium）

## 可能创新点

- 未确认。

## 附录：核验摘要

- 关键结论数：12
- 含证据关键结论数：12（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
