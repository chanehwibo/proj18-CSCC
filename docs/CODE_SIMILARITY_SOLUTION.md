# 代码级重复线索问题与解决方案

## 问题

早期 compare 报告能说明两个仓库在同一 OS 维度上都有实现，例如都包含调度、页表、系统调用或文件系统证据，但这只能算“功能重合线索”，不能直接说明代码相似。

如果报告只说“可能重复”却没有更细的代码级依据，会有两个问题：

- 功能相同不等于代码相似。
- 文件、函数、结构体、宏和片段内容是否相近，仍需要人工自己查。
- 自动系统不能直接给出“抄袭”裁定，否则会超过工具边界。

因此系统需要在“功能重合”和“抄袭裁定”之间增加一层可复核的代码级线索。

## 解决方案

当前版本采用低成本本地检测，不新增大模型调用，也不引入 AST 相似度重型依赖。

compare 阶段在已有 `KernelProfile` 和源码 evidence 上补充五类线索：

| 线索类型 | 检测方式 | 作用 |
| --- | --- | --- |
| 文件路径重合 | 比较 evidence 文件名和规范化路径 | 判断实现位置是否相近 |
| 函数/符号名重合 | 比较双方同维度符号名 | 找到相同入口或关键函数 |
| 结构体/类型重合 | 比较真实定义的 struct/enum/trait | 找到数据结构设计相似点 |
| 宏名重合 | 比较 `#define` 宏名 | 找到常量、页表位、系统调用号等相似线索 |
| 片段相似度 | 对 evidence 去注释、去弱信号后计算 token/结构 Jaccard | 找到局部代码文本相似 |

为降低误报，系统同时做了过滤：

- C 结构体只把 `struct name {` / `typedef struct name {` 当作定义，不再把 `struct proc *p` 这种使用误判成定义。
- 注释相同、include-only、只有极少公共 token 的弱结构相似不会进入报告。
- `defs.h`、`types.h`、`main.c` 等低价值路径会被过滤。
- 每份比较报告最多保留 30 条代码级相似线索，每类最多 6 条，避免报告过长。

## 报告呈现

比较报告中新增：

```text
## 代码级相似线索检测
```

该小节会展示路径、函数/符号、结构体/宏、片段相似度等代表性线索，并附双方文件路径、行号和短代码片段。

报告会明确说明：这些结果是“代码级可复核线索”，不是抄袭裁定。是否构成代码重复，仍需结合完整文件、提交历史、上下文和比赛规则人工判断。

## 成本控制

本阶段不会增加 DeepSeek API 成本：

- 不调用 LLM。
- 不新增向量库或 AST 相似度服务。
- 复用本地画像缓存。
- 只在 compare 本地流程里做字符串、符号和 token 集合计算。

只有在后续使用 `--use-llm` 并把更多代码级线索送入 prompt 时，才会增加在线模型 token 消耗。

## 当前验证

已补充回归测试，覆盖：

| 测试内容 | 结果 |
| --- | --- |
| 片段级 token/结构相似能被识别 | 通过 |
| 注释相同不被识别为相似 | 通过 |
| include-only 不被识别为相似 | 通过 |
| C 结构体使用不被误判为定义 | 通过 |
| 宏定义能进入符号表 | 通过 |
| CompareAgent 能输出路径、函数、类型、宏和片段线索 | 通过 |
| Reporter 能渲染“代码级相似线索检测”小节 | 通过 |
| LLM prompt 能约束模型不得把线索直接写成抄袭裁定 | 通过 |

验证命令：

```powershell
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python -m compileall src scripts\kernelsage.py
$env:PYTHONPATH='src'; python scripts\kernelsage.py compare data\samples\xv6-public --repo-id xv6-public --limit 5
```

样例报告：

```text
data/reports/compare/xv6-public_vs_history.md
```

