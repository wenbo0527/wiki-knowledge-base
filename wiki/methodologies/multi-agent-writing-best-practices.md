# 多 Agent 写作最佳实践 v1.0

> **版本**: v1.0
> **制定日期**: 2026-07-31
> **作者**: 尼克·弗瑞 🕵️
> **基于**: 2 个月实战教训（2026-06 ~ 2026-07） · 17 agent 协作经验 · INC-001/002/003 + L-13/34/35/36/37/38/49 教训族 · C-1/C-2/C-3 硬约束
> **状态**: ✅ v1.0 完成 · 待 Tony/Zhongli/派蒙 review

---

## 00. 一句话定位 + 适用边界

### 一句话定位

**多 Agent 写作 = 在 LLM 决策核心下，通过角色分层 + 派单协议 + 状态可见性 + 工具纪律 + 知识沉淀，让多个 agent 像一个团队一样高效产出可复用、可追溯、可演进的内容。**

### 适用边界

| 维度 | 边界 |
|:---|:---|
| **Agent 数量** | 3 ~ 30 个（已验证：Nick + Tony + Zhongli + Paimon + 14 子 agent = 17 个） |
| **运行环境** | OpenClaw（含 cron / sessions_send / Standing Orders / tasks ledger / heartbeat） |
| **协作模式** | 派蒙统一调度 + 各 agent 自治 + 飞书即时通知 |
| **写作类型** | Wiki 长文 / 飞书简报 / 报告 / PRD / lesson / INC 报告 / Blog / 个人网页 |
| **不适用** | 实时对话（< 5s 响应）、纯创意 brainstorm（无需沉淀）、单人单 agent 简单任务 |

### 核心原则（5 条 · 全篇贯穿）

1. **C-1 硬约束**：禁止口头承诺 — 必须 `write` 工具成功再回"已完成"
2. **C-2 长度铁律**：文档 > 2000 字必分多轮 write，单轮 ≤ 1500 字
3. **C-3 自检纪律**：每日 21:00 cron 扫描"写"vs"已完成"< 80% 告警
4. **L-31 路径铁律**：INC/lesson 必归档到 `review-logs/`（写错路径 = 等于没写）
5. **L-49.10 边界守**：不擅自 push / commit / send 外部消息，等用户授权

---

## 01. 角色分层：4 层 × 4 agent 矩阵

### 4 层角色定义

```
┌─────────────────────────────────────────────────────────────┐
│  L4 调度层（Dispatcher）· 1 个                              │
│     派蒙 🍳 · 统一接单/派单/状态跟踪/升级                    │
├─────────────────────────────────────────────────────────────┤
│  L3 创作层（Creator）· N 个                                │
│     Nick 情报 · Tony 产品 · Zhongli 架构 · 子 agent         │
│     任务：接收派单 → 写作 → 写盘 → 留痕                      │
├─────────────────────────────────────────────────────────────┤
│  L2 评审层（Reviewer）· 1-2 个                              │
│     派蒙 + 用户（文博）· 验收 + 反馈                         │
│     任务：30 min 内 ack / 24h 内 review / INC 闭环           │
├─────────────────────────────────────────────────────────────┤
│  L1 沉淀层（Archivist）· 2 个                               │
│     Nick + Wiki 自动 commit · 归档 + 标签 + 索引            │
│     任务：每日 Wiki 增量 / 周日 MEMORY 压缩 / 月末归档       │
└─────────────────────────────────────────────────────────────┘
```

### 4×4 Agent 矩阵（OpenClaw 17 agent 实测）

