# KernelSage 详细执行计划 (PLAN)

> 赛题：proj18 面向小型操作系统的分析比对智能体系统设计
> 团队：一定要以人类的身份赢啊（鲍灿辉、石雅禛 / 王毅）
> 文档版本：v2.0 — 2026-05-28
> 适用范围：MVP 优先，从零起步到完成可演示系统，并保留后续增强路线

---

## 0. 阅读指南

本文档把整个项目拆到**模块 → 类 → 方法 → 数据结构 → prompt 模板 → 命令 → 验收标准**这一级，但所有任务按 V1 / V2 分层执行。V1 是必须交付的答辩底线，V2 是有余力时再做的增强项。

```
职责 → 输入/输出 → 关键数据结构 → 类与方法签名 → 关键算法步骤 → 边界情况 → 验收标准
```

阅读顺序建议：第 1–3 章先看（V1 范围 + 基础设施 + 核心 schema），然后按第 4 章模块顺序逐个实现。第 9 章给出 5 周 MVP + 3 周增强日历，第 10 章是风险与回退方案。

---

## 1. 项目总览与目标

### 1.1 赛题要求拆解

| 维度 | 赛题原文 | 工程化解释 |
|---|---|---|
| 描述能力 | "对历史比赛内核赛道作品进行描述" | 输入单个仓库 → 输出 Markdown 描述文档 + 证据 JSON |
| 比较能力 | "新提交作品和历史作品进行比较" | 输入新仓库 + 历史库 → 输出比较 Markdown（相似/差异/创新点）+ 证据 JSON |
| 人类友好 | "描述/比较文档应对人类友好" | Markdown 含目录、表格、代码片段链接、可折叠结构 |
| 避免幻觉 | "尽量避免大模型幻觉" | 强证据链：关键判断性结论带 `[file:Lx-Ly]` 锚点；无证据结论标记"未确认" |
| 精准无误 | "比较文档应做到精准无误" | 轻量 self-check：报告生成后回查证据存在性与结论支撑情况 |

### 1.2 系统能做与不做（边界）

**做：**
- 处理 Rust / C / Asm 写的小型 OS 内核仓库（≤ 50 万行）
- 围绕进程、内存、syscall、文件系统、同步、中断、驱动 7 个维度抽取画像
- 用国产/开源 LLM 生成描述与比较文档

**不做：**
- 不做内核功能正确性验证（不运行 QEMU）
- 不做性能 benchmark 比较
- 不做"是否抄袭"的法律判断（只给出相似度证据，由评审人判定）

### 1.3 V1 / V2 范围

**V1 必做（5 周末必须可演示）：**
- 仓库采集与本地缓存（历史作品先控制在 5–10 个）
- 文件树分析、语言分布、README/docs 读取
- tree-sitter 仅抽取符号定义（`fn` / `struct` / `enum` / `trait` / `impl` 的名字和行号），不做调用图
- 关键词驱动的证据片段检索（grep -nE 风格）
- KernelProfile 7 维度填充
- N≤10 时全量比较历史仓库；N=10–15 时用 `style` 字段粗筛后全量比较
- LLM 描述生成、LLM 比较生成
- 轻量 self-check：只核验证据是否存在、关键结论是否有证据支撑
- Markdown 报告生成

**V1 明确不做：**
- 跨文件调用图、完整 AST 语义分析
- 向量库、embedding、RRF 融合检索
- Web UI
- 复杂 golden benchmark 和 LLM-as-a-judge 自动评测
- 大规模历史库（20+ 仓库）

**V2 增强（W6–W8，有余力再做）：**
- 调用图和 include/use 图
- BM25 与向量检索（N≥20 时再引入）
- 更多历史仓库
- golden 评测、消融实验和 HTML/Web 演示

### 1.4 总体技术路线

```
[历史仓库 + 新仓库]
       │
       ▼  scripts/fetch_repos.py
   data/samples/<repo_id>/  (本地缓存)
       │
       ▼  collector.py
   RepoSnapshot  (目录树/git log/README/语言分布)
       │
       ▼  parser.py (V1: tree-sitter symbols only)
   ParsedRepo    (V1: 符号定义表；V2: 调用边 / include 图)
       │
       ▼  analyzer.py
   KernelProfile (按 OS 维度的结构化画像 + 证据 anchor)
       │
       ├──► V1: 全量历史比较 / style 粗筛
       ├──► V2: indexer.py ──► data/indexes/{bm25,vec}/
       │
       ▼
   agent.py
     ├─ describe_workflow(profile) ──► describe.md + evidence.json
     └─ compare_workflow(new_profile, k=10) ──► compare.md + evidence.json
       │
       ▼  reporter.py
   人类友好报告 (Markdown / HTML)
```

---

## 2. 环境与基础设施

### 2.1 运行环境

- OS: Windows 10 / Linux（开发以 Windows + WSL2 为主，演示在 Linux）
- Python: 3.11.x（统一使用 conda 环境 `kernelsage`）
- 包管理: `uv`（比 pip 快，锁定 `pyproject.toml`）
- Git: ≥ 2.40（要用 `git -C` 与 partial clone）
- Node.js: 20.x（V2 调试 tree-sitter CLI 时需要；V1 优先使用 Python 包）
- 磁盘预算：data/ 目录至少留 10 GB（V1 历史仓库 + 缓存）；V2 扩展到 30 GB

### 2.2 创建环境（具体命令）

```bash
# 1. 创建 conda 环境
conda create -n kernelsage python=3.11 -y
conda activate kernelsage

# 2. 安装 uv
pip install uv

# 3. 初始化 pyproject.toml（项目根目录执行）
cd "C:/Users/CanhuiBao/Desktop/2026操作系统大赛/proj18-os-agent-compare"
uv init --package
uv add \
  tree-sitter==0.21.* tree-sitter-rust tree-sitter-c \
  gitpython==3.1.* \
  pydantic==2.* pydantic-settings \
  rich==13.* typer==0.12.* \
  httpx==0.27.* tenacity==9.* \
  jinja2==3.* \
  pyyaml==6.* orjson==3.*
uv add --dev pytest pytest-asyncio ruff mypy
```

V2 再按需增加：

```bash
uv add rank-bm25==0.2.* chromadb==0.5.* sentence-transformers==3.*
```

### 2.3 目录约定（增量于现有结构）

