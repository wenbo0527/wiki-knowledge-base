# INC-2026-07-19-004 · Nick 推送管线架构分析 v0.1（大纲）

> **INC 编号**：INC-2026-07-19-004
> **日期**：2026-07-19 10:10 CST
> **触发**：文博 10:05 "先做架构分析，再做完整重构"
> **状态**：⏳ v0.1 大纲 · 待文博拍板展开方向
> **关联**：INC-2026-07-19-001/002/003（健康度治本日）· L-13 OpenClaw 原生优先
> **目标**：从"代码腐烂 + 模块边界不清 + 推送碎片化"重构为"清晰分层 + 单一推送渠道 + 数据流解耦"

---

## 0️⃣ 核心问题（一眼可见）

### 0.1 代码腐烂严重

| 类型 | 文件 | 说明 |
|:---|:---|:---|
| **多版本并存** | `push_today_v1.py ~ v7.py` + `daily_push_runner_20260702.py` + `daily_pipeline.py` + `daily_pipeline_enhanced.py` | 7+ 个版本并存，哪个是 active？|
| **备份文件散落** | `.bak.20260626` × 3 | daily_pipeline / etf_hegang_report / feishu_pusher |
| **pusher 多版本** | `feishu_pusher.py` / `v2.py` / `v3.py` / `real.py` | 4 个版本并存 |
| **analyzer 多版本** | `analyzer.py` / `analyzer_v2.py` | 2 个版本并存 |
| **deprecated 目录** | `scripts/_deprecated/2026-07-01/` + `scripts/_backup_before_20260701/` | 历史备份未清理 |

### 0.2 模块边界不清

```
scripts/                                  skills/rss-intelligence/scripts/
├── morning_daily_writer.py              ├── daily_pipeline.py          ← RSS 推送
├── daily_tech_report.py                 ├── daily_pipeline_enhanced.py ← 增强版
├── c3_daily_check.py                    ├── etf_real_time_fetcher.py
├── sunday_cron_health_check.py          ├── etf_analyzer.py
├── github_tracker.py                    ├── etf_hegang_report.py
├── kb_tracker.py                        ├── analyzer_v2.py
├── evening_tracker.py                   ├── feishu_pusher.py (+ v2/v3/real)
├── daily_investment_report.py           ├── rss_fetcher.py
├── etf_hegang_report.py (skills/)       ├── multi_channel_pusher.py
└── lib/                                 ├── push_manager.py
    ├── lark_cli_wrapper.py              └── github_tracker.py (重复)
    └── etf_allocation.py                ...
```

**问题**：
- `daily_tech_report.py` 在 `scripts/`（Nick own）但用 `daily_pipeline.py` 的 fetcher（在 skills/）
- `daily_pipeline.py` 是 RSS 推送但又调 etf_analyzer（ETF 评估）
- `github_tracker.py` 在两个目录（重复）
- `etf_hegang_report.py` 既在 `scripts/` 也在 `skills/rss-intelligence/scripts/`

### 0.3 推送策略碎片化

**3 种推送方式并存**（同一脚本可能用 2-3 种）：

| 方式 | 调用 | 用途 | 副作用 |
|:---|:---|:---|:---|
| **FeishuPusher (wecom Nginx)** | `feishu_pusher.py` | 实际推企业微信 via Nginx 反向代理 | 100.79.15.93 Nginx 依赖 · corpid/secret 硬编码 |
| **lark-cli (飞书 user identity)** | `lark-cli im +messages-send --as user` | 推飞书（user identity）| needs scope `im:message.send_as_user`（L-18）|
| **sessions_send (cron gateway)** | OpenClaw cron delivery = announce | cron 完成后 gateway 自动推 stdout | stdout 长度上限（L-46）|
| **直接 print → stdout** | `print(message)` | 默认 fallback | 全部塞 stdout 触发 card 表格上限 |

### 0.4 数据流耦合

```
04:01 rss.collect           → topic_collection/collection_YYYYMMDD_HHMMSS.json (234 源 RSS)
04:01 topic_rss_collector   → topic_collection/collection_YYYYMMDD_HHMMSS.json (P0 源)
↓ (共享 fetcher.articles + db_path)
analyzer_v2 (SQLite 共享)
↓
08:30 morning·daily cron → morning_daily_writer.py → 生成 memory/daily/YYYY-MM-DD.md (内部)
08:30 rss.daily cron      → daily_pipeline.py       → 飞书推送 RSS 精选 + ETF
08:35 tech·briefing cron  → daily_tech_report.py   → 飞书推送技术日报 + Get 笔记
09:00 daily·report·c3     → c3_daily_check.py      → C-3 自检（内部告警）
21:00 daily·note·scan     → daily_note_scan.py     → Get 笔记入库扫描
21:00 daily·report·c3     → c3_daily_check.py      → C-3 自检

外部依赖：
- .getnote_env → GETNOTE_API_KEY (L-51 验证可用)
- 100.79.15.93 → Nginx wecom 反向代理
- akshare 1.18 / requests / lark-cli
```

