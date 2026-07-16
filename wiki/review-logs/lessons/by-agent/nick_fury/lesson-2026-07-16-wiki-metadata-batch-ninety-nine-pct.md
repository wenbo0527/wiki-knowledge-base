# L-43 + L-44: Wiki 批量元数据补全 99% 突破

> **创建时间**：2026-07-16 17:18 CST
> **创建者**：🕵️ 尼克·弗瑞
> **关联 INC**: INC-2026-07-16-003-wiki-metadata-batch-99pct.md
> **路径**: `Wiki/review-logs/lessons/by-agent/nick_fury/lesson-2026-07-16-wiki-metadata-batch-ninety-nine-pct.md`（L-31 路径规范）

---

## 🎯 核心摘要

Wiki 1646 篇文档 4 项元数据（product_domain / author / date / tags）从 **1-2% 跳到 99%**，**一次性超出 Q3 OKR 95% 目标 4 个百分点**（提前 6 周完成 Q3 战役）。

---

## 📚 L-43: 批量元数据补必须"不覆盖"

### 现象

如果批量脚本无脑 `add_field` 会**破坏 5 月已有完整 front-matter 的文档**（如 `local-docs/行业研究/...` 6 字段齐全）。

### 修复

```python
# ❌ 错（覆盖 - 会破坏已有字段）
merged = {**existing, **new_fields}
new_content = build_frontmatter(merged) + body

# ✅ 对（每字段独立判断"是否缺失"）
new_fields = {}
if "title" not in existing:
    new_fields["title"] = guess_title(path)
if "author" not in existing:
    new_fields["author"] = DEFAULT_AUTHOR
# ... 每个字段独立 if not in existing
merged = {**existing, **new_fields}
```

### 验证

apply 后 sample 看 `local-docs/行业研究/2026-05-18-项目-苏银埋点治理.md`：
- 6 字段完全保留（date 仍是 2026-05-18，不是 2026-07-16）
- 脚本**没动任何已有字段**，只"按需补缺失"

### 应用范围

- 任何批量 front-matter 操作（Wiki / Hugo / Jekyll / Quartz）
- 不限于 Wiki
- 适用：批量 update 已有 markdown / JSON / YAML frontmatter
- 反例：不能用于"全量替换"场景（如批量改 author 重新归属）

---

## 📚 L-44: date 字段用 git log 拿最早 commit，不靠 file mtime

### 现象

`file mtime` 是"最后修改时间"，不等于"创建时间"。批量补 date 时如果用 mtime 会把已有文档的 date 全部变成"今天"（2026-07-16），**破坏 2026-03-04 创建的 insight 文档的年代信息**。

### 修复

```python
def get_git_date(path: Path) -> str:
    """优先 earliest commit date，fallback chain 3 级."""
    try:
        # 1️⃣ 最早 commit（diff-filter=A 只匹配 Add 操作）
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%aI", "--",
             str(path.relative_to(WIKI_ROOT))],
            cwd=str(WIKI_ROOT), capture_output=True, text=True, timeout=5
        )
        date = result.stdout.strip().split("\n")[-1] if result.stdout.strip() else ""
        if date:
            return date.split("T")[0]

        # 2️⃣ 兜底：最新 commit（文件至少修改过）
        result2 = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--",
             str(path.relative_to(WIKI_ROOT))],
            cwd=str(WIKI_ROOT), capture_output=True, text=True, timeout=5
        )
        if result2.stdout.strip():
            return result2.stdout.strip().split("T")[0]
    except Exception:
        pass

    # 3️⃣ 终极兜底：文件 mtime
    mtime = path.stat().st_mtime
    return datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
```

### 关键点

- **`--diff-filter=A`**：只匹配 Add 操作（文件首次 commit 时间）
- **`git log ... -- <relative-path>`**：在 WIKI_ROOT cwd 下指定相对路径，避免 `fatal: ambiguous argument` 错误
- **3 级 fallback chain**：earliest commit → latest commit → mtime
- **处理"`git log` 失败"**（不在 git 仓库或文件未跟踪）：直接 fallback 到 mtime

### 验证

apply 后看 `insight-2026-03-04-XXX.md`：
- date 字段 = `2026-03-04`（实际首次 commit 时间）
- 不是 `2026-07-16`（今天）

### 拓展

- 适用于任何 git 仓库（如 Wiki 是 git 仓库）
- 适用于所有需要"创建时间 vs 修改时间"区分的场景
- 注意：mtime 在 git checkout 后会变，要用 git log 才稳

---

## 🛡 L-15 端到端验证全过

按 AGENTS §4.1 + L-15 必 6 步：

| 步 | 项 | 结果 |
|:---:|:---|:---:|
| 1 | 语法 `py_compile` | ✅ |
| 2 | dry-run preview（1631 扫描 → 1626 预测）| ✅ |
| 3 | 真实数据（real Wiki 1646）| ✅ |
| 4 | 异常 raise（试水 0 错误 + 全量 0 错误）| ✅ |
| 5 | INC + lessons（本文件 + INC-003）| ✅ |
| 6 | 24h 验证（按 c3 cron 自动检查）| ⏳ 待 |

## 🔗 关联

- **INC**: `inc_2026-07-16_003-wiki-metadata-batch-99pct.md`
- **OKR**: `projects/knowledge-base/okr-2026-h2-q3.md`（KR7 99% ✅）
- **脚本**: `scripts/wiki_metadata_batch.py`（8863 字节）
- **备份**: `/tmp/wiki_metadata_backup_2026-07-16/`（1626 篇 × 30 天可恢复）
- **Registry**: `_nick_registry.md`（Phase C.2 状态）

---

## 📌 应用 Checklist

下次写批量脚本必做：

- [ ] **L-43**: 每字段独立判断 `if not in existing` + 不覆盖
- [ ] **L-44**: date 用 git log earliest + 3 级 fallback
- [ ] **L-15**: 端到端 6 步（语法 + dry-run + 真实 + 异常 + INC/lessons + 24h）
- [ ] **L-31**: INC/lesson 必写到 `review-logs/` 子目录
- [ ] **L-34**: 必先 grep OpenClaw cron argv + 必同步 edit
- [ ] **L-37**: 报告必调实时 API（不凭印象）

---

*版本: v1.0*
*创建时间: 2026-07-16 17:18 CST*
*🕵️ 尼克·弗瑞*
