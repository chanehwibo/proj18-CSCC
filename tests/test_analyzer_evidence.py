import tempfile
import unittest
from pathlib import Path

from os_agent.analyzer import KernelAnalyzer
from os_agent.collector import RepoCollector
from os_agent.parser import SymbolParser


class KernelAnalyzerEvidenceTest(unittest.TestCase):
    def test_markdown_keyword_does_not_confirm_os_dimension(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("This document mentions syscall and scheduler.\n", encoding="utf-8")
            snapshot = RepoCollector().from_local(root, repo_id="doc-only")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["syscall"][0].confidence, "unconfirmed")
        self.assertEqual(profile.dimensions["scheduler"][0].confidence, "unconfirmed")

    def test_xv6_style_memory_management_is_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "vm.c").write_text(
                "pde_t *pgdir;\n"
                "pte_t *walkpgdir(pde_t *pgdir, const void *va, int alloc) { return 0; }\n"
                "int mappages(pde_t *pgdir, void *va, uint size, uint pa, int perm) { return 0; }\n",
                encoding="utf-8",
            )
            (root / "kalloc.c").write_text(
                "char *kalloc(void) { return 0; }\nvoid kfree(char *v) {}\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="xv6-memory")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["memory"][0].confidence, "high")
        evidence_files = {ev.file for ev in profile.dimensions["memory"][0].evidence}
        self.assertTrue({"vm.c", "kalloc.c"} & evidence_files)

    def test_superblock_does_not_confirm_driver_dimension(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "fs.c").write_text(
                "struct superblock { int size; };\n"
                "// block allocator for file system data\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="fs-only")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["filesystem"][0].confidence, "high")
        self.assertEqual(profile.dimensions["driver"][0].confidence, "unconfirmed")

    def test_filesystem_keywords_do_not_match_common_substrings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "boot.c").write_text(
                "/* fatal boot error */\n"
                "/* reading the timer register */\n"
                "void ready_list_tick(void) {}\n"
                "unsigned smmu_read_reg32(void) { return 0; }\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="substring-only")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["filesystem"][0].confidence, "unconfirmed")

    def test_configmax_syscall_interrupt_priority_is_not_a_syscall(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "list.c").write_text(
                "/* configMAX_SYSCALL_INTERRUPT_PRIORITY is an interrupt mask setting. */\n"
                "/* Trap Class 6, the SYSCALL, is used by the port layer. */\n"
                "/* Ensure the interrupt mask is set to the syscall priority. */\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="freertos-config")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["syscall"][0].confidence, "unconfirmed")

    def test_portable_yield_ecall_is_not_a_syscall_interface(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            portable = root / "portable" / "GCC" / "RISC-V"
            portable.mkdir(parents=True)
            (portable / "portmacro.h").write_text(
                "/* Scheduler utilities. */\n"
                "extern void vTaskSwitchContext( void );\n"
                "#define portYIELD() __asm volatile ( \"ecall\" );\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="portable-ecall")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["syscall"][0].confidence, "unconfirmed")

    def test_clock_text_does_not_confirm_locking(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "timer.c").write_text(
                "/* The boot code reads the clock and synchronizes timer ticks. */\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="clock-only")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["sync"][0].confidence, "unconfirmed")

    def test_xv6_style_driver_names_are_confirmed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ide.c").write_text(
                "void ideinit(void) {}\n"
                "void iderw(void) {}\n"
                "void ideintr(void) {}\n",
                encoding="utf-8",
            )
            (root / "license.c").write_text(
                "/* provided free of charge */\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="xv6-driver")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["driver"][0].confidence, "high")
        evidence_files = {ev.file for ev in profile.dimensions["driver"][0].evidence}
        self.assertIn("ide.c", evidence_files)

    def test_driver_examples_in_headers_do_not_confirm_driver_implementation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            include = root / "include"
            include.mkdir()
            (include / "task.h").write_text(
                "/* Driver library function used to receive bytes from a UART interrupt. */\n"
                "/* No concrete UART, serial or block driver is implemented here. */\n",
                encoding="utf-8",
            )
            snapshot = RepoCollector().from_local(root, repo_id="driver-comment-only")
            parsed = SymbolParser().parse_repo(snapshot)

            profile = KernelAnalyzer().analyze(snapshot, parsed)

        self.assertEqual(profile.dimensions["driver"][0].confidence, "unconfirmed")


if __name__ == "__main__":
    unittest.main()