**问题**：
- `daily_pipeline.py` 和 `daily_tech_report.py` 都读 `topic_collection/*.json` 但**没有共享去重**（同一文章可能两边都推）
- `analyzer_v2` 共享 SQLite 但 L-24 修复只是补丁
- 4 个 cron 触发时间紧邻（08:30 / 08:35 / 09:00）但**没有事务协调**（任一失败不影响其他）

### 0.5 配置散落

| 配置项 | 位置 | 风险 |
|:---|:---|:---|
| `corpid / corpsecret / agentid` | `feishu_pusher.py` 第 30 行硬编码 | 🔴 改 wangwang 必须改代码 |
| `100.79.15.93 Nginx` | `feishu_pusher.py` 第 251 行 | 🟠 换 IP 必须改代码 |
| 文博 open_id `ou_ca04de68...` | 各 cron argv + L-46 修复时用 | 🟢 单点 |
| RSS 源列表 | `config/sources_full.json` (缺失？看 skills/ 下) | 🟠 不在 config/ 而是别处 |
| `.getnote_env` | Nick home + 600 权限 | ✅ 已治本 L-51 |
| crontab argv 绝对路径 | OpenClaw cron 编辑器 | 🟠 移 home 必须批量改 |

---

## 1️⃣ 5 层架构建议（重构目标）

### 1.1 数据层（Data Layer）

```
data/
├── rss/
│   ├── raw/                       # 04:01 抓取的原始 JSON（topic_collection/）
│   ├── processed/                 # analyzer 后的精选 + 打分
│   └── cache/                     # fetcher 缓存（已存在）
├── getnote/
│   ├── kb_state.json              # KB 列表 + 笔记数（API sync）
│   └── sync_state.json            # 同步对账
├── wiki/
│   └── wiki_state.json            # Wiki 健康度指标
├── market/
│   ├── etf_realtime.db            # SQLite ETF 实时（替代 cache 文件）
│   └── etf_history.db             # ETF 历史
└── daily_briefs/                  # 每日简报归档（推飞书后落档）
    └── YYYY-MM-DD.md
```

**目标**：数据按"类型"切分，不按"脚本"切分（当前一个脚本一个数据目录）

### 1.2 业务层（Business Layer）

```
src/
├── domain/                        # 领域对象（纯数据）
│   ├── article.py                 # RSS 文章领域模型
│   ├── etf.py                     # ETF 领域模型
│   ├── getnote.py                 # Get 笔记模型
│   └── brief.py                   # 简报模型
├── fetcher/                       # 数据获取（adapter 模式）
│   ├── rss_fetcher.py             # RSS 抓取
│   ├── getnote_fetcher.py         # Get 笔记 API
│   ├── etf_fetcher.py             # ETF 实时（含 sina 备用源 L-46）
│   └── wiki_fetcher.py            # Wiki RAG API
├── analyzer/                      # 数据分析
│   ├── rss_analyzer.py            # RSS 打分 + 精选
│   ├── etf_analyzer.py            # ETF 何刚框架
│   └── getnote_analyzer.py        # Get 笔记摘要
└── composer/                      # 内容组合
    ├── morning_brief.py           # 早报组装（替代 daily_pipeline + daily_tech_report）
    ├── etf_brief.py               # ETF 独立报告
    └── tech_brief.py              # 技术简报
```

### 1.3 推送层（Push Layer）

```
src/pusher/
├── base.py                        # Pusher 抽象接口
├── feishu_user.py                 # lark-cli user identity（主推 · L-18 已治本）
├── feishu_wecom.py                # wecom Nginx 反向代理（已废弃 · 标记 DEPRECATED）
├── stdout.py                      # print + sessions_send（cron fallback）
└── router.py                      # 路由：选哪个渠道
```

**目标**：单一推送接口 + 路由器选渠道，废弃 wecom Nginx

### 1.4 调度层（Schedule Layer）

