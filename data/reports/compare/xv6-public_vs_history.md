# 项目比较报告

## 比较对象选择

本次分析将待评估仓库 **`xv6-public`**（以下称新项目）与两个历史样本进行横向比较，样本选择依据如下：

- **os-tutorial**（来源：架构参考样本）
  - 选择依据：score=8.08；同属 teaching-monolithic 风格；架构重合度 1.00；语言构成相似度 0.48；OS 维度重合度 0.29；代码规模接近度 0.99。
  - 该样本作为教学式单体内核的比对参照，有助于评估新项目在架构层面与教学样例的异同。

- **xv6-riscv**（来源：教学基线）
  - 选择依据：score=6.79；语言构成相似度 0.97；OS 维度重合度 1.00；代码规模接近度 0.84。
  - 该样本作为经典教学操作系统 xv6 的 RISC‑V 变体，与新项目同属 xv6 系列且功能维度高度重合，为判断复用与移植关系提供了直接基线。

## 功能重合与疑似重复证据

以下功能维度的重合均基于关键词检索命中的源码片段，仅表明双方均实现了同类机制，**不能直接视作代码抄袭**，需人工结合完整文件、架构设计及提交历史进一步复核。

### 与 os-tutorial 的功能重合线索

1. **设备驱动维度**
   - 新项目 `ide.c:L1-L3`、`kbd.c:L2-L6` 与 os-tutorial 的 `15-video-ports/kernel/kernel.c:L18-L22` 均包含驱动相关实现，提示双方在设备驱动层存在相似实现线索（需要人工复核）。

2. **中断与异常维度**
   - 新项目 `trap.c:L9-L13`、`mp.h:L50-L54` 与 os-tutorial 的 `20-interrupts-timer/kernel/kernel.c:L1-L3`、`20-interrupts-timer/drivers/keyboard.c:L1-L5` 均包含中断/异常处理机制，属于可复核的相似实现线索。

### 与 xv6-riscv 的功能重合线索

3. **设备驱动维度**
   - 新项目 `ide.c:L1-L3`、`kbd.c:L2-L6` 与 xv6-riscv 的 `kernel/uart.c:L1-L4`、`kernel/virtio.h:L1-L4` 均有驱动实现，轮廓相似但硬件平台不同，需人工甄别移植或复用关系。

4. **文件系统维度**
   - 新项目 `fs.c:L2-L6`、`fs.h:L7-L11` 与 xv6-riscv 的 `kernel/fs.c:L2-L6`、`kernel/fs.h:L6-L10` 文件注释、布局描述高度一致，提示核心文件系统结构可能存在直接传承，需结合完整实现复核。

5. **中断与异常维度**
   - 新项目 `trap.c:L9-L13`、`mp.h:L50-L54` 与 xv6-riscv 的 `kernel/plic.c:L6-L10`、`kernel/trap.c:L31-L35` 均为中断控制器及 trap 处理相关代码，属于跨架构相似线索，需要人工对照逻辑。

6. **内存管理维度**
   - 新项目 `vm.c:L9-L13`、`kalloc.c:L1-L4` 与 xv6-riscv 的 `kernel/vm.c:L10-L14`、`kernel/kalloc.c:L36-L40` 均涉及页表与物理内存分配器，关键变量名和功能描述相似，需复核具体实现差异。

7. **调度与任务管理维度**
   - 新项目 `proc.c:L5-L9`、`proc.h:L2-L6` 与 xv6-riscv 的 `kernel/proc.c:L4-L8`、`kernel/proc.h:L21-L25` 均有进程结构和 CPU 状态定义，类似顶层组织结构，需人工审查调度逻辑和上下文切换细节。

8. **同步机制维度**
   - 新项目 `fs.c:L16-L20`、`bio.c:L22-L26` 与 xv6-riscv 的 `kernel/fs.c:L15-L19`、`kernel/vm.c:L5-L9` 均使用 spinlock/sleeplock，头文件引用模式相近，属于可复核的实现线索。

