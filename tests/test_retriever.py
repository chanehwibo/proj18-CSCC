import argparse
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from os_agent import cli
from os_agent.indexer import EvidenceIndexer
from os_agent.retriever import EvidenceRetriever


class EvidenceRetrieverTest(unittest.TestCase):
    def _write_samples(self, root: Path) -> Path:
        samples = root / "samples"
        samples.mkdir()
        manifest = {
            "repos": [
                {
                    "repo_id": "sched-os",
                    "name": "Scheduler OS",
                    "url": "https://example.com/sched-os.git",
                    "source_tier": "competition_sample",
                },
                {
                    "repo_id": "vm-os",
                    "name": "VM OS",
                    "url": "https://example.com/vm-os.git",
                    "source_tier": "verified_award",
                    "award_level": "一等奖",
                    "award_source_url": "https://example.com/winners",
                },
                {
                    "repo_id": "syscall-os",
                    "name": "Syscall OS",
                    "url": "https://example.com/syscall-os.git",
                    "source_tier": "teaching_baseline",
                },
            ]
        }
        (samples / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

        sched = samples / "sched-os" / "kernel"
        sched.mkdir(parents=True)
        (sched / "proc.c").write_text(
            "struct proc *current;\n"
            "void schedule(void) {\n"
            "    context_switch(current);\n"
            "}\n",
            encoding="utf-8",
        )

        vm = samples / "vm-os" / "kernel"
        vm.mkdir(parents=True)
        (vm / "vm.c").write_text(
            "typedef unsigned long pte_t;\n"
            "pte_t *walkpagetable(pagetable_t pagetable, unsigned long va) {\n"
            "    return &pagetable[va];\n"
            "}\n",
            encoding="utf-8",
        )

        syscall = samples / "syscall-os" / "kernel"
        syscall.mkdir(parents=True)
        (syscall / "syscall.c").write_text(
            "long do_syscall(int nr) {\n"
            "    return sys_write(nr);\n"
            "}\n",
            encoding="utf-8",
        )
        return samples

    def test_chinese_query_expands_to_os_dimension_keywords(self):
        with tempfile.TemporaryDirectory() as tmp:
            samples = self._write_samples(Path(tmp))
            index = EvidenceIndexer().build_samples_index(samples)

            sched_hits = EvidenceRetriever().query(index, "调度器", limit=3).hits
            vm_hits = EvidenceRetriever().query(index, "页表", limit=3).hits
            syscall_hits = EvidenceRetriever().query(index, "系统调用", limit=3).hits

        self.assertEqual(sched_hits[0].repo_id, "sched-os")
        self.assertEqual(sched_hits[0].file, "kernel/proc.c")
        self.assertIn("schedule", sched_hits[0].matched_terms)
        self.assertEqual(vm_hits[0].repo_id, "vm-os")
        self.assertEqual(vm_hits[0].file, "kernel/vm.c")
        self.assertIn("pagetable", vm_hits[0].matched_terms)
        self.assertEqual(syscall_hits[0].repo_id, "syscall-os")
        self.assertEqual(syscall_hits[0].file, "kernel/syscall.c")

    def test_query_evidence_cli_outputs_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            samples = self._write_samples(Path(tmp))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = cli.cmd_query_evidence(
                    argparse.Namespace(
                        query="系统调用",
                        samples=str(samples),
                        repo_id=None,
                        limit=2,
                        max_files_per_repo=300,
                        json=True,
                    )
                )

        payload = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(payload["summary"]["repos"], 3)
        self.assertEqual(payload["summary"]["hits"], 1)
        self.assertEqual(payload["hits"][0]["repo_id"], "syscall-os")

    def test_query_evidence_parser(self):
        args = cli.build_parser().parse_args(["query-evidence", "调度器/页表", "--limit", "5", "--repo-id", "sched-os"])

        self.assertIs(args.func, cli.cmd_query_evidence)
        self.assertEqual(args.query, "调度器/页表")
        self.assertEqual(args.limit, 5)
        self.assertEqual(args.max_files_per_repo, 300)
        self.assertEqual(args.repo_id, ["sched-os"])


if __name__ == "__main__":
    unittest.main()
