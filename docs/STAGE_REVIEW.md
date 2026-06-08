# KernelSage 阶段性评审材料

本文档整理当前 V1 MVP 的阶段性产出，用于和导师、队友或评审沟通项目进度。运行生成物仍保存在 `data/reports/` 下，默认不提交；本文档只记录可复现命令、关键输出和人工复核结论。

## 当前版本

- 日期：2026-06-08
- 阶段：V1 MVP 可演示阶段
- 演示样本：`data/samples/rcore-tutorial-v3`
- 对比数量：Top 2 历史样本

## 复现命令

```powershell
python scripts\kernelsage.py demo data\samples\rcore-tutorial-v3 --repo-id rcore-tutorial-v3 --limit 2
```

验证命令：

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
```

## 生成物

| 类型 | 路径 | 说明 |
| --- | --- | --- |
| 结构化画像 | `data/profiles/rcore-tutorial-v3.json` | KernelProfile 中间表示 |
| 描述报告 | `data/reports/describe/rcore-tutorial-v3.md` | 按 OS 维度组织的项目描述 |
| 比较报告 | `data/reports/compare/rcore-tutorial-v3_vs_history.md` | 与历史样本的相似点、差异点和可能创新点 |

上述文件属于运行生成物，不提交到仓库。

## 描述报告摘要

样本仓库 `rCore-Tutorial-v3` 的自动画像结果：

| 项目 | 结果 |
| --- | --- |
| 风格 | `rcore-variant` |
| 架构 | `riscv64` |
| 文件数 | 153 |
| 可分析行数 | 11873 |
| 主要语言 | Rust 11081 LOC、Markdown 314 LOC、Build 269 LOC、Asm 150 LOC |
| 抽取符号数 | 1002 |

已确认的 OS 维度：

| 维度 | 代表证据 |
| --- | --- |
| 调度与任务管理 | `os/src/task/id.rs:L1-L3`、`os/src/task/mod.rs:L2-L6`、`os/src/task/task.rs:L1-L3` |
| 内存管理 | `os/src/mm/mod.rs:L1-L4`、`os/src/mm/address.rs:L1-L3`、`os/src/mm/memory_set.rs:L1-L3` |
| 系统调用 | `os/src/trap/mod.rs:L2-L6`、`os/src/trap/trap.S:L7-L11`、`os/src/syscall/fs.rs:L4-L8` |
| 文件系统 | `os/src/fs/mod.rs:L1-L3`、`os/src/fs/pipe.rs:L1-L3`、`os/src/fs/inode.rs:L1-L3` |
| 同步机制 | `os/src/sync/mod.rs:L1-L3`、`os/src/sync/mutex.rs:L1-L4`、`os/src/sync/condvar.rs:L1-L3` |
| 中断与异常 | `os/src/timer.rs:L2-L6`、`os/src/trap/mod.rs:L4-L8`、`os/src/trap/trap.S:L7-L11` |
| 设备驱动 | `os/src/drivers/mod.rs:L1-L3`、`os/src/drivers/bus/mod.rs:L1-L1`、`os/src/drivers/gpu/mod.rs:L1-L3` |

描述报告 self-check：

| 指标 | 结果 |
| --- | --- |
| 关键结论数 | 16 |
| 含证据关键结论数 | 16 |
| 证据覆盖率 | 100.0% |
| 无效证据引用数 | 0 |
| 未确认结论数 | 0 |

## 比较报告摘要

历史样本选择结果：

| 历史样本 | 分数 | 选择依据 |
| --- | --- | --- |
| `zCore` | 10.34 | 同属 `rcore-variant` 风格，语言构成相似度 0.97，OS 维度重合度 1.00 |
| `xv6-riscv` | 7.03 | 同为 `riscv64` 架构，代码规模接近度 0.97，OS 维度重合度 1.00 |

比较结论：

- 与 `zCore` 在设备驱动、文件系统、中断与异常、内存管理、调度与任务管理、同步机制、系统调用等维度均有可确认实现。
- 与 `xv6-riscv` 在上述 7 个 OS 维度也均有可确认实现。
- 与 `zCore` 的主要差异是语言构成和规模不同：新项目 Rust 代码约 11081 LOC，历史项目 Rust 代码约 50074 LOC。
- 与 `xv6-riscv` 的主要差异是语言生态不同：新项目以 Rust 为主，`xv6-riscv` 以 C/Asm 为主。
- 当前规则报告未自动给出“可能创新点”，标记为“未确认”，保留给人工复核或 LLM 二阶段归纳。

比较报告 self-check：

| 指标 | 结果 |
| --- | --- |
| 关键结论数 | 14 |
| 含证据关键结论数 | 14 |
| 证据覆盖率 | 100.0% |
| 无效证据引用数 | 0 |
| 未确认结论数 | 0 |

## 人工复核结论

当前阶段输出符合 V1 MVP 目标：

- 能自动生成 OS 专用 7 维度画像。
- 能避免把 Markdown 文档当成 OS 机制实现证据。
- 能按画像相似度选择历史样本，而不是按目录顺序截断。
- 能输出可追溯源码证据和 self-check 摘要。
- 能保留不确定项，不强行编造创新点。

当前仍需改进：

- 规则报告的自然语言表达偏模板化。
- “可能创新点”仍需要 LLM 或人工二阶段归纳。
- 部分关键词命中仍偏粗粒度，例如只确认模块存在，不能完整说明算法细节。
- 后续需要增加更多历史比赛仓库，提高比较代表性。

## 后续建议

| 优先级 | 建议 |
| --- | --- |
| P1 | 让 LLM 在 evidence/self-check 约束下生成更自然的比较报告 |
| P1 | 固定一份人工审阅后的高质量样例报告用于答辩 |
| P1 | 增加 CLI demo 端到端测试 |
| P2 | 扩展历史样本到更多比赛作品 |
| P2 | 做轻量 HTML 展示页或报告索引页 |

## 对比库扩展记录

- 日期：2026-06-08
- 目标：补充真实比赛作品样本，避免对比库只包含教学基线项目。
- 样本规模：从 6 个基线仓库扩展到 10 个样本仓库。
- 新增样本类型：2024 操作系统比赛公开参赛仓库，统一标记为 `contest-case`。

新增样本：

| repo_id | 名称 | 本地状态 |
| --- | --- | --- |
| `oskernel2024-hfut666` | OSKernel2024-HFUT666 | 已拉取，HEAD `6f91d984` |
| `oskernel2024-aabcb` | OSKernel2024-aabcb | 已拉取，HEAD `d457fa2c` |
| `oskernel2024-nqos` | OSKernel2024-NQOS | 已拉取，HEAD `90724b9d` |
| `oskernel2024-ouye` | OSKernel2024-ouye | 已拉取，HEAD `be84a237` |

复现命令：

```powershell
python scripts\fetch_repos.py --only oskernel2024-hfut666 --only oskernel2024-aabcb --only oskernel2024-nqos --only oskernel2024-ouye
python scripts\kernelsage.py describe data\samples\oskernel2024-hfut666 --repo-id oskernel2024-hfut666
python scripts\kernelsage.py describe data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb
python scripts\kernelsage.py describe data\samples\oskernel2024-nqos --repo-id oskernel2024-nqos
python scripts\kernelsage.py describe data\samples\oskernel2024-ouye --repo-id oskernel2024-ouye
python scripts\kernelsage.py compare data\samples\oskernel2024-hfut666 --repo-id oskernel2024-hfut666 --limit 4
```

本轮保留的报告：

| 类型 | 路径 |
| --- | --- |
| 描述报告 | `data/reports/describe/oskernel2024-hfut666.md` |
| 描述报告 | `data/reports/describe/oskernel2024-aabcb.md` |
| 描述报告 | `data/reports/describe/oskernel2024-nqos.md` |
| 描述报告 | `data/reports/describe/oskernel2024-ouye.md` |
| 对比报告 | `data/reports/compare/oskernel2024-hfut666_vs_history.md` |

对比观察：

- `oskernel2024-hfut666` 的 Top 4 对比对象为 `oskernel2024-nqos`、`xv6-riscv`、`oskernel2024-aabcb`、`arceos`。
- 新增比赛作品已经能进入相似样本排序结果，说明对比库不再只依赖教学基线。
- 王杰优秀获奖案例的公开仓库地址本轮尚未定位到；拿到明确 URL 后应优先加入 `manifest.json` 并生成同类报告。

## 对比库代表性扩展记录

- 日期：2026-06-08
- 目标：在不大规模拉取仓库的前提下，将参考库扩展到 18 个代表性样本，提高未知输入仓库的比较全面性。
- 扩展原则：优先补齐语言、架构和内核形态，而不是按数量堆仓库。

新增技术路线样本：

| repo_id | 路线 | 覆盖价值 |
| --- | --- | --- |
| `xv6-public` | C / x86 / teaching-monolithic | 与 xv6-riscv 形成架构对照 |
| `os-tutorial` | C+ASM / x86 / teaching-monolithic | 覆盖最小启动、中断、驱动教程内核 |
| `littlekernel` | C / ARM+x86+RISC-V / embedded-kernel | 补充嵌入式内核与多架构样本 |
| `freertos-kernel` | C / ARM+RISC-V+x86 / RTOS | 补充实时调度和同步机制样本 |
| `tock` | Rust / ARM+RISC-V / embedded-microkernel | 补充 Rust 嵌入式微内核路线 |
| `sel4` | C / ARM+x86+RISC-V / microkernel | 补充经典微内核参照 |
| `includeos` | C++ / x86_64 / unikernel | 补充 unikernel 和 C++ 路线 |
| `redox-kernel` | Rust / x86_64 / microkernel | 补充 Rust 桌面微内核路线 |

本轮保留的报告：

| 类型 | 路径 |
| --- | --- |
| 描述报告 | `data/reports/describe/xv6-public.md` |
| 描述报告 | `data/reports/describe/freertos-kernel.md` |
| 描述报告 | `data/reports/describe/sel4.md` |
| 描述报告 | `data/reports/describe/includeos.md` |
| 对比报告 | `data/reports/compare/xv6-public_vs_history.md` |

对比观察：

- `xv6-public` 的 Top 5 对比对象为 `os-tutorial`、`sel4`、`xv6-riscv`、`littlekernel`、`oskernel2024-aabcb`。
- 扩容后，x86/C 输入项目能优先匹配到同架构、同风格样本，不再只能依赖 RISC-V/Rust 或单一教学基线。
- 18 个样本仍不是“全覆盖”，因此创新性判断仍应保留置信度和人工复核提示。
