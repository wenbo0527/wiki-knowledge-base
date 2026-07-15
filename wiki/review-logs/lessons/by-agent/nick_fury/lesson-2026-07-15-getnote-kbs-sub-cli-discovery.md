# L-40: 订阅 KB 必用 `getnote kbs-sub` CLI（HTTP API 不返回）

> **教训族**: INC-2026-07-15-005 治本  
> **类别**: 同步链路 / KB 盘点 / CLI vs API  
> **创建**: 2026-07-15 14:21  
> **关联**: INC-2026-07-15-005 / L-37 / L-32 / L-39

---

## 反例（7-15 14:16 揭穿前）

**3 层错误**：

### 错版 1：HTTP API 只返回自有 KB

```bash
curl -s "https://openapi.biji.com/open/api/v1/resource/knowledge/list" \
  -H "Authorization: $GETNOTE_API_KEY"
# 返回: 8 个 KB（全是 scope=DEFAULT 自有）
```

**缺订阅 KB**：高质量人类谈话库 / 快刀青衣 / 2026 WAIC / 罗振宇 / 脱不花 等

### 错版 2：v1.0 备份信息过时

```python
# scripts/_backup_before_20260701/getnote_to_wiki.py v1.0
HIGH_VALUE_KBS = {
    "9YerORB0": {"name": "人工智能+WAIC", "tag": "ai-research"},
    "2eYxaj0z": {"name": "快刀青衣AI学习笔记", "tag": "ai-learning"},
}
# 实际 7-15 14:16：
# - 9YerORB0 = "人工智能+WAIC" 246 笔记（2025 旧版）
# - JawjeBlY = "2026 WAIC 世界人工智能大会知识库 - 持续更新" 487 笔记（新）
# - 2eYxaj0z 笔记数 1146 → 实测 1258（11 天增量）
```

### 错版 3：v1.0 备份写到 `getnote kbs-sub` 命令但 7-1 改造丢失

```python
# scripts/_backup_before_20260701/getnote_to_wiki.py
def get_all_kbs():
    """获取所有知识库（包括订阅）"""
    import subprocess
    result = subprocess.run(["getnote", "kbs-sub", "--output", "json"], 
                           capture_output=True, text=True, timeout=30)
    return data.get("data", {}).get("topics", [])
# ← 7-1 改造 v2.0 丢失这个功能！
```

## 正例（7-15 14:16 · 揭穿后）

### 同步 KB 必须用 `getnote kbs-sub` 命令

```bash
getnote kbs-sub --output json
# 返回 12 个订阅 KB（含完整 list）
```

**实测 12 KB**（14:16）：
| ID | 名称 | 笔记 |
|:---|:---|:---:|
| **JawjeBlY** | **2026 WAIC** | **487** ⭐⭐ 战略 |
| **2eYxaj0z** | **快刀青衣** | **1,258** ⭐⭐ 战略 |
| 9YerORB0 | 人工智能+WAIC | 246 (2025 旧) |
| 5qY2wG04 | 产品&运营&营销一把抓 | 54 |
| 6n1KzOW0 | 产品大神怎么想 | 105 |
| jnZdRod0 | 千行百业AI落地案例 | 0 |
| vnraxLJm | 脱不花职场沟通宝典 | 25 |
| 40DeN9rJ | 「诺贝尔奖」知识库 | 1,181 |
| jnZwqvY9 | 健康生活方式精选集 | 6,051 |
| L20j3RJg | Get笔记大前端技术精选 | 159 |
| lG0Prnaj | 罗振宇学习笔记 | 528 |

## 治本 SOP（KB 盘点 必检）

### ✅ 必用命令

| 场景 | 命令 | 覆盖 |
|:---|:---|:---|
| **列自有 KB** | `curl /openapi/v1/resource/knowledge/list` | 8 自有 |
| **列订阅 KB** ⭐ | `getnote kbs-sub` | 12 订阅 |
| **完整 KB 列表** ⭐ | `getnote kbs-sub + HTTP API 合并` | 8 + 12 = 20 |
| **实测笔记数** | `curl /notes?topic_id=<id>&page=1` | 单 KB 第 1 页 |

### ❌ 反例

| 错误命令 | 后果 |
|:---|:---|
| 只用 `curl /list` | 漏 12 订阅 KB |
| 只看 v1.0 备份 | 信息过时（WAIC 2026 新 KB 没记录）|
| 不实测笔记数 | 备份数字不准 |

## 关键发现（7-15 14:16）

| 揭穿 | 错版 | 正版 |
|:---|:---|:---|
| WAIC 2026 真实 ID | 9YerORB0 (2025 旧 246) | **JawjeBlY (487 持续更新)** |
| 快刀青衣笔记数 | 1,146 (v1.0 备份) | **1,258** (实测) |
| GET 笔记 KB 总数 | 8 自有 | **20** (8 自有 + 12 订阅) |
| 同步 KB 数 | 9 (含 EJ9zwkln 1 订阅) | **11** (8 自有 + 3 订阅战略) |

## 关联教训

- **L-32** (同步脚本 3 必检) — KB_ROUTING 完整
- **L-37** (报告必 verify 实时 API + 完整分类) — 揭穿报告错版
- **L-38** (Agent 数量必用 openclaw agents list) — 类似必用 API/CLI
- **L-39** (本地文档 RAG 化 4 步 SOP) — 同样必 verify
- **L-40** (订阅 KB 必用 `getnote kbs-sub`) — **本条**

## 预防机制

| 周期 | 动作 | 工具 |
|:---:|:---|:---|
| 每次报告 KB 数量 | `getnote kbs-sub + HTTP API 合并` | 必检 |
| 每周日 c3 cron | KB 列表对账（含订阅）| c3 cron 升级 |
| scripts 改造前 | `grep KB_ROUTING` 看当前 + `getnote kbs-sub` 看最新 | 手动 |

---

*Lesson 完稿: 2026-07-15 14:21 CST*
*沉淀: 尼克·弗瑞 🕵️*
*关联: INC-2026-07-15-005 ✅ 11 KB 端到端 · 战略 3 KB 同步*
