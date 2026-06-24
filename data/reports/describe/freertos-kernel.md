# FreeRTOS-Kernel 项目描述报告

## 基本信息

- 仓库 ID：`freertos-kernel`
- 风格：rtos
- 架构：arm, riscv, x86
- 样本来源等级：架构参考样本
- 文件数：818
- 代码/文本行数：407694
- 主要语言：c 347068 LOC, asm 52939 LOC, text 4801 LOC, build 1833 LOC, markdown 998 LOC

## 总览

FreeRTOS-Kernel 是一个 rtos 风格的小型操作系统相关仓库，主要语言统计为 c: 347068 LOC, asm: 52939 LOC, text: 4801 LOC, build: 1833 LOC。仓库包含 818 个已扫描文件、约 407694 行可分析文本，当前抽取到 28729 个符号定义。

## 摘要评分

- 综合成熟度：B 级：主要机制较完整（78/100）
- 已确认 OS 维度：5/7；高置信维度：4/7
- 构建入口：已确认；证据健康度：100.0% 覆盖率；无效证据引用：0
- 评分口径：该分数由本地静态分析、源码证据和 self-check 派生，不代表比赛官方评分，也不调用 LLM。

| 评分项 | 得分 | 依据 |
| --- | --- | --- |
| OS 机制覆盖 | 58/80 | 调度、内存、系统调用、文件系统、同步、中断、驱动等维度的确认情况 |
| 构建入口 | 10/10 | 是否识别到 Makefile、Cargo.toml、CMakeLists.txt 等构建入口 |
| 证据健康度 | 10/10 | 关键结论证据覆盖率与无效证据引用数 |

| OS 维度 | 状态 | 置信度 | 证据数 |
| --- | --- | --- | --- |
| 调度与任务管理 | 已确认 | high | 4 |
| 内存管理 | 已确认 | high | 5 |
| 系统调用 | 已确认 | medium | 6 |
| 文件系统 | 未确认 | unconfirmed | 0 |
| 同步机制 | 已确认 | high | 4 |
| 中断与异常 | 已确认 | high | 4 |
| 设备驱动 | 未确认 | unconfirmed | 0 |

## 构建系统

- 仓库包含构建入口：CMakeLists.txt, include/CMakeLists.txt, portable/CMakeLists.txt, portable/ThirdParty/GCC/RP2040/CMakeLists.txt, examples/cmake_example/CMakeLists.txt。（置信度：high）
  证据：
  - `CMakeLists.txt:L1-L3`：构建入口
    代码片段：`cmake_minimum_required(VERSION 3.15) # User is responsible to one mandatory option:`
  - `include/CMakeLists.txt:L1-L3`：构建入口
    代码片段：`# FreeRTOS internal cmake file. Do not use it in user top-level project add_library(freertos_kernel_include INTERFACE)`
  - `portable/CMakeLists.txt:L1-L3`：构建入口
    代码片段：`if( FREERTOS_PORT STREQUAL "GCC_RISC_V_GENERIC" ) include( GCC/RISC-V/chip_extensions.cmake ) endif()`
  - `portable/ThirdParty/GCC/RP2040/CMakeLists.txt:L1-L3`：构建入口
    代码片段：`cmake_minimum_required(VERSION 3.13) if (NOT TARGET _FreeRTOS_kernel_inclusion_marker)`
  - `examples/cmake_example/CMakeLists.txt:L1-L3`：构建入口
    代码片段：`cmake_minimum_required(VERSION 3.15) project(example)`

## 调度与任务管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `scheduler` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含任务/线程管理与调度相关实现。（置信度：high）
  - 相关符号包括：macro xTaskCreate。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `portable/WizC/PIC18/Drivers/Tick/Tick.c` | L39-L43 | 关键词命中 |
| `portable/WizC/PIC18/Drivers/Tick/isrTick.c` | L31-L35 | 关键词命中 |
| `tasks.c` | L32-L36 | 关键词命中 |
| `include/mpu_wrappers.h` | L98-L102 | macro xTaskCreate |

### 关键代码片段

  - `portable/WizC/PIC18/Drivers/Tick/Tick.c:L39-L43`：关键词命中
    代码片段：`#include <FreeRTOS.h> #include <task.h> /* IO port constants. */`
  - `portable/WizC/PIC18/Drivers/Tick/isrTick.c:L31-L35`：关键词命中
    代码片段：`+ ISRcode pulled inline to reduce stack-usage. + Added functionality to only call vTaskSwitchContext() once when handling multiple interruptsources in a single interruptcall.`
  - `tasks.c:L32-L36`：关键词命中
    代码片段：`#include <string.h> /* Defining MPU_WRAPPERS_INCLUDED_FROM_API_FILE prevents task.h from redefining * all the API functions to use the MPU wrappers.  That should only be done wh...`
  - `include/mpu_wrappers.h:L98-L102`：macro xTaskCreate
    代码片段：`#endif /* #if ( configUSE_MPU_WRAPPERS_V1 == 1 ) */ #define xTaskCreate                              MPU_xTaskCreate #define xTaskCreateStatic                        MPU_xTaskCr...`