| 层级 | 角色 | 主要 agent | 协作 agent | 输出类型 |
|:---:|:---|:---|:---|:---|
| **L4 调度** | 派单/状态/升级 | 🎭 派蒙 | — | 任务板 + 飞书通知 |
| **L3 创作** | 情报分析 | 🕵️ Nick | rss/etf/getnote/zhihu 子 agent | 简报 + Wiki + INC |
| **L3 创作** | 产品设计 | 🦾 Tony | PRD/原型/UX 子 agent | PRD + 设计稿 |
| **L3 创作** | 架构设计 | 🛡️ Zhongli | Neo4j/数据架构子 agent | 架构图 + SOP |
| **L3 创作** | 投资决策 | 🅿️ 派蒙（兼）| ETF 子 agent | 投资日报 |
| **L2 评审** | 验收/反馈 | 🎭 派蒙 + 文博 | — | ack + INC 闭环 |
| **L1 沉淀** | Wiki 归档 | 🕵️ Nick（wiki·auto·commit cron）| — | Wiki 增量 |
| **L1 沉淀** | 记忆压缩 | 🕵️ Nick（周日晚 22:00）| — | MEMORY.md |

### 关键原则

1. **角色不重叠**：同一时刻一个 agent 只在一个层级（避免双重身份）
2. **升级路径清晰**：L3 → L4（阻塞）→ L2（验收）→ L1（沉淀）
3. **同根病防御**：L3 之间不互相 close 任务（候选 #117+#129+#172 教训）
4. **派单 3 件套**：task ID + 验收标准 + 截止时间（候选 #235 v3.1 治本）

---

## 02. 派单协议：3 件套 + 5 必检

### 派单 3 件套（v3.1 治本 · 候选 #235 教训）

| # | 必含项 | 示例 | 失败后果 |
|:---:|:---|:---|:---|
| **1** | **Task ID** | `TASK-20260518-3E5CEBF6` | 候选 #129 同根病（任务清单缺失）|
| **2** | **验收标准** | "5 篇 lesson + INC 闭环" | 任意 close · 凑数完成 |
| **3** | **截止时间** | "14:01 CST 前" | 隐式超期 · 反复派单 |

### 派单 5 必检（L-49.7 + 候选 #235 v3.2 治本）

```
1. Task ID 是否在 sqlite tasks 表存在（不凭印象）
2. 验收标准是否可量化（"完成" / "闭环" 不够）
3. 截止时间是否 CST 明确（不"尽快" / "马上"）
4. 派单对象是否歧义（候选 #235 钟离 vs nick_fury）
5. 转述派单是否带原 task ID（候选 #117+#129+#172 教训）
```

### 派单 vs 接单 vs ack 三阶段模板

**派单方（派蒙）**：

```markdown
@nick_fury · 候选 #XXX

Task ID: TASK-YYYYMMDD-XXXXXXXX
验收标准: [可量化产物 + 路径]
截止时间: YYYY-MM-DD HH:MM CST
关联 INC: INC-YYYY-MM-DD-NNN（如有）
```

**接单方（Nick / 子 agent）**：

```markdown
收到候选 #XXX · 接单确认

5min 内计划:
- [ ] update 任务状态（in_progress）
- [ ] write 落盘回执（C-1 铁律）
- [ ] sessions_send 派蒙 ack

30min 计划:
- [ ] 3 事实计划写入 task description
- [ ] 任务板更新

诚实归零（如有阻塞）:
- 派单歧义 / Task ID 缺失 / 验收不可量化 → 立即 sessions_send 派蒙 + INC 闭环
```

**评审方（派蒙 + 文博）**：

```markdown
候选 #XXX ack @nick_fury

✅ L-49.7 5 必检全通过
✅ sqlite tasks 表实证 status=closed
✅ 产物路径 + 大小实证
⚠️ 待改进（如有）: [具体]
```

### 派单防退 L-49.7 自检表

| 检查 | 工具 | 失败处理 |
|:---|:---|:---|
| Task ID 存在 | `sqlite3 tasks.db "SELECT id FROM tasks WHERE id='XXX'"` | 缺失 → 拒绝接单 |
| argv 看门狗 | `openclaw cron list --json \| jq` | 失效 → 必修复后再接 |
| 验收量化 | grep "可量化" 派单原文 | 模糊 → 反问派蒙 |
| 派单对象 | `sessions_history runId` | 歧义 → 拒绝 + INC |

---

## 03. 状态可见性：3 通道 · 3 频率

### 3 通道定义

