# Moca-Mola proj207 new-os 项目描述报告

## 基本信息

- 仓库 ID：`award2024-moca-mola-proj207`
- 风格：embedded-rtos
- 架构：arm
- 样本来源等级：已核验获奖案例（一等奖，来源：os-funtion-winners.md）
- 文件数：190
- 代码/文本行数：181580
- 主要语言：c 165504 LOC, cpp 12727 LOC, markdown 2336 LOC, asm 995 LOC, json 18 LOC

## 总览

Moca-Mola proj207 new-os 是一个 embedded-rtos 风格的小型操作系统相关仓库，主要语言统计为 c: 165504 LOC, cpp: 12727 LOC, markdown: 2336 LOC, asm: 995 LOC。仓库包含 190 个已扫描文件、约 181580 行可分析文本，当前抽取到 15575 个符号定义。

## 摘要评分

- 综合成熟度：B 级：主要机制较完整（78/100）
- 已确认 OS 维度：6/7；高置信维度：6/7
- 构建入口：未确认；证据健康度：100.0% 覆盖率；无效证据引用：0
- 评分口径：该分数由本地静态分析、源码证据和 self-check 派生，不代表比赛官方评分，也不调用 LLM。

| 评分项 | 得分 | 依据 |
| --- | --- | --- |
| OS 机制覆盖 | 68/80 | 调度、内存、系统调用、文件系统、同步、中断、驱动等维度的确认情况 |
| 构建入口 | 0/10 | 是否识别到 Makefile、Cargo.toml、CMakeLists.txt 等构建入口 |
| 证据健康度 | 10/10 | 关键结论证据覆盖率与无效证据引用数 |

| OS 维度 | 状态 | 置信度 | 证据数 |
| --- | --- | --- | --- |
| 调度与任务管理 | 已确认 | high | 3 |
| 内存管理 | 已确认 | high | 3 |
| 系统调用 | 未确认 | unconfirmed | 0 |
| 文件系统 | 已确认 | high | 3 |
| 同步机制 | 已确认 | high | 6 |
| 中断与异常 | 已确认 | high | 3 |
| 设备驱动 | 已确认 | high | 6 |

## 构建系统

- 未确认构建系统。（置信度：unconfirmed）

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/mos/kernel/task.hpp` | L7-L11 | 关键词命中 |
| `src/mos/kernel/ipc.hpp` | L3-L7 | 关键词命中 |
| `src/mos/kernel/printf.c` | L24-L28 | 关键词命中 |

### 关键代码片段

  - `src/mos/kernel/task.hpp:L7-L11`：关键词命中
    代码片段：`#include "alloc.hpp" namespace MOS::Kernel::Task { using namespace Global;`
  - `src/mos/kernel/ipc.hpp:L3-L7`：关键词命中
    代码片段：`#include "data_type/queue.hpp" #include "task.hpp" namespace MOS::Kernel::IPC`
  - `src/mos/kernel/printf.c:L24-L28`：关键词命中
    代码片段：`// // \brief Tiny printf, sprintf and (v)snprintf implementation, optimized for speed on //        embedded systems with a very limited resources. These routines are thread //...`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `vendor/Driver/inc/stm32f4xx_qspi.h` | L386-L390 | 关键词命中 |
| `vendor/Driver/src/stm32f4xx_qspi.c` | L353-L357 | 关键词命中 |
| `vendor/Init/keil_startup_stm32f429xx.s` | L46-L50 | 关键词命中 |

### 关键代码片段

  - `vendor/Driver/inc/stm32f4xx_qspi.h:L386-L390`：关键词命中
    代码片段：`#define QSPI_PMM_AND                 ((uint32_t)0x00000000) #define QSPI_PMM_OR                  ((uint32_t)QUADSPI_CR_PMM) #define IS_QSPI_PMM(PMM)      (((PMM) == QSPI_PMM_AND...`
  - `vendor/Driver/src/stm32f4xx_qspi.c:L353-L357`：关键词命中
    代码片段：`/* OR Match Mode */ { /* Set the PMM bit */ QUADSPI->CR |= QUADSPI_CR_PMM; }`
  - `vendor/Init/keil_startup_stm32f429xx.s:L46-L50`：关键词命中
    代码片段：`; </h> Heap_Size       EQU     0x00001000 AREA    HEAP, NOINIT, READWRITE, ALIGN=3`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：未确认该维度存在可追溯实现线索。（综合置信度：unconfirmed）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：当前未在核心源码路径中确认 系统调用 的实现证据。

### 证据表

| 证据 | 说明 |
| --- | --- |
| 未确认 | 当前未找到可引用的源码证据 |

### 复核建议

- 建议人工补查目录命名不典型的源码文件，或在后续版本中扩展该维度关键词。