### 相关符号

`macro xTaskCreate` at `include/mpu_wrappers.h:L98`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 内存管理

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `memory` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。（置信度：high）
  - 相关符号包括：macro pvPortMalloc, macro vPortFree。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `portable/MemMang/heap_1.c` | L29-L33 | 关键词命中 |
| `portable/MemMang/heap_2.c` | L28-L32 | 关键词命中 |
| `portable/MemMang/heap_3.c` | L29-L33 | 关键词命中 |
| `portable/ThirdParty/GCC/Xtensa_ESP32/include/portmacro.h` | L476-L480 | macro pvPortMalloc |
| `portable/ThirdParty/GCC/Xtensa_ESP32/include/portmacro.h` | L477-L481 | macro vPortFree |

### 关键代码片段

  - `portable/MemMang/heap_1.c:L29-L33`：关键词命中
    代码片段：`/* * The simplest possible implementation of pvPortMalloc().  Note that this * implementation does NOT allow allocated memory to be freed again. *`
  - `portable/MemMang/heap_2.c:L28-L32`：关键词命中
    代码片段：`/* * A sample implementation of pvPortMalloc() and vPortFree() that permits * allocated blocks to be freed, but does not combine adjacent free blocks * into a single larger bloc...`
  - `portable/MemMang/heap_3.c:L29-L33`：关键词命中
    代码片段：`/* * Implementation of pvPortMalloc() and vPortFree() that relies on the * compilers own malloc() and free() implementations. *`
  - `portable/ThirdParty/GCC/Xtensa_ESP32/include/portmacro.h:L476-L480`：macro pvPortMalloc
    代码片段：`* pvPortMalloc()/vPortFree(). */ #define pvPortMalloc                       heap_caps_malloc_default #define vPortFree                          heap_caps_free #define xPortGetFr...`

### 相关符号

`macro pvPortMalloc` at `portable/ThirdParty/GCC/Xtensa_ESP32/include/portmacro.h:L476`、`macro vPortFree` at `portable/ThirdParty/GCC/Xtensa_ESP32/include/portmacro.h:L477`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 系统调用

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：medium）
- 分析口径：本维度主要关注 `syscall` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 相关符号包括：macro SYS_MODE。（置信度：medium）
  - 静态识别到 37 个系统调用相关符号。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `portable/GCC/ARM_CRx_MPU/portmacro_asm.h` | L85-L89 | macro SYS_MODE |
| `include/mpu_syscall_numbers.h` | L28-L32 | macro MPU_SYSCALL_NUMBERS_H |
| `portable/GCC/TriCore_1782/port.c` | L62-L66 | macro portSYSCALL_TRAP |
| `portable/GCC/ARM_CR82/portmacro.h` | L327-L331 | macro portUNPRIVILEGED_SYSCALLS_REGION |
| `portable/GCC/TriCore_1782/portmacro.h` | L112-L116 | macro portSYSCALL_TASK_YIELD |
| `portable/GCC/TriCore_1782/portmacro.h` | L113-L117 | macro portSYSCALL_RAISE_PRIORITY |

### 关键代码片段

  - `portable/GCC/ARM_CRx_MPU/portmacro_asm.h:L85-L89`：macro SYS_MODE
    代码片段：`#define HYP_MODE    0x1AU #define UND_MODE    0x1BU #define SYS_MODE    0x1FU /**`
  - `include/mpu_syscall_numbers.h:L28-L32`：macro MPU_SYSCALL_NUMBERS_H
    代码片段：`#ifndef MPU_SYSCALL_NUMBERS_H #define MPU_SYSCALL_NUMBERS_H /* Numbers assigned to various system calls. */`
  - `portable/GCC/TriCore_1782/port.c:L62-L66`：macro portSYSCALL_TRAP
    代码片段：`/* OS Interrupt and Trap mechanisms. */ #define portRESTORE_PSW_MASK                            ( ~( 0x000000FFUL ) ) #define portSYSCALL_TRAP                                ( 6...`
  - `portable/GCC/ARM_CR82/portmacro.h:L327-L331`：macro portUNPRIVILEGED_SYSCALLS_REGION
    代码片段：`#define portPRIVILEGED_FLASH_REGION                  ( 0ULL )                                /* Privileged flash region number. */ #define portUNPRIVILEGED_FLASH_REGION...`

### 相关符号

`macro SYS_MODE` at `portable/GCC/ARM_CRx_MPU/portmacro_asm.h:L85`、`macro MPU_SYSCALL_NUMBERS_H` at `include/mpu_syscall_numbers.h:L28`、`macro portSYSCALL_TRAP` at `portable/GCC/TriCore_1782/port.c:L62`、`macro portUNPRIVILEGED_SYSCALLS_REGION` at `portable/GCC/ARM_CR82/portmacro.h:L327`、`macro portSYSCALL_TASK_YIELD` at `portable/GCC/TriCore_1782/portmacro.h:L112`、`macro portSYSCALL_RAISE_PRIORITY` at `portable/GCC/TriCore_1782/portmacro.h:L113`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 文件系统