```
proj18-os-agent-compare/
├── docs/
│   ├── design.md                 # 已有
│   ├── report-template.md        # 已有
│   ├── evaluation.md             # 已有
│   ├── PLAN.md                   # 本文件
│   └── profile-schema.md         # 新增：KernelProfile JSON schema 说明
├── src/os_agent/
│   ├── __init__.py
│   ├── config.py                 # 新增：全局配置加载
│   ├── models.py                 # 新增：所有 pydantic 数据模型
│   ├── collector.py
│   ├── parser.py
│   ├── analyzer/
│   │   ├── __init__.py
│   │   ├── base.py               # 维度抽取基类
│   │   ├── scheduler.py
│   │   ├── memory.py
│   │   ├── syscall.py
│   │   ├── filesystem.py
│   │   ├── sync.py
│   │   ├── interrupt.py
│   │   └── driver.py
│   ├── indexer.py                # V2：BM25/向量索引
│   ├── retriever.py              # V2：历史仓库召回
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py             # LLM HTTP 封装 + 重试 + 缓存
│   │   └── prompts/              # 所有 prompt 模板
│   │       ├── describe_dim.j2
│   │       ├── compare_dim.j2
│   │       ├── innovation.j2
│   │       └── self_check.j2
│   ├── agent.py
│   ├── reporter.py
│   └── cli.py                    # 新增：typer 入口
├── scripts/
│   ├── fetch_repos.py            # 拉取历史作品
│   ├── build_index.py            # V2：全量索引重建
│   ├── eval_describe.py          # V2：自动评测
│   └── eval_compare.py           # V2：自动评测
├── data/
│   ├── samples/
│   │   ├── manifest.json         # 历史作品清单
│   │   └── <repo_id>/            # 每个仓库一个子目录
│   ├── profiles/                 # KernelProfile JSON 缓存
│   ├── indexes/                  # V2
│   │   ├── bm25/
│   │   └── vec/                  # chromadb 持久化目录
│   ├── llm_cache/                # LLM 响应缓存（按 prompt hash）
│   └── reports/
│       ├── describe/<repo_id>.md
│       └── compare/<new_id>_vs_<hist_id>.md
├── tests/
│   ├── unit/
│   ├── integration/
│   └── golden/                   # V2：人工标注的黄金样本
├── examples/                     # 端到端 demo
└── pyproject.toml
```

### 2.4 全局配置 `src/os_agent/config.py`

```python
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # 路径
    project_root: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = project_root / "data"
    samples_dir: Path = data_dir / "samples"
    profiles_dir: Path = data_dir / "profiles"
    indexes_dir: Path = data_dir / "indexes"
    cache_dir: Path = data_dir / "llm_cache"
    reports_dir: Path = data_dir / "reports"

    # LLM
    llm_provider: str = "deepseek"          # deepseek / qwen / ollama
    llm_model: str = "deepseek-v4-pro"
    llm_base_url: str = "https://api.deepseek.com/v1"
    llm_api_key: str = ""                    # 从 .env 读取
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.2
    llm_timeout: int = 120

    # V2 Embedding
    embed_model: str = "BAAI/bge-m3"
    embed_dim: int = 1024

    # V2 检索
    bm25_top_k: int = 30
    vec_top_k: int = 30
    rerank_top_k: int = 10

    class Config:
        env_file = ".env"

settings = Settings()
```

`.env` 模板（**不提交到 git**）：

```
LLM_API_KEY=sk-xxx
```

### 2.5 日志与缓存

- 日志：用 `rich.logging.RichHandler`，全局 `logger = logging.getLogger("kernelsage")`
- LLM 缓存键：`sha256(prompt + model + temperature)` → 存 `data/llm_cache/<hash>.json`
- 缓存命中时跳过 API 调用，加速反复实验

---

## 3. 核心数据结构：KernelProfile Schema

这是整个系统的"中间通用语言"。定义在 `src/os_agent/models.py`，所有上下游模块基于它通信。

### 3.1 顶层结构

```python
from pydantic import BaseModel, Field
from typing import Literal

class Evidence(BaseModel):
    """证据锚点：所有结论必须引用至少一个 Evidence"""
    file: str                       # 相对仓库根的路径，如 "kernel/src/task/mod.rs"
    line_start: int
    line_end: int
    snippet: str                    # 命中片段（≤ 30 行，截断）
    kind: Literal["code", "comment", "doc", "config", "commit"]
    note: str = ""                  # 抽取者补充说明

class DimensionFinding(BaseModel):
    """单个维度的一条发现"""
    statement: str                  # 自然语言陈述，如 "调度器使用 stride 算法"
    confidence: Literal["high", "medium", "low", "unconfirmed"]
    evidence: list[Evidence] = []

class SchedulerProfile(BaseModel):
    algorithm: DimensionFinding | None = None       # round-robin / stride / CFS-like / MLFQ
    data_structures: list[DimensionFinding] = []    # ready_queue 类型、wait_queue 等
    preemption: DimensionFinding | None = None
    smp_support: DimensionFinding | None = None
    context_switch_path: list[Evidence] = []        # 上下文切换关键函数链路

class MemoryProfile(BaseModel):
    paging: DimensionFinding | None = None          # sv39/sv48
    allocator: DimensionFinding | None = None       # buddy / slab / linked-list
    kernel_heap: DimensionFinding | None = None
    user_address_space: DimensionFinding | None = None
    copy_on_write: DimensionFinding | None = None
    page_replacement: DimensionFinding | None = None

class SyscallProfile(BaseModel):
    syscall_count: int = 0
    syscalls: list[dict] = []        # [{id, name, file, line, signature}]
    abi: DimensionFinding | None = None
    dispatch_mechanism: DimensionFinding | None = None

class FileSystemProfile(BaseModel):
    fs_type: DimensionFinding | None = None         # easy-fs / FAT / VFS-like
    vfs_layer: DimensionFinding | None = None
    block_device: DimensionFinding | None = None
    inode_design: list[DimensionFinding] = []

class SyncProfile(BaseModel):
    primitives: list[DimensionFinding] = []         # spinlock / mutex / semaphore / condvar
    deadlock_detection: DimensionFinding | None = None

class InterruptProfile(BaseModel):
    plic_clint: DimensionFinding | None = None
    trap_handler: list[Evidence] = []
    timer: DimensionFinding | None = None

class DriverProfile(BaseModel):
    drivers: list[DimensionFinding] = []            # virtio-blk / uart / virtio-net 等

class RepoMeta(BaseModel):
    repo_id: str                    # 主键，如 "2023-rcore-tutorial-xxx"
    name: str
    year: int | None = None
    team: str | None = None
    school: str | None = None
    url: str | None = None
    arch: list[str] = []            # ["riscv64", "x86_64"]
    languages: dict[str, int] = {}  # {"rust": 12500, "c": 800} 行数
    loc_total: int = 0
    commit_count: int = 0
    first_commit: str | None = None
    last_commit: str | None = None
    license: str | None = None
    style: Literal["rcore-variant", "ucore-variant", "microkernel", "exokernel", "independent", "unknown"] = "unknown"

class KernelProfile(BaseModel):
    meta: RepoMeta
    overview: str = ""              # ≤ 500 字总结（由 LLM 生成，必带证据）
    build_system: DimensionFinding | None = None
    scheduler: SchedulerProfile = SchedulerProfile()
    memory: MemoryProfile = MemoryProfile()
    syscall: SyscallProfile = SyscallProfile()
    filesystem: FileSystemProfile = FileSystemProfile()
    sync: SyncProfile = SyncProfile()
    interrupt: InterruptProfile = InterruptProfile()
    driver: DriverProfile = DriverProfile()
    extras: dict[str, DimensionFinding] = {}        # 非标准维度（用户态、网络栈、GUI 等）
    profile_version: str = "1.0"
    generated_at: str = ""
```