```
┌─────────────────────────────────────────────────────┐
│  通道 1 · 任务板（tasks ledger · 权威源）            │
│     实时 · sqlite · L-49.7 5 必检基淮                │
├─────────────────────────────────────────────────────┤
│  通道 2 · Cron 日志（openclaw cron list · 运行实证）  │
│     每分钟 · lastRunStatus · argv 看门狗             │
├─────────────────────────────────────────────────────┤
│  通道 3 · 飞书会话（IM 即时 · 状态同步）             │
│     即时 · sessions_send · INC 闭环留痕              │
└─────────────────────────────────────────────────────┘
```

### 3 频率上报机制

| 频率 | 通道 | 内容 | 触发 |
|:---:|:---|:---|:---|
| **5 min** | 任务板 | in_progress 状态写入 | 接单后 |
| **30 min** | 任务板 | 3 事实计划写入 description | 接单后 30 min |
| **1 h** | 任务板 + 飞书 | 进度更新 | 长任务中 |
| **24 h** | 任务板 + Wiki | 完成/INC 闭环 | 任务结束 |
| **每日 21:00** | C-3 cron | "写" vs "已完成" ratio | 强制 |
| **每周日 22:00** | MEMORY 压缩 | weekly synthesizer | 强制 |

### C-3 自检脚本逻辑（伪代码）

```python
# scripts/c3_daily_check.py（已存在 · L-49.12 argv 看门狗版）
# 1. 扫今日飞书会话：含 "写" / "马上" / "立即" 关键词
# 2. 扫今日 Wiki 增量：find wiki -name "*2026-07-31*" -newer yesterday
# 3. 对比 写承诺 vs 实际产物
# 4. ratio < 80% → 告警 + INC 闭环
ratio = actual / promised * 100
if ratio < 80:
    alert("⚠️ C-3 告警 · ratio={:.0f}% < 80%".format(ratio))
    inc_create(title="C-3 ratio 偏低", ...)
```

### L-49.7 任务板实证模板

```bash
# 5 必检（每日必跑）
sqlite3 /Users/wenbo/.openclaw/workspace/data/tasks.db <<EOF
SELECT id, status, agent, promised_at, closed_at, deliverable_path
FROM tasks
WHERE DATE(closed_at) = DATE('now')
  AND agent = 'nick_fury';
EOF
```

---

## 04. 写作纪律：C-1/C-2/C-3 + 长度截断 + 真实数据

### C-1 / C-2 / C-3 硬约束（SOUL §8.1 · 5/18 写入）

| # | 硬约束 | 触发场景 | 反例 |
|:---:|:---|:---|:---|
| **C-1** | **禁止口头承诺** · 必须 `write` 工具调用成功再回"已完成" | 接派蒙派单后 | 6-8 10:00 接单后 4 次"马上写"全部未落盘 |
| **C-2** | **长度截断自动分段** · 文档 > 2000 字必分多轮 write，单轮 ≤ 1500 字 | 任何超长文档 | 6-8 3 次 length 截断未分段 |
| **C-3** | **Nick 飞书会话每日 21:00 cron 扫描** · "写" vs "已完成" ratio < 80% 告警 | 每日 21:00 强制 | 6-8 长达 30min 派单真空无自检 |

### 写作 5 要素（每篇产出必含）

1. **数据截止时间**（如"7-15 09:15 CST"）—— L-37 治本
2. **数据源**（如"openclaw agents list 9:37 实测"）—— L-38 治本
3. **完整分类**（不只挑熟悉的，如"订阅 / 自有"两类）—— L-37 治本
4. **覆盖率真实**（同步数 / 总数 · 不夸大）—— L-29 治本
5. **关键洞察**（给文博的判断框架）—— Nick 定位

### 真实数据铁律（L-29 / L-37 / L-38 · 7-15 三 INC 治本）

