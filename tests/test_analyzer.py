import unittest

from os_agent.analyzer import KernelAnalyzer
from os_agent.models import Evidence, ParsedRepo, SymbolDef


class KernelAnalyzerPathPriorityTest(unittest.TestCase):
    def test_kernel_paths_rank_before_docs_and_tools(self):
        analyzer = KernelAnalyzer()
        paths = [
            "outline.md",
            "xtask/src/arch.rs",
            "user/src/main.rs",
            "os/src/trap/mod.rs",
            "kernel/proc.c",
        ]

        ranked = sorted(paths, key=lambda path: analyzer._path_score(path, ["trap", "proc"]))

        self.assertEqual(ranked[:2], ["kernel/proc.c", "os/src/trap/mod.rs"])
        self.assertLess(ranked.index("kernel/proc.c"), ranked.index("outline.md"))
        self.assertLess(ranked.index("os/src/trap/mod.rs"), ranked.index("xtask/src/arch.rs"))
        self.assertLess(ranked.index("os/src/trap/mod.rs"), ranked.index("user/src/main.rs"))

    def test_symbol_hits_do_not_report_unrelated_macros_from_matching_path(self):
        parsed = ParsedRepo(
            repo_id="case",
            symbols=[
                SymbolDef("INC_TASK_H", "macro", "include/task.h", 1, 1, "#define INC_TASK_H"),
                SymbolDef("tskTaskControlBlock", "struct", "include/task.h", 10, 10, "struct tskTaskControlBlock;"),
                SymbolDef("schedule", "fn", "kernel/sched.c", 20, 20, "void schedule(void) {}"),
            ],
        )

        hits = KernelAnalyzer()._symbol_hits(
            parsed,
            ["schedule", "task", "thread", "proc"],
            ["task", "sched", "proc", "thread"],
            limit=5,
        )

        names = [symbol.name for symbol in hits]
        self.assertIn("tskTaskControlBlock", names)
        self.assertIn("schedule", names)
        self.assertNotIn("INC_TASK_H", names)

    def test_symbol_hits_ignore_keyword_only_in_macro_comment(self):
        parsed = ParsedRepo(
            repo_id="case",
            symbols=[
                SymbolDef(
                    "AT91C_MC_LOCKE",
                    "macro",
                    "portable/IAR/AtmelSAM7S64/AT91SAM7S64.h",
                    579,
                    579,
                    "#define AT91C_MC_LOCKE 0x4 /* Lock Error */",
                ),
                SymbolDef("spinlock", "struct", "include/sync/lock.h", 10, 10, "struct spinlock { int locked; };"),
            ],
        )

        hits = KernelAnalyzer()._symbol_hits(
            parsed,
            ["mutex", "spinlock", "spin_lock", "semaphore", "condvar", "rwlock", "lock", "clh_lock", "atomic"],
            ["sync", "lock", "mutex", "semaphore"],
            limit=5,
        )

        names = [symbol.name for symbol in hits]
        self.assertIn("spinlock", names)
        self.assertNotIn("AT91C_MC_LOCKE", names)

    def test_path_hints_match_tokens_not_substrings(self):
        parsed = ParsedRepo(
            repo_id="case",
            symbols=[
                SymbolDef("begin", "fn", "src/kernel/profile.cpp", 56, 56, "void begin() {}"),
                SymbolDef("MBR", "struct", "api/fs/mbr.hpp", 25, 25, "struct MBR {"),
            ],
        )

        hits = KernelAnalyzer()._symbol_hits(
            parsed,
            ["inode", "vfs", "fat", "dentry", "superblock", "readi", "writei"],
            ["fs", "file", "inode", "vfs", "fat", "dentry", "superblock"],
            limit=5,
        )

        names = [symbol.name for symbol in hits]
        self.assertIn("MBR", names)
        self.assertNotIn("begin", names)

    def test_symbol_hits_skip_low_priority_paths(self):
        parsed = ParsedRepo(
            repo_id="case",
            symbols=[
                SymbolDef("irq", "fn", "test/integration/virtio.hpp", 307, 307, "int irq() { return 0; }"),
                SymbolDef("irq", "fn", "src/drivers/ide.cpp", 152, 152, "int irq() { return 1; }"),
            ],
        )

        hits = KernelAnalyzer()._symbol_hits(
            parsed,
            ["trap", "interrupt", "irq", "isr", "plic", "clint", "timer"],
            ["trap", "interrupt", "irq", "isr", "timer", "plic", "clint"],
            limit=5,
        )

        files = [symbol.file for symbol in hits]
        self.assertIn("src/drivers/ide.cpp", files)
        self.assertNotIn("test/integration/virtio.hpp", files)

    def test_syscall_symbol_hints_skip_generic_sys_path(self):
        analyzer = KernelAnalyzer()

        self.assertEqual(analyzer._symbol_hints("syscall", ["syscall", "trap", "sys"]), ["syscall", "trap"])

    def test_syscall_stub_marker_detects_incomplete_entries(self):
        analyzer = KernelAnalyzer()
        evidences = [
            Evidence("src/musl/syscall_n.cpp", 1, 3, "long syscall(long number) { return -ENOSYS; }"),
            Evidence("src/arch/x86_64/syscall_entry.cpp", 22, 26, 'os::panic("Syscalls are not implemented");'),
        ]

        self.assertTrue(analyzer._has_syscall_stub_marker(evidences))

    def test_interrupt_symbol_keywords_do_not_use_generic_exception(self):
        analyzer = KernelAnalyzer()

        self.assertNotIn("exception", analyzer._symbol_keywords("interrupt", ["trap", "exception", "irq"]))


if __name__ == "__main__":
    unittest.main()