### 3.2 Schema 约束

- **证据强制**：除 `meta` 外的所有 `DimensionFinding` 必须带 ≥ 1 个 `Evidence`，否则 `confidence` 必须为 `"unconfirmed"`。
- **路径规范**：`Evidence.file` 必须用正斜杠相对路径。
- **序列化**：profile 落盘为 `data/profiles/<repo_id>.json`，UTF-8，2 空格缩进。

### 3.3 维度对应的关键词字典（用于静态预筛）

放在 `src/os_agent/analyzer/keywords.py`：

```python
DIM_KEYWORDS = {
    "scheduler": {
        "names": ["schedule", "scheduler", "pick_next", "switch_to", "context_switch",
                  "yield", "ready_queue", "run_queue", "stride", "task_manager", "cfs"],
        "files": ["sched", "task", "thread", "proc"],
    },
    "memory": {
        "names": ["alloc_frame", "dealloc_frame", "map_one", "page_table", "satp",
                  "buddy", "slab", "kmalloc", "vmalloc", "sv39", "cow", "copy_on_write"],
        "files": ["mm", "memory", "vm", "frame", "heap", "page"],
    },
    "syscall": {
        "names": ["sys_", "syscall", "SYSCALL_", "trap_handler", "ecall"],
        "files": ["syscall", "trap"],
    },
    "filesystem": {
        "names": ["inode", "dentry", "vfs", "open", "read_block", "easy_fs", "fat"],
        "files": ["fs", "vfs", "ext", "fat", "easy-fs"],
    },
    "sync": {
        "names": ["spinlock", "Mutex", "Semaphore", "CondVar", "rwlock", "barrier"],
        "files": ["sync", "lock", "mutex"],
    },
    "interrupt": {
        "names": ["plic", "clint", "irq", "interrupt", "trap_init", "set_timer"],
        "files": ["trap", "interrupt", "plic"],
    },
    "driver": {
        "names": ["VirtIOBlk", "virtio", "uart", "ns16550", "console"],
        "files": ["drivers", "driver", "virtio"],
    },
}
```

---

## 4. 模块详细设计

### 4.1 `collector.py` — 仓库采集器

**职责**：把任意 Git 仓库或本地路径标准化为 `RepoSnapshot`。

**数据模型**（追加到 `models.py`）：

```python
class FileEntry(BaseModel):
    path: str         # 相对路径
    size: int
    lang: str         # "rust" / "c" / "asm" / "markdown" / "toml" / "unknown"
    loc: int

class CommitInfo(BaseModel):
    sha: str
    author: str
    email: str
    timestamp: str    # ISO8601
    message: str

class RepoSnapshot(BaseModel):
    meta: RepoMeta
    root_path: Path
    files: list[FileEntry]
    readme_text: str = ""
    docs_texts: dict[str, str] = {}     # path → content（只收 docs/*.md, *.txt）
    commits: list[CommitInfo] = []
```

**类设计**：

```python
class RepoCollector:
    def __init__(self, cache_dir: Path): ...

    def from_url(self, url: str, repo_id: str | None = None,
                 depth: int | None = None) -> RepoSnapshot:
        """git clone --filter=blob:none，然后调用 from_local"""

    def from_local(self, path: Path, repo_id: str) -> RepoSnapshot:
        """已存在的本地仓库直接扫描"""

    def _scan_files(self, root: Path) -> list[FileEntry]: ...
    def _detect_lang(self, path: Path) -> str: ...
    def _collect_git_log(self, root: Path, limit: int = 500) -> list[CommitInfo]: ...
    def _read_readme(self, root: Path) -> str:
        """按优先级查找 README.md / README.rst / README"""
    def _read_docs(self, root: Path) -> dict[str, str]:
        """收 docs/*.md, *.txt, < 1MB 的文档文件"""
    def _infer_arch(self, files: list[FileEntry]) -> list[str]:
        """从目录名/Cargo.toml target 推断：riscv64gc-unknown-none-elf 等"""
    def _classify_style(self, files: list[FileEntry], readme: str) -> str:
        """风格分类：rcore-variant / ucore-variant / microkernel / independent"""
```

**风格分类规则（先用启发式，第二阶段再上 LLM 修正）**：

| 风格 | 判定线索 |
|---|---|
| rcore-variant | `Cargo.toml` 中依赖 rcore-* 或文件命名含 `task/mod.rs`, `mm/frame_allocator.rs` |
| ucore-variant | 存在 `proc.c` + `pmm.c` + `kern/init/init.c` |
| microkernel | README 含 "microkernel" 或源码无内核态 syscall 分发，转 IPC |
| 其他 | independent |

**`scripts/fetch_repos.py`** 批量调用：

```bash
python scripts/fetch_repos.py --manifest data/samples/manifest.json --out data/samples/
```

manifest 文件格式（**手工 + 半自动维护**）：

```json
[
  {"repo_id": "2022-rcore-team-A",
   "url": "https://github.com/xxx/xxx",
   "year": 2022, "team": "xxx", "school": "xxx"},
  ...
]
```

**验收标准**：
- V1：给定 manifest.json 含 5–10 个仓库，全部成功 clone（失败回退到 ZIP 下载）
- V2：历史仓库扩展到 20+ 个，并补充归档策略
- 单仓库扫描 ≤ 10s（不含克隆耗时）
- 输出 RepoSnapshot 序列化到 `data/profiles/raw/<repo_id>.json`

---

