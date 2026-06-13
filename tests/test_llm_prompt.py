import json
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

from os_agent.llm import LLMClient, LLMReportGenerator, LLMSettings
from os_agent.models import CompareResult, Finding


class FakeLLMResponse:
    def __init__(self, body: str):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.body.encode("utf-8")


class LLMClientDryRunTest(unittest.TestCase):
    def test_dry_run_writes_prompt_even_when_response_cache_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            client = LLMClient(
                LLMSettings(
                    api_key="",
                    cache_dir=root / "cache",
                )
            )
            system = "system boundary"
            prompt = "user evidence payload"
            cache_path = client.settings.cache_dir / f"{client._cache_key(system, prompt)}.json"
            cache_path.write_text(
                json.dumps({"content": "cached response", "model": client.settings.model}),
                encoding="utf-8",
            )

            dry_run_path = root / "prompts" / "case.prompt.md"
            result = client.chat(prompt, system=system, dry_run_path=dry_run_path)

            self.assertIn("LLM dry-run prompt written", result)
            self.assertNotEqual(result, "cached response")
            self.assertTrue(dry_run_path.exists())
            prompt_text = dry_run_path.read_text(encoding="utf-8")
            self.assertIn("# System", prompt_text)
            self.assertIn(system, prompt_text)
            self.assertIn("# User", prompt_text)
            self.assertIn(prompt, prompt_text)


class LLMClientFallbackTest(unittest.TestCase):
    def _client(self, root: Path) -> LLMClient:
        return LLMClient(LLMSettings(api_key="test-key", cache_dir=root / "cache"))

    def test_url_error_is_wrapped_as_runtime_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = self._client(Path(tmp))
            with patch(
                "os_agent.llm.urllib.request.urlopen",
                side_effect=urllib.error.URLError("bad gateway"),
            ):
                with self.assertRaisesRegex(RuntimeError, "LLM API request failed"):
                    client.chat("prompt", system="system")

    def test_invalid_json_is_wrapped_as_runtime_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = self._client(Path(tmp))
            with patch(
                "os_agent.llm.urllib.request.urlopen",
                return_value=FakeLLMResponse("not json"),
            ):
                with self.assertRaisesRegex(RuntimeError, "invalid JSON"):
                    client.chat("prompt", system="system")

    def test_missing_content_is_wrapped_as_runtime_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = self._client(Path(tmp))
            with patch(
                "os_agent.llm.urllib.request.urlopen",
                return_value=FakeLLMResponse(json.dumps({"choices": [{}]})),
            ):
                with self.assertRaisesRegex(RuntimeError, "missing choices"):
                    client.chat("prompt", system="system")


class LLMComparePromptTest(unittest.TestCase):
    def test_compare_prompt_includes_selection_overlap_self_check_and_uncertain_unique_rule(self):
        result = CompareResult(
            new_repo="new-os",
            history_repos=["hist-os"],
            selection_notes=["hist-os：score=1.00；OS 维度重合度 1.00"],
            overlap_points=[Finding("与 hist-os 在系统调用维度存在功能重合。", confidence="medium")],
            code_similarity_points=[Finding("与 hist-os 在系统调用维度发现片段级代码相似度 0.82。", confidence="high")],
            similarities=[Finding("与 hist-os 在系统调用维度均有可确认实现。", confidence="medium")],
        )

        prompt = LLMReportGenerator.__new__(LLMReportGenerator)._compare_prompt(result)

        self.assertIn("selection_notes", prompt)
        self.assertIn("overlap_points", prompt)
        self.assertIn("code_similarity_points", prompt)
        self.assertIn("代码级相似线索检测", prompt)
        self.assertIn("代码级可复核线索", prompt)
        self.assertIn("不能直接判定代码抄袭", prompt)
        self.assertIn("self_check", prompt)
        self.assertIn("`path:Lx-Ly`", prompt)
        self.assertIn("不能写成 `path:10-14`", prompt)
        self.assertIn("当前证据不足，未自动确认创新点", prompt)
        self.assertIn("不能强行总结创新点", prompt)
        self.assertIn("不得把未标注为 verified_award 的历史样本称为特奖、一等奖或优秀获奖案例", prompt)

    def test_normalizes_shorthand_evidence_references(self):
        generator = LLMReportGenerator.__new__(LLMReportGenerator)

        report = (
            "证据来自 `kernel/syscall.c:10-14`，"
            "中文路径来自 `LAB4 内存管理/trap.c:9-13`，"
            "已规范引用保持 `kernel/proc.c:L4-L8`。"
        )

        normalized = generator._normalize_evidence_refs(report)

        self.assertIn("`kernel/syscall.c:L10-L14`", normalized)
        self.assertIn("`LAB4 内存管理/trap.c:L9-L13`", normalized)
        self.assertIn("`kernel/proc.c:L4-L8`", normalized)


if __name__ == "__main__":
    unittest.main()
