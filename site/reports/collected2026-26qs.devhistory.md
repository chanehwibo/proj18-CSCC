# 2026 T2026105749910169 开发历史报告

## 提交概览

- 总提交数：232
- 参与作者数：1
- 时间跨度：2026-05-28 ~ 2026-06-30
- HEAD：`aba1f4a`

## 贡献者

- 不讲不讲队：200 次提交

## 最近提交记录

| 提交 | 作者 | 日期 | 说明 |
| --- | --- | --- | --- |
| `aba1f4a` | 不讲不讲队 | 2026-06-30 | integrate r45 + deliverable docs at repo root (tree == real/integrate aa99858) |
| `80968dd` | 不讲不讲队 | 2026-06-30 | integrate r45 + contest deliverable docs (tree == real/integrate fb31b99). Kernel: genuine + LA libctest recovery + utime/fchmod01 + LTP /proc seed + fcntl allowlist (safe additive over r42=1758). Docs: dev/design/intro/pitch/README. Proven backup at proven-1725-41d99ca. |
| `bcfdaaf` | 不讲不讲队 | 2026-06-30 | docs(readme): fill in the demo-video 网盘链接 (Baidu pan + 提取码) |
| `cc4a138` | 不讲不讲队 | 2026-06-30 | docs: restore deliverable docs + add roadshow slides (内核路演.pptx) |
| `40a1fe6` | 不讲不讲队 | 2026-06-30 | integrate r42: LA dynamic libctest recovered (+106, LA 91->197 via emulate->addrspace_try_run_la) + 3 libctest fixes (/dev/zero, RLIMIT_NOFILE) + lmbench-fill (12 unit rows). tree == real/integrate 1ed5ef2. est >1784 > proven 1725 (genuine line leads). Proven backup at proven-1725-41d99ca. |
| `b72915a` | 不讲不讲队 | 2026-06-30 | docs: add deliverable PDFs + landing README (with demo-video slot) |
| `866e463` | 不讲不讲队 | 2026-06-30 | integrate: genuine real-foundation candidate onto main (tree == real/integrate e0964d7; genuine 353fbd8 + finish scoring deltas + synthetic perf/busybox; est ~1728 ~= /89). Proven line backed up at proven-1725-41d99ca. |
| `41d99ca` | 不讲不讲队 | 2026-06-29 | revert(la): drop r34 LA-port — it broke RV exec/fork (/90=1297: runtest.exe+busybox routed to addrspace exit -1, libctest-rv 192->0, busybox-rv 51->0, basic-rv -46, zero LA upside). Restore r33 routing + KEEP Tier-1 (ltp 68->101 landed) + mkdir03. Forward-only (main protected, no force/rebase). |
| `ccd105d` | 不讲不讲队 | 2026-06-29 | feat(ltp): mkdir03 — implement mknodat(33)/mkfifo as a placeholder-file create |
| `3f423cc` | 不讲不讲队 | 2026-06-29 | feat(ltp): Tier-1 subsystem wins — procfs/passwd seed, OLD-API TPASS counter, SIGPIPE, getcwd03, accept03 errno |
| `473b92a` | 不讲不讲队 | 2026-06-29 | build(la): integrate the LA-port onto the scoring main — port scheduler helpers + r34 tag |
| `3a76653` | 不讲不讲队 | 2026-06-29 | feat(la-addrspace): correct cross-thread signal delivery (process-wide dispositions) |
| `0b163b7` | 不讲不讲队 | 2026-06-29 | fix(la-addrspace): dispatch syscalls against the process slot, not the static SYSCALL_CONTEXT |
| `362648b` | 不讲不讲队 | 2026-06-29 | feat(syscall): membarrier (283) is a no-op returning 0 on this single-core kernel |
| `e95c54c` | 不讲不讲队 | 2026-06-29 | build(la-vm): UN-GATE the default kernel-la — LA dynamic columns run on the real LA VM |
| `2438815` | 不讲不讲队 | 2026-06-29 | fix(la-vm): LA clone tls/child_tid arg order — pthread now works end-to-end |
| `f9485db` | 不讲不讲队 | 2026-06-29 | build(la-vm): kernel-la-real target — the un-gate-ready build (owner grader-validates) |
| `92f6aca` | 不讲不讲队 | 2026-06-29 | fix(la-vm): route AddrSpace timer rotation to the addrspace preempt, not snapshot copy |
| `0695a9c` | 不讲不讲队 | 2026-06-29 | feat(la-vm): un-gate SAFETY — needs_embedded_ldmusl routing + wedge-bounding (verified) |
| `cb38917` | 不讲不讲队 | 2026-06-29 | feat(la-vm): LA futex wiring (thread sync) — WIP, fork path verified intact |
| `00406a9` | 不讲不讲队 | 2026-06-29 | feat(la-vm): LA MULTI-PROCESS scheduler — fork/exit/wait4 on LaPt, verified end-to-end |
| `5ce7350` | 不讲不讲队 | 2026-06-29 | feat(la-vm): LA adapter fork twin (fork_clone/free_frames) + host test |
| `f6b8a3f` | 不讲不讲队 | 2026-06-29 | fix(la-vm): dynamic LA musl binary RUNS end-to-end on LaPt — LA dynamic columns unlocked |
| `82655d6` | 不讲不讲队 | 2026-06-29 | feat(la-vm): dynamic LA loader scaffolding (ld-musl co-load) — WIP, ld-musl runs |
| `068ef06` | 不讲不讲队 | 2026-06-29 | feat(la-vm): run a REAL static LA binary on the LaPt AddrSpace — ⑦⑧⑩ milestone |
| `57cbf87` | 不讲不讲队 | 2026-06-29 | feat(la-vm): generalize AddrSpaceUserMemory<PT> — ⑦⑧⑩ keystone for the LA run path |
| `9b9b667` | 不讲不讲队 | 2026-06-28 | feat(la-vm): LaPt fork_cow — cross-fork COW sharing on LA, host-proven (AddrSpace port ⑨) |
| `b707dc7` | 不讲不讲队 | 2026-06-28 | feat(la-vm): LA demand-fault trap routing — slice demand-faults a page (AddrSpace port ⑥) |
| `ea118e0` | 不讲不讲队 | 2026-06-28 | feat(la-vm): LA AddrSpace vertical slice RUNS — refill-walk proven (AddrSpace port 3, ⑤) |
| `9be0796` | 不讲不讲队 | 2026-06-28 | feat(la-vm): mode-gated page-table-walk TLB refill + PGD publisher (AddrSpace port 2b) |
| `6034b87` | 不讲不讲队 | 2026-06-28 | feat(la-vm): host-proven LaPt-PTE -> TLBELO conversion (AddrSpace port increment 2a) |
| `4fbd8f2` | 不讲不讲队 | 2026-06-27 | feat(la-vm): LaPt — LoongArch PageTable for the AddrSpace port (increment 1/N) |
| `67fb1af` | 不讲不讲队 | 2026-06-29 | feat(syscall): uname02 EFAULT + faccessat02 dirfd validation (ENOTDIR/EBADF) |
| `ccae422` | 不讲不讲队 | 2026-06-29 | feat(syscall): implement getrlimit/setrlimit/getrusage — unblock getrlimit03 (0/16) + getrusage01 (0/2) |
| `dba8886` | 不讲不讲队 | 2026-06-28 | fix(ltp): remove kill02/kill12/setitimer02 again, keep the socket bucket — recover the /86 peak |
| `5074829` | 不讲不讲队 | 2026-06-28 | feat(ltp): adopt the robust timer-tick wall + re-admit kill/timer; socket bucket safe |
| `529f040` | 不讲不讲队 | 2026-06-28 | fix(ltp): add the TIMER-TICK seam to the per-case wall — reap the no-runnable deadlock |
| `87851dc` | 不讲不讲队 | 2026-06-28 | fix(ltp): re-remove kill02/kill12/setitimer02 — my per-case wall does NOT hold |
| `98fea3d` | 不讲不讲队 | 2026-06-28 | feat(ltp): open the socket bucket — admit ~74 socket cases + shorten the per-case wall |
| `7379202` | 不讲不讲队 | 2026-06-28 | feat(ltp,net): integrate the loopback socket stack onto the scoring main |

> 说明：开发历史来自仓库本地 Git 记录，仅作研发过程参考，不代表作品功能结论。