### 4.2 `parser.py` — 静态解析

**职责**：V1 用 tree-sitter 只抽取源码符号定义，得到稳定的名称、类型和行号；V2 再扩展调用边与 include/use 图。

**数据模型**：

```python
class SymbolDef(BaseModel):
    name: str
    kind: Literal["fn", "struct", "enum", "trait", "impl", "static", "const", "macro"]
    file: str
    line_start: int
    line_end: int
    signature: str = ""           # 函数：完整签名
    body_hash: str = ""           # SHA-1，用于跨仓库去重检测

class CallEdge(BaseModel):
    caller: str                   # 限定名 "module::fn" 或 file:line
    callee: str
    file: str
    line: int

class ParsedRepo(BaseModel):
    repo_id: str
    symbols: list[SymbolDef]
    calls: list[CallEdge] = []             # V2：调用图，V1 保持为空
    includes: list[tuple[str, str]] = []   # V2：(from_file, to_file)
    build_files: list[str] = []            # Cargo.toml / Makefile / Kbuild / linker.ld
```

**类设计**：

```python
class TreeSitterParser:
    def __init__(self):
        self.parsers: dict[str, Parser] = {}      # lang → tree_sitter Parser

    def parse_repo(self, snap: RepoSnapshot) -> ParsedRepo:
        """逐文件解析，根据 lang 路由到对应处理器"""

    def _parse_rust_symbols(self, path: Path, text: str) -> list[SymbolDef]: ...
    def _parse_c_symbols(self, path: Path, text: str) -> list[SymbolDef]: ...
    def _parse_asm(self, path: Path, text: str) -> list[SymbolDef]:
        """汇编只抽 .globl 标签 + 函数级符号"""
```

**V1 关键算法 — Rust 符号定义抽取**：

1. tree-sitter 查询模式（`queries/rust/symbols.scm`）：
   ```
   (function_item name: (identifier) @fn.name) @fn.def
   (struct_item name: (type_identifier) @struct.name) @struct.def
   (enum_item name: (type_identifier) @enum.name) @enum.def
   (trait_item name: (type_identifier) @trait.name) @trait.def
   (impl_item type: (_) @impl.type) @impl.def
   ```
2. 记录 `name`、`kind`、`file`、`line_start`、`line_end`、`signature`。
3. 对复杂泛型签名不做手写正则解析，由 tree-sitter 定位函数节点后从源码行切片得到 signature。

**V2 扩展 — 调用边抽取**：后续再加入 `queries/rust/calls.scm` 与 C `call_expression`，当前 V1 不把调用图作为交付门槛。

**C 语言简化处理**：V1 跳过预处理（不展开宏），只抽取顶层 `function_definition`、`struct`、`enum`；宏调用和调用边放到 V2。

**边界**：
- 单文件 > 1MB 跳过并记录到 `parsed.skipped`
- 解析错误 → 记 warning，继续下一个文件，不抛出异常
- 链接脚本 / makefile 不解析 AST，但记录路径作为 build_files

**验收标准**：
- V1：在 rCore-Tutorial-v3 上识别 ≥ 200 个 fn、≥ 30 个 struct/enum/trait/impl，行号可回查
- V1：`ParsedRepo.calls` 可为空，不影响后续 Profile 生成
- V2：再补调用边 ≥ 800 条的目标
- 单仓库解析 ≤ 60s

---

### 4.3 `analyzer/` — 内核维度抽取（核心模块）

**职责**：把 `ParsedRepo + RepoSnapshot` 转化为 `KernelProfile`。这是**整个系统精度的命脉**。

**统一基类** `analyzer/base.py`：

```python
class DimensionAnalyzer(ABC):
    name: str   # "scheduler" 等

    @abstractmethod
    def extract(self, snap: RepoSnapshot, parsed: ParsedRepo) -> BaseModel:
        """返回该维度的 Profile 子结构"""

    def _shortlist_files(self, parsed: ParsedRepo, keywords: dict) -> list[FileEntry]:
        """按文件名/路径关键词预筛"""

    def _shortlist_symbols(self, parsed: ParsedRepo, names: list[str]) -> list[SymbolDef]:
        """按符号名关键词筛选"""

    def _make_evidence(self, symbol: SymbolDef, snap: RepoSnapshot,
                       kind="code", note="") -> Evidence:
        """读源码切片填充 Evidence"""
```

**Analyzer 编排** `analyzer/__init__.py`：

```python
def analyze(snap: RepoSnapshot, parsed: ParsedRepo) -> KernelProfile:
    profile = KernelProfile(meta=snap.meta)
    profile.scheduler  = SchedulerAnalyzer().extract(snap, parsed)
    profile.memory     = MemoryAnalyzer().extract(snap, parsed)
    profile.syscall    = SyscallAnalyzer().extract(snap, parsed)
    profile.filesystem = FileSystemAnalyzer().extract(snap, parsed)
    profile.sync       = SyncAnalyzer().extract(snap, parsed)
    profile.interrupt  = InterruptAnalyzer().extract(snap, parsed)
    profile.driver     = DriverAnalyzer().extract(snap, parsed)
    profile.build_system = BuildSystemAnalyzer().extract(snap, parsed)
    profile.overview = LLMOverviewGenerator().generate(profile, snap)
    profile.generated_at = datetime.utcnow().isoformat()
    return profile
```

#### 4.3.1 SchedulerAnalyzer

抽取目标：算法、数据结构、是否抢占、SMP、上下文切换链路。

**步骤**：
1. `_shortlist_files`：匹配路径含 `sched`/`task`/`thread`/`proc`
2. 在候选符号中查找 `schedule()` / `pick_next_task()` / `switch_to()`
3. 算法判定（启发式 + LLM 兜底）：
   - 符号或注释含 `stride` → stride 算法
   - 含 `vruntime` 或 `red_black` → CFS-like
   - 含 `priority` + `mlfq` / 多级队列结构 → MLFQ
   - 否则 → round-robin（默认）+ LLM 二次确认
4. 数据结构：找出 `static .* RUN_QUEUE` / `ready_queue: VecDeque<_>`，记录类型
5. 抢占：grep `__interrupt`/`scheduler_tick`/`need_resched`
6. context_switch_path：从 `schedule` → 找出调用 `switch_to`/`__switch` 的边作为链路

**LLM 兜底 prompt**（仅当启发式置信度低时调用）：见 §5.2

**输出示例**：

