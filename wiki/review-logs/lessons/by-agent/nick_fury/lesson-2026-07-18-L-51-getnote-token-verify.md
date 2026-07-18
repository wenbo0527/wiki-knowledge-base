---
title: Lesson 2026 07 18 L-51 getnote token verify
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, 2026-07, L-51, getnote, api-key]
date: 2026-07-18
---

# L-51: getnote API token 验证族（4 条铁律 · 7-18 闭环）

> **触发**: INC-2026-07-18-009 D 任务闭环
> **关联**: L-18（token 协议）+ L-29（输出≠输入真实）+ L-37（API 实测）

---

## L-51.1 · getnote key 失效判断必须 curl 实测

**踩坑**：
- 早上报告"`code 10004` → key 失效"——**错**
- 文档标记"已废弃"≠key 真失效
- 必须 curl 实测才能下结论

**治本**：
```bash
# 任何 key 失效判断必须 curl 实测
curl -s "https://openapi.biji.com/open/api/v1/resource/knowledge/list" \
  -H "Authorization: Bearer $KEY" \
  -H "X-Client-ID: $CLIENT_ID"
# ✅ success=true → key 有效（不管文档怎么说）
# ❌ 10004 → key 真失效
```

## L-51.2 · getnote key 长度 = 80 字符

**格式**：
```
gk_live_<32 字符>.<64 字符 hash>
   ↑  8       ↑ 32      ↑ 1   ↑ 64
   ============================
        总 80 字符
```

**踩坑**：
- 用户给 `5303951f9c9e01de`（17 字符）—— 缺前缀 + 缺后缀
- 我立即 curl 测试 3 种格式（前缀/全/补全）找到完整 key

**治本**：
- 用户给 key 长度 < 60 → 必问"是不是完整 key？"
- 实测前不写入 `.getnote_env`

## L-51.3 · .getnote_env 丢失必须 600 权限重建

**L-51.3 必查清单**：
1. 写入 2 行（API_KEY + CLIENT_ID）
2. `chmod 600 .getnote_env`
3. `ls -la` 验证权限
4. `python3 -c "from getnote_ej9_to_wiki import load_env; load_env()"` dry-run
5. curl API verify（不能只 load_env 不实际 verify）

## L-51.4 · "key 前缀" vs "完整 key" 必实测 3 种格式

**L-51.4 验证矩阵**：
```python
for KEY in [
    f"gk_live_{prefix}",                    # 仅前缀 + gk_live_
    prefix,                                  # 仅前缀
    f"gk_live_{prefix}.<hash>",              # 完整
]:
    curl ... -H "Authorization: Bearer $KEY"
```

**关联**：INC-2026-07-18-009 D 任务实测揭穿。

---

## L-51 关联族系

```
L-18   token 协议（lark-cli auth login device flow）
L-29   输出成功 ≠ 输入真实
L-32   同步脚本必 raise + 不 hardcode
L-37   API 实测验证
L-51   getnote API key 验证族（7-18）
```

🕵️ 尼克·弗瑞 · 2026-07-18 23:40 CST · L-51 闭环
