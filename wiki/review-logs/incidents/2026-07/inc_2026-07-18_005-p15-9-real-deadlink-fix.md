---
title: inc 2026 07 18 005 p15 9 real deadlink fix
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, incidents, 2026-07, deadlink-fix, L-50.8]
date: 2026-07-18
---

# INC-2026-07-18-005: v3 算法揭穿的 9 个真死链修复闭环 + L-50.8 regex alias 踩坑

> **触发**: 2026-07-18 11:57 CST（文博"请继续清理"授权 P1.5 自然延续）
> **关联**: INC-2026-07-18-001（cron bug）+ INC-2026-07-18-004（算法升级）+ L-50.4/50.8
> **状态**: ✅ Closed（9/9 修复 · 总死链 712→703）

---

## 📋 现象

P1.5 算法升级 v3 揭穿 9 个真死链（路径错位 + 大小写 + 主题错位），需手动修引用方。

## 🔍 9 个真死链分类

| 类型 | 数量 | 案例 |
|:---|:---:|:---|
| **路径错位（typo）** | 1 | `topic-ai-native/ai-infrastructure`（缺 s）|
| **路径错位（缺子目录）** | 1 | `insight-20260417-harness-engineering`（实际在子目录）|
| **大小写敏感 + 路径错** | 3 | `AI Native/Agent Engineering` 等 |
| **主题错位（无对应文件）** | 4 | `fintech/data-governance` 等 → 改写到相近文件 |

## 🛠 修复（L-50.4 + L-50.8 治本）

### 修复明细

| 文件 | 修法 |
|:---|:---|
| `insight-20260427-jeff-dean-tpu-story.md` | `topic-ai-native/ai-infrastructure` → `topics/ai-native/ai-infrastructure` + `insight-20260417-...` 补子目录 |
| `insight-20260423-data-platform-report.md` | 4 处 `fintech/...` + `concepts/data-*` 改写到相近文件 |
| `insight-20260426-db-ai-skill-engineering.md` | 2 处 `AI Native/...` 大小写 + 路径 |
| `insight-20260426-linjunyang-agent-thinking.md` | 1 处 `AI Native/Multi-Agent Systems` 改写到 `topics/ai-agent/topic-04-multi-agent.md` |

### 🔴 L-50.8 踩坑（regex alias 处理）

第一次跑 Python 替换时，jeff-dean 的 2 个 wiki-link 没替换上——**我的 regex 没考虑 `|xxx` 别名**！

**踩坑实证**：
```python
# ❌ 错误：假设 wiki-link 结尾是 ]]
re.sub(r'\[\[topic-ai-native/ai-infrastructure\]\]', ..., line)
# 实际内容：'[[topic-ai-native/ai-infrastructure|AI基础设施专题]]'

# ✅ 正确：允许可选别名 \|xxx
re.sub(r'\[\[topic-ai-native/ai-infrastructure(\|[^\]]*)?\]\]', ..., line)
```

**L-50.8 lesson**：所有 wiki-link regex 必允许可选的别名 `\|xxx`。

## 📊 成果

| 指标 | Before（v3）| After（修 9 真死链）| 变化 |
|:---|:---:|:---:|:---:|
| 总死链 | 712 | **703** | **-9** ✅ |
| 总文件 | 1696 | 1697 | +1 |

**剩余 703 个死链**：包含大量 `AI Native/...` 大小写敏感类（前 20 已显示 7 个） + 其他路径错位。

## 🆕 L-50.8 lesson 落档

```
L-50.8 · wiki-link regex 必允许可选别名 \|xxx
  - 形式：\[\[path(\|[^\]]*)?\]\]
  - 错误示范：\[\[path\]\] 假设无别名
  - 实证踩坑：7-18 jeff-dean 2 个 wiki-link 没替换上
```

## 💡 教训族 L-50 升级

```
L-50.1 wiki-link 修前必 verify 真实位置
L-50.2 cron 误报率 > 50% 必须升级
L-50.3 修死链后 cron 数字不变 = 算法 bug
L-50.4 真死链 = 路径错 + 引用方修改
L-50.5 sed BSD bug 换 Python re.sub
L-50.2.1 v1 基础（.md 双向）
L-50.2.2 v2 目录支持
L-50.2.3 v3 大小写不敏感
L-50.2.4 误报率 > 50% 必须升级
L-50.8 wiki-link regex 必允许可选别名（7-18 实证踩坑）
```

## 备份链

```
/tmp/wiki-deadlink-fix3-20260718-115810/
  ├── insight-20260423-data-platform-report.md
  ├── insight-20260426-db-ai-skill-engineering.md
  ├── insight-20260426-linjunyang-agent-thinking.md
```

## 关联

- **INC-2026-07-18-001**（cron 算法 bug 揭穿）
- **INC-2026-07-18-004**（P1.5 算法升级 v1→v2→v3）
- **L-50**（wiki-link + cron 算法升级族）

## 自我归因

第一次跑替换脚本时，jeff-dean 的 2 个 wiki-link 因为 regex 没考虑别名而失败——**我应该在写脚本前先 verify 实际内容**（L-17 + L-50.1 治本未严格落实）。立即修正 + 落档 L-50.8 防再犯。

🕵️ 闭环完成 · 2026-07-18 11:58 CST