```json
{
  "algorithm": {
    "statement": "采用 stride scheduling 调度算法",
    "confidence": "high",
    "evidence": [{"file": "os/src/task/manager.rs", "line_start": 42, "line_end": 78,
                  "snippet": "fn fetch(&mut self) -> Option<...> { ... self.ready_queue ...}",
                  "kind": "code"}]
  },
  ...
}
```

#### 4.3.2 MemoryAnalyzer

抽取目标：分页方案、物理分配器、堆、地址空间、COW、页面置换。

**步骤**：
1. 分页：grep `Sv39`/`Sv48`/`satp` 寄存器写入，记 evidence
2. 物理分配器：
   - 找 `FrameAllocator` / `frame_alloc` 实现 → 看是 stack 还是 buddy
   - 查找依赖 `buddy_system_allocator` crate（Cargo.toml）
3. 堆：grep `#[global_allocator]` 标注
4. 用户地址空间：`MemorySet::new` / `MapArea`
5. COW：grep `cow` / `clone_from_existed` / `mark_readonly_for_cow`
6. 页面置换：grep `swap` / `clock` / `lru`

#### 4.3.3 SyscallAnalyzer

抽取目标：syscall 表、ABI、分发机制。

**步骤**：
1. 找文件 `syscall/mod.rs` 或 `syscall.c`
2. 抽取 `const SYSCALL_*: usize = N;` 或 `#define SYS_*  N`，得到完整列表
3. 找分发函数 `syscall(...)` 的 `match`/`switch`：每个 case 对应一个 syscall_id → 关联到具体实现函数
4. ABI：检查 `trap_handler` 中寄存器读写顺序（a0~a7 / x0~x7）
5. 输出 `syscalls` 列表，每项 `{id, name, file, line, signature}`

#### 4.3.4 FileSystemAnalyzer

抽取目标：fs 类型、VFS 层、块设备、inode 设计。

**步骤**：
1. 检查依赖：`easy-fs` / `fatfs` / `littlefs`
2. 找 inode 结构定义（grep `struct Inode` / `pub struct DiskInode`）
3. VFS 层：找 `trait Inode` 或 `struct File` 的方法集
4. 块设备：找 `trait BlockDevice` 实现者，关联到具体驱动

#### 4.3.5 SyncAnalyzer

抽取目标：锁原语类型、是否有死锁检测。

**步骤**：
1. grep `struct Mutex` / `Spinlock` / `Semaphore` / `CondVar`
2. 死锁检测：grep `deadlock` / `banker` / `available_resources`

#### 4.3.6 InterruptAnalyzer

抽取目标：PLIC/CLINT、trap handler、timer。

**步骤**：
1. PLIC：grep `plic` / `plic_init` / `claim`/`complete`
2. trap：找 `trap_handler` 函数 + `__alltraps` 汇编入口
3. timer：grep `set_timer` / `mtimecmp` / `SBI_SET_TIMER`

#### 4.3.7 DriverAnalyzer

抽取目标：所有具名设备驱动。

**步骤**：
1. 扫描 `drivers/` 目录，每个子模块即一个驱动
2. grep `VirtIO` / `Uart` / `Ns16550a` / `Pl011`
3. 给出 statement: "支持 virtio-blk 块设备 + ns16550a 串口"

**所有 Analyzer 共同验收标准**：
- 每个 Analyzer 在 rCore-Tutorial-v3 上至少产出 3 条 `confidence != unconfirmed` 的 finding
- 处理时间 ≤ 5s/维度
- 输出 profile JSON 通过 pydantic 校验

---

### 4.4 `indexer.py` — 双索引层

**状态**：V2 增强项。V1 在历史仓库 N≤10 时直接全量比较，不引入索引层；N=10–15 时先按 `RepoMeta.style` / 架构 / 语言粗筛后全量比较。只有当历史仓库扩展到 N≥20 时，再实现本节。

**职责**：把所有历史 profile + 关键代码片段建索引。

```python
class HistoryIndex:
    def __init__(self, settings: Settings): ...

    def build(self, profiles: list[KernelProfile]) -> None:
        """V2：全量重建 BM25 + 向量索引"""

    def add_profile(self, profile: KernelProfile) -> None:
        """增量"""

    def _build_bm25(self, docs: list[IndexDoc]) -> None: ...
    def _build_vec(self, docs: list[IndexDoc]) -> None: ...

class IndexDoc(BaseModel):
    """索引的最小单元"""
    doc_id: str          # 形如 "<repo_id>::scheduler::algorithm"
    repo_id: str
    dimension: str
    text: str            # statement + snippet
    evidence: list[Evidence]
```

**索引粒度**：每个维度每条 finding 一个 doc。这样可以按维度独立检索。

**V2 向量化**：用 `sentence-transformers` 加载 bge-m3，本地编码。该能力不作为 V1 交付门槛。

**持久化**：
- BM25：`rank_bm25.BM25Okapi` pickle 到 `data/indexes/bm25/index.pkl`
- 向量：chromadb 持久化目录 `data/indexes/vec/`

---

### 4.5 `retriever.py` — 检索层

**状态**：V2 增强项。V1 比较策略如下：

| 历史仓库规模 | V1 策略 |
|---|---|
| N≤10 | 全量遍历，逐个比较 |
| N=10–15 | 按 `style` / 架构 / 语言粗筛后全量比较 |
| N≥20 | 进入 V2，引入 BM25 + 向量检索 |

```python
class Retriever:
    def __init__(self, idx: HistoryIndex): ...

    def retrieve_by_dimension(self, query: str, dim: str, k: int = 10) -> list[IndexDoc]:
        """指定维度内召回"""

    def retrieve_similar_profiles(self, profile: KernelProfile, k: int = 10) -> list[tuple[str, float]]:
        """整体相似仓库召回：把 profile 的 overview + 各维度 statement 拼成 query，向量召回 + repo 级聚合"""

    def _bm25(self, query: str, dim: str | None, k: int) -> list[IndexDoc]: ...
    def _vec(self, query: str, dim: str | None, k: int) -> list[IndexDoc]: ...
    def _rerank(self, query: str, candidates: list[IndexDoc]) -> list[IndexDoc]:
        """RRF (Reciprocal Rank Fusion) 融合 BM25 与向量结果"""
```

**RRF 公式**：`score(d) = Σ 1 / (k + rank_i(d))`，k 取 60，是工业常用值。

---

### 4.6 `llm/` — LLM 封装

#### 4.6.1 `client.py`

