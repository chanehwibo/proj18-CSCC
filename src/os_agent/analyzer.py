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
        "keywords": [
            "schedule", "scheduler", "switch_to", "context_switch", "swtch", "yield",
            "task", "thread", "proc", "stride", "run_queue", "ready_queue",
            "vTaskSwitchContext", "xTaskCreate",
        ],
        "hints": ["task", "tasks", "sched", "proc", "thread"],
        "statement": "项目包含任务/线程管理与调度相关实现。",
    },
    "memory": {
        "title": "内存管理",
        "keywords": [
            "page_table", "pagetable", "page table", "pgdir", "pgtab", "pte", "pde",
            "pte_", "pde_", "pgd_",
            "walkpgdir", "mappages", "setupkvm", "switchuvm", "allocuvm", "deallocuvm",
            "copyuvm", "kalloc", "kfree", "PGSIZE", "sv39", "satp", "frame_allocator",
            "frame_alloc", "heap_allocator", "pvPortMalloc", "vPortFree", "heap_",
            "memoryset", "pmm", "vmm", "copy_on_write", "cow",
        ],
        "hints": ["mm", "memory", "page", "frame", "heap", "vm", "pmm", "vmm", "kalloc", "alloc"],
        "statement": "项目包含页表、物理页、虚拟内存或堆分配等内存管理实现。",
    },
    "syscall": {
        "title": "系统调用",
        "keywords": ["syscall", "sys_", "ecall", "c_handle_syscall", "handle_syscall", "do_syscall"],
        "hints": ["syscall", "trap", "sys"],
        "statement": "项目包含系统调用入口、编号或分发逻辑。",
    },
    "filesystem": {
        "title": "文件系统",
        "keywords": [
            "inode", "vfs", "fat", "easy_fs", "dentry", "superblock",
            "bmap", "dirlookup", "readi", "writei", "fileread", "filewrite", "namei",
        ],
        "hints": ["fs", "file", "inode", "vfs", "fat", "dentry", "superblock"],
        "statement": "项目包含文件系统、VFS、inode、目录项或文件读写相关实现。",
    },
    "sync": {
        "title": "同步机制",
        "keywords": ["mutex", "spinlock", "spin_lock", "semaphore", "condvar", "rwlock", "lock", "clh_lock", "atomic"],
        "hints": ["sync", "lock", "mutex", "semaphore"],
        "statement": "项目包含锁、信号量或原子操作等同步机制。",
    },
    "interrupt": {
        "title": "中断与异常",
        "keywords": ["trap", "interrupt", "irq", "isr", "plic", "clint", "timer", "mtimecmp", "exception"],
        "hints": ["trap", "interrupt", "irq", "isr", "timer", "plic", "clint"],
        "statement": "项目包含 trap、中断、异常或定时器处理逻辑。",
    },
    "driver": {
        "title": "设备驱动",
        "keywords": [
            "virtio", "virtio_", "uart", "uartinit", "uartgetc", "driver", "blk", "blk_",
            "console", "consoleintr", "ns16550", "device", "ide", "ideinit", "iderw",
            "ideintr", "kbd", "kbdgetc", "lapic", "lapicinit", "ioapic", "ioapicinit",
            "serial",
        ],
        "hints": ["driver", "drivers", "virtio", "uart", "blk", "device", "ide", "kbd", "console", "lapic", "ioapic"],
        "statement": "项目包含串口、块设备、控制台、中断控制器或 virtio 等设备驱动相关实现。",
    },
}


IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9_]+$")
PATH_TOKEN_RE = re.compile(r"[^a-z0-9]+")
INLINE_COMMENT_RE = re.compile(r"/\*.*?\*/|//.*$")


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
        search_limit = 20 if dim in {"syscall", "sync", "driver"} else 6
        search_keywords = spec["keywords"]
        if dim == "syscall":
            search_keywords = [keyword for keyword in search_keywords if keyword != "sys_"]
        evidences = self._search_keywords(root, snap, search_keywords, spec.get("hints", []), limit=search_limit)
        evidences = self._filter_dimension_evidence(dim, evidences)[:6]
        symbol_hits = self._symbol_hits(
            parsed,
            self._symbol_keywords(dim, spec["keywords"]),
            self._symbol_hints(dim, spec.get("hints", [])),
            limit=5,
        )
        findings: list[Finding] = []
        if evidences:
            statement = spec["statement"]
            confidence = "high"
            if dim == "syscall" and self._has_syscall_stub_marker(evidences):
                statement = (
                    "项目包含系统调用入口或兼容层线索，但源码片段显示部分调用仍是 stub/未实现，"
                    "应按接口线索而非完整系统调用实现解读。"
                )
                confidence = "medium"
            findings.append(Finding(statement, confidence=confidence, evidence=evidences[:3]))
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

    def _filter_dimension_evidence(self, dim: str, evidences: list[Evidence]) -> list[Evidence]:
        if dim == "syscall":
            return [ev for ev in evidences if self._is_syscall_evidence(ev)]
        if dim == "sync":
            return [ev for ev in evidences if self._is_sync_evidence(ev)]
        if dim == "driver":
            return [ev for ev in evidences if self._is_driver_evidence(ev)]
        return evidences

    def _is_syscall_evidence(self, ev: Evidence) -> bool:
        path = ev.file.lower()
        if "syscall" in path:
            return True
        if path.startswith("portable/"):
            return False
        if "portyield" in ev.snippet.lower():
            return False
        lowercase_sys_prefix = re.compile(r"(?<![A-Za-z0-9_])sys_[a-z0-9_]*(?![A-Za-z0-9_])")
        explicit_entry = re.compile(
            r"(?<![A-Za-z0-9_])(ecall|c_handle_syscall|handle_syscall|do_syscall)(?![A-Za-z0-9_])",
            re.IGNORECASE,
        )
        return bool(lowercase_sys_prefix.search(ev.snippet) or explicit_entry.search(ev.snippet))

    def _is_sync_evidence(self, ev: Evidence) -> bool:
        path = ev.file.lower()
        if any(part in path for part in ("lock", "sync", "mutex", "semaphore", "atomic", "smp")):
            return True
        strong = re.compile(
            r"(?<![A-Za-z0-9_])("
            r"mutex|spinlock|spin_lock|semaphore|condvar|rwlock|clh_lock|atomic|lock_[A-Za-z0-9_]*"
            r")(?![A-Za-z0-9_])",
            re.IGNORECASE,
        )
        return bool(strong.search(ev.snippet))

    def _is_driver_evidence(self, ev: Evidence) -> bool:
        path = ev.file.lower()
        if any(part in path for part in ("driver", "drivers", "uart", "virtio", "ide", "kbd", "console", "lapic", "ioapic", "serial", "ns16550", "blk")):
            return True
        strong = re.compile(
            r"(?<![A-Za-z0-9_])("
            r"virtio_[A-Za-z0-9_]*|uartinit|uartgetc|consoleintr|ideinit|iderw|ideintr|"
            r"kbdgetc|lapicinit|ioapicinit|ns16550"
            r")(?![A-Za-z0-9_])",
            re.IGNORECASE,
        )
        return bool(strong.search(ev.snippet))

    def _symbol_hits(self, parsed: ParsedRepo, keywords: list[str], hints: list[str], limit: int) -> list:
        pattern = self._compile_keyword_pattern(keywords)
        hint_words = [hint.lower() for hint in hints]
        hits = []
        seen: set[tuple[str, str, str]] = set()
        for sym in sorted(parsed.symbols, key=lambda item: self._path_score(item.file, hint_words)):
            if self._path_role_penalty(sym.file.lower()) >= 8:
                continue
            symbol_hay = self._symbol_search_text(sym)
            path_hit = self._path_has_hint(sym.file, hint_words)
            direct_hit = bool(pattern.search(symbol_hay))
            path_context_hit = path_hit and sym.kind in {"fn", "struct", "class", "enum", "trait"}
            if direct_hit or path_context_hit:
                key = (sym.kind, sym.name, sym.file)
                if key in seen:
                    continue
                seen.add(key)
                hits.append(sym)
                if len(hits) >= limit:
                    break
        return hits

    def _symbol_hints(self, dim: str, hints: list[str]) -> list[str]:
        if dim == "syscall":
            return [hint for hint in hints if hint != "sys"]
        return hints

    def _symbol_keywords(self, dim: str, keywords: list[str]) -> list[str]:
        if dim == "interrupt":
            return [keyword for keyword in keywords if keyword != "exception"]
        return keywords

    def _has_syscall_stub_marker(self, evidences: list[Evidence]) -> bool:
        stub_markers = ("enosys", "not implemented", "stub", "stubtrace")
        return any(marker in ev.snippet.lower() for ev in evidences for marker in stub_markers)

    def _symbol_search_text(self, sym) -> str:
        if sym.kind == "macro":
            return sym.name
        return f"{sym.name} {self._strip_inline_comment(sym.signature)}"

    def _strip_inline_comment(self, text: str) -> str:
        return INLINE_COMMENT_RE.sub("", text)

    def _search_keywords(self, root: Path, snap: RepoSnapshot, keywords: list[str], hints: list[str], limit: int) -> list[Evidence]:
        pattern = self._compile_keyword_pattern(keywords)
        evidences: list[Evidence] = []
        hint_words = [hint.lower() for hint in hints]
        code_files = [entry for entry in snap.files if entry.lang in {"rust", "c", "cpp", "asm"}]
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

    def _compile_keyword_pattern(self, keywords: list[str]) -> re.Pattern[str]:
        pieces: list[str] = []
        for keyword in sorted(keywords, key=len, reverse=True):
            escaped = re.escape(keyword)
            if keyword.endswith("_") and IDENTIFIER_RE.fullmatch(keyword):
                pieces.append(rf"(?<![A-Za-z0-9_]){escaped}[A-Za-z0-9_]*")
            elif IDENTIFIER_RE.fullmatch(keyword):
                pieces.append(rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])")
            else:
                pieces.append(escaped)
        return re.compile("|".join(pieces), re.IGNORECASE)

    def _path_score(self, path: str, hints: list[str]) -> tuple[int, int, str]:
        lowered = path.lower()
        hint_penalty = 0 if self._path_has_hint(lowered, hints) else 2
        role_penalty = self._path_role_penalty(lowered)
        return (role_penalty + hint_penalty, len(path), path)

    def _path_has_hint(self, path: str, hints: list[str]) -> bool:
        lowered = path.lower()
        tokens = {token for token in PATH_TOKEN_RE.split(lowered) if token}
        for hint in hints:
            lowered_hint = hint.lower()
            if not lowered_hint:
                continue
            if lowered_hint in tokens:
                return True
            if "_" in lowered_hint and lowered_hint in lowered:
                return True
        return False

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
