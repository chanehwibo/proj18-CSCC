"""Tests for the web console site builder and renderer."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from os_agent.web_console import WebConsoleBuilder, clone_command, entry_number, year_from_entry
from os_agent.web_render import SiteRenderer, markdown_to_html
from os_agent.models import RepoMeta


def _write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _make_mini_os(root: Path) -> None:
    _write(root, "Makefile", "all:\n\tgcc kernel/main.c\n")
    _write(root, "kernel/proc.c", "void scheduler(){ swtch(); }\nstruct proc { int pid; };\n")
    _write(root, "kernel/vm.c", "pte_t* walkpgdir(){ return mappages(); }\nvoid kalloc(){}\n")
    _write(root, "kernel/syscall.c", "void syscall(){ sys_fork(); }\n#define SYS_fork 1\n")
    _write(root, "kernel/trap.c", "void trap(){ /* interrupt */ }\nvoid plic_init(){}\n")
    _write(root, "kernel/fs.c", "struct inode { int n; };\nvoid readi(){}\n")
    _write(root, "kernel/spinlock.c", "struct spinlock { int locked; };\nvoid acquire(){}\n")
    _write(root, "kernel/uart.c", "void uartinit(){}\n#define RHR 0\n")


class TestWebHelpers(unittest.TestCase):
    def test_entry_number_from_url(self):
        meta = RepoMeta(repo_id="x", name="X", url="https://gitlab.eduxiji.net/T202410003993220-1450/p.git")
        self.assertEqual(entry_number(meta), "T202410003993220-1450")

    def test_entry_number_fallback_repo_id(self):
        meta = RepoMeta(repo_id="my-repo", name="X", url=None)
        self.assertEqual(entry_number(meta), "my-repo")

    def test_year_from_entry(self):
        self.assertEqual(year_from_entry("T202410003993220-1450"), "2024")
        self.assertEqual(year_from_entry("T202518123995568-675"), "2025")
        self.assertIsNone(year_from_entry("no-year-here"))

    def test_clone_command(self):
        self.assertEqual(clone_command("https://x.com/a.git"), "git clone https://x.com/a.git")
        self.assertEqual(clone_command(None), "未提供")
        self.assertEqual(clone_command("not-a-url"), "未提供")


class TestMarkdownRenderer(unittest.TestCase):
    def test_headings_and_lists(self):
        html = markdown_to_html("# Title\n\n- a\n- b\n")
        self.assertIn("<h1>Title</h1>", html)
        self.assertIn("<li>a</li>", html)

    def test_table(self):
        html = markdown_to_html("| h1 | h2 |\n| --- | --- |\n| a | b |\n")
        self.assertIn("<table>", html)
        self.assertIn("<th>h1</th>", html)
        self.assertIn("<td>a</td>", html)

    def test_html_escaped(self):
        html = markdown_to_html("<script>x</script>")
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_inline_bold_code(self):
        html = markdown_to_html("**bold** and `code`")
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<code>code</code>", html)


class TestSiteBuild(unittest.TestCase):
    def test_build_and_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            samples = tmp / "samples"
            new_repo = tmp / "inputs" / "team-x"
            _make_mini_os(new_repo)
            _make_mini_os(samples / "history-os")

            builder = WebConsoleBuilder(samples_dir=samples)
            inputs = {"2025": [{"repo_id": "team-x", "path": str(new_repo), "entry_no": "T202510001999999-1",
                                "url": "https://gitlab.eduxiji.net/T202510001999999-1/p.git"}]}
            data = builder.build_site_data(inputs, samples, years=["2025"], top_n=1)

            self.assertIn("years", data)
            year = next(y for y in data["years"] if y["year"] == "2025")
            self.assertEqual(year["count"], 1)
            card = year["projects"][0]
            self.assertEqual(card["entry_no"], "T202510001999999-1")
            self.assertEqual(card["year"], "2025")  # resolved from entry number
            self.assertIn("describe_md", card["reports"])
            self.assertTrue(card["reports"]["compares"])  # at least one comparison

            out = tmp / "site"
            SiteRenderer().render(data, out)
            self.assertTrue((out / "index.html").exists())
            self.assertTrue((out / "baseline.html").exists())
            self.assertTrue((out / "assets" / "style.css").exists())
            index = (out / "index.html").read_text(encoding="utf-8")
            self.assertIn("T202510001999999-1", index)
            self.assertIn("git clone", index)  # mirror shows clone command

    def test_year_regrouped_by_entry_number(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            samples = tmp / "samples"
            _make_mini_os(samples / "history-os")
            repo = tmp / "inputs" / "old-work"
            _make_mini_os(repo)

            builder = WebConsoleBuilder(samples_dir=samples)
            # placed under 2026 key but entry number says 2024 -> must land in 2024
            inputs = {"2026": [{"repo_id": "old-work", "path": str(repo), "entry_no": "T202410001999999-1"}]}
            data = builder.build_site_data(inputs, samples, years=["2024", "2025", "2026"], top_n=1)
            y2024 = next(y for y in data["years"] if y["year"] == "2024")
            y2026 = next(y for y in data["years"] if y["year"] == "2026")
            self.assertEqual(y2024["count"], 1)
            self.assertEqual(y2026["count"], 0)
            # years are in ascending order
            years = [y["year"] for y in data["years"]]
            self.assertEqual(years, sorted(years))


if __name__ == "__main__":
    unittest.main()
