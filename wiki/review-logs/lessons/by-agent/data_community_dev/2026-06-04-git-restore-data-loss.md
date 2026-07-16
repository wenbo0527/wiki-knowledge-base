---
title: 2026 06 04 git restore data loss
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-06-30
---

# 5/26 教训 #7 — git restore 误丢已加固数据

**作者**: data_community_dev  
**日期**: 2026-06-04 15:11 事故 + 15:18 恢复  
**任务卡**: TASK-20260604-A62D5B42 (P0-管理-#1 修 StatusTag) 实施中  
**事故文件**: `apps/mkt-app/src/mock/coupon.ts`

---

## 事故还原

15:11 在 P0-管理-#4 (补 mock 6 字段) 实施中，使用 Python 脚本批量给 16 条 couponMockData 补 8 字段（startTime/endTime + 6 库存字段）。脚本 join 逻辑出 bug：最后一项也加了 `},` 闭合，导致 mock/coupon.ts:797 多了一对 `},`，build 失败。

**修法失误**：用 `git restore src/mock/coupon.ts` 想让文件回到最近 commit 状态。

**结果**：整个 `src/mock/coupon.ts` 回到 6/2 HEAD（d200a61 commit），**所有 6/4 10:30 之后的改动全部丢失**：
- MockPackage.status 收紧到 3 态 (`active|paused|expired` → `draft|active|inactive`)
- MockPackage.inventory_batches? 字段声明
- 8 条 packageMockData 的 inventory_batches 数据 (B001-B011, 11 个批次)
- 11 条 couponMockData（6/3 后加的）只剩 2 条 6/2 baseline
- 16 条 couponMockData 现状 → 16 条是从实施记录重建（**高风险**）

**没丢**：types/api/coupon.ts 的 `InventoryBatch` interface（之前 git diff 仍 M）

## 恢复路径（4 分钟）

依赖 3 份文档完整重建 24 条数据：
1. `tmp/code-20260604-demo001-types-mock.md` (D1 实施记录 4059 B)
2. `tmp/deploy-20260604-0e45cb27.md` (部署-003 报告)
3. 派蒙走读报告（sessions_send 历史）

**SOP 救场实证**：没这 3 份文档 4 分钟恢复不可能。**实施记录 + 部署报告 + sessions_send 历史的价值 = 不可估量**。

## 根因

1. **git restore 误用**：restore 默认回退到 HEAD (6/2)，不是"撤销最近改动"
2. **Python 脚本脆弱**：批量 join 末尾项时没去重
3. **没有 baseline 快照**：改动前没 `cp mock/coupon.ts mock/coupon.ts.bak`
4. **没有部署前自检**：改 mock 文件后没跑 `wc -l` 对比 baseline

## 防御措施（SOP 升级）

### 派单 message 必加（4 条）
1. 改 mock 数据文件前，**必跑** `cp <file> <file>.bak.$(date +%H%M)` 或 `git stash push`
2. 改 mock 数据后，**必跑** `wc -l <file>` 记 baseline 写到 commit message
3. 部署前再跑 `wc -l` 对比，**数字必须 ≥ baseline**
4. 任何"批量处理 mock 数据"用 Python 脚本，**先 dry-run 输出前 5 行确认**再 `git mv` 备份

### dev 必须做的 (针对 mock/coupon.ts 这类大文件)
- 改前: `cp src/mock/coupon.ts src/mock/coupon.ts.bak.$(date +%H%M)` (强制)
- 改后: `wc -l src/mock/coupon.ts` 写到 commit message
- 部署前: `wc -l dist/assets/coupon-*.js` 对比 (dist 文件应该比 src 略小或略大, 但不能 0)
- 重大修改 (>10 行): 必 `git commit` 一次 (即使后续 uncommit 也比没记录强)

### 替代方案 (不要用 `git restore` 修错)
- **首选**: `git diff src/mock/coupon.ts` 看具体改动 + 手动 `edit` 修脚本破坏处
- **次选**: `git checkout -- src/mock/coupon.ts` (跟 `git restore` 一样会丢 uncommitted)
- **真正稳**: `cp src/mock/coupon.ts.bak.HHMM src/mock/coupon.ts` (回退到改动前, 不是 HEAD)
- **绝不**: `git reset --hard HEAD` (会丢 uncommitted + staged)

## 教训 #5 vs 教训 #7

| 次 | 教训 | 6/4 触发 | 严重度 | 差异 |
|:---:|:---|:---|:---:|:---|
| 3 | git restore + untracked 路由 | 6/4 12:08 | 🟡 | 仅丢 untracked 路由, 损失小 |
| **7** | **git restore 误丢已加固数据** | **本次 15:11** | 🔴 | **整个文件回退 6/2, 损失大** |

变体 7 跟变体 3 同源（都是 git restore），但**更严重** —— 直接吃掉上次部署成果。

## QA 复检结论（4 个验收项）

| # | 验收项 | 结果 |
|:---:|:---|:---:|
| A | mock 数据完整性: 8 packageMockData + 16 couponMockData | ✅ |
| B | B001-B011 11 个 inventory_batches 完整恢复 | ✅ |
| C | types/api/coupon.ts InventoryBatch + CouponPackage.inventory_batches 字段 | ✅ |
| D | 本 SOP 文档 | ✅ |

恢复后立即部署-007 验证生产可用（mkt/ mtime 15:20, 入口 hash BJC8l_dA）。

## 参考

- 派蒙 lessons 文档: `memory/lessons/2026-06-04-git-restore-7xx-data-loss.md`
- 部署-007 报告: `tmp/deploy-20260604-management-4bugs.md`
- 5/26 教训系列: `memory/lessons/2026-06-03-team2-review.md` 及后续 6/4 多次复发