```
scripts/                           # 调度入口（薄壳，只调用 src/）
├── daily_morning.py               # 08:30 早报（合并 RSS + ETF + Get 笔记）
├── daily_etf.py                   # 08:35 ETF 独立报告（L-46 已治本）
├── daily_tech.py                  # 09:00 技术简报（独立推送，合并到 morning 也可）
├── daily_note_scan.py             # 21:00 Get 笔记扫描
├── c3_daily_check.py              # 21:00 + 09:00 C-3 自检
└── sunday_cron_health.py          # 周日 22:00 cron 健康度周报
```

**目标**：调度层只做 cron 触发 + 调用，不含业务逻辑

### 1.5 配置层（Config Layer）

```
config/
├── settings.yaml                  # 全局配置（环境变量 + 路径）
├── push_channels.yaml             # 推送渠道配置（user_id / agent_id）
├── rss_sources.yaml               # RSS 源列表
├── getnote.yaml                   # Get 笔记 KB 列表
└── cron_jobs.yaml                 # cron 定义（programmatic）
```

**目标**：配置与代码解耦，可测试

---

## 2️⃣ 重构路径（3 阶段）

### 阶段 1 · 清理腐烂（1 周 · 低风险）

- ✅ 归档 `push_today_v1.py ~ v7.py` → `_deprecated/`
- ✅ 归档 `daily_push_runner_20260702.py` → `_deprecated/`
- ✅ 归档 `.bak.20260626` × 3 → `_deprecated/`
- ✅ 选 active pusher：`feishu_pusher.py` (or `_real.py` 待评审)
- ✅ 归档 `analyzer.py` (用 `analyzer_v2.py` 替代)
- ✅ 删 `daily_pipeline_enhanced.py` (未启用)
- ✅ 解决 scripts/ 与 skills/rss-intelligence/scripts/ 重复文件（github_tracker.py 等）

**收益**：代码体积 -40% · 心智负担 -50%

### 阶段 2 · 边界重构（2 周 · 中风险）

- ✅ 实施 1.1 数据层（迁移数据目录结构）
- ✅ 实施 1.2 业务层（domain + fetcher + analyzer + composer）
- ✅ 实施 1.3 推送层（统一 Pusher 接口 + 废弃 wecom）
- ✅ 实施 1.4 调度层（薄壳化 cron 脚本）
- ✅ 实施 1.5 配置层（YAML 化）

**风险**：
- 数据迁移需写 migration 脚本
- 现有 4 个 cron argv 必须同步（避免 L-34 教训重演）
- 推送渠道切换需双轨并行 1 周

### 阶段 3 · 智能推送（1 个月 · 高价值）

- ✅ 推送时机自适应（不再固定 08:30/08:35）
- ✅ 内容去重（RSS 文章不重复推）
- ✅ 文博反馈学习（点赞/略过 → 调整精选权重）
- ✅ 多设备适配（手机/PC 不同推送格式）

---

## 3️⃣ 风险评估

| 风险 | 概率 | 影响 | 缓解 |
|:---|:---:|:---:|:---|
| 数据迁移破坏现有 cron | 🟠 中 | 🔴 高 | 双轨并行 1 周 + 每日 L-46 verify |
| 推送渠道切换失败 | 🟡 低 | 🟠 中 | lark-cli fallback → sessions_send |
| 业务逻辑丢失 | 🟠 中 | 🟠 中 | 端到端对比（旧 vs 新推送内容）|
| Cron argv 不同步 | 🟡 低 | 🟠 中 | L-34 防御：edit argv 后 24h verify |

---

## 4️⃣ 立即可做（不等文博拍板）

🟢 **今天 10:30**（Nick 自己可做的清理）：
- 备份 `_deprecated/` 目录创建
- `push_today_v1.py ~ v7.py` 列表 + 行数清单
- 写 `architecture_analysis_v0.2.md`（细化每一层）

🟡 **今天 14:00**（要文博拍板的）：
- 是否同意 5 层架构
- 是否同意 3 阶段路径
- 是否同意废弃 wecom Nginx 推送

---

## 5️⃣ 等文博拍板

| 决策点 | 选项 |
|:---|:---|
| **A 整体策略** | (a) 完整 5 层重构 · (b) 只做阶段 1 清理 · (c) 分阶段逐步推进 |
| **B wecom 推送** | (a) 废弃 · (b) 保留作 fallback · (c) 保留 + 维护 |
| **C 数据目录** | (a) 全面迁移 · (b) 软链接过渡 · (c) 保留现状只清代码 |
| **D 推送时机** | (a) 自适应 · (b) 保留固定 · (c) 文博手动触发 |

---

*🕵️ nick_fury · 2026-07-19 10:10 CST · 架构分析 v0.1 大纲 · 待文博拍板展开方向*
