---
title: lesson 2026 06 23 launchd plist repair
author: 尼克·弗瑞 🕵️
product_domain: PD-OPS
doc_type: 其他
tags: [review-logs, lessons, by-agent]
date: 2026-06-30
---

# Lesson: launchd plist 重复 EnvironmentVariables 修复模式

> 来源: INC-2026-06-23-001
> 作者: nick_fury
> 日期: 2026-06-23 09:13
> 状态: ✅ Validated（11/12 修复成功）

---

## 问题模式

macOS launchd plist 中**重复定义同一个 key**（典型：`<key>EnvironmentVariables</key>` 出现 2 次）会导致 launchd 解析失败或字段失效，表现为：

- `launchctl list` 显示 PID `-` + 状态 `78`
- 任务被 launchd 调度但立即 PermissionError 退出
- 实际以默认用户（root 或 launchd 上下文用户）运行，对 `/Users/wenbo/...` 路径无写权限

**典型错误结构**：

```xml
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.task</string>
    ...
    <key>EnvironmentVariables</key>  <!-- 第一个块 -->
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin</string>
    </dict>
    <key>UserName</key>
    <string>wenbo</string>
    <key>EnvironmentVariables</key>  <!-- 重复！launchd 会拒绝或部分失效 -->
    <dict>
        <key>UMASK</key>
        <string>022</string>
    </dict>
</dict>
</plist>
```

**正确结构**：

```xml
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.task</string>
    ...
    <key>UserName</key>
    <string>wenbo</string>
    <key>EnvironmentVariables</key>  <!-- 单一字典 -->
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin</string>
        <key>UMASK</key>
        <string>022</string>
    </dict>
</dict>
</plist>
```

---

## 修复流程（4 步）

### Step 1: 诊断

```bash
# 列出所有 PermissionError (78) plist
launchctl list | grep " 78 "

# 验证 plist 是否重复 EnvironmentVariables
for f in com.nickfury.*.plist; do
  count=$(grep -c "EnvironmentVariables" "$f")
  if [ "$count" -gt 1 ]; then
    echo "🔴 $f: $count 次 EnvironmentVariables（重复）"
  fi
done
```

### Step 2: 备份

```bash
cd ~/Library/LaunchAgents
for f in [需要修复的 plist]; do
  cp "${f}.plist" "${f}.plist.bak.YYYYMMDD"
done
```

### Step 3: 自动修复（推荐用脚本）

```python
# /tmp/fix_launchd_plists.py
import re
import plistlib
from pathlib import Path

def fix_plist(plist_path: Path):
    with open(plist_path, "rb") as f:
        raw = f.read()
    
    # 检测重复 key
    env_count = raw.count(b"<key>EnvironmentVariables</key>")
    if env_count <= 1:
        return False
    
    # 解析所有 EnvironmentVariables 块
    text = raw.decode("utf-8")
    pattern = re.compile(
        r"<key>EnvironmentVariables</key>\s*<dict>(.*?)</dict>",
        re.DOTALL
    )
    matches = pattern.findall(text)
    
    # 合并所有变量
    merged_env = {}
    for match in matches:
        kv_pattern = re.compile(
            r"<key>([^<]+)</key>\s*<string>([^<]*)</string>",
            re.DOTALL
        )
        for k, v in kv_pattern.findall(match):
            merged_env[k] = v
    
    # plistlib 加载并重写
    with open(plist_path, "rb") as f:
        data = plistlib.load(f)
    data["EnvironmentVariables"] = merged_env
    if data.get("UserName") != "wenbo":
        data["UserName"] = "wenbo"
    
    with open(plist_path, "wb") as f:
        plistlib.dump(data, f, sort_keys=False)
    
    return True
```

### Step 4: 重启 launchd

```bash
cd ~/Library/LaunchAgents
for f in [plist 文件名]; do
  launchctl bootout "gui/$(id -u)/${f%.plist}"
  launchctl bootstrap "gui/$(id -u)" "${f}"
done

# 验证
sleep 2
launchctl list | grep "[plist Label]"
```

---

## 验证清单

- [x] 所有 plist 备份到 `.bak.YYYYMMDD`
- [x] 修复后 `grep -c "EnvironmentVariables" [plist]` = 1（单一字典）
- [x] `launchctl list` 状态从 78 → 0
- [x] 24h 后观察自动 cron 跑通并有新数据落盘

---

## 预防机制

1. **新增 plist 时**：使用 plistlib 序列化（Python）或 `defaults write` 命令，避免手工编辑 XML
2. **CI 检查**：可写一个 lint 脚本定期扫描 `~/Library/LaunchAgents/*.plist` 检测重复 key
3. **C-3 cron 自检**：在 21:00 cron 增加 `launchctl list | grep " 78 "` 报警

---

## 相关 INC

- INC-2026-06-15-001（首批 PermissionError，仅修 getnote-wiki-sync）
- **INC-2026-06-23-001**（本 lesson 来源，批量修复 11 个 plist）