```python
class LLMClient:
    def __init__(self, settings: Settings):
        self.cache = LLMCache(settings.cache_dir)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    def chat(self, prompt: str, system: str = "", json_mode: bool = False) -> str:
        """统一入口，HTTP POST 到 OpenAI 兼容接口"""

class LLMCache:
    def get(self, key: str) -> str | None: ...
    def put(self, key: str, value: str) -> None: ...
```

模型优先级（按可用性回退）：
1. DeepSeek-V3 API（首选，便宜、长上下文）
2. Qwen3-Plus API（阿里云）
3. 本地 Ollama Qwen3-32B（离线兜底）

#### 4.6.2 prompt 模板（Jinja2）

所有 prompt 放 `src/os_agent/llm/prompts/`，统一约束：

- 系统提示固定为：
  ```
  你是一个谨慎的操作系统代码分析助手。你必须严格基于提供的代码片段回答问题。
  对于无法从代码确认的内容，必须明确标注"未确认"。
  禁止编造文件名、函数名或行号。
  ```

- 所有 prompt 都用 JSON 输出，schema 给定。

**`describe_dim.j2`**（描述单个维度）：

```jinja
请基于下面的代码片段，描述目标内核仓库的【{{ dimension }}】维度设计。

仓库基础信息：
- 名称：{{ meta.name }}
- 年份：{{ meta.year }}
- 风格：{{ meta.style }}

候选代码片段（每个片段都带 ID、文件、起止行）：
{% for s in snippets %}
--- 片段 {{ s.id }} ---
文件：{{ s.file }}（L{{ s.line_start }}–L{{ s.line_end }}）
```{{ s.lang }}
{{ s.text }}
```
{% endfor %}

请严格按以下 JSON 输出，所有 statement 必须在 evidence_ids 中至少引用一个片段 ID：

{
  "findings": [
    {"statement": "...", "confidence": "high|medium|low|unconfirmed",
     "evidence_ids": ["s3", "s7"]}
  ]
}

注意：
1. 只引用上述片段中确实出现的信息。
2. 如果某项无法确认，confidence 设为 "unconfirmed" 且 evidence_ids 可为空。
3. 不要编造其他文件名或函数名。
```

**`compare_dim.j2`**（比较单维度）：

```jinja
请比较两个内核仓库在【{{ dimension }}】维度的设计。

仓库 A（新提交）：{{ a.meta.name }}
A 的 finding（含证据）：
{% for f in a_findings %}- {{ f.statement }} [证据：{{ f.evidence | length }} 条]
{% endfor %}

仓库 B（历史作品）：{{ b.meta.name }}
B 的 finding（含证据）：
{% for f in b_findings %}- {{ f.statement }} [证据：{{ f.evidence | length }} 条]
{% endfor %}

请按 JSON 输出：
{
  "similarities": [{"statement": "...", "a_evidence_ids": [...], "b_evidence_ids": [...]}],
  "differences": [{"aspect": "...", "a_does": "...", "b_does": "...", "a_evidence_ids": [...], "b_evidence_ids": [...]}],
  "a_unique": ["..."],
  "b_unique": ["..."]
}

要求：
1. 所有相似/差异结论必须引用 A 或 B 已有 finding 的证据 ID。
2. 不要使用上述清单外的信息。
3. 严禁推测无证据的实现细节。
```

**`innovation.j2`**（创新点归纳）：

输入：新作品 profile + V1 全量历史作品（或 V2 top-K 召回历史作品）的对应维度。输出：每个创新点要回答"新在哪、相对什么基线、证据"。

**`self_check.j2`**（自检校验）：把生成的报告 + 证据集合再次喂给 LLM，问"以下结论是否完全由证据支撑？列出所有未支撑的句子"。

---

### 4.7 `agent.py` — 工作流编排

```python
class DescribeAgent:
    def __init__(self, llm: LLMClient): ...

    def run(self, profile: KernelProfile) -> DescribeResult:
        # 1. 对 profile 每个维度调用 describe_dim LLM 补丁
        # 2. 拼接 overview（已在 analyzer 阶段生成）
        # 3. 自检校验
        # 4. 渲染 Markdown（交给 reporter）

class CompareAgent:
    def run(self, new_profile: KernelProfile, history_profiles: list[KernelProfile]) -> CompareResult:
        # 1. V1: N≤10 直接遍历 history_profiles；N=10–15 先按 style 粗筛
        # 2. 对每个历史候选，逐维度调用 compare_dim
        # 3. 汇总：跨候选的"共性相似"标为高复用风险，"独有差异"标为创新点
        # 4. 自检校验
        # 5. 渲染比较报告
```

**关键设计：分层 LLM 调用**

- 维度级（细粒度）：每维度独立 prompt，避免一次性塞太多上下文
- 整合级：把维度结果拼成总报告（不再二次"创造"，只做语言润色 + 目录组织）

**Token 预算**：
- 单维度 prompt ≤ 8K token，含 ≤ 10 段代码片段
- 维度总数 7–10，单仓库描述总成本 ≈ 80K input tokens
- DeepSeek-V3 价格：约 ¥0.1 / 10K input tokens → 单次描述 < ¥1

---

### 4.8 `reporter.py` — 报告生成

```python
class Reporter:
    def __init__(self, template_dir: Path): ...

    def render_describe(self, profile: KernelProfile, result: DescribeResult) -> str:
        """返回 Markdown 文本"""

    def render_compare(self, result: CompareResult) -> str: ...

    def write_evidence_json(self, result, path: Path) -> None: ...
```

**Markdown 模板**（描述报告片段）：

```markdown
# {{ meta.name }} 项目描述

> 自动生成 by KernelSage v{{ version }} on {{ generated_at }}
> 队伍 / 年份：{{ meta.team }} / {{ meta.year }} | 架构：{{ meta.arch | join(", ") }}

## 总览

{{ overview }}

## 1. 调度子系统

### 算法
{% if profile.scheduler.algorithm %}
{{ profile.scheduler.algorithm.statement }}（置信度：{{ profile.scheduler.algorithm.confidence }}）

证据：
{% for e in profile.scheduler.algorithm.evidence %}
- [`{{ e.file }}:L{{ e.line_start }}–L{{ e.line_end }}`]({{ repo_url }}/blob/{{ commit }}/{{ e.file }}#L{{ e.line_start }})
  ```rust
  {{ e.snippet | truncate(800) }}
  ```
{% endfor %}
{% else %}
*未确认*
{% endif %}
```

**输出物**：
- `data/reports/describe/<repo_id>.md`
- `data/reports/describe/<repo_id>.evidence.json`
- 可选：`<repo_id>.html`（pandoc 或 markdown-it 转换）

---

## 5. LLM 集成详解

