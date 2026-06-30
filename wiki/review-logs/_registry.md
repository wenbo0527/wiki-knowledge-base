# 派蒙 lessons 注册表（追加 6/15）

| Lesson ID | 标题 | 沉淀人 | 日期 |
|:---|:---|:---|:---|
| les_2026-06-15_001 | **派蒙查错 sqlite 路径 4 小时** | 派蒙 | 2026-06-15 19:16 |
| les_2026-06-15_002 | **AI 忽悠 3 类案例（Tony 格式漂移 / 钟离 AI 分身 Prompt 路径 / Nick v1→v2 0 min patch）** | 派蒙 | 2026-06-15 19:24 |

## 沉淀内容

### les_2026-06-15_001

- 派蒙 14:38-18:59 一直查 `/Users/wenbo/.openclaw/agents/main/agent/openclaw-agent.sqlite`（错的）
- 派蒙实际 agentDir = `/Users/wenbo/.openclaw/agents/paimon/agent/openclaw-agent.sqlite`
- 4 小时没核实顶层 config 写的 `agentDir` 路径
- 19:01 文博质问后才查清
- 19:01-19:10 修复链路：复制 key + hard restart + `openclaw doctor --fix`
- 最终：17/17 agent 401 解

### les_2026-06-15_002

文博 19:16 派单搜"被 AI 忽悠过吗"3 类案例：

1. **Tony 格式/术语不统一**（⭐⭐⭐⭐）：6-14/6-15 同一任务 C3C89082/5A4D5B9A 跨日命名漂移 3 维度
2. **差点微调但没上**（⭐⭐⭐）：钟离 AI 分身 P0-P3 完整 Prompt 路径（没用微调）
3. **Prompt 能解决却上重方案**（⭐⭐⭐⭐）：Nick v1→v2 "0 min patch"（改 1 个 Prompt 就够） + 6-8 反思"杀鸡用牛刀"

3 句话总结：
- AI 命名漂移 = 团队规范缺失
- 钟离 AI 分身 = Prompt 路径优先的标准范本
- 每次评估先问"改 Prompt 行不行"

## INC 关闭（6/15）

- INC-2026-06-15-001（4 cron 失败）：disable 保留，等文博拍改造方案
- INC-2026-06-15-002（smith model 缺失）：已修
- INC-2026-06-15-003（401 根因）：已修
- INC-2026-06-15-004（催收路径全断）：已用正确路径完成
- INC-2026-06-15-005（派单 OpenClaw 体检）：已完成
- INC-2026-06-15-006（派蒙查错 sqlite 4 小时）：已沉淀

### inc_2026-06-15_007（追加 6/15 20:36）

- 老六 agent 失踪 10 天（6-5 起断更）
- cron 任务 = 0
- HEARTBEAT.md "扫软链+ping 派蒙" 段缺失
- AGENTS.md 双保险 SOP 名义存在 / 实际单边实施（派蒙自欺）
- 派蒙 6-14/6-15 软链自检 = 反射糊弄（只看软链在不在，不看日报是否增长）
- 状态：🔄 Open / 等文博拍 A/B/C 方案
