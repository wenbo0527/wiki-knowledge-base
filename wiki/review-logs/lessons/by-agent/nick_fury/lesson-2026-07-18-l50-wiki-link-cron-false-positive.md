---
title: Lesson 2026 07 18 L50 wiki link cron false positive
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, 2026-07, L-50, cron-bug]
date: 2026-07-18
---

# L-50: wiki-link 路径规范 + cron 算法升级族（5 条铁律）

> **触发**: 2026-07-18 09:14 CST（P0.5 修 5 个 wiki-link + 发现 cron 严重 bug）
> **关联**: INC-2026-07-18-001（cron bug）+ INC-2026-07-18-002（5 路径修复）
> **治理**: nick_fury 认领

---

## L-50 族系（5 条铁律 · 7-18 闭环）

### L-50.1 · wiki-link 路径修复必先 verify 真实位置

```bash
# 修任何 wiki-link 前必 find 真实位置
find /Users/wenbo/Documents/project/Wiki/wiki -name "*${partial_name}*"
```

**教训**：本次 5 个 wiki-link 中 4 个是"路径错位"（缺前缀/缺子目录），1 个是真不存在。修前不 verify 会修错。

### L-50.2 · cron 算法误报率 > 50% 必须升级（不能信报告数字）

**本次实证**：
- `wiki_auto_review.py` 报告"真实死链 20 个"
- 验证 10/10 真存在 = 100% 误报率
- 修了 5 个后报告数字不变 = 算法根本没解析路径

**触发条件**：
- 跑 cron 后"修死链但报告数字不变"
- 报告里同一文件反复出现同一死链
- 死链路径看起来"应该存在但报死链"

**修法**：升级 `deadlink_check()` 函数——递归解析 + 路径补全 + 白名单。

### L-50.3 · "修死链后跑 cron 数字不变" = 算法 bug 信号

```
修 5 个 → 数字不变 → 不是"没修对"，是"算法错了"
```

**自检流程**：
1. 跑 cron 拿 baseline
2. 修死链
3. 再跑 cron 拿 after
4. 如果 after == baseline → **算法 bug**，不继续修

### L-50.4 · 真死链 = 路径错（缺前缀/子目录）+ 引用方修改

**两种真死链**：
- **路径错位**：文件被移过 / 重新归类，link 没更新
- **文件不存在**：vibe-coding.md 真的没有，需改写为相近文件

**修法**：
- 路径错位 → verify 真实位置 → 改 link
- 文件不存在 → 找语义相近的文件 → 改写 + 在 lesson 备注

### L-50.5 · sed 在 BSD 上对 `[[` 转义有 bug，换 Python re.sub

```python
# sed -i '' "s|\[\[xxx\]\]|...|g" 在 macOS 上会报 "bad flag in substitute command"
# 改用 Python re.sub

import re
content = re.sub(r'\[\[xxx\]\]', '[[yyy|显示]]', content)
```

**节省**：本次踩坑 → 立即换 Python，避免重复试错。

---

## L-50 关联族系

```
L-13   launchd vs OpenClaw cron 迁移          (7-14)
L-48   trash 副作用必查目录结构                (7-17)
L-49   cron edit 必看 argv 完整 JSON          (7-15)
L-49.5 argv 必查脚本路径存在性                 (7-17)
L-49.6 cron cleanup 决策树（4 类 + 4 动作）    (7-17)
L-49.7 INC 报告必加 enabled/disabled tag 区分 (7-17)
L-49.8 ID 引用必完整（grep 原文 + 长度校验）  (7-17)
L-50   wiki-link 路径规范 + cron 算法升级族    (7-18) ← 本次
```

**族系本质**：从"配置写对"→"路径存在"→"清理决策"→"报告精度"→"标识精度"→"链接精度"——逐层把 cron 运维从粗放到精确。

---

## L-50 应用场景（什么时候用）

| 场景 | 触发词 | 用哪条 |
|:---|:---|:---|
| 修 wiki-link 前 | "修死链"/"补路径" | L-50.1 先 verify |
| cron 报死链但没修 | "为什么报告不变" | L-50.2/3 算法 bug 检查 |
| 文件不存在要改写 | "找不到 vibe-coding.md" | L-50.4 找语义相近 |
| sed 转义失败 | "bad flag in substitute" | L-50.5 换 Python |

---

*🕵️ 尼克·弗瑞 · 2026-07-18 09:14 CST · L-50 闭环*