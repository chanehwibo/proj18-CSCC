"""Kernel-oriented static analysis utilities."""

from __future__ import annotations

import re
from pathlib import Path

from .models import Evidence, Finding, KernelProfile, ParsedRepo, RepoSnapshot


KERNEL_PATH_HINTS = (
    "os/src/",
    "kernel/",
    "kern/",
    "src/mm",
    "src/task",
    "src/trap",
    "src/syscall",
    "src/fs",
    "src/sync",
    "src/drivers",
    "drivers/",
    "modules/axhal",
    "modules/axmm",
    "modules/axtask",
    "modules/axfs",
    "modules/axdriver",
    "zcore/src/",
)

SUPPORT_PATH_HINTS = (
    "easy-fs/",
    "crates/",
    "components/",
    "modules/",
)

LOW_PRIORITY_PATH_HINTS = (
    "user/",
    "users/",
    "ulib/",
    "apps/",
    "app/",
    "examples/",
    "example/",
    "tests/",
    "test/",
    "docs/",
    "doc/",
    "book/",
    "outline.md",
    "readme",
    "xtask/",
    "scripts/",
    "tools/",
)


DIMENSIONS = {
    "scheduler": {
        "title": "调度与任务管理",
        "keywords": ["schedule", "scheduler", "switch_to", "context_switch", "yield", "task", "thread", "proc", "stride", "run_queue", "ready_queue"],
        "hints": ["task", "sched", "proc", "thread"],
        "statement": "项目包含任务/线程管理与调度相关实现。",
    },
    "memory": {
        "title": "内存管理",
        "keywords": ["page_table", "pagetable", "sv39", "satp", "frame_allocator", "frame_alloc", "heap_allocator", "memoryset", "pmm", "vmm", "copy_on_write", "cow"],
        "hints": ["mm", "memory", "page", "frame", "heap", "vm", "pmm", "vmm"],
        "statement": "项目包含页表、物理页或堆分配等内存管理实现。",
    },
    "syscall": {
        "title": "系统调用",
        "keywords": ["syscall", "sys_", "ecall", "SYS_", "a7", "trap"],
        "hints": ["syscall", "trap"],
        "statement": "项目包含系统调用入口、编号或分发逻辑。",
    },
    "filesystem": {
        "title": "文件系统",
        "keywords": ["inode", "vfs", "file", "fs", "fat", "easy_fs", "block", "dentry"],
        "hints": ["fs", "file", "inode", "vfs", "block"],
        "statement": "项目包含文件系统、VFS、inode 或块设备相关实现。",
    },
    "sync": {
        "title": "同步机制",
        "keywords": ["mutex", "spinlock", "semaphore", "condvar", "rwlock", "lock", "atomic"],
        "hints": ["sync", "lock", "mutex", "semaphore"],
        "statement": "项目包含锁、信号量或原子操作等同步机制。",
    },
    "interrupt": {
        "title": "中断与异常",
        "keywords": ["trap", "interrupt", "irq", "plic", "clint", "timer", "mtimecmp", "exception"],
        "hints": ["trap", "interrupt", "irq", "timer", "plic", "clint"],
        "statement": "项目包含 trap、中断、异常或定时器处理逻辑。",
    },
    "driver": {
        "title": "设备驱动",
        "keywords": ["virtio", "uart", "driver", "blk", "block", "console", "ns16550", "device"],
        "hints": ["driver", "drivers", "virtio", "uart", "block", "device"],
        "statement": "项目包含串口、块设备或 virtio 等设备驱动相关实现。",
    },
}