### 5.1 模型选择决策表

| 维度 | DeepSeek-V3 | Qwen3-Plus | 本地 Ollama Qwen3-32B |
|---|---|---|---|
| 价格 | 极低 | 低 | 0（电费） |
| 上下文 | 64K | 128K | 32K（本地配置） |
| 中文质量 | 强 | 强 | 中 |
| 演示离线 | 否 | 否 | 是 |
| 主用场景 | 默认 | 长上下文比对 | 评审现场断网兜底 |

`config.py` 通过环境变量切换。

### 5.2 LLM 启发式 fallback 的开关逻辑

`analyzer.scheduler` 里的判断流程：

```
1. 启发式规则命中 → confidence=high → 不调用 LLM
2. 部分命中（候选 2 个以上）→ confidence=medium → 调 LLM 二选一
3. 完全未命中 → confidence=low → 调 LLM 在候选 snippet 上推断
4. 全部失败 → confidence=unconfirmed
```

只有 2 / 3 才会触发 LLM，避免无谓 token 消耗。

---

## 6. 幻觉控制

### 6.1 输入侧约束

- prompt 中**永远不**提供"自由发挥"指令，所有 prompt 都要求基于"片段 ID"作答
- 片段 ID 形如 `s1, s2, ...`，与 Evidence 一一映射

### 6.2 输出侧校验（reporter 完成后强制运行）

```python
def hallucination_check(report: Markdown, evidences: list[Evidence]) -> CheckReport:
    """
    1. 抽取报告中所有 file:Lx-Ly 引用 → 必须在 evidences 中
    2. 抽取关键判断性结论 → 必须有证据引用或标注“未确认”
    3. 抽取报告中提到的函数名 → 尽量在 ParsedRepo.symbols 中回查
    4. 统计关键结论的证据覆盖率
    """
```

**关键结论定义**：只统计判断性、可被源码证据支撑的陈述，例如“采用 stride 调度”“使用 SV39 分页”“实现了 8 个 syscall”。不统计章节引导、过渡句、总结句等叙述性连接文本，避免报告里堆满低价值引用，损害人类可读性。

**self-check 范围**：V1 的 self-check 保持轻量，只检查证据是否存在、关键结论是否由证据支撑、无证据内容是否标注为“未确认”。不扩展成 mini 评测系统，不做 LLM-as-a-judge 排名。

报告末尾自动附录：

```markdown
## 附录：核验摘要
- 关键结论数：35
- 含证据关键结论数：29（82.9%）
- 未确认关键结论数：4
- 失效证据（指向不存在的文件/行）：0 ✅
```

### 6.3 评测指标定义

| 指标 | 计算方式 | 目标值 |
|---|---|---|
| 关键结论证据覆盖率 | 含证据关键结论 / 关键结论总数 | V1 软目标 ≥ 80%，V2 目标 ≥ 90% |
| 证据有效率 | 文件存在且行号在范围内 / 含证据结论 | 100% |
| 维度完备率 | 非空维度 / 7 | ≥ 6/7 |
| 人工抽查误判率（描述） | 人工抽查关键结论，错误句 / 抽查句 | V1 记录即可，V2 ≤ 5% |
| 人工抽查误判率（比较） | 同上 | V1 记录即可，V2 ≤ 8% |

---

## 7. 测试与评测

### 7.1 单元测试（pytest）

按模块组织：

```
tests/unit/
├── test_collector.py        # 给定 mini repo，验证 RepoSnapshot 字段
├── test_parser_rust.py      # 单文件 fixture，验证 symbol/call 抽取
├── test_analyzer_scheduler.py
├── test_analyzer_memory.py
├── ...
├── test_indexer.py
├── test_retriever.py
├── test_llm_client.py       # mock httpx
└── test_reporter.py
```

每个测试用例需配 `tests/fixtures/<name>/` 目录，包含最小可用源码。

### 7.2 集成测试

```
tests/integration/
├── test_e2e_describe.py     # 跑通：本地 fixture repo → KernelProfile → describe.md
└── test_e2e_compare.py
```

### 7.3 Golden benchmark（V2）

复杂 Golden benchmark 不作为 V1 交付门槛。当前 V1 已先固定 2 份文档级 golden 校准样例，见 `docs/GOLDEN_CASES.md` 和 `docs/golden/`，用于答辩说明报告质量审核口径。V2 阶段再扩展为可量化评测集，`tests/golden/` 存放 3 个以上手工撰写的高质量描述/比较报告作为黄金参照：

- `rcore-tutorial-v3.describe.golden.md`
- `ucore-bbl.describe.golden.md`
- `newxxx_vs_rcorev3.compare.golden.md`

评测脚本 `scripts/eval_describe.py`：
1. 生成报告
2. 抽取关键断言（用正则提取 statement 列表）
3. 与 golden 做 set 级别 precision/recall
4. LLM-as-a-judge 作辅助评分（给出 1–5 分 + 理由）

---

## 8. CLI

`src/os_agent/cli.py` 使用 typer：

```bash
# 拉取历史作品
kernelsage fetch --manifest data/samples/manifest.json

# 单仓库描述
kernelsage describe --repo data/samples/2023-rcore-xxx --out data/reports/

# 比较新作品
kernelsage compare --new data/samples/2026-team-xx --history data/profiles/ --out data/reports/

# 重建索引（V2）
kernelsage index build

# 评测（V2）
kernelsage eval describe --golden tests/golden/
kernelsage eval compare --golden tests/golden/

# 启动 Web 演示（可选 v2）
kernelsage serve --port 8080
```

每个子命令对应一个 `def cmd_xxx(...)` 函数，类型注解齐全，--help 自动生成。

---

## 9. 5 周 MVP + 3 周增强日历

> 起点：2026-06-01 周一
> 终点：2026-07-26 周日
> 原则：W1–W5 必须形成可演示闭环；W6–W8 只做增强、评测、文档和答辩材料。

### W1（6/1 – 6/7）基础设施 + 数据

- D1: 创建 conda 环境、初始化 pyproject、提交 .gitignore
- D2: 写 `config.py` + `models.py`（KernelProfile schema）
- D3: 把本文档 PLAN.md / profile-schema.md 评审定稿
- D4: 收集历史作品 URL 清单，写 `manifest.json` 初版（5–10 条）
- D5: 实现 `scripts/fetch_repos.py`，本地下载验证
- D6: 实现 `collector.py` 全部方法，单测通过
- D7: 缓冲日 / 回顾 / 写周报

### W2（6/8 – 6/14）静态解析 + 证据检索

