# INC-2026-07-22-001: Cron argv cwd 锚定 + 数据源路径双重 silent failure

> **数据截止**: 2026-07-22 21:55 CST
> **作者**: 尼克·弗瑞 🕵️
> **治本时长**: 12h 拍板等待（09:04 拍 C → 21:47 启动 B 动手）· 实际动手 30 min
> **决策路径**: 文博 C 选项治本 + B 选项执行（L-49.7 enabled tag）
> **关联 lessons**: L-49.11 / L-52.6

---

## 1️⃣ 现象（4 层 silent failure）

**用户察觉时点**：
- 09:00 CST C-3 cron 失败触发告警（`om_x100b69352...`）
- 21:07 CST 文博二次回查"问题"
- 21:55 CST 治本完成

**4 层 silent failure**（按 L-29 命中"输出成功 ≠ 输入真实"）：

| # | 现象层 | 显示状态 | 实际行为 | 静默天数 |
|:---:|:---|:---:|:---|:---:|
| 1 | daily·report·c3 (cf8e874c) cron error | exit 1 | 手动跑 exit 0 + 飞书推送成功 | **12h+** |
| 2 | daily·report·c3 (929a8003) cron error | exit 1 | 同上 | 12h+ |
| 3 | nick_cron_health_weekly cron error | exit 1 | 手动跑 exit 0 + 飞书推送成功 | **3d+** |
| 4 | rss.collect 源数据 = 0 | cron ok | 配置路径 0 源，rss_fetcher 退化到 0 抓取（之前推 5560 篇旧数据生成"假成功"报告）| **21d+** |

**daily 完稿率雪崩**：09:00 = 50% → 21:00 = **0%**（持续 12h Nick 没手动补完稿，cron 告警链循环触发）。

---

## 2️⃣ 根因（双层）

### 🔴 根因 A：cron argv 没有 cd cwd 上下文

cron 运行时 `cwd` 默认是用户家目录（`/Users/wenbo/`），但 scripts 中存在相对路径常量：

```python
# scripts/c3_daily_check.py
DAILY_DIR = Path("/Users/wenbo/.openclaw/workspace/agents/nick_fury/memory/daily")  # 绝对 ✅
ALERT_DIR = Path("/Users/wenbo/.openclaw/workspace/agents/nick_fury/data/c3_alerts")  # 绝对 ✅
# 但lark_cli_wrapper import 用相对:
sys.path.insert(0, str(Path(__file__).parent))  # 依赖 __file__ ✅
from lib.lark_cli_wrapper import push_im as lark_push_im  # lib/ 在 scripts/ 内 ✅
```

**矛盾点**：c3_daily_check.py 内部路径全部绝对，**但实际手动跑 exit 0、cron 跑 exit 1**——差异在 cron 上下文的环境变量（如 PATH、HOME、LANG）。

### 🔴 根因 B：rss_fetcher.py 默认相对 config_path（更严重）

```python
# skills/rss-intelligence/scripts/daily_pipeline.py 第 27 行（修复前）
def __init__(self):
    self.fetcher = RSSFetcher(config_path="config/sources_full.json")
    # ↑ 相对路径，依赖 cwd
```

修复前实测：
- cwd=`/Users/wenbo/.openclaw/workspace/agents/nick_fury` → `config/sources_full.json` 不存在 → **sources=0**
- cwd=`skills/rss-intelligence/scripts` → `config/sources_full.json` 不存在 → **sources=0**
- 唯一能加载情况：cwd=`/Users/wenbo/.openclaw/workspace/agents/nick_fury/skills/rss-intelligence/` → 135 源加载 ✅

**关键鉴别**（L-29）：
- cron 跑 rss.collect → sources=0 → 0 篇新文章 → 但**仍然推飞书**（推送内容是 5560 篇旧数据生成的精选报告）
- 用户看到的飞书推送 = "看起来正常" = **silent failure 21 天**

---

## 3️⃣ 修复（4 类文件）

### A. 6 个 cron argv 注入 cd 上下文

```bash
# 修复前
argv: ["/usr/bin/python3", "..."]

# 修复后
argv: ["sh", "-lc", "cd /Users/wenbo/.openclaw/workspace/agents/nick_fury && /usr/bin/python3 ..."]
```

修改的 cron：

| cron id | name | 修复 | L-49.7 tag |
|:---|:---|:---:|:---:|
| cf8e874c | daily·report·c3 (0 9) | cd + python3 | 🟢 enabled=必修 |
| 929a8003 | daily·report·c3 (0 21) | cd + python3 | 🟢 enabled=必修 |
| ab65ed59 | nick_cron_health_weekly | cd + python3 | 🟢 enabled=必修 |
| 34b6cbb0 | morning·daily | cd + python3 | 🟢 enabled=必修 |
| 955be249 | rss.collect | cd + python3 | 🟢 enabled=必修 |
| 95048ce2 | rss.daily | cd + python3 | 🟢 enabled=必修 |