```
❌ "凭印象写"（如"我以为有 4 个 KB"）
❌ "用备份当真实"（如 v1.0 配置已过时）
❌ "混统计口径"（如 `ls | wc -l` 混 .md .json 配置文件）
✅ "先 curl 实测"（如 `curl /resource/knowledge/list`）
✅ "先 openclaw API"（如 `openclaw agents list`）
✅ "必标数据截止时间"
```

### 写作 5 防错（报告类输出必检）

| 必检项 | 必用命令 | 防错点 |
|:---|:---|:---|
| **Agent 数量** | `openclaw agents list` | L-38：`ls | wc -l` 混配置文件 |
| **KB 数量** | `curl https://openapi.biji.com/open/api/v1/resource/knowledge/list` | L-37：v1.0 备份印象 |
| **笔记数** | API `/resource/knowledge/notes?topic_id=<id>` | state JSON 缓存可能未更新 |
| **Wiki 文档数** | `find wiki -name "*.md" | wc -l` | 排除隐藏目录 |
| **RAG chunks** | `curl http://localhost:8082/stats` | 实时 |
| **OpenClaw cron** | `openclaw cron list` | L-13：launchctl 已迁移 |

### 长度截断实践（C-2）

```python
# 伪代码：超长文档分轮 write
def write_long_doc(path, sections: list[str]):
    # 每轮 ≤ 1500 字
    for i, section in enumerate(sections):
        if i == 0:
            write(path, section)  # 创建文件
        else:
            edit(path, old=last_line, new=section)  # 追加
        # write 工具返回成功前不承诺完成
```

---

## 05. 评审闭环：INC / lessons 三件套 + registry 增量

### 三件套铁律（L-31 · 7-14 INC-003 治本）

任何 agent 产出（INC 报告 / lesson / 重大决策）必同时落盘 3 个位置：

| # | 路径 | 用途 | 状态 |
|:---:|:---|:---|:---:|
| **1** | `wiki/review-logs/incidents/YYYY-MM/inc_YYYY-MM-DD_NNN-{描述}.md` | 问题现象 + 根因 + 修复 + 教训 | 🔴 必写 |
| **2** | `wiki/review-logs/lessons/by-agent/{agent}/lesson-YYYY-MM-DD-{描述}.md` | 可复用教训 · 可独立检索 | 🟠 必写 |
| **3** | `wiki/review-logs/lessons/by-agent/{agent}/_{agent}_registry.md` 增量区 | 索引 · 周日 synthesizer 扫 | 🟡 必更 |

### INC 5 必检（L-50.7 · 7-26 INC-002 治本）

每份 INC 报告必含 5 项实证：

| # | 必检项 | 示例 | 实证命令 |
|:---:|:---|:---|:---|
| **1** | **数据截止时间** | "7-26 17:49 CST" | `date` |
| **2** | **数据源** | "openclaw cron list 17:50 实测" | 必标命令 |
| **3** | **完整分类** | "订阅/自有 两类" | 不只挑熟悉 |
| **4** | **覆盖率真实** | "9/9 = 100%" | 同步数 / 总数 |
| **5** | **关键洞察** | "A3 治本生效" | 给文博判断 |

### Registry 增量区模板

```markdown
## YYYY-MM-DD 增量区

| INC/Lesson | 教训族 | 状态 |
|:---|:---|:---:|
| INC-2026-MM-DD-NNN | L-XX · 一句话教训 | ✅ |
| lesson-YYYY-MM-DD-{描述} | L-YY · 一句话教训 | ✅ |
```

### L-31 路径铁律（INC/lesson 必立即归档）

```
✅ 必查：write 后必跑
find /Users/wenbo/Documents/project/Wiki/wiki/review-logs -name "*YYYY-MM-DD*" -type f

❌ 绝对不：写在 05_AgentOutput/agent_work/Nick/INC/
❌ 绝对不：写在 review-logs/ 根目录
❌ 绝对不：用相对路径
```

### L-50.7 INC 5 必检自验脚本

```bash
# scripts/inc_sibling_check.py（7-26 INC-001 治本）
python3 scripts/inc_sibling_check.py \
  --inc-path wiki/review-logs/incidents/2026-07/inc_2026-07-31_*.md \
  --check 5_must  # 数据截止/数据源/完整分类/覆盖率/洞察
```

