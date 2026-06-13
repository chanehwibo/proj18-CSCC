# KernelSage Golden 样例校准说明

本文档固定 1 份描述报告和 1 份对比报告作为人工审核后的 golden 样例，用于说明 KernelSage 如何评价报告质量。golden 样例不是自动生成报告的简单备份，也不是官方评分，而是对自动报告中的关键结论、源码证据、相似线索边界进行人工校准后的参照材料。

## 样例清单

| 类型 | 输入仓库 | 自动报告 | Golden 文件 | 选择理由 |
| --- | --- | --- | --- | --- |
| 描述报告 | `xv6-public` | `data/reports/describe/xv6-public.md` | [docs/golden/xv6-public.describe.golden.md](golden/xv6-public.describe.golden.md) | 经典小型 OS，机制完整，适合校准七维画像和证据质量 |
| 对比报告 | `oskernel2024-aabcb` | `data/reports/compare/oskernel2024-aabcb_vs_history.md` | [docs/golden/oskernel2024-aabcb.compare.golden.md](golden/oskernel2024-aabcb.compare.golden.md) | 公开比赛作品样本，适合校准历史样本选择、相似线索和边界表述 |

## 复现命令

```powershell
$env:PYTHONPATH='src'

python scripts\kernelsage.py describe data\samples\xv6-public --repo-id xv6-public --out data\reports\describe\xv6-public.md
python scripts\kernelsage.py compare data\samples\oskernel2024-aabcb --repo-id oskernel2024-aabcb --limit 3 --out data\reports\compare\oskernel2024-aabcb_vs_history.md
```

说明：`data/reports/` 是运行生成物，默认不提交。golden 文件只保留人工审核后的关键结论和校准口径。

## Golden 判定标准

| 检查项 | 合格标准 |
| --- | --- |
| 证据强度 | 关键判断必须能落到源码文件和行号；优先使用函数体、数据结构、宏定义或真实调用关系，不把 include 或目录名当作唯一证据 |
| 维度结论 | 描述报告的 OS 维度必须说明确认理由；弱证据只能作为补充，不能支撑高置信结论 |
| 相似线索 | 对比报告必须区分功能重合、结构/符号重合、硬件通用命名和路径相似，不能把相似线索写成抄袭裁定 |
| 来源边界 | 未核验比赛样本不能硬标特奖、一等奖或优秀案例；只有 `verified_award` 才能作为获奖样本口径 |
| self-check | 自动报告的关键结论证据覆盖率和无效证据引用数要进入审核记录，但不能把覆盖率等同于完全正确 |

## 当前人工审核结论

| Golden 样例 | 结论 | 保留边界 |
| --- | --- | --- |
| `xv6-public.describe.golden.md` | 通过。七个 OS 机制维度均有强源码证据支撑，可作为描述报告质量基线 | 自动报告中少数首条命中偏弱，golden 用人工挑选的强证据进行校准 |
| `oskernel2024-aabcb.compare.golden.md` | 通过。历史样本选择和代码级相似线索有可复核证据，边界表达合格 | UART/PLIC 等硬件宏属于通用实现线索，只能作为弱到中等复核线索 |

## 答辩使用方式

答辩时可以先展示普通自动报告，再打开 golden 文件说明我们如何检查报告质量：

1. 描述报告看“机制结论是否被强证据支撑”。
2. 对比报告看“相似线索是否被分级，是否避免越权裁定”。
3. self-check 只证明证据链存在，不替代人工理解源码。
4. golden 样例用于校准报告质量，不用于声称系统已经能自动判断创新或抄袭。
