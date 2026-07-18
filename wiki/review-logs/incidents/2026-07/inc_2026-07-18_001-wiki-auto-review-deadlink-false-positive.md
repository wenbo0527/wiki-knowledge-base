---
title: inc 2026 07 18 001 wiki auto review deadlink false positive
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07, cron-bug, wiki-auto-review]
date: 2026-07-18
---

# INC-2026-07-18-001: wiki_auto_review.py 死链检测全报 false positive · 10/10 误判

> **揭穿时间**: 2026-07-18 09:14 CST（P0.5 修复 5 个真实 wiki-link 路径后）
> **揭穿者**: 🕵️ 尼克·弗瑞
> **关联**: INC-2026-07-17-004（wiki-health-check 双跑）+ L-50（cron 算法升级族）
> **状态**: ✅ Closed（P0.5 闭环 · 待 P1.5 算法升级）

---

## 📋 现象

P0.5 任务"修 16 个真实死链"完成后，跑 `wiki_auto_review.py` 验证：

| 维度 | Before（7-18 03:31）| After P0.5（7-18 09:11）| 变化 |
|:---|:---:|:---:|:---:|
| 总死链 | 1087 | 1082 | -5（仅因占位符被替换）|
| **真实死链** | **16** | **20** | **+4** |
| 健康度 | 🟠 65/100 | 🟠 65/100 | 0 |

**异常**：修了 5 个真实死链路径，但"真实死链"反而 +4？

## 🔍 根因（verify 实证）

按报告列出的 10 个死链逐一 verify 文件系统：

| # | 报告死链路径 | 真实状态 |
|:---|:---|:---|
| 1 | `AGENT_COLLAB_GUIDE.md → topics/ai-agent` | ✅ **DIR + 11 .md + README.md** |
| 2 | `AGENT_COLLAB_GUIDE.md → insights/ai` | ✅ **DIR + 37 .md** |
| 3 | `AGENT_COLLAB_GUIDE.md → topics/product-management` | ✅ **DIR + 19 .md + README.md** |
| 4 | `AGENT_COLLAB_GUIDE.md → entities/companies/openai` | ✅ **FILE.md** |
| 5 | `AGENT_COLLAB_GUIDE.md → concepts/llm-agent` | ✅ **FILE.md** |
| 6 | `18year-ai-pioneer → insights/agent/insight-20260429-karpathy-ai-agent-revolution` | ✅ **FILE.md** |
| 7 | `18year-ai-pioneer → topics/ai-native/agent-engineering` | ✅ **FILE.md** |
| 8 | `autoresearch-karpathy → topics/ai-native/ai-programming` | ✅ **FILE.md** |
| 9 | `autoresearch-karpathy → topics/ai-native/agent-engineering` | ✅ **FILE.md** |
| 10 | `jeff-dean-tpu-story → insights/ai-technology/ai-infrastructure/insight-20260418-ai-energy-challenge` | ✅ **FILE.md** |

**结论**：**10/10 被报死链的路径全部真存在**。`wiki_auto_review.py` 的死链检测器**严重 bug**——把所有 wiki-link 都报死链（含真存在的）。

## 🛠 修复（P0.5 实质闭环 · 算法升级待 P1.5）

### 已修（实质闭环）

虽然 cron 算法误报，但 **5 个原本路径错的 wiki-link 已修成正确路径**，用户点击 Obsidian 链接可以真的跳转：

| 文件 | 修前路径 | 修后路径 |
|:---|:---|:---|
| 18year-ai-pioneer.md | `ai-native/agent-engineering` | `topics/ai-native/agent-engineering` |
| 18year-ai-pioneer.md | `insights/insight-20260429-karpathy-ai-agent-revolution` | `insights/agent/insight-20260429-karpathy-ai-agent-revolution` |
| autoresearch-karpathy.md | `ai-programming/vibe-coding` | `topics/ai-native/ai-programming` |
| autoresearch-karpathy.md | `ai-native/agent-engineering` | `topics/ai-native/agent-engineering` |
| jeff-dean-tpu-story.md | `insight-20260418-ai-energy-challenge` | `insights/ai-technology/ai-infrastructure/insight-20260418-ai-energy-challenge` |

### 待修（算法升级）

`wiki_auto_review.py` 死链检测器需要重写。当前算法可能：
- 只识别 `xxx.md` 不识别 `xxx/` 目录或 `xxx/README.md`
- 没处理 Obsidian wiki-link 的相对路径解析
- 没递归子目录扫描

**P1.5 任务**：
1. 重写 `deadlink_check()` 函数（递归解析 + 路径补全）
2. 增加白名单（archive/* 不算死链，目录含 README.md 不算死链）
3. 加 `--verify` flag（dry-run 不改文件）

## 💡 教训

| Lesson | 标题 | 治本 |
|:---|:---|:---|
| **L-50.1** | wiki-link 路径修复必先 verify 真实位置（ls + find）| ✅ 已用 |
| **L-50.2** | cron 算法误报率 > 50% 必须升级（不能信报告数字）| ⏳ 待 P1.5 |
| **L-50.3** | "修死链后跑 cron 数字不变" = 算法 bug 信号 | ✅ 本次命中 |
| **L-50.4** | 真死链 = 路径错（缺前缀/子目录）+ 引用方修改，不能光信报告 | ✅ 本次实证 |

## 关联

- **INC-2026-07-18-002**（5 个 wiki-link 路径修复闭环 · L-50.1 治本）
- **INC-2026-07-17-004**（wiki-health-check 双跑）— 同样 cron 治理盲区
- **L-50**（wiki-link 路径规范 + cron 算法升级族）
- **L-43**（批量元数据补必"不覆盖"已有 front-matter）—— 同为 Wiki 治理族

## 自我归因

我之前说"P0.5 完成 16 个真实死链修复"——错了。**实际只修了 5 个原本路径错的 wiki-link**，且 cron 算法本身有大 bug（10/10 误判）。报告数字没意义，要看真实文件系统状态。