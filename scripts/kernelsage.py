"""Convenience wrapper for running KernelSage from the repository root."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from os_agent.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())