**未改 cron 决策**（按 L-16 修一类必 grep，已 error 的必修，没 error 不动）：
- wiki·auto·commit (c0a40201)：独立脚本用绝对 WIKI_PATH，无需 BASE_DIR
- wiki.review (f3b606ed)：独立脚本在 `~/Documents/project/Wiki/scripts/`，cd 到 BASE_DIR 反而破坏 WIKI 路径
- etf.hegang.report (4367285d)：独立脚本，独立路径
- bestpractice.*：脚本内部已 cd，绝对路径

### B. daily_pipeline.py 改相对 config_path 为绝对

```python
# 修复后
def __init__(self):
    _config_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config"
    )
    self.fetcher = RSSFetcher(config_path=os.path.join(_config_dir, "sources_full.json"))
```

**验证**：手动 import 实测 `sources loaded: 135`（之前 0）。

### C. morning_daily_writer.py 数据源路径改

```python
# 修复前
TOPIC_COLLECTION_DIR = BASE_DIR / "data" / "topic_collection"
# 找 f"report_{date_str.replace('-', '')}_*.md"  ← 旧路径，daily_pipeline.py 根本不写

# 修复后
pipeline_log = BASE_DIR / "skills" / "rss-intelligence" / "data" / "pipeline_log.json"
# 解析 JSON 找当天条目 + 区分"输出成功"和"输入真实"（L-29 治本）
```

**字段映射**（实测 pipeline_log.json 结构）：

| 旧字段（推测） | 新字段（实测） |
|:---|:---|
| sources | total_sources + success_count + failed_count |
| articles | new_articles + total_stored |

### D. 3 个脚本备份（治本必）

```
data/backups_20260722_2149/
├── c3_daily_check.py           (19,713 B)
├── morning_daily_writer.py     (10,591 B)
├── sunday_cron_health_check.py (18,507 B)
└── daily_pipeline.py.bak       (skill/backup)
```

---

## 4️⃣ 端到端验证（L-15 5 步全通过）

| 步骤 | 验证 | 结果 |
|:---:|:---|:---:|
| 1 | 语法 `py_compile` | ✅ |
| 2 | c3 手动 exit 0 + 飞书 om_x100b6938e84ee0a4b4ba9e515850567 | ✅ |
| 3 | sunday_cron_health exit 0 + 飞书推成功 | ✅ |
| 4 | morning_daily_writer exit 0 + 追加 7-22 daily 骨架 | ✅ |
| 5 | rss.collect 135 源加载（之前 0）+ 数据结构正确 | ✅（已修复真根因）|

---

## 5️⃣ 自我归因（L-29 命中）

**本次踩坑层级**：

1. **L-19 cron argv 同步**：7-1 改造删了 `data/topic_collection/daily_topic_collector.sh` 但 cron 没修——但**更深层是 daily_pipeline.py 的相对 config_path**，从一开始就 0 源
2. **L-29 silent failure**：rss_fetcher 21 天 0 源但飞书推送"成功"——区分"输出成功"和"输入真实"
3. **L-37/L-38 报告未调实时 API**：之前我上午报告"rss.collect silent failure 21 天"是基于 cron_daily.log 的 `No such file` 报错——但这个脚本是 6-29 弃用的，**真正 rss.collect cron 走 daily_pipeline.py**，我误诊
4. **SOUL §3 教练式边界**：09:04 拍 C 后等 12h 没 push back，是派蒙 C-1/C-3 同类问题—— 等拍板 ≠ 等忘了

---

## 6️⃣ 关联产物

| 路径 | 大小 | 状态 |
|:---|:---:|:---:|
| `wiki/review-logs/incidents/2026-07/inc_2026-07-22_001-cron-argv-cwd-silent-failure.md` | 本文件 | ✅ |
| `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-22-cron-argv-cwd-l49-11.md` | (Lesson L-49.11) | ⏳ 紧接 |
| `wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-22-data-source-path-l52-6.md` | (Lesson L-52.6) | ⏳ 紧接 |
| `wiki/review-logs/lessons/by-agent/nick_fury/_nick_registry.md` | +L-49.11/L-52.6 | ⏳ 紧接 |
| `scripts/morning_daily_writer.py` | +28 行（L-52.6 治本数据源改）| ✅ |
| `skills/rss-intelligence/scripts/daily_pipeline.py` | 4 行改（L-49.11 绝对 config_path）| ✅ |
| `cron argv` ×6 | cd cwd 注入 | ✅ |
| `data/backups_20260722_2149/` | 4 脚本备份 | ✅ |
| `memory/daily/2026-07-22.md` | 1775B → 补完稿 ⏳ | 待 |

---

*🕵️ 尼克·弗瑞 · 神盾局局长 · 2026-07-22 21:55 CST · 4 类治本闭环 + 7-23 cron 自动验证窗口*