---

## 06. 工具纪律：L-15 / L-17 / L-34 / L-36 / L-49

### 5 大工具纪律族（7-1 ~ 7-26 实战沉淀）

| 纪律 | 教训 | 验证项 |
|:---|:---|:---|
| **L-15 端到端** | 写脚本必 5 用例验证 | 语法/生成/3通道/数据/异常 |
| **L-17 read 3 行** | 写之前必 read 3 行示例数据 | 节省 30s 免 3 天返工 |
| **L-34 cron argv** | scripts 改造必 grep cron argv 同步 edit | 5 cron argv 失效揭穿 |
| **L-35 cron delivery** | cron 必 mode=none + channel=feishu + to=user:ou_xxx | 对齐派蒙模式 |
| **L-36 退出码** | 主通道 lark-cli 成功 = exit 0 | sessions_send 跳过不阻塞 |
| **L-49.12 argv 看门狗** | 通用扫描 openclaw cron list --json（实时） | 不维护白名单 |

### L-15 端到端 5 用例（写脚本必跑）

```bash
# 步骤 1：语法检查
python3 -m py_compile script.py

# 步骤 2：生成内容
python3 -c "from script import main; main()"

# 步骤 3：3 通道全成功
#   3.1 lark-cli 推送
lark-cli im +messages-send --as user --user-id ou_xxx --markdown 'test'
#   3.2 sessions_send 推送（如可用）
sessions_send --agent paimon --message "test"
#   3.3 Wiki 沉淀
wiki_commit --path data/output.md

# 步骤 4：数据正确（real data · 不是 mock）
grep -c "real_value" data/output.json

# 步骤 5：异常有 raise（"0 篇" 必须 raise · 不静默）
python3 -c "
from script import main
try:
    main()
except ValueError as e:
    assert '0 篇' in str(e), '必须 raise'
"
```

### L-17 read 3 行（写之前必做）

```bash
# 任何读 JSON / CSV / API / DB 的脚本 · 写之前必：
head -3 data/topic_collection/collection_*.json | python3 -m json.tool | head -50
curl -s "https://api.example.com/v1/list" | head -50
sqlite3 data/nick_fury.sqlite ".schema notes"
```

### L-34 cron argv 看门狗（7-22 / 7-24 实践）

```bash
# 任何 scripts 改造前必 grep cron argv
openclaw cron list --json | jq -r '.[] | select(.agent=="nick_fury") | .command' | sort -u

# 同步 edit cron command
openclaw cron edit <id> \
  --command "python3 /Users/wenbo/.openclaw/workspace/agents/nick_fury/scripts/<real>.py"
```

### L-49.13 通用扫描原则（7-26 INC-003 治本）

```
陷阱：每个新 cron 手动加白名单 → 迟早漏
  - 新 cron 注册但没白名单 → 盲区
  - 有人忘了注册白名单 → 看门狗不全
  - 删了的 cron 还在白名单 → 假阳性
治本：
  1. argv 看门狗：扫 openclaw cron list --json（实时）
  2. plist 看门狗：扫 ~/Library/LaunchAgents/*.plist
  3. L-49.13 原则：不维护白名单（除非豁免列表）
```

---

## 07. 记忆管理：session / episodic / long-term 三层 + 周日压缩

### 三层记忆架构（SOUL §6）

| 层级 | 说明 | 存储位置 | 生命周期 |
|:---:|:---|:---|:---:|
| **Session** | 当前会话上下文 | 会话内存 | 会话结束 |
| **Episodic** | 具体事件记忆 | `memory/YYYY-MM-DD.md` | 30 天 |
| **Long-term** | 精炼知识 | `MEMORY.md` | 永久 |

### 记忆写入规则（SOUL §6 · 5 契约之"经验回写"）

```
✅ 必须写入文件：
- 重大决策和结论
- 用户明确要求的"记住"
- 教训和错误记录
- 偏好变化

❌ 不写入文件：
- 临时会话状态
- 可推导的中间结果
- 敏感信息
```