9. **系统调用维度**
   - 新项目 `syscall.c:L6-L10` 与 xv6-riscv 的 `kernel/trap.c:L58-L62`、`kernel/syscall.c:L5-L9` 均包含系统调用入口处理，提示相似路径，需人工比对系统调用表和分发逻辑。

## 代码级相似线索检测

以下线索通过片段匹配、宏/结构体/符号同名、文件路径重合等方式检出，仅表明在命名、局部结构或文件组织上存在可复核的相似性，**不等同于代码抄袭裁定**，须由人工结合提交历史和完整代码上下文综合判断。

### 文件系统维度

- **片段相似度 1.00**：`dinode` 结构体域同名，`fs.h:L27-L31` 与 `kernel/fs.h:L29-L33` 均包含 `short type; short major;`，token 与结构完全一致。
- **片段相似度 0.84**：`superblock` 结构体域部分重合，`fs.h:L12-L16` 与 `kernel/fs.h:L11-L15` 共享 `uint size;`。
- **宏名重合**：`NELEM`、`CONSOLE`、`min`、`ROOTINO` 等 4 个同名宏（证据：`defs.h:L190` ↔ `kernel/defs.h:L185`；`file.h:L37` ↔ `kernel/file.h:L40`）。
- **结构体/类型重合**：`file`、`inode`、`devsw`、`superblock` 4 个结构体同名（证据：`file.h:L1` ↔ `kernel/file.h:L1`；`file.h:L13` ↔ `kernel/file.h:L17` 等）。
- **文件路径重合**：`fs.c` / `kernel/fs.c`、`fs.h` / `kernel/fs.h` 同名实现文件（证据：`fs.c:L2-L6` ↔ `kernel/fs.c:L2-L6`）。

### 内存管理维度

- **片段相似度 1.00**：`struct run` 定义完全相同，`kalloc.c:L14-L18` ↔ `kernel/kalloc.c:L15-L19`。
- **宏名重合**：`PGSIZE`、`PGROUNDUP`、`PGROUNDDOWN`、`PTE_W` 4 个宏同名（证据：`mmu.h:L85` ↔ `kernel/riscv.h:L352`；`mmu.h:L90` ↔ `kernel/riscv.h:L355`）。
- **结构体/类型重合**：`run`、`trapframe` 同名（证据：`kalloc.c:L16` ↔ `kernel/kalloc.c:L17`；`x86.h:L150` ↔ `kernel/proc.h:L40`）。
- **文件路径重合**：`vm.c` / `kernel/vm.c`、`kalloc.c` / `kernel/kalloc.c`（证据：`vm.c:L9-L13` ↔ `kernel/vm.c:L10-L14`；`kalloc.c:L1-L4` ↔ `kernel/kalloc.c:L36-L40`）。

### 调度与任务管理维度

- **片段相似度 0.74** (`struct cpu`)，token 和结构高度相似（`proc.h:L1-L4` ↔ `kernel/proc.h:L20-L24`）。
- **片段相似度 0.68**（同上结构体，但字段有差异）。
- **宏名重合**：`min`、`NPROC`、`NOFILE` 3 个同名宏（证据：`fs.c:L24` ↔ `kernel/fs.c:L24`；`param.h:L1` ↔ `kernel/param.h:L1`）。
- **结构体/类型重合**：`cpu`、`context`、`procstate`、`proc` 4 个结构体同名（证据：`proc.h:L2` ↔ `kernel/proc.h:L22`；`proc.h:L27` ↔ `kernel/proc.h:L2`）。
- **函数/符号名重合**：`swtch` 函数同名（`swtch.S:L10` ↔ `kernel/swtch.S:L9`）。

### 设备驱动维度

- **宏名重合**：`BACKSPACE`、`CONSOLE`、`NDEV`、`ROOTDEV` 4 个宏同名（证据：`console.c:L127` ↔ `kernel/console.c:L25`；`file.h:L37` ↔ `kernel/file.h:L40`）。

