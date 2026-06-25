# collected-data.xlsx 导入记录

本次导入来源为赛事组提供的 `collected-data.xlsx`，字段包括年份、赛事、子赛事、学校、队伍名称和仓库地址。

## 导入结果

- Excel 原始仓库数：168
- 成功浅克隆并纳入 `data/samples/manifest.json`：120
- 不可访问、clone 失败或只留下半成品目录，未纳入主 manifest：48
- 当前主 manifest 总数：141

成功纳入的样本统一标记为：

```text
category: contest-case
source_tier: competition_history
label: 赛事历史作品
```

源码目录位于 `data/samples/<repo_id>/`，仍按 `.gitignore` 作为本地样本数据处理，不提交第三方源码。

## 成功样本年份分布

- 2021: 16
- 2022: 19
- 2023: 19
- 2024: 29
- 2025: 37

## 未纳入主 manifest 的失败仓库

| repo_id | 年份 | 队伍 | 仓库地址 |
| --- | --- | --- | --- |
| `collected2021-retrhelo-xv6-k210` | 2021 | 3Los | https://gitlab.eduxiji.net/retrhelo/xv6-k210 |
| `collected2021-deng19992008-openbhos` | 2021 | 广告位招租 | https://gitlab.eduxiji.net/deng19992008/openbhos |
| `collected2021-hzc1998-oskernel2021-xbook2` | 2021 | 小骨头 | https://gitlab.eduxiji.net/hzc1998/oskernel2021-xbook2 |
| `collected2021-chenzhiy-atom` | 2021 | ATOM | https://gitlab.eduxiji.net/chenzhiy/atom |
| `collected2021-potato-kernal-cy-os` | 2021 | 文火土豆丝 | https://gitlab.eduxiji.net/potato-kernal/cy-os |
| `collected2022-2019301887-oskernel2022-npucore` | 2022 | NPUcore | https://gitlab.eduxiji.net/2019301887/oskernel2022-npucore.git |
| `collected2022-c-core1-2022os-c-core` | 2022 | C-core | https://gitlab.eduxiji.net/c-core1/2022os-c-core.git |
| `collected2022-19061120-oskernel2022-segmentfault` | 2022 | 段错误 | https://gitlab.eduxiji.net/19061120/oskernel2022-segmentfault.git |
| `collected2022-weihuan_tang-runos` | 2022 | RunOS | https://gitlab.eduxiji.net/weihuan_tang/runos |
| `collected2022-dh2zz-oskernel2022` | 2022 | 健康向上好青年 | https://gitlab.eduxiji.net/dh2zz/oskernel2022 |
| `collected2022-nullpointer-os` | 2022 | untitled-project(1)(2) | https://gitlab.eduxiji.net/nullpointer/os |
| `collected2022-853476998-run` | 2022 | 能run就行 | https://gitlab.eduxiji.net/853476998/run |
| `collected2022-educg-group-14158-894147-oskernel2022-s0s` | 2022 | S0S | https://gitlab.eduxiji.net/educg-group-14158-894147/oskernel2022-s0s |
| `collected2022-910191774-oskernel2022` | 2022 | Enforce Core | https://gitlab.eduxiji.net/910191774/oskernel2022.git |
| `collected2022-wsy-oskernel2022-whw` | 2022 | WHW | https://gitlab.eduxiji.net/wsy/oskernel2022-whw.git |
| `collected2022-yyz-oskernel-1` | 2022 | hfut.happy | https://gitlab.eduxiji.net/yyz/oskernel-1 |
| `collected2023-202318123101314-oskernel2023-titanix` | 2023 | Titanix | https://gitlab.eduxiji.net/202318123101314/oskernel2023-Titanix |
| `collected2023-202310007101563-alien` | 2023 | Alien | https://gitlab.eduxiji.net/202310007101563/Alien |
| `collected2023-404-oskernel2023-sos` | 2023 | SOS | https://gitlab.eduxiji.net/404/OSKernel2023-SOS |
| `collected2023-202310008101520-oskernel2023-x` | 2023 | Main.os(2)(1)(1) | https://gitlab.eduxiji.net/202310008101520/oskernel2023-x |
| `collected2023-202314430101195-oskernel2023-nutos` | 2023 | 编写吧!NutOS | https://gitlab.eduxiji.net/202314430101195/oskernel2023-nutos |
| `collected2023-202318123101332-oskernel2023-moos` | 2023 | MoOS | https://gitlab.eduxiji.net/202318123101332/OSKernel2023-MoOS |
| `collected2023-202310359101097-oskernel2023-ouros` | 2023 | OurOS | https://gitlab.eduxiji.net/202310359101097/oskernel2023-ouros |
| `collected2023-202314430101100-oskernel2023-550w` | 2023 | 550W | https://gitlab.eduxiji.net/202314430101100/OSKernel2023-550W.git |
| `collected2024-educg-group-26010-2376550-t202410287992637-1454` | 2024 | 学到东西就算胜利队 | https://gitlab.eduxiji.net/educg-group-26010-2376550/T202410287992637-1454 |
| `collected2024-educg-group-26010-2376550-t202410214992509-3687` | 2024 | NPUcore-whoami | https://gitlab.eduxiji.net/educg-group-26010-2376550/T202410214992509-3687 |
| `collected2024-educg-group-26010-2376550-t202410213992561-2280` | 2024 | ᕕ(◠ڼ◠)ᕗ旺仔 | https://gitlab.eduxiji.net/educg-group-26010-2376550/T202410213992561-2280 |
| `collected2024-educg-group-26010-2376550-t202410487992457-1800` | 2024 | RustTrustHuster | https://gitlab.eduxiji.net/educg-group-26010-2376550/T202410487992457-1800 |
| `collected2024-educg-group-26010-2376550-t202418123993075-2940` | 2024 | Phoenix | https://gitlab.eduxiji.net/educg-group-26010-2376550/T202418123993075-2940 |
| `collected2024-educg-group-26010-2376550-t202410213992712-3123` | 2024 | 练习时长两年半 | https://gitlab.eduxiji.net/educg-group-26010-2376550/T202410213992712-3123 |
| `collected2024-educg-group-26010-2376550-t202419145993048-647` | 2024 | neuqOS | https://gitlab.eduxiji.net/educg-group-26010-2376550/T202419145993048-647 |
| `collected2024-educg-group-26010-2376550-t202410336992584-3678` | 2024 | Pantheon | https://gitlab.eduxiji.net/educg-group-26010-2376550/T202410336992584-3678 |
| `collected2024-educg-group-26011-2376549-t202410460992502-2319` | 2024 | NPUcore-重生之我是秦始皇 | https://gitlab.eduxiji.net/educg-group-26011-2376549/T202410460992502-2319 |
| `collected2025-educg-group-36002-2710490-starry-mix` | 2025 | Starry Mix | https://gitlab.eduxiji.net/educg-group-36002-2710490/starry-mix |
| `collected2025-educg-group-36002-2710490-t202510008995695-2720` | 2025 | SubsToKernel | https://gitlab.eduxiji.net/educg-group-36002-2710490/T202510008995695-2720 |
| `collected2025-educg-group-36002-2710490-t202510213995926-2475` | 2025 | 火箭队 | https://gitlab.eduxiji.net/educg-group-36002-2710490/T202510213995926-2475 |
| `collected2025-educg-group-36002-2710490-t202510486995158-3041` | 2025 | 武大前锋 | https://gitlab.eduxiji.net/educg-group-36002-2710490/T202510486995158-3041 |
| `collected2025-educg-group-36002-2710490-t202510487995221-883` | 2025 | 塔特林设计局 | https://gitlab.eduxiji.net/educg-group-36002-2710490/T202510487995221-883 |
| `collected2025-educg-group-36002-2710490-t202510699995276-827` | 2025 | 西北工业大学一二三队 | https://gitlab.eduxiji.net/educg-group-36002-2710490/T202510699995276-827 |
| `collected2025-educg-group-36002-2710490-oskernel2025-npucore-blossom` | 2025 | NPUcore-BLOSSOM | https://gitlab.eduxiji.net/educg-group-36002-2710490/oskernel2025-npucore-blossom |
| `collected2025-educg-group-36002-2710490-t202510701995284-398` | 2025 | 广告位招租 | https://gitlab.eduxiji.net/educg-group-36002-2710490/T202510701995284-398 |
| `collected2025-educg-group-36002-2710490-t202518123995600-2523` | 2025 | Del0n1x | https://gitlab.eduxiji.net/educg-group-36002-2710490/T202518123995600-2523 |
| `collected2025-educg-group-36002-2710490-bakaos` | 2025 | 只敲代码不玩耍聪明baka也变傻ᗜˬᗜ | https://gitlab.eduxiji.net/educg-group-36002-2710490/bakaos |
| `collected2025-educg-group-38066-3006609-t202510699997579-3142` | 2025 | litangzhiwang | https://gitlab.eduxiji.net/educg-group-38066-3006609/T202510699997579-3142 |
| `collected2025-educg-group-38066-3006609-t202510699997586-594` | 2025 | 翱翔大飞机 | https://gitlab.eduxiji.net/educg-group-38066-3006609/T202510699997586-594 |
| `collected2025-educg-group-38066-3006609-t202510699997598-2620` | 2025 | HHH | https://gitlab.eduxiji.net/educg-group-38066-3006609/T202510699997598-2620 |
| `collected2025-educg-group-38066-3006609-t202510699997589-2461` | 2025 | 西北工业大学25队 | https://gitlab.eduxiji.net/educg-group-38066-3006609/T202510699997589-2461 |
| `collected2025-educg-group-38066-3006609-t202510699997577-535` | 2025 | 专业团队 | https://gitlab.eduxiji.net/educg-group-38066-3006609/T202510699997577-535 |