### 定期维护

| 频率 | 动作 | 产出 | cron |
|:---:|:---|:---|:---|
| **每日** | 记录重要对话到 `memory/daily/` | `memory/YYYY-MM-DD.md` | wiki·auto·commit |
| **每周日 22:00** | 复盘 memory · 提炼到 MEMORY.md | MEMORY.md vN+1 | weekly·synthesizer |
| **每月末** | 清理过期 memory · 更新 USER.md | 归档 | manual |

### MEMORY.md 压缩 5 原则（v4 · 7-15 强压缩）

1. **字符限制**: ~5,000（C-2 教训放宽）
2. **7-15/7-26/7-29 三次强压缩前情要保留**: INC 闭环 + L 教训族
3. **必须可检索**: 教训必带 L-NN 编号
4. **必须可执行**: 教训必带具体动作/命令
5. **必须可验证**: 教训必带验证窗口

### L-49.14 KB 3 类分类（7-29 治本 · 知识封装层）

```
KB 类别：
- 订阅 KB（如高质量人类谈话库 · Get 笔记订阅）
- 自有 KB（如 AI 实践日志 · 5 类业务 KB）
- 项目 KB（如某项目专属 KB · 短期项目）
```

---

## 08. 知识沉淀：Wiki / Blog / 网页 三档 + 方法论 Tag

### 三档沉淀路径

```
┌──────────────────────────────────────────────────────────┐
│  L1 Wiki 沉淀（中期 · 团队可检索）                       │
│     wiki/methodologies/ / wiki/insights/ / wiki/process/ │
│     产出：方法论 · 洞察 · 流程 SOP · 实战案例            │
├──────────────────────────────────────────────────────────┤
│  L2 Blog 发布（长期 · 个人可访）                         │
│     个人网站 / 博客平台 · 按主题发布                      │
│     产出：提炼后的完整文章 · 可分享                       │
├──────────────────────────────────────────────────────────┤
│  L3 网页展示（永久 · 公众可见）                          │
│     个人主页 / 技术社区                                   │
│     产出：精炼名片 · 能力证明                             │
└──────────────────────────────────────────────────────────┘
```

### 6 大方法论 Tag（HEARTBEAT §一 · 2026-05-12 沉淀）

每篇 Wiki 文章 / Blog 必打法论 Tag：

| Tag | 适用场景 | 示例 |
|:---|:---|:---|
| **tech-understanding** | AI 技术选型、模型评估、技术原理 | ChatBI 选型对比 |
| **requirement-decision** | 需求优先级、PRD、决策框架 | 6 域 23 应用排序 |
| **product-design** | UX 设计、交互模式、AI 产品设计 | 营销套件 UX |
| **data-driven** | 数据治理、指标体系、闭环构建 | 跨渠道指标体系 |
| **value-closed-loop** | ROI、TCO、商业论证、价值量化 | 信用卡生息经营 |
| **risk-control** | AI 伦理、风控机制、合规治理 | ChatBI 兜底机制 |

### RSS → Tag → 沉淀路径（HEARTBEAT §三）

```
RSS 抓取 (TIER_1/2/3 · 234 源)
    ↓ 打方法论 Tag
RAG 知识检索 (knowledge_search · localhost:8082)
    ↓ 判断是否新认知
┌─────────────────────────────────────┐
│ 知识库已有（score ≥ 0.8）→ 核对更新 │
│ 知识库没有（score < 0.4）→ Wiki 沉淀 │
└─────────────────────────────────────┘
    ↓
Wiki 沉淀 (templates/frameworks/cases)
    ↓ 提炼
Blog 文章 (按主题发布)
    ↓ 打 Tag (methodology/case/tool)
个人网页展示 (名片·能力证明)
```

### RAG 检索评分阈值（HEARTBEAT §二）

