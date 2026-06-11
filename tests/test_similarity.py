import unittest

from os_agent.models import Evidence, Finding, KernelProfile, RepoMeta, SymbolDef
from os_agent.agent import CompareAgent
from os_agent.similarity import CodeSimilarityDetector


class CodeSimilarityDetectorTest(unittest.TestCase):
    def test_detects_token_and_structure_similarity(self):
        left = Evidence(
            "kernel/vm.c",
            1,
            6,
            "int mappages(pde_t *pgdir, void *va, uint size) {\n"
            "  pte_t *pte = walkpgdir(pgdir, va, 1);\n"
            "  if(pte == 0) return -1;\n"
            "  *pte = PTE_P;\n"
            "  return 0;\n"
            "}\n",
        )
        right = Evidence(
            "hist/vm.c",
            10,
            15,
            "int map_pages(pde_t *root, void *addr, uint len) {\n"
            "  pte_t *pte = walkpgdir(root, addr, 1);\n"
            "  if(pte == 0) return -1;\n"
            "  *pte = PTE_P;\n"
            "  return 0;\n"
            "}\n",
        )

        matches = CodeSimilarityDetector(threshold=0.5).compare_evidence([left], [right])

        self.assertEqual(len(matches), 1)
        self.assertGreaterEqual(matches[0].score, 0.5)
        self.assertIn("pte", matches[0].shared_tokens)

    def test_ignores_comment_only_similarity(self):
        left = Evidence("a.c", 1, 2, "/* scheduler task switch */\n// syscall memory fs\n")
        right = Evidence("b.c", 1, 2, "/* scheduler task switch */\n// syscall memory fs\n")

        matches = CodeSimilarityDetector(threshold=0.5).compare_evidence([left], [right])

        self.assertEqual(matches, [])

    def test_ignores_include_only_similarity(self):
        left = Evidence("proc.c", 1, 4, '#include "proc.h"\n#include "spinlock.h"\n')
        right = Evidence("kernel/proc.c", 1, 4, '#include "proc.h"\n#include "spinlock.h"\n')

        matches = CodeSimilarityDetector(threshold=0.5).compare_evidence([left], [right])

        self.assertEqual(matches, [])

    def test_ignores_weak_structural_similarity_with_too_few_shared_tokens(self):
        left = Evidence("ide.c", 1, 4, "void ideintr(void) {\n  struct buf *b;\n}\n")
        right = Evidence("driver.h", 1, 4, "typedef void (* irq_handler_t)(void);\ntypedef enum { READY } state_t;\n")

        matches = CodeSimilarityDetector(threshold=0.5).compare_evidence([left], [right])

        self.assertEqual(matches, [])


class CompareAgentCodeSimilarityTest(unittest.TestCase):
    def test_compare_adds_code_similarity_points_for_shared_dimension(self):
        new_profile = KernelProfile(
            meta=RepoMeta(repo_id="new", name="new"),
            dimensions={
                "memory": [
                    Finding(
                        "new memory",
                        confidence="high",
                        evidence=[
                            Evidence(
                                "kernel/vm.c",
                                1,
                                5,
                                "pte_t *pte = walkpgdir(pgdir, va, 1);\n"
                                "if(pte == 0) return -1;\n"
                                "*pte = PTE_P;\n",
                            )
                        ],
                    )
                ]
            },
        )
        history_profile = KernelProfile(
            meta=RepoMeta(repo_id="hist", name="hist"),
            dimensions={
                "memory": [
                    Finding(
                        "hist memory",
                        confidence="high",
                        evidence=[
                            Evidence(
                                "hist/vm.c",
                                10,
                                14,
                                "pte_t *pte = walkpgdir(root, addr, 1);\n"
                                "if(pte == 0) return -1;\n"
                                "*pte = PTE_P;\n",
                            )
                        ],
                    )
                ]
            },
        )

        result = CompareAgent(CodeSimilarityDetector(threshold=0.45)).compare(new_profile, [history_profile])

        self.assertTrue(result.code_similarity_points)
        snippet_points = [
            point for point in result.code_similarity_points if "片段级代码相似度" in point.statement
        ]
        self.assertTrue(snippet_points)
        self.assertEqual(len(snippet_points[0].evidence), 2)

    def test_compare_adds_path_function_type_and_macro_overlap_points(self):
        new_profile = KernelProfile(
            meta=RepoMeta(repo_id="new", name="new"),
            dimensions={
                "syscall": [
                    Finding(
                        "new syscall",
                        confidence="high",
                        evidence=[
                            Evidence(
                                "kernel/syscall.c",
                                1,
                                3,
                                "int sys_fork(void) { return 0; }\n"
                                "struct syscall_frame { int num; };\n"
                                "#define SYS_fork 1\n",
                            )
                        ],
                    )
                ]
            },
            symbols=[
                SymbolDef("sys_fork", "fn", "kernel/syscall.c", 1, 1, "int sys_fork(void) { return 0; }"),
                SymbolDef("syscall_frame", "struct", "kernel/syscall.c", 2, 2, "struct syscall_frame { int num; };"),
                SymbolDef("SYS_fork", "macro", "kernel/syscall.c", 3, 3, "#define SYS_fork 1"),
            ],
        )
        history_profile = KernelProfile(
            meta=RepoMeta(repo_id="hist", name="hist"),
            dimensions={
                "syscall": [
                    Finding(
                        "hist syscall",
                        confidence="high",
                        evidence=[
                            Evidence(
                                "kernel/syscall.c",
                                10,
                                12,
                                "int sys_fork(void) { return 1; }\n"
                                "struct syscall_frame { int nr; };\n"
                                "#define SYS_fork 1\n",
                            )
                        ],
                    )
                ]
            },
            symbols=[
                SymbolDef("sys_fork", "fn", "kernel/syscall.c", 10, 10, "int sys_fork(void) { return 1; }"),
                SymbolDef("syscall_frame", "struct", "kernel/syscall.c", 11, 11, "struct syscall_frame { int nr; };"),
                SymbolDef("SYS_fork", "macro", "kernel/syscall.c", 12, 12, "#define SYS_fork 1"),
            ],
        )

        result = CompareAgent(CodeSimilarityDetector(threshold=0.95)).compare(new_profile, [history_profile])

        statements = "\n".join(finding.statement for finding in result.code_similarity_points)
        self.assertIn("文件路径重合", statements)
        self.assertIn("函数/符号名重合", statements)
        self.assertIn("结构体/类型重合", statements)
        self.assertIn("宏名重合", statements)


if __name__ == "__main__":
    unittest.main()