- 结论：未确认该维度存在可追溯实现线索。（综合置信度：unconfirmed）
- 分析口径：本维度主要关注 `filesystem` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：当前未在核心源码路径中确认 文件系统 的实现证据。

### 证据表

| 证据 | 说明 |
| --- | --- |
| 未确认 | 当前未找到可引用的源码证据 |

### 复核建议

- 建议人工补查目录命名不典型的源码文件，或在后续版本中扩展该维度关键词。

## 同步机制

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `sync` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含锁、信号量或原子操作等同步机制。（置信度：high）
  - 相关符号包括：fn spin_try_lock_unsafe。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `list.c` | L182-L186 | 关键词命中 |
| `queue.c` | L56-L60 | 关键词命中 |
| `include/list.h` | L66-L70 | 关键词命中 |
| `portable/ThirdParty/GCC/RP2040/include/portmacro.h` | L209-L213 | fn spin_try_lock_unsafe |

### 关键代码片段

  - `list.c:L182-L186`：关键词命中
    代码片段：`*      the scheduler is suspended, or calling an API function that does *      not end in "FromISR" from an interrupt. *   4) Using a queue or semaphore before it has been initi...`
  - `queue.c:L56-L60`：关键词命中
    代码片段：`/* When the Queue_t structure is used to represent a base queue its pcHead and * pcTail members are used as pointers into the queue storage area.  When the * Queue_t structure i...`
  - `include/list.h:L66-L70`：关键词命中
    代码片段：`* The list structure members are modified from within interrupts, and therefore * by rights should be declared volatile.  However, they are only modified in a * functionally ato...`
  - `portable/ThirdParty/GCC/RP2040/include/portmacro.h:L209-L213`：fn spin_try_lock_unsafe
    代码片段：`#if PICO_SDK_VERSION_MAJOR < 2 __force_inline static bool spin_try_lock_unsafe(spin_lock_t *lock) { return *lock; }`

### 相关符号

`fn spin_try_lock_unsafe` at `portable/ThirdParty/GCC/RP2040/include/portmacro.h:L209`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 中断与异常

- 结论：已确认该维度存在可追溯实现线索。（综合置信度：high）
- 分析口径：本维度主要关注 `interrupt` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：
  - 项目包含 trap、中断、异常或定时器处理逻辑。（置信度：high）
  - 相关符号包括：macro interrupt。（置信度：medium）

### 证据表

| 文件 | 行号 | 说明 |
| --- | --- | --- |
| `portable/WizC/PIC18/Drivers/Tick/Tick.c` | L76-L80 | 关键词命中 |
| `portable/WizC/PIC18/Drivers/Tick/isrTick.c` | L41-L45 | 关键词命中 |
| `portable/GCC/RL78/isr_support.h` | L64-L68 | 关键词命中 |
| `portable/GCC/MSP430F449/portmacro.h` | L122-L126 | macro interrupt |

### 关键代码片段

  - `portable/WizC/PIC18/Drivers/Tick/Tick.c:L76-L80`：关键词命中
    代码片段：`/* * Setup a timer for a regular tick. */ void portSetupTick( void )`
  - `portable/WizC/PIC18/Drivers/Tick/isrTick.c:L41-L45`：关键词命中
    代码片段：`/* * ISR for the tick. * This increments the tick count and, if using the preemptive scheduler, * performs a context switch.  This must be identical to the manual`
  - `portable/GCC/RL78/isr_support.h:L64-L68`：关键词命中
    代码片段：`PUSH DE PUSH HL /* Registers in bank 3 are for ISR use only so don't need saving. */ SEL RB0 /* Save the usCriticalNesting value. */`
  - `portable/GCC/MSP430F449/portmacro.h:L122-L126`：macro interrupt
    代码片段：`/* GCC used to define these but doesn't any more */ #define interrupt(vector) __attribute__((__interrupt__(vector))) #define wakeup __attribute__((__wakeup__))`

### 相关符号

`macro interrupt` at `portable/GCC/MSP430F449/portmacro.h:L122`

### 复核建议

- 建议人工检查上述代码片段所在文件，确认关键词命中是否确实对应完整机制，而不是仅出现名称或注释。

## 设备驱动

- 结论：未确认该维度存在可追溯实现线索。（综合置信度：unconfirmed）
- 分析口径：本维度主要关注 `driver` 相关的源码路径、符号定义和关键词证据；文档命中不直接作为实现证据。
- 设计判断：当前未在核心源码路径中确认 设备驱动 的实现证据。

### 证据表

| 证据 | 说明 |
| --- | --- |
| 未确认 | 当前未找到可引用的源码证据 |

### 复核建议

- 建议人工补查目录命名不典型的源码文件，或在后续版本中扩展该维度关键词。

## 附录：核验摘要

- 关键结论数：11
- 含证据关键结论数：11（100.0%）
- 无效证据引用数：0
- 未确认结论数：3
- 统计口径：关键结论指需要源码证据支撑的设计判断；语言构成、风格标签和汇总性描述不计入证据率。
