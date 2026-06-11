"""Minimal LLM client with dry-run and cache support.

The client uses the OpenAI-compatible chat completions API exposed by DeepSeek.
It intentionally depends only on the Python standard library for the MVP.
"""

from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .analyzer import DIMENSIONS
from .models import CompareResult, KernelProfile, to_dict
from .selfcheck import EvidenceChecker


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CACHE_DIR = PROJECT_ROOT / "data" / "llm_cache"


@dataclass
class LLMSettings:
    provider: str = "deepseek"
    base_url: str = "https://api.deepseek.com/v1"
    model: str = "deepseek-chat"
    api_key: str = ""
    timeout: int = 120
    max_tokens: int = 4096
    temperature: float = 0.2
    cache_dir: Path = DEFAULT_CACHE_DIR


def load_dotenv(path: Path = PROJECT_ROOT / ".env") -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_settings() -> LLMSettings:
    load_dotenv()
    return LLMSettings(
        provider=os.getenv("LLM_PROVIDER", "deepseek"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1").rstrip("/"),
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        api_key=os.getenv("LLM_API_KEY", ""),
        timeout=int(os.getenv("LLM_TIMEOUT", "120")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "4096")),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
    )


class LLMClient:
    def __init__(self, settings: LLMSettings | None = None):
        self.settings = settings or load_settings()
        self.settings.cache_dir.mkdir(parents=True, exist_ok=True)

    def chat(self, prompt: str, *, system: str, dry_run_path: Path | None = None, use_cache: bool = True) -> str:
        cache_key = self._cache_key(system, prompt)
        cache_path = self.settings.cache_dir / f"{cache_key}.json"
        if use_cache and cache_path.exists():
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            return data["content"]

        if dry_run_path:
            dry_run_path.parent.mkdir(parents=True, exist_ok=True)
            dry_run_path.write_text(self._format_prompt(system, prompt), encoding="utf-8")
            return f"LLM dry-run prompt written to {dry_run_path}"

        if not self.settings.api_key or self.settings.api_key == "replace_with_your_new_api_key":
            raise RuntimeError("LLM_API_KEY is not configured. Copy .env.example to .env and set a new API key.")

        payload = {
            "model": self.settings.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
        }
        request = urllib.request.Request(
            f"{self.settings.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.settings.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM API HTTP {exc.code}: {detail}") from exc

        content = data["choices"][0]["message"]["content"]
        cache_path.write_text(
            json.dumps({"content": content, "model": self.settings.model}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return content

    def _cache_key(self, system: str, prompt: str) -> str:
        raw = json.dumps(
            {
                "provider": self.settings.provider,
                "model": self.settings.model,
                "temperature": self.settings.temperature,
                "system": system,
                "prompt": prompt,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _format_prompt(self, system: str, prompt: str) -> str:
        return f"# System\n\n{system}\n\n# User\n\n{prompt}\n"


class LLMReportGenerator:
    SYSTEM = (
        "你是一个谨慎的操作系统代码分析助手。你必须严格基于提供的 KernelProfile 和证据回答。"
        "不要编造文件名、函数名、行号、算法名称或实现细节；无法确认的信息必须标注“未确认”。"
        "所有关键结论必须使用输入 evidence 中已有的 file 和行号，引用格式使用 `path:Lx-Ly`。"
        "输出 Markdown，面向评审专家阅读，语言清晰、克制，不要使用寒暄开头。"
    )

    def __init__(self, client: LLMClient | None = None):
        self.client = client or LLMClient()

    def render_profile(self, profile: KernelProfile, *, dry_run_path: Path | None = None) -> str:
        prompt = self._profile_prompt(profile)
        return self.client.chat(prompt, system=self.SYSTEM, dry_run_path=dry_run_path)

    def render_compare(self, result: CompareResult, *, dry_run_path: Path | None = None) -> str:
        prompt = self._compare_prompt(result)
        return self.client.chat(prompt, system=self.SYSTEM, dry_run_path=dry_run_path)

    def _profile_prompt(self, profile: KernelProfile) -> str:
        compact: dict[str, Any] = {
            "meta": to_dict(profile.meta),
            "overview": profile.overview,
            "build_system": to_dict(profile.build_system),
            "dimensions": {},
            "self_check": EvidenceChecker().profile_summary(profile),
        }
        for dim, findings in profile.dimensions.items():
            compact["dimensions"][dim] = {
                "title": DIMENSIONS.get(dim, {}).get("title", dim),
                "findings": [to_dict(finding) for finding in findings[:3]],
            }
        return (
            "请基于下面的 KernelProfile 生成一份项目描述报告。\n"
            "要求：\n"
            "1. 必须按操作系统维度组织，包括调度、内存、系统调用、文件系统、同步、中断、驱动。\n"
            "2. 每个关键判断都要引用已有 evidence 的 file 和行号，不能引用 JSON 中不存在的文件或行号。\n"
            "3. 不要引入 profile 之外的信息。\n"
            "4. 不要根据文件名或常识扩写具体算法；如果 evidence 没有说明算法，只能写“未确认”。\n"
            "5. 只有 source_tier 为 verified_award 且带 award_source_url 的样本，才能称为获奖案例；其他样本只能称为教学基线、架构参考或比赛作品样本。\n"
            "6. 最后给出“核验摘要”，说明 self_check 统计值和仍未确认的信息。\n\n"
            f"KernelProfile JSON:\n```json\n{json.dumps(compact, ensure_ascii=False, indent=2)}\n```"
        )

    def _compare_prompt(self, result: CompareResult) -> str:
        compact = {
            "new_repo": result.new_repo,
            "history_repos": result.history_repos,
            "selection_notes": result.selection_notes,
            "overlap_points": [to_dict(item) for item in result.overlap_points],
            "code_similarity_points": [to_dict(item) for item in result.code_similarity_points],
            "similarities": [to_dict(item) for item in result.similarities],
            "differences": [to_dict(item) for item in result.differences],
            "unique_points": [to_dict(item) for item in result.unique_points],
            "self_check": EvidenceChecker().compare_summary(result),
        }
        return (
            "请基于下面的规则比较结果生成一份人类友好的项目比较报告。\n"
            "要求：\n"
            "1. 分为比较对象选择、功能重合与疑似重复证据、代码级相似线索检测、相似点、差异点、可能创新点、待人工复核项、核验摘要。\n"
            "2. 所有关键判断都必须保留 evidence 中已有的 file 和行号，不能引用 JSON 中不存在的文件或行号。\n"
            "3. overlap_points 只能表述为功能维度和实现线索重合，不能直接判定代码抄袭；必须说明需要人工复核。\n"
            "4. code_similarity_points 可能包含文件路径、函数/符号名、结构体/宏名和片段 token/结构相似度线索，只能表述为代码级可复核线索，不能直接裁定抄袭。\n"
            "5. 不要引入输入 JSON 之外的信息。\n"
            "6. 必须保留 selection_notes 中的历史样本选择依据。\n"
            "7. 如果 unique_points 为空或只有“未确认”，必须明确写“当前证据不足，未自动确认创新点”，不能强行总结创新点。\n"
            "8. 不得把未标注为 verified_award 的历史样本称为特奖、一等奖或优秀获奖案例；未核验比赛样本只能称为比赛作品样本。\n"
            "9. 核验摘要必须引用 self_check 的统计值，并说明证据率只统计关键设计判断。\n\n"
            f"CompareResult JSON:\n```json\n{json.dumps(compact, ensure_ascii=False, indent=2)}\n```"
        )
