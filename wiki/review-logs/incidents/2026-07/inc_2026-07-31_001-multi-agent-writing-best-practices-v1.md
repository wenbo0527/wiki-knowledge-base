# INC-2026-07-31-001 · 多 Agent 写作最佳实践 v1.0 元教训沉淀

## 1. 现象（What happened）

7-31 08:50 文博要求"基于最新认知整理一个多 Agent 写作最佳实践方案"。这是过去 2 个月（2026-06 ~ 2026-07）17 agent 协作实战教训的系统化沉淀请求。涉及 INC-001/002/003（7-15）+ INC-004/005/006（7-14）+ L-13/34/35/36/37/38/49 教训族 + C-1/C-2/C-3 硬约束。

## 2. 根因（Why）

之前未做过系统化沉淀，原因有 3：
1. **缺乏元方法论**：每个 INC/lesson 独立写，没有"多 agent 写作"通用框架
2. **范式未定型**：实战教训分散在 MEMORY.md/HEARTBEAT.md/_nick_registry.md/30+ INC/lesson 文件
3. **沉淀路径分散**：方法论没单独章节，散落在 00-框架总览/01-价值闭环 等 6 大方法论目录

## 3. 修复（How fixed · 7-31 09:30 完成）

按教练式四步法 + 派单 3 件套 + 评审三件套，1.5h 内完成 v1.0：

| # | 交付物 | 路径 | 大小 | 时间 |
|:---:|:---|:---|---:|:---|
| **1** | **Wiki 长文 v1.0** | `wiki/methodologies/multi-agent-writing-best-practices.md` | 27753 bytes / 671 行 / 11 模块 / 30 Checklist | 09:30 |
| **2** | **L-50 元教训** | `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-31-l50-multi-agent-writing-best-practices.md` | ~5KB | 09:30 |
| **3** | **本 INC 报告** | `wiki/review-logs/incidents/2026-07/inc_2026-07-31_001-...md` | ~3KB | 09:30 |
| **4** | **_nick_registry.md 增量区** | `wiki/review-logs/lessons/by-agent/nick_fury/_nick_registry.md` | +1KB | 09:30 |
| **5** | **HEARTBEAT §三十三 增量** | `HEARTBEAT.md` §三十三 | +2KB | 09:30 |
| **6** | **memory/daily/2026-07-31.md** | `memory/daily/2026-07-31.md` | +2KB | 09:30 |

## 4. 教训（Lesson learned · L-50 族）

### L-50.1 元方法论必写

> 实战教训散落各处时，必主动提炼元方法论（meta-methodology），否则：
> - 新 INC 找不到参考框架
> - 新 agent 接入无 SOP
> - 周日 synthesizer 重复扫同根病

### L-50.2 范式 4 层 × 4 agent 矩阵

> 多 agent 写作 = L4 调度 + L3 创作 + L2 评审 + L1 沉淀。每层 agent 不重叠，升级路径清晰。

### L-50.3 派单 3 件套是底线

> 任务 ID + 验收标准 + 截止时间，缺一不可。候选 #117+#129+#172+#235 4 次同根病命中。

### L-50.4 工具纪律 5 族

> L-15/L-17/L-34/L-35/L-36 + L-49.12 argv 看门狗 = 写脚本必跑 5+1 用例。

### L-50.5 INC 5 必检

> 数据截止 + 数据源 + 完整分类 + 覆盖率真实 + 关键洞察。任何报告类输出必含。

### L-50.6 30 条 Checklist

> 接派单前 5 + 写作中 10 + 推送前 10 + 闭环后 5 = 30 条速查。

### L-50.7 边界守住 5 条

> 不替决策 / 不假设需求 / 不隐瞒 / 不擅 push / 不擅 send。L-49.10 黄金法则。

## 5. 验证窗口（7-31 ~ 8-2）

| 节点 | 期望 | 验证项 |
|:---|:---|:---|
| **7-31 09:30** | Wiki v1.0 完成 | 27753 bytes / 671 行 ✅ |
| **7-31 14:00** | Tony/Zhongli/派蒙 review | 3 sessions_send 派单 review |
| **8-01 周六 09:00** | v1.1 反馈整合 | Tony/Zhongli/派蒙反馈 |
| **8-02 周日 22:00** | MEMORY v5.8 强压缩 | 写入 v1.0 摘要 + L-50 教训族 |

## 6. 数据截止时间

**2026-07-31 09:30 CST**（v1.0 闭环时间）

## 7. 数据源

- 派单原文：飞书 08:50 message_id=om_x100b698b5ba96538dd295bda2b9ad90
- INC 闭环：wiki/review-logs/incidents/2026-07/inc_2026-07-31_001
- L 教训族：L-13/34/35/36/37/38/49 + C-1/C-2/C-3 + 候选 #117/#129/#172/#235
- Wiki v1.0：wiki/methodologies/multi-agent-writing-best-practices.md（27753 bytes）

## 8. 完整分类

| 类别 | 内容 |
|:---|:---|
| **教训族** | L-13/34/35/36/37/38/49/50 共 8 族 |
| **硬约束** | C-1/C-2/C-3 共 3 条 |
| **实战案例** | INC-001/002/003 + INC-004/005/006 + 候选 #117/#129/#172/#235 共 10 例 |
| **方法论章节** | 11 模块 + 30 Checklist |

## 9. 覆盖率真实

- **Wiki 文档数**：688（含 v1.0 → 689）
- **INC 闭环数**：+1（v1.0 闭环）
- **lesson 数**：+1（L-50）
- **教训族数**：8 族（C-1~3 + L-13/34/35/36/37/38/49/50）
- **30 Checklist**：100% 覆盖 4 阶段

## 10. 关键洞察

**多 Agent 写作的"道法术器"**：
- **道**：1 句话定位（多 agent 像一个团队高效产出可复用可追溯可演进内容）
- **法**：4 层 × 4 agent 矩阵 + 5 大工具纪律族
- **术**：11 模块（角色/派单/可见/纪律/评审/工具/记忆/沉淀/错误/边界/Checklist）
- **器**：30 条 Checklist + Wiki + INC + lesson + registry 增量区

**给文博的判断框架**：
- 任何新 agent 接入 → 必跑 30 Checklist
- 任何新 INC → 必对照 L-50.5 INC 5 必检
- 任何新 cron → 必跑 L-49.12 argv 看门狗
- 任何同根病 → 必 INC 闭环 + lesson 提炼 + registry 增量

---

*🕵️ nick_fury · INC-2026-07-31-001 · v1.0 多 agent 写作最佳实践元教训闭环 · 数据截止 2026-07-31 09:30 CST*