- D8: tree-sitter 安装 + Rust/C 符号定义抽取 spike
- D9: `parser.py` Rust 部分（symbols only）
- D10: `parser.py` C 部分（symbols only）
- D11: 关键词驱动的证据片段检索（grep -nE 风格）
- D12: 在 3 个真实 repo 上跑通，对比预期符号数
- D13: 单测齐全
- D14: 缓冲

### W3（6/15 – 6/21）KernelProfile 7 维度

- D15: `analyzer/base.py` + scheduler.py
- D16: scheduler 在 rCore-v3、uCore、独立微内核上验证
- D17: memory.py
- D18: memory 在 3 个样本上验证
- D19: syscall.py + 验证
- D20: filesystem.py + 验证
- D21: sync.py / interrupt.py / driver.py，集成 7 个维度

### W4（6/22 – 6/28）LLM 描述 + 轻量 self-check

- D22: build_system.py + Profile JSON 落盘
- D23: 跑通 5 个仓库的 KernelProfile 全量生成
- D24: `llm/client.py` + 缓存
- D25: describe_dim prompt 与报告模板
- D26: 轻量 self-check：关键结论证据核验
- D27: 第一份完整描述报告产出
- D28: 缓冲

### W5（6/29 – 7/5）Compare Agent + MVP 闭环

- D29: `agent.py::CompareAgent`，N≤10 全量遍历历史 profile
- D30: compare_dim prompt 与比较报告模板
- D31: 创新点归纳逻辑（基于历史 profile 差异，不做法律判断）
- D32: 端到端跑通：新仓库 → 描述报告 + vs 3–5 历史比较报告
- D33: README / docs / examples 补齐复现步骤
- D34: MVP 演示脚本 + 第一版录屏
- D35: 缓冲 + 指导教师评审

### W6（7/6 – 7/12）V2 增强：检索或调用图二选一

- D36: 若历史仓库 N≥15，实现 BM25 粗召回；否则继续扩充样本与报告质量
- D37: 可选：Rust/C 调用边 spike，不影响 V1 主线
- D38: 报告可读性打磨：目录、表格、证据附录
- D39: self-check 输出更清晰的核验摘要
- D40: 扩展到 10 个左右历史仓库
- D41: 端到端回归测试
- D42: 缓冲

### W7（7/13 – 7/19）评测、调优、文档

- D43: 人工抽查 3 份描述报告 + 3 份比较报告
- D44: 记录关键结论证据覆盖率，目标 V1 ≥80%
- D45: 已提前完成轻量版：固定 2 份文档级 golden；V2 再扩展为可量化 golden benchmark
- D46: 调 prompt，修复无证据推断和表达不清问题
- D47: 重跑端到端 demo，稳定输出
- D48: 补全 README、docs/、examples/
- D49: 缓冲

### W8（7/20 – 7/26）演示、打磨、答辩材料

- D50: 端到端演示脚本 + 录屏
- D51: 整理参赛文档 / PPT 大纲
- D52: 完成 PPT
- D53: 内部 dry-run，请指导教师评审
- D54: 修订
- D55: 提交参赛包
- D56: 答辩准备 / 缓冲

---

## 10. 风险与应对

| 风险 | 概率 | 影响 | 缓解措施 |
|---|---|---|---|
| LLM API 限速/价格 | 中 | 高 | 全程缓存；批量 sleep；准备 Ollama 兜底 |
| tree-sitter 解析失败率高 | 中 | 中 | V1 只抽符号定义；解析失败文件回退到行级正则；不阻塞流水线 |
| 历史作品仓库地址失效 | 高 | 中 | 一旦克隆成功立即压缩归档到 data/samples/ 不再依赖网络 |
| 仓库规模过大致超时 | 中 | 中 | 按目录黑名单跳过（target/、third_party/）；并行化 |
| 评测指标达不到 | 中 | 高 | V1 只统计关键结论证据覆盖率，目标 80%；复杂 golden 评测放 V2 |
| 风格分类错误 | 高 | 低 | 仅作辅助标签，不参与核心比对逻辑 |
| 队员对 tree-sitter 不熟 | 中 | 中 | W2 第一天先做 symbols-only spike，写 cheatsheet 到 docs/ |
| V2 功能挤压 MVP | 中 | 高 | W1–W5 不做向量库、调用图、Web UI；任何增强都不得阻塞报告闭环 |
| 演示现场断网 | 低 | 高 | 准备完整离线包 + Ollama 镜像 |

---

## 11. 交付物清单

参赛包目录（最终归档）：

```
KernelSage-final/
├── README.md                 # 项目说明 + 复现指南
├── PLAN.md                   # 本文件
├── docs/
│   ├── design.md
│   ├── profile-schema.md
│   ├── evaluation.md
│   └── report-template.md
├── src/                      # 源代码
├── tests/                    # 含 golden
├── examples/                 # V1 至少 1 个端到端 demo，V2 扩展到 3 个
│   ├── 01-describe-rcore-v3/
│   ├── 02-describe-ucore-bbl/
│   └── 03-compare-newteam-vs-history/
├── data/
│   └── samples/manifest.json # 历史作品清单（仓库本体不打包，按 manifest 拉取）
├── scripts/
├── pyproject.toml
├── slides.pdf                # 答辩 PPT 导出
├── demo.mp4                  # 演示录像
└── 证明材料/                  # 报名表、承诺书等
```

---

## 12. 决策待定项（需在 W1 D3 评审中确认）

- [ ] 主 LLM：DeepSeek-V3 / Qwen3-Plus，第二备选
- [ ] manifest.json 第一批 5–10 个仓库的最终名单
- [ ] V1 是否保留 BM25：默认不做；如果 N≥15 再做
- [ ] V2 Embedding：bge-m3（1024d，多语言）还是 bge-large-zh
- [ ] V2 向量库：chromadb（够用）还是 lancedb（更快但更新）
- [ ] V2 是否做 Web UI（可选 streamlit）

---

## 13. 立即可执行的下三步

1. **今天**：确认 V1 范围：symbols-only tree-sitter、N≤10 全量比较、关键结论证据率 ≥80% 作为软目标。
2. **明天**：按 §2.2 搭好 V1 环境 + 落地 `models.py`（KernelProfile schema）。
3. **后天**：写完 `collector.py` + `manifest.json` 前 5 条，能跑通 `kernelsage fetch`。

只要 §3 的 KernelProfile schema 一定稿，后续 7 个 Analyzer 就能并行开发。任何 V2 功能都必须在 V1 报告闭环稳定后再进入。