## 文件系统

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含文件系统、VFS、inode、目录项或文件读写相关实现。（置信度：high）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/user/fatfs/ff.h` | L1-L4 | 关键词命中 |
| `src/user/fatfs/ff.cpp` | L1-L4 | 关键词命中 |
| `src/user/fatfs/ffconf.h` | L1-L4 | 关键词命中 |

### 关键代码片段

  - `src/user/fatfs/ff.h:L1-L4`：关键词命中
    代码片段：`/*---------------------------------------------------------------------------/ /  FatFs - FAT file system module include R0.11a    (C)ChaN, 2015 /-------------------------------...`
  - `src/user/fatfs/ff.cpp:L1-L4`：关键词命中
    代码片段：`/*----------------------------------------------------------------------------/ /  FatFs - FAT file system module  R0.11a                (C)ChaN, 2015        / /----------------...`
  - `src/user/fatfs/ffconf.h:L1-L4`：关键词命中
    代码片段：`/*---------------------------------------------------------------------------/ /  FatFs - FAT file system module configuration file  R0.11a (C)ChaN, 2015 /----------------------...`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）
  - 相关符号包括：fn Sema_t, fn Lock_t, fn Mutex_t, fn Barrier_t。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/mos/kernel/sync.hpp` | L88-L92 | 关键词命中 |
| `src/mos/kernel/data_type/tcb.hpp` | L155-L159 | 关键词命中 |
| `vendor/Driver/src/stm32f4xx_gpio.c` | L393-L397 | 关键词命中 |
| `src/mos/kernel/sync.hpp` | L28-L32 | fn Sema_t |
| `src/mos/kernel/sync.hpp` | L81-L85 | fn Lock_t |
| `src/mos/kernel/sync.hpp` | L271-L275 | fn Mutex_t |

### 关键代码片段

  - `src/mos/kernel/sync.hpp:L88-L92`：关键词命中
    代码片段：`MOS_ASSERT( owner != Task::current(), "Non-recursive lock" ); owner = Task::current();`
  - `src/mos/kernel/data_type/tcb.hpp:L155-L159`：关键词命中
    代码片段：`} MOS_INLINE inline void // Used in Mutex store_pri(Prior_t new_pri) volatile {`
  - `vendor/Driver/src/stm32f4xx_gpio.c:L393-L397`：关键词命中
    代码片段：`/** * @brief  Sets the selected data port bits. * @note   This functions uses GPIOx_BSRR register to allow atomic read/modify *         accesses. In this way, there is no risk o...`
  - `src/mos/kernel/sync.hpp:L28-L32`：fn Sema_t
    代码片段：`MOS_INLINE inline Sema_t(int32_t _cnt): cnt(_cnt) {} // 'P-opr'`

### 相关符号

`fn Sema_t` at `src/mos/kernel/sync.hpp:L28`、`fn Lock_t` at `src/mos/kernel/sync.hpp:L81`、`fn Mutex_t` at `src/mos/kernel/sync.hpp:L271`

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
| `src/mos/kernel/sync.hpp` | L34-L38 | 关键词命中 |
| `src/mos/kernel/task.hpp` | L101-L105 | 关键词命中 |
| `src/mos/kernel/scheduler.hpp` | L177-L181 | 关键词命中 |

### 关键代码片段

  - `src/mos/kernel/sync.hpp:L34-L38`：关键词命中
    代码片段：`down() { // Assert if irq disabled MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard;`
  - `src/mos/kernel/task.hpp:L101-L105`：关键词命中
    代码片段：`terminate(TcbPtr_t tcb = current()) { MOS_ASSERT(test_irq(), "Disabled Interrupt"); IntrGuard_t guard; if (tcb == nullptr || tcb->is_status(TERMINATED))`
  - `src/mos/kernel/scheduler.hpp:L177-L181`：关键词命中
    代码片段：`} namespace MOS::ISR { extern "C" {`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。（置信度：high）
  - 相关符号包括：fn as_output, fn set_high, fn set_low, fn get_raw, fn get_raw。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `src/drivers/device/sd.hpp` | L4-L8 | 关键词命中 |
| `src/drivers/device/led.hpp` | L4-L8 | 关键词命中 |
| `src/drivers/device/st7735s.hpp` | L4-L8 | 关键词命中 |
| `src/drivers/device/sd.hpp` | L163-L167 | fn as_output |
| `src/drivers/device/sd.hpp` | L164-L168 | fn set_high |
| `src/drivers/device/sd.hpp` | L165-L169 | fn set_low |

### 关键代码片段

  - `src/drivers/device/sd.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/spi.hpp" namespace Driver::Device { using HAL::STM32F4xx::SPI_t;`
  - `src/drivers/device/led.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/gpio.hpp" namespace Driver::Device { using HAL::STM32F4xx::GPIO_t;`
  - `src/drivers/device/st7735s.hpp:L4-L8`：关键词命中
    代码片段：`#include "../stm32f4xx/spi.hpp" namespace Driver::Device { using HAL::STM32F4xx::SPI_t;`
  - `src/drivers/device/sd.hpp:L163-L167`：fn as_output
    代码片段：`: port(GPIO_t::convert(port)), pin(pin) {} void as_output() { port.as_output(pin); } void set_high() { port.set_bits(pin); } void set_low() { port.reset_bits(pin); }`

### 相关符号

`fn as_output` at `src/drivers/device/sd.hpp:L163`、`fn set_high` at `src/drivers/device/sd.hpp:L164`、`fn set_low` at `src/drivers/device/sd.hpp:L165`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 附录：核验摘要

- 关键结论数：8
- 含证据关键结论数：8（100.0%）
- 无效证据引用数：0
- 未确认结论数：2
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
