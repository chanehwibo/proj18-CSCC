import unittest

from os_agent.models import Finding, KernelProfile, RepoMeta
from os_agent.selector import HistorySelector


def profile(repo_id: str, *, style: str, arch: list[str], languages: dict[str, int], dims: list[str]) -> KernelProfile:
    return KernelProfile(
        meta=RepoMeta(
            repo_id=repo_id,
            name=repo_id,
            style=style,
            arch=arch,
            languages=languages,
            loc_total=sum(languages.values()),
        ),
        dimensions={dim: [Finding(f"{dim} confirmed", confidence="high")] for dim in dims},
    )


class HistorySelectorTest(unittest.TestCase):
    def test_selects_by_profile_similarity_not_input_order(self):
        target = profile(
            "target",
            style="rcore-variant",
            arch=["riscv64"],
            languages={"rust": 1000},
            dims=["scheduler", "memory", "syscall"],
        )
        weak_first = profile(
            "weak-first",
            style="unknown",
            arch=["x86_64"],
            languages={"c": 1000},
            dims=["driver"],
        )
        strong_second = profile(
            "strong-second",
            style="rcore-variant",
            arch=["riscv64"],
            languages={"rust": 900, "asm": 100},
            dims=["scheduler", "memory", "syscall"],
        )

        selected = HistorySelector().select(target, [weak_first, strong_second], limit=1)

        self.assertEqual(selected[0].profile.meta.repo_id, "strong-second")
        self.assertGreater(selected[0].score, 0)


if __name__ == "__main__":
    unittest.main()
