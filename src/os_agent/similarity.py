"""Lightweight code snippet similarity utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .models import Evidence


TOKEN_RE = re.compile(
    r"[A-Za-z_][A-Za-z0-9_]*|0x[0-9A-Fa-f]+|\d+|==|!=|<=|>=|->|::|&&|\|\||[{}()\[\];,.*+\-/&|<>:=]"
)
STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
LINE_COMMENT_RE = re.compile(r"//.*")
PREPROCESSOR_RE = re.compile(r"^\s*#\s*(include|pragma|ifdef|ifndef|endif|define)\b.*$", re.MULTILINE)
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
NUMBER_RE = re.compile(r"^(?:0x[0-9A-Fa-f]+|\d+)$")
BEHAVIOR_TOKENS = {"if", "for", "while", "switch", "return", "=", "->", "{", "}", "case"}


@dataclass(frozen=True)
class CodeSimilarity:
    left: Evidence
    right: Evidence
    token_score: float
    structure_score: float
    score: float
    shared_tokens: list[str]

    @property
    def confidence(self) -> str:
        if self.score >= 0.78:
            return "high"
        if self.score >= 0.58:
            return "medium"
        return "low"


class CodeSimilarityDetector:
    """Compare evidence snippets with token and structure overlap.

    This is intentionally a lightweight detector. It reports review leads, not
    plagiarism conclusions.
    """

    def __init__(self, *, min_tokens: int = 8, threshold: float = 0.58, min_token_score: float = 0.5, min_shared_tokens: int = 3):
        self.min_tokens = min_tokens
        self.threshold = threshold
        self.min_token_score = min_token_score
        self.min_shared_tokens = min_shared_tokens

    def compare_evidence(self, left_items: list[Evidence], right_items: list[Evidence], limit: int = 3) -> list[CodeSimilarity]:
        matches: list[CodeSimilarity] = []
        for left in left_items:
            left_tokens = self._tokens(left.snippet)
            if len(left_tokens) < self.min_tokens or not self._has_behavior(left_tokens):
                continue
            left_shape = self._shape_tokens(left_tokens)
            for right in right_items:
                right_tokens = self._tokens(right.snippet)
                if len(right_tokens) < self.min_tokens or not self._has_behavior(right_tokens):
                    continue
                right_shape = self._shape_tokens(right_tokens)
                token_score = self._jaccard(set(left_tokens), set(right_tokens))
                structure_score = self._jaccard(set(left_shape), set(right_shape))
                shared = sorted(
                    token
                    for token in (set(left_tokens) & set(right_tokens))
                    if IDENTIFIER_RE.match(token) and token not in {"id", "num", "str"}
                )[:12]
                score = round((token_score * 0.65 + structure_score * 0.35), 3)
                if score < self.threshold or token_score < self.min_token_score or len(shared) < self.min_shared_tokens:
                    continue
                matches.append(
                    CodeSimilarity(
                        left=left,
                        right=right,
                        token_score=round(token_score, 3),
                        structure_score=round(structure_score, 3),
                        score=score,
                        shared_tokens=shared,
                    )
                )
        matches.sort(key=lambda item: (-item.score, item.left.file, item.right.file))
        return matches[:limit]

    def _tokens(self, snippet: str) -> list[str]:
        text = self._strip_comments_and_strings(snippet)
        return [token.lower() for token in TOKEN_RE.findall(text)]

    def _shape_tokens(self, tokens: list[str]) -> list[str]:
        shaped: list[str] = []
        for token in tokens:
            if NUMBER_RE.match(token):
                shaped.append("num")
            elif IDENTIFIER_RE.match(token):
                shaped.append("id")
            else:
                shaped.append(token)
        return shaped

    def _strip_comments_and_strings(self, snippet: str) -> str:
        text = PREPROCESSOR_RE.sub(" ", snippet)
        text = BLOCK_COMMENT_RE.sub(" ", text)
        text = LINE_COMMENT_RE.sub(" ", text)
        text = STRING_RE.sub(" STR ", text)
        return text

    def _has_behavior(self, tokens: list[str]) -> bool:
        return any(token in BEHAVIOR_TOKENS for token in tokens)

    def _jaccard(self, left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0.0
        return len(left & right) / len(left | right)
