"""Repository structure parsing utilities."""

from __future__ import annotations

import re
from pathlib import Path

from .models import ParsedRepo, RepoSnapshot, SymbolDef


RUST_PATTERNS = [
    ("fn", re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?(?:unsafe\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)\b")),
    ("struct", re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?struct\s+([A-Za-z_][A-Za-z0-9_]*)\b")),
    ("enum", re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?enum\s+([A-Za-z_][A-Za-z0-9_]*)\b")),
    ("trait", re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?trait\s+([A-Za-z_][A-Za-z0-9_]*)\b")),
    ("impl", re.compile(r"^\s*impl(?:<[^>]*>)?\s+([^{]+)")),
]

C_FUNC_PATTERN = re.compile(
    r"^\s*(?:static\s+)?(?:inline\s+)?[A-Za-z_][A-Za-z0-9_\s\*]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*\{"
)
C_TYPE_PATTERNS = [
    ("struct", re.compile(r"^\s*(?:typedef\s+)?struct\s+([A-Za-z_][A-Za-z0-9_]*)?\b")),
    ("enum", re.compile(r"^\s*(?:typedef\s+)?enum\s+([A-Za-z_][A-Za-z0-9_]*)?\b")),
]
C_CONTROL_PREFIXES = (
    "if",
    "else",
    "for",
    "while",
    "switch",
    "do",
    "return",
)
C_CONTROL_NAMES = {"if", "else", "for", "while", "switch", "do", "return", "sizeof"}


class SymbolParser:
    def parse_repo(self, snap: RepoSnapshot) -> ParsedRepo:
        root = Path(snap.meta.root_path)
        symbols: list[SymbolDef] = []
        for entry in snap.files:
            if entry.lang not in {"rust", "c", "asm"}:
                continue
            path = root / entry.path
            text = path.read_text(encoding="utf-8", errors="ignore")
            if entry.lang == "rust":
                symbols.extend(self._parse_rust(entry.path, text))
            elif entry.lang == "c":
                symbols.extend(self._parse_c(entry.path, text))
            elif entry.lang == "asm":
                symbols.extend(self._parse_asm(entry.path, text))
        return ParsedRepo(repo_id=snap.meta.repo_id, symbols=symbols)

    def _parse_rust(self, rel: str, text: str) -> list[SymbolDef]:
        symbols: list[SymbolDef] = []
        for line_no, line in enumerate(text.splitlines(), start=1):
            for kind, pattern in RUST_PATTERNS:
                match = pattern.search(line)
                if not match:
                    continue
                name = match.group(1).strip()
                if kind == "impl":
                    name = name.replace(" for ", "::for::").strip()
                symbols.append(SymbolDef(name=name, kind=kind, file=rel, line_start=line_no, line_end=line_no, signature=line.strip()))
                break
        return symbols

    def _parse_c(self, rel: str, text: str) -> list[SymbolDef]:
        symbols: list[SymbolDef] = []
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            leading = stripped.split(maxsplit=1)[0] if stripped else ""
            if leading in C_CONTROL_PREFIXES:
                continue
            func = C_FUNC_PATTERN.search(line)
            if func:
                name = func.group(1)
                if name in C_CONTROL_NAMES:
                    continue
                symbols.append(SymbolDef(name=name, kind="fn", file=rel, line_start=line_no, line_end=line_no, signature=line.strip()))
                continue
            for kind, pattern in C_TYPE_PATTERNS:
                match = pattern.search(line)
                if match and match.group(1):
                    symbols.append(SymbolDef(name=match.group(1), kind=kind, file=rel, line_start=line_no, line_end=line_no, signature=line.strip()))
                    break
        return symbols

    def _parse_asm(self, rel: str, text: str) -> list[SymbolDef]:
        symbols: list[SymbolDef] = []
        globl = re.compile(r"^\s*\.globl\s+([A-Za-z_][A-Za-z0-9_]*)")
        label = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):")
        globals_seen: set[str] = set()
        for line_no, line in enumerate(text.splitlines(), start=1):
            g = globl.search(line)
            if g:
                globals_seen.add(g.group(1))
                continue
            l = label.search(line)
            if l and l.group(1) in globals_seen:
                symbols.append(SymbolDef(name=l.group(1), kind="fn", file=rel, line_start=line_no, line_end=line_no, signature=line.strip()))
        return symbols