class KernelAnalyzer:
    def analyze(self, snap: RepoSnapshot, parsed: ParsedRepo) -> KernelProfile:
        profile = KernelProfile(meta=snap.meta, symbols=parsed.symbols[:500])
        profile.overview = self._overview(snap, parsed)
        profile.build_system = self._build_system(snap)
        for dim, spec in DIMENSIONS.items():
            profile.dimensions[dim] = self._find_dimension(snap, parsed, dim, spec)
        return profile

    def _overview(self, snap: RepoSnapshot, parsed: ParsedRepo) -> str:
        langs = ", ".join(f"{k}: {v} LOC" for k, v in sorted(snap.meta.languages.items(), key=lambda x: -x[1])[:4])
        return (
            f"{snap.meta.name} 是一个 {snap.meta.style} 风格的小型操作系统相关仓库，"
            f"主要语言统计为 {langs or '未识别'}。仓库包含 {snap.meta.file_count} 个已扫描文件、"
            f"约 {snap.meta.loc_total} 行可分析文本，当前抽取到 {len(parsed.symbols)} 个符号定义。"
        )

    def _build_system(self, snap: RepoSnapshot) -> Finding:
        build_files = [f for f in snap.files if f.lang == "build"]
        if not build_files:
            return Finding("未确认构建系统。", confidence="unconfirmed")
        evidences = [self._evidence_at(Path(snap.meta.root_path), item.path, 1, "config", "构建入口") for item in build_files[:5]]
        names = ", ".join(item.path for item in build_files[:5])
        return Finding(f"仓库包含构建入口：{names}。", confidence="high", evidence=evidences)

    def _find_dimension(self, snap: RepoSnapshot, parsed: ParsedRepo, dim: str, spec: dict) -> list[Finding]:
        root = Path(snap.meta.root_path)
        evidences = self._search_keywords(root, snap, spec["keywords"], spec.get("hints", []), limit=6)
        symbol_hits = self._symbol_hits(parsed, spec["keywords"], spec.get("hints", []), limit=5)
        findings: list[Finding] = []
        if evidences:
            findings.append(Finding(spec["statement"], confidence="high", evidence=evidences[:3]))
        else:
            findings.append(Finding(f"未确认{spec['title']}相关实现。", confidence="unconfirmed"))
        if symbol_hits:
            evidence = [
                self._evidence_at(root, sym.file, sym.line_start, "code", f"{sym.kind} {sym.name}")
                for sym in symbol_hits[:3]
            ]
            names = ", ".join(f"{sym.kind} {sym.name}" for sym in symbol_hits[:5])
            findings.append(Finding(f"相关符号包括：{names}。", confidence="medium", evidence=evidence))
        if dim == "syscall":
            syscall_symbols = [s for s in parsed.symbols if s.name.startswith("sys_") or "syscall" in s.name.lower()]
            if syscall_symbols:
                syscall_symbols = sorted(syscall_symbols, key=lambda item: self._path_score(item.file, ["syscall", "trap", "os/src"]))
                evidence = [
                    self._evidence_at(root, sym.file, sym.line_start, "code", f"{sym.kind} {sym.name}")
                    for sym in syscall_symbols[:5]
                ]
                findings.append(Finding(f"静态识别到 {len(syscall_symbols)} 个系统调用相关符号。", confidence="medium", evidence=evidence))
        return findings

    def _symbol_hits(self, parsed: ParsedRepo, keywords: list[str], hints: list[str], limit: int) -> list:
        lowered = [kw.lower() for kw in keywords]
        hint_words = [hint.lower() for hint in hints]
        hits = []
        for sym in sorted(parsed.symbols, key=lambda item: self._path_score(item.file, hint_words)):
            hay = f"{sym.name} {sym.file} {sym.signature}".lower()
            if any(kw.lower() in hay for kw in lowered):
                hits.append(sym)
                if len(hits) >= limit:
                    break
        return hits

    def _search_keywords(self, root: Path, snap: RepoSnapshot, keywords: list[str], hints: list[str], limit: int) -> list[Evidence]:
        pattern = re.compile("|".join(re.escape(kw) for kw in keywords), re.IGNORECASE)
        evidences: list[Evidence] = []
        hint_words = [hint.lower() for hint in hints]
        code_files = [entry for entry in snap.files if entry.lang in {"rust", "c", "asm"}]
        support_files = [entry for entry in snap.files if entry.lang in {"build", "toml"}]
        ordered = sorted(code_files, key=lambda item: self._path_score(item.path, hint_words)) + support_files
        for entry in ordered:
            path = root / entry.path
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for idx, line in enumerate(lines, start=1):
                if pattern.search(line):
                    evidences.append(self._snippet(entry.path, lines, idx, "code", "关键词命中"))
                    break
            if len(evidences) >= limit:
                break
        return evidences

    def _path_score(self, path: str, hints: list[str]) -> tuple[int, int, str]:
        lowered = path.lower()
        hint_penalty = 0 if any(hint in lowered for hint in hints) else 2
        role_penalty = self._path_role_penalty(lowered)
        return (role_penalty + hint_penalty, len(path), path)

    def _path_role_penalty(self, lowered_path: str) -> int:
        if any(hint in lowered_path for hint in LOW_PRIORITY_PATH_HINTS):
            return 8
        if any(hint in lowered_path for hint in KERNEL_PATH_HINTS):
            return 0
        if any(hint in lowered_path for hint in SUPPORT_PATH_HINTS):
            return 2
        return 4

    def _evidence_at(self, root: Path, rel: str, line_no: int, kind: str, note: str) -> Evidence:
        path = root / rel
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        return self._snippet(rel, lines, line_no, kind, note)

    def _snippet(self, rel: str, lines: list[str], line_no: int, kind: str, note: str) -> Evidence:
        start = max(1, line_no - 2)
        end = min(len(lines), line_no + 2)
        snippet = "\n".join(lines[start - 1:end])
        return Evidence(file=rel, line_start=start, line_end=end, snippet=snippet[:2000], kind=kind, note=note)