### 同步机制维度

- **宏名重合**：`min`、`BSIZE`、`IBLOCK`、`BBLOCK` 4 个宏同名（证据：`fs.c:L24` ↔ `kernel/fs.c:L24`；`fs.h:L6` ↔ `kernel/fs.h:L5`）。
- **结构体/类型重合**：`superblock`、`sleeplock`、`spinlock` 3 个结构体同名（证据：`fs.h:L14` ↔ `kernel/fs.h:L13`；`sleeplock.h:L2` ↔ `kernel/sleeplock.h:L2`）。

### 中断与异常维度

- **结构体/类型重合**：`trapframe` 同名（证据：`x86.h:L150` ↔ `kernel/proc.h:L40`）。
- **文件路径重合**：`trap.c` / `kernel/trap.c`、`vm.c` / `kernel/vm.c`（证据：`trap.c:L9-L13` ↔ `kernel/trap.c:L31-L35`）。

### 系统调用维度

- **宏名重合**：`NFILE`、`ROOTDEV`、`FSSIZE`、`SYS_fork` 4 个宏同名（证据：`param.h:L5` ↔ `kernel/param.h:L4`；`param.h:L8` ↔ `kernel/param.h:L7`）。
- **结构体/类型重合**：`trapframe` 同名（同上）。

## 相似点

- 新项目与 **os-tutorial** 同属 teaching-monolithic 风格。
- 两者均具有设备驱动、中断与异常等维度的可确认实现，可在这些方向上进行人工对比。
- 新项目与 **xv6-riscv** 在设备驱动、文件系统、中断与异常、内存管理、调度与任务管理、同步机制、系统调用等 7 个经典 OS 维度均有实现，体现高度功能重合。
- 两两样本间在上述维度的源码文件均存在关键词命中，可作为进一步人工复核的重点线索。

## 差异点

- **语言构成差异**：新项目为 `{'json': 18, 'c': 9405, 'asm': 373, 'build': 286}`，而 os-tutorial 包含较多 Markdown 和汇编（`{'markdown': 1418, 'asm': 4100, 'c': 4193}`），反映教程性质更强。
- 与 xv6-riscv 相比，新项目 C 代码量略少（9405 vs 11718），且汇编占比略高，可能与 x86 架构相关（`{'asm': 373}` vs `{'asm': 276}`）。

## 可能创新点

以下诸项均基于与 **os-tutorial** 的对比，该样本未确认对应维度，而新项目具备实现证据。由于置信度标记为 `low`，且 xv6-riscv 已覆盖这些维度，故这些点不宜直接标定为原创创新，需人工审查后判定其独立贡献。

1. **文件系统**：新项目 `fs.c:L2-L6`、`fs.h:L7-L11` 有完整磁盘布局注释和文件系统实现，os-tutorial 未确认提供。
2. **内存管理**：新项目 `vm.c:L9-L13`、`kalloc.c:L1-L4` 包含页表和物理页分配器，os-tutorial 未确认。
3. **调度与任务管理**：新项目 `proc.c:L5-L9`、`proc.h:L2-L6` 有进程结构体和 CPU 状态定义，os-tutorial 未确认。
4. **同步机制**：新项目 `fs.c:L16-L20`、`bio.c:L22-L26` 使用 spinlock/sleeplock，os-tutorial 未确认。

## 待人工复核项

- 功能重合、路径/符号重合和片段级相似度只能作为可复核线索，不构成抄袭裁定；需要人工结合完整源码、提交历史和实现语义复核。

## 核验摘要

- 关键结论数：47
- 含证据关键结论数：47（100.0%）
- 无效证据引用数：0
- 未确认关键结论数：0
- 统计口径：关键结论指需要源码证据支撑的设计判断；证据率只统计关键设计判断。
- 来源：本节由本地 self-check 根据结构化证据自动补全。
