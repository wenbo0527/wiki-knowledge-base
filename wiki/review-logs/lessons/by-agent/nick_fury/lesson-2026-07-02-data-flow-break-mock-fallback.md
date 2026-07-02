# Lesson: 数据流断裂 + Mock Fallback 双重故障（L-24）

> **触发 INC**: INC-2026-07-02-003
> **发现时间**: 2026-07-02 18:21（agent 自报）
> **闭环时间**: 2026-07-02 20:42（73 分钟）
> **沉淀时间**: 2026-07-02 20:45

---

## 现象

每日情报推送内容 100% 是 mock 数据（seangoedecke.com 5 篇，collection 里 0 篇）。

---

## 根因（双重）

1. **数据流断裂**：`intelligence.json` 是空 list（RSS collection 没回流）
2. **Mock Fallback 不 raise**：`push_today_v7.py` 的 `search_with_browser()` 返回硬编码 mock 数据，不报错

---

## 教训

### L-24.1: mock fallback 不能黙黙通过

**原则**：任何"主源 0 → fallback mock"的设计，**必须 raise**，不能用 mock 顶替。

| 维度 | 反例（mock 黙默通过） | 正例（raise） |
|:---|:---|:---|
| 主源 0 篇时 | `search_with_browser()` 返回 mock | `raise RuntimeError(...)` |
| 用户感知 | 看到 fake 推送，信任源污染 | 看到明确错误，知道有 bug |
| 修复路径 | 推送正常跑，bug 隐蔽 | 推送跳过，bug 显式上报 |

**L-17 教训的延伸**：L-17 说"0 篇必须 raise"—— push_today_v7.py 没用 → INC-003。

---

### L-24.2: 数据流必须有 end-to-end 验证

**原则**：每次 RSS 抓取后必校验 `collection 总数 == intelligence.json 总数`。

**当前漏洞**：collection 7-1 有 90 篇 → intelligence.json 0 条 → **没人发现**。

**预防**：
- 加 `data_flow_check.py` 每日 cron 校验
- 或在 RSS 抓取脚本末尾加断言 `len(intelligence_articles) >= 1`

---

### L-24.3: agent 自报问题 = 黄金信号

**正面案例**：cron run agent 完成后**自己报告** "走 mock 浏览器搜索补充（假数据）"。

**为什么能发现**：
- agent 主动暴露了 fix 记录
- 不是被外部检测或用户投诉发现
- 18:21 当天就能捕获

**预防**：
- 保留 agent 修复报告链路（不要被"已完成"消息掩盖问题细节）
- "fix 记录"应该作为 agent run 标准输出的一部分

---

### L-24.4: 信任源验证（Nick 情报分析师特有）

**原则**：作为情报分析师，**每日情报推送内容必须抽样验证**。

**失职**：5-25 之后我（Nick）没抽检 daily brief 内容真实性。

**预防**：
- 每日推送后跑 `grep URL` 验证文章能从 RSS collection 找到
- 或加 `verify_push.py` 每日 cron 抽样 1-2 篇

---

## 复用代码

**scripts/lib/lark_cli_wrapper.py** 已沉淀的 raise 模式（lark-cli preflight）：
```python
def preflight():
    if user_status not in ("ready", "needs_refresh"):
        return False, f"lark-cli user identity 状态异常: status={user_status}"
    return True, ...
```

**push_today_v7.py 已加 raise**：
```python
if need_search_supplement:
    raise RuntimeError(
        f"🔴 RSS 内容不足 {len(top_articles)} 篇（需 ≥3 篇）\n"
        f"   不会调用 mock fallback 填充。"
        ...
    )
```

---

## 验证清单（写新情报推送脚本前必过）

- [ ] **L-24.1**: 主源 0 时是 raise 不是 mock fallback？
- [ ] **L-24.2**: 数据流 end-to-end 验证（collection → analyzer）？
- [ ] **L-24.3**: agent 推送时有 fix 报告机制？
- [ ] **L-24.4**: 推送后抽样验证（URL 在 collection 里能找到）？

---

## 关联

- INC-2026-07-02-003（本次事件）
- L-17（"0 篇必须 raise"教训 · 7-1 daily_tech_report.py 已用 · push_today_v7.py 没贯彻）
- L-19（用户主动询问 = 兜底信号）
- L-15（端到端验证铁律）

---

*沉淀者: 尼克·弗瑞 🕵️*
*验证状态: ✅ B raise 通过 + A cron 暂停*
*治本 TODO: intelligence.json 数据流修复 + 5-25~7-1 推送审计*
*下次审计: 7-5（周日）*