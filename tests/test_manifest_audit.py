import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from os_agent import cli
from os_agent.manifest_audit import ManifestAuditor


class ManifestAuditTest(unittest.TestCase):
    def _write_manifest(self, root: Path, repos: list[dict]) -> Path:
        path = root / "manifest.json"
        path.write_text(json.dumps({"repos": repos}, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def test_manifest_audit_accepts_trusted_sample_with_recorded_head(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            samples = root / "samples"
            samples.mkdir()
            repo = samples / "award-os"
            repo.mkdir()
            (repo / ".kernelsage_meta.json").write_text(
                json.dumps({"head_sha": "abc123"}, ensure_ascii=False),
                encoding="utf-8",
            )
            source = root / "winners.md"
            source.write_text("official winners", encoding="utf-8")
            manifest = self._write_manifest(
                root,
                [
                    {
                        "repo_id": "award-os",
                        "name": "Award OS",
                        "url": "https://gitlab.example.com/group/award-os.git",
                        "source_tier": "verified_award",
                        "award_level": "first",
                        "award_source_url": "winners.md",
                    }
                ],
            )

            result = ManifestAuditor().audit(manifest, samples)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, 0)
        self.assertEqual(result.warnings, 0)

    def test_manifest_audit_reports_manifest_errors_and_local_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            samples = root / "samples"
            samples.mkdir()
            repo = samples / "missing-head"
            repo.mkdir()
            manifest = self._write_manifest(
                root,
                [
                    {"repo_id": "../escape", "url": "https://example.com/escape.git"},
                    {
                        "repo_id": "award-no-source",
                        "url": "https://example.com/award.git",
                        "source_tier": "verified_award",
                    },
                    {"repo_id": "not-fetched", "url": "https://example.com/not-fetched.git"},
                    {"repo_id": "missing-head", "url": "https://example.com/missing-head.git"},
                ],
            )

            result = ManifestAuditor().audit(manifest, samples)
            codes = {issue.code for issue in result.issues}

        self.assertFalse(result.ok)
        self.assertIn("repo_id_unsafe", codes)
        self.assertIn("award_level_missing", codes)
        self.assertIn("award_source_missing", codes)
        self.assertIn("sample_dir_missing", codes)
        self.assertIn("head_missing", codes)

    def test_manifest_audit_cli_returns_zero_for_warnings_unless_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            samples = root / "samples"
            samples.mkdir()
            manifest = self._write_manifest(
                root,
                [{"repo_id": "not-fetched", "url": "https://example.com/not-fetched.git"}],
            )

            with patch("builtins.print"):
                code = cli.cmd_manifest_audit(
                    argparse.Namespace(
                        manifest=str(manifest),
                        samples=str(samples),
                        json=False,
                        strict=False,
                    )
                )
                strict_code = cli.cmd_manifest_audit(
                    argparse.Namespace(
                        manifest=str(manifest),
                        samples=str(samples),
                        json=False,
                        strict=True,
                    )
                )

        self.assertEqual(code, 0)
        self.assertEqual(strict_code, 1)


if __name__ == "__main__":
    unittest.main()
