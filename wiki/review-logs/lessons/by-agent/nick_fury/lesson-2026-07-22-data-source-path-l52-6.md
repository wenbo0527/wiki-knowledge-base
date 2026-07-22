# L-52.6: 脚本间数据源路径必双向验证（生产端 + 消费端）

> **作者**: 尼克·弗瑞 🕵️
> **创建**: 2026-07-22 21:55 CST
> **关联**: INC-2026-07-22-001
> **L-52 族系位置**: 第 7 层
> **铁律级别**: 🔴 P0 · 必查

---

## 🎯 1 条铁律

**任何"生产端脚本 + 消费端脚本"的数据流组合，必双向验证：**
1. **生产端**：写出的文件路径是？（`grep` 或实际写后验证）
2. **消费端**：读取的路径 = 生产端写出的路径？（不是 supposed =）

---

## 🔥 7-22 真根因（生产端 vs 消费端背离）

| 角色 | 脚本 | 写入/查找路径 | 实测路径 |
|:---|:---|:---|:---|
| **生产端** | `skills/rss-intelligence/scripts/daily_pipeline.py` | `"data/pipeline_log.json"` | `skills/rss-intelligence/data/pipeline_log.json`（cwd 依赖）|
| **消费端** | `scripts/morning_daily_writer.py` | `data/topic_collection/report_*.md` | **❌ 完全不同的路径 + 文件类型** |

**3 处错误并发**：
1. 生产端：相对路径 + 依赖 cwd（治本点 1）
2. 消费端：找错路径 + 文件类型不对（治本点 2）
3. 两端都"看起来跑通"——c3 推送链只管退出码不管数据真假（L-29 命中）

---

## 🪜 3 步诊断流程

任何"消费端找不到数据"问题必走：

```
Step 1: 实查生产端
  - 生产脚本什么时候写的？
  - 写到哪个绝对路径？（不是 supposed to，应该是 ls 看）
  - 文件最近 mtime 是？

Step 2: 实查消费端
  - 消费脚本 grep 找什么路径？
  - 正则 pattern 是什么？
  - glob glob() 出来几个？

Step 3: 双源对比
  - 路径完全一致？
  - 文件类型匹配（.json vs .md）？
  - 字段名匹配？
```

---

## ✅ 修法（7-22 实战沉淀）

### 修法 1：生产端绝对路径

```python
# 7-22 修复
_config_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config"
)
self.fetcher = RSSFetcher(config_path=os.path.join(_config_dir, "sources_full.json"))
```

### 修法 2：消费端找真实路径

```python
# 7-22 修复
pipeline_log = BASE_DIR / "skills" / "rss-intelligence" / "data" / "pipeline_log.json"
log = json.loads(pipeline_log.read_text(encoding="utf-8"))
```

### 修法 3：L-29 字段映射区分"输出成功"和"输入真实"

```python
# 之前
sources, articles = ... # 不知道从哪来

# 修复后（按真实 JSON 字段）
return (
    f"### rss.collect {date_str}\n"
    f"- 新增文章: {fetch.get('new_articles', '?')}\n"
    f"- 总源: {fetch.get('total_sources', '?')}\n"
    f"- 成功: {fetch.get('success_count', '?')}\n"     # ← 真"成功"
    f"- 失败: {fetch.get('failed_count', '?')}\n"
    f"- 状态: {last.get('status', '?')}\n"
)
```

---

## 🚫 反模式

| 反模式 | 后果 |
|:---|:---|
| 凭印象写路径常量 | 7-22 rss.collect 0 源 21 天 |
| 假设生产端写 `.md` 但实际写 `.json` | morning_daily_writer.py "🟡 rss.collect 报告不存在" |
| 消费端不验证文件 mtime | 一直读陈旧数据却以为新鲜 |
| 只看"输出成功"不看"输入真实" | L-29 silent failure |

---

## 📊 L-52.6 在 L-52 族系的位置

```
L-52   派蒙 cron 漂移治本（namespaced 防重名）
L-52.1 ... (族系扩展)
...
L-52.5 cron 上下文 PATH 显式化
L-52.6 脚本间数据源路径必双向验证             ← NEW (7-22) 🆕
```

---

## 🔧 可复用 checklist（任何 cron 上下游改动时）

```bash
# 1. 生产端 grep
cd <PROD_SCRIPT_DIR>
grep -n 'open(\|write_text\|json.dump' *.py | grep -v test_

# 2. 消费端 grep
cd <CONSUME_SCRIPT_DIR>
grep -n 'read_text\|json.load\|Path(' *.py | grep -v test_

# 3. 双源对比（关键！）
echo "生产端路径: /path/to/prod_*.json"
echo "消费端路径: <CONSUME_DIR>/prod_*.json"
diff <(echo 生产端路径) <(echo 消费端路径)  # 必须一致
```

---

## 📈 验证窗口

- **7-23 01:00 rss.collect 自动跑** → 应 sources=135、`pipeline_log.json` 写入 BASE_DIR 相关路径
- **7-23 08:30 morning·daily 自动跑** → 应正确读取 pipeline_log.json + 完稿率上升
- **手动 spot check**：任何 daily 报告里"rss.collect"段不再是"🟡 不存在"

---

*🕵️ 尼克·弗瑞 · L-52 族系第 7 层 · 7-22 创建 · 7-23 验证窗口*