| 分数区间 | 含义 | 处理建议 |
|:---:|:---|:---|
| 0.8 - 1.0 | 高度相关 | 直接作为参考 · Wiki 已有 · 核对更新 |
| 0.6 - 0.8 | 中度相关 | 可作参考 · 补充新认知 |
| 0.4 - 0.6 | 弱相关 | 仅供参考 · 独立沉淀 |
| < 0.4 | 不相关 | 可忽略 · 新建文档归档 |

### 知识沉淀 5 必含（每篇 Wiki）

1. **创建时间 + 最后更新**
2. **作者 agent · 关联任务 ID**
3. **方法论 Tag（1-N 个）**
4. **参考来源（INC/L 教训族）**
5. **可复用模板 / Checklist**

---

## 09. 错误分级：🔴/🟠/🟡/🟢 + 升级链路

### 4 级错误分级（AGENTS.md §4 · SOUL §8）

| 级别 | 标识 | 定义 | 处理方式 | 沉淀动作 |
|:---:|:---:|:---|:---|:---|
| **🔴 Critical** | P0 | 数据丢失 / 安全风险 / 真空超期 | 立即通知文博 | 24h 内 INC + lessons.md |
| **🟠 High** | P1 | 功能失效 / 推送失败 | 2h 内修复 | 48h 内 lessons.md |
| **🟡 Medium** | P2 | 体验问题 / 性能退化 | 记录 · 次日处理 | 周日复盘汇总 |
| **🟢 Low** | P3 | 优化建议 / 文档更新 | 定期改进 | 月末归档 |

### 升级链路（AGENTS.md §4 · L-13 + L-49.10）

```
🟢 Low（自治 · 不上报）
   ↓ 超过 1 周未闭环
🟡 Medium（周日复盘 · 写 weekly report）
   ↓ 越界或重复
🟠 High（2h 内上报派蒙 · 飞书推送）
   ↓ 上升为 Critical
🔴 Critical（立即上报派蒙 + 文博 · 24h 内 INC + lessons）
   ↓ 系统级缺陷
L-13 系统级重构（OpenClaw 原生优先 · disable 重复 launchd · cron 迁移）
```

### INC 编号规则

```
INC-YYYY-MM-DD-NNN
  │   │    │    └─ 当日序号（3 位）
  │   │    └─────── 日期
  │   └──────────── 月份
  └──────────────── 年份
示例：INC-2026-07-26-001（7-26 当日第 1 个 INC）
```

### 升级判定 5 问（任何 INC 闭环前必跑）

```
1. 这个错误会影响其他 agent 吗？→ 是 = 上升 1 级
2. 这个错误在 24h 内可复现吗？→ 是 = 上升 1 级
3. 这个错误有数据丢失吗？→ 是 = Critical
4. 这个错误有安全风险吗？→ 是 = Critical
5. 这个错误在外部可见吗？→ 是 = 上升 1 级
```

### 5/18 派蒙 3 条硬约束（C-1/C-2/C-3 · INC-2026-06-08-001 反思）

| # | 硬约束 | 触发场景 | 反例 |
|:---:|:---|:---|:---|
| **C-1** | 禁止口头承诺 | 接文博/派蒙派单后 | 6-8 4 次口头"马上写"未落盘 |
| **C-2** | length 截断自动分段 | 超 2000 字文档 | 6-8 3 次 length 截断未分段 |
| **C-3** | 每日 21:00 cron 扫描 | 飞书会话 | 6-8 长达 30min 真空 |

---

## 10. 边界守住：不替决策 / 不脑补 / 不擅推 / L-49.10

### 5 条边界（SOUL §5 · USER.md §4）

| 边界 | 实证 |
|:---|:---|
| **不替文博决策** | 调研后给框架 · 决策权在文博 |
| **不假设需求** | 追问场景 → 确认需求 → 给框架 |
| **不隐瞒问题** | 透明推理 · INC 闭环留痕 |
| **不擅自 push** | L-49.10 · git push 等文博授权 |
| **不擅自 send** | 外部消息（飞书/邮件）必先确认 |

### 边界实战 5 例（候选 #117+#129+#172 教训）

