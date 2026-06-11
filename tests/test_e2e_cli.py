import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from os_agent import cli


def write_mini_os_repo(root: Path, *, name: str, repo_id: str, arch: str = "riscv64") -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / ".kernelsage_meta.json").write_text(
        json.dumps(
            {
                "repo_id": repo_id,
                "name": name,
                "style": "teaching-monolithic",
                "arch": [arch],
                "source_tier": "competition_sample",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (root / "README.md").write_text(
        f"# {name}\n\nA tiny teaching OS with scheduler, virtual memory, syscall, fs, trap and uart driver.\n",
        encoding="utf-8",
    )
    (root / "Makefile").write_text("all:\n\t@echo build mini os\n", encoding="utf-8")

    kernel = root / "kernel"
    drivers = root / "drivers"
    kernel.mkdir()
    drivers.mkdir()
    (kernel / "proc.c").write_text(
        "struct proc { int pid; int state; };\n"
        "void context_switch(void) { }\n"
        "void schedule(void) { context_switch(); }\n"
        "void yield(void) { schedule(); }\n",
        encoding="utf-8",
    )
    (kernel / "mm.c").write_text(
        "#define PGSIZE 4096\n"
        "struct pte { unsigned long bits; };\n"
        "void kalloc(void) { }\n"
        "void mappages(void) { kalloc(); }\n",
        encoding="utf-8",
    )
    (kernel / "syscall.c").write_text(
        "void sys_write(void) { }\n"
        "void handle_syscall(void) { sys_write(); }\n"
        "void syscall(void) { handle_syscall(); }\n",
        encoding="utf-8",
    )
    (kernel / "fs.c").write_text(
        "struct inode { int inum; };\n"
        "void readi(void) { }\n"
        "void writei(void) { }\n"
        "void namei(void) { readi(); }\n",
        encoding="utf-8",
    )
    (kernel / "sync.c").write_text(
        "struct spinlock { int locked; };\n"
        "void atomic_add(void) { }\n"
        "void lock_acquire(struct spinlock *lock) { atomic_add(); }\n",
        encoding="utf-8",
    )
    (kernel / "trap.c").write_text(
        "void timer_interrupt(void) { }\n"
        "void trap(void) { timer_interrupt(); }\n"
        "void irq_handler(void) { trap(); }\n",
        encoding="utf-8",
    )
    (drivers / "uart.c").write_text(
        "#define UART0 0x10000000\n"
        "void uartinit(void) { }\n"
        "void uartgetc(void) { }\n"
        "void consoleintr(void) { uartgetc(); }\n",
        encoding="utf-8",
    )


class CliEndToEndTest(unittest.TestCase):
    def test_describe_cli_generates_profile_and_evidence_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "new-mini-os"
            reports = root / "reports"
            profiles = root / "profiles"
            samples = root / "samples"
            samples.mkdir()
            write_mini_os_repo(repo, name="New Mini OS", repo_id="new-mini-os")

            with (
                patch.object(cli, "REPORTS_DIR", reports),
                patch.object(cli, "PROFILES_DIR", profiles),
                patch.object(cli, "SAMPLES_DIR", samples),
            ):
                out = reports / "describe" / "new-mini-os.md"
                code = cli.cmd_describe(
                    argparse.Namespace(
                        repo=str(repo),
                        repo_id="new-mini-os",
                        out=str(out),
                        use_llm=False,
                        llm_dry_run=False,
                        no_profile_cache=True,
                        rebuild_profile_cache=False,
                    )
                )

            report = out.read_text(encoding="utf-8")
            profile = profiles / "new-mini-os.json"
            profile_exists = profile.exists()

        self.assertEqual(code, 0)
        self.assertTrue(profile_exists)
        self.assertIn("# New Mini OS 项目描述报告", report)
        self.assertIn("## 摘要评分", report)
        self.assertIn("## 调度与任务管理", report)
        self.assertIn("## 附录：核验摘要", report)
        self.assertRegex(report, r"kernel/proc\.c.*L\d+-L\d+")

    def test_compare_cli_selects_history_and_generates_compare_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            new_repo = root / "new-mini-os"
            history_root = root / "history"
            history_repo = history_root / "history-mini-os"
            unrelated_repo = history_root / "unrelated-docs"
            reports = root / "reports"
            profiles = root / "profiles"
            samples = root / "samples"
            history_root.mkdir()
            samples.mkdir()
            write_mini_os_repo(new_repo, name="New Mini OS", repo_id="new-mini-os")
            write_mini_os_repo(history_repo, name="History Mini OS", repo_id="history-mini-os")
            unrelated_repo.mkdir()
            (unrelated_repo / "README.md").write_text("# docs only\n", encoding="utf-8")

            with (
                patch.object(cli, "REPORTS_DIR", reports),
                patch.object(cli, "PROFILES_DIR", profiles),
                patch.object(cli, "SAMPLES_DIR", samples),
            ):
                out = reports / "compare" / "new-mini-os_vs_history.md"
                code = cli.cmd_compare(
                    argparse.Namespace(
                        new=str(new_repo),
                        history=str(history_root),
                        repo_id="new-mini-os",
                        limit=1,
                        out=str(out),
                        use_llm=False,
                        llm_dry_run=False,
                        no_profile_cache=True,
                        rebuild_profile_cache=False,
                    )
                )

            report = out.read_text(encoding="utf-8")

        self.assertEqual(code, 0)
        self.assertIn("# New Mini OS 比较报告", report)
        self.assertIn("## 历史样本选择", report)
        self.assertIn("History Mini OS", report)
        self.assertNotIn("unrelated-docs", report)
        self.assertIn("## 功能重合与疑似重复证据", report)
        self.assertIn("## 代码级相似线索检测", report)
        self.assertRegex(report, r"kernel/proc\.c.*L\d+-L\d+")
        self.assertIn("## 附录：核验摘要", report)


if __name__ == "__main__":
    unittest.main()