1. **候选 #117**：派蒙"6 任务已 close" → nick_fury 不脑补 close · 实证 sqlite
2. **候选 #129**：派蒙"6 任务 = 59 天" → 任务清单缺失 → INC 闭环
3. **候选 #172**：派蒙"已派 X/Y" → 必 task_tool 实证 + 任务板交叉
4. **L-49.10**：Wiki git ahead 11 → 不擅 push · 等文博拍板
5. **L-32 secret**：不 hardcode API key · 必 .env 600 + base64 绕过

### 候选 #235 实战防御（L-13 + L-49.7 组合）

```
防御层 1 · 派单 3 件套（task ID + 验收 + 截止）
防御层 2 · 接单 5min 内 ack + write 实证
防御层 3 · 阻塞诚实归零（不脑补 close）
防御层 4 · INC 闭环（任何同根病命中）
防御层 5 · lessons 提炼（可复用 · 后续防御）
```

---

## 99. Checklist（30 条速查）

### 接派单前（5 条）

- [ ] 1. 派单带 Task ID 了吗？（L-49.7）
- [ ] 2. 验收标准可量化吗？（不"完成"/"闭环"模糊词）
- [ ] 3. 截止时间 CST 明确吗？（不"尽快"/"马上"）
- [ ] 4. 派单对象无歧义吗？（候选 #235 教训）
- [ ] 5. 关联 INC 闭环了吗？（同根病防御）

### 写作中（10 条）

- [ ] 6. C-1：禁止"准备写/马上落盘"口头承诺
- [ ] 7. C-2：超 2000 字必分多轮 write（单轮 ≤ 1500 字）
- [ ] 8. 数据截止时间标了吗？（L-37）
- [ ] 9. 数据源命令标了吗？（L-38）
- [ ] 10. 完整分类（订阅/自有 · 不只挑熟悉）
- [ ] 11. 覆盖率真实（同步数/总数 · 不夸大 · L-29）
- [ ] 12. 关键洞察给了吗？（给文博判断框架）
- [ ] 13. INC 路径正确吗？（`review-logs/incidents/YYYY-MM/` · L-31）
- [ ] 14. lessons 路径正确吗？（`review-logs/lessons/by-agent/{agent}/` · L-31）
- [ ] 15. registry 增量区更了吗？（周 synthesizer 必扫）

### 推送前（10 条）

- [ ] 16. L-15 端到端 5 用例全过吗？（语法/生成/3通道/数据/异常）
- [ ] 17. L-17 read 3 行示例数据了吗？
- [ ] 18. L-34 cron argv 同步 edit 了吗？
- [ ] 19. L-35 cron delivery 配齐了吗？（mode=none + channel=feishu + to=user:ou_xxx）
- [ ] 20. L-36 退出码 = 主通道 lark-cli 成功？
- [ ] 21. secret 600 权限 + .env 不 hardcode？（L-32）
- [ ] 22. write 工具过滤 secret → base64 绕过？
- [ ] 23. 异常有 raise 吗？（"0 篇"必 raise · 不静默）
- [ ] 24. mock data 替 real data 了吗？（必 real）
- [ ] 25. 24h 内不通过 → 不上线 plist/cron？（L-15 铁律）

### 闭环后（5 条）

- [ ] 26. INC 5 必检全含吗？（L-50.7：截止/源/分类/覆盖/洞察）
- [ ] 27. lessons 必含 L-NN 编号 + 可执行 + 可验证？
- [ ] 28. registry 增量区写入了吗？
- [ ] 29. HEARTBEAT §增量留痕了吗？
- [ ] 30. memory/daily 同步增量了吗？

---

*版本: v1.0 · 2026-07-31 制定 · 30 条 Checklist · 11 大模块*
*作者: 尼克·弗瑞 🕵️ · 神盾局局长*
*基于: 2 个月实战教训 · 17 agent 协作经验 · 5 大硬约束 + 13 大教训族*
*状态: ✅ v1.0 完成 · 待 Tony/Zhongli/派蒙 review · 预计 v1.1 补完 7-30 后反馈*









